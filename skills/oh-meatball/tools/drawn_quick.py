#!/usr/bin/env python3
"""One outline -> both cuts. Writes the YouTube Short (18-24 s) and the TikTok deep cut (61-75 s) specs from ONE
short YAML outline, checks their spoken length, renders both with tools/drawn.py, writes 2 fps contact sheets
and ffprobe-checks every file.

Usage:
  drawn_quick.py OUTLINE.yaml [--no-render] [--only yt|tt] [--force]
  drawn_quick.py --scaffold "silverfish | study | Something older than dinosaurs is eating your books." \
                 --facts facts.txt > outlines/silverfish.yaml      (a starting outline to edit; one fact a line)

Outline (see scripts/drawn-house/outlines/*.yaml):
  slug: silverfish            # file names: <out>/yt-<slug>.mp4, tt-<slug>.mp4; specs <specs>/<slug>-yt.json
  out: episodes/drawn-house   # optional (default episodes/drawn-house); specs: scripts/drawn-house
  series: Things Living In Your House
  part: 4
  title: A Bug Older Than Dinosaurs Is Eating Your Books        # a claim, not a question
  tiktok_caption: "silverfish in my books 😬 ... Would you keep the books? 📚 yes / 🔥 no"
  creature: silverfish        # a drawn_species name (or creature_cfg: {...} for a new animal inline)
  scene: study                # a drawn_habitats kind;  scene_p: {time: night}
  wild: forest_floor          # optional: the habitat for "solo" lines (the creature alone, no Meatball)
  music: mystery
  next: Part five is in your basement.     # the tease, said after "Subscribe."
  next_scene: basement                     # optional: the tease plays in the next part's room
  sources: [...]
  yt:                         # act 1: both cuts.  Each line = {macro: "the line", ...overrides}
    - hook: Something older than dinosaurs is eating your books.
    - name: Silverfish. No wings, and covered in silver scales.
    - fact: It eats starch. Glue, paste, paper.
      with: [booklouse]
  tt:                         # act 2: TikTok only, between act 1 and the tease
    - calm: ...
Macros: hook name fact xray scale count escalate chase calm punch tease solo (see drawn_macros.py).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
MACROS = ("hook", "name", "fact", "xray", "scale", "count", "escalate", "chase", "calm", "punch", "tease", "solo")
YT_RANGE, TT_RANGE = (18.0, 24.0), (61.0, 75.0)


def load(path):
    txt = open(path).read()
    if path.endswith((".yaml", ".yml")):
        import yaml
        return yaml.safe_load(txt)
    return json.loads(txt)


def line(item):
    item = dict(item)
    for m in MACROS:
        if m in item:
            return dict(item, m=m, say=str(item.pop(m)).strip())
    raise SystemExit(f"drawn_quick: line has no macro key ({', '.join(MACROS)}): {item}")


def specs(o):
    stage = {"creature": o["creature"], "scene": o["scene"], "scene_p": o.get("scene_p", {})}
    for k in ("creature_cfg", "hero_p", "s", "actor", "wild", "wild_p"):
        if k in o:
            stage[k] = o[k]
    tease = {"m": "tease", "say": "Subscribe. " + o["next"]}
    if o.get("next_scene"):
        tease["scene"] = o["next_scene"]
        tease["scene_p"] = o.get("next_scene_p", {})
    act1 = [line(x) for x in o["yt"]]
    act2 = [line(x) for x in o.get("tt", [])]
    base = {"series": f'{o.get("series", "")}, Part {o.get("part", "")}'.strip(", "), "sources": o["sources"],
            "photo_credits": [], "voice": o.get("voice", "en-US-AndrewMultilingualNeural"), "rate": o.get("rate", "+12%"),
            "music": o.get("music", "mystery"), "music_db": o.get("music_db", -26), "captions": 66,
            "caption_y": o.get("caption_y", 1640), "stage": stage,
            "_note": "Written by tools/drawn_quick.py from the outline; beats are drawn_macros lines."}
    yt = dict(base, title=o["title"], tiktok_caption=o["tiktok_caption"], beats=act1 + [tease])
    tt = dict(base, title=o.get("tt_title", o["title"]), tiktok_caption=o["tiktok_caption"],
              beats=act1 + act2 + [tease])
    return yt, tt


def spoken_length(spec, work):
    import drawn
    beats, total = drawn.plan(drawn.drawn_macros.expand(spec), work)
    return total


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    kinds = sorted(s["codec_type"] for s in j["streams"])
    return float(j["format"]["duration"]), kinds, os.path.getsize(path) / 1e6


def contact(mp4, jpg):
    dur = probe(mp4)[0]
    rows = int(dur * 2 / 10) + 1
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", f"fps=2,scale=216:384,tile=10x{rows}",
                    "-frames:v", "1", "-q:v", "4", jpg], check=True)


def scaffold(topic, facts):
    name, scene, hook = [x.strip() for x in topic.split("|")]
    fl = [x.strip() for x in open(facts) if x.strip()] if facts else []
    o = {"slug": name.replace("_", "-"), "series": "Things Living In Your House", "part": 0,
         "title": hook.rstrip("."), "tiktok_caption": f"{name.replace('_', ' ')} 😬 ... Would you ...? yes / no",
         "creature": name, "scene": scene, "music": "mystery", "next": "Part N is in your ...",
         "sources": ["SOURCE 1 (name, what it supports, URL)"],
         "yt": [{"hook": hook}] + [{("name" if i == 0 else "fact"): f} for i, f in enumerate(fl[:5])],
         "tt": [{"fact": f} for f in fl[5:]]}
    import yaml
    return yaml.safe_dump(o, sort_keys=False, allow_unicode=True, width=120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outline", nargs="?")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--only", choices=["yt", "tt"])
    ap.add_argument("--force", action="store_true", help="render even if a cut is outside its length range")
    ap.add_argument("--scaffold")
    ap.add_argument("--facts")
    ap.add_argument("--work", default=os.environ.get("DRAWN_WORK", "/tmp/drawn-work"))
    args = ap.parse_args()
    if args.scaffold:
        print(scaffold(args.scaffold, args.facts))
        return
    t0 = time.time()
    o = load(args.outline)
    out_dir = os.path.join(ROOT, o.get("out", "episodes/drawn-house"))
    spec_dir = os.path.join(ROOT, o.get("specs", "scripts/drawn-house"))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(spec_dir, exist_ok=True)
    yt, tt = specs(o)
    ok = True
    report = []
    for cut, spec, rng in (("yt", yt, YT_RANGE), ("tt", tt, TT_RANGE)):
        if args.only and cut != args.only:
            continue
        sp = os.path.join(spec_dir, f'{o["slug"]}-{cut}.json')
        json.dump(spec, open(sp, "w"), indent=1, ensure_ascii=False)
        work = os.path.join(args.work, f'{o["slug"]}-{cut}')
        os.makedirs(work, exist_ok=True)
        L = spoken_length(spec, work)
        fits = rng[0] <= L <= rng[1]
        ok &= fits
        report.append(f"{cut}: {L:.1f} s ({'ok' if fits else 'OUT OF RANGE %g-%g s' % rng})  {sp}")
        print(report[-1], flush=True)
        if not fits and not args.force:
            continue
        if args.no_render:
            continue
        mp4 = os.path.join(out_dir, f'{cut}-{o["slug"]}.mp4')
        tmp = os.path.join(work, f"render-{cut}.mp4")   # rendered and checked outside the repo first
        subprocess.run([sys.executable, os.path.join(HERE, "drawn.py"), sp, tmp, "--work", work], check=True)
        dur, kinds, mb = probe(tmp)
        if kinds != ["audio", "video"] or mb >= 50 or not (rng[0] - 0.5 <= dur <= rng[1] + 0.5):
            raise SystemExit(f"drawn_quick: {tmp} failed the check ({dur:.2f} s, {kinds}, {mb:.1f} MB)")
        shutil.move(tmp, mp4)   # never leave an incomplete mp4 under the real name
        jpg = os.path.join(out_dir, f'{cut}-{o["slug"]}-contact-2fps.jpg')
        contact(mp4, jpg)
        report.append(f"   {mp4}  {dur:.2f} s  {mb:.1f} MB  contact: {jpg}")
        print(report[-1], flush=True)
    print(f"done in {time.time() - t0:.0f} s" + ("" if ok else "  (a cut is out of range: edit the outline)"))
    sys.exit(0 if ok or args.force else 2)


if __name__ == "__main__":
    main()
