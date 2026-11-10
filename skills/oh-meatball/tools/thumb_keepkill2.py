#!/usr/bin/env python3
"""Thumbnails for "Kill It or Keep It? Part 2" (same rules as Part 1: the creature drives clicks, clean background,
at most 3 words, no Meatball face).   thumb_keepkill2.py OUT_DIR -> thumb_a/b/c.jpg + *_168.jpg"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from thumb_keepkill import backdrop, creature, words, save, W, H  # noqa: E402
import drawn  # noqa: E402
from drawn_species import SPECIES  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

ANT = {"plan": "insect", "label": "carpenter ant", "body": "round", "color": "#1e1a1a", "dark": "#3a3434", "length": 520,
       "height": 190, "leg_len": 140, "ant": 220, "mood": "angry", "s": 0.75}
drawn.ACTORS.setdefault("sp.carpenter_ant", drawn.build(dict(SPECIES.get("carpenter_ant", {}), **ANT)))


def thumb_a(out):   # wolf spider close-up + "DON'T SQUISH IT"
    im = backdrop((14, 52, 38), (36, 120, 78), glow=(90, 140, 70), gx=0.55, gy=0.65)
    im.alpha_composite(creature("wolf_spider", (1120, 540), rot=-8, p={"mood": "happy"}), (80, 185))
    words(im, "DON'T SQUISH IT", (W // 2, 22), 140, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_a")


def thumb_b(out):   # KEEP vs KILL split: wolf spider vs carpenter ant
    left = backdrop((18, 80, 48), (40, 140, 80), glow=(60, 110, 50), gx=0.3, gy=0.6)
    right = backdrop((90, 14, 18), (170, 30, 30), glow=(110, 40, 20), gx=0.7, gy=0.6)
    im = left.copy()
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(700, 0), (W, 0), (W, H), (580, H)], fill=255)
    im.paste(right, (0, 0), mask)
    ImageDraw.Draw(im).line([(700, 0), (580, H)], fill=(255, 255, 255, 255), width=14)
    im.alpha_composite(creature("wolf_spider", (640, 420), rot=-6, p={"mood": "happy"}), (-10, 240))
    im.alpha_composite(creature("sp.carpenter_ant", (560, 380), rot=6, p={"mood": "angry"}), (680, 270))
    words(im, "KEEP", (300, 34), 170, (255, 255, 255, 255), "ma", 14, plate=(47, 170, 80, 255))
    words(im, "KILL", (960, 34), 170, (255, 255, 255, 255), "ma", 14, plate=(220, 40, 40, 255))
    save(im, out, "thumb_b")


def thumb_c(out):   # earwig close-up + "IN YOUR EAR?"
    im = backdrop((20, 16, 30), (60, 40, 70), glow=(120, 80, 40), gx=0.55, gy=0.65)
    im.alpha_composite(creature("sp.earwig", (1200, 460), rot=-6, p={"mood": "smug"}), (50, 250))
    words(im, "IN YOUR EAR?", (W // 2, 22), 150, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_c")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    thumb_a(out)
    thumb_b(out)
    thumb_c(out)
