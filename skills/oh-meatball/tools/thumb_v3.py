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


def badge(canvas, label, x=18, y=18, h=78, col=YEL, fg=INK):
    """Series badge, top-left: a yellow tag with a little ink house and the part number."""
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(ANTON, int(h * 0.62))
    tw = d.textlength(label, font=f)
    wbox = int(h * 1.05 + tw + h * 0.35)
    d.rounded_rectangle([x, y, x + wbox, y + h], int(h * 0.22), fill=col, outline=INK, width=max(4, h // 14))
    hx, hy, s = x + h * 0.55, y + h * 0.54, h * 0.3
    d.polygon([(hx - s * 1.25, hy - s * 0.05), (hx, hy - s * 1.25), (hx + s * 1.25, hy - s * 0.05)], fill=fg)
    d.rectangle([hx - s * 0.85, hy - s * 0.1, hx + s * 0.85, hy + s * 1.0], fill=fg)
    d.rectangle([hx - s * 0.25, hy + s * 0.3, hx + s * 0.25, hy + s * 1.0], fill=col)
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
    """RIGHT NOW: Meatball in bed at night, blanket to his chin, a house centipede crawling over the blanket at
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
    cv.alpha_composite(cent, (400, 175))
    words(cv, "RIGHT NOW", 1260, -6, 170, YEL, anchor="ra", max_w=560)
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
    """6 HIDING: the house cut open like a doll's house, six creatures in six rooms, a red arrow in."""
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
    words(cv, "6 HIDING", 18, -6, 150, YEL, max_w=480)
    badge(cv, "#1", 1100, 18, 62)
    return cv


# ------------------------------------------------------------------ preview sheets

def small(im, w):
    return im.convert("RGB").resize((w, int(w * im.height / im.width)), Image.LANCZOS)


def sheet(items, title_of, out):
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
                d.text((x, y + s.height + 6), title_of[:26] + "...", font=fr, fill=(241, 241, 241))
                y += s.height + 40
            continue
        s = small(im, 360)
        sh.paste(s, (x, y))
        _dur(d, x + 360, y + s.height, fr)
        y += s.height + 18
        s = small(im, 168)
        sh.paste(s, (x, y))
        _dur(d, x + 168, y + 94, fr)
        lines = _wrap(title_of, fb, 168 + 250, d)[:2]
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
CONCEPTS = {"t1a": t1a, "t1b": t1b, "t1c": t1c, "t1d": t1d}


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
    for group, title in (("t1", T1), ("t2", T2), ("t3", "Silverfish Can Go a Year Without Food")):
        items = [(n, im) for n, im in done.items() if n.startswith(group)]
        if items:
            sheet(items, title, os.path.join(a.outdir, f"sheet-{group}.png"))


if __name__ == "__main__":
    main()
