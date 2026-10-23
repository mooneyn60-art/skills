#!/usr/bin/env python3
"""Myth-list thumbnail (v3), modelled on the niche's breakout channels (Kelevin, What Gives?, Lying Pie;
see research/18-thumbnail-teardown.md): clean white page, "<SUBJECT> ~~FACTS~~ lies" headline with a red
strike-through, 3-4 real animals cut out as stickers each marked with a red X, and a shocked Meatball.

Usage: thumb3.py OUT.jpg PHOTO [PHOTO ...] [--subject ANIMAL] [--crossed FACTS] [--lie lies] [--tag "#1"]
Needs rembg (pip install rembg pymatting pooch opencv-python-headless scikit-image).
"""
import argparse
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from mascot import draw

W, H = 1280, 720
BRAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "fonts")
HEAVY = os.path.join(BRAND, "Anton-Regular.ttf")
HAND = os.path.join(BRAND, "Bangers-Regular.ttf")
INK, RED, PAPER = (17, 17, 17), (222, 22, 30), (250, 248, 242)
_SESSION = None


def cutout(path):
    global _SESSION
    from rembg import new_session, remove
    _SESSION = _SESSION or new_session("isnet-general-use")
    im = Image.open(path).convert("RGB")
    im = ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.12)).enhance(1.3)
    out = remove(im, session=_SESSION)
    # Hard edge: soft matte fringes (fog, water) read as smudges at thumbnail size.
    a = out.split()[3].point(lambda v: 255 if v > 110 else 0)
    # Keep only blobs at least 15% the size of the biggest: drops stray specks the matting leaves behind.
    import cv2
    import numpy as np
    n, lab, stats, _ = cv2.connectedComponentsWithStats(np.array(a), connectivity=8)
    if n > 2:
        areas = stats[1:, cv2.CC_STAT_AREA]
        keep = [i + 1 for i, s in enumerate(areas) if s >= 0.15 * areas.max()]
        a = Image.fromarray(np.isin(lab, keep).astype("uint8") * 255)
    a = a.filter(ImageFilter.GaussianBlur(1))
    out.putalpha(a)
    return out.crop(a.getbbox())


def sticker(im, edge=10, rim=4):
    a = im.split()[3]
    pad = edge + rim + 18
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big = Image.new("L", c.size, 0)
    big.paste(a, (pad, pad))
    white = big.filter(ImageFilter.MaxFilter(edge * 2 + 1))
    black = white.filter(ImageFilter.MaxFilter(rim * 2 + 1))
    c.paste((0, 0, 0, 60), (8, 10), black.filter(ImageFilter.GaussianBlur(8)))
    c.paste(INK + (255,), (0, 0), black)
    c.paste((255, 255, 255, 255), (0, 0), white)
    c.alpha_composite(im, (pad, pad))
    return c


def red_x(size):
    """Hand-drawn-looking red X: two thick strokes with a white halo so it reads on any animal."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    m = size * 0.12
    for wdt, col in ((int(size * 0.32), (255, 255, 255, 255)), (int(size * 0.22), RED + (255,))):
        d.line([(m, m), (size - m, size - m)], fill=col, width=wdt)
        d.line([(size - m, m), (m, size - m)], fill=col, width=wdt)
    return im


def headline(d, subject, crossed, lie, x, y):
    f = ImageFont.truetype(HEAVY, 132)
    d.text((x, y), subject + " ", font=f, fill=INK)
    x2 = x + d.textlength(subject + " ", font=f)
    d.text((x2, y), crossed, font=f, fill=INK)
    cw = d.textlength(crossed, font=f)
    # Strike-through sits on the cap-height middle of the crossed word.
    d.line([(x2 - 10, y + 92), (x2 + cw + 10, y + 82)], fill=RED, width=16)
    g = ImageFont.truetype(HAND, 140)
    d.text((x2 + cw * 0.1, y + 118), lie, font=g, fill=RED, stroke_width=6, stroke_fill=(255, 255, 255))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("photos", nargs="+")
    ap.add_argument("--subject", default="ANIMAL")
    ap.add_argument("--crossed", default="FACTS")
    ap.add_argument("--lie", default="lies")
    ap.add_argument("--tag", default="")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-x", action="store_true", help="no red X stickers (story/history episodes)")
    a = ap.parse_args()
    random.seed(a.seed)

    canvas = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(canvas)
    headline(d, a.subject, a.crossed, a.lie, 40, 10)

    # Collage slots on the right two-thirds; the first photo (the hero myth) gets the biggest slot.
    slots = [(760, 470, 430), (1080, 330, 300), (1090, 590, 270), (520, 600, 230)]
    for path, (cx, cy, size) in list(zip(a.photos, slots))[::-1]:
        im = cutout(path)
        s = size / max(im.width, im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        st = sticker(im).rotate(random.uniform(-6, 6), expand=True, resample=Image.BICUBIC)
        canvas.alpha_composite(st, (int(cx - st.width / 2), int(cy - st.height / 2)))
        if a.no_x:
            continue
        # X overlaps the sticker's top-right corner so it reads as "this one is wrong".
        x = red_x(int(size * 0.38))
        canvas.alpha_composite(x, (int(cx + st.width / 2 - x.width * 1.05), int(cy - st.height / 2 + x.height * 0.05)))

    body = draw("shock", 1150).crop((150, 120, 950, 1000))
    m = sticker(body.resize((470, 517), Image.LANCZOS), edge=12, rim=4)
    canvas.alpha_composite(m, (-40, H - m.height + 70))

    if a.tag:
        t = ImageFont.truetype(HEAVY, 90)
        tw = d.textlength(a.tag, font=t)
        d.rounded_rectangle([W - tw - 70, 20, W - 20, 140], 24, fill=RED)
        d.text((W - tw - 45, 22), a.tag, font=t, fill=(255, 255, 255))
    canvas.convert("RGB").save(a.out, quality=93)
    print("ok", a.out)


if __name__ == "__main__":
    main()
