#!/usr/bin/env python3
"""Build a finished Oh Meatball part and QA it. Exits non-zero if the audio check fails.

Usage:
  python finish.py --shots s1.mp4 s2.mp4 --part 3 -o part3.mp4 \
      [--expect "line one" "line two"] [--music brand/theme.m4a] [--sting brand/sting.wav]

Mix: shot audio (voices + Veo's own SFX) on top; theme music looped underneath and ducked
under the voices (sidechain); sting hits 1.5 s before the end; loudness -14 LUFS (YouTube).
Text: "PART N" for the first 2 s, "PART N+1 NEXT" for the last 1.7 s.
QA: audio stream present, loudness in range, music audible under dialogue, and every
--expect line found in a Whisper transcript (fuzzy).
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout
    return float(out.strip())


def build(a):
    n = len(a.shots)
    total = sum(duration(s) for s in a.shots)
    inputs = []
    for s in a.shots:
        inputs += ["-i", s]
    inputs += ["-stream_loop", "-1", "-i", a.music, "-i", a.sting]
    m, st = n, n + 1
    v = "".join(f"[{i}:v]fps=24,scale=1080:1920,setsar=1[v{i}];" for i in range(n))
    au = "".join(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(n))
    cat = "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][voice];"
    end = total - 1.7
    txt = (f"[vc]drawtext=fontfile={FONT}:text='PART {a.part}':fontcolor=white:fontsize=80:borderw=7:"
           f"bordercolor=black:x=(w-tw)/2:y=170:enable='lt(t,2)',"
           f"drawtext=fontfile={FONT}:text='PART {a.part + 1}':fontcolor=0xFFD400:fontsize=110:borderw=9:"
           f"bordercolor=black:x=(w-tw)/2:y=140:enable='gte(t,{end:.2f})',"
           f"drawtext=fontfile={FONT}:text='NEXT':fontcolor=white:fontsize=72:borderw=7:"
           f"bordercolor=black:x=(w-tw)/2:y=270:enable='gte(t,{end:.2f})',format=yuv420p[vo];")
    mix = (f"[voice]asplit=2[vk][vmix];"
           f"[{m}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.2f},volume={a.music_db}dB,"
           f"afade=t=out:st={total - 1.5:.2f}:d=1.5[bed];"
           f"[bed][vk]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[ducked];"
           f"[{st}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-4dB,"
           f"adelay={int((total - 1.5) * 1000)}|{int((total - 1.5) * 1000)}[hit];"
           f"[vmix][ducked][hit]amix=inputs=3:duration=first:normalize=0,"
           f"loudnorm=I=-14:TP=-1.5:LRA=11[ao]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", v + au + cat + txt + mix,
           "-map", "[vo]", "-map", "[ao]", "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "20",
           "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", a.output]
    r = run(cmd)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {r.stderr[-800:]}")


def qa(a):
    report, ok = {}, True
    streams = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", a.output]).stdout
    report["audio_stream"] = "audio" in streams
    ok &= report["audio_stream"]
    vol = run(["ffmpeg", "-hide_banner", "-i", a.output, "-af", "volumedetect", "-vn", "-f", "null", "-"]).stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+)", vol).group(1))
    report["mean_db"] = mean
    ok &= -22 <= mean <= -9
    # music audible: the quietest stretch must not be silent (bed keeps playing between lines)
    sil = run(["ffmpeg", "-hide_banner", "-i", a.output, "-af", "silencedetect=n=-45dB:d=0.8", "-f", "null", "-"]).stderr
    report["silent_gaps"] = sil.count("silence_start")
    ok &= report["silent_gaps"] == 0
    if a.expect:
        import numpy as np
        from faster_whisper import WhisperModel
        raw = run_bytes(["ffmpeg", "-loglevel", "error", "-i", a.output, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"])
        segs, _ = WhisperModel("base.en", device="cpu", compute_type="int8").transcribe(np.frombuffer(raw, np.float32))
        heard = " ".join(s.text for s in segs).lower()
        report["transcript"] = heard.strip()
        for line in a.expect:
            score = difflib.SequenceMatcher(None, norm(line), norm(heard)).find_longest_match(0, len(norm(line)), 0, len(norm(heard))).size / max(1, len(norm(line)))
            report[f"line: {line}"] = round(score, 2)
            ok &= score >= 0.6
    report["PASS"] = bool(ok)
    print(json.dumps(report, indent=2))
    return ok


def run_bytes(cmd):
    return subprocess.run(cmd, capture_output=True).stdout


def norm(s):
    return re.sub(r"[^a-z ]", "", s.lower())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--shots", nargs="+", required=True)
    p.add_argument("--part", type=int, required=True)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--expect", nargs="*", default=[])
    p.add_argument("--music", default=str(HERE / "brand/theme.m4a"))
    p.add_argument("--sting", default=str(HERE / "brand/sting.wav"))
    p.add_argument("--music-db", type=float, default=-17)
    a = p.parse_args()
    build(a)
    sys.exit(0 if qa(a) else 1)


if __name__ == "__main__":
    main()
