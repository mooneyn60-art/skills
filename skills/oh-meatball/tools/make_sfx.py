#!/usr/bin/env python3
"""Build the Shorts v3 sound-effect kit in sfx/ (48 kHz stereo WAV, peak -3 dBFS).

Usage: make_sfx.py KENNEY_DIR [OUT_DIR]
  KENNEY_DIR  a folder holding the unzipped Kenney CC0 packs (kenney.nl "Impact Sounds",
              "Interface Sounds", "Digital Audio"); only .ogg files are read, nothing in it is run.
  OUT_DIR     default: ../sfx next to this tools/ folder
Kenney sounds are CC0. The rest are synthesized here with ffmpeg (nothing to license).
"""
import glob
import os
import subprocess
import sys

SYNTH = {  # name -> lavfi source (and an optional filter chain)
    "whoosh": ("anoisesrc=d=0.42:c=pink:r=48000:a=0.9",
               "highpass=f=350,lowpass=f=3200,afade=t=in:d=0.22:curve=exp,afade=t=out:st=0.22:d=0.2:curve=exp"),
    "boing": ("aevalsrc=0.8*sin(2*PI*(150*t+300*t*t)+2.4*sin(2*PI*12*t))*exp(-3.2*t):d=0.6:s=48000", None),
    "pop": ("aevalsrc=0.9*sin(2*PI*(280*t+2600*t*t))*exp(-22*t):d=0.13:s=48000", None),
    "scratch": ("aevalsrc=(0.7*sin(2*PI*(160*t+1500*t*t-2600*t*t*t))+0.3*(2*random(0)-1))*(1-t/0.42):d=0.42:s=48000",
                "bandpass=f=1400:w=2200"),
    "splash": ("anoisesrc=d=0.75:c=white:r=48000:a=0.9",
               "highpass=f=250,lowpass=f=2600,afade=t=in:d=0.03,afade=t=out:st=0.05:d=0.7:curve=exp"),
    "tink": ("aevalsrc=0.30*sin(2*PI*2960*t)*exp(-22*t)+0.18*sin(2*PI*4410*t)*exp(-30*t)"
             "+0.10*sin(2*PI*6650*t)*exp(-40*t):d=0.35:s=48000", None),
    "click": ("aevalsrc=0.8*(2*random(0)-1)*exp(-700*t)+0.45*sin(2*PI*1900*t)*exp(-90*t)"
              "+0.5*(2*random(1)-1)*exp(-900*(t-0.055))*gte(t\\,0.055):d=0.12:s=48000", "highpass=f=600"),
}
KENNEY = {  # name -> file inside the packs
    "crunch": "impactPunch_heavy_002.ogg",
    "hit": "impactPunch_medium_001.ogg",
    "thud": "impactSoft_heavy_001.ogg",
    "zap": "zap2.ogg",
    "plate": "impactPlate_light_002.ogg",
}


def norm(src_args, out, chain=None):
    af = (chain + "," if chain else "") + "aformat=sample_rates=48000:channel_layouts=stereo"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + src_args + ["-af", af, "/tmp/_sfx.wav"], check=True)
    peak = subprocess.run(["ffmpeg", "-i", "/tmp/_sfx.wav", "-af", "volumedetect", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    mx = float(peak.split("max_volume: ")[1].split(" dB")[0])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "/tmp/_sfx.wav", "-af", f"volume={-3 - mx}dB",
                    "-c:a", "pcm_s16le", out], check=True)


def main():
    kdir = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sfx")
    os.makedirs(out, exist_ok=True)
    for name, (src, chain) in SYNTH.items():
        norm(["-f", "lavfi", "-i", src], f"{out}/{name}.wav", chain)
    for name, fn in KENNEY.items():
        hit = glob.glob(f"{kdir}/**/{fn}", recursive=True)
        if not hit:
            raise SystemExit(f"missing {fn} in {kdir}")
        norm(["-i", hit[0]], f"{out}/{name}.wav")
    print("ok", out, sorted(os.listdir(out)))


if __name__ == "__main__":
    main()
