"""Additional accessibility stress tests for the evaluation copy."""

import argparse
import json

from playwright.sync_api import sync_playwright

from refinement_audit import ROOT


def luminance(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + .05) / (dark + .05)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:5180')
    args = parser.parse_args()
    output = ROOT / 'artifacts/editorial/accessibility'
    output.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, passed, detail=None):
        checks.append({'name': name, 'passed': bool(passed), 'detail': detail})
        print(f'{"PASS" if passed else "FAIL"} {name}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel='chrome')
        page = browser.new_page(reduced_motion='reduce')
        for width, height in ((767, 800), (768, 800), (959, 700), (960, 700),
                              (1280, 579), (1280, 580), (959, 699), (959, 700)):
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(args.url)
            page.wait_for_load_state('networkidle')
            data = page.evaluate('''() => {
              const el=document.querySelector('.sidebar');
              const toggle=document.querySelector('.menu-toggle');
              return {collapse:!!toggle.getClientRects().length,
                inert:document.querySelector('.sidebar-body').inert,
                fits:el.scrollHeight<=el.clientHeight+1,
                overflow:document.documentElement.scrollWidth>innerWidth};
            }''')
            expected = width <= 767 or height <= 579 or (width <= 959 and height <= 699)
            check(f'collapse boundary {width}x{height}',
                  data['collapse'] == expected and data['inert'] == expected
                  and data['fits'] and not data['overflow'], data)

        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(args.url)
        page.wait_for_load_state('networkidle')
        page.emulate_media(reduced_motion='no-preference')
        page.locator('.menu-toggle').click()
        page.locator('.nav-link[href="#contato"]').click()
        page.wait_for_function('Math.abs(document.querySelector("#contato").getBoundingClientRect().top - 24) < 2')
        check('normal-motion anchor navigation settles with visible focus',
              page.locator('#contato').evaluate('el => document.activeElement===el')
              and page.locator('.menu-toggle').get_attribute('aria-expanded') == 'false')
        page.emulate_media(reduced_motion='reduce')
        check('reduced motion disables smooth scroll', page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto')

        # Cross both navigation modes while keeping keyboard focus reachable.
        page.goto(args.url)
        page.wait_for_load_state('networkidle')
        page.locator('.menu-toggle').focus()
        page.set_viewport_size({'width': 1280, 'height': 720})
        page.wait_for_function('document.activeElement.classList.contains("nav-link")')
        check('resize into desktop moves focus from hidden toggle to navigation',
              page.locator('.menu-toggle').is_hidden())
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_function('document.activeElement.classList.contains("menu-toggle")')
        check('resize into disclosure returns visible focus', page.locator('.menu-toggle').is_visible())

        page.set_viewport_size({'width': 320, 'height': 568})
        page.goto(args.url)
        page.wait_for_load_state('networkidle')
        page.add_style_tag(content='''* {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p {margin-bottom:2em!important}''')
        spacing = page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,
          form:document.querySelector('#contact-form').getBoundingClientRect().width,
          labels:[...document.querySelectorAll('label')].every(el=>el.getClientRects().length)})''')
        check('320px with WCAG text-spacing overrides has no horizontal loss',
              spacing['scroll'] <= spacing['width'] and spacing['labels'] and spacing['form'] > 0, spacing)
        page.screenshot(path=str(output / 'text-spacing-320.png'), full_page=True)

        # Derived from the actual refined control CSS, not an assumed palette value.
        colors = page.locator('#name').evaluate('''el => ({border:getComputedStyle(el).borderColor,
          background:getComputedStyle(el).backgroundColor})''')
        def rgb_hex(value):
            values = value[value.index('(') + 1:value.index(')')].split(',')
            return '#' + ''.join(f'{int(v.strip()):02x}' for v in values[:3])
        boundary = contrast(rgb_hex(colors['border']), rgb_hex(colors['background']))
        check('input boundary contrast at least 3:1', boundary >= 3, boundary)

        no_js = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
        plain = no_js.new_page()
        plain.goto(args.url)
        check('all five navigation links remain available without JavaScript',
              plain.locator('.nav-link:visible').count() == 5)
        check('no-JS briefing submission remains disabled', plain.locator('button[type="submit"]').is_disabled())
        no_js.close()
        browser.close()

    report = {'url': args.url, 'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks)}
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if report['passed'] != report['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
