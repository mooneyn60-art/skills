#!/usr/bin/env python3
"""Transformation thumbnail for history episodes: a big "before" animal, a red arrow, a comically small
"after" animal, one word of text and a shocked Meatball. The joke is the size gap (wolf -> lap dog), so
the thumbnail adds something the title doesn't say. Bottom-right stays clear for YouTube's timestamp.

Usage: thumb_evo.py OUT.jpg BEFORE.jpg AFTER.jpg [--word "HOW?!"]
"""
import argparse
import math

from PIL import Image, ImageDraw, ImageFont

from mascot import draw
from thumb3 import H, HEAVY, INK, PAPER, RED, W, cutout, sticker


def arrow(d, a, b, bend, width=26):
    """Curved hand-drawn arrow from a to b (quadratic curve) with a white halo, red body and a fat head."""
    (x0, y0), (x1, y1) = a, b
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
           for t in [i / 40 for i in range(41)]]
    ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    head = [(x1 + 70 * math.cos(ang), y1 + 70 * math.sin(ang)),
            (x1 + 60 * math.cos(ang + 2.3), y1 + 60 * math.sin(ang + 2.3)),
            (x1 + 60 * math.cos(ang - 2.3), y1 + 60 * math.sin(ang - 2.3))]
    for w, col in ((width + 18, (255, 255, 255)), (width, RED)):
        d.line(pts, fill=col, width=w, joint="curve")
        d.polygon(head, fill=col, outline=col, width=w - width + 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--word", default="HOW?!")
    a = ap.parse_args()
    c = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(c)

    big = cutout(a.before)
    s = 640 / big.height
    big = sticker(big.resize((int(big.width * s), int(big.height * s)), Image.LANCZOS), edge=12, rim=4)
    c.alpha_composite(big, (-30, H - big.height + 40))

    small = cutout(a.after)
    s = 250 / small.height
    small = sticker(small.resize((int(small.width * s), int(small.height * s)), Image.LANCZOS), edge=10, rim=4)
    sx, sy = 760, 330
    c.alpha_composite(small, (sx, sy))

    arrow(d, (520, 250), (sx + 20, sy + 40), bend=140)

    f = ImageFont.truetype(HEAVY, 210)
    tw = d.textlength(a.word, font=f)
    d.text((W - tw - 50, 10), a.word, font=f, fill=RED, stroke_width=10, stroke_fill=(255, 255, 255))

    m = sticker(draw("shock", 900).crop((120, 80, 880, 1000)).resize((300, 363), Image.LANCZOS), edge=10, rim=4)
    c.alpha_composite(m, (sx + small.width - 30, H - m.height + 60))
    c.convert("RGB").save(a.out, quality=92)
    print("ok", a.out)


if __name__ == "__main__":
    main()
