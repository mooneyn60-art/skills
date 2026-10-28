#!/usr/bin/env python3
"""Build the v2 "nature doc" sound kit in sfx/v2/ (Nolan 10/28: switch away from the cartoon boing/pop kit).

Same names as sfx/ so every spec and macro keeps working; drawn.py reads sfx/v2/ first.
  whoosh  soft cloth swish            tink   soft light tap            pop    leather drop
  boing   soft landing bump           scratch paper flick              thud   soft heavy bump
  hit     light body punch            zap    electric crackle           step   one grass footstep  (no beeps: Nolan 10/28)
  click   short tap (clock ticks)
  splash, crunch, plate, stamp, case: copied from sfx/ unchanged

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
    # Nolan 10/28: no beeps. Every cue is a natural, unpitched foley sound.
    "tink": ("impactGeneric_light_002.ogg", None),
    "pop": ("dropLeather.ogg", None),
    "click": ("impactGeneric_light_000.ogg", "atrim=0:0.15"),
}
SYNTH = {
    # electric crackle: sparse random clicks through a band-pass, no pitch
    "zap": ("aevalsrc=(2*random(0)-1)*gt(random(1)\\,0.82)*exp(-4*t):d=0.5:s=48000", "bandpass=f=2500:w=3000"),
}
KEEP = ["splash", "crunch", "plate", "stamp", "case"]


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
