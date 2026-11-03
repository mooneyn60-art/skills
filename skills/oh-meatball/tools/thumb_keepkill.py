#!/usr/bin/env python3
"""Thumbnails for "Kill It or Keep It? Every Bug in Your House" (Studio 11/3: the creature drives clicks, a close-up
on a clean background, at most 3 words, no Meatball face). Same drawn creatures as the video.

  thumb_keepkill.py OUT_DIR     -> thumb_a.jpg, thumb_b.jpg, thumb_c.jpg (1280x720) + *_168.jpg previews
"""
import math
import os
import sys

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_keepkill  # noqa: E402  (registers the actors at 16:9)
import drawn  # noqa: E402

W, H = 1280, 720
FONT = drawn_keepkill.FONT


def backdrop(c0, c1, glow=None, gx=0.62, gy=0.55):
    y = np.linspace(0, 1, H)[:, None, None]
    x = np.linspace(0, 1, W)[None, :, None]
    a, b = np.array(c0, float), np.array(c1, float)
    im = a + (b - a) * (0.55 * y + 0.45 * x)
    if glow:
        d = np.sqrt(((x - gx) * 1.6) ** 2 + (y - gy) ** 2)
        im = im + np.array(glow, float) * np.clip(1 - d / 0.62, 0, 1)[..., :1] ** 1.6
    return Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).convert("RGBA")


def creature(spec, box, rot=0.0, p=None):
    """The drawn creature, alone, fitted to box (w, h) px, as an RGBA image with a soft shadow."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, box[0], box[1])
    ctx = cairo.Context(surf)
    rec = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
    c = cairo.Context(rec)
    drawn.ACTORS[spec](c, 0.3, dict({"look": [0.6, 0.2], "walk": 0.0}, **(p or {})))
    x, y, w, h = rec.ink_extents()
    ctx.translate(box[0] / 2, box[1] / 2)
    ctx.rotate(math.radians(rot))
    k = min(box[0] / w, box[1] / h) * (0.98 if not rot else 0.9)
    ctx.scale(k, k)
    ctx.translate(-(x + w / 2), -(y + h / 2))
    ctx.set_source_surface(rec, 0, 0)
    ctx.paint()
    surf.flush()
    a = np.ndarray((box[1], box[0], 4), np.uint8, surf.get_data()).copy()
    al = a[..., 3:4].astype(np.float32)
    rgb = np.where(al > 0, a[..., [2, 1, 0]] * 255.0 / np.maximum(al, 1), 0)
    im = Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), al], 2).astype(np.uint8), "RGBA")
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.55)).filter(ImageFilter.GaussianBlur(14)))
    out = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
    out.alpha_composite(sh, (30, 34))
    out.alpha_composite(im, (14, 14))
    return out


def words(im, text, xy, px, fill, anchor="la", stroke=12, rot=0, plate=None):
    f = ImageFont.truetype(FONT, px)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    pad = 26 if plate else 0
    t = Image.new("RGBA", (x1 - x0 + 2 * pad + 8, y1 - y0 + 2 * pad + 8), (0, 0, 0, 0))
    dr = ImageDraw.Draw(t)
    if plate:
        dr.rounded_rectangle((0, 0, t.width - 1, t.height - 1), 26, fill=plate, outline=(17, 17, 17, 255), width=8)
    dr.text((pad + 4 - x0, pad + 4 - y0), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(10, 10, 10, 255))
    if rot:
        t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    x, y = xy
    if anchor == "ma":
        x -= t.width // 2
    elif anchor == "ra":
        x -= t.width
    im.alpha_composite(t, (int(x), int(y)))


def save(im, out, name):
    im = im.convert("RGB")
    im.save(os.path.join(out, name + ".jpg"), quality=92)
    im.resize((168, 94), Image.LANCZOS).save(os.path.join(out, name + "_168.jpg"), quality=92)


def thumb_a(out):   # house centipede close-up + "DON'T KILL IT"
    im = backdrop((14, 52, 38), (36, 120, 78), glow=(90, 140, 70), gx=0.62, gy=0.62)
    im.alpha_composite(creature("house_centipede", (1180, 560), rot=-14, p={"mood": "happy", "lunge": 0.4}), (90, 175))
    words(im, "DON'T KILL IT", (W // 2, 26), 150, (255, 214, 10, 255), "ma", 14)
    save(im, out, "thumb_a")


def thumb_b(out):   # KEEP vs KILL split: house centipede vs bed bug
    left = backdrop((18, 80, 48), (40, 140, 80), glow=(60, 110, 50), gx=0.3, gy=0.6)
    right = backdrop((90, 14, 18), (170, 30, 30), glow=(110, 40, 20), gx=0.7, gy=0.6)
    im = left.copy()
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(700, 0), (W, 0), (W, H), (580, H)], fill=255)
    im.paste(right, (0, 0), mask)
    ImageDraw.Draw(im).line([(700, 0), (580, H)], fill=(255, 255, 255, 255), width=14)
    im.alpha_composite(creature("house_centipede", (640, 420), rot=-10, p={"mood": "happy"}), (-10, 230))
    im.alpha_composite(creature("sp.bed_bug", (520, 400), rot=8, p={"mood": "angry"}), (690, 250))
    words(im, "KEEP", (300, 34), 170, (255, 255, 255, 255), "ma", 14, plate=(47, 170, 80, 255))
    words(im, "KILL", (960, 34), 170, (255, 255, 255, 255), "ma", 14, plate=(220, 40, 40, 255))
    save(im, out, "thumb_b")


def thumb_c(out):   # brown recluse close-up + "KILL IT?"
    im = backdrop((14, 10, 14), (40, 16, 18), glow=(150, 30, 20), gx=0.5, gy=0.62)
    im.alpha_composite(creature("brown_recluse", (1100, 600), rot=0, p={"mood": "angry", "lunge": 1.0}), (110, 130))
    words(im, "KILL IT?", (W // 2, 20), 170, (255, 214, 10, 255), "ma", 15)
    save(im, out, "thumb_c")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    thumb_a(out)
    thumb_b(out)
    thumb_c(out)
    print("thumbs in", out)
