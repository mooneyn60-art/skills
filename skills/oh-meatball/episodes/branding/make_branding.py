#!/usr/bin/env python3
"""Meatball Investigates channel art (Growth desk, research/51 §2).
banner.jpg 2560x1440: everything that must be read sits in the 1546x423 all-device safe area (centre);
the cork case wall, polaroid cards and red string outside it only show on desktop/TV.
avatar.png 800x800: Meatball's shocked face (same as the old profile, so returning viewers still know him)
on the case-file cork, with a yellow lens ring; reads at 48 px as a circle.
Usage: PYTHONHASHSEED=7 python3 episodes/branding/make_branding.py   (from skills/oh-meatball; the seed fixes the stamp wear)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import investigate as inv  # noqa: E402
from brand import sticker  # noqa: E402

ANTON = os.path.join(HERE, "..", "..", "brand", "fonts", "Anton-Regular.ttf")
RED, YELLOW, INK, CREAM = (215, 30, 35), (255, 214, 10), (17, 17, 17), (250, 246, 236)
MANILA = (236, 205, 140)


def stamp(text, scale):
    color = inv.BLUE if text == "UNSOLVED" else None   # stamp_color reads "SOLVED" as green
    return Image.fromarray(inv.stamp_img(text, color=color, scale=scale))


def card(dr, box, lines, rot_img=None):
    x0, y0, x1, y1 = box
    dr.rectangle([x0 + 8, y0 + 10, x1 + 8, y1 + 10], fill=(0, 0, 0, 90))
    dr.rectangle(box, fill=CREAM + (255,))
    f = ImageFont.truetype(inv.MONO, 34)
    for k, line in enumerate(lines):
        dr.text((x0 + 26, y0 + 60 + k * 52), line, font=f, fill=INK)
    dr.line([(x0 + 20, y0 + 22), (x1 - 20, y0 + 22)], fill=RED + (255,), width=3)


def banner(out):
    W, H = 2560, 1440
    sw, sh = 1546, 423
    sx, sy = (W - sw) // 2, (H - sh) // 2
    bg = inv._cork(W, H, seed=21).convert("RGBA")
    dr = ImageDraw.Draw(bg)
    # Desktop-only wall: case cards + red string, kept well outside the safe area.
    cards = [((150, 180, 700, 470), ["CASE #1", "BERMUDA TRIANGLE", "VERDICT: BUSTED"]),
             ((1860, 160, 2410, 450), ["CASE #19", "MKULTRA", "VERDICT: PROVEN"]),
             ((180, 980, 730, 1270), ["CASE #12", "MARY CELESTE", "VERDICT: UNSOLVED"]),
             ((1830, 990, 2380, 1280), ["CASE #21", "THE EMU WAR", "VERDICT: TRUE"])]
    for box, lines in cards:
        card(dr, box, lines)
    # Pinned at the top centre, above the typed lines; red string links the two top cards across the top edge only.
    pins = [((b[0] + b[2]) // 2, b[1] + 12) for b, _ in cards]
    inv._string(dr, (pins[0][0], 120), (pins[1][0], 100), sag=60)
    inv._string(dr, (pins[0][0], 120), pins[0], sag=0)
    inv._string(dr, (pins[1][0], 100), pins[1], sag=0)
    for x, y in pins + [(pins[0][0], 120), (pins[1][0], 100)]:
        inv._pin(dr, x, y, r=18)
    # Safe-area plate: dark case-file panel so the text reads on every crop.
    plate = Image.new("RGBA", (sw + 40, sh + 20), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.rounded_rectangle([0, 0, sw + 39, sh + 19], 46, fill=(18, 18, 22, 236), outline=MANILA + (255,), width=6)
    bg.alpha_composite(plate.filter(ImageFilter.SMOOTH), (sx - 20, sy - 10))
    m = sticker("point", 520)
    bg.alpha_composite(m, (sx - 40, sy + sh - 500))
    x, right = sx + 440, sx + sw - 40
    title = ImageFont.truetype(ANTON, 168)
    while dr.textlength("MEATBALL INVESTIGATES", font=title) > right - x:
        title = ImageFont.truetype(ANTON, title.size - 4)
    d = ImageDraw.Draw(bg)
    d.text((x, sy + 10), "MEATBALL ", font=title, fill=(255, 255, 255))
    d.text((x + d.textlength("MEATBALL ", font=title), sy + 10), "INVESTIGATES", font=title, fill=YELLOW)
    tag = ImageFont.truetype(inv.font(inv.INTER_BLACK, 10).path, 44)
    d.text((x + 4, sy + 10 + title.size + 18), "Conspiracies, strange history & weird animals.", font=tag,
           fill=(255, 255, 255))
    d.text((x + 4, sy + 10 + title.size + 76), "Every case gets a verdict.", font=tag, fill=MANILA)
    sx2 = x
    for word in ("PROVEN", "BUSTED", "UNSOLVED"):
        s = stamp(word, 0.42)
        bg.alpha_composite(s, (int(sx2), sy + sh - s.height + 6))
        sx2 += s.width + 18
    pill = ImageFont.truetype(inv.font(inv.INTER_BLACK, 10).path, 40)
    label = "NEW CASE EVERY DAY"
    pw = d.textlength(label, font=pill) + 56
    px = right - pw
    py = sy + sh - 96
    if px > sx2 + 10:
        d.rounded_rectangle([px, py, px + pw, py + 74], 37, fill=RED)
        d.text((px + 28, py + 12), label, font=pill, fill=(255, 255, 255))
    bg.convert("RGB").save(f"{out}/banner.jpg", quality=92)
    # Safe-area preview (what a phone shows) for the QA eye.
    bg.convert("RGB").crop((sx, sy, sx + sw, sy + sh)).save(f"{out}/banner_safe_preview.jpg", quality=85)


def avatar(out):
    S = 800
    bg = inv._cork(S, S, seed=5).convert("RGBA")
    d = ImageDraw.Draw(bg)
    d.ellipse([40, 40, S - 40, S - 40], fill=(18, 18, 22, 255))
    d.ellipse([70, 70, S - 70, S - 70], fill=MANILA + (255,))
    m = sticker("shock", 1500, edge=31).crop((300, 160, 1200, 1060)).resize((720, 720), Image.LANCZOS)
    bg.alpha_composite(m, (40, 95))
    # Magnifier ring around one eye: the "investigates" cue that still reads small.
    d = ImageDraw.Draw(bg)
    d.arc([18, 18, S - 18, S - 18], 0, 360, fill=YELLOW + (255,), width=26)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
    out_im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out_im.paste(bg, (0, 0), mask)
    flat = Image.new("RGB", (S, S), RED)
    flat.paste(out_im, (0, 0), out_im)
    flat.save(f"{out}/avatar.png")
    flat.resize((96, 96), Image.LANCZOS).save(f"{out}/avatar_96_preview.png")


if __name__ == "__main__":
    banner(HERE)
    avatar(HERE)
    print("ok", HERE)
