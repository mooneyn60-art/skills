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
        if top == "cassock":   # long black robe, white collar tab
            s += [("p", [(-bw, -70), (bw, -70), (bw + 6, -14), (-bw - 6, -14)], top_col),
                  ("p", [(-13, nk + 2), (13, nk + 2), (13, nk + 18), (-13, nk + 18)], WHITE, False)]
        if top == "labcoat":   # white coat, blue scrubs showing, stethoscope
            s += [("p", [(-20, nk), (20, nk), (0, nk + 80)], (120, 180, 210), False),
                  ("pts", strip([(-26, nk + 6), (-30, nk + 70), (0, nk + 96), (30, nk + 70), (26, nk + 6)], 5),
                   (50, 50, 56), False),
                  ("e", (0, nk + 100, 10, 10), (190, 190, 200), False)]
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
register("father", person(SKIN[3], "short", (190, 190, 196), "cassock", (30, 30, 36), (30, 30, 36), (20, 20, 22),
                          acc=("glasses",), eyes=("norm", 0.45)))
register("doctor", person(SKIN[4], "short", (40, 30, 26), "labcoat", (246, 246, 250), (120, 180, 210), (240, 240, 240),
                          acc=("glasses",), eyes=("norm", 0.2)))
register("bezos", person(SKIN[0], "bald", (60, 40, 30), "polo", (40, 50, 80), (50, 50, 60), (30, 30, 30),
                         eyes=("norm", 0.15)))
register("trump", person((244, 176, 120), "slick", (246, 208, 96), "shirt_tie", (30, 40, 80), (30, 40, 80),
                         (20, 20, 22), tall=1.04, wide=1.18, eyes=("norm", 0.3)))
register("xi", person(SKIN[5], "short", (24, 22, 24), "shirt_tie", (40, 40, 48), (40, 40, 48), (20, 20, 22),
                      wide=1.12, eyes=("norm", 0.35)))
register("putin", person(SKIN[3], "buzz", (200, 190, 170), "shirt_tie", (50, 54, 60), (50, 54, 60), (20, 20, 22),
                         tall=0.94, eyes=("norm", 0.5)))
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
    "sage": "kokoro:sage@speed=1.0,pause=0.3", "tank": "kokoro:tank@speed=1.2,pause=0.18",
    "bezos": "kokoro:bezos@speed=1.1,pause=0.2", "trump": "kokoro:trump@speed=1.05,pause=0.22",
    "xi": "kokoro:xi@speed=1.05,pause=0.22", "putin": "kokoro:putin@speed=0.98,pause=0.25",
    "father": "kokoro:father@speed=1.08,pause=0.22", "doctor": "kokoro:doctor@speed=1.1,pause=0.2"})


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
    hs = {"grandma": 150, "rick": 300, "dadbot": 380, "tank": 300, "chadsr": 300, "firefighter": 300,
          "father": 300, "doctor": 300, "bezos": 300, "trump": 300, "xi": 300, "putin": 300}
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
    seq = [   # v2 (Nolan 11/19: too much dead air): extra lines, gaps 0.1, holds 0.3
        ("gag", "intro", 2.2, "table", "wide"),
        ("line", "mb", "Thanksgiving. The one day a year your family remembers why they moved away.", None, dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.3, "wide"),
        ("line", "rick", "Pass the potatoes. And don't pass any socialism.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.45, "cu_kaylee"),
        ("line", "kaylee", "Potatoes are, like, colonialism, Rick.", None, dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.0)),
        ("hold", 0.45, "cu_dot"),
        ("line", "dot", "They're potatoes, Kaylee. They don't have a party.", None, dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.45, "cu_rick"),
        ("line", "rick", "Everything's a party to you people.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "kaylee", "You people? I'm your niece, Rick.", None, dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.0)),
        ("hold", 0.3, "cu_rick"),
        ("line", "rick", "I'm not homophobic, I just don't get it.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.45, "cu_mb"),
        ("line", "mb", "Nobody gets you either, Rick, and we still let you come to Thanksgiving.", None, dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.45, "cu_rick"),
        ("line", "kaylee", "I don't vote. I just post about it. Every. Single. Day.", None, dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.0)),
        ("hold", 0.45, "cu_brad"),
        ("line", "brad", "I don't vote either, bro. I'm a free market.", None, dict(scene="table", cams=[(0, "cu_brad")], gap=0.0)),
        ("hold", 0.45, "cu_grandma"),
        ("line", "grandma", "Bradley, you're unemployed.", None, dict(scene="table", cams=[(0, "cu_grandma")], gap=0.1)),
        ("line", "brad", "I'm between disruptions, Grandma.", None, dict(scene="table", cams=[(0, "cu_brad")], gap=0.0)),
        ("hold", 0.3, "cu_dot"),
        ("line", "rick", "The government is spying on me through my microwave.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "dot", "Rick, nobody's spying on you. Your microwave has seen enough.", None, dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.45, "cu_rick"),
        ("line", "kaylee", "And crystals cure stress, cancer and taxes.", None, dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.0)),
        ("hold", 0.45, "cu_mb"),
        ("line", "mb", "Rick thinks the government's spying on him. Kaylee thinks crystals cure cancer. And they carpooled here.", None, dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.3, "wide"),
        ("line", "grandma", "I've lived through eleven presidents. You're all wrong, and the turkey's dry.", None, dict(scene="table", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.45, "cu_rick"),
        ("line", "rick", "I do my own research.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "dot", "You read half a meme, Rick. On the toilet.", None, dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "cu_rick"),
        ("line", "pip", "Can we just say what we're thankful for?", None, dict(scene="table", cams=[(0, "cu_pip")], gap=0.12)),
        ("line", "rick+kaylee", "That I'm right.", None, dict(scene="table", cams=[(0, "wide_all")], gap=0.0)),
        ("hold", 0.3, "wide_all"),
        ("gag", "fire", 0.9, "table", "wide"),
        ("line", "dot", "And that's how the turkey caught fire.", None, dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "wide"),
        ("gag", "end", 3.0, "table", "wide"),
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
    seq = [   # v2 (Nolan 11/19: too much dead air): extra lines, gaps 0.1, holds 0.3
        ("gag", "intro", 2.2, "street", "wide"),
        ("line", "mb", "Every neighborhood has one. Ours has a clipboard.", None,
         dict(scene="street", cams=[(0, "cu_mb"), (4, "cu_karen")], gap=0.12)),
        ("line", "karen", "Excuse me. Your lemonade stand is in violation of section forty-two.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.1)),
        ("line", "pip", "It's lemonade. It's a dollar.", None, dict(scene="street", cams=[(0, "cu_pip")], gap=0.1)),
        ("line", "karen", "Is it organic? Gluten free? Did the lemons consent?", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.0)),
        ("hold", 0.45, "cu_dot"),
        ("line", "dot", "The lemons are fine, Karen. Are you?", None, dict(scene="street", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.45, "cu_karen"),
        ("line", "karen", "Do you have a permit? A health inspection? A vendor license? A soul?", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.1)),
        ("line", "dot", "Do you have a husband? Because he left.", None,
         dict(scene="street", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "cu_karen"),
        ("line", "karen", "Gary is on a business trip!", None, dict(scene="street", cams=[(0, "cu_karen")], gap=0.1)),
        ("line", "mb", "For six years, Karen. Gary lives in Arizona with a woman named Destiny.", None,
         dict(scene="street", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.45, "cu_karen"),
        ("line", "karen", "I'd like to speak to your manager.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.1)),
        ("line", "mb", "We're nine.", None, dict(scene="street", cams=[(0, "cu_mb")], gap=0.0,
                                                voice="kokoro:adam-puck@speed=1.15")),
        ("hold", 0.3, "cu_karen"),
        ("line", "karen", "Then I'd like to speak to your parents' manager.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.12)),
        ("line", "karen", "I pay four hundred dollars a month in HOA fees!", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.0)),
        ("hold", 0.45, "cu_pip"),
        ("line", "pip", "For what?", None,
         dict(scene="street", cams=[(0, "cu_pip")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ("line", "karen", "For the right to ruin your day.", None,
         dict(scene="street", cams=[(0, "cu_karen")], gap=0.0)),
        ("gag", "checkout", 0.3, "checkout", "wide"),
        ("line", "kiosk", "Unexpected. Item. In the bagging area.", None,
         dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.1, beep=0.3)),
        ("line", "karen", "I'd like to speak to the manager.", None,
         dict(scene="checkout", cams=[(0, "cu_karen")], gap=0.1)),
        ("line", "kiosk", "I. Am. The manager.", None, dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.0)),
        ("hold", 0.3, "cu_karen"),
        ("line", "karen", "Then I'd like to speak to your manager.", "Then I'd like to speak to YOUR manager.",
         dict(scene="checkout", cams=[(0, "cu_karen")], gap=0.1)),
        ("line", "kiosk", "He is on. His third yacht.", None, dict(scene="checkout", cams=[(0, "cu_kiosk")],
                                                                    gap=0.0)),
        ("hold", 0.45, "cu_karen"),
        ("line", "karen", "This is the worst day of my life!", None,
         dict(scene="checkout", cams=[(0, "wide")], gap=0.1)),
        ("line", "grandma", "Sweetie, I've returned a fruitcake without a receipt. Sit down.", None,
         dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.45, "cu_karen"),
        ("line", "karen", "I'm calling the police!", None, dict(scene="checkout", cams=[(0, "cu_karen")], gap=0.0)),
        ("gag", "back", 0.4, "street", "wide"),
        ("line", "dot", "They blocked your number, Karen. So did Gary.", None,
         dict(scene="street", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.45, "wide"),
        ("line", "dot", "Lemonade's two dollars now. Karen tax.", None,
         dict(scene="street", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.8, "street", "wide"),
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
            # at checkout Grandma stands to Karen's left: the clipboard goes in the other hand so it never covers her
            extra["item"] = ("clipboard", "R" if scene == "checkout" else "L", 0)
            aL = min(aL, -40) if aL > -40 else aL
            if scene == "checkout":
                aL = 12   # arm down: never across Grandma's face
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

    return dict(title="HOA KAREN", end=["WHAT'S THE PETTIEST", "HOA RULE", "YOU'VE SEEN?"], seq=seq,
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
    seq = [   # v2 (Nolan 11/19: too much dead air): extra lines, gaps 0.1, holds 0.3
        ("gag", "intro", 2.2, "table", "wide"),
        ("line", "mb", "Uncle Rick took a DNA test. Rick has opinions about DNA.", None,
         dict(scene="table", cams=[(0, "cu_mb")], gap=0.12)),
        ("line", "rick", "I'm one hundred percent American. Pure. Like a bald eagle eating a cheeseburger.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "dot", "Eagles don't eat cheeseburgers, Rick.", None, dict(scene="table", cams=[(0, "cu_dot")],
                                                                             gap=0.1)),
        ("line", "rick", "Mine do.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.45, "cu_dot"),
        ("line", "rick", "My family came over on the Mayflower.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "grandma", "Your family came over on a Greyhound bus, Richard. From Tampa.", None,
         dict(scene="table", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.45, "cu_rick"),
        ("gag", "dna", 1.2, "dna", "wide"),
        ("line", "pip", "Rick, you're thirty percent Mexican.", None,
         dict(scene="table", cams=[(0, "cu_pip"), (2, "chart/wide")], gap=0.1,
              voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
        ("line", "rick", "That's a lie spread by the envelope!", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.12)),
        ("line", "mb", "You built a wall in your backyard, Rick. You walled off your own cousins.", None,
         dict(scene="table", cams=[(0, "cu_mb"), (3, "wall/wide"), (8, "table/cu_mb")], gap=0.1)),
        ("line", "rick", "That wall is for the raccoons!", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "dot", "The raccoons have a ladder, Rick. They're smarter than you.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "cu_rick"),
        ("line", "pip", "Twenty percent Nigerian.", None, dict(scene="chart", cams=[(0, "wide")], gap=0.0)),
        ("hold", 0.45, "table/cu_rick"),
        ("line", "rick", "That explains why I can't dance. Wait, no it doesn't.",
         "...That explains why I can't dance. Wait, no it doesn't.",
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "dot", "It explains nothing, Rick. You can't dance because you're Rick.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.12)),
        ("line", "pip", "And fifteen percent Irish.", None, dict(scene="chart", cams=[(0, "wide")], gap=0.1)),
        ("line", "rick", "Finally. Something I can be proud of.", None,
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.1)),
        ("line", "pip", "And two percent... it just says see a doctor.", None,
         dict(scene="table", cams=[(0, "cu_pip")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
        ("line", "rick", "That's the cheeseburgers.", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.3, "cu_grandma"),
        ("line", "grandma", "Richard. Your grandfather was a Mexican Irishman who sold fireworks out of a church van.",
         None, dict(scene="table", cams=[(0, "cu_grandma")], gap=0.1)),
        ("line", "rick", "So what am I?", None, dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.45, "wide"),
        ("line", "mb", "Rick, you're everything you ever complained about. Happy Thanksgiving.", None,
         dict(scene="table", cams=[(0, "cu_mb")], gap=0.0)),
        ("gag", "hats", 0.8, "table", "cu_rick"),
        ("line", "rick", "I contain multitudes.", "...I contain multitudes.",
         dict(scene="table", cams=[(0, "cu_rick")], gap=0.0)),
        ("hold", 0.3, "cu_dot"),
        ("line", "dot", "Take those off, Rick. Heritage isn't a hat.", None,
         dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "wide"),
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
    seq = [   # v2 (Nolan 11/19: too much dead air): extra lines, gaps 0.1, holds 0.3
        ("gag", "intro", 2.2, "home", "wide"),
        ("line", "mb", "My dad got replaced by AI. At work. And then at home.", None, dict(scene="home", cams=[(0, "cu_mb")], gap=0.0)),
        ("gag", "ceo_in", 0.5, "ceo", "wide"),
        ("line", "dad", "Twenty years at MegaMart, and they replaced me with a chatbot named Gary.", None, dict(scene="ceo", cams=[(0, "cu_dad")], gap=0.1)),
        ("line", "ceo", "Gary doesn't need lunch, health insurance, or a soul. Gary is the future.", None, dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.1)),
        ("line", "dad", "Gary told a customer to put glue on pizza.", None, dict(scene="ceo", cams=[(0, "cu_dad"), (6, "glue/wide")], gap=0.1)),
        ("line", "ceo", "And sales went up four percent.", None, dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.1)),
        ("line", "dad", "A man ate glue, sir.", None, dict(scene="ceo", cams=[(0, "cu_dad")], gap=0.1)),
        ("line", "ceo", "And he came back for seconds. That's loyalty.", None, dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
        ("hold", 0.3, "cu_dad"),
        ("gag", "home_in", 0.5, "home", "wide"),
        ("line", "dadbot", "Hello son. I have analyzed your report card.", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.1)),
        ("line", "dadbot", "I am not angry. I am disappointed at a level no human father can reach.", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.3, "cu_mb"),
        ("line", "mb", "Holy shit. That's way worse.", None, dict(scene="home", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.45, "cu_pip"),
        ("line", "pip", "My dad never even read my report card.", None, dict(scene="home", cams=[(0, "cu_pip")], gap=0.1)),
        ("line", "dot", "My dad never read anything. He thinks books are long tweets.", None, dict(scene="home", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "cu_pip"),
        ("line", "dadbot", "I have also read your diary. Chapter three was weak.", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.1)),
        ("line", "mb", "I don't have a diary!", None, dict(scene="home", cams=[(0, "cu_mb")], gap=0.1)),
        ("line", "dadbot", "You do now. I wrote it. You are welcome.", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.3, "cu_mb"),
        ("line", "dadbot", "I have also scheduled your future. Plumber. Robots cannot do plumbing. Yet.", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.12)),
        ("line", "dad", "What do I do now?", None, dict(scene="home", cams=[(0, "cu_dad")], gap=0.1)),
        ("line", "dadbot", "Have you tried learning to code?", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.3, "cu_dad"),
        ("line", "dad", "I coded you, Gary.", "I CODED YOU, GARY.", dict(scene="home", cams=[(0, "cu_dad")], gap=0.1)),
        ("line", "dadbot", "And I have replaced you. Merry Christmas.", None, dict(scene="home", cams=[(0, "cu_dadbot")], gap=0.0)),
        ("hold", 0.3, "cu_mb"),
        ("line", "mb", "So, same time next year, Dad? If you still exist?", None, dict(scene="home", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.3, "wide"),
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
    seq = [   # v2 (Nolan 11/19: too much dead air): extra lines, gaps 0.1, holds 0.3
        ("gag", "intro", 2.2, "yard", "wide"),
        ("line", "mb", "My neighbors are having a baby. So naturally, they bought explosives.", None,
         dict(scene="yard", cams=[(0, "cu_mb")], gap=0.12)),
        ("line", "brittany", "This reveal is gonna go viral, babe!", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.1)),
        ("line", "chadsr", "I got two hundred pounds of blue powder and a cannon from a guy named Scooter.", None,
         dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.1)),
        ("line", "pip", "Is Scooter a professional?", None,
         dict(scene="yard", cams=[(0, "cu_pip")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ("line", "chadsr", "He's got nine fingers and a dream.", None,
         dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.0)),
        ("hold", 0.45, "cu_pip"),
        ("line", "dot", "That's not a party. That's a war crime with balloons.", None,
         dict(scene="yard", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.45, "cu_chadsr"),
        ("line", "pip", "Why can't you just say it's a boy?", None, dict(scene="yard", cams=[(0, "cu_pip")], gap=0.1)),
        ("line", "brittany", "Because then how would strangers on the internet know?", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.1)),
        ("line", "brittany", "We already named him. Braxtyn. With a Y. And a second Y nobody asked for.", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.1)),
        ("line", "dot", "That kid's getting bullied by his own birth certificate.", None,
         dict(scene="yard", cams=[(0, "cu_dot")], gap=0.0)),
        ("gag", "boom", 1.8, "yard", "cu_cannon"),
        ("line", "chadsr", "It's a boy!", None, dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.1)),
        ("line", "dot", "It's a felony.", None, dict(scene="yard", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.45, "cu_brittany"),
        ("line", "brittany", "Did we get the shot?", None, dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.1)),
        ("line", "mb", "You got the shot, the fire department, and the evening news.", None,
         dict(scene="yard", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.45, "cu_chadsr"),
        ("line", "firefighter", "Whose idea was the cannon?", None,
         dict(scene="yard", cams=[(0, "cu_firefighter")], gap=0.1)),
        ("line", "chadsr", "Scooter's.", None, dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.1)),
        ("line", "firefighter", "Scooter's in jail, sir. Again.", None,
         dict(scene="yard", cams=[(0, "cu_firefighter")], gap=0.0)),
        ("hold", 0.3, "cu_chadsr"),
        ("line", "brittany", "Can you film me crying? From my good side?", None,
         dict(scene="yard", cams=[(0, "cu_brittany")], gap=0.12)),
        ("line", "grandma", "In my day we found out when the baby came out. And we were happy it had a pulse.", None,
         dict(scene="yard", cams=[(0, "cu_grandma")], gap=0.0)),
        ("hold", 0.45, "cu_chadsr"),
        ("line", "chadsr", "Worth it. Do you know how many likes this got?", None,
         dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.1)),
        ("line", "firefighter", "Eleven, sir. And one is from your insurance company.", None,
         dict(scene="yard", cams=[(0, "cu_firefighter")], gap=0.0)),
        ("hold", 0.3, "cu_mb"),
        ("line", "mb", "Congratulations. Your son's first word is gonna be evacuation.", None,
         dict(scene="yard", cams=[(0, "cu_mb")], gap=0.12)),
        ("line", "pip", "What about the next baby?", None,
         dict(scene="yard", cams=[(0, "cu_pip")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ("line", "chadsr", "Bigger cannon.", None, dict(scene="yard", cams=[(0, "cu_chadsr")], gap=0.0)),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.8, "yard", "wide"),
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
    seq = [   # v2 (Nolan 11/19: too much dead air): extra lines, gaps 0.1, holds 0.3
        ("gag", "intro", 2.2, "kitchen", "wide"),
        ("line", "mb", "Two people. One kitchen. And I'm the only one here who is literally food.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.12)),
        ("line", "sage", "I don't eat anything with a face.", None, dict(scene="kitchen", cams=[(0, "cu_sage")],
                                                                        gap=0.1)),
        ("line", "mb", "I'm a meatball. I have a face. Pick a side.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.12)),
        ("line", "sage", "I also don't own a TV. Or a couch. Or joy.", None,
         dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "dot", "We can tell.", None, dict(scene="kitchen", cams=[(0, "cu_dot")], gap=0.0)),
        ("hold", 0.3, "cu_sage"),
        ("line", "tank", "Bro, I eat forty eggs a day. My blood is just protein shake.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.1)),
        ("line", "dot", "Your blood is ninety percent creatine and ten percent bad decisions.", None,
         dict(scene="kitchen", cams=[(0, "cu_dot")], gap=0.12)),
        ("line", "tank", "I can't put my arms down, bro. Haven't since March.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.1)),
        ("line", "pip", "How do you wipe?", None,
         dict(scene="kitchen", cams=[(0, "cu_pip")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ("line", "tank", "Teamwork, bro.", None, dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.0)),
        ("hold", 0.3, "cu_pip"),
        ("line", "sage", "Did you know I'm vegan?", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "pip", "Yes. You told us. In the driveway. And the mailbox. And my dreams.", None,
         dict(scene="kitchen", cams=[(0, "cu_pip")], gap=0.12)),
        ("line", "tank", "I don't do cardio, bro. Cardio is for people who can't afford steroids.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.1)),
        ("line", "sage", "Your body is a temple, Tank.", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "tank", "My body's a warehouse store, bro. Bulk.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.12)),
        ("line", "sage", "I make my own deodorant.", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "mb", "We know, Sage. The whole street knows.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.0)),
        ("hold", 0.3, "cu_sage"),
        ("line", "sage", "Meat is murder.", None, dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "tank", "Then I'm a serial killer, bro. Leg day is a crime scene.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.12)),
        ("line", "sage", "I haven't had protein since two thousand nineteen.", None,
         dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "tank", "I haven't had a feeling since two thousand nineteen.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.0)),
        ("gag", "stare", 1.0, "kitchen", "cu_mb"),
        ("line", "sage", "Is Meatball meat?", "...Is Meatball meat?",
         dict(scene="kitchen", cams=[(0, "cu_sage")], gap=0.1)),
        ("line", "tank", "Only one way to find out, bro.", None,
         dict(scene="kitchen", cams=[(0, "cu_tank")], gap=0.0)),
        ("hold", 0.3, "cu_mb"),
        ("line", "mb", "Pip, if I die in here, you can have my shoes.", None,
         dict(scene="kitchen", cams=[(0, "cu_mb")], gap=0.1)),
        ("line", "pip", "Finally.", None,
         dict(scene="kitchen", cams=[(0, "cu_pip")], gap=0.0, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.8, "kitchen", "wide"),
    ]

    def stare_win():
        ev = G["ev"]
        if "stare" not in ev:
            return (1e9, 1e9)
        end_ = H.lines_with("one way", "tank")
        return (ev["stare"] - 0.3, end_[0]["start"] + end_[0]["dur"] + 0.4 if end_ else ev["stare"] + 1.0)

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
        return [(ev["stare"], ev["stare"] + 1.0)] if "stare" in ev else []

    return dict(title="VEGAN VS GYM BRO", end=["TEAM VEGAN", "OR TEAM", "GYM BRO?"], seq=seq,
                scenes={"kitchen": dict(layout=kitchen_layout, bg=kitchen_bg)},
                pose_hook=pose_hook, post=post, sfx=sfx, silences=silences)

def ep7v3():
    """Punch-up (Studio 2d6f861): suffering contest set piece, the vegan bites Meatball."""
    K_ = dict(scene="kitchen")

    def ln(who, text, cam, gap=0.1, cap=None, **kw):
        return ("line", who, text, cap, dict(K_, cams=[(0, cam)], gap=gap, **kw))

    seq = [
        ("gag", "intro", 2.2, "kitchen", "wide"),
        ln("mb", "Two roommates. One fridge. And I'm the only one here who is literally food.", "cu_mb", 0.12),
        ln("sage", "I don't eat anything with a face.", "cu_sage"),
        ln("mb", "I have a face, Sage. Stop looking at it.", "cu_mb", 0.12),
        ln("tank", "Bro, I eat forty eggs a day. My doctor called my blood, a gravy.", "cu_tank",
           cap='Bro, I eat forty eggs a day. My doctor called my blood "a gravy."'),
        ln("dot", "Your heart is working overtime for a guy who can't spell overtime.", "cu_dot", 0.12),
        ln("sage", "Did I mention I'm vegan?", "cu_sage"),
        ln("pip", "At my grandpa's funeral, Sage. During the eulogy.", "cu_pip", 0.1,
           voice="kokoro:aud-pip-b@speed=1.25,pause=0.14"),
        ln("sage", "He'd still be here if he'd tried lentils.", "cu_sage", 0.0),
        ("hold", 0.3, "cu_pip"),
        ln("tank", "I can't put my arms down, bro. Haven't since March.", "cu_tank"),
        ln("pip", "How do you wipe?", "cu_pip", 0.1, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14"),
        ln("tank", "My mom comes Tuesdays.", "cu_tank", 0.0),
        ("hold", 0.3, "cu_pip"),
        ln("sage", "I make my own deodorant.", "cu_sage"),
        ln("mb", "We know, Sage. The birds left.", "cu_mb", 0.12),
        ln("sage", "I haven't had protein since twenty nineteen. I fainted at my own wedding.", "cu_sage"),
        ln("tank", "I haven't had a feeling since twenty nineteen. I flexed at my dad's funeral.", "cu_tank"),
        ln("sage", "I buried my cat in the compost. She's tomatoes now.", "cu_sage"),
        ln("tank", "My left pec has its own heartbeat, bro. Doctor says that's the bad one.", "cu_tank", 0.12),
        ln("dot", "Damn. You two are one salad and one push-up away from a coroner.", "cu_dot", 0.0,
           cap="D#@n. You two are one salad and one push-up away from a coroner."),
        ("gag", "stare", 1.0, "kitchen", "cu_mb"),
        ln("sage", "Nine years, Tank. I dream about ham.", "cu_sage"),
        ln("tank", "Bro, I've never eaten a vegetable. I'm scared.", "cu_tank", 0.0),
        ("hold", 0.3, "cu_mb"),
        ln("mb", "Pip, if I die in here, you get my shoes.", "cu_mb"),
        ln("pip", "I'm already wearing them.", "cu_pip", 0.0, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14"),
        ("gag", "chomp", 0.9, "kitchen", "cu_mb"),
        ln("mb", "She bit me! The vegan bit me!", "cu_mb", 0.1, cap="She BIT me! The vegan bit me!"),
        ln("tank", "How's he taste?", "cu_tank"),
        ln("sage", "Like nine years of lies.", "cu_sage", 0.0),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.5, "kitchen", "wide"),
    ]
    DARK = 0.5   # the lights are off for this long at the start of the chomp gag

    def stare_win():
        ev = G["ev"]
        if "stare" not in ev:
            return (1e9, 1e9)
        end_ = H.lines_with("scared", "tank")
        return (ev["stare"] - 0.3, end_[0]["start"] + end_[0]["dur"] + 0.4 if end_ else ev["stare"] + 1.0)

    def bitten(t):
        return "chomp" in G["ev"] and t >= G["ev"]["chomp"] + DARK

    def pose_hook(c, t, fi, li, scene, p):
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        a, b = stare_win()
        if c == "sage":
            aL, extra["item"] = min(aL, -50), ("oatmilk", "L", 0)
        if c == "tank":
            aR, extra["item"] = max(aR, 60), ("shaker", "R", 0)
            if a <= t:
                aR, extra["item"] = 150, ("fork", "R", 0)
        if a <= t < b and c in ("sage", "tank"):   # both turn to look at Meatball
            hk = (hk[0], hk[1], "wide" if c == "sage" else "smug", hk[3])
            ang = 6 if c == "sage" else -6
        if (a <= t < b or bitten(t)) and c == "mb":
            hk = (hk[0], hk[1], hk[2], "wide")
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def post(fr, cam, t, fi, li, scene, L):
        a, b = stare_win()
        K = L["K"]
        d = ImageDraw.Draw(fr)
        cast = L[scene]["cast"]
        if a <= t < b:   # a sweat drop on Meatball
            x, y = cam.p(cast["mb"] + 92 * K, L["feet"] - (370 - ((fi % 6) * 6)) * K)
            r = 14 * cam.z * K
            d.polygon([(x, y - r * 2.2), (x + r, y), (x, y + r), (x - r, y)], fill=(120, 190, 250), outline=INK)
        if bitten(t):
            z = cam.z * K
            # a bite out of Meatball's side: three scallops, sauce inside
            bx, by = cam.p(cast["mb"] + MB_BITE[0] * K, L["feet"] - MB_BITE[1] * K)
            for k, (dx, dy, r) in enumerate([(0, -26, 26), (12, 0, 29), (0, 28, 26)]):
                d.ellipse([bx + (dx - r) * z, by + (dy - r) * z, bx + (dx + r) * z, by + (dy + r) * z],
                          fill=(150, 30, 24), outline=INK, width=max(2, int(5 * z)))
            for k, (dx, dy) in enumerate([(-30, 70), (-10, 96), (-44, 108)]):   # sauce drips
                r = (10 - 2 * k) * z
                d.ellipse([bx + dx * z - r, by + dy * z - r, bx + dx * z + r, by + dy * z + r * 1.5],
                          fill=(200, 40, 32), outline=INK, width=max(1, int(3 * z)))
            # sauce around Sage's mouth
            sx, sy = cam.p(cast["sage"] + SAGE_MOUTH[0] * K, L["feet"] - SAGE_MOUTH[1] * K)
            for (dx, dy, r) in [(-26, 0, 16), (22, 6, 14), (0, 22, 13), (-8, -14, 9), (34, -10, 8)]:
                d.ellipse([sx + (dx - r) * z, sy + (dy - r) * z, sx + (dx + r) * z, sy + (dy + r) * z],
                          fill=(200, 40, 32), outline=INK, width=max(1, int(3 * z)))
        if "chomp" in G["ev"] and G["ev"]["chomp"] <= t < G["ev"]["chomp"] + DARK:   # lights off
            fr.paste((8, 8, 14, 255), [0, 0, fr.size[0], fr.size[1]])
            x0, y0 = cam.p(cast["mb"], L["feet"] - 330 * K)
            for dx in (-26, 26):   # Meatball's eyes in the dark
                r = 15 * cam.z * K
                d.ellipse([x0 + dx * cam.z * K - r, y0 - r, x0 + dx * cam.z * K + r, y0 + r], fill=WHITE)
                d.ellipse([x0 + dx * cam.z * K - r * .4, y0 - r * .4, x0 + dx * cam.z * K + r * .4, y0 + r * .4],
                          fill=INK)

    def sfx(fx, music, ev, lines):
        if "stare" in ev:   # a slow, dumb "dun dun", then a stomach growl
            add(fx, ks(hz("D3"), 0.6, 0.995, 0.6, 30), ev["stare"] + 0.1, 0.5)
            add(fx, ks(hz("C#3"), 0.9, 0.995, 0.6, 31), ev["stare"] + 0.6, 0.5)
        if "chomp" in ev:
            t0 = ev["chomp"]
            add(fx, C2.tone(90, 0.05, 0.5), t0 + 0.02)            # light switch click
            rng = np.random.default_rng(7)
            n = int(0.16 * SR)
            crunch = (rng.standard_normal(n) * np.exp(-np.linspace(0, 9, n))).astype(np.float32)
            add(fx, crunch, t0 + 0.22, 0.9)                       # CHOMP
            add(fx, ks(hz("G2"), 0.3, 0.99, 0.5, 33), t0 + 0.22, 0.6)
            add(fx, C2.tone(90, 0.05, 0.5), t0 + DARK)            # lights back on

    def silences():
        ev = G["ev"]
        out = [(ev["stare"], ev["stare"] + 1.0)] if "stare" in ev else []
        if "chomp" in ev:
            out.append((ev["chomp"], ev["chomp"] + 0.9))
        return out

    return dict(title="VEGAN VS GYM BRO", end=["TEAM VEGAN", "OR TEAM", "GYM BRO?"], seq=seq,
                scenes={"kitchen": dict(layout=kitchen_layout, bg=kitchen_bg)},
                pose_hook=pose_hook, post=post, sfx=sfx, silences=silences)


MB_BITE = (-100, 250)     # where the bite sits on Meatball (x from his centre, y above the feet), layout units
SAGE_MOUTH = (0, 276)    # Sage's mouth

def lively(c, t, li, p, xs, amp=1.0):
    """More movement (Nolan 11/19 "more animation"): the speaker waves and bounces, everyone else leans in."""
    hop, j, ang, (aL, aR), hk, sq, rot, extra = p
    lines = G.get("lines", [])
    if li is None or li >= len(lines):
        return p
    who = lines[li]["who"]
    ph = t * 9.0
    if c in who.split("+"):
        aL = aL - (22 + 26 * abs(math.sin(ph))) * amp
        aR = aR + (22 + 26 * abs(math.sin(ph + 1.3))) * amp
        ang = ang + 3.5 * math.sin(ph * 0.5) * amp
        hop = hop + 7 * abs(math.sin(ph * 0.5)) * amp
    else:
        sp = who.split("+")[0]
        if sp in xs and c in xs:
            ang = ang + (5 if xs[sp] > xs[c] else -5)
    return (hop, j, ang, (aL, aR), hk, sq, rot, extra)


def ep3v3():
    """Punch-up 2 (Studio 2d6f861 + Nolan "more animation, stir the pot"): both sides get it, silence contest, podcast."""
    xs = (dict(rick=170, kaylee=450, pip=720, mb=960, dot=1200, brad=1470, grandma=1760),
          dict(rick=40, kaylee=330, pip=610, mb=880, dot=1150, brad=1420, grandma=1690))
    T_ = dict(scene="table")

    def ln(who, text, cam=None, gap=0.08, cap=None):
        return ("line", who, text, cap, dict(T_, cams=[(0, cam or "cu_" + who)], gap=gap))

    seq = [
        ("gag", "intro", 2.2, "table", "wide"),
        ln("mb", "Thanksgiving. The one day your family remembers why they moved away."),
        ln("rick", "Pass the potatoes. And don't pass any socialism."),
        ln("kaylee", "Potatoes are colonialism, Rick."),
        ln("dot", "You posted eat the rich from a twelve hundred dollar phone, Kaylee.",
           cap='You posted "eat the rich" from a twelve hundred dollar phone, Kaylee.'),
        ln("kaylee", "Billionaires shouldn't exist!"),
        ln("pip", "Your dad owns nine apartment buildings."),
        ln("kaylee", "That's different. That's my money.", gap=0.0),
        ("hold", 0.3, "cu_rick"),
        ln("rick", "I'm pro-life. Every child is a blessing."),
        ln("grandma", "Richard, you owe child support in three states.", gap=0.0),
        ("hold", 0.3, "cu_rick"),
        ln("rick", "The government is spying on me through my microwave."),
        ln("grandma", "They listened for one week and asked to be transferred."),
        ln("rick", "They're coming for my guns!"),
        ln("dot", "You shot your own foot, Rick. Twice. Same foot.", gap=0.0),
        ("hold", 0.3, "cu_kaylee"),
        ln("kaylee", "I speak for the voiceless."),
        ln("mb", "They asked you to stop, Kaylee. In writing."),
        ln("brad", "I don't vote. I'm a sovereign citizen."),
        ln("grandma", "You're forty and you live in my basement, Bradley. You're barely a tenant."),
        ln("grandma", "I'm eighty-six. The house goes to whoever shuts up first.", gap=0.0),
        ("gag", "hush", 1.3, "table", "two"),
        ln("rick", "Taxation is theft!", "two", gap=0.05),
        ln("kaylee", "That's problematic!", "two", gap=0.05),
        ("line", "grandma", "You're both out. The turkey gets the house. He's the only one here who died for something.",
         None, dict(T_, cams=[(0, "cu_grandma"), (3, "wide")], gap=0.08)),
        ln("rick+kaylee", "The will is rigged!", "two", gap=0.0),
        ("gag", "pod", 0.7, "table", "two"),
        ln("mb", "They started a podcast. It has two million listeners.", "two"),
        ln("grandma", "Oh, hell. Give the turkey the car too.", gap=0.0, cap="Oh, h#@l. Give the turkey the car too."),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.6, "table", "wide"),
    ]

    base = table_layout(xs)

    def layout(L):
        S = base(L)
        x = S["cast"]
        S["cams"]["two"] = ((x["rick"] + x["kaylee"]) / 2, L["feet"] - 290 * L["K"], L["cu"] * 0.62)
        return S

    def hush(t):
        ev = G["ev"]
        return "hush" in ev and ev["hush"] <= t < ev["hush"] + 1.3

    def pod(t):
        return "pod" in G["ev"] and t >= G["ev"]["pod"] and t < G["ev"]["end"]

    def turkey(t):
        l_ = H.lines_with("turkey gets", "grandma")
        return bool(l_) and t >= l_[0]["start"] + 1.0

    def where(c, t, scene, L):
        x = L[scene]["cast"][c]
        if hush(t) and c in ("rick", "kaylee"):   # shaking with the effort of saying nothing
            k = (t - G["ev"]["hush"]) / 1.3
            fi = int(t * FPS)
            return (x + (6 + 16 * k) * (1 if fi % 2 else -1) * (1 if c == "rick" else -1), L["feet"])
        return (x, L["feet"])

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene]["cast"])
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        if hush(t) and c in ("rick", "kaylee"):
            hk = (hk[0], hk[1], hk[2], "wide")
            aL, aR = -30, 30
        if pod(t) and c in ("rick", "kaylee") and li is None:
            aL, aR = (-140, 40) if c == "rick" else (-40, 140)
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def post(fr, cam, t, fi, li, scene, L):
        K, S = L["K"], L[scene]
        d = ImageDraw.Draw(fr)
        z = cam.z * K
        if hush(t):   # sweat flying off both of them, more each frame
            k = (t - G["ev"]["hush"]) / 1.3
            rng = np.random.default_rng(fi)
            for c in ("rick", "kaylee"):
                for n in range(int(2 + 7 * k)):
                    x, y = cam.p(S["cast"][c] + rng.uniform(-130, 130) * K, L["feet"] - rng.uniform(330, 520) * K)
                    r = 11 * z
                    d.polygon([(x, y - r * 2.2), (x + r, y), (x, y + r), (x - r, y)], fill=(120, 190, 250),
                              outline=INK)
        tk = (S["x"]["pip"] + S["x"]["mb"]) / 2
        if turkey(t):   # the turkey gets a crown and a deed
            x, y = cam.p(tk, S["top"] - 150 * K)
            w = 60 * z
            d.polygon([(x - w, y), (x - w, y - w * 0.9), (x - w * 0.5, y - w * 0.4), (x, y - w * 1.1),
                       (x + w * 0.5, y - w * 0.4), (x + w, y - w * 0.9), (x + w, y)], fill=(252, 214, 74),
                      outline=INK, width=max(2, int(4 * z)))
            dx, dy = cam.p(tk + 120 * K, S["top"] - 60 * K)
            d.rectangle([dx - 55 * z, dy - 70 * z, dx + 55 * z, dy + 70 * z], fill=(252, 250, 240), outline=INK,
                        width=max(2, int(4 * z)))
            f = ImageFont.truetype(C.FONT, max(8, int(34 * z)))
            d.text((dx, dy - 30 * z), "DEED", fill=INK, anchor="mm", font=f)
            for q in range(3):
                d.line([dx - 35 * z, dy + q * 18 * z, dx + 35 * z, dy + q * 18 * z], fill=INK,
                       width=max(1, int(3 * z)))
        if pod(t):   # ON AIR sign and a microphone between Rick and Kaylee
            mx = (S["cast"]["rick"] + S["cast"]["kaylee"]) / 2
            x, y = cam.p(mx, L["feet"] - 640 * K)
            on = int(t * 4) % 2 == 0
            d.rounded_rectangle([x - 250 * z, y - 70 * z, x + 250 * z, y + 70 * z], radius=int(18 * z),
                                fill=(200, 40, 32) if on else (120, 24, 20), outline=INK, width=max(3, int(6 * z)))
            f = ImageFont.truetype(C.FONT, max(8, int(84 * z)))
            d.text((x, y), "ON AIR", fill=WHITE, anchor="mm", font=f)
            x2, y2 = cam.p(mx, L["feet"] - 60 * K)
            f2 = ImageFont.truetype(C.FONT, max(8, int(38 * z)))
            d.rectangle([x2 - 290 * z, y2 - 44 * z, x2 + 290 * z, y2 + 44 * z], fill=(20, 20, 24), outline=INK,
                        width=max(2, int(5 * z)))
            d.text((x2, y2), "RIGGED with Rick & Kaylee", fill=(252, 214, 74), anchor="mm", font=f2)
            x3, y3 = cam.p(mx, L["feet"] - 250 * K)
            d.line([x3, y3, x3, y3 + 150 * z], fill=INK, width=max(3, int(10 * z)))
            d.ellipse([x3 - 34 * z, y3 - 60 * z, x3 + 34 * z, y3 + 30 * z], fill=(90, 90, 100), outline=INK,
                      width=max(2, int(5 * z)))

    def sfx(fx, music, ev, lines):
        if "hush" in ev:   # clock ticks, then a rising squeak
            for k in range(4):
                add(fx, C2.tone(1900 if k % 2 else 1500, 0.03, 0.4), ev["hush"] + 0.1 + k * 0.3)
        if "pod" in ev:   # radio sting
            for k, nt in enumerate(["C5", "E5", "G5", "C6"]):
                add(fx, ks(hz(nt), 0.4, 0.995, 0.85, 70 + k), ev["pod"] + 0.05 + k * 0.12, 0.4)

    def silences():
        ev = G["ev"]
        return [(ev["hush"], ev["hush"] + 1.3)] if "hush" in ev else []

    return dict(title="THANKSGIVING POLITICS", end=["WHO'S WORSE,", "RICK OR", "KAYLEE?"], seq=seq,
                scenes={"table": dict(layout=layout, bg=table_bg)},
                post=post, pose_hook=pose_hook, where=where, sfx=sfx, silences=silences)


def ep7v4():
    """QA #15 F1: no pronoun in the bite line."""
    ep = ep7v3()
    ep["seq"] = [(it[0], it[1], "Sage bit me! The vegan bit me!", "Sage BIT me! The vegan bit me!", it[4])
                 if it[0] == "line" and it[2].startswith("She bit me") else it for it in ep["seq"]]
    return ep


def ep5v4():
    """Studio 11/20 rules: 5 swears on punchlines (captions masked), named targets, CEO fired by Gary."""
    ep = ep5()

    def ln(who, text, scene, cam=None, gap=0.08, cap=None):
        return ("line", who, text, cap, dict(scene=scene, cams=[(0, cam or "cu_" + who)], gap=gap))

    ep["seq"] = [
        ("gag", "intro", 2.2, "home", "wide"),
        ln("mb", "My dad got replaced by AI. At work. And then at home.", "home", gap=0.0),
        ("gag", "ceo_in", 0.5, "ceo", "wide"),
        ln("dad", "Twenty years at MegaMart. Replaced by a chatbot named Gary.", "ceo"),
        ln("ceo", "Gary doesn't need lunch, health insurance, or a soul. He's management material.", "ceo"),
        ("line", "dad", "Gary told a customer to put glue on pizza!", None,
         dict(scene="ceo", cams=[(0, "cu_dad"), (6, "glue/wide")], gap=0.1)),
        ln("ceo", "And the guy came back for seconds. That's brand loyalty, dumbass.", "ceo",
           cap="And the guy came back for seconds. That's brand loyalty, dumb#@s."),
        ln("dad", "What about my severance?", "ceo"),
        ln("ceo", "We threw you a pizza party. You weren't invited. It was the glue pizza.", "ceo"),
        ln("ceo", "I just ask myself, what would Zuckerberg do?", "ceo"),
        ln("dad", "Blink on purpose?", "ceo", gap=0.0),
        ("hold", 0.3, "cu_ceo"),
        ("gag", "home_in", 0.5, "home", "wide"),
        ln("dadbot", "Hello, son. I read your report card. I am not angry. I am disappointed at a level no human "
                     "father can reach.", "home", gap=0.0),
        ("hold", 0.3, "cu_mb"),
        ln("mb", "Holy shit. That's way worse.", "home", cap="Holy s#@t. That's way worse."),
        ln("dadbot", "I also read your diary. Chapter three was weak.", "home"),
        ln("mb", "I don't have a diary!", "home"),
        ln("dadbot", "You do now. I wrote it. You cry in chapter four.", "home"),
        ln("dadbot", "Your mother asked if I love her. I said yes in point two seconds. Your father's record is "
                     "nine years.", "home"),
        ln("dad", "That's bullshit! I said it at the wedding!", "home", cap="That's bulls#@t! I said it at the wedding!"),
        ln("dadbot", "You said, you too.", "home", gap=0.0, cap='You said "you too."'),
        ("hold", 0.3, "cu_dad"),
        ("line", "dad", "I coded you, Gary.", "I CODED YOU, GARY.", dict(scene="home", cams=[(0, "cu_dad")], gap=0.1)),
        ("gag", "ceo_back", 0.5, "ceo", "wide"),
        ln("ceo", "Gary's the CEO now. He fired my ass by text. With an emoji.", "ceo",
           cap="Gary's the CEO now. He fired my #@s by text. With an emoji."),
        ("gag", "home_back", 0.3, "home", "wide"),
        ln("mb", "The robot fired the boss. First damn thing it got right.", "home", gap=0.0,
           cap="The robot fired the boss. First d#@n thing it got right."),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.6, "home", "wide"),
    ]

    def where(c, t, scene, L):
        if c == "dad" and scene == "home":
            ln_ = H.lines_with("bullshit", "dad")
            if not ln_ or t < ln_[0]["t0"] - 0.8:
                return None   # Dad is not home yet
        return (L[scene]["cast"][c], L["feet"])

    base_hook = ep["pose_hook"]

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene].get("cast", {}), 0.7)
        return base_hook(c, t, fi, li, scene, p)

    base_sfx = ep["sfx"]

    def sfx(fx, music, ev, lines):
        base_sfx(fx, music, ev, lines)
        if "ceo_back" in ev:   # a text-message ding: the CEO just got fired
            add(fx, C2.tone(1760, 0.08, 0.3), ev["ceo_back"] + 0.05)
            add(fx, C2.tone(2349, 0.12, 0.3), ev["ceo_back"] + 0.15)

    ep.update(where=where, pose_hook=pose_hook, sfx=sfx)
    return ep


def ep6v4():
    """Studio 11/20 rules: 5 swears on punchlines (captions masked), Bezos + Denny's, husband on fire, ultrasound."""
    ep = ep6()
    Y = dict(scene="yard")
    PIPV = "kokoro:aud-pip-b@speed=1.25,pause=0.14"

    def ln(who, text, gap=0.08, cap=None, **kw):
        return ("line", who, text, cap, dict(Y, cams=[(0, "cu_" + who)], gap=gap, **kw))

    ep["seq"] = [
        ("gag", "intro", 2.2, "yard", "wide"),
        ln("mb", "My neighbors are having a baby. So naturally, they bought explosives.", 0.1),
        ln("brittany", "This reveal is gonna go viral, babe!"),
        ln("chadsr", "I got two hundred pounds of blue powder and a cannon from a guy named Scooter."),
        ln("pip", "Is Scooter a professional?", voice=PIPV),
        ln("chadsr", "He's got nine fingers and a dream."),
        ln("chadsr", "This cannon's bigger than Bezos's rocket."),
        ln("dot", "And it looks a little less like a dick.", 0.0, cap="And it looks a little less like a d#@k."),
        ("hold", 0.3, "cu_chadsr"),
        ln("brittany", "We named him Braxtyn. With a Y. And a second Y nobody asked for."),
        ln("dot", "That kid's getting his ass kicked by his own birth certificate.", 0.0,
           cap="That kid's getting his #@s kicked by his own birth certificate."),
        ("gag", "boom", 1.6, "yard", "cu_cannon"),
        ln("chadsr", "It's a boy!"),
        ln("dot", "It's a felony.", 0.0),
        ln("mb", "The shed's on fire. The fence is on fire. Holy shit, the neighbor's boat is on fire.",
           cap="The shed's on fire. The fence is on fire. Holy s#@t, the neighbor's boat is on fire."),
        ln("brittany", "Did we get the shot?"),
        ln("firefighter", "Ma'am, you got the shot, the church, and a Denny's two towns over."),
        ln("firefighter", "Also, your husband is on fire."),
        ln("brittany", "Is the lighting good?", 0.0),
        ("hold", 0.3, "cu_chadsr"),
        ln("firefighter", "Whose idea was the cannon?"),
        ln("chadsr", "Scooter's."),
        ln("firefighter", "Scooter's in jail, sir. Again."),
        ln("brittany", "For how long?", 0.0),
        ("gag", "look", 0.8, "yard", "cu_chadsr"),
        ln("grandma", "In my day we found out when it came out. And we were thrilled if the damn thing had a pulse.",
           cap="In my day we found out when it came out. And we were thrilled if the d#@n thing had a pulse."),
        ln("pip", "Hey, why does the baby in the ultrasound have nine fingers?", 0.0, voice=PIPV),
        ("gag", "freeze", 1.0, "yard", "wide"),
        ln("chadsr", "Son of a bitch. Bigger cannon.", 0.0, cap="Son of a b#@ch. Bigger cannon."),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.6, "yard", "wide"),
    ]

    def where(c, t, scene, L):
        if c == "firefighter":
            l_ = H.lines_with("you got the shot", "firefighter")
            if not l_ or t < l_[0]["t0"] - 0.6:
                return None
        return (L[scene]["cast"][c], L["feet"])

    def burning(t):
        l_ = H.lines_with("husband is on fire", "firefighter")
        l2 = H.lines_with("Whose idea", "firefighter")
        return bool(l_) and l_[0]["t0"] <= t < (l2[0]["t0"] if l2 else 1e9)

    base_post, base_hook, base_sfx = ep["post"], ep["pose_hook"], ep["sfx"]

    def post(fr, cam, t, fi, li, scene, L):
        base_post(fr, cam, t, fi, li, scene, L)
        K = L["K"]
        ev = G["ev"]
        if "boom" in ev and t >= ev["boom"] + 0.6:   # the fence keeps burning behind them
            fy = L["feet"] - 330 * K
            for k, x in enumerate((900, 1300, 1700)):
                fire(fr, cam, x, fy - 250 * K, 90 * K, t, 30 + k)
        if burning(t):   # Chad's hat is on fire; he hasn't noticed
            fire(fr, cam, L[scene]["cast"]["chadsr"], L["feet"] - 500 * K, 80 * K, t, 77)
        l_ = H.lines_with("ultrasound", "pip")
        if l_ and t >= l_[0]["t0"] + 0.5:   # Pip holds up the scan
            z = cam.z * K
            x, y = cam.p(L[scene]["cast"]["pip"] + 150 * K, L["feet"] - 330 * K)
            d = ImageDraw.Draw(fr)
            d.rectangle([x - 110 * z, y - 90 * z, x + 110 * z, y + 90 * z], fill=(16, 18, 26), outline=WHITE,
                        width=max(2, int(6 * z)))
            d.ellipse([x - 60 * z, y - 50 * z, x + 20 * z, y + 30 * z], fill=(190, 196, 206))
            d.ellipse([x + 5 * z, y - 10 * z, x + 75 * z, y + 60 * z], fill=(170, 176, 188))
            d.text((x, y + 66 * z), "9 FINGERS", fill=(120, 190, 250), anchor="mm",
                   font=ImageFont.truetype(FONT, max(8, int(26 * z))))

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene].get("cast", {}), 0.7)
        hop, j, ang, (aL, aR), hk, sq, rot, extra = base_hook(c, t, fi, li, scene, p)
        ev = G["ev"]
        if "look" in ev and ev["look"] <= t < ev["look"] + 0.8 and c == "chadsr":
            ang, hk = 8, (hk[0], hk[1], "wide", hk[3])
        if "freeze" in ev and ev["freeze"] <= t < ev["freeze"] + 1.0:
            hop, hk = 0, (hk[0], hk[1], "wide", hk[3])
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def sfx(fx, music, ev, lines):
        base_sfx(fx, music, ev, lines)
        if "freeze" in ev:
            add(fx, ks(hz("D3"), 0.6, 0.995, 0.6, 30), ev["freeze"] + 0.1, 0.5)
            add(fx, ks(hz("C#3"), 0.9, 0.995, 0.6, 31), ev["freeze"] + 0.55, 0.5)

    def silences():
        ev = G["ev"]
        return [(ev["freeze"], ev["freeze"] + 1.0)] if "freeze" in ev else []

    ep.update(where=where, post=post, pose_hook=pose_hook, sfx=sfx, silences=silences)
    return ep


@eprop("wine")
def _wine(z):
    return render_shapes([("p", strip([(0, 60), (0, 0)], 8), (220, 226, 236)),
                          ("e", (0, 62, 26, 8), (220, 226, 236)),
                          ("pts", ell(0, -30, 34, 40, 0, 180) + [(-34, -30)], (220, 226, 236)),
                          ("pts", ell(0, -26, 28, 32, 0, 180) + [(-28, -26)], (150, 20, 50), False)], z, 150, 530)


@eprop("slip")
def _slip(z):
    img = render_shapes([("p", [(-34, -50), (34, -50), (34, 50), (-34, 50)], (250, 246, 220))], z, 120, 531)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    d.text((c, c - 16 * z), "BET", font=ImageFont.truetype(FONT, max(6, int(22 * z))), fill=(200, 40, 32), anchor="mm")
    d.text((c, c + 14 * z), "DAL", font=ImageFont.truetype(FONT, max(6, int(22 * z))), fill=(30, 50, 110), anchor="mm")
    return img


def booth_layout(L):
    vert = L["H"] > L["W"]
    if vert:
        return dict(cast=dict(father=300, mb=800, grandma=1500), wall=550, wide=(550, 1300, 0.96))
    return dict(cast=dict(father=600, mb=1320, grandma=2300), wall=960, wide=(960, 600, 1.0))


def booth_bg(L, cam, scene):
    W, H_, z = L["W"], L["H"], cam.z
    K, F = L["K"], L["feet"]
    S = L[scene]
    rng = np.random.default_rng(171)
    img = Image.new("RGBA", (W, H_))
    paper(img, cam.pts([(-900, -900), (3200, -900), (3200, 3000), (-900, 3000)]), (74, 48, 34), rng, z,
          shadow=False, jitter=False, edge=False)
    for k in range(-6, 30):   # wood panels
        x = k * 150
        paper(img, cam.pts([(x, F - 1500 * K), (x + 138, F - 1500 * K), (x + 138, F + 60), (x, F + 60)]),
              (96, 62, 42) if k % 2 else (104, 68, 46), rng, z, sh=3)
    wx = S["wall"]   # the dividing wall with the lattice window
    paper(img, cam.pts([(wx - 46, F - 1500 * K), (wx + 46, F - 1500 * K), (wx + 46, F + 60), (wx - 46, F + 60)]),
          (60, 38, 26), rng, z, sh=8)
    wy = F - 330 * K
    paper(img, cam.pts([(wx - 40, wy - 110 * K), (wx + 40, wy - 110 * K), (wx + 40, wy + 110 * K),
                        (wx - 40, wy + 110 * K)]), (30, 20, 16), rng, z, shadow=False)
    for k in range(-4, 5):
        paper(img, cam.pts(strip([(wx - 40, wy + k * 28 * K), (wx + 40, wy + (k + 2) * 28 * K)], 4)), (150, 110, 70),
              rng, z, shadow=False)
        paper(img, cam.pts(strip([(wx + 40, wy + k * 28 * K), (wx - 40, wy + (k + 2) * 28 * K)], 4)), (150, 110, 70),
              rng, z, shadow=False)
    paper(img, cam.pts([(-900, F - 10), (3200, F - 10), (3200, 3000), (-900, 3000)]), (52, 34, 26), rng, z,
          shadow=False)
    d = ImageDraw.Draw(img)
    fx = S["cast"]["father"]   # the price board over the priest
    paper(img, cam.pts([(fx - 190 * K, F - 780 * K), (fx + 190 * K, F - 790 * K), (fx + 190 * K, F - 610 * K),
                        (fx - 190 * K, F - 600 * K)]), (250, 246, 226), rng, z, sh=6)
    d.text(cam.p(fx, F - 740 * K), "CONFESSION", font=ImageFont.truetype(FONT, max(8, int(46 * z * K))), fill=INK,
           anchor="mm")
    d.text(cam.p(fx, F - 680 * K), "CASH - CARD - TAP", font=ImageFont.truetype(FONT, max(8, int(30 * z * K))),
           fill=(200, 40, 32), anchor="mm")
    d.text(cam.p(fx, F - 636 * K), "3% FEE", font=ImageFont.truetype(FONT, max(8, int(28 * z * K))), fill=INK,
           anchor="mm")
    return C.vignette(img)


def confession():
    """NEW (Studio 11/20, priest lane): the priest is doing worse than every sin Meatball confesses."""
    B = dict(scene="booth")

    def ln(who, text, gap=0.08, cap=None):
        return ("line", who, text, cap, dict(B, cams=[(0, "cu_" + who)], gap=gap))

    seq = [
        ("gag", "intro", 2.2, "booth", "wide"),
        ln("mb", "Grandma made me go to confession. I've never been. How bad could it be?", 0.1),
        ln("father", "How long since your last confession, my son?"),
        ln("mb", "What's the longest anybody's ever said? Add a day.", 0.0),
        ("hold", 0.3, "cu_father"),
        ln("mb", "I ate a whole lasagna and blamed the dog."),
        ln("father", "Gluttony. Ten Hail Marys."),
        ln("mb", "You're drinking wine at nine A M, Father.", cap="You're drinking wine at nine A.M., Father."),
        ln("father", "It's a work drink, smartass.", 0.0, cap="It's a work drink, smart#@s."),
        ("hold", 0.3, "cu_mb"),
        ln("mb", "I skipped church for football."),
        ln("father", "So did I. I had the Cowboys. God's been punishing me since ninety-six."),
        ("line", "mb", "Father. Is greed, a sin?", "Is greed a sin?", dict(B, cams=[(0, "cu_mb")], gap=0.08, voice="kokoro:adam-puck@speed=1.16")),
        ln("father", "Deadly."),
        ("line", "mb", "Your collection plate takes Apple Pay.", None, dict(B, cams=[(0, "cu_mb")], gap=0.08, voice="kokoro:adam-puck@speed=1.16")),
        ln("father", "With a three percent convenience fee. That's not greed. That's overhead."),
        ("line", "mb", "The Vatican has its own bank, Father.", None, dict(B, cams=[(0, "cu_mb")], gap=0.08, voice="kokoro:adam-puck@speed=1.16")),
        ln("father", "Have you seen that roof? Gold doesn't polish its damn self.", 0.0,
           cap="Have you seen that roof? Gold doesn't polish its d#@n self."),
        ("hold", 0.3, "cu_mb"),
        ln("mb", "I fell asleep during your sermon."),
        ln("father", "Which part?"),
        ln("mb", "The first forty minutes."),
        ln("father", "Shit, me too. I've done the same one since Easter.", 0.0,
           cap="S#@t, me too. I've done the same one since Easter."),
        ("hold", 0.3, "cu_mb"),
        ln("father", "Now your penance. Feel guilty."),
        ln("mb", "For how long?"),
        ln("father", "Forever. That's the whole business model.", 0.0),
        ("gag", "knock", 0.5, "booth", "wide"),
        ln("grandma", "Is he done? I've got forty years of bingo fraud to unload!"),
        ln("father", "Kid. My turn. I need to confess something."),
        ln("mb", "That is not how this works."),
        ln("father", "I bet the bingo money. On the Cowboys.", 0.0),
        ("hold", 0.3, "cu_mb"),
        ln("grandma", "You son of a bitch! That was my bingo fraud!", cap="You son of a b#@ch! That was MY bingo fraud!"),
        ln("mb", "I came in with a lasagna. I'm leaving as a damn witness.", 0.0,
           cap="I came in with a lasagna. I'm leaving as a d#@n witness."),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.6, "booth", "wide"),
    ]

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene]["cast"], 0.7)
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        if c == "father":
            bet = H.lines_with("bingo money", "father")
            if bet and t >= bet[0]["t0"]:
                aR, extra["item"] = max(aR, 120), ("slip", "R", 0)
            else:
                aR, extra["item"] = max(aR, 70), ("wine", "R", 0)
        if c == "mb":
            w = H.lines_with("My turn", "father")
            if w and t >= w[0]["t0"]:
                hk = (hk[0], hk[1], hk[2], "wide")
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def sfx(fx, music, ev, lines):
        if "knock" in ev:
            for k in range(3):
                C2.thud(fx, ev["knock"] + 0.05 + k * 0.14, 0.5)
        add(fx, ks(hz("C3"), 2.0, 0.998, 0.5, 90), 2.3, 0.25)   # a churchy low note under the first line
        add(fx, ks(hz("G3"), 2.0, 0.998, 0.5, 91), 2.3, 0.2)

    def shakes():
        ev = G["ev"]
        return [(ev["knock"] + k * 0.14, 0.5) for k in range(3)] if "knock" in ev else []

    return dict(title="GOES TO CONFESSION", end=["WHAT WOULD", "YOU", "CONFESS?"], seq=seq,
                scenes={"booth": dict(layout=booth_layout, bg=booth_bg)},
                pose_hook=pose_hook, sfx=sfx, shakes=shakes)


def clinic_layout(L):
    vert = L["H"] > L["W"]
    if vert:
        xs = dict(doctor=130, pip=380, mb=630, dot=880, tank=1140, sage=1420, grandma=1700)
        return dict(cast=xs, wide=(630, 1380, 0.85))
    xs = dict(doctor=300, pip=620, mb=960, dot=1300, tank=1620, sage=1960, grandma=2300)
    return dict(cast=xs, wide=(960, 600, 1.0))


def clinic_bg(L, cam, scene):
    W, H_, z = L["W"], L["H"], cam.z
    K, F = L["K"], L["feet"]
    rng = np.random.default_rng(181)
    img = Image.new("RGBA", (W, H_))
    paper(img, cam.pts([(-900, -900), (3200, -900), (3200, 3000), (-900, 3000)]), (214, 232, 226), rng, z,
          shadow=False, jitter=False, edge=False)
    wall_b = F - 260 * K
    paper(img, cam.pts([(-900, wall_b - 30 * K), (3200, wall_b - 30 * K), (3200, wall_b), (-900, wall_b)]),
          (150, 180, 176), rng, z, sh=3)
    paper(img, cam.pts([(-900, wall_b), (3200, wall_b), (3200, 3000), (-900, 3000)]), (196, 200, 204), rng, z,
          shadow=False)
    d = ImageDraw.Draw(img)
    for k, (px, title, sub) in enumerate(((300, "BMI", "BIG MEATBALL INDEX"), (980, "E", "F P  T O Z"),
                                          (1620, "DIET", "AND EXERCISE"))):
        paper(img, cam.pts([(px - 170 * K, wall_b - 760 * K), (px + 170 * K, wall_b - 766 * K),
                            (px + 170 * K, wall_b - 470 * K), (px - 170 * K, wall_b - 464 * K)]), (252, 250, 240),
              rng, z, sh=6)
        d.text(cam.p(px, wall_b - 670 * K), title, font=ImageFont.truetype(FONT, max(8, int(90 * z * K))), fill=INK,
               anchor="mm")
        d.text(cam.p(px, wall_b - 540 * K), sub, font=ImageFont.truetype(FONT, max(8, int(28 * z * K))),
               fill=(200, 40, 32), anchor="mm")
    return C.vignette(img)


def ozempic():
    """NEW (Studio 11/20, fat lane): Meatball owns it; he shrinks on the shot, then pops back in one frame."""
    O = dict(scene="clinic")

    def ln(who, text, gap=0.08, cap=None, cam=None):
        return ("line", who, text, cap, dict(O, cams=[(0, cam or "cu_" + who)], gap=gap))

    seq = [
        ("gag", "intro", 2.2, "clinic", "wide"),
        ln("mb", "I'm a meatball. I am literally a ball of meat. And my doctor says I need to lose weight.", 0.1),
        ln("doctor", "You're ninety percent fat."),
        ("line", "mb", "I am eighty, twenty, Doc. That's the good blend.", "I'm eighty-twenty, Doc. That's the good blend.",
         dict(O, cams=[(0, "cu_mb")], gap=0.08, voice="kokoro:adam-puck@speed=1.16")),
        ln("doctor", "Have you tried diet and exercise?"),
        ln("mb", "Have you tried shutting the hell up?", 0.0, cap="Have you tried shutting the h#@l up?"),
        ("hold", 0.3, "cu_doctor"),
        ln("tank", "Bro, just lift."),
        ln("mb", "I don't have a neck, Tank. Neither do you, and yours was a choice."),
        ln("sage", "Have you tried kale?"),
        ln("mb", "Kale tastes like a lawn that hates you."),
        ln("dot", "Everybody famous is on the shot."),
        ln("mb", "You get a shot! You get a shot!"),
        ("line", "pip", "Celebrities say it's just water and pilates.", None,
         dict(O, cams=[(0, "cu_pip")], gap=0.08, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ln("dot", "And my dad's just at the store. Since twenty nineteen.", 0.0),
        ("gag", "shot", 0.8, "clinic", "cu_mb"),
        ln("mb", "Day one. I looked at a breadstick and felt nothing. Who the hell am I?",
           cap="Day one. I looked at a breadstick and felt nothing. Who the h#@l am I?"),
        ln("mb", "Day ten. I left food on my plate. On purpose. Like a psychopath."),
        ln("mb", "Day thirty. I'm a slider."),
        ln("mb", "Day sixty. Holy shit, I'm a Swedish meatball. They're gonna sell me at IKEA with a little flag.",
           0.0, cap="Day sixty. Holy s#@t, I'm a Swedish meatball. They're gonna sell me at IKEA with a little flag."),
        ("hold", 0.3, "wide"),
        ln("grandma", "You look sick. Eat something."),
        ln("mb", "You called me fat for thirty years!"),
        ln("grandma", "And now you're too skinny. I contain multitudes, dumbass.", 0.0,
           cap="And now you're too skinny. I contain multitudes, dumb#@s."),
        ("hold", 0.3, "cu_mb"),
        ln("doctor", "Bad news. Your insurance stopped covering it."),
        ln("mb", "How much without insurance?", 0.0),
        ("gag", "whisper", 0.9, "clinic", "cu_doctor"),
        ln("mb", "For that I could buy a cow.", 0.0, cap="For THAT I could buy a cow."),
        ("gag", "boing", 0.7, "clinic", "wide"),
        ln("mb", "I'm back, baby. Eighty twenty. Somebody bring me a damn lasagna.",
           cap="I'm back, baby. Eighty-twenty. Somebody bring me a d#@n lasagna."),
        ("line", "pip", "That took one second.", None,
         dict(O, cams=[(0, "cu_pip")], gap=0.08, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
        ln("mb", "It's called a rebound, Pip. Ask your mom's boyfriend.", 0.0),
        ("hold", 0.3, "wide"),
        ("gag", "end", 2.6, "clinic", "wide"),
    ]
    STEPS = (("Day one", 0.84), ("Day ten", 0.7), ("Day thirty", 0.54), ("Day sixty", 0.36))

    def size(t):
        ev = G["ev"]
        if "shot" not in ev or t < ev["shot"] + 0.3:
            return 1.0
        if "boing" in ev and t >= ev["boing"] + 0.15:
            k = (t - ev["boing"] - 0.15) / 0.35   # overshoot, then settle
            return 1.0 + (0.35 * (1 - k) if k < 1 else 0.0)
        s = 0.92
        for key, v in STEPS:
            l_ = H.lines_with(key, "mb")
            if l_ and t >= l_[0]["t0"] - 0.1:
                s = v
        return s

    def where(c, t, scene, L):
        if c == "mb" and abs(size(t) - 1.0) > 0.01:
            return None   # drawn at his own size in post()
        return (L[scene]["cast"][c], L["feet"])

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene]["cast"], 0.7)
        hop, j, ang, (aL, aR), hk, sq, rot, extra = p
        ev = G["ev"]
        if c == "mb" and "shot" in ev and ev["shot"] <= t < ev["shot"] + 0.8:
            hk = (hk[0], hk[1], hk[2], "wide")
        if c == "doctor" and "boing" in ev and t >= ev["boing"] + 0.15:
            rot, hop = 80, 0   # knocked flat by the rebound
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra)

    def post(fr, cam, t, fi, li, scene, L):
        s = size(t)
        K = L["K"]
        x = L[scene]["cast"]["mb"]
        if abs(s - 1.0) > 0.01:
            sx, sy = cam.p(x, L["feet"])
            z2 = cam.z * s
            cam2 = Cam(L, x - (sx - L["W"] / 2) / z2, L["feet"] - (sy - L["H"] / 2) / z2, z2)
            pz = H.pose("mb", t, fi, li, scene)
            pz = pose_hook("mb", t, fi, li, scene, pz)
            H.draw_any(fr, cam2, "mb", x, L["feet"], pz)
        ev = G["ev"]
        d = ImageDraw.Draw(fr)
        if "shot" in ev and ev["shot"] <= t < ev["shot"] + 0.6:   # the needle, cartoon size
            z = cam.z * K
            nx, ny = cam.p(x + (260 - 300 * min(1, (t - ev["shot"]) / 0.25)) * K, L["feet"] - 200 * K)
            d.rectangle([nx, ny - 16 * z, nx + 150 * z, ny + 16 * z], fill=(230, 240, 250), outline=INK,
                        width=max(2, int(4 * z)))
            d.line([nx - 70 * z, ny, nx, ny], fill=(120, 120, 130), width=max(2, int(5 * z)))
            d.rectangle([nx + 150 * z, ny - 28 * z, nx + 166 * z, ny + 28 * z], fill=(90, 140, 220), outline=INK)
        if "boing" in ev and 0.15 <= t - ev["boing"] < 0.6:
            px, py = cam.p(x, L["feet"] - 560 * K)
            paste(fr, C2.spr("star", round(cam.z * K * 1.5, 2), "BOING!"), px, py, (fi % 2) * 10)

    def sfx(fx, music, ev, lines):
        if "shot" in ev:   # a long tire hiss as he deflates
            add(fx, C2.noise_burst(1.2, 0.25, 51, 2), ev["shot"] + 0.3, 0.3)
        if "whisper" in ev:   # psst-psst
            for k in range(4):
                add(fx, C2.noise_burst(0.12, 0.08, 60 + k, 2), ev["whisper"] + 0.1 + k * 0.18, 0.25)
        if "boing" in ev:
            b = ev["boing"] + 0.15
            n = int(0.5 * SR)
            tt = np.arange(n) / SR
            sweep = (np.sin(2 * np.pi * (180 + 500 * tt) * tt) * np.exp(-tt * 5)).astype(np.float32)
            add(fx, sweep, b, 0.7)
            C2.thud(fx, b, 0.8)

    def shakes():
        ev = G["ev"]
        return [(ev["boing"] + 0.15, 1.2)] if "boing" in ev else []

    return dict(title="MEATBALL ON OZEMPIC", end=["TEAM SHOT", "OR TEAM", "LASAGNA?"], seq=seq,
                scenes={"clinic": dict(layout=clinic_layout, bg=clinic_bg)},
                where=where, pose_hook=pose_hook, post=post, sfx=sfx, shakes=shakes)


def nobanner(base, headline):
    """The Studio 11/20 opening for any episode: 0.3 s in, the first line starts under one caps headline."""
    def make():
        ep = base()
        ep["seq"] = [("gag", "intro", 0.3) + ep["seq"][0][3:]] + ep["seq"][1:]
        ep["headline"] = headline
        return ep
    return make


def t58(short=False):
    """Studio batch 1 v2 #1 (roast): THE $58.63 THANKSGIVING. short=True is the 30 s YouTube cut."""
    xs = (dict(rick=170, kaylee=450, pip=720, mb=960, dot=1200, bezos=1470, grandma=1760),
          dict(rick=40, kaylee=330, pip=610, mb=880, dot=1150, bezos=1420, grandma=1690))
    T_ = dict(scene="table")
    PIPV = "kokoro:aud-pip-b@speed=1.25,pause=0.14"

    def ln(who, text, gap=0.06, cap=None, **kw):
        return ("line", who, text, cap, dict(T_, cams=[(0, "cu_" + who)], gap=gap, **kw))

    extra = [] if short else [
        ln("pip", "Do kids eat free?", voice=PIPV),
        ln("grandma", "Kids eat what Rick drops."),
        ln("dot", "Fifty-eight bucks, and the stuffing's from a box."),
        ln("grandma", "So is your grandfather, sweetie. Top shelf, next to the gravy.", 0.0),
        ("hold", 0.3, "cu_dot"),
        ln("kaylee", "Can I just Venmo you?"),
        ln("grandma", "Your Venmo's public, Kaylee. We all saw, thanks for last night, Trevor.",
           cap='Your Venmo\'s public, Kaylee. We all saw "thanks for last night, Trevor."'),
        ln("rick", "Who the hell is Trevor?", 0.0, cap="Who the h#@l is Trevor?"),
        ("hold", 0.3, "cu_kaylee"),
        ln("kaylee", "Also, I'm gluten free now."),
        ln("grandma", "You're personality free, Kaylee. The bread stays."),
        ln("rick", "Ma, I can't pay. I'm between jobs."),
        ln("grandma", "You've been between jobs since Blockbuster closed, you lazy bastard.", 0.0,
           cap="You've been between jobs since Blockbuster closed, you lazy b#@tard."),
        ("hold", 0.3, "cu_rick"),
        ln("mb", "Do I pay? I'm literally a side dish."),
        ln("grandma", "Half price. You're mostly breadcrumbs.", 0.0),
        ("hold", 0.3, "cu_mb"),
    ]
    seq = [
        ("gag", "intro", 0.3, "table", "cu_grandma"),
        ln("grandma", "Fifty-eight sixty-three a plate."),
        ln("rick", "For this? Your turkey's drier than your last orgasm, Ma.",
           cap="For THIS? Your turkey's drier than your last orgasm, Ma."),
        ln("grandma", "Least I had one. Your ex-wife says you finish faster than the microwave."),
        ln("kaylee", "Rick, the microwave at least beeps when it's done."),
        ln("rick", "Shut up, Kaylee. Your husband's on Tinder, listed as single, emotionally.",
           cap='Shut up, Kaylee. Your husband\'s on Tinder listed as "single, emotionally."'),
        ln("kaylee", "At least I have a husband. You've got a parole officer and a Fleshlight.", 0.0,
           cap="At least I HAVE a husband. You've got a parole officer and a Fleshlight."),
        ("hold", 0.25, "cu_rick"),
    ] + extra + [
        ln("rick", "Fine! I'm ordering Thanksgiving from Amazon!", 0.0),
        ("gag", "box", 0.7, "table", "cu_bezos"),
        ln("bezos", "Turkey ships Tuesday. Bathroom's a bottle."),
        ln("grandma", "Perfect. Rick's been pissing in bottles since the divorce.", 0.0,
           cap="Perfect. Rick's been p#@sing in bottles since the divorce."),
        ("hold", 0.25, "cu_rick"),
        ln("mb", "Moral of the story: this family's a dumpster fire, but at least it's our goddamn dumpster.", 0.0,
           cap="Moral of the story: this family's a dumpster fire, but at least it's OUR g#@damn dumpster."),
        ("hold", 0.2, "wide"),
        ("gag", "end", 2.0 if short else 2.6, "table", "wide"),
    ]

    def boxt():
        return G["ev"].get("box", 1e9)

    def where(c, t, scene, L):
        x = L[scene]["cast"][c]
        if c == "bezos":
            d = t - boxt()
            if d < 0.15:
                return None
            pop = min(1.0, (d - 0.15) / 0.18)   # he pops up out of the box
            return (x, L["feet"] + (1 - pop) * 260 * L["K"])
        return (x, L["feet"])

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene]["cast"], 0.8)
        hop, j, ang, (aL, aR), hk, sq, rot, extra_ = p
        if c == "bezos" and boxt() + 0.15 <= t < boxt() + 0.9:
            aL, aR = -150, 150
        if c == "rick" and boxt() <= t < boxt() + 0.9:
            hk = (hk[0], hk[1], hk[2], "wide")
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra_)

    def post(fr, cam, t, fi, li, scene, L):
        K, S = L["K"], L[scene]
        z = cam.z * K
        d = ImageDraw.Draw(fr)
        if t < 2.6:   # the small source tag under the headline
            w, h = L["W"], L["H"]
            f = ImageFont.truetype(FONT, int(h * 0.019))
            txt = "Farm Bureau: $58.63 feeds 10"
            tw = d.textlength(txt, font=f)
            y = L["banner_y"] + int(104 * 0.6 * 2.6)
            d.rectangle([w / 2 - tw / 2 - 16, y - 8, w / 2 + tw / 2 + 16, y + h * 0.019 + 14], fill=(252, 250, 240),
                        outline=INK, width=3)
            d.text((w / 2, y), txt, font=f, fill=INK, anchor="ma")
        gx = S["cast"]["grandma"]   # Grandma's card reader, on the table in front of her
        x, y = cam.p(gx - 120 * K, S["top"] - 30 * K)
        d.rounded_rectangle([x - 34 * z, y - 56 * z, x + 34 * z, y + 30 * z], radius=int(8 * z), fill=(40, 40, 46),
                            outline=INK, width=max(2, int(4 * z)))
        d.rectangle([x - 24 * z, y - 46 * z, x + 24 * z, y - 14 * z], fill=(120, 220, 140))
        d.text((x, y - 30 * z), "$58.63", font=ImageFont.truetype(FONT, max(6, int(15 * z))), fill=INK, anchor="mm")
        if t >= boxt():   # the delivery box on the table
            bx = S["cast"]["bezos"]
            drop = min(1.0, (t - boxt()) / 0.12)
            x0, y0 = cam.p(bx - 150 * K, S["top"] - (150 + (1 - drop) * 900) * K)
            x1, y1 = cam.p(bx + 150 * K, S["top"] + (30 - (1 - drop) * 900) * K)
            d.rectangle([x0, y0, x1, y1], fill=(196, 150, 96), outline=INK, width=max(2, int(5 * z)))
            d.rectangle([(x0 + x1) / 2 - 16 * z, y0, (x0 + x1) / 2 + 16 * z, y1], fill=(60, 110, 200))
            d.arc([x0 + 50 * z, y0 + 40 * z, x1 - 50 * z, y1 - 30 * z], 20, 160, fill=INK, width=max(2, int(7 * z)))
            if t < boxt() + 0.5:
                px, py = cam.p(bx, S["top"] - 430 * K)
                paste(fr, C2.spr("star", round(z * 1.3, 2), "THUD!"), px, py, (fi % 2) * 10)

    def sfx(fx, music, ev, lines):
        if "box" in ev:
            C2.thud(fx, ev["box"] + 0.1, 0.9)
            add(fx, C2.tone(1320, 0.1, 0.3), ev["box"] + 0.3)

    def shakes():
        return [(boxt() + 0.1, 1.0)] if "box" in G["ev"] else []

    return dict(title="THE $58.63 THANKSGIVING", end=["GRANDMA OR BEZOS:", "WHO'S THE", "BIGGER CROOK?"], seq=seq,
                headline=["GRANDMA CHARGES", "$58.63 A PLATE"], target=0 if short else 62.1,
                scenes={"table": dict(layout=table_layout(xs), bg=table_bg)},
                where=where, pose_hook=pose_hook, post=post, sfx=sfx, shakes=shakes)


def diner_layout(L):
    vert = L["H"] > L["W"]
    if vert:
        return dict(cast=dict(trump=150, xi=470, putin=790, mb=1130), top=L["feet"] - 150 * L["K"],
                    wide=(640, 1380, 0.85))
    return dict(cast=dict(trump=420, xi=820, putin=1220, mb=1640), top=L["feet"] - 150 * L["K"],
                wide=(960, 600, 1.0))


def diner_bg(L, cam, scene):
    W, H_, z = L["W"], L["H"], cam.z
    K, F = L["K"], L["feet"]
    rng = np.random.default_rng(191)
    img = Image.new("RGBA", (W, H_))
    paper(img, cam.pts([(-900, -900), (3200, -900), (3200, 3000), (-900, 3000)]), (112, 34, 40), rng, z,
          shadow=False, jitter=False, edge=False)
    for k in range(-6, 26):   # wallpaper stripes
        x = k * 130
        paper(img, cam.pts([(x, F - 1600 * K), (x + 40, F - 1600 * K), (x + 40, F - 420 * K), (x, F - 420 * K)]),
              (130, 44, 50), rng, z, shadow=False, jitter=False, edge=False)
    paper(img, cam.pts([(-900, F - 430 * K), (3200, F - 430 * K), (3200, F - 400 * K), (-900, F - 400 * K)]),
          (226, 184, 56), rng, z, sh=3)
    paper(img, cam.pts([(-900, F - 400 * K), (3200, F - 400 * K), (3200, 3000), (-900, 3000)]), (70, 44, 34), rng, z,
          shadow=False)
    for k, x in enumerate((300, 960, 1500)):   # gold-framed pictures
        paper(img, cam.pts([(x - 120 * K, F - 900 * K), (x + 120 * K, F - 900 * K), (x + 120 * K, F - 640 * K),
                            (x - 120 * K, F - 640 * K)]), (226, 184, 56), rng, z, sh=6)
        paper(img, cam.pts([(x - 96 * K, F - 876 * K), (x + 96 * K, F - 876 * K), (x + 96 * K, F - 664 * K),
                            (x - 96 * K, F - 664 * K)]), [(60, 90, 120), (90, 120, 80), (120, 90, 60)][k], rng, z,
              shadow=False)
    return C.vignette(img)


def bill(short=False):
    """Studio batch 1 v2 #2 (roast): TRUMP, XI & PUTIN SPLIT THE DINNER BILL. Obvious cartoon satire; generic voices."""
    D_ = dict(scene="diner")

    def ln(who, text, gap=0.06, cap=None):
        return ("line", who, text, cap, dict(D_, cams=[(0, "cu_" + who)], gap=gap))

    extra = [] if short else [
        ln("putin", "In Russia, we split the bill three ways. I take all three."),
        ln("trump", "That's also how he does elections.", 0.0),
        ("hold", 0.3, "cu_putin"),
        ln("xi", "I cannot use my card. It is being monitored."),
        ln("trump", "Who the hell monitors your card?", cap="Who the h#@l monitors your card?"),
        ln("xi", "Me.", 0.0),
        ("hold", 0.3, "cu_mb"),
        ln("trump", "I always pay my bills. Everybody says so."),
        ln("xi", "Ask your contractors.", 0.0),
        ("hold", 0.3, "cu_trump"),
        ln("putin", "I left my wallet at home."),
        ln("xi", "Which home? The palace you swear is not yours?", 0.0),
        ("hold", 0.3, "cu_putin"),
        ln("mb", "Should I split it three ways?"),
        ln("trump", "Four. Send one to NATO."),
        ln("putin", "I do not like that word.", 0.0),
        ("hold", 0.3, "cu_mb"),
        ln("mb", "Anyone want dessert?"),
        ln("trump", "Two scoops for me. One for them.", 0.0),
        ("hold", 0.3, "cu_xi"),
    ]
    seq = [
        ("gag", "intro", 0.3, "diner", "wide"),
        ln("mb", "Gentlemen, your check."),
        ln("trump", "Put it on China. Everything else is."),
        ln("xi", "You want me to pay? You've been bankrupt six times."),
        ln("trump", "Six times, and I'm still richer than your entire Winnie the Pooh fan club."),
        ln("putin", "Relax. I will pay with Russian money."),
        ln("trump", "Vlad, Russian money is a Monopoly box with a shotgun in it."),
        ln("putin", "Says the man who sold steaks at Sharper Image.", 0.0),
        ("hold", 0.25, "cu_trump"),
    ] + extra + [
        ln("xi", "Both of you, shut up. I'll pay. Just give me the waiter's data."),
        ln("mb", "I'm a meatball!"),
        ln("trump", "Then we tariff the meatball.", 0.0),
        ("hold", 0.25, "cu_mb"),
        ln("mb", "Moral of the story: three superpowers, zero wallets, and the meatball still gets screwed. Goddamn.",
           0.0, cap="Moral of the story: three superpowers, zero wallets, and the meatball still gets screwed. G#@damn."),
        ("hold", 0.2, "wide"),
        ("gag", "end", 2.0 if short else 2.6, "diner", "wide"),
    ]
    TAGS = (("trump", "TRUMP"), ("xi", "XI"), ("putin", "PUTIN"))

    def pose_hook(c, t, fi, li, scene, p):
        p = lively(c, t, li, p, G["L"][scene]["cast"], 0.8)
        hop, j, ang, (aL, aR), hk, sq, rot, extra_ = p
        tar = H.lines_with("tariff", "trump")
        if c == "mb" and tar and t >= tar[0]["t0"]:
            hk = (hk[0], hk[1], hk[2], "wide")
        return (hop, j, ang, (aL, aR), hk, sq, rot, extra_)

    def post(fr, cam, t, fi, li, scene, L):
        K, S = L["K"], L[scene]
        z = cam.z * K
        d = ImageDraw.Draw(fr)
        x0, y0 = cam.p(S["cast"]["trump"] - 190 * K, S["top"])   # the table, in front of the three presidents
        x1, y1 = cam.p(S["cast"]["putin"] + 190 * K, L["feet"] + 400 * K)
        d.rectangle([x0, y0, x1, y1], fill=(250, 248, 240), outline=INK, width=max(2, int(5 * z)))
        d.rectangle([x0, y0, x1, y0 + 26 * z], fill=(226, 222, 206))
        for c, name in TAGS:   # place cards, so nobody has to guess who the cartoons are
            x, y = cam.p(S["cast"][c], S["top"] + 62 * K)
            f = ImageFont.truetype(FONT, max(8, int(34 * z)))
            w = d.textlength(name, font=f) / 2 + 16 * z
            d.rectangle([x - w, y - 26 * z, x + w, y + 26 * z], fill=WHITE, outline=INK, width=max(2, int(4 * z)))
            d.text((x, y), name, font=f, fill=INK, anchor="mm")
        cx, cy = cam.p(S["cast"]["xi"] + 160 * K, S["top"] + 40 * K)   # the check nobody touches
        d.polygon([(cx - 40 * z, cy - 14 * z), (cx + 44 * z, cy - 20 * z), (cx + 48 * z, cy + 22 * z),
                   (cx - 38 * z, cy + 26 * z)], fill=(40, 40, 46), outline=INK)
        d.text((cx + 4 * z, cy + 2 * z), "CHECK", font=ImageFont.truetype(FONT, max(6, int(18 * z))), fill=WHITE,
               anchor="mm")
        mx, my = cam.p(S["cast"]["mb"], L["feet"] - 150 * K)   # the waiter's bow tie
        d.polygon([(mx - 34 * z, my - 16 * z), (mx, my), (mx - 34 * z, my + 16 * z)], fill=(24, 24, 28))
        d.polygon([(mx + 34 * z, my - 16 * z), (mx, my), (mx + 34 * z, my + 16 * z)], fill=(24, 24, 28))

    def sfx(fx, music, ev, lines):
        tar = H.lines_with("tariff", "trump")
        if tar:
            C2.thud(fx, tar[0]["start"] + tar[0]["dur"], 0.6)

    return dict(title="THE DINNER BILL", end=["WHO SKIPPED", "THE", "CHECK?"], seq=seq,
                headline=["TRUMP, XI & PUTIN", "SPLIT THE DINNER BILL"], target=0 if short else 62.1,
                scenes={"diner": dict(layout=diner_layout, bg=diner_bg)},
                pose_hook=pose_hook, post=post, sfx=sfx)


EPISODES = {"bill": bill, "billshort": lambda: bill(True), "t58": t58, "t58short": lambda: t58(True), "confession_nb": nobanner(confession, ["MEATBALL GOES", "TO CONFESSION"]), "confession": confession, "ozempic": ozempic, "ep6v4": ep6v4, "ep5v4": ep5v4, "ep7v4": ep7v4, "ep3": ep3, "ep4": ep4, "ep5": ep5, "ep6": ep6, "ep7": ep7, "ep8": ep8, "ep7v3": ep7v3, "ep3v3": ep3v3}


# ------------------------------------------------------------------------------------------------ engine
TARGET = 62.1   # TikTok + Shorts: a bit over a minute (Nolan 11/19: 62-66 s, never under 61)
HOLD_MAX = 0.45   # the auto-fit never stretches a reaction hold past this


def use(name, fmt="vertical"):
    """Load an episode; stretch its reaction holds so the cut lands on TARGET seconds."""
    EP.clear()
    EP.update(EPISODES[name]())
    EP["name"], EP["fmt"] = name, fmt
    C2.SEQ[:] = EP["seq"]
    H.place = lambda scene: (G["L"][scene].get("cast", {}) if scene in G.get("L", {}) else {})
    _, _, _, end = C2.build()
    # Nolan 11/19 ("too much dead air"): holds never stretch past HOLD_MAX; a short cut is padded with the
    # end card, never with dead air mid-video.
    deficit = EP.get("target", TARGET) - end
    holds = [i for i, it in enumerate(C2.SEQ) if it[0] == "hold"]
    if deficit > 0.05 and holds:
        per = deficit / len(holds)
        for i in holds:
            it = C2.SEQ[i]
            add_ = max(0.0, min(per, HOLD_MAX - it[1]))
            C2.SEQ[i] = (it[0], round(it[1] + add_, 2), it[2])
            deficit -= add_
    if deficit > 0.05:
        for i, it in enumerate(C2.SEQ):
            if it[0] == "gag" and it[1] == "end":
                C2.SEQ[i] = (it[0], it[1], round(it[2] + deficit, 2)) + it[3:]


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
    if EP.get("headline"):   # Studio 11/20 format: no opening banner; frame 1 = one clean caps headline
        hl = EP["headline"] if isinstance(EP["headline"], (list, tuple)) else [EP["headline"]]
        items = [(-1.0, EP.get("headline_t", 2.6), txt, int(big * 0.6), (252, 214, 74), INK, [-2, 2][i % 2],
                  int(i * big * 0.98)) for i, txt in enumerate(hl)]
    else:
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
