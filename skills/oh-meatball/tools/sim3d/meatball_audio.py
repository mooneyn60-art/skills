#!/usr/bin/env python3
"""Voices + timeline + mixed audio for the 3D Meatball dialogue test.
Writes work/mb/timeline.json (line starts, word timings, 30 fps mouth envelopes) and work/mb/mix.wav.
Run from skills/oh-meatball/tools' parent so `facts` and `music` import (path added below)."""
import asyncio
import json
import os
import subprocess
import sys

import numpy as np

TOOLS = os.environ.get("MB_TOOLS", "/home/user/skills/skills/oh-meatball/tools")
sys.path.insert(0, TOOLS)
import facts  # noqa: E402  (sets the proxy CA SSL context for edge-tts)
import music  # noqa: E402

OUT = "/dev/shm/sim3d/work/mb"
FPS = 30
GAP = 0.45
TAIL = 2.4
LINES = [
    ("human", "Meatball, there's a bug with 30 legs in my bathroom. Do I squish it?", "en-US-BrianNeural", "+6%", "+0Hz"),
    ("meatball", "Don't! It's eating your roaches.", "en-US-AndrewMultilingualNeural", "+10%", "+3Hz"),
    ("human", "...How many roaches?", "en-US-BrianNeural", "+0%", "+0Hz"),
    ("meatball", ["Oh.", "You don't want to know."], "en-US-AndrewMultilingualNeural", "+10%", "+3Hz"),
]


def pcm(path, sr):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(np.float32) / 32768


def trim_silence(x, sr, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    if not len(idx):
        return x, 0.0
    a = max(0, idx[0] - int(0.02 * sr))
    return x[a:idx[-1] + int(0.08 * sr)], a / sr


async def main():
    os.makedirs(OUT, exist_ok=True)
    sr = music.SR
    t, lines, voice = 0.0, [], []
    for i, (who, text, v, rate, pitch) in enumerate(LINES):
        parts = text if isinstance(text, list) else [text]
        x, words = np.zeros(0, np.float32), []
        for j, part in enumerate(parts):   # a list = separate takes joined by a short beat (deadpan timing)
            mp3 = f"{OUT}/line{i}_{j}.mp3"
            ws = await facts.speak(part, v, mp3, rate=rate, pitch=pitch)
            y, lead = trim_silence(pcm(mp3, sr), sr)
            off = len(x) / sr
            words += [(a - lead + off, b - lead + off, w) for a, b, w in ws]
            x = np.concatenate([x, y, np.zeros(int(0.32 * sr) if j < len(parts) - 1 else 0, np.float32)])
        text = " ".join(parts)
        lead = 0.0
        dur = len(x) / sr
        n = int(dur * FPS) + 1
        hop = sr // FPS
        e = np.array([np.sqrt(np.mean(x[k * hop:(k + 1) * hop] ** 2) + 1e-12) for k in range(n)])
        e = np.clip(e / (np.percentile(e, 92) + 1e-9), 0, 1)
        e = np.convolve(e, [0.25, 0.5, 0.25], "same")
        lines.append({"who": who, "text": text, "t": round(t, 3), "dur": round(dur, 3),
                      "words": [[round(a - lead, 3), round(b - lead, 3), w] for a, b, w in words],
                      "env": [round(float(v_), 3) for v_ in e]})
        voice.append((t, x))
        t += dur + GAP
    total = round(t - GAP + TAIL, 2)
    json.dump({"fps": FPS, "total": total, "lines": lines}, open(f"{OUT}/timeline.json", "w"))
    vo = np.zeros(int(total * sr) + sr, np.float32)
    for t0, x in voice:
        a = int(t0 * sr)
        vo[a:a + len(x)] += x
    bed = music.render("detective", total)[:, 0]
    act = np.abs(vo) > 0.01
    vrms = np.sqrt(np.mean(vo[act] ** 2))
    brms = np.sqrt(np.mean(bed ** 2))
    bed *= (vrms / brms) * 10 ** (-7.0 / 20)        # bed sits ~7 dB under the voices, never silent
    n = min(len(bed), len(vo))
    mix = vo[:n] + bed[:n]
    mix *= 0.89 / (np.abs(mix).max() + 1e-9)
    st = np.stack([mix, mix], 1)
    import wave
    with wave.open(f"{OUT}/mix.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
    print("total", total, [(l["who"], l["t"], l["dur"]) for l in lines])


asyncio.run(main())
