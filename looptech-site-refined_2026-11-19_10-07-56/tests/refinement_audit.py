"""Capture matched viewport evidence and assert the refinement's layout contracts."""

import argparse
import json
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = ((1280, 720), (1366, 768), (1440, 900), (1920, 1080),
             (1280, 600), (768, 1024), (390, 844), (320, 568))

MEASURE = """() => {
  const rect = el => {
    if (!el || !el.getClientRects().length) return null;
    const r = el.getBoundingClientRect();
    return {x:r.x, y:r.y, width:r.width, height:r.height, right:r.right, bottom:r.bottom};
  };
  const sidebar = document.querySelector('.sidebar');
  const nav = document.querySelector('#main-navigation');
  const names = [...document.querySelectorAll('.wordmark')].map(el => ({
    text: el.querySelector('.sr-only')?.textContent || el.getAttribute('aria-label'),
    box: rect(el)
  }));
  const loops = [...document.querySelectorAll('.hero-infinity, .sidebar-loop, .about-infinity, .contact-loop, .wordmark svg')].map(svg => {
    const r = rect(svg);
    const clipping = [];
    for (let p = svg.parentElement; p && p !== document.body; p = p.parentElement) {
      const style = getComputedStyle(p), pr = p.getBoundingClientRect();
      if (r && /(hidden|clip|auto|scroll)/.test(style.overflowX + style.overflowY) &&
          (r.x < pr.x - 1 || r.right > pr.right + 1 || r.y < pr.y - 1 || r.bottom > pr.bottom + 1)) {
        clipping.push(p.className.baseVal ?? p.className);
      }
    }
    return {class:svg.getAttribute('class'), box:r, clipping, viewBox:svg.getAttribute('viewBox')};
  });
  return {
    viewport: {width:innerWidth,height:innerHeight,dpr:devicePixelRatio},
    horizontalOverflow:document.documentElement.scrollWidth > innerWidth,
    sidebar:{box:rect(sidebar),clientHeight:sidebar.clientHeight,scrollHeight:sidebar.scrollHeight,
      position:getComputedStyle(sidebar).position,overflow:getComputedStyle(sidebar).overflowY},
    navigation:{box:rect(nav),clientHeight:nav.clientHeight,scrollHeight:nav.scrollHeight,
      overflow:getComputedStyle(nav).overflowY,inert:nav.inert},
    toggleVisible:!!document.querySelector('.menu-toggle').getClientRects().length,
    institution:rect(document.querySelector('.university')),
    cta:rect(document.querySelector('.sidebar-cta')),
    navLinksBox:rect(document.querySelector('.sidebar nav')),
    secondaryBox:rect(document.querySelector('.sidebar-bottom')),
    targets:[...document.querySelectorAll('.nav-link, .sidebar-cta')].map(rect),
    main:rect(document.querySelector('main')),names,loops,
    values:[...document.querySelectorAll('.values-strip > div')].map(el => ({
      text:el.textContent.trim(),box:rect(el),icon:rect(el.querySelector('svg')),
      stroke:getComputedStyle(el.querySelector('svg')).strokeWidth
    }))
  };
}"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=('before', 'after'), required=True)
    parser.add_argument('--url', default='http://127.0.0.1:5180')
    parser.add_argument('--output', default='artifacts/refinement')
    args = parser.parse_args()
    directory = ROOT / args.output / args.phase
    directory.mkdir(parents=True, exist_ok=True)
    if args.phase == 'before':
        if (directory / 'report.json').exists():
            raise SystemExit('Baseline already exists: not overwriting pre-change evidence.')
        for name in ('index.html', 'src/styles.css', 'src/navigation.js', 'public/favicon.svg'):
            target = directory / 'source' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel='chrome')
        page = browser.new_page(reduced_motion='reduce')
        for width, height in VIEWPORTS:
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(args.url)
            page.wait_for_load_state('networkidle')
            page.evaluate('document.fonts.ready')
            metrics = page.evaluate(MEASURE)
            metrics['checks'] = {
                'no_horizontal_overflow': not metrics['horizontalOverflow'],
                'sidebar_not_scrollable': metrics['sidebar']['scrollHeight'] <= metrics['sidebar']['clientHeight'] + 1,
                'main_reserved_space': abs(metrics['main']['x'] - (metrics['sidebar']['box']['width'] if not metrics['toggleVisible'] else 0)) <= 1,
                'values_fit': all(v['box']['right'] <= width + 1 and v['box']['x'] >= -1 for v in metrics['values']),
                'loops_not_clipped_by_ancestors': all(not loop['clipping'] for loop in metrics['loops'] if loop['box']),
                'loops_fit_page_width': all(loop['box']['x'] >= -1 and loop['box']['right'] <= width + 1 for loop in metrics['loops'] if loop['box']),
            }
            if not metrics['toggleVisible']:
                metrics['checks']['institution_in_view'] = metrics['institution'] is not None and metrics['institution']['bottom'] <= height - 4
                metrics['checks']['cta_in_view'] = metrics['cta'] is not None and metrics['cta']['bottom'] <= height - 4
                metrics['checks']['nav_before_cta'] = metrics['navigation']['box']['y'] < metrics['cta']['y']
                metrics['checks']['nav_does_not_overlap_secondary_content'] = metrics['navLinksBox']['bottom'] + 8 <= metrics['secondaryBox']['y']
                metrics['checks']['all_targets_visible_and_comfortable'] = all(target and target['y'] >= 0 and target['bottom'] <= height and target['height'] >= 44 for target in metrics['targets'])
            else:
                page.locator('.menu-toggle').click()
                page.screenshot(path=str(directory / f'menu-{width}x{height}.png'))
                opened = page.evaluate(MEASURE)
                metrics['openMenu'] = opened
                metrics['checks']['secondary_content_retained'] = opened['institution'] is not None and opened['cta'] is not None
                metrics['checks']['no_nested_menu_scroll'] = opened['navigation']['scrollHeight'] <= opened['navigation']['clientHeight'] + 1
                page.keyboard.press('Escape')
                page.evaluate('window.scrollTo(0,0)')

            page.screenshot(path=str(directory / f'viewport-{width}x{height}.png'))
            if (width, height) in ((1440, 900), (390, 844)):
                page.screenshot(path=str(directory / f'full-{width}x{height}.png'), full_page=True)
            results.append(metrics)
            print(f'{width}x{height}: sidebar {metrics["sidebar"]["scrollHeight"]}/{metrics["sidebar"]["clientHeight"]}; checks={metrics["checks"]}')

        page.set_viewport_size({'width': 1440, 'height': 900})
        page.goto(args.url)
        page.wait_for_load_state('networkidle')
        page.evaluate('document.fonts.ready')
        for selector, name in (('.sidebar-heading .wordmark', 'wordmark'), ('.hero-art', 'hero-loop'), ('.values-strip', 'icons'), ('#sobre', 'about'), ('#contato', 'contact'), ('.footer', 'footer')):
            page.locator(selector).screenshot(path=str(directory / f'{name}-1440.png'))
        browser.close()

    report = {'phase': args.phase, 'url': args.url, 'viewports': results}
    report['passed'] = all(all(r['checks'].values()) for r in results)
    (directory / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if args.phase == 'after' and not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
