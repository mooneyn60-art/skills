#!/usr/bin/env python3
"""Build the v2 "nature doc" sound kit in sfx/v2/ (Nolan 10/28: switch away from the cartoon boing/pop kit).

Same names as sfx/ so every spec and macro keeps working; drawn.py reads sfx/v2/ first.
  whoosh  soft cloth swish            tink   soft light tap            pop    leather drop
  boing   soft landing bump           scratch paper flick              thud   soft heavy bump
  hit     light body punch            zap    electric crackle (unused: too sharp)           step   one grass footstep  (no beeps: Nolan 10/28)
  click   short tap (clock ticks)      sting  the series' signature cue (synthesised: low whoomp + warm pluck)
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
# Nolan 10/28 "get rid of the loud beeps, make it softer": the sharp cues are low-passed to 3 kHz, given a 5 ms
# attack and a fade over their second half, and sit 8 dB under the others. zap stays in the kit but nothing uses it.
SOFT = ["tink", "click", "hit", "scratch"]


def soften(path):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout)
    af = f"lowpass=f=3000,lowpass=f=3000,afade=t=in:d=0.005,afade=t=out:st={d / 2:.3f}:d={d / 2:.3f},volume=-8dB"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-af", af, "-c:a", "pcm_s16le", TMP], check=True)
    shutil.move(TMP, path)


def norm(args, out, chain=None, peak=-6):
    af = (chain + "," if chain else "") + "aformat=sample_rates=48000:channel_layouts=stereo"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args, "-af", af, TMP], check=True)
    s = subprocess.run(["ffmpeg", "-i", TMP, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mx = float(s.split("max_volume: ")[1].split(" dB")[0])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", TMP, "-af", f"volume={peak - mx}dB", "-c:a", "pcm_s16le", out],
                   check=True)


def sting(out, sr=48000):
    """The series' signature cue (YouTube Studio 10/28: viewers don't recognise the channel; a recurring sound):
    0.5 s, a soft low "whoomp" (a sine falling 140 -> 55 Hz) under a warm, low-passed pluck (G3 with a soft fifth).
    No beep: nothing above ~2 kHz, gentle 8 ms attacks. Same on every video, played under the hook's first word."""
    import numpy as np
    import wave
    n = int(0.5 * sr)
    t = np.arange(n) / sr
    f = 55 + 85 * np.exp(-t / 0.08)
    whoomp = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.minimum(1, t / 0.008) * np.exp(-t / 0.12)
    pk = np.clip((t - 0.04) / 0.008, 0, 1) * np.exp(-np.maximum(0, t - 0.04) / 0.11)
    pluck = sum(a * np.sin(2 * np.pi * hz * t) for hz, a in ((196.0, 1.0), (392.0, 0.35), (293.66, 0.3), (588.0, 0.08))) * pk
    x = 0.9 * whoomp + 0.45 * pluck
    x *= np.minimum(1, (n - np.arange(n)) / (0.06 * sr))   # fade the tail
    x = x / np.abs(x).max() * 10 ** (-6 / 20)
    pcm = (np.repeat(x[:, None], 2, 1) * 32767).astype("<i2")
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


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
    for name in SOFT:
        soften(f"{OUT}/{name}.wav")
    sting(f"{OUT}/sting.wav")
    print("ok", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
