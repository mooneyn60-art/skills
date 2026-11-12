#!/usr/bin/env python3
"""Gates for a 16:9 drawn long-form (tools/drawn_keepkill.py):

  lf_gates.py OUT.mp4 --work WORK_DIR --spec SPEC.json [--sheets DIR]

  size        1920x1080
  beep scan   tonal beeps near 2.5 kHz in the final mix: a narrow peak in 2.3-2.7 kHz that stands >= 15 dB above
              the 1.6-2.1 / 2.9-3.4 kHz shoulders for >= 80 ms. Must be 0.
  first voice the first voice sample (|x| > 0.01 in the first line's trimmed TTS) must start < 0.2 s
  shots       no camera framing held > 4 s: every line start, macro camera move and auto re-cut counts as a new
              shot; boards/cards don't count. Also prints the longest pixel hold (4 fps, greyscale diff)
  sheets      contact sheets: every 2 s for the first 60 s, and every 20 s for the whole video
"""
import argparse
import io
import json
import os
import subprocess
import sys
import contextlib

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", path], capture_output=True, text=True)
    j = json.loads(out.stdout)
    return j["streams"][0]["width"], j["streams"][0]["height"], float(j["format"]["duration"])


def audio(path, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32), sr


def beep_scan(x, sr):
    """Pure-tone beeps near 2.5 kHz: a spectral peak in 2.3-2.7 kHz that is >= 15 dB above the bins 4-8 either side
    (narrow, i.e. a tone, not a voice formant) and stays on the same bin (+-1) for >= 80 ms (voice harmonics glide)."""
    n, hop = 1024, 256
    win = np.hanning(n).astype(np.float32)
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * win
    spec = 20 * np.log10(np.abs(np.fft.rfft(frames, axis=1)) + 1e-9)
    f = np.fft.rfftfreq(n, 1 / sr)
    lo, hi = np.searchsorted(f, 2300), np.searchsorted(f, 2700)
    idx = lo + spec[:, lo:hi].argmax(1)
    rows = np.arange(len(idx))
    side = np.maximum(spec[rows, idx - 6], spec[rows, idx + 6])
    side = np.maximum(side, np.maximum(spec[rows, idx - 4], spec[rows, idx + 4]))
    loud = 20 * np.log10(np.sqrt(np.mean(frames ** 2, 1)) + 1e-9) > -50
    hit = (spec[rows, idx] - side >= 15) & loud
    need = int(0.08 * sr / hop) + 1
    events, run = [], 0
    for i in range(len(hit)):
        run = run + 1 if hit[i] and (run == 0 or abs(int(idx[i]) - int(idx[i - 1])) <= 1) else (1 if hit[i] else 0)
        if run == need:
            events.append(round(i * hop / sr, 2))
    return events


def shots(spec_path, work, end_hold=0.0):
    sys.argv = ["x", spec_path, "/dev/null"]
    import drawn_keepkill as kk
    import drawn
    raw = json.load(open(spec_path))
    if raw.get("builder") and raw.get("lines") and not raw.get("beats"):   # opt-in: a built line spec (e.g. drawn_catlife):
        import importlib                                                     # its own module turns it into drawn beats
        raw = importlib.import_module(raw["builder"]).drawn_spec(raw, raw["lines"])
    if raw.get("ds"):   # a "Don't squish it" spec: register its overlays and music envelope too
        import drawn_dontsquish  # noqa: F401
    with contextlib.redirect_stdout(io.StringIO()):
        beats, total = drawn.plan(kk.drawn_macros.expand(raw), work)
    # opt-in (--end-hold S): the end screen's last S s is a deliberate hold for YouTube's end-screen elements
    end = total - end_hold if end_hold else total
    marks = sorted({0.0, end} | {round(b["t0"] + s["at"], 3) for b in beats for s in b["shots"] if b["t0"] + s["at"] < end} |
                   {round(b["t0"], 3) for b in beats if b["t0"] < end})
    gaps = [(b - a, a) for a, b in zip(marks, marks[1:])]
    first = beats[0]
    on = np.where(np.abs(first["audio"]) > 0.01)[0]
    return max(gaps), total, (on[0] / drawn.SR if len(on) else None), beats


def pixel_hold(path, fps=4):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale=160:90,format=gray", "-f",
                          "rawvideo", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.float32)
    d = np.abs(np.diff(a, axis=0)).mean((1, 2))
    best, run, at = 0, 0, 0
    for i, v in enumerate(d):
        run = run + 1 if v < 0.6 else 0
        if run > best:
            best, at = run, i - run + 1
    return best / fps, at / fps


def sheet(path, times, out, cols):
    ims = []
    for t in times:
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1", "-vf",
                              "scale=384:216", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if png:
            ims.append((t, Image.open(io.BytesIO(png)).convert("RGB")))
    rows = (len(ims) + cols - 1) // cols
    m = Image.new("RGB", (cols * 384, rows * 236), (20, 20, 20))
    from PIL import ImageDraw
    d = ImageDraw.Draw(m)
    for k, (t, im) in enumerate(ims):
        x, y = (k % cols) * 384, (k // cols) * 236
        m.paste(im, (x, y))
        d.text((x + 6, y + 218), f"{int(t // 60)}:{t % 60:05.2f}", fill=(255, 220, 0))
    m.save(out, quality=86)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--work", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--sheets")
    ap.add_argument("--end-hold", type=float, default=0.0, help="opt-in: ignore the end screen's last S s in the shots gate")
    ap.add_argument("--lufs", type=float, help="opt-in: integrated loudness target (+-1 LU) and true peak < -1 dBFS")
    ap.add_argument("--max-mb", type=float, help="opt-in: file size limit in MB")
    a = ap.parse_args()
    ok = True
    w, h, dur = probe(a.mp4)
    print(f"size        {w}x{h}  {'PASS' if (w, h) == (1920, 1080) else 'FAIL'}   length {int(dur // 60)}:{dur % 60:04.1f}")
    ok &= (w, h) == (1920, 1080)
    x, sr = audio(a.mp4)
    ev = beep_scan(x, sr)
    print(f"beep scan   {len(ev)} at 2.5 kHz  {'PASS' if not ev else 'FAIL ' + str(ev[:10])}")
    ok &= not ev
    if a.lufs is not None:
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", a.mp4, "-af", "ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True).stderr.split("Summary:")[-1]
        import re
        li = float(re.search(r"I:\s+(-?[\d.]+) LUFS", r).group(1))
        tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", r).group(1))
        good = abs(li - a.lufs) <= 1.0 and tp < -1.0
        print(f"loudness    {li:.1f} LUFS, true peak {tp:.1f} dBFS  {'PASS' if good else 'FAIL'}")
        ok &= good
    if a.max_mb is not None:
        mb = os.path.getsize(a.mp4) / 1e6
        print(f"file size   {mb:.1f} MB  {'PASS' if mb < a.max_mb else 'FAIL'}")
        ok &= mb < a.max_mb
    (gap, at), total, fv, _ = shots(a.spec, a.work, a.end_hold)
    print(f"first voice {fv:.3f} s  {'PASS' if fv is not None and fv < 0.2 else 'FAIL'}")
    ok &= fv is not None and fv < 0.2
    print(f"shots       longest framing {gap:.2f} s at {int(at // 60)}:{at % 60:05.2f}  {'PASS' if gap <= 4.0 else 'FAIL'}")
    ok &= gap <= 4.0
    hold, hat = pixel_hold(a.mp4)
    print(f"            longest pixel hold {hold:.2f} s at {int(hat // 60)}:{hat % 60:05.2f} (info)")
    if a.sheets:
        os.makedirs(a.sheets, exist_ok=True)
        sheet(a.mp4, [k * 2.0 for k in range(30)], os.path.join(a.sheets, "first60-every2s.jpg"), 6)
        sheet(a.mp4, [k * 20.0 for k in range(int(dur // 20) + 1)], os.path.join(a.sheets, "every20s.jpg"), 6)
        print("sheets in", a.sheets)
    print("GATES", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    main()
