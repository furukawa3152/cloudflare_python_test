"""HERO写真から共有用画像を作る。"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "images" / "web" / "hero.jpg"
OUT = ROOT / "public" / "images" / "web" / "og.jpg"

W, H = 1200, 630
INK = (241, 240, 232)
LIME = (217, 241, 141)
MUTED = (166, 170, 161)
BG = (23, 25, 23)


def crop_center(image: Image.Image) -> Image.Image:
    sw, sh = image.size
    target = W / H
    if sw / sh > target:
        new_w = int(round(sh * target))
        left = (sw - new_w) // 2
        image = image.crop((left, 0, left + new_w, sh))
    else:
        new_h = int(round(sw / target))
        top = (sh - new_h) // 2
        image = image.crop((0, top, sw, top + new_h))
    return image.resize((W, H), Image.Resampling.LANCZOS)


def darken(image: Image.Image) -> Image.Image:
    image = Image.blend(image, Image.new("RGB", image.size, BG), 0.28)
    mask = Image.new("L", (W, H))
    pixels = mask.load()
    for y in range(H):
        for x in range(W):
            left = max(0.0, 1 - x / 780)
            bottom = max(0.0, (y - 250) / 380)
            pixels[x, y] = int(min(1, left * 0.95 + bottom * 0.82) * 230)
    return Image.composite(Image.new("RGB", image.size, BG), image, mask)


def tracked(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, fill, gap: float) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += draw.textlength(char, font=font) + gap


def main() -> None:
    image = darken(crop_center(Image.open(SRC).convert("RGB")))
    draw = ImageDraw.Draw(image)
    ja = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 52, index=0)
    en = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    lead = "ITの力で、"
    accent = "「ちょっと面白く」"
    x, y = 72, 392
    draw.text((x, y), lead, font=ja, fill=INK)
    draw.text((x + draw.textlength(lead, font=ja), y), accent, font=ja, fill=LIME)
    tracked(draw, (x, y + 86), "itaru's portfoliosite", en, MUTED, 1.6)
    image.save(OUT, quality=86, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
