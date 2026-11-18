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
    "onyx": [("am_onyx", 1.0)],        # deep male candidates for Meatball Investigates (10/26 voice sampler)
    "fenrir": [("am_fenrir", 1.0)],
    "adam": [("am_adam", 1.0)],
    "adam-puck": [("am_adam", 0.6), ("am_puck", 0.4)],      # voice test v3 E2 (11/17)
    "adam-michael": [("am_adam", 0.6), ("am_michael", 0.4)],        # Studio voice test 11/17 (B)
    "michael": [("am_michael", 1.0)],
}
SPEED = 1.05
# Per-blend overrides: speed, and "pause" = the longest silence kept inside a line (s). The drawn animal
# Shorts' narrator is fenrir at 0.86 with comma pauses capped at 0.22 s (outlier-matching voice test, 10/28).
TUNING = {"fenrir": {"speed": 0.86, "pause": 0.22}, "adam": {"speed": 1.18, "pause": 0.25},
          "adam-puck": {"speed": 1.18, "pause": 0.2}, "adam-michael": {"speed": 1.18, "pause": 0.2},
          "michael": {"speed": 1.18, "pause": 0.25}}
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


def parse(name):
    """"kokoro:adam@speed=1.3,pitch=2,gain=3" -> ("kokoro", "adam", {"speed": 1.3, "pitch": 2.0, "gain": 3.0}).
    Per-line acting (voice test v2, 11/17): speed (Kokoro), ex/cfg (Chatterbox exaggeration and cfg weight),
    pitch (semitones, after the take), gain (dB, after loudness), pause (longest kept inner silence, s)."""
    eng, rest = name.split(":", 1)
    blend, _, ps = rest.partition("@")
    params = {}
    for kv in filter(None, ps.split(",")):
        k, _, v = kv.partition("=")
        params[k.strip()] = float(v)
    return eng, blend, params


def cache_name(name):
    """The shared-cache name: the voice name, plus its tuning when a blend has one (so a retune re-voices)."""
    t = TUNING.get(parse(name)[1])
    base = name + "|trim1"   # 11/17: every take is trimmed now, so older untrimmed takes are re-voiced
    return base if not t else base + "|" + ",".join(f"{k}={v}" for k, v in sorted(t.items()))


_cb = None
CB_REF = os.path.expanduser("~/.cache/chatterbox-ref")


def _chatterbox():
    global _cb
    if _cb is None:
        from chatterbox.tts import ChatterboxTTS
        _cb = ChatterboxTTS.from_pretrained(device="cpu")
    return _cb


TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")


def post_chain(params, sr=24000):
    """Trim the take's lead-in and tail silence (Studio 11/17: lines butt together), the voice chain, then the
    line's acting: pitch (semitones), formant (ratio, >1 = smaller, more cartoon), gain (dB), drive (soft clip)."""
    pre = [TRIM]
    st = params.get("pitch", 0.0)
    fm = params.get("formant", 1.0)
    if fm != 1.0:   # move the formants up by fm, keep the pitch where `pitch` puts it
        pre.append(f"asetrate={int(sr * fm)},aresample={sr},rubberband=pitch={2 ** (st / 12) / fm:.5f}:formant=preserved")
    elif st:
        pre.append(f"rubberband=pitch={2 ** (st / 12):.5f}:formant=preserved")
    chain = ",".join(pre) + "," + CHAIN
    g = params.get("gain", 0.0)
    if g:
        chain += f",volume={g}dB"
    if params.get("drive"):
        chain += f",asoftclip=type=tanh:threshold={max(0.3, 1 - 0.3 * params['drive']):.2f}"
    return chain


def cap_pauses(audio, sr, cap, floor=0.01, frame=0.01):
    """Shorten every silent run inside the line (10 ms frames whose peak is under 1% of the line's peak) to
    `cap` s, keeping half of it on each side of the cut. Lead-in and tail silence are left alone."""
    import numpy as np
    n = int(sr * frame)
    if not len(audio) or cap is None:
        return audio
    peak = float(np.max(np.abs(audio))) or 1.0
    frames = len(audio) // n
    loud = np.abs(audio[:frames * n]).reshape(frames, n).max(axis=1) >= floor * peak
    on = np.where(loud)[0]
    if len(on) < 2:
        return audio
    keep, i, half = [], on[0], int(cap * sr / 2)
    pos = 0
    while i <= on[-1]:
        if loud[i]:
            i += 1
            continue
        j = i
        while not loud[j]:
            j += 1
        a, b = i * n, j * n
        if b - a > 2 * half:
            keep.append(audio[pos:a + half])
            pos = b - half
        i = j
    keep.append(audio[pos:])
    return np.concatenate(keep)


def make(name, say):
    """Voice one line into the shared cache; returns the cached mp3 path."""
    cname = cache_name(name)
    out = pv.cached(cname, say)
    if out:
        return out
    import soundfile as sf
    eng, blend_name, params = parse(name)
    tune = dict(TUNING.get(blend_name, {}), **params)
    if eng == "chatterbox":
        m = _chatterbox()
        ref = f"{CB_REF}/{blend_name}.wav"
        wav = m.generate(say, audio_prompt_path=ref if os.path.exists(ref) else None,
                         exaggeration=tune.get("ex", 0.7), cfg_weight=tune.get("cfg", 0.3))
        audio, sr = wav.squeeze(0).numpy(), m.sr
    else:
        blend = BLENDS[blend_name]
        k = _kokoro()
        style = sum(w * k.get_voice_style(v) for v, w in blend)
        audio, sr = k.create(say, voice=style, speed=tune.get("speed", SPEED), lang="en-us")
    audio = cap_pauses(audio, sr, tune.get("pause"))
    os.makedirs(pv.CACHE, exist_ok=True)
    base = f"{pv.CACHE}/{pv.key(cname, say)}"
    sf.write(base + ".wav", audio, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base + ".wav", "-af", post_chain(params, sr), "-q:a", "2",
                    base + ".mp3"], check=True)
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
