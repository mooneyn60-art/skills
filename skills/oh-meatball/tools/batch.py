#!/usr/bin/env python3
"""Batch: prompts JSON -> self-hosted CPU clip -> ambient audio -> camify -> meta.json.

Each job: {"slug","prompt","preset","label","animal","hook","type"}; optional "seconds" (default 8).
Usage: batch.py jobs.json OUTDIR
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Silent model output gets a quiet bed so the clip doesn't feel dead: brown noise
# (wind/room tone), plus faint cricket-like chirps at night.
AMBIENCE = {
    "night": "anoisesrc=c=brown:a=0.02:d={d},aformat=channel_layouts=stereo[n];"
             "aevalsrc='0.015*sin(2*PI*4400*t)*gt(sin(2*PI*1.5*t),0.85)':d={d}:s=48000,"
             "aformat=channel_layouts=stereo[c];[n][c]amix=inputs=2:normalize=0",
    "day": "anoisesrc=c=pink:a=0.015:d={d},aformat=channel_layouts=stereo",
}


def run(cmd):
    print("+", " ".join(cmd[:3]), "...", flush=True)
    subprocess.run(cmd, check=True)


def main():
    jobs, out = json.load(open(sys.argv[1])), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for j in jobs:
        slug = j["slug"]
        raw, aud, final = (f"{out}/{slug}_{k}.mp4" for k in ("raw", "aud", "cam"))
        if os.path.exists(final):
            continue
        secs = j.get("seconds", 8)
        frames = secs * 12 + 1
        run(["python3", f"{HERE}/gen_cpu.py", j["prompt"], raw, "--frames", str(frames), "--fps", "12"])
        night = j["preset"] == "doorbell_night"
        amb = AMBIENCE["night" if night else "day"].format(d=secs)
        run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-filter_complex", f"{amb}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-shortest", aud])
        run([f"{HERE}/camify.sh", aud, final, j["preset"], j.get("label", "")])
        meta = subprocess.run(["python3", f"{HERE}/meta.py", "--type", j["type"], "--animal", j["animal"],
                               "--hook", j["hook"]], check=True, capture_output=True, text=True).stdout
        open(f"{out}/{slug}_meta.json", "w").write(meta)
        print(f"done {slug}", flush=True)


if __name__ == "__main__":
    main()
