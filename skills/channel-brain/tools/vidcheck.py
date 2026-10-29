#!/usr/bin/env python3
"""Visual gate for a rendered Short: is it a video or a slideshow? Run before anything is queued.

    python3 vidcheck.py episodes/drawn-house/yt-scabies.mp4 [more.mp4 ...]

Measures from the pixels (no OCR, no API):
  length        YouTube Shorts: <= 20 s (Nolan's channel data, NICHE_PLAYBOOK)
  changes/10s   big visual changes (cut, reframe, new scene) per 10 s (info)
  longest hold  longest stretch where the picture barely changes (info)
  same scene    share of frames whose background bands match frame 0 (info)
Only length is a gate (exit 1). The other three are printed as information: on 10/29 the best Short ever
(Daddy Longlegs) scored LOW on them, so they don't predict retention by themselves. The real content checks
(is the creature recognisable at frame 0, does Meatball act, does the scene move) are in CONTENT_REVIEW_2026-10-29.md.
"""
import subprocess, sys
import numpy as np

try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = "ffmpeg"
FPS, W, H = 4, 90, 160  # 4 samples a second, tiny 9:16 greyscale frames


def frames(path):
    out = subprocess.run([FF, "-v", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(out, dtype=np.uint8).astype(np.float32)
    return list(a.reshape(-1, H, W))


def check(path):
    fs = frames(path)
    n = len(fs)
    secs = n / FPS
    d = [float(np.mean(np.abs(fs[k] - fs[k - 1]))) for k in range(1, n)]
    big = [x > 12 for x in d]  # a cut / reframe / new scene (tuned on the 10/29 renders)
    changes = sum(1 for k, b in enumerate(big) if b and (k == 0 or not big[k - 1]))
    hold, best = 0, 0
    for x in d:
        hold = hold + 1 if x < 4 else 0
        best = max(best, hold)
    # background match vs frame 0: compare the top and bottom bands (where the scene is, not the actor)
    h = fs[0].shape[0]
    band = lambda f: np.concatenate([f[int(h * .2):int(h * .35)], f[int(h * .75):int(h * .9)]])
    same = sum(float(np.mean(np.abs(band(f) - band(fs[0])))) < 10 for f in fs) / n
    r = {"length_s": round(secs, 1), "changes_per_10s": round(changes / secs * 10, 1),
         "longest_hold_s": round(best / FPS, 1), "same_scene_pct": round(same * 100)}
    fails = []
    if secs > 20.5: fails.append("over 20 s")
    # changes/hold/same-scene are INFO only: the channel's best Short (Daddy Longlegs, 19.8 s) scored
    # 1.5 changes/10s and a 5.5 s hold, so pixel motion alone does not predict retention (tested 10/29).
    return r, fails


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        r, fails = check(p)
        bad += bool(fails)
        print(f"{'FAIL' if fails else 'PASS'}  {p.split('/')[-1]:32s} {r}  {'; '.join(fails)}")
    sys.exit(1 if bad else 0)
