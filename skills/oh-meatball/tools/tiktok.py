#!/usr/bin/env python3
"""TikTok cuts of an episode: consecutive myths grouped until the cut runs past one minute, because
TikTok's Creator Rewards Program only pays on videos longer than 60 s (Shorts stay 25-45 s).

Usage: tiktok.py SCRIPT.json SLUG [--work DIR]
Needs the long-form build's photos (run episode.py first). Writes episodes/SLUG/tt-<n>.mp4 and
tiktok.json (file URL, caption, first comment) for the scheduler.
"""
import argparse
import json
import os
import re
import shutil
import subprocess

import explainer
from episode import RAW, ROOT, claim

MIN_S = 75  # margin over TikTok's 60 s floor; the estimate below can run ~10% long
WPS = 2.9   # en-US-AndrewMultilingualNeural at rate +15%; +0% measured 2.5 on episodes 2-3
END = {"say": "How many did you get? Comment your score, and follow, because the full twelve-myth quiz is on my profile.",
       "pose": "wave", "text": "COMMENT\nYOUR SCORE"}


TAGS = ["#didyouknow", "#mythbusting", "#animals", "#wildlife", "#science", "#nature", "#funfacts", "#learnsomethingnew"]


def question(q):
    """The hand-written searched question (short_title) without emoji or 'TRUE or FALSE' tails."""
    t = q.get("short_title") or claim(q) + "?"
    t = re.sub(r"\s*(🤔|TRUE or FALSE|#\w+).*$", "", t).strip()
    return re.sub(r"[^\w\s'?,!.&-]", "", t).strip()


def title(quizzes, n):
    """Unique per cut: the first myth's searched question plus a Part label (research/35: 'Part N' series win)."""
    return f"Part {n}: {question(quizzes[0])}" if quizzes else f"Part {n}"


def caption(quizzes, n, slug):
    """Unique per cut: every myth question in the cut, then 3 hashtags rotated by slug and part (no file nicknames)."""
    k = sum(map(ord, slug)) + n
    tags = [TAGS[(k + i) % len(TAGS)] for i in range(2)] + ["#learnontiktok"]
    return " ".join(question(q) for q in quizzes) + " Comment your score 👇 " + " ".join(tags)


def estimate(beats):
    return sum(len(b["say"].split()) / WPS + (3 if "quiz" in b else 0.6) for b in beats)


def groups(beats):
    myths = list(dict.fromkeys(b["myth"] for b in beats if b.get("myth") not in (None, "intro", "outro")))
    out, cur = [], []
    for m in myths:
        cur.append(m)
        if estimate([b for b in beats if b.get("myth") in cur] + [END]) >= MIN_S:
            out.append(cur)
            cur = []
    if cur:  # leftover myths join the last group rather than make a cut under a minute
        if out:
            out[-1] += cur
        else:
            out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("slug")
    ap.add_argument("--work", default="/tmp/meatball-build")
    ap.add_argument("--skip-existing", action="store_true", help="keep cuts already rendered (resume after a stop)")
    a = ap.parse_args()
    spec = json.load(open(a.script))
    beats = spec["beats"]
    out = f"{ROOT}/episodes/{a.slug}"
    long_photos = f"{a.work}/{a.slug}/long/photos"
    release = []
    for n, ms in enumerate(groups(beats), 1):
        work = f"{a.work}/{a.slug}/tt-{n}"
        os.makedirs(f"{work}/photos", exist_ok=True)
        subprocess.run(f"cp -n {long_photos}/* {work}/photos/ 2>/dev/null || true", shell=True)
        sspec = f"{work}/script.json"
        json.dump({"voice": spec.get("voice", "en-US-AndrewNeural"), "rate": spec.get("short_rate", spec.get("rate", "+0%")),
                   "music": spec.get("music"), "style": spec.get("style"),
                   "beats": [b for b in beats if b.get("myth") in ms] + ([] if spec.get("style") == "punch" else [END])},
                  open(sspec, "w"))
        path = f"{out}/tt-{n}.mp4"
        # Render in the work dir and move into the repo only when finished, so a commit never grabs a half-written file.
        if not (a.skip_existing and os.path.exists(path)):
            subprocess.run(["python3", "explainer.py", sspec, work, "build", f"{work}/tt.mp4", "--vertical"], check=True,
                           cwd=os.path.dirname(os.path.abspath(__file__)))
            shutil.move(f"{work}/tt.mp4", path)
        dur = explainer.duration(path)
        quizzes = [b for b in beats if b.get("myth") in ms and "quiz" in b]
        release.append({
            "file": f"{RAW}/{a.slug}/tt-{n}.mp4", "seconds": round(dur, 1), "myths": ms,
            "title": title(quizzes, n),
            "caption": caption(quizzes, n, a.slug),
            "comment": "Comment your score: " + " / ".join(f"{i}. {claim(q)}?" for i, q in enumerate(quizzes, 1)),
        })
        print(f"tt-{n} {dur:.1f}s {ms}" + ("  UNDER 60s" if dur <= 60 else ""))
    json.dump(release, open(f"{out}/tiktok.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
