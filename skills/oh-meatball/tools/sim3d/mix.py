#!/usr/bin/env python3
"""Mux a rendered (silent) sim3d video with a music bed and optional voice lines.
mix.py VIDEO MUSIC.wav OUT.mp4 [--vo vo.json] [--dur SECONDS] [--music-db -4] [--duck-db -8]
vo.json: [{"t": start_s, "mp3": path}, ...]. Music is ducked under each line, faded at the end."""
import argparse
import json
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("music"); ap.add_argument("out")
ap.add_argument("--vo"); ap.add_argument("--dur", type=float)
ap.add_argument("--music-db", type=float, default=-3.0); ap.add_argument("--duck-db", type=float, default=-9.0)
ap.add_argument("--vo-lead", type=float, default=0.25)
a = ap.parse_args()
dur = a.dur or float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                                   capture_output=True, text=True, check=True).stdout)
inputs = ["-i", a.video, "-i", a.music]
lines = json.load(open(a.vo)) if a.vo else []
for l in lines:
    inputs += ["-i", l["mp3"]]
duck = ""
if lines:
    expr = "+".join(f"between(t,{l['t'] + a.vo_lead - 0.15:.2f},{l['t'] + a.vo_lead + l['dur'] + 0.2:.2f})" for l in lines)
    duck = f",volume='if({expr},{10 ** (a.duck_db / 20):.3f},1)':eval=frame"
fc = [f"[1:a]atrim=0:{dur},volume={10 ** (a.music_db / 20):.3f}{duck},afade=t=out:st={dur - 1.5}:d=1.5[m]"]
mixin = "[m]"
for i, l in enumerate(lines):
    ms = int((l["t"] + a.vo_lead) * 1000)
    fc.append(f"[{i + 2}:a]aresample=48000,adelay={ms}|{ms},volume=1.6[v{i}]")
    mixin += f"[v{i}]"
fc.append(f"{mixin}amix=inputs={len(lines) + 1}:normalize=0,alimiter=limit=0.89:level=0,aresample=48000[aout]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur}", "-movflags", "+faststart", a.out], check=True)
print("ok", a.out)
