#!/usr/bin/env python3
"""Burn the 2-line hook text (Anton, white line + yellow line, black stroke) onto a finished Short.
hook_text.py IN.mp4 OUT.mp4 "LINE ONE" "LINE TWO" [--all] [--y 210]
Default: shown 0.0-1.6 s, fading out by 1.9 s (research 68 NEW opening; the first fact card comes after 2 s).
--all: kept on screen for the whole video (micro-loops, so the last frame matches the first).
Video is re-encoded (crf 18); the audio stream is copied untouched (loudness stays as mastered)."""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "fonts", "Anton-Regular.ttf")
W, H = 1080, 1920

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("l1"); ap.add_argument("l2")
ap.add_argument("--all", action="store_true"); ap.add_argument("--y", type=int, default=210)
a = ap.parse_args()

im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dr = ImageDraw.Draw(im)
y = a.y
for s, col in ((a.l1, (255, 255, 255)), (a.l2, (255, 205, 40))):
    if not s:
        continue
    sz = 150
    f = ImageFont.truetype(FONT, sz)
    while dr.textlength(s, font=f) > 960:
        sz -= 6
        f = ImageFont.truetype(FONT, sz)
    w = dr.textlength(s, font=f)
    dr.text(((W - w) / 2, y), s, font=f, fill=col + (255,), stroke_width=12, stroke_fill=(0, 0, 0, 255))
    y += 175
png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
im.save(png)
fade = "" if a.all else ",fade=t=out:st=1.6:d=0.3:alpha=1"
filt = f"[1:v]format=rgba{fade}[t];[0:v][t]overlay=0:0:shortest=1[v]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-loop", "1", "-framerate", "30", "-i", png,
                "-filter_complex", filt, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", a.out], check=True)
os.unlink(png)
print("ok", a.out)
