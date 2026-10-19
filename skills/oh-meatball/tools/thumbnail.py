#!/usr/bin/env python3
"""Make a YouTube thumbnail from a video frame.

thumbnail.py VIDEO OUT.jpg --time T --text "HE CAME BACK" [--circle x,y,r]
             [--arrow x1,y1,x2,y2] [--size 1280x720|1080x1920]

Coordinates for --circle/--arrow are in OUTPUT pixels (after crop/fit).
"""
import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
RED = (230, 20, 20)


def ints(spec, n, name):
    try:
        vals = [int(float(v)) for v in spec.split(",")]
    except ValueError:
        sys.exit(f"thumbnail: --{name} must be {n} comma-separated numbers")
    if len(vals) != n:
        sys.exit(f"thumbnail: --{name} needs {n} values, got {len(vals)}")
    return vals


def grab_frame(video, t):
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", path]
    if subprocess.run(cmd).returncode != 0 or os.path.getsize(path) == 0:
        sys.exit(f"thumbnail: could not grab frame at {t}s from {video}")
    img = Image.open(path).convert("RGB")
    os.remove(path)
    return img


def fit(img, w, h):
    """Fill target; if aspect differs a lot (vertical clip -> 16:9), use blurred fill behind."""
    src_ar, dst_ar = img.width / img.height, w / h
    if abs(src_ar - dst_ar) / dst_ar < 0.35:
        return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=(0.5, 0.4))
    from PIL import ImageFilter
    bg = ImageOps.fit(img, (w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))
    bg = ImageEnhance.Brightness(bg).enhance(0.7)
    fg = ImageOps.contain(img, (w, h), Image.LANCZOS)
    bg.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
    return bg


def font_path():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    sys.exit("thumbnail: no bold sans font found")


def wrap_lines(words):
    if len(words) <= 2:
        return [" ".join(words)]
    cut = (len(words) + 1) // 2
    return [" ".join(words[:cut]), " ".join(words[cut:])]


def draw_text(img, text, fpath):
    w, h = img.size
    d = ImageDraw.Draw(img)
    lines = wrap_lines(text.upper().split())
    max_w = w * 0.92
    max_h = h * (0.36 if h < w else 0.24)
    size = int(h * 0.3)
    while size > 20:
        font = ImageFont.truetype(fpath, size)
        stroke = max(4, size // 11)
        boxes = [d.textbbox((0, 0), ln, font=font, stroke_width=stroke) for ln in lines]
        tw = max(b[2] - b[0] for b in boxes)
        th = sum(b[3] - b[1] for b in boxes) + (len(lines) - 1) * size * 0.08
        if tw <= max_w and th <= max_h:
            break
        size -= 4
    y = h * 0.04
    for i, (ln, b) in enumerate(zip(lines, boxes)):
        lw = b[2] - b[0]
        fill = (255, 230, 0) if i == len(lines) - 1 else (255, 255, 255)
        d.text(((w - lw) / 2 - b[0], y - b[1]), ln, font=font, fill=fill,
               stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += (b[3] - b[1]) + size * 0.08


def draw_circle(img, x, y, r):
    d = ImageDraw.Draw(img)
    lw = max(8, img.width // 110)
    d.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], outline=(0, 0, 0), width=lw + 6)
    d.ellipse([x - r, y - r, x + r, y + r], outline=RED, width=lw)


def draw_arrow(img, x1, y1, x2, y2):
    import math
    d = ImageDraw.Draw(img)
    lw = max(12, img.width // 70)
    ang = math.atan2(y2 - y1, x2 - x1)
    head = lw * 3.2
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py = -math.sin(ang), math.cos(ang)
    tri = [(x2, y2), (bx + px * head * 0.7, by + py * head * 0.7), (bx - px * head * 0.7, by - py * head * 0.7)]
    for color, extra in (((0, 0, 0), 8), (RED, 0)):
        d.line([(x1, y1), (bx, by)], fill=color, width=lw + extra)
        d.polygon(tri, fill=color, outline=(0, 0, 0) if color == RED else color, width=extra // 2 or 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--time", type=float, default=1.0, help="frame time in seconds")
    ap.add_argument("--text", required=True, help="2-4 words, e.g. 'HE CAME BACK'")
    ap.add_argument("--circle", help="x,y,r")
    ap.add_argument("--arrow", help="x1,y1,x2,y2 (tip at x2,y2)")
    ap.add_argument("--size", default="1280x720", choices=["1280x720", "1080x1920"])
    a = ap.parse_args()
    if not os.path.exists(a.video):
        sys.exit(f"thumbnail: video not found: {a.video}")
    if not 1 <= len(a.text.split()) <= 4:
        print("thumbnail: warning: best results with 2-4 words", file=sys.stderr)
    w, h = map(int, a.size.split("x"))
    img = fit(grab_frame(a.video, a.time), w, h)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Color(img).enhance(1.4)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    if a.circle:
        draw_circle(img, *ints(a.circle, 3, "circle"))
    if a.arrow:
        draw_arrow(img, *ints(a.arrow, 4, "arrow"))
    draw_text(img, a.text, font_path())
    img.save(a.out, "JPEG", quality=90)
    print(f"thumbnail: wrote {a.out} ({w}x{h}, {os.path.getsize(a.out) // 1024} KB)")


if __name__ == "__main__":
    main()
