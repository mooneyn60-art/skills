#!/usr/bin/env python3
"""Wolf-rule long-form thumbnail (OPERATIONS.md "Wolf rule"; checked by tools/thumbcheck.py).
Modelled on "How Wolves Became Dogs" (the best long-form CTR so far): ONE big, sharp, bright subject
filling ~half the frame on a clean light page, one hook (a small "after" cut-out with a red arrow, a red X,
or a red ring on the shocking detail), 1-3 huge words that add to the title, and a small reacting Meatball.

Usage:
  wolf_thumb.py --out X.jpg --title "Video title" --text "PUSHED?!" --hero ov:ID|inat:ID|file
                [--hero-crop x0,y0,x1,y1] [--flip] [--side left|right] [--area 0.52]
                [--second ov:ID|inat:ID|file [--second-crop ...] [--second-flip]] [--hook transformation|contrast|detail]
                [--ring x,y,r] [--xmark x,y,s] [--pose shock|terror|smug|disgust] [--tint r,g,b] [--text-color red|ink]
Writes X.jpg (1280x720), X.json (spec for thumbcheck), X.credit and runs thumbcheck (X_168x4.png to look at).
Photos: CC0 / public domain / CC BY only (iNaturalist via thumbnail.fetch, Openverse ids via ov:ID).
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from thumb3 import HEAVY, cutout
from thumbnail import CACHE, INK, RED, fetch, meatball, outline, red_arrow

W, H = 1280, 720
OK_LICENSES = {"cc0", "pdm", "by"}
UA = {"User-Agent": "MeatballMyths/1.0"}


def photo(spec):
    """Local path, inat:ID, or ov:ID -> (path, credit). Refuses share-alike and no-derivatives licenses."""
    if not spec.startswith("ov:"):
        return fetch(spec)
    oid = spec[3:]
    os.makedirs(CACHE, exist_ok=True)
    meta_p, path = f"{CACHE}/ov_{oid}.json", f"{CACHE}/ov_{oid}.img"
    if not os.path.exists(meta_p):
        req = urllib.request.Request(f"https://api.openverse.org/v1/images/{oid}/", headers=UA)
        json.dump(json.load(urllib.request.urlopen(req, timeout=60)), open(meta_p, "w"))
    m = json.load(open(meta_p))
    if m["license"] not in OK_LICENSES:
        sys.exit(f"wolf_thumb: {spec} is CC {m['license']}; CC0 / PD / CC BY only")
    if not os.path.exists(path):
        req = urllib.request.Request(m["url"], headers=UA)
        open(path, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    lic = "public domain" if m["license"] in ("pdm", "cc0") else f"CC BY {m.get('license_version', '')}".strip()
    credit = f"\"{m['title']}\" by {m.get('creator') or 'unknown'} ({lic}), via {m.get('source')}: {m.get('foreign_landing_url')}"
    return path, credit


def subject(spec, crop, flip):
    path, credit = photo(spec)
    src = Image.open(path).convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        src = src.crop((int(x0 * src.width), int(y0 * src.height), int(x1 * src.width), int(y1 * src.height)))
    tmp = f"{CACHE}/_wolf_{os.getpid()}.png"
    src.save(tmp)
    try:
        cut = cutout(tmp)
    finally:
        os.remove(tmp)
    if flip:
        cut = cut.transpose(Image.FLIP_LEFT_RIGHT)
    # Sharp and bright at feed size: lift shadows, then sharpen.
    rgb, a = cut.convert("RGB"), cut.split()[3]
    lum = np.asarray(rgb.convert("L"))[np.asarray(a) > 128]
    if lum.size and lum.mean() < 105:
        rgb = ImageEnhance.Brightness(rgb).enhance(min(1.6, 110 / max(1.0, lum.mean())))
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.3)
    rgb.putalpha(a)
    return rgb, credit


def page(tint):
    """Clean light page with a faint tint toward the subject's side: the wolf look, no rays, no vignette."""
    c = Image.new("RGB", (W, H), (250, 248, 242))
    if tint:
        g = Image.new("L", (W, H))
        d = ImageDraw.Draw(g)
        for x in range(0, W, 4):
            d.rectangle((x, 0, x + 4, H), fill=int(70 * (1 - x / W)))
        c = Image.composite(Image.new("RGB", (W, H), tint), c, g)
    return c.convert("RGBA")


def headline(c, text, x0, x1, y0, color, max_h=420):
    """1-3 words, as big as fits: one line if the cap height stays >= 150 px, else two lines."""
    d = ImageDraw.Draw(c)
    ws = text.split()
    best = None
    for lines in [[text]] + [[" ".join(ws[:k]), " ".join(ws[k:])] for k in range(1, len(ws))]:
        size = 260
        while size > 90:
            f = ImageFont.truetype(HEAVY, size)
            if max(d.textlength(ln, font=f) for ln in lines) <= x1 - x0 and size * len(lines) * 1.05 <= max_h:
                break
            size -= 4
        if not best or size > best[0] * (1.0 if len(lines) == 1 else 1.25):
            best = (size, lines)
    size, lines = best
    f = ImageFont.truetype(HEAVY, size)
    y, box = y0, [W, H, 0, 0]
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        x = x0 + (x1 - x0 - tw) / 2
        fill = RED if (color == "red" or (len(lines) > 1 and i == len(lines) - 1)) else INK
        d.text((x, y), ln, font=f, fill=fill, stroke_width=10, stroke_fill=(255, 255, 255))
        b = d.textbbox((x, y), ln, font=f, stroke_width=10)
        box = [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
        y += int(size * 0.98)
    cap = f.getbbox("H")[3] - f.getbbox("H")[1]
    return box, cap


def xmark(c, x, y, s):
    d = ImageDraw.Draw(c)
    for w, col in ((s // 3 + 14, (255, 255, 255)), (s // 3, RED)):
        d.line((x - s, y - s, x + s, y + s), fill=col, width=w)
        d.line((x - s, y + s, x + s, y - s), fill=col, width=w)


def ring(c, x, y, r):
    d = ImageDraw.Draw(c)
    for w, col in ((30, (255, 255, 255)), (16, RED)):
        d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=w)


def drop(c, x, y, s):
    """Cartoon water drop (blue, white rim), point up, centred on (x, y), s px tall."""
    d = ImageDraw.Draw(c)
    r = s * 0.32
    cy = y + s * 0.5 - r
    for grow, col in ((10, (255, 255, 255)), (0, (40, 140, 235))):
        d.ellipse((x - r - grow, cy - r - grow, x + r + grow, cy + r + grow), fill=col)
        d.polygon([(x, y - s * 0.5 - grow * 1.6), (x - r * 0.94 - grow, cy - r * 0.3), (x + r * 0.94 + grow, cy - r * 0.3)],
                  fill=col)
    d.ellipse((x - r * 0.45, cy - r * 0.45, x - r * 0.1, cy - r * 0.05), fill=(200, 235, 255))


def alpha_box(im, ox, oy):
    x0, y0, x1, y1 = im.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox()
    return [max(0, ox + x0), max(0, oy + y0), min(W, ox + x1), min(H, oy + y1)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ("--out", "--title", "--text", "--hero"):
        ap.add_argument(k, required=True)
    ap.add_argument("--hero-crop")
    ap.add_argument("--flip", action="store_true")
    ap.add_argument("--side", choices=("left", "right"), default="left", help="side the hero sits on")
    ap.add_argument("--area", type=float, default=0.52, help="hero bounding box as a share of the frame")
    ap.add_argument("--second")
    ap.add_argument("--second-crop")
    ap.add_argument("--second-flip", action="store_true")
    ap.add_argument("--second-h", type=int, default=230)
    ap.add_argument("--hook", choices=("transformation", "contrast", "detail"), required=True)
    ap.add_argument("--ring", help="x,y,r in output px: red ring on the shocking detail")
    ap.add_argument("--xmark", help="x,y,s in output px: red X")
    ap.add_argument("--drop", help="x,y,s in output px: blue water drop (pair with --xmark to cross it out)")
    ap.add_argument("--arrow", help="x1,y1,x2,y2 in output px: red arrow (head at x2,y2)")
    ap.add_argument("--pose", default="shock")
    ap.add_argument("--meatball-h", type=int, default=300, help="Meatball height in px (300 ~ 8%% of the frame)")
    ap.add_argument("--tint", help="r,g,b faint page tint")
    ap.add_argument("--text-color", choices=("red", "ink"), default="red")
    a = ap.parse_args()
    if not 1 <= len(a.text.split()) <= 3:
        sys.exit("wolf_thumb: 1-3 words")
    fr = lambda s: [float(v) for v in s.split(",")] if s else None  # noqa: E731
    left = a.side == "left"

    hero, credit = subject(a.hero, fr(a.hero_crop), a.flip)
    # Scale so the hero's box covers --area of the frame; it may bleed off the bottom/side edge.
    s = (a.area * W * H / (hero.width * hero.height)) ** 0.5
    s = min(s, H * 1.02 / hero.height, W * 0.66 / hero.width) if hero.height * s > H * 1.02 else s
    hero = hero.resize((int(hero.width * s), int(hero.height * s)), Image.LANCZOS)
    st = outline(hero, edge=12)
    pad = (st.width - hero.width) // 2
    hx = -pad - 10 if left else W - st.width + pad + 10
    hy = max(-pad, H - st.height + pad + 20)
    c = page(tuple(int(v) for v in a.tint.split(",")) if a.tint else None)
    c.alpha_composite(st, (hx, hy))
    sbox = alpha_box(hero, hx + pad, hy + pad)
    mask = Image.new("L", (W, H), 0)
    mask.paste(hero.split()[3], (hx + pad, hy + pad))

    free0, free1 = (sbox[2] + 10, W - 24) if left else (24, sbox[0] - 10)
    elements, cutouts, credits = 3, 1, [credit]  # hero + words + Meatball
    sec_box = None
    if a.second:
        sec, c2 = subject(a.second, fr(a.second_crop), a.second_flip)
        k = a.second_h / sec.height
        sec = outline(sec.resize((int(sec.width * k), a.second_h), Image.LANCZOS), edge=10)
        sx = free0 + 20 if left else free1 - sec.width - 20
        sy = H - sec.height - 40
        c.alpha_composite(sec, (sx, sy))
        sec_box = [sx, sy, sx + sec.width, sy + sec.height]
        x1 = sbox[2] - 120 if left else sbox[0] + 120
        red_arrow(c, x1, sy + 10, sx + (10 if left else sec.width - 10), sy + sec.height * 0.35)
        elements, cutouts = elements + 2, 2
        credits.append(c2)
    if a.ring:
        ring(c, *[int(v) for v in a.ring.split(",")])
        elements += 1
    if a.drop:
        drop(c, *[int(v) for v in a.drop.split(",")])
        elements += 1
    if a.arrow:
        red_arrow(c, *[float(v) for v in a.arrow.split(",")])
        elements += 1
    if a.xmark:
        xmark(c, *[int(v) for v in a.xmark.split(",")])
        elements += 1

    tbox, cap = headline(c, a.text.upper(), free0, free1, 6, a.text_color, H - a.meatball_h + 20)
    # Meatball: small reaction in the free corner, never over the words or the hook.
    mb = meatball(a.pose, not left, a.meatball_h)
    mx = W - mb.width + 30 if left else -30
    if sec_box and left:
        mx = max(mx, sec_box[2] - 40)
    if sec_box and not left:
        mx = min(mx, sec_box[0] - mb.width + 40)
    my = H - mb.height + 40
    c.alpha_composite(mb, (mx, my))
    mbox = alpha_box(mb, mx, my)

    out = c.convert("RGB")
    out.save(a.out, quality=92)
    base = a.out.rsplit(".", 1)[0]
    mpath = f"{CACHE}/{os.path.basename(base)}_{abs(hash(os.path.abspath(base))) % 10**8}_mask.png"
    mask.save(mpath)
    open(base + ".credit", "w").write("\n".join(x for x in credits if x) + "\n")
    spec = {"title": a.title, "text": a.text, "hook": a.hook, "subject_box": sbox, "subject_mask": mpath,
            "meatball_box": mbox, "text_box": tbox, "cap_px": cap, "cutouts": cutouts, "elements": elements,
            "credits": [x for x in credits if x]}
    json.dump(spec, open(base + ".json", "w"), indent=1)
    print(f"ok {a.out} {os.path.getsize(a.out) // 1024} KB")
    here = os.path.dirname(os.path.abspath(__file__))
    sys.exit(subprocess.run([sys.executable, os.path.join(here, "thumbcheck.py"), a.out]).returncode)


if __name__ == "__main__":
    main()
