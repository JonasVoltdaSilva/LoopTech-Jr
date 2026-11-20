"""Matched captures and evidence for the scoped editorial refinement."""

import argparse
import hashlib
import json
from collections import Counter
from html.parser import HTMLParser

from PIL import Image
from playwright.sync_api import sync_playwright

from refinement_audit import MEASURE, ROOT, VIEWPORTS


class TextInventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []

    def handle_data(self, text):
        text = ' '.join(text.split())
        if text:
            self.texts.append(text)


PROTECTED = ('public/looptech-logo-dark.png', 'public/looptech-logo-light.png',
             'public/looptech-favicon.png', 'public/looptech-logo-reference.png',
             'public/fonts/sora-latin-variable.woff2', 'src/brand.css')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--phase', required=True, choices=('before', 'after'))
    args = parser.parse_args()
    base = ROOT / 'artifacts/editorial'
    output = base / args.phase
    output.mkdir(parents=True, exist_ok=True)
    if args.phase == 'before' and (output / 'report.json').exists():
        raise SystemExit('Existing baseline is protected; refusing to overwrite.')
    text = TextInventory()
    text.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    protected = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PROTECTED}
    report = {'phase': args.phase, 'url': args.url, 'text_nodes': text.texts,
              'protected_sha256': protected, 'viewports': [], 'checks': []}

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        print(f'{"PASS" if passed else "FAIL"} {name}')

    if args.phase == 'after':
        before = json.loads((base / 'before/report.json').read_text(encoding='utf-8'))
        missing = list((Counter(before['text_nodes']) - Counter(text.texts)).elements())
        check('all original text nodes retained', not missing, missing)
        check('approved logos, local Sora and logo styling unchanged byte-for-byte',
              protected == before['protected_sha256'])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel='chrome')
        page = browser.new_page(reduced_motion='reduce')
        for width, height in VIEWPORTS:
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(args.url)
            page.wait_for_load_state('networkidle')
            page.evaluate('document.fonts.ready')
            metrics = page.evaluate(MEASURE)
            report['viewports'].append(metrics)
            label = f'{width}x{height}'
            check(f'no horizontal overflow: {label}', not metrics['horizontalOverflow'])
            check(f'no sidebar scroller: {label}',
                  metrics['sidebar']['scrollHeight'] <= metrics['sidebar']['clientHeight'] + 1)
            check(f'loop decorations not clipped: {label}',
                  all(not loop['clipping'] for loop in metrics['loops'] if loop['box']))
            if not metrics['toggleVisible']:
                check(f'CTA and institution fit: {label}',
                      metrics['institution']['bottom'] <= height
                      and metrics['cta']['bottom'] <= height
                      and metrics['navLinksBox']['bottom'] < metrics['secondaryBox']['y'])
            page.screenshot(path=str(output / f'viewport-{label}.png'))
            if (width, height) in ((1440, 900), (390, 844), (320, 568)):
                # Crop the clean full-page surface. Element screenshots can resize
                # the viewport and inadvertently include fixed focus/skip UI.
                boxes = {name: page.locator(selector).bounding_box()
                         for selector, name in (('#servicos', 'services'), ('#projetos', 'projects'),
                                                ('#sobre', 'about'), ('#contato', 'contact'))}
                page.screenshot(path=str(output / f'full-{label}.png'), full_page=True)
                with Image.open(output / f'full-{label}.png') as full:
                    for name, box in boxes.items():
                        bounds = (round(box['x']), round(box['y']),
                                  round(box['x'] + box['width']), round(box['y'] + box['height']))
                        full.crop(bounds).save(output / f'{name}-{label}.png')
        browser.close()

    report['passed'] = all(c['passed'] for c in report['checks'])
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
