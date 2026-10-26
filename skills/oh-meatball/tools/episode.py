#!/usr/bin/env python3
"""One command from episode script to upload-ready release: long-form + one quiz Short per myth,
chapters, photo credits, titles, tags and a release.json the scheduler posts from.

Usage: episode.py SCRIPT.json SLUG [--work DIR] [--skip-long] [--skip-shorts] [--skip-existing]
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
import openloop
import retention
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


def loop(beats):
    """Seamless Short loop: open claim-first ("Porcupines can shoot their quills. True or false?") and end on
    the same quiz card with a line that runs straight into it ("So be honest... did you really think"),
    so a replay sounds like one sentence and the last frame matches the first."""
    q = beats[0]
    first = dict(q, say=f"{claim(q)}. True or false?")
    # Rotate the bridge line per myth so Shorts don't all end the same way (research/30: templated sameness).
    lines = ["So be honest. Did you really think", "And yet half the internet still swears that",
             "Next time someone tells you that", "Tell me you didn't believe that", "Somebody out there still thinks"]
    # A quiz beat's "loop_say" replaces the rotated line (it must still run straight into the claim).
    tail = {"say": q.get("loop_say") or lines[sum(map(ord, q.get("myth") or "")) % len(lines)], "quiz": q["quiz"],
            "pose": q.get("pose", "think"), "myth": q.get("myth"), "nocount": True, "loop": True}
    return [first] + beats[1:] + [tail]


def hook_loop(beats):
    """Shorts v2 (research/38): no quiz card or countdown. The myth opens on its "hook" beat, a moving
    full-frame photo with the claim stated as a fact, and ends on a "loop" beat that shows the hook's
    first picture (the zoom ends where frame 0 starts) while saying the hook's "loop_say", a line that
    runs straight into the opening sentence."""
    h = beats[0]
    first = explainer.shots(h)[0]
    tail = {"say": h["loop_say"], "pose": h.get("pose", "deadpan"), "myth": h.get("myth"), "loop": True,
            **({"sfx": h["loop_sfx"]} if h.get("loop_sfx") else {}),
            "bleed": h.get("bleed"), "shots": [{k: v for k, v in first.items() if k in explainer.VISUAL}]}
    return beats + [tail]


def credit_lines(work, beats):
    by = collections.OrderedDict()
    for b in (v for x in beats for v in explainer.shots(x)):  # multi-shot beats credit every picture
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
    """Start time of each myth, from the rendered segment list (countdown segments included), or, for a
    v3/v4 long-form ("aspect": "16:9"), from tools/v3.py's timeline.json."""
    if os.path.exists(f"{work}/timeline.json") and not os.path.exists(f"{work}/list.txt"):
        out = collections.OrderedDict()
        for e in json.load(open(f"{work}/timeline.json")):
            b = beats[e["i"]]
            if b.get("chapter") or not out:
                out.setdefault(b.get("chapter") or "Cold open", e["start"])
        return [f"{int(v // 60)}:{int(v % 60):02d} {k}" for k, v in out.items()]
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
    ap.add_argument("--skip-existing", action="store_true", help="keep Shorts already rendered (resume after a stop)")
    ap.add_argument("--no-openloop", action="store_true", help="skip the deep-dive open-loop gate (old packs only)")
    ap.add_argument("--no-retention", action="store_true", help="skip the long-form retention gate (old episodes only)")
    a = ap.parse_args()
    spec = json.load(open(a.script))
    # Deep dives (61-75 s) must promise something at 0:02 and pay it off at 50-80% (research/40, openloop.py).
    bad = [r for r in openloop.check(spec) if r["fails"]]
    if bad and not a.no_openloop:
        for r in bad:
            print(f"OPENLOOP FAIL {r['myth']}: " + "; ".join(r["fails"]))
        raise SystemExit("deep dive(s) fail tools/openloop.py; fix the script or pass --no-openloop for an old pack")
    # Story long-forms (16:9) must hook, loop, count and save the best for last (research/47, retention.py).
    if retention.is_long(spec) and not a.skip_long:
        rep = retention.check(spec)
        for w in rep["warns"]:
            print(f"RETENTION WARN: {w}")
        if rep["fails"] and not a.no_retention:
            for f in rep["fails"]:
                print(f"RETENTION FAIL: {f}")
            raise SystemExit("long-form fails tools/retention.py; fix the script or pass --no-retention for an old episode")
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
    # Shorts-only packs (originals-*) have no long-form, so no chapters or long release entry.
    built = any(os.path.exists(f"{long_work}/{f}") for f in ("list.txt", "timeline.json"))
    release["long"] = None if not built else {
        "file": f"{RAW}/{a.slug}/ep.mp4", "thumb": f"{RAW}/{a.slug}/thumb.jpg", "title": spec["title"],
        "tags": spec.get("tags", []), "comment": spec.get("pinned", ""),
        "description": "\n".join([spec.get("blurb", ""), ""] + chapters(long_work, beats) + [
            "", spec.get("next", ""), "", f"Wildlife photos from iNaturalist, used under their licenses ({LICENSES}):"]
            + credits + ["", spec.get("hashtags", "#animalfacts #trueorfalse #quiz #mythbusting #animals")]),
    }

    for m in myths:
        mb = [b for b in beats if b.get("myth") == m]
        q = next((b for b in mb if "quiz" in b), None)
        # A hook without "loop_say" is a story cold open, not a Short (Explains-03 crashed on it, 10/25).
        hook = mb[0] if mb and mb[0].get("hook") and mb[0].get("loop_say") else None
        if q is None and hook is None:  # story chapters with no quiz don't make a standalone Short
            continue
        swork = f"{a.work}/{a.slug}/short-{m}"
        sspec = f"{swork}/script.json"
        os.makedirs(swork, exist_ok=True)
        # Breakout single-myth Shorts run 17-30 s (vidIQ outliers, 10/23): claim, reveal, punchline, loop line.
        json.dump({"voice": spec.get("voice", "en-US-AndrewNeural"), "rate": spec.get("short_rate", "+8%"),
                   "music": spec.get("music"), "style": spec.get("style"),
                   **({"pitch": spec["pitch"]} if spec.get("pitch") else {}),
                   **({"tempo": spec["tempo"]} if spec.get("tempo") else {}),  # v3: atempo speed-up
                   **({"subjects": spec["subjects"]} if spec.get("subjects") else {}),  # v4: per-photo pins
                   # Meatball Investigates (research/48): series card (hook "case" sets the number), bold
                   # captions, and a generated music bed (hook "music" picks it per Short)
                   **({"series": dict(spec["series"], **({"case": hook["case"]} if hook and hook.get("case") else {}))}
                      if spec.get("series") else {}),
                   **({"captions": spec["captions"]} if spec.get("captions") else {}),
                   **({"music": hook["music"]} if hook and hook.get("music") else {}),
                   # "short_beats" lets a joke-dense script keep more than 3 hand-picked beats (default 3).
                   "beats": hook_loop(mb) if hook else loop(tighten(mb, spec.get("short_beats", 3)))},
                  open(sspec, "w"))
        if not a.skip_shorts and not (a.skip_existing and os.path.exists(f"{out}/short-{m}.mp4")):
            os.makedirs(f"{swork}/photos", exist_ok=True)
            subprocess.run(f"cp -n {long_work}/photos/* {swork}/photos/ 2>/dev/null || true", shell=True)
            run_build(sspec, swork, f"{swork}/short.mp4", vertical=True)
            shutil.move(f"{swork}/short.mp4", f"{out}/short-{m}.mp4")  # never expose a half-written file to git
        if hook:  # v2: a statement, not a quiz, so the title/description/comment are not quiz-shaped
            release["shorts"].append({
                "myth": m, "file": f"{RAW}/{a.slug}/short-{m}.mp4", "title": hook.get("short_title", hook["say"])[:100],
                "description": f"{hook['say']} {hook.get('bonus', '')}\n\n"
                               + spec.get("short_hashtags", "#shorts #animalfacts #meatballmyths") + "\n\n"
                               + f"Photos ({spec.get('photo_source', 'iNaturalist')}), cropped and color-adjusted: " + "; ".join(credit_lines(long_work, mb))
                               + f". {LICENSES}",
                "comment": hook.get("comment", "Who told you the opposite? 👇"),
                "tags": [m, "animal facts", "animal myths", "fun facts", "shorts", "Meatball Myths"],
            })
            continue
        c = claim(q)
        release["shorts"].append({
            "myth": m, "file": f"{RAW}/{a.slug}/short-{m}.mp4",
            # The question people search ("Can Porcupines Really Shoot Their Quills?"): search is our 2nd source.
            "title": (q.get("short_title") or f"{c}? 🤔 TRUE or FALSE")[:100],
            "description": f"TRUE or FALSE? {c}. Guess before the timer, then comment if you got it right 👇 "
                           + (f"\n\nBonus fact: {q['bonus']}" if q.get("bonus") else "")
                           + f"\n\nFull quiz episode on the channel.\n\n#shorts #trueorfalse #animalfacts #quiz\n\n"
                           f"Photos (iNaturalist), cropped and color-adjusted: " + "; ".join(credit_lines(long_work, mb))
                           + f". {LICENSES}",
            "comment": (f"{q['bonus']}\n\n" if q.get("bonus") else "") + "Did you guess right? Comment ✅ TRUE or ❌ FALSE 👇",
            "tags": [m, "true or false", "animal quiz", "animal facts", "animal myths", "fun facts", "shorts",
                     "Meatball Myths"],
        })
    json.dump(release, open(f"{out}/release.json", "w"), indent=1, ensure_ascii=False)
    print(f"ok {out} long={'skipped' if a.skip_long else 'built'} shorts={len(release['shorts'])}")


if __name__ == "__main__":
    main()
