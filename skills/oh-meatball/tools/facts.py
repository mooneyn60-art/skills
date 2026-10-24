#!/usr/bin/env python3
"""Facts Short builder: script JSON -> neural voiceover -> real footage -> pop-up captions.

Script JSON:
  {"slug": "octopus", "voice": "en-US-AndrewNeural",
   "lines": [{"text": "Octopuses have three hearts...", "footage": "octopus swimming"}, ...]}
"footage" is a local video path, or a search query fetched from Pexels when PEXELS_KEY is set.
Usage: facts.py script.json OUT.mp4
"""
import asyncio
import json
import os
import ssl
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

import edge_tts
import edge_tts.communicate as ec

# The sandbox proxy re-signs TLS; trust its bundle when present.
CA = "/root/.ccr/ca-bundle.crt"
if os.path.exists(CA):
    ec._SSL_CTX = ssl.create_default_context(cafile=CA)

W, H = 1080, 1920
FONT = "DejaVu Sans"


async def speak(text, voice, mp3, rate="+8%", pitch="+0Hz"):
    # The TTS endpoint intermittently returns no audio; retry before failing the build.
    for attempt in range(4):
        try:
            return await _speak(text, voice, mp3, rate, pitch)
        except edge_tts.exceptions.NoAudioReceived:
            await asyncio.sleep(2 * (attempt + 1))
    return await _speak(text, voice, mp3, rate, pitch)


async def _speak(text, voice, mp3, rate="+8%", pitch="+0Hz"):
    c = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(mp3, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    return words


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def pexels(query, dest):
    key = os.environ["PEXELS_KEY"]
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": query, "orientation": "portrait", "per_page": 5})
    data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": key})))
    for v in data["videos"]:
        files = sorted((f for f in v["video_files"] if f.get("height", 0) >= 1280),
                       key=lambda f: f["height"])
        if files:
            urllib.request.urlretrieve(files[0]["link"], dest)
            return dest
    raise RuntimeError(f"no portrait footage for {query!r}")


def footage(spec, tmp, i):
    if os.path.exists(spec):
        return spec
    return pexels(spec, f"{tmp}/foot{i}.mp4")


def ass_time(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def captions(words, path):
    # Two words per card, white with thick black outline, active word yellow.
    head = (f"[Script Info]\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
            "BorderStyle, Outline, Shadow, Alignment, MarginV\n"
            f"Style: Cap,{FONT},96,&H00FFFFFF,&H00000000,&H64000000,-1,1,7,3,5,0\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Text\n")
    lines = []
    for i in range(0, len(words), 2):
        group = words[i:i + 2]
        for j, (s, e, _) in enumerate(group):
            end = group[j + 1][0] if j + 1 < len(group) else e
            text = " ".join(("{\\c&H00FFFF&}" + w.upper() + "{\\c&HFFFFFF&}") if k == j else w.upper()
                            for k, (_, _, w) in enumerate(group))
            lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(end)},Cap,{{\\fscx110\\fscy110}}{text}")
    open(path, "w").write(head + "\n".join(lines) + "\n")


def build(script, out):
    voice = script.get("voice", "en-US-AndrewNeural")
    with tempfile.TemporaryDirectory() as tmp:
        segs = []
        for i, line in enumerate(script["lines"]):
            mp3, ass, seg = f"{tmp}/v{i}.mp3", f"{tmp}/c{i}.ass", f"{tmp}/s{i}.mp4"
            words = asyncio.run(speak(line["text"], voice, mp3))
            dur = duration(mp3) + 0.15
            captions(words, ass)
            src = footage(line["footage"], tmp, i)
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"eq=contrast=1.05:saturation=1.1,ass={ass}")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-stream_loop", "-1", "-i", src, "-i", mp3,
                            "-t", f"{dur:.2f}", "-vf", vf, "-map", "0:v", "-map", "1:a",
                            "-r", "30", "-c:v", "libx264", "-crf", "21", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-ar", "48000", "-ac", "2", seg], check=True)
            segs.append(seg)
        lst = f"{tmp}/list.txt"
        open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-af", "loudnorm=I=-14:TP=-1.5", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                        "-movflags", "+faststart", out], check=True)
    print(f"ok {out} {duration(out):.1f}s")


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])
