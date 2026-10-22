#!/usr/bin/env python3
"""Meatball — the channel's original stick-figure mascot, drawn in code so every frame is identical.

Usage: mascot.py OUTDIR            -> renders every pose to OUTDIR/<pose>.png (+ sheet.png)
       from mascot import draw; draw("point", 600) -> RGBA PIL image
Poses: neutral, point, shock, think, laugh, shrug, facepalm, wave
"""
import math
import os
import sys

from PIL import Image, ImageDraw

INK = (17, 17, 17, 255)
MEAT = (150, 78, 44, 255)
MEAT_DARK = (112, 54, 30, 255)
SHINE = (214, 140, 98, 255)
SAUCE = (196, 38, 30, 255)
PARSLEY = (64, 150, 60, 255)

# Limb end points per pose, in a 1000x1000 canvas. Shoulder (500,560), hip (500,780).
POSES = {
    "neutral":  {"l": [(430, 640), (410, 720)], "r": [(570, 640), (590, 720)], "mouth": "smile", "brow": None},
    "point":    {"l": [(430, 640), (410, 720)], "r": [(640, 520), (770, 460)], "mouth": "talk", "brow": "up"},
    "shock":    {"l": [(390, 520), (380, 420)], "r": [(610, 520), (620, 420)], "mouth": "o", "brow": "up"},
    "think":    {"l": [(430, 640), (410, 720)], "r": [(590, 520), (540, 430)], "mouth": "flat", "brow": "tilt"},
    "laugh":    {"l": [(420, 600), (440, 690)], "r": [(580, 600), (560, 690)], "mouth": "laugh", "brow": "up"},
    "shrug":    {"l": [(400, 560), (360, 500)], "r": [(600, 560), (640, 500)], "mouth": "flat", "brow": "up"},
    "facepalm": {"l": [(430, 640), (410, 720)], "r": [(600, 520), (510, 350)], "mouth": "frown", "brow": None},
    "wave":     {"l": [(430, 640), (410, 720)], "r": [(620, 470), (680, 360)], "mouth": "smile", "brow": None},
}
HEAD_C, HEAD_R = (500, 360), 150


def _line(d, a, b, w=26):
    d.line([a, b], fill=INK, width=w)
    for p in (a, b):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=INK)


def _head(d):
    cx, cy = HEAD_C
    r = HEAD_R
    # Lumpy meatball silhouette: a circle perturbed by a few low-frequency bumps.
    pts = [(cx + (r + 7 * math.sin(5 * t) + 4 * math.sin(9 * t + 1)) * math.cos(t),
            cy + (r + 7 * math.sin(5 * t) + 4 * math.sin(9 * t + 1)) * math.sin(t))
           for t in [i * 2 * math.pi / 180 for i in range(180)]]
    d.polygon(pts, fill=MEAT, outline=INK, width=14)
    for (x, y, s) in [(-70, -60, 16), (60, -85, 12), (85, 30, 18), (-95, 45, 13), (10, 95, 15), (-30, -110, 10)]:
        d.ellipse([cx + x - s, cy + y - s, cx + x + s, cy + y + s], fill=MEAT_DARK)
    d.ellipse([cx - 95, cy - 105, cx - 45, cy - 70], fill=SHINE)
    # Tomato-sauce cap with a parsley fleck: the brand detail.
    d.chord([cx - 120, cy - 175, cx + 120, cy - 40], 200, 340, fill=SAUCE, outline=INK, width=10)
    d.ellipse([cx + 20, cy - 150, cx + 48, cy - 132], fill=PARSLEY, outline=INK, width=4)


def _face(d, mouth, brow):
    cx, cy = HEAD_C
    for ex in (-48, 48):
        d.ellipse([cx + ex - 24, cy - 30, cx + ex + 24, cy + 20], fill=(255, 255, 255, 255), outline=INK, width=6)
        d.ellipse([cx + ex - 11, cy - 12, cx + ex + 11, cy + 10], fill=INK)
    if brow == "up":
        for ex in (-48, 48):
            d.arc([cx + ex - 28, cy - 62, cx + ex + 28, cy - 22], 200, 340, fill=INK, width=9)
    elif brow == "tilt":
        d.line([(cx - 76, cy - 44), (cx - 24, cy - 34)], fill=INK, width=9)
        d.line([(cx + 22, cy - 50), (cx + 76, cy - 58)], fill=INK, width=9)
    my = cy + 62
    if mouth == "smile":
        d.arc([cx - 45, my - 40, cx + 45, my + 20], 20, 160, fill=INK, width=10)
    elif mouth == "talk":
        d.chord([cx - 38, my - 22, cx + 38, my + 30], 0, 180, fill=INK)
    elif mouth == "o":
        d.ellipse([cx - 22, my - 22, cx + 22, my + 30], fill=INK)
    elif mouth == "laugh":
        d.chord([cx - 55, my - 30, cx + 55, my + 45], 0, 180, fill=INK)
        d.chord([cx - 30, my + 5, cx + 30, my + 40], 0, 180, fill=SAUCE)
    elif mouth == "frown":
        d.arc([cx - 40, my, cx + 40, my + 50], 200, 340, fill=INK, width=10)
    else:
        d.line([(cx - 32, my + 6), (cx + 32, my + 6)], fill=INK, width=10)


def draw(pose="neutral", size=600):
    p = POSES[pose]
    im = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sh, hip = (500, 560), (500, 790)
    _line(d, (500, 505), hip)                         # spine
    _line(d, hip, (440, 960)); _line(d, hip, (560, 960))  # legs
    _head(d)
    _face(d, p["mouth"], p["brow"])
    # Arms go on top of the head so hand-to-face poses (shock, facepalm, think) stay visible.
    for side in ("l", "r"):
        elbow, hand = p[side]
        _line(d, sh, elbow); _line(d, elbow, hand)
        d.ellipse([hand[0] - 22, hand[1] - 22, hand[0] + 22, hand[1] + 22], fill=INK)
    return im.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    sheet = Image.new("RGBA", (300 * len(POSES), 340), (255, 255, 255, 255))
    for i, name in enumerate(POSES):
        im = draw(name, 300)
        im.save(f"{out}/{name}.png")
        sheet.alpha_composite(im, (300 * i, 0))
        ImageDraw.Draw(sheet).text((300 * i + 120, 310), name, fill=INK)
    sheet.convert("RGB").save(f"{out}/sheet.png")
    print("ok", out)
