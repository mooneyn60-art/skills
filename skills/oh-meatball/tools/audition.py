#!/usr/bin/env python3
"""Voice audition for the cutout cast (Nolan 11/19: "voices a little better for each person", "different
accents"). Three candidates per character (A = the current voice), each saying that character's best v4 line.
No pitch / formant / autotune: differences come from Kokoro voice choice, blends, speed and punctuation.

  python3 tools/audition.py OUT_DIR      -> OUT_DIR/voice-audition.mp4 + OUT_DIR/voice-audition/*.mp3
"""
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout as C  # noqa: E402
import free_voice as fv  # noqa: E402

SR = 44100
CAST = [  # (character, key, line, [(letter, voice spec, note, say-override)])
    ("MEATBALL", "meatball", "There it is. Seventy-five inches. Ninety-nine dollars. Probably made of cardboard and "
     "child tears. I don't give a crap.",
     [("A", "kokoro:adam-puck@speed=1.36", "current: am_adam 0.6 + am_puck 0.4, American", None),
      ("B", "kokoro:aud-mb-b@speed=1.3,pause=0.18", "am_puck, younger American kid", None),
      ("C", "kokoro:aud-mb-c@speed=1.25,pause=0.18", "bm_fable 0.6 + am_puck 0.4, British smartass", None)]),
    ("PIP", "pip", "Holy shit! A grandma just body-slammed me!",
     [("A", "kokoro:pip@speed=1.34,pause=0.16", "current: am_puck 0.6 + af_sky 0.4, American", None),
      ("B", "kokoro:aud-pip-b@speed=1.42,pause=0.14", "am_puck 0.4 + af_bella 0.6, higher, faster", None),
      ("C", "kokoro:aud-pip-c@speed=1.4,pause=0.14", "bf_lily 0.5 + am_puck 0.5, British-ish nervous", None)]),
    ("DOT", "dot", "That's not a sale, you jackass. That's a hostage situation with coupons.",
     [("A", "kokoro:dot@speed=1.2,pause=0.16", "current: af_sky 0.5 + af_river 0.5, American", None),
      ("B", "kokoro:aud-dot-b@speed=1.1,pause=0.3", "af_nicole 0.7 + af_river 0.3, breathy bored", None),
      ("C", "kokoro:aud-dot-c@speed=1.1,pause=0.3", "bf_emma 0.7 + af_river 0.3, dry British", None)]),
    ("GRANDMA", "grandma", "Back off, you little shit. I've been training since July and I have nothing left to "
     "lose.",
     [("A", "kokoro:grandma@speed=1.18,pause=0.16", "current: bf_isabella 0.6 + af_heart 0.4", None),
      ("B", "kokoro:aud-gran-b@speed=1.05,pause=0.3", "bf_alice, British, older", None),
      ("C", "kokoro:aud-gran-c@speed=1.0,pause=0.4", "bf_emma 0.5 + bf_isabella 0.5, British, sweet then scary "
       "(pauses)", "Back off... you little shit. I've been training since July. And I have nothing. Left. To lose.")]),
    ("CEO", "ceo", "Welcome, shoppers! We raised every price forty percent last week, so today's sixty percent off "
     "is a gift from my heart.",
     [("A", "kokoro:ceo@speed=1.3,pause=0.16", "current: am_michael 0.5 + bm_lewis 0.5", None),
      ("B", "kokoro:aud-ceo-b@speed=1.15,pause=0.25", "bm_george 0.7 + bm_lewis 0.3, posh British", None),
      ("C", "kokoro:aud-ceo-c@speed=1.2,pause=0.25", "am_onyx 0.5 + am_eric 0.5, deep American announcer", None)]),
    ("SELF-CHECKOUT", "robot", "Please... wait... for an associate.",
     [("A", "kokoro:kiosk@speed=1.0,pause=0.15", "current: am_echo 0.6 + bm_george 0.4", None),
      ("B", "kokoro:aud-bot-b@speed=0.9,pause=0.3", "bm_daniel, flat British machine", None),
      ("C", "kokoro:aud-bot-c@speed=0.92,pause=0.35", "am_echo 0.5 + af_alloy 0.5, monotone, word by word",
       "Please. Wait. For. An. Associate.")]),
]
GAP = 2.0


def card(name, letter, note, line, W=1080, H=1920):
    img = Image.new("RGBA", (W, H))
    rng = np.random.default_rng(1)
    C.paper(img, [(-20, -20), (W + 20, -20), (W + 20, H + 20), (-20, H + 20)], (36, 40, 70), rng, 1.0,
            shadow=False, jitter=False, edge=False)
    C.paper(img, [(60, 300), (W - 60, 290), (W - 50, 1500), (70, 1510)], (246, 240, 226), rng, 1.5, sh=10)
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(C.FONT, 120 if len(name) < 10 else 92)
    d.text((W / 2, 520), name, font=big, fill=C.INK, anchor="mm")
    d.text((W / 2, 760), letter, font=ImageFont.truetype(C.FONT, 300), fill=(200, 40, 32), anchor="mm")
    f = ImageFont.truetype(C.FONT.replace("Black", "Bold"), 40)
    y = 980
    for chunk in wrap(note, f, W - 200):
        d.text((W / 2, y), chunk, font=f, fill=(60, 60, 70), anchor="mm")
        y += 52
    f2 = ImageFont.truetype(C.FONT.replace("Black", "Bold"), 46)
    y += 40
    for chunk in wrap('"' + line + '"', f2, W - 200):
        d.text((W / 2, y), chunk, font=f2, fill=C.INK, anchor="mm")
        y += 60
    d.text((W / 2, 200), "VOICE AUDITION", font=ImageFont.truetype(C.FONT, 70), fill=(252, 214, 74), anchor="mm")
    return img.convert("RGB")


def wrap(text, font, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font.getlength(t) > width and cur:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def main(out_dir):
    tmp = "/dev/shm/cutout/audition"
    os.makedirs(tmp, exist_ok=True)
    mp3_dir = os.path.join(out_dir, "voice-audition")
    os.makedirs(mp3_dir, exist_ok=True)
    audio, concat, listing = [], [], []
    for name, key, line, cands in CAST:
        for letter, spec, note, say in cands:
            mp3 = fv.make(spec, say or line)
            shutil.copy(mp3, os.path.join(mp3_dir, f"{key}-{letter}.mp3"))
            a = C.load_audio(mp3)
            seg = np.concatenate([np.zeros(int(0.4 * SR), np.float32), a, np.zeros(int(GAP * SR), np.float32)])
            audio.append(seg)
            png = f"{tmp}/{key}-{letter}.png"
            card(f"{name} - {letter}", letter, f"{spec.split(':', 1)[1]}  ({note})", say or line).save(png)
            concat.append(f"file '{png}'\nduration {len(seg) / SR:.3f}")
            listing.append(f"{name} {letter}: {spec}  ({note}){' say: ' + say if say else ''}")
    concat.append(f"file '{png}'")
    open(f"{tmp}/list.txt", "w").write("\n".join(concat) + "\n")
    import soundfile as sf
    sf.write(f"{tmp}/aud.wav", np.concatenate(audio), SR)
    out = os.path.join(out_dir, "voice-audition.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-i",
                    f"{tmp}/aud.wav", "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    open(os.path.join(mp3_dir, "LIST.txt"), "w").write("\n".join(listing) + "\n")
    print("\n".join(listing))
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
