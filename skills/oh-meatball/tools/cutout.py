#!/usr/bin/env python3
"""Construction-paper cutout renderer (preview, 11/18). Nolan: "Think of South Park for inspiration" -> a STYLE
reference only: flat paper cutouts, circle heads, mitten hands, choppy 12 fps motion, small bratty kids. Every
character, design, voice, jingle and font choice here is original (no show characters, catchphrases, music, fonts).

  python3 tools/cutout.py --fmt vertical|wide --out file.mp4      render one cut (12 fps held to 24 fps)
  python3 tools/cutout.py --sheet file.mp4                        3-frame contact sheet next to it

Cast: MEATBALL (brand mascot, know-it-all narrator kid, kokoro adam-puck), PIP (tall anxious kid, teal slouch
beanie, kokoro "pip" blend), DOT (short deadpan kid, yellow rain hood, kokoro "dot" blend). Voices are clean
Kokoro takes from free_voice.make() (no pitch or formant effects); lip flap = word timings + the take's loudness.
Music: an original ukulele-style Karplus-Strong strum + plucked melody + soft kit, synthesized here in numpy.
"""
import argparse
import json
import math
import os
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import free_voice as fv  # noqa: E402

FPS, OUT_FPS, SR = 12, 24, 44100
TMP = "/dev/shm/cutout"
FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
INK = (34, 28, 26)

# ------------------------------------------------------------------------------------------------ script
LINES = [  # (who, voice, said text, caption text)
    ("pip", "kokoro:pip@speed=1.22,pause=0.2",
     "Most of your body's cells get swapped out over the years. So are you even still you?", None),
    ("dot", "kokoro:dot@speed=1.08,pause=0.2", "Great. I'm a knockoff of myself.", None),
    ("mb", "kokoro:adam-puck@speed=1.2", "It's the Ship of Theseus. Swap every plank... is it the same ship?", None),
    ("pip", "kokoro:pip@speed=1.22,pause=0.2", "Yes?", None),
    ("mb", "kokoro:adam-puck@speed=1.2",
     "It's not the same ship. And if you disagree, you've never replaced a phone screen.",
     "It's NOT the same ship. And if you disagree, you've never replaced a phone screen."),
    ("dot", "kokoro:dot@speed=1.08,pause=0.2", "Same ship or new ship. Pick one. No fence-sitting.", None),
]
INTRO = 3.0
GAP_AFTER = [0.45, 0.3, 0.95, 0.6, 0.3, 0.5]   # comic beats after each line (reaction holds)
OUTRO = 1.9

# ------------------------------------------------------------------------------------------------ paper kit
_rng0 = np.random.default_rng(7)
_N = _rng0.normal(0, 1, (1024, 1024)).astype(np.float32)
GRAIN = np.asarray(Image.fromarray(((_N * 40) + 128).clip(0, 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(0.8)), np.float32) / 128.0 - 1.0          # fine paper grain, about -1..1
FIBRE = np.asarray(Image.fromarray(((_rng0.normal(0, 1, (256, 256)) * 50) + 128).clip(0, 255).astype(np.uint8))
                   .resize((1024, 1024), Image.BICUBIC), np.float32) / 128.0 - 1.0   # soft mottling


def ell(cx, cy, rx, ry, a0=0.0, a1=360.0, n=None, rot=0.0):
    n = n or max(24, int((a1 - a0) / 5))
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return pts


def lumpy(cx, cy, r, bumps, n=90):
    return [(cx + (r + sum(a * math.sin(k * t + p) for a, k, p in bumps)) * math.cos(t),
             cy + (r + sum(a * math.sin(k * t + p) for a, k, p in bumps)) * math.sin(t))
            for t in [i * 2 * math.pi / n for i in range(n)]]


def strip(pts, w):
    """A paper strip of width w along a polyline."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    return left + right[::-1]


def torn(pts, rng, step, amp):
    """Resample the outline every `step` px and nudge each point off the line: scissor-cut paper."""
    out = []
    m = len(pts)
    for i in range(m):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % m]
        L = math.hypot(x1 - x0, y1 - y0)
        k = max(1, int(L / step))
        nx, ny = (-(y1 - y0) / L, (x1 - x0) / L) if L else (0, 0)
        for j in range(k):
            f = j / k
            d = rng.uniform(-amp, amp)
            out.append((x0 + (x1 - x0) * f + nx * d, y0 + (y1 - y0) * f + ny * d))
    return out


def paper(img, pts, color, rng, z=1.0, shadow=True, jitter=True, grain=0.06, sh=None, edge=True):
    """Composite one paper shape (screen px) onto an RGBA image: soft drop shadow, grained flat fill, a faint
    lighter cut edge. pts in pixels."""
    if jitter:
        pts = torn(pts, rng, max(6.0, 9 * z), 0.9 * max(1.0, z))
    W, H = img.size
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    off = (sh if sh is not None else 4.5 * max(0.7, z)) if shadow else 0
    pad = int(off + 10)
    x0, y0 = int(math.floor(min(xs))) - pad, int(math.floor(min(ys))) - pad
    x1, y1 = int(math.ceil(max(xs))) + pad, int(math.ceil(max(ys))) + pad
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if cx1 <= cx0 or cy1 <= cy0:
        return
    w, h = x1 - x0, y1 - y0
    ss = 2
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).polygon([((x - x0) * ss, (y - y0) * ss) for x, y in pts], fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    layer = np.zeros((h, w, 4), np.float32)
    if shadow:
        sm = np.asarray(m.filter(ImageFilter.GaussianBlur(max(1.5, 2.2 * z))), np.float32) / 255
        o = int(round(off))
        shm = np.zeros_like(sm)
        shm[o:, int(o * 0.7):] = sm[:h - o, :w - int(o * 0.7)]
        layer[..., 3] = shm * 0.38
    a = np.asarray(m, np.float32) / 255
    gx, gy = int(rng.integers(0, 1024 - min(w, 1023))), int(rng.integers(0, 1024 - min(h, 1023)))
    g = np.zeros((h, w), np.float32)
    gw, gh = min(w, 1024 - gx), min(h, 1024 - gy)
    g[:gh, :gw] = GRAIN[gy:gy + gh, gx:gx + gw] * grain + FIBRE[gy:gy + gh, gx:gx + gw] * grain * 0.6
    col = np.array(color[:3], np.float32)[None, None, :] * (1 + g[..., None])
    if edge:   # a hairline of lighter paper core where the scissors cut (layered paper read)
        er = np.asarray(m.filter(ImageFilter.MinFilter(3)), np.float32) / 255
        rim = np.clip(a - er, 0, 1)[..., None]
        col = col * (1 - 0.35 * rim) + 255 * 0.35 * rim
    sa = layer[..., 3:4]
    out_a = a[..., None] + sa * (1 - a[..., None])
    rgb = (col * a[..., None] + 0 * sa * (1 - a[..., None])) / np.maximum(out_a, 1e-4)
    layer = np.concatenate([np.clip(rgb, 0, 255), out_a * 255], axis=2).astype(np.uint8)
    L = Image.fromarray(layer, "RGBA").crop((cx0 - x0, cy0 - y0, cx1 - x0, cy1 - y0))
    img.alpha_composite(L, (cx0, cy0))


# ------------------------------------------------------------------------------------------------ cast
SKIN_P, SKIN_D = (242, 198, 164), (139, 92, 62)
MEAT, MEAT_DK, SHINE, SAUCE, PARSLEY = (150, 78, 44), (112, 54, 30), (206, 132, 92), (200, 40, 32), (70, 150, 62)
TEAL, TEAL_DK = (31, 158, 150), (20, 112, 108)
YEL, YEL_DK = (246, 198, 48), (206, 156, 28)
WHITE, PUPIL = (250, 248, 240), (24, 22, 22)
MOUTH, TONGUE = (92, 20, 26), (226, 98, 104)

PIP_V2 = True   # Studio 11/20: the tall kid no longer wears a green flap hat
PIP_JACKET, PIP_CAP = (236, 128, 44), (52, 104, 200)

CAST = {
    "mb": dict(neck=(0, -182), sh=((-60, -170), (60, -170)), arm_col=(243, 235, 216), hand=MEAT, arm_len=62),
    "pip": dict(neck=(0, -240), sh=((-52, -230), (52, -230)), arm_col=PIP_JACKET if PIP_V2 else (122, 79, 176),
                hand=SKIN_P, arm_len=82),
    "dot": dict(neck=(0, -148), sh=((-46, -136), (46, -136)), arm_col=YEL, hand=SKIN_D, arm_len=50),
}


def body_shapes(c):
    if c == "mb":
        return [
            ("p", [(-34, -62), (-6, -62), (-8, -10), (-32, -10)], (88, 52, 34)),
            ("p", [(6, -62), (34, -62), (32, -10), (8, -10)], (88, 52, 34)),
            ("e", (-26, -8, 30, 13), (40, 36, 40)), ("e", (26, -8, 30, 13), (40, 36, 40)),
            ("p", [(-62, -188), (62, -188), (78, -54), (-78, -54)], (243, 235, 216)),
            ("p", [(-78, -72), (78, -72), (80, -50), (-80, -50)], (110, 66, 40)),            # belt / pants top
            ("p", [(-40, -186), (40, -186), (0, -112)], (214, 46, 40)),                       # napkin bib
            ("e", (-14, -168, 6, 6), WHITE, False), ("e", (12, -164, 6, 6), WHITE, False),
            ("e", (0, -140, 6, 6), WHITE, False),
            ("e", (-16, -186, 14, 9), (214, 46, 40)), ("e", (16, -186, 14, 9), (214, 46, 40)),  # the knot
        ]
    if c == "pip" and PIP_V2:   # Studio 11/20: new look (orange zip jacket, blue jeans, red sneakers)
        return [
            ("p", [(-30, -74), (-6, -74), (-8, -14), (-28, -14)], (60, 84, 150)),
            ("p", [(6, -74), (30, -74), (28, -14), (8, -14)], (60, 84, 150)),
            ("e", (-24, -10, 28, 12), (200, 52, 44)), ("e", (24, -10, 28, 12), (200, 52, 44)),
            ("p", [(-55, -246), (55, -246), (66, -66), (-66, -66)], PIP_JACKET),
            ("p", strip([(0, -244), (0, -68)], 6), (250, 248, 240), False),                    # zipper
            ("p", [(-66, -88), (66, -88), (66, -66), (-66, -66)], (190, 96, 30)),             # hem band
            ("p", [(-30, -246), (30, -246), (22, -222), (-22, -222)], (250, 248, 240)),       # white collar
        ]
    if c == "pip":
        return [
            ("p", [(-30, -74), (-6, -74), (-8, -14), (-28, -14)], (84, 94, 110)),
            ("p", [(6, -74), (30, -74), (28, -14), (8, -14)], (84, 94, 110)),
            ("e", (-24, -10, 28, 12), (236, 236, 228)), ("e", (24, -10, 28, 12), (236, 236, 228)),
            ("p", [(-55, -246), (55, -246), (66, -66), (-66, -66)], (122, 79, 176)),
            ("p", [(-60, -170), (60, -170), (62, -146), (-62, -146)], (190, 160, 232)),       # sweater band
            ("p", [(-26, -246), (26, -246), (0, -226)], (92, 56, 140)),                       # v-neck
        ]
    return [  # dot
        ("p", [(-30, -46), (-8, -46), (-8, -10), (-32, -10)], (200, 52, 44)),                 # boots
        ("p", [(8, -46), (30, -46), (32, -10), (8, -10)], (200, 52, 44)),
        ("e", (-24, -8, 24, 11), (172, 40, 36)), ("e", (24, -8, 24, 11), (172, 40, 36)),
        ("p", [(-48, -152), (48, -152), (86, -40), (-86, -40)], YEL),
        ("p", [(-2, -150), (2, -150), (3, -42), (-3, -42)], YEL_DK, False),
        ("e", (-14, -118, 6, 6), (60, 60, 70), False), ("e", (-14, -88, 6, 6), (60, 60, 70), False),
        ("e", (-14, -58, 6, 6), (60, 60, 70), False),
        ("p", [(30, -96), (58, -96), (60, -80), (30, -80)], YEL_DK),                           # pocket
    ]


def eyes(cx, cy, dx, rx, ry, gaze, look, lids, lid_col, brow, brow_col):
    """Two white ovals, pupils by gaze, optional lids (fraction closed) and brows (angle each side)."""
    s = []
    gx, gy = {"l": (-1, 0), "r": (1, 0), "c": (0, 0.15), "u": (0.3, -0.7)}[gaze]
    pr = {"wide": 0.25, "norm": 0.36}[look]
    for side in (-1, 1):
        ex = cx + side * dx
        s.append(("e", (ex, cy, rx, ry), WHITE))
        s.append(("e", (ex + gx * rx * 0.42, cy + gy * ry * 0.4 + (ry * 0.08 if lids else 0), rx * pr, rx * pr),
                  PUPIL, False))
        if lids > 0:
            top = cy - ry
            yb = top + 2 * ry * lids
            lid = [(x, min(y, yb)) for x, y in ell(ex, cy, rx + 1.5, ry + 1.5, 180, 360, 40)]
            s.append(("p", lid, lid_col, False))
            if lids < 0.98:
                hw = rx * math.sqrt(max(0.0, 1 - ((yb - cy) / ry) ** 2))
                s.append(("p", strip([(ex - hw - 2, yb), (ex + hw + 2, yb)], 4.5), INK, False))
            else:
                s.append(("p", strip([(ex - rx, cy + 2), (ex, cy + 8), (ex + rx, cy + 2)], 5), INK, False))
        if brow is not None:
            a = math.radians(brow * side)
            bx, by = ex, cy - ry - 12 - (0 if lids < 0.4 else -ry * 0.25)
            L = rx * 0.95
            s.append(("p", strip([(bx - L * math.cos(a), by - L * math.sin(a)),
                                  (bx + L * math.cos(a), by + L * math.sin(a))], 9), brow_col, False))
    return s


def mouth(cx, cy, lvl, w, kind, style="oval"):
    """Closed: a line (smirk / frown / flat). Open, per character: grin (D shape, Meatball), oval (tall, Pip),
    slot (small, barely moves: Dot's deadpan), dent (both rows of teeth: Grandma)."""
    if lvl == 0:
        if kind == "smirk":
            return [("p", strip([(cx - w * 0.7, cy + 2), (cx, cy + 4), (cx + w * 0.8, cy - 6)], 6), MOUTH, False)]
        if kind == "frown":
            return [("p", strip([(cx - w * 0.6, cy + 4), (cx, cy - 2), (cx + w * 0.6, cy + 4)], 6), MOUTH, False)]
        return [("p", strip([(cx - w * 0.55, cy), (cx + w * 0.55, cy)], 6), MOUTH, False)]
    h = [0, 0.42, 0.85][lvl] * w
    if style == "grin":
        top = cy - h * 0.15
        pts = [(cx - w, top), (cx + w, top)] + ell(cx, top, w, h * 0.95 + 4, 0, 180)[1:-1]
        s = [("pts", pts, MOUTH)]
        s.append(("c", (cx, top + h * 0.55, w * 0.55, h * 0.35 + 2), TONGUE, False))
        s.append(("p", [(cx - w * 0.85, top + 2), (cx + w * 0.85, top + 2), (cx + w * 0.75, top + h * 0.22 + 4),
                        (cx - w * 0.75, top + h * 0.22 + 4)], WHITE, False))
        return s
    if style == "slot":
        hh = [0, 0.18, 0.32][lvl] * w
        return [("e", (cx, cy, w * 0.5, hh + 3), MOUTH)]
    if style == "dent":
        s = [("e", (cx, cy + h * 0.2, w * 0.85, h * 0.6 + 4), MOUTH)]
        s.append(("p", [(cx - w * 0.7, cy - h * 0.3), (cx + w * 0.7, cy - h * 0.3), (cx + w * 0.6, cy - h * 0.1),
                        (cx - w * 0.6, cy - h * 0.1)], WHITE, False))
        s.append(("p", [(cx - w * 0.6, cy + h * 0.55), (cx + w * 0.6, cy + h * 0.55), (cx + w * 0.7, cy + h * 0.72),
                        (cx - w * 0.7, cy + h * 0.72)], WHITE, False))
        return s
    if style == "oval":
        s = [("e", (cx, cy + h * 0.3, w * (0.55 if lvl == 1 else 0.62), h * 0.75 + 3), MOUTH)]
        s.append(("c", (cx, cy + h * 0.3 + h * 0.4, w * 0.4, h * 0.3), TONGUE, False))
        return s
    s = [("e", (cx, cy + h * 0.25, w * (0.75 if lvl == 1 else 0.9), h * 0.6 + 3), MOUTH)]
    s.append(("c", (cx, cy + h * 0.25 + h * 0.3, w * 0.5, h * 0.3), TONGUE, False))
    if lvl == 2:
        s.append(("p", [(cx - w * 0.55, cy - h * 0.3), (cx + w * 0.55, cy - h * 0.3), (cx + w * 0.5, cy - h * 0.12),
                        (cx - w * 0.5, cy - h * 0.12)], WHITE, False))
    return s


def head_shapes(c, lvl, gaze, blink, expr):
    """Shapes around the neck pivot (0, 0). expr: norm | wide | smug | deadpan | worried."""
    if c == "mb":
        cy = -108
        s = [("pts", lumpy(0, cy, 112, [(5, 5, 0), (3, 9, 1)]), MEAT)]
        for (x, y, r) in [(-70, -60, 15), (62, -78, 11), (82, 25, 16), (-88, 40, 12), (12, 88, 13), (40, 60, 9)]:
            s.append(("e", (x, cy + y, r, r * 0.85), MEAT_DK, False))
        s.append(("e", (-78, cy - 6, 13, 18, 0, 360, None, 20), SHINE, False))
        edge = [(x, cy - 66 + 7 * math.sin(x / 17.0)) for x in range(92, -93, -12)]
        s.append(("pts", ell(0, cy - 4, 116, 116, 214, 326) + edge, SAUCE))
        for (x, y, r) in [(58, -58, 10), (-20, -54, 12), (-70, -60, 8)]:
            s.append(("e", (x, cy + y, r, r * 1.25), SAUCE, False))
        s.append(("e", (24, cy - 104, 15, 9, 0, 360, None, -20), PARSLEY))
        lids = 1.0 if blink else {"smug": 0.45}.get(expr, 0.0)
        brow = {"smug": -8, "wide": 14, "worried": 18}.get(expr, 4)
        s += eyes(0, cy - 4, 31, 28, 34, gaze, "wide" if expr == "wide" else "norm", lids, MEAT, brow, (70, 34, 18))
        s += mouth(4, cy + 58, lvl, 40, "smirk" if expr == "smug" else "flat", "grin")
        return s
    if c == "pip":
        cy = -100
        s = [("e", (0, cy, 100, 102), SKIN_P)]
        for (x, y) in [(-50, 34), (-38, 42), (-58, 46), (48, 34), (38, 43), (58, 46)]:
            s.append(("e", (x, cy + y, 4, 4), (198, 120, 86), False))
        if PIP_V2:   # curly black hair, a blue baseball cap with the brim forward, round glasses
            for (x, y, r) in [(-92, -30, 26), (-100, -4, 22), (92, -30, 26), (100, -4, 22), (-70, -52, 24),
                              (70, -52, 24)]:
                s.append(("e", (x, cy + y, r, r), (34, 26, 24)))
            s.append(("pts", ell(0, cy - 50, 98, 78, 180, 360) + [(98, cy - 46), (-98, cy - 46)], PIP_CAP))
            s.append(("pts", ell(0, cy - 54, 44, 50, 180, 360) + [(44, cy - 50), (-44, cy - 50)], (250, 248, 240),
                      False))                                                                   # white front panel
            s.append(("pts", [(-100, cy - 50), (30, cy - 50), (150, cy - 34), (146, cy - 20), (-98, cy - 30)],
                      (30, 70, 150)))                                                           # the brim
            s.append(("e", (0, cy - 128, 12, 8), (30, 70, 150)))
            lids = 1.0 if blink else 0.0
            brow = {"wide": 26, "worried": 22, "norm": 16}.get(expr, 16)
            s += eyes(0, cy + 18, 30, 25, 30, gaze, "wide" if expr in ("wide", "worried") else "norm", lids, SKIN_P,
                      brow, (34, 26, 24))
            for side in (-1, 1):
                s.append(("pts", strip(ell(side * 30, cy + 18, 31, 34, 0, 360, 24), 5), (40, 40, 46), False))
            s.append(("p", strip([(-6, cy + 16), (6, cy + 16)], 5), (40, 40, 46), False))
            s += mouth(0, cy + 72, lvl, 34, "frown", "oval")
            return s
        s.append(("p", [(-92, cy - 38), (-112, cy - 20), (-86, cy - 14)], (120, 74, 44)))     # hair tufts
        s.append(("p", [(92, cy - 38), (114, cy - 22), (86, cy - 14)], (120, 74, 44)))
        s.append(("pts", ell(0, cy - 58, 104, 88, 180, 360) + [(118, cy - 52), (-104, cy - 52)], TEAL))
        s.append(("pts", [(30, cy - 142), (96, cy - 164), (132, cy - 132), (118, cy - 106), (70, cy - 120)], TEAL))
        s.append(("p", [(-108, cy - 70), (112, cy - 70), (116, cy - 40), (-110, cy - 40)], TEAL_DK))
        for x in range(-96, 110, 22):
            s.append(("p", strip([(x, cy - 68), (x + 2, cy - 42)], 4), (14, 90, 86), False))
        lids = 1.0 if blink else 0.0
        brow = {"wide": 26, "worried": 22, "norm": 16}.get(expr, 16)
        s += eyes(0, cy + 14, 30, 27, 33, gaze, "wide" if expr in ("wide", "worried") else "norm", lids, SKIN_P,
                  brow, (110, 70, 40))
        s += mouth(0, cy + 70, lvl, 34, "frown", "oval")
        return s
    cy = -96   # dot
    s = [("e", (0, cy - 6, 134, 132), YEL)]
    s.append(("e", (0, cy + 4, 98, 98), SKIN_D))
    s.append(("pts", ell(0, cy - 10, 102, 74, 180, 360) + [(96, cy - 4), (40, cy - 34), (-10, cy - 24),
                                                            (-60, cy - 36), (-96, cy - 4)], (34, 24, 22)))   # bangs
    s.append(("pts", strip(ell(0, cy - 6, 122, 120, 196, 344), 26), YEL_DK))                                 # hood rim
    s.append(("p", strip([(-30, cy + 110), (-22, cy + 150)], 7), (70, 70, 80), False))                      # toggles
    s.append(("p", strip([(30, cy + 110), (22, cy + 150)], 7), (70, 70, 80), False))
    lids = 1.0 if blink else {"wide": 0.1, "deadpan": 0.52, "smug": 0.6}.get(expr, 0.45)
    s += eyes(0, cy + 24, 30, 26, 30, gaze, "norm", lids, SKIN_D, None, None)
    s += mouth(0, cy + 72, lvl, 30, "flat", "slot")
    return s


def arm_shapes(c):
    k = CAST[c]
    L = k["arm_len"]
    return [("p", [(-12, -6), (12, -6), (13, L), (-13, L)], k["arm_col"]),
            ("e", (0, L + 14, 22, 20), k["hand"]), ("e", (17, L + 4, 9, 12, 0, 360, None, -30), k["hand"])]


def render_shapes(shapes, z, R, seed):
    S = int(2 * R * z) + 20
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    rng = np.random.default_rng(seed)
    P = lambda pts: [(S / 2 + x * z, S / 2 + y * z) for x, y in pts]   # noqa: E731
    for sh in shapes:
        kind, geo, col = sh[0], sh[1], sh[2]
        shadow = sh[3] if len(sh) > 3 else True
        if kind == "e":
            cx, cy, rx, ry = geo[:4]
            rot = geo[7] if len(geo) > 7 else 0
            pts = ell(cx, cy, rx, ry, rot=rot, n=48)
        elif kind == "c":   # lower half ellipse
            cx, cy, rx, ry = geo
            pts = ell(cx, cy, rx, ry, 0, 180)
        else:
            pts = geo
        small = max(abs(max(p[0] for p in pts) - min(p[0] for p in pts)),
                    abs(max(p[1] for p in pts) - min(p[1] for p in pts))) * z < 30
        paper(img, P(pts), col, rng, z, shadow=shadow and not small, jitter=not small, sh=3.2 * z, edge=not small)
    return img


@lru_cache(maxsize=512)
def sprite(c, part, z, *key):
    if part == "body":
        return render_shapes(body_shapes(c), z, 270, hash((c, 1)) & 0xffff)
    if part == "arm":
        return render_shapes(arm_shapes(c), z, 120, hash((c, 2)) & 0xffff)
    return render_shapes(head_shapes(c, *key), z, 260, 99 + (hash(c) & 0xff))


# ------------------------------------------------------------------------------------------------ ship
def ship_shapes():
    hull = [(-300, -62), (-250, -60), (240, -60), (290, -66), (300, -20), (348, 12), (300, 28), (220, 62),
            (0, 80), (-210, 62), (-292, 24), (-318, -30)]
    s = [("p", strip([(-150 + 0, -62), (-150, -400)], 12), (110, 70, 40)),                       # mast
         ("p", [(-268, -360), (-34, -360), (-24, -150), (-276, -150)], (246, 236, 210)),              # sail
         ("p", [(-270, -300), (-30, -300), (-28, -268), (-272, -268)], (200, 48, 40), False),
         ("p", [(-274, -222), (-26, -222), (-25, -190), (-275, -190)], (200, 48, 40), False),
         ("p", strip([(-300, -364), (0, -364)], 10), (110, 70, 40)),
         ("p", [(-150, -400), (-96, -386), (-150, -372)], (200, 48, 40)),                          # pennant
         ("p", strip([(-292, -40), (-334, -110), (-360, -160), (-340, -196), (-306, -184), (-318, -150)], 26),
          (150, 98, 58)),                                                                           # stern curl
         ("p", strip([(290, -40), (318, -110), (300, -130)], 22), (150, 98, 58)),                    # bow post
         ("p", hull, (156, 100, 58))]
    for i, y in enumerate((-28, 6, 40)):
        s.append(("p", strip([(-300 + i * 8, y), (300 - i * 20, y)], 4), (98, 60, 32), False))      # seams
    s.append(("p", [(-80, -26), (60, -26), (60, 6), (-80, 6)], (44, 26, 16), False))               # plank hole
    for k, x in enumerate(range(-230, 240, 58)):                                                    # shields
        s.append(("e", (x, -66, 22, 22), [(200, 48, 40), (246, 198, 48), (40, 120, 180)][k % 3]))
        s.append(("e", (x, -66, 7, 7), (246, 236, 210), False))
    s.append(("e", (262, -10, 22, 13), WHITE))
    s.append(("e", (268, -10, 8, 8), PUPIL, False))
    return s


OARS = [(x, -10) for x in range(-220, 240, 70)]
PLANK = [(-80, -26), (60, -26), (60, 6), (-80, 6)]


# ------------------------------------------------------------------------------------------------ layout
def layout(fmt):
    if fmt == "wide":
        return dict(W=1920, H=1080, horizon=600, water=708, wave=722, dock=830, feet=1006,
                    kids={"pip": 320, "mb": 690, "dot": 1040}, ship=(1460, 708, 0.92),
                    cu=2.3, cu_dy=-250, cap_y=920, cap_size=74, banner_y=230, wide=(960, 540, 1.0))
    return dict(W=1080, H=1920, horizon=860, water=1090, wave=1104, dock=1220, feet=1640,
                kids={"pip": 262, "mb": 540, "dot": 818}, ship=(560, 1090, 0.86),
                cu=1.9, cu_dy=-290, cap_y=1490, cap_size=86, banner_y=330, wide=(540, 1250, 1.3))


class Cam:
    def __init__(self, L, cx, cy, z):
        self.W, self.H, self.cx, self.cy, self.z = L["W"], L["H"], cx, cy, z

    def p(self, x, y):
        return ((x - self.cx) * self.z + self.W / 2, (y - self.cy) * self.z + self.H / 2)

    def pts(self, pts):
        return [self.p(x, y) for x, y in pts]


def cams(L):
    wx, wy, wz = L["wide"]
    out = {"wide": (wx, wy, wz)}
    for k, x in L["kids"].items():
        cx = min(max(x, L["W"] / (2 * L["cu"])), L["W"] - L["W"] / (2 * L["cu"]))
        out["cu_" + k] = (cx, L["feet"] + L["cu_dy"], L["cu"])
    sx, sy, ss = L["ship"]
    zs = 2.5 if L["W"] > L["H"] else 2.1
    out["cu_ship"] = (sx - 10 * ss, sy - (110 if L["W"] > L["H"] else 60) * ss, zs)
    return out


def draw_background(L, cam):
    """Back layer (sky, sea, ship) and front layer (front wave, dock), both RGBA at screen size."""
    W, H, z = L["W"], L["H"], cam.z
    rng = np.random.default_rng(11)
    back = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paper(back, [(-50, -50), (W + 50, -50), (W + 50, H + 50), (-50, H + 50)], (150, 204, 232), rng, z,
          shadow=False, jitter=False, grain=0.05, edge=False)
    sun = (L["W"] * 0.16 if L["W"] > L["H"] else 190, L["horizon"] - (360 if L["W"] > L["H"] else 600))
    paper(back, cam.pts(ell(sun[0], sun[1], 70, 70)), (252, 214, 74), rng, z)
    for (x, y, s) in ([(600, 140, 1.0), (1180, 230, 0.8)] if W > H else [(720, 260, 1.0), (300, 560, 0.8)]):
        for dx, dy, r in [(-60, 10, 42), (0, -14, 56), (62, 8, 44), (0, 22, 46)]:
            pass
        cloud = lumpy(x, y, 0, [])
        pts = []
        for i in range(60):
            t = i * 2 * math.pi / 60
            rr = 1 + 0.18 * abs(math.sin(3 * t))
            pts.append((x + 120 * s * rr * math.cos(t), y + 42 * s * rr * math.sin(t)))
        paper(back, cam.pts(pts), (252, 252, 246), rng, z)
        del cloud
    # distant hills and a tiny temple
    hz = L["horizon"]
    x1h = W * 0.62
    hill = [(-60, hz + 4)] + [(x, hz + 4 - (90 + 30 * math.sin(x / 140.0)) * max(0.0, math.sin(math.pi * (x + 60) / (x1h + 60))) ** 0.6)
                              for x in range(-60, int(x1h), 30)] + [(x1h, hz + 4)]
    paper(back, cam.pts(hill), (112, 170, 92), rng, z)
    x0h = W * 0.42
    hill2 = [(x0h, hz + 4)] + [(x, hz + 4 - 70 * max(0.0, math.sin(math.pi * (x - x0h) / (W + 200 - x0h))) ** 0.7)
                               for x in range(int(x0h), W + 80, 30)] + [(W + 80, hz + 4)]
    paper(back, cam.pts(hill2), (92, 150, 80), rng, z)
    tx, ty = (W * 0.3, hz - 118) if W > H else (W * 0.2, hz - 112)
    paper(back, cam.pts([(tx - 60, ty), (tx + 60, ty), (tx + 64, ty + 10), (tx - 64, ty + 10)]), WHITE, rng, z)
    for i in range(4):
        x = tx - 46 + i * 30
        paper(back, cam.pts([(x - 6, ty - 50), (x + 6, ty - 50), (x + 6, ty), (x - 6, ty)]), (240, 236, 224), rng, z,
              sh=2)
    paper(back, cam.pts([(tx - 68, ty - 50), (tx + 68, ty - 50), (tx, ty - 82)]), (236, 230, 214), rng, z)
    # sea
    sea = [(-60, hz)] + [(x, hz + 6 * math.sin(x / 50.0)) for x in range(-60, W + 80, 30)] + [(W + 80, H + 60),
                                                                                              (-60, H + 60)]
    paper(back, cam.pts(sea), (54, 128, 196), rng, z, shadow=False)
    for i in range(7):
        y = hz + 40 + i * (L["water"] - hz) / 6
        x0 = (i * 397) % max(1, W - 300)
        paper(back, cam.pts(strip([(x0, y), (x0 + 120, y)], 6)), (120, 184, 230), rng, z, shadow=False)
    sx, sy, ss = L["ship"]
    sp = lambda pts: cam.pts([(sx + x * ss, sy + y * ss) for x, y in pts])   # noqa: E731
    for (ox, oy) in OARS:
        paper(back, sp(strip([(ox, oy), (ox - 40, oy + 90)], 9)), (120, 78, 44), rng, z, shadow=False)
    for sh in ship_shapes():
        kind, geo, col = sh[:3]
        pts = ell(*geo[:4]) if kind == "e" else geo
        paper(back, sp(pts), col, rng, z, shadow=sh[3] if len(sh) > 3 else True)
    # front: wave strip over the hull's waterline, then the dock
    front = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wave = [(-60, L["wave"])] + [(x, L["wave"] - 12 * abs(math.sin(x / 38.0))) for x in range(-60, W + 80, 12)] + \
        [(W + 80, L["dock"] + 40), (-60, L["dock"] + 40)]
    paper(front, cam.pts(wave), (40, 106, 176), rng, z)
    dock = [(-60, L["dock"]), (W + 80, L["dock"] - 4), (W + 80, H + 80), (-60, H + 80)]
    paper(front, cam.pts(dock), (196, 150, 98), rng, z, sh=7 * z)
    paper(front, cam.pts([(-60, L["dock"]), (W + 80, L["dock"] - 4), (W + 80, L["dock"] + 22),
                          (-60, L["dock"] + 26)]), (160, 112, 66), rng, z)
    n = 0
    y = L["dock"] + 70
    while y < H + 60:
        paper(front, cam.pts(strip([(-60, y), (W + 80, y + 3)], 5)), (150, 104, 62), rng, z, shadow=False)
        for k in range(4):
            x = (n * 233 + k * 517) % W
            paper(front, cam.pts([(x - 4, y + 18), (x + 4, y + 18), (x + 4, y + 26), (x - 4, y + 26)]),
                  (90, 70, 56), rng, z, shadow=False, jitter=False)
        y += 78 + 8 * n
        n += 1
    for px in ([140, W - 140] if W > H else [80, W - 80]):
        paper(front, cam.pts([(px - 26, L["dock"] - 60), (px + 26, L["dock"] - 60), (px + 26, L["dock"] + 40),
                              (px - 26, L["dock"] + 40)]), (128, 86, 50), rng, z)
        paper(front, cam.pts(ell(px, L["dock"] - 60, 26, 9)), (160, 116, 70), rng, z, shadow=False)
    return vignette(back), front


def vignette(img):
    a = np.asarray(img, np.float32)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    d = ((xx / W - 0.5) ** 2 + (yy / H - 0.5) ** 2)
    v = 1 - 0.22 * d
    a[..., :3] *= v[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


# ------------------------------------------------------------------------------------------------ timeline
def load_audio(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).copy()


def build_timeline():
    T = []
    t = INTRO
    for i, (who, voice, say, cap) in enumerate(LINES):
        mp3 = fv.make(voice, say)
        words = json.load(open(mp3 + ".words.json"))
        a = load_audio(mp3)
        dur = len(a) / SR
        capw = (cap or say).split()
        T.append(dict(who=who, start=t, dur=dur, words=[(t + s, t + e, capw[j] if j < len(capw) else w)
                                                        for j, (s, e, w) in enumerate(words)], audio=a, voice=voice))
        t += dur + GAP_AFTER[i]
    return T, t + OUTRO


def shots(T, end):
    """(start, cam) list. Hard cuts, a close-up on each speaker, wides for the gag."""
    w = lambda li, wi: T[li]["words"][wi][0]   # noqa: E731
    S = [(0, "wide"),
         (w(0, 11) - 0.05, "cu_pip"),                         # "So are you even still you?"
         (T[0]["start"] + T[0]["dur"] + 0.05, "cu_dot"),      # reaction hold on Dot, then her line
         (T[2]["start"] - 0.05, "cu_mb"),
         (w(2, 5) - 0.04, "cu_ship"),                         # "Swap every plank..." plank gag
         (w(2, 5) + 2.3, "wide"),                             # everyone stares at the new plank
         (T[3]["start"] - 0.05, "cu_pip"),
         (T[3]["start"] + T[3]["dur"] + 0.15, "cu_mb"),       # Meatball's stare (reaction hold)
         (w(4, 5) - 0.04, "wide"),                            # "And if you disagree..."
         (T[5]["start"] - 0.05, "cu_dot"),
         (T[5]["start"] + T[5]["dur"] + 0.35, "wide")]
    return S


def plank_state(t, t0):
    """Old plank wobbles, drops into the sea; a brand-new plank (price tag still on) clonks in from the sky."""
    d = t - t0
    if d < 0:
        return [("old", 0, 0, 0)]
    if d < 0.42:
        return [("old", 0, 0, [-7, 7, -9, 9, -5][int(d * FPS) % 5])]
    if d < 1.0:
        f = (d - 0.42) / 0.58
        return [("old", 40 * f, 420 * f * f, 50 * f)]
    if d < 1.35:
        return []
    if d < 1.9:
        f = (d - 1.35) / 0.55
        return [("new", 0, -900 * (1 - f) ** 2, 0)]
    if d < 2.1:
        return [("new", 0, [-22, 0, -8, 0][int((d - 1.9) * FPS) % 4], 0)]
    return [("new", 0, 0, 0)]


def plank_sprite(kind, z):
    key = (kind, z)
    if key in _PLANK:
        return _PLANK[key]
    R = 220
    shapes = [("p", [(x + 10, y + 10) for x, y in PLANK], (156, 100, 58) if kind == "old" else (232, 198, 132))]
    for y in (-4, 4):
        shapes.append(("p", strip([(-62, y), (62, y)], 2), (120, 76, 40) if kind == "old"
                       else (200, 160, 96), False))
    if kind == "new":   # the price tag: the gag
        shapes += [("p", strip([(50, 0), (80, 40)], 4), (60, 60, 60), False),
                   ("p", [(66, 34), (176, 22), (184, 88), (74, 98)], WHITE),
                   ("e", (80, 46, 6, 6), (60, 60, 60), False)]
    img = render_shapes(shapes, z, R, 5)
    if kind == "new":
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype(FONT, max(8, int(34 * z)))
        c = img.size[0] / 2
        d.text((c + 128 * z, c + 60 * z), "NEW!", font=f, fill=(200, 40, 32), anchor="mm")
    _PLANK[key] = img
    return img


_PLANK = {}


# ------------------------------------------------------------------------------------------------ frames
G = {}


def paste(frame, spr, x, y, ang=0.0):
    if ang:
        spr = spr.rotate(ang, resample=Image.BICUBIC)
    S = spr.size[0]
    frame.alpha_composite(spr, (int(round(x - S / 2)), int(round(y - S / 2)))) if \
        0 <= x - S / 2 and 0 <= y - S / 2 and x + S / 2 <= frame.size[0] and y + S / 2 <= frame.size[1] else \
        _paste_clip(frame, spr, int(round(x - S / 2)), int(round(y - S / 2)))


def _paste_clip(frame, spr, x0, y0):
    W, H = frame.size
    S = spr.size[0]
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x0 + S), min(H, y0 + S)
    if cx1 > cx0 and cy1 > cy0:
        frame.alpha_composite(spr.crop((cx0 - x0, cy0 - y0, cx1 - x0, cy1 - y0)), (cx0, cy0))


def speaking(T, t):
    for li, ln in enumerate(T):
        if ln["start"] - 0.02 <= t <= ln["start"] + ln["dur"]:
            return li
    return None


def mouth_level(ln, t):
    inword = any(s - 0.03 <= t <= e + 0.02 for s, e, _ in ln["words"])
    if not inword:
        return 0
    a = ln["audio"]
    i = int((t - ln["start"]) * SR)
    seg = a[max(0, i - SR // 30):i + SR // 30]
    if not len(seg):
        return 0
    r = float(np.sqrt(np.mean(seg ** 2)))
    pk = ln["rms_pk"]
    return 2 if r > 0.5 * pk else 1 if r > 0.14 * pk else 0


def char_state(c, t, fi, T, li, plank_t0):
    """Pose for one kid at time t: (dy hop, head jitter, head angle, arm angles, head key)."""
    rng = np.random.default_rng(fi * 31 + hash(c) % 997)
    spk = li is not None and T[li]["who"] == c
    lvl, hop, armL, armR, expr = 0, 0.0, -12.0, 12.0, {"mb": "norm", "pip": "worried", "dot": "deadpan"}[c]
    jit = {"pip": 2.2, "mb": 1.2, "dot": 0.6}[c]
    ang = 0.0
    if t < INTRO:   # bounce to the jingle (beat 60/168 s), each kid on a different beat
        beat = int(t / (60 / 168))
        k = {"pip": 0, "mb": 1, "dot": 2}[c]
        if beat % 3 == k and (t % (60 / 168)) < 0.17:
            hop = -16
        armL, armR = (-25, 25) if beat % 2 else (-10, 10)
        ang = [-3, 3][beat % 2]
        expr = {"mb": "smug", "pip": "norm", "dot": "deadpan"}[c]
    if spk:
        ln = T[li]
        lvl = mouth_level(ln, t)
        wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
        ws = ln["words"][wi][0]
        if t - ws < 0.09:
            hop = -10 if c != "dot" else -4
        poses = {"mb": [(-20, 30), (-30, 150), (-15, 100), (-120, 120), (-60, 60), (-25, 135)],
                 "pip": [(-40, 40), (-150, 150), (-60, 25), (-100, 100), (-30, 60)],
                 "dot": [(-10, 10), (-12, 12), (-10, 70), (-10, 10)]}[c]
        armL, armR = poses[(wi * 7 + li) % len(poses)]
        ang = float(rng.uniform(-3.5, 3.5)) if c != "dot" else float(rng.uniform(-1, 1))
        jit *= 1.6
        if c == "mb":
            expr = "smug" if li == 4 else "norm"
            word = ln["words"][wi][2]
            if word.startswith("NOT"):
                expr, armL, armR, hop = "wide", -130, 130, -18
        if c == "pip":
            expr = "wide" if li == 3 else "worried"
        if c == "dot" and li == 5 and wi in (4, 5):   # "Pick one."
            armL, armR = -10, 100
    else:
        ang = float(rng.uniform(-1, 1))
    # reaction holds
    if li is None and t > INTRO:
        if c == "pip" and T[0]["start"] + T[0]["dur"] < t < T[1]["start"]:
            expr = "worried"
        if c == "mb" and T[3]["start"] + T[3]["dur"] < t < T[4]["start"]:
            expr, ang = "smug", -4
    if plank_t0 is not None and plank_t0 + 0.5 < t < plank_t0 + 2.6 and not spk:
        expr = "wide" if c != "dot" else "deadpan"
    # gaze: speaker to camera, others to the speaker (or the ship during the gag)
    xs = G["L"]["kids"]
    if spk:
        gaze = "c"
    elif li is not None:
        gaze = "l" if xs[T[li]["who"]] < xs[c] else "r"
    else:
        gaze = "c"
    if plank_t0 is not None and plank_t0 + 0.3 < t < plank_t0 + 2.6 and not spk:
        gaze = "r" if G["L"]["W"] > G["L"]["H"] else "u"
    if t > G["end"] - OUTRO:
        gaze, expr = "c", {"mb": "smug", "pip": "worried", "dot": "deadpan"}[c]
        if int(t * FPS) % 6 < 3:
            hop = -8 if c == "mb" else 0
    blink = (int(t * FPS) + {"mb": 0, "pip": 17, "dot": 29}[c]) % 41 == 0
    jx, jy = float(rng.uniform(-jit, jit)), float(rng.uniform(-jit, jit))
    return hop, (jx, jy), ang, (armL, armR), (lvl, gaze, blink, expr)


def frame(fi):
    L, T, S, end = G["L"], G["T"], G["S"], G["end"]
    t = fi / FPS
    cam_name = [n for s, n in S if s <= t][-1]
    cx, cy, z = G["cams"][cam_name]
    cam = Cam(L, cx, cy, z)
    back, front = G["bg"][cam_name]
    fr = back.copy()
    sx, sy, ss = L["ship"]
    for kind, dx, dy, rot in plank_state(t, G["plank_t0"]):
        spr = plank_sprite(kind, round(ss * z, 3))
        px, py = cam.p(sx + (-10 + dx) * ss, sy + (-10 + dy) * ss)
        paste(fr, spr, px, py, rot)
        if kind == "new" and dy == 0 and t < G["plank_t0"] + 2.3:   # bonk stars
            for k in range(3):
                a = math.radians(-60 - 30 * k + (fi % 2) * 10)
                qx, qy = px + math.cos(a) * 80 * ss * z, py + math.sin(a) * 60 * ss * z
                ImageDraw.Draw(fr).regular_polygon((qx, qy, 12 * z), 5, rotation=fi * 20, fill=(252, 214, 74),
                                                   outline=INK)
    fr.alpha_composite(front)
    li = speaking(T, t)
    zz = round(z, 3)
    for c in ("pip", "mb", "dot"):
        hop, (jx, jy), ang, (aL, aR), hk = char_state(c, t, fi, T, li, G["plank_t0"])
        k = CAST[c]
        bx, by = L["kids"][c], L["feet"] + hop
        ox, oy = cam.p(bx, by)
        paste(fr, sprite(c, "body", zz), ox, oy)
        for (sx_, sy_), a in zip(k["sh"], (aL, aR)):
            px, py = cam.p(bx + sx_, by + sy_)
            paste(fr, sprite(c, "arm", zz), px, py, a)
        hx, hy = cam.p(bx + k["neck"][0] + jx, by + k["neck"][1] + jy)
        paste(fr, sprite(c, "head", zz, *hk), hx, hy, ang)
    draw_banner(fr, L, t, end)
    draw_caption(fr, L, T, t, top=cam_name == "cu_ship")
    return np.asarray(fr.convert("RGB")).tobytes()


@lru_cache(maxsize=64)
def tag(text, size, seed):
    f = ImageFont.truetype(FONT, size)
    w = int(f.getlength(text))
    h = size
    rng = np.random.default_rng(seed)
    padx, pady = int(size * 0.42), int(size * 0.3)
    S = int(max(w + 2 * padx, h + 2 * pady) * 1.25) + 40
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    c = S / 2
    paper(img, [(c - w / 2 - padx, c - h / 2 - pady), (c + w / 2 + padx, c - h / 2 - pady),
                (c + w / 2 + padx, c + h / 2 + pady), (c - w / 2 - padx, c + h / 2 + pady)], (252, 250, 240), rng,
          1.4, sh=6)
    ImageDraw.Draw(img).text((c, c + size * 0.04), text, font=f, fill=INK, anchor="mm")
    return img.rotate(float(rng.uniform(-3, 3)), resample=Image.BICUBIC)


def draw_caption(fr, L, T, t, top=False):
    li = speaking(T, t + 0.04)
    if li is None:
        return
    ln = T[li]
    chunks, cur = [], []
    for wd in ln["words"]:
        cur.append(wd)
        if len(cur) == 3 or wd[2][-1] in ".?!," or wd[2].endswith("...") or \
                (len(cur) == 2 and len(" ".join(x[2] for x in cur)) > 12):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    show = None
    for ch in chunks:
        if ch[0][0] - 0.04 <= t:
            show = ch
    if show is None:
        return
    text = " ".join(w[2] for w in show).upper().rstrip(".,")
    text = text.replace("...", "…")
    img = tag(text, L["cap_size"], hash(text) & 0xfff)
    w = img.size[0]
    if w > L["W"] - 40:
        img = img.resize((L["W"] - 40, int(img.size[1] * (L["W"] - 40) / w)), Image.LANCZOS)
    paste(fr, img, L["W"] / 2, L["H"] * (0.13 if L["W"] > L["H"] else 0.2) if top else L["cap_y"])


@lru_cache(maxsize=4)
def banner_img(text, size, col, tcol, seed):
    f = ImageFont.truetype(FONT, size)
    w = int(f.getlength(text))
    rng = np.random.default_rng(seed)
    S = int(w * 1.3) + 80
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    c = S / 2
    pts = [(c - w / 2 - 40, c - size * 0.75), (c + w / 2 + 40, c - size * 0.7), (c + w / 2 + 34, c + size * 0.75),
           (c - w / 2 - 36, c + size * 0.72)]
    paper(img, pts, col, rng, 2.0, sh=9)
    ImageDraw.Draw(img).text((c, c + size * 0.05), text, font=f, fill=tcol, anchor="mm")
    return img


def draw_banner(fr, L, t, end):
    big = 120 if L["W"] > L["H"] else 104
    by = L["banner_y"]
    W = L["W"]
    out = end - OUTRO + 0.25

    def drop(t0):   # choppy slam: off top -> overshoot -> settle
        d = t - t0
        if d < 0:
            return None
        k = int(d * FPS)
        return [-700, -320, 40, -12, 0][k] if k < 5 else 0

    for (t0, t1, text, size, col, tcol, ang, dy) in [
            (0.15, INTRO - 0.15, "MEATBALL MYTHS", big, (200, 40, 32), WHITE, -3, 0),
            (0.85, INTRO - 0.15, "SHIP OF THESEUS", int(big * 0.62), (252, 250, 240), INK, 2, int(big * 1.25)),
            (out, end + 1, "MEATBALL MYTHS", big, (200, 40, 32), WHITE, 3, 0),
            (out + 0.35, end + 1, "SAME SHIP OR NEW SHIP?", int(big * 0.5), (252, 250, 240), INK, -2, int(big * 1.2))]:
        if not (t0 <= t < t1):
            continue
        off = drop(t0)
        if t1 - t < 0.25:
            off = -int((0.25 - (t1 - t)) * 3000)
        img = banner_img(text, size, col, tcol, len(text))
        if img.size[0] > W * 0.98:
            s = W * 0.98 / img.size[0]
            img = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.LANCZOS)
        paste(fr, img, W / 2, by + dy + off, ang)


# ------------------------------------------------------------------------------------------------ audio
def ks(freq, dur, decay=0.994, bright=0.5, seed=0):
    """Karplus-Strong pluck, vectorized one period at a time."""
    n = int(dur * SR)
    N = max(2, int(SR / freq))
    rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, N)
    buf = bright * buf + (1 - bright) * np.convolve(buf, [0.5, 0.5], "same")
    y = np.zeros(n + N + 1)
    y[:N] = buf
    k = N
    while k < n:
        e = min(k + N, n)
        idx = np.arange(k, e)
        y[k:e] = decay * 0.5 * (y[idx - N] + y[idx - N - 1 + (idx - N - 1 < 0)])
        k = e
    y = y[:n]
    env = np.minimum(1, np.arange(n) / (0.002 * SR))
    return (y * env).astype(np.float32)


def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    return 440 * 2 ** ((names[note[:-1]] + 12 * (int(note[-1]) + 1) - 69) / 12)


CHORDS = {"C": ["G4", "C4", "E4", "C5"], "A7": ["G4", "C#4", "E4", "A4"], "D7": ["A4", "D4", "F#4", "C5"],
          "G7": ["G4", "D4", "F4", "B4"], "F": ["A4", "C4", "F4", "C5"]}
BPM = 168
BEAT = 60 / BPM


def add(buf, sig, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[:j - i] * g


def strum(buf, t, chord, g, up=False, seed=0):
    notes = CHORDS[chord][::-1] if up else CHORDS[chord]
    for k, nt in enumerate(notes):
        add(buf, ks(hz(nt), 1.2, 0.993, 0.6, seed + k), t + k * 0.011, g * (0.8 if up else 1.0))


def snare(buf, t, g, seed=0):
    n = int(0.16 * SR)
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n)
    x = np.diff(x, prepend=0)   # bright
    env = np.exp(-np.arange(n) / (0.035 * SR))
    tone = np.sin(2 * np.pi * 190 * np.arange(n) / SR) * np.exp(-np.arange(n) / (0.02 * SR))
    add(buf, (0.35 * x * env + 0.5 * tone).astype(np.float32), t, g)


def kick(buf, t, g):
    n = int(0.22 * SR)
    tt = np.arange(n) / SR
    f = 50 + 70 * np.exp(-tt / 0.03)
    add(buf, (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.08)).astype(np.float32), t, g)


def jingle_bar(buf, t0, chords, g, melody=None, drums=True, seed=0):
    """One bar of 4 beats: chords = 1 or 2 chord names; strum pattern D . D U . U D U (eighths)."""
    pat = [(0, False), (1, False), (1.5, True), (2.5, True), (3, False), (3.5, True)]
    for k, (b, up) in enumerate(pat):
        ch = chords[0] if b < 2 or len(chords) == 1 else chords[1]
        strum(buf, t0 + b * BEAT, ch, g * (0.55 if up else 0.75), up, seed + k * 10)
    if drums:
        kick(buf, t0, g * 0.9)
        kick(buf, t0 + 2 * BEAT, g * 0.7)
        snare(buf, t0 + BEAT, g * 0.45, seed)
        snare(buf, t0 + 3 * BEAT, g * 0.45, seed + 1)
    for (b, nt, d) in melody or []:
        add(buf, ks(hz(nt), d * BEAT + 0.3, 0.996, 0.85, seed + 99), t0 + b * BEAT, g * 1.1)


def sfx_splash(buf, t, g):
    n = int(0.6 * SR)
    rng = np.random.default_rng(3)
    x = rng.normal(0, 1, n)
    x = np.convolve(x, np.ones(6) / 6, "same")
    env = np.exp(-np.arange(n) / (0.15 * SR)) * np.minimum(1, np.arange(n) / (0.01 * SR))
    bub = sum(np.sin(2 * np.pi * (500 + 300 * k) * np.arange(n) / SR * (1 + 0.5 * np.arange(n) / n)) *
              np.exp(-np.arange(n) / (0.05 * SR)) for k in range(3)) * 0.15
    add(buf, (x * env * 0.6 + bub).astype(np.float32), t, g)


def sfx_thunk(buf, t, g):
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * 140 * tt) * np.exp(-tt / 0.05) + 0.5 * np.sin(2 * np.pi * 330 * tt) * np.exp(-tt / 0.03)
    add(buf, s.astype(np.float32), t, g)
    add(buf, ks(1046, 0.4, 0.99, 0.9, 5), t + 0.08, g * 0.5)   # little "bonk" ding


def sfx_slap(buf, t, g, seed=0):
    n = int(0.07 * SR)
    x = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-np.arange(n) / (0.012 * SR))
    add(buf, x.astype(np.float32), t, g)


def mix(T, end):
    music = np.zeros(int((end + 0.5) * SR), np.float32)
    # intro: 2 bars (C A7 | D7 G7) with an original plucked tune, then a C stab under the first line
    mel1 = [(0, "E5", 1), (1, "G5", 0.5), (1.5, "A5", 0.5), (2, "G5", 1), (3, "E5", 0.5), (3.5, "C#5", 0.5)]
    mel2 = [(0, "D5", 0.5), (0.5, "F#5", 0.5), (1, "A5", 1), (2, "B5", 0.5), (2.5, "A5", 0.5), (3, "G5", 1)]
    jingle_bar(music, 0.0, ["C", "A7"], 0.32, mel1, seed=1)
    jingle_bar(music, 4 * BEAT, ["D7", "G7"], 0.32, mel2, seed=2)
    strum(music, 8 * BEAT, "C", 0.4, seed=3)
    add(music, ks(hz("C6"), 1.0, 0.996, 0.85, 4), 8 * BEAT, 0.35)
    kick(music, 8 * BEAT, 0.3)
    # bed: the progression, chords only, -22 dB relative to the intro
    bed = np.zeros_like(music)
    prog = [["C"], ["A7"], ["D7"], ["G7"]]
    t, k = 9 * BEAT, 0
    out_t = end - OUTRO
    while t < out_t:
        jingle_bar(bed, t, prog[k % 4], 0.32, None, drums=True, seed=10 + k)
        t += 4 * BEAT
        k += 1
    fade = np.ones_like(bed)
    i0, i1 = int(9 * BEAT * SR), int(out_t * SR)
    fade[:i0] = 0
    ramp = int(0.3 * SR)
    fade[i0:i0 + ramp] = np.linspace(0, 1, ramp)
    fade[i1:] = 0
    fade[i1 - ramp:i1] = np.linspace(1, 0, ramp)
    music += bed * fade * 10 ** (-22 / 20) * 1.6   # bed sits 22 dB under the intro's level (x1.6 = strum density)
    # outro sting: G7 -> C with a quick original pluck run
    o = out_t + 0.05
    strum(music, o, "G7", 0.35, seed=40)
    for k2, nt in enumerate(["B5", "D6", "G5", "E5"]):
        add(music, ks(hz(nt), 0.6, 0.995, 0.85, 50 + k2), o + 0.18 + k2 * BEAT / 2, 0.32)
    strum(music, o + 2.5 * BEAT, "C", 0.45, seed=60)
    strum(music, o + 2.5 * BEAT + 0.02, "F", 0.0, seed=61)
    add(music, ks(hz("C6"), 1.2, 0.996, 0.85, 62), o + 2.5 * BEAT, 0.35)
    kick(music, o + 2.5 * BEAT, 0.3)
    snare(music, o + 2.5 * BEAT, 0.3, 63)
    # fx
    for t0 in (0.15, 0.85, out_t + 0.25, out_t + 0.6):
        sfx_slap(music, t0 + 2 / FPS, 0.25, int(t0 * 10))
    voice = np.zeros_like(music)
    for ln in T:
        add(voice, ln["audio"], ln["start"], 1.0)
    p0 = G["plank_t0"]
    sfx_splash(voice, p0 + 0.92, 0.35)
    sfx_thunk(voice, p0 + 1.9, 0.6)
    out = voice + music
    out *= 0.97 / max(1e-6, float(np.max(np.abs(out))))
    return out[:int(end * SR)]


# ------------------------------------------------------------------------------------------------ main
def setup(fmt):
    L = layout(fmt)
    T, end = build_timeline()
    for ln in T:
        ln["rms_pk"] = float(np.percentile(np.sqrt(np.convolve(ln["audio"] ** 2, np.ones(1470) / 1470, "same")), 98))
    G.update(L=L, T=T, end=end, S=shots(T, end), cams=cams(L), plank_t0=T[2]["words"][5][0])
    G["bg"] = {}
    for name, (cx, cy, z) in G["cams"].items():
        G["bg"][name] = draw_background(L, Cam(L, cx, cy, z))


def render(fmt, out):
    os.makedirs(TMP, exist_ok=True)
    setup(fmt)
    L, end = G["L"], G["end"]
    wav = f"{TMP}/mix-{fmt}.wav"
    import soundfile as sf
    sf.write(wav, mix(G["T"], end), SR)
    n = int(math.ceil(end * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{L['W']}x{L['H']}",
           "-framerate", str(FPS), "-i", "-", "-i", wav, "-vf", f"fps={OUT_FPS}", "-c:v", "libx264", "-preset",
           "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for b in pool.imap(frame, range(n), chunksize=4):
            ff.stdin.write(b)
    ff.stdin.close()
    ff.wait()
    print(out, f"{end:.2f}s", n, "frames")


def stills(fmt, times):
    setup(fmt)
    W, H = G["L"]["W"], G["L"]["H"]
    for t in times:
        out = f"{TMP}/still-{fmt}-{t:.2f}.png"
        Image.frombytes("RGB", (W, H), frame(int(t * FPS))).save(out)
        print(out)


def sheet(mp4, times=None):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                             capture_output=True, text=True).stdout)
    times = times or [1.5, d * 0.45, d * 0.62]
    ims = []
    for t in times:
        p = f"{TMP}/sheet-{t:.2f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", mp4, "-frames:v", "1", p], check=True)
        ims.append(Image.open(p).convert("RGB"))
    w, h = ims[0].size
    s = 640 / max(w, h)
    ims = [i.resize((int(w * s), int(h * s)), Image.LANCZOS) for i in ims]
    out = Image.new("RGB", (sum(i.size[0] for i in ims) + 10 * 4, ims[0].size[1] + 20), (30, 30, 30))
    x = 10
    for i in ims:
        out.paste(i, (x, 10))
        x += i.size[0] + 10
    p = mp4.rsplit(".", 1)[0] + "-sheet.jpg"
    out.save(p, quality=90)
    print(p)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fmt", default="vertical", choices=["vertical", "wide"])
    ap.add_argument("--out")
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--sheet")
    a = ap.parse_args()
    if a.sheet:
        sheet(a.sheet)
    elif a.still:
        stills(a.fmt, a.still)
    else:
        render(a.fmt, a.out)
