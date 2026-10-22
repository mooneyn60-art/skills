#!/usr/bin/env python3
"""Explainer thumbnail: shocked Meatball + real photo + 2-line headline with a red punch word.

Usage: myth_thumb.py PHOTO OUT.jpg "LINE ONE" "RED LINE" [--pose shock]
"""
import argparse

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from mascot import draw

W, H = 1280, 720
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SAUCE = (214, 30, 24)


def fit(d, text, max_w, start):
    size = start
    while d.textlength(text, font=ImageFont.truetype(BOLD, size)) > max_w and size > 40:
        size -= 4
    return ImageFont.truetype(BOLD, size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("line1")
    ap.add_argument("line2")
    ap.add_argument("--pose", default="shock")
    ap.add_argument("--circle", help="x,y,r red ring around the subject's money detail")
    a = ap.parse_args()
    # Photo fills the frame (cover crop), slightly punched up so it pops in the feed.
    ph = Image.open(a.photo).convert("RGB")
    s = max(W / ph.width, H / ph.height)
    ph = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)
    ph = ph.crop(((ph.width - W) // 2, (ph.height - H) // 2, (ph.width - W) // 2 + W, (ph.height - H) // 2 + H))
    from PIL import ImageEnhance
    ph = ImageEnhance.Color(ImageEnhance.Contrast(ph).enhance(1.15)).enhance(1.25)
    canvas = ph.convert("RGBA")
    # Dark gradient on the left keeps the headline readable over any photo.
    grad = Image.new("L", (W, H))
    gd = ImageDraw.Draw(grad)
    for x in range(W):
        gd.line([(x, 0), (x, H)], fill=int(200 * max(0, 1 - x / (W * 0.75))))
    canvas = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), canvas, grad)
    d = ImageDraw.Draw(canvas)
    y = 40
    for text, fill in ((a.line1, (255, 255, 255)), (a.line2, (255, 214, 0))):
        f = fit(d, text, 760, 130)
        d.text((40, y), text, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0))
        y += f.size * 1.12
    if a.circle:
        x, y, r = (int(v) for v in a.circle.split(","))
        for w, col in ((22, (0, 0, 0)), (14, SAUCE)):
            d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=w)
    # Big shocked mascot under the headline, white sticker outline; the photo's subject stays clear on the right.
    m = draw(a.pose, 600)
    halo = m.split()[3].filter(ImageFilter.MaxFilter(25))
    pos = (-90, H - 520)
    canvas.paste((255, 255, 255, 255), pos, halo)
    canvas.alpha_composite(m, pos)
    canvas.convert("RGB").save(a.out, quality=92)
    print("ok", a.out)


if __name__ == "__main__":
    main()
