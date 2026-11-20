"""Repair baseline crop provenance without overwriting raw before captures."""

import argparse
import json
import shutil

from PIL import Image
from playwright.sync_api import sync_playwright

from refinement_audit import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:5173')
    args = parser.parse_args()
    before = ROOT / 'artifacts/editorial/before'
    raw = before / 'raw-element-captures'
    raw.mkdir(exist_ok=True)
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel='chrome')
        page = browser.new_page(reduced_motion='reduce')
        for width, height in ((1440, 900), (390, 844), (320, 568)):
            page.set_viewport_size({'width': width, 'height': height})
            page.goto(args.url)
            page.wait_for_load_state('networkidle')
            page.evaluate('document.fonts.ready')
            label = f'{width}x{height}'
            path = before / f'full-{label}.png'
            # Never replace an existing full-page baseline. The 320px proof is
            # supplementary, captured from the unchanged preserved original.
            if not path.exists():
                page.screenshot(path=str(path), full_page=True)
            with Image.open(path) as full:
                for selector, name in (('#servicos', 'services'), ('#projetos', 'projects'),
                                       ('#sobre', 'about'), ('#contato', 'contact')):
                    box = page.locator(selector).bounding_box()
                    target = before / f'{name}-{label}.png'
                    if target.exists() and not (raw / target.name).exists():
                        shutil.copy2(target, raw / target.name)
                    bounds = (round(box['x']), round(box['y']),
                              round(box['x'] + box['width']), round(box['y'] + box['height']))
                    full.crop(bounds).save(target)
                    records.append({'crop': target.name, 'source': path.name, 'bounds': bounds})
        browser.close()
    (before / 'crop-provenance.json').write_text(json.dumps({'url': args.url, 'crops': records}, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
