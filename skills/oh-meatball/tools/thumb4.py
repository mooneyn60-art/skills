#!/usr/bin/env python3
"""Thumbnail spec v4 (research/25-thumbnails.md), myth-list layout: one hero animal (face visible, >= 45% of
the frame height), at most one secondary animal, a 2-4 word headline whose capitals are >= 12% of the frame
height, and Meatball as head-and-shoulders bottom-left, looking at the animal. One red device at most.
Bottom-right 22% x 18% stays free for YouTube's duration stamp. Also writes 168 px and 360 px previews.

Usage: thumb4.py OUT.jpg HERO.jpg [SECOND.jpg] --headline "MOST ARE|WRONG" [--x] [--pose shock]
"""
import argparse

from PIL import Image, ImageDraw, ImageFont

from mascot import draw
from thumb3 import H, HEAVY, INK, PAPER, RED, W, cutout, red_x, sticker


def fit(im, h):
    s = h / im.height
    return im.resize((int(im.width * s), h), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("hero")
    ap.add_argument("second", nargs="?")
    ap.add_argument("--headline", required=True, help="2-4 words; '|' splits the two lines, last line is red")
    ap.add_argument("--x", action="store_true", help="red X on the secondary animal (the myth being judged)")
    ap.add_argument("--pose", default="shock")
    a = ap.parse_args()
    lines = a.headline.split("|")
    words = sum(len(x.split()) for x in lines)
    assert 2 <= words <= 4 and len(lines) <= 2, "spec v4: 2-4 words on at most 2 lines"

    c = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(c)

    hero = sticker(fit(cutout(a.hero), int(H * 0.80)), edge=12, rim=4)
    hx = W - hero.width + 30
    c.alpha_composite(hero, (hx, H - hero.height + 40))  # touches the right and bottom edges
    if a.second:
        sec = sticker(fit(cutout(a.second), int(H * 0.36)), edge=10, rim=4)
        sx, sy = max(470, hx - sec.width + 60), H - sec.height - 30
        c.alpha_composite(sec, (sx, sy))
        if a.x:  # the one red device, inside the sticker it judges
            x = red_x(int(sec.height * 0.45))
            c.alpha_composite(x, (sx + sec.width - x.width - 20, sy + 20))

    size = 150
    f = ImageFont.truetype(HEAVY, size)
    while size > 110 and max(d.textlength(x, font=f) for x in lines) > hx - 40:
        size -= 6
        f = ImageFont.truetype(HEAVY, size)
    y = 18
    for i, line in enumerate(lines):
        last = i == len(lines) - 1 and len(lines) > 1
        d.text((40, y), line, font=f, fill=RED if last else INK, stroke_width=8, stroke_fill=(255, 255, 255))
        y += int(size * 1.02)

    # Head and shoulders only, gaze toward the animal; the head is ~1/3 of the frame height.
    body = draw(a.pose, 1000, look=(11, 2)).crop((170, 160, 830, 600))
    m = sticker(body.resize((int(660 * 0.78), int(440 * 0.78)), Image.LANCZOS), edge=10, rim=4)
    top = max(y + 6, H - m.height + 30)  # never over the headline
    c.alpha_composite(m, (-20, top))

    c = c.convert("RGB")
    c.save(a.out, quality=92)
    for w in (168, 360):
        c.resize((w, int(w * H / W)), Image.LANCZOS).save(a.out.replace(".jpg", f"_{w}.jpg"))
    cap = f.getbbox("H")[3] - f.getbbox("H")[1]
    print(f"ok {a.out} words={words} cap={cap / H:.0%} of height elements={2 + bool(a.second)}")


if __name__ == "__main__":
    main()
