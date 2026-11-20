#!/usr/bin/env python3
"""Per-line voice check for a cutout2 render: each scripted line is transcribed (faster-whisper small.en) from
its own time span of the rendered mix and compared with the script. One long pass, or even 10 s windows, drops
whole stretches of these mixes (music bed + sound effects), so this is the check that proves every line is heard.

  python3 tools/linecheck.py --script v5 /dev/shm/cutout/bf-mix-vertical.wav      (the mix render() writes)
  python3 tools/linecheck.py --script v5 episodes/cutout-test/x.mp4               (or the finished video)
Exit code = number of lines under the match threshold (0.6).
"""
import argparse
import difflib
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutout2 as c  # noqa: E402


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n):
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n == 100:
        return "one hundred"
    return str(n)


def norm(s):
    """Lower case, words only; whisper writes "20%" and "$99" where the script says the words."""
    s = s.lower().replace("%", " percent").replace("$", "")
    s = re.sub(r"\d+", lambda m: " " + num_words(m.group()) + " ", s)
    return re.sub(r"[^a-z ]", "", s.replace("-", " ").replace("...", " "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default="v5")
    ap.add_argument("media")
    ap.add_argument("--min", type=float, default=0.6)
    a = ap.parse_args()
    if a.script in ("holy", "holyv4"):   # episode 2 lives in cutout_holy.py
        import cutout_holy
        cutout_holy.use("v4" if a.script == "holyv4" else "short")
    elif a.script.startswith("ep"):   # episodes 3+ live in cutout_eps.py
        import cutout_eps
        cutout_eps.use(a.script[3:] if a.script.startswith("ep-") else a.script)
    else:
        c.use_script(a.script)
    lines, _, _, _ = c.build()
    fd, wav = tempfile.mkstemp(suffix=".wav", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    os.close(fd)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.media, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    audio, sr = sf.read(wav, dtype="float32")
    os.remove(wav)
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    bad = 0
    for i, ln in enumerate(lines):
        x = audio[int(max(0, ln["t0"] - 0.15) * sr):int((ln["start"] + ln["dur"] + 0.25) * sr)]
        heard = " ".join(s.text.strip() for s in m.transcribe(x, language="en", beam_size=5,
                                                              condition_on_previous_text=False)[0])
        said = " ".join(w[2] for w in ln["words"])
        r = difflib.SequenceMatcher(None, norm(said).split(), norm(heard).split()).ratio()
        bad += r < a.min
        print(f"{'OK ' if r >= a.min else 'LOW'} {i + 1:2d} {ln['who']:8s} {r:.2f} | {heard}", flush=True)
    print("lines under %.2f: %d" % (a.min, bad))
    sys.exit(bad)


if __name__ == "__main__":
    main()
