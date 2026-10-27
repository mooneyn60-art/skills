#!/usr/bin/env python3
"""Screen gate (TARS review 10/27): checks what a viewer actually SEES, on a rendered timeline or an mp4.

  (a) HOLD    no single picture on screen longer than the cap (Shorts 2.5 s; a spec "max_shot" raises it,
              e.g. the sleep compilations' 4-6 s holds)
  (d) SMEAR   hard cuts only: no motion-blur whip pans (timeline: a "whip" transition; video: frames whose
              horizontal detail collapses against their neighbours, the smeared look TARS saw ~1 in 8)
  (f) ASKS    no poll card or subscribe pill before 0:10; the opinion poll lands at ~10-12 s; the subscribe
              pill sits in the last 3-5 s; at most one pill. A render made with spec "early_asks": true (the
              6-v-6 ask test) is checked against the old ask-kit windows instead and says so.

Usage:
  screengate.py WORK/timeline.json            exact check of a tools/v3.py render (v3.build runs it itself)
  screengate.py VIDEO.mp4 [--hold 2.5]        pixel check of any render, old or new (holds + smear + the red
                                              SUBSCRIBE pill in the first 10 s); no timeline needed
Exit 1 when anything fails. --json prints the report as JSON.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

HOLD = 2.5
NO_ASK_BEFORE = 10.0
POLL = (9.5, 13.0)
PILL_FROM_END = (6.0, 2.5)   # the pill pops between 6 s and 2.5 s before the end (aim: the last 3-5 s)


def check_timeline(tl):
    """tl: the dict v3.build writes (timeline.json): {"total", "policy", "beats": [...], "transitions": [...]}."""
    pol = tl.get("policy", {})
    hold = float(pol.get("hold", HOLD))
    total = float(tl["total"])
    fails, notes = [], []
    for b in tl.get("pictures") or tl["beats"]:   # "pictures": runs of one photo+crop merged across lines
        for a, z in b["shots"]:
            if z - a > hold + 0.04:
                fails.append(f"(a) HOLD one picture {z - a:.2f}s at {b['start'] + a:.1f}s (cap {hold:g} s)")
    for t in tl.get("transitions", []):
        if t["kind"] == "whip":
            fails.append(f"(d) SMEAR motion-blur whip pan at {t['t']:.2f}s (hard cuts only)")
    if pol.get("asks") == "landscape":
        notes.append("asks: long-form windows (checked by v3's own gate)")
        return dict(fails=fails, notes=notes)
    early = pol.get("asks") == "early"
    pills = [a for a in tl.get("asks", []) if a["kind"] == "pill"]
    polls = [a for a in tl.get("asks", []) if a["kind"] == "poll"]
    if early:
        notes.append("asks: early_asks flag set (6-v-6 test arm): old ask-kit windows")
        for a in tl.get("asks", []):
            if a["t"] < 3.0:
                fails.append(f"(f) ASK {a['kind']} at {a['t']:.1f}s: nothing in the first 3 s")
    else:
        for a in tl.get("asks", []):
            if a["t"] < NO_ASK_BEFORE:
                fails.append(f"(f) ASK {a['kind']} at {a['t']:.1f}s: no poll or pill before 0:{NO_ASK_BEFORE:02.0f}")
        for a in polls:
            if a["t"] >= NO_ASK_BEFORE and not POLL[0] <= a["t"] <= POLL[1] and total < 120:
                notes.append(f"poll at {a['t']:.1f}s (aim ~10-12 s)")
        for a in pills:
            left = total - a["t"]
            if a["t"] >= NO_ASK_BEFORE and not PILL_FROM_END[1] <= left <= PILL_FROM_END[0]:
                fails.append(f"(f) ASK subscribe pill {left:.1f}s before the end (aim: the last 3-5 s)")
    if len(pills) > 1:
        fails.append(f"(f) ASK {len(pills)} subscribe pills (one)")
    return dict(fails=fails, notes=notes)


# ---------------------------------------------------------------- video

def _frames(path, fps, w, h):
    cmd = ["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}", "-pix_fmt", "rgb24",
           "-f", "rawvideo", "pipe:1"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def _size(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    w, h = map(int, out.strip().split(",")[:2])
    return w, h


def check_video(path, hold=HOLD):
    import cv2
    W, H = _size(path)
    w, h = (270, 480) if H > W else (480, 270)
    fps = 30
    fr = _frames(path, fps, w, h)
    g = np.stack([cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in fr]).astype(np.float32)
    # (a) cuts: a big jump in the picture region (captions and the lower third ignored). A tighter re-cut of the
    # same photo counts as a new picture; a slow push, a pop-in label or Meatball's moves do not.
    top = slice(0, int(h * 0.62)) if H > W else slice(0, int(h * 0.8))
    small = np.stack([cv2.resize(cv2.GaussianBlur(x[top], (0, 0), 2), (48, 48)) for x in g])
    d = np.abs(np.diff(small, axis=0)).mean(axis=(1, 2))
    cuts = [0] + [k + 1 for k in range(len(d)) if d[k] > 14 and (k == 0 or d[k] > 2.2 * np.median(d[max(0, k - 15):k + 15]))]
    cuts.append(len(g))
    fails, holds = [], []
    for a, z in zip(cuts, cuts[1:]):
        dur = (z - a) / fps
        holds.append(dur)
        if dur > hold + 0.1:
            fails.append(f"(a) HOLD one picture {dur:.1f}s from {a / fps:.1f}s (cap {hold:g} s)")
    # (d) smear: horizontal detail collapses (a horizontal motion blur) against the frames around it
    gx = np.array([np.abs(cv2.Sobel(x, cv2.CV_32F, 1, 0, ksize=3)).mean() for x in g])
    gy = np.array([np.abs(cv2.Sobel(x, cv2.CV_32F, 0, 1, ksize=3)).mean() for x in g])
    r = gx / np.maximum(gy, 1e-3)
    smear = [k for k in range(len(r)) if r[k] < 0.62 * np.median(r[max(0, k - 30):k + 30])]
    if smear:
        runs, s0 = [], smear[0]
        for p, q in zip(smear, smear[1:] + [None]):
            if q != p + 1:
                runs.append((s0, p))
                s0 = q
        fails.append(f"(d) SMEAR {len(smear)} motion-blurred frames ({100 * len(smear) / len(g):.0f}% of frames) "
                     f"at " + ", ".join(f"{a / fps:.1f}s" for a, _ in runs[:8]) + (" ..." if len(runs) > 8 else ""))
    # (f) the red SUBSCRIBE pill (v3 ask kit, RGB 230,33,23) inside the first 10 s
    band = slice(int(h * 0.66), int(h * 0.84)) if H > W else slice(int(h * 0.7), h)   # where the pill sits
    red = [(k / fps) for k in range(0, min(len(fr), 10 * fps), 3)
           if ((np.abs(fr[k][band][..., 0].astype(int) - 230) < 22) & (fr[k][band][..., 1] < 70)
               & (fr[k][band][..., 2] < 70)).mean() > 0.02]
    if red:
        fails.append(f"(f) ASK a red subscribe pill on screen at {red[0]:.1f}s (none before 0:10)")
    return dict(fails=fails, notes=[f"{len(cuts) - 2} cuts, longest picture {max(holds):.1f}s, "
                                    f"{len(g) / fps:.1f}s"], holds=holds, smear=len(smear))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--hold", type=float, default=HOLD)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rep = check_video(a.path, a.hold) if a.path.endswith(".mp4") else check_timeline(json.load(open(a.path)))
    if a.json:
        print(json.dumps({k: v for k, v in rep.items() if k != "holds"}, indent=1))
    else:
        for n in rep["notes"]:
            print("screengate:", n)
        for f in rep["fails"]:
            print("SCREENGATE FAIL", f)
        print("screengate:", "PASS" if not rep["fails"] else f"{len(rep['fails'])} fail(s)")
    sys.exit(1 if rep["fails"] else 0)


if __name__ == "__main__":
    main()
