#!/usr/bin/env python3
"""Build the v2 "nature doc" sound kit in sfx/v2/ (Nolan 10/28: switch away from the cartoon boing/pop kit).

Same names as sfx/ so every spec and macro keeps working; drawn.py reads sfx/v2/ first.
  whoosh  soft cloth swish            tink   warm kalimba pluck        pop    wooden marimba knock
  boing   soft landing bump           scratch paper flick              thud   soft heavy bump
  hit     light body punch            zap    gentle shimmer sweep       step   one grass footstep
  splash, click, crunch, plate, stamp, case: copied from sfx/ unchanged

Usage: make_sfx2.py KENNEY_DIR   (unzipped Kenney CC0 packs: "RPG Audio", "Impact Sounds", "Interface Sounds";
       only .ogg files are read, nothing in it is run)
"""
import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(HERE, "..", "sfx")
OUT = os.path.join(SFX, "v2")
TMP = "/tmp/_sfx2.wav"

KENNEY = {  # name -> (file, extra filter chain)
    "whoosh": ("cloth2.ogg", "highpass=f=200,afade=t=out:st=0.25:d=0.2"),
    "boing": ("impactSoft_medium_001.ogg", None),
    "scratch": ("bookFlip2.ogg", None),
    "thud": ("impactSoft_heavy_002.ogg", None),
    "hit": ("impactPunch_medium_002.ogg", "lowpass=f=4000"),
    "step": ("footstep_grass_001.ogg", None),
}
SYNTH = {
    # kalimba: two partials with fast decay, slight detune
    "tink": ("aevalsrc=0.55*sin(2*PI*880*t)*exp(-9*t)+0.2*sin(2*PI*2640*t)*exp(-20*t)+0.08*sin(2*PI*5300*t)*exp(-40*t)"
             ":d=0.6:s=48000", None),
    # marimba knock: low fundamental + hollow 4th harmonic
    "pop": ("aevalsrc=0.7*sin(2*PI*523*t)*exp(-14*t)+0.3*sin(2*PI*2092*t)*exp(-30*t):d=0.35:s=48000", None),
    # shimmer: rising soft sine cluster
    "zap": ("aevalsrc=0.25*(sin(2*PI*(700*t+500*t*t))+sin(2*PI*(1050*t+750*t*t))+sin(2*PI*(1400*t+900*t*t)))"
            "*sin(PI*t/0.7):d=0.7:s=48000", "lowpass=f=5000"),
}
KEEP = ["splash", "click", "crunch", "plate", "stamp", "case"]


def norm(args, out, chain=None, peak=-6):
    af = (chain + "," if chain else "") + "aformat=sample_rates=48000:channel_layouts=stereo"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args, "-af", af, TMP], check=True)
    s = subprocess.run(["ffmpeg", "-i", TMP, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mx = float(s.split("max_volume: ")[1].split(" dB")[0])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", TMP, "-af", f"volume={peak - mx}dB", "-c:a", "pcm_s16le", out],
                   check=True)


def main():
    kdir = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    for name, (fn, chain) in KENNEY.items():
        hit = glob.glob(f"{kdir}/**/{fn}", recursive=True)
        if not hit:
            raise SystemExit(f"missing {fn} in {kdir}")
        norm(["-i", hit[0]], f"{OUT}/{name}.wav", chain)
    for name, (src, chain) in SYNTH.items():
        norm(["-f", "lavfi", "-i", src], f"{OUT}/{name}.wav", chain)
    for name in KEEP:
        shutil.copy(os.path.join(SFX, name + ".wav"), os.path.join(OUT, name + ".wav"))
    print("ok", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
