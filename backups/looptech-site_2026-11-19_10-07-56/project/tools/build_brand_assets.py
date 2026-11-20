"""Derive transparent color variants from the user's raster; no font redrawing."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CROP = (165, 168, 1438, 402)
PALETTES = {
    'dark': ((245, 243, 255), (178, 152, 255)),
    'light': ((11, 7, 26), (101, 69, 255)),
}


def transparent_variant(source, ink, accent):
    pixels = []
    for r, g, b in source.convert('RGB').get_flattened_data():
        deficits = (255 - r, 255 - g, 255 - b)
        purple = deficits[2] < .65 * deficits[1]
        # Median solid foreground in this reference: (15,11,34) / (81,35,242).
        # Recover edge coverage from the white matte; discard paper texture.
        coverage = (max(deficits) - 6) / ((220 if purple else 244) - 6)
        alpha = 0 if coverage < .04 else (255 if coverage >= .96 else round(255 * coverage))
        color = accent if purple else ink
        pixels.append((*color, alpha))
    result = Image.new('RGBA', source.size)
    result.putdata(pixels)
    return result


def main():
    with Image.open(ROOT / 'public/looptech-logo-reference.png') as reference:
        cropped = reference.crop(CROP)
        for theme, (ink, accent) in PALETTES.items():
            logo = transparent_variant(cropped, ink, accent)
            logo.save(ROOT / f'public/looptech-logo-{theme}.png', optimize=True)
        # Same source infinity, without any letters or a white canvas.
        symbol = transparent_variant(reference.crop((286, 213, 572, 355)),
                                     *PALETTES['light'])
        symbol.thumbnail((224, 224), Image.Resampling.LANCZOS)
        icon = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        icon.paste(symbol, ((256 - symbol.width) // 2, (256 - symbol.height) // 2))
        icon.save(ROOT / 'public/looptech-favicon.png', optimize=True)


if __name__ == '__main__':
    main()
