"""Native Chromium tab zoom, not CSS zoom or viewport-resizing equivalence."""

import argparse
import base64
import io
import json
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

from refinement_audit import MEASURE, ROOT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:5173')
    parser.add_argument('--executable', default=str(Path.home() / 'AppData/Local/ms-playwright/chromium-1248/chrome-win64/chrome.exe'))
    args = parser.parse_args()
    output = ROOT / 'artifacts/refinement/zoom'
    output.mkdir(parents=True, exist_ok=True)
    extension = ROOT / 'tests/zoom-extension'
    results = []

    # Temporary profile means neither the user's Chrome profile nor its zoom changes.
    cache = Path.home() / 'AppData/Local/Temp/opencode'
    with tempfile.TemporaryDirectory(prefix='looptech-zoom-', dir=cache, ignore_cleanup_errors=True) as profile, sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            profile, executable_path=args.executable, headless=True, no_viewport=True,
            reduced_motion='reduce', args=[
                f'--disable-extensions-except={extension}', f'--load-extension={extension}',
                '--window-size=1280,900',
            ],
        )
        worker = context.service_workers[0] if context.service_workers else context.wait_for_event('serviceworker')
        page = context.pages[0]
        page.goto(args.url)
        page.wait_for_load_state('networkidle')
        cdp = context.new_cdp_session(page)
        window = cdp.send('Browser.getWindowForTarget')
        dimensions = page.evaluate('({outerWidth, outerHeight, width:innerWidth, height:innerHeight})')
        cdp.send('Browser.setWindowBounds', {'windowId': window['windowId'], 'bounds': {
            'width': 1280 + dimensions['outerWidth'] - dimensions['width'],
            'height': 720 + dimensions['outerHeight'] - dimensions['height'],
        }})
        page.wait_for_function('innerWidth === 1280 && innerHeight === 720')
        base_dpr = page.evaluate('devicePixelRatio')

        def capture_native(name):
            # Playwright's CSS-pixel clip can crop native-zoom captures. Request
            # the entire physical surface directly, with no emulation or clip.
            shot = cdp.send('Page.captureScreenshot', {'format': 'png', 'fromSurface': True, 'captureBeyondViewport': False})
            data = base64.b64decode(shot['data'])
            (output / name).write_bytes(data)
            return Image.open(io.BytesIO(data)).size

        # Native browser zoom is set through chrome.tabs.setZoom in the test worker.
        # Browser bounds stay fixed; no CDP emulation or CSS zoom is used here.
        for factor in (1, 1.25, 1.5, 2):
            applied = worker.evaluate("""async factor => {
              const tabs = await chrome.tabs.query({active:true, currentWindow:true});
              const id = tabs[0].id;
              await chrome.tabs.setZoom(id, factor);
              return await chrome.tabs.getZoom(id);
            }""", factor)
            page.wait_for_function('(expected) => Math.abs(devicePixelRatio - expected) < .02', arg=base_dpr * factor)
            page.evaluate('window.scrollTo(0,0)')
            page.evaluate('document.fonts.ready')
            data = page.evaluate(MEASURE)
            data['factor'] = factor
            data['nativeZoom'] = applied
            data['checks'] = {
                'native_zoom_confirmed': abs(applied - factor) < .01 and abs(data['viewport']['dpr'] - base_dpr * factor) < .02,
                'no_horizontal_overflow': not data['horizontalOverflow'],
                'no_sidebar_scroller': data['sidebar']['scrollHeight'] <= data['sidebar']['clientHeight'] + 1,
            }
            if data['toggleVisible']:
                page.locator('.menu-toggle').click()
                opened = page.evaluate(MEASURE)
                data['openMenu'] = opened
                data['checks']['all_navigation_retained'] = page.locator('.nav-link:visible').count() == 5
                data['checks']['institution_retained'] = opened['institution'] is not None and opened['cta'] is not None
                data['checks']['menu_is_in_document_flow'] = opened['sidebar']['position'] == 'relative' and opened['navigation']['overflow'] == 'visible'
                capture_native(f'zoom-{int(factor * 100)}-menu.png')
                page.locator('.university').scroll_into_view_if_needed()
                data['checks']['institution_reachable_with_page_scroll'] = page.locator('.university').evaluate('(el) => { const r=el.getBoundingClientRect();return r.top >= 0 && r.bottom <= innerHeight; }')
                capture_native(f'zoom-{int(factor * 100)}-menu-bottom.png')
                page.keyboard.press('Escape')
                data['checks']['escape_restores_focus'] = page.locator('.menu-toggle').evaluate('(e) => document.activeElement === e')
                try:
                    page.wait_for_function('() => { const r=document.querySelector(".menu-toggle").getBoundingClientRect();return r.top >= 0 && r.bottom <= innerHeight; }', timeout=5000)
                except Exception:
                    diagnostic = page.evaluate('() => {const e=document.querySelector(".menu-toggle"),r=e.getBoundingClientRect();return {scrollY,innerHeight,top:r.top,bottom:r.bottom,active:document.activeElement===e,header:document.querySelector(".sidebar").getBoundingClientRect().toJSON()}}')
                    print('Focus diagnostic:', diagnostic)
                    capture_native(f'focus-failure-{int(factor * 100)}.png')
                    raise
                data['checks']['returned_focus_is_visible'] = True
            page.evaluate('window.scrollTo(0,0)')
            page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
            data['checks']['viewport_capture_at_document_top'] = page.evaluate('window.scrollY === 0')
            surface = capture_native(f'zoom-{int(factor * 100)}.png')
            data['screenshotPixels'] = surface
            data['checks']['whole_physical_viewport_captured'] = surface == (1280, 720)
            results.append(data)
            print(f'Native {factor:.0%}: {data["viewport"]}, checks={data["checks"]}')

        context.close()

    report = {'method': 'Native chrome.tabs.setZoom in isolated Chromium, constant physical browser window; not viewport emulation.', 'results': results}
    report['passed'] = all(all(r['checks'].values()) for r in results)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
