#!/usr/bin/env python3
"""Driving bed for the doubling Short, from the channel's own generator (tools/music.py, CC0, made from oscillators).
Peak-stacking: a hit on every caption beat, then on EVERY doubling in the last 10 s, with the level climbing into
the final beat; it settles under the question card. Usage: music_bed.py OUT.wav"""
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.environ.get("MB_TOOLS", "/home/user/skills/skills/oh-meatball/tools"))
import music  # noqa: E402

TOTAL, CARD = 59.5, 54.4
BEATS = [3.2, 6.6, 10.0, 13.2, 16.6, 20.0, 23.2, 26.4, 30.4, 34.4, 38.4, 42.4, 46.4, 50.4]
REVEALS = sorted(set(BEATS + [44.4, 48.4, 52.4, CARD]))

st = music.render("cold-war", TOTAL, REVEALS, drop=False, hit=True)
t = np.arange(len(st)) / music.SR
gain = 0.62 + 0.38 * np.clip((t - 8) / (CARD - 8), 0, 1) ** 1.6          # climbs all the way to the last beat
gain = np.where(t > CARD, 1.0 - 0.4 * np.clip((t - CARD) / 2.5, 0, 1), gain)  # settles under the card
gain *= np.clip(t / 0.4, 0, 1)
st = st * gain[:, None]
st *= 0.89 / (np.abs(st).max() + 1e-9)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(music.SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
print("ok", sys.argv[1], len(st) / music.SR)
