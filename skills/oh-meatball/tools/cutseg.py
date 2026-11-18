#!/usr/bin/env python3
"""Vertical cut of a 16:9 long-form segment (Studio 11/18 VOLUME: flagship segment cuts for Shorts and TikToks).

  cutseg.py IN.mp4 START END OUT.mp4 --title "Is a house centipede dangerous?" [--tag "THINGS LIVING IN YOUR HOUSE"]

1080x1920: a blurred, zoomed copy of the picture fills the frame, the 16:9 picture sits full width in the middle,
and the typed search question sits on a card at the top from 0:00 (TikTok search rule 8aca56b). Audio is copied
from the segment (the flagship's QA-passed words, word for word). Picture and sound are cut on the same frames."""
import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn as D  # noqa: E402


def card(text, tag, path):
    W, H = 1080, 520
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    words, lines, size = text.split(), [], 104
    while True:
        f = ImageFont.truetype(D.FONT, size)
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if dr.textlength(t, font=f) > W - 120 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        if len(lines) <= 3 or size <= 70:
            break
        size -= 8
    lh = int(size * 1.08)
    top = 150
    box_h = lh * len(lines) + 60
    dr.rounded_rectangle((30, top, W - 30, top + box_h), radius=36, fill=(20, 24, 38, 235), outline=(255, 211, 77, 255),
                         width=8)
    y = top + 30
    for ln in lines:
        x = (W - dr.textlength(ln, font=f)) / 2
        dr.text((x, y), ln, font=f, fill=(255, 211, 77, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += lh
    if tag:
        ft = ImageFont.truetype(D.FONT, 44)
        x = (W - dr.textlength(tag, font=ft)) / 2
        dr.text((x, top - 66), tag, font=ft, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    im.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("start", type=float)
    ap.add_argument("end", type=float)
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--tag", default="THINGS LIVING IN YOUR HOUSE")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "card.png")
        card(a.title, a.tag, png)
        fc = ("[0:v]split=2[a][b];"
              "[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.12[bg];"
              "[b]scale=1080:-2[fg];"
              "[bg][fg]overlay=0:(H-h)/2+80[v1];"
              "[v1][1:v]overlay=0:0,format=yuv420p[v]")
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % a.start, "-to", "%.3f" % a.end, "-i", a.src, "-loop", "1",
               "-i", png, "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-shortest", "-c:v", "libx264",
               "-preset", "medium", "-crf", "20", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
               "-af", "afade=t=out:st=%.3f:d=0.25" % max(0.0, a.end - a.start - 0.25), "-movflags", "+faststart",
               a.out]
        subprocess.run(cmd, check=True)
    print("cut %s  %.2f s" % (a.out, a.end - a.start))


if __name__ == "__main__":
    main()
