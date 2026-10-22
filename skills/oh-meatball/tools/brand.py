#!/usr/bin/env python3
"""Meatball Myths channel art: banner (2560x1440, text kept in the 1546x423 all-device safe area)
and profile picture (800x800, read as a circle).

Usage: brand.py OUTDIR
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from mascot import draw

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RED, DARK, CREAM, YELLOW, INK = (196, 38, 30), (140, 22, 18), (250, 248, 242), (255, 214, 0), (17, 17, 17)


def sticker(pose, size, edge=21):  # MaxFilter needs an odd size
    m = draw(pose, size)
    out = Image.new("RGBA", m.size)
    out.paste((255, 255, 255, 255), (0, 0), m.split()[3].filter(ImageFilter.MaxFilter(edge)))
    out.alpha_composite(m)
    return out


def background(w, h):
    bg = Image.new("RGBA", (w, h), RED + (255,))
    d = ImageDraw.Draw(bg)
    # Faint "?" pattern: the quiz motif, visible on TV/desktop crops, never competing with the text.
    f = ImageFont.truetype(BOLD, 120)
    for row, y in enumerate(range(-40, h, 170)):
        for x in range(-60 + (row % 2) * 110, w, 220):
            d.text((x, y), "?", font=f, fill=DARK + (255,))
    return bg


def banner(out):
    W, H = 2560, 1440
    sx, sy, sw, sh = (W - 1546) // 2, (H - 423) // 2, 1546, 423
    bg = background(W, H)
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([sx - 20, sy - 10, sx + sw + 20, sy + sh + 10], 60, fill=CREAM + (255,))
    m = sticker("point", 470)
    bg.alpha_composite(m, (sx - 10, sy + sh - 455))
    x, right = sx + 400, sx + sw - 30

    def fit(text, size):
        while d.textlength(text, font=ImageFont.truetype(BOLD, size)) > right - x and size > 30:
            size -= 2
        return ImageFont.truetype(BOLD, size)

    title = fit("MEATBALL MYTHS", 150)
    d.text((x, sy + 30), "MEATBALL ", font=title, fill=INK)
    d.text((x + d.textlength("MEATBALL ", font=title), sy + 30), "MYTHS", font=title, fill=RED)
    pill = ImageFont.truetype(BOLD, 56)
    label = "TRUE OR FALSE?"
    pw = d.textlength(label, font=pill) + 60
    y = sy + 30 + title.size + 30
    d.rounded_rectangle([x, y, x + pw, y + 90], 45, fill=RED)
    d.text((x + 30, y + 12), label, font=pill, fill=(255, 255, 255))
    tag = fit("Everything you know about animals is wrong.", 48)
    d.text((x, y + 115), "Everything you know about animals is wrong.", font=tag, fill=INK)
    bg.convert("RGB").save(f"{out}/banner.jpg", quality=92)


def profile(out):
    S = 800
    bg = background(S, S)
    d = ImageDraw.Draw(bg)
    d.ellipse([60, 60, S - 60, S - 60], fill=CREAM + (255,))
    # Head-and-shoulders crop of the shocked pose: the face is what reads at 48 px.
    m = sticker("shock", 1500, edge=31).crop((300, 160, 1200, 1060)).resize((760, 760), Image.LANCZOS)
    bg.alpha_composite(m, (20, 70))
    bg.convert("RGB").save(f"{out}/profile.png")


if __name__ == "__main__":
    os.makedirs(sys.argv[1], exist_ok=True)
    banner(sys.argv[1])
    profile(sys.argv[1])
    print("ok")
