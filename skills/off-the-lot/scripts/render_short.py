#!/usr/bin/env python3
"""Render a vertical 1080x1920 Short from a JSON scene list (silent; add voice with --audio).

Usage:
    python render_short.py ../shorts/001-four-square.json -o out.mp4 [--audio voice.m4a]

Scene types: "text" (big caption), "foursquare" (dealer worksheet, optional
highlighted box), "math" (rows of label/value, last row emphasised).
"""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG, INK, ACCENT, MUTED = "#111214", "#F5F5F0", "#FFD400", "#8A8D93"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BRAND = "OFF THE LOT"


def font(size):
    return ImageFont.truetype(FONT, size)


def wrap(draw, text, f, width):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=f) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


def base(scene_no, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((80, 110), BRAND, font=font(44), fill=ACCENT)
    d.rectangle((80, 180, 80 + int((W - 160) * scene_no / total), 188), fill=ACCENT)
    return img, d


def centered(d, text, y, size, fill=INK, width=W - 160):
    f = font(size)
    for line in wrap(d, text, f, width):
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=fill)
        y += int(size * 1.2)
    return y


def render_text(d, s):
    y = H // 2 - 200
    if s.get("kicker"):
        y = centered(d, s["kicker"], y - 120, 48, MUTED) + 40
    centered(d, s["text"], y, s.get("size", 96), ACCENT if s.get("accent") else INK)


def render_foursquare(d, s):
    boxes = ["Trade-in", "Price", "Down payment", "Monthly payment"]
    x0, y0, size, gap = 110, 560, 420, 20
    for i, label in enumerate(boxes):
        x = x0 + (i % 2) * (size + gap)
        y = y0 + (i // 2) * (size + gap)
        hot = label == s.get("highlight")
        d.rectangle((x, y, x + size, y + size), outline=ACCENT if hot else MUTED, width=10 if hot else 4,
                    fill="#2A2400" if hot else None)
        f = font(52)
        for j, line in enumerate(wrap(d, label, f, size - 40)):
            d.text((x + (size - d.textlength(line, font=f)) / 2, y + size / 2 - 40 + j * 62), line,
                   font=f, fill=ACCENT if hot else INK)
    if s.get("text"):
        centered(d, s["text"], 1500, 64)


def render_math(d, s):
    y = 520
    if s.get("title"):
        y = centered(d, s["title"], y, 64, MUTED) + 60
    for i, (label, value) in enumerate(s["rows"]):
        last = i == len(s["rows"]) - 1
        f = font(72 if last else 60)
        color = ACCENT if last else INK
        d.text((110, y), label, font=f, fill=color)
        d.text((W - 110 - d.textlength(value, font=f), y), value, font=f, fill=color)
        y += 140 if last else 110
        if i == len(s["rows"]) - 2:
            d.line((110, y - 20, W - 110, y - 20), fill=MUTED, width=3)
    if s.get("text"):
        centered(d, s["text"], 1500, 60)


RENDER = {"text": render_text, "foursquare": render_foursquare, "math": render_math}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--audio")
    a = p.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    scenes = spec["scenes"]
    with tempfile.TemporaryDirectory() as tmp:
        listing = []
        for n, s in enumerate(scenes, 1):
            img, d = base(n, len(scenes))
            RENDER[s["type"]](d, s)
            path = Path(tmp) / f"{n:02d}.png"
            img.save(path)
            listing += [f"file '{path}'", f"duration {s['seconds']}"]
        listing.append(f"file '{path}'")  # concat demuxer needs the last frame repeated
        concat = Path(tmp) / "list.txt"
        concat.write_text("\n".join(listing))
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat)]
        if a.audio:
            cmd += ["-i", a.audio, "-shortest", "-c:a", "aac"]
        cmd += ["-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-movflags", "+faststart", a.output]
        subprocess.run(cmd, check=True)
    print(a.output)


if __name__ == "__main__":
    main()
