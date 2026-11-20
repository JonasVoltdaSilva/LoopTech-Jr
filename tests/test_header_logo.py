"""Check all brand signatures against the supplied artwork and shared styling."""

import argparse
import json

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

from refinement_audit import MEASURE, ROOT, VIEWPORTS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:5173')
    parser.add_argument('--output', default='artifacts/brand-transparent')
    args = parser.parse_args()
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
        print(f'{"PASS" if passed else "FAIL"} {name}')

    with Image.open(ROOT / 'public/looptech-logo-reference.png') as reference, \
            Image.open(ROOT / 'public/looptech-logo-dark.png') as dark, \
            Image.open(ROOT / 'public/looptech-logo-light.png') as light:
        crop = reference.crop((165, 168, 1438, 402)).convert('RGB')
        check('dark/light variants have exactly the same silhouette and source dimensions',
              dark.mode == light.mode == 'RGBA' and crop.size == dark.size == light.size
              and ImageChops.difference(dark.getchannel('A'), light.getchannel('A')).getbbox() is None)
        for name, variant, palette in (
                ('dark', dark, {(245, 243, 255), (178, 152, 255)}),
                ('light', light, {(11, 7, 26), (101, 69, 255)})):
            pixels = list(variant.get_flattened_data())
            check(f'only approved site colors, no white matte: {name}',
                  all(pixel[:3] in palette for pixel in pixels if pixel[3]))
            alpha = variant.getchannel('A')
            border = [*alpha.crop((0, 0, variant.width, 1)).get_flattened_data(),
                      *alpha.crop((0, variant.height - 1, variant.width, variant.height)).get_flattened_data(),
                      *alpha.crop((0, 0, 1, variant.height)).get_flattened_data(),
                      *alpha.crop((variant.width - 1, 0, variant.width, variant.height)).get_flattened_data()]
            check(f'outer background completely transparent: {name}', not any(border))
            source_pixels = crop.get_flattened_data()
            check(f'source foreground retained and white holes removed: {name}',
                  all((a > 175 if min(rgb) < 75 else a == 0 if min(rgb) > 248 else True)
                      for rgb, a in zip(source_pixels, alpha.get_flattened_data())))
        symbol = light.crop((121, 45, 407, 187))
        symbol.thumbnail((224, 224), Image.Resampling.LANCZOS)
        expected_icon = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        expected_icon.paste(symbol, ((256 - symbol.width) // 2, (256 - symbol.height) // 2))
        with Image.open(ROOT / 'public/looptech-favicon.png') as icon:
            check('favicon uses the same transparent infinity without distortion',
                  icon.size == expected_icon.size and icon.mode == expected_icon.mode
                  and ImageChops.difference(icon, expected_icon).getbbox() is None)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel='chrome')
        page = browser.new_page(reduced_motion='reduce')
        for width, height in VIEWPORTS:
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(args.url)
            page.wait_for_load_state('networkidle')
            page.evaluate('document.fonts.ready')
            label = f'{width}x{height}'
            applications = (('.sidebar-heading .wordmark', 'header'),
                            ('.about-wordmark', 'about'), ('.footer .wordmark', 'footer'))
            for selector, name in applications:
                logo = page.locator(selector)
                image = logo.locator('img')
                image.scroll_into_view_if_needed()
                image.evaluate('el => el.decode()')
                dimensions = image.evaluate('''el => {
                  const r = el.getBoundingClientRect(), p = el.parentElement.getBoundingClientRect();
                  const s = getComputedStyle(el), parent = getComputedStyle(el.parentElement);
                  return {loaded:el.complete && el.naturalWidth === 1273 && el.naturalHeight === 234,
                    src:el.getAttribute('src'), ratio:r.width/r.height, filter:s.filter,
                    contained:r.x>=p.x-.1 && r.right<=p.right+.1 && r.y>=p.y-.1 && r.bottom<=p.bottom+.1,
                    background:parent.backgroundColor, padding:parent.padding,
                    radius:parent.borderRadius, targetHeight:p.height};
                }''')
                expected_src = '/looptech-logo-light.png' if name == 'footer' else '/looptech-logo-dark.png'
                check(f'correct color variant, proportional and contained: {name} {label}',
                      dimensions['src'] == expected_src
                      and dimensions['loaded'] and dimensions['contained']
                      and abs(dimensions['ratio'] - 1273 / 234) < .02)
                check(f'no background, box, padding or filters: {name} {label}',
                      dimensions['background'] == 'rgba(0, 0, 0, 0)'
                      and dimensions['filter'] == 'none' and dimensions['targetHeight'] >= 44
                      and dimensions['padding'] == '0px' and dimensions['radius'] == '0px')
                logo.screenshot(path=str(output / f'logo-{name}-{label}.png'))
                if (width, height) in ((1440, 900), (390, 844)) and name in ('about', 'footer'):
                    page.locator('.about-art' if name == 'about' else '.footer').screenshot(
                        path=str(output / f'after-{name}-{label}.png'))
            check(f'accessible brand links without duplicates: {label}',
                  page.get_by_role('link', name='LoopTech Jr.', exact=True).count() == 2)
            page.evaluate('window.scrollTo(0,0)')
            metrics = page.evaluate(MEASURE)
            check(f'no horizontal or sidebar overflow: {label}',
                  not metrics['horizontalOverflow']
                  and metrics['sidebar']['scrollHeight'] <= metrics['sidebar']['clientHeight'] + 1)
            if not metrics['toggleVisible']:
                check(f'CTA and institution visible without overlap: {label}',
                      metrics['institution']['bottom'] <= height
                      and metrics['cta']['bottom'] <= height
                      and metrics['navLinksBox']['bottom'] < metrics['secondaryBox']['y'])
            else:
                page.locator('.menu-toggle').click()
                check(f'mobile destinations and institution retained: {label}',
                      page.locator('.nav-link:visible').count() == 5
                      and page.locator('.university').is_visible())
                page.keyboard.press('Escape')
                check(f'escape returns focus: {label}',
                      page.locator('.menu-toggle').evaluate('el => document.activeElement === el'))
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(output / f'after-{label}.png'))
        check('all three signatures use controlled transparent variants, without obsolete signature',
              page.locator('.wordmark img[src="/looptech-logo-dark.png"]').count() == 2
              and page.locator('.wordmark img[src="/looptech-logo-light.png"]').count() == 1
              and page.locator('#looptech-wordmark, .wordmark svg').count() == 0)
        check('decorative hero remains continuous and independent of the raster logo',
              page.locator('.hero-infinity use[href="#brand-loop"]').count() == 1)
        check('browser favicon references the supplied-artwork derivative',
              page.locator('link[rel="icon"]').get_attribute('href') == '/looptech-favicon.png')
        browser.close()

    report = {'url': args.url, 'checks': checks,
              'passed': sum(c['passed'] for c in checks), 'total': len(checks)}
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{report["passed"]}/{report["total"]} checks passed')
    if report['passed'] != report['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
