#!/usr/bin/env python3
""""Don't Kill It" thumbnails: the white-background look small channels in the house-creature niche break out with
(research/70-niche-outliers-1110.md section 4): ONE huge illustrated creature on plain white, a shoe sole coming in
from a top corner about to squish it, 2 to 4 hand-lettered words in black with one accent word in red or blue, and a
hand-drawn arrow at the creature. Nothing else.

    thumb_dontkill.py --creature wolf_spider --headline "DON'T|*KILL* IT!" --shoe tl -o out.jpg
    thumb_dontkill.py --json episodes/thumbs-dontkill/specs.json            (one spec or a list of specs)
    thumb_dontkill.py --json specs.json --only kk2_a                         (render one spec by name)

Every render writes OUT.jpg (1280x720, < 2 MB) and OUT_168.jpg (YouTube's smallest size): LOOK at the _168.

Headline: lines split by "|", the accent word wrapped in *stars* ("DON'T|*KILL* IT!"). Accent colour: red (#e5383b),
blue (#1f6fd1) or any #hex.

Spec keys (JSON; CLI flags map onto the same keys):
  name        output basename (with --out-dir) / label
  out         output path (.jpg)
  creature    {"kind": kit (any animal of the video drawing kit: "cfg" = the episode's stage creature_cfg, "mood") |
               wolf_spider | cellar_spider | house_centipede | egg_case_twig (mantis egg case on a fir twig;
               "ornament": true adds a hanging red glass ball), "box": [x, y, w, h], "rot": deg,
               "zoom": 1.0 (>1 lets legs run off the box/frame), "look": [dx, dy] pupils, "mood": worried | happy}
  headline    "LINE|LINE" with *accent*;  accent: red | blue | #hex;  font: marker | gochi
  text_box    [x0, y0, x1, y1] where the words go (default: right 40% of the frame); text_rot: deg
  shoe        false | {"corner": tl | tr, "size": px sole length, "at": [x, y] toe-in centre, "rot": deg}
  arrow       false | {"from": [x, y], "to": [x, y], "bend": -1..1, "color": "#hex"}
  meatball    false | {"at": [x, y] feet, "h": px tall, "look": [dx, dy]}   (the brand host, arms out)
  shears      false | {"at": [x, y] pivot, "rot": deg (blades point along +x), "size": px, "open": deg}   (pruning shears)
  web         false | true (a few cobweb strands in the top-left corner: cellar spider)
"""
import argparse
import json
import math
import os
import random
import sys

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

W, H = 1280, 720
FONTS = {"marker": os.path.join(ROOT, "brand/fonts/PermanentMarker-Regular.ttf"),
         "gochi": os.path.join(ROOT, "brand/fonts/GochiHand-Regular.ttf")}
ACCENTS = {"red": "#e5383b", "blue": "#1f6fd1"}
INK = (0.08, 0.06, 0.05)
PX_LW = 6.5          # creature outline width in final pixels


# ================================================================= colour + cairo helpers

def hexf(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexi(h):
    return tuple(int(round(v * 255)) for v in hexf(h))


def mix(c, d, k):
    return tuple(a + (b - a) * k for a, b in zip(c, d))


def darker(c, k=0.7):
    return tuple(v * k for v in c)


def lighter(c, k=0.45):
    return mix(c, (1, 1, 1), k)


def src(ctx, c, a=1.0):
    ctx.set_source_rgba(c[0], c[1], c[2], a)


def smooth(ctx, pts, close=True):
    """Catmull-Rom through pts as cubic beziers."""
    n = len(pts)
    ctx.move_to(*pts[0])
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (close or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (close or i + 2 < n) else p2
        ctx.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                     p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if close:
        ctx.close_path()


def ellipse(ctx, cx, cy, rx, ry, rot=0.0):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def part(ctx, path, base, lw, shade=(0.0, 0.0), hi=(), shade_k=0.72, hi_k=0.5, hi_a=0.85, outline=True):
    """The illustrated cel look: flat base, a crescent of shadow on the far side (the body shape shifted by -shade,
    knocked out of a darker fill), soft lighter highlight blobs, then a bold ink outline."""
    ctx.new_path()
    path(ctx)
    src(ctx, base)
    ctx.fill()
    ctx.save()
    ctx.new_path()
    path(ctx)
    ctx.clip()
    if shade != (0.0, 0.0):
        ctx.new_path()
        path(ctx)
        src(ctx, darker(base, shade_k))
        ctx.fill()
        ctx.save()
        ctx.translate(-shade[0], -shade[1])
        ctx.new_path()
        path(ctx)
        src(ctx, base)
        ctx.fill()
        ctx.restore()
    for h in hi:
        ctx.new_path()
        ellipse(ctx, *h)
        src(ctx, lighter(base, hi_k), hi_a)
        ctx.fill()
    ctx.restore()
    if outline:
        ctx.new_path()
        path(ctx)
        src(ctx, INK)
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()


def line(ctx, pts, w, color, a=1.0, cap=cairo.LINE_CAP_ROUND, curve=False):
    ctx.new_path()
    if curve and len(pts) > 2:
        smooth(ctx, pts, close=False)
    else:
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
    src(ctx, color, a)
    ctx.set_line_width(w)
    ctx.set_line_cap(cap)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()


def leg(ctx, pts, widths, base, lw, bands=(), light=(-0.6, -0.8), hairs=0, rng=None):
    """A jointed limb: ink under-stroke, flat fill, a shadow strip on the side away from the light and a thin
    highlight on the lit side (per segment), optional joint bands [(segment index, t, colour, length k)] and hairs."""
    segs = list(zip(pts[:-1], pts[1:], widths))
    for a, b, w in segs:
        line(ctx, [a, b], w + 2 * lw, INK)
    for a, b, w in segs:
        line(ctx, [a, b], w, base)
    lx, ly = light
    for a, b, w in segs:
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        if nx * lx + ny * ly > 0:
            nx, ny = -nx, -ny          # n points away from the light
        sh = [(a[0] + nx * w * 0.24, a[1] + ny * w * 0.24), (b[0] + nx * w * 0.24, b[1] + ny * w * 0.24)]
        line(ctx, sh, w * 0.46, darker(base, 0.7), cap=cairo.LINE_CAP_BUTT)
        h0 = (a[0] + dx * 0.12 - nx * w * 0.2, a[1] + dy * 0.12 - ny * w * 0.2)
        h1 = (a[0] + dx * 0.8 - nx * w * 0.2, a[1] + dy * 0.8 - ny * w * 0.2)
        line(ctx, [h0, h1], w * 0.18, lighter(base, 0.55), a=0.9)
    for si, t, col, k in bands:
        a, b, w = segs[si]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        c0 = (a[0] + dx * t - dx / L * w * k / 2, a[1] + dy * t - dy / L * w * k / 2)
        c1 = (a[0] + dx * t + dx / L * w * k / 2, a[1] + dy * t + dy / L * w * k / 2)
        line(ctx, [c0, c1], w * 0.98, col, cap=cairo.LINE_CAP_BUTT)
    if hairs and rng:
        for a, b, w in segs[:2]:
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            for _ in range(hairs):
                t = rng.uniform(0.15, 0.9)
                s = rng.choice((-1, 1))
                px, py = a[0] + dx * t, a[1] + dy * t
                nx, ny = -dy / L * s, dx / L * s
                r = w / 2 + lw * 0.5
                line(ctx, [(px + nx * r, py + ny * r),
                           (px + nx * (r + w * 0.38) + dx / L * w * 0.3, py + ny * (r + w * 0.38) + dy / L * w * 0.3)],
                     lw * 0.55, INK)


def cartoon_eye(ctx, x, y, r, look, lw, lid=None, brow=None):
    ellipse(ctx, x, y, r, r * 1.08)
    src(ctx, (1, 1, 1))
    ctx.fill_preserve()
    src(ctx, INK)
    ctx.set_line_width(lw)
    ctx.stroke()
    px, py = x + look[0] * r * 0.38, y + look[1] * r * 0.38
    ellipse(ctx, px, py, r * 0.56, r * 0.6)
    src(ctx, INK)
    ctx.fill()
    ellipse(ctx, px - r * 0.2, py - r * 0.24, r * 0.2, r * 0.2)
    src(ctx, (1, 1, 1))
    ctx.fill()
    if brow is not None:      # brow = tilt in radians (+ = worried: inner end up)
        ctx.save()
        ctx.translate(x, y - r * 1.45)
        ctx.rotate(brow)
        line(ctx, [(-r * 0.85, r * 0.12), (0, -r * 0.08), (r * 0.85, r * 0.08)], lw * 1.6, INK, curve=True)
        ctx.restore()


def fuzz(ctx, cx, cy, rx, ry, n, length, lw, rng, start=0, end=2 * math.pi):
    for k in range(n):
        a = start + (end - start) * (k + rng.uniform(-0.3, 0.3)) / n
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        L = length * rng.uniform(0.6, 1.2)
        tilt = rng.uniform(-0.35, 0.35)
        line(ctx, [(x, y), (x + L * math.cos(a + tilt), y + L * math.sin(a + tilt))], lw * 0.6, INK)


# ================================================================= creatures (local units, light from the top left)

def wolf_spider(ctx, o):
    """Top-down, head toward the viewer (down): hairy brown, striped carapace, lance mark on the abdomen, 8 banded
    legs (front pairs reach forward, back pairs back), two big front eyes over a row of four, chelicerae, palps."""
    lw = o["lw"]
    rng = random.Random(7)
    base, dark, pale = hexf("#8d6a43"), hexf("#46301d"), hexf("#d2b07a")
    legc = hexf("#86643f")
    look = o.get("look", (0, 0))
    # legs: hips around the carapace, femur / patella+tibia / metatarsus
    spec = [  # hip (x, y), femur angle, bends, lengths
        ((92, 252), 50, (36, 20), (190, 185, 140)),
        ((118, 190), 10, (34, 16), (185, 175, 130)),
        ((120, 118), -24, (-32, -16), (180, 170, 125)),
        ((96, 52), -60, (-28, -12), (215, 205, 150)),
    ]
    for i in (3, 2, 1, 0):
        (hx, hy), a0, (b1, b2), (l1, l2, l3) = spec[i]
        for s in (-1, 1):
            a = math.radians(a0)
            p0 = (s * hx, hy)
            p1 = (p0[0] + s * l1 * math.cos(a), p0[1] + l1 * math.sin(a))
            a2 = a + math.radians(b1)
            p2 = (p1[0] + s * l2 * math.cos(a2), p1[1] + l2 * math.sin(a2))
            a3 = a2 + math.radians(b2)
            p3 = (p2[0] + s * l3 * math.cos(a3), p2[1] + l3 * math.sin(a3))
            leg(ctx, [p0, p1, p2, p3], (56, 46, 34), legc, lw,
                bands=[(0, 0.55, darker(legc, 0.55), 0.7), (1, 0.45, darker(legc, 0.55), 0.8),
                       (2, 0.5, darker(legc, 0.55), 0.8)], hairs=5, rng=rng)
    # palps
    for s in (-1, 1):
        leg(ctx, [(s * 48, 318), (s * 96, 372), (s * 92, 420)], (30, 26), legc, lw,
            bands=[(1, 0.6, darker(legc, 0.55), 0.8)])
    # abdomen
    ab = lambda c: ellipse(c, 0, -205, 178, 228)
    fuzz(ctx, 0, -205, 178, 228, 70, 22, lw, rng)
    part(ctx, ab, base, lw, shade=(-26, -26), hi=[(-60, -300, 70, 95, -0.4)], hi_a=0.5)
    ctx.save()
    ab(ctx)
    ctx.clip()
    for k in range(26):          # mottling
        ellipse(ctx, rng.uniform(-160, 160), rng.uniform(-420, -10), rng.uniform(10, 26), rng.uniform(8, 18))
        src(ctx, dark, 0.35)
        ctx.fill()
    ctx.new_path()
    smooth(ctx, [(0, -20), (58, -110), (52, -220), (0, -360), (-52, -220), (-58, -110)])
    src(ctx, pale)
    ctx.fill()
    ctx.new_path()
    smooth(ctx, [(0, -30), (40, -110), (34, -215), (0, -330), (-34, -215), (-40, -110)])
    src(ctx, dark)
    ctx.fill()
    for k in range(3):           # chevrons toward the back
        y = -340 - k * 30
        line(ctx, [(-70 + k * 12, y + 22), (0, y - 4), (70 - k * 12, y + 22)], 16, dark)
    ctx.restore()
    # carapace
    car = lambda c: smooth(c, [(0, 330), (78, 312), (138, 232), (156, 128), (132, 36), (64, -6), (0, -12),
                               (-64, -6), (-132, 36), (-156, 128), (-138, 232), (-78, 312)])
    part(ctx, car, base, lw, shade=(-18, -22), hi=[], outline=False)
    ctx.save()
    car(ctx)
    ctx.clip()
    for s in (-1, 1):            # two dark bands either side of a pale mid stripe, pale margins
        ctx.new_path()
        smooth(ctx, [(s * 30, 0), (s * 105, 40), (s * 116, 140), (s * 92, 250), (s * 40, 300), (s * 26, 160)])
        src(ctx, dark)
        ctx.fill()
    for (x, y, rx, ry, r) in [(-50, 70, 40, 80, -0.3)]:
        ellipse(ctx, x, y, rx, ry, r)
        src(ctx, lighter(base, 0.5), 0.35)
        ctx.fill()
    ctx.restore()
    ctx.new_path()
    car(ctx)
    src(ctx, INK)
    ctx.set_line_width(lw)
    ctx.stroke()
    fuzz(ctx, 0, 150, 150, 170, 40, 16, lw, rng, start=-0.2, end=math.pi + 0.2)
    # chelicerae
    for s in (-1, 1):
        part(ctx, lambda c, s=s: ellipse(c, s * 34, 338, 36, 46), darker(base, 0.62), lw, shade=(-6, -8),
             hi=[(s * 34 - 10, 324, 10, 16, 0)], hi_k=0.4)
    # eyes: the two big ones (cartoon), the row of four below, the side pair
    for s in (-1, 1):
        ellipse(ctx, s * 96, 196, 12, 12)
        src(ctx, INK)
        ctx.fill()
    for k in range(4):
        ellipse(ctx, -51 + k * 34, 296, 11, 11)
        src(ctx, INK)
        ctx.fill()
    brow = {"worried": 0.32, "happy": None, "calm": None}.get(o.get("mood", "worried"))
    for s in (-1, 1):
        cartoon_eye(ctx, s * 58, 232, 60, look, lw, brow=None)


def cellar_spider(ctx, o):
    """Pholcus seen from above: small pale peanut body (round carapace + long abdomen), 8 extremely long thin legs
    with dark-and-white knee bands, arched knees. Leg strokes far thicker than life so it reads at phone size."""
    lw = o["lw"]
    look = o.get("look", (0, 0))
    body, mark = hexf("#e0c99a"), hexf("#9a7f58")
    legc = hexf("#a88f68")
    spec = [  # femur angle (deg, from +x toward +y = forward), bend, lengths
        (62, 28, (400, 430, 380)),
        (20, 26, (360, 390, 330)),
        (-22, -24, (340, 360, 310)),
        (-60, -26, (400, 430, 380)),
    ]
    B = o.get("body", 2.1)          # body scale: the real body is tiny; the thumbnail needs it to read
    hips = [(44 * B, 120 * B), (58 * B, 92 * B), (58 * B, 58 * B), (44 * B, 30 * B)]
    for i in (3, 2, 1, 0):
        a0, bend, (l1, l2, l3) = spec[i]
        for s in (-1, 1):
            a = math.radians(a0)
            p0 = (s * hips[i][0], hips[i][1])
            p1 = (p0[0] + s * l1 * math.cos(a), p0[1] + l1 * math.sin(a))
            a2 = a + math.radians(bend)
            p2 = (p1[0] + s * l2 * math.cos(a2), p1[1] + l2 * math.sin(a2))
            a3 = a2 + math.radians(bend * 0.5)
            p3 = (p2[0] + s * l3 * math.cos(a3), p2[1] + l3 * math.sin(a3))
            leg(ctx, [p0, p1, p2, p3], (44, 36, 28), legc, lw,
                bands=[(0, 0.93, hexf("#3b2e22"), 1.5), (1, 0.04, (1, 1, 1), 1.1), (1, 0.96, hexf("#3b2e22"), 1.1),
                       (2, 0.03, (1, 1, 1), 0.9)])
    ctx.save()
    ctx.scale(B, B)
    lw = lw / B
    for s in (-1, 1):   # palps
        leg(ctx, [(s * 26, 170), (s * 52, 205), (s * 48, 236)], (20, 18), legc, lw)
    ab = lambda c: smooth(c, [(0, 10), (70, -30), (92, -150), (80, -290), (0, -350), (-80, -290), (-92, -150),
                              (-70, -30)])
    part(ctx, ab, body, lw, shade=(-14, -14), hi=[(-24, -190, 22, 90, 0)], hi_a=0.7)
    ctx.save()
    ab(ctx)
    ctx.clip()
    for k, y in enumerate((-60, -120, -180, -240, -290)):
        w = 38 - k * 3
        line(ctx, [(-w, y + 16), (0, y - 6), (w, y + 16)], 10, mark, a=0.75)
    ctx.restore()
    car = lambda c: ellipse(c, 0, 92, 82, 88)
    part(ctx, car, body, lw, shade=(-10, -12), hi=[(-26, 70, 22, 26, 0)])
    ctx.save()
    car(ctx)
    ctx.clip()
    ellipse(ctx, 0, 60, 30, 46)
    src(ctx, mark, 0.6)
    ctx.fill()
    ctx.restore()
    brow = {"worried": 0.3, "happy": None, "calm": None}.get(o.get("mood", "happy"))
    for s in (-1, 1):
        cartoon_eye(ctx, s * 38, 124, 36, look, lw * 0.9, brow=None)
    ctx.restore()


def house_centipede(ctx, o):
    """Top-down Scutigera: yellowish-grey body with three dark stripes along it, 15 pairs of very long striped legs
    (longer toward the back, the last pair trailing like a second set of antennae), very long antennae, a cartoon
    face. Head toward +x."""
    lw = o["lw"]
    look = o.get("look", (0, 0))
    rng = random.Random(3)
    base, stripe = hexf("#d4b97f"), hexf("#4f4766")
    legl, legd = hexf("#efe4c8"), hexf("#5d5474")
    n = 15
    x0, x1 = -520, 470

    def spine(u):
        x = x0 + (x1 - x0) * u
        y = 46 * math.sin(math.pi * 1.6 * u + 0.4)
        dy = 46 * math.pi * 1.6 * math.cos(math.pi * 1.6 * u + 0.4) / (x1 - x0)
        L = math.hypot(1, dy)
        return (x, y), (1 / L, dy / L), (-dy / L, 1 / L)

    def width(u):
        return 120 + 90 * math.sin(math.pi * min(1, u * 1.15)) ** 0.6

    # legs (behind the body). Pair k sits at u_k; each leg: hip -> knee (out, slightly forward) -> foot (back)
    for k in range(n):
        u = 0.07 + 0.86 * k / (n - 1)
        (px, py), t, nrm = spine(u)
        w = width(u)
        last = k == 0
        for s in (-1, 1):
            hip = (px + s * nrm[0] * w * 0.45, py + s * nrm[1] * w * 0.45)
            if last:   # the long trailing last pair
                pts = [hip, (hip[0] - 190, hip[1] + s * 120), (hip[0] - 520, hip[1] + s * 190),
                       (hip[0] - 820, hip[1] + s * 150)]
                wd = (20, 17, 14)
            else:
                f = k / (n - 1)                       # 0 = rear .. 1 = front
                reach = 300 + 200 * (1 - f) ** 0.8 + 30 * (k % 2)
                th = -1.3 + 2.2 * f                  # rear legs sweep back, front legs reach forward: a fan

                def d(a):
                    return (s * nrm[0] * math.cos(a) + t[0] * math.sin(a), s * nrm[1] * math.cos(a) + t[1] * math.sin(a))
                d1, d2 = d(th + 0.3), d(th - 0.35)
                kx, ky = hip[0] + d1[0] * reach * 0.48, hip[1] + d1[1] * reach * 0.48
                fx, fy = kx + d2[0] * reach * 0.62, ky + d2[1] * reach * 0.62
                pts = [hip, (kx, ky), (fx, fy)]
                wd = (24, 19)
            nb = 3 if not last else 4
            bands = [(si, (j + 0.5) / nb, legd, 1.1) for si in range(len(wd)) for j in range(nb)]
            leg(ctx, pts, wd, legl, lw * 0.85, bands=bands)
    # antennae
    (hx, hy), t, nrm = spine(1.0)
    for s in (-1, 1):
        ak = o.get("ant", 1.0)          # antenna length (shorten when they would run into the words)
        pts = [(hx + 100, hy + s * 40)] + [(hx + 100 + (dx - 100) * ak, hy + s * 40 + (dy - s * 40) * ak)
                                         for dx, dy in ((300, s * 170), (560, s * 250 - 40), (800, s * 240 - 120))]
        line(ctx, pts, 14 + 2 * lw, INK, curve=True)
        line(ctx, pts, 14, legl, curve=True)
        ctx.save()
        ctx.set_dash([20, 26])
        line(ctx, pts, 14, legd, cap=cairo.LINE_CAP_BUTT, curve=True)
        ctx.restore()
    # body outline from the spine
    us = [i / 40 for i in range(41)]
    top = []
    bot = []
    for u in us:
        (px, py), t, nrm = spine(u)
        w = width(u) * (0.75 if u < 0.04 else 1) / 2
        top.append((px - nrm[0] * w, py - nrm[1] * w))
        bot.append((px + nrm[0] * w, py + nrm[1] * w))
    (tx, ty), t0, _ = spine(0)
    outline_pts = top + [(spine(1)[0][0] + 20, spine(1)[0][1])] + bot[::-1] + [(tx - 30, ty)]
    bodyp = lambda c: smooth(c, outline_pts)
    part(ctx, bodyp, base, lw, shade=(-14, -22), outline=False)
    ctx.save()
    bodyp(ctx)
    ctx.clip()
    for off in (-0.3, 0.0, 0.3):
        pts = []
        for u in us:
            (px, py), t, nrm = spine(u)
            w = width(u)
            pts.append((px + nrm[0] * w * off, py + nrm[1] * w * off))
        line(ctx, pts, 17 if off == 0 else 15, stripe, curve=True)
    for j in range(1, 8):           # 7-8 back plates
        u = j / 8
        (px, py), t, nrm = spine(u)
        w = width(u)
        line(ctx, [(px - nrm[0] * w, py - nrm[1] * w), (px - t[0] * 12, py - t[1] * 12),
                   (px + nrm[0] * w, py + nrm[1] * w)], 6, darker(base, 0.55), curve=True)
    for u in (0.2, 0.45, 0.7):
        (px, py), t, nrm = spine(u)
        ellipse(ctx, px - nrm[0] * 24, py - nrm[1] * 24, 46, 12, math.atan2(t[1], t[0]))
        src(ctx, lighter(base, 0.6), 0.6)
        ctx.fill()
    ctx.restore()
    ctx.new_path()
    bodyp(ctx)
    src(ctx, INK)
    ctx.set_line_width(lw)
    ctx.stroke()
    # forcipules + head
    for s in (-1, 1):
        fp = [(hx + 110, hy + s * 50), (hx + 180, hy + s * 64), (hx + 200, hy + s * 18)]
        line(ctx, fp, 20 + 2 * lw, INK, curve=True)
        line(ctx, fp, 20, hexf("#9a5a2e"), curve=True)
    head = lambda c: ellipse(c, hx + 60, hy, 125, 115)
    part(ctx, head, base, lw, shade=(-12, -16), hi=[(hx + 20, hy - 60, 40, 22, 0)])
    brow = {"worried": 0.3, "happy": None, "calm": None}.get(o.get("mood", "worried"))
    for s in (-1, 1):
        cartoon_eye(ctx, hx + 80, hy + s * 52, 46, look, lw * 0.9, brow=None)


def egg_case_twig(ctx, o):
    """A mantis egg case (ootheca) glued to a short fir twig, drawn horizontal (rotate it with "rot"): dark stem with
    two rows of green needles, a lumpy tan foam case with horizontal ridges, bubbles, highlight and shadow, optional
    red glass ornament hanging from the twig (o["ornament"]). Light from the top left."""
    lw = o["lw"]
    rng = random.Random(11)
    green, wood = hexf("#2f8a4e"), hexf("#5a3a22")
    foam, foam_d, foam_l = hexf("#dcb978"), hexf("#a67c3c"), hexf("#f6e6b8")
    L0, L1 = -470, 470
    stem = [(L0, 60), (L0 / 2, 34), (0, 18), (L1 / 2, 2), (L1, -22)]

    def at(u):          # point and tangent along the stem
        i = min(int(u * 4), 3)
        f = u * 4 - i
        a, b = stem[i], stem[i + 1]
        return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), math.atan2(b[1] - a[1], b[0] - a[0])

    def needles(row):
        n = 14
        for k in range(n):
            u = 0.04 + 0.92 * (k + 0.5 * row) / (n - 0.5)
            (x, y), ang = at(u)
            length = 215 - 70 * u + 25 * math.sin(k * 1.7)
            if row == 0:        # far row: up and forward, darker
                a2 = ang - 0.95 + rng.uniform(-0.08, 0.08)
                col = darker(green, 0.7)
            else:               # near row: down and forward, lighter
                a2 = ang + 0.95 + rng.uniform(-0.08, 0.08)
                col = green
            e = (x + length * math.cos(a2), y + length * math.sin(a2))
            nx, ny = -math.sin(a2), math.cos(a2)
            nd = lambda c: smooth(c, [(x + nx * 24, y + ny * 24), (x + (e[0] - x) * 0.55 + nx * 22, y + (e[1] - y) * 0.55 + ny * 22),
                                      e, (x + (e[0] - x) * 0.55 - nx * 22, y + (e[1] - y) * 0.55 - ny * 22),
                                      (x - nx * 24, y - ny * 24)], close=False)
            ctx.new_path()
            nd(ctx)
            ctx.close_path()
            src(ctx, col)
            ctx.fill_preserve()
            src(ctx, INK)
            ctx.set_line_width(lw)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.stroke()
            line(ctx, [(x + 5, y + 5), (x + (e[0] - x) * 0.75, y + (e[1] - y) * 0.75)], 7, lighter(col, 0.4), a=0.85)
    needles(0)
    # the stem
    line(ctx, stem, 50 + 2 * lw, INK, curve=True)
    line(ctx, stem, 50, wood, curve=True)
    line(ctx, [(x, y + 11) for x, y in stem], 20, darker(wood, 0.6), curve=True, cap=cairo.LINE_CAP_BUTT)
    line(ctx, [(x + 10, y - 13) for x, y in stem[1:4]], 7, lighter(wood, 0.5), a=0.8, curve=True)
    needles(1)
    # ornament: a string hung from the twig's left end, silver cap, red glass ball with a window highlight
    orn = o.get("ornament")
    if orn:
        ox, oy = -330, 400
        sx, sy = at(0.12)[0]
        line(ctx, [(sx, sy + 20), (ox, oy - 120)], 12 + 2 * lw * 0.5, INK)
        line(ctx, [(sx, sy + 20), (ox, oy - 120)], 7, (0.85, 0.8, 0.6))
        part(ctx, lambda c: c.rectangle(ox - 28, oy - 146, 56, 40), hexf("#d9d9d4"), lw, shade=(-6, -8), shade_k=0.75)
        ball = lambda c: ellipse(c, ox, oy, 135, 135)
        part(ctx, ball, hexf("#d8262c"), lw, shade=(-28, -34), shade_k=0.62,
             hi=[(ox - 48, oy - 50, 30, 44, 0.6)], hi_k=0.6, hi_a=0.95)
        ctx.save()
        ball(ctx)
        ctx.clip()
        ellipse(ctx, ox + 60, oy + 64, 50, 22, -0.8)
        src(ctx, (1, 0.7, 0.6), 0.35)
        ctx.fill()
        ctx.restore()
    # the egg case: a lumpy oval, tilted a little, standing on the twig
    cx, cy, rx, ry, tilt = 20, -205, 335, 235, -0.06
    pts = []
    for k in range(30):
        a = 2 * math.pi * k / 30
        r = 1 + 0.05 * math.sin(2 * a + 1) + 0.04 * math.sin(5 * a + 2) + rng.uniform(-0.03, 0.035)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    # glue: foam flowing down onto the stem
    glue = lambda c: smooth(c, [(cx - 210, cy + 190), (cx - 130, 8), (cx + 10, 14), (cx + 150, 2), (cx + 230, cy + 190)])
    part(ctx, glue, foam_d, lw, shade=(0, 0))
    body = lambda c: smooth(c, pts)
    part(ctx, body, foam, lw, shade=(-50, -56), shade_k=0.74, outline=False)
    ctx.save()
    body(ctx)
    ctx.clip()
    ctx.translate(cx, cy)
    ctx.rotate(tilt)
    # horizontal ridges: sagging wavy grooves (read as bands round a barrel) with a light lip under each
    n = 8
    for k in range(n):
        y = -ry * 0.86 + (2 * ry * 0.86) * k / (n - 1)
        sag = 30 * (1 - (abs(y) / ry) ** 2) ** 0.5 + 14
        wv = [(x, y + sag * (1 - (x / (rx + 30)) ** 2) + 7 * math.sin(x / 45 + k * 1.9))
              for x in range(-int(rx) - 30, int(rx) + 31, 30)]
        line(ctx, [(x, yy + 12) for x, yy in wv], 12, foam_l, a=0.8, curve=True)
        line(ctx, wv, 17, foam_d, a=0.95, curve=True)
    # bubbles in the foam
    for k in range(22):
        bx, by = rng.uniform(-rx * 0.9, rx * 0.9), rng.uniform(-ry * 0.85, ry * 0.85)
        br = rng.uniform(12, 24)
        ellipse(ctx, bx, by, br, br * 0.85)
        src(ctx, foam_l, 0.9)
        ctx.fill_preserve()
        src(ctx, foam_d, 0.9)
        ctx.set_line_width(5)
        ctx.stroke()
        ellipse(ctx, bx - br * 0.3, by - br * 0.3, br * 0.28, br * 0.22)
        src(ctx, (1, 1, 1), 0.9)
        ctx.fill()
    ctx.restore()
    # big soft highlight top left, rim shadow bottom right
    ctx.save()
    body(ctx)
    ctx.clip()
    ctx.new_path()
    body(ctx)
    ctx.set_source_rgba(0.45, 0.28, 0.1, 0.4)
    ctx.set_line_width(70)
    ctx.save()
    ctx.translate(-34, -40)
    ctx.new_path()
    ctx.rectangle(-2000, -2000, 4000, 4000)
    body(ctx)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.fill()
    ctx.restore()
    ellipse(ctx, cx - 140, cy - 120, 80, 40, -0.6)
    src(ctx, (1, 1, 0.92), 0.5)
    ctx.fill()
    ellipse(ctx, cx - 190, cy - 20, 22, 40, -0.3)
    src(ctx, (1, 1, 0.92), 0.5)
    ctx.fill()
    ctx.restore()
    ctx.new_path()
    body(ctx)
    src(ctx, INK)
    ctx.set_line_width(lw * 1.1)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()


def kit_animal(ctx, o):
    """Any animal from the video drawing kit (tools/drawn_creatures.py), so a thumbnail can show the episode's own
    cat, dog or bear. o: cfg (the episode's stage creature_cfg), mood (calm, happy, shock, worry, angry, smug,
    sleepy), look [dx, dy], t (pose time)."""
    import drawn_creatures
    cfg = dict(o["cfg"])
    if o.get("mood"):
        cfg["mood"] = o["mood"]
    p = {"look": list(o.get("look", (0, 0)))}
    if o.get("mood"):
        p["mood"] = o["mood"]
    drawn_creatures.build(cfg)(ctx, o.get("t", 0.3), p)


CREATURES = {"wolf_spider": wolf_spider, "cellar_spider": cellar_spider, "house_centipede": house_centipede,
             "egg_case_twig": egg_case_twig, "kit": kit_animal}


# ================================================================= layers

def to_pil(surf):
    surf.flush()
    a = np.ndarray((surf.get_height(), surf.get_width(), 4), np.uint8, surf.get_data()).copy()
    al = a[..., 3:4].astype(np.float32)
    rgb = np.where(al > 0, a[..., [2, 1, 0]] * 255.0 / np.maximum(al, 1), 0)
    return Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), al], 2).astype(np.uint8), "RGBA")


def layer(draw):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    draw(ctx)
    return to_pil(surf)


def creature_layer(c):
    fn = CREATURES[c["kind"]]
    x, y, bw, bh = c.get("box", [40, 150, 760, 540])
    rot = math.radians(c.get("rot", 0))
    o = dict(c)
    lx, ly = c.get("look", (0, 0))      # pupils aim in screen space: undo the creature's rotation
    o["look"] = (lx * math.cos(-rot) - ly * math.sin(-rot), lx * math.sin(-rot) + ly * math.cos(-rot))
    o["lw"] = 10.0
    rec = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
    fn(cairo.Context(rec), o)
    ex, ey, ew, eh = rec.ink_extents()
    cw = abs(ew * math.cos(rot)) + abs(eh * math.sin(rot))
    ch = abs(ew * math.sin(rot)) + abs(eh * math.cos(rot))
    k = min(bw / cw, bh / ch) * c.get("zoom", 1.0)
    o["lw"] = PX_LW / k
    cx, cy = c.get("anchor", (ex + ew / 2, ey + eh / 2))

    def draw(ctx):
        ctx.translate(x + bw / 2, y + bh / 2)
        ctx.rotate(rot)
        ctx.scale(k, k * c.get("squash", 1.0))
        ctx.translate(-cx, -cy)
        fn(ctx, o)
    return layer(draw)


def ground_shadow(im_layer, off=(16, 26), blur=14, a=0.32):
    al = im_layer.getchannel("A").point(lambda v: int(v * a))
    sh = Image.new("RGBA", (W, H), (40, 34, 30, 0))
    sh.putalpha(al.filter(ImageFilter.GaussianBlur(blur)))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(sh, (off[0], off[1]))
    return out


def contact_shadow(box, a=0.22):
    """A soft oval on the floor under the creature's middle (it sits on a surface)."""
    x, y, w, h = box
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((x + w * 0.22, y + h * 0.42, x + w * 0.82, y + h * 0.9), fill=(40, 34, 30, int(255 * a)))
    return sh.filter(ImageFilter.GaussianBlur(40))


# ---------------------------------------------------------------- shoe

SOLE = [(-450, 0), (-432, -96), (-350, -132), (-210, -122), (-60, -132), (120, -168), (300, -176), (420, -128),
        (472, -30), (462, 70), (380, 148), (240, 176), (90, 150), (-60, 104), (-190, 112), (-330, 128), (-428, 92)]


def shoe_draw(ctx, color_sole, color_tread, color_upper):
    lw = 10
    sole = lambda c: smooth(c, SOLE)
    # the shoe's upper, seen past the sole's outer edge (we look at the sole from below, tilted)
    upper = lambda c: smooth(c, [(-450, -60), (-430, -190), (-340, -250), (-180, -236), (-20, -300), (160, -330),
                                 (330, -290), (440, -200), (480, -60), (300, 0), (-300, 0)])
    part(ctx, upper, color_upper, lw, shade=(0, 34), hi=[(40, -270, 200, 30, -0.1)], hi_k=0.35)
    ctx.save()
    upper(ctx)
    ctx.clip()
    line(ctx, [(-430, -150), (-300, -205), (-140, -196), (20, -258), (200, -290), (380, -240), (470, -150)], 16,
         (0.97, 0.96, 0.94))      # toe-cap / foxing stripe
    ctx.restore()
    for k in range(5):          # laces across the top
        x = -150 + k * 70
        line(ctx, [(x, -282 - k * 8), (x + 46, -250 - k * 8)], 14, INK)
        line(ctx, [(x, -282 - k * 8), (x + 46, -250 - k * 8)], 7, (1, 1, 1))
    # midsole rim
    ctx.save()
    ctx.translate(-12, -46)
    part(ctx, sole, (0.97, 0.96, 0.94), lw, shade=(0, 16))
    ctx.restore()
    # outsole + tread
    part(ctx, sole, color_sole, lw, shade=(10, 18), outline=False)
    ctx.save()
    sole(ctx)
    ctx.clip()
    for i in range(-2, 15):     # forefoot: chevron lugs
        x = -40 + i * 38
        if x > 500:
            break
        line(ctx, [(x, -190), (x + 26, -60), (x, 0), (x + 26, 60), (x, 190)], 16, color_tread,
             cap=cairo.LINE_CAP_SQUARE)
    for r in range(4):          # heel: block lugs
        for q in range(4):
            ctx.new_path()
            ctx.rectangle(-440 + q * 66, -120 + r * 62, 44, 42)
            src(ctx, color_tread)
            ctx.fill()
    ctx.new_path()
    ellipse(ctx, -150, 0, 70, 64)       # arch: smooth logo pad
    src(ctx, color_sole)
    ctx.fill()
    ctx.new_path()
    ellipse(ctx, -150, 0, 46, 40)
    src(ctx, lighter(color_sole, 0.25))
    ctx.fill()
    ellipse(ctx, 120, -110, 260, 34, -0.12)   # sheen
    src(ctx, (1, 1, 1), 0.18)
    ctx.fill()
    ctx.restore()
    ctx.new_path()
    sole(ctx)
    src(ctx, INK)
    ctx.set_line_width(lw)
    ctx.stroke()


def shoe_transform(s):
    corner = s.get("corner", "tl")
    size = s.get("size", 480)
    k = size / 920.0
    if corner == "tl":
        at, rot, flip = s.get("at", (240, 100)), s.get("rot", 22), 1
    else:
        at, rot, flip = s.get("at", (W - 240, 100)), s.get("rot", -22), -1
    return at, math.radians(rot), k, flip


def shoe_layers(s):
    at, rot, k, flip = shoe_transform(s)
    cols = (hexf(s.get("sole", "#5b7fbd")), hexf(s.get("tread", "#33507f")), hexf(s.get("upper", "#e0603a")))

    def place(ctx):
        ctx.translate(*at)
        ctx.rotate(rot)
        ctx.scale(k * flip, k)

    def draw(ctx):
        place(ctx)
        shoe_draw(ctx, *cols)

    def shadow(ctx):
        sx, sy = s.get("shadow", (120, 200))
        ctx.translate(sx * flip, sy)
        place(ctx)
        ctx.scale(0.9, 0.82)
        smooth(ctx, SOLE)
        src(ctx, (0.12, 0.1, 0.1), 1)
        ctx.fill()
    sh = layer(shadow)
    sh.putalpha(sh.getchannel("A").point(lambda v: int(v * s.get("shadow_a", 0.40))).filter(ImageFilter.GaussianBlur(26)))
    return layer(draw), sh


# ---------------------------------------------------------------- pruning shears

def shears_draw(ctx, open_deg=14):
    """Bypass pruning shears, pivot at the origin, blades toward +x (about 640 long), handles toward -x (about 520)."""
    lw = 10
    o = math.radians(open_deg)
    steel, steel_d = hexf("#c9d3dc"), hexf("#7d8a96")
    red, red_d = hexf("#d8262c"), hexf("#8f1519")
    for sgn, hcol in ((-1, red), (1, hexf("#e9892b"))):       # handles (behind the blades)
        ctx.save()
        ctx.rotate(sgn * (o + 0.06) + math.pi)
        hp = lambda c: smooth(c, [(0, -34), (200, -46), (500, -40), (540, 0), (500, 40), (200, 46), (0, 34)])
        part(ctx, hp, hcol, lw, shade=(0, 14), hi=[(250, -20, 170, 10, 0)], hi_k=0.5)
        ctx.restore()
    for sgn in (-1, 1):                                            # blades
        ctx.save()
        ctx.rotate(sgn * o)
        if sgn < 0:
            bp = lambda c: smooth(c, [(-30, -34), (200, -52), (470, -44), (650, 0), (460, 8), (200, 22), (-30, 34)])
        else:
            bp = lambda c: smooth(c, [(-30, -34), (200, -22), (470, -8), (650, 0), (470, 44), (200, 52), (-30, 34)])
        part(ctx, bp, steel, lw, shade=(0, 12 * -sgn), hi=[(300, -16 * sgn, 190, 7, 0)], hi_k=0.6, shade_k=0.8)
        ctx.restore()
    ellipse(ctx, 0, 0, 34, 34)
    src(ctx, steel_d)
    ctx.fill_preserve()
    src(ctx, INK)
    ctx.set_line_width(lw)
    ctx.stroke()
    ellipse(ctx, -8, -8, 10, 10)
    src(ctx, (1, 1, 1), 0.7)
    ctx.fill()


def shears_layers(s):
    at, rot, k = s.get("at", (330, 120)), math.radians(s.get("rot", 30)), s.get("size", 1000) / 1170.0

    def place(ctx):
        ctx.translate(*at)
        ctx.rotate(rot)
        ctx.scale(k, k)

    def draw(ctx):
        place(ctx)
        shears_draw(ctx, s.get("open", 14))

    def shadow(ctx):
        sx, sy = s.get("shadow", (40, 70))
        ctx.translate(sx, sy)
        place(ctx)
        ctx.new_path()
        ctx.rectangle(-540, -48, 1190, 96)
        src(ctx, (0.12, 0.1, 0.1), 1)
        ctx.fill()
    sh = layer(shadow)
    sh.putalpha(sh.getchannel("A").point(lambda v: int(v * s.get("shadow_a", 0.35))).filter(ImageFilter.GaussianBlur(22)))
    return layer(draw), sh


# ---------------------------------------------------------------- Meatball

def meatball_layer(m):
    import mascot
    st = mascot.pose_state("shock")
    st["l"], st["r"] = (112, 4, 0), (112, 4, 0)     # arms straight out: "stop!"
    st["mouth"], st["brow"] = m.get("mouth", "o"), m.get("brow", "up")
    st["look"] = tuple(m.get("look", (0, -0.6)))
    st["blink"] = 0
    h = m.get("h", 260)
    size = int(h / 0.86)
    img = mascot.render(st, size)
    bb = img.getbbox()
    img = img.crop(bb)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fx, fy = m.get("at", (520, 640))
    out.alpha_composite(img, (int(fx - img.width / 2), int(fy - img.height)))
    halo = out.getchannel("A").filter(ImageFilter.MaxFilter(9))     # white sticker edge so he separates
    wh = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    wh.putalpha(halo)
    wh.alpha_composite(out)
    return wh


# ---------------------------------------------------------------- lettering

def parse_headline(s):
    lines = []
    for ln in s.split("|"):
        words = []
        for w in ln.split():
            acc = w.startswith("*") or w.endswith("*")
            words.append((w.strip("*"), acc))
        lines.append(words)
    return lines


def letter_line(words, font, accent, rng, size, wobble=1.0, bold=0.028):
    """One hand-lettered line: each glyph jittered in angle and baseline, a thick white halo behind."""
    asc, desc = font.getmetrics()
    space = font.getlength(" ") * 1.25 + size * 0.06
    glyphs = []
    x = 0.0
    for wi, (w, acc) in enumerate(words):
        for ch in w:
            glyphs.append((ch, x, acc))
            x += font.getlength(ch) * 0.97
        x += space
    width = int(x - space + size * 0.4)
    hgt = int((asc + desc) * 1.25)
    im = Image.new("RGBA", (width + 40, hgt + 40), (0, 0, 0, 0))
    fat = int(round(size * bold))          # faux bold: the marker drawn twice as thick (reads at 168 px)
    halo = int(max(6, size * 0.07)) + fat
    for pass_ in (0, 1):
        for (ch, gx, acc), seed in zip(glyphs, range(len(glyphs))):
            g = random.Random(seed * 7 + int(size))
            ang = g.uniform(-4, 4) * wobble
            dy = g.uniform(-0.035, 0.035) * size * wobble
            sc = 1 + g.uniform(-0.03, 0.05) * wobble
            f = font.font_variant(size=int(size * sc))
            gw = int(f.getlength(ch)) + 2 * halo + 20
            gi = Image.new("RGBA", (gw, hgt + 2 * halo), (0, 0, 0, 0))
            d = ImageDraw.Draw(gi)
            col = hexi(accent) if acc else (17, 17, 17)
            if pass_ == 0:
                d.text((halo + 10, halo), ch, font=f, fill=(255, 255, 255, 255), stroke_width=halo,
                       stroke_fill=(255, 255, 255, 255))
            else:
                d.text((halo + 10, halo), ch, font=f, fill=col + (255,), stroke_width=fat, stroke_fill=col + (255,))
            gi = gi.rotate(ang, resample=Image.BICUBIC, expand=False)
            im.alpha_composite(gi, (int(20 + gx - halo - 10), int(20 + dy - halo + (size - f.size) * 0.6)))
    return im.crop(im.getbbox())


def lettering(spec, rng):
    lines = parse_headline(spec["headline"])
    accent = ACCENTS.get(spec.get("accent", "red"), spec.get("accent", "red"))
    if not str(accent).startswith("#"):
        accent = "#" + accent
    x0, y0, x1, y1 = spec.get("text_box", [770, 60, 1250, 520])
    bw, bh = x1 - x0, y1 - y0
    fpath = FONTS.get(spec.get("font", "marker"), spec.get("font"))
    gap = spec.get("line_gap", -0.12)
    size = spec.get("max_size", 240)
    while size > 30:
        font = ImageFont.truetype(fpath, size)
        ls = spec.get("line_scale") or [1.0] * len(lines)     # e.g. [1.4, 1]: one line bigger than the rest
        imgs = []
        for ln, k in zip(lines, ls):
            f = font if k == 1 else ImageFont.truetype(fpath, int(size * k))
            imgs.append(letter_line(ln, f, accent, rng, int(size * k), spec.get("wobble", 1.0),
                                    spec.get("bold", 0.014)))
        tw = max(i.width for i in imgs)
        th = sum(i.height for i in imgs) + gap * size * (len(imgs) - 1)
        if tw <= bw and th <= bh:
            break
        size = int(size * min(0.97, max(0.8, min(bw / tw, bh / th) ** 0.5)))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = y0 + (bh - th) / 2 if spec.get("valign", "middle") == "middle" else y0
    align = spec.get("align", "center")
    for i, im in enumerate(imgs):
        if align == "center":
            x = x0 + (bw - im.width) / 2
        elif align == "left":
            x = x0
        else:
            x = x1 - im.width
        off = spec.get("line_offsets", [0] * len(imgs))[i] if spec.get("line_offsets") else 0
        out.alpha_composite(im, (int(x + off), int(y)))
        y += im.height + gap * size
    rot = spec.get("text_rot", -3)
    if rot:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        out = out.rotate(rot, resample=Image.BICUBIC, center=(cx, cy))
    return out


# ---------------------------------------------------------------- arrow

def arrow_layer(a, rng):
    (sx, sy), (tx, ty) = a["from"], a["to"]
    bend = a.get("bend", 0.35)
    col = hexf(a.get("color", "#111111"))
    wmax = a.get("width", 13)
    dx, dy = tx - sx, ty - sy
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    c1 = (sx + dx * 0.3 + nx * L * bend, sy + dy * 0.3 + ny * L * bend)
    c2 = (sx + dx * 0.75 + nx * L * bend * 0.6, sy + dy * 0.75 + ny * L * bend * 0.6)
    ph = rng.uniform(0, 6)

    def bez(t):
        mt = 1 - t
        return (mt ** 3 * sx + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * tx,
                mt ** 3 * sy + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * ty)
    pts = []
    N = 60
    for i in range(N + 1):
        t = i / N
        x, y = bez(t)
        wob = 2.2 * math.sin(t * 9 + ph) + 1.2 * math.sin(t * 23 + ph * 2)
        pts.append((x + nx * wob, y + ny * wob))

    def draw(ctx):
        for i in range(N):
            t = i / N
            w = wmax * (0.55 + 0.45 * math.sin(math.pi * min(1, t * 1.25)) ** 0.7) * (0.95 + 0.1 * math.sin(t * 17))
            line(ctx, [pts[i], pts[i + 1]], w, col)
        # two-stroke arrowhead
        ex, ey = pts[-1]
        bx, by = pts[-6]
        ang = math.atan2(ey - by, ex - bx)
        for s, ln, da in ((1, 70, 0.52), (-1, 60, 0.46)):
            a2 = ang + math.pi + s * da
            mid = (ex + math.cos(a2 + s * 0.05) * ln * 0.5, ey + math.sin(a2 + s * 0.05) * ln * 0.5)
            end = (ex + math.cos(a2) * ln, ey + math.sin(a2) * ln)
            line(ctx, [(ex, ey), mid, end], wmax * 1.05, col, curve=True)
    lay = layer(draw)
    wh = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    wh.putalpha(lay.getchannel("A").filter(ImageFilter.MaxFilter(7)))
    wh.alpha_composite(lay)
    return wh


# ---------------------------------------------------------------- cobweb

def web_layer(w):
    def draw(ctx):
        ox, oy = w.get("origin", (0, 0))
        rng = random.Random(5)
        angs = [math.radians(a) for a in (8, 26, 45, 64, 82)]
        R = w.get("r", 420)
        for a in angs:
            line(ctx, [(ox, oy), (ox + R * math.cos(a), oy + R * math.sin(a))], 2.5, (0.62, 0.62, 0.66), a=0.8)
        for r in range(60, R, 62):
            pts = [(ox + r * math.cos(a) * rng.uniform(0.95, 1.03), oy + r * math.sin(a) * rng.uniform(0.95, 1.03))
                   for a in angs]
            for p, q in zip(pts[:-1], pts[1:]):
                m = ((p[0] + q[0]) / 2 - 8 * math.cos((angs[0] + angs[-1]) / 2),
                     (p[1] + q[1]) / 2 - 8 * math.sin((angs[0] + angs[-1]) / 2))
                line(ctx, [p, m, q], 2.2, (0.62, 0.62, 0.66), a=0.75, curve=True)
    return layer(draw)


# ================================================================= compose + save

def render(spec):
    rng = random.Random(spec.get("seed", 1))
    bg = spec.get("bg", "#ffffff")
    im = Image.new("RGBA", (W, H), hexi(bg) + (255,))
    if spec.get("web"):
        im.alpha_composite(web_layer(spec["web"] if isinstance(spec["web"], dict) else {}))
    c = spec["creature"]
    cl = creature_layer(c)
    im.alpha_composite(contact_shadow(c.get("box", [40, 150, 760, 540]), c.get("contact", 0.18)))
    im.alpha_composite(ground_shadow(cl, tuple(c.get("shadow_off", (14, 22))), 12, c.get("shadow_a", 0.30)))
    im.alpha_composite(cl)
    m = spec.get("meatball")
    shoe = spec.get("shoe")
    if shoe:
        sl, ssh = shoe_layers(shoe)
        im.alpha_composite(ssh)
    if m:
        ml = meatball_layer(m)
        im.alpha_composite(ground_shadow(ml, (10, 14), 8, 0.25))
        im.alpha_composite(ml)
    if shoe:
        im.alpha_composite(sl)
    if spec.get("shears"):
        shl, shsh = shears_layers(spec["shears"])
        im.alpha_composite(shsh)
        im.alpha_composite(shl)
    if spec.get("arrow"):
        im.alpha_composite(arrow_layer(spec["arrow"], rng))
    im.alpha_composite(lettering(spec, rng))
    return im.convert("RGB")


def save(im, out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    q = 92
    while True:
        im.save(out, quality=q, optimize=True)
        if os.path.getsize(out) < 2_000_000 or q < 60:
            break
        q -= 6
    stem = out[:-4] if out.lower().endswith(".jpg") else out
    small = im.resize((168, 94), Image.LANCZOS)
    small.save(stem + "_168.jpg", quality=92)
    return out, os.path.getsize(out)


def _label_font(px):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONTS["marker"]):
        if os.path.exists(f):
            return ImageFont.truetype(f, px)
    return ImageFont.load_default()


def contact(paths, out_dir, compare=(), prefix=""):
    """contact.jpg: every thumbnail 3-up at 640x360 with its name; contact_168.jpg: every thumbnail at YouTube's
    smallest size (168x94, 1:1 pixels) on a mid-grey feed-like background, next to the comparison thumbs."""
    names = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    cols, tw, th, pad, lab = 3, 640, 360, 16, 34
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    f = _label_font(22)
    for i, (p, n) in enumerate(zip(paths, names)):
        x, y = pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + lab + pad)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + lab))
        d.text((x, y + 4), n, font=f, fill=(235, 235, 235))
    sheet.save(os.path.join(out_dir, prefix + "contact.jpg"), quality=90)
    tiles = [(p, n) for p, n in zip(paths, names)] + [(p, "OLD " + os.path.splitext(os.path.basename(p))[0])
                                                      for p in compare]
    cols, tw, th, pad, lab = 5, 168, 94, 18, 16
    rows = (len(paths) + cols - 1) // cols + (len(compare) + cols - 1) // cols
    sm = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad + 22), (113, 113, 113))
    d = ImageDraw.Draw(sm)
    f = _label_font(11)
    d.text((pad, 6), "168x94 (YouTube's smallest size), 1:1 pixels. Last row: current thumbnails.", font=f,
           fill=(240, 240, 240))
    for i, (p, n) in enumerate(tiles):
        r = i // cols if i < len(paths) else (len(paths) + cols - 1) // cols + (i - len(paths)) // cols
        c = i % cols if i < len(paths) else (i - len(paths)) % cols
        x, y = pad + c * (tw + pad), 22 + pad + r * (th + lab + pad)
        sm.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 3), n, font=f, fill=(245, 245, 245))
    sm.save(os.path.join(out_dir, prefix + "contact_168.jpg"), quality=92)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", help="spec file (one spec or a list)")
    ap.add_argument("--only", help="render only the spec with this name")
    ap.add_argument("--out-dir", help="with --json: write NAME.jpg here (overrides spec 'out')")
    ap.add_argument("-o", "--out", default="thumb.jpg")
    ap.add_argument("--creature", default="wolf_spider", choices=sorted(CREATURES))
    ap.add_argument("--headline", default="DON'T|*KILL* IT!")
    ap.add_argument("--accent", default="red")
    ap.add_argument("--font", default="marker", choices=sorted(FONTS))
    ap.add_argument("--shoe", default="tl", choices=["tl", "tr", "off"])
    ap.add_argument("--no-arrow", action="store_true")
    ap.add_argument("--meatball", action="store_true", help="small Meatball, arms out, between shoe and creature")
    ap.add_argument("--contact", metavar="DIR", help="with --json: also write DIR/contact.jpg + contact_168.jpg")
    ap.add_argument("--contact-prefix", default="", help="with --contact: file prefix, e.g. xmas_ -> xmas_contact.jpg")
    ap.add_argument("--compare", nargs="*", default=[], help="existing thumbs to show in contact_168.jpg")
    a = ap.parse_args()
    if a.json:
        specs = json.load(open(a.json))
        specs = specs if isinstance(specs, list) else [specs]
        done = []
        for s in specs:
            if a.only and s.get("name") != a.only:
                continue
            out = os.path.join(a.out_dir, s["name"] + ".jpg") if a.out_dir else s["out"]
            if not os.path.isabs(out) and not a.out_dir:
                out = os.path.join(os.path.dirname(os.path.abspath(a.json)), out)
            print(*save(render(s), out))
            done.append(out)
        if a.contact:
            contact(done, a.contact, a.compare, a.contact_prefix)
            print(os.path.join(a.contact, a.contact_prefix + "contact.jpg"),
                  os.path.join(a.contact, a.contact_prefix + "contact_168.jpg"))
        return
    spec = {"creature": {"kind": a.creature, "box": [30, 140, 760, 560], "rot": -8, "look": [-0.6, -0.7]},
            "headline": a.headline, "accent": a.accent, "font": a.font,
            "shoe": False if a.shoe == "off" else {"corner": a.shoe},
            "arrow": False if a.no_arrow else {"from": [880, 560], "to": [640, 520], "bend": -0.35},
            "meatball": {"at": [260, 600], "h": 220} if a.meatball else False}
    if a.shoe == "tr":
        spec["creature"]["box"] = [480, 150, 780, 560]
        spec["text_box"] = [30, 60, 520, 520]
        spec["arrow"] = False if a.no_arrow else {"from": [380, 560], "to": [620, 540], "bend": 0.35}
    print(*save(render(spec), a.out))


if __name__ == "__main__":
    main()
