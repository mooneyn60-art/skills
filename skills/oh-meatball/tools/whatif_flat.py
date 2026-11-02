#!/usr/bin/env python3
"""What If, flat-vector style (the @vibecodingiseasy / @totheru format): every frame drawn in code.

Dark navy palette with one warm accent, a faceless second-person "YOU" (blue shirt, seen from behind or as feet),
a new full-screen composition every <= 2.1 s with a slow camera push, flat bug silhouettes that crawl and hover,
a serif title on the opening shots, a top-left "DAYS WITHOUT CLEANING" readout that rolls up continuously,
2-3 word captions with one yellow key word, and a two-tone end card (tiny Meatball cameo for branding).

Usage: whatif_flat.py OUTLINE.yaml --cut tt|yt --out OUT.mp4 --work DIR
  outline: scripts/drawn-house/outlines/*.yaml (the lines are the first value of each yt/tt item, "counter" = day)
  shot plan: PLANS[slug][cut] below, one entry per line: a list of shot names (cycled, re-framed, when a line is
  longer than MAX_SHOT per shot). Voice: Kokoro onyx (free_voice). Music: music.render bed, rising into each day
  tick, a soft whoosh on every tick. Writes WORK/screen.json and runs screengate on it.
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import subprocess
import sys
import wave

import cv2
import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

W, H, FPS, SR = 1080, 1920, 30, 48000
Z = 1.10                       # base canvas headroom for the push
OX, OY = int(W * (Z - 1) / 2), int(H * (Z - 1) / 2)
SS = 2                         # supersampling for base scenes
MAX_SHOT = 2.1
GAP = 0.22
TEMPO = 1.12                   # onyx reads slow: atempo keeps the pitch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf"

N0, N1, N2, N3, N4 = (9, 14, 28), (17, 27, 52), (27, 42, 76), (41, 62, 108), (66, 92, 142)
YEL, RED, SKIN, SHIRT, HAIR = (255, 211, 77), (232, 69, 60), (226, 160, 122), (60, 108, 182), (46, 32, 26)
STEEL, CREAM = (112, 132, 168), (226, 230, 240)
DAYMESS = {1: 0, 3: 1, 7: 2, 30: 3, 365: 4}


def F(kind, size):
    return ImageFont.truetype(kind, int(size))


# ------------------------------------------------------------------ pen (design coords 1080x1920 + headroom)
class Pen:
    def __init__(self, bg=N1):
        self.im = Image.new("RGB", ((W + 2 * OX) * SS, (H + 2 * OY) * SS), bg)
        self.d = ImageDraw.Draw(self.im, "RGBA")

    def P(self, x, y):
        return ((x + OX) * SS, (y + OY) * SS)

    def rect(self, x0, y0, x1, y1, c, r=0, oc=None, ow=0):
        a, b = self.P(x0, y0), self.P(x1, y1)
        self.d.rounded_rectangle([a, b], radius=r * SS, fill=c, outline=oc, width=int(ow * SS))

    def ell(self, cx, cy, rx, ry, c, oc=None, ow=0):
        self.d.ellipse([self.P(cx - rx, cy - ry), self.P(cx + rx, cy + ry)], fill=c, outline=oc, width=int(ow * SS))

    def poly(self, pts, c):
        self.d.polygon([self.P(*p) for p in pts], fill=c)

    def line(self, pts, c, w):
        self.d.line([self.P(*p) for p in pts], fill=c, width=max(1, int(w * SS)), joint="curve")

    def text(self, x, y, s, font, size, c, anchor="mm", spacing=0):
        f = F(font, size * SS)
        if not spacing:
            self.d.text(self.P(x, y), s, font=f, fill=c, anchor=anchor)
            return
        ws = [self.d.textlength(ch, font=f) + spacing * SS for ch in s]
        tot = sum(ws) - spacing * SS
        px = self.P(x, y)[0] - (tot / 2 if anchor[0] == "m" else 0)
        for ch, w_ in zip(s, ws):
            self.d.text((px, self.P(x, y)[1]), ch, font=f, fill=c, anchor="l" + anchor[1])
            px += w_

    def full(self, c):
        self.rect(-OX - 5, -OY - 5, W + OX + 5, H + OY + 5, c)

    def vgrad(self, y0, y1, c0, c1, n=28):
        for i in range(n):
            u = i / (n - 1)
            c = tuple(int(c0[k] + (c1[k] - c0[k]) * u) for k in range(3))
            a, b = y0 + (y1 - y0) * i / n, y0 + (y1 - y0) * (i + 1) / n + 1
            self.rect(-OX - 5, a, W + OX + 5, b, c)

    def glow(self, cx, cy, r, c, a=40, n=6):
        for i in range(n):
            rr = r * (1 - i / n)
            self.ell(cx, cy, rr, rr, c + (a,))

    def sprite(self, kind, L, x, y, ang=0, phase=0):
        im = bug_img(kind, L * SS, phase, ang)
        px, py = self.P(x, y)
        self.im.paste(im, (int(px - im.width / 2), int(py - im.height / 2)), im)

    def done(self):
        return np.asarray(self.im.resize((W + 2 * OX, H + 2 * OY), Image.LANCZOS))


# ------------------------------------------------------------------ bugs (head up, length L px)
def _rell(cx, cy, rx, ry, ang, n=28):
    a = math.radians(ang)
    return [(cx + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a),
             cy + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a))
            for t in [2 * math.pi * i / n for i in range(n)]]


_BUG = {}


def bug_img(kind, L, phase=0, ang=0):
    key = (kind, int(L), phase, int(round(ang / 15)) * 15 % 360)
    if key in _BUG:
        return _BUG[key]
    wide = 2.6 if kind == "centipede" else 2.0
    ss = max(1, min(3, int(600 / max(L, 1)) + 1))
    S = int(L * wide * ss)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    k, c0 = L * ss / 100, S / 2
    P = lambda x, y: (c0 + x * k, c0 + y * k)
    E = lambda x, y, rx, ry, col: d.ellipse([P(x - rx, y - ry), P(x + rx, y + ry)], fill=col)
    Ln = lambda pts, col, w: d.line([P(*p) for p in pts], fill=col, width=max(1, int(w * k)), joint="curve")
    Pg = lambda pts, col: d.polygon([P(*p) for p in pts], fill=col)
    sw = 1 if phase else -1

    def legs(ys, reach, col, w, bend=1.0):
        for side in (-1, 1):
            for j, y in enumerate(ys):
                s = sw * (1 if j % 2 else -1) * side
                a = (-55 + 55 * j + 10 * s) * bend
                r = math.radians(a)
                k1 = (side * reach * 0.55 * math.cos(r * 0.4), y + reach * 0.35 * math.sin(r))
                k2 = (side * reach * math.cos(r * 0.2) * 0.95, y + reach * 0.75 * math.sin(r) + reach * 0.15)
                Ln([(side * 4, y), k1, k2], col, w)

    if kind in ("fruitfly", "deadfly"):
        dk = (70, 45, 25)
        legs([-12, -4, 4], 24, dk, 2.2)
        Ln([(-4, -32), (-10, -40)], dk, 2)
        Ln([(4, -32), (10, -40)], dk, 2)
        Pg(_rell(-17, 8, 11, 31, -22 - 14 * phase), (205, 218, 240, 140))
        Pg(_rell(17, 8, 11, 31, 22 + 14 * phase), (205, 218, 240, 140))
        E(0, 18, 12, 20, (176, 122, 58))
        for yy in (10, 18, 26):
            Ln([(-10, yy), (10, yy)], (92, 58, 28), 3)
        E(0, -8, 13, 13, (150, 98, 48))
        E(0, -26, 12, 9, (138, 92, 44))
        E(-8, -27, 7, 8, (214, 50, 38))
        E(8, -27, 7, 8, (214, 50, 38))
    elif kind == "drainfly":
        dk = (70, 68, 64)
        legs([-6, 2, 10], 22, dk, 1.6)
        for side in (-1, 1):
            pts = _rell(side * 25, 4, 23, 34, side * (34 + 5 * phase))
            Pg(pts, (150, 148, 140, 245))
            for i, (x, y) in enumerate(pts):
                if i % 2 == 0:
                    E(x, y, 2.6, 2.6, (172, 170, 162))
            for v in (-0.5, 0, 0.5):
                Ln([(side * 6, -2), (side * (25 + 18 * v), 4 + 30 * (0.5 + v * 0.6)), (side * (30 + 10 * v), 34)], (108, 106, 100), 1.4)
        E(0, 0, 8, 22, (92, 90, 86))
        E(0, -24, 8, 7, (98, 96, 92))
        for side in (-1, 1):
            for i in range(6):
                E(side * (3 + i * 3), -30 - i * 4, 2.2, 2.2, (150, 148, 140))
    elif kind in ("roach", "babyroach"):
        pale = kind == "babyroach"
        body, dark, leg = ((214, 196, 160), (150, 130, 100), (180, 160, 130)) if pale else \
            ((156, 98, 46), (64, 40, 22), (110, 70, 34))
        legs([-14, -2, 12], 46, leg, 3, 1.1)
        Ln([(-4, -46), (-14, -70), (-26, -88), (-40, -98)], leg, 1.8)
        Ln([(4, -46), (14, -70), (26, -88), (40, -98)], leg, 1.8)
        Ln([(-6, 46), (-12, 58)], leg, 2)
        Ln([(6, 46), (12, 58)], leg, 2)
        E(0, 8, 23, 40, body)
        Ln([(0, -14), (0, 46)], dark, 2)
        E(0, -26, 22, 15, tuple(min(255, v + 18) for v in body))
        Ln([(-7, -36), (-7, -16)], dark, 4)
        Ln([(7, -36), (7, -16)], dark, 4)
        E(0, -42, 10, 7, dark)
    elif kind == "mite":
        leg = (196, 182, 160)
        for side in (-1, 1):
            for j, a in enumerate((-60, -25, 20, 55)):
                r = math.radians(a + 8 * sw * (1 if j % 2 else -1))
                Ln([(side * 18, -6 + j * 9), (side * (18 + 22 * math.cos(r)), -6 + j * 9 + 22 * math.sin(r)),
                    (side * (22 + 30 * math.cos(r)), -6 + j * 9 + 34 * math.sin(r))], leg, 3.5)
        E(0, 2, 26, 32, (226, 216, 198))
        E(0, -6, 18, 18, (208, 194, 172))
        Ln([(-14, 18), (14, 18)], (196, 182, 160), 1.5)
        E(0, -32, 7, 6, (190, 170, 145))
    elif kind == "beetle":
        legs([-8, 2, 12], 22, (40, 34, 30), 2.4)
        Ln([(-5, -36), (-12, -46)], (40, 34, 30), 2)
        Ln([(5, -36), (12, -46)], (40, 34, 30), 2)
        E(0, 6, 30, 34, (52, 42, 34))
        for (x, y, c) in ((-12, -4, (230, 224, 210)), (10, 6, (214, 124, 60)), (-6, 18, (214, 124, 60)), (12, 24, (230, 224, 210)),
                          (-16, 14, (230, 224, 210)), (2, -12, (214, 124, 60)), (16, -8, (230, 224, 210)), (-2, 30, (230, 224, 210))):
            E(x, y, 5.5, 4.5, c)
        Ln([(0, -24), (0, 38)], (30, 24, 20), 1.6)
        E(0, -30, 14, 8, (40, 34, 30))
    elif kind == "centipede":
        col, band, leg = (178, 158, 118), (70, 62, 66), (196, 178, 140)
        n = 15
        for i in range(n):
            y = -42 + i * 6
            wig = 4 * math.sin(i * 1.3 + phase * 2.5)
            for side in (-1, 1):
                a = math.radians(20 + i * 4)
                Ln([(side * 3, y), (side * (26 + wig), y + 6 + 18 * math.sin(a)), (side * (46 + wig), y + 22 + 22 * math.sin(a))], leg, 1.2)
        Ln([(-2, 46), (-10, 80), (-14, 112)], leg, 1.2)
        Ln([(2, 46), (10, 80), (14, 112)], leg, 1.2)
        Ln([(-2, -46), (-14, -80), (-24, -110), (-30, -125)], leg, 1.0)
        Ln([(2, -46), (14, -80), (24, -110), (30, -125)], leg, 1.0)
        for i in range(n):
            y = -42 + i * 6
            E(0, y, 5, 4, col)
            Ln([(-4, y + 1.5), (4, y + 1.5)], band, 1.5)
        E(0, -46, 4.5, 4, (110, 98, 86))
    elif kind == "egg":
        E(0, 0, 26, 42, (242, 242, 232))
        E(-7, -14, 7, 12, (255, 255, 255))
    elif kind == "larva":
        for i in range(8):
            E(0, -35 + i * 10, 14 - abs(i - 3) * 1.2, 7, (236, 226, 202))
        E(0, -42, 6, 5, (60, 44, 34))
    elif kind == "pupa":
        E(0, 0, 22, 46, (146, 94, 52))
        for yy in range(-30, 40, 10):
            Ln([(-18, yy), (18, yy)], (110, 70, 38), 2)
    elif kind == "eggcase":
        E(0, 0, 40, 80, (122, 72, 36))
        for yy in range(-66, 72, 11):
            Ln([(-34 + abs(yy) * 0.25, yy), (34 - abs(yy) * 0.25, yy)], (86, 50, 26), 3)
        Ln([(0, -78), (0, 78)], (150, 96, 52), 3)
    out = im.resize((max(1, S // ss), max(1, S // ss)), Image.LANCZOS) if ss > 1 else im
    if key[3]:
        out = out.rotate(-key[3], resample=Image.BICUBIC, expand=False)
    _BUG[key] = out
    return out


def bug_arr(kind, L, phase, ang):
    key = ("A", kind, int(L), phase, int(round(ang / 15)) * 15 % 360)
    if key not in _BUG:
        _BUG[key] = np.asarray(bug_img(kind, L, phase, ang))
    return _BUG[key]


# ------------------------------------------------------------------ common props
def person_back(p, x, yh, s=1.0, shirt=SHIRT):
    """The faceless YOU from behind: dark hair, blue shirt, shoulders running off the bottom."""
    p.rect(x - 175 * s, yh + 120 * s, x + 175 * s, H + OY + 10, shirt, r=110 * s)
    p.rect(x - 215 * s, yh + 175 * s, x - 120 * s, H + OY + 10, tuple(int(v * 0.86) for v in shirt), r=50 * s)
    p.rect(x + 120 * s, yh + 175 * s, x + 215 * s, H + OY + 10, tuple(int(v * 0.86) for v in shirt), r=50 * s)
    p.rect(x - 40 * s, yh + 60 * s, x + 40 * s, yh + 140 * s, tuple(int(v * 0.85) for v in SKIN))
    p.ell(x - 82 * s, yh + 6 * s, 16 * s, 26 * s, SKIN)
    p.ell(x + 82 * s, yh + 6 * s, 16 * s, 26 * s, SKIN)
    p.ell(x, yh, 84 * s, 92 * s, HAIR)
    p.ell(x - 24 * s, yh - 40 * s, 40 * s, 28 * s, (64, 46, 36))


def kitchen(p, mess, dark=False):
    p.full(N0 if dark else N2)
    for i in range(3):                       # upper cabinets
        x0 = 40 + i * 340
        p.rect(x0, 300, x0 + 320, 700, N3, r=10)
        p.rect(x0 + 24, 324, x0 + 296, 676, tuple(v - 6 for v in N3), r=8)
        p.rect(x0 + 140, 640, x0 + 180, 652, STEEL, r=5)
    p.rect(-OX, 1060, W + OX, 1110, (78, 96, 134))
    p.rect(-OX, 1110, W + OX, 1520, N1)
    for i in range(4):
        x0 = 20 + i * 265
        p.rect(x0, 1140, x0 + 245, 1490, tuple(v + 4 for v in N1), r=8)
        p.rect(x0 + 100, 1170, x0 + 145, 1182, STEEL, r=5)
    p.rect(-OX, 1520, W + OX, H + OY, (14, 22, 42))
    for i in range(6):
        p.line([(-OX, 1560 + i * 80), (W + OX, 1560 + i * 80)], (20, 30, 54), 3)
    if mess >= 1:
        p.ell(300, 1080, 120, 14, (110, 84, 46, 150))
    if mess >= 2:
        for i in range(mess * 3):
            p.ell(100 + (i * 173) % 900, 1600 + (i * 97) % 280, 30 + i % 3 * 12, 10, (96, 74, 40, 170))
        bag(p, 920, 1430, 1.0)
    if mess >= 3:
        bag(p, 80, 1460, 1.1)
        p.rect(600, 1020, 860, 1062, (196, 150, 90), r=4)      # pizza boxes
        p.rect(620, 980, 840, 1022, (180, 136, 80), r=4)
    if mess >= 4:
        bag(p, 300, 1500, 1.2)
        bag(p, 780, 1520, 1.3)
        for i in range(14):
            p.ell(60 + (i * 211) % 960, 1080 - (i % 3) * 8, 10, 7, (150, 120, 70))


def bag(p, x, y, s):
    p.ell(x, y, 120 * s, 105 * s, (24, 28, 40))
    p.ell(x - 30 * s, y - 40 * s, 40 * s, 30 * s, (44, 52, 72))
    p.poly([(x - 20 * s, y - 100 * s), (x, y - 140 * s), (x + 22 * s, y - 100 * s)], (24, 28, 40))


def window(p, x0, y0, x1, y1, moon=True):
    p.rect(x0, y0, x1, y1, (10, 16, 32), r=6, oc=N3, ow=14)
    if moon:
        p.ell(x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.34, 42, 42, (222, 228, 240))
    p.line([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], N3, 12)
    p.line([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], N3, 12)


def flies(n, box, kind="fruitfly", L=60, seed=0):
    x0, y0, x1, y1 = box
    r = np.random.RandomState(seed)
    return [dict(kind=kind, L=L * r.uniform(0.85, 1.15), mode="hover", x=r.uniform(x0, x1), y=r.uniform(y0, y1),
                 A=r.uniform(40, 120), B=r.uniform(25, 70), seed=r.uniform(0, 9)) for _ in range(n)]


def crawlers(n, box, kind="roach", L=150, seed=0, speed=180, u0=0.0, spread=0.0):
    x0, y0, x1, y1 = box
    r = np.random.RandomState(seed)
    return [dict(kind=kind, L=L * r.uniform(0.85, 1.1), mode="crawl", x=r.uniform(x0, x1), y=r.uniform(y0, y1),
                 h=r.uniform(0, 360), speed=speed * r.uniform(0.7, 1.2), seed=r.uniform(0, 9), box=box,
                 u0=u0 + spread * i / max(1, n)) for i in range(n)]


# ------------------------------------------------------------------ shots: draw(p, ctx) -> sprites
def s_house(p, c):
    m = c["mess"]
    p.vgrad(-OY, 1500, N0, N2)
    r = np.random.RandomState(3)
    for _ in range(60):
        p.ell(r.uniform(-OX, W + OX), r.uniform(-OY, 1100), 2.5, 2.5, (200, 210, 235, 160))
    p.ell(840, 520, 58, 58, (224, 230, 242))
    p.glow(840, 520, 160, (200, 210, 240), 14)
    p.rect(-OX, 1460, W + OX, H + OY, (14, 26, 30))
    p.rect(250, 960, 830, 1470, N2)
    p.poly([(200, 975), (540, 690), (880, 975)], N1)
    p.rect(700, 740, 770, 900, N1)
    lit = [YEL, YEL, YEL, YEL] if m < 3 else [YEL, (40, 50, 70), YEL, YEL]
    for i, (x, y) in enumerate(((330, 1030), (590, 1030), (330, 1230), (590, 1230))):
        p.rect(x, y, x + 160, y + 150, lit[i], r=4)
        p.line([(x + 80, y), (x + 80, y + 150)], N2, 10)
        p.line([(x, y + 75), (x + 160, y + 75)], N2, 10)
        if m >= 4 and lit[i] == YEL:      # bugs in the windows
            p.sprite("centipede" if i % 2 else "roach", 70, x + 50 + i * 12, y + 50, ang=40 * i)
    p.rect(495, 1300, 585, 1470, N1)
    if m >= 3:
        for i in range(30):
            x = -OX + i * 42
            p.poly([(x, 1470), (x + 14, 1380 - (i * 37) % 70), (x + 28, 1470)], (20, 40, 36))
        bag(p, 180, 1470, 0.7)
        bag(p, 900, 1480, 0.8)
    sp = []
    if m >= 2:
        sp += flies(4 + 3 * m, (250, 900, 830, 1300), L=34, seed=m)
    return sp


def s_you_kitchen(p, c):
    kitchen(p, c["mess"])
    window(p, 380, 330, 700, 650)
    person_back(p, 540, 1240, 1.1)
    return flies(2 * c["mess"], (100, 700, 980, 1050), L=40, seed=5) if c["mess"] else []


def s_calendar(p, c):
    p.full(N1)
    p.glow(540, 900, 600, N3, 30)
    p.line([(540, 470), (330, 600)], (150, 160, 180), 4)
    p.line([(540, 470), (750, 600)], (150, 160, 180), 4)
    p.ell(540, 470, 12, 12, STEEL)
    p.rect(290, 590, 790, 1200, CREAM, r=22)
    p.rect(290, 590, 790, 760, RED, r=22)
    p.rect(290, 700, 790, 760, RED)
    p.text(540, 676, "DAY", FONT % "Black", 84, (255, 255, 255))
    p.text(540, 985, str(c["day"]), FONT % "Black", 260 if c["day"] < 100 else 210, N1)
    p.poly([(820, 380), (1060, 300), (1110, 520), (880, 600)], (210, 214, 226))   # a page flying away
    p.poly([(820, 380), (1060, 300), (1072, 352), (836, 432)], (200, 60, 50))
    return []


def s_sink(p, c, bath=False, banana=True):
    m = c["mess"]
    p.full(N3 if bath else N2)
    tile = (52, 76, 122) if bath else N3
    for i in range(-1, 14):
        p.line([(-OX, 80 + i * 90), (W + OX, 80 + i * 90)], tile, 3)
        p.line([(i * 90, -OY), (i * 90, 1000)], tile, 3)
    p.rect(-OX, 980, W + OX, H + OY, (52, 64, 94))
    p.ell(540, 1260, 420, 240, (24, 34, 60))
    p.ell(540, 1270, 380, 205, (18, 26, 48))
    p.rect(500, 760, 580, 1010, STEEL, r=30)
    p.line([(540, 780), (540, 700), (700, 700), (700, 860)], STEEL, 46)
    p.ell(540, 1330, 40, 20, (8, 12, 22))
    if bath:
        for i in range(10):
            a = 2 * math.pi * i / 10
            p.ell(540 + 60 * math.cos(a), 1330 + 30 * math.sin(a), 30, 16, (70, 96, 52, 200))
        p.ell(540, 1330, 70, 34, (64, 88, 46, 150))
    else:
        n = 1 + m * 2
        for i in range(n):
            p.ell(470 + (i % 3) * 60, 1290 - i * 26, 150, 36, (200, 208, 224), oc=(150, 160, 182), ow=4)
            if m >= 1:
                p.ell(440 + (i % 3) * 70, 1286 - i * 26, 40, 9, (120, 90, 50))
        p.rect(720, 1150, 820, 1270, (180, 70, 60), r=14)   # a mug
        if m >= 2:
            p.rect(140, 1170, 420, 1200, (60, 64, 78), r=14)  # a pan handle
            p.ell(300, 1230, 140, 70, (60, 64, 78))
        if banana:
            rot = min(3, m + c.get("rot", 0))
            col = [(250, 214, 70), (226, 186, 60), (176, 132, 48), (96, 70, 36)][rot]
            pts = [(560 + 360 * math.cos(a), 1420 + 220 * math.sin(a)) for a in np.linspace(0.35, 1.25, 18)]
            inner = [(560 + 310 * math.cos(a), 1420 + 160 * math.sin(a)) for a in np.linspace(1.25, 0.35, 18)]
            p.poly(pts + inner, col)
            p.ell(pts[0][0] + 4, pts[0][1], 14, 12, (70, 56, 30))
            for i in range(rot * 5):
                a = 0.45 + 0.75 * ((i * 0.37) % 1)
                p.ell(560 + 335 * math.cos(a), 1420 + 190 * math.sin(a), 9 + rot * 2, 7 + rot, (80, 56, 28))
    nf = c.get("flies", 2 * m)
    kind = "drainfly" if bath else "fruitfly"
    return flies(nf, (200, 1000, 900, 1500), kind=kind, L=58 if bath else 52, seed=7 + m)


def s_banana_close(p, c):
    p.full(N1)
    p.glow(540, 1050, 700, N3, 26)
    pts = [(-200 + 1500 * math.cos(a), -900 + 2200 * math.sin(a)) for a in np.linspace(1.0, 1.75, 30)]
    inner = [(-200 + 1260 * math.cos(a), -900 + 1950 * math.sin(a)) for a in np.linspace(1.75, 1.0, 30)]
    p.poly(pts + inner, (214, 172, 58))
    for i in range(22):
        a = 1.05 + 0.65 * ((i * 0.41) % 1)
        rr = 1300 + 140 * ((i * 0.29) % 1)
        p.ell(-200 + rr * math.cos(a), -900 + rr * 1.68 * math.sin(a) * 0.98, 26 + i % 4 * 8, 18 + i % 3 * 6, (96, 66, 30))
    sp = flies(3, (150, 500, 950, 900), L=110, seed=2)
    r = np.random.RandomState(11)
    for i in range(26):
        sp.append(dict(kind="egg", L=18, mode="still", x=430 + r.uniform(-120, 120), y=1180 + r.uniform(-80, 80),
                       h=r.uniform(0, 180), u0=0.15 + 0.7 * i / 26))
    return sp


def s_portrait(p, c, kind, label, L=560):
    p.full(N1)
    for i in range(7):
        rr = 620 - i * 70
        p.ell(540, 960, rr, rr, tuple(min(255, v + i * 3) for v in N1))
    p.ell(540, 960 + L * 0.62, L * 0.5, 26, (8, 12, 24, 120))
    p.text(540, 1520, label, FONT % "Bold", 40, (150, 166, 200), spacing=8)
    mode = "hover" if kind in ("fruitfly", "drainfly") else "breathe"
    return [dict(kind=kind, L=L, mode=mode, x=540, y=930, A=18, B=14, seed=1, h=0)]


def s_eggs(p, c):
    p.full(N1)
    p.sprite("fruitfly", 300, 540, 560)
    p.text(540, 1600, "500 EGGS", FONT % "Black", 64, YEL, spacing=6)
    sp = []
    for i in range(140):
        col, row = i % 14, i // 14
        sp.append(dict(kind="egg", L=22, mode="still", x=150 + col * 60, y=880 + row * 62, h=0, u0=0.04 + 0.85 * i / 140))
    return sp


def s_hallway(p, c):
    p.full(N0)
    p.poly([(-OX, -OY), (360, 520), (360, 1400), (-OX, H + OY)], N1)
    p.poly([(W + OX, -OY), (720, 520), (720, 1400), (W + OX, H + OY)], N1)
    p.poly([(-OX, H + OY), (360, 1400), (720, 1400), (W + OX, H + OY)], (14, 22, 42))
    p.rect(360, 520, 720, 1400, (20, 30, 54))
    p.rect(420, 640, 660, 1400, (12, 18, 34))
    p.poly([(560, 640), (660, 640), (660, 1400), (560, 1400)], YEL)
    p.poly([(560, 1400), (660, 1400), (900, H + OY), (380, H + OY)], YEL + (90,))
    p.rect(420, 640, 560, 1400, (30, 44, 74))
    return flies(7, (480, 700, 720, 1300), kind="drainfly", L=34, seed=4)


def s_feet(p, c, bath=True):
    m = c["mess"]
    p.full(N3 if bath else (32, 46, 80))
    for i in range(-1, 14):
        p.line([(-OX, i * 150), (W + OX, i * 150 + 40)], (52, 76, 122) if bath else (26, 38, 68), 4)
        p.line([(i * 150, -OY), (i * 150 - 40, H + OY)], (52, 76, 122) if bath else (26, 38, 68), 4)
    for i in range(6 + 8 * m):
        p.ell(80 + (i * 137) % 920, 200 + (i * 211) % 1100, 18 + i % 3 * 10, 10, (64, 86, 50, 170) if bath else (100, 76, 40, 180))
    for x in (380, 700):
        p.rect(x - 95, 1440, x + 95, H + OY, (34, 52, 92), r=40)
        p.ell(x, 1290, 92, 170, SKIN)
        for t in range(5):
            p.ell(x - 62 + t * 31, 1130 + abs(t - 1.5) * 10, 18 - abs(t - 1) * 1.5, 20, SKIN)
    return flies(3 + m * 2, (100, 200, 980, 1000), kind="drainfly", L=48, seed=9)


def s_drain(p, c):
    m = c["mess"]
    p.full((40, 58, 96))
    for i in range(-1, 14):
        p.line([(-OX, i * 160), (W + OX, i * 160)], (54, 76, 118), 5)
        p.line([(i * 160, -OY), (i * 160, H + OY)], (54, 76, 118), 5)
    p.ell(540, 1000, 420, 420, (56, 78, 46, 210))
    p.ell(540, 1000, 330, 330, (74, 98, 54))
    for i in range(18):
        a = 2 * math.pi * i / 18
        p.ell(540 + 300 * math.cos(a), 1000 + 300 * math.sin(a), 46, 34, (88, 116, 62))
    p.ell(540, 1000, 250, 250, STEEL)
    p.ell(540, 1000, 220, 220, (60, 72, 96))
    for i in range(-3, 4):
        p.rect(540 + i * 56 - 16, 820 + abs(i) * 18, 540 + i * 56 + 16, 1180 - abs(i) * 18, (8, 12, 22), r=14)
    sp = crawlers(5 + m * 2, (300, 760, 780, 1240), kind="larva", L=70, seed=3, speed=40)
    return sp + flies(3 + m, (160, 400, 920, 1500), kind="drainfly", L=70, seed=6)


def s_lifecycle(p, c):
    p.full(N1)
    xs = (190, 430, 670, 900)
    for i, (x, lab) in enumerate(zip(xs, ("EGG", "LARVA", "PUPA", "FLY"))):
        p.ell(x, 960, 110, 110, N2)
        p.text(x, 1130, lab, FONT % "Bold", 34, (150, 166, 200), spacing=5)
        if i < 3:
            p.poly([(x + 112, 948), (x + 132, 960), (x + 112, 972)], YEL)
    p.text(540, 640, "~1 WEEK", FONT % "Black", 90, YEL, spacing=4)
    return [dict(kind=k, L=L, mode="still", x=x, y=960, h=0, u0=0.08 + 0.22 * i)
            for i, (k, L, x) in enumerate((("egg", 70, 190), ("larva", 120, 430), ("pupa", 110, 670), ("fruitfly", 150, 900)))]


def s_kitchen_dark(p, c):
    kitchen(p, c["mess"], dark=True)
    p.rect(700, 520, 1060, 1520, (48, 62, 92), r=16)
    p.rect(700, 900, 1060, 912, (30, 40, 62))
    p.rect(730, 700, 744, 860, STEEL, r=6)
    p.rect(730, 960, 744, 1100, STEEL, r=6)
    window(p, 140, 330, 460, 650)
    p.poly([(200, 650), (420, 650), (760, 1920), (100, 1920)], (190, 200, 230, 26))
    return crawlers(1, (720, 1530, 1000, 1560), kind="roach", L=90, seed=8, speed=30)


def s_fridge_gap(p, c):
    p.full((14, 22, 42))
    p.rect(-OX, -OY, W + OX, 980, (52, 66, 98))
    for i in range(14):
        p.rect(80 + i * 66, 860, 120 + i * 66, 940, (30, 40, 62), r=6)
    p.rect(-OX, 980, W + OX, 1060, (4, 6, 12))
    for x in (260, 330, 610, 690):
        p.line([(x, 1040), (x - 40 + (x % 3) * 30, 1180), (x - 90 + (x % 5) * 30, 1330)], (150, 100, 52), 4)
    sp = crawlers(2, (150, 1060, 930, 1800), kind="roach", L=200, seed=12, speed=200)
    sp[0].update(x=450, y=1080, h=170)
    return sp


def s_crumbs(p, c):
    p.full((24, 34, 62))
    for i in range(12):
        p.line([(-OX, i * 180), (W + OX, i * 180)], (18, 26, 50), 6)
    p.ell(640, 1200, 330, 170, (110, 70, 34, 200))
    p.ell(600, 1180, 200, 90, (140, 92, 46, 160))
    r = np.random.RandomState(1)
    for _ in range(90):
        x, y, s = r.uniform(0, 1080), r.uniform(300, 1700), r.uniform(6, 20)
        p.poly([(x, y), (x + s, y + s * 0.3), (x + s * 0.6, y + s)], (212, 168, 92))
    p.rect(80, 340, 420, 560, (196, 70, 60), r=10)
    p.poly([(420, 380), (520, 420), (520, 600), (420, 560)], (150, 50, 44))
    return crawlers(6 + c["mess"], (60, 400, 1020, 1700), kind="roach", L=150, seed=4, speed=170)


def s_eggcase(p, c):
    p.full(N1)
    p.glow(540, 900, 500, N3, 34)
    p.sprite("eggcase", 520, 540, 820, ang=12)
    sp = crawlers(40, (100, 900, 980, 1700), kind="babyroach", L=70, seed=21, speed=150, u0=0.05, spread=0.8)
    for s in sp:
        s.update(x=540 + (s["x"] - 540) * 0.2, y=1100)
    return sp


def s_trash(p, c):
    kitchen(p, max(3, c["mess"]))
    p.rect(380, 1180, 700, 1560, (60, 72, 100), r=20)
    p.rect(360, 1160, 720, 1200, (80, 94, 126), r=10)
    bag(p, 540, 1100, 1.2)
    bag(p, 430, 1170, 0.8)
    for i in range(6):
        p.rect(150 + i * 140, 1600 + (i % 2) * 60, 230 + i * 140, 1640 + (i % 2) * 60, (180, 70, 60) if i % 2 else (200, 200, 210), r=10)
    return flies(10, (200, 700, 900, 1300), L=44, seed=13)


def bed(p, m):
    p.full(N2)
    window(p, 640, 260, 960, 620)
    p.rect(80, 760, 1000, 1080, (36, 54, 92), r=20)
    p.rect(40, 1060, 1040, 1520, (56, 84, 136), r=30)
    p.rect(40, 1240, 1040, 1520, (48, 74, 122), r=30)
    p.ell(300, 1080, 190, 70, CREAM)
    p.rect(-OX, 1520, W + OX, H + OY, (14, 22, 42))
    r = np.random.RandomState(5)
    for _ in range(40 + 40 * m):
        p.ell(r.uniform(60, 1020), r.uniform(1060, 1500), 4, 4, (180, 184, 196, 200))
    for _ in range(6 + 6 * m):
        x, y = r.uniform(80, 1000), r.uniform(1080, 1480)
        p.line([(x, y), (x + 30, y - 18), (x + 60, y + 6), (x + 90, y - 10)], (30, 24, 20), 2)
    if m >= 3:
        for i in range(5):
            p.ell(200 + i * 170, 1360, 70, 26, (110, 96, 64, 120))


def s_bed(p, c):
    bed(p, c["mess"])
    return []


def s_mite_zoom(p, c):
    bed(p, c["mess"])
    p.rect(-OX, -OY, W + OX, H + OY, (5, 8, 16, 120))
    p.line([(700, 1360), (820, 1620)], CREAM, 30)
    p.ell(540, 1000, 360, 360, (196, 190, 178))
    for i in range(-8, 9):   # fabric weave, clipped to the lens
        h_ = math.sqrt(max(0, 345 ** 2 - (i * 40) ** 2))
        p.line([(540 + i * 40, 1000 - h_), (540 + i * 40, 1000 + h_)], (176, 170, 158), 6)
        p.line([(540 - h_, 1000 + i * 40), (540 + h_, 1000 + i * 40)], (186, 180, 168), 6)
    p.ell(540, 1000, 360, 360, None, oc=CREAM, ow=26)
    r = np.random.RandomState(2)
    for _ in range(18):
        x, y = 540 + r.uniform(-260, 260), 1000 + r.uniform(-260, 260)
        p.poly([(x, y), (x + 30, y + 6), (x + 18, y + 26)], (236, 226, 206))
    return crawlers(6, (300, 760, 780, 1240), kind="mite", L=110, seed=6, speed=35)


def s_mites_many(p, c):
    p.full((180, 174, 162))
    for i in range(-12, 13):
        p.line([(540 + i * 60, -OY), (540 + i * 60, H + OY)], (160, 154, 142), 10)
        p.line([(-OX, 960 + i * 60), (W + OX, 960 + i * 60)], (170, 164, 152), 10)
    r = np.random.RandomState(9)
    for _ in range(60):
        x, y = r.uniform(0, 1080), r.uniform(0, 1920)
        p.poly([(x, y), (x + 40, y + 10), (x + 22, y + 34)], (236, 228, 210))
    return crawlers(22, (0, 150, 1080, 1800), kind="mite", L=90, seed=7, speed=30)


def s_carpet(p, c):
    p.full((40, 50, 84))
    r = np.random.RandomState(4)
    for _ in range(900):
        x, y = r.uniform(-OX, W + OX), r.uniform(-OY, H + OY)
        p.line([(x, y), (x + r.uniform(-6, 6), y - 14)], (54, 66, 104), 3)
    for _ in range(9):
        x, y = r.uniform(80, 1000), r.uniform(300, 1700)
        for k in range(10):
            p.ell(x + r.uniform(-30, 30), y + r.uniform(-30, 30), 22, 22, (150, 150, 160, 160))
    for _ in range(14):
        x, y = r.uniform(80, 1000), r.uniform(300, 1700)
        p.line([(x, y), (x + 50, y - 30), (x + 110, y + 10), (x + 170, y - 20)], (30, 22, 18), 2)
    p.sprite("deadfly", 120, 760, 520, ang=170)
    return crawlers(5, (100, 300, 980, 1700), kind="beetle", L=110, seed=3, speed=60)


def s_poll(p, c):
    p.full(N1)
    p.text(540, 560, "WHAT WOULD YOU DO?", FONT % "Black", 66, (255, 255, 255))
    for i, (lab, dot) in enumerate((("MOVE OUT", (232, 92, 120)), ("BURN THE HOUSE", (90, 140, 230)),
                                     ("ADOPT THEM", (226, 190, 110)), ("CLEAN. RIGHT. NOW.", (80, 200, 110)))):
        y = 700 + i * 140
        p.rect(130, y, 950, y + 110, N2, r=22)
        p.ell(200, y + 55, 26, 26, dot)
        p.text(250, y + 55, lab, FONT % "ExtraBold", 46, (255, 255, 255), anchor="lm")
        p.text(900, y + 55, "✕" if i < 3 else "✓", FONT % "Black", 40, RED if i < 3 else (80, 200, 110))
    return []


def s_swarm(p, c):
    kitchen(p, 4)
    return crawlers(26, (40, 900, 1040, 1880), kind="roach", L=130, seed=31, speed=230)


def s_stairs(p, c):
    p.full(N0)
    for i in range(9):
        y = 1820 - i * 150
        w = 900 - i * 60
        p.rect(540 - w / 2, y, 540 + w / 2, y + 70, (34, 50, 88))
    p.line([(540, -OY), (540, 300)], (60, 66, 80), 4)
    p.ell(540, 330, 34, 46, (255, 236, 160))
    p.glow(540, 340, 380, YEL, 16)
    sp = [dict(kind="centipede", L=380, mode="crawl", x=200, y=700, h=120, speed=260, seed=1, box=(-100, 300, 1180, 1500))]
    return sp


def s_centipede_wall(p, c):
    p.full((30, 44, 78))
    for i in range(12):
        p.line([(i * 100, -OY), (i * 100, H + OY)], (26, 38, 70), 6)
    p.ell(700, 1500, 300, 60, (10, 14, 28, 120))
    return [dict(kind="centipede", L=820, mode="crawl", x=380, y=1300, h=25, speed=140, seed=2, box=(100, 300, 980, 1700))]


def s_chase(p, c):
    p.full((22, 32, 58))
    for i in range(12):
        p.line([(-OX, i * 180), (W + OX, i * 180)], (16, 24, 46), 6)
    return [dict(kind="roach", L=150, mode="crawl", x=540, y=760, h=0, speed=360, seed=3, box=(60, 200, 1020, 1800)),
            dict(kind="centipede", L=460, mode="chase", x=540, y=1500, h=0, speed=330, seed=4, target=0)]


def s_wall_many(p, c):
    p.full((30, 44, 78))
    for i in range(12):
        p.line([(i * 100, -OY), (i * 100, H + OY)], (26, 38, 70), 6)
    person_back(p, 540, 1400, 1.0)
    return crawlers(6, (40, 150, 1040, 1250), kind="centipede", L=320, seed=8, speed=120)


def s_doorway(p, c):
    p.full(N0)
    p.rect(250, 380, 830, 1650, N2)
    for i in range(2):
        p.rect(280 + i * 290, 520, 520 + i * 290, 840, N3, r=8)
    p.rect(250, 1100, 830, 1140, (78, 96, 134))
    p.rect(250, 1140, 830, 1650, N1)
    bag(p, 380, 1560, 0.8)
    bag(p, 700, 1580, 0.9)
    p.ell(540, 1600, 200, 30, (96, 74, 40, 170))
    p.poly([(250, 1650), (830, 1650), (W + OX, H + OY), (-OX, H + OY)], (14, 22, 42))
    person_back(p, 540, 1260, 1.25)
    return crawlers(5, (280, 1150, 800, 1620), kind="roach", L=70, seed=6, speed=120) + \
        flies(6, (280, 500, 800, 1000), L=30, seed=2)


def s_clock(p, c):
    p.full((8, 10, 16))
    p.rect(150, 720, 930, 1200, (20, 22, 30), r=30)
    p.text(540, 960, c.get("time", "3:12"), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 260, RED)
    p.text(860, 1120, "AM", FONT % "Black", 50, RED)
    p.glow(540, 960, 460, RED, 10)
    return []


def s_end(p, c):
    p.full((14, 14, 18))
    p.text(540, 760, "IS YOUR HOUSE", FONT % "Black", 104, (230, 230, 236))
    p.text(540, 900, "NEXT?", FONT % "Black", 150, RED)
    p.text(540, 1060, "Comment  DAY 1  or  DAY 365", FONT % "Bold", 46, (200, 200, 210))
    p.text(540, 1150, "PART 2 SOON", FONT % "Bold", 40, (120, 120, 132), spacing=6)
    try:
        import mascot
        p.ell(540, 1600, 190, 190, (34, 36, 48))
        mb = mascot.draw("wave", size=420)
        mb = mb.resize((mb.width * SS, mb.height * SS), Image.LANCZOS)
        px, py = p.P(540, 1580)
        p.im.paste(mb, (int(px - mb.width / 2), int(py - mb.height / 2)), mb)
    except Exception as e:   # the cameo is branding only
        print("end card: no Meatball cameo:", e, flush=True)
    return []


SHOTS = {
    "house": s_house, "you": s_you_kitchen, "calendar": s_calendar, "sink": s_sink,
    "sink_flies": lambda p, c: s_sink(p, dict(c, flies=4, rot=1)),
    "bath_sink": lambda p, c: s_sink(p, dict(c, flies=6), bath=True), "banana": s_banana_close,
    "fly": lambda p, c: s_portrait(p, c, "fruitfly", "FRUIT FLY"), "eggs": s_eggs, "hallway": s_hallway,
    "feet": s_feet, "drainfly": lambda p, c: s_portrait(p, c, "drainfly", "DRAIN FLY"), "drain": s_drain,
    "lifecycle": s_lifecycle, "kitchen_dark": s_kitchen_dark, "fridge": s_fridge_gap,
    "roach": lambda p, c: s_portrait(p, c, "roach", "GERMAN COCKROACH", 520), "crumbs": s_crumbs,
    "eggcase": s_eggcase, "trash": s_trash, "bed": s_bed, "mite_zoom": s_mite_zoom, "mites": s_mites_many,
    "mite": lambda p, c: s_portrait(p, c, "mite", "DUST MITE", 520),
    "beetle": lambda p, c: s_portrait(p, c, "beetle", "CARPET BEETLE", 460), "carpet": s_carpet, "poll": s_poll,
    "swarm": s_swarm, "stairs": s_stairs, "centipede_wall": s_centipede_wall,
    "centipede": lambda p, c: s_portrait(p, c, "centipede", "HOUSE CENTIPEDE", 480), "chase": s_chase,
    "wall_many": s_wall_many, "doorway": s_doorway, "clock": s_clock, "end": s_end,
    "feet_floor": lambda p, c: s_feet(p, c, bath=False),
}

PLANS = {"what-if-never-clean": {
    "tt": [["house", "you"], ["calendar", "sink"], ["sink_flies", "banana"], ["fly", "eggs"], ["hallway", "feet"],
           ["drainfly", "drain"], ["bath_sink", "drain"], ["calendar", "lifecycle"], ["kitchen_dark", "fridge"],
           ["roach", "crumbs"], ["eggcase", "eggcase"], ["trash", "bed"], ["mite_zoom", "mites"],
           ["beetle", "carpet"], ["poll", "poll"], ["house", "swarm"], ["stairs", "centipede_wall"],
           ["centipede", "chase"], ["wall_many", "house"], ["doorway", "clock"], ["end"]],
    "yt": [["house", "you"], ["drainfly", "drain"], ["crumbs", "fridge"], ["bed", "mite_zoom"], ["chase", "house"]],
}}
FOCUS = {"you": (540, 1100), "feet": (540, 1200), "doorway": (540, 1200), "wall_many": (540, 1100), "end": (540, 960)}


# ------------------------------------------------------------------ overlays
def _txt_img(rows, pad=10):
    """rows: [(text, font, size, color, spacing)] stacked, left aligned. RGBA array with a soft shadow."""
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    sizes = []
    for t, f, s, c, sp in rows:
        ft = F(f, s)
        w = sum(d0.textlength(ch, font=ft) + sp for ch in t) if sp else d0.textlength(t, font=ft)
        sizes.append((w, int(s * 1.15)))
    Wd, Hd = int(max(w for w, _ in sizes)) + 2 * pad + 8, sum(h for _, h in sizes) + 2 * pad
    im = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = pad
    for (t, f, s, c, sp), (w, h) in zip(rows, sizes):
        ft = F(f, s)
        for dx, dy, col in ((4, 4, (0, 0, 0, 150)), (0, 0, c)):
            x = pad + dx
            if sp:
                for ch in t:
                    d.text((x, y + dy), ch, font=ft, fill=col)
                    x += d.textlength(ch, font=ft) + sp
            else:
                d.text((x, y + dy), t, font=ft, fill=col)
        y += h
    return np.asarray(im)


def title_img(text):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur + " " + w) > 26 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    ims = [_txt_img([(ln, SERIF % "Regular", 78, (255, 255, 255), 0)]) for ln in lines]
    Wd = max(i.shape[1] for i in ims)
    out = np.zeros((sum(i.shape[0] for i in ims) - 10 * (len(ims) - 1), Wd, 4), np.uint8)
    y = 0
    for i in ims:
        x = (Wd - i.shape[1]) // 2
        out[y:y + i.shape[0], x:x + i.shape[1]] = np.maximum(out[y:y + i.shape[0], x:x + i.shape[1]], i)
        y += i.shape[0] - 10
    return out


_CNT = {}


def counter_img(n, flash):
    key = (n, flash)
    if key not in _CNT:
        _CNT[key] = _txt_img([("DAYS WITHOUT CLEANING", FONT % "Bold", 34, (200, 210, 230), 4),
                              (f"{n:,}", SERIF % "Bold", 170 if not flash else 190, YEL if flash else (255, 255, 255), 0)])
    return _CNT[key]


def over(dst, src, x, y, alpha=1.0):
    h, w = src.shape[:2]
    x, y = int(x), int(y)
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = s[..., 3:4] / 255.0 * alpha
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (d * (1 - a) + s[..., :3] * a).astype(np.uint8)


# ------------------------------------------------------------------ plan
def sprite_track(s, n):
    """Per-frame (x, y, angle, phase, visible) for one sprite over n frames of its shot."""
    t = np.arange(n) / FPS
    sd = s.get("seed", 0)
    if s["mode"] == "hover":
        x = s["x"] + s["A"] * np.sin(1.7 * t + sd) + 0.3 * s["A"] * np.sin(5.1 * t + 2 * sd)
        y = s["y"] + s["B"] * np.sin(2.3 * t + 2 * sd)
        ang = 12 * np.sin(1.3 * t + sd)
        ph = (np.arange(n) % 2)
    elif s["mode"] == "breathe":
        x, y = np.full(n, s["x"]), s["y"] + 6 * np.sin(2 * t)
        ang, ph = 4 * np.sin(0.9 * t), (np.arange(n) // 6) % 2
    elif s["mode"] == "still":
        x, y, ang, ph = np.full(n, s["x"]), np.full(n, s["y"]), np.full(n, s.get("h", 0)), np.zeros(n, int)
    else:   # crawl / chase
        x, y, ang = np.zeros(n), np.zeros(n), np.zeros(n)
        cx, cy, h = s["x"], s["y"], s.get("h", 0)
        x0, y0, x1, y1 = s.get("box", (-200, -200, 1280, 2120))
        for i in range(n):
            if s["mode"] == "chase":
                tx, ty = s["_target"][0][i], s["_target"][1][i]
                want = math.degrees(math.atan2(tx - cx, -(ty - cy)))
                h += max(-6, min(6, (want - h + 180) % 360 - 180))
            else:
                h += 2.2 * math.sin(0.9 * t[i] + sd) + 1.2 * math.sin(2.3 * t[i] + 2 * sd)
            nx = cx + s["speed"] / FPS * math.sin(math.radians(h))
            ny = cy - s["speed"] / FPS * math.cos(math.radians(h))
            if s["mode"] != "chase" and not (x0 <= nx <= x1 and y0 <= ny <= y1):
                h = math.degrees(math.atan2(((x0 + x1) / 2 - cx), -(((y0 + y1) / 2) - cy))) + 20 * math.sin(i)
                nx, ny = cx + s["speed"] / FPS * math.sin(math.radians(h)), cy - s["speed"] / FPS * math.cos(math.radians(h))
            cx, cy = nx, ny
            x[i], y[i], ang[i] = cx, cy, h
        ph = (np.arange(n) // 3) % 2
    vis = t >= s.get("u0", 0) * n / FPS
    return x, y, ang, ph, vis


def plan(o, cut, work):
    import free_voice as fv
    slug = o["slug"]
    items = o[cut]
    lines = [str(list(it.values())[0]) for it in items]
    if cut == "tt":
        lines.append("Follow me. " + o["next"])
    shots_plan = PLANS[slug][cut]
    assert len(shots_plan) == len(lines), (len(shots_plan), len(lines))
    beats, t, day = [], 0.0, 1
    for i, say in enumerate(lines):
        src = fv.make("kokoro:onyx", say)
        mp3 = f"{work}/vo-{i:02d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"atempo={TEMPO}", "-ar", str(SR), mp3], check=True)
        words = [(a / TEMPO, b / TEMPO, w) for a, b, w in json.load(open(src + ".words.json"))]
        dur = fv.pv_duration(src) / TEMPO
        if i < len(items) and items[i].get("counter") is not None:
            day = int(items[i]["counter"])
        last = i == len(lines) - 1
        D = dur + (1.6 if last and cut == "tt" else (0.5 if last else GAP))
        names = shots_plan[i]
        n = max(len(names), math.ceil(D / MAX_SHOT))
        cuts = [0.0]
        for k in range(1, n):   # cut on the word start nearest each even split
            aim = D * k / n
            cand = [w[0] for w in words if 0.4 < w[0] < D - 0.4]
            near = min(cand, key=lambda v: abs(v - aim)) if cand else aim
            cuts.append(near if abs(near - aim) < 0.45 and near > cuts[-1] + 0.6 else aim)
        cuts.append(D)
        shots = []
        for k in range(n):
            nm = names[k % len(names)]
            shots.append(dict(name=nm, a=t + cuts[k], z=t + cuts[k + 1], alt=k // len(names), day=day,
                              mess=DAYMESS.get(day, 4)))
        beats.append(dict(i=i, say=say, mp3=mp3, words=words, t=t, dur=dur, D=D, day=day,
                          tick=items[i].get("counter") if i < len(items) else None, shots=shots))
        t += D
    return beats, t


def build_shots(beats):
    cache, out = {}, []
    for bt in beats:
        for s in bt["shots"]:
            key = (s["name"], s["mess"], s["day"])
            if key not in cache:
                p = Pen()
                ctx = dict(mess=s["mess"], day=s["day"])
                sp = SHOTS[s["name"]](p, ctx) or []
                cache[key] = (p.done(), sp)
            base, sp = cache[key]
            n = max(1, int(round((s["z"] - s["a"]) * FPS)))
            tracks = []
            for j, spr in enumerate(sp):
                spr = dict(spr)
                if spr["mode"] == "chase":
                    spr["_target"] = tracks[spr["target"]][1]
                tracks.append((spr, sprite_track(spr, n)))
            fx, fy = FOCUS.get(s["name"], (540, 960))
            if s["alt"]:
                fx, fy = fx + (60 if s["alt"] % 2 else -60), fy + 80
            out.append(dict(s, base=base, tracks=tracks, focus=(fx, fy), pull=(len(out) % 3 == 2)))
    return out


# ------------------------------------------------------------------ render
PL = {}


def frame(g):
    T = g / FPS
    shots = PL["shots"]
    sh = next((s for s in shots if s["a"] <= T < s["z"]), shots[-1])
    u = min(1.0, (T - sh["a"]) / max(1e-3, sh["z"] - sh["a"]))
    z = 1.0 + 0.075 * ((1 - u) if sh["pull"] else u)
    fx, fy = sh["focus"]
    vw, vh = W / z, H / z
    cx = min(max(fx, -OX + vw / 2), W + OX - vw / 2)
    cy = min(max(fy, -OY + vh / 2), H + OY - vh / 2)
    vx0, vy0 = cx - vw / 2, cy - vh / 2
    M = np.float32([[z, 0, -(vx0 + OX) * z], [0, z, -(vy0 + OY) * z]])
    fr = cv2.warpAffine(sh["base"], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    k = min(int(round((T - sh["a"]) * FPS)), 10 ** 9)
    for spr, (xs, ys, angs, phs, vis) in sh["tracks"]:
        i = min(k, len(xs) - 1)
        if not vis[i]:
            continue
        arr = bug_arr(spr["kind"], spr["L"] * z, int(phs[i]), angs[i])
        pop = i - int(spr.get("u0", 0) * len(xs))
        if spr.get("u0") and 0 <= pop < 4:
            sc = (0.4, 0.8, 1.15, 1.05)[pop]
            arr = cv2.resize(arr, (max(1, int(arr.shape[1] * sc)), max(1, int(arr.shape[0] * sc))))
        px, py = (xs[i] - vx0) * z, (ys[i] - vy0) * z
        over(fr, arr, px - arr.shape[1] / 2, py - arr.shape[0] / 2)
    if sh["name"] != "end":
        ticks = PL["ticks"]
        val = ticks[0][1]
        for (t0, a), (t1, b) in zip(ticks, ticks[1:]):
            if t0 <= T < t1:   # holds, then rolls up over the last 1.2 s into the next day tick
                uu = max(0.0, (T - (t1 - 1.2)) / 1.2)
                val = int(round(a * (b / a) ** uu))
                break
        else:
            if T >= ticks[-1][0]:
                val = ticks[-1][1]
        flash = any(0 <= T - t0 < 0.35 for t0, _ in ticks[1:])
        ci = counter_img(val, flash)
        over(fr, ci, 52, 330)
    ti = PL["title"]
    if T < PL["title_end"]:
        a = min(1.0, (PL["title_end"] - T) / 0.3)
        over(fr, ti, W // 2 - ti.shape[1] // 2, 110, a)
    return fr.tobytes()


def captions(beats, keys, path):
    from facts import ass_time
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, "
            "Shadow, Alignment, MarginV\n"
            "Style: Cap,Inter Black,96,&H00FFFFFF,&H00180E09,&H90000000,0,1,7,4,5,0\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Text\n")
    out = []
    kk = lambda w: "".join(ch for ch in w.lower() if ch.isalnum())
    for bt in beats:
        if bt["shots"][0]["name"] == "end":
            continue
        groups, cur = [], []
        for w in bt["words"]:
            cur.append(w)
            if len(cur) == 3 or (w[2].rstrip()[-1:] in ".,!?;:" and len(cur) >= 2):
                groups.append(cur)
                cur = []
        if cur:
            if len(cur) == 1 and groups and len(groups[-1]) < 4:
                groups[-1] += cur
            else:
                groups.append(cur)
        for gi, gr in enumerate(groups):
            ws = [w for _, _, w in gr]
            hot = [q for q, w in enumerate(ws) if kk(w) in keys or any(ch.isdigit() for ch in w)][:1] or \
                [max(range(len(ws)), key=lambda q: len(kk(ws[q])))]
            end = groups[gi + 1][0][0] if gi + 1 < len(groups) else gr[-1][1] + 0.1
            text = " ".join(("{\\c&H4DD3FF&}" + w.upper() + "{\\c&HFFFFFF&}") if q in hot else w.upper()
                            for q, w in enumerate(ws))
            sc = min(100, int(100 * 14 / max(1, len(" ".join(ws)))))
            pop = rf"\fscx{sc * 7 // 10}\fscy{sc * 7 // 10}\t(0,90,\fscx{sc}\fscy{sc})"
            out.append(f"Dialogue: 0,{ass_time(bt['t'] + gr[0][0])},{ass_time(bt['t'] + end)},Cap,"
                       f"{{\\an5\\pos(540,1340){pop}}}{text}")
    open(path, "w").write(head + "\n".join(out) + "\n")


def read_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def write_wav(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((a * 32767).astype("<i2").tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outline")
    ap.add_argument("--cut", default="tt")
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--music", default="cold-war")
    ap.add_argument("--music-lufs", type=float, default=-19)
    ap.add_argument("--stills", default="")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    o = yaml.safe_load(open(a.outline))
    beats, total = plan(o, a.cut, a.work)
    print(f"plan: {len(beats)} lines, {total:.2f} s, {sum(len(b['shots']) for b in beats)} shots", flush=True)
    ticks = [(b["t"], int(b["tick"])) for b in beats if b["tick"] is not None]
    PL.update(shots=build_shots(beats), ticks=ticks, title=title_img(str(o[a.cut][0][next(iter(o[a.cut][0]))])),
              title_end=beats[1]["t"] + 1.2)
    total_f = int(round(total * FPS))
    if a.stills:
        for s in a.stills.split(","):
            g = min(total_f - 1, int(float(s) * FPS))
            Image.fromarray(np.frombuffer(frame(g), np.uint8).reshape(H, W, 3)).save(f"{a.work}/still-{float(s):06.2f}.png")
        print("stills in", a.work)
        return
    voice = np.zeros((int(total * SR) + SR, 2), np.float32)
    sfx = np.zeros_like(voice)
    for b in beats:
        v = read_audio(b["mp3"])
        s0 = int(b["t"] * SR)
        voice[s0:s0 + len(v)] += v[:len(voice) - s0]
    wh = read_audio(f"{ROOT}/sfx/whoosh.wav") * 0.32
    for t0, _ in ticks[1:]:
        s0 = max(0, int((t0 - 0.12) * SR))
        sfx[s0:s0 + len(wh)] += wh[:len(sfx) - s0]
    write_wav(f"{a.work}/voice.wav", voice)
    write_wav(f"{a.work}/sfx.wav", sfx)
    import music as mus
    mus.render(a.music, total, [t for t, _ in ticks[1:]], f"{a.work}/music.wav", drop=False, hit=False)
    keys = {"".join(ch for ch in str(k).lower() if ch.isalnum()) for k in o.get("cap_key", [])}
    captions(beats, keys, f"{a.work}/cap.ass")
    af = (f"[1:a]loudnorm=I=-16:TP=-2,asplit[vo][key];[3:a]loudnorm=I={a.music_lufs:g}:TP=-6[m];"
          "[m][key]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=350[d];"
          "[vo][d][2:a]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "pipe:0", "-i", f"{a.work}/voice.wav", "-i", f"{a.work}/sfx.wav", "-i", f"{a.work}/music.wav",
           "-filter_complex", f"[0:v]ass={a.work}/cap.ass,format=yuv420p[v];{af}", "-map", "[v]", "-map", "[a]",
           "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
           "-movflags", "+faststart", a.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with mp.get_context("fork").Pool(int(os.environ.get("MEATBALL_JOBS", "6"))) as pool:
        for k, buf in enumerate(pool.imap(frame, range(total_f), chunksize=8)):
            proc.stdin.write(buf)
            if k % 300 == 0:
                print(f"frame {k}/{total_f}", flush=True)
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    for f in ("voice.wav", "sfx.wav", "music.wav"):
        os.remove(f"{a.work}/{f}")
    tl = dict(total=total, policy=dict(hold=2.5),
              beats=[dict(start=b["t"], shots=[(s["a"] - b["t"], s["z"] - b["t"]) for s in b["shots"]]) for b in beats],
              transitions=[dict(t=s["a"], kind="cut") for s in PL["shots"][1:]],
              asks=[dict(kind="poll", t=b["t"]) for b in beats if b["shots"][0]["name"] == "poll"])
    json.dump(tl, open(f"{a.work}/screen.json", "w"), indent=1)
    import screengate
    rep = screengate.check_timeline(tl)
    for nt in rep["notes"]:
        print("screengate:", nt)
    for fl in rep["fails"]:
        print("SCREENGATE FAIL", fl)
    print(f"ok {a.out} {total:.1f}s shots={len(PL['shots'])} screengate_fails={len(rep['fails'])}")


if __name__ == "__main__":
    main()
