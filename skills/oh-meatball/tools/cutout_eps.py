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
        for k in ("kaylee", "pip", "mb", "dot", "brad"):
            full.setdefault(k, xs.get(k, 0))
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


EPISODES = {"ep3": ep3}


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
