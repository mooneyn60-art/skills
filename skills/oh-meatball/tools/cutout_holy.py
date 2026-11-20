#!/usr/bin/env python3
"""Cutout episode 2: HOLY BLACK FRIDAY (script: side-hustles/channels/scripts/cutout-holy-black-friday.md).

Built on cutout2.py (paper kit, the kid cast and Grandma, voices, captions, cameras, the shared state G) with its
own scenes, characters, gags and mix. Everything is original: PASTOR CHAD (a fictional TV preacher), UNCLE RICK,
cousins KAYLEE and BRAD, the stage, the church, the store name MEGAMART, all music and sound effects.
The jokes land on Rick and Chad (the bigot, the scammer); Rick's cut-off joke is never finished.

  python3 tools/cutout_holy.py --fmt vertical|wide --out file.mp4
  python3 tools/cutout_holy.py --fmt vertical --still 10 42 ...
  python3 tools/cutout2.py --sheet file.mp4 --times ...            (sheets)
  python3 tools/linecheck.py --script holy file.mp4                (per-line voice check)
"""
import argparse
import math
import os
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout as C  # noqa: E402
import cutout2 as C2  # noqa: E402
from cutout import FONT, INK, WHITE, PUPIL, MOUTH, ell, strip, lumpy, paper, render_shapes, add, ks, hz  # noqa
from cutout import kick, snare, strum, jingle_bar, sfx_slap, BEAT, SR, FPS, OUT_FPS, TMP  # noqa
from cutout2 import paste, Cam, G  # noqa: E402

C2.V.update({"chad": "kokoro:chad@speed=1.1,pause=0.25", "rick": "kokoro:rick@speed=1.08,pause=0.3",
             "kaylee": "kokoro:kaylee@speed=1.15,pause=0.2", "brad": "kokoro:brad@speed=1.25,pause=0.18"})
TABLE = ("rick", "kaylee", "pip", "mb", "dot", "brad", "grandma")
KIDS = ("pip", "mb", "dot")
RIGS = ("rick", "kaylee", "brad", "chad")


def L_(o, **k):
    return dict(o, **k)


SEQ_HOLY = [   # SHORT (~63 s): side-hustles/channels/scripts/cutout-holy-black-friday-short.md
    ("gag", "intro", 2.4, "table", "wide"),
    ("line", "rick", "I'm not racist. I've got plenty of Black friends.", None,
     dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
    ("line", "pip", "Name one.", None,
     dict(scene="table", cams=[(0, "cu_pip")], gap=0.0, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
    ("hold", 1.4, "cu_rick"),
    ("line", "rick", "Black Friday.", "...Black Friday.", dict(scene="table", cams=[(0, "cu_rick")], gap=0.25)),
    ("line", "dot", "That's a sale, Rick. You're friends with a sale.", None,
     dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 1.0, "cu_rick"),
    ("line", "rick", "Okay, here's a good one. So a guy from Mexico, a guy from China and a...", None,
     dict(scene="table", cams=[(0, "cu_rick"), (5, "wide_all")], gap=0.0)),
    ("gag", "gravy", 2.0, "table", "wide_all"),
    ("line", "grandma", "Not at my table, Richard.", None, dict(scene="table", cams=[(0, "cu_grandma")], gap=0.0)),
    ("hold", 1.0, "cu_dot"),
    ("line", "kaylee", "I don't take medicine, besties. I manifest.", None,
     dict(scene="table", cams=[(0, "cu_kaylee")], gap=0.2)),
    ("line", "dot", "You manifested a rash, Kaylee. It's on your face.", None,
     dict(scene="table", cams=[(0, "cu_dot"), (3, "cu_kaylee")], gap=0.0)),
    ("hold", 1.1, "cu_kaylee"),
    ("line", "grandma", "Bradley, you lost your house on a coin named after a dog.", None,
     dict(scene="table", cams=[(0, "cu_grandma"), (7, "coin/wide")], gap=0.0)),
    ("hold", 0.9, "coin/wide"),
    ("hold", 1.0, "table/cu_brad"),
    ("gag", "tvon", 1.5, "table", "cu_tv"),
    ("line", "chad", "The Lord told me I need a fourth jet. And He said you should pay for it.", None,
     dict(scene="studio", cams=[(0, "wide"), (2, "cu_chad")], gap=0.2)),
    ("line", "dot", "God talks to you a lot for a guy with three DUIs.", None,
     dict(scene="table", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 1.0, "studio/cu_chad"),
    ("line", "chad", "Jesus turned water into wine. I turn your grandma's pension into a sports car.", None,
     dict(scene="studio", cams=[(0, "cu_chad")], gap=0.2)),
    ("line", "grandma", "Over my dead body.", None, dict(scene="table", cams=[(0, "cu_grandma")], gap=0.2)),
    ("line", "chad", "That's the premium package, ma'am.", None,
     dict(scene="studio", cams=[(0, "cu_chad")], gap=0.0)),
    ("hold", 1.2, "cu_chad"),
    ("gag", "cops", 1.6, "lot", "wide"),
    ("line", "chad", "This isn't fraud! It's a miracle with paperwork!", None,
     dict(scene="lot", cams=[(0, "cu_chad")], gap=0.0)),
    ("hold", 1.2, "cu_chad"),
    ("gag", "dawn", 1.2, "dawn", "wide"),
    ("line", "mb", "Happy Thanksgiving. Somebody pass the damn pie.", None,
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.8)),
    ("gag", "end", 3.2, "dawn", "wide"),
]
def _l(who, text, scene, cam=None, gap=0.08, cap=None):
    return ("line", who, text, cap, dict(scene=scene, cams=[(0, cam or "cu_" + who)], gap=gap))


SEQ_HOLY_V4 = [   # Studio 11/20 rules: side-hustles/channels/scripts/cutout-holy-black-friday-v4.md
    ("gag", "intro", 2.2, "table", "wide"),
    _l("rick", "I'm not racist. I've got plenty of Black friends.", "table", gap=0.15),
    ("line", "pip", "Name one.", None,
     dict(scene="table", cams=[(0, "cu_pip")], gap=0.0, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
    ("hold", 0.9, "cu_rick"),
    ("line", "rick", "Black Friday.", "...Black Friday.", dict(scene="table", cams=[(0, "cu_rick")], gap=0.2)),
    _l("dot", "That's a sale, Rick. And even the sale won't sit with you.", "table", gap=0.0),
    ("hold", 0.4, "cu_rick"),
    ("line", "rick", "Here's a good one. A guy from Mexico, a guy from China and a...", None,
     dict(scene="table", cams=[(0, "cu_rick"), (4, "wide_all")], gap=0.0)),
    ("gag", "gravy", 1.6, "table", "wide_all"),
    _l("grandma", "Not at my table, jackass.", "table", gap=0.0, cap="Not at my table, jack#@s."),
    ("hold", 0.4, "cu_dot"),
    ("gag", "tvon", 1.2, "table", "cu_tv"),
    ("line", "chad", "The Lord told me I need a fourth jet. And He said you're paying.", None,
     dict(scene="studio", cams=[(0, "wide"), (2, "cu_chad")], gap=0.1)),
    _l("chad", "Basic prayer, nine ninety-nine. Premium, He actually hears it.", "studio"),
    _l("dot", "God talks to you a lot for a guy with three D U I's.", "table", gap=0.0,
       cap="God talks to you a lot for a guy with three DUIs."),
    _l("chad", "My church seats sixteen thousand!", "studio"),
    _l("dot", "Joel Osteen called. He wants his teeth back.", "table"),
    _l("mb", "Even the Vatican thinks that's too much gold, Chad. And they have a damn bank.", "table", gap=0.0,
       cap="Even the Vatican thinks that's too much gold, Chad. And they have a d#@n bank."),
    _l("chad", "Platinum plan: I turn your grandma's pension into my sports car. Live.", "studio"),
    _l("grandma", "Over my dead body.", "table"),
    _l("chad", "That's the Diamond plan, ma'am. I do the funeral and keep the casket.", "studio", gap=0.0),
    ("gag", "cops", 1.3, "lot", "wide"),
    _l("chad", "This isn't fraud! It's a miracle with paperwork!", "lot", gap=0.0),
    ("gag", "dawn", 0.9, "dawn", "wide"),
    ("line", "pip", "Who called the cops?", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.2,pause=0.14")),
    _l("grandma", "Forty years a church treasurer. I know a bullshit collection plate when I see one.", "dawn",
       cap="Forty years a church treasurer. I know a bulls#@t collection plate when I see one."),
    _l("dot", "The feds give you a reward?", "dawn"),
    _l("grandma", "Ten percent. I kept the damn jet.", "dawn", gap=0.0, cap="Ten percent. I kept the d#@n jet."),
    ("hold", 0.3, "cu_mb"),
    _l("mb", "Happy Thanksgiving. Grandma's flying us to Denny's.", "dawn", gap=0.5),
    ("gag", "end", 2.8, "dawn", "wide"),
]
ACTIVE = [SEQ_HOLY]
# Lines 14a's sign: the script's line text is the spoken part only.
END_TEXT = ["WHO'S THE WORST PERSON", "AT YOUR", "THANKSGIVING TABLE?"]


# ------------------------------------------------------------------------------------------------ layout
def layout(fmt):
    if fmt == "wide":
        K, F = 1.0, 1010
        xs = dict(rick=170, kaylee=450, pip=720, mb=960, dot=1200, brad=1470, grandma=1760)
        return dict(W=1920, H=1080, K=K, feet=F, cu=2.2, cap_y=935, cap_size=74, banner_y=230,
                    table=dict(x=xs, top=F - 170, tv=(1690, 250), window=(500, 240), x0=-200, x1=2120),
                    studio=dict(chad=(760, F), tv=(1480, F - 246), panel=(1180, 90, 1850, 330)),
                    lot=dict(chad=(820, F), grandma=(600, F), x=dict(rick=1110, pip=1340, mb=1560, dot=1780),
                             door=820, car=(1450, F + 130)),
                    wide_table=(960, 600, 1.0), wide_lot=(960, 560, 1.0))
    K, F = 1.28, 1640
    xs = dict(rick=40, kaylee=330, pip=610, mb=880, dot=1150, brad=1420, grandma=1690)
    return dict(W=1080, H=1920, K=K, feet=F, cu=1.85, cap_y=1470, cap_size=84, banner_y=380,
                table=dict(x=xs, top=F - 170 * K, tv=(1180, 720), window=(560, 720), x0=-500, x1=2300),
                studio=dict(chad=(380, F), tv=(830, F - 246), panel=(60, 180, 1020, 520)),
                lot=dict(chad=(420, F), grandma=(200, F), x=dict(rick=660, pip=900, mb=1140, dot=1380),
                         door=420, car=(760, F + 230)),
                wide_table=(880, 1250, 0.9), wide_lot=(760, 1260, 0.72))


def cams(L):
    K, F, vert = L["K"], L["feet"], L["H"] > L["W"]
    z = L["cu"]
    out = {}
    t = {"wide": L["wide_table"],   # wide_all: the whole table, Rick to Grandma (the gravy throw)
         "wide_all": (865, 1180, 0.56) if vert else L["wide_table"]}
    for c, x in L["table"]["x"].items():
        h = {"grandma": 150, "rick": 300}.get(c, 270)
        t["cu_" + c] = (x, F - h * K, z * (1.15 if c == "grandma" else 1.0))
    tx, ty = L["table"]["tv"]
    t["cu_tv"] = (tx, ty + 10, 2.4 if not vert else 1.9)
    out["table"] = t
    out["dawn"] = dict(t)
    cx, cy = L["studio"]["chad"]
    out["studio"] = {"wide": (L["W"] / 2, L["H"] / 2, 1.0), "cu_chad": (cx, F - 330 * K, z * 0.95)}
    lo = L["lot"]
    lt = {"wide": L["wide_lot"], "cu_chad": (lo["chad"][0], F - 340 * K, z * 0.95),
          "cu_grandma": (lo["grandma"][0], F - 150 * K, z * 1.15)}
    for c, x in lo["x"].items():
        lt["cu_" + c] = (x, F - (300 if c == "rick" else 270) * K, z)
    out["lot"] = lt
    for sc in ("tag", "selfie", "coin", "jessica"):
        out[sc] = {"wide": (L["W"] / 2, L["H"] / 2, 1.0)}
    return out


# ------------------------------------------------------------------------------------------------ characters
SKIN_T, SUN, GOLD, GOLD_DK = (236, 190, 150), (232, 128, 104), (226, 184, 56), (186, 146, 34)
PASTEL, BLONDE, VEST, NAVY = (206, 178, 232), (246, 214, 120), (40, 54, 92), (60, 70, 110)

RIG = {
    "chad": dict(neck=(0, -250), sh=((-70, -236), (70, -236)), arm_len=96, arm_col=GOLD, hand=SKIN_T),
    "rick": dict(neck=(0, -250), sh=((-84, -232), (84, -232)), arm_len=92, arm_col=SUN, hand=SUN),
    "kaylee": dict(neck=(0, -226), sh=((-54, -214), (54, -214)), arm_len=84, arm_col=PASTEL, hand=(246, 206, 180)),
    "brad": dict(neck=(0, -240), sh=((-60, -228), (60, -228)), arm_len=88, arm_col=(170, 200, 230), hand=SKIN_T),
}


def body_shapes(c):
    if c == "chad":
        return [("p", [(-36, -80), (-6, -80), (-8, -12), (-34, -12)], GOLD_DK),
                ("p", [(6, -80), (36, -80), (34, -12), (8, -12)], GOLD_DK),
                ("e", (-26, -8, 30, 12), WHITE), ("e", (26, -8, 30, 12), WHITE),
                ("p", [(-72, -250), (72, -250), (86, -70), (-86, -70)], GOLD),
                ("p", [(-26, -250), (26, -250), (0, -150)], WHITE),
                ("p", [(-6, -244), (6, -244), (10, -160), (0, -150), (-10, -160)], (200, 40, 32)),
                ("p", [(-30, -250), (-6, -250), (-36, -150)], GOLD_DK),
                ("p", [(30, -250), (6, -250), (36, -150)], GOLD_DK),
                ("p", [(40, -200), (66, -200), (64, -184), (42, -184)], (200, 40, 32), False)]
    if c == "rick":
        return [("p", [(-40, -80), (-8, -80), (-10, -12), (-38, -12)], (70, 100, 160)),
                ("p", [(8, -80), (40, -80), (38, -12), (10, -12)], (70, 100, 160)),
                ("e", (-26, -8, 32, 13), (110, 70, 40)), ("e", (26, -8, 32, 13), (110, 70, 40)),
                ("e", (0, -150, 100, 100), (244, 240, 230)),
                ("p", [(-56, -250), (56, -250), (80, -150), (-80, -150)], (244, 240, 230)),
                ("p", [(-40, -250), (-20, -250), (-10, -220), (-34, -220)], SUN, False),
                ("p", [(-80, -84), (80, -84), (82, -66), (-82, -66)], (90, 70, 50))]
    if c == "kaylee":
        return [("p", [(-30, -70), (-6, -70), (-8, -10), (-28, -10)], (150, 120, 190)),
                ("p", [(6, -70), (30, -70), (28, -10), (8, -10)], (150, 120, 190)),
                ("e", (-22, -8, 26, 11), WHITE), ("e", (22, -8, 26, 11), WHITE),
                ("p", [(-56, -226), (56, -226), (66, -64), (-66, -64)], PASTEL),
                ("p", [(-20, -226), (20, -226), (0, -196)], (176, 146, 210))]
    if c == "brad":
        return [("p", [(-34, -76), (-6, -76), (-8, -12), (-32, -12)], (180, 170, 150)),
                ("p", [(6, -76), (34, -76), (32, -12), (8, -12)], (180, 170, 150)),
                ("e", (-24, -8, 30, 12), (120, 80, 50)), ("e", (24, -8, 30, 12), (120, 80, 50)),
                ("p", [(-60, -240), (60, -240), (72, -70), (-72, -70)], (170, 200, 230)),
                ("p", [(-62, -236), (-14, -236), (-22, -74), (-74, -74)], VEST),
                ("p", [(14, -236), (62, -236), (74, -74), (22, -74)], VEST),
                ("p", strip([(-66, -190), (-18, -190)], 4), (70, 84, 124), False),
                ("p", strip([(-70, -140), (-20, -140)], 4), (70, 84, 124), False),
                ("p", strip([(18, -190), (66, -190)], 4), (70, 84, 124), False),
                ("p", strip([(20, -140), (70, -140)], 4), (70, 84, 124), False)]
    raise KeyError(c)


def head_shapes(c, lvl, blink, expr, extra):
    """Shapes around the neck pivot. extra: frozenset of flags (rash, gravy, hat, glare)."""
    s = []
    if c == "chad":
        cy = -112
        s += [("e", (-100, cy, 18, 26), SKIN_T), ("e", (100, cy, 18, 26), SKIN_T),
              ("e", (0, cy, 100, 112), SKIN_T),
              ("pts", ell(0, cy - 30, 104, 92, 185, 355) + [(110, cy - 40), (60, cy - 70), (-20, cy - 60),
                                                             (-90, cy - 46)], (64, 42, 30)),
              ("pts", [(-60, cy - 112), (40, cy - 136), (110, cy - 100), (60, cy - 108), (-10, cy - 96)], (64, 42, 30)),
              ("p", strip([(-30, cy - 108), (40, cy - 124)], 6), (200, 180, 160), False)]
        for side in (-1, 1):
            ex = side * 38
            if blink:
                s.append(("p", strip([(ex - 18, cy - 12), (ex + 18, cy - 12)], 5), INK, False))
            else:
                s += [("e", (ex, cy - 14, 20, 24), WHITE), ("e", (ex, cy - 10, 8, 8), PUPIL, False)]
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
        s.append(("p", strip([(100, cy), (96, cy + 50), (60, top + 6)], 5), (30, 30, 30), False))   # headset
        s.append(("e", (56, top + 6, 8, 8), (30, 30, 30), False))
        if "hat" in extra:   # the big white hat (parking lot)
            s += [("e", (0, cy - 96, 170, 30), (250, 248, 240)),
                  ("pts", ell(0, cy - 110, 96, 100, 180, 360) + [(96, cy - 104)], (250, 248, 240)),
                  ("p", [(-94, cy - 130), (94, cy - 130), (96, cy - 108), (-96, cy - 108)], GOLD, False)]
        return s
    if c == "rick":
        cy = -108
        s += [("e", (0, cy, 106, 104), SUN)]
        for (x, y) in [(-50, 40), (-34, 52), (-60, 58), (40, 44), (56, 54), (30, 58), (-10, 62), (10, 64)]:
            s.append(("e", (x, cy + y, 3, 3), (150, 70, 60), False))
        lids = 1.0 if blink else (0.45 if expr != "wide" else 0.0)
        s += C.eyes(0, cy - 4, 34, 22, 20, "l" if expr == "l" else "c", "norm", lids, SUN, 6 if expr != "wide" else 18,
                    (120, 70, 40))
        s.append(("e", (0, cy + 18, 14, 10), (210, 100, 84), False))
        s += C.mouth(0, cy + 60, lvl, 38, "frown", "oval")
        s.append(("pts", strip([(-46, cy + 66), (-40, cy + 38), (0, cy + 34), (40, cy + 38), (46, cy + 66)], 14),
                  (120, 80, 50)))   # horseshoe moustache
        # trucker hat: white front panel with a generic flag patch, red mesh back, bill
        s += [("pts", ell(0, cy - 40, 110, 84, 180, 360) + [(110, cy - 36)], (200, 52, 44)),
              ("pts", ell(-6, cy - 46, 74, 78, 180, 360) + [(68, cy - 42)], (250, 248, 240)),
              ("p", [(-120, cy - 50), (60, cy - 50), (80, cy - 34), (-128, cy - 30)], (170, 40, 36))]
        fx, fy = -12, cy - 92
        s.append(("p", [(fx - 30, fy - 18), (fx + 30, fy - 18), (fx + 30, fy + 18), (fx - 30, fy + 18)], WHITE))
        for k in range(3):
            y = fy - 18 + k * 12 + 2
            s.append(("p", [(fx - 30, y), (fx + 30, y), (fx + 30, y + 5), (fx - 30, y + 5)], (200, 52, 44), False))
        s.append(("p", [(fx - 30, fy - 18), (fx - 6, fy - 18), (fx - 6, fy + 2), (fx - 30, fy + 2)], (40, 60, 140),
                  False))
        if "gravy" in extra:
            s += [("pts", lumpy(0, cy - 110, 70, [(8, 5, 0), (5, 9, 1)]), (120, 76, 40)),
                  ("e", (-50, cy - 40, 12, 22), (120, 76, 40)), ("e", (40, cy - 30, 10, 26), (120, 76, 40)),
                  ("e", (8, cy - 20, 8, 18), (120, 76, 40))]
        return s
    if c == "kaylee":
        cy = -100
        s += [("pts", lumpy(0, cy - 60, 70, [(6, 7, 0)]), BLONDE),
              ("e", (0, cy - 150, 34, 40), BLONDE), ("e", (0, cy - 118, 26, 12), (236, 140, 180)),   # high ponytail
              ("e", (0, cy, 96, 98), (246, 206, 180)),
              ("pts", ell(0, cy - 20, 100, 82, 180, 360) + [(96, cy - 10), (40, cy - 50), (-40, cy - 50),
                                                             (-96, cy - 10)], BLONDE)]
        if "rash" in extra:
            for (x, y, r) in [(-56, 30, 20), (-40, 56, 14), (52, 34, 22), (36, 62, 12), (-6, 74, 12), (70, 6, 10)]:
                s.append(("pts", lumpy(x, cy + y, r, [(3, 5, x)]), (226, 82, 90)))
        # giant sunglasses, indoors
        for side in (-1, 1):
            s += [("e", (side * 40, cy + 4, 42, 32), (24, 24, 28)), ("e", (side * 52, cy - 8, 10, 6), (140, 140, 160),
                                                                         False)]
        s.append(("p", strip([(-4, cy), (4, cy)], 6), (24, 24, 28), False))
        if "glare" in extra:
            s.append(("pts", [(40 + 24 * math.cos(a * math.pi / 4) * (1 if a % 2 else 0.35),
                               cy - 2 + 24 * math.sin(a * math.pi / 4) * (1 if a % 2 else 0.35)) for a in range(8)],
                      (255, 255, 240), False))
        if expr == "duck" and lvl == 0:
            s.append(("e", (0, cy + 56, 22, 14), (220, 100, 130)))
        else:
            s += C.mouth(0, cy + 56, lvl, 32, "flat", "oval")
            if lvl == 0:
                s.append(("e", (0, cy + 57, 18, 5), (220, 100, 130), False))
        return s
    if c == "brad":
        cy = -104
        s += [("e", (-92, cy + 4, 14, 22), SKIN_T), ("e", (92, cy + 4, 14, 22), SKIN_T),
              ("e", (-92, cy + 10, 7, 8), WHITE, False), ("e", (92, cy + 10, 7, 8), WHITE, False),   # earbuds
              ("e", (0, cy, 92, 100), SKIN_T),
              ("pts", ell(0, cy - 34, 96, 72, 180, 360) + [(96, cy - 30), (-70, cy - 36)], (50, 36, 30)),
              ("pts", [(-80, cy - 70), (30, cy - 110), (100, cy - 74), (20, cy - 84)], (50, 36, 30)),
              ("p", strip([(-40, cy - 84), (30, cy - 100)], 5), (150, 130, 120), False)]
        lids = 1.0 if blink else 0.38
        s += C.eyes(0, cy + 6, 32, 22, 22, "c", "norm", lids, SKIN_T, -6, (50, 36, 30))
        s.append(("e", (0, cy + 26, 10, 9), (214, 168, 130), False))
        s += C.mouth(6, cy + 62, lvl, 34, "smirk", "grin")
        return s
    raise KeyError(c)


def arm_shapes(c):
    k = RIG[c]
    Ln = k["arm_len"]
    return [("p", [(-13, -6), (13, -6), (14, Ln), (-14, Ln)], k["arm_col"]),
            ("e", (0, Ln + 15, 23, 21), k["hand"]), ("e", (18, Ln + 5, 9, 12, 0, 360, None, -30), k["hand"])]


@lru_cache(maxsize=768)
def rspr(c, part, z, *key):
    if part == "body":
        return render_shapes(body_shapes(c), z, 300, 200 + RIGS.index(c))
    if part == "arm":
        return render_shapes(arm_shapes(c), z, 140, 210 + RIGS.index(c))
    return render_shapes(head_shapes(c, *key), z, 330, 220 + RIGS.index(c))


@lru_cache(maxsize=256)
def prop(name, z, *key):
    if name == "pie":
        return render_shapes([("e", (0, 0, 90, 30), (214, 160, 90)), ("e", (0, -4, 76, 22), (178, 92, 60)),
                              ("p", strip([(-60, -10), (60, 2)], 8), (226, 180, 110), False),
                              ("p", strip([(-50, 8), (50, -12)], 8), (226, 180, 110), False),
                              ("e", (0, 18, 100, 14), (250, 250, 246))], z, 120, 300)
    if name == "slice":
        return render_shapes([("p", [(-30, -20), (30, -24), (0, 40)], (178, 92, 60)),
                              ("p", strip([(-32, -20), (32, -24)], 12), (226, 180, 110))], z, 60, 301)
    if name == "phone":
        img = render_shapes([("p", [(-18, -40), (18, -40), (18, 40), (-18, 40)], (40, 40, 46)),
                             ("p", [(-13, -32), (13, -32), (13, 28), (-13, 28)], (140, 200, 240), False)], z, 60, 302)
        return img
    if name == "juice":
        img = render_shapes([("p", [(-18, -40), (18, -40), (20, 50), (-20, 50)], (120, 200, 100)),
                             ("p", [(-10, -60), (10, -60), (10, -40), (-10, -40)], (250, 250, 246)),
                             ("p", [(10, -10), (66, -18), (70, 14), (14, 20)], WHITE)], z, 90, 303)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c + 40 * z, c), "$70", font=ImageFont.truetype(FONT, max(6, int(20 * z))), fill=(200, 40, 32),
               anchor="mm")
        return img
    if name == "sign":   # protest-style board on a stick
        img = render_shapes([("p", strip([(0, 0), (0, 200)], 12), (170, 130, 80)),
                             ("p", [(-160, -110), (160, -116), (164, 20), (-156, 26)], (250, 248, 240))], z, 220, 304)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        f = ImageFont.truetype(FONT, max(6, int(40 * z)))
        d.text((c, c - 66 * z), "GOD HATES", font=f, fill=(200, 40, 32), anchor="mm")
        d.text((c, c - 20 * z), "TAXES", font=f, fill=(200, 40, 32), anchor="mm")
        return img
    if name == "gravyboat":
        return render_shapes([("pts", ell(0, 0, 60, 26, 0, 180) + [(70, -16), (-60, 0)], (250, 250, 246)),
                              ("e", (0, -2, 50, 8), (120, 76, 40), False),
                              ("p", strip([(-60, 0), (-80, -10), (-74, 14)], 7), (250, 250, 246))], z, 100, 305)
    if name == "turkey":
        return render_shapes([("pts", lumpy(0, -60, 110, [(8, 3, 0), (6, 7, 1)]), (70, 40, 26)),
                              ("e", (-30, -100, 40, 22), (90, 52, 30), False),
                              ("p", strip([(-100, -40), (-150, -70)], 26), (60, 34, 22)),
                              ("p", strip([(100, -40), (150, -70)], 26), (60, 34, 22)),
                              ("e", (-160, -76, 16, 13), (246, 240, 226)), ("e", (160, -76, 16, 13), (246, 240, 226)),
                              ("e", (0, 0, 170, 20), (250, 250, 246))], z, 220, 306)
    if name == "chair":   # Rick's folding chair, behind him
        return render_shapes([("p", strip([(-70, 0), (60, -220)], 12), (150, 150, 160)),
                              ("p", strip([(70, 0), (-60, -220)], 12), (150, 150, 160)),
                              ("p", [(-80, -220), (80, -220), (84, -300), (-84, -300)], (60, 100, 70)),
                              ("p", [(-90, -110), (90, -110), (92, -90), (-92, -90)], (60, 100, 70))], z, 330, 307)
    if name == "check":
        img = render_shapes([("p", [(-60, -26), (60, -30), (62, 26), (-58, 30)], (230, 246, 230))], z, 80, 308)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c, c), "PAY CHAD", font=ImageFont.truetype(FONT, max(6, int(14 * z))), fill=(60, 120, 60),
               anchor="mm")
        return img
    if name == "car":
        img = render_shapes([("p", [(-260, -120), (260, -120), (280, 0), (-280, 0)], (246, 246, 246)),
                             ("p", [(-160, -200), (140, -200), (190, -120), (-210, -120)], (246, 246, 246)),
                             ("p", [(-140, -190), (120, -190), (160, -126), (-180, -126)], (140, 180, 220), False),
                             ("p", [(-280, -70), (280, -70), (280, -40), (-280, -40)], (40, 60, 140), False),
                             ("p", [(-60, -226), (0, -226), (0, -204), (-60, -204)], (220, 40, 40)),
                             ("p", [(0, -226), (60, -226), (60, -204), (0, -204)], (40, 80, 230)),
                             ("e", (-170, 0, 50, 50), (40, 40, 46)), ("e", (170, 0, 50, 50), (40, 40, 46))], z, 320, 309)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c, c - 90 * z), "POLICE", font=ImageFont.truetype(FONT, max(6, int(34 * z))), fill=(40, 60, 140),
               anchor="mm")
        return img
    if name == "people":   # the line of check-holders (back of the lot)
        k = key[0]
        return C2.spr("shopper", z, k % 6)
    raise KeyError(name)


# ------------------------------------------------------------------------------------------------ poses
def lines_with(text, who=None):
    return [l_ for l_ in G["lines"] if text in " ".join(w[2] for w in l_["words"]) and (who is None or l_["who"] == who)]


def word_t(ln, prefix, default=None):
    for w in ln["words"]:
        if w[2].startswith(prefix):
            return w[0]
    return default


def pose(c, t, fi, li, scene):
    """Generic pose (the cutout2 tuple) + per-gag overrides for any table/lot/dawn character."""
    lines, ev = G["lines"], G["ev"]
    rng = np.random.default_rng(fi * 31 + hash(c) % 997)
    ln = lines[li] if li is not None else None
    spk = ln is not None and (ln["who"] == c or (ln["who"] == "all" and c in KIDS) or c in ln["who"].split("+"))
    base = {"mb": "norm", "pip": "worried", "dot": "deadpan", "rick": "norm", "kaylee": "norm", "brad": "smug",
            "chad": "norm"}.get(c, "norm")
    lvl, hop, aL, aR, expr, ang = 0, 0.0, -12.0, 12.0, base, 0.0
    jit = {"pip": 2.2, "mb": 1.2, "dot": 0.6}.get(c, 1.0)
    extra = {"fi": fi}
    if t < C2.GD.get("intro", 2.9):
        beat = int(t / BEAT)
        if beat % 3 == hash(c) % 3 and (t % BEAT) < 0.17:
            hop = -14
    say = " ".join(w[2] for w in ln["words"]) if ln is not None else ""
    if spk:
        lvl = C2.mouth_level(ln, t)
        wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
        if t - ln["words"][wi][0] < 0.09 and t >= ln["start"]:
            hop = -10 if c != "dot" else -4
        poses = [(-20, 30), (-30, 150), (-15, 100), (-120, 120), (-60, 60), (-25, 135)]
        if c == "dot":
            poses = [(-10, 10), (-12, 12), (-10, 70), (-10, 10)]
        aL, aR = poses[(wi * 7 + li) % len(poses)]
        ang = float(rng.uniform(-3.5, 3.5)) if c != "dot" else float(rng.uniform(-1, 1))
        jit *= 1.6
    else:
        ang = float(rng.uniform(-1, 1))
    xs = place(scene)
    gaze = "c"
    if ln is not None and not spk and ln["who"] in xs and c in xs:
        gaze = "l" if xs[ln["who"]] < xs[c] else "r"
    if ln is not None and ln["who"] in ("chad",) and scene == "table":
        gaze = "r" if c != "grandma" else "u"   # everyone looks at the TV
    # ---- gag overrides
    if c == "rick" and lines_with("Jessica gets", "rick") and spk and "Jessica gets" in say:
        aR, extra["item"] = 150, ("phone", "R", 0)
    if c == "rick" and "dial" in ev and ev["dial"] <= t and lines_with("man of God", "rick") and \
            t < lines_with("man of God", "rick")[0]["start"] + lines_with("man of God", "rick")[0]["dur"]:
        aR, extra["item"] = 150, ("phone", "R", 0)
    if c == "rick" and spk and ("long pause" in say or say.startswith("...")):
        pass
    if c == "kaylee":
        if lines_with("celery", "kaylee") and spk and "celery" in say:
            aR, extra["item"] = 130, ("juice", "R", 0)
        if (fi // 3) % 7 == 0 and scene == "table":
            extra["glare"] = True
        rash = lines_with("rash", "dot")
        if rash and t >= word_t(rash[0], "rash", 1e9):
            extra["rash"] = True
        if lines_with("Bali", "kaylee") and spk and "Bali" in say:
            aL, aR = -150, 150   # namaste-ish arms up
    if c == "brad" and spk:
        aR = 95   # bro point
    if c == "rick":
        gv = ev.get("gravy")
        if gv is not None and t >= gv + 0.45:
            extra["gravy"] = True
        if lines_with("I don't even see", "rick") and spk and "see color" in say:
            expr = "smug"
    if c == "mb" and spk and ("shipped" in say or "scam bots" in say or "laxative" in say):
        expr = "smug"
    if c == "pip" and spk and "Name one" in say:
        expr, aL, aR = "norm", -12, 12
    if c == "rick" and li is None and scene == "table":   # long pauses: dead still, blinking
        for nm in ("That's a lie", "Black Friday."):
            ll = lines_with(nm, "rick")
            if ll and ll[0]["t0"] - 1.05 <= t < ll[0]["t0"]:
                jit, ang, expr = 0.0, 0.0, "norm"
    if scene == "dawn":
        aR, extra["item"] = 140, ("slice", "R", 0)
        if spk:
            aR = 150
    blink = (int(t * FPS) + hash(c) % 37) % 41 == 0
    if c in RIGS:
        hk = (lvl, blink, expr if expr in ("wide", "smug", "duck") else ("l" if gaze == "l" else "norm"),
              frozenset(k for k in ("rash", "gravy", "hat", "glare") if extra.get(k)))
    else:
        hk = (lvl, gaze, blink, expr)
    return (hop, (float(rng.uniform(-jit, jit)), float(rng.uniform(-jit, jit))), ang, (aL, aR), hk, 1.0, 0.0,
            extra)


def place(scene):
    L = G["L"]
    if scene in ("table", "dawn"):
        return L["table"]["x"]
    if scene == "lot":
        d = dict(L["lot"]["x"])
        d["chad"] = L["lot"]["chad"][0]
        d["grandma"] = L["lot"]["grandma"][0]
        return d
    if scene == "studio":
        return {"chad": L["studio"]["chad"][0]}
    return {}


def compose_rig(c, z, p):
    hop, (jx, jy), ang, (aL, aR), hk, squash, rot, extra = p
    k = RIG[c]
    S = int(2 * 600 * z)
    im = Image.new("RGBA", (S, S))
    o = S / 2
    if c == "rick" and G.get("scene") in ("table", "dawn"):
        paste(im, prop("chair", z), o - 30 * z, o + 10 * z)
    paste(im, rspr(c, "body", z), o, o)
    held = []
    for (sx, sy), a in zip(k["sh"], (aL, aR)):
        paste(im, rspr(c, "arm", z), o + sx * z, o + sy * z, a)
        it = extra.get("item")
        if it and ((it[1] == "L") == (sx < 0)):
            Ln = k["arm_len"] + 30
            held.append((it, o + (sx + Ln * math.sin(math.radians(a))) * z,
                         o + (sy + Ln * math.cos(math.radians(a))) * z))
    paste(im, rspr(c, "head", z, *hk), o + (k["neck"][0] + jx) * z, o + (k["neck"][1] + jy) * z, ang)
    for it, hx, hy in held:
        paste(im, prop(it[0], z), hx, hy - 30 * z, it[2])
    if extra.get("cuffs"):
        d = ImageDraw.Draw(im)
        for dx in (-16, 16):
            x, y = o + dx * z, o - 120 * z
            d.ellipse((x - 14 * z, y - 14 * z, x + 14 * z, y + 14 * z), outline=(150, 150, 160), width=max(2, int(6 * z)))
    return im


def draw_rig(fr, cam, c, x, y, p, scale=1.0):
    K = G["L"]["K"]
    z = round(cam.z * K * scale, 3)
    im = compose_rig(c, z, p)
    if p[6]:
        im = im.rotate(p[6], resample=Image.BICUBIC)
    px, py = cam.p(x, y + p[0] * K)
    paste(fr, im, px, py)


def draw_any(fr, cam, c, x, y, p):
    if c in KIDS:
        C2.draw_kid(fr, cam, c, x, y, p)
    elif c == "grandma":
        hop, (jx, jy), ang, (aL, aR), hk, _, rot, extra = p
        C2.draw_granny(fr, cam, x, y, hk[0], "mean", aL, aR, ang=ang, hop=hop, rot=rot)
    else:
        draw_rig(fr, cam, c, x, y, p)


# ------------------------------------------------------------------------------------------------ backgrounds
def bg_table(L, cam, dawn):
    W, H, z = L["W"], L["H"], cam.z
    S = L["table"]
    rng = np.random.default_rng(81)
    back = Image.new("RGBA", (W, H))
    x0, x1 = S["x0"], S["x1"]
    paper(back, cam.pts([(x0 - 600, -800), (x1 + 600, -800), (x1 + 600, 4000), (x0 - 600, 4000)]), (226, 214, 176),
          rng, z, shadow=False, jitter=False, edge=False)
    for k in range(int((x1 - x0) / 80) + 14):   # wallpaper stripes
        x = x0 - 500 + k * 80
        paper(back, cam.pts([(x, -800), (x + 28, -800), (x + 28, S["top"]), (x, S["top"])]), (210, 196, 152), rng, z,
              shadow=False, jitter=False, edge=False)
    wx, wy = S["window"]
    paper(back, cam.pts([(wx - 160, wy - 130), (wx + 160, wy - 130), (wx + 160, wy + 130), (wx - 160, wy + 130)]),
          (250, 250, 240), rng, z, sh=6)
    sky = (250, 180, 120) if dawn else (30, 40, 80)
    paper(back, cam.pts([(wx - 140, wy - 110), (wx + 140, wy - 110), (wx + 140, wy + 110), (wx - 140, wy + 110)]), sky,
          rng, z, shadow=False)
    if dawn:
        paper(back, cam.pts(ell(wx + 40, wy + 110, 60, 60, 180, 360)), (255, 230, 150), rng, z, shadow=False)
    else:
        paper(back, cam.pts(ell(wx + 60, wy - 50, 26, 26)), (240, 236, 200), rng, z, shadow=False)
    paper(back, cam.pts(strip([(wx, wy - 110), (wx, wy + 110)], 8)), (250, 250, 240), rng, z, shadow=False)
    # the corner TV (screen drawn live)
    tx, ty = S["tv"]
    paper(back, cam.pts([(tx - 160, ty - 120), (tx + 160, ty - 120), (tx + 160, ty + 120), (tx - 160, ty + 120)]),
          (90, 70, 60), rng, z, sh=8)
    paper(back, cam.pts([(tx - 60, ty + 120), (tx + 60, ty + 120), (tx + 80, ty + 240), (tx - 80, ty + 240)]),
          (110, 86, 70), rng, z)
    paper(back, cam.pts(strip([(tx - 40, ty - 120), (tx - 90, ty - 200)], 5)), (60, 60, 60), rng, z, shadow=False)
    paper(back, cam.pts(strip([(tx + 40, ty - 120), (tx + 90, ty - 200)], 5)), (60, 60, 60), rng, z, shadow=False)
    # front: table top, cloth to the floor, plates, the burnt turkey
    front = Image.new("RGBA", (W, H))
    top = S["top"]
    xs = S["x"]
    a, b = xs["kaylee"] - 200, xs["brad"] + 200
    paper(front, cam.pts([(a, top), (b, top), (b + 30, top + 40), (a - 30, top + 40)]), (176, 124, 74), rng, z, sh=6)
    paper(front, cam.pts([(a - 30, top + 30), (b + 30, top + 30), (b + 40, 4000), (a - 40, 4000)]), (240, 236, 226),
          rng, z, sh=8)
    for k in range(int((b - a) / 120) + 1):
        x = a + k * 120
        paper(front, cam.pts([(x, top + 34), (x + 50, top + 34), (x + 56, 4000), (x - 6, 4000)]), (200, 60, 50), rng,
              z, shadow=False)
    for c in ("kaylee", "pip", "mb", "dot", "brad"):
        paper(front, cam.pts(ell(xs[c], top + 6, 70, 16)), (250, 250, 246), rng, z, sh=3)
    K = L["K"]
    tk = (xs["pip"] + xs["mb"]) / 2
    paste(front, prop("turkey", round(z * K * 0.8, 3)), *cam.p(tk, top + 8))
    if not dawn:
        for k in range(3):   # smoke
            paper(front, cam.pts(lumpy(tk - 40 + k * 40, top - 230 - k * 30, 26, [(4, 5, k)])), (150, 150, 150), rng,
                  z, shadow=False)
    return C.vignette(back), front


def bg_studio(L, cam):
    W, H, z = L["W"], L["H"], cam.z
    S = L["studio"]
    rng = np.random.default_rng(91)
    img = Image.new("RGBA", (W, H))
    paper(img, cam.pts([(-600, -600), (W + 600, -600), (W + 600, H + 600), (-600, H + 600)]), (60, 30, 80), rng, z,
          shadow=False, jitter=False, edge=False)
    for k in range(-6, int(W / 90) + 8):   # gold curtain folds
        x = k * 90
        paper(img, cam.pts([(x, -600), (x + 50, -600), (x + 56, L["feet"] - 120), (x - 6, L["feet"] - 120)]),
              (196, 150, 40) if k % 2 else (226, 184, 56), rng, z, shadow=False)
    F = L["feet"]
    paper(img, cam.pts([(-600, F - 120), (W + 600, F - 120), (W + 600, H + 600), (-600, H + 600)]), (150, 110, 30), rng,
          z, sh=8)
    for k in range(-4, 12):
        paper(img, cam.pts(strip([(k * 220, F - 120), (k * 220 - 300, H + 300)], 6)), (120, 86, 20), rng, z,
              shadow=False)
    # spotlight + the neon word
    cx = S["chad"][0]
    paper(img, cam.pts([(cx - 70, -100), (cx + 70, -100), (cx + 320, F + 40), (cx - 320, F + 40)]), (255, 240, 180),
          rng, z, shadow=False, grain=0.03)
    d = ImageDraw.Draw(img)
    nx, ny = (cx, 150) if W > H else (W / 2, 120)
    d.text(cam.p(nx, ny), "BLESSED", font=ImageFont.truetype(FONT, int(96 * z)), fill=(255, 236, 120), anchor="mm",
           stroke_width=max(2, int(8 * z)), stroke_fill=(220, 60, 140))
    x0, y0, x1, y1 = S["panel"]
    paper(img, cam.pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), (24, 24, 30), rng, z, sh=8)
    d.text(cam.p((x0 + x1) / 2, y0 + (y1 - y0) * 0.27), "CALL NOW: 1-800-SOW-SEED",
           font=ImageFont.truetype(FONT, int(min(40, (x1 - x0) / 17) * z)), fill=(255, 220, 90), anchor="mm")
    return C.vignette(img)


def bg_lot(L, cam):
    W, H, z = L["W"], L["H"], cam.z
    S = L["lot"]
    K = L["K"]
    F = L["feet"]
    rng = np.random.default_rng(101)
    img = Image.new("RGBA", (W, H))
    paper(img, cam.pts([(-1200, -1200), (W + 1200, -1200), (W + 1200, H + 1200), (-1200, H + 1200)]), (160, 210, 236),
          rng, z, shadow=False, jitter=False, edge=False)
    g = F - 260 * K
    door = S["door"]
    bx0, bx1 = door - 700 * K, door + 520 * K
    top = g - 620 * K
    paper(img, cam.pts([(bx0, top), (bx1, top), (bx1, g), (bx0, g)]), (236, 230, 214), rng, z, sh=8)
    paper(img, cam.pts([(bx0 + 40, top + 40), (bx1 - 40, top + 40), (bx1 - 40, top + 160 * K), (bx0 + 40, top + 160 * K)]),
          (226, 184, 56), rng, z, sh=6)
    d = ImageDraw.Draw(img)
    d.text(cam.p((bx0 + bx1) / 2, top + 40 + 60 * K), "CHAD'S BLESSING CENTER",
           font=ImageFont.truetype(FONT, int(48 * z * K)), fill=(120, 40, 120), anchor="mm")
    paper(img, cam.pts([(door - 110 * K, g - 300 * K), (door + 110 * K, g - 300 * K), (door + 110 * K, g),
                        (door - 110 * K, g)]), (140, 200, 230), rng, z, sh=5)
    paper(img, cam.pts([(-1200, g), (W + 1200, g), (W + 1200, H + 1200), (-1200, H + 1200)]), (96, 96, 104), rng, z,
          shadow=False)
    for k in range(-6, 14):
        x = k * 260
        paper(img, cam.pts(strip([(x, g + 40), (x - 220, H + 400)], 10)), (240, 240, 240), rng, z, shadow=False)
    # the line of check-holders, back of the lot, receding left
    for k in range(9):
        px = S["grandma"][0] - (170 + k * 120) * K
        sc = max(0.45, 0.82 - k * 0.04) * K
        py = F - 40 - k * 10
        paste(img, C2.spr("shopper", round(z * sc * 0.8, 3), k % 6), *cam.p(px, py))
        paste(img, prop("check", round(z * sc, 3)), *cam.p(px + 100 * sc, py - 330 * sc))
    return C.vignette(img)


def bg_cutaway(L, cam, kind):
    """Paper close-ups: the hat tag, Kaylee's Bali selfie, Brad's coin chart, Rick's 'Jessica' phone."""
    W, H, z = L["W"], L["H"], 1.0
    vert = H > W
    rng = np.random.default_rng(111)
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    if kind == "tag":
        paper(img, [(-20, -20), (W + 20, -20), (W + 20, H + 20), (-20, H + 20)], (200, 52, 44), rng, 1.5, shadow=False,
              jitter=False)
        for k in range(0, W + 60, 40):   # mesh dots
            for j in range(0, H + 60, 40):
                d.ellipse((k - 5, j - 5, k + 5, j + 5), fill=(170, 40, 36))
        tw, th = (W * 0.6, H * 0.34) if not vert else (W * 0.8, H * 0.2)
        cx, cy = W / 2, H / 2
        paper(img, [(cx - tw / 2, cy - th / 2), (cx + tw / 2, cy - th / 2 - 8), (cx + tw / 2 + 6, cy + th / 2),
                    (cx - tw / 2, cy + th / 2 + 6)], (250, 250, 244), rng, 2.0, sh=12)
        f = ImageFont.truetype(FONT, int(tw / 7.5))
        d.text((cx, cy - th * 0.14), "MADE", font=f, fill=INK, anchor="mm")
        d.text((cx, cy + th * 0.2), "OVERSEAS", font=f, fill=INK, anchor="mm")
        for k in (-1, 1):
            paper(img, [(cx + k * tw / 2 - 10, cy - th / 2), (cx + k * tw / 2 + 10, cy - th / 2),
                        (cx + k * tw / 2 + 10, cy + th / 2), (cx + k * tw / 2 - 10, cy + th / 2)], (230, 230, 220),
                  rng, 1.0, shadow=False)
        return img
    if kind == "selfie":   # a paper photo: beach, palm, Kaylee duck-face, a calm robed figure
        paper(img, [(-20, -20), (W + 20, -20), (W + 20, H + 20), (-20, H + 20)], (60, 50, 70), rng, 1.0, shadow=False,
              jitter=False)
        pw, ph = (W * 0.62, H * 0.84) if not vert else (W * 0.9, H * 0.6)
        cx, cy = W / 2, H / 2
        paper(img, [(cx - pw / 2, cy - ph / 2), (cx + pw / 2, cy - ph / 2 + 10), (cx + pw / 2, cy + ph / 2),
                    (cx - pw / 2 + 6, cy + ph / 2)], (250, 250, 244), rng, 2.0, sh=14)
        ix0, iy0, ix1, iy1 = cx - pw / 2 + 24, cy - ph / 2 + 24, cx + pw / 2 - 24, cy + ph / 2 - 110
        paper(img, [(ix0, iy0), (ix1, iy0), (ix1, iy1), (ix0, iy1)], (150, 210, 240), rng, 1.0, shadow=False,
              jitter=False)
        sea = iy0 + (iy1 - iy0) * 0.52
        paper(img, [(ix0, sea), (ix1, sea), (ix1, iy1), (ix0, iy1)], (60, 150, 200), rng, 1.0, shadow=False)
        paper(img, [(ix0, iy1 - (iy1 - iy0) * 0.18), (ix1, iy1 - (iy1 - iy0) * 0.22), (ix1, iy1), (ix0, iy1)],
              (240, 214, 160), rng, 1.0, shadow=False)
        px_ = ix0 + (ix1 - ix0) * 0.12
        paper(img, strip([(px_, iy1 - 20), (px_ + 30, iy0 + (iy1 - iy0) * 0.25)], 18), (130, 90, 60), rng, 1.0)
        for a in range(5):
            ang = math.radians(200 + a * 36)
            tx, ty = px_ + 30, iy0 + (iy1 - iy0) * 0.25
            paper(img, strip([(tx, ty), (tx + 110 * math.cos(ang), ty + 60 * math.sin(ang) + 30)], 22), (60, 150, 70),
                  rng, 1.0)
        s_ = (iy1 - iy0) / 900 * (1.6 if vert else 1.3)
        # the robed figure: calm, simple, respectful (same paper style as everyone)
        mx = ix0 + (ix1 - ix0) * 0.66
        my = iy1 + 40 * s_
        robe = (230, 140, 50)
        paste(img, render_shapes([("p", [(-90, -360), (90, -360), (120, 0), (-120, 0)], robe),
                                  ("p", [(-90, -360), (20, -360), (110, -100), (60, -60)], (210, 120, 40)),
                                  ("e", (0, -440, 76, 84), (200, 150, 110)),
                                  ("e", (-26, -446, 9, 10), PUPIL, False), ("e", (26, -446, 9, 10), PUPIL, False),
                                  ("p", strip([(-18, -404), (0, -398), (18, -404)], 5), (120, 70, 50), False)],
                                 s_, 520, 401), mx, my - 120 * s_)
        # Kaylee, duck-face, peace sign
        kx = ix0 + (ix1 - ix0) * 0.33
        kz = s_ * 1.05
        paste(img, rspr("kaylee", "body", round(kz, 3)), kx, my - 120 * s_)
        paste(img, rspr("kaylee", "arm", round(kz, 3)), kx + 54 * kz, my - 120 * s_ - 214 * kz, 160)
        paste(img, rspr("kaylee", "head", round(kz, 3), 0, False, "duck", frozenset()), kx, my - 120 * s_ - 226 * kz)
        d.text((cx, cy + ph / 2 - 55), "#blessed #bali #spiritual", font=ImageFont.truetype(FONT, int(pw / 18)),
               fill=(90, 90, 110), anchor="mm")
        return img
    if kind == "coin":   # Brad's phone: a red crashing chart and a cartoon dog coin
        paper(img, [(-20, -20), (W + 20, -20), (W + 20, H + 20), (-20, H + 20)], (40, 50, 80), rng, 1.0, shadow=False,
              jitter=False)
        pw, ph = (H * 0.5, H * 0.9) if not vert else (W * 0.78, H * 0.7)
        cx, cy = W / 2, H / 2
        paper(img, [(cx - pw / 2, cy - ph / 2), (cx + pw / 2, cy - ph / 2), (cx + pw / 2, cy + ph / 2),
                    (cx - pw / 2, cy + ph / 2)], (24, 24, 28), rng, 2.0, sh=14)
        sx0, sy0, sx1, sy1 = cx - pw / 2 + 20, cy - ph / 2 + 50, cx + pw / 2 - 20, cy + ph / 2 - 50
        paper(img, [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)], (250, 250, 250), rng, 1.0, shadow=False,
              jitter=False)
        pts, n = [], 14
        r2 = np.random.default_rng(3)
        for k in range(n):
            fx = k / (n - 1)
            hgt = 0.2 + 0.1 * r2.random() if k < 8 else 0.2 + (k - 7) * 0.11
            pts.append((sx0 + 30 + fx * (sx1 - sx0 - 60), sy0 + (sy1 - sy0) * (0.25 + hgt * 0.75)))
        d.line(pts, fill=(220, 40, 40), width=10)
        f = ImageFont.truetype(FONT, int(pw / 9))
        d.text((cx, sy0 + 60), "WOOFCOIN", font=f, fill=INK, anchor="mm")
        d.text((cx, sy1 - 70), "-99.9%", font=f, fill=(220, 40, 40), anchor="mm")
        r = pw * 0.17
        ccx, ccy = sx1 - r - 20, sy0 + (sy1 - sy0) * 0.4
        paper(img, ell(ccx, ccy, r, r), (236, 190, 60), rng, 1.5, sh=6)
        for side in (-1, 1):   # floppy ears, eyes, nose, tongue: a cartoon dog
            paper(img, ell(ccx + side * r * 0.5, ccy - r * 0.45, r * 0.22, r * 0.35, rot=side * 25), (150, 100, 50),
                  rng, 1.0)
            d.ellipse((ccx + side * r * 0.28 - 7, ccy - r * 0.1 - 7, ccx + side * r * 0.28 + 7, ccy - r * 0.1 + 7),
                      fill=INK)
        d.ellipse((ccx - 12, ccy + r * 0.12 - 9, ccx + 12, ccy + r * 0.12 + 9), fill=INK)
        d.ellipse((ccx - 9, ccy + r * 0.3, ccx + 9, ccy + r * 0.5), fill=(230, 90, 110))
        return img
    if kind == "jessica":   # Rick's phone: the bot "Jessica" and her hearts
        paper(img, [(-20, -20), (W + 20, -20), (W + 20, H + 20), (-20, H + 20)], (226, 214, 176), rng, 1.0,
              shadow=False, jitter=False)
        pw, ph = (H * 0.5, H * 0.9) if not vert else (W * 0.78, H * 0.7)
        cx, cy = W / 2, H / 2
        paper(img, [(cx - pw / 2, cy - ph / 2), (cx + pw / 2, cy - ph / 2), (cx + pw / 2, cy + ph / 2),
                    (cx - pw / 2, cy + ph / 2)], (24, 24, 28), rng, 2.0, sh=14)
        sx0, sy0, sx1, sy1 = cx - pw / 2 + 20, cy - ph / 2 + 50, cx + pw / 2 - 20, cy + ph / 2 - 50
        paper(img, [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)], (250, 240, 246), rng, 1.0, shadow=False,
              jitter=False)
        f = ImageFont.truetype(FONT, int(pw / 11))
        f2 = ImageFont.truetype(FONT.replace("Black", "Bold"), int(pw / 15))
        d.text((cx, sy0 + 50), "Jessica (bot?)", font=f, fill=INK, anchor="mm")
        for (txt, yy) in (("hi handsome", 0.32), ("u r so smart", 0.47), ("send gift cards pls", 0.62)):
            bx0, by = sx0 + 30, sy0 + (sy1 - sy0) * yy
            paper(img, [(bx0, by - 34), (bx0 + pw * 0.75, by - 36), (bx0 + pw * 0.75, by + 34), (bx0, by + 36)],
                  (236, 120, 170), rng, 1.0, sh=3)
            d.text((bx0 + 24, by), txt, font=f2, fill=WHITE, anchor="lm")
        for k in range(6):
            hx, hy = sx0 + 50 + k * (sx1 - sx0 - 100) / 5, sy0 + (sy1 - sy0) * 0.85
            heart(d, hx, hy, 22)
        return img
    raise KeyError(kind)


def heart(d, x, y, r, col=(230, 50, 90)):
    d.ellipse((x - r, y - r, x, y), fill=col)
    d.ellipse((x, y - r, x + r, y), fill=col)
    d.polygon([(x - r, y - r / 2), (x + r, y - r / 2), (x, y + r)], fill=col)


def bg(scene, cam_name):
    key = (scene, cam_name)
    if key not in G["bg"]:
        cx, cy, z = G["cams"][scene][cam_name]
        cam = Cam(G["L"], cx, cy, z)
        L = G["L"]
        if scene in ("table", "dawn"):
            G["bg"][key] = bg_table(L, cam, scene == "dawn")
        elif scene == "studio":
            G["bg"][key] = (bg_studio(L, cam), None)
        elif scene == "lot":
            G["bg"][key] = (bg_lot(L, cam), None)
        else:
            G["bg"][key] = (bg_cutaway(L, cam, scene), None)
    return G["bg"][key]


# ------------------------------------------------------------------------------------------------ frame
def grandma_table(t):
    """Grandma at the table: there, walking off with the pie, gone, back with the pie."""
    ev = G["ev"]
    gx = G["L"]["table"]["x"]["grandma"]
    p0 = ev.get("pie", 1e9)
    back = lines_with("Bradley", "grandma")
    back_t = back[0]["t0"] - 3.0 if back else 1e9
    if t < p0:
        return ("sit", gx)
    if t < p0 + 1.5:
        f = int((t - p0) / 1.5 * 10) / 10
        return ("walk", gx + f * 700)
    if t < back_t:
        return ("gone", None)
    return ("pie", gx)


def shake(t):
    ev = G["ev"]
    for name, dt in (("gravy", 0.45), ("cops", 0.1)):
        if name in ev and 0 <= t - (ev[name] + dt) < 2 / FPS:
            return (22, -14) if t - (ev[name] + dt) < 1 / FPS else (-12, 8)
    return (0, 0)


def frame(fi):
    L, ev = G["L"], G["ev"]
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
    K = L["K"]
    if scene in ("table", "dawn"):
        draw_corner_tv(fr, cam, t, li)
        xs = L["table"]["x"]
        rick_y = F
        gv = ev.get("gravy")
        back_rick = lines_with("Kids today", "rick")
        if gv is not None and gv + 0.55 <= t and (not back_rick or t < back_rick[0]["t0"]):
            rick_y = F + min(1.0, (t - gv - 0.55) / 0.5) * 420 * K   # slid under the table
        for c in TABLE:
            if c == "grandma":
                continue
            p = pose(c, t, fi, li, scene)
            draw_any(fr, cam, c, xs[c], rick_y if c == "rick" else F, p)
        st, gx = grandma_table(t) if scene == "table" else ("sit", xs["grandma"])
        if st != "gone":
            p = pose("grandma", t, fi, li, scene)
            hop, (jx, jy), ang, (aL, aR), hk, _, _, extra = p
            if st == "walk":
                aL, aR = -160, 160
            if gv is not None and gv - 0.05 <= t < gv + 0.25 and scene == "table":
                aR = 150   # the throw
            n = lines_with("you're next", "grandma")
            if n and n[0]["t0"] <= t <= n[0]["start"] + n[0]["dur"] + 0.6:   # slow head turn to Rick
                ang = min(14.0, (t - n[0]["t0"]) * 4)
            C2.draw_granny(fr, cam, gx, F, hk[0], "mean", aL, aR, ang=ang, hop=hop)
            if st in ("walk",):
                paste(fr, prop("pie", round(z * K * 0.8, 3)), *cam.p(gx, F - 330 * K))
        fr.alpha_composite(front)
        if scene == "table" and st in ("sit", "pie"):   # the pie on the table (or Grandma's, after)
            paste(fr, prop("pie", round(z * K * 0.8, 3)), *cam.p(xs["grandma"] - (0 if st == "pie" else 200) * K,
                                                                 L["table"]["top"]))
        if scene == "dawn":
            paste(fr, prop("pie", round(z * K * 0.8, 3)), *cam.p((xs["mb"] + xs["dot"]) / 2, L["table"]["top"]))
            if ev["dawn"] <= t < ev["dawn"] + 1.4:
                C2.draw_tag(fr, "7:04 AM", L["W"] / 2, L["H"] * (0.18 if L["W"] > L["H"] else 0.2), 0, 1.0)
        if scene == "table":
            draw_gravy(fr, cam, t)
            draw_dial(fr, cam, t)
    elif scene == "studio":
        draw_studio(fr, cam, t, fi, li)
    elif scene == "lot":
        draw_lot(fr, cam, t, fi, li)
    banners(fr, t)
    C2.draw_caption(fr, t, cam_name)
    return np.asarray(fr.convert("RGB")).tobytes()


def draw_corner_tv(fr, cam, t, li):
    L = G["L"]
    tx, ty = L["table"]["tv"]
    on = G["ev"].get("tvon", 1e9)
    d = ImageDraw.Draw(fr)
    a, b = cam.p(tx - 140, ty - 100)
    c_, e = cam.p(tx + 140, ty + 100)
    if t < on or G["scene"] == "dawn":
        d.rectangle((a, b, c_, e), fill=(40, 44, 48))
        return
    if t < on + 0.5:   # static
        w, h = int(c_ - a), int(e - b)
        if w > 0 and h > 0:
            n = Image.effect_noise((max(1, w // 5), max(1, h // 5)), 90).resize((w, h), Image.NEAREST).convert("RGBA")
            paste(fr, n, (a + c_) / 2, (b + e) / 2)
        return
    d.rectangle((a, b, c_, e), fill=(255, 226, 120))   # glowing gold screen
    ln = G["lines"][li] if li is not None else None
    lvl = C2.mouth_level(ln, t) if ln is not None and ln["who"] == "chad" else 0
    zz = round(cam.z * 0.36, 3)
    paste(fr, rspr("chad", "head", zz, lvl, False, "norm", frozenset()), (a + c_) / 2, e + 10 * cam.z)


def draw_gravy(fr, cam, t):
    gv = G["ev"].get("gravy")
    if gv is None or not (gv <= t < gv + 1.6):
        return
    L = G["L"]
    K = L["K"]
    xs = L["table"]["x"]
    d = t - gv
    if d < 0.45:   # flies across the table, spinning
        f = int(d / 0.45 * 8) / 8
        x = xs["grandma"] + (xs["rick"] - xs["grandma"]) * f
        y = L["feet"] - 300 * K - math.sin(f * math.pi) * 260 * K
        paste(fr, prop("gravyboat", round(cam.z * K, 3)), *cam.p(x, y), f * 720)
    elif d < 1.0:
        px, py = cam.p(xs["rick"], L["feet"] - 380 * K)
        paste(fr, C2.spr("star", round(cam.z * K * (1.3 if int(t * FPS) % 2 else 1.15), 2), "BONK!"), px, py,
              (int(t * FPS) % 2) * 8)


def draw_dial(fr, cam, t):
    dl = G["ev"].get("dial")
    if dl is None or not (dl <= t < dl + 0.8):
        return
    L = G["L"]
    K = L["K"]
    x, y = cam.p(L["table"]["x"]["rick"] + 150 * K, L["feet"] - 470 * K)
    d = ImageDraw.Draw(fr)
    n = 1 + int((t - dl) / 0.1)
    d.text((x, y), "1-800-SOW-SEED"[:min(14, n * 2)], font=ImageFont.truetype(FONT, int(30 * cam.z * K)),
           fill=(200, 40, 32), anchor="mm", stroke_width=3, stroke_fill=WHITE)


def draw_studio(fr, cam, t, fi, li):
    L = G["L"]
    K = L["K"]
    S = L["studio"]
    ln = G["lines"][li] if li is not None else None
    x0, y0, x1, y1 = S["panel"]
    dollars = 1284903 + int(max(0, t - G["ev"].get("tvon", 0)) * 74321)
    d = ImageDraw.Draw(fr)
    d.text(cam.p((x0 + x1) / 2, y0 + (y1 - y0) * 0.66), "$ {:,}".format(dollars),
           font=ImageFont.truetype(FONT, int(min(70, (x1 - x0) / 9) * cam.z)), fill=(120, 255, 140), anchor="mm")
    tx, ty = S["tv"]
    paste(fr, C2.spr("tv", round(cam.z * 0.9, 3)), *cam.p(tx, ty))
    C2.screen_glow(fr, cam, tx - 228, ty - 292, tx + 228, ty - 50, t, 0.9)
    cx, cy = S["chad"]
    p = pose("chad", t, fi, li, "studio")
    hop, j, ang, (aL, aR), hk, sq, rot, extra = p
    if ln is not None and ln["who"] == "chad" and "never pay" in " ".join(w[2] for w in ln["words"]):
        aL, aR, extra["item"] = -165, 165, ("sign", "R", 0)
    p = (hop, j, ang, (aL, aR), hk, sq, rot, extra)
    draw_rig(fr, cam, "chad", cx, cy, p)
    sparkle(fr, cam, t, cx, cy)


def sparkle(fr, cam, t, cx, cy):
    """A twinkle on Chad's teeth at the start of each of his lines."""
    K = G["L"]["K"]
    for ln in G["lines"]:
        if ln["who"] == "chad" and 0 <= t - ln["t0"] < 0.35:
            x, y = cam.p(cx + 50 * K, cy - (250 + 112 - 56) * K)
            s_ = 26 * cam.z * K * (1.2 if int(t * FPS) % 2 else 0.8)
            ImageDraw.Draw(fr).polygon([(x, y - s_), (x + s_ * 0.25, y - s_ * 0.25), (x + s_, y),
                                        (x + s_ * 0.25, y + s_ * 0.25), (x, y + s_), (x - s_ * 0.25, y + s_ * 0.25),
                                        (x - s_, y), (x - s_ * 0.25, y - s_ * 0.25)], fill=WHITE, outline=(200, 200, 120))


def draw_lot(fr, cam, t, fi, li):
    L = G["L"]
    K = L["K"]
    F = L["feet"]
    S = L["lot"]
    ev = G["ev"]
    cops = ev.get("cops", 1e9)
    gx = S["grandma"][0]
    lt = ev.get("lot", 0)
    if t < lt + 1.2:   # Grandma cuts the line: walks in from the right
        f = int(min(1.0, (t - lt) / 1.2) * 8) / 8
        gx = S["grandma"][0] + (1 - f) * 600 * K
    p = pose("grandma", t, fi, li, "lot")
    hop, (jx, jy), ang, (aL, aR), hk, _, _, _ = p
    cx, cy = S["chad"]
    pc = pose("chad", t, fi, li, "lot")
    hop2, j2, ang2, (aL2, aR2), hk2, sq, rot, extra = pc
    hk2 = (hk2[0], hk2[1], "smug" if t >= cops else hk2[2], frozenset({"hat"}))
    if t >= cops + 0.6:
        aL2, aR2, extra["cuffs"] = 20, -20, True
    draw_rig(fr, cam, "chad", cx, cy, (hop2, j2, ang2, (aL2, aR2), hk2, sq, rot, extra))
    C2.draw_granny(fr, cam, gx, F, hk[0], "mean", aL, aR, ang=ang, hop=hop)
    for c, x in S["x"].items():
        draw_any(fr, cam, c, x, F, pose(c, t, fi, li, "lot"))
    if t >= cops:   # the police car slides in, in front of everyone
        f = min(1.0, int((t - cops) / 0.6 * 6) / 6)
        carx = S["car"][0] + (1 - f) * 1200
        paste(fr, prop("car", round(cam.z * K * 0.9, 3)), *cam.p(carx, S["car"][1]))
    if t >= cops:   # red/blue wash
        col = (255, 40, 40, 85) if int(t * FPS) % 4 < 2 else (40, 80, 255, 85)
        fr.alpha_composite(Image.new("RGBA", fr.size, col))


def banners(fr, t):
    L = G["L"]
    W = L["W"]
    big = 120 if L["W"] > L["H"] else 104
    by = L["banner_y"]

    def drop(t0):
        k = int((t - t0) * FPS)
        return [-700, -320, 40, -12, 0][k] if k < 5 else 0

    end = G["ev"]["end"]
    it_ = C2.GD.get("intro", 2.9)
    items = [(0.1, it_ - 0.05, "MEATBALL MYTHS", big, (200, 40, 32), WHITE, -3, 0),
             (0.6, it_ - 0.05, "HOLY BLACK FRIDAY", int(big * 0.62), (20, 20, 24), (252, 214, 74), 2, int(big * 1.25))]
    eb = int(big * 0.52)
    for i, txt in enumerate(END_TEXT):
        items.append((end + 0.2 + 0.25 * i, end + 99, txt, eb, (252, 250, 240), INK, [-2, 2, -1][i],
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
    if t >= end + 1.0:   # arrow to the comments, off to the right of the text
        ay = by + 3 * eb * 1.55 + (60 if L["H"] > L["W"] else 20) + (8 if int(t * FPS) % 4 < 2 else 0)
        x = W * 0.8
        rng = np.random.default_rng(3)
        paper(fr, [(x - 30, ay), (x + 30, ay), (x + 30, ay + 60), (x + 70, ay + 60), (x, ay + 130),
                   (x - 70, ay + 60), (x - 30, ay + 60)], (252, 214, 74), rng, 1.5, sh=6)


# ------------------------------------------------------------------------------------------------ audio
def mix(end):
    ev, lines = G["ev"], G["lines"]
    music = np.zeros(int((end + 1) * SR), np.float32)
    mel1 = [(0, "E5", 1), (1, "G5", 0.5), (1.5, "A5", 0.5), (2, "G5", 1), (3, "E5", 0.5), (3.5, "C#5", 0.5)]
    mel2 = [(0, "D5", 0.5), (0.5, "F#5", 0.5), (1, "A5", 1), (2, "B5", 0.5), (2.5, "A5", 0.5), (3, "G5", 1)]
    jingle_bar(music, 0.0, ["C", "A7"], 0.32, mel1, seed=1)   # one bar + a stab: the short-cut intro
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
    for nm in ("That's a lie", "Black Friday."):   # the long pauses are silent
        ll = lines_with(nm, "rick")
        if ll:
            gate[int((ll[0]["t0"] - 1.05) * SR):int(ll[0]["t0"] * SR)] = 0
    gate[int(ev["end"] * SR):] = 0
    gate = np.convolve(gate, np.ones(4410) / 4410, "same").astype(np.float32)
    music += bed * gate * 10 ** (-22 / 20) * 1.6
    fx = np.zeros_like(music)
    if "pie" in ev:   # sneaky tiptoe plucks
        for k in range(6):
            add(fx, ks(hz(["C5", "E5", "C5", "E5", "G5", "C6"][k]), 0.25, 0.99, 0.9, 80 + k), ev["pie"] + 0.1 + k * 0.22,
                0.3)
    tagl = lines_with("made overseas", "pip")
    if tagl:   # zip-zoom to the tag
        tt = np.arange(int(0.25 * SR)) / SR
        add(fx, (np.sin(2 * np.pi * np.cumsum(400 + 2400 * tt / 0.25) / SR) * 0.2).astype(np.float32),
            word_t(tagl[0], "made", 0) - 0.12, 1.0)
    if "gravy" in ev:
        gv = ev["gravy"]
        tt = np.arange(int(0.45 * SR)) / SR
        add(fx, (np.sin(2 * np.pi * np.cumsum(1500 - 900 * tt / 0.45) / SR) * 0.22).astype(np.float32), gv, 1.0)
        C2.thud(fx, gv + 0.45, 1.0)
        sfx_slap(fx, gv + 0.46, 0.6, 3)
        add(fx, ks(hz("A6"), 0.6, 0.99, 0.9, 6), gv + 0.5, 0.3)
        tt = np.arange(int(0.5 * SR)) / SR
        add(fx, (np.sin(2 * np.pi * np.cumsum(500 - 350 * tt / 0.5) / SR) * 0.18).astype(np.float32), gv + 0.6, 1.0)
    if "tvon" in ev:
        on = ev["tvon"]
        sfx_slap(fx, on, 0.4, 5)
        add(fx, C2.noise_burst(0.5, 0.4, 21, 1), on + 0.02, 0.18)
        add(fx, C2.choir(1.2, ("C3", "G3", "C4", "E4", "G4", "C5")), on + 0.45, 0.35)
    for ln in lines:   # Chad's tooth twinkle
        if ln["who"] == "chad":
            add(fx, ks(hz("C7"), 0.5, 0.995, 0.95, 90), ln["t0"] + 0.02, 0.22)
            add(fx, ks(hz("G7"), 0.4, 0.995, 0.95, 91), ln["t0"] + 0.1, 0.18)
    if "dial" in ev:   # touch-tone beeps (two tones each, not a real number)
        pairs = [(697, 1209), (770, 1336), (852, 1477), (941, 1336), (697, 1477), (770, 1209), (852, 1336)]
        for k, (a, b) in enumerate(pairs):
            add(fx, C2.tone(a, 0.08, 0.15) + C2.tone(b, 0.08, 0.15), ev["dial"] + 0.05 + k * 0.1)
    if "cops" in ev:   # two-tone siren
        c0 = ev["cops"]
        for k in range(4):
            add(fx, C2.tone(960, 0.36, 0.14), c0 + k * 0.72)
            add(fx, C2.tone(770, 0.36, 0.14), c0 + k * 0.72 + 0.36)
        C2.thud(fx, c0 + 0.6, 0.6)
    for k in range(3):   # dawn bird
        tt = np.arange(int(0.09 * SR)) / SR
        add(fx, (np.sin(2 * np.pi * np.cumsum(3800 - 1500 * tt / 0.09) / SR) * np.sin(np.pi * tt / 0.09) *
                 0.2).astype(np.float32), ev["dawn"] + 0.3 + k * 0.14)
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


# ------------------------------------------------------------------------------------------------ main
def use(name=None):
    if name:
        ACTIVE[0] = SEQ_HOLY_V4 if name == "v4" else SEQ_HOLY
    C2.SEQ[:] = ACTIVE[0]


def setup(fmt):
    use()
    L = layout(fmt)
    lines, segs, ev, end = C2.build()
    G.update(L=L, lines=lines, segs=segs, ev=ev, end=end, cams=cams(L), bg={})
    for (_, scene, cam) in segs:
        bg(scene, cam)


def render(fmt, out):
    os.makedirs(TMP, exist_ok=True)
    setup(fmt)
    L, end = G["L"], G["end"]
    wav = f"{TMP}/holy-mix-{fmt}.wav"
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


def stills(fmt, times):
    setup(fmt)
    W, H = G["L"]["W"], G["L"]["H"]
    outs = []
    for t in times:
        p = f"{TMP}/holy-{fmt}-{t:.2f}.png"
        Image.frombytes("RGB", (W, H), frame(int(t * FPS))).save(p)
        outs.append(p)
    print(" ".join(outs))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fmt", default="vertical", choices=["vertical", "wide"])
    ap.add_argument("--out")
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--timeline", action="store_true")
    ap.add_argument("--script", default="short", choices=["short", "v4"])
    a = ap.parse_args()
    use(a.script)
    if a.timeline:
        use()
        lines, segs, ev, end = C2.build()
        for i, ln in enumerate(lines):
            print(f"{i + 1:2d} {ln['who']:8s} {ln['t0']:7.2f} {ln['dur']:5.2f} {' '.join(w[2] for w in ln['words'])[:60]}")
        print({k: round(v, 1) for k, v in ev.items()}, round(end, 2))
    elif a.still:
        stills(a.fmt, a.still)
    else:
        render(a.fmt, a.out)
