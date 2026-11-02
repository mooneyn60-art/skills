#!/usr/bin/env python3
"""Project Azorian long-form thumbnails (research/61 change 1 + 2), built from the drawn kit (thumb_v3 helpers).

A: the whole K-129 as a black silhouette with a red star, ~40% of the frame, gripped in the drawn claw, Meatball's
   horrified face, "STEAL A SUB?!". B: A plus a small inset of the CIA's AZORIAN painting under a red
   DECLASSIFIED stamp (the case-file look's one real archive element).
Usage: thumb_azorian.py OUTDIR [--photo CIA_PAINTING.jpg]   -> thumb.jpg, thumb_168.jpg, thumb_b.jpg, thumb_b_168.jpg
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import thumb_v3 as T  # noqa: E402
import drawn_cast  # noqa: E402

RED = (226, 30, 36)


def silhouette(im, col=(12, 12, 14)):
    a = im.split()[3].point(lambda v: 255 if v > 30 else 0)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", im.size, col + (255,)), (0, 0), a)
    return out


def star(d, cx, cy, r, col=RED):
    import math
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = -math.pi / 2 + k * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)


def hero():
    """Black K-129 (bow right) with a red star on the sail, gripped in the closed yellow claw."""
    sub = silhouette(T.actor(drawn_cast.sub, {"missiles": 0}, 1.0, 2600, 1400, 1300, 900))
    star(ImageDraw.Draw(sub), sub.width * 0.575, sub.height * 0.27, sub.height * 0.17)
    claw = T.actor(drawn_cast.claw, {"close": 1.0}, 1.0, 2000, 5000, 1000, 4300)
    claw = claw.crop((0, claw.height - 1000, claw.width, claw.height))   # frame + fingers, a stub of pipe
    claw = claw.resize((int(claw.width * 0.8), 800), Image.LANCZOS)
    pad = 100
    cv = Image.new("RGBA", (sub.width + 2 * pad, 800 + sub.height), (0, 0, 0, 0))
    cv.alpha_composite(claw, (pad + int(sub.width * 0.55) - claw.width // 2, 0))
    cx = pad + int(sub.width * 0.55) - claw.width // 2
    cv.alpha_composite(sub, (pad, 800 - 420))   # the hull sits in the closed fingers
    tips = claw.crop((0, 640, claw.width, claw.height))   # finger hooks drawn again over the lower hull: gripped
    cv.alpha_composite(tips, (cx, 640))
    return T.pop(cv.crop(cv.getbbox()), 8, 9, (235, 245, 255), 30, (120, 190, 255))


def stamp_inset(cv, photo, x, y, w):
    im = Image.open(photo).convert("RGB")
    h = int(w * 0.68)
    k = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    card = Image.new("RGBA", (w + 24, h + 24), (246, 244, 236, 255))
    card.paste(im, (12, 12))
    lay = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    lay.alpha_composite(card, (30, 30))
    f = ImageFont.truetype(T.ANTON, 10)
    for size in range(90, 20, -2):   # the stamp spans the print's width
        f = ImageFont.truetype(T.ANTON, size)
        if ImageDraw.Draw(Image.new("L", (1, 1))).textlength("DECLASSIFIED", font=f) < w * 0.92:
            break
    tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength("DECLASSIFIED", font=f))
    st = Image.new("RGBA", (tw + 40, int(size * 1.45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.rounded_rectangle([4, 4, st.width - 4, st.height - 4], 10, fill=(255, 255, 255, 60), outline=RED, width=7)
    d.text((st.width / 2, st.height / 2), "DECLASSIFIED", font=f, fill=RED, anchor="mm")
    st = st.rotate(-14, expand=True, resample=Image.BICUBIC)
    lay.alpha_composite(st, ((lay.width - st.width) // 2, (lay.height - st.height) // 2))
    lay = lay.rotate(5, expand=True, resample=Image.BICUBIC)
    cv.alpha_composite(lay, (x, y))


def make(photo=None):
    cv = T.radial(T.W, T.H, (36, 84, 130), (6, 14, 30), cx=0.68, cy=0.45, r=0.85)
    d = ImageDraw.Draw(cv)
    for x, y, r in ((560, 300, 7), (600, 250, 5), (700, 120, 6), (1180, 210, 7), (1215, 420, 6), (520, 560, 5)):
        d.ellipse([x - r, y - r, x + r, y + r], outline=(170, 215, 255), width=3)
    if photo:
        stamp_inset(cv, photo, 985, 8, 230)
    h = hero()
    T.paste_c(cv, T.fit(h, 740, 560), 900, 420, rot=-4)
    T.words(cv, "STEAL A SUB?!", 40, 22, 150, T.YEL, max_w=760)
    mb = T.pop(T.fit(T.meatball("shock", 1000, look=(16, -6), head=0.5), h=420), 8, 8, T.WHITE, 20)
    cv.alpha_composite(mb, (20, T.H - mb.height - 10))
    T.badge(cv, "INVESTIGATES", 22, T.H - 100, 74, (90, 220, 120), T.INK, icon="mag")
    return cv.convert("RGB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--photo")
    a = ap.parse_args()
    for name, ph in (("thumb", None), ("thumb_b", a.photo)):
        if name == "thumb_b" and not ph:
            continue
        im = make(ph)
        im.save(f"{a.out}/{name}.jpg", quality=90)
        im.resize((168, 94), Image.LANCZOS).save(f"{a.out}/{name}_168.jpg", quality=92)
