#!/usr/bin/env python3
"""Style sheet for the drawn look: Meatball poses, two animals, two habitats. Usage: drawn_sheet.py OUT.jpg"""
import os
import sys

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mascot  # noqa: E402
from drawn_actors import ACTORS  # noqa: E402
from drawn_assets import SCENES  # noqa: E402
from drawn_cast import ACTORS as CAST  # noqa: E402

FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "brand/fonts/Anton-Regular.ttf")


def cairo_img(w, h, draw):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(s)
    c.set_source_rgb(0.97, 0.95, 0.9)
    c.paint()
    draw(c)
    s.flush()
    a = np.ndarray((h, w, 4), np.uint8, s.get_data())
    return Image.fromarray(a[..., [2, 1, 0]].copy())


def scene(name, cam, p=None):
    def d(c):
        def layer(depth):
            c.identity_matrix()
            z = 1 + (cam[2] - 1) * depth
            c.translate(540, 960)
            c.scale(z, z)
            c.translate(-(540 + (cam[0] - 540) * depth), -(960 + (cam[1] - 960) * depth))
        SCENES[name](c, 1.0, layer, p or {})
    return cairo_img(1080, 1920, d).resize((540, 960))


def actor(fn, s, y, p, w=540, h=600):
    def d(c):
        c.translate(w / 2, y)
        c.scale(s, s)
        fn(c, 1.0, p)
    return cairo_img(w, h, d)


def main(out):
    sheet = Image.new("RGB", (2160, 2560), (247, 242, 230))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 46)
    dr.text((40, 20), "MEATBALL MYTHS: DRAWN LOOK STYLE SHEET", font=f, fill=(17, 17, 17))
    poses = [("neutral", None), ("shock", None), ("nervous", None), ("think", None), ("laugh", None),
             ("point", None), ("facepalm", None), ("deadpan", None)]
    for i, (pz, _) in enumerate(poses):
        im = mascot.draw(pz, 520, mouth="talk" if pz == "point" else None)
        x, y = 20 + (i % 4) * 535, 90 + (i // 4) * 470
        sheet.paste(im.crop((0, 60, 520, 520)), (x, y), im.crop((0, 60, 520, 520)))
        dr.text((x + 200, y + 430), pz, font=ImageFont.truetype(FONT, 30), fill=(90, 70, 50))
    h = actor(ACTORS["harvestman"], 1.0, 520, {"mood": "happy", "wave": 1.0}, 1060, 560)
    c = actor(ACTORS["cellar_spider"], 0.95, 20, {"mood": "angry", "fangs": 1.0}, 1060, 560)
    sheet.paste(h, (20, 1060))
    sheet.paste(c, (1080, 1060))
    dr.text((40, 1070), "harvestman (no venom glands)", font=ImageFont.truetype(FONT, 30), fill=(90, 70, 50))
    dr.text((1100, 1070), "cellar spider (weak venom)", font=ImageFont.truetype(FONT, 30), fill=(90, 70, 50))
    sheet.paste(scene("basement", (600, 1080, 1.1)).crop((0, 0, 540, 900)), (20, 1640))
    sheet.paste(scene("ocean", (640, 960, 0.9)).crop((0, 0, 540, 900)), (580, 1640))
    sheet.paste(scene("deep", (700, 8050, 0.9)).crop((0, 0, 540, 900)), (1140, 1640))
    b = actor(CAST["billionaire"], 0.5, 560, {"arm": "up", "item": "rock"}, 440, 600)
    sheet.paste(b.crop((0, 40, 440, 600)).resize((440, 560)), (1700, 1660))
    dr.text((1740, 2240), "generic tycoon", font=ImageFont.truetype(FONT, 30), fill=(90, 70, 50))
    sheet.save(out, quality=90)
    print("ok", out)


if __name__ == "__main__":
    main(sys.argv[1])
