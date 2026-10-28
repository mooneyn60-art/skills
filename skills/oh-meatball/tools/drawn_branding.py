#!/usr/bin/env python3
"""Channel branding in the drawn style (YouTube banner, avatar, watermark), drawn with the same kit as the
Shorts: the garden habitat from drawn_habitats, animals from drawn_creatures/drawn_species (configs copied
from the scripts/drawn-tt specs so they look exactly like their episodes) and Meatball from mascot.py.

Usage: drawn_branding.py [OUTDIR]     (default episodes/branding-drawn/)
  banner.png     2560x1440; everything that matters sits in the 1546x423 centre safe area
  avatar.png     800x800, Meatball's head on a flat circle-safe colour
  avatar-48.png  the avatar downscaled to 48 px (legibility check)
  watermark.png  150x150 transparent, Meatball's head
"""
import os
import sys

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mascot  # noqa: E402
from drawn_creatures import build  # noqa: E402
from drawn_habitats import SCENES  # noqa: E402
from drawn_kit import BG_OUT, OUT, PAL, darker, hexc, p_ellipse, p_rrect, shape, stroke  # noqa: E402
from drawn_species import SPECIES  # noqa: E402

ROOT = os.path.dirname(HERE)
FONT = os.path.join(ROOT, "brand/fonts/Anton-Regular.ttf")   # the caption font
BW, BH = 2560, 1440
SAFE = ((BW - 1546) // 2, (BH - 423) // 2, (BW + 1546) // 2, (BH + 423) // 2)   # x0, y0, x1, y1
GROUND = SAFE[3] - 14   # banner y of the habitat ground line: feet stand just inside the safe area
INK8 = (17, 17, 17, 255)

# Hero animals, configs as in their Animal Files episodes (scripts/drawn-tt/<name>-yt.json stage.creature_cfg).
ANIMALS = {
    "owl": {"plan": "bird", "label": "owl", "color": "#8a6a48", "dark": "#5a4430", "belly": "#e6d6b8",
            "beak": "hook", "length": 460, "height": 340, "face_disc": True, "ear_tufts": True},
    "moose": {"plan": "mammal", "label": "moose", "color": "#5c3f2b", "dark": "#3e2a1c", "belly": "#8a6a50",
              "length": 700, "height": 300, "leg_len": 380, "leg_w": 34, "ears": "pointed", "tail": "thin",
              "tail_w": 8, "whiskers": False, "mood": "calm", "antlers": True, "beard": True},
    "wombat": {"plan": "mammal", "label": "common wombat", "color": "#8a7560", "dark": "#5e4e3e",
               "belly": "#a8937c", "length": 560, "height": 300, "leg_len": 60, "leg_w": 40, "ears": "round",
               "tail": "thin", "tail_w": 0.1, "whiskers": True, "mood": "happy"},
    "octopus": {"plan": "octopus", "label": "common octopus", "color": "#e0704a", "dark": "#b8502e",
                "eye_r": 44, "mood": "happy", "size": 260},
    "polar_bear": {"plan": "mammal", "label": "polar bear", "color": "#f4f1e8", "dark": "#cfc9b8",
                   "belly": "#e6e1d2", "length": 680, "height": 340, "leg_len": 150, "leg_w": 60, "ears": "round",
                   "tail": "thin", "tail_w": 0.1, "whiskers": False, "mood": "happy"},
    "jumping_spider": SPECIES["jumping_spider"],
    # extras that only show outside the safe area (TV / desktop)
    "parrot": SPECIES["parrot"], "rabbit": SPECIES["rabbit"], "squirrel": SPECIES["squirrel"],
}


def extents(name, p):
    """Ink bounds of one creature at scale 1 (x0, y0, x1, y1), its feet at (0, 0)."""
    rec = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
    build(ANIMALS[name])(cairo.Context(rec), 0.0, p)
    x, y, w, h = rec.ink_extents()
    return x, y, x + w, y + h


def put(ctx, name, cx, base, height=None, width=None, flip=False, p=None):
    """Draw a creature with its feet centred at (cx, base), scaled so its ink fits height (and width) px.
    Returns its banner-space box."""
    p = dict({"blink": 0, "look": (0, 0)}, **(p or {}))
    x0, y0, x1, y1 = extents(name, p)
    k = min(height / (y1 - y0) if height else 9e9, width / (x1 - x0) if width else 9e9)
    mid = (x0 + x1) / 2
    ctx.save()
    ctx.identity_matrix()
    ctx.translate(cx, base - y1 * k)
    ctx.scale(-k if flip else k, k)
    ctx.translate(-mid, 0)
    build(ANIMALS[name])(ctx, 0.0, p)
    ctx.restore()
    return (cx - (x1 - x0) * k / 2, base - (y1 - y0) * k, cx + (x1 - x0) * k / 2, base)


def to_pil(surf):
    surf.flush()
    a = np.ndarray((surf.get_height(), surf.get_width(), 4), np.uint8, surf.get_data()).copy()
    return Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")


def meatball(pose, size, look=(0, 0)):
    return mascot.draw(pose, size, look=look)


def text(im, xy, s, px, fill, stroke_px, anchor="mm", stroke_fill=INK8, shadow=None):
    f = ImageFont.truetype(FONT, px)
    d = ImageDraw.Draw(im)
    if shadow:
        d.text((xy[0] + shadow[0], xy[1] + shadow[1]), s, font=f, fill=shadow[2], anchor=anchor,
               stroke_width=stroke_px, stroke_fill=shadow[2])
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke_px, stroke_fill=stroke_fill)
    return d.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke_px)


# ---------------------------------------------------------------- banner

def banner(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, BW, BH)
    ctx = cairo.Context(surf)
    dy = GROUND - 1500   # the habitat's world ground line is y 1500

    def layer(depth):   # sky/sun/clouds sit higher so they show above the safe area; the ground layer is 1:1
        ctx.identity_matrix()
        ctx.translate(0, dy if depth >= 1 else -70)

    props = [["tree", 140, 1500, 1.15], ["bush", 470, 1500, 0.9], ["flowers", 2050, 1500, 0.9], ["bush", 2290, 1500, 1.0], ["tree", 2470, 1500, 1.0],
             ["mushroom", 390, 1640, 0.7], ["grass", 2140, 1700, 1.0], ["grass", 330, 1760, 1.0],
             ["rock", 2390, 1780, 0.8], ["flowers", 700, 1760, 0.8], ["mushroom", 1850, 1780, 0.6],
             ["grass", 1300, 1820, 1.0]]
    SCENES["garden"](ctx, 0.0, layer, {"time": "day", "props": props})
    ctx.identity_matrix()   # two more clouds so the sky reads across the full TV width
    for x, y in ((1880, 170), (2420, 300), (-60, 320)):
        for ddx, ddy, r in ((-90, 10, 70), (0, -30, 95), (100, 5, 75)):
            shape(ctx, lambda c, x=x, ddx=ddx, ddy=ddy, r=r: p_ellipse(c, x + ddx, y + ddy, r, r * 0.8),
                  PAL["cloud"], BG_OUT * 0.8, (0, 0.18), shade_k=0.92)

    # left of the sign: the owl on a stump beside Meatball (drawn first so its tail tucks behind the sign)
    gy = GROUND
    shape(ctx, lambda c: p_rrect(c, 770, gy - 70, 110, 70 + 6, 14), hexc("#7a5233"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_ellipse(c, 825, gy - 70, 55, 14), hexc("#c9a06a"), OUT * 0.8, None)
    put(ctx, "owl", 815, gy - 70, height=175, width=190, flip=True, p={"mood": "happy"})

    # the sign: a wooden board on two posts, centre of the safe area
    sx0, sx1, sy0, sy1 = 895, 1665, SAFE[1] + 10, SAFE[1] + 232
    for px in (sx0 + 120, sx1 - 120):
        shape(ctx, lambda c, px=px: c.rectangle(px - 20, sy1 - 10, 40, GROUND - sy1 + 10), PAL["wood_dk"], OUT,
              (0.1, 0))
    shape(ctx, lambda c: p_rrect(c, sx0, sy0, sx1 - sx0, sy1 - sy0, 34), PAL["wood"], OUT * 1.3, (0.02, 0.05))
    for yy in (sy0 + 78, sy0 + 156):
        stroke(ctx, [(sx0 + 22, yy), (sx1 - 22, yy)], 4, color=darker(PAL["wood"], 0.82))
    for nx in (sx0 + 30, sx1 - 30):
        for ny in (sy0 + 30, sy1 - 30):
            shape(ctx, lambda c, nx=nx, ny=ny: p_ellipse(c, nx, ny, 9, 9), PAL["steel"], OUT * 0.5, None)

    # small animals in the gap under the sign, between the posts
    put(ctx, "jumping_spider", 1100, gy, height=150, p={"mood": "happy"})
    put(ctx, "wombat", 1290, gy, height=125, p={"mood": "happy"})
    put(ctx, "octopus", 1460, gy, height=150, flip=True, p={"mood": "happy"})
    # right of the sign: polar bear in front of the moose (both face left, toward the title)
    put(ctx, "moose", 1865, gy - 8, height=SAFE[3] - SAFE[1] - 30, width=370, flip=True, p={"mood": "happy"})
    put(ctx, "polar_bear", 1760, gy + 4, height=150, flip=True, p={"mood": "happy"})
    # extras outside the safe area (TV / desktop only)
    put(ctx, "parrot", 2230, 470, height=120, flip=True, p={"fly": 1.0})   # flying, right of the safe area
    put(ctx, "rabbit", 2180, GROUND + 330, height=170, flip=True, p={"mood": "happy"})
    put(ctx, "squirrel", 300, GROUND + 260, height=170, p={"mood": "happy"})

    im = to_pil(surf)
    ms = 500
    mb = meatball("wave", ms)   # feet at drawing (500, 960)
    k = ms / 1000
    im.alpha_composite(mb, (int(620 - 500 * k), int(GROUND - 960 * k)))

    cx = (sx0 + sx1) // 2
    px = 120   # the biggest title that fits the board with a margin
    f = ImageFont.truetype(FONT, px)
    while ImageDraw.Draw(im).textbbox((0, 0), "MEATBALL MYTHS", font=f, stroke_width=8)[2] > sx1 - sx0 - 70:
        px -= 2
        f = ImageFont.truetype(FONT, px)
    text(im, (cx, sy0 + 84), "MEATBALL MYTHS", px, (255, 255, 255, 255), 8, shadow=(0, 6, (120, 40, 20, 255)))
    pill = (sx0 + 48, sy0 + 156, sx1 - 48, sy1 - 18)
    ImageDraw.Draw(im).rounded_rectangle(pill, radius=24, fill=(17, 17, 17, 255))
    sb = text(im, (cx, (pill[1] + pill[3]) // 2), "Weird animal facts, drawn. New every day.", 38,
              (255, 246, 214, 255), 0)
    assert pill[0] + 10 < sb[0] and sb[2] < pill[2] - 10, sb
    im.convert("RGB").save(out, optimize=True)


# ---------------------------------------------------------------- avatar + watermark

def head(size):
    """Meatball's head (+ a little neck) as RGBA, the head circle centred; the 1000-unit head is r 150."""
    k = size / 1000
    im = meatball("neutral", size)
    hx, hy = mascot.HEAD_C
    box = (int((hx - 215) * k), int((hy - 235) * k), int((hx + 230) * k), int((hy + 190) * k))
    return im.crop(box), (int((hx * k) - box[0]), int((hy * k) - box[1])), k


def avatar(out, out48):
    S = 800
    im = Image.new("RGBA", (S, S), (255, 216, 74, 255))   # PAL sun yellow: warm, contrasts the brown head
    ImageDraw.Draw(im).ellipse((40, 40, S - 40, S - 40), fill=(255, 228, 120, 255))
    size = 1650   # head ~500 px wide: cap and cheeks stay inside the circle crop
    k = size / 1000
    mb = meatball("neutral", size * 2)   # drawn at 2x and reduced: clean outlines at this size
    mb = mb.filter(ImageFilter.MedianFilter(7)).resize((size, size), Image.LANCZOS)   # drops hairline specks
    hx, hy = mascot.HEAD_C
    ox, oy = int(S / 2 - hx * k), int(S * 0.5 - hy * k)
    im.alpha_composite(mb.crop((max(0, -ox), max(0, -oy), max(0, -ox) + S, max(0, -oy) + S)),
                       (max(0, ox), max(0, oy)))
    im = im.convert("RGB")
    im.save(out, optimize=True)
    im.resize((48, 48), Image.LANCZOS).save(out48)


def watermark(out):
    S = 150
    h, (cx, cy), k = head(600)
    h = h.crop(h.getbbox())
    h.thumbnail((S - 6, S - 6), Image.LANCZOS)
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    im.alpha_composite(h, ((S - h.width) // 2, (S - h.height) // 2))
    im.save(out, optimize=True)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "episodes/branding-drawn")
    os.makedirs(out, exist_ok=True)
    banner(os.path.join(out, "banner.png"))
    avatar(os.path.join(out, "avatar.png"), os.path.join(out, "avatar-48.png"))
    watermark(os.path.join(out, "watermark.png"))
    for f in ("banner.png", "avatar.png", "avatar-48.png", "watermark.png"):
        p = os.path.join(out, f)
        print(f, Image.open(p).size, f"{os.path.getsize(p) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
