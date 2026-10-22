#!/usr/bin/env python3
"""Illustrated explainer builder (Kelevin-style): beats JSON -> cartoon images + voiceover -> 1080p video.

Beats JSON: {"voice": "en-US-AndrewNeural", "beats": [{"say": "...", "img": "prompt"}, ...]}
Stages (re-runnable, cached in WORKDIR):
  images  explainer.py beats.json WORKDIR images [--seeds 2]   -> img/NN_sK.png candidates
  build   explainer.py beats.json WORKDIR build OUT.mp4 [--pick picks.json]
picks.json maps beat index -> chosen seed (default seed 0).
"""
import argparse
import asyncio
import json
import os
import random
import subprocess

STYLE = (", flat 2D cartoon illustration, thick black outlines, bold flat colors, simple shapes, "
         "webcomic style, one single subject, clean plain background")
MODEL = os.environ.get("SDTURBO", "/tmp/claude-0/-home-user/f2581a8c-fe42-5876-b5f9-d941a863a7fa/scratchpad/models/sdturbo")
W, H, FPS = 1920, 1080, 30


def images(beats, work, seeds):
    import torch
    from diffusers import AutoPipelineForText2Image
    torch.set_num_threads(os.cpu_count())
    pipe = AutoPipelineForText2Image.from_pretrained(MODEL, torch_dtype=torch.float32, variant="fp16")
    os.makedirs(f"{work}/img", exist_ok=True)
    for i, b in enumerate(beats):
        for s in range(seeds):
            path = f"{work}/img/{i:02d}_s{s}.png"
            if os.path.exists(path):
                continue
            g = torch.Generator().manual_seed(1000 * i + s)
            pipe(b["img"] + STYLE, num_inference_steps=3, guidance_scale=0.0, width=768, height=448,
                 generator=g).images[0].save(path)
            print("img", path, flush=True)


def voice(beats, work, name):
    from facts import speak  # reuse the proxy-aware, retrying TTS
    os.makedirs(f"{work}/vo", exist_ok=True)
    for i, b in enumerate(beats):
        mp3 = f"{work}/vo/{i:02d}.mp3"
        if not os.path.exists(mp3):
            asyncio.run(speak(b["say"], name, mp3))


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 path], capture_output=True, text=True, check=True).stdout)


def build(beats, work, out, picks, name):
    voice(beats, work, name)
    segs = []
    for i, _ in enumerate(beats):
        img, mp3, seg = f"{work}/img/{i:02d}_s{picks.get(str(i), 0)}.png", f"{work}/vo/{i:02d}.mp3", f"{work}/seg{i:02d}.mp4"
        dur = duration(mp3) + 0.35
        frames = int(dur * FPS)
        # Slow Ken Burns: alternate zoom-in / zoom-out so consecutive beats don't feel identical.
        z = "min(1.0+0.0009*on,1.12)" if i % 2 == 0 else "max(1.12-0.0009*on,1.0)"
        vf = (f"scale={W*2}:{H*2}:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d={frames}:s={W}x{H}:fps={FPS},format=yuv420p")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", img, "-i", mp3,
                        "-vf", vf, "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-af", "apad", seg], check=True)
        segs.append(seg)
    lst = f"{work}/list.txt"
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "loudnorm=I=-14:TP=-1.5", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], check=True)
    print(f"ok {out} {duration(out):.1f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("beats")
    ap.add_argument("work")
    ap.add_argument("stage", choices=["images", "build"])
    ap.add_argument("out", nargs="?")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--pick")
    a = ap.parse_args()
    spec = json.load(open(a.beats))
    if a.stage == "images":
        images(spec["beats"], a.work, a.seeds)
    else:
        picks = json.load(open(a.pick)) if a.pick else {}
        build(spec["beats"], a.work, a.out, picks, spec.get("voice", "en-US-AndrewNeural"))


if __name__ == "__main__":
    random.seed(0)
    main()
