"""Mix a music bed + timed SFX cues into one WAV (used by build-formats.js).
Usage: python3 src/mix-audio.py spec.json
spec = {"music": "xmas-lofi.wav", "musicVol": .8, "dur": 18.0, "out": "/abs/out.wav",
        "cues": [["send", 0.5, 0.5], ...]}   # name -> tiktok/sfx-<name>.wav, start seconds, volume
"""
import json, os, sys, wave
import numpy as np
TT = os.path.join(os.path.dirname(__file__), "..", "tiktok")

def load(path):
    with wave.open(path) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32767
    x = x.reshape(-1, ch)
    if ch == 1: x = np.repeat(x, 2, 1)
    return sr, x

spec = json.load(open(sys.argv[1]))
sr, music = load(os.path.join(TT, spec["music"]))
N = int(spec["dur"] * sr)
out = np.zeros((N, 2), np.float32)
m = music[:N] * spec.get("musicVol", .8)
out[:len(m)] += m
for name, at, vol in spec["cues"]:
    _, s = load(os.path.join(TT, f"sfx-{name}.wav"))
    i = int(max(0, at) * sr)
    if i >= N: continue
    j = min(N, i + len(s))
    out[i:j] += s[:j - i] * vol
fade = int(.7 * sr); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
peak = np.max(np.abs(out))
if peak > .97: out *= .97 / peak                      # avoid clipping
with wave.open(spec["out"], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("mixed", spec["out"])
