#!/usr/bin/env python3
"""Thumbnails for "Every Bug in Your House, Ranked From Harmless to Nightmare" (same rules as Kill-or-Keep: the
creature drives clicks, clean background, at most 3 words, no Meatball face).
thumb_ranked.py OUT_DIR -> thumb_a/b/c.jpg + *_168.jpg"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from thumb_keepkill import backdrop, creature, words, save, W, H  # noqa: E402
from PIL import ImageDraw, ImageFont  # noqa: E402
import drawn  # noqa: E402
from drawn_species import SPECIES  # noqa: E402

CARPET = {"plan": "insect", "label": "carpet beetle", "body": "round", "color": "#6b4f3a", "dark": "#efe4c8",
          "head": "#3a2a20", "length": 400, "height": 230, "leg_len": 90, "ant": 120, "stripes": 3, "wings": "shell",
          "mood": "smug", "s": 0.85}
drawn.ACTORS.setdefault("sp.carpet_beetle", drawn.build(dict(SPECIES.get("carpet_beetle", {}), **CARPET)))

FONT = os.path.join(os.path.dirname(HERE), "brand/fonts/Anton-Regular.ttf")
TIERS = [("HARMLESS", (63, 185, 80)), ("ANNOYING", (167, 201, 87)), ("DAMAGING", (255, 159, 28)),
         ("RISKY", (244, 81, 30)), ("NIGHTMARE", (229, 56, 59))]


def board(im, x0=40, y0=150, w=1200, rh=104, gap=10, lw=300):
    """A tier list: coloured label cells on the left, dark rows to the right."""
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 58)
    rows = []
    for i, (name, col) in enumerate(TIERS):
        y = y0 + i * (rh + gap)
        d.rounded_rectangle((x0, y, x0 + w, y + rh), 14, fill=(40, 36, 52, 255), outline=(12, 12, 12, 255), width=5)
        d.rounded_rectangle((x0, y, x0 + lw, y + rh), 14, fill=col + (255,), outline=(12, 12, 12, 255), width=5)
        d.text((x0 + lw / 2, y + rh / 2), name, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=5,
               stroke_fill=(12, 12, 12, 255))
        rows.append((x0 + lw, y, x0 + w, y + rh))
    return rows


def thumb_a(out):   # tier list, recluse bursting out of NIGHTMARE + "#1 IS WORST"
    im = backdrop((18, 14, 26), (48, 30, 52), glow=(120, 40, 40), gx=0.75, gy=0.8)
    rows = board(im)
    for r, sp in ((0, "house_centipede"), (1, "sp.bed_bug"), (2, "sp.carpet_beetle"), (3, "cockroach")):
        x0, y0, x1, y1 = rows[r]
        im.alpha_composite(creature(sp, (200, int(y1 - y0 - 10)), p={"mood": "happy"}), (int(x0) + 30, int(y0) + 5))
    im.alpha_composite(creature("brown_recluse", (700, 420), rot=-6, p={"mood": "angry"}), (530, 330))
    words(im, "#1 IS WORST", (W // 2 + 120, 10), 120, (255, 214, 10, 255), "ma", 12)
    save(im, out, "thumb_a")


def thumb_b(out):   # brown recluse close-up + "NUMBER ONE?"
    im = backdrop((40, 12, 14), (120, 26, 30), glow=(160, 70, 40), gx=0.55, gy=0.65)
    im.alpha_composite(creature("brown_recluse", (1150, 520), rot=-8, p={"mood": "angry"}), (70, 190))
    words(im, "NUMBER ONE?", (W // 2, 18), 140, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_b")


def thumb_c(out):   # the twist: house centipede filed under HARMLESS + "HARMLESS?!"
    im = backdrop((14, 52, 38), (36, 120, 78), glow=(90, 140, 70), gx=0.55, gy=0.65)
    im.alpha_composite(creature("house_centipede", (1180, 500), rot=-6, p={"mood": "happy"}), (50, 210))
    words(im, "HARMLESS?!", (W // 2, 18), 150, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_c")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    thumb_a(out)
    thumb_b(out)
    thumb_c(out)
