#!/usr/bin/env python3
"""Drawn long-form: stitch finished drawn cuts (9:16) into one 16:9 YouTube video with chapters.

Each segment is centred on a 1920x1080 canvas over a soft, blurred, darkened copy of itself (no text, no pop-ups).
A short whoosh-free crossfade joins segments; the segments' own "Subscribe. Next, ..." teases act as the bridges,
so order the list so each tease points at the next segment.

Usage:
  drawn_compile.py OUT.mp4 --title "Things Living In Your House (All 6 Parts)" \
      --seg "A 30-Legged Hunter Lives in Your House=episodes/drawn-house/tt-house-centipede.mp4" ...
  Writes OUT.mp4 and OUT.chapters.txt (YouTube chapter lines, first at 0:00).
"""
import argparse
import os
import subprocess
import tempfile

FADE = 0.4


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout.strip())


def landscape(src, dst):
    vf = ("[0:v]split=2[a][b];"
          "[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.18[bg];"
          "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", vf, "-map", "[v]", "-map", "0:a",
                    "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                    "-ar", "48000", "-ac", "2", dst], check=True)


def stamp(t):
    t = int(round(t))
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seg", action="append", required=True, help="Chapter title=path/to/cut.mp4")
    ap.add_argument("--title", default="")
    a = ap.parse_args()
    segs = [s.split("=", 1) for s in a.seg]
    work = tempfile.mkdtemp(prefix="compile-", dir=os.environ.get("DRAWN_WORK", "/tmp"))
    parts, chapters, t = [], [], 0.0
    for i, (name, path) in enumerate(segs):
        p = os.path.join(work, f"s{i:03d}.mp4")
        landscape(path, p)
        parts.append(p)
        chapters.append(f"{stamp(t)} {name}")
        t += dur(p) - (FADE if i < len(segs) - 1 else 0)
        print(f"  {stamp(t)}  {name}", flush=True)
    # chain crossfades (video) + acrossfades (audio)
    inputs, fc, v, au = [], [], "[0:v]", "[0:a]"
    off = 0.0
    for i, p in enumerate(parts):
        inputs += ["-i", p]
    for i in range(1, len(parts)):
        off += dur(parts[i - 1]) - FADE
        fc.append(f"{v}[{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{i}]")
        fc.append(f"{au}[{i}:a]acrossfade=d={FADE}[a{i}]")
        v, au = f"[v{i}]", f"[a{i}]"
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
    if fc:
        cmd += ["-filter_complex", ";".join(fc), "-map", v, "-map", au]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    with open(os.path.splitext(a.out)[0] + ".chapters.txt", "w") as f:
        f.write("\n".join(chapters) + "\n")
    subprocess.run(["rm", "-rf", work])
    print(f"done {a.out}  {stamp(dur(a.out))}  ({len(segs)} segments)")


if __name__ == "__main__":
    main()
