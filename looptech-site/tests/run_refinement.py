"""Run the real suites against one externally managed server and pair captures."""

import argparse
import json
import subprocess
import sys

from PIL import Image, ImageDraw

from refinement_audit import ROOT, VIEWPORTS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:5173')
    args = parser.parse_args()
    commands = (
        ['tests/test_site.py', '--output', 'artifacts/refinement/regression'],
        ['tests/refinement_audit.py', '--phase', 'after'],
        ['tests/test_vectors.py'],
        ['tests/test_zoom.py'],
    )
    results = []
    for command in commands:
        completed = subprocess.run([sys.executable, *command, '--url', args.url], cwd=ROOT, check=False)
        results.append({'script': command[0], 'exitCode': completed.returncode})

    output = ROOT / 'artifacts/refinement'
    pairs = output / 'comparisons'
    pairs.mkdir(parents=True, exist_ok=True)
    names = [f'viewport-{w}x{h}.png' for w, h in VIEWPORTS]
    names += ['wordmark-1440.png', 'hero-loop-1440.png', 'icons-1440.png', 'about-1440.png', 'contact-1440.png', 'footer-1440.png']
    for name in names:
        with Image.open(output / 'before' / name) as before, Image.open(output / 'after' / name) as after:
            width = max(before.width, after.width)
            image = Image.new('RGB', (width * 2 + 24, max(before.height, after.height) + 42), '#e4dff0')
            draw = ImageDraw.Draw(image)
            draw.text((12, 12), f'ANTES | {name}', fill='#0b071a')
            draw.text((width + 36, 12), f'DEPOIS | {name}', fill='#0b071a')
            image.paste(before, (0, 42))
            image.paste(after, (width + 24, 42))
            image.save(pairs / name)

    report = {'url': args.url, 'suites': results, 'passed': all(result['exitCode'] == 0 for result in results), 'comparisons': len(names)}
    (output / 'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'\nRefinement suites: {sum(r["exitCode"] == 0 for r in results)}/{len(results)} passed; {len(names)} matched comparisons.')
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
