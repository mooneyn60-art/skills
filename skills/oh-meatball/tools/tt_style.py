#!/usr/bin/env python3
"""TikTok style layer for finished drawn cuts (Nolan 10/28: "push TikTok hard ... a style change TikTok might like").

The 60 s+ animated TikTok outliers (vidIQ outlier search 10/28: "Worst Mating Rituals In Animal Kingdom" 2.5M from a
13.6K account, "Your Pet Doesn't See You as a Human" 3.3M, cartoon T. rex 1.6M) all keep the topic as a big title on
screen from frame 0, often with "Part N", and many are LISTS across several animals. Ours had neither.

  header  IN OUT --title "THE BUG IN YOUR BED" [--sub "PART 7"]
          burns a title bar across the top of a finished cut, for the whole video.
  listify OUT --title "ANIMALS THAT CHEAT DEATH" SPEC_JSON:MP4 [SPEC_JSON:MP4 ...]
          trims each drawn Short before its "Subscribe. Next, ..." tease, numbers it (#1, #2 ...) under the title
          and joins them into one TikTok (aim for 61-120 s).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT = os.path.join(ROOT, "brand/fonts/Anton-Regular.ttf")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def fit(title, size=84, width=1000):
    """Largest font size (<= size) at which the title fits the frame width."""
    from PIL import ImageFont
    while size > 40 and ImageFont.truetype(FONT, size).getlength(title) > width:
        size -= 2
    return size


def title_for(outline):
    """(title, sub) for a drawn outline: data/tt_headers.json by slug; house parts get "PART N"."""
    heads = json.load(open(os.path.join(ROOT, "data/tt_headers.json")))
    slug = outline["slug"].replace("-tiny", "")
    sub = f'PART {outline["part"]}' if outline.get("part") else None
    if sub and outline.get("series", "").lower() == "things living in your house":   # numbered series badge (10/28)
        sub = f'THINGS LIVING IN YOUR HOUSE #{outline["part"]}'
    return heads.get(slug), sub


def bar(title, sub=None):
    """drawtext filters for the top title bar (inside TikTok's safe area: below the status bar, above the caption)."""
    fs = fit(title)
    f = [f"drawbox=x=0:y=150:w=iw:h={250 if sub else 190}:color=black@0.55:t=fill",
         f"drawtext=fontfile={FONT}:text='{esc(title)}':fontcolor=white:fontsize={fs}:x=(w-tw)/2:y={175 + (84 - fs) // 2}:"
         "borderw=6:bordercolor=black"]
    if sub:
        ss = fit(sub, 52 if "#" in sub else 60, 960)   # the series badge is smaller, on one line
        f.append(f"drawtext=fontfile={FONT}:text='{esc(sub)}':fontcolor=#ffd34d:fontsize={ss}:x=(w-tw)/2:y={278 + (60 - ss) // 2}:"
                 "borderw=5:bordercolor=black")
    return ",".join(f)


def header(src, out, title, sub=None):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", bar(title, sub), "-c:v", "libx264", "-preset",
                    "veryfast", "-crf", "20", "-c:a", "copy", "-movflags", "+faststart", out], check=True)


def tease_start(spec_path):
    """Seconds into the cut where the closing tease beat starts (from the same TTS plan the render used)."""
    sys.path.insert(0, HERE)
    import drawn
    spec = drawn.drawn_macros.expand(json.load(open(spec_path)))
    work = tempfile.mkdtemp(prefix="tt-", dir=os.environ.get("DRAWN_WORK", "/tmp"))
    beats, _ = drawn.plan(spec, work)
    subprocess.run(["rm", "-rf", work])
    return beats[-1]["t0"]


def listify(out, title, items):
    work = tempfile.mkdtemp(prefix="ttl-", dir=os.environ.get("DRAWN_WORK", "/tmp"))
    parts = []
    for k, it in enumerate(items, 1):
        spec, mp4 = it.split(":", 1)
        end = tease_start(spec)
        p = os.path.join(work, f"p{k}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-t", f"{end:.2f}", "-vf",
                        bar(title, f"#{k}"), "-af", f"afade=t=out:st={end - 0.25:.2f}:d=0.25",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                        "-ar", "48000", p], check=True)
        parts.append(p)
        print(f"  #{k} {os.path.basename(mp4)}  {end:.1f} s", flush=True)
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", out], check=True)
    subprocess.run(["rm", "-rf", work])


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    h = sp.add_parser("header")
    h.add_argument("src")
    h.add_argument("out")
    h.add_argument("--title", required=True)
    h.add_argument("--sub")
    li = sp.add_parser("listify")
    li.add_argument("out")
    li.add_argument("--title", required=True)
    li.add_argument("items", nargs="+", help="SPEC_JSON:MP4 per animal, in list order")
    a = ap.parse_args()
    if a.cmd == "header":
        header(a.src, a.out, a.title, a.sub)
    else:
        listify(a.out, a.title, a.items)
    print("done", a.out)


if __name__ == "__main__":
    main()
