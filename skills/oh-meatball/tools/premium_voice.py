#!/usr/bin/env python3
"""Premium narrator voice (vidIQ voiceover) for scripts whose "voice" is "vidiq:<voiceId>".

The voiceover API is an MCP tool, so the agent calls it; this script does the rest:

  premium_voice.py prep SCRIPT.json OUTDIR
      Writes OUTDIR/chunk-NN.txt (beat texts joined, at most ~4,800 characters each) and manifest.json.
      Send each chunk's text to vidiq_voiceover_generate with the script's voice id (one call per chunk:
      cost is 14 credits per started 1,000 characters), then save the MP3 as OUTDIR/chunk-NN.mp3.
  premium_voice.py prep-missing VOICE OUTDIR
      Same, for lines a render stopped on (Short hooks and loop lines that are built at render time).
  premium_voice.py split SCRIPT.json OUTDIR
      Aligns each chunk MP3 with faster-whisper, cuts it at beat boundaries and stores one MP3 plus
      .words.json per beat in the shared cache, where explainer.voice() picks them up by text.

Beats whose text is already cached are skipped by prep, so Shorts reuse their episode's audio.
"""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys

CACHE = os.environ.get("MEATBALL_VO_CACHE", os.path.expanduser("~/.cache/meatball-vo"))
MAX_CHARS = 4800


def key(name, say):
    return hashlib.sha1(f"{name}|{say}".encode()).hexdigest()[:16]


def cached(name, say):
    p = f"{CACHE}/{key(name, say)}.mp3"
    return p if os.path.exists(p) and os.path.exists(p + ".words.json") else None


def texts(spec):
    """Every distinct spoken line in script order, including Short hooks and loop lines when present."""
    out = [spec["loop_say"]] if spec.get("loop_say") else []  # v2 Shorts' loop tail is a script-level line
    for b in spec["beats"]:
        for t in [b.get("say")] + [s.get("say") for s in b.get("shots", []) if isinstance(s, dict)]:
            if t and t not in out:
                out.append(t)
    return out


def prep(script, outdir, todo=None, name=None):
    if todo is None:
        spec = json.load(open(script))
        name = spec["voice"]
        todo = [t for t in texts(spec) if not cached(name, t)]
    os.makedirs(outdir, exist_ok=True)
    chunks, cur = [], []
    for t in todo:
        if cur and sum(len(x) + 1 for x in cur) + len(t) > MAX_CHARS:
            chunks.append(cur)
            cur = []
        cur.append(t)
    if cur:
        chunks.append(cur)
    for i, c in enumerate(chunks):
        # A blank line between beats gives the narrator a natural pause we can cut in.
        open(f"{outdir}/chunk-{i:02d}.txt", "w").write("\n\n".join(c))
    json.dump({"voice": name, "chunks": chunks}, open(f"{outdir}/manifest.json", "w"), indent=1)
    chars = sum(len(t) for t in todo)
    print(f"{len(todo)} lines to voice in {len(chunks)} chunk(s), {chars} chars, "
          f"~{sum(14 * -(-len(' '.join(c)) // 1000) for c in chunks)} vidIQ credits")


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def align(mp3):
    from faster_whisper import WhisperModel
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768  # PyAV's loader breaks here; decode ourselves
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, word_timestamps=True)
    return [(w.start, w.end, w.word.strip()) for s in segs for w in s.words]


def split(script, outdir):
    man = json.load(open(f"{outdir}/manifest.json"))
    name = man["voice"]
    os.makedirs(CACHE, exist_ok=True)
    for i, chunk in enumerate(man["chunks"]):
        mp3 = f"{outdir}/chunk-{i:02d}.mp3"
        heard = align(mp3)
        script_words = [(bi, w) for bi, t in enumerate(chunk) for w in t.split()]
        sm = difflib.SequenceMatcher(None, [norm(w) for _, w in script_words], [norm(w) for *_, w in heard],
                                     autojunk=False)
        timing = {}
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                timing[a + k] = heard[b + k][:2]
        # Fill unmatched words (numbers, names) by interpolating between their matched neighbours.
        known = sorted(timing)
        for j in range(len(script_words)):
            if j not in timing:
                prev = max([k for k in known if k < j], default=None)
                nxt = min([k for k in known if k > j], default=None)
                s = timing[prev][1] if prev is not None else 0.0
                e = timing[nxt][0] if nxt is not None else s + 0.4
                timing[j] = (s, max(s + 0.05, e))
        total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                      "csv=p=0", mp3], capture_output=True, text=True).stdout)
        idx = [[j for j, (bi, _) in enumerate(script_words) if bi == b] for b in range(len(chunk))]
        for b, text in enumerate(chunk):
            first, last = idx[b][0], idx[b][-1]
            start = 0.0 if b == 0 else (timing[idx[b - 1][-1]][1] + timing[first][0]) / 2
            end = total if b == len(chunk) - 1 else (timing[last][1] + timing[idx[b + 1][0]][0]) / 2
            out = f"{CACHE}/{key(name, text)}.mp3"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
                            "-c:a", "libmp3lame", "-q:a", "2", out], check=True)
            words = [(timing[j][0] - start, timing[j][1] - start, script_words[j][1]) for j in idx[b]]
            json.dump(words, open(out + ".words.json", "w"))
        print(f"chunk {i}: {len(chunk)} beats cached, {len(timing)} words aligned")


def prep_missing(voice, outdir):
    """Lines a render stopped on (explainer.voice logs them to CACHE/missing.txt)."""
    path = f"{CACHE}/missing.txt"
    rows = [json.loads(l) for l in open(path)] if os.path.exists(path) else []
    todo = list(dict.fromkeys(r["say"] for r in rows if r["voice"] == voice and not cached(voice, r["say"])))
    prep(None, outdir, todo, voice)
    if os.path.exists(path):
        os.remove(path)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prep-missing":
        prep_missing(sys.argv[2], sys.argv[3])  # VOICE OUTDIR
    else:
        {"prep": prep, "split": split}[cmd](sys.argv[2], sys.argv[3])
