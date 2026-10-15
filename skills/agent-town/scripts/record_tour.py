#!/usr/bin/env python3
"""Record a 9:16 tour of town.html to out/tour.mp4 (1080x1920, 30 fps) plus 3 PNG stills.

The page exposes window.__town: we switch it to a virtual clock and step it one
frame at a time, so every frame is captured sharp and the motion is perfectly
smooth no matter how long each screenshot takes.

Usage:
    python scripts/record_tour.py               # full tour (~50 s)
    python scripts/record_tour.py --fps 24 --keep-frames
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent
TOWN = HERE / "town.html"
OUT = HERE / "out"
CHROMIUM = "/opt/pw-browsers/chromium"

INTRO, PER_AGENT, OUTRO = 4.5, 7.0, 4.0


def timeline(ids: list[str]) -> list[tuple[float, str]]:
    """(seconds, js) cues: open each building, scroll its panel, close it."""
    cues, t = [], INTRO
    for agent in ids:
        cues += [
            (t, f"__town.open('{agent}')"),
            (t + 1.5, "__town.scroll(0.62, 2400)"),
            (t + 4.6, "__town.scroll(0, 1100)"),
            (t + 5.9, "__town.close()"),
        ]
        t += PER_AGENT
    return cues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--keep-frames", action="store_true")
    args = ap.parse_args()
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found", file=sys.stderr)
        return 1
    OUT.mkdir(exist_ok=True)
    frames = Path(tempfile.mkdtemp(prefix="agent-town-frames-"))
    dt = 1000 / args.fps

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(TOWN.as_uri())
        page.wait_for_function("window.__town && document.querySelectorAll('.hit').length > 0", timeout=15000)
        page.wait_for_timeout(600)
        ids = page.evaluate("__town.ids()")
        page.evaluate("__town.virtual(1000)")

        cues = timeline(ids)
        total = INTRO + PER_AGENT * len(ids) + OUTRO
        n = int(total * args.fps)
        stills = {
            int(2.2 * args.fps): "still_1_town.png",
            int((INTRO + 1.3) * args.fps): f"still_2_{ids[0]}.png",
            int((INTRO + PER_AGENT * ids.index("meatball") + 4.2) * args.fps) if "meatball" in ids else -1: "still_3_meatball.png",
        }
        ci = 0
        for i in range(n):
            t = i / args.fps
            while ci < len(cues) and cues[ci][0] <= t:
                page.evaluate(cues[ci][1])
                ci += 1
            page.evaluate(f"__town.advance({dt})")
            page.screenshot(path=str(frames / f"f_{i:05d}.jpg"), type="jpeg", quality=92)
            if i in stills:
                page.screenshot(path=str(OUT / stills[i]))
            if i % (args.fps * 5) == 0:
                print(f"  frame {i}/{n}", flush=True)
        browser.close()
    if errors:
        print("page errors:", *errors, sep="\n  ", file=sys.stderr)

    mp4 = OUT / "tour.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(args.fps), "-i", str(frames / "f_%05d.jpg"),
        "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4),
    ], check=True)
    if not args.keep_frames:
        shutil.rmtree(frames)
    print(f"wrote {mp4} ({n} frames, {total:.1f} s) and stills in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
