#!/usr/bin/env python3
"""Thumbnails for "Do You Really Swallow 8 Spiders a Year in Your Sleep?" (house bug stories long-form). Same rules as the
Kill-or-Keep thumbs: the creature drives clicks, clean background, at most 3 words, cartoon not gross.
thumb_myths.py OUT_DIR -> thumb_a/b/c.jpg + *_168.jpg"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from thumb_keepkill import backdrop, creature, words, save, W, H  # noqa: E402
from PIL import ImageDraw, ImageFilter, Image  # noqa: E402


def pillow_scene(im):
    """A night bed: a big soft pillow and a sleeper's 'Zzz', no face (the spider is the subject)."""
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((90, 470, 1010, 760), 140, fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (10, 14))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 450, 1010, 740), 140, fill=(236, 240, 250, 255), outline=(17, 17, 17, 255), width=10)
    d.arc((300, 520, 800, 700), 200, 340, fill=(190, 198, 220, 255), width=8)   # pillow crease
    words(im, "Z", (200, 380), 110, (255, 255, 255, 255), "mm", 10)
    words(im, "z", (130, 300), 80, (255, 255, 255, 255), "mm", 8)
    words(im, "z", (85, 240), 56, (255, 255, 255, 255), "mm", 6)


def spider_on_thread(im, x, y, size):
    d = ImageDraw.Draw(im)
    d.line([(x + size[0] // 2, 0), (x + size[0] // 2, y + size[1] // 3)], fill=(240, 240, 240, 255), width=6)
    im.alpha_composite(creature("jumping_spider", size, rot=0, p={"mood": "smug"}), (x, y))


def thumb_a(out):   # spider dropping onto a pillow + "8 A YEAR?"
    im = backdrop((14, 18, 46), (40, 50, 110), glow=(90, 90, 160), gx=0.45, gy=0.55)
    pillow_scene(im)
    spider_on_thread(im, 300, 205, (600, 420))
    words(im, "8 A YEAR?", (W // 2, 18), 170, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_a")


def thumb_b(out):   # the roach drawn with no head (drawn_anatomy.cockroach "headless": a plain cap, no gore) + "NO HEAD?"
    im = backdrop((40, 14, 10), (120, 40, 24), glow=(170, 90, 40), gx=0.5, gy=0.65)
    im.alpha_composite(creature("cockroach", (1150, 520), rot=-6, p={"mood": "smug", "headless": 1.0}), (60, 200))
    words(im, "NO HEAD?", (W // 2, 22), 160, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_b")


def thumb_c(out):   # the spider crawling over the pillow, close + "IN YOUR MOUTH?" (matches the alternate title)
    im = backdrop((16, 14, 40), (52, 40, 104), glow=(120, 90, 170), gx=0.55, gy=0.6)
    pillow_scene(im)
    im.alpha_composite(creature("jumping_spider", (760, 520), rot=-8, p={"mood": "smug"}), (330, 190))
    words(im, "IN YOUR MOUTH?", (W // 2, 18), 150, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_c")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    thumb_a(out)
    thumb_b(out)
    thumb_c(out)
