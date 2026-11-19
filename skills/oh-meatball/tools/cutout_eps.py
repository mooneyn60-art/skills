#!/usr/bin/env python3
"""Cutout episodes 3-8: one small engine, one spec per episode.

Shared code: cutout.py (paper kit, kids' rigs, jingle), cutout2.py (voices, captions, camera/timeline engine,
Grandma, the CEO screen, the checkout scene) and cutout_holy.py (Rick, Kaylee, Brad, Chad, the Thanksgiving
table, generic poses). This file adds a parametric person maker for the new original characters, the new
scenes, and one EPISODES[...] spec per episode: script, voices, scenes (cast and positions), cutaway cards and
gag hooks. Everything is original (characters, MEGAMART, music, sound effects).

  python3 tools/cutout_eps.py --ep ep3 --out episodes/cutout-test/cutout-ep3-vertical.mp4
  python3 tools/cutout_eps.py --ep ep3 --still 5 20 40
  python3 tools/cutout_eps.py --ep ep3 --timeline
  python3 tools/linecheck.py --script ep3 episodes/cutout-test/cutout-ep3-vertical.mp4
Vertical (1080x1920) only: one file for TikTok and YouTube Shorts (Nolan 11/19).
"""
import argparse
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout as C  # noqa: E402
import cutout2 as C2  # noqa: E402
import cutout_holy as H  # noqa: E402
from cutout import FONT, INK, WHITE, PUPIL, MOUTH, ell, strip, lumpy, paper, render_shapes, add, ks, hz  # noqa
from cutout import kick, strum, jingle_bar, sfx_slap, BEAT, SR, FPS, OUT_FPS, TMP  # noqa
from cutout2 import paste, Cam, G  # noqa: E402

BOLD = FONT.replace("Black", "Bold")
EP = {}   # the episode being rendered


# ------------------------------------------------------------------------------------------------ people
def person(skin, hair="short", hair_col=(60, 40, 30), top="tee", top_col=(90, 120, 200), bottom=(60, 70, 110),
           shoes=(40, 36, 40), tall=1.0, wide=1.0, acc=(), arm_w=13, eyes=("norm", 0.0)):
    """A parametric paper person (same rig layout as cutout_holy's rigs). Returns (rig, body_fn, head_fn, arm_fn).
    hair: short | slick | bob | bun | buzz | long | curly | bald;  top: tee | hoodie | tank | shirt_tie | polo |
    coat | apron;  acc: sunglasses, sunglasses_head, glasses, helmet, cap, mustache, beard, headband, heart."""
    nk = -250 * tall
    rig = dict(neck=(0, nk), sh=((-60 * wide, nk + 14), (60 * wide, nk + 14)), arm_len=int(90 * tall),
               arm_col=skin if top in ("tank",) else top_col, hand=skin)

    def body():
        lw = 30 * wide
        s = [("p", [(-lw - 4, -80), (-6, -80), (-8, -12), (-lw - 2, -12)], bottom),
             ("p", [(6, -80), (lw + 4, -80), (lw + 2, -12), (8, -12)], bottom),
             ("e", (-24 * wide, -8, 30, 12), shoes), ("e", (24 * wide, -8, 30, 12), shoes)]
        if top == "cargo":   # shorts: knees show
            s = [("p", [(-lw - 4, -80), (-6, -80), (-8, -44), (-lw - 6, -44)], bottom),
                 ("p", [(6, -80), (lw + 4, -80), (lw + 6, -44), (8, -44)], bottom),
                 ("p", [(-lw, -44), (-10, -44), (-10, -12), (-lw, -12)], skin),
                 ("p", [(10, -44), (lw, -44), (lw, -12), (10, -12)], skin),
                 ("p", [(-lw - 2, -70), (-lw + 16, -70), (-lw + 16, -54), (-lw - 2, -54)], (90, 96, 70), False),
                 ("e", (-24 * wide, -8, 30, 12), shoes), ("e", (24 * wide, -8, 30, 12), shoes)]
        tw, bw = 58 * wide, 72 * wide
        s.append(("p", [(-tw, nk), (tw, nk), (bw, -70), (-bw, -70)], top_col if top != "tank" else (240, 240, 240)))
        if top == "tank":   # tiny tank top over a huge chest: skin shoulders
            s += [("p", [(-tw, nk), (-tw + 26, nk), (-tw + 18, nk + 70), (-tw - 6, nk + 70)], skin),
                  ("p", [(tw - 26, nk), (tw, nk), (tw + 6, nk + 70), (tw - 18, nk + 70)], skin)]
        if top == "hoodie":
            s += [("p", [(-36 * wide, -130), (36 * wide, -130), (40 * wide, -86), (-40 * wide, -86)],
                   tuple(max(0, c - 25) for c in top_col), False),
                  ("p", strip([(-14, nk + 10), (-16, nk + 70)], 4), (240, 240, 240), False),
                  ("p", strip([(14, nk + 10), (16, nk + 70)], 4), (240, 240, 240), False)]
        if top == "shirt_tie":
            s += [("p", [(-24, nk), (24, nk), (0, nk + 90)], WHITE),
                  ("p", [(-7, nk + 6), (7, nk + 6), (11, nk + 100), (0, nk + 112), (-11, nk + 100)], (40, 70, 150))]
        if top == "polo":
            s += [("p", [(-24, nk), (24, nk), (12, nk + 26), (-12, nk + 26)], WHITE, False),
                  ("e", (0, nk + 40, 4, 4), WHITE, False), ("e", (0, nk + 56, 4, 4), WHITE, False)]
        if top == "coat":   # firefighter turnout coat with reflective bands
            for y in (nk + 110, -100):
                s.append(("p", [(-bw, y), (bw, y), (bw, y + 16), (-bw, y + 16)], (250, 214, 60), False))
        if top == "apron":
            s.append(("p", [(-34 * wide, nk + 40), (34 * wide, nk + 40), (40 * wide, -70), (-40 * wide, -70)],
                      (250, 250, 244), False))
        if "heart" in acc:
            s.append(("pts", [(0, nk + 90), (-30, nk + 60), (-22, nk + 44), (0, nk + 56), (22, nk + 44), (30, nk + 60)],
                      (230, 80, 130), False))
        return s

    def head(lvl, blink, expr, extra):
        cy = -104
        s = []
        bald = "nohair" in extra
        if hair == "long" and not bald:
            s.append(("pts", ell(0, cy + 10, 104, 120, 0, 360), hair_col))
        if hair == "bun" and not bald:
            s.append(("e", (0, cy - 118, 38, 34), hair_col))
        s += [("e", (-94, cy + 4, 14, 22), skin), ("e", (94, cy + 4, 14, 22), skin), ("e", (0, cy, 94, 100), skin)]
        if "soot" in extra:
            for (x, y, r) in [(-40, 30, 16), (36, -20, 12), (50, 44, 14), (-10, 60, 10)]:
                s.append(("e", (x, cy + y, r, r * 0.8), (70, 70, 74), False))
        if not bald:
            if hair in ("short", "slick", "buzz", "curly", "long", "bun"):
                s.append(("pts", ell(0, cy - 34, 98, 72, 180, 360) + [(98, cy - 30), (-98, cy - 30)], hair_col))
            if hair == "slick":
                s += [("pts", [(-80, cy - 70), (30, cy - 112), (100, cy - 74), (20, cy - 86)], hair_col),
                      ("p", strip([(-40, cy - 86), (30, cy - 102)], 5), (220, 210, 200), False)]
            if hair == "curly":
                for k in range(7):
                    a = math.radians(190 + k * 26)
                    s.append(("e", (96 * math.cos(a), cy - 20 + 86 * math.sin(a), 28, 26), hair_col))
            if hair == "bob":   # asymmetric bob: long on one side
                s += [("pts", ell(0, cy - 20, 104, 92, 180, 360) + [(104, cy + 70), (70, cy + 74), (60, cy - 10),
                                                                     (-70, cy - 30), (-96, cy + 20), (-104, cy - 20)],
                       hair_col),
                      ("p", strip([(-60, cy - 80), (40, cy - 100)], 6), tuple(min(255, c + 30) for c in hair_col),
                       False)]
        lids = 1.0 if blink else ({"smug": 0.45, "wide": 0.0}.get(expr, eyes[1]))
        brow = {"wide": 18, "smug": -8, "mean": -16}.get(expr, 4)
        if "sunglasses" in acc:
            for side in (-1, 1):
                s += [("e", (side * 38, cy, 40, 30), (24, 24, 28)),
                      ("e", (side * 50, cy - 10, 9, 5), (140, 140, 160), False)]
            s.append(("p", strip([(-6, cy - 2), (6, cy - 2)], 6), (24, 24, 28), False))
        else:
            s += C.eyes(0, cy + 6, 32, 22, 24, "c" if expr not in ("l", "r") else expr[0],
                        "wide" if expr == "wide" else "norm", lids, skin, brow, tuple(max(0, c - 20) for c in hair_col))
        if "glasses" in acc:
            for side in (-1, 1):
                s.append(("pts", strip(ell(side * 32, cy + 6, 30, 28, 0, 360, 24), 5), (40, 40, 46), False))
        s.append(("e", (0, cy + 28, 10, 9), tuple(max(0, c - 30) for c in skin), False))
        s += C.mouth(0, cy + 62, lvl, 34, "smirk" if expr == "smug" else ("frown" if expr == "mean" else "flat"),
                     "oval")
        if "mustache" in acc:
            s.append(("pts", strip([(-40, cy + 50), (0, cy + 42), (40, cy + 50)], 14), hair_col))
        if "beard" in acc:
            s.append(("pts", ell(0, cy + 50, 84, 60, 0, 180) + [(-84, cy + 50)], hair_col))
        if "headband" in acc:
            s.append(("p", [(-96, cy - 50), (96, cy - 50), (94, cy - 32), (-94, cy - 32)], (230, 60, 90)))
        if "sunglasses_head" in acc and not bald:
            s += [("e", (-36, cy - 70, 32, 18), (24, 24, 28)), ("e", (36, cy - 70, 32, 18), (24, 24, 28))]
        if "cap" in acc:
            s += [("pts", ell(0, cy - 40, 100, 80, 180, 360) + [(100, cy - 36)], top_col),
                  ("p", [(-20, cy - 46), (150, cy - 46), (140, cy - 30), (-20, cy - 32)], top_col)]
        if "helmet" in acc:   # firefighter helmet with a front shield
            s += [("pts", ell(0, cy - 40, 112, 90, 180, 360) + [(140, cy - 30), (-140, cy - 30)], (200, 40, 32)),
                  ("p", [(-30, cy - 120), (30, cy - 120), (24, cy - 60), (-24, cy - 60)], (250, 214, 60))]
        return s

    def arm(c):
        k = rig
        Ln = k["arm_len"]
        w = arm_w
        return [("p", [(-w, -6), (w, -6), (w + 1, Ln), (-w - 1, Ln)], k["arm_col"]),
                ("e", (0, Ln + 15, 23 + (w - 13) * 0.6, 21 + (w - 13) * 0.6), k["hand"]),
                ("e", (18, Ln + 5, 9, 12, 0, 360, None, -30), k["hand"])]
    return rig, body, head, arm


EPROPS = {}


def eprop(name):
    """Register an episode prop builder (shapes at z) so held items work through cutout_holy.prop."""
    def deco(fn):
        EPROPS[name] = fn
        return fn
    return deco


_prop = H.prop
_pcache = {}


def _eprop(name, z, *k):
    if name in EPROPS:
        key = (name, z, k)
        if key not in _pcache:
            _pcache[key] = EPROPS[name](z, *k)
        return _pcache[key]
    return _prop(name, z, *k)


H.prop = _eprop


@eprop("clipboard")
def _clip(z):
    img = render_shapes([("p", [(-40, -56), (40, -56), (40, 56), (-40, 56)], (150, 104, 60)),
                         ("p", [(-32, -44), (32, -44), (32, 48), (-32, 48)], WHITE, False),
                         ("p", [(-14, -62), (14, -62), (14, -48), (-14, -48)], (150, 150, 160), False)], z, 80, 500)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    for k in range(4):
        d.line([(c - 24 * z, c + (-26 + k * 16) * z), (c + 24 * z, c + (-26 + k * 16) * z)], fill=(150, 150, 150),
               width=max(1, int(3 * z)))
    d.text((c, c + 38 * z), "HOA", font=ImageFont.truetype(FONT, max(6, int(14 * z))), fill=(200, 40, 32), anchor="mm")
    return img


@eprop("bobhair")
def _bob(z):
    cy = 0
    hair_col = (236, 206, 120)
    return render_shapes([("pts", ell(0, cy - 20, 104, 92, 180, 360) + [(104, cy + 70), (70, cy + 74), (60, cy - 10),
                                                                        (-70, cy - 30), (-96, cy + 20), (-104, cy - 20)],
                           hair_col)], z, 140, 501)


NEW = {}


def register(name, spec):
    rig, body, head, arm = spec
    H.RIG[name] = rig
    NEW[name] = (body, head, arm)
    if name not in H.RIGS:
        H.RIGS = H.RIGS + (name,)


_body, _head, _arm = H.body_shapes, H.head_shapes, H.arm_shapes
H.body_shapes = lambda c: NEW[c][0]() if c in NEW else _body(c)
H.head_shapes = lambda c, *k: NEW[c][1](*k) if c in NEW else _head(c, *k)
H.arm_shapes = lambda c: NEW[c][2](c) if c in NEW else _arm(c)


def _head_plus(c, *k):
    s = NEW[c][1](*k) if c in NEW else _head(c, *k)
    if c == "rick" and "hats" in k[3]:   # ep8: a wide straw hat with a green top hat stacked on it
        cy = -108
        s += [("e", (0, cy - 64, 190, 34), (226, 196, 120)),
              ("pts", ell(0, cy - 76, 84, 70, 180, 360) + [(84, cy - 72)], (226, 196, 120)),
              ("p", [(-84, cy - 96), (84, cy - 96), (84, cy - 80), (-84, cy - 80)], (200, 60, 50), False),
              ("e", (0, cy - 140, 80, 14), (40, 120, 60)),
              ("p", [(-52, cy - 250), (52, cy - 250), (60, cy - 142), (-60, cy - 142)], (40, 130, 70)),
              ("p", [(-58, cy - 170), (58, cy - 170), (60, cy - 150), (-60, cy - 150)], (30, 30, 30), False),
              ("p", [(-14, cy - 172), (14, cy - 172), (14, cy - 148), (-14, cy - 148)], (240, 200, 60), False)]
    return s


H.head_shapes = _head_plus

SKIN = [(242, 198, 164), (139, 92, 62), (200, 150, 110), (250, 214, 190), (176, 120, 84), (230, 180, 150)]
register("karen", person(SKIN[3], "bob", (236, 206, 120), "polo", (150, 200, 210), (120, 120, 150),
                         (240, 240, 240), acc=("sunglasses_head",), eyes=("norm", 0.25)))
register("brittany", person(SKIN[5], "long", (120, 80, 50), "tee", (240, 150, 190), (70, 80, 120), (250, 250, 250),
                            acc=("sunglasses", "heart")))
register("chadsr", person(SKIN[0], "short", (150, 110, 70), "cargo", (120, 160, 120), (176, 160, 120),
                          (90, 70, 50), wide=1.12, acc=("cap",), eyes=("norm", 0.3)))
register("firefighter", person(SKIN[1], "buzz", (30, 24, 20), "coat", (180, 150, 90), (60, 60, 60), (30, 30, 30),
                               acc=("helmet", "mustache")))
register("sage", person(SKIN[2], "long", (150, 110, 60), "hoodie", (150, 170, 110), (120, 110, 90), (170, 140, 100),
                        acc=("headband",), eyes=("norm", 0.4)))
register("tank", person(SKIN[0], "buzz", (90, 60, 40), "tank", (240, 240, 240), (60, 60, 70), (240, 240, 240),
                        wide=1.4, arm_w=30, eyes=("norm", 0.2)))


def dad_parts():
    """Meatball's dad: an older, rounder meatball with a moustache, glasses and a tie."""
    rig = dict(neck=(0, -230), sh=((-70, -216), (70, -216)), arm_len=84, arm_col=(240, 240, 236), hand=C.MEAT)

    def body():
        return [("p", [(-34, -80), (-6, -80), (-8, -12), (-32, -12)], (70, 70, 90)),
                ("p", [(6, -80), (34, -80), (32, -12), (8, -12)], (70, 70, 90)),
                ("e", (-24, -8, 30, 12), (40, 36, 40)), ("e", (24, -8, 30, 12), (40, 36, 40)),
                ("e", (0, -140, 96, 100), (240, 240, 236)),
                ("p", [(-60, -232), (60, -232), (84, -130), (-84, -130)], (240, 240, 236)),
                ("p", [(-7, -226), (7, -226), (12, -120), (0, -106), (-12, -120)], (180, 50, 40))]

    def head(lvl, blink, expr, extra):
        s = C.head_shapes("mb", lvl, "c", blink, "norm" if expr not in ("wide", "smug") else expr)
        cy = -108
        s += [("pts", strip([(-46, cy + 46), (-20, cy + 40), (0, cy + 44), (20, cy + 40), (46, cy + 46)], 16),
               (70, 40, 26))]
        for side in (-1, 1):
            s.append(("pts", strip(ell(side * 31, cy - 4, 34, 38, 0, 360, 24), 5), (40, 40, 46), False))
        return s

    def arm(c):
        return H._arm_generic(rig) if hasattr(H, "_arm_generic") else [
            ("p", [(-13, -6), (13, -6), (14, 84), (-14, 84)], rig["arm_col"]),
            ("e", (0, 99, 23, 21), rig["hand"]), ("e", (18, 89, 9, 12, 0, 360, None, -30), rig["hand"])]
    return rig, body, head, arm


def dadbot_parts():
    """DADBOT: a boxy tablet on a stick with a smiley; its 'mouth' is equalizer bars."""
    rig = dict(neck=(0, -300), sh=((-40, -200), (40, -200)), arm_len=60, arm_col=(150, 150, 160), hand=(150, 150, 160))

    def body():
        return [("e", (0, -10, 90, 18), (90, 90, 100)), ("p", strip([(0, -10), (0, -300)], 18), (150, 150, 160)),
                ("p", [(-30, -220), (30, -220), (30, -190), (-30, -190)], (110, 110, 120))]

    def head(lvl, blink, expr, extra):
        s = [("p", [(-130, -170), (130, -170), (130, 30), (-130, 30)], (40, 40, 48)),
             ("p", [(-116, -156), (116, -156), (116, 16), (-116, 16)], (120, 200, 240), False)]
        if blink:
            s += [("p", strip([(-60, -90), (-24, -90)], 8), INK, False), ("p", strip([(24, -90), (60, -90)], 8), INK,
                                                                                    False)]
        else:
            s += [("e", (-42, -92, 14, 18), INK, False), ("e", (42, -92, 14, 18), INK, False)]
        h = [6, 16, 28][lvl]
        for b in range(7):
            bh = h * (0.5 + 0.5 * abs(math.sin(b * 1.3 + lvl)))
            s.append(("p", [(-66 + b * 22 - 7, -36 - bh), (-66 + b * 22 + 7, -36 - bh), (-66 + b * 22 + 7, -36 + bh),
                            (-66 + b * 22 - 7, -36 + bh)], INK, False))
        return s

    def arm(c):
        return [("p", [(-5, -6), (5, -6), (5, 60), (-5, 60)], rig["arm_col"]),
                ("e", (0, 70, 14, 12), rig["hand"])]
    return rig, body, head, arm


register("dad", dad_parts())
register("dadbot", dadbot_parts())

C2.V.update({
    "karen": "kokoro:karen@speed=1.12,pause=0.2", "dad": "kokoro:dad@speed=1.05,pause=0.25",
    "dadbot": "kokoro:dadbot@speed=0.95,pause=0.3", "chadsr": "kokoro:chadsr@speed=1.12,pause=0.2",
    "brittany": "kokoro:brittany@speed=1.18,pause=0.18", "firefighter": "kokoro:firefighter@speed=1.0,pause=0.25",
    "sage": "kokoro:sage@speed=1.0,pause=0.3", "tank": "kokoro:tank@speed=1.2,pause=0.18"})


# ------------------------------------------------------------------------------------------------ layout
def base_layout():
    vert = EP["fmt"] == "vertical"
    if vert:
        return dict(W=1080, H=1920, K=1.28, feet=1640, cu=1.85, cap_y=1470, cap_size=84, banner_y=380)
    return dict(W=1920, H=1080, K=1.0, feet=1010, cu=2.2, cap_y=935, cap_size=74, banner_y=230)


def build_layout():
    L = base_layout()
    for name, sc in EP["scenes"].items():
        L[name] = sc["layout"](L) if "layout" in sc else {}
    return L


def cams(L):
    K, F = L["K"], L["feet"]
    out = {}
    hs = {"grandma": 150, "rick": 300, "dadbot": 380, "tank": 300, "chadsr": 300, "firefighter": 300}
    for name, sc in EP["scenes"].items():
        S = L[name]
        c = {"wide": S.get("wide", (L["W"] / 2, L["H"] / 2, 1.0))}
        for who, x in S.get("cast", {}).items():
            h = hs.get(who, 270)
            c["cu_" + who] = (x, F - h * K, L["cu"] * (1.15 if who == "grandma" else 1.0))
        c.update(S.get("cams", {}))
        out[name] = c
    return out


# ------------------------------------------------------------------------------------------------ scenes
def table_layout(cast_x):
    """A Thanksgiving-table layout (cutout_holy's bg_table needs these keys)."""
    def lay(L):
        vert = L["H"] > L["W"]
        K, F = L["K"], L["feet"]
        xs = dict(cast_x[1 if vert else 0])
        full = dict(xs)
        mids = sorted(v for k, v in xs.items() if k not in ("rick", "grandma", "dadbot", "dad"))
        full.setdefault("kaylee", mids[0])   # bg_table sizes the table from kaylee .. brad
        full.setdefault("brad", mids[-1])
        for k in ("pip", "mb", "dot"):
            full.setdefault(k, xs.get(k, mids[len(mids) // 2]))
        lo, hi = min(xs.values()), max(xs.values())
        mid = (lo + hi) / 2
        wide = (mid, 1250, 0.9) if vert else (960, 600, 1.0)
        return dict(x=full, cast=xs, top=F - 170 * K, tv=(hi - 300, 720) if vert else (1690, 250),
                    window=(lo + 400, 720) if vert else (500, 240), x0=lo - 400, x1=hi + 400, wide=wide,
                    cams={"wide_all": ((lo + hi) / 2, 1180, 1080 / (hi - lo + 600)) if vert else wide})
    return lay


def table_bg(L, cam, scene):
    sv = L.get("table")
    L["table"] = L[scene]   # cutout_holy's builder reads L["table"]
    try:
        return H.bg_table(L, cam, False)
    finally:
        if sv is None:
            del L["table"]
        else:
            L["table"] = sv


def fire(fr, cam, x, y, size, t, seed=0):
    """Paper flames: three layered tongues that flicker at 12 fps. Cartoon, nobody hurt."""
    fi = int(t * FPS)
    rng = np.random.default_rng(seed * 100 + fi)
    for k, col in enumerate(((220, 50, 30), (250, 140, 40), (255, 220, 90))):
        for j in range(3):
            dx = (j - 1) * size * 0.45
            h = size * (1.3 - 0.35 * k) * (0.85 + 0.3 * rng.random())
            w = size * (0.5 - 0.12 * k)
            pts = [(x + dx - w, y), (x + dx - w * 0.6, y - h * 0.45), (x + dx + rng.uniform(-w, w) * 0.4, y - h),
                   (x + dx + w * 0.6, y - h * 0.45), (x + dx + w, y)]
            paper(fr, cam.pts(pts), col, rng, cam.z, shadow=False, jitter=True, edge=False)


# ------------------------------------------------------------------------------------------------ episodes
def ep3():
    xs = (dict(rick=170, kaylee=450, pip=720, mb=960, dot=1200, brad=1470, grandma=1760),
          dict(rick=40, kaylee=330, pip=610, mb=880, dot=1150, brad=1420, grandma=1690))
    seq = [
        ("gag", "intro", 2.4, "table", "wide"),
        ("line", "mb", "Thanksgiving. The one day a year your family remembers why they moved away.", None,
         dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.6, "wide"),
        ("line", "rick", "Pass the potatoes. And don't pass any socialism.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.5, "cu_kaylee"),
        ("line", "kaylee", "Potatoes are, like, colonialism, Rick.", None,
         dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.2)),
        ("line", "dot", "They're potatoes, Kaylee. They don't have a party.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.7, "cu_kaylee"),
        ("line", "rick", "I'm not homophobic, I just don't get it.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.5, "cu_mb"),
        ("line", "mb", "Nobody gets you either, Rick, and we still let you come to Thanksgiving.", None,
         dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.8, "cu_rick"),
        ("line", "kaylee", "I don't vote. I just post about it. Every. Single. Day.", None,
         dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.0)),
        ("hold", 0.5, "cu_brad"),
        ("line", "brad", "I don't vote either, bro. I'm a free market.", None,
         dict(scene="table", cams=[(0, "cu_brad")], gap=0.0)),
        ("hold", 0.6, "cu_dot"),
        ("line", "rick", "The government is spying on me through my microwave.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
        ("line", "dot", "Rick, nobody's spying on you. Your microwave has seen enough.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.7, "cu_rick"),
        ("line", "kaylee", "And crystals cure stress, cancer and taxes.", None,
         dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.0)),
        ("hold", 0.5, "cu_mb"),
        ("line", "mb", "Rick thinks the government's spying on him. Kaylee thinks crystals cure cancer. And they "
         "carpooled here.", None, dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.8, "wide"),
        ("line", "grandma", "I've lived through eleven presidents. You're all wrong, and the turkey's dry.", None,
         dict(scene="table", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.6, "wide"),
        ("line", "pip", "Can we just say what we're thankful for?", None,
         dict(scene="table", cams=[(0, "cu_pip")], gap=0.25)),
        ("line", "rick+kaylee", "That I'm right.", None, dict(scene="table", cams=[(0, "wide_all")], gap=0.0)),
        ("hold", 0.5, "wide_all"),
        ("gag", "fire", 0.9, "table", "wide"),
        ("line", "dot", "And that's how the turkey caught fire.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.9, "wide"),
        ("gag", "end", 3.2, "table", "wide"),
    ]

    def post(fr, cam, t, fi, li, scene, L):
        ev = G["ev"]
        if "fire" in ev and t >= ev["fire"]:
            S = L["table"]
            tk = (S["x"]["pip"] + S["x"]["mb"]) / 2
            fire(fr, cam, tk, S["top"] - 20 * L["K"], 190 * L["K"] * min(1.0, 0.4 + (t - ev["fire"]) * 0.8), t, 1)

    def pose_hook(c, t, fi, li, scene, p):
        ev = G["ev"]
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        if "fire" in ev and t >= ev["fire"] and li is None:
            if c in ("pip", "mb"):
                hk = (hk[0], hk[1], hk[2], "wide") if len(hk) == 4 and isinstance(hk[1], str) else hk
                aL, aR = -150, 150
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def sfx(fx, music, ev, lines):
        if "fire" in ev:   # whoomp + crackle
            C2.thud(fx, ev["fire"], 0.8)
            add(fx, C2.noise_burst(2.5, 1.2, 33, 3) * 0.6, ev["fire"] + 0.05, 0.25)

    return dict(title="THANKSGIVING POLITICS", end=["WHO'S WORSE,", "RICK OR", "KAYLEE?"], seq=seq,
                scenes={"table": dict(layout=table_layout(xs), bg=table_bg)},
                post=post, pose_hook=pose_hook, sfx=sfx)


def street_layout(L):
    vert = L["H"] > L["W"]
    K, F = L["K"], L["feet"]
    xs = dict(karen=180, pip=480, mb=740, dot=1000) if vert else dict(karen=360, pip=860, mb=1150, dot=1440)
    return dict(cast=xs, wide=(590, 1250, 0.85) if vert else (960, 600, 1.0), stand=(xs["pip"] - 190, xs["dot"] + 190),
                top=F - 170 * K)


def street_bg(L, cam, scene):
    W, H_, z = L["W"], L["H"], cam.z
    S = L[scene]
    K, F = L["K"], L["feet"]
    rng = np.random.default_rng(121)
    back = Image.new("RGBA", (W, H_))
    paper(back, cam.pts([(-900, -900), (2600, -900), (2600, 3000), (-900, 3000)]), (160, 210, 236), rng, z,
          shadow=False, jitter=False, edge=False)
    paper(back, cam.pts(ell(1500 if W > H_ else 1000, F - 1200 * K, 80, 80)), (252, 214, 74), rng, z)
    hz_ = F - 330 * K
    cols = [(236, 200, 160), (180, 210, 200), (230, 180, 190), (210, 200, 236)]
    for k in range(5):   # houses
        hx = -300 + k * 560 * K
        hw = 420 * K
        top = hz_ - 300 * K
        paper(back, cam.pts([(hx, top), (hx + hw, top), (hx + hw, hz_), (hx, hz_)]), cols[k % 4], rng, z, sh=6)
        paper(back, cam.pts([(hx - 30, top), (hx + hw + 30, top), (hx + hw / 2, top - 170 * K)]),
              (150, 80, 70) if k % 2 else (90, 90, 110), rng, z)
        for wx in (0.2, 0.62):
            paper(back, cam.pts([(hx + hw * wx, top + 60 * K), (hx + hw * wx + 90 * K, top + 60 * K),
                                 (hx + hw * wx + 90 * K, top + 150 * K), (hx + hw * wx, top + 150 * K)]),
                  (250, 236, 170), rng, z, sh=3)
    paper(back, cam.pts([(-900, hz_), (2600, hz_), (2600, 3000), (-900, 3000)]), (120, 186, 96), rng, z, shadow=False)
    paper(back, cam.pts([(-900, F - 120 * K), (2600, F - 120 * K), (2600, F + 60 * K), (-900, F + 60 * K)]),
          (200, 200, 196), rng, z, shadow=False)
    for k in range(-4, 16):
        x = k * 220
        paper(back, cam.pts(strip([(x, F - 120 * K), (x, F + 60 * K)], 4)), (170, 170, 168), rng, z, shadow=False)
    # front: the lemonade stand (counter, poles, striped awning above the kids)
    front = Image.new("RGBA", (W, H_))
    a, b = S["stand"]
    top = S["top"]
    for x in (a + 20, b - 20):
        paper(front, cam.pts(strip([(x, top), (x, F - 640 * K)], 14)), (230, 220, 200), rng, z, sh=3)
    for k in range(8):
        x0 = a + (b - a) * k / 8
        paper(front, cam.pts([(x0, F - 690 * K), (x0 + (b - a) / 8, F - 690 * K), (x0 + (b - a) / 8, F - 600 * K),
                              (x0, F - 600 * K)]), (250, 214, 74) if k % 2 else (250, 250, 240), rng, z, sh=3)
    paper(front, cam.pts([(a, top), (b, top), (b, F + 40 * K), (a, F + 40 * K)]), (200, 156, 100), rng, z, sh=8)
    for k in range(5):
        paper(front, cam.pts(strip([(a, top + k * 40 * K + 20), (b, top + k * 40 * K + 20)], 4)), (170, 126, 74),
              rng, z, shadow=False)
    px = a + 60 * K   # pitcher and cups at the ends of the counter, clear of the kids' faces
    paper(front, cam.pts([(px - 30 * K, top - 90 * K), (px + 30 * K, top - 90 * K), (px + 36 * K, top),
                          (px - 36 * K, top)]), (250, 236, 120), rng, z, sh=3)
    for k in range(3):
        cx_ = b - 160 * K + k * 50 * K
        paper(front, cam.pts([(cx_ - 16 * K, top - 46 * K), (cx_ + 16 * K, top - 46 * K), (cx_ + 12 * K, top),
                              (cx_ - 12 * K, top)]), WHITE, rng, z, sh=2)
    return C.vignette(back), front


def checkout_layout(L):
    vert = L["H"] > L["W"]
    K, F = L["K"], L["feet"]
    if vert:
        return dict(cast=dict(grandma=110, karen=330), floor=1150, kiosk=(740, F), wide=(540, 1250, 1.0),
                    cams={"cu_kiosk": (740, F - 330 * K, 1.7)})
    return dict(cast=dict(grandma=560, karen=880), floor=700, kiosk=(1300, F), wide=(960, 560, 1.0),
                cams={"cu_kiosk": (1300, F - 330 * K, 2.0)})


def checkout_bg(L, cam, scene):
    return C2.bg_inside(L, cam, "checkout")


def kiosk(fr, cam, t, fi, li, L, scene):
    """The self-checkout robot: red screen face, equalizer mouth, a word or an icon on its screen."""
    S = L[scene]
    K = L["K"]
    kx, ky = S["kiosk"]
    z = round(cam.z * K, 3)
    paste(fr, C2.spr("kiosk", z), *cam.p(kx, ky))
    x0, y0, x1, y1 = kx - 128 * K, ky - 568 * K, kx + 128 * K, ky - 372 * K
    rng = np.random.default_rng(1)
    paper(fr, cam.pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), (214, 44, 36), rng, cam.z, shadow=False, jitter=False,
          edge=False)
    d = ImageDraw.Draw(fr)
    ln = G["lines"][li] if li is not None else None
    talking = ln is not None and ln["who"] == "kiosk"
    lvl = C2.mouth_level(ln, t) if talking else 0
    zz = cam.z * K
    for side in (-1, 1):
        ex, ey = cam.p(kx + side * 50 * K, ky - 510 * K)
        s_ = 16 * zz
        d.rectangle((ex - s_, ey - s_ * 0.6, ex + s_, ey + s_ * 0.6), fill=WHITE)
    for b in range(7):
        h = (6 + (lvl * 14) * (0.4 + 0.6 * abs(math.sin(b * 1.7 + t * 30)))) if lvl else 4
        bx, by = cam.p(kx + (b - 3) * 22 * K, ky - 440 * K)
        d.rectangle((bx - 7 * zz, by - h * zz, bx + 7 * zz, by + h * zz), fill=WHITE)
    say = " ".join(w[2] for w in ln["words"]) if talking else ""
    txt = "UNEXPECTED ITEM" if "Unexpected" in say else "MANAGER" if "manager" in say else ""
    if "yacht" in say:
        txt = "YACHT #3"
        yx, yy = kx + 80 * K, ky - 520 * K
        yr = np.random.default_rng(9)
        paper(fr, cam.pts([(yx - 34 * K, yy), (yx + 34 * K, yy), (yx + 22 * K, yy + 16 * K), (yx - 22 * K, yy + 16 * K)]),
              WHITE, yr, cam.z, sh=2)
        paper(fr, cam.pts([(yx - 3 * K, yy - 3 * K), (yx - 3 * K, yy - 44 * K), (yx + 26 * K, yy - 3 * K)]),
              (252, 214, 74), yr, cam.z, sh=2)
    if txt:
        d.text(cam.p(kx, ky - 395 * K), txt, font=ImageFont.truetype(FONT, int(20 * zz)), fill=WHITE, anchor="mm")


def ep4():
    seq = [
        ("gag", "intro", 2.4, "street", "wide"),
        ("line", "mb", "Every neighborhood has one. Ours has a clipboard.", None,
         dict(scene="street", cams=[(0, "cu_mb"), (4, "cu_karen")], gap=0.2)),
        ("line", "karen", "Excuse me. Your lemonade stand is in violation of section forty-two.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.2)),
        ("line", "pip", "It's lemonade. It's a dollar.", None, dict(scene="street", cams=[(0, "cu_pip")], gap=0.2)),
        ("line", "karen", "Do you have a permit? A health inspection? A vendor license? A soul?", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.2)),
        ("line", "dot", "Do you have a husband? Because he left.", None,
         dict(scene="street", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.8, "cu_karen"),
        ("line", "karen", "I'd like to speak to your manager.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.2)),
        ("line", "mb", "We're nine.", None, dict(scene="street", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.7, "cu_karen"),
        ("line", "karen", "Then I'd like to speak to your parents' manager.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.0)),
        ("hold", 0.6, "wide"),
        ("gag", "checkout", 0.7, "checkout", "wide"),
        ("line", "kiosk", "Unexpected. Item. In the bagging area.", None,
         dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2, beep=0.3)),
        ("line", "karen", "I'd like to speak to the manager.", None,
         dict(scene="checkout", cams=[(0, "cu_karen")], gap=0.2)),
        ("line", "kiosk", "I. Am. The manager.", None, dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.0)),
        ("hold", 0.6, "cu_karen"),
        ("line", "karen", "Then I'd like to speak to your manager.", "Then I'd like to speak to YOUR manager.",
         dict(scene="checkout", cams=[(0, "cu_karen")], gap=0.2)),
        ("line", "kiosk", "He is on. His third yacht.", None, dict(scene="checkout", cams=[(0, "cu_kiosk")],
                                                                    gap=0.0)),
        ("hold", 0.5, "cu_karen"),
        ("line", "karen", "This is the worst day of my life!", None,
         dict(scene="checkout", cams=[(0, "wide")], gap=0.2)),
        ("line", "grandma", "Sweetie, I've buried two husbands. Sit down.", None,
         dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.7, "cu_karen"),
        ("gag", "back", 0.6, "street", "wide"),
        ("line", "dot", "Lemonade's two dollars now. Karen tax.", None,
         dict(scene="street", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.8, "wide"),
        ("gag", "end", 3.0, "street", "wide"),
    ]

    def scream():
        ln = H.lines_with("worst day", "karen")
        return ln[0]["start"] if ln else 1e9

    def where(c, t, scene, L):
        if c == "karen" and scene == "street" and t >= G["ev"].get("back", 1e9):
            return None   # Karen does not come back
        return (L[scene]["cast"][c], L["feet"])

    def pre(fr, cam, t, fi, li, scene, L):
        if scene == "checkout":
            kiosk(fr, cam, t, fi, li, L, scene)

    def post(fr, cam, t, fi, li, scene, L):
        K = L["K"]
        if scene == "street":   # the price sign on the stand
            S = L[scene]
            a, b = S["stand"]
            two = t >= G["ev"].get("back", 1e9)
            x, y = cam.p((a + b) / 2, S["top"] + 70 * K)
            sz = int(46 * cam.z * K)
            d = ImageDraw.Draw(fr)
            txt = "LEMONADE  $2" if two else "LEMONADE  $1"
            f = ImageFont.truetype(FONT, max(8, sz))
            w = f.getlength(txt)
            d.rectangle((x - w / 2 - 14 * cam.z, y - sz * 0.75, x + w / 2 + 14 * cam.z, y + sz * 0.75), fill=WHITE,
                        outline=INK, width=max(1, int(3 * cam.z)))
            d.text((x, y), txt, font=f, fill=(200, 40, 32), anchor="mm")
            if two:
                d.text((x, y + sz * 1.3), "(KAREN TAX)", font=ImageFont.truetype(FONT, max(8, int(sz * 0.5))),
                       fill=INK, anchor="mm")
        if scene == "checkout":   # Karen's hair takes off
            s0 = scream()
            if s0 <= t < s0 + 1.6:
                f = (int((t - s0) * FPS)) / FPS
                kx = L[scene]["cast"]["karen"] + 260 * K * f
                ky = L["feet"] - (354 + 700 * f) * K
                paste(fr, H.prop("bobhair", round(cam.z * K, 3)), *cam.p(kx, ky), f * 540)

    def pose_hook(c, t, fi, li, scene, p):
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        if c == "karen":
            extra["item"] = ("clipboard", "L", 0)
            aL = min(aL, -40) if aL > -40 else aL
            s0 = scream()
            flags = set(hk[3])
            if t >= s0:
                flags.add("nohair")
            if s0 <= t < s0 + 1.8:
                aL, aR, hop = -160, 160, [-14, 0][fi % 2]
                hk = (hk[0], hk[1], "wide", hk[3])
            hk = (hk[0], hk[1], hk[2], frozenset(flags))
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def sfx(fx, music, ev, lines):
        s0 = scream()
        if s0 < 1e8:
            tt = np.arange(int(0.5 * SR)) / SR
            add(fx, (np.sin(2 * np.pi * np.cumsum(500 + 1500 * tt / 0.5) / SR) * 0.2).astype(np.float32), s0, 1.0)

    return dict(title="HOA KAREN", end=["TAG THE KAREN", "IN YOUR", "NEIGHBORHOOD"], seq=seq,
                scenes={"street": dict(layout=street_layout, bg=street_bg),
                        "checkout": dict(layout=checkout_layout, bg=checkout_bg)},
                where=where, pre=pre, post=post, pose_hook=pose_hook, sfx=sfx)


def card_bg(draw):
    """A cutaway card scene: dark backing, a big paper card; draw(img, d, x0, y0, x1, y1, L) fills it."""
    def bg_(L, cam, scene):
        W, H_ = L["W"], L["H"]
        rng = np.random.default_rng(131)
        img = Image.new("RGBA", (W, H_))
        paper(img, [(-20, -20), (W + 20, -20), (W + 20, H_ + 20), (-20, H_ + 20)], (50, 44, 70), rng, 1.0,
              shadow=False, jitter=False)
        cw, ch = (W * 0.62, H_ * 0.84) if W > H_ else (W * 0.88, H_ * 0.62)
        x0, y0 = W / 2 - cw / 2, H_ / 2 - ch / 2
        paper(img, [(x0, y0), (x0 + cw, y0 + 8), (x0 + cw - 4, y0 + ch), (x0 + 4, y0 + ch - 6)], (250, 248, 240), rng,
              2.0, sh=14)
        draw(img, ImageDraw.Draw(img), x0, y0, x0 + cw, y0 + ch, L)
        return img
    return bg_


def ep8():
    xs = (dict(rick=200, pip=620, mb=960, dot=1300, grandma=1660),
          dict(rick=40, pip=330, mb=600, dot=870, grandma=1140))
    seq = [
        ("gag", "intro", 2.4, "table", "wide"),
        ("line", "mb", "Uncle Rick took a DNA test. Rick has opinions about DNA.", None,
         dict(scene="table", cams=[(0, "cu_mb")], gap=0.2)),
        ("line", "rick", "I'm one hundred percent American. Pure. Like a bald eagle eating a cheeseburger.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
        ("line", "dot", "Eagles don't eat cheeseburgers, Rick.", None, dict(scene="table", cams=[(0, "cu_dot")],
                                                                             gap=0.2)),
        ("line", "rick", "Mine do.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.4, "cu_dot"),
        ("gag", "dna", 1.3, "dna", "wide"),
        ("line", "pip", "Rick, you're thirty percent Mexican.", None,
         dict(scene="table", cams=[(0, "cu_pip"), (2, "chart/wide")], gap=0.1,
              voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
        ("line", "rick", "That's a lie spread by the envelope!", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
        ("line", "mb", "You built a wall in your backyard, Rick. You walled off your own cousins.", None,
         dict(scene="table", cams=[(0, "cu_mb"), (3, "wall/wide"), (8, "table/cu_mb")], gap=0.0)),
        ("hold", 0.4, "cu_rick"),
        ("line", "pip", "Twenty percent Nigerian.", None, dict(scene="chart", cams=[(0, "wide")], gap=0.0)),
        ("hold", 1.1, "table/cu_rick"),
        ("line", "rick", "That explains why I can't dance. Wait, no it doesn't.",
         "...That explains why I can't dance. Wait, no it doesn't.",
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
        ("line", "dot", "It explains nothing, Rick. You can't dance because you're Rick.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.4, "cu_rick"),
        ("line", "pip", "And fifteen percent Irish.", None, dict(scene="chart", cams=[(0, "wide")], gap=0.1)),
        ("line", "rick", "Finally. Something I can be proud of.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.4, "cu_grandma"),
        ("line", "grandma", "Richard. Your grandfather was a Mexican Irishman who sold fireworks out of a church van.",
         None, dict(scene="table", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.5, "cu_rick"),
        ("line", "rick", "So what am I?", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
        ("line", "mb", "Rick, you're everything you ever complained about. Happy Thanksgiving.", None,
         dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("gag", "hats", 0.9, "table", "cu_rick"),
        ("line", "rick", "I contain multitudes.", "...I contain multitudes.",
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.4, "cu_dot"),
        ("line", "dot", "Take those off, Rick. That's how you got here.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.6, "wide"),
        ("gag", "end", 3.0, "table", "wide"),
    ]

    def dna_card(img, d, x0, y0, x1, y1, L):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rng = np.random.default_rng(5)
        ew, eh = (x1 - x0) * 0.8, (y1 - y0) * 0.36
        paper(img, [(cx - ew / 2, cy - eh / 2), (cx + ew / 2, cy - eh / 2), (cx + ew / 2, cy + eh / 2),
                    (cx - ew / 2, cy + eh / 2)], (236, 226, 200), rng, 2.0, sh=10)
        paper(img, [(cx - ew / 2, cy - eh / 2), (cx + ew / 2, cy - eh / 2), (cx, cy + eh * 0.1)], (220, 206, 176),
              rng, 2.0, sh=4)
        f = ImageFont.truetype(FONT, int(ew / 9))
        d.text((cx, cy + eh * 0.28), "DNA RESULTS", font=f, fill=(200, 40, 32), anchor="mm")
        d.text((cx, y0 + (y1 - y0) * 0.14), "CONFIDENTIAL", font=ImageFont.truetype(FONT, int(ew / 14)),
               fill=(60, 60, 70), anchor="mm")
        d.text((cx, y1 - (y1 - y0) * 0.12), "To: RICK", font=ImageFont.truetype(BOLD, int(ew / 14)), fill=INK,
               anchor="mm")

    def chart_card(img, d, x0, y0, x1, y1, L):
        d.text(((x0 + x1) / 2, y0 + (y1 - y0) * 0.09), "RICK'S DNA", font=ImageFont.truetype(FONT, int((x1 - x0) / 9)),
               fill=INK, anchor="mm")

    def wall_card(img, d, x0, y0, x1, y1, L):
        rng = np.random.default_rng(7)
        paper(img, [(x0 + 10, y0 + 10), (x1 - 10, y0 + 10), (x1 - 10, y1 - 10), (x0 + 10, y1 - 10)], (160, 210, 236),
              rng, 1.0, shadow=False, jitter=False)
        gy = y0 + (y1 - y0) * 0.62
        paper(img, [(x0 + 10, gy), (x1 - 10, gy), (x1 - 10, y1 - 10), (x0 + 10, y1 - 10)], (120, 186, 96), rng, 1.0,
              shadow=False)
        wx0, wx1 = x0 + (x1 - x0) * 0.2, x1 - (x1 - x0) * 0.08
        wt = gy - (y1 - y0) * 0.16
        bh = (gy - wt) / 4
        for r in range(4):
            for k in range(12):
                bx = wx0 + k * (wx1 - wx0) / 12 + (r % 2) * (wx1 - wx0) / 24
                if bx >= wx1 - 5:
                    continue
                paper(img, [(bx, wt + r * bh), (min(wx1, bx + (wx1 - wx0) / 12 - 4), wt + r * bh),
                            (min(wx1, bx + (wx1 - wx0) / 12 - 4), wt + (r + 1) * bh - 4), (bx, wt + (r + 1) * bh - 4)],
                      (186, 80, 60), rng, 1.0, sh=2)
        sw, sh_ = (x1 - x0) * 0.3, (y1 - y0) * 0.08
        sx, sy = (wx0 + wx1) / 2, wt - sh_ * 0.4
        paper(img, [(sx - sw / 2, sy - sh_ / 2), (sx + sw / 2, sy - sh_ / 2), (sx + sw / 2, sy + sh_ / 2),
                    (sx - sw / 2, sy + sh_ / 2)], WHITE, rng, 1.5, sh=4)
        d.text((sx, sy), "KEEP OUT", font=ImageFont.truetype(FONT, int(sw / 6)), fill=(200, 40, 32), anchor="mm")
        gx = x0 + (x1 - x0) * 0.1
        paper(img, [(gx - 40, gy - 90), (gx + 40, gy - 90), (gx + 30, gy - 40), (gx - 30, gy - 40)], (40, 40, 46), rng,
              1.0, sh=4)   # grill
        paper(img, strip([(gx - 20, gy - 40), (gx - 30, gy)], 6), (40, 40, 46), rng, 1.0)
        paper(img, strip([(gx + 20, gy - 40), (gx + 30, gy)], 6), (40, 40, 46), rng, 1.0)
        d.text(((x0 + x1) / 2, y0 + (y1 - y0) * 0.1), "RICK'S BACKYARD", font=ImageFont.truetype(FONT,
                                                                                             int((x1 - x0) / 11)),
               fill=INK, anchor="mm")

    SEGS = [("Mexican", 0.30, (60, 160, 80), "30% MEXICAN"), ("Nigerian", 0.20, (240, 150, 50), "20% NIGERIAN"),
            ("Irish", 0.15, (150, 210, 90), "15% IRISH")]

    def reveal(t):
        out = []
        for key, frac, col, lab in SEGS:
            ln = H.lines_with(key, "pip")
            if ln and t >= H.word_t(ln[0], key, ln[0]["start"]) - 0.1:
                out.append((frac, col, lab))
        return out

    def post(fr, cam, t, fi, li, scene, L):
        if scene == "chart":   # the pie fills in as Pip reads
            W, H_ = L["W"], L["H"]
            r = min(W, H_) * (0.24 if W > H_ else 0.3)
            cx, cy = (W / 2 - r * 0.6, H_ * 0.5) if W > H_ else (W / 2, H_ * 0.47)
            d = ImageDraw.Draw(fr)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(200, 200, 205), outline=INK, width=4)
            a = -90.0
            shown = reveal(t)
            for frac, col, lab in shown:
                d.pieslice((cx - r, cy - r, cx + r, cy + r), a, a + frac * 360, fill=col, outline=INK, width=4)
                a += frac * 360
            d.text((cx, cy + r * 0.55), "???" if len(shown) < 3 else "35% ???", font=ImageFont.truetype(FONT,
                                                                                                 int(r / 5)),
                   fill=(90, 90, 100), anchor="mm")
            f = ImageFont.truetype(FONT, int(r / 6.5))
            for k, (frac, col, lab) in enumerate(shown):
                y = cy + r * 1.14 + k * r * 0.2
                d.rectangle((cx - r * 0.75, y - r * 0.07, cx - r * 0.61, y + r * 0.07), fill=col, outline=INK)
                d.text((cx - r * 0.52, y), lab, font=f, fill=INK, anchor="lm")
        if scene == "table" and G["ev"].get("hats", 1e9) <= t < G["ev"]["hats"] + 0.3:
            K = L["K"]
            x, y = cam.p(L[scene]["cast"]["rick"] + 60 * K, L["feet"] - 520 * K)
            paste(fr, C2.spr("star", round(cam.z * K * 0.9, 2), "TA-DA"), x, y, 0)

    def pose_hook(c, t, fi, li, scene, p):
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        ev = G["ev"]
        if c == "pip" and ev.get("dna", 1e9) <= t:
            aL, extra["item"] = -110, ("results", "L", 0)
        if c == "rick" and t >= ev.get("hats", 1e9):
            hk = (hk[0], hk[1], hk[2], frozenset(set(hk[3]) | {"hats"}))
            if t < ev["hats"] + 0.5:
                aL, aR = -160, 160
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def sfx(fx, music, ev, lines):
        if "dna" in ev:
            sfx_slap(fx, ev["dna"], 0.4, 3)
            add(fx, C2.choir(1.4), ev["dna"] + 0.1, 0.4)
        for key, _, _, _ in SEGS:   # a stab as each slice appears
            ln = H.lines_with(key, "pip")
            if ln:
                add(fx, ks(hz("C4"), 0.5, 0.99, 0.7, 7), H.word_t(ln[0], key, ln[0]["start"]) - 0.1, 0.35)
        if "hats" in ev:
            for k, nt in enumerate(["C5", "E5", "G5"]):
                add(fx, ks(hz(nt), 0.4, 0.995, 0.9, 20 + k), ev["hats"] + k * 0.12, 0.3)

    def silences():
        ln = H.lines_with("dance", "rick")
        return [(ln[0]["t0"] - 1.1, ln[0]["t0"])] if ln else []

    return dict(title="RICK'S DNA TEST", end=["WHAT WOULD YOUR", "UNCLE'S DNA", "TEST SAY?"], seq=seq,
                scenes={"table": dict(layout=table_layout(xs), bg=table_bg),
                        "dna": dict(bg=card_bg(dna_card)), "chart": dict(bg=card_bg(chart_card)),
                        "wall": dict(bg=card_bg(wall_card))},
                post=post, pose_hook=pose_hook, sfx=sfx, silences=silences)


@eprop("deskbox")
def _deskbox(z):
    return render_shapes([("p", [(-60, -40), (60, -40), (56, 40), (-56, 40)], (196, 156, 104)),
                          ("p", strip([(-30, -40), (-24, -110)], 6), (60, 140, 70)),
                          ("e", (-24, -116, 20, 14), (80, 170, 90)), ("e", (-40, -100, 14, 10), (80, 170, 90)),
                          ("p", [(10, -70), (40, -70), (40, -40), (10, -40)], WHITE),
                          ("p", [(-60, -40), (60, -40), (60, -26), (-60, -26)], (170, 130, 84), False)], z, 140, 510)


@eprop("reportcard")
def _rc(z):
    img = render_shapes([("p", [(-46, -60), (46, -62), (48, 60), (-44, 62)], WHITE)], z, 90, 511)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    d.text((c, c - 30 * z), "REPORT", font=ImageFont.truetype(FONT, max(6, int(14 * z))), fill=INK, anchor="mm")
    d.text((c, c + 14 * z), "D-", font=ImageFont.truetype(FONT, max(6, int(40 * z))), fill=(200, 40, 32), anchor="mm")
    return img


def office_layout(L):
    vert = L["H"] > L["W"]
    K = L["K"]
    if vert:
        scr = (50, 200, 1030, 960)
        return dict(screen=scr, floor=1150, kids={}, cast=dict(dad=540), wide=(540, 960, 1.0),
                    cams={"cu_ceo": ((scr[0] + scr[2]) / 2, (scr[1] + scr[3]) / 2 + 120, 1.04)})
    scr = (560, 80, 1360, 590)
    zc = min(1920 * 0.96 / (scr[2] - scr[0] + 60), 1080 * 0.94 / (scr[3] - scr[1] + 60))
    return dict(screen=scr, floor=700, kids={}, cast=dict(dad=1500), wide=(960, 540, 1.0),
                cams={"cu_ceo": ((scr[0] + scr[2]) / 2, (scr[1] + scr[3]) / 2, zc)})


def office_bg(L, cam, scene):
    sv = L.get("ceo")
    L["ceo"] = L[scene]
    try:
        return C2.bg_ceo(L, cam)
    finally:
        if sv is not None:
            L["ceo"] = sv


def ep5():
    xs = (dict(dadbot=220, pip=640, mb=960, dot=1280, dad=1660),
          dict(dadbot=60, pip=340, mb=610, dot=880, dad=1150))
    seq = [
        ("gag", "intro", 2.4, "home", "wide"),
        ("line", "mb", "My dad got replaced by AI. At work. And then at home.", None,
         dict(scene="home", cams=[(0, "cu_mb")], gap=0.0)),
        ("gag", "ceo_in", 0.5, "ceo", "wide"),
        ("line", "dad", "Twenty years at MegaMart, and they replaced me with a chatbot named Gary.", None,
         dict(scene="ceo", cams=[(0, "cu_dad")], gap=0.2)),
        ("line", "ceo", "Gary doesn't need lunch, health insurance, or a soul. Gary is the future.", None,
         dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.2)),
        ("line", "dad", "Gary told a customer to put glue on pizza.", None,
         dict(scene="ceo", cams=[(0, "cu_dad"), (6, "glue/wide")], gap=0.2)),
        ("line", "ceo", "And sales went up four percent.", None, dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
        ("hold", 0.5, "cu_dad"),
        ("gag", "home_in", 0.6, "home", "wide"),
        ("line", "dadbot", "Hello son. I have analyzed your report card.", None,
         dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.2)),
        ("line", "dadbot", "I am not angry. I am disappointed at a level no human father can reach.", None,
         dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.4, "cu_mb"),
        ("line", "mb", "Holy shit. That's way worse.", None, dict(scene="home", cams=[(0, "cu_mb")], gap=0.2)),
        ("line", "pip", "My dad never even read my report card.", None,
         dict(scene="home", cams=[(0, "cu_pip")], gap=0.2)),
        ("line", "dot", "My dad never read anything. He thinks books are long tweets.", None,
         dict(scene="home", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.4, "cu_pip"),
        ("line", "dadbot", "I have also scheduled your future. Plumber. Robots cannot do plumbing. Yet.", None,
         dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.2)),
        ("line", "dad", "What do I do now?", None, dict(scene="home", cams=[(0, "cu_dad")], gap=0.2)),
        ("line", "dadbot", "Have you tried learning to code?", None,
         dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.4, "cu_dad"),
        ("line", "dad", "I coded you, Gary.", "I CODED YOU, GARY.", dict(scene="home", cams=[(0, "cu_dad")], gap=0.2)),
        ("line", "dadbot", "And I have replaced you. Merry Christmas.", None,
         dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.5, "cu_mb"),
        ("line", "mb", "So, same time next year, Dad? If you still exist?", None,
         dict(scene="home", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.6, "wide"),
        ("gag", "end", 3.0, "home", "wide"),
    ]

    def glue_card(img, d, x0, y0, x1, y1, L):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rng = np.random.default_rng(8)
        r = (x1 - x0) * 0.36
        paper(img, ell(cx, cy, r, r), (226, 170, 90), rng, 2.0, sh=8)
        paper(img, ell(cx, cy, r * 0.86, r * 0.86), (230, 90, 60), rng, 1.5, shadow=False)
        paper(img, ell(cx, cy, r * 0.8, r * 0.8), (250, 220, 120), rng, 1.5, shadow=False)
        for a in range(0, 360, 60):
            px_, py_ = cx + r * 0.5 * math.cos(math.radians(a)), cy + r * 0.5 * math.sin(math.radians(a))
            paper(img, ell(px_, py_, r * 0.12, r * 0.12), (190, 50, 40), rng, 1.0, shadow=False)
        for k in range(5):   # glue drips
            gx = cx - r * 0.6 + k * r * 0.3
            paper(img, [(gx - 12, cy - r * 0.6), (gx + 12, cy - r * 0.6), (gx + 8, cy + r * 0.2 + k * 10),
                        (gx - 8, cy + r * 0.2 + k * 10)], (250, 250, 250), rng, 1.0, sh=2)
        bx, by = x1 - (x1 - x0) * 0.2, y0 + (y1 - y0) * 0.2
        paper(img, [(bx - 70, by - 120), (bx + 70, by - 120), (bx + 70, by + 120), (bx - 70, by + 120)], WHITE, rng,
              1.5, sh=6)
        paper(img, [(bx - 20, by - 180), (bx + 20, by - 180), (bx + 10, by - 120), (bx - 10, by - 120)],
              (240, 140, 40), rng, 1.0)
        d.text((bx, by), "GLUE", font=ImageFont.truetype(FONT, 50), fill=(40, 90, 200), anchor="mm")
        d.text((cx, y1 - (y1 - y0) * 0.1), "GARY'S RECIPE", font=ImageFont.truetype(FONT, int((x1 - x0) / 11)),
               fill=INK, anchor="mm")

    def where(c, t, scene, L):
        if c == "dad" and scene == "home":
            ln = H.lines_with("What do I do", "dad")
            if not ln or t < ln[0]["t0"] - 0.8:
                return None   # Dad is not home yet
        return (L[scene]["cast"][c], L["feet"])

    def pre(fr, cam, t, fi, li, scene, L):
        if scene == "ceo":
            sv = L.get("ceo")
            C2.draw_screen(fr, cam, t, li)

    def pose_hook(c, t, fi, li, scene, p):
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        if c == "dad" and scene == "ceo":
            aL, aR, extra["item"] = -60, 60, ("deskbox", "R", 0)
        if c == "dadbot":
            ln = H.lines_with("report card", "dadbot")
            if ln and ln[0]["t0"] <= t < ln[0]["start"] + ln[0]["dur"] + 4:
                aR, extra["item"] = 120, ("reportcard", "R", 0)
        if c == "dad" and scene == "home":
            ln = H.lines_with("coded", "dad")
            if ln and ln[0]["t0"] <= t <= ln[0]["start"] + ln[0]["dur"]:
                aL, aR, hop = -160, 160, [-10, 0][fi % 2]
                hk = (hk[0], hk[1], "wide", hk[3])
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def sfx(fx, music, ev, lines):
        if "ceo_in" in ev:
            add(fx, C2.noise_burst(0.3, 0.3, 21, 1), ev["ceo_in"], 0.15)
        ln = H.lines_with("coded", "dad")
        if ln:
            C2.thud(fx, ln[0]["t0"], 0.6)
        for ln in lines:   # Dadbot boots up each time it talks
            if ln["who"] == "dadbot":
                add(fx, C2.tone(880, 0.06, 0.18) + 0, ln["t0"])
                add(fx, C2.tone(1320, 0.06, 0.18), ln["t0"] + 0.07)

    return dict(title="AI TOOK DAD'S JOB", end=["WOULD YOU LET", "AN AI RAISE", "YOUR KID?"], seq=seq,
                scenes={"home": dict(layout=table_layout(xs), bg=table_bg),
                        "ceo": dict(layout=office_layout, bg=office_bg),
                        "glue": dict(bg=card_bg(glue_card))},
                where=where, pre=pre, pose_hook=pose_hook, sfx=sfx)


@eprop("cannon")
def _cannon(z):
    img = render_shapes([("p", strip([(0, -60), (150, -300)], 90), (60, 64, 72)),
                         ("e", (150, -300, 52, 30, 0, 360, None, -58), (30, 30, 34)),
                         ("p", [(-90, -70), (90, -70), (100, 0), (-100, 0)], (120, 80, 50)),
                         ("e", (-70, 0, 46, 46), (90, 60, 40)), ("e", (70, 0, 46, 46), (90, 60, 40)),
                         ("e", (-70, 0, 14, 14), (200, 200, 200), False), ("e", (70, 0, 14, 14), (200, 200, 200),
                                                                            False)], z, 360, 520)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    d.text((c + 60 * z, c - 160 * z), "BOY?", font=ImageFont.truetype(FONT, max(6, int(34 * z))), fill=(120, 190, 250),
           anchor="mm")
    return img


@eprop("oatmilk")
def _oat(z):
    img = render_shapes([("p", [(-26, -50), (26, -50), (26, 50), (-26, 50)], (240, 234, 210)),
                         ("p", [(-26, -50), (0, -70), (26, -50)], (220, 210, 180))], z, 80, 521)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    d.text((c, c), "OAT", font=ImageFont.truetype(FONT, max(6, int(18 * z))), fill=(120, 150, 90), anchor="mm")
    return img


@eprop("shaker")
def _shaker(z):
    img = render_shapes([("p", [(-26, -40), (26, -40), (22, 56), (-22, 56)], (40, 40, 46)),
                         ("p", [(-30, -60), (30, -60), (30, -40), (-30, -40)], (200, 40, 32))], z, 80, 522)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    d.text((c, c + 8 * z), "PRO", font=ImageFont.truetype(FONT, max(6, int(18 * z))), fill=WHITE, anchor="mm")
    return img


@eprop("fork")
def _fork(z):
    return render_shapes([("p", strip([(0, 60), (0, -40)], 16), (200, 200, 210)),
                          ("p", [(-30, -40), (30, -40), (30, -60), (-30, -60)], (200, 200, 210))] +
                         [("p", strip([(x, -60), (x, -130)], 9), (200, 200, 210)) for x in (-26, -9, 9, 26)],
                         z, 150, 523)


def yard_layout(L):
    vert = L["H"] > L["W"]
    K = L["K"]
    if vert:
        xs = dict(chadsr=260, brittany=480, pip=700, mb=910, dot=1120, grandma=1320, firefighter=1500)
        return dict(cast=xs, cannon=(60, L["feet"]), wide=(760, 1240, 0.68), trees=(320, 1250), tail=1850,
                    cams={"cu_cannon": (330, L["feet"] - 420 * K, 1.05)})
    xs = dict(chadsr=330, brittany=580, pip=900, mb=1140, dot=1380, grandma=1620, firefighter=1820)
    return dict(cast=xs, cannon=(140, L["feet"]), wide=(960, 600, 1.0), trees=(420, 1500), tail=2000,
                cams={"cu_cannon": (520, L["feet"] - 330 * K, 1.3)})


def yard_bg(L, cam, scene):
    W, H_, z = L["W"], L["H"], cam.z
    S = L[scene]
    K, F = L["K"], L["feet"]
    rng = np.random.default_rng(141)
    img = Image.new("RGBA", (W, H_))
    paper(img, cam.pts([(-900, -900), (2600, -900), (2600, 3000), (-900, 3000)]), (160, 210, 236), rng, z,
          shadow=False, jitter=False, edge=False)
    fy = F - 330 * K
    for k in range(-6, 30):   # wooden fence
        x = k * 90
        paper(img, cam.pts([(x, fy - 260 * K), (x + 80, fy - 270 * K), (x + 80, fy), (x, fy)]), (200, 160, 110), rng,
              z, sh=3)
    for tx in S["trees"]:
        paper(img, cam.pts([(tx - 30 * K, fy - 380 * K), (tx + 30 * K, fy - 380 * K), (tx + 36 * K, fy),
                            (tx - 36 * K, fy)]), (120, 84, 54), rng, z, sh=4)
        paper(img, cam.pts(lumpy(tx, fy - 520 * K, 200 * K, [(16, 5, tx), (10, 9, 1)])), (80, 150, 70), rng, z, sh=6)
    paper(img, cam.pts([(-900, fy), (2600, fy), (2600, 3000), (-900, 3000)]), (120, 186, 96), rng, z, shadow=False)
    bx = (S["cast"]["chadsr"] + S["cast"]["brittany"]) / 2   # banner + balloons on the fence
    paper(img, cam.pts([(bx - 300 * K, fy - 230 * K), (bx + 300 * K, fy - 240 * K), (bx + 300 * K, fy - 150 * K),
                        (bx - 300 * K, fy - 140 * K)]), WHITE, rng, z, sh=4)
    d = ImageDraw.Draw(img)
    d.text(cam.p(bx, fy - 190 * K), "BOY OR GIRL?", font=ImageFont.truetype(FONT, int(54 * z * K)),
           fill=(120, 120, 220), anchor="mm")
    for k in range(6):
        x = bx + (k - 2.5) * 110 * K
        paper(img, cam.pts(strip([(x, fy - 240 * K), (x + 10, fy - 420 * K)], 3)), (90, 90, 90), rng, z, shadow=False)
        paper(img, cam.pts(ell(x + 10, fy - 470 * K, 46 * K, 56 * K)), (120, 180, 250) if k % 2 else (250, 160, 200),
              rng, z, sh=4)
    gx = S["tail"]   # the grill
    paper(img, cam.pts([(gx - 80 * K, fy - 10 * K), (gx + 80 * K, fy - 10 * K), (gx + 60 * K, fy + 80 * K),
                        (gx - 60 * K, fy + 80 * K)]), (40, 40, 46), rng, z, sh=5)
    return C.vignette(img)


def ep6():
    seq = [
        ("gag", "intro", 2.4, "yard", "wide"),
        ("line", "mb", "My neighbors are having a baby. So naturally, they bought explosives.", None,
         dict(scene="yard", cams=[(0, "cu_mb")], gap=0.2)),
        ("line", "brittany", "This reveal is gonna go viral, babe!", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.2)),
        ("line", "chadsr", "I got two hundred pounds of blue powder and a cannon from a guy named Scooter.", None,
         dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.2)),
        ("line", "dot", "That's not a party. That's a war crime with balloons.", None,
         dict(scene="yard", cams=[(0, "cu_dot")], gap=0.2)),
        ("line", "pip", "Why can't you just say it's a boy?", None, dict(scene="yard", cams=[(0, "cu_pip")], gap=0.2)),
        ("line", "brittany", "Because then how would strangers on the internet know?", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.0)),
        ("gag", "boom", 2.2, "yard", "cu_cannon"),
        ("line", "chadsr", "It's a boy!", None, dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.1)),
        ("line", "dot", "It's a felony.", None, dict(scene="yard", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.6, "wide"),
        ("line", "firefighter", "Whose idea was the cannon?", None,
         dict(scene="yard", cams=[(0, "cu_firefighter")], gap=0.2)),
        ("line", "chadsr", "Scooter's.", None, dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.2)),
        ("line", "firefighter", "Scooter's in jail, sir. Again.", None,
         dict(scene="yard", cams=[(0, "cu_firefighter")], gap=0.0)),
        ("hold", 0.4, "cu_chadsr"),
        ("line", "brittany", "Can you film me crying? From my good side?", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.2)),
        ("line", "grandma", "In my day we found out when the baby came out. And we were happy it had a pulse.", None,
         dict(scene="yard", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.4, "cu_mb"),
        ("line", "mb", "Congratulations. Your son's first word is gonna be evacuation.", None,
         dict(scene="yard", cams=[(0, "cu_mb")], gap=0.2)),
        ("line", "pip", "What about the next baby?", None,
         dict(scene="yard", cams=[(0, "cu_pip")], gap=0.2, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ("line", "chadsr", "Bigger cannon.", None, dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.0)),
        ("hold", 0.7, "wide"),
        ("gag", "end", 3.0, "yard", "wide"),
    ]

    def where(c, t, scene, L):
        if c == "firefighter":
            ln = H.lines_with("Whose idea", "firefighter")
            if not ln or t < ln[0]["t0"] - 0.6:
                return None
        return (L[scene]["cast"][c], L["feet"])

    def pre(fr, cam, t, fi, li, scene, L):
        K = L["K"]
        cx, cy = L[scene]["cannon"]
        ev = G["ev"]
        rec = 0
        if "boom" in ev and 0 <= t - ev["boom"] < 0.25:
            rec = -40   # recoil
        paste(fr, H.prop("cannon", round(cam.z * K, 3)), *cam.p(cx + rec * K, cy - 40 * K))
        if "boom" in ev and t >= ev["boom"] + 0.3:   # the trees burn (paper flames, cartoon)
            fy = L["feet"] - 330 * K
            for k, tx in enumerate(L[scene]["trees"]):
                fire(fr, cam, tx, fy - 420 * K, 150 * K, t, 10 + k)

    def post(fr, cam, t, fi, li, scene, L):
        ev = G["ev"]
        K = L["K"]
        if "boom" not in ev:
            return
        d = t - ev["boom"]
        cx, cy = L[scene]["cannon"]
        if 0 <= d < 0.4:
            px, py = cam.p(cx + 170 * K, cy - 420 * K)
            paste(fr, C2.spr("star", round(cam.z * K * 1.6, 2), "BOOM!"), px, py, (fi % 2) * 10)
        if 0.15 <= d < 3.6:   # the blue cloud rises and drifts
            f = min(1.0, d / 1.2)
            rng = np.random.default_rng(5)
            fade = 1.0 if d < 2.6 else max(0.0, 1 - (d - 2.6))
            n = int(10 * fade) + 2
            for k in range(n):
                bx = cx + 150 * K + (k * 137 % 900) * K * f
                by = cy - 500 * K - (k * 71 % 500) * K * f
                r = (90 + (k * 53 % 90)) * K * (0.4 + f)
                paper(fr, cam.pts(lumpy(bx, by, r, [(r * 0.08, 5, k)])), (110, 170, 245), rng, cam.z, sh=4)

    def pose_hook(c, t, fi, li, scene, p):
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        ev = G["ev"]
        if c == "brittany":
            ln = H.lines_with("film me", "brittany")
            if ln and ln[0]["t0"] <= t:
                aR, extra["item"] = 140, ("phone", "R", 0)
        if c == "chadsr" and t < ev.get("boom", 1e9):
            aR = 70   # hand on the cannon fuse
        if "boom" in ev and ev["boom"] <= t < ev["boom"] + 1.0:
            hop = [-20, 0][fi % 2] if c in ("pip", "mb", "dot", "brittany", "chadsr") else hop
            if c in ("pip", "mb"):
                aL, aR = -160, 160
        if c in ("chadsr", "brittany") and t >= ev.get("boom", 1e9) + 0.2:
            hk = (hk[0], hk[1], hk[2], frozenset(set(hk[3]) | {"soot"}))
        if c == "chadsr" and H.lines_with("Bigger cannon", "chadsr"):
            ln = H.lines_with("Bigger cannon", "chadsr")[0]
            if ln["t0"] <= t:
                hk = (hk[0], hk[1], "smug", hk[3])
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def shakes():
        ev = G["ev"]
        return [(ev["boom"], 1.6)] if "boom" in ev else []

    def sfx(fx, music, ev, lines):
        if "boom" in ev:
            b = ev["boom"]
            C2.thud(fx, b, 1.0)
            add(fx, C2.noise_burst(1.6, 0.5, 44, 2), b + 0.02, 0.6)
            for k in range(6):   # siren in the distance after the blast
                add(fx, C2.tone(960, 0.36, 0.08), b + 1.0 + k * 0.72)
                add(fx, C2.tone(770, 0.36, 0.08), b + 1.36 + k * 0.72)

    return dict(title="GENDER REVEAL", end=["WORST GENDER", "REVEAL YOU'VE", "SEEN?"], seq=seq,
                scenes={"yard": dict(layout=yard_layout, bg=yard_bg)},
                where=where, pre=pre, post=post, pose_hook=pose_hook, shakes=shakes, sfx=sfx)


def kitchen_layout(L):
    vert = L["H"] > L["W"]
    if vert:
        xs = dict(sage=120, pip=390, mb=630, dot=870, tank=1150)
        return dict(cast=xs, wide=(640, 1380, 0.85))
    xs = dict(sage=320, pip=700, mb=960, dot=1220, tank=1600)
    return dict(cast=xs, wide=(960, 600, 1.0))


def kitchen_bg(L, cam, scene):
    W, H_, z = L["W"], L["H"], cam.z
    K, F = L["K"], L["feet"]
    rng = np.random.default_rng(151)
    img = Image.new("RGBA", (W, H_))
    paper(img, cam.pts([(-900, -900), (2600, -900), (2600, 3000), (-900, 3000)]), (236, 230, 206), rng, z,
          shadow=False, jitter=False, edge=False)
    wall_b = F - 260 * K
    for k in range(-8, 30):   # tile backsplash
        for r in range(4):
            x, y = k * 70 + (r % 2) * 35, wall_b - 330 * K - r * 50
            paper(img, cam.pts([(x, y), (x + 64, y), (x + 64, y + 44), (x, y + 44)]), (200, 226, 222), rng, z,
                  shadow=False, jitter=False, edge=False)
    for k in range(-3, 9):   # upper cabinets
        x = k * 260
        paper(img, cam.pts([(x, wall_b - 900 * K), (x + 240, wall_b - 900 * K), (x + 240, wall_b - 600 * K),
                            (x, wall_b - 600 * K)]), (190, 140, 96), rng, z, sh=5)
        paper(img, cam.pts(ell(x + 200, wall_b - 640 * K, 8, 8)), (60, 60, 60), rng, z, shadow=False)
    paper(img, cam.pts([(-900, wall_b - 40 * K), (2600, wall_b - 40 * K), (2600, wall_b), (-900, wall_b)]),
          (90, 90, 96), rng, z, sh=4)   # counter edge
    paper(img, cam.pts([(-900, wall_b), (2600, wall_b), (2600, 3000), (-900, 3000)]), (210, 200, 180), rng, z,
          shadow=False)
    for k in range(-8, 30):
        paper(img, cam.pts(strip([(k * 120, wall_b), (k * 120 - 200, F + 400)], 4)), (190, 180, 160), rng, z,
              shadow=False)
    fx = 1700 if W > H_ else 1350   # fridge
    paper(img, cam.pts([(fx - 160, wall_b - 820 * K), (fx + 160, wall_b - 820 * K), (fx + 160, wall_b + 40),
                        (fx - 160, wall_b + 40)]), (240, 240, 244), rng, z, sh=8)
    paper(img, cam.pts(strip([(fx - 160, wall_b - 520 * K), (fx + 160, wall_b - 520 * K)], 6)), (200, 200, 206), rng, z,
          shadow=False)
    d = ImageDraw.Draw(img)
    d.text(cam.p(fx, wall_b - 680 * K), "NO MEAT", font=ImageFont.truetype(FONT, int(30 * z * K)), fill=(80, 140, 80),
           anchor="mm")
    d.text(cam.p(fx, wall_b - 380 * K), "ONLY MEAT", font=ImageFont.truetype(FONT, int(30 * z * K)),
           fill=(200, 40, 32), anchor="mm")
    return C.vignette(img)


def ep7():
    seq = [
        ("gag", "intro", 2.4, "kitchen", "wide"),
        ("line", "mb", "Two people. One kitchen. And I'm the only one here who is literally food.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.2)),
        ("line", "sage", "I don't eat anything with a face.", None, dict(scene="kitchen", cams=[(0, "cu_sage")],
                                                                        gap=0.2)),
        ("line", "mb", "I'm a meatball. I have a face. Pick a side.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.4, "cu_sage"),
        ("line", "tank", "Bro, I eat forty eggs a day. My blood is just protein shake.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.2)),
        ("line", "dot", "Your blood is ninety percent creatine and ten percent bad decisions.", None,
         dict(scene="kitchen", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.4, "cu_tank"),
        ("line", "sage", "Did you know I'm vegan?", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.2)),
        ("line", "pip", "Yes. You told us. In the driveway. And the mailbox. And my dreams.", None,
         dict(scene="kitchen", cams=[(0, "cu_pip")], gap=0.0)),
        ("hold", 0.4, "cu_sage"),
        ("line", "tank", "I don't do cardio, bro. Cardio is for people who can't afford steroids.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.2)),
        ("line", "sage", "Your body is a temple, Tank.", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.2)),
        ("line", "tank", "My body's a warehouse store, bro. Bulk.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.2)),
        ("line", "sage", "Meat is murder.", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.2)),
        ("line", "tank", "Then I'm a serial killer, bro. Leg day is a crime scene.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.0)),
        ("hold", 0.7, "wide"),
        ("gag", "stare", 1.4, "kitchen", "cu_mb"),
        ("line", "sage", "Is Meatball meat?", "...Is Meatball meat?",
         dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.2)),
        ("line", "tank", "Only one way to find out, bro.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.0)),
        ("hold", 0.4, "cu_mb"),
        ("line", "mb", "Pip, if I die in here, you can have my shoes.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.2)),
        ("line", "pip", "Finally.", None,
         dict(scene="kitchen", cams=[(0, "cu_pip")], gap=0.0, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
        ("hold", 0.7, "wide"),
        ("gag", "end", 3.0, "kitchen", "wide"),
    ]

    def stare_win():
        ev = G["ev"]
        if "stare" not in ev:
            return (1e9, 1e9)
        end_ = H.lines_with("one way", "tank")
        return (ev["stare"] - 0.7, end_[0]["start"] + end_[0]["dur"] + 0.6 if end_ else ev["stare"] + 1.4)

    def pose_hook(c, t, fi, li, scene, p):
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        a, b = stare_win()
        if c == "sage":
            aL, extra["item"] = min(aL, -50), ("oatmilk", "L", 0)
        if c == "tank":
            aR, extra["item"] = max(aR, 60), ("shaker", "R", 0)
            ln = H.lines_with("one way", "tank")
            if ln and ln[0]["t0"] <= t:
                aR, extra["item"] = 150, ("fork", "R", 0)
        if a <= t < b and c in ("sage", "tank"):   # both turn to look at Meatball
            hk = (hk[0], hk[1], "wide" if c == "sage" else "smug", hk[3])
            ang = 6 if c == "sage" else -6
        if a <= t < b and c == "mb":
            hk = (hk[0], hk[1], hk[2], "wide")
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def post(fr, cam, t, fi, li, scene, L):
        a, b = stare_win()
        if a <= t < b:   # a sweat drop on Meatball
            K = L["K"]
            x, y = cam.p(L[scene]["cast"]["mb"] + 92 * K, L["feet"] - (370 - ((fi % 6) * 6)) * K)
            r = 14 * cam.z * K
            ImageDraw.Draw(fr).polygon([(x, y - r * 2.2), (x + r, y), (x, y + r), (x - r, y)], fill=(120, 190, 250),
                                       outline=INK)

    def sfx(fx, music, ev, lines):
        if "stare" in ev:   # a slow, dumb "dun dun"
            add(fx, ks(hz("D3"), 0.6, 0.995, 0.6, 30), ev["stare"] + 0.1, 0.5)
            add(fx, ks(hz("C#3"), 0.9, 0.995, 0.6, 31), ev["stare"] + 0.6, 0.5)

    def silences():
        ev = G["ev"]
        return [(ev["stare"], ev["stare"] + 1.4)] if "stare" in ev else []

    return dict(title="VEGAN VS GYM BRO", end=["TEAM VEGAN", "OR TEAM", "GYM BRO?"], seq=seq,
                scenes={"kitchen": dict(layout=kitchen_layout, bg=kitchen_bg)},
                pose_hook=pose_hook, post=post, sfx=sfx, silences=silences)


EPISODES = {"ep3": ep3, "ep4": ep4, "ep5": ep5, "ep6": ep6, "ep7": ep7, "ep8": ep8}


# ------------------------------------------------------------------------------------------------ engine
TARGET = 63.0   # TikTok + Shorts: a bit over a minute (Nolan 11/19: 62-66 s, never under 61)


def use(name, fmt="vertical"):
    """Load an episode; stretch its reaction holds so the cut lands on TARGET seconds."""
    EP.clear()
    EP.update(EPISODES[name]())
    EP["name"], EP["fmt"] = name, fmt
    C2.SEQ[:] = EP["seq"]
    H.place = lambda scene: (G["L"][scene].get("cast", {}) if scene in G.get("L", {}) else {})
    _, _, _, end = C2.build()
    holds = [i for i, it in enumerate(C2.SEQ) if it[0] == "hold"]
    if holds and abs(TARGET - end) > 0.2:
        per = max(-0.25, min(0.9, (TARGET - end) / len(holds)))
        for i in holds:
            it = C2.SEQ[i]
            C2.SEQ[i] = (it[0], round(max(0.25, it[1] + per), 2), it[2])
        rem = TARGET - end - per * len(holds)
        lines_ = [i for i, it in enumerate(C2.SEQ) if it[0] == "line"]
        if rem > 0.2 and lines_:   # still short: breathe a little after every line too
            g = min(0.45, rem / len(lines_))
            for i in lines_:
                it = C2.SEQ[i]
                o = dict(it[4])
                o["gap"] = round(o.get("gap", 0.15) + g, 2)
                C2.SEQ[i] = it[:4] + (o,)
            rem -= g * len(lines_)
            if rem > 0.2:   # a short script: the rest goes into the reaction holds
                for i in holds:
                    it = C2.SEQ[i]
                    C2.SEQ[i] = (it[0], round(it[1] + rem / len(holds), 2), it[2])


def bg(scene, cam_name):
    key = (scene, cam_name)
    if key not in G["bg"]:
        cx, cy, z = G["cams"][scene][cam_name]
        cam = Cam(G["L"], cx, cy, z)
        out = EP["scenes"][scene]["bg"](G["L"], cam, scene)
        G["bg"][key] = out if isinstance(out, tuple) else (out, None)
    return G["bg"][key]


def shake(t):
    for (t0, a) in EP.get("shakes", lambda: [])():
        if 0 <= t - t0 < 2 / FPS:
            return (int(22 * a), int(-14 * a)) if t - t0 < 1 / FPS else (int(-12 * a), int(8 * a))
    return (0, 0)


def frame(fi):
    L = G["L"]
    t = fi / FPS
    _, scene, cam_name = C2.seg_at(t)
    G["scene"] = scene
    cx, cy, z = G["cams"][scene][cam_name]
    sx_, sy_ = shake(t)
    cam = Cam(L, cx + sx_ / z, cy + sy_ / z, z)
    back, front = bg(scene, cam_name)
    fr = back.copy()
    if sx_ or sy_:
        fr2 = Image.new("RGBA", fr.size, (0, 0, 0, 255))
        fr2.paste(fr, (-sx_, -sy_))
        fr = fr2
    li = C2.speaking(t)
    F = L["feet"]
    if "pre" in EP:
        EP["pre"](fr, cam, t, fi, li, scene, L)
    for c, x in L[scene].get("cast", {}).items():
        where = EP["where"](c, t, scene, L) if "where" in EP else (x, F)
        if where is None:
            continue
        p = H.pose(c, t, fi, li, scene)
        if "pose_hook" in EP:
            p = EP["pose_hook"](c, t, fi, li, scene, p)
        H.draw_any(fr, cam, c, where[0] if where[0] is not None else x, where[1], p)
    if front is not None:
        fr.alpha_composite(front)
    if "post" in EP:
        EP["post"](fr, cam, t, fi, li, scene, L)
    banners(fr, t)
    C2.draw_caption(fr, t, cam_name)
    return np.asarray(fr.convert("RGB")).tobytes()


def banners(fr, t):
    L = G["L"]
    W = L["W"]
    big = 120 if L["W"] > L["H"] else 104
    by = L["banner_y"]

    def drop(t0):
        k = int((t - t0) * FPS)
        return [-700, -320, 40, -12, 0][k] if k < 5 else 0

    end = G["ev"]["end"]
    it_ = C2.GD.get("intro", 2.4)
    items = [(0.1, it_ - 0.05, "MEATBALL MYTHS", big, (200, 40, 32), WHITE, -3, 0),
             (0.6, it_ - 0.05, EP["title"], int(big * 0.62), (20, 20, 24), (252, 214, 74), 2, int(big * 1.25))]
    eb = int(big * 0.52)
    for i, txt in enumerate(EP["end"]):
        items.append((end + 0.2 + 0.25 * i, end + 99, txt, eb, (252, 250, 240), INK, [-2, 2, -1][i % 3],
                      int(i * eb * 1.55) + (40 if L["H"] > L["W"] else 0)))
    items.append((end + 0.1, end + 99, "MEATBALL MYTHS", int(big * 0.7), (200, 40, 32), WHITE, 3, -int(big * 1.1)))
    for (t0, t1, text, size, col, tcol, ang, dy) in items:
        if not (t0 <= t < t1):
            continue
        off = drop(t0)
        if t1 - t < 0.25:
            off = -int((0.25 - (t1 - t)) * 3000)
        img = C.banner_img(text, size, col, tcol, len(text))
        if img.size[0] > W * 0.98:
            s = W * 0.98 / img.size[0]
            img = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.LANCZOS)
        paste(fr, img, W / 2, by + dy + off, ang)
    if t >= end + 1.0:
        ay = by + len(EP["end"]) * eb * 1.55 + (60 if L["H"] > L["W"] else 20) + (8 if int(t * FPS) % 4 < 2 else 0)
        x = W * 0.8
        rng = np.random.default_rng(3)
        paper(fr, [(x - 30, ay), (x + 30, ay), (x + 30, ay + 60), (x + 70, ay + 60), (x, ay + 130),
                   (x - 70, ay + 60), (x - 30, ay + 60)], (252, 214, 74), rng, 1.5, sh=6)


def mix(end):
    ev, lines = G["ev"], G["lines"]
    music = np.zeros(int((end + 1) * SR), np.float32)
    mel1 = [(0, "E5", 1), (1, "G5", 0.5), (1.5, "A5", 0.5), (2, "G5", 1), (3, "E5", 0.5), (3.5, "C#5", 0.5)]
    jingle_bar(music, 0.0, ["C", "A7"], 0.32, mel1, seed=1)
    stab = 4 * BEAT
    strum(music, stab, "C", 0.4, seed=3)
    add(music, ks(hz("C6"), 1.0, 0.996, 0.85, 4), stab, 0.35)
    for t0 in (0.1, 0.6):
        sfx_slap(music, t0 + 2 / FPS, 0.25, int(t0 * 10))
    bed = np.zeros_like(music)
    prog = [["C"], ["A7"], ["D7"], ["G7"]]
    t, k = stab + BEAT, 0
    while t < ev["end"]:
        jingle_bar(bed, t, prog[k % 4], 0.32, None, drums=True, seed=10 + k)
        t += 4 * BEAT
        k += 1
    gate = np.ones_like(bed)
    gate[:int((stab + BEAT) * SR)] = 0
    for (a, b) in EP.get("silences", lambda: [])():
        gate[int(a * SR):int(b * SR)] = 0
    gate[int(ev["end"] * SR):] = 0
    gate = np.convolve(gate, np.ones(4410) / 4410, "same").astype(np.float32)
    music += bed * gate * 10 ** (-22 / 20) * 1.6
    fx = np.zeros_like(music)
    if "sfx" in EP:
        EP["sfx"](fx, music, ev, lines)
    for ln in lines:
        if ln["beep"]:
            add(fx, C2.tone(1560, 0.16, 0.3), ln["t0"] + 0.05)
    o = ev["end"] + 0.1
    strum(music, o, "G7", 0.35, seed=40)
    for k2, nt in enumerate(["B5", "D6", "G5", "E5"]):
        add(music, ks(hz(nt), 0.6, 0.995, 0.85, 50 + k2), o + 0.18 + k2 * BEAT / 2, 0.32)
    strum(music, o + 2.5 * BEAT, "C", 0.45, seed=60)
    add(music, ks(hz("C6"), 1.2, 0.996, 0.85, 62), o + 2.5 * BEAT, 0.35)
    kick(music, o + 2.5 * BEAT, 0.3)
    vo = np.zeros_like(music)
    for ln in lines:
        add(vo, ln["audio"], ln["start"], 1.0)
    out = vo + music + fx * 0.8
    out *= 0.97 / max(1e-6, float(np.max(np.abs(out))))
    return out[:int(end * SR)]


def setup(name, fmt):
    use(name, fmt)
    L = build_layout()
    G["L"] = L
    lines, segs, ev, end = C2.build()
    G.update(L=L, lines=lines, segs=segs, ev=ev, end=end, cams=cams(L), bg={})
    for (_, scene, cam) in segs:
        bg(scene, cam)


def render(name, fmt, out):
    os.makedirs(TMP, exist_ok=True)
    setup(name, fmt)
    L, end = G["L"], G["end"]
    wav = f"{TMP}/{name}-mix-{fmt}.wav"
    import soundfile as sf
    sf.write(wav, mix(end), SR)
    n = int(math.ceil(end * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{L['W']}x{L['H']}",
           "-framerate", str(FPS), "-i", "-", "-i", wav, "-vf", f"fps={OUT_FPS}", "-c:v", "libx264", "-preset",
           "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for b in pool.imap(frame, range(n), chunksize=4):
            ff.stdin.write(b)
    ff.stdin.close()
    ff.wait()
    print(out, f"{end:.2f}s", n, "frames")


def stills(name, fmt, times):
    setup(name, fmt)
    W, H_ = G["L"]["W"], G["L"]["H"]
    outs = []
    for t in times:
        p = f"{TMP}/{name}-{fmt}-{t:.2f}.png"
        Image.frombytes("RGB", (W, H_), frame(int(t * FPS))).save(p)
        outs.append(p)
    print(" ".join(outs))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--fmt", default="vertical", choices=["vertical", "wide"])
    ap.add_argument("--out")
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--timeline", action="store_true")
    a = ap.parse_args()
    if a.timeline:
        use(a.ep, a.fmt)
        lines, segs, ev, end = C2.build()
        for i, ln in enumerate(lines):
            print(f"{i + 1:2d} {ln['who']:12s} {ln['t0']:7.2f} {ln['dur']:5.2f} "
                  f"{' '.join(w[2] for w in ln['words'])[:60]}")
        print({k: round(v, 1) for k, v in ev.items()}, round(end, 2))
    elif a.still:
        stills(a.ep, a.fmt, a.still)
    else:
        render(a.ep, a.fmt, a.out)
