#!/usr/bin/env python3
"""Cutout test 2: BLACK FRIDAY (Nolan 11/18: "funnier, way edgier"). Multi-scene paper-cutout engine on top of
cutout.py's paper kit and cast. Comedy is in timing (hard cuts on punchlines, deadpan reaction holds) and visual
gags (door burst + paper stampede that flattens the kids, glowing TV + choir chord, a tiny grandma body-slam,
a self-checkout robot that gets punched, dawn parking lot with one sock). Style reference only: everything here
is original (characters, store MEGAMART, voices, music, sound effects).

  python3 tools/cutout2.py --fmt vertical|wide --out file.mp4
  python3 tools/cutout2.py --fmt vertical --still 3.5 20 ...
  python3 tools/cutout2.py --sheet file.mp4 [--times 4 30 60]
Script: side-hustles/channels/scripts/cutout-black-friday.md (render the words exactly).
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
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout as C  # noqa: E402
import free_voice as fv  # noqa: E402
from cutout import (FONT, INK, WHITE, PUPIL, MOUTH, ell, strip, lumpy, paper, render_shapes, add, ks, hz,  # noqa
                    strum, snare, kick, jingle_bar, sfx_slap, load_audio, BEAT, SR, FPS, OUT_FPS, TMP)

# Cast voices (Nolan's audition picks 11/19: Meatball A, Pip B, Dot C, Grandma C, CEO B, Self-checkout C).
V = {"mb": "kokoro:adam-puck@speed=1.36",                      # American smartass kid (am_adam .6 + am_puck .4)
     "pip": "kokoro:aud-pip-b@speed=1.42,pause=0.14",          # nervous, higher, faster (am_puck .4 + af_bella .6)
     "dot": "kokoro:aud-dot-c@speed=1.1,pause=0.3",            # dry, bored, British (bf_emma .7 + af_river .3)
     "grandma": "kokoro:aud-gran-c@speed=1.0,pause=0.4",       # sweet then scary, British (bf_emma .5 + bf_isabella .5)
     "kiosk": "kokoro:aud-bot-c@speed=0.92,pause=0.35",        # monotone machine (am_echo .5 + af_alloy .5)
     "ceo": "kokoro:aud-ceo-b@speed=1.15,pause=0.25"}          # posh British announcer (bm_george .7 + bm_lewis .3)
# The voices v2-v4 were rendered with (--script v2|v3|v4 swaps these back in).
V_OLD = {"mb": "kokoro:adam-puck@speed=1.36", "pip": "kokoro:pip@speed=1.34,pause=0.16",
         "dot": "kokoro:dot@speed=1.2,pause=0.16", "grandma": "kokoro:grandma@speed=1.18,pause=0.16",
         "kiosk": "kokoro:kiosk@speed=1.0,pause=0.15", "ceo": "kokoro:ceo@speed=1.3,pause=0.16"}

# Items: ("line", who, say, caption, opts) | ("gag", name, seconds, scene, cam) | ("hold", seconds, cam)
# opts: scene, cams [(word index, cam)], gap (s after the line)
SEQ_V2 = [   # v2 HARD script: side-hustles/channels/scripts/cutout-black-friday-v2-hard.md
    ("gag", "intro", 2.9, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")])),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "My mom said if I come home, she's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.35)),
    ("line", "mb", "Relax. We go in fast, grab the TV, and leave with our dignity.", None,
     dict(scene="outside", cams=[(0, "cu_mb"), (1, "wide")], gap=0.1, voice="kokoro:adam-puck@speed=1.2")),
    ("gag", "stampede", 2.8, "outside", "wide"),
    ("line", "pip", "There goes our dignity. And my spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.1, voice="kokoro:pip@speed=1.22,pause=0.16")),
    ("hold", 0.5, "wide"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "wide"), (18, "cu_ceo")],
                                            gap=0.2)),
    ("line", "dot", "That's not a sale. That's a hostage situation with coupons.", None,
     dict(scene="ceo", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.5, "cu_dot"),
    ("gag", "tv", 1.7, "inside", "cu_tv"),
    ("line", "mb", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and child tears.",
     None, dict(scene="inside", cams=[(0, "wide"), (3, "cu_tv"), (7, "cu_mb")], gap=0.1)),
    ("hold", 0.4, "cu_mb"),
    ("gag", "slam", 1.4, "inside", "wide"),
    ("line", "pip", "[BLEEP]! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.2)),
    ("line", "grandma", "Back off, sweetie. I've been training since July and I have nothing left to lose.", None,
     dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.35)),
    ("line", "mb", "New plan. Grandma takes the TV, we follow her home, and we watch it through her window.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.2)),
    ("line", "dot", "That's called stalking.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "mb", "It's called a payment plan.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.55, "cu_dot"),
    ("gag", "checkout", 0.8, "checkout", "wide"),
    ("line", "kiosk", "Unexpected item in the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25, beep=0.35)),
    ("line", "grandma", "The unexpected item is my fist.", None,
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.05)),
    ("gag", "punch", 1.0, "checkout", "wide"),
    ("line", "kiosk", "Please... wait... for an associate.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2)),
    ("line", "ceo", "There are no associates. We replaced them with you.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.5, "cu_ceo"),
    ("gag", "dawn", 1.4, "dawn", "wide"),
    ("line", "mb", "You know, guys, Black Friday taught us something. It's not about the stuff. It's about the people...",
     None, dict(scene="dawn", cams=[(0, "wide"), (5, "cu_mb")], gap=0.25)),
    ("line", "pip", "I got a free sock. Somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.25)),
    ("line", "mb", "we stepped on to get the stuff.", "...we stepped on to get the stuff.",
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.55, "wide"),
    ("line", "dot", "Dang. That got dark.", None, dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.5, "cu_dot"),
    ("line", "pip", "Same time next year?", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.2)),
    ("line", "all", "Obviously. [BLEEP] yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.4)),
    ("gag", "end", 2.9, "dawn", "wide"),
]
SEQ_V3 = [   # v3 cursing: side-hustles/channels/scripts/cutout-black-friday-v3-cursing.md
    ("gag", "intro", 2.9, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")])),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "My mom said if I come home, she's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.35)),
    ("line", "mb", "Relax. We go in fast, grab the damn TV, and leave with our dignity.", None,
     dict(scene="outside", cams=[(0, "cu_mb"), (1, "wide")], gap=0.1, voice="kokoro:adam-puck@speed=1.2")),
    ("gag", "stampede", 2.8, "outside", "wide"),
    ("line", "pip", "There goes our dignity. And my [BLEEP] spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.1, voice="kokoro:pip@speed=1.22,pause=0.16")),
    ("hold", 0.4, "wide"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "wide"), (18, "cu_ceo")],
                                            gap=0.2)),
    ("line", "dot", "That's not a sale, you [BLEEP]. That's a hostage situation with coupons.", None,
     dict(scene="ceo", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("gag", "tv", 1.5, "inside", "cu_tv"),
    ("line", "mb", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and child tears. "
     "I don't give a crap.",
     None, dict(scene="inside", cams=[(0, "wide"), (3, "cu_tv"), (7, "cu_mb")], gap=0.1)),
    ("hold", 0.4, "cu_mb"),
    ("gag", "slam", 1.4, "inside", "wide"),
    ("line", "pip", "[BLEEP]! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.2)),
    ("line", "grandma", "Back off, you little [BLEEP]. I've been training since July and I have nothing left to lose.", None,
     dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.35)),
    ("line", "mb", "New plan. Grandma takes the TV, we follow her home, and we watch it through her window.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.2)),
    ("line", "dot", "That's called stalking, dumbass.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "mb", "It's called a payment plan.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "cu_dot"),
    ("gag", "checkout", 0.7, "checkout", "wide"),
    ("line", "kiosk", "Unexpected item in the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25, beep=0.35)),
    ("line", "grandma", "The unexpected item is my [BLEEP] fist.", None,
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.05)),
    ("gag", "punch", 1.0, "checkout", "wide"),
    ("line", "kiosk", "Please... wait... for an associate.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2)),
    ("line", "ceo", "There are no associates. We replaced them with you.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.4, "cu_ceo"),
    ("gag", "dawn", 1.2, "dawn", "wide"),
    ("line", "mb", "You know, guys, Black Friday taught us something. It's not about the stuff. It's about the people...",
     None, dict(scene="dawn", cams=[(0, "wide"), (5, "cu_mb")], gap=0.25)),
    ("line", "pip", "I got a free sock. Holy crap, somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.25)),
    ("line", "mb", "we stepped on to get the stuff.", "...we stepped on to get the stuff.",
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "wide"),
    ("line", "dot", "Well, that got dark as hell.", None, dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("line", "pip", "Same time next year?", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.2)),
    ("line", "all", "Obviously. [BLEEP] yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.25)),
    ("gag", "end", 2.6, "dawn", "wide"),
]
SEQ_V4 = [   # v4 uncensored: side-hustles/channels/scripts/cutout-black-friday-v4-uncensored.md
    ("gag", "intro", 2.9, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")])),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "My mom said if I come home, she's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.35)),
    ("line", "mb", "Relax. We go in fast, grab the damn TV, and leave with our dignity.", None,
     dict(scene="outside", cams=[(0, "cu_mb"), (1, "wide")], gap=0.1, voice="kokoro:adam-puck@speed=1.2")),
    ("gag", "stampede", 2.8, "outside", "wide"),
    ("line", "pip", "There goes our dignity. And my fucking spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.1, voice="kokoro:pip@speed=1.22,pause=0.16")),
    ("hold", 0.4, "wide"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "wide"), (18, "cu_ceo")],
                                            gap=0.2)),
    ("line", "dot", "That's not a sale, you jackass. That's a hostage situation with coupons.", None,
     dict(scene="ceo", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("gag", "tv", 1.5, "inside", "cu_tv"),
    ("line", "mb", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and child tears. "
     "I don't give a crap.",
     None, dict(scene="inside", cams=[(0, "wide"), (3, "cu_tv"), (7, "cu_mb")], gap=0.1)),
    ("hold", 0.4, "cu_mb"),
    ("gag", "slam", 1.4, "inside", "wide"),
    ("line", "pip", "Holy shit! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.2)),
    ("line", "grandma", "Back off, you little shit. I've been training since July and I have nothing left to lose.", None,
     dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.35)),
    ("line", "mb", "New plan. Grandma takes the TV, we follow her home, and we watch it through her window.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.2)),
    ("line", "dot", "That's called stalking, dumbass.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "mb", "It's called a payment plan.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "cu_dot"),
    ("gag", "checkout", 0.7, "checkout", "wide"),
    ("line", "kiosk", "Unexpected item in the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25, beep=0.35)),
    ("line", "grandma", "The unexpected item is my God-damn fist.", "The unexpected item is my goddamn fist.",
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.05)),
    ("gag", "punch", 1.0, "checkout", "wide"),
    ("line", "kiosk", "Please... wait... for an associate.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2)),
    ("line", "ceo", "There are no associates. We replaced them with you.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.4, "cu_ceo"),
    ("gag", "dawn", 1.2, "dawn", "wide"),
    ("line", "mb", "You know, guys, Black Friday taught us something. It's not about the stuff. It's about the people...",
     None, dict(scene="dawn", cams=[(0, "wide"), (5, "cu_mb")], gap=0.25)),
    ("line", "pip", "I got a free sock. Holy crap, somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.25)),
    ("line", "mb", "we stepped on to get the stuff.", "...we stepped on to get the stuff.",
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.0, voice="kokoro:adam-puck@speed=1.2")),
    ("hold", 0.45, "wide"),
    ("line", "dot", "Well, that got dark as hell.", None, dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("line", "pip", "Same time next year?", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.2)),
    ("line", "all", "Obviously. Fuck yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.25)),
    ("gag", "end", 2.6, "dawn", "wide"),
]
SEQ_V5 = [   # v5: v4 words, the new cast voices, delivery punctuation for Grandma 10 and the robot 16
    ("gag", "intro", 2.9, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")])),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "My mom said if I come home, she's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.35)),
    ("line", "mb", "Relax. We go in fast, grab the damn TV, and leave with our dignity.", None,
     dict(scene="outside", cams=[(0, "cu_mb"), (1, "wide")], gap=0.1, voice="kokoro:adam-puck@speed=1.2")),
    ("gag", "stampede", 2.8, "outside", "wide"),
    ("line", "pip", "There goes our dignity. And my fucking spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.1, voice="kokoro:aud-pip-b@speed=1.3,pause=0.14")),
    ("hold", 0.4, "wide"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "wide"), (18, "cu_ceo")],
                                            gap=0.2)),
    ("line", "dot", "That's not a sale, you jackass. That's a hostage situation with coupons.", None,
     dict(scene="ceo", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("gag", "tv", 1.5, "inside", "cu_tv"),
    ("line", "mb", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and child tears. "
     "I don't give a crap.",
     None, dict(scene="inside", cams=[(0, "wide"), (3, "cu_tv"), (7, "cu_mb")], gap=0.1)),
    ("hold", 0.4, "cu_mb"),
    ("gag", "slam", 1.4, "inside", "wide"),
    ("line", "pip", "Holy shit! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.2)),
    ("line", "grandma", "Back off... you little shit. I've been training since July. And I have nothing. Left. To lose.",
     "Back off, you little shit. I've been training since July and I have nothing left to lose.",
     dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.35)),
    ("line", "mb", "New plan. Grandma takes the TV, we follow her home, and we watch it through her window.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.2)),
    ("line", "dot", "That's called stalking, dumbass.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "mb", "It's called a payment plan.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "cu_dot"),
    ("gag", "checkout", 0.7, "checkout", "wide"),
    ("line", "kiosk", "Unexpected item in the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25, beep=0.35)),
    ("line", "grandma", "The unexpected item is my God-damn fist.", "The unexpected item is my goddamn fist.",
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.05)),
    ("gag", "punch", 1.0, "checkout", "wide"),
    ("line", "kiosk", "Please. Wait. For. An. Associate.", "Please... wait... for an associate.",
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2)),
    ("line", "ceo", "There are no associates. We replaced them with you.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.4, "cu_ceo"),
    ("gag", "dawn", 1.2, "dawn", "wide"),
    ("line", "mb", "You know, guys, Black Friday taught us something. It's not about the stuff. It's about the people...",
     None, dict(scene="dawn", cams=[(0, "wide"), (5, "cu_mb")], gap=0.25)),
    ("line", "pip", "I got a free sock. Holy crap, somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.25)),
    ("line", "mb", "we stepped on to get the stuff.", "...we stepped on to get the stuff.",
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.0, voice="kokoro:adam-puck@speed=1.2")),
    ("hold", 0.45, "wide"),
    ("line", "dot", "Well, that got dark as hell.", None, dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("line", "pip", "Same time next year?", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.2)),
    ("line", "all", "Obviously. Fuck yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.25)),
    ("gag", "end", 2.6, "dawn", "wide"),
]
SEQ_V6 = [   # v6: side-hustles/channels/scripts/cutout-black-friday-v6.md (29 lines, swears spoken, v5 cast voices)
    ("gag", "intro", 2.9, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")])),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "My mom said if I come home, she's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.35)),
    ("line", "mb", "Relax. We go in fast, grab the damn TV, and leave with our dignity.", None,
     dict(scene="outside", cams=[(0, "cu_mb"), (1, "wide")], gap=0.1, voice="kokoro:adam-puck@speed=1.2")),
    ("gag", "stampede", 2.8, "outside", "wide"),
    ("line", "pip", "There goes our dignity. And my fucking spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.15, voice="kokoro:aud-pip-b@speed=1.3,pause=0.14")),
    ("line", "dot", "You didn't need it. You've never used it.", None,
     dict(scene="outside", cams=[(0, "cu_dot_flat")], gap=0.0)),
    ("hold", 0.45, "cu_pip_flat"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "wide"), (18, "cu_ceo")],
                                            gap=0.2)),
    ("line", "dot", "That's not a sale, you jackass. That's a hostage situation with coupons.", None,
     dict(scene="ceo", cams=[(0, "cu_dot")], gap=0.25)),
    ("line", "ceo", "And remember: if you get trampled, that's not an injury. That's engagement.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.4, "wide"),
    ("line", "mb", "This guy is the biggest piece of shit I've ever seen, and I've seen Pip's science project.", None,
     dict(scene="ceo", cams=[(0, "cu_mb")], gap=0.1)),
    ("line", "pip", "It was a volcano!", None, dict(scene="ceo", cams=[(0, "cu_pip")], gap=0.1)),
    ("line", "mb", "It was a turd in a cup, Pip.", None,
     dict(scene="ceo", cams=[(0, "cu_mb"), (3, "cup/wide")], gap=0.0)),
    ("hold", 0.6, "cup/wide"),
    ("hold", 0.45, "ceo/cu_pip"),
    ("gag", "tv", 1.5, "inside", "cu_tv"),
    ("line", "mb", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and child tears. "
     "I don't give a crap.",
     None, dict(scene="inside", cams=[(0, "wide"), (3, "cu_tv"), (7, "cu_mb")], gap=0.1)),
    ("hold", 0.35, "cu_mb"),
    ("gag", "slam", 1.4, "inside", "wide"),
    ("line", "pip", "Holy shit! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.2)),
    ("line", "grandma", "Back off... you little shit. I've been training since July. And I have nothing. Left. To lose.",
     None, dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.3)),
    ("line", "dot", "Respect.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.6, "cu_dot"),
    ("line", "mb", "New plan. Grandma takes the TV, we follow her home, and we watch it through her window.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.2)),
    ("line", "dot", "That's called stalking, dumbass.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "mb", "It's called a payment plan.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "cu_dot"),
    ("gag", "checkout", 0.7, "checkout", "wide"),
    ("line", "kiosk", "Unexpected. Item. In the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25, beep=0.35)),
    ("line", "grandma", "The unexpected item is my God-damn fist.", "The unexpected item is my goddamn fist.",
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.05)),
    ("gag", "punch", 1.0, "checkout", "wide"),
    ("line", "kiosk", "Please. Wait. For. An. Associate.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2)),
    ("line", "ceo", "There are no associates. We replaced them with you. Merry fucking Christmas.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.5, "cu_ceo"),
    ("gag", "dawn", 1.2, "dawn", "wide"),
    ("line", "mb", "You know, guys, Black Friday taught us something. It's not about the stuff. It's about the people...",
     None, dict(scene="dawn", cams=[(0, "wide"), (5, "cu_mb")], gap=0.25)),
    ("line", "pip", "I got a free sock. Holy crap, somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.25)),
    ("line", "mb", "we stepped on to get the stuff.", "...we stepped on to get the stuff.",
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.0, voice="kokoro:adam-puck@speed=1.2")),
    ("hold", 0.45, "wide"),
    ("line", "dot", "Well, that got dark as hell.", None, dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.4, "cu_dot"),
    ("line", "pip", "Same time next year?", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.2)),
    ("line", "all", "Obviously. Fuck yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.25)),
    ("gag", "end", 2.6, "dawn", "wide"),
]

SEQ_V7 = [   # v7: side-hustles/channels/scripts/cutout-black-friday-v7.md (v6 + 3b, 3c, 12b, 12c, 19b, 19c, 27b)
    ("gag", "intro", 2.9, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")])),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "My mom said if I come home, she's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "pip", "Your mom's a genius.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12, voice="kokoro:aud-pip-b@speed=1.25,pause=0.14")),
    ("line", "dot", "My mom's a landlord, Pip. It's worse.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.2)),
    ("line", "mb", "My dad left to get Black Friday deals six years ago. Still hasn't come back.", None,
     dict(scene="outside", cams=[(0, "cu_mb")], gap=0.12)),
    ("line", "pip", "Maybe there's a really long line.", None, dict(scene="outside", cams=[(0, "cu_pip")], gap=0.15)),
    ("line", "mb", "There's a new family, Pip. It's a very long line.", None,
     dict(scene="outside", cams=[(0, "cu_mb")], gap=0.0)),
    ("gag", "sadpluck", 0.9, "outside", "cu_mb"),
    ("line", "mb", "Relax. We go in fast, grab the damn TV, and leave with our dignity.", None,
     dict(scene="outside", cams=[(0, "cu_mb"), (1, "wide")], gap=0.25, voice="kokoro:adam-puck@speed=1.2")),
    ("line", "pip", "I peed a little.", None, dict(scene="outside", cams=[(0, "cu_pip")], gap=0.12)),
    ("line", "dot", "You peed a lot, Pip. It's in my boot.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.1)),
    ("hold", 0.35, "cu_dot"),
    ("gag", "stampede", 2.8, "outside", "wide"),
    ("line", "pip", "There goes our dignity. And my fucking spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.15, voice="kokoro:aud-pip-b@speed=1.3,pause=0.14")),
    ("line", "mb", "Pip, if you die in here, can I have your shoes?", None,
     dict(scene="outside", cams=[(0, "cu_mb_flat")], gap=0.12)),
    ("line", "pip", "I'm not dead!", None, dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.12)),
    ("line", "mb", "Yet. Shoes, Pip.", None,
     dict(scene="outside", cams=[(0, "cu_mb_flat")], gap=0.3, voice="kokoro:adam-puck@speed=1.15")),
    ("line", "dot", "You didn't need it. You've never used it.", None,
     dict(scene="outside", cams=[(0, "cu_dot_flat")], gap=0.0)),
    ("hold", 0.45, "cu_pip_flat"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "wide"), (18, "cu_ceo")],
                                            gap=0.2)),
    ("line", "dot", "That's not a sale, you jackass. That's a hostage situation with coupons.", None,
     dict(scene="ceo", cams=[(0, "cu_dot")], gap=0.25)),
    ("line", "ceo", "And remember: if you get trampled, that's not an injury. That's engagement.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.25)),
    ("line", "ceo", "Our staff gave up Thanksgiving to be here. We thanked them with a pizza party. One slice. "
     "They're sharing it.", None, dict(scene="ceo", cams=[(0, "cu_ceo"), (13, "pizza/wide")], gap=0.0)),
    ("hold", 0.45, "pizza/wide"),
    ("line", "ceo", "And every TV is assembled by hand! Small hands. Very affordable hands.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.25)),
    ("line", "ceo", "And our return policy is simple: you can return anything. Except your childhood. We kept that.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.5, "cu_ceo"),
    ("hold", 0.4, "wide"),
    ("line", "mb", "This guy is the biggest piece of shit I've ever seen, and I've seen Pip's science project.", None,
     dict(scene="ceo", cams=[(0, "cu_mb")], gap=0.1)),
    ("line", "pip", "It was a volcano!", None, dict(scene="ceo", cams=[(0, "cu_pip")], gap=0.1)),
    ("line", "mb", "It was a turd in a cup, Pip.", None,
     dict(scene="ceo", cams=[(0, "cu_mb"), (3, "cup/wide")], gap=0.0)),
    ("hold", 0.6, "cup/wide"),
    ("hold", 0.3, "ceo/cu_pip"),
    ("line", "pip", "It got a ribbon!", None, dict(scene="ceo", cams=[(0, "cu_pip")], gap=0.1)),
    ("line", "dot", "It got a participation ribbon. The judge threw up.", None,
     dict(scene="ceo", cams=[(0, "cu_dot"), (5, "cup/wide")], gap=0.0)),
    ("hold", 0.55, "cup/wide"),
    ("hold", 0.35, "ceo/cu_pip"),
    ("gag", "tv", 1.5, "inside", "cu_tv"),
    ("line", "mb", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and child tears. "
     "I don't give a crap.",
     None, dict(scene="inside", cams=[(0, "wide"), (3, "cu_tv"), (7, "cu_mb")], gap=0.1)),
    ("hold", 0.35, "cu_mb"),
    ("gag", "slam", 1.4, "inside", "wide"),
    ("line", "pip", "Holy shit! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.2)),
    ("line", "grandma", "Back off... you little shit. I've been training since July. And I have nothing. Left. To lose.",
     None, dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.25)),
    ("line", "grandma", "I've buried two husbands, sweetie. One of them was still breathing. You're a speed bump.", None,
     dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.3)),
    ("line", "dot", "Respect.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.6, "cu_dot"),
    ("line", "mb", "Okay. I would sell Pip's kidney for this TV.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.12)),
    ("line", "pip", "You already sold one for a game console!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.12)),
    ("line", "mb", "And I'd do it again, Pip.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "cu_pip_down"),
    ("line", "mb", "New plan. Grandma takes the TV, we follow her home, and we watch it through her window.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.2)),
    ("line", "dot", "That's called stalking, dumbass.", None, dict(scene="inside", cams=[(0, "cu_dot")], gap=0.15)),
    ("line", "mb", "It's called a payment plan.", None, dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.45, "cu_dot"),
    ("line", "pip", "Is that legal?", None, dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.15)),
    ("line", "mb", "On Black Friday, nothing is legal. It's a riot with a loyalty card.", None,
     dict(scene="inside", cams=[(0, "cu_mb")], gap=0.0)),
    ("hold", 0.5, "cu_mb"),
    ("gag", "checkout", 0.7, "checkout", "wide"),
    ("line", "kiosk", "Unexpected. Item. In the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25, beep=0.35)),
    ("line", "grandma", "The unexpected item is my God-damn fist.", "The unexpected item is my goddamn fist.",
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.05)),
    ("gag", "punch", 1.0, "checkout", "wide"),
    ("line", "kiosk", "Please. Wait. For. An. Associate.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.25)),
    ("line", "kiosk", "Would you like to round up. To buy the CEO. A third yacht.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.2)),
    ("line", "ceo", "There are no associates. We replaced them with you. Merry fucking Christmas.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.5, "cu_ceo"),
    ("gag", "dawn", 1.2, "dawn", "wide"),
    ("line", "mb", "You know, guys, Black Friday taught us something. It's not about the stuff. It's about the people...",
     None, dict(scene="dawn", cams=[(0, "wide"), (5, "cu_mb")], gap=0.25)),
    ("line", "pip", "I got a free sock. Holy crap, somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.25)),
    ("line", "mb", "we stepped on to get the stuff.", "...we stepped on to get the stuff.",
     dict(scene="dawn", cams=[(0, "cu_mb")], gap=0.0, voice="kokoro:adam-puck@speed=1.2")),
    ("hold", 0.45, "wide"),
    ("line", "dot", "Well, that got dark as hell.", None, dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.3, "cu_dot"),
    ("line", "dot", "When I die, I want my ashes scattered in a MegaMart. So I can finally get returned.", None,
     dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.45, "cu_dot"),
    ("gag", "cart", 0.5, "dawn", "wide"),
    ("line", "grandma", "Suck it, children!", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.1)),
    ("gag", "bump", 1.5, "dawn", "wide"),
    ("line", "grandma", "Not today. I have the extended warranty.", None,
     dict(scene="dawn", cams=[(0, "cu_granny_lot")], gap=0.0)),
    ("hold", 0.45, "wide"),
    ("line", "pip", "Same time next year?", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.2)),
    ("line", "all", "Obviously. Fuck yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.25)),
    ("gag", "end", 2.6, "dawn", "wide"),
]

SEQ_V8 = [   # v8 SHORT (~60 s): side-hustles/channels/scripts/cutout-black-friday-v8-short.md
    ("gag", "intro", 2.2, "outside", "wide"),
    ("line", "mb", "Black Friday. The one day a year we fight a stranger over a toaster.", None,
     dict(scene="outside", cams=[(0, "wide"), (6, "cu_mb")], gap=0.0)),
    ("hold", 0.6, "cu_dot"),
    ("line", "pip", "My mom said if I don't come home with the TV, don't come home.", None,
     dict(scene="outside", cams=[(0, "cu_pip")], gap=0.2)),
    ("line", "dot", "My mom's renting out my room. On Airbed.", None,
     dict(scene="outside", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 0.6, "cu_pip"),
    ("gag", "stampede", 1.6, "outside", "wide"),
    ("line", "pip", "There goes my fucking spleen.", None,
     dict(scene="outside", cams=[(0, "cu_pip_flat")], gap=0.2, voice="kokoro:aud-pip-b@speed=1.3,pause=0.14")),
    ("line", "mb", "If you die in here, can I have your shoes?", None,
     dict(scene="outside", cams=[(0, "cu_mb_flat")], gap=0.0)),
    ("hold", 0.9, "cu_pip_flat"),
    ("gag", "ceo_in", 0.5, "ceo", "wide"),
    ("line", "ceo", "We raised every price forty percent last week, so sixty percent off is a gift from my heart.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 0.5, "wide"),
    ("line", "ceo", "And every TV is assembled by hand. Small hands. Very affordable hands.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 1.0, "wide"),
    ("gag", "slam", 1.2, "inside", "wide"),
    ("line", "pip", "Holy shit! A grandma just body-slammed me!", None,
     dict(scene="inside", cams=[(0, "cu_pip_down")], gap=0.0)),
    ("hold", 0.4, "cu_pip_down"),
    ("line", "grandma", "I've buried two husbands. One was still breathing. You're a speed bump.", None,
     dict(scene="inside", cams=[(0, "cu_grandma")], gap=0.0)),
    ("hold", 1.0, "cu_mb"),
    ("gag", "checkout", 0.6, "checkout", "wide"),
    ("line", "kiosk", "Unexpected. Item. In the bagging area.", None,
     dict(scene="checkout", cams=[(0, "cu_kiosk")], gap=0.4, beep=0.3)),
    ("line", "grandma", "The unexpected item is my God-damn fist.", "The unexpected item is my goddamn fist.",
     dict(scene="checkout", cams=[(0, "cu_grandma")], gap=0.0)),
    ("gag", "punch", 1.1, "checkout", "wide"),
    ("line", "ceo", "There are no workers. We replaced them with you. Merry fucking Christmas.", None,
     dict(scene="ceo", cams=[(0, "cu_ceo")], gap=0.0)),
    ("hold", 1.0, "cu_ceo"),
    ("gag", "dawn", 1.0, "dawn", "wide"),
    ("line", "pip", "I got a free sock. Somebody's foot is still in it.", None,
     dict(scene="dawn", cams=[(0, "cu_pip")], gap=0.0)),
    ("hold", 0.5, "cu_mb"),
    ("line", "dot", "When I die, scatter my ashes in a MegaMart. So I can finally get returned.", None,
     dict(scene="dawn", cams=[(0, "cu_dot")], gap=0.0)),
    ("hold", 1.0, "cu_dot"),
    ("line", "pip", "Same time next year?", None,
     dict(scene="dawn", cams=[(0, "wide")], gap=0.2, voice="kokoro:aud-pip-b@speed=1.3,pause=0.14")),
    ("line", "all", "Fuck yeah.", None, dict(scene="dawn", cams=[(0, "wide")], gap=0.5)),
    ("gag", "end", 3.0, "dawn", "wide"),
]

def _mask(seq, subs):
    """Same audio, masked swears in the burned-in caption (Studio 11/20: v9)."""
    out = []
    for it in seq:
        if it[0] == "line":
            cap = it[3] or it[2]
            for a, b in subs:
                cap = cap.replace(a, b)
            it = (it[0], it[1], it[2], cap if cap != it[2] else it[3], it[4])
        out.append(it)
    return out


SEQ_V9 = _mask(SEQ_V8, [("fucking", "f#@%ing"), ("Fuck", "F#@k"), ("shit", "s#@t"), ("goddamn", "g#@damn")])

SEQ = list(SEQ_V8)   # the script build() renders; use_script() swaps it


def use_script(name):
    """Pick the script (and the voices it was cast with)."""
    SEQ[:] = {"v2": SEQ_V2, "v3": SEQ_V3, "v4": SEQ_V4, "v5": SEQ_V5, "v6": SEQ_V6, "v7": SEQ_V7, "v8": SEQ_V8, "v9": SEQ_V9}[name]
    if name in ("v2", "v3", "v4"):
        V.update(V_OLD)


FLAT = 1.0   # stampede: seconds from the doors to the kids getting flattened
END_TEXT = ["WHAT'S THE DUMBEST THING", "YOU'D FIGHT FOR", "ON BLACK FRIDAY?"]

# ------------------------------------------------------------------------------------------------ layout
def layout(fmt):
    if fmt == "wide":
        W, H, K = 1920, 1080, 1.0
        return dict(W=W, H=H, K=K, feet=1010, cu=2.25, cap_y=935, cap_size=74, banner_y=230,
                    outside=dict(kids={"pip": 380, "mb": 720, "dot": 1060}, ground=770, store=(160, 160, 1760),
                                 doors=(1400, 300)),
                    inside=dict(kids={"pip": 360, "mb": 700, "dot": 1000}, floor=700, tv=(1460, 440, 1.0),
                                grandma_land=(360, 1010)),
                    checkout=dict(floor=700, kiosk=(1300, 1010), grandma=(880, 1010)),
                    ceo=dict(kids={"pip": 330, "mb": 960, "dot": 1590}, floor=700, screen=(560, 80, 1360, 590)),
                    cup=dict(table=760, cup=(1000, 760)),
                    pizza=dict(table=820, cx=960),
                    dawn=dict(kids={"pip": 600, "mb": 960, "dot": 1300}, horizon=660))
    W, H, K = 1080, 1920, 1.28
    return dict(W=W, H=H, K=K, feet=1640, cu=1.85, cap_y=1470, cap_size=84, banner_y=380,
                outside=dict(kids={"pip": 225, "mb": 540, "dot": 855}, ground=1160, store=(30, 520, 1050),
                             doors=(760, 290)),
                inside=dict(kids={"pip": 225, "mb": 540, "dot": 855}, floor=1150, tv=(540, 760, 1.25),
                            grandma_land=(225, 1640)),
                checkout=dict(floor=1150, kiosk=(700, 1640), grandma=(300, 1640)),
                ceo=dict(kids={"pip": 225, "mb": 540, "dot": 855}, floor=1150, screen=(50, 200, 1030, 960)),
                cup=dict(table=1260, cup=(560, 1260)),
                pizza=dict(table=1250, cx=540),
                dawn=dict(kids={"pip": 225, "mb": 540, "dot": 855}, horizon=1120))


class Cam:
    def __init__(self, L, cx, cy, z):
        self.W, self.H, self.cx, self.cy, self.z = L["W"], L["H"], cx, cy, z

    def p(self, x, y):
        return ((x - self.cx) * self.z + self.W / 2, (y - self.cy) * self.z + self.H / 2)

    def pts(self, pts):
        return [self.p(x, y) for x, y in pts]


def clampcx(L, x, z):
    h = L["W"] / (2 * z)
    return min(max(x, h), L["W"] - h)


def cams(L):
    W, H, K, F = L["W"], L["H"], L["K"], L["feet"]
    vert = H > W
    out = {}
    for scene in ("outside", "inside", "checkout", "dawn", "ceo", "cup", "pizza"):
        if scene == "ceo":
            wide = (W / 2, H / 2, 1.0)
        elif scene == "pizza":
            wide = (L["pizza"]["cx"], L["pizza"]["table"] - 220, 1.35 if not vert else 1.55)
        elif scene == "cup":
            cx_, tb_ = L["cup"]["cup"][0], L["cup"]["table"]
            wide = (cx_, tb_ - 210, 1.5) if vert else (cx_, tb_ - 190, 1.55)
        else:   # wides sit low and zoomed in so the kids read big (both formats)
            wide = (W / 2, 1160, 1.18) if vert else (W / 2, 575, 1.12)
        c = {"wide": wide}
        S = L[scene]
        z = L["cu"]
        for k, x in S.get("kids", {}).items():
            c["cu_" + k] = (clampcx(L, x, z), F - 270 * K, z)
        out[scene] = c
    o = out["outside"]
    px = L["outside"]["kids"]["pip"]
    o["cu_pip_flat"] = (clampcx(L, px + 40, L["cu"]), F - 180 * K, L["cu"])
    mx_ = L["outside"]["kids"]["mb"]
    o["cu_mb_flat"] = (clampcx(L, mx_, L["cu"] * 1.15), F - 120 * K, L["cu"] * 1.15)
    lx, ly = granny_lot(L)
    out["dawn"]["cu_granny_lot"] = (clampcx(L, lx, 2.2), ly - 150 * K, 2.2 if not vert else 1.9)
    dx_ = L["outside"]["kids"]["dot"]
    o["cu_dot_flat"] = (clampcx(L, dx_, L["cu"] * 1.15), F - 120 * K, L["cu"] * 1.15)
    i = out["inside"]
    tx, ty, ts = L["inside"]["tv"]
    i["cu_tv"] = (tx, ty - 50 * ts, 1.45 if not vert else 1.2)
    gx, gy = L["inside"]["grandma_land"]
    go = granny_on(L)
    i["cu_pip_down"] = (clampcx(L, gx + 230 * K, L["cu"]), gy - 200 * K, L["cu"])
    i["cu_grandma"] = (clampcx(L, gx + go * K, 2.4), gy - 260 * K, 2.4 if not vert else 2.1)
    x0, y0, x1, y1 = L["ceo"]["screen"]
    zc = min(W * 0.96 / (x1 - x0 + 60), H * 0.94 / (y1 - y0 + 60)) if not vert else 1.04
    out["ceo"]["cu_ceo"] = ((x0 + x1) / 2, (y0 + y1) / 2 + (0 if not vert else 120), zc)
    k = out["checkout"]
    kx, ky = L["checkout"]["kiosk"]
    k["cu_kiosk"] = (kx, ky - 330 * K, 2.0 if not vert else 1.7)
    gx, gy = L["checkout"]["grandma"]
    k["cu_grandma"] = (clampcx(L, gx + 40 * K, 2.4), gy - 170 * K, 2.4 if not vert else 2.1)
    return out


# ------------------------------------------------------------------------------------------------ props
GRANNY_SKIN, PERM, CARDI, DRESS = (244, 206, 190), (150, 96, 200), (126, 196, 156), (196, 170, 226)


def granny_body():
    return [("p", [(-14, -30), (-4, -30), (-5, -8), (-14, -8)], GRANNY_SKIN),
            ("p", [(4, -30), (14, -30), (14, -8), (5, -8)], GRANNY_SKIN),
            ("e", (-14, -6, 18, 9), WHITE), ("e", (14, -6, 18, 9), WHITE),
            ("p", [(-34, -112), (34, -112), (52, -26), (-52, -26)], DRESS),
            ("p", [(-38, -116), (-6, -116), (-12, -30), (-50, -30)], CARDI),
            ("p", [(6, -116), (38, -116), (50, -30), (12, -30)], CARDI),
            ("e", (-14, -94, 4, 4), WHITE, False), ("e", (-14, -70, 4, 4), WHITE, False),
            ("e", (-16, -46, 4, 4), WHITE, False)]


def granny_head(lvl, blink, expr):
    cy = -66
    s = []
    for (x, y, r) in [(-56, -30, 26), (-40, -62, 28), (-8, -78, 30), (28, -72, 28), (54, -44, 26), (-62, 4, 20),
                      (62, 0, 20)]:
        s.append(("e", (x, cy + y, r, r), PERM))
    s.append(("e", (0, cy, 62, 64), GRANNY_SKIN))
    s.append(("p", [(-64, cy - 40), (64, cy - 40), (62, cy - 22), (-62, cy - 22)], (228, 48, 92)))   # sweatband
    for (x, y, r) in [(-30, -52, 16), (2, -60, 18), (32, -52, 16)]:
        s.append(("e", (x, cy + y, r, r * 0.8), PERM, False))
    s.append(("p", strip([(-46, cy + 22), (-36, cy + 26)], 3), (200, 150, 140), False))
    s.append(("p", strip([(46, cy + 22), (36, cy + 26)], 3), (200, 150, 140), False))
    for side in (-1, 1):   # glasses
        ex = side * 24
        s.append(("e", (ex, cy - 2, 22, 20), (60, 40, 70)))
        s.append(("e", (ex, cy - 2, 17, 15), WHITE, False))
        if blink:
            s.append(("p", strip([(ex - 12, cy), (ex + 12, cy)], 4), INK, False))
        else:
            s.append(("e", (ex + (2 if expr == "mean" else 0), cy - 1, 6, 6), PUPIL, False))
        if expr == "mean":
            s.append(("p", strip([(ex - 18 * side, cy - 30), (ex + 16 * side, cy - 20)], 6), (120, 80, 150), False))
    s.append(("p", strip([(-4, cy - 2), (4, cy - 2)], 4), (60, 40, 70), False))
    s.append(("e", (0, cy + 14, 7, 6), (230, 170, 160), False))
    s += C.mouth(0, cy + 34, lvl, 26, "frown" if expr == "mean" else "flat", "dent")
    if lvl == 0:
        s.append(("e", (0, cy + 35, 14, 4), (210, 70, 120), False))
    return s


def granny_arm():
    return [("p", [(-8, -4), (8, -4), (8, 34), (-8, 34)], CARDI), ("e", (0, 44, 14, 13), GRANNY_SKIN)]


def kiosk_shapes():
    return [("p", [(-120, -330), (120, -330), (130, 0), (-130, 0)], (170, 178, 190)),
            ("p", [(-130, -14), (130, -14), (134, 0), (-134, 0)], (90, 96, 108)),
            ("p", [(-160, -250), (-20, -250), (-20, -228), (-160, -228)], (120, 128, 140)),        # scanner shelf
            ("p", [(-150, -248), (-40, -248), (-44, -240), (-146, -240)], (220, 60, 60), False),
            ("p", [(40, -250), (200, -250), (200, -228), (40, -228)], (120, 128, 140)),           # bagging area
            ("p", strip([(70, -250), (70, -330), (180, -330), (180, -250)], 6), (220, 220, 225)),
            ("p", strip([(-6, -330), (-6, -560)], 12), (90, 96, 108)),
            ("p", [(-150, -580), (150, -580), (140, -360), (-140, -360)], (60, 64, 76)),            # screen frame
            ("e", (0, -600, 16, 16), (255, 210, 60)),
            ("p", [(-90, -150), (90, -150), (90, -60), (-90, -60)], (150, 158, 170)),
            ("p", [(-60, -120), (60, -120), (60, -96), (-60, -96)], (60, 64, 76), False)]


def tv_shapes():
    return [("p", [(-90, 0), (90, 0), (110, 230), (-110, 230)], (246, 240, 230)),                 # pedestal
            ("p", [(-120, 220), (120, 220), (124, 246), (-124, 246)], (220, 210, 196)),
            ("p", [(-104, -10), (104, -10), (100, 8), (-100, 8)], (220, 210, 196)),
            ("p", strip([(0, -20), (0, -50)], 18), (40, 40, 46)),
            ("p", [(-270, -340), (270, -340), (270, -40), (-270, -40)], (30, 30, 36))]


def screen_glow(img, cam, x0, y0, x1, y1, t, ts):
    """The TV screen: bright paper gradient bands with a choppy sparkle."""
    rng = np.random.default_rng(int(t * FPS))
    cols = [(120, 220, 255), (90, 170, 250), (150, 110, 240), (240, 120, 200)]
    n = len(cols)
    for i, c in enumerate(cols):
        ya, yb = y0 + (y1 - y0) * i / n, y0 + (y1 - y0) * (i + 1) / n
        paper(img, cam.pts([(x0, ya), (x1, ya), (x1, yb), (x0, yb)]), c, rng, cam.z, shadow=False, jitter=False,
              edge=False)


def shopper_shapes(k):
    rng = np.random.default_rng(100 + k)
    coat = [(70, 120, 200), (200, 80, 60), (90, 160, 90), (230, 170, 60), (140, 90, 170), (60, 60, 70)][k % 6]
    skin = [(242, 198, 164), (139, 92, 62), (200, 150, 110), (250, 214, 190)][k % 4]
    h = rng.uniform(0.9, 1.15)
    s = [("p", [(-26, -80), (-6, -80), (-24, 0), (-44, 0)], (60, 60, 80)),
         ("p", [(6, -80), (26, -80), (44, 0), (24, 0)], (60, 60, 80)),
         ("p", [(-70, -300 * h), (70, -300 * h), (80, -80), (-80, -80)], coat),
         ("p", strip([(-62, -290 * h), (-120, -420 * h)], 26), coat), ("e", (-124, -430 * h, 22, 22), skin),
         ("p", strip([(62, -290 * h), (120, -420 * h)], 26), coat), ("e", (124, -430 * h, 22, 22), skin),
         ("e", (0, -370 * h, 70, 72), skin)]
    if k % 3 == 0:
        s.append(("pts", ell(0, -384 * h, 74, 70, 180, 360) + [(74, -384 * h)], [(40, 30, 26), (220, 190, 80),
                                                                                  (120, 70, 40)][k % 3]))
    s += [("e", (-24, -376 * h, 14, 16), WHITE), ("e", (24, -376 * h, 14, 16), WHITE),
          ("e", (-22, -372 * h, 6, 6), PUPIL, False), ("e", (22, -372 * h, 6, 6), PUPIL, False),
          ("p", strip([(-40, -404 * h), (-8, -394 * h)], 7), INK, False),
          ("p", strip([(40, -404 * h), (8, -394 * h)], 7), INK, False),
          ("e", (0, -330 * h, 22, 18), MOUTH, False)]
    if k % 2 == 1:   # a shopping bag
        s.append(("p", [(90, -250), (150, -250), (154, -170), (86, -170)], (240, 236, 220)))
    return s


CEO_SKIN, SUIT, GOLD = (240, 200, 176), (36, 40, 62), (236, 184, 40)


def ceo_shapes(lvl, wink):
    s = [("p", [(-250, 170), (250, 170), (300, 420), (-300, 420)], SUIT),
         ("p", [(-70, 150), (70, 150), (0, 300)], WHITE),
         ("p", [(-24, 166), (24, 166), (16, 196), (-16, 196)], GOLD),
         ("p", [(-16, 192), (16, 192), (34, 330), (0, 370), (-34, 330)], GOLD),
         ("p", [(-90, 150), (-10, 170), (-60, 300)], (50, 56, 84)), ("p", [(90, 150), (10, 170), (60, 300)], (50, 56, 84)),
         ("p", [(150, 250), (200, 250), (196, 270), (150, 270)], GOLD, False),
         ("e", (-150, -10, 26, 40), CEO_SKIN), ("e", (150, -10, 26, 40), CEO_SKIN),
         ("p", [(-46, 120), (46, 120), (50, 170), (-50, 170)], CEO_SKIN),
         ("e", (0, -10, 150, 168), CEO_SKIN),
         ("pts", ell(0, -40, 156, 150, 190, 350) + [(150, -90), (60, -120), (-40, -96), (-140, -80)], (150, 150, 162)),
         ("p", strip([(-40, -170), (-30, -110)], 6), (110, 110, 120), False)]
    for side in (-1, 1):   # smug squint: eyes as arcs with tiny pupils, brows high
        ex = side * 56
        if wink and side == -1:   # the wink: a closed, curved lid
            s.append(("p", strip([(ex - 32, -26), (ex, -36), (ex + 32, -26)], 7), INK, False))
            s.append(("p", strip([(ex - 34, -78), (ex + 30, -70)], 10), (120, 120, 130), False))
            continue
        s.append(("e", (ex, -30, 30, 18), WHITE))
        s.append(("e", (ex + 4, -26, 8, 8), PUPIL, False))
        s.append(("pts", [(x, min(y, -30)) for x, y in ell(ex, -30, 32, 20, 180, 360, 30)], CEO_SKIN, False))
        s.append(("p", strip([(ex - 36, -30), (ex + 36, -30)], 5), INK, False))
        s.append(("p", strip([(ex - 34, -78 - side * 4), (ex + 30, -82 + side * 4)], 10), (120, 120, 130), False))
    s.append(("p", [(-10, -10), (10, -10), (18, 36), (-18, 36)], (226, 176, 150), False))
    # the huge fake smile: a wide D with a full row of teeth; opens on speech
    h = [24, 46, 70][lvl]
    top = 66
    s.append(("pts", [(-104, top), (104, top)] + ell(0, top, 104, h + 10, 0, 180)[1:-1], MOUTH))
    s.append(("pts", [(-98, top + 3), (98, top + 3)] + ell(0, top + 3, 98, 26 if lvl else h, 0, 180)[1:-1], WHITE,
              False))
    for x in range(-80, 90, 20):
        s.append(("p", strip([(x, top + 4), (x, top + 18)], 2.5), (200, 200, 200), False))
    s.append(("p", strip([(-120, top - 10), (-104, top + 2)], 5), INK, False))
    s.append(("p", strip([(120, top - 10), (104, top + 2)], 5), INK, False))
    return s


@lru_cache(maxsize=256)
def spr(name, z, *key):
    if name == "granny_body":
        return render_shapes(granny_body(), z, 160, 3)
    if name == "granny_head":
        return render_shapes(granny_head(*key), z, 170, 4)
    if name == "granny_arm":
        return render_shapes(granny_arm(), z, 70, 5)
    if name == "kiosk":
        img = render_shapes(kiosk_shapes(), z, 640, 6)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        f = ImageFont.truetype(FONT, max(8, int(22 * z)))
        d.text((c, c - 108 * z), "MEGAMART", font=f, fill=WHITE, anchor="mm")
        return img
    if name == "tv":
        return render_shapes(tv_shapes(), z, 350, 7)
    if name == "shopper":
        return render_shapes(shopper_shapes(key[0]), z, 470, 8 + key[0])
    if name == "ceo":
        return render_shapes(ceo_shapes(*key), z, 440, 12)
    if name == "foot":
        return render_shapes([("e", (0, -26, 30, 46), (70, 60, 66)), ("e", (2, 48, 24, 26), (70, 60, 66)),
                              ("p", strip([(-18, -40), (18, -40)], 5), (110, 100, 106), False),
                              ("p", strip([(-22, -20), (22, -20)], 5), (110, 100, 106), False),
                              ("p", strip([(-20, 0), (20, 0)], 5), (110, 100, 106), False),
                              ("p", strip([(-12, 46), (14, 46)], 5), (110, 100, 106), False)], z, 90, 13)
    if name == "boot":
        return render_shapes([("p", [(-30, -80), (30, -80), (26, 48), (-30, 48)], (200, 52, 44)),
                              ("p", [(-30, 16), (64, 16), (70, 54), (-30, 54)], (200, 52, 44)),
                              ("e", (-2, -80, 32, 11), (120, 30, 28), False)], z, 120, 15)
    if name == "ribbon":
        img = render_shapes([("p", [(-14, 0), (-30, 70), (-6, 56), (0, 0)], (90, 140, 210)),
                             ("p", [(14, 0), (30, 70), (6, 56), (0, 0)], (90, 140, 210)),
                             ("pts", lumpy(0, -10, 36, [(3, 12, 0)]), (90, 140, 210))], z, 90, 16)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c, c - 10 * z), "TRIED", font=ImageFont.truetype(FONT, max(6, int(15 * z))), fill=WHITE, anchor="mm")
        return img
    if name == "judge":   # science-fair judge, upper body over the table edge (y = 0), turning green
        green, suit = (150, 196, 110), (70, 74, 90)
        return render_shapes([("p", [(-80, -250), (80, -250), (96, 0), (-96, 0)], suit),
                              ("p", [(-26, -250), (26, -250), (0, -170)], WHITE),
                              ("p", [(-8, -240), (8, -240), (12, -160), (0, -150), (-12, -160)], (200, 40, 32)),
                              ("e", (0, -340, 72, 78), green),
                              ("pts", ell(0, -372, 74, 50, 180, 360) + [(74, -372)], (200, 200, 205)),
                              ("e", (-46, -312, 20, 16), (176, 220, 136), False),
                              ("e", (46, -312, 20, 16), (176, 220, 136), False),
                              ("p", strip([(-44, -352), (-24, -344), (-44, -336)], 5), INK, False),
                              ("p", strip([(44, -352), (24, -344), (44, -336)], 5), INK, False),
                              ("p", strip([(-60, -230), (-30, -300)], 26), suit), ("e", (-20, -306, 24, 22), green),
                              ("p", [(60, -200), (150, -210), (150, -90), (60, -80)], (150, 104, 60)),
                              ("p", [(70, -190), (140, -198), (140, -100), (70, -92)], WHITE, False),
                              ("p", strip([(80, -170), (130, -174)], 3), (150, 150, 150), False),
                              ("p", strip([(80, -150), (130, -154)], 3), (150, 150, 150), False),
                              ("p", strip([(64, -230), (100, -170)], 26), suit)], z, 420, 17)
    if name == "worker":   # sad MEGAMART staffer at the one-slice pizza party (key: variant)
        k = key[0]
        skin = [(242, 198, 164), (139, 92, 62), (200, 150, 110), (250, 214, 190), (176, 120, 84), (230, 180, 150)][k]
        shapes = [("p", [(-60, -220), (60, -220), (70, 0), (-70, 0)], (236, 234, 226)),
                  ("p", [(-56, -216), (-26, -216), (-34, -10), (-64, -10)], (214, 44, 36)),
                  ("p", [(26, -216), (56, -216), (64, -10), (34, -10)], (214, 44, 36)),
                  ("p", [(-20, -160), (20, -160), (20, -130), (-20, -130)], (252, 214, 74), False),
                  ("e", (0, -290, 62, 64), skin),
                  ("pts", ell(0, -322, 64, 40, 180, 360) + [(90, -322)], (214, 44, 36)),
                  ("e", (-22, -292, 12, 13), WHITE), ("e", (22, -292, 12, 13), WHITE),
                  ("e", (-22, -288, 5, 5), PUPIL, False), ("e", (22, -288, 5, 5), PUPIL, False),
                  ("p", strip([(-36, -316), (-12, -306)], 5), INK, False),
                  ("p", strip([(36, -316), (12, -306)], 5), INK, False),
                  ("p", strip([(-16, -252), (0, -258), (16, -252)], 5), MOUTH, False)]
        if k == 2:   # the one party hat
            shapes.append(("p", [(-20, -350), (20, -350), (0, -420)], (252, 214, 74)))
        return render_shapes(shapes, z, 450, 30 + k)
    if name == "cart_back":   # golf cart: canopy, poles, the strapped-on TV box
        img = render_shapes([("p", strip([(-180, -150), (-180, -360)], 12), (200, 200, 205)),
                             ("p", strip([(180, -150), (180, -360)], 12), (200, 200, 205)),
                             ("p", [(-230, -390), (230, -390), (240, -350), (-240, -350)], (70, 150, 90)),
                             ("p", [(-300, -300), (-150, -300), (-150, -150), (-300, -150)], (196, 156, 104)),
                             ("p", strip([(-300, -230), (-150, -230)], 6), (90, 70, 50), False),
                             ("p", strip([(-230, -300), (-230, -150)], 6), (90, 70, 50), False)], z, 420, 40)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c - 225 * z, c - 262 * z), "TV", font=ImageFont.truetype(FONT, max(6, int(40 * z))), fill=INK,
               anchor="mm")
        return img
    if name == "cart_front":
        return render_shapes([("p", [(-260, -160), (250, -160), (270, -50), (-270, -50)], (246, 244, 236)),
                              ("p", [(-270, -90), (270, -90), (272, -70), (-272, -70)], (70, 150, 90), False),
                              ("e", (-170, -40, 46, 46), (40, 40, 46)), ("e", (170, -40, 46, 46), (40, 40, 46)),
                              ("e", (-170, -40, 18, 18), (170, 170, 180), False),
                              ("e", (170, -40, 18, 18), (170, 170, 180), False),
                              ("e", (262, -120, 14, 10), (252, 230, 120))], z, 420, 41)
    if name == "results":   # a paper of DNA results (episode 8)
        img = render_shapes([("p", [(-34, -46), (34, -48), (36, 46), (-32, 48)], WHITE)], z, 70, 19)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c, c - 30 * z), "DNA", font=ImageFont.truetype(FONT, max(6, int(16 * z))), fill=(200, 40, 32),
               anchor="mm")
        for k in range(4):
            d.line([(c - 24 * z, c + (-10 + k * 14) * z), (c + 24 * z, c + (-10 + k * 14) * z)], fill=(150, 150, 150),
                   width=max(1, int(3 * z)))
        return img
    if name == "slice":   # a slice of cold pie (episode 2, dawn)
        return render_shapes([("p", [(-30, -20), (30, -24), (0, 40)], (178, 92, 60)),
                              ("p", strip([(-32, -20), (32, -24)], 12), (226, 180, 110))], z, 60, 18)
    if name == "palm":
        hand = C.CAST[key[0]]["hand"]
        return render_shapes([("e", (0, 0, 48, 36), hand), ("e", (-42, 12, 13, 19, 0, 360, None, 20), hand)], z, 80,
                             14)
    if name == "sock":
        return render_shapes([("p", [(-14, -40), (14, -40), (14, 20), (40, 26), (40, 46), (-14, 46)], WHITE),
                              ("p", [(-14, -40), (14, -40), (14, -26), (-14, -26)], (200, 40, 32), False),
                              ("p", [(-14, -16), (14, -16), (14, -6), (-14, -6)], (200, 40, 32), False)], z, 70, 9)
    if name == "box":
        img = render_shapes([("p", [(-150, -190), (150, -190), (150, 0), (-150, 0)], (196, 156, 104)),
                             ("p", [(-150, -190), (150, -190), (150, -170), (-150, -170)], (170, 130, 84), False)],
                            z, 220, 10)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c, c - 100 * z), 'TV 75"', font=ImageFont.truetype(FONT, max(8, int(48 * z))), fill=INK,
               anchor="mm")
        return img
    if name == "star":
        pts = []
        for i in range(22):
            r = 150 if i % 2 == 0 else 70 + (i * 37 % 30)
            a = i * math.pi / 11
            pts.append((r * math.cos(a), r * math.sin(a)))
        inner = [(x * 0.55, y * 0.55) for x, y in pts]
        img = render_shapes([("pts", pts, (252, 214, 74)), ("pts", inner, (240, 80, 40))], z, 170, 11)
        d = ImageDraw.Draw(img)
        c = img.size[0] / 2
        d.text((c, c), key[0], font=ImageFont.truetype(FONT, max(8, int(46 * z))), fill=WHITE, anchor="mm",
               stroke_width=max(1, int(4 * z)), stroke_fill=INK)
        return img
    raise KeyError(name)


# ------------------------------------------------------------------------------------------------ backgrounds
def bg_outside(L, cam):
    W, H, z = L["W"], L["H"], cam.z
    S = L["outside"]
    rng = np.random.default_rng(21)
    img = Image.new("RGBA", (W, H))
    full = [(-400, -400), (W + 400, -400), (W + 400, H + 400), (-400, H + 400)]
    paper(img, cam.pts(full), (28, 34, 70), rng, z, shadow=False, jitter=False, edge=False)
    for i in range(26):
        x, y = (i * 389) % W, (i * 211) % int(S["ground"] * 0.45)
        paper(img, cam.pts(ell(x, y, 5, 5, n=10)), (240, 236, 200), rng, z, shadow=False, jitter=False, edge=False)
    mx = W * 0.08 if W > H else W * 0.12
    paper(img, cam.pts(ell(mx + 60, 100, 50, 50)), (244, 240, 210), rng, z)
    paper(img, cam.pts(ell(mx + 84, 86, 44, 44)), (28, 34, 70), rng, z, shadow=False)
    g = S["ground"]
    paper(img, cam.pts([(-400, g), (W + 400, g), (W + 400, H + 400), (-400, H + 400)]), (88, 90, 98), rng, z,
          shadow=False)
    for i in range(-2, 9):
        x = i * (W / 6)
        paper(img, cam.pts(strip([(x, g + 40), (x - 240, H + 40)], 10)), (226, 200, 60), rng, z, shadow=False)
    x0, top, x1 = S["store"]
    paper(img, cam.pts([(x0, top + 80), (x1, top + 80), (x1, g), (x0, g)]), (206, 196, 176), rng, z, sh=8)
    paper(img, cam.pts([(x0 - 20, top + 60), (x1 + 20, top + 60), (x1 + 20, top + 100), (x0 - 20, top + 100)]),
          (176, 60, 52), rng, z)
    for k in range(5):   # windows glow
        wx = x0 + 60 + k * (x1 - x0 - 120) / 5
        if abs(wx + (x1 - x0 - 120) / 10 - S["doors"][0]) < S["doors"][1] * 0.75:
            continue
        paper(img, cam.pts([(wx, g - 300), (wx + (x1 - x0 - 120) / 5 - 30, g - 300),
                            (wx + (x1 - x0 - 120) / 5 - 30, g - 60), (wx, g - 60)]), (250, 226, 150), rng, z)
    # sign
    cx = (x0 + x1) / 2
    sw = (x1 - x0) * 0.62
    paper(img, cam.pts([(cx - sw / 2, top - 30), (cx + sw / 2, top - 40), (cx + sw / 2, top + 70),
                        (cx - sw / 2, top + 76)]), (214, 44, 36), rng, z, sh=8)
    d = ImageDraw.Draw(img)
    fs = int(sw / 6.0 * z)
    d.text(cam.p(cx, top + 18), "MEGAMART", font=ImageFont.truetype(FONT, fs), fill=WHITE, anchor="mm",
           stroke_width=max(1, int(3 * z)), stroke_fill=(120, 20, 20))
    # banner on the facade
    dx, dw = S["doors"]
    bx = (x0 + dx - dw / 2) / 2 if W > H else cx - 120
    by = g - 380 if W > H else top + 180
    bw = 520 if W > H else 400
    paper(img, cam.pts([(bx - bw / 2, by - 50), (bx + bw / 2, by - 44), (bx + bw / 2 - 6, by + 50),
                        (bx - bw / 2 + 4, by + 46)]), (252, 214, 74), rng, z, sh=6)
    d.text(cam.p(bx, by), "DOORBUSTERS!", font=ImageFont.truetype(FONT, int(56 * z * bw / 520)), fill=INK,
           anchor="mm")
    # door frame (doors themselves are dynamic)
    paper(img, cam.pts([(dx - dw / 2 - 20, g - 360), (dx + dw / 2 + 20, g - 360), (dx + dw / 2 + 20, g),
                        (dx - dw / 2 - 20, g)]), (70, 74, 84), rng, z)
    paper(img, cam.pts([(dx - dw / 2, g - 340), (dx + dw / 2, g - 340), (dx + dw / 2, g), (dx - dw / 2, g)]),
          (255, 236, 170), rng, z, shadow=False)
    return C.vignette(img)


def bg_inside(L, cam, scene):
    W, H, z = L["W"], L["H"], cam.z
    S = L[scene]
    rng = np.random.default_rng(31)
    img = Image.new("RGBA", (W, H))
    fl = S["floor"]
    paper(img, cam.pts([(-400, -400), (W + 400, -400), (W + 400, fl), (-400, fl)]), (232, 226, 206), rng, z,
          shadow=False, jitter=False, edge=False)
    for k in range(-1, 6):   # ceiling lights
        x = k * W / 4 + 80
        paper(img, cam.pts([(x - 110, 30), (x + 110, 30), (x + 110, 54), (x - 110, 54)]), (255, 250, 230), rng, z)
    paper(img, cam.pts([(-400, fl), (W + 400, fl), (W + 400, H + 400), (-400, H + 400)]), (196, 200, 206), rng, z,
          shadow=False)
    step = 140
    for i in range(0, int((H + 400 - fl) / step) + 1):
        y = fl + 30 + i * step * (1 + 0.15 * i)
        paper(img, cam.pts(strip([(-400, y), (W + 400, y)], 5)), (170, 174, 182), rng, z, shadow=False)
    for i in range(-6, 16):
        x = W / 2 + i * 160
        paper(img, cam.pts(strip([(W / 2 + i * 60, fl), (x, H + 400)], 5)), (170, 174, 182), rng, z,
              shadow=False)
    # shelves with product boxes
    shelves = [(40, 560), (W - 520, W - 40)] if W > H else [(-40, 300), (W - 300, W + 40)]
    if scene == "checkout":
        shelves = [(40, 560)] if W > H else [(-40, 260)]
    pal = [(214, 44, 36), (40, 120, 200), (252, 214, 74), (90, 170, 90), (240, 140, 60), (150, 96, 200)]
    for (a, b) in shelves:
        paper(img, cam.pts([(a, fl - 520), (b, fl - 520), (b, fl), (a, fl)]), (150, 158, 170), rng, z, sh=7)
        for r in range(4):
            y = fl - 500 + r * 125
            paper(img, cam.pts([(a + 10, y + 100), (b - 10, y + 100), (b - 10, y + 112), (a + 10, y + 112)]),
                  (110, 116, 128), rng, z, shadow=False)
            x = a + 20
            k = r * 3
            while x < b - 70:
                w = 50 + (k * 17) % 40
                hh = 60 + (k * 23) % 36
                paper(img, cam.pts([(x, y + 100 - hh), (x + w, y + 100 - hh), (x + w, y + 100), (x, y + 100)]),
                      pal[k % 6], rng, z, sh=3)
                x += w + 10
                k += 1
    if scene == "inside":
        tx, ty, ts = S["tv"]
        # spotlight cone
        paper(img, cam.pts([(tx - 60 * ts, -50), (tx + 60 * ts, -50), (tx + 300 * ts, fl + 60),
                            (tx - 300 * ts, fl + 60)]), (255, 246, 196), rng, z, shadow=False, grain=0.03)
        d = ImageDraw.Draw(img)
        sx, sy = cam.p(tx, ty - 300 * ts)
        d.text((sx, sy), "ONLY 1 LEFT!", font=ImageFont.truetype(FONT, int(44 * z * ts)), fill=(214, 44, 36),
               anchor="mm", stroke_width=max(1, int(4 * z)), stroke_fill=WHITE)
    if scene == "checkout":
        paper(img, cam.pts([(W * 0.62 if W > H else W * 0.4, 70), (W - 40 if W > H else W - 30, 70),
                            (W - 40 if W > H else W - 30, 150), (W * 0.62 if W > H else W * 0.4, 150)]),
              (40, 120, 200), rng, z)
        d = ImageDraw.Draw(img)
        sx, sy = cam.p(((W * 0.62 if W > H else W * 0.4) + (W - 40 if W > H else W - 30)) / 2, 110)
        d.text((sx, sy), "SELF CHECKOUT", font=ImageFont.truetype(FONT, int(44 * z)), fill=WHITE, anchor="mm")
    return C.vignette(img)


def bg_ceo(L, cam):
    img = bg_inside(L, cam, "ceo")
    x0, y0, x1, y1 = L["ceo"]["screen"]
    rng = np.random.default_rng(51)
    paper(img, cam.pts([(x0 - 26, y0 - 26), (x1 + 26, y0 - 26), (x1 + 26, y1 + 26), (x0 - 26, y1 + 26)]),
          (34, 34, 40), rng, cam.z, sh=10)
    return img


def draw_screen(fr, cam, t, li):
    L = G["L"]
    x0, y0, x1, y1 = L["ceo"]["screen"]
    rng = np.random.default_rng(int(t * FPS))
    if t < G["ev"]["ceo_in"] + 0.3:   # static, then the CEO pops on
        a, b = cam.p(x0, y0)
        c_, d = cam.p(x1, y1)
        w, h = int(c_ - a), int(d - b)
        if w > 0 and h > 0:
            n = Image.effect_noise((max(1, w // 6), max(1, h // 6)), 80).resize((w, h), Image.NEAREST).convert("RGBA")
            paste(fr, n, (a + c_) / 2, (b + d) / 2)
        return
    bands = [(70, 140, 220), (90, 160, 230), (110, 180, 236)]
    for i, col in enumerate(bands):
        ya, yb = y0 + (y1 - y0) * i / 3, y0 + (y1 - y0) * (i + 1) / 3
        paper(fr, cam.pts([(x0, ya), (x1, ya), (x1, yb), (x0, yb)]), col, rng, cam.z, shadow=False, jitter=False,
              edge=False)
    ln = G["lines"][li] if li is not None else None
    lvl = mouth_level(ln, t) if ln is not None and ln["who"] == "ceo" else 0
    sc = (y1 - y0) / 1000
    hop = -8 if ln is not None and ln["who"] == "ceo" and any(0 <= t - s < 0.09 for s, _, _ in ln["words"]) else 0
    k_ = (y1 - y0 - 40) / 560
    hands0 = G.get("hands_from", 1e9) <= t < G.get("hands_until", 0)
    cx, cy = cam.p((x0 + x1) / 2 - (x1 - x0) * (0.2 if hands0 else 0), y0 + 30 + 180 * k_ + hop)
    wink = ln is not None and ln["who"] == "ceo" and any(w[2].startswith("Merry") and t >= w[0] for w in ln["words"])
    hands = G.get("hands_from", 1e9) <= t < G.get("hands_until", 0)
    if hands:
        lvl = max(lvl, 1)   # the grin widens
    held = (not wink) and G.get("wink_from", 1e9) <= t < G.get("wink_until", 0)
    img = spr("ceo", round(cam.z * k_, 3), lvl, wink or held)
    # clip the CEO to the screen
    layer = Image.new("RGBA", fr.size)
    paste(layer, img, cx, cy, float(rng.uniform(-1.5, 1.5)))
    a, b = cam.p(x0, y0)
    c_, d = cam.p(x1, y1)
    box = (max(0, int(a)), max(0, int(b)), min(fr.size[0], int(c_)), min(fr.size[1], int(d)))
    if box[2] > box[0] and box[3] > box[1]:
        fr.alpha_composite(layer.crop(box), box[:2])
    if hands:   # a paper "factory photo" inset: a conveyor of TVs and a row of tiny mitten hands, no faces
        px0, py0 = x0 + (x1 - x0) * 0.58, y0 + (y1 - y0) * 0.1
        pw, ph = (x1 - x0) * 0.36, (y1 - y0) * 0.42
        rng2 = np.random.default_rng(5)
        paper(fr, cam.pts([(px0 - 8, py0 - 8), (px0 + pw + 8, py0 - 6), (px0 + pw + 6, py0 + ph + 8),
                           (px0 - 6, py0 + ph + 6)]), (250, 250, 244), rng2, cam.z, sh=5)
        paper(fr, cam.pts([(px0, py0), (px0 + pw, py0), (px0 + pw, py0 + ph), (px0, py0 + ph)]), (150, 154, 160), rng2,
              cam.z, shadow=False, jitter=False)
        bel = py0 + ph * 0.55
        paper(fr, cam.pts([(px0, bel), (px0 + pw, bel), (px0 + pw, bel + ph * 0.12), (px0, bel + ph * 0.12)]),
              (60, 60, 66), rng2, cam.z, shadow=False, jitter=False)
        for k in range(3):   # TVs on the belt
            tx_ = px0 + pw * (0.12 + 0.3 * k)
            paper(fr, cam.pts([(tx_, bel - ph * 0.26), (tx_ + pw * 0.2, bel - ph * 0.26), (tx_ + pw * 0.2, bel),
                               (tx_, bel)]), (30, 30, 36), rng2, cam.z, shadow=False)
        for k in range(9):   # tiny mittens reaching up from below the belt
            hx_ = px0 + pw * (0.07 + 0.105 * k)
            hy_ = bel + ph * (0.22 + 0.05 * ((k + int(t * FPS)) % 2))
            paper(fr, cam.pts(ell(hx_, hy_, pw * 0.03, ph * 0.045)), (240, 196, 160), rng2, cam.z, shadow=False)
            paper(fr, cam.pts(strip([(hx_, hy_ + ph * 0.04), (hx_, py0 + ph)], pw * 0.025)), (110, 120, 140), rng2,
                  cam.z, shadow=False)
        dr = ImageDraw.Draw(fr)
        dr.text(cam.p(px0 + pw / 2, py0 + ph + 30 * k_), "MADE WITH LOVE*", font=ImageFont.truetype(
            FONT, max(8, int(24 * cam.z * k_))), fill=WHITE, anchor="mm", stroke_width=2, stroke_fill=INK)
    if wink or held:   # gold sparkles around the grin
        dr = ImageDraw.Draw(fr)
        for k in range(5):
            a = k * 72 + (int(t * FPS) % 2) * 30
            r = 250 * k_ + (int(t * FPS) % 2) * 20 * k_
            qx, qy = cam.p((x0 + x1) / 2 + r * math.cos(math.radians(a)) * 1.3,
                           y0 + 30 + 180 * k_ + r * 0.8 * math.sin(math.radians(a)))
            s_ = (18 + 6 * (k % 2)) * cam.z * k_ * 1.4
            dr.polygon([(qx, qy - s_), (qx + s_ * 0.3, qy - s_ * 0.3), (qx + s_, qy), (qx + s_ * 0.3, qy + s_ * 0.3),
                        (qx, qy + s_), (qx - s_ * 0.3, qy + s_ * 0.3), (qx - s_, qy), (qx - s_ * 0.3, qy - s_ * 0.3)],
                       fill=(252, 214, 74), outline=(150, 110, 20))
    # lower third
    ly = y1 - 70 * sc * 1.4
    paper(fr, cam.pts([(x0, ly), (x1, ly), (x1, y1), (x0, y1)]), (214, 44, 36), rng, cam.z, shadow=False,
          jitter=False, edge=False)
    dr = ImageDraw.Draw(fr)
    dr.text(cam.p((x0 + x1) / 2, (ly + y1) / 2), "MEGAMART CEO  •  A MESSAGE FROM THE TOP",
            font=ImageFont.truetype(FONT, max(8, int(30 * cam.z * sc * 1.4))), fill=WHITE, anchor="mm")


def bg_cup(L, cam):
    """Cutaway: Pip's science-fair 'volcano' (a sad brown blob in a paper cup with a tiny flag)."""
    W, H, z = L["W"], L["H"], cam.z
    S = L["cup"]
    rng = np.random.default_rng(61)
    img = Image.new("RGBA", (W, H))
    tb = S["table"]
    paper(img, cam.pts([(-50, -50), (W + 50, -50), (W + 50, H + 50), (-50, H + 50)]), (206, 220, 196), rng, z,
          shadow=False, jitter=False, edge=False)
    for k in range(-2, 14):   # cinder-block gym wall
        y = tb - 120 - k * 90
        paper(img, cam.pts(strip([(-50, y), (W + 50, y)], 4)), (184, 198, 174), rng, z, shadow=False)
    cx, cy = S["cup"]
    bw = 520 if W > H else 460
    bh = 380 if W > H else 420
    # tri-fold board
    for (a, b) in ((cx - bw * 0.95, cx - bw * 0.5), (cx - bw * 0.5, cx + bw * 0.5), (cx + bw * 0.5, cx + bw * 0.95)):
        paper(img, cam.pts([(a, tb - bh - 60), (b, tb - bh - 70), (b, tb - 20), (a, tb - 20)]), (250, 248, 240),
              rng, z, sh=6)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, int(54 * z))
    d.text(cam.p(cx, tb - bh - 12), "MY VOLCANO", font=f, fill=(214, 44, 36), anchor="mm")
    d.text(cam.p(cx, tb - bh + 36), "by Pip", font=ImageFont.truetype(FONT, int(30 * z)), fill=(40, 40, 60),
           anchor="mm")
    for k in range(3):   # crayon doodles on the side panels
        y = tb - bh + 40 + k * 70
        paper(img, cam.pts(strip([(cx - bw * 0.88, y), (cx - bw * 0.58, y + 10)], 6)), (90, 140, 210), rng, z,
              shadow=False)
        paper(img, cam.pts(strip([(cx + bw * 0.58, y + 10), (cx + bw * 0.88, y)], 6)), (90, 140, 210), rng, z,
              shadow=False)
    # table
    paper(img, cam.pts([(-50, tb), (W + 50, tb), (W + 50, H + 50), (-50, H + 50)]), (176, 124, 74), rng, z, sh=8)
    paper(img, cam.pts([(-50, tb), (W + 50, tb), (W + 50, tb + 24), (-50, tb + 24)]), (150, 102, 60), rng, z,
          shadow=False)
    # the cup and the blob
    paper(img, cam.pts([(cx - 70, tb - 150), (cx + 70, tb - 150), (cx + 52, tb), (cx - 52, tb)]), (250, 250, 246),
          rng, z, sh=6)
    paper(img, cam.pts([(cx - 66, tb - 120), (cx + 66, tb - 120), (cx + 63, tb - 100), (cx - 63, tb - 100)]),
          (214, 44, 36), rng, z, shadow=False)
    blob = (102, 66, 40)
    for (bx, by, r) in [(0, -160, 66), (6, -205, 48), (-2, -240, 32), (4, -262, 16)]:
        paper(img, cam.pts(lumpy(cx + bx, tb + by, r, [(3, 5, bx), (2, 9, by)])), blob, rng, z, sh=4)
    paper(img, cam.pts(strip([(cx + 4, tb - 270), (cx + 4, tb - 330)], 5)), (220, 196, 150), rng, z, shadow=False)
    paper(img, cam.pts([(cx + 6, tb - 330), (cx + 62, tb - 316), (cx + 6, tb - 302)]), (214, 44, 36), rng, z, sh=3)
    # participation ribbon
    rx, ry = cx + 170, tb - 120
    paper(img, cam.pts([(rx - 16, ry), (rx - 30, ry + 70), (rx - 6, ry + 56), (rx, ry)]), (90, 140, 210), rng, z)
    paper(img, cam.pts([(rx + 16, ry), (rx + 30, ry + 70), (rx + 6, ry + 56), (rx, ry)]), (90, 140, 210), rng, z)
    paper(img, cam.pts(ell(rx, ry - 10, 34, 34)), (90, 140, 210), rng, z)
    d.text(cam.p(rx, ry - 10), "TRIED", font=ImageFont.truetype(FONT, int(14 * z)), fill=WHITE, anchor="mm")
    return C.vignette(img)


def bg_pizza(L, cam):
    """Cutaway: the staff 'pizza party'. Six sad staffers, one slice, a drooping banner."""
    W, H, z = L["W"], L["H"], cam.z
    S = L["pizza"]
    K = L["K"]
    rng = np.random.default_rng(71)
    img = Image.new("RGBA", (W, H))
    tb, cx = S["table"], S["cx"]
    paper(img, cam.pts([(-400, -400), (W + 400, -400), (W + 400, H + 400), (-400, H + 400)]), (214, 206, 180), rng, z,
          shadow=False, jitter=False, edge=False)
    paper(img, cam.pts([(-400, tb - 60), (W + 400, tb - 60), (W + 400, H + 400), (-400, H + 400)]), (150, 150, 156),
          rng, z, shadow=False)
    # drooping bunting + banner
    span = 620 if W > H else 460
    pts = [(cx - span + i * span / 6, tb - 640 + 70 * math.sin(math.pi * i / 12)) for i in range(13)]
    paper(img, cam.pts(strip(pts, 5)), (90, 90, 96), rng, z, shadow=False)
    for i in range(12):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        paper(img, cam.pts([(ax + 4, ay), (bx - 4, by), ((ax + bx) / 2, (ay + by) / 2 + 50)]),
              [(214, 44, 36), (252, 214, 74), (90, 140, 210)][i % 3], rng, z, sh=3)
    paper(img, cam.pts([(cx - 230, tb - 520), (cx + 230, tb - 540), (cx + 236, tb - 470), (cx - 224, tb - 440)]),
          (252, 250, 240), rng, z, sh=6)
    d = ImageDraw.Draw(img)
    d.text(cam.p(cx, tb - 490), "PIZZA PARTY!", font=ImageFont.truetype(FONT, int(50 * z)), fill=(214, 44, 36),
           anchor="mm")
    # six staffers behind the table
    xs = [-330, -200, -70, 70, 200, 330] if W > H else [-300, -180, -60, 60, 180, 300]
    for k, dx in enumerate(xs):
        paste(img, spr("worker", round(z * K * 0.9, 3), k), *cam.p(cx + dx * K * 0.9, tb + 110 - (k % 2) * 30))
    # table, plate, one slice
    paper(img, cam.pts([(cx - 440 * K, tb), (cx + 440 * K, tb), (cx + 450 * K, tb + 230 * K),
                        (cx - 450 * K, tb + 230 * K)]), (240, 238, 230), rng, z, sh=8)   # paper tablecloth
    for j in range(-4, 5):
        paper(img, cam.pts([(cx + (j * 100 - 22) * K, tb + 10), (cx + (j * 100 + 22) * K, tb + 10),
                            (cx + (j * 100 + 24) * K, tb + 220 * K), (cx + (j * 100 - 24) * K, tb + 220 * K)]),
              (214, 44, 36), rng, z, shadow=False)
    paper(img, cam.pts(ell(cx, tb + 10, 90 * K, 22 * K)), (250, 250, 246), rng, z, sh=4)
    sl = [(cx - 50 * K, tb + 2), (cx + 50 * K, tb - 6), (cx + 6 * K, tb + 22)]
    paper(img, cam.pts(sl), (250, 206, 90), rng, z, sh=3)
    paper(img, cam.pts(strip([(cx - 52 * K, tb + 2), (cx + 52 * K, tb - 6)], 9 * K)), (200, 140, 70), rng, z, sh=2)
    for (px, py) in ((-14, 4), (14, 2), (2, 12)):
        paper(img, cam.pts(ell(cx + px * K, tb + py * K - 2, 6 * K, 4 * K)), (200, 52, 44), rng, z, shadow=False,
              jitter=False, edge=False)
    return C.vignette(img)


def draw_flies(fr, cam, t):
    """Two choppy flies circling the blob."""
    cx, cy = G["L"]["cup"]["cup"]
    tb = G["L"]["cup"]["table"]
    fi = int(t * FPS)
    d = ImageDraw.Draw(fr)
    for k in range(2):
        a = fi * 0.9 + k * math.pi
        x, y = cam.p(cx + 120 * math.cos(a), tb - 250 + 50 * math.sin(a * 1.3))
        r = 7 * cam.z
        d.ellipse((x - r, y - r, x + r, y + r), fill=(30, 30, 34))
        w = 9 * cam.z
        d.ellipse((x - w * 1.6, y - w * 1.4, x - w * 0.2, y - w * 0.2), fill=(220, 236, 250), outline=(60, 60, 70))
        d.ellipse((x + w * 0.2, y - w * 1.4, x + w * 1.6, y - w * 0.2), fill=(220, 236, 250), outline=(60, 60, 70))


def bg_dawn(L, cam):
    W, H, z = L["W"], L["H"], cam.z
    S = L["dawn"]
    rng = np.random.default_rng(41)
    img = Image.new("RGBA", (W, H))
    hz_ = S["horizon"]
    bands = [(84, 70, 140), (160, 90, 150), (236, 120, 130), (250, 170, 110), (252, 210, 130)]
    for i, c in enumerate(bands):
        y0 = -400 if i == 0 else hz_ * i / len(bands)
        paper(img, cam.pts([(-400, y0), (W + 400, y0 + 6), (W + 400, hz_ + 10), (-400, hz_ + 10)]), c, rng, z,
              shadow=False, edge=False)
    sx = W * 0.72
    paper(img, cam.pts(ell(sx, hz_, 120, 120, 180, 360)), (255, 236, 160), rng, z, shadow=False)
    # distant store silhouette
    x0 = W * 0.06
    paper(img, cam.pts([(x0, hz_ - 150), (x0 + 420, hz_ - 150), (x0 + 420, hz_), (x0, hz_)]), (120, 84, 120), rng, z)
    paper(img, cam.pts([(x0 + 80, hz_ - 190), (x0 + 340, hz_ - 194), (x0 + 340, hz_ - 150), (x0 + 80, hz_ - 150)]),
          (160, 70, 90), rng, z)
    paper(img, cam.pts([(-400, hz_), (W + 400, hz_), (W + 400, H + 400), (-400, H + 400)]), (96, 92, 104), rng, z,
          shadow=False)
    for i in range(-2, 9):
        x = i * (W / 6)
        paper(img, cam.pts(strip([(x, hz_ + 30), (x - 260, H + 40)], 10)), (226, 200, 60), rng, z, shadow=False)
    # litter: paper scraps, a torn box, a tipped cart
    for k in range(14):
        x, y = (k * 331) % W, hz_ + 60 + (k * 173) % int(H - hz_ - 80)
        paper(img, cam.pts([(x, y), (x + 40, y - 8), (x + 46, y + 22), (x + 4, y + 26)]),
              [(240, 236, 220), (214, 44, 36), (252, 214, 74)][k % 3], rng, z, sh=3)
    cx, cy = (W * 0.86, hz_ + 120) if W > H else (W * 0.82, hz_ + 140)
    paper(img, cam.pts(strip([(cx - 90, cy - 60), (cx + 90, cy - 40), (cx + 70, cy + 40), (cx - 70, cy + 20),
                              (cx - 90, cy - 60)], 8)), (180, 186, 196), rng, z)
    for wx in (-60, 50):
        paper(img, cam.pts(ell(cx + wx, cy + 50, 14, 14)), (40, 40, 46), rng, z)
    return C.vignette(img)


# ------------------------------------------------------------------------------------------------ timeline
G = {}


def voice(who, say, v=None):
    mp3 = fv.make(v or V[who], say)
    words = json.load(open(mp3 + ".words.json"))
    return load_audio(mp3), words


GD = {}   # gag name -> seconds (filled by build)
BLEEP = 0.36   # seconds of 1 kHz tone per [BLEEP]; the voice is silent there


def all_take(seg):
    """The three kids in unison. "yeah." alone voices badly, so it is cut from a "Heck yeah." take at the k stop
    (the cut part is thrown away, never heard)."""
    parts = []
    for k, g in (("pip", 0.6), ("mb", 0.6), ("dot", 0.6)):
        if seg.strip().lower() == "yeah.":
            a_, _ = voice(k, "Heck yeah.")
            e = np.array([np.sqrt(np.mean(a_[i:i + 441] ** 2)) for i in range(0, len(a_) - 441, 441)])
            lo, hi = int(len(e) * 0.2), int(len(e) * 0.6)
            a_ = a_[(lo + int(np.argmin(e[lo:hi]))) * 441:] * (g if k != "dot" else 0.3)
        else:
            a_ = voice(k, seg)[0] * g
        parts.append(a_)
    A = np.zeros(max(len(x) for x in parts), np.float32)
    for x in parts:
        A[:len(x)] += x
    return A, None


def voice_line(who, say, o):
    """Audio + word times for a line. Each [BLEEP] splits the line: the pieces are voiced separately and a
    silent gap of BLEEP s goes where the bleeped word is (tone added in the mix, caption #@%!)."""
    pieces = say.split("[BLEEP]")
    audio, words, bwins, t = [], [], [], 0.0
    for i, seg in enumerate(pieces):
        seg = seg.strip().lstrip(".!,?").strip()
        if seg:
            if who == "all":
                a_, _ = all_take(seg)
                w_ = None
            elif "+" in who:   # two characters in unison ("rick+kaylee")
                parts = [voice(k, seg)[0] * 0.65 for k in who.split("+")]
                a_ = np.zeros(max(len(x) for x in parts), np.float32)
                for x in parts:
                    a_[:len(x)] += x
                w_ = None
            else:
                a_, w_ = voice(who, seg, o.get("voice"))
            sw = seg.split()
            if w_ is None or len(w_) != len(sw):
                d = len(a_) / SR
                w_ = [(d * j / len(sw), d * (j + 1) / len(sw), x) for j, x in enumerate(sw)]
            words += [(t + s_, t + e_, w) for s_, e_, w in w_]
            audio.append(a_)
            t += len(a_) / SR
        if i < len(pieces) - 1:
            n = int(BLEEP * SR)
            audio.append(np.zeros(n, np.float32))
            bwins.append((t, t + BLEEP))
            words.append((t, t + BLEEP, "#@%!"))
            t += BLEEP
    return np.concatenate(audio).astype(np.float32), words, bwins


def build():
    t = 0.0
    lines, segs, ev = [], [], {}
    for it in SEQ:
        if it[0] == "gag":
            _, name, dur, scene, cam = it
            ev[name] = t
            GD[name] = dur
            segs.append((t, scene, cam))
            t += dur
            continue
        if it[0] == "hold":
            sc, cm = it[2].split("/") if "/" in it[2] else (segs[-1][1], it[2])
            segs.append((t, sc, cm))
            t += it[1]
            continue
        _, who, say, cap, o = it
        pre = o.get("beep", 0)
        audio, words, bwins = voice_line(who, say, o)
        start = t + pre
        if cap and "[BLEEP]" not in cap:   # a caption that only changes how words are shown ("...we stepped")
            cw = cap.split()
            words = [(s_, e_, cw[j] if j < len(cw) else w) for j, (s_, e_, w) in enumerate(words)]
        ln = dict(who=who, start=start, dur=len(audio) / SR, audio=audio, pre=pre, bleep=0,
                  beep=o.get("beep", 0), t0=t, scene=o["scene"],
                  words=[(start + s_, start + e_, w) for s_, e_, w in words],
                  bwins=[(start + a_, start + b_) for a_, b_ in bwins])
        env = np.sqrt(np.convolve(audio ** 2, np.ones(1470) / 1470, "same"))
        ln["rms_pk"] = float(np.percentile(env, 98))
        for wi, cam in o["cams"]:
            sc, cm = cam.split("/") if "/" in cam else (o["scene"], cam)
            segs.append((t if wi == 0 else ln["words"][wi][0] - 0.04, sc, cm))
        lines.append(ln)
        t = start + ln["dur"] + o.get("gap", 0.15)
    return lines, segs, ev, t


def seg_at(t):
    s = G["segs"][0]
    for x in G["segs"]:
        if x[0] <= t:
            s = x
    return s


def speaking(t):
    for i, ln in enumerate(G["lines"]):
        if ln["t0"] - 0.02 <= t <= ln["start"] + ln["dur"]:
            return i
    return None


def mouth_level(ln, t):
    if ln["bleep"] and ln["t0"] <= t < ln["start"]:
        return 2
    if any(a <= t < b for a, b in ln.get("bwins", ())):
        return 2
    if not any(s - 0.03 <= t <= e + 0.02 for s, e, _ in ln["words"]):
        return 0
    a = ln["audio"]
    i = int((t - ln["start"]) * SR)
    seg = a[max(0, i - SR // 30):i + SR // 30]
    if not len(seg):
        return 0
    r = float(np.sqrt(np.mean(seg ** 2)))
    return 2 if r > 0.5 * ln["rms_pk"] else 1 if r > 0.14 * ln["rms_pk"] else 0


# ------------------------------------------------------------------------------------------------ characters
def paste(fr, im, x, y, ang=0.0):
    if ang:
        im = im.rotate(ang, resample=Image.BICUBIC)
    S = im.size
    x0, y0 = int(round(x - S[0] / 2)), int(round(y - S[1] / 2))
    W, H = fr.size
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x0 + S[0]), min(H, y0 + S[1])
    if cx1 > cx0 and cy1 > cy0:
        fr.alpha_composite(im.crop((cx0 - x0, cy0 - y0, cx1 - x0, cy1 - y0)), (cx0, cy0))


def kid_pose(c, t, fi, li):
    """(hop, (jx, jy), head angle, (armL, armR), head key, squash, rot, extra)."""
    lines = G["lines"]
    ev = G["ev"]
    rng = np.random.default_rng(fi * 31 + {"mb": 1, "pip": 2, "dot": 3}[c])
    base = {"mb": "norm", "pip": "worried", "dot": "deadpan"}[c]
    lvl, hop, aL, aR, expr, ang = 0, 0.0, -12.0, 12.0, base, 0.0
    jit = {"pip": 2.2, "mb": 1.2, "dot": 0.6}[c]
    squash, rot, extra = 1.0, 0.0, {}
    ln = lines[li] if li is not None else None
    spk = ln is not None and (ln["who"] == c or ln["who"] == "all")
    if t < GD.get("intro", 2.9):
        beat = int(t / BEAT)
        if beat % 3 == {"pip": 0, "mb": 1, "dot": 2}[c] and (t % BEAT) < 0.17:
            hop = -16
        aL, aR = (-25, 25) if beat % 2 else (-10, 10)
        ang = [-3, 3][beat % 2]
    if spk:
        lvl = mouth_level(ln, t)
        wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
        if t - ln["words"][wi][0] < 0.09 and t >= ln["start"]:
            hop = -10 if c != "dot" else -4
        poses = {"mb": [(-20, 30), (-30, 150), (-15, 100), (-120, 120), (-60, 60), (-25, 135)],
                 "pip": [(-40, 40), (-150, 150), (-60, 25), (-100, 100), (-30, 60)],
                 "dot": [(-10, 10), (-12, 12), (-10, 70), (-10, 10)]}[c]
        aL, aR = poses[(wi * 7 + li) % len(poses)]
        ang = float(rng.uniform(-3.5, 3.5)) if c != "dot" else float(rng.uniform(-1, 1))
        jit *= 1.6
    else:
        ang = float(rng.uniform(-1, 1))
    # gaze
    scene = seg_at(t)[1]
    kids = G["L"].get(scene, {}).get("kids", {})
    gaze = "c"
    if ln is not None and not spk and ln["who"] in kids and c in kids:
        gaze = "l" if kids[ln["who"]] < kids[c] else "r"
    if ln is not None and ln["who"] == "grandma" and c != "pip":
        gaze = "l"
    say = ln and ln["words"] and " ".join(w[2] for w in ln["words"])
    # per-beat acting
    if scene == "outside":
        st = ev["stampede"]
        if t >= st + FLAT:   # flattened
            squash = 0.16
            if c == "pip" and li is not None and lines[li]["who"] == "pip" and t > st:
                p = (t - lines[li]["t0"]) / max(0.3, lines[li]["dur"])
                squash = [0.16, 0.3, 0.5, 0.75, 1.0][min(4, int(p * 5))]
                expr = "worried"
            else:
                peel = next((l_ for l_ in lines if l_["who"] == "pip" and l_["t0"] > st), None)
                if c == "pip" and peel is not None and t > peel["start"] + peel["dur"]:
                    squash = 1.0
            if c in ("dot", "mb") and spk:
                squash = [0.3, 0.38][fi % 2]   # talking from the floor, face readable
            if squash < 1:
                expr = "wide" if c == "pip" else "deadpan" if c == "dot" else "smug"
        elif st <= t < st + FLAT:
            expr, gaze = "wide", "r" if G["L"]["W"] > G["L"]["H"] else "u"
            if t > st + 0.5:
                aL, aR = -150, 150
        if li is not None and say and "dignity" in say and c == "mb" and t < st:
            expr = "smug"
    if scene == "inside":
        tv = ev.get("tv", -99.0)
        if t < tv + GD.get("tv", 0) + 0.5:
            expr, gaze = ("wide" if c != "dot" else "deadpan"), "r"
        sl = ev["slam"]
        if c == "pip" and t >= sl + 0.55:
            rot = -84
            expr = "wide" if not spk else "worried"
            aL, aR = (-160, 30) if spk else (-60, 60)
        if c != "pip" and sl + 0.55 <= t < sl + 1.4:
            expr, gaze = ("wide" if c == "mb" else "deadpan"), "l"
        if c == "mb" and spk and say and "payment" in say:
            expr = "smug"
        if c == "mb" and spk and say and "Seventy" in say:
            expr = "wide" if t < ln["words"][7][0] else "smug"
    if scene == "dawn":
        if c == "mb" and spk and say and "people" in say:
            expr, ang, aL, aR = "norm", 0, -40, 40
        if c == "mb" and spk and say and "stepped" in say:
            expr = "smug"
        cx_ = cart_x(t)
        gs = granny_cart_state(t)
        if gs[0] != "cart":
            cx_ = gs[1]
        if cx_ is not None and not spk:
            gaze = "l" if cx_ < kids[c] else "r"
            ang = (6 if cx_ < kids[c] else -6)
            expr = "wide" if c != "dot" else "deadpan"
        if t > ev["end"]:
            gaze = "c"
    if scene == "ceo" and not spk:
        gaze = "u"
        expr = {"mb": "smug", "pip": "worried", "dot": "deadpan"}[c]
    if c == "pip" and t >= ev["stampede"] + FLAT:
        extra["foot"] = True
    if scene == "dawn":
        if c == "pip" and not (spk and say and ("Same" in say)):
            aL = -125
            extra["sock"] = True
            if spk and say and "foot" in say:
                wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
                if wi >= 5:
                    extra["wig"] = [-16, 14, -10, 18][fi % 4]
                    expr = "wide"
        if c == "dot" and not spk:
            aL, aR = -10, 22
    # punchline poses: point and facepalm
    vert = G["L"]["H"] > G["L"]["W"]
    extra["fi"] = fi
    boot = next((l_ for l_ in lines if l_["who"] == "dot" and "boot" in " ".join(w[2] for w in l_["words"])), None)
    if c == "dot" and boot is not None and scene == "outside" and \
            boot["words"][min(5, len(boot["words"]) - 1)][0] <= t < ev["stampede"]:
        aR, extra["item"] = 130, ("boot", "R", -10)   # lifts the wet boot
        expr = "deadpan"
    if c == "pip" and boot is not None and scene == "outside" and boot["t0"] - 1.0 <= t < ev["stampede"]:
        expr = "worried"
    rib = next((l_ for l_ in lines if l_["who"] == "pip" and "ribbon" in " ".join(w[2] for w in l_["words"])), None)
    if c == "pip" and rib is not None and scene == "ceo" and rib["t0"] <= t < rib["start"] + rib["dur"] + 0.4:
        aL, extra["item"], expr = -140, ("ribbon", "L", 0), "norm"   # proud
    kid = next((l_ for l_ in lines if l_["who"] == "pip" and "console" in " ".join(w[2] for w in l_["words"])), None)
    if c == "pip" and kid is not None and kid["t0"] <= t < kid["start"] + kid["dur"] + 1.3:
        extra["bandaid"] = True
    if spk and c == "mb" and say and "kidney" in say:
        aL, aR = -95, 15   # points at Pip
    if spk and c == "mb" and say and "do it again" in say:
        expr = "smug"
    dad = [l_ for l_ in lines if l_["who"] == "mb" and ("dad left" in " ".join(w[2] for w in l_["words"]) or
                                                        "new family" in " ".join(w[2] for w in l_["words"]))]
    if c == "mb" and dad and dad[0]["t0"] <= t < ev.get("sadpluck", 0) + 0.9:
        expr, gaze, ang, hop, aL, aR = "smug", "c", 0.0, 0.0, -10, 10   # deadpan, dead still
        extra["still"] = True
    if c == "pip" and dad and dad[0]["t0"] <= t < ev.get("sadpluck", 0) + 0.9 and not spk:
        expr = "worried"
    if spk and c == "mb" and say and "loyalty" in say:   # deadpan to camera
        expr, gaze, ang, hop, aL, aR, jx_off = "smug", "c", 0.0, 0.0, -12, 12, True
        extra["still"] = True
    if spk and c == "mb" and scene == "inside" and say and "Seventy" in say:
        wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
        if wi <= 2:   # "There it is." points at the TV
            aL, aR = -15, (145 if vert else 95)
    if spk and c == "dot" and say and "dumbass" in say and t >= ln["words"][-1][0] - 0.05:
        aL, aR = -95, 12   # points at Meatball
    pay = next((l_ for l_ in lines if "payment" in " ".join(w[2] for w in l_["words"])), None)
    if c == "dot" and scene == "inside" and li is None and pay is not None and \
            pay["start"] + pay["dur"] < t < min(ev["checkout"], pay["start"] + pay["dur"] + 0.6):
        aR, extra["palm"] = 150, True   # "It's called a payment plan." -> facepalm
    if c == "mb" and scene == "ceo" and spk is False and ln is not None and ln["who"] == "ceo" and \
            len(ln["words"]) > 15 and t >= ln["words"][13][0]:
        aR, extra["palm"] = 150, True   # the CEO's "gift from my heart"
    if spk and c == "mb" and say and "piece" in say:
        aL, aR = -15, (140 if vert else 120)   # points up at the CEO on the screen
        expr = "wide" if "shit" in " ".join(w[2] for w in ln["words"] if w[0] <= t) and \
            "science" not in " ".join(w[2] for w in ln["words"] if w[0] <= t) else "smug"
    if spk and c == "pip" and say and "volcano" in say:
        aL, aR, expr = -150, 150, "wide"
    if spk and c == "mb" and say and "turd" in say:
        expr = "smug"
    if c == "pip" and scene == "ceo" and li is None and t > ev.get("ceo_in", 0) and any(
            "turd" in " ".join(w[2] for w in l_["words"]) and l_["start"] + l_["dur"] < t < l_["start"] + l_["dur"] + 1.6
            for l_ in lines):
        expr, aL, aR = "worried", -12, 12   # Pip after "a turd in a cup"
    if c == "dot" and spk and say and say.strip() == "Respect.":
        expr = "deadpan"
    if c == "dot" and spk and say and "dark" in say:
        expr = "wide"
    if spk and any(a <= t < b for a, b in ln.get("bwins", ())):
        ang, lvl = [-7, 7][fi % 2], 2
    blink = (int(t * FPS) + {"mb": 0, "pip": 17, "dot": 29}[c]) % 41 == 0
    if extra.get("still"):
        jit = 0.0
    return (hop, (float(rng.uniform(-jit, jit)), float(rng.uniform(-jit, jit))), ang, (aL, aR),
            (lvl, gaze, blink, expr), squash, rot, extra)


def compose_kid(c, z, pose):
    """The kid as one RGBA, feet at the centre (for squash / rotate)."""
    hop, (jx, jy), ang, (aL, aR), hk, squash, rot, extra = pose
    k = C.CAST[c]
    S = int(2 * 560 * z)
    im = Image.new("RGBA", (S, S))
    o = S / 2
    paste(im, C.sprite(c, "body", z), o, o)
    held = []
    for (sx, sy), a in zip(k["sh"], (aL, aR)):
        paste(im, C.sprite(c, "arm", z), o + sx * z, o + sy * z, a)
        it = extra.get("item")
        if it and ((it[1] == "L") == (sx < 0)):
            L_ = k["arm_len"] + 30
            hx = o + (sx + L_ * math.sin(math.radians(a))) * z
            hy = o + (sy + L_ * math.cos(math.radians(a))) * z
            held.append((it, hx, hy))
        if extra.get("sock") and a == aL and sx < 0:
            L_ = k["arm_len"] + 30
            hx = o + (sx + L_ * math.sin(math.radians(a))) * z
            hy = o + (sy + L_ * math.cos(math.radians(a))) * z
            paste(im, spr("sock", z), hx, hy - 40 * z, 10 + extra.get("wig", 0))
    paste(im, C.sprite(c, "head", z, *hk), o + (k["neck"][0] + jx) * z, o + (k["neck"][1] + jy) * z, ang)
    for it, hx, hy in held:   # held items go over the head (Dot's hood would hide them)
        paste(im, spr(it[0], z), hx, hy - 30 * z, it[2])
        if it[0] == "boot":   # it drips
            d_ = ImageDraw.Draw(im)
            for j in range(3):
                yy = hy + (20 + ((extra.get("fi", 0) * 9 + j * 23) % 70)) * z
                xx = hx + (-6 + j * 8) * z
                d_.ellipse((xx - 5 * z, yy - 7 * z, xx + 5 * z, yy + 5 * z), fill=(252, 226, 70))
    if extra.get("bandaid"):   # shirt lifted: skin and a paper band-aid where a kidney used to be
        sk = render_shapes([("p", [(-50, -150), (50, -150), (54, -100), (-54, -100)], C.SKIN_P),
                            ("p", [(-46, -138), (-2, -146), (2, -122), (-42, -114)], (236, 200, 150)),
                            ("e", (-22, -130, 7, 6), (210, 170, 120), False)], z, 200, 50)
        paste(im, sk, o, o)
    if extra.get("palm"):   # facepalm: the mitten over the eyes (the arm is up behind the head)
        hc = {"mb": 108, "pip": 92, "dot": 70}[c]
        paste(im, spr("palm", z, c), o + (k["neck"][0] + jx) * z, o + (k["neck"][1] + jy - hc) * z, 6)
    if extra.get("foot"):   # a stampede footprint stays on Pip's face
        paste(im, spr("foot", z), o + (k["neck"][0] + jx + 30) * z, o + (k["neck"][1] + jy - 120) * z, -25)
    return im


def draw_kid(fr, cam, c, x, y, pose):
    K = G["L"]["K"]
    z = round(cam.z * K, 3)
    hop, _, _, _, _, squash, rot, extra = pose
    px, py = cam.p(x, y + hop * K)
    im = compose_kid(c, z, pose)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC)
    if squash != 1.0:
        S = im.size[0]
        wide = 1 + (1 - squash) * 0.35
        im = im.resize((int(S * wide), max(2, int(S * squash))), Image.BICUBIC)
    paste(fr, im, px, py)


def draw_granny(fr, cam, x, y, lvl=0, expr="mean", aL=-15, aR=15, ang=0.0, hop=0.0, rot=0.0):
    K = G["L"]["K"]
    z = round(cam.z * K, 3)
    S = int(2 * 260 * z)
    im = Image.new("RGBA", (S, S))
    o = S / 2
    paste(im, spr("granny_body", z), o, o)
    for sx, a in ((-38, aL), (38, aR)):
        paste(im, spr("granny_arm", z), o + sx * z, o - 110 * z, a)
    blink = int(cam.z * 1000) % 1 == 1
    paste(im, spr("granny_head", z, lvl, blink, expr), o, o - 112 * z, ang)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC)
    px, py = cam.p(x, y + hop * K)
    paste(fr, im, px, py)


# ------------------------------------------------------------------------------------------------ frame
def bg(scene, cam_name):
    key = (scene, cam_name)
    if key not in G["bg"]:
        cx, cy, z = G["cams"][scene][cam_name]
        cam = C.Cam if False else None
        cam = Cam(G["L"], cx, cy, z)
        G["bg"][key] = (bg_outside(G["L"], cam) if scene == "outside" else bg_ceo(G["L"], cam) if scene == "ceo" else
                        bg_cup(G["L"], cam) if scene == "cup" else bg_pizza(G["L"], cam) if scene == "pizza" else
                        bg_dawn(G["L"], cam) if scene == "dawn" else bg_inside(G["L"], cam, scene))
    return G["bg"][key]


def shake(t):
    for name, dt in (("stampede", 0.25), ("stampede", FLAT), ("slam", 0.55), ("punch", 0.35), ("bump", 0.0),
                     ("bump", 0.5)):
        if name not in G["ev"]:
            continue
        d = t - (G["ev"][name] + dt)
        if 0 <= d < 2 / FPS:
            return (22, -14) if d < 1 / FPS else (-12, 8)
    return (0, 0)


def frame(fi):
    L, ev = G["L"], G["ev"]
    t = fi / FPS
    _, scene, cam_name = seg_at(t)
    cx, cy, z = G["cams"][scene][cam_name]
    sx_, sy_ = shake(t)
    cam = Cam(L, cx + sx_ / z, cy + sy_ / z, z)
    fr = bg(scene, cam_name).copy()
    if sx_ or sy_:   # shake: shift the cached background too
        fr2 = Image.new("RGBA", fr.size, (0, 0, 0, 255))
        fr2.paste(fr, (-sx_, -sy_))
        fr = fr2
    li = speaking(t)
    K = L["K"]
    F = L["feet"]
    if scene == "outside":
        draw_doors(fr, cam, t)
        S = L["outside"]
        for c in ("pip", "mb", "dot"):
            draw_kid(fr, cam, c, S["kids"][c], F, kid_pose(c, t, fi, li))
        draw_stampede(fr, cam, t)
    elif scene == "inside":
        S = L["inside"]
        tx, ty, ts = S["tv"]
        zz = round(z * ts, 3)
        tvx, tvy = cam.p(tx, ty)
        paste(fr, spr("tv", zz), tvx, tvy)
        screen_glow(fr, cam, tx - 254 * ts, ty - 324 * ts, tx + 254 * ts, ty - 56 * ts, t, ts)
        if "tv" in ev and t < ev["tv"] + GD["tv"]:   # choppy sparkles on the reveal
            for k in range(6):
                a = k * 60 + (fi % 3) * 20
                r = 260 * ts + (fi % 2) * 20
                qx, qy = cam.p(tx + r * math.cos(math.radians(a)), ty - 140 * ts + r * 0.7 * math.sin(math.radians(a)))
                ImageDraw.Draw(fr).regular_polygon((qx, qy, 14 * z), 4, rotation=45 * (fi % 2),
                                                   fill=(255, 250, 200), outline=INK)
        for c in ("mb", "dot", "pip"):
            pose = kid_pose(c, t, fi, li)
            x = S["kids"][c]
            draw_kid(fr, cam, c, x, F, pose)
        draw_granny_inside(fr, cam, t, li)
    elif scene == "ceo":
        draw_screen(fr, cam, t, li)
        S = L["ceo"]
        for c in ("pip", "mb", "dot"):
            draw_kid(fr, cam, c, S["kids"][c], F, kid_pose(c, t, fi, li))
    elif scene == "pizza":
        pass   # a cutaway: everything is in the background
    elif scene == "cup":
        if t >= G.get("judge_from", 1e9):
            S = L["cup"]
            jx = S["cup"][0] - (400 if L["W"] > L["H"] else 255)
            green_shake = (int(t * FPS) % 2) * 4
            paste(fr, spr("judge", round(z * (0.9 if L["W"] > L["H"] else 0.8), 3)),
                  *cam.p(jx + green_shake, S["table"]))
        draw_flies(fr, cam, t)
    elif scene == "checkout":
        S = L["checkout"]
        kx, ky = S["kiosk"]
        draw_kiosk(fr, cam, t, li)
        gx, gy = S["grandma"]
        bxp = cam.p(gx - 230 * K, gy)
        paste(fr, spr("box", round(z * K * 0.8, 3)), *bxp)
        draw_granny_checkout(fr, cam, t, li)
    else:
        S = L["dawn"]
        for c in ("pip", "mb", "dot"):
            pose = kid_pose(c, t, fi, li)
            draw_kid(fr, cam, c, S["kids"][c], F, pose)
            if c == "dot":
                draw_receipt(fr, cam, S["kids"]["dot"], F, pose)
        draw_cart(fr, cam, t, li)
        if ev["dawn"] <= t < ev["dawn"] + GD["dawn"]:
            draw_tag(fr, "6:12 AM", L["W"] / 2, L["H"] * (0.18 if L["W"] > L["H"] else 0.2), 0, 1.0)
    draw_banners(fr, t)
    draw_caption(fr, t, cam_name)
    return np.asarray(fr.convert("RGB")).tobytes()


def cart_x(t):
    """Grandma's golf cart crossing the lot, left to right, choppy (None when off-screen). With a speed bump
    (v7) it reaches the bump at ev["bump"] and rolls on off the right edge without her."""
    win = G.get("cart")
    if not win or not (win[0] <= t < win[1]):
        return None
    L = G["L"]
    W = L["W"]
    q = lambda f: int(f * 12) / 12   # noqa: E731  (choppy)
    bump = G["ev"].get("bump")
    if bump is None:
        return -500 + (W + 1000) * q((t - win[0]) / (win[1] - win[0]))
    xb = bump_x(L)
    if t < bump:
        return -500 + (xb + 500) * q((t - win[0]) / (bump - win[0]))
    return xb + (W + 600 - xb) * q(min(1.0, (t - bump) / 0.9))


def bump_x(L):
    return granny_lot(L)[0] - 260 * L["K"]


def granny_cart_state(t):
    """(where, x, y, rot) for Grandma at dawn: in the cart, flying, lying flat, or sat bolt upright."""
    ev = G["ev"]
    if "bump" not in ev:
        return ("cart", None, None, 0)
    L = G["L"]
    K = L["K"]
    b = ev["bump"]
    lx, ly = granny_lot(L)
    if t < b:
        return ("cart", None, None, 0)
    d = t - b
    if d < 0.5:   # launched: arc from the cart seat to the asphalt, tumbling
        f = int(d / 0.5 * 6) / 6
        sx, sy = bump_x(L) + 40 * K * 0.85, L["feet"] + 80 * K - 175 * K * 0.85
        x = sx + (lx - sx) * f
        y = sy + (ly - sy) * f - math.sin(f * math.pi) * 320 * K
        return ("fly", x, y, -360 * f)
    up = next((l_["t0"] for l_ in G["lines"] if l_["who"] == "grandma" and "warranty" in
               " ".join(w[2] for w in l_["words"])), b + 1.5)
    if t < up:
        return ("down", lx, ly, 90)   # lies still
    return ("up", lx, ly, 0)   # bolt upright


def draw_bump(fr, cam, t):
    win = G.get("cart")
    if not win or "bump" not in G["ev"] or not (win[0] <= t < G["ev"]["bump"] + 4.0):
        return
    L = G["L"]
    K = L["K"]
    x, y = bump_x(L), L["feet"] + 80 * K
    rng = np.random.default_rng(3)
    paper(fr, cam.pts(ell(x, y, 120 * K, 26 * K, 180, 360) + [(x + 120 * K, y)]), (252, 214, 74), rng, cam.z, sh=4)
    for k in range(-2, 3):
        paper(fr, cam.pts(strip([(x + k * 44 * K - 8 * K, y - 20 * K), (x + k * 44 * K + 8 * K, y - 4 * K)], 10 * K)),
              (40, 40, 46), rng, cam.z, shadow=False)


def draw_granny_lot(fr, cam, t, li):
    where, x, y, rot = granny_cart_state(t)
    if where == "cart":
        return
    ln = G["lines"][li] if li is not None else None
    lvl = mouth_level(ln, t) if ln is not None and ln["who"] == "grandma" else 0
    if where == "fly":
        draw_granny(fr, cam, x, y, 2, "mean", -160, 160, rot=rot)
    elif where == "down":
        draw_granny(fr, cam, x, y, 0, "mean", -20, 20, rot=rot)
    else:
        aR = 140 if ln is not None and ln["who"] == "grandma" else 30
        draw_granny(fr, cam, x, y, lvl, "mean", -20, aR, ang=[-2, 2][int(t * FPS) % 2])


def draw_cart(fr, cam, t, li):
    draw_bump(fr, cam, t)
    draw_granny_lot(fr, cam, t, li)
    x = cart_x(t)
    if x is None:
        return
    L = G["L"]
    K = L["K"]
    z = round(cam.z * K * 0.85, 3)
    y = L["feet"] + 80 * K
    rng = np.random.default_rng(int(t * FPS))
    for k in range(3):   # speed lines
        yy = y - (120 + 60 * k) * K
        paper(fr, cam.pts(strip([(x - 330 * K, yy), (x - (520 + 60 * k) * K, yy)], 7)), (250, 250, 240), rng, cam.z,
              shadow=False, jitter=False, edge=False)
    px, py = cam.p(x, y)
    paste(fr, spr("cart_back", z), px, py)
    ln = G["lines"][li] if li is not None else None
    lvl = mouth_level(ln, t) if ln is not None and ln["who"] == "grandma" else 0
    if granny_cart_state(t)[0] == "cart":
        draw_granny(fr, cam, x + 40 * K * 0.85, y - 175 * K * 0.85, lvl, "mean", -20,
                    [150, 170][int(t * FPS) % 2], ang=[-4, 4][int(t * FPS) % 2])
    paste(fr, spr("cart_front", z), px, py)


def draw_receipt(fr, cam, x, F, pose):
    """Dot's receipt: from her hand to the floor and way along it (longer than she is)."""
    K = G["L"]["K"]
    hop, (jx, jy), _, (aL, aR), _, _, _, _ = pose
    k = C.CAST["dot"]
    sx, sy = k["sh"][1]
    L_ = k["arm_len"] + 14
    hx = x + (sx + L_ * math.sin(math.radians(aR))) * K
    hy = F + (sy + L_ * math.cos(math.radians(aR)) + hop) * K
    dirx = -1 if G["L"]["W"] < G["L"]["H"] else 1
    pts = [(hx, hy), (hx + 6 * K, F - 30 * K), (hx + 30 * K, F + 10 * K)]
    for i in range(1, 7):
        pts.append((hx + 30 * K + dirx * i * 60 * K, F + 14 * K + 4 * math.sin(i)))
    pts.append((pts[-1][0] + dirx * 20 * K, pts[-1][1] - 26 * K))
    rng = np.random.default_rng(77)
    paper(fr, cam.pts(strip(pts, 34 * K)), (252, 250, 244), rng, cam.z, sh=3)
    d = ImageDraw.Draw(fr)
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        for f in (0.3, 0.7):
            px, py = ax + (bx - ax) * f, ay + (by - ay) * f
            q = cam.p(px, py)
            d.line([(q[0] - 9 * cam.z * K, q[1]), (q[0] + 9 * cam.z * K, q[1])], fill=(150, 150, 150),
                   width=max(1, int(3 * cam.z)))
    q = cam.p(hx - 2 * K, hy)
    d.ellipse((q[0] - 13 * cam.z * K, q[1] - 13 * cam.z * K, q[0] + 13 * cam.z * K, q[1] + 13 * cam.z * K),
              fill=(139, 92, 62))


def draw_doors(fr, cam, t):
    S = G["L"]["outside"]
    dx, dw = S["doors"]
    g = S["ground"]
    st = G["ev"]["stampede"]
    d = t - st
    open_ = 0 if d < 0.25 else min(1.0, [0.5, 0.9, 1.0][min(2, int((d - 0.25) * FPS))])
    rng = np.random.default_rng(5)
    for side in (-1, 1):
        x_in = dx + side * open_ * dw * 0.48
        pts = [(x_in, g - 340), (x_in + side * dw / 2, g - 340), (x_in + side * dw / 2, g), (x_in, g)]
        pts = [(min(max(x, dx - dw / 2 - 10), dx + dw / 2 + 10), y) for x, y in pts]
        if abs(pts[0][0] - pts[1][0]) > 4:
            paper(fr, cam.pts(pts), (170, 214, 236), rng, cam.z, sh=3)


def draw_stampede(fr, cam, t):
    S = G["L"]["outside"]
    st = G["ev"]["stampede"]
    d = t - st
    sd = GD.get("stampede", 2.8)
    if d < 0.2 or d > min(2.8, sd + 0.5 if sd >= 2.5 else sd):
        return
    fct = min(1.0, max(0.45, (sd - 0.3) / 2.5))   # a short stampede runs the same crowd faster
    dx, dw = S["doors"]
    g = S["ground"]
    W, H, K = G["L"]["W"], G["L"]["H"], G["L"]["K"]
    F = G["L"]["feet"]
    items = []
    for k in range(16):
        t0 = 0.28 * fct + k * 0.08 * fct
        p = (d - t0) / (1.3 * max(0.6, fct))
        if p < 0 or p > 1:
            continue
        p = int(p * 12) / 12   # choppy
        tx = (k * 0.37 % 1.0) * W * 1.2 - W * 0.1
        x = dx + (tx - dx) * p + math.sin(k * 7 + d * 10) * 6
        y = g + (F + 380 * K - g) * p
        sc = (0.45 + 0.95 * p) * K
        items.append((y, x, sc, k, p))
    for y, x, sc, k, p in sorted(items):
        z = round(cam.z * sc, 2)
        hop = -18 if int((t * FPS) + k) % 2 else 0
        px, py = cam.p(x, y + hop)
        paste(fr, spr("shopper", z, k % 6), px, py)
    if 0.8 < d < 2.4:   # dust puffs
        rng = np.random.default_rng(int(t * FPS))
        for k in range(5):
            x = rng.uniform(0, W)
            y = F - rng.uniform(0, 60)
            paper(fr, cam.pts(lumpy(x, y, 40, [(6, 5, k)])), (230, 226, 216), rng, cam.z, sh=3)


def granny_lot(L):
    """Where Grandma lands after the speed bump (world x, ground y): in front of the kids, right of centre."""
    return (L["W"] * 0.66 if L["W"] > L["H"] else L["W"] * 0.62), L["feet"] + 120 * L["K"]


def granny_on(L):
    """Where Grandma stands on Pip after the slam (units from his feet): on his chest in 16:9; on his shins in
    vertical, where the kids stand close and she would otherwise cover Meatball's close-ups."""
    return 210 if L["W"] > L["H"] else 40


def granny_flight(t):
    """Grandma's position during the slam: off-screen left -> arc -> onto Pip."""
    S = G["L"]["inside"]
    K = G["L"]["K"]
    gx, gy = S["grandma_land"]
    sl = G["ev"]["slam"]
    d = t - sl
    if d < 0:
        return None
    if d < 0.55:
        p = int(d / 0.55 * 7) / 7
        x = -200 + (gx + granny_on(G["L"]) * K + 200) * p
        y = gy - 400 * K - math.sin(p * math.pi) * 260 * K + 200 * K * p
        return x, y, 360 * p * 2
    return gx + granny_on(G["L"]) * K, gy - 58 * K, 0


def draw_granny_inside(fr, cam, t, li):
    g = granny_flight(t)
    if g is None:
        return
    x, y, rot = g
    ln = G["lines"][li] if li is not None else None
    lvl = mouth_level(ln, t) if ln is not None and ln["who"] == "grandma" else 0
    sl = G["ev"]["slam"]
    aL, aR = (-160, 160) if t < sl + 0.55 else (-40, 40)
    if ln is not None and ln["who"] == "grandma":
        wi = max([j for j, (s, _, _) in enumerate(ln["words"]) if s <= t + 0.01] or [0])
        aL, aR = [(-40, 40), (-30, 150), (-150, 30), (-90, 90)][wi % 4]
    ang = [-7, 7][int(t * FPS) % 2] if ln is not None and ln["who"] == "grandma" and any(
        a <= t < b for a, b in ln.get("bwins", ())) else 0.0
    draw_granny(fr, cam, x, y, lvl, "mean", aL, aR, ang=ang, rot=rot)
    if sl + 0.55 <= t < sl + 1.2:
        K = G["L"]["K"]
        px, py = cam.p(x + 60 * K, y - 20 * K)
        paste(fr, spr("star", round(cam.z * K * (1.3 if int(t * FPS) % 2 else 1.15), 2), "SLAM!"), px, py,
              (int(t * FPS) % 2) * 8)


def draw_kiosk(fr, cam, t, li):
    S = G["L"]["checkout"]
    K = G["L"]["K"]
    kx, ky = S["kiosk"]
    z = round(cam.z * K, 3)
    paste(fr, spr("kiosk", z), *cam.p(kx, ky))
    pu = G["ev"]["punch"]
    broken = t >= pu + 0.35
    x0, y0, x1, y1 = kx - 128 * K, ky - 568 * K, kx + 128 * K, ky - 372 * K
    rng = np.random.default_rng(1)
    ln = G["lines"][li] if li is not None else None
    talking = ln is not None and ln["who"] == "kiosk"
    fi = int(t * FPS)
    red = (not broken) or (talking and fi % 3 != 0)
    paper(fr, cam.pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), (214, 44, 36) if red else (40, 40, 48), rng,
          cam.z, shadow=False, jitter=False, edge=False)
    d = ImageDraw.Draw(fr)
    lvl = mouth_level(ln, t) if talking else 0
    zz = cam.z * K
    if red:   # face: two eyes and an equalizer mouth (crooked once it is broken)
        for side in (-1, 1):
            tilt = (side * 10 if broken else 0)
            ex, ey = cam.p(kx + side * 50 * K, ky - (510 + tilt) * K)
            s_ = 16 * zz
            d.rectangle((ex - s_, ey - s_ * 0.6, ex + s_, ey + s_ * 0.6), fill=WHITE)
        for b in range(7):
            h = (6 + (lvl * 14) * (0.4 + 0.6 * abs(math.sin(b * 1.7 + t * 30)))) if lvl else 4
            bx, by = cam.p(kx + (b - 3) * 22 * K + (fi % 2) * 6 * broken, ky - 440 * K)
            d.rectangle((bx - 7 * zz, by - h * zz, bx + 7 * zz, by + h * zz), fill=WHITE)
    if broken:
        cxp, cyp = cam.p(kx + 20 * K, ky - 470 * K)
        for a in range(0, 360, 50):
            pts = [(cxp, cyp)]
            for r in (40, 90, 150):
                aa = math.radians(a + r * 0.2)
                pts.append((cxp + r * zz * math.cos(aa), cyp + r * zz * 0.6 * math.sin(aa)))
            d.line(pts, fill=(230, 230, 240), width=max(2, int(4 * cam.z)))
        sr = np.random.default_rng(fi)
        for k in range(6 if fi % 2 == 0 else 3):   # sparks
            a = sr.uniform(0, 2 * math.pi)
            pts = [(cxp, cyp)]
            r = 0
            for _ in range(4):
                r += sr.uniform(30, 60)
                pts.append((cxp + r * zz * math.cos(a) + sr.uniform(-12, 12) * zz,
                            cyp + r * zz * math.sin(a) + sr.uniform(-12, 12) * zz))
            d.line(pts, fill=(255, 220, 60), width=max(2, int(5 * cam.z)))
            d.ellipse((pts[-1][0] - 6 * zz, pts[-1][1] - 6 * zz, pts[-1][0] + 6 * zz, pts[-1][1] + 6 * zz),
                      fill=(255, 250, 200))
        if talking and "yacht" in " ".join(w[2] for w in ln["words"]):   # a little paper yacht on the cracked screen
            yx, yy = kx + 70 * K, ky - 500 * K
            yr = np.random.default_rng(9)
            paper(fr, cam.pts([(yx - 46 * K, yy), (yx + 46 * K, yy), (yx + 30 * K, yy + 20 * K),
                               (yx - 30 * K, yy + 20 * K)]), WHITE, yr, cam.z, sh=2)
            paper(fr, cam.pts([(yx - 4 * K, yy - 4 * K), (yx - 4 * K, yy - 60 * K), (yx + 34 * K, yy - 4 * K)]),
                  (252, 214, 74), yr, cam.z, sh=2)
            d.text(cam.p(kx - 40 * K, ky - 520 * K), "x3", font=ImageFont.truetype(FONT, int(26 * zz)),
                   fill=(255, 230, 120), anchor="mm")
            txt = "ROUND UP?" if fi % 4 < 3 else "R0UND UP?"
        else:
            txt = ("PLEASE WAIT" if fi % 4 < 3 else "PL3A5E W@IT") if talking else "ERROR"
        d.text(cam.p(kx + (fi % 2) * 4, ky - 395 * K), txt, font=ImageFont.truetype(FONT, int(24 * zz)),
               fill=(255, 230, 230), anchor="mm")
        return
    if talking or (G["ev"]["checkout"] + 0.4 < t < pu):
        d.text(cam.p(kx, ky - 395 * K), "UNEXPECTED ITEM", font=ImageFont.truetype(FONT, int(19 * zz)),
               fill=WHITE, anchor="mm")


def draw_granny_checkout(fr, cam, t, li):
    S = G["L"]["checkout"]
    K = G["L"]["K"]
    gx, gy = S["grandma"]
    ln = G["lines"][li] if li is not None else None
    lvl = mouth_level(ln, t) if ln is not None and ln["who"] == "grandma" else 0
    pu = G["ev"]["punch"]
    aL, aR, x, hop = -20, 20, gx, 0.0
    if ln is not None and ln["who"] == "grandma":
        aR = 120 if "fist" in ln["words"][-1][2] and t > ln["words"][-1][0] else 60
    d = t - pu
    if 0 <= d < 1.0:   # wind-up, lunge, punch
        kx = S["kiosk"][0]
        if d < 0.2:
            aR, x = 30, gx - 30 * K
        elif d < 0.35:
            aR, x, hop = 120, gx + (kx - gx) * 0.5, -200
        elif d < 0.8:
            aR, x, hop = 100, kx - 190 * K, -360
        else:
            aR, x, hop = 40, kx - 230 * K, -120
    ang = [-7, 7][int(t * FPS) % 2] if ln is not None and ln["who"] == "grandma" and any(
        a <= t < b for a, b in ln.get("bwins", ())) else 0.0
    draw_granny(fr, cam, x, gy, lvl, "mean", aL, aR, ang=ang, hop=hop)
    if 0.35 <= d < 1.0:
        kx, ky = S["kiosk"]
        px, py = cam.p(kx - 70 * K, ky - 470 * K)
        paste(fr, spr("star", round(cam.z * K * (1.25 if int(t * FPS) % 2 else 1.1), 2), "POW!"), px, py,
              (int(t * FPS) % 2) * -8)


# ------------------------------------------------------------------------------------------------ text
@lru_cache(maxsize=128)
def tag_img(text, size, seed):
    return C.tag(text, size, seed)


def draw_tag(fr, text, x, y, seed, scale):
    img = tag_img(text, G["L"]["cap_size"], seed)
    W = G["L"]["W"]
    s = scale
    if img.size[0] * s > W - 30:
        s = (W - 30) / img.size[0]
    if s != 1.0:
        img = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.BICUBIC)
    paste(fr, img, x, y)


def chunks_of(ln):
    out, cur = [], []
    for wd in ln["words"]:
        cur.append(wd)
        if len(cur) == 3 or wd[2][-1] in ".?!," or (len(cur) == 2 and len(" ".join(x[2] for x in cur)) > 12):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def draw_caption(fr, t, cam_name):
    li = speaking(t + 0.04)
    if li is None:
        return
    ln = G["lines"][li]
    show = None
    for ch in chunks_of(ln):
        if ch[0][0] - 0.04 <= t:
            show = ch
    if show is None:
        return
    text = " ".join(w[2] for w in show).upper().replace("...", "…").rstrip(".,")
    if text.startswith("…") and len(text) > 1:
        text = "…" + text[1:]
    k = int((t - (show[0][0] - 0.04)) * FPS)
    scale = [1.22, 0.94, 1.0][min(2, k)]   # pop
    L = G["L"]
    y = L["cap_y"]
    if cam_name in ("cu_tv", "cu_kiosk"):
        y = L["H"] * (0.86 if L["W"] > L["H"] else 0.8)
    draw_tag(fr, text, L["W"] / 2, y, hash(text) & 0xfff, scale)


def draw_banners(fr, t):
    L = G["L"]
    W = L["W"]
    big = 120 if L["W"] > L["H"] else 104
    by = L["banner_y"]

    def drop(t0):
        k = int((t - t0) * FPS)
        return [-700, -320, 40, -12, 0][k] if k < 5 else 0

    end = G["ev"]["end"]
    it_ = GD.get("intro", 2.9)
    items = [(0.1, it_ - 0.05, "MEATBALL MYTHS", big, (200, 40, 32), WHITE, -3, 0),
             (min(0.85, it_ * 0.3), it_ - 0.05, "BLACK FRIDAY", int(big * 0.7), (20, 20, 24), (252, 214, 74), 2,
              int(big * 1.25))]
    eb = int(big * 0.52)
    for i, txt in enumerate(END_TEXT):
        items.append((end + 0.2 + 0.25 * i, end + 99, txt, eb, (252, 250, 240), INK, [-2, 2, -1][i],
                      int(i * eb * 1.55) - (0 if L["W"] > L["H"] else -40)))
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
    if t >= end + 1.0:   # a paper arrow pointing down at the comments
        ay = by + 3 * eb * 1.55 + (40 if L["H"] > L["W"] else 10) + (8 if int(t * FPS) % 4 < 2 else 0)
        rng = np.random.default_rng(3)
        cam = Cam(L, *G["cams"]["dawn"]["wide"])
        kd = L["dawn"]["kids"]
        x = cam.p((kd["mb"] + kd["dot"]) / 2, 0)[0]
        paper(fr, [(x - 30, ay), (x + 30, ay), (x + 30, ay + 60), (x + 70, ay + 60), (x, ay + 130),
                   (x - 70, ay + 60), (x - 30, ay + 60)], (252, 214, 74), rng, 1.5, sh=6)
        del cam


# ------------------------------------------------------------------------------------------------ audio
def tone(f, dur, g=1.0):
    tt = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, np.minimum(tt / 0.005, (dur - tt) / 0.01))
    return (np.sin(2 * np.pi * f * tt) * env * g).astype(np.float32)


def choir(dur, notes=("C3", "G3", "C4", "E4", "G4", "C5")):
    """Additive 'aah' choir: harmonics shaped by vowel formants, a few detuned voices, vibrato, swell."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    out = np.zeros(n)
    form = [(730, 90, 1.0), (1090, 110, 0.5), (2440, 160, 0.25)]
    for ni, nt in enumerate(notes):
        f0 = hz(nt)
        for v in range(3):
            det = 1 + (v - 1) * 0.004
            vib = 1 + 0.006 * np.sin(2 * np.pi * (5.2 + v * 0.3) * tt + v)
            ph = 2 * np.pi * np.cumsum(f0 * det * vib) / SR
            for k in range(1, int(5000 / f0)):
                fk = k * f0
                a = sum(g * math.exp(-((fk - fc) / bw) ** 2 / 2) for fc, bw, g in form) + 0.02 / k
                out += a * np.sin(k * ph)
    env = np.minimum(1, tt / 0.35) * np.minimum(1, (dur - tt) / 0.6)
    out *= env
    return (out / np.max(np.abs(out))).astype(np.float32)


def noise_burst(dur, decay, seed=0, smooth=1):
    n = int(dur * SR)
    x = np.random.default_rng(seed).normal(0, 1, n)
    if smooth > 1:
        x = np.convolve(x, np.ones(smooth) / smooth, "same")
    return (x * np.exp(-np.arange(n) / (decay * SR))).astype(np.float32)


def thud(buf, t, g):
    kick(buf, t, g)
    add(buf, noise_burst(0.2, 0.04, int(t * 100), 4), t, g * 0.5)


def mix(end):
    ev, lines = G["ev"], G["lines"]
    music = np.zeros(int((end + 1) * SR), np.float32)
    mel1 = [(0, "E5", 1), (1, "G5", 0.5), (1.5, "A5", 0.5), (2, "G5", 1), (3, "E5", 0.5), (3.5, "C#5", 0.5)]
    mel2 = [(0, "D5", 0.5), (0.5, "F#5", 0.5), (1, "A5", 1), (2, "B5", 0.5), (2.5, "A5", 0.5), (3, "G5", 1)]
    short = GD.get("intro", 2.9) < 2.5   # v8: a one-bar jingle and the bed under everything
    jingle_bar(music, 0.0, ["C", "A7"], 0.32, mel1, seed=1)
    if short:
        stab = 4 * BEAT
    else:
        jingle_bar(music, 4 * BEAT, ["D7", "G7"], 0.32, mel2, seed=2)
        stab = 8 * BEAT
    strum(music, stab, "C", 0.4, seed=3)
    add(music, ks(hz("C6"), 1.0, 0.996, 0.85, 4), stab, 0.35)
    for t0 in (0.1, min(0.85, GD.get("intro", 2.9) * 0.3)):
        sfx_slap(music, t0 + 2 / FPS, 0.25, int(t0 * 10))
    # bed (-22 dB) everywhere except the gags that carry their own sound
    bed = np.zeros_like(music)
    prog = [["C"], ["A7"], ["D7"], ["G7"]]
    t, k = stab + BEAT, 0
    while t < ev["end"]:
        jingle_bar(bed, t, prog[k % 4], 0.32, None, drums=True, seed=10 + k)
        t += 4 * BEAT
        k += 1
    gate = np.ones_like(bed)
    gate[:int((stab + BEAT) * SR)] = 0
    for name, d0, d1 in (("sadpluck", -0.2, 1.0), ("stampede", 0, 3.6), ("tv", 0, GD.get("tv", 0)), ("punch", 0, 1.0),
                         ("dawn", 0, GD.get("dawn", 1.2) - 0.2)):
        if name in ev and not short:
            gate[int((ev[name] + d0) * SR):int((ev[name] + d1) * SR)] = 0
    gate[int(ev["end"] * SR):] = 0
    gate = np.convolve(gate, np.ones(4410) / 4410, "same").astype(np.float32)
    music += bed * gate * 10 ** (-22 / 20) * 1.6
    fx = np.zeros_like(music)
    # stampede: door bang, rumble of feet, crowd roar
    st = ev["stampede"]
    thud(fx, st + 0.25, 0.9)
    add(fx, noise_burst(0.5, 0.12, 9, 2), st + 0.27, 0.35)
    rng = np.random.default_rng(4)
    sd = min(2.3, GD.get("stampede", 2.8) + 0.4)
    for k in range(int(60 * sd / 2.3)):
        kick(fx, st + 0.4 + rng.uniform(0, sd - 0.2), 0.25)
    n = int(sd * SR)
    roar = np.convolve(np.random.default_rng(5).normal(0, 1, n), np.ones(30) / 30, "same")
    roar -= np.convolve(roar, np.ones(200) / 200, "same")
    am = 0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * np.arange(n) / SR) * np.sin(2 * np.pi * 0.7 * np.arange(n) / SR)
    env = np.minimum(1, np.arange(n) / (0.3 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.6 * SR))
    add(fx, (roar * am * env * 2.2).astype(np.float32), st + 0.35, 0.5)
    thud(fx, st + FLAT, 0.8)   # flattened
    sfx_slap(fx, st + FLAT + 0.02, 0.5, 7)
    # peel off the floor: a tape rip
    pl = next((l_ for l_ in lines if l_["who"] == "pip" and l_["t0"] > st), None)
    if pl is not None:
        add(fx, noise_burst(0.4, 0.15, 11, 1), max(st + FLAT + 0.1, pl["t0"] - 0.5), 0.12)
    if "tv" in ev:
        add(fx, choir(GD["tv"] + 0.2), ev["tv"] + 0.05, 0.42)
    # grandma slam: whistle-in, impact
    sl = ev["slam"]
    tt = np.arange(int(0.55 * SR)) / SR
    add(fx, (np.sin(2 * np.pi * np.cumsum(1400 - 900 * tt / 0.55) / SR) * 0.3).astype(np.float32), sl, 0.4)
    thud(fx, sl + 0.55, 1.0)
    sfx_slap(fx, sl + 0.56, 0.6, 3)
    add(fx, ks(hz("A6"), 0.6, 0.99, 0.9, 6), sl + 0.62, 0.3)
    # bleep on line 8
    for ln in lines:
        if ln["bleep"]:
            add(fx, tone(1000, ln["bleep"] - 0.06, 0.32), ln["t0"])
        if ln["beep"]:
            add(fx, tone(1560, 0.16, 0.3), ln["t0"] + 0.05)
        for a, b in ln.get("bwins", ()):
            add(fx, tone(1000, b - a - 0.03, 0.34), a + 0.015)
    if not short:
        add(fx, tone(1560, 0.12, 0.25), ev["checkout"] + 0.6)
    pu = ev["punch"]
    thud(fx, pu + 0.35, 1.0)
    add(fx, noise_burst(0.6, 0.15, 13, 1), pu + 0.36, 0.3)
    tt = np.arange(int(0.35 * SR)) / SR
    add(fx, (np.sign(np.sin(2 * np.pi * np.cumsum(600 - 500 * tt / 0.35) / SR)) * 0.06 *
             np.exp(-tt / 0.15)).astype(np.float32), pu + 0.45, 1.0)   # power-down
    if "bump" in ev:   # speed bump: clunk, a whistle up, a thud down
        thud(fx, ev["bump"], 0.8)
        tt = np.arange(int(0.45 * SR)) / SR
        add(fx, (np.sin(2 * np.pi * np.cumsum(600 + 900 * tt / 0.45) / SR) * 0.25).astype(np.float32),
            ev["bump"] + 0.03, 0.4)
        thud(fx, ev["bump"] + 0.5, 1.0)
        sfx_slap(fx, ev["bump"] + 0.52, 0.5, 9)
    # dawn: a bird
    for k in range(3):
        tt = np.arange(int(0.09 * SR)) / SR
        add(fx, (np.sin(2 * np.pi * np.cumsum(3800 - 1500 * tt / 0.09) / SR) * np.sin(np.pi * tt / 0.09) *
                 0.2).astype(np.float32), ev["dawn"] + 0.3 + k * 0.14)
    if "sadpluck" in ev:
        for k2, nt in enumerate(["G4", "F#4", "F4", "E4"]):
            add(music, ks(hz(nt), 1.0 if k2 == 3 else 0.5, 0.996, 0.7, 70 + k2), ev["sadpluck"] + 0.05 + k2 * 0.22,
                0.42 if k2 < 3 else 0.5)
    # end sting
    o = ev["end"] + 0.1
    strum(music, o, "G7", 0.35, seed=40)
    for k2, nt in enumerate(["B5", "D6", "G5", "E5"]):
        add(music, ks(hz(nt), 0.6, 0.995, 0.85, 50 + k2), o + 0.18 + k2 * BEAT / 2, 0.32)
    strum(music, o + 2.5 * BEAT, "C", 0.45, seed=60)
    add(music, ks(hz("C6"), 1.2, 0.996, 0.85, 62), o + 2.5 * BEAT, 0.35)
    kick(music, o + 2.5 * BEAT, 0.3)
    for i in range(4):
        sfx_slap(music, ev["end"] + 0.1 + 0.25 * i + 2 / FPS, 0.2, 20 + i)
    vo = np.zeros_like(music)
    for ln in lines:
        add(vo, ln["audio"], ln["start"], 1.0)
    out = vo + music + fx * 0.8
    out *= 0.97 / max(1e-6, float(np.max(np.abs(out))))
    return out[:int(end * SR)]


# ------------------------------------------------------------------------------------------------ main
def setup(fmt):
    L = layout(fmt)
    lines, segs, ev, end = build()
    G.update(L=L, lines=lines, segs=segs, ev=ev, end=end, cams=cams(L), bg={})
    merry = [l_ for l_ in lines if l_["who"] == "ceo" and any(w[2].startswith("Merry") for w in l_["words"])]
    G["wink_until"] = merry[0]["start"] + merry[0]["dur"] + 0.6 if merry else 0
    G["wink_from"] = merry[0]["start"] + merry[0]["dur"] if merry else 0
    hl = [l_ for l_ in lines if l_["who"] == "ceo" and "affordable" in " ".join(w[2] for w in l_["words"])]
    G["hands_from"] = next((w[0] for w in hl[0]["words"] if w[2].startswith("Small")), 1e9) - 0.05 if hl else 1e9
    G["hands_until"] = hl[0]["start"] + hl[0]["dur"] + 0.5 if hl else 0
    jl = [l_ for l_ in lines if "judge" in " ".join(w[2] for w in l_["words"])]
    G["judge_from"] = next((w[0] for w in jl[0]["words"] if w[2] == "The"), jl[0]["start"]) - 0.05 if jl else 1e9
    cl = [l_ for l_ in lines if l_["who"] == "grandma" and "children" in " ".join(w[2] for w in l_["words"])]
    G["cart"] = ((ev["cart"], ev["bump"] + 1.0) if "bump" in ev else
                 (ev["cart"], cl[0]["start"] + cl[0]["dur"] + 0.8)) if cl and "cart" in ev else None
    for (_, scene, cam) in segs:   # build backgrounds before forking
        bg(scene, cam)


def render(fmt, out):
    os.makedirs(TMP, exist_ok=True)
    setup(fmt)
    L, end = G["L"], G["end"]
    wav = f"{TMP}/bf-mix-{fmt}.wav"
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
        p = f"{TMP}/bf-{fmt}-{t:.2f}.png"
        Image.frombytes("RGB", (W, H), frame(int(t * FPS))).save(p)
        outs.append(p)
    print(" ".join(outs))


def timeline(fmt="wide"):
    setup(fmt)
    for k, v in G["ev"].items():
        print(f"{k:10s} {v:6.2f}")
    for i, ln in enumerate(G["lines"]):
        print(f"L{i + 1:<2d} {ln['who']:8s} {ln['t0']:6.2f} {ln['start']:6.2f} {ln['dur']:5.2f}")
    print("end", round(G["end"], 2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fmt", default="vertical", choices=["vertical", "wide"])
    ap.add_argument("--out")
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--sheet")
    ap.add_argument("--times", type=float, nargs="*")
    ap.add_argument("--timeline", action="store_true")
    ap.add_argument("--script", default="v8", choices=["v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"])
    a = ap.parse_args()
    use_script(a.script)
    if a.timeline:
        timeline(a.fmt)
    elif a.sheet:
        C.sheet(a.sheet, a.times)
    elif a.still:
        stills(a.fmt, a.still)
    else:
        render(a.fmt, a.out)
