#!/usr/bin/env python3
"""Meatball — the channel's original stick-figure mascot, drawn in code so every frame is identical.

Usage: mascot.py OUTDIR            -> renders every pose to OUTDIR/<pose>.png (+ sheet.png)
       from mascot import draw; draw("point", 600) -> RGBA PIL image
Poses: neutral, point, shock, think, laugh, shrug, facepalm, wave
"""
import math
import os
import sys

from PIL import Image, ImageDraw

INK = (17, 17, 17, 255)
MEAT = (150, 78, 44, 255)
MEAT_DARK = (112, 54, 30, 255)
SHINE = (214, 140, 98, 255)
SAUCE = (196, 38, 30, 255)
PARSLEY = (64, 150, 60, 255)

# Limb end points per pose, in a 1000x1000 canvas. Shoulder (500,560), hip (500,780).
POSES = {
    "neutral":  {"l": [(430, 640), (410, 720)], "r": [(570, 640), (590, 720)], "mouth": "smile", "brow": None},
    "point":    {"l": [(430, 640), (410, 720)], "r": [(640, 520), (770, 460)], "mouth": "talk", "brow": "up"},
    "shock":    {"l": [(390, 520), (380, 420)], "r": [(610, 520), (620, 420)], "mouth": "o", "brow": "up"},
    "think":    {"l": [(430, 640), (410, 720)], "r": [(590, 520), (540, 430)], "mouth": "flat", "brow": "tilt"},
    "laugh":    {"l": [(420, 600), (440, 690)], "r": [(580, 600), (560, 690)], "mouth": "laugh", "brow": "up"},
    "shrug":    {"l": [(400, 560), (360, 500)], "r": [(600, 560), (640, 500)], "mouth": "flat", "brow": "up"},
    "facepalm": {"l": [(430, 640), (410, 720)], "r": [(600, 520), (510, 350)], "mouth": "frown", "brow": None},
    "wave":     {"l": [(430, 640), (410, 720)], "r": [(620, 470), (680, 360)], "mouth": "smile", "brow": None},
}
HEAD_C, HEAD_R = (500, 360), 150


def _line(d, a, b, w=26):
    d.line([a, b], fill=INK, width=w)
    for p in (a, b):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=INK)


def _head(d):
    cx, cy = HEAD_C
    r = HEAD_R
    # Lumpy meatball silhouette: a circle perturbed by a few low-frequency bumps.
    pts = [(cx + (r + 7 * math.sin(5 * t) + 4 * math.sin(9 * t + 1)) * math.cos(t),
            cy + (r + 7 * math.sin(5 * t) + 4 * math.sin(9 * t + 1)) * math.sin(t))
           for t in [i * 2 * math.pi / 180 for i in range(180)]]
    d.polygon(pts, fill=MEAT, outline=INK, width=14)
    for (x, y, s) in [(-70, -60, 16), (60, -85, 12), (85, 30, 18), (-95, 45, 13), (10, 95, 15), (-30, -110, 10)]:
        d.ellipse([cx + x - s, cy + y - s, cx + x + s, cy + y + s], fill=MEAT_DARK)
    d.ellipse([cx - 95, cy - 105, cx - 45, cy - 70], fill=SHINE)
    # Tomato-sauce cap with a parsley fleck: the brand detail.
    d.chord([cx - 120, cy - 175, cx + 120, cy - 40], 200, 340, fill=SAUCE, outline=INK, width=10)
    d.ellipse([cx + 20, cy - 150, cx + 48, cy - 132], fill=PARSLEY, outline=INK, width=4)


def _face(d, mouth, brow, look=(0, 0)):
    cx, cy = HEAD_C
    lx, ly = look  # pupil shift: thumbnails point his gaze at the animal or the key word
    for ex in (-48, 48):
        d.ellipse([cx + ex - 24, cy - 30, cx + ex + 24, cy + 20], fill=(255, 255, 255, 255), outline=INK, width=6)
        d.ellipse([cx + ex - 11 + lx, cy - 12 + ly, cx + ex + 11 + lx, cy + 10 + ly], fill=INK)
    if brow == "up":
        for ex in (-48, 48):
            d.arc([cx + ex - 28, cy - 62, cx + ex + 28, cy - 22], 200, 340, fill=INK, width=9)
    elif brow == "tilt":
        d.line([(cx - 76, cy - 44), (cx - 24, cy - 34)], fill=INK, width=9)
        d.line([(cx + 22, cy - 50), (cx + 76, cy - 58)], fill=INK, width=9)
    my = cy + 62
    if mouth == "smile":
        d.arc([cx - 45, my - 40, cx + 45, my + 20], 20, 160, fill=INK, width=10)
    elif mouth == "talk":
        d.chord([cx - 38, my - 22, cx + 38, my + 30], 0, 180, fill=INK)
    elif mouth == "o":
        d.ellipse([cx - 22, my - 22, cx + 22, my + 30], fill=INK)
    elif mouth == "laugh":
        d.chord([cx - 55, my - 30, cx + 55, my + 45], 0, 180, fill=INK)
        d.chord([cx - 30, my + 5, cx + 30, my + 40], 0, 180, fill=SAUCE)
    elif mouth == "frown":
        d.arc([cx - 40, my, cx + 40, my + 50], 200, 340, fill=INK, width=10)
    else:
        d.line([(cx - 32, my + 6), (cx + 32, my + 6)], fill=INK, width=10)


def draw(pose="neutral", size=600, mouth=None, blink=False, arms=None, look=(0, 0)):
    """mouth/blink override the pose for animation frames; arms = {"l"/"r": (dx, dy)} moves each hand
    (the elbow follows by half) for talking gestures."""
    p = POSES[pose]
    im = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sh, hip = (500, 560), (500, 790)
    _line(d, (500, 505), hip)                         # spine
    _line(d, hip, (440, 960)); _line(d, hip, (560, 960))  # legs
    _head(d)
    _face(d, mouth or p["mouth"], p["brow"], look)
    if blink:  # lids over both eyes
        cx, cy = HEAD_C
        for ex in (-48, 48):
            d.ellipse([cx + ex - 27, cy - 33, cx + ex + 27, cy + 23], fill=MEAT, outline=INK, width=6)
            d.line([(cx + ex - 24, cy - 4), (cx + ex + 24, cy - 4)], fill=INK, width=8)
    # Arms go on top of the head so hand-to-face poses (shock, facepalm, think) stay visible.
    for side in ("l", "r"):
        elbow, hnd = p[side]
        if arms and side in arms:
            dx, dy = arms[side]
            elbow, hnd = (elbow[0] + dx // 2, elbow[1] + dy // 2), (hnd[0] + dx, hnd[1] + dy)
        _line(d, sh, elbow); _line(d, elbow, hnd)
        d.ellipse([hnd[0] - 22, hnd[1] - 22, hnd[0] + 22, hnd[1] + 22], fill=INK)
    return im.resize((size, size), Image.LANCZOS)


TALK = {"talk": "o", "o": "talk", "laugh": "talk", "smile": "talk", "flat": "talk", "frown": "o"}


SWAP = {"point": "shrug", "shock": "shrug", "think": "point", "laugh": "point", "shrug": "point",
        "facepalm": "shrug", "wave": "point", "neutral": "point"}  # second pose always has open hands


def _gesture(t, words, phase):
    """Hand offset (in the 1000-unit drawing) for talking hands: a flick out on every word, a slow
    sweep while speaking, and back to rest in pauses. Quantized so frames can be cached."""
    flick = 0.0
    for s, e, _ in words:
        if s <= t < s + 0.35:
            flick = max(flick, math.sin(math.pi * (t - s) / 0.35))
    speaking = any(s - 0.05 <= t <= e + 0.15 for s, e, _ in words)
    sweep = math.sin(t * 2 * math.pi * 0.9 + phase) if speaking else 0.0
    dx = 45 * sweep + 25 * flick * math.cos(phase)
    dy = -55 * flick - 20 * abs(sweep)
    return int(dx // 8 * 8), int(dy // 8 * 8)


HAND_ON_FACE = {"think": "r", "facepalm": "r", "shock": None}  # that hand stays put on the face


def animate(pose, size, words, dur, fps, outdir, seed=0, pop=True):
    """PNG frames of Meatball talking. The body stays still (no bobbing); the life is in the face and
    hands: mouth flaps on spoken words, blinks every ~3 s, both hands gesture on each word, and the
    pose steps to a second one every ~2.2 s like rival stick-figure channels. pop is kept for callers
    but unused. Returns frame count."""
    from PIL import ImageFilter
    os.makedirs(outdir, exist_ok=True)
    first, second = pose, SWAP.get(pose, "point")
    cache = {}
    n = max(1, int(dur * fps))
    pad = int(size * 0.25)
    blink_at = [1.2 + 2.9 * k + (seed % 7) * 0.13 for k in range(int(dur / 2.9) + 2)]
    for f in range(n):
        t = f / fps
        pose = second if dur > 2.8 and int(t / 2.2) % 2 == 1 else first
        base_mouth = POSES[pose]["mouth"]
        speaking = any(s - 0.02 <= t <= e for s, e, _ in words)
        mouth = (TALK.get(base_mouth, "talk") if int(t / 0.11) % 2 == 0 else base_mouth) if speaking else None
        blink = any(b <= t < b + 0.12 for b in blink_at)
        still = HAND_ON_FACE.get(pose, "")
        arms = {side: _gesture(t, words, ph) for side, ph in (("l", 0.0), ("r", 2.4)) if side != still}
        if pose == "shock":  # both hands on the cheeks: small shakes only
            arms = {k: (v[0] // 3, v[1] // 3) for k, v in arms.items()}
        key = (pose, mouth, blink, tuple(sorted(arms.items())))
        if key not in cache:
            im = draw(pose, size, mouth, blink, arms)
            halo = im.split()[3].filter(ImageFilter.MaxFilter(13))
            framed = Image.new("RGBA", im.size, (0, 0, 0, 0))
            framed.paste((255, 255, 255, 255), (0, 0), halo)
            framed.alpha_composite(im)
            cache[key] = framed
        canvas = Image.new("RGBA", (size + 2 * pad, size + 2 * pad), (0, 0, 0, 0))
        canvas.alpha_composite(cache[key], (pad, pad))
        canvas.save(f"{outdir}/{f:04d}.png")
    return n


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    sheet = Image.new("RGBA", (300 * len(POSES), 340), (255, 255, 255, 255))
    for i, name in enumerate(POSES):
        im = draw(name, 300)
        im.save(f"{out}/{name}.png")
        sheet.alpha_composite(im, (300 * i, 0))
        ImageDraw.Draw(sheet).text((300 * i + 120, 310), name, fill=INK)
    sheet.convert("RGB").save(f"{out}/sheet.png")
    print("ok", out)
