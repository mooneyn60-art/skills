#!/usr/bin/env python3
"""Self-checks for a finished explainer cut.
checks.py FINAL.mp4 TIMELINE.json VO_STEM.wav [--min 62 --max 65]
Prints JSON: duration, voice onset, truncated lines, 2.5 kHz zap windows, integrated LUFS, true peak."""
import argparse
import json
import re
import subprocess

import numpy as np
import pyloudnorm

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("timeline"); ap.add_argument("vo")
ap.add_argument("--min", type=float, default=62); ap.add_argument("--max", type=float, default=65)
a = ap.parse_args()


def decode(path, sr, ch):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<f4").reshape(-1, ch)


dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                           capture_output=True, text=True, check=True).stdout)
tl = json.load(open(a.timeline))
vo = decode(a.vo, 48000, 1)[:, 0]
onset = float(np.argmax(np.abs(vo) > 0.02) / 48000)
trunc = []   # a line is truncated if its audio ends before its last word boundary
for l in tl["lines"]:
    s0, s1 = int(l["t"] * 48000), int((l["t"] + l["dur"]) * 48000)
    seg = vo[s0:s1]
    idx = np.where(np.abs(seg) > 0.01)[0]
    end = idx[-1] / 48000 if len(idx) else 0
    wa, wb = l["words"][-1][0], l["words"][-1][1]
    if end < wa + 0.5 * (wb - wa):
        trunc.append({"i": l["i"], "audio_end": round(end, 3), "last_word": [wa, wb]})
# 2.5 kHz zap detector: mono 24 kHz, 2400-sample hanning windows, band 2400-2600 Hz vs reference 900-4000 Hz
x = decode(a.video, 24000, 1)[:, 0]   # float [-1, 1]; also evaluated at int16 scale (stricter)
N, hop = 2400, 1200
win = np.hanning(N)
f = np.fft.rfftfreq(N, 1 / 24000)
band, ref = (f >= 2400) & (f <= 2600), (f >= 900) & (f <= 4000)
zaps, zaps16 = [], []
for k in range(0, len(x) - N, hop):
    sp = np.abs(np.fft.rfft(x[k:k + N] * win))
    mb, mr = sp[band].max(), np.median(sp[ref])
    if mb / (mr + 1e-9) > 120:
        if mb > 15:
            zaps.append(round(k / 24000, 2))
        if mb * 32768 > 15:
            zaps16.append(round(k / 24000, 2))
st = decode(a.video, 48000, 2)
lufs = pyloudnorm.Meter(48000).integrated_loudness(st.astype(np.float64))
eb = subprocess.run(["ffmpeg", "-v", "info", "-nostats", "-i", a.video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
tp = re.findall(r"Peak:\s+(-?[\d.]+|-inf) dBFS", eb)
out = {"duration": round(dur, 3), "duration_ok": a.min <= dur <= a.max, "voice_onset_s": round(onset, 3), "onset_ok": onset < 0.1,
       "truncated_lines": trunc, "zap_windows": len(zaps), "zap_windows_int16_scale": len(zaps16), "zap_times": (zaps16 or zaps)[:10], "lufs": round(lufs, 2),
       "true_peak_dbfs": float(tp[-1]) if tp else None, "sample_peak_dbfs": round(float(20 * np.log10(np.abs(st).max() + 1e-12)), 2)}
print(json.dumps(out))
