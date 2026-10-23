#!/usr/bin/env python3
"""One command from episode script to upload-ready release: long-form + one quiz Short per myth,
chapters, photo credits, titles, tags and a release.json the scheduler posts from.

Usage: episode.py SCRIPT.json SLUG [--work DIR] [--skip-long] [--skip-shorts]
  SCRIPT.json  episode beats (each beat tagged with "myth"; each myth opens on a "quiz" beat)
  SLUG         output folder name under episodes/, e.g. myths-03

Writes episodes/SLUG/{ep.mp4, short-<myth>.mp4, credits.txt, release.json}. Commit + push, then
schedule from release.json (every media URL in it is the public raw GitHub URL of the pushed file).
"""
import argparse
import collections
import json
import os
import re
import shutil
import subprocess

import explainer
from shorts_split import END, tighten

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = ("https://raw.githubusercontent.com/mooneyn60-art/skills/claude/youtube-monetization-strategy-m9vz6i/"
       "skills/oh-meatball/episodes")
MAX_MB = 45  # GitHub warns above 50 MB and refuses above 100 MB
COMMON = {}  # optional scientific -> common name map loaded from the script's "names"
LICENSES = "creativecommons.org/licenses/by/4.0 · creativecommons.org/licenses/by-sa/4.0"


def run_build(spec, work, out, vertical=False):
    cmd = ["python3", f"{HERE}/explainer.py", spec, work, "build", out] + (["--vertical"] if vertical else [])
    subprocess.run(cmd, check=True, cwd=HERE)


def claim(beat):
    """'True or false? Camels store water in their humps.' -> 'Camels store water in their humps'"""
    return re.sub(r"^true or false\?\s*", "", beat["say"], flags=re.I).rstrip(".!? ")


def credit_lines(work, beats):
    by = collections.OrderedDict()
    for b in beats:
        if "photo" not in b:
            continue
        path = explainer.photo(b["photo"], b.get("n", 0), work, b.get("obs"))
        line = open(path + ".credit").read()
        m = re.search(r"\(c\) (.+?), some rights reserved \((CC [A-Z-]+)\)", line)
        name = COMMON.get(b["photo"], b["photo"])
        if " via " in line:  # Openverse art/fossil credit is already a full sentence
            by.setdefault(name, []).append(line.split(": ", 1)[1])
            continue
        by.setdefault(name, []).append(f"{m.group(1)} ({m.group(2)})" if m else "CC0")
    return [f"{k}: " + ", ".join(dict.fromkeys(v)) for k, v in by.items()]


def chapters(work, beats):
    """Start time of each myth, from the rendered segment list (countdown segments included)."""
    segs = [line.split("'")[1] for line in open(f"{work}/list.txt")]
    t, out = 0.0, collections.OrderedDict()
    for s in segs:
        name = os.path.basename(s)
        if "_c" not in name:
            b = beats[int(name[3:5])]
            label = (b.get("chapter") or {"intro": "Play along", "outro": "Scores"}.get(b["myth"])
                     or claim(b) + "?")
            out.setdefault(b["myth"], (t, label))
        t += explainer.duration(s)
    return [f"{int(v // 60)}:{int(v % 60):02d} {label}" for v, label in out.values()]


def shrink(path):
    if os.path.getsize(path) < MAX_MB * 1e6:
        return
    tmp = path + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-c:v", "libx264", "-crf", "26",
                    "-preset", "medium", "-c:a", "copy", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("slug")
    ap.add_argument("--work", default=f"/tmp/meatball-build")
    ap.add_argument("--skip-long", action="store_true")
    ap.add_argument("--skip-shorts", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.script))
    COMMON.update(spec.get("names", {}))
    beats = spec["beats"]
    out = f"{ROOT}/episodes/{a.slug}"
    os.makedirs(out, exist_ok=True)
    long_work = f"{a.work}/{a.slug}/long"
    release = {"long": None, "shorts": []}

    if not a.skip_long:
        run_build(os.path.abspath(a.script), long_work, f"{long_work}/ep.mp4")
        shrink(f"{long_work}/ep.mp4")
        shutil.move(f"{long_work}/ep.mp4", f"{out}/ep.mp4")
    credits = credit_lines(long_work, beats)
    open(f"{out}/credits.txt", "w").write("\n".join(credits) + "\n")
    myths = list(dict.fromkeys(b["myth"] for b in beats if b.get("myth") not in ("intro", "outro")))
    release["long"] = {
        "file": f"{RAW}/{a.slug}/ep.mp4", "thumb": f"{RAW}/{a.slug}/thumb.jpg", "title": spec["title"],
        "tags": spec.get("tags", []), "comment": spec.get("pinned", ""),
        "description": "\n".join([spec.get("blurb", ""), ""] + chapters(long_work, beats) + [
            "", spec.get("next", ""), "", f"Wildlife photos from iNaturalist, used under their licenses ({LICENSES}):"]
            + credits + ["", spec.get("hashtags", "#animalfacts #trueorfalse #quiz #mythbusting #animals")]),
    }

    for m in myths:
        mb = [b for b in beats if b.get("myth") == m]
        q = next((b for b in mb if "quiz" in b), None)
        if q is None:  # story chapters with no quiz don't make a standalone Short
            continue
        swork = f"{a.work}/{a.slug}/short-{m}"
        sspec = f"{swork}/script.json"
        os.makedirs(swork, exist_ok=True)
        json.dump({"voice": spec.get("voice", "en-US-AndrewNeural"), "rate": spec.get("short_rate", "+8%"),
                   "music": spec.get("music"), "beats": tighten(mb) + [END]}, open(sspec, "w"))
        if not a.skip_shorts:
            os.makedirs(f"{swork}/photos", exist_ok=True)
            subprocess.run(f"cp -n {long_work}/photos/* {swork}/photos/ 2>/dev/null || true", shell=True)
            run_build(sspec, swork, f"{swork}/short.mp4", vertical=True)
            shutil.move(f"{swork}/short.mp4", f"{out}/short-{m}.mp4")  # never expose a half-written file to git
        c = claim(q)
        release["shorts"].append({
            "myth": m, "file": f"{RAW}/{a.slug}/short-{m}.mp4",
            "title": f"TRUE or FALSE: {c}? 🤔 #shorts"[:100],
            "description": f"TRUE or FALSE? {c}. Guess before the timer, then comment if you got it right 👇 "
                           f"Full quiz episode on the channel.\n\n#shorts #trueorfalse #animalfacts #quiz\n\n"
                           f"Photos (iNaturalist): " + "; ".join(credit_lines(long_work, mb)) + f". {LICENSES}",
            "comment": (f"{q['bonus']}\n\n" if q.get("bonus") else "") + "Did you guess right? Comment ✅ TRUE or ❌ FALSE 👇",
            "tags": [m, "true or false", "animal quiz", "animal facts", "animal myths", "fun facts", "shorts",
                     "Meatball Myths"],
        })
    json.dump(release, open(f"{out}/release.json", "w"), indent=1, ensure_ascii=False)
    print(f"ok {out} long={'skipped' if a.skip_long else 'built'} shorts={len(release['shorts'])}")


if __name__ == "__main__":
    main()
