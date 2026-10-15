"""Five 2000x2000 listing images per product, composed from real renders of the PDF pages.

01 cover mockup, 02 inside pages, 03 what's included, 04 sizes, 05 how it works.
Everything is drawn at 2x and downsampled once, so edges are anti-aliased.
"""

import glob
import math
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .kit import FONT_DIR, THEMES

OUT = 2000
SS = 2
S = OUT * SS


def rgb(hex_value, alpha=255):
    h = hex_value.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def font(name, size):
    files = {"display": "YoungSerif-Regular.ttf", "head": "BricolageGrotesque-Bold.ttf",
             "body": "WorkSans-Regular.ttf", "bold": "WorkSans-Bold.ttf", "italic": "WorkSans-Italic.ttf"}
    return ImageFont.truetype(os.path.join(FONT_DIR, files[name]), int(size * SS))


def render_pages(pdf, dpi=110, first_only=False):
    """Render PDF pages to PNG; returns PIL images (RGB)."""
    tmp = tempfile.mkdtemp(prefix="pages-")
    rng = ["-f", "1", "-l", "1"] if first_only else []
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), *rng, pdf, os.path.join(tmp, "p")], check=True)
    files = sorted(glob.glob(os.path.join(tmp, "p-*.png")), key=lambda p: int(p.rsplit("-", 1)[1].split(".")[0]))
    return [Image.open(f).convert("RGB") for f in files]


class Board:
    def __init__(self, theme):
        self.t = THEMES[theme]
        self.img = Image.new("RGBA", (S, S), rgb(self.t["paper"]))
        self.d = ImageDraw.Draw(self.img)
        self.pattern()

    def pattern(self):
        """Faint scattered ornaments so the background is not flat."""
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        cols = [self.t["primary"], self.t["secondary"], self.t["accent"]]
        k = 0
        for gy in range(9):
            for gx in range(9):
                k += 1
                x = (gx + 0.5 + (0.35 if gy % 2 else 0)) * S / 9
                y = (gy + 0.5) * S / 9
                r = S * (0.010 + 0.006 * (k * 7 % 4))
                self.motif(d, x, y, r, rgb(cols[k % 3], 26), (k * 37) % 360)
        self.img.alpha_composite(layer)

    def motif(self, d, x, y, r, col, rot=0):
        kind = self.t["ornament"]
        a0 = math.radians(rot)
        if kind == "snowflake":
            for k in range(6):
                a = a0 + math.pi / 3 * k
                d.line([(x, y), (x + r * math.cos(a), y + r * math.sin(a))], fill=col, width=int(r * 0.16))
                bx, by = x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a)
                for s in (-1, 1):
                    b = a + s * math.pi / 4
                    d.line([(bx, by), (bx + r * 0.32 * math.cos(b), by + r * 0.32 * math.sin(b))], fill=col, width=int(r * 0.14))
        elif kind == "star":
            pts = []
            for k in range(10):
                a = a0 - math.pi / 2 + k * math.pi / 5
                rr = r if k % 2 == 0 else r * 0.45
                pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
            d.polygon(pts, fill=col)
        elif kind == "leaf":
            pts = []
            for k in range(40):
                u = k / 39 * math.pi * 2
                px, py = r * math.cos(u), r * 0.45 * math.sin(u) * (1 + 0.3 * math.cos(u))
                pts.append((x + px * math.cos(a0) - py * math.sin(a0), y + px * math.sin(a0) + py * math.cos(a0)))
            d.polygon(pts, fill=col)
        else:
            d.ellipse([x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4], fill=col)

    # helpers in output (2000) coordinates
    def text(self, xy, s, f, fill, anchor="mm"):
        self.d.text((xy[0] * SS, xy[1] * SS), s, font=f, fill=fill, anchor=anchor)

    def fit_font(self, s, name, size, max_w):
        while size > 20:
            f = font(name, size)
            if self.d.textlength(s, font=f) <= max_w * SS:
                return f
            size -= 4
        return font(name, size)

    def rrect(self, box, r, fill=None, outline=None, width=1):
        self.d.rounded_rectangle([v * SS for v in box], radius=r * SS, fill=fill, outline=outline, width=width * SS)

    def circle(self, cx, cy, r, fill=None, outline=None, width=1):
        self.d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=fill, outline=outline, width=width * SS)

    def paste_page(self, page, cx, cy, height, angle=0, border=True):
        """Place a rendered page centred at (cx, cy) with a soft drop shadow."""
        hh = int(height * SS)
        ww = int(page.width * hh / page.height)
        pg = page.resize((ww, hh), Image.LANCZOS).convert("RGBA")
        if border:
            ImageDraw.Draw(pg).rectangle([0, 0, ww - 1, hh - 1], outline=(0, 0, 0, 40), width=2)
        pad = int(60 * SS)
        shadow = Image.new("RGBA", (ww + 2 * pad, hh + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rectangle([pad, pad, pad + ww, pad + hh], fill=(40, 30, 20, 95))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18 * SS))
        if angle:
            pg = pg.rotate(angle, resample=Image.BICUBIC, expand=True)
            shadow = shadow.rotate(angle, resample=Image.BICUBIC, expand=True)
        sx, sy = int(cx * SS - shadow.width / 2 + 10 * SS), int(cy * SS - shadow.height / 2 + 22 * SS)
        self._composite_clipped(shadow, sx, sy)
        self._composite_clipped(pg, int(cx * SS - pg.width / 2), int(cy * SS - pg.height / 2))
        return ww / SS, hh / SS

    def _composite_clipped(self, layer, x, y):
        canvas = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        canvas.paste(layer, (x, y), layer)
        self.img.alpha_composite(canvas)

    def headline(self, title, sub=None, y=170):
        f = self.fit_font(title, "display", 118, 1760)
        self.text((1000, y), title, f, rgb(self.t["primary"]))
        if sub:
            fs = self.fit_font(sub, "bold", 46, 1700)
            self.text((1000, y + 112), sub, fs, rgb(self.t["secondary"]))

    def pill(self, cx, cy, label, fill, color=(255, 255, 255, 255), size=40):
        f = font("bold", size)
        tw = self.d.textlength(label, font=f) / SS
        self.rrect((cx - tw / 2 - 34, cy - size * 0.95, cx + tw / 2 + 34, cy + size * 0.95), size * 0.95, fill=fill)
        self.text((cx, cy), label, f, color)

    def save(self, path):
        self.img.resize((OUT, OUT), Image.LANCZOS).convert("RGB").save(path, "JPEG", quality=92, optimize=True)


def check_mark(b, cx, cy, r, color):
    b.circle(cx, cy, r, fill=color)
    pts = [(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.12, cy + r * 0.35), (cx + r * 0.48, cy - r * 0.32)]
    b.d.line([(x * SS, y * SS) for x, y in pts], fill=(255, 255, 255, 255), width=int(r * 0.24 * SS), joint="curve")


def image_cover(spec, pages, path):
    b = Board(spec["theme"])
    t = b.t
    hero = spec["hero"]
    b.headline(hero["headline"], hero["sub"], y=175)
    back = [pages[i] for i in spec["preview_pages"][:2]]
    b.paste_page(back[1], 1290, 1210, 1240, angle=-7)
    b.paste_page(back[0], 710, 1210, 1240, angle=7)
    b.paste_page(pages[0], 1000, 1180, 1300)
    b.circle(1640, 520, 150, fill=rgb(t["secondary"]))
    b.circle(1640, 520, 136, outline=rgb("#FFFFFF", 200), width=3)
    for i, line in enumerate(hero.get("badge", ["INSTANT", "DOWNLOAD"])):
        b.text((1640, 520 + (i - (len(hero.get("badge", [1, 2])) - 1) / 2) * 52), line, font("bold", 40), (255, 255, 255, 255))
    b.pill(1000, 1905, hero.get("strip", "PRINTABLE PDF  ·  US LETTER + A4"), rgb(t["primary"]), size=38)
    b.save(path)


def image_inside(spec, pages, path):
    b = Board(spec["theme"])
    b.headline("Peek Inside", spec["hero"].get("inside_sub", "Clean, large, easy-to-read pages"), y=165)
    a, c = (pages[i] for i in spec["inside_pages"][:2])
    b.paste_page(a, 525, 1080, 1170)
    b.paste_page(c, 1475, 1080, 1170)
    caps = spec["hero"].get("inside_captions")
    if caps:
        for x, cap in zip((530, 1470), caps):
            b.pill(x, 1815, cap, rgb(b.t["primary"]), size=34)
    b.save(path)


def image_included(spec, pages, path):
    b = Board(spec["theme"])
    t = b.t
    b.headline("What's Included", None, y=150)
    idx = spec["included_pages"][:3]
    for k, i in enumerate(idx):
        b.paste_page(pages[i], 400 + k * 600, 650, 690)
    items = spec["included"]
    b.rrect((120, 1060, 1880, 1900), 46, fill=rgb("#FFFFFF", 235), outline=rgb(t["accent"]), width=3)
    cols = 1 if len(items) <= 6 else 2
    per = -(-len(items) // cols)
    row_h = min(120, 760 / per)
    size = 46 if cols == 1 else 40
    for k, item in enumerate(items):
        col, row = divmod(k, per)
        x = 210 + col * 850
        y = 1140 + row * row_h + row_h / 2 - 20
        check_mark(b, x, y, 26, rgb(t["secondary"]))
        f = b.fit_font(item, "body", size, (1600 if cols == 1 else 760) - 60)
        b.text((x + 52, y), item, f, rgb(t["ink"]), anchor="lm")
    b.save(path)


def image_sizes(spec, pages, path, a4_cover=None):
    b = Board(spec["theme"])
    t = b.t
    b.headline("Two Paper Sizes", "BOTH FILES INCLUDED WITH YOUR PURCHASE", y=165)
    letter_h = 1060
    a4_h = letter_h * (297 / 279.4)
    for cx, h, pg, lab, dim in ((545, letter_h, pages[0], "US LETTER", "8.5 x 11 inches"),
                                (1455, a4_h, a4_cover or pages[0], "A4", "210 x 297 mm")):
        cy = 1030 + (a4_h - h) / 2
        b.paste_page(pg, cx, cy, h)
        b.text((cx, 1760), lab, font("head", 70), rgb(t["primary"]))
        b.text((cx, 1835), dim, font("body", 44), rgb(t["ink"]))
    b.save(path)


def image_how(spec, pages, path):
    b = Board(spec["theme"])
    t = b.t
    b.headline("How It Works", "INSTANT DIGITAL DOWNLOAD", y=165)
    steps = [("Purchase", "Check out on Etsy. Your files are ready the moment payment completes."),
             ("Download", "Go to You > Purchases and reviews and click Download Files. Etsy emails you a link too."),
             ("Print & Enjoy", spec["hero"].get("how_last", "Print at home or at any print shop, as many copies as you need for your own use."))]
    for k, (head, body) in enumerate(steps):
        y0 = 430 + k * 390
        b.rrect((150, y0, 1850, y0 + 330), 50, fill=rgb("#FFFFFF", 240), outline=rgb(t["accent"]), width=3)
        b.circle(310, y0 + 165, 105, fill=rgb([t["primary"], t["secondary"], t["primary"]][k]))
        b.text((310, y0 + 170), str(k + 1), font("display", 110), (255, 255, 255, 255))
        b.text((470, y0 + 105), head, font("head", 66), rgb(t["primary"]), anchor="lm")
        f = font("body", 40)
        words, lines, cur = body.split(), [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if b.d.textlength(trial, font=f) / SS > 1300:
                lines.append(cur)
                cur = wd
            else:
                cur = trial
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            b.text((470, y0 + 185 + j * 54), ln, f, rgb(t["ink"]), anchor="lm")
    b.text((1000, 1660), "This is a digital product. No physical item will be shipped.", font("italic", 42), rgb(t["ink"]))
    b.pill(1000, 1800, "PDF  ·  US LETTER + A4  ·  PRINT AT HOME", rgb(t["secondary"]), size=38)
    b.save(path)


def make_all(spec, pdf_letter, pdf_a4, out_dir):
    pages = render_pages(pdf_letter)
    a4_cover = render_pages(pdf_a4, first_only=True)[0]
    paths = []
    for k, fn in enumerate((image_cover, image_inside, image_included, image_sizes, image_how), 1):
        p = os.path.join(out_dir, f"{k:02d}-{fn.__name__.split('_', 1)[1]}.jpg")
        if fn is image_sizes:
            fn(spec, pages, p, a4_cover)
        else:
            fn(spec, pages, p)
        paths.append(p)
    return paths
