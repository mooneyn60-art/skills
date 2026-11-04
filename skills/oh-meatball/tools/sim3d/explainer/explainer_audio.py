#!/usr/bin/env python3
"""Voices + timeline + premaster mix for the 3D Meatball explainer (script JSON driven, restart-safe).
explainer_audio.py SCRIPT.json KEY [TAG]  (TAG names the outputs, default KEY; env: MBX_PERSIST=/home/user/mbx-persist, MBX_WORK=/dev/shm/mbx/work)
Takes are cached in $MBX_PERSIST/vo/ (mp3 + word json); truncated takes are rejected and re-requested.
Writes $MBX_PERSIST/timeline-TAG.json and $MBX_WORK/premaster-TAG.wav (voice + the script's "music" bed, default
"playful", ~7 LU under it)."""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np
import pyloudnorm

TOOLS = os.environ.get("MB_TOOLS", "/home/user/skills/skills/oh-meatball/tools")
sys.path.insert(0, TOOLS)
import facts  # noqa: E402  (sets the proxy CA SSL context for edge-tts)
import music  # noqa: E402

PERSIST = os.environ.get("MBX_PERSIST", "/home/user/mbx-persist")
WORK = os.environ.get("MBX_WORK", "/dev/shm/mbx/work")
FPS, GAP, BEAT = 30, 0.48, 0.32
TAILS = {"tiktok": 1.3, "youtube": 0.3}   # YouTube Short: short tail so the last line loops into the first
VOICES = {"P": ("en-US-BrianNeural", "+6%", "+0Hz"), "M": ("en-US-AndrewMultilingualNeural", "+10%", "+3Hz")}
SR = music.SR


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(np.float32) / 32768


def tokens(text):
    return re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", text)   # TTS gives one boundary per hyphenated word


def check_take(x, ws, text):
    """None if the take is complete, else the reason it is rejected."""
    if not ws:
        return "no word boundaries"
    if len(ws) < len(tokens(text)):
        return f"{len(ws)} boundaries < {len(tokens(text))} words"
    idx = np.where(np.abs(x) > 0.01)[0]
    if not len(idx):
        return "silent"
    end = idx[-1] / SR
    a, b, _ = ws[-1]
    if len(x) / SR < b - 0.02 or end < a + 0.5 * (b - a):
        return f"audio ends {end:.2f}s before last word {a:.2f}-{b:.2f}s"
    return None


async def take(text, who):
    voice, rate, pitch = VOICES[who]
    key = hashlib.sha1(f"{text}|{voice}|{rate}|{pitch}".encode()).hexdigest()[:12]
    mp3, js = f"{PERSIST}/vo/{key}.mp3", f"{PERSIST}/vo/{key}.json"
    if os.path.exists(mp3) and os.path.exists(js):
        return pcm(mp3), json.load(open(js))
    best = None
    for attempt in range(6):
        tmp = mp3 + ".part"
        ws = await facts.speak(text, voice, tmp, rate=rate, pitch=pitch)
        x = pcm(tmp) if os.path.getsize(tmp) else np.zeros(0, np.float32)
        why = check_take(x, ws, text)
        if why is None:
            os.replace(tmp, mp3)
            json.dump(ws, open(js, "w"))
            return x, ws
        print(f"  reject take {attempt} of {text!r}: {why}", flush=True)
        if best is None or len(x) > len(best[0]):
            best = (x, ws)
        await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"no complete take for {text!r}")


def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    a = max(0, idx[0] - int(0.02 * SR))
    return x[a:idx[-1] + int(0.08 * SR)], a / SR


async def main():
    script, key = sys.argv[1], sys.argv[2]
    tag = sys.argv[3] if len(sys.argv) > 3 else key
    os.makedirs(f"{PERSIST}/vo", exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    doc = json.load(open(script))
    rows, kind = doc[key], doc.get("music", "playful")
    t, lines, voice = 0.0, [], []
    for i, row in enumerate(rows):
        parts = [p.strip() for p in row["t"].split(" / ")]
        x, words = np.zeros(0, np.float32), []
        for j, part in enumerate(parts):   # "a / b" = separate takes joined by a short beat (deadpan timing)
            y, ws = await take(part, row["s"])
            y, lead = trim(y)
            off = len(x) / SR
            words += [(a - lead + off, b - lead + off, w) for a, b, w in ws]
            x = np.concatenate([x, y, np.zeros(int(BEAT * SR) if j < len(parts) - 1 else 0, np.float32)])
        dur = len(x) / SR
        hop, n = SR // FPS, int(dur * FPS) + 1
        e = np.array([np.sqrt(np.mean(x[k * hop:(k + 1) * hop] ** 2) + 1e-12) for k in range(n)])
        e = np.convolve(np.clip(e / (np.percentile(e, 92) + 1e-9), 0, 1), [0.25, 0.5, 0.25], "same")
        lines.append({"i": i, "who": row["s"], "text": " ".join(parts), "t": round(t, 3), "dur": round(dur, 3),
                      "words": [[round(a, 3), round(b, 3), w] for a, b, w in words], "env": [round(float(v), 3) for v in e],
                      "card": row.get("card"), "src": row.get("src"), "shot": row.get("shot")})
        voice.append((t, x))
        print(f"{i:2d} {row['s']} t={t:6.2f} dur={dur:5.2f} {row['t']}", flush=True)
        t += dur + GAP
    total = round(t - GAP + TAILS.get(key, 1.3), 2)
    json.dump({"key": key, "fps": FPS, "total": total, "lines": lines}, open(f"{PERSIST}/timeline-{tag}.json", "w"))
    vo = np.zeros(int(total * SR), np.float32)
    for t0, x in voice:
        a = int(round(t0 * SR))
        vo[a:a + len(x)] += x[:len(vo) - a]
    with wave.open(f"{WORK}/vo-{tag}.wav", "wb") as w:   # voice-only stem for the onset / truncation checks
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(vo, -1, 1) * 32767).astype("<i2").tobytes())
    bed = music.render(kind, total)
    meter = pyloudnorm.Meter(SR)
    lv, lb = meter.integrated_loudness(np.stack([vo, vo], 1)), meter.integrated_loudness(bed)
    bed *= 10 ** ((lv - 7.0 - lb) / 20)     # bed sits ~7 LU under the voices
    n = min(len(bed), len(vo))
    mix = bed[:n] + vo[:n, None]
    mix *= 0.5 / (np.abs(mix).max() + 1e-9)  # headroom; the master gain + limiter come at the mux
    with wave.open(f"{WORK}/premaster-{tag}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
    print("total", total, "music", kind, "voice LUFS", round(lv, 1), "bed LUFS", round(lb, 1), "->", round(lv - 7, 1))


asyncio.run(main())
