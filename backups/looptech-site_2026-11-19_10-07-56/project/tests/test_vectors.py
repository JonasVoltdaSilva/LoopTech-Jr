"""Raster evidence for the actual reusable vector: continuity, holes and safe edges."""

import argparse
import io
import json
from collections import deque

from PIL import Image
from playwright.sync_api import sync_playwright

from refinement_audit import ROOT


def components(mask, width, height, target, diagonal=False):
    seen, groups = set(), []
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    if diagonal:
        steps += ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for y in range(height):
        for x in range(width):
            if (x, y) in seen or mask[y * width + x] != target:
                continue
            queue, size, touches_edge = deque([(x, y)]), 0, False
            seen.add((x, y))
            while queue:
                px, py = queue.popleft()
                size += 1
                touches_edge |= px in (0, width - 1) or py in (0, height - 1)
                for dx, dy in steps:
                    nx, ny = px + dx, py + dy
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen and mask[ny * width + nx] == target:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            groups.append({'pixels': size, 'touchesEdge': touches_edge})
    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:5173')
    parser.add_argument('--output', default='artifacts/refinement/vectors')
    args = parser.parse_args()
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    checks, cases = [], []

    def check(name, passed, evidence=None):
        checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})
        print(f'{"PASS" if passed else "FAIL"} {name}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel='chrome')
        for density in (1, 2):
            context = browser.new_context(viewport={'width': 1200, 'height': 1100}, device_scale_factor=density, reduced_motion='reduce')
            page = context.new_page()
            page.goto(args.url)
            page.wait_for_load_state('networkidle')
            page.evaluate('document.fonts.ready')
            if density == 1:
                metadata = page.evaluate("""() => {
                  const symbol = document.querySelector('#brand-loop');
                  const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
                  return {path:symbol.querySelector('path').getAttribute('d'),
                    transform:symbol.querySelector('path').getAttribute('transform'),
                    paths:symbol.querySelectorAll('path').length,
                    masks:document.querySelectorAll('mask, clipPath').length,
                    duplicateIds:ids.filter((id,i) => ids.indexOf(id) !== i),
                    counters:document.querySelectorAll('.hero-infinity path').length,
                    wordmarks:[...document.querySelectorAll('.wordmark img')].map(u => u.getAttribute('src')),
                    icons:[...document.querySelectorAll('.values-strip .icon')].map(e => ({
                      stroke:getComputedStyle(e).strokeWidth, symbol:e.querySelector('use').getAttribute('href')
                    }))};
                }""")
                check('one path, no separator overlay or masks', metadata['paths'] == 1 and metadata['masks'] == 0 and metadata['counters'] == 0, metadata)
                check('no duplicate SVG IDs', not metadata['duplicateIds'])
                check('same supplied shape with dark/light variants; no obsolete vector signature',
                      metadata['wordmarks'] == ['/looptech-logo-dark.png'] * 2 + ['/looptech-logo-light.png']
                      and page.locator('#looptech-wordmark').count() == 0)
                check('accessible brand names are exactly LoopTech Jr.', page.get_by_role('link', name='LoopTech Jr.', exact=True).count() == 2)
                check('consistent Lucide canvas stroke', all(icon['stroke'] == '2px' for icon in metadata['icons']))
                check('favicon uses the supplied-artwork derivative, not the decorative vector',
                      page.locator('link[rel="icon"]').get_attribute('href') == '/looptech-favicon.png')

            # Isolated proof sheet references the live site's existing definitions.
            # No implementation asset or screenshot is used as a replacement image.
            page.evaluate("""() => {
              document.querySelector('header').hidden = true;
              document.querySelector('main').hidden = true;
              const proof = document.createElement('div');
              proof.id = 'vector-proof';
              proof.style.cssText = 'display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:24px;background:#eee9fb';
              for (const size of [36,128,520]) for (const theme of ['light','dark']) {
                const cell = document.createElement('div');
                cell.style.cssText = 'padding:14px;min-width:0;background:' + (theme==='light' ? '#f5f3ff' : '#0b071a');
                cell.innerHTML = `<p style="color:${theme==='light'?'#0b071a':'#f5f3ff'};font-size:12px">${size} px / ${theme}</p><svg data-proof="${size}-${theme}" width="${size}" height="${size/2}" viewBox="0 0 128 64" preserveAspectRatio="xMidYMid meet" fill="none" stroke="${theme==='light'?'url(#looptech-ribbon)':'#ffffff'}" style="display:block"><use href="#brand-loop" /></svg>`;
                proof.append(cell);
              }
              document.body.append(proof);
            }""")
            page.locator('#vector-proof').screenshot(path=str(output / f'proof-dpr-{density}.png'))
            for size in (36, 128, 520):
                for theme in ('light', 'dark'):
                    png = page.locator(f'[data-proof="{size}-{theme}"]').screenshot()
                    image = Image.open(io.BytesIO(png)).convert('RGB')
                    width, height = image.size
                    mask = [int((b - r > 30 and g < 235) if theme == 'light' else (r > 180 and g > 180 and b > 180)) for r, g, b in image.get_flattened_data()]
                    painted = components(mask, width, height, 1, diagonal=True)
                    holes = [group for group in components(mask, width, height, 0) if not group['touchesEdge'] and group['pixels'] >= 2]
                    case = {'size': size, 'theme': theme, 'dpr': density, 'components': painted, 'holes': holes}
                    cases.append(case)
                    check(f'continuous shape and two natural holes: {size}px {theme} DPR{density}', len(painted) == 1 and len(holes) == 2, case)
                    if size >= 128:
                        check(f'paint has safe edge clearance: {size}px {theme} DPR{density}', not any(group['touchesEdge'] for group in painted))
            context.close()
        browser.close()

    report = {'method': 'Screenshot pixel topology: 8-connected paint, 4-connected counters; supported by source/visual inspection, not an exhaustive vector quality certification.', 'checks': checks, 'cases': cases}
    report['passed'] = sum(c['passed'] for c in checks)
    report['total'] = len(checks)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{report["passed"]}/{report["total"]} vector checks passed')
    if report['passed'] != report['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
