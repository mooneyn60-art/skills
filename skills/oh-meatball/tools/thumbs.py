#!/usr/bin/env python3
"""Thumbnail system for bug long-forms (Studio 11/18): a huge bug face on the left, Meatball reacting big on the
right, a yellow 2-3 word label, ONE bright background colour on every thumbnail, a small tier-board hint in a
corner. Same drawn bugs and the same Meatball as the videos.

  thumbs.py one --bug centipede --label "GET OUT?" --pose shock OUT.png [--board] [--mark "GET OUT"]
  thumbs.py preset flagship OUTDIR      the 3 Test & Compare thumbnails for "House Bugs Ranked by Meatball"
  thumbs.py preset older OUTDIR         the 4 older bug long-forms, named thumb-<video id>.png
  thumbs.py banner OUTDIR               banner.png (2560x1440) + banner-safe-preview.png
  thumbs.py watermark OUTDIR            watermark-150.png (transparent)
  thumbs.py sheet OUTDIR                brand-sheet.jpg: every output on one page
  thumbs.py list                        bugs and poses

Each PNG is 1280x720 and kept under 2 MB. Every call also writes phone-check/OUT_320.png (the phone-size downscale) and prints
the label's cap height at 320x180 (>= 18 px reads on a phone; the check fails below 14 px).
Rule from the brief: label words never claim more than the video's title says (questions, or the title's words).
"""
import argparse
import math
import os
import sys

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn  # noqa: E402  (registers every actor)
import mascot  # noqa: E402
from drawn_kit import INK, OUT, darker, eyes, hexc, lighter, limb, mouth, p_ellipse, p_smooth, shape, src  # noqa: E402

W, H = 1280, 720
ROOT = os.path.dirname(HERE)
FONT = os.path.join(ROOT, "brand/fonts/Anton-Regular.ttf")
BG = (22, 168, 255)          # THE background colour: bright sky blue, every thumbnail (contrasts brown, tan, red)
YELLOW = (255, 214, 10, 255)
TIERS = [("HARMLESS", (63, 185, 80)), ("ANNOYING", (255, 211, 77)), ("GROSS", (255, 159, 67)),
         ("GET OUT", (229, 56, 59))]   # the flagship's tier names and colours (tools/drawn_ranked.py TIERS/TCOL)


# ================================================================================ close-up bug faces (cairo)

def _banded(ctx, pts, w, col, band):
    limb(ctx, pts, w, col, OUT * 0.9)
    ctx.save()
    p_smooth(ctx, pts, close=False)
    ctx.set_dash([w * 1.5, w * 1.9])
    src(ctx, band)
    ctx.set_line_width(w)
    ctx.stroke()
    ctx.restore()


def centipede_face(ctx, p):
    """House centipede close-up, head at (0, 0) facing screen right: big faceted eyes, long banded antennae,
    many long banded legs fanning out behind, a striped body going back to the lower left, the forcipules
    (the venom claws) under the head. Cartoon, same colours as sp.house_centipede (#cdb27c / #4a3b2c)."""
    col, dk, leg = hexc("#d6bb83"), hexc("#4a3b2c"), hexc("#e6cf9c")
    body = [(-130 - i * 150, 70 + i * 62) for i in range(9)]   # segment centres, head to tail
    for i, (bx, by) in enumerate(body):   # legs: one pair per segment, arching out and down
        for s in (-1, 1):
            reach = 820 + i * 60
            a = math.radians(-118 + i * 4) if s < 0 else math.radians(70 - i * 5)
            mx, my = bx + math.cos(a) * reach * 0.55, by + math.sin(a) * reach * 0.55 - 260
            fx, fy = bx + math.cos(a) * reach - 120, by + math.sin(a) * reach + (120 if s > 0 else -40)
            _banded(ctx, [(bx, by), (mx, my), (fx, fy)], 30, darker(leg, 0.85 if s < 0 else 1.0), dk)
    for i, (bx, by) in reversed(list(enumerate(body))):   # body segments, back to front
        r = 175 - i * 9
        shape(ctx, lambda c, bx=bx, by=by, r=r: p_ellipse(c, bx, by, r, r * 0.78, 0.4), col, OUT, (0.0, 0.18))
        for k in (-1, 0, 1):   # the three dark stripes running down the back
            ctx.save()
            p_ellipse(ctx, bx, by, r, r * 0.78, 0.4)
            ctx.clip()
            ctx.translate(bx, by)
            ctx.rotate(0.4)
            ctx.rectangle(-r, k * r * 0.42 - r * 0.09, 2 * r, r * 0.18)
            src(ctx, dk)
            ctx.fill()
            ctx.restore()
    for s, a0 in ((-1, -150), (1, 35)):   # the first leg pair reaches forward around the head
        a = math.radians(a0)
        _banded(ctx, [(-60, 90), (-60 + math.cos(a) * 300, 90 + math.sin(a) * 300 - 180),
                      (-60 + math.cos(a) * 640 + 200, 90 + math.sin(a) * 640 + 60)], 30, leg, dk)
    for s in (-1, 1):   # antennae: long, banded, sweeping up and out toward Meatball
        sw = 0 if s < 0 else 1
        _banded(ctx, [(60, -150 + 30 * sw), (260, -420 - 60 * sw), (620, -560 - 40 * sw), (1050, -470 + 60 * sw),
                      (1350, -300 + 120 * sw)], 22, leg, dk)
    for s in (-1, 1):   # forcipules: curved claws under the head, dark tips
        shape(ctx, lambda c, s=s: p_smooth(c, [(-10 + s * 60, 120), (60 + s * 120, 230), (40 + s * 70, 320),
                                               (10 + s * 20, 290), (40 + s * 70, 230)]),
              hexc("#7a4a2a"), OUT * 0.9, None)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 225, 185), col, OUT, (0.0, 0.16), hi=(0.32, 0.2, 0.22))   # head
    ctx.save()
    p_ellipse(ctx, 0, 0, 225, 185)
    ctx.clip()
    shape(ctx, lambda c: p_ellipse(c, -40, -150, 120, 60), dk, 0, None)   # dark cap
    ctx.restore()
    mood = p.get("mood", "angry")
    eyes(ctx, 40, -20, 88, 104, look=p.get("look", (0.75, 0.1)), mood=mood, lw=OUT * 0.9, lid=col)
    mouth(ctx, 75, 115, 110, p.get("mouth", "grin"), lw=OUT * 0.9)


def bedbug_face(ctx, p):
    """Bed bug close-up, head at (0, 0) facing screen right: a flat oval mahogany body behind it with fine
    segment lines and short hairs, short jointed legs, 4-part antennae, the beak folded under the head.
    Cartoon, same colours as sp.bed_bug."""
    col, dk, leg = hexc("#9c4524"), hexc("#5e2410"), hexc("#b5643a")
    for s, xs in ((-1, (-520, -330, -140)), (1, (-560, -360, -160))):   # legs (far side darker)
        for i, x in enumerate(xs):
            y = 60 + (230 if s > 0 else -40)
            kx, ky = x + 140 - i * 30, y + (210 if s > 0 else -170)
            fx, fy = kx + 160 + i * 40, ky + (170 if s > 0 else -60)
            limb(ctx, [(x, y), (kx, ky), (fx, fy)], 34, darker(leg, 0.8 if s < 0 else 1.0), OUT * 0.9, smooth=False)
            shape(ctx, lambda c, kx=kx, ky=ky: p_ellipse(c, kx, ky, 22, 22), darker(leg, 0.9), OUT * 0.6, None)
    shape(ctx, lambda c: p_ellipse(c, -560, 180, 520, 360, 0.18), col, OUT, (0.0, 0.18), hi=(0.32, 0.22, 0.24))
    ctx.save()
    p_ellipse(ctx, -560, 180, 520, 360, 0.18)
    ctx.clip()
    ink(ctx, OUT * 0.6)
    for k in range(1, 7):   # abdomen segment lines
        ctx.arc(-1150 + k * 130, 180 + k * 22, 420, math.radians(-38), math.radians(38))
        ctx.stroke()
    ctx.restore()
    shape(ctx, lambda c: p_smooth(c, [(-330, -60), (-120, -170), (60, -120), (120, 60), (40, 200), (-180, 230),
                                       (-360, 170)]), col, OUT, (0.0, 0.15))   # pronotum (wide collar)
    for i in range(14):   # fine hairs on the edge
        a = math.radians(-160 + i * 11)
        x, y = -560 + 520 * math.cos(a) * 0.98, 180 + 360 * math.sin(a) * 0.98
        stroke(ctx, [(x, y), (x + 26 * math.cos(a), y + 26 * math.sin(a))], OUT * 0.5)
    for s in (-1, 1):   # antennae, 4 segments
        pts = [(110, -60 + s * 30), (260, -230 + s * 40), (420, -260 + s * 90), (560, -150 + s * 120),
               (650, -10 + s * 140)]
        limb(ctx, pts, 22, leg, OUT * 0.8, smooth=False)
        for x, y in pts[1:4]:
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 17, 17), leg, OUT * 0.5, None)
    limb(ctx, [(120, 120), (60, 260), (-40, 330)], 24, dk, OUT * 0.8)   # the beak, folded under
    shape(ctx, lambda c: p_ellipse(c, 60, 0, 200, 165), lighter(col, 0.08), OUT, (0.0, 0.16), hi=(0.3, 0.2, 0.22))
    eyes(ctx, 85, -20, 66, 86, look=p.get("look", (0.75, 0.1)), mood=p.get("mood", "angry"), lw=OUT * 0.9,
         lid=lighter(col, 0.08))
    mouth(ctx, 115, 95, 95, p.get("mouth", "grin"), lw=OUT * 0.9)


def ink(ctx, lw):
    src(ctx, INK)
    ctx.set_line_width(lw)


def stroke(ctx, pts, lw):
    from drawn_kit import stroke as _s
    _s(ctx, pts, lw)


SPIDERS = {   # front-view close-up looks: body colour, leg colour, leg bands, leg width, leg length, abdomen size
    "black_widow": dict(col="#1c1c24", leg="#26262f", band=None, lw=36, ll=1.0, abd=(330, 290), eyes=8),
    "wolf_spider": dict(col="#7d5836", leg="#8c6542", band="#4a3220", lw=44, ll=0.95, abd=(300, 250), eyes=8,
                        stripes=True),
    "cellar_spider": dict(col="#dccaa2", leg="#b39a74", band=None, lw=13, ll=1.55, abd=(150, 250), eyes=8,
                          small=0.75),
    "brown_recluse": dict(col="#c09160", leg="#b48552", band=None, lw=30, ll=1.1, abd=(260, 230), eyes=6,
                          violin=True),
}


def spider_face(ctx, p, kind="black_widow"):
    """Spider close-up, head at (0, 0), seen from the front and a little above: abdomen behind the head, eight
    arched legs, the big main eye pair plus the smaller eyes (6 in pairs for the recluse), chelicerae with fangs,
    palps. Cartoon; colours follow the video actors."""
    c = SPIDERS[kind]
    col, leg = hexc(c["col"]), hexc(c["leg"])
    band = hexc(c["band"]) if c.get("band") else None
    k = c.get("small", 1.0)
    ax, ay = c["abd"]
    shape(ctx, lambda cc: p_ellipse(cc, -90, -270, ax, ay, -0.25), col, OUT, (0.0, 0.18),
          hi=(0.3, 0.22, 0.22) if kind == "black_widow" else (0.3, 0.2, 0.18))
    if c.get("stripes"):   # wolf spider: pale mid stripe and side bands
        shape(ctx, lambda cc: p_ellipse(cc, -90, -280, ax * 0.22, ay * 0.8, -0.25), hexc("#c9a97c"), 0, None)
    for side in (-1, 1):   # 8 legs: knee high, foot far out and down
        for i in range(4):
            ll = c["ll"]
            bx, by = side * 150 * k, -40 + i * 40
            kx, ky = side * (330 + i * 70) * ll, (-420 + i * 110) * ll
            fx, fy = side * (720 + i * 60) * ll, (180 + i * 170) * ll
            col_l = darker(leg, 0.8) if i % 2 else leg
            if band is not None:
                _banded(ctx, [(bx, by), (kx, ky), (fx, fy)], c["lw"], col_l, band)
            else:
                limb(ctx, [(bx, by), (kx, ky), (fx, fy)], c["lw"], col_l, OUT * 0.9, smooth=False)
            shape(ctx, lambda cc, kx=kx, ky=ky: p_ellipse(cc, kx, ky, c["lw"] * 0.7, c["lw"] * 0.7), col_l,
                  OUT * 0.6, None)
    shape(ctx, lambda cc: p_ellipse(cc, 0, 0, 235 * k, 200 * k), lighter(col, 0.06), OUT, (0.0, 0.16),
          hi=(0.3, 0.2, 0.22))
    if c.get("violin"):   # the recluse's dark violin: wide end at the eyes, neck pointing back
        shape(ctx, lambda cc: p_smooth(cc, [(-70, -150), (70, -150), (60, -90), (16, -60), (12, 30), (-12, 30),
                                            (-16, -60), (-60, -90)]), hexc("#3e2414"), 0, None)
    for s in (-1, 1):   # palps and chelicerae with fangs
        limb(ctx, [(s * 120 * k, 90 * k), (s * 190 * k, 200 * k), (s * 150 * k, 270 * k)], 30 * k, darker(leg, 0.9),
             OUT * 0.8)
        shape(ctx, lambda cc, s=s: p_ellipse(cc, s * 58 * k, 140 * k, 58 * k, 82 * k), darker(col, 0.85), OUT,
              (0.0, 0.15))
        shape(ctx, lambda cc, s=s: p_smooth(cc, [(s * 70 * k, 200 * k), (s * 40 * k, 285 * k), (s * 8 * k, 300 * k),
                                                (s * 30 * k, 250 * k)]), hexc("#3a1a10"), OUT * 0.7, None)
    small = [(-95, -115), (95, -115), (-150, -60), (150, -60)] if c["eyes"] == 6 else \
        [(-40, -135), (40, -135), (-110, -120), (110, -120), (-165, -55), (165, -55)]
    for x, y in small:   # the smaller eyes: shiny black beads
        shape(ctx, lambda cc, x=x, y=y: p_ellipse(cc, x * k, y * k, 24 * k, 24 * k), INK, OUT * 0.5, None)
        shape(ctx, lambda cc, x=x, y=y: p_ellipse(cc, (x - 7) * k, (y - 8) * k, 7 * k, 7 * k), (1, 1, 1), 0, None)
    eyes(ctx, 0, -10 * k, 64 * k, 78 * k, look=p.get("look", (0.75, 0.1)), mood=p.get("mood", "angry"),
         lw=OUT * 0.9, lid=lighter(col, 0.06))


FACES = {"centipede": centipede_face, "bedbug": bedbug_face}
FACES.update({k: (lambda ctx, p, k=k: spider_face(ctx, p, k)) for k in SPIDERS})

# Bugs with no dedicated face: the video's own drawn actor, zoomed so its front end fills the left half.
# name -> (actor, focus x, focus y as fractions of the actor's ink box, zoom = box widths shown across the panel,
#          extra params)
CROPS = {
    "cockroach": ("sp.roach", 0.7, 0.45, 0.9, {"mood": "angry"}),
}
NAMES = {"centipede": "HOUSE CENTIPEDE", "bedbug": "BED BUG", "black_widow": "BLACK WIDOW",
         "brown_recluse": "BROWN RECLUSE", "wolf_spider": "WOLF SPIDER", "cellar_spider": "CELLAR SPIDER",
         "cockroach": "COCKROACH"}


def _surface_to_rgba(surf, w, h):
    surf.flush()
    a = np.ndarray((h, w, 4), np.uint8, surf.get_data()).copy()
    al = a[..., 3:4].astype(np.float32)
    rgb = np.where(al > 0, a[..., [2, 1, 0]] * 255.0 / np.maximum(al, 1), 0)
    return Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), al], 2).astype(np.uint8), "RGBA")


def bug_layer(bug, size=(860, 720), at=(420, 330), scale=0.62, rot=-6.0, p=None):
    """The bug close-up as a size-px RGBA layer: head (or focus point) at `at`, with a soft drop shadow."""
    w, h = size
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    ctx.translate(*at)
    ctx.rotate(math.radians(rot))
    if bug in FACES:
        ctx.scale(scale, scale)
        FACES[bug](ctx, dict(p or {}))
    else:
        actor, fx, fy, zoom, extra = CROPS[bug]
        rec = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
        c = cairo.Context(rec)
        drawn.ACTORS[actor](c, 0.3, dict({"look": [0.8, 0.1], "walk": 0.0}, **extra, **(p or {})))
        x, y, bw, bh = rec.ink_extents()
        k = w / (bw * zoom) * scale / 0.62
        ctx.scale(k, k)
        ctx.translate(-(x + bw * fx), -(y + bh * fy))
        ctx.set_source_surface(rec, 0, 0)
        ctx.paint()
    im = _surface_to_rgba(surf, w, h)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.45)).filter(ImageFilter.GaussianBlur(16)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (14, 18))
    out.alpha_composite(im)
    return out


# ================================================================================ Meatball, label, board

CUT = {"nervous": 0.5, "shock": 0.55}   # crop at the chest: big face (clasped hands read as a knot when small)


def meatball_layer(pose="shock", height=540, cut=None, look=(-1.0, 0.15), edge=17):
    """Meatball as a white-edged sticker, cropped at the hips (cut = share of his drawn height kept) so his
    face reads big. look aims his eyes at the bug on the left."""
    m = mascot.draw(pose, 1400, look=look)
    bb = m.getchannel("A").getbbox()
    m = m.crop(bb)
    m = m.crop((0, 0, m.width, int(m.height * (cut or CUT.get(pose, 0.66)))))
    k = height / m.height
    m = m.resize((max(1, int(m.width * k)), height), Image.LANCZOS)
    pad = edge + 4
    out = Image.new("RGBA", (m.width + 2 * pad, m.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", out.size, 0)
    a.paste(m.getchannel("A"), (pad, pad))
    white = Image.new("RGBA", out.size, (255, 255, 255, 255))
    out.paste(white, (0, 0), a.filter(ImageFilter.MaxFilter(edge)))
    out.alpha_composite(m, (pad, pad))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.putalpha(out.getchannel("A").point(lambda v: int(v * 0.4)).filter(ImageFilter.GaussianBlur(12)))
    fin = Image.new("RGBA", (out.width + 20, out.height + 20), (0, 0, 0, 0))
    fin.alpha_composite(sh, (14, 16))
    fin.alpha_composite(out)
    return fin


def text_layer(text, px, fill=YELLOW, stroke=14, max_w=None, rot=0.0):
    """Anton caps, thick black outline and a hard drop shadow; shrinks to max_w. Returns (layer, cap height)."""
    while True:
        f = ImageFont.truetype(FONT, px)
        d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
        if not max_w or x1 - x0 <= max_w or px < 40:
            break
        px -= 4
    cap = d.textbbox((0, 0), "H", font=f)[3] - d.textbbox((0, 0), "H", font=f)[1]
    t = Image.new("RGBA", (x1 - x0 + 24, y1 - y0 + 24), (0, 0, 0, 0))
    dr = ImageDraw.Draw(t)
    dr.text((6 - x0 + 10, 6 - y0 + 10), text, font=f, fill=(10, 10, 10, 255), stroke_width=stroke,
            stroke_fill=(10, 10, 10, 255))
    dr.text((6 - x0, 6 - y0), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(10, 10, 10, 255))
    if rot:
        t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    return t, cap


def tier_board(mark=None, w=250, rh=34, gap=5):
    """The tier-board hint: the flagship's four tiers as coloured chips on a dark card. mark = a tier name that
    gets a '?' badge (only for a tier the video really puts that bug in, or none)."""
    f = ImageFont.truetype(FONT, 25)
    hgt = 4 * rh + 3 * gap + 20
    im = Image.new("RGBA", (w + 16, hgt + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 8, w + 8, hgt + 10), 14, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w, hgt), 14, fill=(30, 28, 42, 255), outline=(10, 10, 10, 255), width=4)
    for i, (name, c) in enumerate(TIERS):
        y = 10 + i * (rh + gap)
        d.rounded_rectangle((10, y, 140, y + rh), 8, fill=c + (255,), outline=(10, 10, 10, 255), width=3)
        d.text((75, y + rh / 2 + 1), name, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=3,
               stroke_fill=(10, 10, 10, 255))
        d.rounded_rectangle((148, y, w - 10, y + rh), 8, fill=(58, 54, 76, 255))
        if mark == name:
            d.text((w - 30, y + rh / 2 + 1), "?", font=f, fill=YELLOW, anchor="mm", stroke_width=3,
                   stroke_fill=(10, 10, 10, 255))
    return im.rotate(4, expand=True, resample=Image.BICUBIC)


def backdrop():
    """BG everywhere, a touch lighter behind Meatball and a soft edge vignette; the colour reads the same."""
    y = np.linspace(-1, 1, H)[:, None, None]
    x = np.linspace(-1, 1, W)[None, :, None]
    base = np.array(BG, float)[None, None, :] * np.ones((H, W, 1))
    glow = np.clip(1 - np.sqrt(((x - 0.45) / 1.0) ** 2 + ((y + 0.1) / 1.1) ** 2), 0, 1) ** 1.5
    vig = np.clip(np.sqrt((x / 1.25) ** 2 + (y / 1.15) ** 2) - 0.55, 0, 1)
    im = base + 70 * glow - 70 * vig
    out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).convert("RGBA")
    rays = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(rays)
    cx, cy = 1000, 380
    for k in range(14):
        a0 = math.radians(k * 360 / 14)
        a1 = a0 + math.radians(9)
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a0), cy + 1600 * math.sin(a0)),
                   (cx + 1600 * math.cos(a1), cy + 1600 * math.sin(a1))], fill=26)
    out.paste((255, 255, 255, 255), (0, 0), rays.filter(ImageFilter.GaussianBlur(3)))
    return out


# ================================================================================ compose

FRAMING = {"black_widow": ((400, 400), 0.95), "wolf_spider": ((400, 400), 0.95), "brown_recluse": ((400, 400), 0.95),
           "cellar_spider": ((400, 400), 1.2)}   # head position and scale; default ((430, 350), 0.7)


def make(out, bug, label, pose="shock", board=True, mark=None, bug_p=None, bug_at=None, bug_scale=None,
         bug_rot=-6.0, label_px=176, tag=True):
    at, sc = FRAMING.get(bug, ((430, 350), 0.7))
    bug_at, bug_scale = bug_at or at, bug_scale or sc
    im = backdrop()
    im.alpha_composite(bug_layer(bug, (1100, H), bug_at, bug_scale, bug_rot, bug_p), (-40, 0))
    mb = meatball_layer(pose, 540)
    mx, my = W - mb.width + 6, max(H - mb.height + 26, 196)   # head clear of the label
    im.alpha_composite(mb, (mx, my))
    if pose in ("shock", "nervous"):   # reaction mark by his head, on the bug's side
        t, _ = text_layer("!!" if pose == "shock" else "?", 110, (255, 255, 255, 255), 10, rot=-14)
        im.alpha_composite(t, (mx - t.width + 40, my + 40))
    lab, cap = text_layer(label, label_px, max_w=680, rot=3)
    lx = W - lab.width - 18
    im.alpha_composite(lab, (max(380, lx), 4))
    if board:
        im.alpha_composite(tier_board(mark), (10, 8))
    if tag and bug in NAMES:   # BUG ID-style name chip (drawn_cine.py card colours), bottom left
        f = ImageFont.truetype(FONT, 36)
        name = NAMES[bug]
        d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw = d.textbbox((0, 0), name, font=f)[2]
        chip = Image.new("RGBA", (tw + 40, 58), (0, 0, 0, 0))
        dc = ImageDraw.Draw(chip)
        dc.rounded_rectangle((0, 0, chip.width - 1, 57), 12, fill=(255, 248, 225, 255), outline=(10, 10, 10, 255),
                             width=4)
        dc.text((20, 29), name, font=f, fill=(20, 20, 20, 255), anchor="lm")
        im.alpha_composite(chip.rotate(-3, expand=True, resample=Image.BICUBIC), (22, H - 84))
    return save(im, out, cap * 320 / W)


def save(im, out, cap320):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    rgb = im.convert("RGB")
    rgb.save(out, optimize=True)
    if os.path.getsize(out) > 2_000_000:   # keep under YouTube's 2 MB: 256-colour quantise as a fallback
        rgb.quantize(256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG).save(out, optimize=True)
    small = rgb.resize((320, 180), Image.LANCZOS)
    pc = os.path.join(os.path.dirname(os.path.abspath(out)), "phone-check")
    os.makedirs(pc, exist_ok=True)
    small.save(os.path.join(pc, os.path.basename(out)[:-4] + "_320.png"))
    kb = os.path.getsize(out) / 1024
    ok = "OK" if cap320 >= 14 else "FAIL"
    print(f"{os.path.basename(out)}  {kb:.0f} KB  label cap height at 320x180: {cap320:.1f} px  {ok}")
    return out


# ================================================================================ presets

FLAGSHIP = "House Bugs Ranked by Meatball, From Harmless to Get Out"
PRESETS = {
    "flagship": [   # bed bug is the flagship's GET OUT pick (drawn_ranked.py RANK), so it carries "GET OUT?"
        ("thumb-flagship-A-getout.png", dict(bug="bedbug", label="GET OUT?", pose="shock", mark="GET OUT",
                                             bug_at=(470, 360), bug_scale=0.6, bug_rot=-4)),
        ("thumb-flagship-B-ranked.png", dict(bug="centipede", label="RANKED", pose="shock", mark=None)),
        ("thumb-flagship-C-whichone.png", dict(bug="centipede", label="WHICH ONE?", pose="nervous", mark=None,
                                               bug_p={"mood": "smug"})),
    ],
    "older": [
        # "3 Bugs in Your House You Should Never Kill (And 4 You Must)": house centipede is one of its KEEP bugs
        ("thumb-cH3HCZ8GlHk.png", dict(bug="centipede", label="NEVER KILL?", pose="shock", board=False,
                                       bug_p={"mood": "happy", "mouth": "smile"})),
        # "Bugs in Your House You Should Never Kill: 3 More": wolf spider is in part 2's KEEP pile
        ("thumb-xeAsg5ECpgw.png", dict(bug="wolf_spider", label="3 MORE", pose="nervous", board=False)),
        # "Most Dangerous Bugs in Your House, Ranked": the black widow is its last (17th) creature
        ("thumb-bqij8Ht6SX4.png", dict(bug="black_widow", label="RANKED", pose="shock", board=False)),
        # "Should You Kill the Spider in Your Ceiling Corner?": the cellar spider episode
        ("thumb-KWOM2-mNmww.png", dict(bug="cellar_spider", label="KILL IT?", pose="nervous", board=False)),
    ],
}


# ================================================================================ banner, watermark, sheet

BW, BH = 2560, 1440
SAFE = ((BW - 1546) // 2, (BH - 423) // 2, (BW + 1546) // 2, (BH + 423) // 2)   # all-device safe area


def banner(outdir):
    """2560x1440 channel banner: Meatball scared of a giant house centipede, same blue as the thumbnails. Both
    faces sit in the 423 px desktop strip; all text inside the 1546x423 safe area (checked, not assumed)."""
    y = np.linspace(-1, 1, BH)[:, None, None]
    x = np.linspace(-1, 1, BW)[None, :, None]
    glow = np.clip(1 - np.sqrt((x / 1.0) ** 2 + (y / 0.9) ** 2), 0, 1) ** 1.5
    vig = np.clip(np.sqrt((x / 1.3) ** 2 + (y / 1.1) ** 2) - 0.6, 0, 1)
    im = Image.fromarray(np.clip(np.array(BG, float) + 60 * glow - 60 * vig, 0, 255).astype(np.uint8)).convert("RGBA")
    rays = Image.new("L", (BW, BH), 0)
    d = ImageDraw.Draw(rays)
    cx, cy = BW // 2, BH // 2
    for k in range(18):
        a0 = math.radians(k * 20)
        a1 = a0 + math.radians(10)
        d.polygon([(cx, cy), (cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0)),
                   (cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))], fill=22)
    im.paste((255, 255, 255, 255), (0, 0), rays.filter(ImageFilter.GaussianBlur(4)))
    im.alpha_composite(bug_layer("centipede", (2100, BH), (430, 700), 0.9, -6, {"mood": "angry"}), (-60, 0))
    mb = meatball_layer("shock", 760)
    im.alpha_composite(mb, (BW - mb.width - 60, 470))
    t, _ = text_layer("!!", 150, (255, 255, 255, 255), 12, rot=-14)
    im.alpha_composite(t, (BW - mb.width - 120, 470))
    # text block, fitted to the safe area with a margin
    x0, y0, x1, y1 = SAFE
    l1, _ = text_layer("REAL ANSWERS ABOUT", 112, (255, 255, 255, 255), 10, max_w=1420)
    l2, _ = text_layer("THE BUGS IN YOUR HOUSE", 112, (255, 255, 255, 255), 10, max_w=1420)
    l3, _ = text_layer("NEW VIDEO EVERY WEDNESDAY", 74, YELLOW, 8, max_w=1100)
    gap = 4
    total = l1.height + l2.height + l3.height + 2 * gap + 14
    ty = (y0 + y1) // 2 - total // 2
    half = max(l1.width, l2.width, l3.width) // 2 + 50   # plate hugs the text, clear of Meatball
    plate_box = (BW // 2 - half, ty - 6, BW // 2 + half, ty + total + 10)
    plate = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle(plate_box, 40, fill=(8, 40, 90, 150))
    im.alpha_composite(plate.filter(ImageFilter.GaussianBlur(2)))
    boxes = []
    for lay, extra in ((l1, gap), (l2, gap + 14), (l3, 0)):
        lx = (BW - lay.width) // 2
        im.alpha_composite(lay, (lx, ty))
        boxes.append((lx, ty, lx + lay.width, ty + lay.height))
        ty += lay.height + extra
    for b in boxes:
        assert b[0] >= x0 and b[1] >= y0 and b[2] <= x1 and b[3] <= y1, ("text outside the safe area", b, SAFE)
    out = os.path.join(outdir, "banner.png")
    rgb = im.convert("RGB")
    rgb.save(out, optimize=True)
    if os.path.getsize(out) > 6_000_000:   # YouTube banner limit is 6 MB
        rgb.quantize(256, method=Image.MEDIANCUT).save(out, optimize=True)
    pv = rgb.copy()
    d = ImageDraw.Draw(pv)
    d.rectangle((0, y0, BW - 1, y1), outline=(255, 140, 0), width=6)                  # desktop strip (2560x423)
    d.rectangle(SAFE, outline=(255, 30, 30), width=10)                                 # all-device safe area
    f = ImageFont.truetype(FONT, 44)
    d.text((x0 + 14, y0 + 10), "SAFE AREA 1546x423 (all devices)", font=f, fill=(255, 30, 30), stroke_width=4,
           stroke_fill=(255, 255, 255))
    d.text((20, y0 + 10), "DESKTOP 2560x423", font=f, fill=(255, 140, 0), stroke_width=4, stroke_fill=(10, 10, 10))
    d.text((20, 20), "TV 2560x1440 (full image)", font=f, fill=(255, 255, 255), stroke_width=4,
           stroke_fill=(10, 10, 10))
    for b in boxes:
        d.rectangle(b, outline=(0, 255, 120), width=3)
    pv.save(os.path.join(outdir, "banner-safe-preview.png"), optimize=True)
    print(f"banner.png  {os.path.getsize(out) / 1024:.0f} KB; text boxes {boxes} inside {SAFE}")


def watermark(outdir):
    """150x150 transparent watermark: Meatball's smiling face, white sticker edge, a red SUB pill (subscribe)."""
    S = 600   # draw at 4x, downscale once
    m = mascot.draw("neutral", 1400, look=(0.0, 0.0))
    m = m.crop(m.getchannel("A").getbbox())
    m = m.crop((0, 0, m.width, int(m.height * 0.42)))   # the head
    k = min((S - 70) / m.width, (S - 70) / m.height)
    m = m.resize((int(m.width * k), int(m.height * k)), Image.LANCZOS)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ox, oy = (S - m.width) // 2 - 20, 20
    a = Image.new("L", (S, S), 0)
    a.paste(m.getchannel("A"), (ox, oy))
    im.paste((255, 255, 255, 255), (0, 0), a.filter(ImageFilter.MaxFilter(29)))
    im.alpha_composite(m, (ox, oy))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 118)
    bx0, by0, bx1, by1 = S - 300, S - 170, S - 6, S - 14   # red SUB pill, bottom right (the subscribe cue)
    d.rounded_rectangle((bx0 - 12, by0 - 12, bx1 + 6, by1 + 6), 70, fill=(255, 255, 255, 255))
    d.rounded_rectangle((bx0, by0, bx1, by1), 60, fill=(230, 33, 23, 255), outline=(17, 17, 17, 255), width=10)
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2 + 4), "SUB", font=f, fill=(255, 255, 255, 255), anchor="mm")
    out = os.path.join(outdir, "watermark-150.png")
    im.resize((150, 150), Image.LANCZOS).save(out, optimize=True)
    print(f"watermark-150.png  {os.path.getsize(out) / 1024:.0f} KB")


def sheet(outdir):
    """brand-sheet.jpg: every output on one page (thumbnails at 640x360 with their 320x180 phone check)."""
    names = sorted(f for f in os.listdir(outdir) if f.startswith("thumb-") and f.endswith(".png")
                   and not f.endswith("_320.png"))
    cw = 640 + 20 + 320
    rows = []
    f = ImageFont.truetype(FONT, 26)
    for n in names:
        t = Image.open(os.path.join(outdir, n)).convert("RGB")
        row = Image.new("RGB", (cw, 400), (245, 245, 245))
        row.paste(t.resize((640, 360), Image.LANCZOS), (0, 36))
        row.paste(t.resize((320, 180), Image.LANCZOS), (660, 36))
        ImageDraw.Draw(row).text((0, 2), n + "   (right: phone size 320x180)", font=f, fill=(20, 20, 20))
        rows.append(row)
    cols = 2
    tw = cols * cw + (cols + 1) * 30
    th_rows = (len(rows) + cols - 1) // cols
    bn = Image.open(os.path.join(outdir, "banner-safe-preview.png")).convert("RGB").resize((1280, 720), Image.LANCZOS)
    bb = Image.open(os.path.join(outdir, "banner.png")).convert("RGB").resize((640, 360), Image.LANCZOS)
    wm = Image.open(os.path.join(outdir, "watermark-150.png"))
    H2 = 60 + th_rows * 420 + 800
    sh = Image.new("RGB", (tw, H2), (245, 245, 245))
    d = ImageDraw.Draw(sh)
    d.text((30, 10), "MEATBALL MYTHS BRAND KIT  (thumbnails, banner, watermark)", font=ImageFont.truetype(FONT, 40),
           fill=(20, 20, 20))
    for i, r in enumerate(rows):
        sh.paste(r, (30 + (i % cols) * (cw + 30), 60 + (i // cols) * 420))
    y = 60 + th_rows * 420 + 20
    d.text((30, y), "banner-safe-preview.png", font=f, fill=(20, 20, 20))
    d.text((1340, y), "banner.png", font=f, fill=(20, 20, 20))
    sh.paste(bn, (30, y + 34))
    sh.paste(bb, (1340, y + 34))
    d.text((1340, y + 420), "watermark-150.png (on dark and light)", font=f, fill=(20, 20, 20))
    for j, bgc in enumerate(((30, 30, 30), (230, 230, 230), BG)):
        tile = Image.new("RGB", (170, 170), bgc)
        tile.paste(wm, (10, 10), wm)
        sh.paste(tile, (1340 + j * 190, y + 456))
    out = os.path.join(outdir, "brand-sheet.jpg")
    sh.save(out, quality=88)
    print(f"brand-sheet.jpg  {sh.size}  {os.path.getsize(out) / 1024:.0f} KB")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("one")
    o.add_argument("out")
    o.add_argument("--bug", required=True, choices=sorted(set(FACES) | set(CROPS)))
    o.add_argument("--label", required=True)
    o.add_argument("--pose", default="shock", choices=sorted(mascot.POSES))
    o.add_argument("--board", action="store_true")
    o.add_argument("--mark", choices=[t for t, _ in TIERS])
    o.add_argument("--mood", help="bug face mood: angry, smug, happy, shock, worry")
    pr = sub.add_parser("preset")
    pr.add_argument("name", choices=sorted(PRESETS))
    pr.add_argument("outdir")
    pr.add_argument("--only")
    sub.add_parser("list")
    for c in ("banner", "watermark", "sheet"):
        sub.add_parser(c).add_argument("outdir")
    a = ap.parse_args()
    if a.cmd in ("banner", "watermark", "sheet"):
        os.makedirs(a.outdir, exist_ok=True)
        {"banner": banner, "watermark": watermark, "sheet": sheet}[a.cmd](a.outdir)
        return
    if a.cmd == "list":
        print("bugs:", ", ".join(sorted(set(FACES) | set(CROPS))))
        print("poses:", ", ".join(sorted(mascot.POSES)))
        return
    if a.cmd == "one":
        make(a.out, a.bug, a.label, a.pose, a.board, a.mark, {"mood": a.mood} if a.mood else None)
        return
    for name, kw in PRESETS[a.name]:
        if a.only and a.only not in name:
            continue
        make(os.path.join(a.outdir, name), **kw)


if __name__ == "__main__":
    main()
