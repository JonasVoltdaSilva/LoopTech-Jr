"""Run the evaluation suites and create matched before/after comparison sheets."""

import argparse
import json
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

from refinement_audit import ROOT, VIEWPORTS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:5181')
    args = parser.parse_args()
    scripts = (
        ('tests/test_site.py', '--output', 'artifacts/editorial/regression'),
        ('tests/test_header_logo.py', '--output', 'artifacts/editorial/brand'),
        ('tests/test_vectors.py', '--output', 'artifacts/editorial/vectors'),
        ('tests/refinement_audit.py', '--phase', 'after', '--output', 'artifacts/editorial/layout'),
        ('tests/test_zoom.py', '--output', 'artifacts/editorial/zoom'),
        ('tests/test_editorial.py',),
        ('tests/editorial_evidence.py', '--phase', 'after'),
    )
    runs = []
    for script in scripts:
        run = subprocess.run([sys.executable, *script, '--url', args.url], cwd=ROOT, check=False)
        runs.append({'script': script[0], 'exitCode': run.returncode})

    directory = ROOT / 'artifacts/editorial'
    pairs = directory / 'comparisons'
    pairs.mkdir(parents=True, exist_ok=True)
    names = [f'viewport-{w}x{h}.png' for w, h in VIEWPORTS]
    names += [f'{section}-{size}.png' for section in ('services', 'projects', 'about', 'contact')
              for size in ('1440x900', '390x844')]
    for name in names:
        with Image.open(directory / 'before' / name) as before, Image.open(directory / 'after' / name) as after:
            width = max(before.width, after.width)
            image = Image.new('RGB', (width * 2 + 24, max(before.height, after.height) + 42), '#e4dff0')
            draw = ImageDraw.Draw(image)
            draw.text((12, 12), 'ANTES | ' + name, fill='#0b071a')
            draw.text((width + 36, 12), 'DEPOIS | ' + name, fill='#0b071a')
            image.paste(before, (0, 42))
            image.paste(after, (width + 24, 42))
            image.save(pairs / name)

    # Reduced overviews are for navigation only; the exact-resolution captures
    # and unscaled matched pairs above remain the fidelity evidence.
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
    for size, target_width in (('1440x900', 540), ('390x844', 260)):
        images = []
        for phase in ('before', 'after'):
            source = Image.open(directory / phase / f'full-{size}.png').convert('RGB')
            source = source.resize((target_width, round(source.height * target_width / source.width)), Image.Resampling.LANCZOS)
            images.append(source)
        sheet = Image.new('RGB', (target_width * 2 + 32, max(i.height for i in images) + 48), '#e4dff0')
        draw = ImageDraw.Draw(sheet)
        draw.text((12, 10), 'ANTES', font=font, fill='#0b071a')
        draw.text((target_width + 44, 10), 'DEPOIS', font=font, fill='#0b071a')
        sheet.paste(images[0], (0, 48))
        sheet.paste(images[1], (target_width + 32, 48))
        sheet.save(pairs / f'overview-{size}.png')

    report = {'url': args.url, 'suites': runs, 'passed': all(r['exitCode'] == 0 for r in runs),
              'unscaled_comparisons': len(names), 'reduced_overviews': 2}
    (directory / 'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'{sum(r["exitCode"] == 0 for r in runs)}/{len(runs)} suites; {len(names)} matched comparisons.')
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
