#!/usr/bin/env python3
"""Meatball-system thumbnail (research/42 §2): Meatball huge and cropped at the chest with an extreme
expression, looking AT one cut-out subject (white outline), at most 3 words in Anton, a sauce-orange to
yellow background with a dark vignette, and an optional red arrow. Writes OUT and OUT_168.jpg (feed size).

Usage:
  thumbnail.py --photo inat:381755705 --pose disgust --text "CUBE POOP?" --out x.jpg [--layout left|right]
               [--crop x0,y0,x1,y1] [--flip] [--arrow auto|x1,y1,x2,y2] [--fill 0.88] [--no-rays]

--photo: a local file, or an iNaturalist observation id ("inat:ID" or bare digits); CC0/CC BY only, the
credit is printed and saved as OUT.credit. --crop takes 0-1 fractions of the photo, applied before the
cut-out (zoom onto a face or spider). --layout left = Meatball on the left, subject on the right.
--pose: shock, terror, disgust, smug, or any tools/mascot.py pose name.
Needs rembg (see thumb3.py) for the cut-out.
"""
import argparse
import html
import json
import math
import os
import re
import sys
import tempfile
import urllib.request

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from mascot import draw
from thumb3 import HEAVY, cutout

W, H = 1280, 720
RED = (226, 24, 30)
INK = (17, 17, 17)
ORANGE, YELLOW = (238, 92, 12), (255, 214, 48)
CACHE = os.path.expanduser("~/.cache/meatball-thumbs")
LICENSES = ("cc0", "cc-by")
# Expression -> (mascot pose, mouth override). Hands-on-cheeks reads at 168 px; a hand over the face doesn't.
EXPRESSIONS = {"shock": ("shock", "o"), "terror": ("nervous", "o"), "disgust": ("deadpan", "wobble"),
               "smug": ("deadpan", "smile")}
BANNED = re.compile(r"\b(TRUE|FALSE|QUIZ|TOP\s*\d+|#\d+|\d+/\d+)\b", re.I)


def fetch(spec):
    m = re.fullmatch(r"(?:inat:)?(\d+)", spec)
    if not m:
        return spec, ""
    obs = m.group(1)
    path = f"{CACHE}/inat_{obs}.jpg"
    os.makedirs(CACHE, exist_ok=True)
    o = json.load(urllib.request.urlopen(f"https://api.inaturalist.org/v1/observations/{obs}", timeout=60))
    p = o["results"][0]["photos"][0]
    if p.get("license_code") not in LICENSES:
        sys.exit(f"thumbnail: observation {obs} photo is {p.get('license_code')}; CC0/CC BY only")
    taxon = (o["results"][0].get("taxon") or {}).get("name", "")
    credit = f"{taxon}: {html.unescape(p['attribution'])} — iNaturalist photo {p['id']} (obs {obs})"
    if not os.path.exists(path):
        urllib.request.urlretrieve(p["url"].replace("square", "original"), path)
    return path, credit


def background(subject_x, rays=True):
    """Radial yellow core behind the subject fading to sauce orange, soft rays, dark vignette."""
    yy, xx = H * 0.5, subject_x
    far = math.hypot(max(xx, W - xx), H) * 0.85
    small = Image.new("RGB", (W // 4, H // 4))
    px = small.load()
    for y in range(small.height):
        for x in range(small.width):
            t = min(1.0, math.hypot(x * 4 - xx, y * 4 - yy) / far) ** 1.2
            px[x, y] = tuple(int(YELLOW[i] + (ORANGE[i] - YELLOW[i]) * t) for i in range(3))
    bg = small.resize((W, H), Image.BICUBIC).convert("RGBA")
    if rays:
        r = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(r)
        for k in range(18):
            a0, a1 = math.radians(k * 20), math.radians(k * 20 + 9)
            d.polygon([(xx, yy), (xx + 2000 * math.cos(a0), yy + 2000 * math.sin(a0)),
                       (xx + 2000 * math.cos(a1), yy + 2000 * math.sin(a1))], fill=34)
        glow = Image.new("RGBA", (W, H), (255, 236, 150, 255))
        glow.putalpha(r.filter(ImageFilter.GaussianBlur(3)))
        bg.alpha_composite(glow)
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-W * 0.18, -H * 0.3, W * 1.18, H * 1.3), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGBA", (W, H), (40, 8, 0, 255))
    dark.putalpha(vig.point(lambda v: int((255 - v) * 0.9)))
    bg.alpha_composite(dark)
    return bg


def outline(im, edge=12):
    """White outline plus a soft dark drop shadow, so the cut-out lifts off the warm background."""
    a = im.split()[3]
    pad = edge + 24
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big = Image.new("L", c.size, 0)
    big.paste(a, (pad, pad))
    white = big.filter(ImageFilter.MaxFilter(edge * 2 + 1)).filter(ImageFilter.GaussianBlur(1))
    shadow = white.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55))
    c.paste((30, 6, 0, 255), (6, 10), shadow)
    c.paste((255, 255, 255, 255), (0, 0), white)
    c.alpha_composite(im, (pad, pad))
    return c


def subject(spec, crop, flip):
    path, credit = fetch(spec)
    src = Image.open(path).convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        src = src.crop((int(x0 * src.width), int(y0 * src.height), int(x1 * src.width), int(y1 * src.height)))
    os.makedirs(CACHE, exist_ok=True)
    fd, tmp = tempfile.mkstemp(suffix=".png", dir=CACHE)  # per-run file: parallel runs swapped each other's cutouts
    os.close(fd)
    try:
        src.save(tmp)
        cut = cutout(tmp)
    finally:
        os.remove(tmp)
    if flip:
        cut = cut.transpose(Image.FLIP_LEFT_RIGHT)
    cut = ImageEnhance.Sharpness(cut).enhance(1.4)
    return cut, credit


def meatball(expr, left, size):
    """Head and chest only, gaze on the subject. Returns an RGBA crop about `size` px tall."""
    pose, mouth = EXPRESSIONS.get(expr, (expr, None))
    # Drawn facing right, then mirrored for the right layout so props (sweat drop) stay on the subject side.
    body = draw(pose, 1400, mouth=mouth, look=(14, 3))
    if not left:
        body = body.transpose(Image.FLIP_LEFT_RIGHT)
    # 1000-unit box (x 260-740, y 170-640) scaled by 1.4: hat to mid-chest, hands included.
    m = body.crop((364, 238, 1036, 896))
    s = size / m.height
    m = m.resize((int(m.width * s), size), Image.LANCZOS)
    return outline(m, edge=10)


def red_arrow(c, x1, y1, x2, y2, width=30):
    """Chunky red arrow with a white rim, curving slightly, head at (x2, y2)."""
    mx, my = (x1 + x2) / 2 - (y2 - y1) * 0.2, (y1 + y2) / 2 + (x2 - x1) * 0.2
    ang = math.atan2(y2 - my, x2 - mx)
    hl, hw = width * 2.2, width * 1.5
    bx, by = x2 - hl * math.cos(ang), y2 - hl * math.sin(ang)  # base of the head: the shaft ends here
    pts = [((1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * bx, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * my + t * t * by)
           for t in [i / 24 for i in range(25)]]
    tip = [(x2, y2), (bx + hw * math.sin(ang), by - hw * math.cos(ang)), (bx - hw * math.sin(ang), by + hw * math.cos(ang))]
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.line(pts, fill=255, width=width, joint="curve")
    d.ellipse((x1 - width / 2, y1 - width / 2, x1 + width / 2, y1 + width / 2), fill=255)
    d.polygon(tip, fill=255)
    rim = mask.filter(ImageFilter.MaxFilter(15))
    c.paste((30, 6, 0, 255), (5, 8), rim.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.5)))
    c.paste((255, 255, 255, 255), (0, 0), rim)
    c.paste(RED + (255,), (0, 0), mask)


def headline(c, text, box):
    """At most 3 words, one font, white with a heavy black stroke; 1 line if it fits big, else 2."""
    x0, y0, x1 = box
    d = ImageDraw.Draw(c)
    words = text.split()
    best = None
    for lines in [[text]] + [[" ".join(words[:k]), " ".join(words[k:])] for k in range(1, len(words))]:
        size = 190
        while size > 70:
            f = ImageFont.truetype(HEAVY, size)
            if max(d.textlength(ln, font=f) for ln in lines) <= x1 - x0 and size * 1.0 * len(lines) <= 300:
                break
            size -= 4
        if not best or size > best[0] * (1.0 if len(lines) == 1 else 1.12):
            best = (size, lines)
    size, lines = best
    f = ImageFont.truetype(HEAVY, size)
    y, bottom = y0, y0
    for ln in lines:
        tw = d.textlength(ln, font=f)
        x = x0 + (x1 - x0 - tw) / 2
        d.text((x + 6, y + 9), ln, font=f, fill=(40, 8, 0), stroke_width=12, stroke_fill=(40, 8, 0))
        d.text((x, y), ln, font=f, fill=(255, 255, 255), stroke_width=12, stroke_fill=INK)
        bottom = d.textbbox((x, y), ln, font=f, stroke_width=12)[3]
        y += int(size * 0.98)
    return size, bottom


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--photo", required=True)
    ap.add_argument("--pose", default="shock")
    ap.add_argument("--text", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--layout", choices=("left", "right"), default="left", help="side Meatball is on")
    ap.add_argument("--crop", help="x0,y0,x1,y1 fractions of the photo")
    ap.add_argument("--flip", action="store_true", help="mirror the subject so it faces Meatball")
    ap.add_argument("--arrow", help="auto, or x1,y1,x2,y2 in output pixels")
    ap.add_argument("--fill", type=float, default=0.86, help="subject height as a fraction of the frame")
    ap.add_argument("--no-rays", action="store_true")
    a = ap.parse_args()
    if len(a.text.split()) > 3:
        sys.exit("thumbnail: 3 words max (research/42 §2)")
    if BANNED.search(a.text):
        sys.exit("thumbnail: no quiz/score/countdown text (research/42 §2)")
    left = a.layout == "left"
    crop = [float(v) for v in a.crop.split(",")] if a.crop else None

    cut, credit = subject(a.photo, crop, a.flip)
    # Meatball ~0.9 of the frame tall, pushed part-way off his edge and cropped at the chest by the bottom.
    mb = meatball(a.pose, left, int(H * 0.9))
    mx = -int(mb.width * 0.16) if left else W - mb.width + int(mb.width * 0.16)
    my = H - mb.height + 50
    inner = mx + mb.width * 0.8 if left else mx + mb.width * 0.2  # Meatball's edge facing the subject

    # Words first (own layer) so the subject can be sized to sit under them, not behind them.
    words = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    text_bottom = 0
    if a.text:
        tx0, tx1 = (inner - 20, W - 24) if left else (24, inner + 20)
        _, text_bottom = headline(words, a.text.upper(), (tx0, 14, tx1))

    # Subject zone: everything from Meatball's near edge to the far frame edge. Fit by height, cap by width.
    zone_w = int(W - inner + 60) if left else int(inner + 60)
    room = H + 30 - max(0, text_bottom - 40)
    s = min(min(H * a.fill, room) / cut.height, zone_w / cut.width)
    cut = cut.resize((max(1, int(cut.width * s)), max(1, int(cut.height * s))), Image.LANCZOS)
    st = outline(cut)
    sx = (W - st.width + 24) if left else -24
    sy = H - st.height + 34  # touches the bottom edge: no floating tile (research/37 §3.3 rule 4)
    scx = sx + st.width / 2

    c = background(scx, rays=not a.no_rays)
    c.alpha_composite(st, (int(sx), int(sy)))
    c.alpha_composite(mb, (int(mx), int(my)))
    c.alpha_composite(words)

    if a.arrow:
        if a.arrow == "auto":  # from under the words to just short of the subject's centre of mass
            import numpy as np
            alpha = np.asarray(st.split()[3]) > 128
            ys, xs = np.nonzero(alpha)
            cx, cy = sx + xs.mean(), sy + ys.mean()
            x1 = ((tx0 + tx1) / 2 if a.text else scx) + (-80 if left else 80)
            y1 = (text_bottom + 20) if a.text else 40
            dist = math.hypot(cx - x1, cy - y1) or 1
            k = max(0.0, (dist - 70) / dist)
            red_arrow(c, x1, y1, x1 + (cx - x1) * k, y1 + (cy - y1) * k)
        else:
            red_arrow(c, *[float(v) for v in a.arrow.split(",")])

    out = c.convert("RGB")
    out.save(a.out, quality=93)
    prev = a.out.rsplit(".", 1)[0] + "_168.jpg"
    out.resize((168, 94), Image.LANCZOS).save(prev, quality=92)
    if credit:
        open(a.out.rsplit(".", 1)[0] + ".credit", "w").write(credit + "\n")
    print(f"ok {a.out} preview={prev}" + (f"\ncredit: {credit}" if credit else ""))


if __name__ == "__main__":
    main()
