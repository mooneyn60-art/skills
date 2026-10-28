#!/usr/bin/env python3
"""Thumbnails v3 (10/28, research/58: long-form CTR 1.2-2.65%): drawn-style thumbnails built ONLY from the channel's
own drawn kit (drawn_bugs / drawn_creatures / drawn_actors / mascot), no photos.

Rules baked in (top animal/science channels): one huge focal subject with a visible face, a big horrified
Meatball, 1-3 huge Anton words that never repeat the title, saturated colour with the subject outlined and
rim-lit off a simple dark background, a curiosity device (pore, magnifier, arrow), nothing important bottom-right
(timestamp), and a series badge top-left so the house series reads as one set.

Usage: thumb_v3.py OUTDIR [--only t1a,t2b,...]
Writes NAME.png (1280x720 or 1080x1920), NAME_168.png / NAME_360.png and preview sheets sheet-*.png.
"""
import argparse
import math
import os
import random
import sys

import cairo
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mascot  # noqa: E402
import drawn_bugs as B  # noqa: E402
from drawn_actors import cellar_spider  # noqa: E402
from drawn_creatures import creature  # noqa: E402
from drawn_species import SPECIES  # noqa: E402

FONTS = os.path.join(HERE, "..", "brand", "fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
W, H = 1280, 720
INK = (17, 17, 17)
YEL = (255, 214, 10)
RED = (232, 36, 30)
WHITE = (255, 255, 255)
BADGER = {"plan": "mammal", "label": "honey badger", "color": "#2a2522", "dark": "#171412", "belly": "#2a2522",
          "length": 560, "height": 240, "leg_len": 90, "leg_w": 36, "ears": "round", "tail": "thin", "tail_w": 14,
          "whiskers": False, "back_stripe": "#d9d5cc", "back_stripe_w": 70, "mood": "angry"}


# ------------------------------------------------------------------ Meatball: a horrified face for thumbnails

_face0 = mascot._face


def _face(pen, cx, cy, mouth, brow, look=(0, 0), level=0, blink=0, eyes=None):
    """eyes="horror": huge whites, pin-prick pupils, brows flung up, a tall screaming mouth with a red tongue."""
    if eyes != "horror":
        return _face0(pen, cx, cy, mouth, brow, look, level, blink, eyes)
    d, box = pen.d, pen.box
    lx, ly = look
    for ex in (-50, 50):
        d.ellipse(box(cx + ex - 34, cy - 44, cx + ex + 34, cy + 26), fill=WHITE, outline=INK, width=pen.w(8))
        d.ellipse(box(cx + ex - 11 + lx, cy - 19 + ly, cx + ex + 11 + lx, cy + 3 + ly), fill=INK)
        d.arc(box(cx + ex - 36, cy - 96, cx + ex + 36, cy - 44), 200, 340, fill=INK, width=pen.w(11))
    my = cy + 52
    d.ellipse(box(cx - 40, my, cx + 40, my + 104), fill=INK)
    d.chord(box(cx - 28, my + 50, cx + 28, my + 100), 180, 360, fill=(196, 38, 30))
    d.rectangle(box(cx - 26, my + 4, cx + 26, my + 18), fill=WHITE)


mascot._face = _face


def meatball(pose="shock", size=900, look=(0, 0), horror=True, sweat=True, head=None):
    """Horrified Meatball, cropped to his drawing. head=0.55 keeps only the top 55% (head, hands, shoulders):
    the big-face crop thumbnails want."""
    st = mascot.pose_state(pose)
    st["look"] = look
    if horror:
        st["eyes"] = "horror"
    im = mascot.render(st, size)
    im = im.crop(im.getbbox())
    k = size / 1000
    pad = int(90 * k)
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + pad), (0, 0, 0, 0))
    c.alpha_composite(im, (pad, pad))
    if sweat:   # two flying sweat drops off the top of the head
        d = ImageDraw.Draw(c)
        hx = c.width / 2
        for sx, sy, r in ((hx + 185 * k, pad + 30 * k, 24 * k), (hx - 195 * k, pad + 60 * k, 19 * k)):
            d.polygon([(sx, sy - 2.4 * r), (sx - r, sy), (sx + r, sy)], fill=(120, 190, 240), outline=INK)
            d.ellipse([sx - r, sy - r * 0.9, sx + r, sy + r * 1.1], fill=(120, 190, 240), outline=INK,
                      width=max(2, int(6 * k)))
    if head:
        c = c.crop((0, 0, c.width, int(pad + im.height * head)))
    return c.crop(c.getbbox())


# ------------------------------------------------------------------ drawn creatures -> PIL

def actor(fn, p, scale, w=2400, h=2000, ox=None, oy=None, t=0.3):
    """Render a drawn-kit actor (ctx, t, p) at `scale` onto a transparent surface; returns the cropped RGBA."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(s)
    c.translate(w / 2 if ox is None else ox, h * 0.8 if oy is None else oy)
    c.scale(scale, scale)
    base = {"phase": 0.0, "walking": False, "blink": 0}
    base.update(p)
    fn(c, t, base)
    s.flush()
    im = Image.frombuffer("RGBA", (w, h), bytes(s.get_data()), "raw", "BGRa", 0, 1)
    return im.crop(im.getbbox())


def sp(name, **p):
    cfg = SPECIES[name] if isinstance(name, str) else name
    return lambda c, t, q: creature(c, t, dict(q, cfg=cfg, **p))


def pop(im, ink=7, rim=7, rim_col=WHITE, glow=26, glow_col=None, glow_a=200):
    """Sticker treatment: thick ink silhouette outline, a coloured rim outside that, and a soft glow, so the
    subject separates from any background at phone size."""
    a = im.split()[3].point(lambda v: 255 if v > 40 else 0)
    pad = ink + rim + glow * 2 + 4
    big = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
    big.paste(a, (pad, pad))
    k1 = big.filter(ImageFilter.MaxFilter(ink * 2 + 1))
    k2 = k1.filter(ImageFilter.MaxFilter(rim * 2 + 1)) if rim else k1
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    if glow:
        g = k2.filter(ImageFilter.GaussianBlur(glow)).point(lambda v: min(255, int(v * glow_a / 255 * 1.6)))
        out.paste(Image.new("RGBA", big.size, (glow_col or rim_col) + (255,)), (0, 0), g)
    if rim:
        out.paste(Image.new("RGBA", big.size, rim_col + (255,)), (0, 0), k2)
    out.paste(Image.new("RGBA", big.size, INK + (255,)), (0, 0), k1)
    out.alpha_composite(im, (pad, pad))
    return out


def fit(im, w=None, h=None):
    s = min(w / im.width if w else 9e9, h / im.height if h else 9e9)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def paste_c(canvas, im, cx, cy, rot=0):
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ------------------------------------------------------------------ backgrounds, text, devices

def radial(w, h, inner, outer, cx=0.5, cy=0.5, r=0.75):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx / w - cx) * (w / h)) ** 2 + (yy / h - cy) ** 2) / r
    d = np.clip(d, 0, 1)[..., None] ** 1.3
    a = np.array(inner, np.float32) * (1 - d) + np.array(outer, np.float32) * d
    return Image.fromarray(a.astype(np.uint8), "RGB").convert("RGBA")


def vignette(canvas, k=0.55):
    w, h = canvas.size
    v = radial(w, h, (255, 255, 255), (int(255 * (1 - k)),) * 3, r=0.9).convert("RGB")
    canvas.paste(ImageChops.multiply(canvas.convert("RGB"), v).convert("RGBA"))


def words(canvas, text, x, y, size, fill=YEL, stroke=None, anchor="la", rot=0, max_w=None, shadow=True):
    """Huge Anton words with a thick ink stroke and a hard drop shadow. Returns the text box."""
    f = ImageFont.truetype(ANTON, size)
    tmp = ImageDraw.Draw(canvas)
    while max_w and tmp.textlength(text, font=f) > max_w and size > 40:
        size -= 4
        f = ImageFont.truetype(ANTON, size)
    sw = stroke or max(6, size // 11)
    l, t, r, b = tmp.textbbox((0, 0), text, font=f, stroke_width=sw)
    lay = Image.new("RGBA", (r - l + 40, b - t + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if shadow:
        d.text((20 - l + sw * 0.6, 20 - t + sw * 0.8), text, font=f, fill=INK, stroke_width=sw, stroke_fill=INK)
    d.text((20 - l, 20 - t), text, font=f, fill=fill, stroke_width=sw, stroke_fill=INK)
    if rot:
        lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    ax = {"l": 0, "m": 0.5, "r": 1}[anchor[0]]
    ay = {"a": 0, "m": 0.5, "b": 1}[anchor[1]]
    px, py = int(x - lay.width * ax), int(y - lay.height * ay)
    canvas.alpha_composite(lay, (px, py))
    return (px, py, px + lay.width, py + lay.height)


def badge(canvas, label, x=18, y=18, h=78, col=YEL, fg=INK, icon="house"):
    """Series badge: a tag with a little ink icon (house | x | mag) and the label (part number or series)."""
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(ANTON, int(h * 0.62))
    tw = d.textlength(label, font=f)
    wbox = int(h * 1.05 + tw + h * 0.35)
    d.rounded_rectangle([x, y, x + wbox, y + h], int(h * 0.22), fill=col, outline=INK, width=max(4, h // 14))
    hx, hy, s = x + h * 0.55, y + h * 0.54, h * 0.3
    if icon == "house":
        d.polygon([(hx - s * 1.25, hy - s * 0.05), (hx, hy - s * 1.25), (hx + s * 1.25, hy - s * 0.05)], fill=fg)
        d.rectangle([hx - s * 0.85, hy - s * 0.1, hx + s * 0.85, hy + s * 1.0], fill=fg)
        d.rectangle([hx - s * 0.25, hy + s * 0.3, hx + s * 0.25, hy + s * 1.0], fill=col)
    elif icon == "x":
        for a, b in (((-1, -1), (1, 1)), ((1, -1), (-1, 1))):
            d.line([(hx + a[0] * s, hy + a[1] * s), (hx + b[0] * s, hy + b[1] * s)], fill=fg, width=int(s * 0.6))
    else:   # magnifier
        d.ellipse([hx - s, hy - s * 1.1, hx + s * 0.6, hy + s * 0.5], outline=fg, width=int(s * 0.4))
        d.line([(hx + s * 0.4, hy + s * 0.3), (hx + s * 1.1, hy + s * 1.0)], fill=fg, width=int(s * 0.5))
    d.text((x + h * 1.05, y + h * 0.5), label, font=f, fill=fg, anchor="lm")


def arrow(canvas, tail, head, col=RED, w=26):
    """Fat hand-drawn arrow with an ink outline, curved slightly."""
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    (x0, y0), (x1, y1) = tail, head
    mx, my = (x0 + x1) / 2 + (y1 - y0) * 0.18, (y0 + y1) / 2 - (x1 - x0) * 0.18
    pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1)
           for u in np.linspace(0, 0.82, 24)]
    ang = math.atan2(y1 - pts[-1][1], x1 - pts[-1][0])
    hl = w * 2.6
    tri = [(x1, y1), (x1 - hl * math.cos(ang - 0.5), y1 - hl * math.sin(ang - 0.5)),
           (x1 - hl * math.cos(ang + 0.5), y1 - hl * math.sin(ang + 0.5))]
    for wd, c in ((w + 14, INK), (w, col)):
        d.line(pts, fill=c, width=wd, joint="curve")
        for q in (pts[0],):
            d.ellipse([q[0] - wd / 2, q[1] - wd / 2, q[0] + wd / 2, q[1] + wd / 2], fill=c)
        if c == INK:
            d.polygon(tri, fill=c, outline=c, width=14)
        else:
            d.polygon(tri, fill=c)
    canvas.alpha_composite(lay)


def ring(canvas, cx, cy, r, col=RED, w=16):
    d = ImageDraw.Draw(canvas)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=w + 12)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], outline=col, width=w)


# ------------------------------------------------------------------ target 1: "6 Creatures Living In Your House Right Now"

def skin_bg(w=W, h=H, seed=4, base=(214, 132, 102), dark=(120, 52, 40)):
    """Macro skin: warm flesh with ink-ringed pores and fine creases, darkened to the edges."""
    bg = radial(w, h, base, dark, cx=0.62, cy=0.62, r=0.95)
    d = ImageDraw.Draw(bg)
    rng = random.Random(seed)
    for _ in range(int(w * h / 9000)):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(4, 11)
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=(96, 40, 32))
        d.arc([x - r - 3, y - r - 2, x + r + 3, y + r + 2], 200, 330, fill=(240, 170, 140), width=2)
    for _ in range(30):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        L, a = rng.uniform(60, 180), rng.uniform(-0.5, 0.5)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=(170, 86, 66), width=3)
    return bg.filter(ImageFilter.GaussianBlur(1.2))


def pore(canvas, cx, cy, rx, ry, part="back"):
    """A follicle opening: dark hole (back), and its front lip drawn over whatever climbs out (front)."""
    d = ImageDraw.Draw(canvas)
    if part == "back":
        d.ellipse([cx - rx - 10, cy - ry - 8, cx + rx + 10, cy + ry + 8], fill=(150, 66, 50))
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(36, 10, 8), outline=INK, width=8)
        d.ellipse([cx - rx * 0.7, cy - ry * 0.6, cx + rx * 0.7, cy + ry * 0.5], fill=(14, 4, 3))
    else:
        lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        e = ImageDraw.Draw(lay)
        e.chord([cx - rx - 10, cy - ry - 8, cx + rx + 10, cy + ry + 8], 0, 180, fill=(196, 104, 80))
        e.chord([cx - rx - 10, cy - ry * 0.2, cx + rx + 10, cy + ry + 8], 0, 180, fill=(214, 128, 98))
        e.arc([cx - rx, cy - ry, cx + rx, cy + ry], 0, 180, fill=INK, width=9)
        e.arc([cx - rx - 10, cy - ry - 8, cx + rx + 10, cy + ry + 8], 10, 170, fill=(246, 178, 150), width=5)
        canvas.alpha_composite(lay)


def _demodex_big_face(c, t, p):
    """demodex with a thumbnail-size face: bigger eyes and an open toothy grin over the stock ones."""
    B.demodex(c, t, p)
    B.shape(c, lambda q: B.p_ellipse(q, 0, -585, 74, 92), B.C["demo"], 0.0, None)
    B.eyes(c, 0, -628, 34, 36, p.get("look", (0, 0)), p.get("mood", "smug"), 0, B.OUT * 0.6, lid=B.C["demo"])
    B.mouth(c, 0, -556, 64, "grin", p.get("talk", 0.7), B.OUT * 0.6, teeth=True)


def face_mite(scale, mood="smug", look=(0, 0.3), mouth="grin", talk=0.7):
    return actor(_demodex_big_face, {"mood": mood, "look": look, "mouth": mouth, "talk": talk}, scale, 1000, 1500,
                 500, 1300)


def t1a():
    """IN YOUR FACE: a giant face mite climbing out of a pore (grinning), Meatball screaming at the left."""
    cv = skin_bg()
    for (x, y, s, r) in ((560, 625, 0.18, -12),):   # more mites peeking: there are many
        pore(cv, x, y, 46 * s / 0.2, 20 * s / 0.2)
        m = face_mite(s, "happy", (0, 0), talk=0.0)
        m = pop(m.crop((0, 0, m.width, int(m.height * 0.62))), 4, 3, (255, 240, 200), 8)
        m = m.rotate(r, expand=True, resample=Image.BICUBIC)
        cv.alpha_composite(m, (int(x - m.width / 2), int(y - m.height + 20)))
        pore(cv, x, y, 46 * s / 0.2, 20 * s / 0.2, "front")
    px, py = 860, 650
    pore(cv, px, py, 200, 72)
    mite = face_mite(0.9, "smug", (-0.9, 0.1))
    mite = mite.crop((0, 0, mite.width, int(mite.height * 0.9)))
    mite = pop(mite, 9, 9, (255, 246, 210), 34, (255, 230, 150))
    mite = mite.rotate(-10, expand=True, resample=Image.BICUBIC)
    cv.alpha_composite(mite, (int(px - mite.width / 2 + 40), int(py - mite.height + 120)))
    pore(cv, px, py, 200, 72, "front")
    vignette(cv, 0.3)
    mb = pop(fit(meatball("shock", 1000, look=(14, 0), head=0.46), h=470), 7, 8, WHITE, 18)
    cv.alpha_composite(mb, (-30, H - mb.height + 40))
    words(cv, "IN YOUR FACE", 22, -4, 150, YEL, max_w=640)
    badge(cv, "#1", 1120, 18)
    return cv


def night_bg(w=W, h=H):
    return radial(w, h, (52, 64, 132), (8, 10, 30), cx=0.5, cy=0.42, r=0.85)


def eyes_in_dark(cv, n=24, keep_out=(330, 950), y0=230, seed=9):
    d = ImageDraw.Draw(cv)
    rng = random.Random(seed)
    g = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    e = ImageDraw.Draw(g)
    spots = []
    while len(spots) < n:
        x, y = rng.uniform(30, cv.width - 30), rng.uniform(y0, cv.height - 60)
        if keep_out[0] < x < keep_out[1]:
            continue
        spots.append((x, y, rng.uniform(6, 12)))
    for x, y, r in spots:
        for dx in (-r * 1.7, r * 1.7):
            e.ellipse([x + dx - r * 2.6, y - r * 2.6, x + dx + r * 2.6, y + r * 2.6], fill=(255, 210, 40, 120))
    cv.alpha_composite(g.filter(ImageFilter.GaussianBlur(9)))
    for x, y, r in spots:
        for dx in (-r * 1.7, r * 1.7):
            d.ellipse([x + dx - r, y - r * 0.75, x + dx + r, y + r * 0.75], fill=(255, 240, 120))
            d.ellipse([x + dx - r * 0.22, y - r * 0.65, x + dx + r * 0.22, y + r * 0.65], fill=INK)


def t1b():
    """THEY'RE AWAKE: Meatball in bed at night, blanket to his chin, a house centipede crawling over the blanket at
    him and dozens of glowing eyes in the dark."""
    cv = night_bg()
    eyes_in_dark(cv, 22, (250, 900))
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle([170, 360, 860, 640], 90, fill=(206, 216, 240), outline=INK, width=9)
    mb = pop(fit(meatball("shock", 1000, look=(18, 2), head=0.46), h=520), 7, 7, (190, 210, 255), 20)
    cv.alpha_composite(mb, (int(470 - mb.width / 2), 90))
    bl = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    e = ImageDraw.Draw(bl)
    pts = [(60, H + 10), (80, 600), (300, 575), (520, 595), (760, 570), (1020, 610), (1300, 640), (1300, H + 10)]
    e.polygon(pts, fill=(200, 44, 54))
    e.line(pts[1:-1], fill=INK, width=12, joint="curve")
    for x in range(160, 1300, 130):
        e.line([(x, 640), (x + 40, H)], fill=(160, 30, 42), width=10)
    for hx in (330, 700):   # his fists gripping the blanket edge
        e.ellipse([hx - 36, 556, hx + 36, 624], fill=INK)
    cv.alpha_composite(bl)
    cent = actor(B.house_centipede, {"mood": "angry", "look": (-1, 0.3), "mouth": "grin", "talk": 0.6,
                                     "bite": 0.0}, 0.62, 2600, 1300, 1300, 1000)
    cent = cent.transpose(Image.FLIP_LEFT_RIGHT)
    cent = pop(cent, 3, 4, (255, 214, 90), 22, (255, 190, 60)).rotate(8, expand=True, resample=Image.BICUBIC)
    cv.alpha_composite(cent, (410, 205))
    words(cv, "THEY'RE AWAKE", 1260, -6, 160, YEL, anchor="ra", max_w=720)
    badge(cv, "#1", 18, 18)
    return cv


def fabric_bg(w, h, base=(250, 236, 196), line=(226, 204, 160)):
    bg = Image.new("RGBA", (w, h), base + (255,))
    d = ImageDraw.Draw(bg)
    for x in range(-h, w, 26):
        d.line([(x, 0), (x + h, h)], fill=line, width=7)
    for x in range(0, w + h, 26):
        d.line([(x, 0), (x - h, h)], fill=line, width=4)
    return bg


def t1c():
    """YOUR PILLOW?: a magnifying glass over the pillow shows a dust mite the size of a dog, chewing a skin flake."""
    cv = radial(W, H, (70, 96, 170), (14, 18, 46), cx=0.4, cy=0.5)
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle([-60, 330, 1000, 800], 140, fill=(232, 236, 248), outline=INK, width=10)
    d.arc([160, 450, 700, 660], 200, 330, fill=(190, 198, 222), width=10)
    cx, cy, r = 790, 330, 300
    lens = fabric_bg(2 * r, 2 * r)
    for x, y, s, rot in ((90, 470, 0.26, 18), (540, 470, 0.24, -16)):
        m = pop(actor(B.dust_mite, {"mood": "happy", "chew": 1.0}, s, 900, 700, 450, 650), 5, 0, glow=0)
        paste_c(lens, m, x, y, rot)
    big = actor(B.dust_mite, {"mood": "smug", "look": (-0.7, 0.3), "mouth": "grin", "talk": 0.8, "flake": 1.0},
                0.7, 1200, 900, 600, 820)
    paste_c(lens, pop(big, 8, 0, glow=0), 300, 320)
    mask = Image.new("L", lens.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    g = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([cx - r - 40, cy - r - 40, cx + r + 40, cy + r + 40], fill=(255, 236, 150, 190))
    cv.alpha_composite(g.filter(ImageFilter.GaussianBlur(28)))
    hl = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    e = ImageDraw.Draw(hl)
    a = math.radians(145)
    p0 = (cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a))
    p1 = (cx + (r + 210) * math.cos(a), cy + (r + 210) * math.sin(a))
    e.line([p0, p1], fill=INK, width=76)
    e.line([p0, p1], fill=(150, 78, 44), width=52)
    cv.alpha_composite(hl)
    cv.paste(lens, (cx - r, cy - r), mask)
    d = ImageDraw.Draw(cv)
    d.ellipse([cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18], outline=INK, width=46)
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], outline=(200, 206, 216), width=24)
    d.arc([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], 200, 250, fill=WHITE, width=14)
    mb = pop(fit(meatball("shock", 1000, look=(16, -6), head=0.46), h=430), 7, 7, WHITE, 18)
    cv.alpha_composite(mb, (-20, H - mb.height + 30))
    words(cv, "YOUR", 26, -6, 130, WHITE)
    words(cv, "PILLOW?", 26, 118, 150, YEL)
    badge(cv, "#1", 18, 640, 62)
    return cv


def t1d():
    """WHERE?!: the house cut open like a doll's house, six creatures in six rooms, a red arrow in."""
    cv = night_bg()
    d = ImageDraw.Draw(cv)
    x0, x1, yt, yb = 330, 1250, 240, 712
    d.polygon([(x0 - 40, yt), ((x0 + x1) / 2, 50), (x1 + 40, yt)], fill=(170, 52, 44), outline=INK, width=10)
    d.rectangle([x0, yt, x1, yb], fill=(110, 80, 60), outline=INK, width=10)
    cw, rh = (x1 - x0) / 3, (yb - yt) / 2
    tints = [(250, 236, 200), (214, 236, 244), (244, 224, 214), (232, 222, 196), (206, 214, 196), (90, 84, 78)]
    cast = [
        (B.house_centipede, {"mood": "angry", "mouth": "grin", "talk": 0.5}, 0.17),
        (_demodex_big_face, {"mood": "smug", "talk": 0.7}, 0.3),
        (B.jumping_spider, {"mood": "angry"}, 0.22),
        (B.silverfish, {"mood": "smug"}, 0.24),
        (B.dust_mite, {"mood": "smug", "mouth": "grin", "talk": 0.6}, 0.3),
        (cellar_spider, {"mood": "worry"}, 0.42),
    ]
    for k, (fn, p, s) in enumerate(cast):
        ri, ci = divmod(k, 3)
        rx0, ry0 = x0 + ci * cw, yt + ri * rh
        d.rectangle([rx0 + 10, ry0 + 10, rx0 + cw - 10, ry0 + rh - 10], fill=tints[k], outline=INK, width=6)
        im = actor(fn, p, s, 1000, 900, 500, 760)
        im = pop(fit(im, cw - 50, rh - 50), 5, 4, WHITE, 6)
        paste_c(cv, im, rx0 + cw / 2, ry0 + rh / 2 + 4)
    mb = pop(fit(meatball("shock", 1000, look=(18, -4), head=0.46, sweat=False), h=380), 7, 7, WHITE, 18)
    cv.alpha_composite(mb, (-20, H - mb.height + 30))
    arrow(cv, (250, 150), (420, 300))
    words(cv, "WHERE?!", 18, -6, 170, YEL, max_w=480)
    badge(cv, "#1", 1100, 18, 62)
    return cv


# ------------------------------------------------------------------ target 2: "6 More Creatures Living In Your House"
# Same kit as #1 (yellow Anton words, horrified Meatball head bottom-left, glowing outlined creature, house badge).

def bug_cfg(name, **kw):
    cfg = dict(SPECIES[name])
    cfg.update(kw)
    return cfg


def sheet_bg(w=W, h=H):
    """Bed sheet at night: pale blue cotton with folds, dark at the edges."""
    bg = radial(w, h, (176, 196, 236), (22, 28, 70), cx=0.62, cy=0.55, r=0.9)
    d = ImageDraw.Draw(bg)
    for k in range(7):
        y = 120 + k * 100
        d.arc([-200, y - 60, w + 200, y + 120], 190, 350, fill=(140, 160, 210), width=6)
    return bg.filter(ImageFilter.GaussianBlur(1.5))


def blood_drop(cv, x, y, r):
    d = ImageDraw.Draw(cv)
    d.polygon([(x, y - 2.3 * r), (x - r, y), (x + r, y)], fill=(214, 20, 30), outline=INK, width=6)
    d.ellipse([x - r, y - r * 0.9, x + r, y + r * 1.1], fill=(214, 20, 30), outline=INK, width=6)
    d.polygon([(x, y - 2.1 * r), (x - r + 5, y), (x + r - 5, y)], fill=(214, 20, 30))
    d.ellipse([x - r * 0.45, y - r * 0.5, x - r * 0.1, y - r * 0.05], fill=(255, 150, 150))


def t2a():
    """WHILE YOU SLEEP: a fat blood-full bed bug on your sheet, grinning, a drop of blood at its mouth."""
    cv = sheet_bg()
    cfg = bug_cfg("bed_bug", color="#b0301e", length=560, height=330, leg_len=70, head_r=0.38, eye_r=50,
                  teeth=True, fangs=True, mood="smug", mouth="grin", stripes=6, sheen=True)
    bug = actor(sp(cfg), {"look": (-0.4, 0.4), "talk": 0.7}, 1.25, 2000, 1100, 1000, 900)
    bug = pop(bug.transpose(Image.FLIP_LEFT_RIGHT), 9, 9, (255, 236, 200), 36, (255, 120, 90))
    paste_c(cv, bug, 860, 430, -4)
    blood_drop(cv, 520, 590, 30)
    blood_drop(cv, 590, 660, 20)
    vignette(cv, 0.25)
    mb = pop(fit(meatball("shock", 1000, look=(16, 2), head=0.46), h=420), 7, 7, WHITE, 18)
    cv.alpha_composite(mb, (-20, H - mb.height + 30))
    words(cv, "WHILE YOU SLEEP", 22, -6, 140, YEL, max_w=800)
    badge(cv, "#2", 1120, 18)
    return cv


def tiles_bg(w=W, h=H):
    bg = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    d = ImageDraw.Draw(bg)
    s = 120
    for i in range(-1, w // s + 2):
        for j in range(-1, h // s + 2):
            c = (34, 98, 104) if (i + j) % 2 else (22, 70, 78)
            d.rectangle([i * s, j * s, i * s + s - 4, j * s + s - 4], fill=c)
    v = radial(w, h, (255, 255, 255), (40, 40, 40), cx=0.6, cy=0.55, r=0.85).convert("RGB")
    return Image.fromarray((np.array(bg.convert("RGB"), np.float32) * np.array(v, np.float32) / 255).astype(
        np.uint8)).convert("RGBA")


def split_actor(fn, p, scale, xu, w=2400, h=1300, ox=1200, oy=1050):
    """Render an actor and cut it in two at drawing x = xu: (left part, right part), each cropped."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(s)
    c.translate(ox, oy)
    c.scale(scale, scale)
    fn(c, 0.3, dict({"phase": 0.0, "walking": False, "blink": 0}, **p))
    s.flush()
    im = Image.frombuffer("RGBA", (w, h), bytes(s.get_data()), "raw", "BGRa", 0, 1)
    cut = int(ox + xu * scale)
    left, right = im.crop((0, 0, cut, h)), im.crop((cut, 0, w, h))
    return left.crop(left.getbbox()), right.crop(right.getbbox())


def t2b():
    """NO HEAD?!: a cockroach still walking with its head gone; the head lies beside it, still blinking."""
    cv = tiles_bg()
    cfg = bug_cfg("roach", head_r=0.6, eye_r=32, mood="shock", mouth="o", ant=0)
    fn = sp(cfg)
    body, _ = split_actor(fn, {"walking": True, "phase": 1.2}, 0.95, 140)
    _, head = split_actor(fn, {"look": (-0.8, -0.3)}, 1.0, 150)
    body = pop(body, 9, 9, (255, 214, 90), 34, (255, 190, 60))
    head = pop(head, 9, 9, (255, 214, 90), 30, (255, 190, 60))
    paste_c(cv, body, 700, 420)
    ring(cv, 700 + body.width / 2 - 115, 420 + 25, 70)   # the empty neck
    paste_c(cv, head, 1060, 540, -30)
    d = ImageDraw.Draw(cv)
    for k in range(3):   # shock marks around the head
        a = -2.2 + k * 0.55
        x, y = 1040 + 160 * math.cos(a), 520 + 160 * math.sin(a)
        d.line([(x, y), (x + 34 * math.cos(a), y + 34 * math.sin(a))], fill=INK, width=18)
        d.line([(x, y), (x + 34 * math.cos(a), y + 34 * math.sin(a))], fill=WHITE, width=9)
    mb = pop(fit(meatball("shock", 1000, look=(18, 6), head=0.46), h=420), 7, 7, WHITE, 18)
    cv.alpha_composite(mb, (-20, H - mb.height + 30))
    words(cv, "NO HEAD?!", 22, -6, 190, YEL, max_w=640)
    badge(cv, "#2", 1120, 18)
    return cv


def _earwig_pincers(c, t, p):
    cfg = p["cfg"]
    creature(c, t, p)
    H_, ll, L = cfg["height"], cfg["leg_len"], cfg["length"]
    by = -H_ * 0.55 - ll * 0.45 + 3 * math.sin(t * 2.4)
    x0 = -L * 0.5
    for s in (-1, 1):
        pts = [(x0 + 20, by + s * H_ * 0.18), (x0 - 140, by + s * 70), (x0 - 260, by + s * 20)]
        B.stroke(c, pts, 40, smooth=True)
        B.stroke(c, pts, 24, smooth=True, color=B.hexc("#4a2414"))


def t2c():
    """YOUR EAR?!: an earwig, pincers up, marching at Meatball's head; red arrow from bug to his ear."""
    cv = night_bg()
    eyes_in_dark(cv, 12, (0, 760), 260, seed=4)
    cfg = bug_cfg("earwig", tails=0, head_r=0.75, eye_r=34, mood="angry", mouth="grin", teeth=True, length=620,
                  height=140)
    bug = actor(lambda c, t, p: _earwig_pincers(c, t, dict(p, cfg=cfg)), {"look": (-1, 0), "talk": 0.6,
                                                                          "walking": True, "phase": 0.6},
                0.8, 2600, 1100, 1300, 900)
    bug = pop(bug.transpose(Image.FLIP_LEFT_RIGHT), 9, 9, (255, 214, 90), 34, (255, 170, 60))
    paste_c(cv, bug, 880, 440, -10)
    mb = pop(fit(meatball("shock", 1000, look=(18, 0), head=0.46), h=470), 7, 7, WHITE, 18)
    cv.alpha_composite(mb, (-30, H - mb.height + 30))
    words(cv, "YOUR EAR?!", 22, -6, 190, YEL, max_w=700)
    badge(cv, "#2", 1120, 18)
    return cv


# ------------------------------------------------------------------ published long-forms (Nolan 10/28: redo them all)
# Same kit; series badge colour by show: MYTHS red-X tag, EXPLAINS yellow, INVESTIGATES green magnifier.

MYTH_TAG = dict(col=(255, 255, 255), icon="x")
EXPL_TAG = dict(col=YEL, icon="house")
CASE_TAG = dict(col=(90, 220, 120), icon="mag")


def sky_bg(top, bottom, w=W, h=H):
    a = np.linspace(0, 1, h)[:, None, None]
    g = np.array(top, np.float32) * (1 - a) + np.array(bottom, np.float32) * a
    return Image.fromarray(np.repeat(g, w, axis=1).astype(np.uint8), "RGB").convert("RGBA")


def red_x(cv, cx, cy, r, w=30):
    d = ImageDraw.Draw(cv)
    for a, b in (((-1, -1), (1, 1)), ((1, -1), (-1, 1))):
        p0, p1 = (cx + a[0] * r, cy + a[1] * r), (cx + b[0] * r, cy + b[1] * r)
        d.line([p0, p1], fill=INK, width=w + 16)
    for a, b in (((-1, -1), (1, 1)), ((1, -1), (-1, 1))):
        d.line([(cx + a[0] * r, cy + a[1] * r), (cx + b[0] * r, cy + b[1] * r)], fill=RED, width=w)


def mb_left(cv, h=430, look=(16, 0), y_off=30, sweat=True):
    mb = pop(fit(meatball("shock", 1000, look=look, head=0.46, sweat=sweat), h=h), 7, 7, WHITE, 18)
    cv.alpha_composite(mb, (-20, H - mb.height + y_off))


OSTRICH = {"plan": "bird", "color": "#2b2522", "belly": "#3a322e", "dark": "#151110", "length": 560, "height": 360,
           "leg_len": 330, "foot_color": "#e7a6a0", "beak_color": "#e7a6a0", "mood": "calm"}


def ostrich(c, t, p):
    """Ostrich, side view facing right, feet at y = 0: fluffy black body, white plumes, long thick neck, small head
    with big lashed eyes and a flat beak, long bare pink legs with two toes."""
    K = B
    pink, pink_dk = K.hexc("#e7a6a0"), K.hexc("#c9807a")
    for hx, far in ((-30, True), (60, False)):   # legs: thigh, backward knee, shin, two toes
        col = pink_dk if far else pink
        K.limb(c, [(hx, -470), (hx + 40, -300), (hx - 10, -40)], 30 if not far else 26, col, K.OUT * 0.7)
        for dx in (60, 110):
            K.limb(c, [(hx - 10, -30), (hx - 10 + dx, -6)], 22, col, K.OUT * 0.6)
    K.shape(c, lambda q: K.p_smooth(q, [(-150, -620), (-330, -760), (-290, -600), (-380, -650), (-300, -520)]),
            (1, 1, 1), K.OUT, (0.05, 0.1))   # white tail plumes
    K.shape(c, lambda q: K.p_blob(q, 0, -580, 250, 170, 0.07, seed=5), K.hexc("#221c1a"), K.OUT, (0.1, 0.15),
            hi=(0.3, 0.2, 0.15))
    for k in range(9):   # fluff
        a = math.pi * (1.05 + 0.9 * k / 8)
        x, y = 250 * math.cos(a), -580 + 170 * math.sin(a)
        K.stroke(c, [(x, y), (x * 1.12, y - 18)], 8, color=K.hexc("#3a302c"))
    K.shape(c, lambda q: K.p_smooth(q, [(-120, -600), (40, -660), (160, -560), (40, -520)]), (1, 1, 1), K.OUT * 0.8,
            (0.05, 0.15))   # white wing plume
    K.limb(c, [(170, -640), (250, -820), (230, -1000), (270, -1090)], 56, K.hexc("#d7b2a8"), K.OUT)   # neck
    K.shape(c, lambda q: K.p_poly(q, [(310, -1110), (420, -1085), (312, -1060)]), K.hexc("#e9b28a"), K.OUT * 0.7,
            None)   # flat beak
    K.shape(c, lambda q: K.p_ellipse(q, 280, -1100, 64, 54), K.hexc("#d7b2a8"), K.OUT, (0.08, 0.15))
    K.eyes(c, 282, -1112, 30, 26, p.get("look", (1, 0)), p.get("mood", "smug"), 0, K.OUT * 0.6,
           lid=K.hexc("#d7b2a8"))
    for ex in (256, 308):   # big lashes
        for k in range(3):
            a = -math.pi / 2 + (k - 1) * 0.45
            K.stroke(c, [(ex + 22 * math.cos(a), -1150 + 22 * math.sin(a)),
                         (ex + 46 * math.cos(a), -1150 + 46 * math.sin(a))], 7)
    K.mouth(c, 345, -1082, 40, p.get("mouth", "grin"), p.get("talk", 0.0), K.OUT * 0.5)


def cat(c, t, p):
    """House cat, side view facing right, feet at y = 0: slim body, rounded head, triangle ears, whiskers, long curled
    tail, slim legs with paws; a red collar with a CIA antenna. """
    K = B
    fur, fur_dk = K.hexc("#f1ede4"), K.hexc("#c9c2b4")
    K.stroke(c, [(-210, -250), (-360, -330), (-420, -520), (-330, -620), (-280, -540)], 34, smooth=True)
    K.stroke(c, [(-210, -250), (-360, -330), (-420, -520), (-330, -620), (-280, -540)], 20, smooth=True, color=fur)
    for hx, far in ((-150, True), (150, True), (-110, False), (190, False)):
        col = fur_dk if far else fur
        K.limb(c, [(hx, -230), (hx + 10, -110), (hx + 4, -16)], 28, col, K.OUT * 0.6)
        K.shape(c, lambda q, hx=hx: K.p_ellipse(q, hx + 18, -14, 30, 16), col, K.OUT * 0.6, None)
    K.shape(c, lambda q: K.p_ellipse(q, 0, -280, 240, 105), fur, K.OUT, (0.05, 0.18), hi=(0.35, 0.2, 0.2))
    for s_ in (-1, 1):   # ears
        ex = 300 + s_ * 70
        K.shape(c, lambda q, ex=ex, s_=s_: K.p_poly(q, [(ex - 50, -440), (ex + s_ * 10, -560), (ex + 50, -430)]),
                fur, K.OUT, None)
        K.flat(c, lambda q, ex=ex, s_=s_: K.p_poly(q, [(ex - 26, -450), (ex + s_ * 8, -520), (ex + 26, -445)]),
               K.hexc("#f2a6b4"))
    K.shape(c, lambda q: K.p_ellipse(q, 300, -380, 125, 112), fur, K.OUT, (0.06, 0.15))
    K.shape(c, lambda q: K.p_rrect(q, 190, -300, 120, 34, 14), K.hexc("#d8322a"), K.OUT * 0.7, None)   # collar
    K.stroke(c, [(205, -290), (110, -640)], 14)   # antenna on the collar, raked back behind the head
    K.stroke(c, [(205, -290), (110, -640)], 6, color=K.hexc("#c8ccd4"))
    K.shape(c, lambda q: K.p_ellipse(q, 106, -655, 24, 24), K.hexc("#ff3a2a"), K.OUT * 0.6, None)
    K.eyes(c, 310, -400, 34, 46, p.get("look", (1, 0)), p.get("mood", "angry"), 0, K.OUT * 0.6, lid=fur)
    K.shape(c, lambda q: K.p_poly(q, [(360, -366), (388, -366), (374, -348)]), K.hexc("#f28aa0"), K.OUT * 0.4, None)
    K.mouth(c, 370, -322, 42, p.get("mouth", "grin"), p.get("talk", 0.0), K.OUT * 0.5)
    for k in (-1, 0, 1):   # whiskers
        K.stroke(c, [(330, -345 + k * 14), (418, -352 + k * 22)], 4)


def l_ostrich():
    """gFhrONKK0rI Everything You Know About Animals Is WRONG -> FAKE!: a smug ostrich standing tall beside the sand hole it never
    sticks its head in (red X)."""
    cv = sky_bg((120, 196, 240), (250, 214, 140))
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 560, W, H], fill=(226, 180, 104))
    d.ellipse([560, 590, 820, 660], fill=(120, 80, 40), outline=INK, width=8)   # the sand hole it never uses
    d.ellipse([600, 600, 780, 640], fill=(60, 36, 18))
    bird = actor(ostrich, {"look": (1, 0.3), "mood": "smug", "mouth": "grin", "talk": 0.5}, 1.0, 1600, 1500,
                 800, 1350)
    bird = pop(fit(bird.transpose(Image.FLIP_LEFT_RIGHT), 560, 620), 9, 8, WHITE, 26, (255, 236, 170))
    paste_c(cv, bird, 1000, 380)
    red_x(cv, 690, 590, 80)
    vignette(cv, 0.25)
    mb_left(cv, 420, (18, -4))
    words(cv, "FAKE!", 30, -6, 230, YEL)
    badge(cv, "MYTHS", 1050, 18, 70, **MYTH_TAG)
    return cv


LEMMING = {"plan": "mammal", "color": "#c98a4a", "dark": "#7a4a22", "belly": "#f0dcc0", "length": 420, "height": 230,
           "leg_len": 60, "leg_w": 26, "ears": "round", "tail": "thin", "tail_w": 10, "mood": "shock", "mouth": "o"}


def l_lemming():
    """RwbgzQisvYM 12 Animal Myths ... (Disney Faked One) -> STAGED!: lemmings flung off a cliff past a film camera."""
    cv = sky_bg((90, 150, 220), (40, 70, 140))
    d = ImageDraw.Draw(cv)
    d.polygon([(0, 330), (560, 300), (600, 360), (520, H), (0, H)], fill=(110, 96, 86), outline=INK, width=10)
    d.polygon([(0, 300), (560, 280), (566, 320), (0, 340)], fill=(236, 240, 248), outline=INK, width=6)   # snow lip
    d.rectangle([600, 640, W, H], fill=(40, 90, 150))
    lem = actor(sp(LEMMING), {}, 0.95, 1400, 900, 700, 750)
    for x, y, r, s in ((700, 330, -60, 0.7), (900, 470, -140, 1.0), (1090, 300, -30, 0.62)):
        paste_c(cv, pop(fit(lem, int(lem.width * s * 0.62)), 7, 6, WHITE, 18, (255, 236, 170)), x, y, r)
    cam = Image.new("RGBA", (300, 240), (0, 0, 0, 0))   # an old film camera on a tripod, aimed at the drop
    e = ImageDraw.Draw(cam)
    e.rounded_rectangle([20, 60, 220, 170], 14, fill=(40, 40, 46), outline=INK, width=8)
    e.ellipse([10, 0, 90, 80], fill=(60, 60, 66), outline=INK, width=8)
    e.ellipse([100, 0, 180, 80], fill=(60, 60, 66), outline=INK, width=8)
    e.polygon([(220, 90), (290, 70), (290, 160), (220, 140)], fill=(60, 60, 66), outline=INK)
    for x in (60, 120, 180):
        e.line([(120, 170), (x, 240)], fill=INK, width=10)
    paste_c(cv, pop(cam, 6, 6, WHITE, 12), 300, 230)
    mb_left(cv, 400, (18, -8))
    words(cv, "STAGED!", 1262, -6, 200, YEL, anchor="ra", max_w=620)
    badge(cv, "MYTHS", 18, 18, 70, **MYTH_TAG)
    return cv


WOLF = {"plan": "mammal", "color": "#8e8f99", "dark": "#5d5e68", "belly": "#e2e2e6", "length": 680, "height": 300,
        "leg_len": 170, "leg_w": 40, "ears": "pointed", "tail": "fluffy", "whiskers": False, "mood": "angry",
        "mouth": "grin", "teeth": True}
PUP = {"plan": "mammal", "color": "#e9b06a", "dark": "#b07a3a", "belly": "#fff6e6", "length": 380, "height": 240,
       "leg_len": 80, "leg_w": 30, "ears": "pointed", "tail": "fluffy", "whiskers": False, "mood": "happy"}


def l_wolf():
    """Uqj0QL8G0d4 How Wolves Became Dogs -> HOW?!: a snarling wolf, red arrow, a tiny fluffy pup."""
    cv = night_bg()
    wolf = actor(sp(WOLF), {"look": (1, 0.2), "talk": 0.7}, 1.0, 2000, 1100, 1000, 950)
    paste_c(cv, pop(fit(wolf, 600, 420), 9, 8, (220, 230, 255), 26, (150, 170, 255)), 690, 440)
    pup = actor(sp(PUP), {"look": (-1, 0), "talk": 0.4}, 0.7, 1400, 800, 700, 700)
    paste_c(cv, pop(fit(pup.transpose(Image.FLIP_LEFT_RIGHT), 260, 200), 7, 7, WHITE, 22, (255, 220, 150)),
            1090, 540)
    arrow(cv, (930, 300), (1060, 440))
    mb_left(cv, 400, (18, -4))
    words(cv, "HOW?!", 30, -6, 230, YEL)
    badge(cv, "EXPLAINS", 990, 18, 70, **EXPL_TAG)
    return cv


STICK = {"plan": "insect", "body": "long", "color": "#1f1a17", "dark": "#0e0b0a", "length": 900, "height": 120,
         "leg_len": 210, "leg_w": 18, "ant": 320, "sheen": True, "head_r": 0.75, "eye_r": 32, "mood": "worry"}


def l_stick():
    """o9Emu9oMgCs Animals Thought Extinct Found Alive -> ONLY 24: the tree lobster on its sea-stack rock."""
    cv = sky_bg((40, 70, 140), (120, 170, 220))
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 600, W, H], fill=(30, 100, 160))
    for k in range(5):
        d.arc([k * 300 - 100, 600, k * 300 + 200, 660], 200, 340, fill=(200, 230, 250), width=6)
    d.polygon([(920, 640), (990, 260), (1030, 90), (1070, 250), (1180, 640)], fill=(96, 92, 96), outline=INK,
              width=10)
    d.polygon([(1000, 260), (1030, 120), (1060, 260)], fill=(130, 126, 130))
    bug = actor(sp(STICK), {"look": (1, 0.3), "mouth": "o"}, 0.95, 2400, 1000, 1200, 800)
    bug = pop(fit(bug, 600, 300), 9, 9, (255, 236, 170), 34, (255, 210, 110))
    paste_c(cv, bug, 640, 420, 10)
    ring(cv, 1035, 190, 70)
    mb_left(cv, 380, (18, -6))
    words(cv, "ONLY 24", 24, -6, 200, YEL, max_w=600)
    badge(cv, "EXPLAINS", 990, 18, 70, **EXPL_TAG)
    return cv


WOMBAT = {"plan": "mammal", "color": "#8b6a4d", "dark": "#5c4430", "belly": "#a8896a", "length": 580, "height": 330,
          "leg_len": 70, "leg_w": 44, "ears": "round", "tail": "thin", "tail_w": 0.01, "tail_color": "#8b6a4d", "whiskers": True, "mood": "smug",
          "mouth": "grin"}


def l_wombat():
    """z-Kg8sXCxlU Weird Animal Facts (3 Are Fake) -> CUBES?!: a smug wombat beside a stack of cube poops."""
    cv = radial(W, H, (120, 190, 110), (24, 60, 30), cx=0.6, cy=0.5, r=0.85)
    wom = actor(sp(WOMBAT), {"look": (-0.6, 0.4), "talk": 0.4}, 1.15, 2000, 1100, 1000, 950)
    paste_c(cv, pop(fit(wom.transpose(Image.FLIP_LEFT_RIGHT), 600, 400), 9, 8, WHITE, 24, (255, 236, 170)), 940, 450)
    cube = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
    e = ImageDraw.Draw(cube)
    e.polygon([(10, 40), (70, 10), (120, 40), (60, 70)], fill=(140, 96, 56), outline=INK, width=6)
    e.polygon([(10, 40), (60, 70), (60, 125), (10, 95)], fill=(110, 72, 40), outline=INK, width=6)
    e.polygon([(60, 70), (120, 40), (120, 95), (60, 125)], fill=(90, 58, 32), outline=INK, width=6)
    for x, y in ((530, 610), (640, 610), (585, 530)):
        paste_c(cv, pop(cube, 4, 5, (255, 236, 170), 14), x, y)
    ring(cv, 585, 580, 135)
    mb_left(cv, 400, (18, 6))
    words(cv, "CUBES?!", 24, -6, 210, YEL, max_w=620)
    badge(cv, "MYTHS", 1050, 18, 70, **MYTH_TAG)
    return cv


CAT = {"plan": "mammal", "color": "#f1ede4", "dark": "#bdb6a8", "belly": "#ffffff", "length": 560, "height": 260,
       "leg_len": 140, "leg_w": 32, "ears": "pointed", "tail": "thin", "tail_w": 16, "tail_color": "#e2dccf",
       "whiskers": True, "mood": "angry", "mouth": "grin", "teeth": True}


def l_cat():
    """2EC5LDtbUbo Conspiracy Theories That Turned Out To Be TRUE -> SPY CAT?!: Acoustic Kitty, a white cat with a
    CIA antenna wired up its tail, in a dark interrogation-room spotlight."""
    cv = radial(W, H, (60, 66, 80), (8, 8, 12), cx=0.62, cy=0.5, r=0.75)
    g = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).polygon([(760, -20), (900, -20), (1240, 700), (420, 700)], fill=(255, 244, 200, 70))
    cv.alpha_composite(g.filter(ImageFilter.GaussianBlur(20)))
    kitty = actor(cat, {"look": (1, 0.2), "talk": 0.6}, 1.0, 1400, 1000, 700, 900)
    kitty = pop(fit(kitty.transpose(Image.FLIP_LEFT_RIGHT), 640, 480), 9, 8, WHITE, 24, (255, 236, 170))
    paste_c(cv, kitty, 900, 400)
    mb_left(cv, 420, (18, -2))
    words(cv, "SPY CAT?!", 24, -6, 190, YEL, max_w=620)
    badge(cv, "INVESTIGATES", 18, 640, 62, **CASE_TAG)
    return cv


LONGFORMS = [   # (video id, current public title, concept)
    ("gFhrONKK0rI", "Everything You Know About Animals Is WRONG", "l_ostrich"),
    ("RwbgzQisvYM", "12 Animal Myths You've Believed Your Whole Life (Disney Faked One)", "l_lemming"),
    ("Uqj0QL8G0d4", "How Wolves Became Dogs (The Funny History of Man's Best Friend)", "l_wolf"),
    ("o9Emu9oMgCs", "Animals Thought Extinct Found Alive (One Was Hiding on a Rock for 80 Years)", "l_stick"),
    ("z-Kg8sXCxlU", "Weird Animal Facts You Didn't Know (3 Are Fake. Can You Spot Them?)", "l_wombat"),
    ("2EC5LDtbUbo", "Conspiracy Theories That Turned Out To Be TRUE", "l_cat"),
]


# ------------------------------------------------------------------ target 3: Shorts cover template (1080x1920)
# Series band up top (inside the safe area), the animal huge in the middle with its glow, 1-3 words under it,
# horrified Meatball head bottom-left. The centre 1080x1080 alone still reads (search crops it square).

SERIES = {"house": ("IN YOUR HOUSE", YEL, ((52, 64, 132), (8, 10, 30))),
          "survive": ("WOULD MEATBALL SURVIVE?", (255, 120, 40), ((150, 62, 30), (30, 10, 6))),
          "vs": ("MEATBALL VS", (90, 220, 120), ((30, 100, 70), (6, 24, 18)))}


def series_band(cv, series, part, y=170):
    label, col, _ = SERIES[series]
    d = ImageDraw.Draw(cv)
    f = ImageFont.truetype(ANTON, 92)
    text = f"{label}  #{part}" if part else label
    tw = d.textlength(text, font=f)
    w = tw + 170
    x = (cv.width - w) / 2
    d.rounded_rectangle([x, y, x + w, y + 132], 30, fill=col, outline=INK, width=10)
    hx, hy, sz = x + 70, y + 70, 34
    if series == "house":
        d.polygon([(hx - sz * 1.3, hy - 2), (hx, hy - sz * 1.3), (hx + sz * 1.3, hy - 2)], fill=INK)
        d.rectangle([hx - sz * 0.9, hy - 4, hx + sz * 0.9, hy + sz], fill=INK)
    else:
        d.ellipse([hx - sz, hy - sz, hx + sz, hy + sz], fill=(150, 78, 44), outline=INK, width=6)
        d.chord([hx - sz, hy - sz, hx + sz, hy + sz * 0.2], 200, 340, fill=(196, 38, 30))
    d.text((x + 125, y + 66), text, font=f, fill=INK, anchor="lm")


def cover(series, part, hero, text, look=(14, -10)):
    w, h = 1080, 1920
    inner, outer = SERIES[series][2]
    cv = radial(w, h, inner, outer, cx=0.5, cy=0.42, r=0.8)
    if series == "house":
        eyes_in_dark(cv, 16, (160, 920), 360, seed=3)
    series_band(cv, series, part)
    paste_c(cv, fit(hero, 1150, 980), 560, 1230)
    lines = text.split("|")
    y = 330
    for i, ln in enumerate(lines):
        bx = words(cv, ln, 540, y, 230, YEL if i == len(lines) - 1 else WHITE, anchor="ma", max_w=980)
        y = bx[3] - 40
    mb = pop(fit(meatball("shock", 1000, look=look, head=0.46), h=400), 8, 8, WHITE, 20)
    cv.alpha_composite(mb, (0, h - mb.height - 60))
    return cv


def t3a():
    hero = actor(B.silverfish, {"mood": "smug", "look": (-0.2, 0.4), "mouth": "grin", "talk": 0.6}, 1.0,
                 2000, 900, 1100, 700)
    hero = pop(hero, 10, 10, (230, 240, 255), 40, (170, 210, 255)).rotate(24, expand=True, resample=Image.BICUBIC)
    return cover("house", 9, hero, "1 YEAR|NO FOOD", look=(14, -14))


def t3b():
    hero = actor(cellar_spider, {"mood": "angry", "fangs": 1.0, "look": (0, 0.5)}, 1.6, 1400, 1300, 700, 60)
    return cover("vs", 1, pop(hero, 8, 8, (255, 236, 180), 36, (255, 210, 120)), "EATS|SPIDERS", look=(14, -14))


def t3c():
    hero = actor(sp(BADGER), {"mood": "angry", "look": (-1, 0.2), "mouth": "grin", "talk": 0.7}, 1.25,
                 2000, 1000, 1000, 850)
    hero = hero.transpose(Image.FLIP_LEFT_RIGHT)
    return cover("survive", 0, pop(hero, 10, 10, (255, 220, 160), 40, (255, 150, 60)), "BAD|IDEA", look=(16, -6))


# ------------------------------------------------------------------ preview sheets

def small(im, w):
    return im.convert("RGB").resize((w, int(w * im.height / im.width)), Image.LANCZOS)


def sheet(items, title_of, out):
    titles = title_of if isinstance(title_of, list) else [title_of] * len(items)
    """Dark YouTube UI: each thumbnail at 640x360 with its 360x202 search-row size and 168x94 mobile-feed size
    under it, title text beside the small ones, as in the feed."""
    vert = items[0][1].height > items[0][1].width
    tw, th = (300, 533) if vert else (640, 360)
    colw = tw + 40
    sh = Image.new("RGB", (40 + colw * len(items), th + (720 if vert else 420)), (15, 15, 15))
    d = ImageDraw.Draw(sh)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17) \
        if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else ImageFont.load_default()
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14) \
        if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") else ImageFont.load_default()
    for i, (name, im) in enumerate(items):
        x = 40 + i * colw
        sh.paste(small(im, tw), (x, 40))
        d.text((x, 12), name, font=fb, fill=(170, 170, 170))
        y = 40 + th + 20
        if vert:   # Shorts shelf (search / channel page) sizes
            for w in (180, 110):
                s = small(im, w)
                sh.paste(s, (x, y))
                d.text((x, y + s.height + 6), titles[i][:26] + "...", font=fr, fill=(241, 241, 241))
                y += s.height + 40
            continue
        s = small(im, 360)
        sh.paste(s, (x, y))
        _dur(d, x + 360, y + s.height, fr)
        y += s.height + 18
        s = small(im, 168)
        sh.paste(s, (x, y))
        _dur(d, x + 168, y + 94, fr)
        lines = _wrap(titles[i], fb, 168 + 250, d)[:2]
        for j, ln in enumerate(lines):
            d.text((x + 180, y + j * 22), ln, font=fb, fill=(241, 241, 241))
        d.text((x + 180, y + 50), "Meatball Myths · 1.2K views · 1 day ago", font=fr, fill=(170, 170, 170))
    sh.save(out, optimize=True)


def _dur(d, xr, yb, f):
    d.rounded_rectangle([xr - 44, yb - 22, xr - 4, yb - 4], 3, fill=(0, 0, 0))
    d.text((xr - 40, yb - 21), "7:42", font=f, fill=WHITE)


def _wrap(text, f, w, d):
    out, cur = [], ""
    for wd in text.split():
        if d.textlength(cur + " " + wd, font=f) > w and cur:
            out.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    return out + [cur]


T1 = "6 Creatures Living In Your House Right Now (You Never See Them)"
T2 = "6 More Creatures Living In Your House (Bed Bugs Are Just the Start)"
CONCEPTS = {"t1a": t1a, "t1b": t1b, "t1c": t1c, "t1d": t1d, "t2a": t2a, "t2b": t2b, "t2c": t2c, "t3a": t3a, "t3b": t3b, "t3c": t3c, "l_ostrich": l_ostrich, "l_lemming": l_lemming, "l_wolf": l_wolf, "l_stick": l_stick,
            "l_wombat": l_wombat, "l_cat": l_cat}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    only = [s for s in a.only.split(",") if s]
    done = {}
    for name, fn in CONCEPTS.items():
        if only and name not in only:
            continue
        im = fn().convert("RGB")
        im.save(os.path.join(a.outdir, name + ".png"), optimize=True)
        for w in ((168, 360) if im.width > im.height else (180, 110)):
            small(im, w).save(os.path.join(a.outdir, f"{name}_{w}.png"))
        done[name] = im
        print("ok", name)
    for group, title in (("t1", T1), ("t2", T2), ("t3", "Things Living In Your House")):
        items = [(n, im) for n, im in done.items() if n.startswith(group)]
        if items:
            sheet(items, title, os.path.join(a.outdir, f"sheet-{group}.png"))
    titles = {c: t for _, t, c in LONGFORMS}
    items = [(n, im) for n, im in done.items() if n.startswith("l_")]
    for k in range(0, len(items), 3):
        sheet(items[k:k + 3], [titles[n] for n, _ in items[k:k + 3]], os.path.join(a.outdir, f"sheet-l{k // 3 + 1}.png"))


if __name__ == "__main__":
    main()
