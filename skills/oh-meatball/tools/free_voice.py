#!/usr/bin/env python3
"""Free narrator voice (Kokoro, runs locally) for scripts whose "voice" is "kokoro:<blend>".

Nolan picked blend C, "kokoro:eric-michael", on 10/24 for long-forms and TikTok-only videos (Bill stays on
YouTube Shorts while vidIQ credits last). explainer.voice() calls make() for each line not yet in the shared
cache, so there is no prep step: lines are generated, studio-processed, aligned with faster-whisper and cached
under the same key scheme as premium_voice.py.

Model files: $KOKORO_DIR (default ~/.cache/kokoro) must hold kokoro-v1.0.onnx and voices-v1.0.bin from
github.com/thewh1teagle/kokoro-onnx releases (model-files-v1.0).
"""
import difflib
import json
import os
import subprocess
import sys

import premium_voice as pv

KOKORO_DIR = os.environ.get("KOKORO_DIR", os.path.expanduser("~/.cache/kokoro"))
BLENDS = {  # name -> [(kokoro voice, weight)]; C is Nolan's pick (research/39-voice-tests/kokoro-v2)
    "eric-michael": [("am_eric", 0.5), ("am_michael", 0.5)],
}
SPEED = 1.05
# Warmth, presence, de-harsh, gentle compression, a touch of room, broadcast loudness.
CHAIN = ("highpass=f=70,equalizer=f=180:t=q:w=1:g=3,equalizer=f=3200:t=q:w=1.2:g=2.5,"
         "equalizer=f=7500:t=q:w=2:g=-2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
         "aecho=0.8:0.6:18:0.08,loudnorm=I=-16:TP=-1.5")
_model = None


def _kokoro():
    global _model
    if _model is None:
        from kokoro_onnx import Kokoro
        _model = Kokoro(f"{KOKORO_DIR}/kokoro-v1.0.onnx", f"{KOKORO_DIR}/voices-v1.0.bin")
    return _model


def make(name, say):
    """Voice one line into the shared cache; returns the cached mp3 path."""
    out = pv.cached(name, say)
    if out:
        return out
    import soundfile as sf
    blend = BLENDS[name.split(":", 1)[1]]
    k = _kokoro()
    style = sum(w * k.get_voice_style(v) for v, w in blend)
    audio, sr = k.create(say, voice=style, speed=SPEED, lang="en-us")
    os.makedirs(pv.CACHE, exist_ok=True)
    base = f"{pv.CACHE}/{pv.key(name, say)}"
    sf.write(base + ".wav", audio, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base + ".wav", "-af", CHAIN, "-q:a", "2", base + ".mp3"],
                   check=True)
    os.remove(base + ".wav")
    json.dump(_words(base + ".mp3", say), open(base + ".mp3.words.json", "w"))
    return base + ".mp3"


def _words(mp3, say):
    """Script words with times from whisper; unmatched words are interpolated between matched neighbours."""
    heard = pv.align(mp3)
    script = say.split()
    sm = difflib.SequenceMatcher(None, [pv.norm(w) for w in script], [pv.norm(w) for *_, w in heard], autojunk=False)
    t = {}
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            t[a + i] = heard[b + i][:2]
    total = pv_duration(mp3)
    j = 0
    while j < len(script):  # spread each run of unmatched words ("600,000" vs "six hundred thousand") over its gap
        if j in t:
            j += 1
            continue
        run_end = j
        while run_end < len(script) and run_end not in t:
            run_end += 1
        s = t[j - 1][1] if j > 0 else 0.0
        e = t[run_end][0] if run_end < len(script) else total
        if e - s < 0.15 * (run_end - j):
            e = min(total, s + 0.3 * (run_end - j))
        step = (e - s) / (run_end - j)
        for i in range(j, run_end):
            t[i] = (s + step * (i - j), s + step * (i - j + 1))
        j = run_end
    return [(t[i][0], max(t[i][1], t[i][0] + 0.05), w) for i, w in enumerate(script)]


def pv_duration(mp3):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                                capture_output=True, text=True, check=True).stdout)


if __name__ == "__main__":  # free_voice.py "kokoro:eric-michael" "A line to voice"
    print(make(sys.argv[1], sys.argv[2]))
