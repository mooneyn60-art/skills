#!/usr/bin/env python3
"""Cutout episode: THE COOKOUT AT THE END OF THE WORLD (script: side-hustles/channels/scripts/
cutout-ep1-cookout-end-of-world.md). Vertical 1080x1920, about 70 s, loops (the last line cuts to the first).

Built on cutout.py (paper kit, Meatball, captions, synth) and cutout2.py (SEQ build, cameras, voices, the shared
state G); nothing in those files is changed. Everything here is original: TODD, UNCLE RAY, NONNA, a TV ANCHOR,
KAREN, a CONGRESSMAN, a LOBBYIST in a dollar-bill costume, a CRYPTO BRO, and PASTOR CHAD (design from
cutout_holy.py). Two public figures appear only as plain paper caricatures with a name tag (ELON, ZUCK): no photo
likeness, generic Kokoro voices, no real quotes, no logos. Voices are plain Kokoro blends (no pitch, formant or
autotune effects). Music and sound effects are synthesized here.

  python3 tools/cutout_cookout.py --out file.mp4
  python3 tools/cutout_cookout.py --still 3 12.5 ...        (PNG frames in /dev/shm/cookout)
  python3 tools/cutout_cookout.py --timeline
  python3 tools/cutout_cookout.py --linecheck file.mp4      (per-line whisper check, as tools/linecheck.py)
  python3 tools/cutout_cookout.py --sheet file.mp4 --sheet-out sheet.jpg
"""
import argparse
import difflib
import math
import os
import re
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout as C  # noqa: E402
import cutout2 as C2  # noqa: E402
import free_voice as fv  # noqa: E402
from cutout import FONT, INK, WHITE, MOUTH, ell, strip, lumpy, paper, render_shapes, add, ks, hz  # noqa: E402
from cutout import kick, snare, strum, jingle_bar, sfx_slap, BEAT, SR, FPS, OUT_FPS  # noqa: E402
from cutout2 import paste, Cam, G  # noqa: E402

TMP = "/dev/shm/cookout"

# Voices: plain Kokoro blends, one per character (names are prefixed so the shared voice cache never collides).
fv.BLENDS.update({
    "ck-todd": [("am_eric", 0.7), ("am_puck", 0.3)],       # Todd: earnest suburban dad
    "ck-ray": [("am_onyx", 0.75), ("am_santa", 0.25)],     # Uncle Ray: deep, calm
    "ck-nonna": [("if_sara", 0.7), ("bf_isabella", 0.3)],  # Nonna: Italian grandmother
    "ck-guest2": [("am_echo", 0.6), ("am_liam", 0.4)],     # the ZUCK cutout: flat generic voice (no imitation)
    "ck-anchor": [("bm_daniel", 0.5), ("am_michael", 0.5)],  # TV anchor
    "ck-congress": [("am_santa", 0.6), ("bm_lewis", 0.4)],   # Congressman: old and booming
    "ck-chad": [("am_michael", 0.7), ("am_eric", 0.3)],    # Pastor Chad (same recipe as episode 2's "chad")
    "ck-karen": [("af_sarah", 0.6), ("af_kore", 0.4)],     # Karen (same recipe as the "karen" blend)
})
VOICES = {"todd": "kokoro:ck-todd@speed=1.02,pause=0.25", "ray": "kokoro:ck-ray@speed=0.93,pause=0.3",
          "nonna": "kokoro:ck-nonna@speed=0.92,pause=0.2", "zuck": "kokoro:ck-guest2@speed=0.82,pause=0.2",
          "anchor": "kokoro:ck-anchor@speed=1.06,pause=0.28", "chad": "kokoro:ck-chad@speed=1.02,pause=0.25",
          "karen": "kokoro:ck-karen@speed=1.06,pause=0.2", "congress": "kokoro:ck-congress@speed=0.95,pause=0.3"}

SEQ_COOK = [
    ("line", "mb", "The news says it's the end of the world. So naturally, everybody's coming to my cookout.", None,
     dict(scene="yard", cams=[(0, "med"), (9, "cu_mb")], gap=0.25)),
    ("line", "todd", "Six hours, Meatball. Low and slow.", None,
     dict(scene="smoker", cams=[(0, "cu_todd"), (3, "two")], gap=0.1)),
    ("gag", "lid", 2.7, "smoker", "cu_grill"),
    ("hold", 0.9, "smoker/cu_mb"),
    ("line", "ray", "Who brought store-bought potato salad?", None,
     dict(scene="ray", cams=[(0, "cu_ray")], gap=0.3)),
    ("gag", "hand", 1.3, "ray", "cu_elon"),
    ("gag", "point", 0.9, "ray", "cu_ray"),
    ("gag", "rocket", 3.0, "ray", "wide"),
    ("line", "nonna", "Mangia!", None, dict(scene="nonna", cams=[(0, "two")], gap=0.2)),
    ("line", "zuck", "Processing.", None, dict(scene="nonna", cams=[(0, "cu_zuck")], gap=0.5)),
    ("gag", "feed", 0.9, "nonna", "two"),
    ("gag", "bsod", 2.0, "nonna", "cu_zuck"),
    ("line", "mb", "Relatable.", None, dict(scene="nonna", cams=[(0, "cu_mb")], gap=0.45, voice="kokoro:adam-puck@speed=1.15")),   # 1.36 drops the t
    ("gag", "tvon", 0.5, "tv", "tv"),
    ("line", "anchor", "Breaking: unprecedented crisis. Again. For the fifth time today.", None,
     dict(scene="tv", cams=[(0, "tv")], gap=0.9)),
    ("gag", "walkin", 1.0, "pastor", "two"),
    ("line", "chad", "Brothers and sisters, God told me to launch JesusCoin.", None,
     dict(scene="pastor", cams=[(0, "cu_chad"), (7, "two")], gap=0.1)),
    ("gag", "chart", 3.2, "chart", "wide"),
    ("line", "chad", "God says buy the dip.", None, dict(scene="pastor", cams=[(0, "cu_chad")], gap=0.5)),
    ("gag", "grab", 1.6, "pastor", "two"),
    ("line", "karen", "I want to speak to whoever's in charge of this cookout!", None,
     dict(scene="karen", cams=[(0, "cu_karen")], gap=0.25)),
    ("line", "ray", "That's me. You reported me to HR in 2019. I got promoted.", None,
     dict(scene="karen", cams=[(0, "cu_ray"), (9, "ecu_ray")], gap=0.1)),
    ("hold", 1.0, "karen/cu_karen"),
    ("gag", "cash", 1.3, "congress", "two"),
    ("line", "congress", "I don't see color. I only see green.", None,
     dict(scene="congress", cams=[(0, "cu_congress"), (4, "two")], gap=0.1)),
    ("hold", 0.9, "congress/cu_lobby"),
    ("gag", "red", 1.7, "red", "wide"),
    ("line", "mb", "Okay, real question. If the world ends, who's got the best last meal? Comment your culture's "
                   "food. Wrong answers get roasted next episode.", None,
     dict(scene="red", cams=[(0, "cu_mb"), (13, "ecu_mb"), (17, "cu_mb")], gap=0.15)),
    ("gag", "land", 0.6, "red", "wide"),
    ("gag", "done", 1.6, "done", "cu_dog"),
    ("line", "todd", "Worth it.", None, dict(scene="done", cams=[(0, "cu_todd")], gap=0.6)),
]
TITLE = ["THE COOKOUT", "AT THE END", "OF THE WORLD"]
W, H, K, F = 1080, 1920, 1.28, 1640
LAYOUT = dict(W=W, H=H, K=K, feet=F, cap_y=1470, cap_size=84)
X = dict(yard=dict(mb=540), smoker=dict(todd=290, smoker=740, mb=-700), ray=dict(ray=300, elon=850),
         nonna=dict(nonna=320, zuck=770, mb=1560), pastor=dict(chad=340, bro=790), karen=dict(ray=300, karen=790),
         congress=dict(congress=330, lobby=775), red=dict(mb=540), done=dict(todd=470))


def cam_at(x, z, feet=1600):
    return (x, F - (feet - H / 2) / z, z)


def cams():
    c = {}
    c["yard"] = {"med": cam_at(540, 1.45, 1610), "cu_mb": cam_at(540, 2.05)}
    c["smoker"] = {"cu_todd": cam_at(X["smoker"]["todd"], 1.85), "two": cam_at(540, 1.12, 1600),
                   "cu_grill": (X["smoker"]["smoker"] - 20, F - 330 * K, 1.75), "cu_mb": cam_at(-700, 2.05)}
    c["ray"] = {"cu_ray": cam_at(315, 1.8), "cu_elon": cam_at(850, 1.85), "wide": cam_at(545, 1.0, 1560)}
    c["karen"] = {"cu_ray": cam_at(315, 1.8), "ecu_ray": cam_at(315, 2.5, 1820), "cu_karen": cam_at(790, 1.85)}
    c["nonna"] = {"two": cam_at(545, 1.3, 1610), "cu_zuck": cam_at(770, 1.85), "cu_mb": cam_at(1560, 2.05)}
    c["tv"] = {"tv": (540, 930, 1.25)}
    c["pastor"] = {"cu_chad": cam_at(340, 1.8), "two": cam_at(560, 1.22, 1610)}
    c["chart"] = {"wide": (540, 960, 1.0)}
    c["congress"] = {"cu_congress": cam_at(330, 1.85), "two": cam_at(550, 1.2, 1610), "cu_lobby": cam_at(775, 1.7)}
    c["red"] = {"wide": cam_at(540, 1.0, 1560), "cu_mb": cam_at(540, 1.75, 1690), "ecu_mb": cam_at(540, 2.4, 1900)}
    c["done"] = {"cu_dog": (X["done"]["todd"] + 150 * K, F - 300 * K, 2.3), "cu_todd": cam_at(600, 1.6)}
    return c


# ------------------------------------------------------------------------------------------------ paper helpers
@lru_cache(maxsize=64)
def font(size):
    return ImageFont.truetype(FONT, max(6, int(size)))


def rs(shapes, z, R, seed):
    """render_shapes plus text items: ("t", (x, y, text, size), colour), always on top."""
    img = render_shapes([s for s in shapes if s[0] != "t"], z, R, seed)
    d = ImageDraw.Draw(img)
    c = img.size[0] / 2
    for s in shapes:
        if s[0] == "t":
            x, y, text, size = s[1]
            d.text((c + x * z, c + y * z), text, font=font(size * z), fill=s[2], anchor="mm")
    return img


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def box(fr, cam, x0, y0, x1, y1, col, seed=1, **kw):
    paper(fr, cam.pts(rect(x0, y0, x1, y1)), col, np.random.default_rng(seed), cam.z, **kw)


def poly(fr, cam, pts, col, seed=1, **kw):
    paper(fr, cam.pts(pts), col, np.random.default_rng(seed), cam.z, **kw)


def txt(fr, cam, x, y, s, size, fill, stroke=None, sw=0.08):
    px, py = cam.p(x, y)
    ImageDraw.Draw(fr).text((px, py), s, font=font(size * cam.z), fill=fill, anchor="mm",
                            stroke_width=int(size * cam.z * sw) if stroke else 0, stroke_fill=stroke)


# ------------------------------------------------------------------------------------------------ characters
SKIN, PALE, ZPALE, RSKIN, OLIVE, CSKIN = ((236, 190, 150), (240, 204, 176), (246, 228, 212), (134, 88, 60),
                                          (222, 174, 130), (240, 180, 160))
POLO, KHAKI, HAIR_BR, GRAY, TAN, TAN_DK = ((120, 170, 220), (196, 170, 120), (104, 70, 44), (200, 200, 204),
                                           (222, 200, 150), (190, 166, 116))
GOLD, GOLD_DK, GREEN, GREEN_LT, GREEN_DK = (226, 184, 56), (186, 146, 34), (120, 170, 110), (196, 224, 186), (40, 96, 52)
BLONDE, BLONDE_DK, PINK, SUIT, HOOD, PURPLE = ((246, 214, 120), (214, 176, 80), (236, 150, 170), (70, 72, 84),
                                               (44, 44, 52), (130, 84, 190))
RED = (200, 40, 32)
GEST = [(-20, 30), (-30, 150), (-15, 100), (-120, 120), (-60, 60), (-25, 135)]

RIG = {
    "todd": dict(neck=(0, -250), sh=((-76, -232), (76, -232)), arm_len=96, arm_col=SKIN, sleeve=(POLO, 36), hand=SKIN),
    "ray": dict(neck=(-14, -292), sh=((-84, -270), (56, -270)), arm_len=92, arm_col=RSKIN, sleeve=((240, 150, 60), 38),
                hand=RSKIN, rest=(-10, 30), gest=[(-10, 60), (-30, 60), (-10, 60), (-60, 60)]),
    "nonna": dict(neck=(0, -200), sh=((-54, -186), (54, -186)), arm_len=74, arm_col=(44, 40, 46), hand=OLIVE,
                  scale=0.84),
    "elon": dict(neck=(0, -250), sh=((-70, -234), (70, -234)), arm_len=94, arm_col=PALE, sleeve=((40, 40, 46), 34),
                 hand=PALE),
    "zuck": dict(neck=(0, -246), sh=((-66, -232), (66, -232)), arm_len=92, arm_col=ZPALE,
                 sleeve=((150, 150, 158), 34), hand=ZPALE, gest=[(-12, 12)]),
    "chad": dict(neck=(0, -250), sh=((-70, -236), (70, -236)), arm_len=96, arm_col=GOLD, hand=SKIN),
    "bro": dict(neck=(0, -244), sh=((-70, -230), (70, -230)), arm_len=92, arm_col=HOOD, hand=SKIN),
    "karen": dict(neck=(0, -236), sh=((-58, -222), (58, -222)), arm_len=88, arm_col=PINK, hand=PALE,
                  gest=[(-12, 110), (-12, 95), (-12, 140), (-12, 100)]),
    "congress": dict(neck=(0, -252), sh=((-78, -236), (78, -236)), arm_len=96, arm_col=SUIT, hand=CSKIN),
    "lobby": dict(neck=(0, -206), sh=((-150, -236), (150, -236)), arm_len=80, arm_col=SUIT, hand=SKIN, rest=(-25, 25)),
}
CI = {c: i for i, c in enumerate(RIG)}
CI["mb"] = 40

try:   # Pastor Chad: the episode 2 design, straight from cutout_holy.py when it imports
    import cutout_holy as _H
    _CHAD = (_H.body_shapes("chad"), lambda lvl, blink: _H.head_shapes("chad", lvl, blink, "norm", frozenset()))
    _CHAD[1](0, False)
except Exception:   # the same shapes, kept here so this episode still renders while that file is being edited
    _H = None

    def _chad_head(lvl, blink):
        cy, s = -112, []
        s += [("e", (-100, cy, 18, 26), SKIN), ("e", (100, cy, 18, 26), SKIN), ("e", (0, cy, 100, 112), SKIN),
              ("pts", ell(0, cy - 30, 104, 92, 185, 355) + [(110, cy - 40), (60, cy - 70), (-20, cy - 60),
                                                             (-90, cy - 46)], (64, 42, 30)),
              ("pts", [(-60, cy - 112), (40, cy - 136), (110, cy - 100), (60, cy - 108), (-10, cy - 96)], (64, 42, 30)),
              ("p", strip([(-30, cy - 108), (40, cy - 124)], 6), (200, 180, 160), False)]
        for side in (-1, 1):
            ex = side * 38
            if blink:
                s.append(("p", strip([(ex - 18, cy - 12), (ex + 18, cy - 12)], 5), INK, False))
            else:
                s += [("e", (ex, cy - 14, 20, 24), WHITE), ("e", (ex, cy - 10, 8, 8), C.PUPIL, False)]
            s.append(("p", strip([(ex - 22, cy - 52 - side * 2), (ex + 20, cy - 56 + side * 2)], 8), (64, 42, 30),
                      False))
        s.append(("p", [(-8, cy + 4), (8, cy + 4), (12, cy + 30), (-12, cy + 30)], (214, 168, 130), False))
        top = cy + 48
        h = [20, 40, 60][lvl]
        s.append(("pts", [(-82, top), (82, top)] + ell(0, top, 82, h + 6, 0, 180)[1:-1], MOUTH))
        s.append(("pts", [(-80, top + 2), (80, top + 2)] + ell(0, top + 2, 80, (20 if lvl else h), 0, 180)[1:-1],
                  WHITE, False))
        for x in range(-64, 70, 16):
            s.append(("p", strip([(x, top + 3), (x, top + 14)], 2.5), (210, 210, 210), False))
        s.append(("p", strip([(100, cy), (96, cy + 50), (60, top + 6)], 5), (30, 30, 30), False))
        s.append(("e", (56, top + 6, 8, 8), (30, 30, 30), False))
        return s
    _CHAD = ([("p", [(-36, -80), (-6, -80), (-8, -12), (-34, -12)], GOLD_DK),
              ("p", [(6, -80), (36, -80), (34, -12), (8, -12)], GOLD_DK),
              ("e", (-26, -8, 30, 12), WHITE), ("e", (26, -8, 30, 12), WHITE),
              ("p", [(-72, -250), (72, -250), (86, -70), (-86, -70)], GOLD),
              ("p", [(-26, -250), (26, -250), (0, -150)], WHITE),
              ("p", [(-6, -244), (6, -244), (10, -160), (0, -150), (-10, -160)], RED),
              ("p", [(-30, -250), (-6, -250), (-36, -150)], GOLD_DK),
              ("p", [(30, -250), (6, -250), (36, -150)], GOLD_DK),
              ("p", [(40, -200), (66, -200), (64, -184), (42, -184)], RED, False)], _chad_head)


def legs(col, shoe, top=-80, w=30, sock=None):
    s = [("p", [(-w - 6, top), (-6, top), (-8, -12), (-w - 4, -12)], col),
         ("p", [(6, top), (w + 6, top), (w + 4, -12), (8, -12)], col)]
    if sock:
        s += [("p", rect(-w - 4, -40, -8, -12), sock, False), ("p", rect(8, -40, w + 4, -12), sock, False)]
    return s + [("e", (-26, -8, 31, 13), shoe), ("e", (26, -8, 31, 13), shoe)]


def nametag(x, y, name):
    return [("p", rect(x - 40, y - 26, x + 40, y + 26), WHITE), ("p", rect(x - 40, y - 26, x + 40, y - 8), RED, False),
            ("t", (x, y - 17, "HELLO", 12), WHITE), ("t", (x, y + 9, name, 26), INK)]


def body_shapes(c):
    if c == "chad":
        return _CHAD[0]
    if c == "todd":
        return legs(SKIN, (244, 244, 240), -70, 30, WHITE) + [
            ("p", [(-76, -124), (76, -124), (72, -60), (5, -60), (0, -84), (-5, -60), (-72, -60)], KHAKI),
            ("p", [(-74, -250), (74, -250), (86, -112), (-86, -112)], POLO),
            ("e", (0, -152, 92, 62), POLO, False),
            ("p", [(-22, -250), (22, -250), (0, -224)], (90, 140, 196), False),
            ("p", [(-40, -232), (40, -232), (64, -190), (70, -76), (-70, -76), (-64, -190)], WHITE),
            ("p", strip([(-40, -232), (-52, -252)], 9), WHITE, False), ("p", strip([(40, -232), (52, -252)], 9), WHITE, False),
            ("p", rect(-30, -122, 30, -88), (232, 228, 216), False),
            ("t", (0, -186, "GRILL", 30), RED), ("t", (0, -152, "SGT.", 30), RED)]
    if c == "ray":
        alum, web = (176, 180, 188), (70, 150, 110)
        return [("p", strip([(-110, 0), (40, -130)], 11), alum), ("p", strip([(110, 0), (-60, -130)], 11), alum),
                ("p", strip([(-66, -110), (-126, -372)], 12), alum),
                ("p", [(-128, -366), (-72, -366), (-28, -122), (-88, -122)], web),
                ("p", [(-122, -330), (-66, -330), (-60, -300), (-116, -300)], WHITE, False),
                ("p", [(-108, -250), (-52, -250), (-46, -220), (-102, -220)], WHITE, False),
                ("p", rect(-96, -130, 128, -108), web),
                ("p", strip([(-30, -196), (140, -196)], 10), alum),
                # legs: thighs forward, shins down, sandals
                ("p", rect(-20, -168, 130, -122), (60, 90, 150)), ("p", rect(86, -130, 128, -92), (60, 90, 150), False),
                ("p", rect(92, -96, 124, -16), RSKIN), ("e", (116, -8, 38, 13), (90, 60, 40)),
                ("p", strip([(96, -20), (134, -14)], 7), (40, 30, 26), False),
                # shirt: orange with paper leaves
                ("p", [(-90, -290), (60, -290), (56, -130), (-66, -130)], (240, 150, 60)),
                ("e", (-10, -180, 76, 62), (240, 150, 60), False),
                ("p", [(-36, -290), (8, -290), (-14, -252)], RSKIN, False),
                ("e", (-50, -230, 14, 8, 0, 360, None, 30), (60, 150, 90), False),
                ("e", (20, -210, 14, 8, 0, 360, None, -30), (250, 230, 120), False),
                ("e", (-30, -168, 14, 8, 0, 360, None, -20), (250, 230, 120), False),
                ("e", (30, -156, 14, 8, 0, 360, None, 40), (60, 150, 90), False),
                ("e", (-64, -180, 12, 7, 0, 360, None, 60), (60, 150, 90), False)]
    if c == "nonna":
        return legs((150, 110, 86), (40, 36, 40), -44, 24) + [
            ("p", [(-58, -204), (58, -204), (90, -34), (-90, -34)], (44, 40, 46)),
            ("p", [(-34, -196), (34, -196), (40, -150), (-40, -150)], WHITE),
            ("p", [(-44, -152), (44, -152), (62, -46), (-62, -46)], WHITE),
            ("p", rect(-22, -120, 0, -98), RED, False), ("p", rect(0, -98, 22, -76), RED, False),
            ("p", rect(-22, -76, 0, -54), RED, False), ("p", rect(22, -120, 44, -98), RED, False),
            ("p", rect(-44, -98, -22, -76), RED, False),
            ("p", strip([(-60, -150), (60, -150)], 9), (232, 228, 216), False)]
    if c == "elon":
        return legs((50, 56, 84), (30, 30, 34)) + [
            ("p", [(-68, -250), (68, -250), (78, -76), (-78, -76)], (40, 40, 46)),
            ("p", [(-20, -250), (20, -250), (0, -228)], PALE, False),
            ("p", [(-34, -130), (-22, -168), (-10, -130)], (236, 236, 240), False),      # a paper rocket doodle
            ("p", rect(-30, -132, -14, -112), (236, 236, 240), False),
            ("p", [(-30, -112), (-22, -98), (-14, -112)], (240, 150, 60), False)] + nametag(32, -196, "ELON")
    if c == "zuck":
        return legs((70, 84, 124), (236, 236, 228)) + [
            ("p", [(-64, -246), (64, -246), (74, -76), (-74, -76)], (150, 150, 158)),
            ("p", [(-22, -246), (22, -246), (0, -230)], ZPALE, False)] + nametag(30, -194, "ZUCK")
    if c == "bro":
        return legs(SKIN, (60, 60, 70), -70, 30, WHITE) + [
            ("p", [(-70, -124), (70, -124), (68, -62), (5, -62), (0, -84), (-5, -62), (-68, -62)], (120, 124, 136)),
            ("p", [(-68, -244), (68, -244), (82, -104), (-82, -104)], HOOD),
            ("p", [(-46, -150), (46, -150), (54, -112), (-54, -112)], (60, 60, 70), False),
            ("p", strip([(-14, -238), (-18, -196)], 5), WHITE, False), ("p", strip([(14, -238), (18, -196)], 5), WHITE, False),
            ("p", strip([(-30, -240), (0, -200), (30, -240)], 5), GOLD, False), ("e", (0, -196, 12, 12), GOLD, False),
            ("t", (0, -168, "2 THE MOON", 19), (250, 220, 80))]
    if c == "karen":
        return legs(PALE, (190, 150, 110), -50, 24) + [
            ("p", [(-52, -130), (52, -130), (40, -46), (4, -46), (0, -70), (-4, -46), (-40, -46)], (250, 248, 240)),
            ("p", [(-56, -236), (56, -236), (64, -116), (-64, -116)], WHITE),
            ("p", [(-58, -236), (-16, -236), (-26, -110), (-70, -110)], PINK),
            ("p", [(16, -236), (58, -236), (70, -110), (26, -110)], PINK),
            ("e", (-8, -222, 5, 5), (250, 250, 250), False), ("e", (8, -222, 5, 5), (250, 250, 250), False),
            ("e", (0, -218, 5, 5), (250, 250, 250), False)]
    if c == "congress":
        return legs(SUIT, (30, 30, 34)) + [
            ("p", [(-80, -252), (80, -252), (92, -74), (-92, -74)], SUIT),
            ("e", (0, -140, 96, 70), SUIT, False),
            ("p", [(-28, -252), (28, -252), (0, -130)], WHITE),
            ("p", [(-8, -246), (8, -246), (12, -136), (0, -120), (-12, -136)], RED),
            ("p", [(-34, -252), (-8, -252), (-40, -150)], (54, 56, 66)),
            ("p", [(34, -252), (8, -252), (40, -150)], (54, 56, 66)),
            ("e", (-50, -204, 7, 7), GOLD, False)]
    if c == "lobby":
        s = legs(SUIT, (30, 30, 34), -84, 30) + [
            ("p", rect(-156, -346, 156, -72), GREEN), ("p", rect(-142, -332, 142, -86), GREEN_LT, False),
            ("p", rect(-130, -320, 130, -98), (140, 186, 128), False),
            ("e", (0, -206, 80, 92), GREEN_LT, False)]
        for sx in (-1, 1):
            for y in (-296, -122):
                s.append(("t", (sx * 104, y, "$", 44), GREEN_DK))
        return s + [("t", (0, -318, "LOBBY", 26), GREEN_DK), ("t", (0, -100, "100% LEGAL", 20), GREEN_DK)]
    raise KeyError(c)


def head_shapes(c, lvl, blink, expr, gaze, flags):
    s = []
    if c == "chad":
        return _CHAD[1](lvl, blink)
    if c == "todd":
        cy = -108
        s += [("e", (-98, cy + 4, 16, 24), SKIN), ("e", (98, cy + 4, 16, 24), SKIN), ("e", (0, cy, 98, 104), SKIN),
              ("pts", ell(0, cy - 34, 100, 78, 182, 358) + [(98, cy - 40), (30, cy - 66), (-50, cy - 52), (-98, cy - 36)],
               HAIR_BR),
              ("p", strip([(-50, cy - 92), (30, cy - 104)], 5), (150, 110, 80), False)]
        s += C.eyes(0, cy - 6, 37, 21, 24, gaze, "norm", 1.0 if blink else 0.0, SKIN, 10 if expr == "proud" else 5,
                    HAIR_BR)
        for sd in (-1, 1):
            s.append(("pts", strip(ell(sd * 37, cy - 6, 31, 32), 5), (60, 60, 70), False))
            s.append(("p", strip([(sd * 66, cy - 10), (sd * 98, cy - 16)], 5), (60, 60, 70), False))
        s += [("p", strip([(-8, cy - 8), (8, cy - 8)], 5), (60, 60, 70), False),
              ("e", (0, cy + 24, 12, 10), (220, 170, 130), False)]
        s += C.mouth(0, cy + 64, lvl, 34, "smirk" if expr == "proud" else "flat", "grin")
        s.append(("pts", strip([(-42, cy + 50), (-20, cy + 38), (0, cy + 42), (20, cy + 38), (42, cy + 50)], 13), HAIR_BR))
        return s
    if c == "ray":
        cy = -104
        s += [("e", (-94, cy + 4, 14, 22), RSKIN), ("e", (94, cy + 4, 14, 22), RSKIN), ("e", (0, cy, 94, 100), RSKIN),
              ("pts", ell(0, cy + 6, 97, 98, 0, 180) + ell(0, cy + 2, 64, 40, 0, 180)[::-1], GRAY)]
        s += C.mouth(0, cy + 52, lvl, 26, "flat", "oval")
        s += [("pts", strip([(-36, cy + 40), (0, cy + 30), (36, cy + 40)], 13), GRAY),
              ("e", (0, cy + 18, 15, 11), (112, 70, 46), False)]
        for sd in (-1, 1):
            s += [("e", (sd * 40, cy - 12, 37, 27), (22, 22, 26)), ("e", (sd * 40 - 12, cy - 22, 10, 5), (120, 120, 140), False)]
        s += [("p", strip([(-6, cy - 14), (6, cy - 14)], 6), (22, 22, 26), False),
              ("pts", ell(0, cy - 56, 94, 84, 180, 360) + [(94, cy - 52), (-94, cy - 52)], TAN),
              ("p", [(-134, cy - 58), (134, cy - 58), (120, cy - 34), (-120, cy - 34)], TAN_DK),
              ("p", rect(-94, cy - 78, 94, cy - 62), (60, 90, 150), False)]
        return s
    if c == "nonna":
        cy = -92
        s += [("e", (0, cy - 108, 38, 32), GRAY), ("e", (0, cy - 10, 96, 94), GRAY), ("e", (0, cy + 4, 84, 86), OLIVE),
              ("pts", ell(0, cy - 14, 90, 76, 180, 360) + [(86, cy - 6), (30, cy - 44), (-30, cy - 44), (-86, cy - 6)], GRAY),
              ("e", (-88, cy + 32, 7, 9), GOLD, False), ("e", (88, cy + 32, 7, 9), GOLD, False),
              ("e", (-48, cy + 38, 14, 9), (230, 150, 130), False), ("e", (48, cy + 38, 14, 9), (230, 150, 130), False)]
        s += C.eyes(0, cy + 2, 28, 18, 20, gaze, "norm", 1.0 if blink else 0.25, OLIVE, -14, (110, 110, 116))
        s.append(("e", (0, cy + 26, 15, 19), (200, 150, 108), False))
        s += C.mouth(0, cy + 60, lvl, 30, "frown", "dent")
        return s
    if c == "elon":
        cy, hair = -110, (60, 44, 36)
        s += [("e", (-98, cy + 4, 15, 24), PALE), ("e", (98, cy + 4, 15, 24), PALE), ("e", (0, cy, 98, 108), PALE),
              ("pts", ell(0, cy - 36, 100, 78, 182, 358) + [(100, cy - 34), (50, cy - 62), (-30, cy - 50), (-96, cy - 40)], hair),
              ("pts", [(-70, cy - 100), (20, cy - 130), (98, cy - 96), (40, cy - 104), (-20, cy - 92)], hair)]
        s += C.eyes(0, cy - 4, 34, 20, 22, gaze, "norm", 1.0 if blink else 0.35, PALE, -4, hair)
        s.append(("e", (0, cy + 24, 11, 10), (220, 180, 150), False))
        s += C.mouth(6, cy + 60, lvl, 32, "smirk", "grin")
        return s
    if c == "zuck":
        cy, hair = -108, (150, 110, 70)
        s += [("e", (-90, cy + 4, 15, 26), ZPALE), ("e", (90, cy + 4, 15, 26), ZPALE), ("e", (0, cy, 90, 108), ZPALE)]
        if "full" in flags:
            s += [("e", (-66, cy + 44, 34, 30), ZPALE), ("e", (66, cy + 44, 34, 30), ZPALE)]
        s.append(("pts", ell(0, cy - 30, 93, 84, 180, 360) + [(93, cy - 46), (-93, cy - 46)], hair))
        for x in range(-78, 80, 26):
            s.append(("pts", lumpy(x, cy - 104 + abs(x) * 0.34, 17, [(3, 5, x)]), hair, False))
        if "bsod" in flags:
            s += [("p", rect(-76, cy - 44, 76, cy + 88), (30, 90, 220)), ("t", (-34, cy + 2, ":(", 66), WHITE),
                  ("t", (0, cy + 50, "TASTE.EXE", 20), WHITE), ("t", (0, cy + 72, "NOT FOUND", 20), WHITE)]
            return s
        s += C.eyes(0, cy - 2, 34, 26, 28, "c", "wide", 0.0, ZPALE, None, None)
        s.append(("e", (0, cy + 28, 9, 9), (226, 200, 180), False))
        s += C.mouth(0, cy + 62, 0 if "full" in flags else lvl, 26, "flat", "slot")
        return s
    if c == "bro":
        cy = -106
        s += [("e", (-92, cy + 4, 14, 22), SKIN), ("e", (92, cy + 4, 14, 22), SKIN), ("e", (0, cy, 92, 100), SKIN)]
        for (x, y) in [(-44, 62), (-28, 74), (-10, 80), (10, 80), (28, 74), (44, 62), (-56, 48), (56, 48)]:
            s.append(("e", (x, cy + y, 3, 3), (150, 110, 80), False))
        s += [("pts", ell(0, cy - 50, 96, 78, 180, 360) + [(96, cy - 44), (-96, cy - 44)], PURPLE),
              ("pts", ell(0, cy - 46, 34, 28, 180, 360), SKIN, False),
              ("p", strip([(-34, cy - 47), (34, cy - 47)], 7), (100, 60, 150), False),
              ("p", [(-86, cy - 24), (86, cy - 24), (76, cy + 12), (12, cy + 6), (-12, cy + 6), (-76, cy + 12)], (28, 28, 34)),
              ("p", strip([(-70, cy - 14), (-40, cy - 16)], 5), (150, 220, 250), False)]
        if "sad" in flags:
            s += C.mouth(0, cy + 58, 1, 30, "frown", "oval")
            s += [("e", (-52, cy + 28, 8, 13), (120, 190, 240), False), ("e", (56, cy + 40, 8, 13), (120, 190, 240), False)]
        else:
            s += C.mouth(4, cy + 56, lvl, 34, "smirk", "grin")
        return s
    if c == "karen":
        cy = -104
        s += [("pts", [(-110, cy + 84), (-120, cy - 40), (-84, cy - 112), (-10, cy - 136), (62, cy - 122), (106, cy - 70),
                       (102, cy + 2), (60, cy - 20), (-60, cy - 20), (-70, cy + 78)], BLONDE),
              ("pts", [(40, cy - 126), (80, cy - 150), (72, cy - 110)], BLONDE),
              ("pts", [(70, cy - 112), (116, cy - 124), (100, cy - 84)], BLONDE),
              ("e", (0, cy, 90, 98), PALE),
              ("pts", [(-96, cy + 30), (-100, cy - 40), (-50, cy - 100), (30, cy - 104), (94, cy - 56), (40, cy - 66),
                       (-30, cy - 50), (-66, cy - 10), (-74, cy + 40)], BLONDE),
              ("p", strip([(-88, cy + 20), (-84, cy - 40), (-40, cy - 84)], 7), BLONDE_DK, False),
              ("p", strip([(-10, cy - 84), (50, cy - 80)], 6), BLONDE_DK, False),
              ("e", (92, cy + 30, 7, 7), WHITE, False)]
        wide = expr == "wide"
        s += C.eyes(0, cy + 2, 32, 20, 22, gaze, "wide" if wide else "norm", 1.0 if blink else (0.0 if wide else 0.3),
                    PALE, 20 if wide else -16, (150, 110, 50))
        s.append(("e", (0, cy + 28, 9, 9), (220, 180, 150), False))
        s += C.mouth(0, cy + 62, lvl, 32, "frown", "big")
        return s
    if c == "congress":
        cy, wh = -110, (236, 236, 232)
        s += [("pts", lumpy(-94, cy - 16, 34, [(4, 5, 0)]), wh), ("pts", lumpy(94, cy - 16, 34, [(4, 5, 1)]), wh),
              ("e", (0, cy + 46, 106, 66), CSKIN), ("e", (0, cy, 98, 102), CSKIN),
              ("pts", ell(0, cy - 44, 96, 60, 185, 355) + [(94, cy - 52), (0, cy - 76), (-94, cy - 52)], wh)]
        s += C.eyes(0, cy - 6, 36, 18, 20, gaze, "norm", 1.0 if blink else 0.4, CSKIN, -6, wh)
        s.append(("e", (0, cy + 22, 18, 16), (226, 140, 120), False))
        s += C.mouth(0, cy + 64, lvl, 40, "smirk", "grin")
        return s
    if c == "lobby":
        hair = (30, 26, 26)
        s += [("e", (0, 0, 56, 62), SKIN),
              ("pts", ell(0, -18, 58, 50, 180, 360) + [(58, -16), (0, -36), (-58, -16)], hair)]
        if "dollar" in flags:
            for sd in (-1, 1):
                s += [("e", (sd * 21, -2, 15, 17), WHITE), ("t", (sd * 21, -2, "$", 26), GREEN_DK)]
        else:
            s += C.eyes(0, -2, 21, 14, 16, gaze, "norm", 1.0 if blink else 0.35, SKIN, -4, hair)
        s += C.mouth(2, 34, lvl, 20, "smirk", "grin")
        return s
    raise KeyError(c)


def arm_shapes(c):
    k = RIG[c]
    Ln = k["arm_len"]
    s = [("p", [(-13, -6), (13, -6), (14, Ln), (-14, Ln)], k["arm_col"])]
    if k.get("sleeve"):
        col, sl = k["sleeve"]
        s.append(("p", [(-16, -8), (16, -8), (17, sl), (-17, sl)], col, False))
    return s + [("e", (0, Ln + 15, 23, 21), k["hand"]), ("e", (18, Ln + 5, 9, 12, 0, 360, None, -30), k["hand"])]


@lru_cache(maxsize=1024)
def rspr(c, part, z, *key):
    if part == "body":
        return rs(body_shapes(c), z, 400, 500 + CI[c])
    if part == "arm":
        return rs(arm_shapes(c), z, 140, 520 + CI[c])
    return rs(head_shapes(c, *key), z, 330, 540 + CI[c])


# ------------------------------------------------------------------------------------------------ props
MEAT, MEAT_DK, SAUCE = C.MEAT, C.MEAT_DK, C.SAUCE
STEEL, STEEL_DK, CHAR = (56, 56, 62), (40, 40, 46), (30, 28, 30)


def dog_shapes(x, y, s, charred=False):
    col = (120, 56, 40) if charred else (206, 96, 70)
    out = [("e", (x, y, 60 * s, 13 * s), col)]
    for k in (-1, 0, 1):
        out.append(("p", strip([(x + k * 26 * s - 5 * s, y - 9 * s), (x + k * 26 * s + 5 * s, y + 9 * s)], 4 * s),
                    (60, 30, 24) if charred else (150, 60, 44), False))
    return out


@lru_cache(maxsize=512)
def prop(name, z, *key):
    if name == "plate":   # Meatball's paper plate: chips and a pickle
        return rs([("e", (0, 0, 74, 20), WHITE), ("e", (0, -2, 56, 13), (232, 230, 220), False),
                   ("p", [(-40, -6), (-10, -26), (-4, -4)], (246, 206, 90)), ("p", [(-16, -4), (10, -30), (24, -6)], (240, 190, 70)),
                   ("e", (34, -10, 20, 8, 0, 360, None, -20), (110, 160, 70))], z, 90, 600)
    if name == "plate_balls":
        s = [("e", (0, 0, 80, 22), WHITE), ("e", (0, -2, 60, 14), (232, 230, 220), False),
             ("e", (0, -8, 54, 12), (236, 214, 150), False)]
        for i, x in enumerate((-30, 30, 0)[:key[0]]):
            s += [("pts", lumpy(x, -22 - (16 if x == 0 else 0), 24, [(3, 5, i)]), MEAT),
                  ("pts", ell(x, -26 - (16 if x == 0 else 0), 24, 22, 200, 340), SAUCE, False)]
        return rs(s, z, 100, 601)
    if name == "meatball":
        return rs([("pts", lumpy(0, 0, 26, [(3, 5, 0)]), MEAT), ("pts", ell(0, -4, 26, 24, 200, 340), SAUCE, False),
                   ("e", (8, 10, 5, 4), MEAT_DK, False)], z, 40, 602)
    if name == "spoon":
        return rs([("p", strip([(0, 30), (0, -110)], 11), (190, 140, 84)), ("e", (0, -132, 22, 30), (190, 140, 84)),
                   ("e", (0, -132, 13, 20), (160, 112, 64), False)], z, 180, 603)
    if name == "spatula":
        return rs([("p", strip([(0, 30), (0, -90)], 9), (60, 60, 66)), ("p", rect(-24, -150, 24, -88), (190, 194, 200)),
                   ("p", strip([(-12, -140), (-12, -100)], 4), (120, 120, 130), False),
                   ("p", strip([(12, -140), (12, -100)], 4), (120, 120, 130), False)], z, 170, 604)
    if name == "can":
        return rs([("p", rect(-15, -30, 15, 26), (60, 130, 200)), ("p", rect(-15, -10, 15, 6), WHITE, False),
                   ("p", rect(-13, -36, 13, -30), (190, 194, 200), False)], z, 50, 605)
    if name == "tub":
        return rs([("p", [(-64, -54), (64, -54), (54, 40), (-54, 40)], (238, 228, 190)),
                   ("p", rect(-70, -68, 70, -50), RED), ("p", rect(-50, -34, 50, 14), WHITE, False),
                   ("t", (0, -20, "POTATO", 20), INK), ("t", (0, 2, "SALAD", 20), INK),
                   ("e", (40, 28, 26, 16), (250, 220, 60)), ("t", (40, 28, "$3.99", 13), RED)], z, 100, 606)
    if name == "smoker":   # key: open
        s = [("p", strip([(-150, -200), (-190, 0)], 14), STEEL_DK), ("p", strip([(150, -200), (190, 0)], 14), STEEL_DK),
             ("p", strip([(-180, -60), (180, -60)], 10), STEEL_DK),
             ("e", (-190, -6, 30, 30), CHAR), ("e", (-190, -6, 10, 10), (150, 150, 160), False),
             ("p", rect(170, -540, 214, -330), STEEL_DK), ("p", rect(160, -560, 224, -536), CHAR),
             ("p", rect(-300, -330, -200, -230), STEEL_DK), ("p", rect(-286, -300, -240, -260), (240, 130, 40), False),
             ("p", rect(196, -312, 330, -296), (150, 104, 64)),
             ("e", (0, -300, 210, 126), STEEL)]
        if key[0]:
            s += [("e", (0, -316, 196, 62), (24, 22, 24), False), ("e", (0, -306, 186, 52), (92, 92, 100), False)]
            for x in range(-160, 170, 32):
                hh = 52 * math.sqrt(max(0, 1 - (x / 186) ** 2))
                s.append(("p", strip([(x, -306 - hh), (x, -306 + hh)], 5), (40, 40, 46), False))
            s += dog_shapes(0, -306, 0.42)
        return rs(s, z, 600, 607)
    if name == "lid":   # hinge at the origin, the lid runs to +x
        return rs([("pts", ell(210, 0, 210, 126, 180, 360) + [(420, 0), (0, 0)], (66, 66, 74)),
                   ("p", strip([(160, -124), (160, -150), (260, -150), (260, -124)], 9), (150, 104, 64)),
                   ("e", (90, -70, 22, 22), WHITE), ("p", strip([(90, -70), (104, -82)], 4), RED, False)], z, 460, 608)
    if name == "smoke":
        return rs([("pts", lumpy(0, 0, 34, [(5, 4, key[0]), (3, 7, 1)]), (232, 232, 236))], z, 50, 609 + key[0])
    if name == "rocket":
        return rs([("p", [(-96, -90), (-170, -10), (-96, -250)], RED), ("p", [(96, -90), (170, -10), (96, -250)], RED),
                   ("p", rect(-96, -520, 96, -60), (244, 244, 240)),
                   ("p", [(-96, -520), (96, -520), (0, -700)], RED),
                   ("p", rect(-96, -110, 96, -60), (150, 150, 160), False),
                   ("e", (0, -390, 70, 70), (60, 60, 70)), ("e", (0, -390, 58, 58), (150, 210, 240), False),
                   ("p", rect(-70, -250, 70, -180), WHITE, False), ("t", (0, -214, "BYE", 54), RED),
                   ("p", [(-40, -60), (40, -60), (56, -20), (-56, -20)], STEEL_DK)], z, 720, 620)
    if name == "flame":
        k = key[0]
        return rs([("p", [(-56, 0), (56, 0), (30 - k * 20, 150), (0, 250 + k * 60), (-30 + k * 16, 140)], (240, 130, 40)),
                   ("p", [(-30, 0), (30, 0), (10, 90), (0, 150 + k * 30), (-14, 80)], (252, 220, 80), False)], z, 330, 621 + k)
    if name == "fire":   # small flames, pointing up (toaster, meteor)
        k = key[0]
        return rs([("p", [(-50, 0), (-60, -50 - k * 20), (-30, -30), (-16, -100 + k * 20), (4, -44), (26, -90 - k * 16),
                          (36, -30), (58, -60 + k * 20), (50, 0)], (240, 110, 30)),
                   ("p", [(-28, 0), (-30, -30), (-12, -18), (0, -60 - k * 10), (14, -22), (30, -40), (28, 0)],
                    (252, 220, 80), False)], z, 120, 623 + k)
    if name == "toaster":
        return rs([("p", rect(-56, -40, -30, -6), (214, 160, 90)), ("p", rect(-8, -52, 20, -6), (214, 160, 90)),
                   ("p", [(-70, 0), (70, 0), (78, 80), (-78, 80)], (200, 204, 212)),
                   ("p", rect(-60, 4, -24, 12), CHAR, False), ("p", rect(-12, 4, 26, 12), CHAR, False),
                   ("p", rect(78, 20, 92, 34), CHAR), ("p", rect(-84, 80, 84, 92), STEEL_DK)], z, 120, 625)
    if name == "coin":   # JesusCoin: a paper coin with a halo (key: halo)
        s = [("e", (0, 0, 44, 44), GOLD_DK), ("e", (0, 0, 35, 35), GOLD, False), ("t", (0, 1, "JC", 34), (130, 96, 20))]
        if key and key[0]:
            s = [("pts", strip(ell(0, -58, 34, 10), 7), (252, 236, 130))] + s
        return rs(s, z, 80, 626)
    if name == "cplate":   # the collection plate
        return rs([("p", [(-30, -8), (-10, -50), (14, -44), (0, -4)], (120, 180, 110)),
                   ("p", [(-4, -6), (16, -56), (40, -46), (26, -4)], (140, 196, 126)),
                   ("p", [(-52, -6), (-40, -40), (-18, -32), (-28, -2)], (140, 196, 126)),
                   ("pts", ell(0, 0, 76, 24, 0, 180) + [(-76, 0)], GOLD_DK), ("e", (0, 0, 76, 10), (150, 30, 40), False)],
                  z, 100, 627)
    if name == "cash":
        return rs([("p", rect(-40, -22, 40, 22), (120, 180, 110)), ("p", rect(-12, -22, 12, 22), (236, 232, 210), False),
                   ("t", (-26, 0, "$", 26), GREEN_DK), ("t", (26, 0, "$", 26), GREEN_DK)], z, 60, 628)
    if name == "bill":
        return rs([("p", rect(-26, -13, 26, 13), (140, 196, 126)), ("t", (0, 0, "$", 18), GREEN_DK)], z, 40, 629)
    if name == "clipboard":
        return rs([("p", rect(-40, -56, 40, 56), (150, 104, 64)), ("p", rect(-32, -44, 32, 48), WHITE, False),
                   ("p", rect(-18, -64, 18, -46), (170, 174, 184)),
                   ("p", strip([(-22, -24), (22, -24)], 4), (120, 120, 130), False),
                   ("p", strip([(-22, -6), (22, -6)], 4), (120, 120, 130), False),
                   ("p", strip([(-22, 12), (10, 12)], 4), RED, False)], z, 80, 630)
    if name == "phone":
        return rs([("p", rect(-18, -40, 18, 40), (40, 40, 46)), ("p", rect(-13, -32, 13, 28), (240, 90, 80), False)],
                  z, 60, 631)
    if name == "meteor":   # a ball of fire with a tail up and to the right
        return rs([("p", [(-60, -70), (300, -420), (90, 40)], (240, 110, 30)),
                   ("p", [(-30, -60), (200, -300), (60, 10)], (252, 200, 70), False),
                   ("pts", lumpy(0, 0, 96, [(8, 5, 0), (5, 9, 1)]), (240, 110, 30)),
                   ("pts", lumpy(-6, 6, 64, [(5, 6, 2)]), (252, 220, 80), False)], z, 460, 632)
    if name == "dogplate":   # the hot dog, finally done, on a bun
        s = [("e", (0, 30, 150, 30), WHITE), ("e", (0, 26, 120, 20), (232, 230, 220), False),
             ("e", (0, 6, 118, 34), (226, 180, 110))]
        s += dog_shapes(0, -12, 2.2, True)
        s += [("p", strip([(-100 + i * 25, -12 + (8 if i % 2 else -8)) for i in range(9)], 8), (250, 210, 50), False),
              ("pts", ell(0, 6, 118, 34, 20, 160) + [(-110, 4)], (236, 194, 124), False)]
        return rs(s, z, 170, 633)
    if name == "steam":
        k = key[0]
        return rs([("p", strip([(0, 0), (12 - k * 24, -30), (-12 + k * 24, -60), (10 - k * 20, -90)], 9), (250, 250, 250), False)],
                  z, 110, 634 + k)
    if name == "table":
        wood = (170, 96, 60)
        return rs([("p", strip([(-300, 0), (-200, -230)], 22), (130, 72, 44)), ("p", strip([(300, 0), (200, -230)], 22), (130, 72, 44)),
                   ("p", rect(-470, -130, 470, -104), wood), ("p", rect(-400, -250, 400, -216), wood)], z, 500, 636)
    if name == "twinkle":
        return rs([("pts", [(0, -40), (8, -8), (40, 0), (8, 8), (0, 40), (-8, 8), (-40, 0), (-8, -8)], (255, 250, 220), False)],
                  z, 50, 637)
    if name == "dust":
        return rs([("pts", lumpy(0, 0, 60, [(10, 6, key[0]), (5, 9, 1)]), (226, 214, 190))], z, 90, 638 + key[0])
    if name == "anchor":   # head and shoulders for the TV (key: lvl, blink)
        lvl, blink = key
        hair, skin, cy = (112, 100, 96), (226, 172, 126), -230
        s = [("p", [(-170, 0), (170, 0), (130, -124), (-130, -124)], (40, 54, 92)),
             ("p", [(-40, -124), (40, -124), (0, -30)], WHITE), ("p", [(-10, -118), (10, -118), (14, -40), (0, -26), (-14, -40)], RED),
             ("p", [(-50, -128), (-12, -128), (-46, -40)], (54, 70, 112)), ("p", [(50, -128), (12, -128), (46, -40)], (54, 70, 112)),
             ("pts", lumpy(0, cy - 26, 108, [(4, 5, 0)]), hair), ("e", (0, cy + 8, 84, 94), skin),
             ("pts", ell(0, cy - 28, 90, 70, 180, 360) + [(90, cy - 26), (20, cy - 58), (-90, cy - 20)], hair)]
        s += C.eyes(0, cy + 2, 30, 18, 20, "c", "norm", 1.0 if blink else 0.2, skin, -8, (70, 60, 56))
        s.append(("e", (0, cy + 28, 10, 10), (206, 150, 106), False))
        s += C.mouth(0, cy + 62, lvl, 30, "flat", "dent")
        return rs(s, z, 380, 640)
    raise KeyError(name)


# ------------------------------------------------------------------------------------------------ rig drawing
def compose(c, z, p, jx, jy):
    k = RIG[c]
    S = int(2 * 600 * z)
    im = Image.new("RGBA", (S, S))
    o = S / 2
    paste(im, rspr(c, "body", z), o, o)
    held = []
    for (sx, sy), a, side in zip(k["sh"], (p["aL"], p["aR"]), "LR"):
        paste(im, rspr(c, "arm", z), o + sx * z, o + sy * z, a)
        for it in p["items"]:
            if it[1] == side:
                Ln = k["arm_len"] + 18
                held.append((it, o + (sx + Ln * math.sin(math.radians(a))) * z, o + (sy + Ln * math.cos(math.radians(a))) * z))
    hk = (p["lvl"], p["blink"], p["expr"], p["gaze"], frozenset(p["flags"]))
    paste(im, rspr(c, "head", z, *hk), o + (k["neck"][0] + jx) * z, o + (k["neck"][1] + jy) * z, p["ang"])
    for it, hx, hy in held:
        paste(im, prop(it[0], z, *it[3:]), hx, hy, it[2])
    return im


def state(c, st):
    """(speaking, mouth level, word index) for character c at this frame."""
    t, fi, li = st
    ln = G["lines"][li] if li is not None else None
    if ln is None or ln["who"] != c or ln["scene"] != G["scene"]:
        return False, 0, 0
    wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
    return True, C2.mouth_level(ln, t), wi


def rig(fr, cam, c, x, st, y=None, **ov):
    t, fi, li = st
    k = RIG[c]
    px = cam.p(x, 0)[0]
    if px < -420 * cam.z or px > W + 420 * cam.z:
        return
    rng = np.random.default_rng(fi * 31 + CI[c])
    spk, lvl, wi = state(c, st)
    aL, aR = k.get("rest", (-12, 12))
    hop, ang, jit = 0.0, float(rng.uniform(-1, 1)), 1.0
    if spk:
        ln = G["lines"][li]
        if t - ln["words"][wi][0] < 0.09 and t >= ln["start"]:
            hop = -10
        g = k.get("gest", GEST)
        aL, aR = g[(wi * 7 + li) % len(g)]
        ang, jit = float(rng.uniform(-3.5, 3.5)), 1.6
    p = dict(lvl=lvl, hop=hop, ang=ang, aL=aL, aR=aR, blink=(fi + CI[c] * 7) % 41 == 0, expr="norm", gaze="c",
             flags=(), items=(), rot=0.0, jit=jit, scale=1.0)
    p.update(ov)
    jx, jy = (float(v) for v in rng.uniform(-p["jit"], p["jit"], 2))
    z = round(cam.z * K * k.get("scale", 1.0) * p["scale"], 3)
    im = compose(c, z, p, jx, jy)
    if p["rot"]:
        im = im.rotate(p["rot"], resample=Image.BICUBIC)
    qx, qy = cam.p(x, (F if y is None else y) + p["hop"] * K)
    paste(fr, im, qx, qy)


def meat(fr, cam, x, st, y=None, expr="norm", gaze="c", plate=True, arms=None, hop=None):
    t, fi, li = st
    if not -400 * cam.z < cam.p(x, 0)[0] < W + 400 * cam.z:
        return
    rng = np.random.default_rng(fi * 31 + 40)
    spk, lvl, wi = state("mb", st)
    aL, aR, h, ang, jit = -12.0, 12.0, 0.0, float(rng.uniform(-1, 1)), 1.2
    if spk:
        ln = G["lines"][li]
        if t - ln["words"][wi][0] < 0.09 and t >= ln["start"]:
            h = -10
        aL, aR = [(-20, 30), (-30, 150), (-120, 100), (-60, 60), (-150, 135), (-25, 100)][(wi * 7 + li) % 6]
        ang, jit = float(rng.uniform(-3.5, 3.5)), 1.9
    if plate:
        aR = 76
    if arms:
        aL, aR = arms
    if hop is not None:
        h = hop
    y = F if y is None else y
    pose = (h, (float(rng.uniform(-jit, jit)), float(rng.uniform(-jit, jit))), ang, (aL, aR),
            (lvl, gaze, (fi + 11) % 41 == 0, expr), 1.0, 0.0, {})
    C2.draw_kid(fr, cam, "mb", x, y, pose)
    if plate:
        a = math.radians(aR)
        paste(fr, prop("plate", round(cam.z * K, 3)),
              *cam.p(x + (60 + 86 * math.sin(a)) * K, y + (-170 + 86 * math.cos(a) + h - 6) * K))


def P(fr, cam, name, x, y, ang=0.0, scale=1.0, key=()):
    paste(fr, prop(name, round(cam.z * K * scale, 3), *key), *cam.p(x, y), ang)


# ------------------------------------------------------------------------------------------------ backgrounds
def tint(col, red):
    if not red:
        return col
    return tuple(int(c * 0.5 + r * 0.5) for c, r in zip(col, (150, 36, 28)))


def bg_yard(cam, scene):
    red = scene == "red"
    z = cam.z
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    rng = np.random.default_rng(7)
    x0, x1 = -1500, 2500
    flat = dict(shadow=False, jitter=False, edge=False)
    paper(img, cam.pts(rect(x0, -1500, x1, 1300)), (150, 34, 30) if red else (126, 196, 236), rng, z, **flat)
    if red:
        paper(img, cam.pts(rect(x0, -1500, x1, 260)), (92, 16, 22), rng, z, **flat)
        paper(img, cam.pts([(x0, 260), (x1, 200), (x1, 520), (x0, 600)]), (124, 24, 26), rng, z, shadow=False, edge=False)
        for (cx, cy, r) in [(140, 330, 120), (300, 300, 90), (-200, 520, 130), (1200, 620, 110), (1700, 300, 140)]:
            paper(img, cam.pts(lumpy(cx, cy, r, [(14, 5, cx), (8, 9, 1)])), (64, 14, 20), rng, z, sh=5)
    else:
        sx, sy = 880, 330
        for a in range(0, 360, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            paper(img, cam.pts([(sx + 130 * ca - 22 * sa, sy + 130 * sa + 22 * ca), (sx + 130 * ca + 22 * sa, sy + 130 * sa - 22 * ca),
                                (sx + 196 * ca, sy + 196 * sa)]), (250, 214, 90), rng, z, shadow=False)
        paper(img, cam.pts(ell(sx, sy, 112, 112)), (252, 226, 110), rng, z, sh=5)
        for (cx, cy, r) in [(190, 300, 100), (330, 330, 76), (60, 350, 70), (1500, 420, 110), (1650, 440, 80), (-600, 380, 110),
                            (-760, 420, 80)]:
            paper(img, cam.pts(lumpy(cx, cy, r, [(10, 5, cx), (6, 9, 1)])), (250, 250, 250), rng, z, sh=5)
        for k, tx in enumerate(range(x0 + 100, x1, 260)):   # hedge tops behind the fence
            paper(img, cam.pts(lumpy(tx + (k * 53) % 70, 880, 170 + (k * 31) % 50, [(16, 5, k), (9, 8, 1)])),
                  (70, 140, 70) if k % 2 else (84, 156, 80), rng, z, sh=5)
    for k, px in enumerate(range(x0, x1, 112)):   # fence
        col = tint((224, 190, 138) if k % 2 else (212, 176, 122), red)
        paper(img, cam.pts([(px, 1210), (px, 930), (px + 53, 890), (px + 106, 930), (px + 106, 1210)]), col, rng, z, sh=4)
    for ry in (980, 1130):
        paper(img, cam.pts(rect(x0, ry, x1, ry + 26)), tint((190, 154, 104), red), rng, z, sh=4)
    if scene in ("ray", "karen"):   # the gate
        paper(img, cam.pts(rect(880, 900, 1080, 1215)), tint((170, 120, 76), red), rng, z)
        paper(img, cam.pts(strip([(890, 1200), (1070, 920)], 22)), tint((140, 96, 60), red), rng, z, sh=3)
        paper(img, cam.pts(rect(915, 990, 1045, 1060)), WHITE, rng, z, sh=4)
        d = ImageDraw.Draw(img)
        d.text(cam.p(980, 1026), "EXIT", font=font(50 * z), fill=RED, anchor="mm")
    if not red:   # bunting along the fence
        cols = [(230, 70, 60), (250, 210, 70), (70, 150, 220), (250, 250, 246), (240, 140, 60)]
        for k, bx in enumerate(range(x0, x1, 96)):
            by = 912 + 22 * math.sin(bx / 150.0)
            paper(img, cam.pts([(bx, by), (bx + 80, by + 6), (bx + 40, by + 96)]), cols[k % 5], rng, z, sh=3)
    paper(img, cam.pts(rect(x0, 1190, x1, 4000)), tint((104, 170, 84), red), rng, z, **flat)
    paper(img, cam.pts([(x0, 1190), (x1, 1190), (x1, 1230), (x0, 1250)]), tint((92, 156, 76), red), rng, z, shadow=False, edge=False)
    g2 = np.random.default_rng(9)
    for _ in range(170):   # grass tufts
        gx, gy = float(g2.uniform(x0, x1)), float(g2.uniform(1260, 2300))
        paper(img, cam.pts([(gx - 14, gy), (gx - 8, gy - 26), (gx, gy - 4), (gx + 8, gy - 30), (gx + 15, gy)]),
              tint((84, 148, 70), red), rng, z, shadow=False, jitter=False, edge=False)
    if scene in ("yard", "tv"):
        tx = 900 if scene == "yard" else 540
        paste(img, prop("table", round(z * (0.8 if scene == "yard" else 1.25), 3)), *cam.p(tx, 1500 if scene == "tv" else F - 120))
    return img


def bg_chart(cam):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    rng = np.random.default_rng(21)
    paper(img, rect(-50, -50, W + 50, H + 50), (30, 66, 78), rng, 1.0, shadow=False, jitter=False, edge=False)
    paper(img, [(50, 410), (1030, 396), (1036, 1530), (44, 1520)], (250, 248, 240), rng, 1.5, sh=10)
    for gy in range(560, 1500, 130):
        paper(img, strip([(110, gy), (980, gy)], 4), (220, 222, 226), rng, 1.0, shadow=False, edge=False)
    paper(img, strip([(110, 480), (110, 1440), (990, 1440)], 10), INK, rng, 1.0, shadow=False)
    paper(img, [(116, 1436), (116, 1150), (300, 1040), (470, 900), (640, 760), (656, 1436)], (156, 108, 68), rng, 1.5, sh=6)
    paper(img, [(116, 1150), (300, 1040), (470, 900), (640, 760), (646, 800), (480, 936), (306, 1076), (116, 1186)],
          (104, 170, 84), rng, 1.2, shadow=False)
    b = C.banner_img("JESUSCOIN", 120, GOLD, INK, 5)
    paste(img, b, W / 2, 300, 2)
    return img


def bg(scene, cam_name):
    key = (scene, cam_name)
    if key not in G["bg"]:
        cam = Cam(LAYOUT, *G["cams"][scene][cam_name])
        G["bg"][key] = bg_chart(cam) if scene == "chart" else bg_yard(cam, scene)
    return G["bg"][key]


# ------------------------------------------------------------------------------------------------ scenes
def gd(name, t):
    """Seconds into gag `name`, or None before it."""
    e = G["ev"].get(name)
    return None if e is None or t < e else t - e


def step(v):
    return int(v * FPS) / FPS


def sc_yard(fr, cam, st):
    t, fi, li = st
    meat(fr, cam, X["yard"]["mb"], st)
    first = G["lines"][0]
    t1 = first["words"][9][0] - 0.04
    if t < t1:
        for i, txt_ in enumerate(TITLE):
            t0 = 0.0 + 0.12 * i
            if t < t0:
                continue
            k = int((t - t0) * FPS)
            off = [-90, 14, 0][min(2, k)]
            img = C.banner_img(txt_, 112, [RED, (252, 214, 74), RED][i], [WHITE, INK, WHITE][i], 30 + i)
            paste(fr, img, W / 2, 250 + i * 176 + off, [-3, 2, -2][i])


def smoke(fr, cam, x, y, fi, n=4):
    for k in range(n):
        ph = (fi + k * 5) % 20
        P(fr, cam, "smoke", x + 14 * math.sin(ph * 0.7 + k) * K, y - ph * 22 * K, 0, 0.6 + ph * 0.05, (k % 3,))


def sc_smoker(fr, cam, st):
    t, fi, li = st
    xs = X["smoker"]
    d = gd("lid", t)
    op = d is not None
    P(fr, cam, "smoker", xs["smoker"], F, 0, 1.0, (op,))
    a = 0 if not op else min(72, int(d * FPS) * 24)
    P(fr, cam, "lid", xs["smoker"] - 210 * K, F - 300 * K, a)
    smoke(fr, cam, xs["smoker"] + 192 * K, F - 570 * K, fi)
    if op and 0.25 < d < 1.3:
        for k in range(3):
            ph = int((d - 0.25) * FPS) + k * 2
            P(fr, cam, "smoke", xs["smoker"] + (-120 + k * 120) * K, F - (340 + ph * 26) * K, 0, 0.8 + ph * 0.06, (k,))
    spk, _, wi = state("todd", st)
    kw = dict(items=(("spatula", "L", 8),), aL=-150 if (spk and wi >= 3) else -40)
    if op:
        kw.update(expr="proud", aR=110, aL=-150, hop=-12 if 0.3 < d < 0.45 else 0)
    rig(fr, cam, "todd", xs["todd"], st, **kw)
    meat(fr, cam, xs["mb"], st, expr="smug" if (fi // 5) % 2 else "norm")


def sc_ray(fr, cam, st):
    t, fi, li = st
    xs = X[G["scene"]]
    karen = G["scene"] == "karen"
    spk, _, wi = state("ray", st)
    kw = dict(items=(("can", "R", 0),), aR=62)
    pt = gd("point", t)
    rk = gd("rocket", t)
    if not karen:
        if pt is not None and rk is None:
            kw.update(aR=88 if pt >= 0.17 else 30, items=(), hop=-8 if 0.17 <= pt < 0.26 else 0, ang=4)
        if rk is not None and rk > 1.5:
            kw.update(aR=158)
    else:
        kw.update(ang=-7, aL=-10, hop=0, jit=0.5)
    rig(fr, cam, "ray", xs["ray"], st, **kw)
    if karen:
        spk_k, _, _ = state("karen", st)
        hold = li is None
        rig(fr, cam, "karen", xs["karen"], st, items=(() if hold else (("clipboard", "L", -8),)), aL=-36,
            expr="wide" if hold else "norm", jit=5 if hold else (1.6 if spk_k else 1), gaze="l",
            **({"aR": 12} if hold else {}))
        if hold:
            P(fr, cam, "clipboard", xs["karen"] - 150 * K, F - 10 * K, 70)
        return
    ex = xs["elon"]
    hd = gd("hand", t)
    P(fr, cam, "tub", ex - 150 * K, F - 40 * K) if rk is not None and rk >= 0.25 else None
    if rk is None or rk < 0.25:
        up = hd is not None and hd >= 0.17
        rig(fr, cam, "elon", ex, st, items=(("tub", "L", 0),), aL=-52, aR=168 if up else 12, gaze="l",
            hop=-10 if (hd is not None and 0.17 <= hd < 0.26) else 0, lvl=1 if up else 0)
        return
    lift = 0.0 if rk < 1.0 else (int((rk - 1.0) * FPS) + 1) ** 2 * 15 * K
    zz = round(cam.z * K * (1.12 if rk < 0.34 else 1.0), 3)
    sh_ = (6 if fi % 2 else -6) if 0.6 < rk else 0
    bx, by = ex + sh_, F - lift
    if rk > 0.6:
        P(fr, cam, "flame", bx, by - 24 * K, 0, 1.0 if rk >= 1.0 else 0.6, (fi % 2,))
    paste(fr, prop("rocket", zz), *cam.p(bx, by))
    paste(fr, rspr("elon", "head", round(cam.z * K * 0.5, 3), 0, False, "norm", "c", frozenset()),
          *cam.p(bx, by - (390 - 54) * K))
    if rk > 0.6:
        for k in range(5):
            ph = int((rk - 0.6) * FPS) + k
            P(fr, cam, "smoke", ex + (k - 2) * (40 + ph * 9) * K, F - (10 + (ph % 5) * 12) * K, 0, 1.0 + ph * 0.07, (k % 3,))
    if 2.2 <= rk < 2.5:
        P(fr, cam, "twinkle", ex + 40, 170, 0, 1.6 if fi % 2 else 1.0)


def sc_nonna(fr, cam, st):
    t, fi, li = st
    xs = X["nonna"]
    fd, bs = gd("feed", t), gd("bsod", t)
    spk_n, _, _ = state("nonna", st)
    n_kw = dict(items=(("plate_balls", "R", 0, 3 if fd is None or fd < 0.17 else 2), ("spoon", "L", 0)), aR=82, aL=-150)
    if spk_n:
        n_kw.update(aR=96, hop=-14)
    z_kw = dict(blink=False, jit=0.3, ang=0.0, hop=0)
    if fd is not None:
        n_kw.update(aL=-175 if fd < 0.17 else -80)
        if 0.1 <= fd < 0.52:
            z_kw.update(lvl=2)
        if fd >= 0.52:
            z_kw.update(flags=("full",), hop=-12 if fd < 0.62 else 0)
    if bs is not None:
        n_kw.update(aL=-150, aR=82)
        if bs < 0.25:
            z_kw.update(flags=("full",), jit=9)
        else:
            rot = 0.0 if bs < 1.1 else -min(12.0, (int((bs - 1.1) * FPS) + 1) * 4.0)
            z_kw.update(flags=("bsod",), aL=-62, aR=62, rot=rot, jit=0)
    rig(fr, cam, "nonna", xs["nonna"], st, **n_kw)
    rig(fr, cam, "zuck", xs["zuck"], st, **z_kw)
    if bs is not None and bs >= 0.6:
        for k in range(3):
            ph = (fi + k * 3) % 9
            P(fr, cam, "smoke", xs["zuck"] + (-50 + k * 50) * K, F - (500 + ph * 24) * K, 0, 0.6 + ph * 0.06, (k,))
    spk_z, _, _ = state("zuck", st)
    if spk_z:   # loading dots over his head
        for k in range(8):
            a = k * math.pi / 4
            px, py = cam.p(xs["zuck"] + 46 * math.cos(a) * K, F - 590 * K + 46 * math.sin(a) * K)
            r = 9 * cam.z * K
            on = (fi - k) % 8 < 3
            ImageDraw.Draw(fr).ellipse((px - r, py - r, px + r, py + r), fill=(40, 90, 220) if on else (190, 200, 220))
    if fd is not None and 0.17 <= fd < 0.52 and bs is None:
        f = (int((fd - 0.17) * FPS) + 1) / 5
        x0_, y0_ = xs["nonna"] + 110 * K, F - 250 * K
        x1_, y1_ = xs["zuck"], F - 292 * K
        P(fr, cam, "meatball", x0_ + (x1_ - x0_) * f, y0_ + (y1_ - y0_) * f - math.sin(f * math.pi) * 230 * K, f * 300)
    meat(fr, cam, xs["mb"], st, expr="smug")


def sc_tv(fr, cam, st):
    t, fi, li = st
    d = gd("tvon", t)
    sx0, sy0, sx1, sy1 = 190, 600, 800, 1090
    box(fr, cam, 130, 540, 950, 1215, (120, 84, 56), 3, sh=8)
    a, b = cam.p(sx0, sy0)
    c_, e = cam.p(sx1, sy1)
    a, b, c_, e = int(a), int(b), int(c_), int(e)
    scr = Image.new("RGBA", (c_ - a, e - b), (40, 70, 140, 255))
    sc_cam = Cam(dict(W=scr.size[0], H=scr.size[1]), (sx0 + sx1) / 2, (sy0 + sy1) / 2, cam.z)
    if d is not None and d < 0.34:
        n = Image.effect_noise((scr.size[0] // 6, scr.size[1] // 6), 90).resize(scr.size, Image.NEAREST).convert("RGBA")
        scr = n
    else:
        for k in range(6):
            poly(scr, sc_cam, [(sx0 + k * 130 - 80, sy0), (sx0 + k * 130 - 20, sy0), (sx0 + k * 130 - 160, sy1),
                               (sx0 + k * 130 - 220, sy1)], (52, 86, 160), 4 + k, shadow=False, edge=False)
        spk, lvl, wi = state("anchor", st)
        rng = np.random.default_rng(fi)
        paste(scr, prop("anchor", round(cam.z * 0.95, 3), lvl, (fi + 5) % 37 == 0),
              *sc_cam.p(380 + float(rng.uniform(-1.5, 1.5)), 1010 + (-6 if spk and lvl == 2 else 0)))
        box(scr, sc_cam, 596, 622, 786, 800, WHITE, 5, sh=5)
        box(scr, sc_cam, 606, 632, 776, 790, (70, 30, 40), 6, shadow=False)
        paste(scr, prop("fire", round(cam.z * 1.15, 3), fi % 2), *sc_cam.p(690, 728))
        paste(scr, prop("toaster", round(cam.z * 0.8, 3)), *sc_cam.p(690, 712))
        paste(scr, prop("fire", round(cam.z * 0.6, 3), (fi + 1) % 2), *sc_cam.p(668, 712))
        box(scr, sc_cam, 190, 990, 430, 1080, RED, 7, sh=4)
        box(scr, sc_cam, 430, 990, 800, 1080, WHITE, 8, sh=4)
        if (fi // 3) % 2 or not spk:
            txt(scr, sc_cam, 310, 1037, "BREAKING", 44, WHITE)
        label = "CRISIS"
        if spk:
            label = ["CRISIS", "CRISIS", "CRISIS", "CRISIS (AGAIN)", "CRISIS (AGAIN)", "CRISIS (AGAIN)"][min(wi, 5)]
            if wi >= 6:
                label = "CRISIS #5 TODAY"
        elif li is None and d is None:
            label = "CRISIS #5 TODAY"
        txt(scr, sc_cam, 615, 1037, label, 40 if len(label) > 8 else 50, INK)
        r = 9 * cam.z
        qx, qy = sc_cam.p(222, 636)
        if (fi // 4) % 2:
            ImageDraw.Draw(scr).ellipse((qx - r, qy - r, qx + r, qy + r), fill=(240, 50, 40))
        txt(scr, sc_cam, 280, 638, "LIVE", 30, WHITE)
    fr.alpha_composite(scr, (a, b))
    for (x0_, y0_, x1_, y1_) in [(170, 580, 820, 604), (170, 1086, 820, 1110), (170, 580, 194, 1110), (796, 580, 820, 1110)]:
        box(fr, cam, x0_, y0_, x1_, y1_, (60, 50, 44), 9, shadow=False)
    for k, ky in enumerate((680, 800)):
        poly(fr, cam, ell(884, ky, 34, 34), (230, 224, 206), 11 + k, sh=4)
        poly(fr, cam, strip([(884, ky), (884 + 20 * (1 if k else -1), ky - 24)], 8), INK, 13, shadow=False)
    for k in range(5):
        box(fr, cam, 850, 900 + k * 34, 918, 914 + k * 34, (70, 56, 44), 15, shadow=False)
    poly(fr, cam, strip([(470, 545), (330, 330)], 10), (170, 174, 184), 16, sh=4)
    poly(fr, cam, strip([(610, 545), (760, 350)], 10), (170, 174, 184), 17, sh=4)


def sc_pastor(fr, cam, st):
    t, fi, li = st
    xs = X["pastor"]
    w, g = gd("walkin", t), gd("grab", t)
    off, hop = 0.0, 0
    if w is not None and w < 0.84:
        k = int(w * FPS)
        off, hop = (10 - k) * 95.0, -16 if k % 2 else 0
    spk, _, wi = state("chad", st)
    c_kw, b_kw = dict(hop=hop) if off else {}, dict(hop=-hop - 16 if off else 0, items=(("cplate", "L", 0),), aL=-70)
    ln = G["lines"][li] if li is not None else None
    if spk and "launch" in " ".join(x[2] for x in ln["words"]) and wi >= 7:
        b_kw.update(aR=165, items=b_kw["items"] + (("coin", "R", 0, True),), hop=-12 if (fi % 4 < 2) else 0)
    cx = xs["chad"] + off
    if g is not None:
        if g < 0.25:
            c_kw.update(aR=86)
        else:
            b_kw.update(items=(), aL=-150, aR=150, flags=("sad",), hop=-10 if fi % 2 else 0)
            k = max(0, int((g - 0.42) * FPS) + 1) if g >= 0.42 else 0
            cx = xs["chad"] - k * 105.0
            c_kw.update(items=(("cplate", "R", 0),), aR=150, aL=-70, hop=(-18 if k % 2 else 0), lvl=2)
            for j in range(3):
                if k > j + 1:
                    P(fr, cam, "bill", cx + (150 + j * 130) * K, F - (330 + 40 * math.sin(fi + j * 2)) * K - j * 30, (fi * 40 + j * 70) % 360)
    rig(fr, cam, "bro", xs["bro"] + off * 1.15, st, **b_kw)
    rig(fr, cam, "chad", cx, st, **c_kw)


def sc_chart(fr, cam, st):
    t, fi, li = st
    d = gd("chart", t) or 0.0
    path = [(116, 1150), (300, 1040), (470, 900), (640, 760)]
    seg = [math.hypot(path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]) for i in range(3)]
    f = min(1.0, step(d) / 0.8)

    def along(f_):
        s = f_ * sum(seg)
        for i in range(3):
            if s <= seg[i] or i == 2:
                r = min(1.0, s / seg[i])
                return (path[i][0] + (path[i + 1][0] - path[i][0]) * r, path[i][1] + (path[i + 1][1] - path[i][1]) * r)
            s -= seg[i]
    pts = [path[0]] + [along(f * k / 8) for k in range(1, 9)]
    rng = np.random.default_rng(31)
    paper(fr, strip([(x, y - 14) for x, y in pts], 18), (40, 170, 80), rng, 1.2, sh=4)
    cx, cy = along(f)
    zc = 1.5
    if d < 0.8:
        paste(fr, prop("coin", zc, True), cx, cy - 80 - (14 if int(d * FPS) % 2 else 0))
    elif d < 1.15:
        paste(fr, prop("coin", zc, True), 660, 680, 14 if fi % 2 else -14)
        tg = C.tag("TO THE MOON!", 54, 3)
        paste(fr, tg, 520, 600)
    else:
        k = int((d - 1.15) * FPS) + 1
        y = min(1385.0, 680 + k * k * 7.2)
        x = min(790.0, 670 + k * 16)
        landed = y >= 1385
        paper(fr, strip([(650, 760), (700, 800), (x - 10, max(810, y - 40))], 18), (220, 50, 40), rng, 1.2, sh=4)
        if landed:
            im = prop("coin", zc, False)
            im = im.resize((im.size[0], im.size[1] // 3), Image.BICUBIC)
            paste(fr, im, x, 1420)
            paste(fr, prop("dust", 1.4, 0), x - 90, 1400)
            paste(fr, prop("dust", 1.1, 1), x + 100, 1410)
            lt = d - (1.15 + 10 / FPS)
            if lt > 0.1:
                tg = C.tag("$0.00", 96, 4)
                paste(fr, tg, 800, 1130 + (-20 if lt < 0.2 else 0))
            paper(fr, [(840, 560), (960, 560), (960, 800), (1010, 800), (900, 940), (790, 800), (840, 800)], (220, 50, 40),
                  rng, 1.5, sh=8)
        else:
            paste(fr, prop("coin", zc, True), x, y, -k * 40)


def sc_congress(fr, cam, st):
    t, fi, li = st
    xs = X["congress"]
    d = gd("cash", t)
    in_gag = d is not None and d < G["gd"]["cash"]
    spk, _, wi = state("congress", st)
    c_kw, l_kw = {}, {}
    if in_gag:
        if d < 0.5:
            c_kw.update(aR=40 + min(4, int(d * FPS)) * 12, items=(("cash", "R", 0),), gaze="l", ang=-6)
            l_kw.update(aL=-70, gaze="r")
        elif d < 0.85:
            c_kw.update(aR=12, gaze="l", ang=-8)
            l_kw.update(aL=-86, items=(("cash", "L", 0),), hop=-10 if d < 0.6 else 0)
        else:
            c_kw.update(gaze="l", ang=-8, lvl=1)
            l_kw.update(aL=-20, flags=("dollar",))
    elif spk:
        l_kw.update(aL=-150, aR=150, hop=-12 if fi % 4 < 2 else 0, flags=("dollar",) if wi >= 6 else ())
    elif li is None:
        l_kw.update(flags=("dollar",), aL=-150, aR=150, hop=-10 if fi % 4 < 2 else 0, lvl=1)
    rig(fr, cam, "congress", xs["congress"], st, **c_kw)
    rig(fr, cam, "lobby", xs["lobby"], st, **l_kw)


RUNNERS = [("todd", 1, 310, 0), ("karen", -1, 380, 500), ("chad", 1, 440, 900), ("lobby", -1, 300, 1300),
           ("nonna", 1, 360, 1500), ("bro", -1, 420, 200), ("congress", 1, 280, 1150)]


def sc_red(fr, cam, st):
    t, fi, li = st
    e0, e1 = G["ev"]["red"], G["ev"]["land"]
    f = min(1.0, max(0.0, (t - e0) / (e1 - e0)))
    ld = gd("land", t)
    if ld is None:   # the meteor hangs in the sky (screen space: it is far away), growing
        z = 0.34 + 0.4 * step(f * 10) / 10
        paste(fr, prop("meteor", round(z, 3)), 860 - 190 * f, 150 + 130 * f, 4 if fi % 2 else -4)
        paste(fr, prop("fire", round(z * 1.6, 3), fi % 2), 860 - 190 * f - 10, 150 + 130 * f - 30 * z, 200)
    for (c, sgn, sp, ph) in RUNNERS:
        x = ((ph + sgn * (t - e0) * sp * 2.2) % 2300) - 600
        rig(fr, cam, c, x, st, y=F - 150, scale=0.74, aL=-158 + (10 if fi % 2 else 0), aR=158 - (10 if fi % 2 else 0),
            lvl=2, hop=-22 if (fi + CI[c]) % 2 else 0, jit=3, items=(), expr="wide", flags=())
    spk, _, wi = state("mb", st)
    smug = spk and wi >= 17
    meat(fr, cam, X["red"]["mb"], st, expr="smug" if smug else ("wide" if not spk else "norm"),
         gaze="u" if (not spk and ld is None) else "c")
    if ld is not None:   # it comes down
        k = int(ld * FPS)
        g = min(1.0, (k + 1) / 6)
        x, y = 670 + (760 - 670) * g, 280 + (1250 - 280) * g
        paste(fr, prop("meteor", round(0.74 + 0.9 * g, 3)), x, y, 0)
        if k >= 6:
            fr.alpha_composite(Image.new("RGBA", fr.size, (255, 250, 230, 235)))


def sc_done(fr, cam, st):
    t, fi, li = st
    xs = X["done"]
    d = gd("done", t) or 0.0
    P(fr, cam, "smoker", xs["todd"] - 520, F, 0, 1.0, (True,))
    P(fr, cam, "lid", xs["todd"] - 520 - 210 * K, F - 300 * K, 72)
    spk, _, wi = state("todd", st)
    rig(fr, cam, "todd", xs["todd"], st, expr="proud", aR=96, aL=-150 if spk else -30,
        items=(("dogplate", "R", 0), ("spatula", "L", 8)), hop=-12 if 0.25 < d < 0.34 else (-10 if spk and fi % 4 < 2 else 0))
    hx, hy = xs["todd"] + (76 + 114 * math.sin(math.radians(96))) * K, F + (-232 + 114 * math.cos(math.radians(96))) * K
    for k in range(3):
        ph = (fi + k * 3) % 9
        P(fr, cam, "steam", hx + (-60 + k * 60) * K, hy - (60 + ph * 10) * K, 0, 1.0, ((fi // 2 + k) % 2,))
    if d < 2 / FPS:
        fr.alpha_composite(Image.new("RGBA", fr.size, (255, 250, 230, 235 if d < 1 / FPS else 120)))
    elif d < 0.75:
        px, py = cam.p(hx + 10, hy - 250 * K)
        paste(fr, C2.spr("star", round(1.5 if fi % 2 else 1.3, 2), "DING!"), px, py, (fi % 2) * 8)


SCENES = dict(yard=sc_yard, smoker=sc_smoker, ray=sc_ray, karen=sc_ray, nonna=sc_nonna, tv=sc_tv, pastor=sc_pastor,
              chart=sc_chart, congress=sc_congress, red=sc_red, done=sc_done)


def shake(t):
    ev = G["ev"]
    r = gd("rocket", t)
    if r is not None and 0.6 < r < 2.0:
        return (10, -8) if int(t * FPS) % 2 else (-8, 10)
    for name, dt in (("chart", 1.15 + 10 / FPS), ("done", 0.0)):
        if name in ev and 0 <= t - (ev[name] + dt) < 2 / FPS:
            return (22, -14) if t - (ev[name] + dt) < 1 / FPS else (-12, 8)
    return (0, 0)


def frame(fi):
    t = fi / FPS
    _, scene, cam_name = C2.seg_at(t)
    G["scene"] = scene
    cx, cy, z = G["cams"][scene][cam_name]
    sx_, sy_ = shake(t)
    cam = Cam(LAYOUT, cx + sx_ / z, cy + sy_ / z, z)
    fr = bg(scene, cam_name).copy()
    if sx_ or sy_:
        fr = ImageChops.offset(fr, -sx_, -sy_)
    li = C2.speaking(t)
    SCENES[scene](fr, cam, (t, fi, li))
    C2.draw_caption(fr, t, cam_name)
    return np.asarray(fr.convert("RGB")).tobytes()


# ------------------------------------------------------------------------------------------------ audio
def sweep(f0, f1, dur, g=0.2, harm=(1.0,)):
    tt = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * np.cumsum(f0 + (f1 - f0) * tt / dur) / SR
    x = sum(a * np.sin((k + 1) * ph) for k, a in enumerate(harm))
    env = np.minimum(1, np.minimum(tt / 0.01, (dur - tt) / 0.03))
    return (x * env * g).astype(np.float32)


def ching(fx, t, g=0.3):
    add(fx, ks(hz("E6"), 0.5, 0.995, 0.95, 70), t, g)
    add(fx, ks(hz("B6"), 0.7, 0.996, 0.95, 71), t + 0.08, g)
    add(fx, C2.noise_burst(0.12, 0.03, 5, 1), t, g * 0.25)


def line_with(text, who=None):
    for ln in G["lines"]:
        if text in " ".join(w[2] for w in ln["words"]) and (who is None or ln["who"] == who):
            return ln


def mix(end):
    ev, lines = G["ev"], G["lines"]
    n = int((end + 1) * SR)
    music, fx = np.zeros(n, np.float32), np.zeros(n, np.float32)
    strum(music, 0.0, "C", 0.35, seed=3)
    for i in range(3):
        sfx_slap(fx, 0.02 + 0.12 * i, 0.3, i)
    bed = np.zeros(n, np.float32)
    prog = [["C"], ["A7"], ["D7"], ["G7"]]
    t, k = 0.0, 0
    while t < ev["red"]:
        jingle_bar(bed, t, prog[k % 4], 0.32, None, drums=True, seed=10 + k)
        t += 4 * BEAT
        k += 1
    gate = np.ones(n, np.float32)
    for a, b in ((ev["lid"] + 0.3, ev["lid"] + 3.5), (ev["bsod"] + 0.25, ev["bsod"] + 2.0), (ev["tvon"], ev["walkin"]),
                 (ev["chart"] + 0.8, ev["chart"] + 3.2), (ev["red"], end + 1)):
        gate[int(a * SR):int(b * SR)] = 0
    kr = line_with("promoted", "ray")
    gate[int((kr["start"] + kr["dur"]) * SR):int((kr["start"] + kr["dur"] + 0.8) * SR)] = 0
    gate = np.convolve(gate, np.ones(2205) / 2205, "same").astype(np.float32)
    music += bed * gate * 10 ** (-22 / 20) * 1.6
    # --- smoker
    L0 = ev["lid"]
    add(fx, sweep(180, 420, 0.3, 0.14, (1, 0.4, 0.2)), L0)
    add(fx, C2.noise_burst(1.4, 0.5, 3, 1) * 0.5, L0 + 0.3, 0.1)
    for i, (f0, f1, dd) in enumerate([(311, 294, 0.32), (294, 277, 0.32), (277, 196, 0.7)]):   # sad horn
        add(fx, sweep(f0, f1, dd, 0.16, (1, 0.5, 0.33, 0.2)), L0 + 0.75 + i * 0.36)
    # --- potato salad
    add(fx, ks(hz("C6"), 0.6, 0.995, 0.9, 20), ev["hand"] + 0.17, 0.35)
    sfx_slap(fx, ev["point"] + 0.17, 0.5, 4)
    add(fx, sweep(300, 900, 0.14, 0.12), ev["point"] + 0.1)
    R0 = ev["rocket"]
    sfx_slap(fx, R0 + 0.25, 0.6, 6)
    rum = C2.noise_burst(1.9, 5.0, 8, 12)
    rum *= np.linspace(0.2, 1.0, len(rum)) ** 1.5 * 6
    add(fx, rum, R0 + 0.6, 0.5)
    add(fx, sweep(200, 2400, 1.1, 0.12, (1, 0.3)), R0 + 1.0)
    add(fx, ks(hz("C7"), 0.5, 0.995, 0.95, 21), R0 + 2.2, 0.3)
    add(fx, ks(hz("G7"), 0.4, 0.995, 0.95, 22), R0 + 2.28, 0.25)
    # --- nonna
    Fd, B0 = ev["feed"], ev["bsod"]
    sfx_slap(fx, Fd + 0.17, 0.6, 7)
    add(fx, sweep(400, 1100, 0.3, 0.12), Fd + 0.17)
    C2.thud(fx, Fd + 0.52, 0.5)
    add(fx, sweep(260, 120, 0.16, 0.2), Fd + 0.6)
    for i, f in enumerate((660, 520, 392)):
        add(fx, C2.tone(f, 0.16, 0.16) + C2.tone(f * 1.5, 0.16, 0.06), B0 + 0.25 + i * 0.17)
    add(fx, C2.tone(110, 0.5, 0.1), B0 + 0.8)
    add(fx, C2.noise_burst(1.0, 0.5, 17, 1) * 0.5, B0 + 0.6, 0.08)
    add(fx, sweep(500, 90, 0.5, 0.14, (1, 0.5)), B0 + 1.1)
    # --- tv
    Tv = ev["tvon"]
    sfx_slap(fx, Tv, 0.4, 5)
    add(fx, C2.noise_burst(0.34, 0.4, 21, 1), Tv + 0.02, 0.14)
    for i, nt in enumerate(["C5", "E5", "G5", "C6", "G5", "C6"]):
        add(fx, ks(hz(nt), 0.3, 0.993, 0.9, 30 + i), Tv + 0.36 + i * 0.09, 0.26)
    an = line_with("Breaking", "anchor")
    for i in range(int(an["dur"] / 0.5)):   # a news tick under the anchor
        add(fx, C2.tone(1400, 0.03, 0.05), an["start"] + 0.9 + i * 0.5)
    # --- pastor
    add(fx, C2.choir(1.3, ("C3", "G3", "C4", "E4", "G4")), ev["walkin"], 0.3)
    for ln in lines:
        if ln["who"] == "chad":
            add(fx, ks(hz("C7"), 0.5, 0.995, 0.95, 90), ln["t0"] + 0.02, 0.2)
            add(fx, ks(hz("G7"), 0.4, 0.995, 0.95, 91), ln["t0"] + 0.1, 0.16)
    Ch = ev["chart"]
    for i, nt in enumerate(["C5", "D5", "E5", "G5", "A5", "C6", "D6", "E6"]):
        add(fx, ks(hz(nt), 0.25, 0.99, 0.9, 80 + i), Ch + 0.05 + i * 0.1, 0.3)
    add(fx, sweep(1500, 220, 10 / FPS, 0.16, (1, 0.25)), Ch + 1.15)
    C2.thud(fx, Ch + 1.15 + 10 / FPS, 1.0)
    add(fx, sweep(277, 185, 0.6, 0.14, (1, 0.5, 0.33)), Ch + 2.2)
    Gr = ev["grab"]
    ching(fx, Gr + 0.25)
    for i in range(7):
        add(fx, ks(hz(["G5", "A5"][i % 2]), 0.12, 0.985, 0.9, 60 + i), Gr + 0.42 + i * 0.1, 0.25)
    # --- karen / ray
    kt = kr["start"] + kr["dur"] + 0.08
    kick(fx, kt, 0.5)
    snare(fx, kt + 0.12, 0.5, 3)
    add(fx, ks(hz("C3"), 0.8, 0.996, 0.5, 33), kt, 0.4)
    # --- congress
    ching(fx, ev["cash"] + 0.5)
    cg = line_with("green", "congress")
    ching(fx, cg["start"] + cg["dur"] + 0.15, 0.25)
    # --- the end of the world
    Rd, Ld, Dn = ev["red"], ev["land"], ev["done"]
    C2.thud(fx, Rd, 1.0)
    add(fx, sweep(110, 70, 1.2, 0.2, (1, 0.5, 0.3)), Rd)
    t = Rd
    while t < Ld:   # a quiet two-tone alarm and a low rumble under the question
        add(fx, C2.tone(620, 0.3, 0.035), t)
        add(fx, C2.tone(470, 0.3, 0.035), t + 0.3)
        kick(fx, t, 0.22)
        t += 0.6
    rum = C2.noise_burst(Ld - Rd + 0.6, 30.0, 9, 40)
    add(fx, rum * np.linspace(0.3, 1.0, len(rum)) * 10, Rd, 0.07)
    add(fx, sweep(1900, 300, 0.5, 0.18, (1, 0.3)), Ld)
    C2.thud(fx, Dn, 1.2)
    snare(fx, Dn + 0.02, 0.6, 5)
    add(fx, ks(hz("C7"), 0.9, 0.997, 0.95, 40), Dn + 0.2, 0.4)
    add(fx, ks(hz("E7"), 0.9, 0.997, 0.95, 41), Dn + 0.26, 0.3)
    add(fx, C2.noise_burst(0.9, 0.4, 13, 1) * 0.4, Dn + 0.3, 0.07)
    last = lines[-1]
    strum(music, last["start"] + last["dur"] + 0.02, "C", 0.35, seed=60)
    vo = np.zeros(n, np.float32)
    for ln in lines:
        add(vo, ln["audio"], ln["start"], 1.0)
    out = vo + music + fx * 0.8
    out *= 0.97 / max(1e-6, float(np.max(np.abs(out))))
    return out[:int(end * SR)]


# ------------------------------------------------------------------------------------------------ main
def use():
    C2.SEQ[:] = SEQ_COOK
    C2.V.update(VOICES)


def setup(pre=True):
    use()
    lines, segs, ev, end = C2.build()
    G.update(L=LAYOUT, lines=lines, segs=segs, ev=ev, end=end, cams=cams(), bg={}, gd=dict(C2.GD))
    if pre:
        for (_, scene, cam) in segs:
            bg(scene, cam)


def render(out):
    os.makedirs(TMP, exist_ok=True)
    setup()
    end = G["end"]
    wav = f"{TMP}/cookout-mix.wav"
    import soundfile as sf
    sf.write(wav, mix(end), SR)
    n = int(math.ceil(end * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", str(FPS),
           "-i", "-", "-i", wav, "-vf", f"fps={OUT_FPS}", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(int(os.environ.get("COOKOUT_PROCS", "3"))) as pool:
        for b in pool.imap(frame, range(n), chunksize=4):
            ff.stdin.write(b)
    ff.stdin.close()
    ff.wait()
    print(out, f"{end:.2f}s", n, "frames")


def stills(times):
    os.makedirs(TMP, exist_ok=True)
    setup(pre=False)
    for t in times:
        p = f"{TMP}/still-{t:06.2f}.png"
        Image.frombytes("RGB", (W, H), frame(int(t * FPS))).save(p)
        print(p)


def timeline():
    setup(pre=False)
    for i, ln in enumerate(G["lines"]):
        print(f"{i + 1:2d} {ln['who']:8s} {ln['t0']:7.2f} {ln['dur']:5.2f} {' '.join(w[2] for w in ln['words'])[:70]}")
    print({k: round(v, 2) for k, v in G["ev"].items()}, "end", round(G["end"], 2))
    for s in G["segs"]:
        print(f"  {s[0]:7.2f} {s[1]}/{s[2]}")


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ").replace("...", " "))


def linecheck(media, minimum=0.6):
    """tools/linecheck.py, for this episode: each scripted line is transcribed from its own span of the mix."""
    import soundfile as sf
    setup(pre=False)
    wav = f"{TMP}/linecheck.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", media, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    audio, sr = sf.read(wav, dtype="float32")
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    bad = 0
    for i, ln in enumerate(G["lines"]):
        x = audio[int(max(0, ln["t0"] - 0.15) * sr):int((ln["start"] + ln["dur"] + 0.25) * sr)]
        heard = " ".join(s.text.strip() for s in m.transcribe(x, language="en", beam_size=5,
                                                              condition_on_previous_text=False)[0])
        said = " ".join(w[2] for w in ln["words"])
        r = difflib.SequenceMatcher(None, norm(said).split(), norm(heard).split()).ratio()
        if r < minimum and norm(said).replace(" ", "") == norm(heard).replace(" ", ""):
            r = 1.0   # same letters, split differently ("JesusCoin" / "Jesus coin")
        bad += r < minimum
        print(f"{'OK ' if r >= minimum else 'LOW'} {i + 1:2d} {ln['who']:8s} {r:.2f} | {said} | heard: {heard}", flush=True)
    print("lines under %.2f: %d" % (minimum, bad))
    return bad


def sheet(mp4, out, cols=6):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                             capture_output=True, text=True).stdout)
    setup(pre=False)
    times = sorted(set([0.6] + [min(d - 0.1, ln["start"] + ln["dur"] * 0.5) for ln in G["lines"]] +
                       [min(d - 0.1, G["ev"][k] + dt) for k, dt in (("lid", 1.2), ("hand", 0.6), ("rocket", 1.3), ("feed", 0.4),
                                                                    ("bsod", 0.9), ("chart", 0.6), ("chart", 2.5), ("grab", 0.9),
                                                                    ("cash", 0.6), ("red", 0.6), ("land", 0.3), ("done", 0.6))]))
    tw, th = 270, 480
    rows = math.ceil(len(times) / cols)
    img = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 34) + 8), (30, 30, 30))
    dr = ImageDraw.Draw(img)
    for i, t in enumerate(times):
        p = f"{TMP}/sheet-{i}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", p], check=True)
        x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 34)
        img.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        dr.text((x + 4, y + th + 4), f"{t:.1f}s", font=font(22), fill=(240, 240, 240))
    img.save(out, quality=88)
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--timeline", action="store_true")
    ap.add_argument("--linecheck")
    ap.add_argument("--sheet")
    ap.add_argument("--sheet-out")
    a = ap.parse_args()
    if a.timeline:
        timeline()
    elif a.linecheck:
        sys.exit(linecheck(a.linecheck))
    elif a.sheet:
        sheet(a.sheet, a.sheet_out or a.sheet.rsplit(".", 1)[0] + "-sheet.jpg")
    elif a.still:
        stills(a.still)
    else:
        render(a.out)
