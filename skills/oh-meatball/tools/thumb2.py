#!/usr/bin/env python3
"""High-contrast quiz thumbnail (v2): sunburst background, the animal cut out big with a sticker outline,
a red stamp, shocked Meatball, and 1-3 huge words. Built to read at phone size in a busy feed.

Usage: thumb2.py PHOTO OUT.jpg "TOP WORDS" [--stamp FALSE?] [--palette sun|ocean|jungle] [--flip]
Cut-out uses rembg when installed; otherwise the photo goes in a tilted white-bordered frame.
"""
import argparse
import math
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from mascot import draw

W, H = 1280, 720
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "brand", "fonts", "Anton-Regular.ttf")
PALETTES = {  # inner, outer, ray
    "sun": ((255, 226, 60), (255, 120, 0), (255, 196, 30)),
    "ocean": ((70, 200, 255), (0, 70, 190), (40, 150, 240)),
    "jungle": ((150, 240, 80), (20, 130, 40), (110, 210, 60)),
    "hot": ((255, 120, 120), (190, 0, 40), (240, 70, 80)),
}
RED = (225, 20, 30)


def background(pal):
    inner, outer, ray = PALETTES[pal]
    bg = Image.new("RGB", (W, H), outer)
    # Radial gradient, then sunburst rays from a point right of center (behind the animal).
    cx, cy = int(W * 0.66), int(H * 0.5)
    grad = Image.new("L", (W, H))
    gp = grad.load()
    rmax = math.hypot(W, H) * 0.6
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            v = int(255 * max(0, 1 - math.hypot(x - cx, y - cy) / rmax))
            gp[x, y] = v
            if x + 1 < W:
                gp[x + 1, y] = v
            if y + 1 < H:
                gp[x, y + 1] = v
                if x + 1 < W:
                    gp[x + 1, y + 1] = v
    bg = Image.composite(Image.new("RGB", (W, H), inner), bg, grad)
    rays = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(rays)
    for k in range(24):
        a0, a1 = k * 15, k * 15 + 7
        pts = [(cx, cy)] + [(cx + 2000 * math.cos(math.radians(a)), cy + 2000 * math.sin(math.radians(a)))
                            for a in (a0, a1)]
        d.polygon(pts, fill=70)
    return Image.composite(Image.new("RGB", (W, H), ray), bg, rays).convert("RGBA")


def sticker(im, edge=16, dark=5):
    """White outline + thin black rim + soft drop shadow around an RGBA cut-out."""
    a = im.split()[3]
    pad = edge + dark + 30
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big = Image.new("L", canvas.size, 0)
    big.paste(a, (pad, pad))
    white = big.filter(ImageFilter.MaxFilter(edge * 2 + 1))
    black = white.filter(ImageFilter.MaxFilter(dark * 2 + 1))
    shadow = black.filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.55)
    canvas.paste((0, 0, 0, 255), (12, 16), shadow)
    canvas.paste((17, 17, 17, 255), (0, 0), black)
    canvas.paste((255, 255, 255, 255), (0, 0), white)
    canvas.alpha_composite(im, (pad, pad))
    return canvas


def cutout(path, zoom=0.72):
    photo = Image.open(path).convert("RGB")
    photo = ImageEnhance.Color(ImageEnhance.Contrast(photo).enhance(1.15)).enhance(1.35)
    try:
        from rembg import remove
        cut = remove(photo)
        box = cut.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
        if box and (box[2] - box[0]) * (box[3] - box[1]) > 0.08 * photo.width * photo.height:
            return cut.crop(box), True
    except Exception:
        pass
    # No reliable cut-out: zoom toward the subject (photos are centred on it), then a tilted white frame
    # so it still reads as a real photo and pops off the background.
    zw, zh = int(photo.width * zoom), int(photo.height * zoom)
    l, t = (photo.width - zw) // 2, (photo.height - zh) // 2
    photo = photo.crop((l, t, l + zw, t + zh))
    framed = ImageOps.expand(photo, border=int(photo.width * 0.025), fill="white").convert("RGBA")
    return framed.rotate(4, expand=True, resample=Image.BICUBIC), False


def stamp(text, size=120):
    f = ImageFont.truetype(FONT, size)
    tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=f))
    im = Image.new("RGBA", (tw + 80, int(size * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, im.width - 6, im.height - 6], 22, fill=RED, outline=(255, 255, 255), width=10)
    d.text((40, int(size * 0.12)), text, font=f, fill=(255, 255, 255))
    return im.rotate(-12, expand=True, resample=Image.BICUBIC)


def headline(d, words, x, y, max_w):
    """1-3 words, huge, white with a thick black stroke; the last word in yellow."""
    size = 190
    while size > 70:
        f = ImageFont.truetype(FONT, size)
        if d.textlength(words, font=f) <= max_w:
            break
        size -= 6
    parts = words.split()
    cx = x
    for i, w in enumerate(parts):
        fill = (255, 230, 0) if i == len(parts) - 1 and len(parts) > 1 else (255, 255, 255)
        d.text((cx, y), w, font=f, fill=fill, stroke_width=12, stroke_fill=(0, 0, 0))
        cx += d.textlength(w + " ", font=f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("words")
    ap.add_argument("--stamp", default="FALSE?")
    ap.add_argument("--palette", default="sun", choices=PALETTES)
    ap.add_argument("--flip", action="store_true", help="mirror the animal so it faces Meatball")
    ap.add_argument("--pose", default="shock")
    ap.add_argument("--zoom", type=float, default=0.72, help="framed-photo crop; 1.0 keeps the whole photo")
    a = ap.parse_args()

    canvas = background(a.palette)
    animal, cut = cutout(a.photo, a.zoom)
    if a.flip:
        animal = ImageOps.mirror(animal)
    # Animal fills the right ~60% and bleeds off the bottom: big subject = readable at 120 px wide.
    target_h = 640 if cut else 540
    s = min(target_h / animal.height, (760 if cut else 820) / animal.width)
    animal = animal.resize((int(animal.width * s), int(animal.height * s)), Image.LANCZOS)
    st = sticker(animal) if cut else animal
    ax = W - st.width + (40 if cut else -20)
    ay = H - st.height + (60 if cut else -40)
    canvas.alpha_composite(st, (max(ax, 380), max(ay, 120)))

    # Head-and-shoulders crop: the face carries the emotion, the stick legs add nothing at 120 px.
    body = draw(a.pose, 1100).crop((150, 120, 950, 820))
    m = sticker(body.resize((520, 455), Image.LANCZOS), edge=12, dark=4)
    canvas.alpha_composite(m, (-60, H - m.height + 40))

    sp = stamp(a.stamp)
    canvas.alpha_composite(sp, (W - sp.width - 30, 30))

    d = ImageDraw.Draw(canvas)
    headline(d, a.words, 36, 14, W - sp.width - 90)
    canvas.convert("RGB").save(a.out, quality=93)
    print("ok", a.out, "cutout" if cut else "framed")


if __name__ == "__main__":
    main()
