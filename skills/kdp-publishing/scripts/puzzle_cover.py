"""Draw a full-wrap KDP paperback cover for a puzzle book, entirely in code (no AI art).

Reads the same JSON spec as word_search_book.py plus a "cover" block:
  "cover": {
    "pattern": "quilt" | "yarn" | "honeycomb",
    "palette": ["#B5443A", "#E8B04B", "#3E6E8E", "#7A9E5A", "#F2E3C6"],
    "headline": ["QUILTING", "WORD SEARCH"],
    "tagline": "60 Easy-to-Read Puzzles\\nfor Quilters, Adults & Seniors",   # \\n forces a line break
    "back_title": "...", "back_text": "...", "bullets": ["...", "..."]
  }

Usage:
  python puzzle_cover.py book.json --pages 82 --paper white -o cover.pdf
"""

import argparse
import json
import math
import random

from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

import kdp_specs as kdp
from cover_calc import cover_dimensions
from format_interior import register_fonts
from word_search_book import ALL_DIRS, EASY_DIRS, draw_grid, make_puzzle

INCH = 72
CREAM = HexColor("#FBF6EC")
INK = HexColor("#2B2B2B")


def pattern_quilt(c, x, y, w, h, palette, rng, size=0.85 * INCH):
    """Half-square-triangle quilt blocks."""
    cols, rows = math.ceil(w / size) + 1, math.ceil(h / size) + 1
    for i in range(cols):
        for j in range(rows):
            bx, by = x + i * size, y + j * size
            a, b = rng.sample(palette, 2)
            c.setFillColor(HexColor(a))
            c.rect(bx, by, size, size, stroke=0, fill=1)
            c.setFillColor(HexColor(b))
            p = c.beginPath()
            if (i + j) % 2:
                p.moveTo(bx, by); p.lineTo(bx + size, by); p.lineTo(bx + size, by + size)
            else:
                p.moveTo(bx, by + size); p.lineTo(bx, by); p.lineTo(bx + size, by)
            p.close()
            c.drawPath(p, stroke=0, fill=1)
            c.setStrokeColor(white)
            c.setLineWidth(1)
            c.setDash(2, 2)
            c.rect(bx + 4, by + 4, size - 8, size - 8, stroke=1, fill=0)
            c.setDash()


def pattern_yarn(c, x, y, w, h, palette, rng, size=0.32 * INCH):
    """Rows of knit 'V' stitches in striped colors."""
    rows = math.ceil(h / (size * 0.8)) + 1
    cols = math.ceil(w / size) + 1
    for j in range(rows):
        color = HexColor(palette[(j // 3) % len(palette)])
        c.setFillColor(color)
        c.rect(x, y + j * size * 0.8, w, size * 0.8 + 1, stroke=0, fill=1)
        c.setStrokeColor(HexColor("#FFFFFF"))
        c.setStrokeAlpha(0.45)
        c.setLineWidth(2)
        for i in range(cols):
            cx, cy = x + i * size, y + j * size * 0.8
            c.bezier(cx, cy + size * 0.8, cx + size * 0.15, cy + size * 0.3, cx + size * 0.35, cy + size * 0.1, cx + size * 0.5, cy)
            c.bezier(cx + size, cy + size * 0.8, cx + size * 0.85, cy + size * 0.3, cx + size * 0.65, cy + size * 0.1, cx + size * 0.5, cy)
        c.setStrokeAlpha(1)


def pattern_honeycomb(c, x, y, w, h, palette, rng, r=0.42 * INCH):
    """Honeycomb hexagons, a few filled with 'honey'."""
    dx, dy = r * math.sqrt(3), r * 1.5
    c.setFillColor(HexColor(palette[0]))
    c.rect(x, y, w, h, stroke=0, fill=1)
    for j in range(int(h / dy) + 2):
        for i in range(int(w / dx) + 2):
            cx = x + i * dx + (dx / 2 if j % 2 else 0)
            cy = y + j * dy
            p = c.beginPath()
            for k in range(6):
                ang = math.radians(60 * k + 30)
                px, py = cx + r * 0.92 * math.cos(ang), cy + r * 0.92 * math.sin(ang)
                p.moveTo(px, py) if k == 0 else p.lineTo(px, py)
            p.close()
            c.setFillColor(HexColor(rng.choice(palette[1:])))
            c.setStrokeColor(HexColor(palette[0]))
            c.setLineWidth(3)
            c.drawPath(p, stroke=1, fill=1)


def draw_pumpkin(c, cx, cy, r, orange, stem):
    c.setFillColor(stem)
    c.roundRect(cx - r * 0.12, cy + r * 0.7, r * 0.24, r * 0.45, r * 0.08, stroke=0, fill=1)
    c.setFillColor(orange)
    c.setStrokeColor(HexColor("#9A4A12"))
    c.setLineWidth(max(1, r * 0.06))
    for dx, rx in ((-0.45, 0.6), (0.45, 0.6), (0, 0.62)):
        c.ellipse(cx + (dx - rx) * r, cy - 0.8 * r, cx + (dx + rx) * r, cy + 0.8 * r, stroke=1, fill=1)


def draw_bat(c, cx, cy, s, color):
    c.setFillColor(color)
    p = c.beginPath()
    pts = [(-1, 0.2), (-0.7, 0.35), (-0.45, 0.1), (-0.2, 0.25), (-0.1, 0.45), (0, 0.3), (0.1, 0.45), (0.2, 0.25),
           (0.45, 0.1), (0.7, 0.35), (1, 0.2), (0.65, -0.05), (0.4, -0.3), (0.2, -0.1), (0, -0.35), (-0.2, -0.1),
           (-0.4, -0.3), (-0.65, -0.05)]
    p.moveTo(cx + pts[0][0] * s, cy + pts[0][1] * s)
    for px, py in pts[1:]:
        p.lineTo(cx + px * s, cy + py * s)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def pattern_halloween(c, x, y, w, h, palette, rng, step=1.15 * INCH):
    """Night sky with pumpkins, bats and stars. Palette: orange, night, purple, gold, green, cream."""
    orange, night, purple, gold, green = (HexColor(v) for v in palette[:5])
    c.setFillColor(night)
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.setFillColor(gold)
    for _ in range(int(w * h / (0.35 * INCH) ** 2)):
        c.circle(x + rng.random() * w, y + rng.random() * h, rng.choice((0.8, 1.2, 1.8)), stroke=0, fill=1)
    for j in range(int(h / step) + 2):
        for i in range(int(w / step) + 2):
            cx = x + i * step + (step / 2 if j % 2 else 0) + rng.uniform(-8, 8)
            cy = y + j * step + rng.uniform(-8, 8)
            if (i + j) % 3 == 0:
                draw_bat(c, cx, cy, step * 0.28, purple)
            else:
                draw_pumpkin(c, cx, cy, step * rng.uniform(0.2, 0.28), orange, green)


def draw_snowflake(c, cx, cy, r, color):
    c.setStrokeColor(color)
    c.setLineWidth(max(0.8, r * 0.12))
    c.setLineCap(1)
    for k in range(6):
        ang = math.radians(60 * k)
        ex, ey = cx + r * math.cos(ang), cy + r * math.sin(ang)
        c.line(cx, cy, ex, ey)
        for side in (-1, 1):
            bx, by = cx + 0.6 * r * math.cos(ang), cy + 0.6 * r * math.sin(ang)
            b = ang + side * math.radians(40)
            c.line(bx, by, bx + 0.3 * r * math.cos(b), by + 0.3 * r * math.sin(b))


def draw_tree(c, cx, cy, s, green, star, trunk):
    c.setFillColor(trunk)
    c.rect(cx - s * 0.08, cy - s * 0.55, s * 0.16, s * 0.18, stroke=0, fill=1)
    c.setFillColor(green)
    for tier, (w, y0) in enumerate(((0.55, -0.4), (0.42, -0.1), (0.3, 0.18))):
        p = c.beginPath()
        p.moveTo(cx - w * s, cy + y0 * s)
        p.lineTo(cx + w * s, cy + y0 * s)
        p.lineTo(cx, cy + (y0 + 0.42) * s)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(star)
    c.circle(cx, cy + 0.62 * s, s * 0.07, stroke=0, fill=1)


def draw_ornament(c, cx, cy, r, color, cap):
    c.setFillColor(cap)
    c.rect(cx - r * 0.3, cy + r * 0.85, r * 0.6, r * 0.3, stroke=0, fill=1)
    c.setFillColor(color)
    c.circle(cx, cy, r, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#FFFFFF"))
    c.setStrokeAlpha(0.5)
    c.setLineWidth(max(1, r * 0.15))
    c.arc(cx - r * 0.6, cy - r * 0.1, cx + r * 0.2, cy + r * 0.7, 100, 80)
    c.setStrokeAlpha(1)


def pattern_christmas(c, x, y, w, h, palette, rng, step=1.1 * INCH):
    """Pine trees, ornaments and snowflakes. Palette: red, deep green, green, gold, white."""
    red, night, green, gold, snow = (HexColor(v) for v in palette[:5])
    c.setFillColor(night)
    c.rect(x, y, w, h, stroke=0, fill=1)
    for _ in range(int(w * h / (0.5 * INCH) ** 2)):
        draw_snowflake(c, x + rng.random() * w, y + rng.random() * h, rng.uniform(3, 7), snow)
    for j in range(int(h / step) + 2):
        for i in range(int(w / step) + 2):
            cx = x + i * step + (step / 2 if j % 2 else 0) + rng.uniform(-6, 6)
            cy = y + j * step + rng.uniform(-6, 6)
            kind = (i + 2 * j) % 3
            if kind == 0:
                draw_tree(c, cx, cy, step * 0.55, green, gold, HexColor("#6B4423"))
            elif kind == 1:
                draw_ornament(c, cx, cy, step * 0.18, rng.choice((red, gold)), gold)
            else:
                draw_snowflake(c, cx, cy, step * 0.2, snow)


PATTERNS = {"quilt": pattern_quilt, "yarn": pattern_yarn, "honeycomb": pattern_honeycomb,
            "halloween": pattern_halloween, "christmas": pattern_christmas}


def clip_rect(c, x, y, w, h):
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)


def text_block(c, text, x, y, width, font, size, leading=None, color=INK):
    leading = leading or size * 1.35
    c.setFillColor(color)
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def fit_size(text, font, max_size, width):
    from reportlab.pdfbase.pdfmetrics import stringWidth

    size = max_size
    while stringWidth(text, font, size) > width and size > 10:
        size -= 1
    return size


def draw_cover(spec, pages, paper, out):
    cov = spec["cover"]
    font = register_fonts(sans=True)
    bold, reg = f"{font}-Bold", f"{font}-Regular"
    dims = cover_dimensions(spec.get("trim", "8.5x11"), pages, paper)
    b, tw, th, sp = kdp.BLEED, dims["trim_width_in"], dims["trim_height_in"], dims["spine_width_in"]
    W, H = dims["full_cover_width_in"] * INCH, dims["full_cover_height_in"] * INCH
    palette = cov["palette"]
    accent = HexColor(palette[0])
    rng = random.Random(spec.get("seed", 1))
    c = canvas.Canvas(out, pagesize=(W, H), initialFontName=reg)
    c.setTitle(f"{spec['title']} cover")

    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    front_x = (b + tw + sp) * INCH
    front_w = (tw + b) * INCH
    safe = (kdp.COVER_SAFE_MARGIN + 0.25) * INCH

    band_h = H * 0.42
    c.saveState()
    clip_rect(c, front_x, H - band_h, front_w, band_h)
    PATTERNS[cov["pattern"]](c, front_x, H - band_h, front_w, band_h, palette, rng)
    c.restoreState()
    c.saveState()
    clip_rect(c, front_x, 0, front_w, 1.1 * INCH + b * INCH)
    PATTERNS[cov["pattern"]](c, front_x, 0, front_w, 1.1 * INCH + b * INCH, palette, rng)
    c.restoreState()

    inner_left = front_x + safe
    inner_w = tw * INCH - 2 * safe
    panel_top = H - band_h + 0.9 * INCH
    panel_h = 3.6 * INCH
    c.setFillColor(white)
    c.setStrokeColor(accent)
    c.setLineWidth(5)
    c.roundRect(inner_left, panel_top - panel_h, inner_w, panel_h, 0.25 * INCH, stroke=1, fill=1)
    y = panel_top - 1.15 * INCH
    lead = fit_size(cov["headline"][0], bold, 78, inner_w - 0.5 * INCH)
    for k, line in enumerate(cov["headline"]):
        size = lead if k == 0 else fit_size(line, bold, min(54, max(40, lead * 0.72)), inner_w - 0.5 * INCH)
        c.setFillColor(accent if k == 0 else INK)
        c.setFont(bold, size)
        c.drawCentredString(inner_left + inner_w / 2, y, line)
        y -= max(size, 46) * 1.2
    c.setFillColor(HexColor(palette[2]))
    c.roundRect(inner_left + inner_w / 2 - 1.5 * INCH, panel_top - panel_h + 0.3 * INCH, 3 * INCH, 0.6 * INCH,
                0.3 * INCH, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont(bold, 26)
    c.drawCentredString(inner_left + inner_w / 2, panel_top - panel_h + 0.49 * INCH, "LARGE PRINT")

    tag_y = panel_top - panel_h - 0.65 * INCH
    size = 21
    c.setFillColor(INK)
    c.setFont(bold, size)
    lines = [l for part in cov["tagline"].split("\n") for l in simpleSplit(part, bold, size, inner_w - 0.3 * INCH)]
    for line in lines:
        c.drawCentredString(inner_left + inner_w / 2, tag_y, line)
        tag_y -= 30
    c.setFont(reg, 17)
    c.drawCentredString(inner_left + inner_w / 2, tag_y - 8, "Big letters  •  Easy to read  •  Solutions included")
    c.setFillColor(white)
    c.setFillAlpha(0.9)
    c.roundRect(inner_left + inner_w / 2 - 1.6 * INCH, 0.45 * INCH, 3.2 * INCH, 0.45 * INCH, 0.2 * INCH, stroke=0, fill=1)
    c.setFillAlpha(1)
    c.setFillColor(INK)
    c.setFont(bold, 15)
    c.drawCentredString(inner_left + inner_w / 2, 0.6 * INCH, spec["author"])

    c.setFillColor(accent)
    c.rect((b + tw) * INCH, 0, sp * INCH, H, stroke=0, fill=1)

    back_x = 0
    back_w = (b + tw) * INCH
    c.saveState()
    clip_rect(c, back_x, 0, back_w, H)
    PATTERNS[cov["pattern"]](c, back_x, 0, back_w, H, palette, rng)
    c.restoreState()
    bl = (b + kdp.COVER_SAFE_MARGIN + 0.3) * INCH
    bw = tw * INCH - 2 * (kdp.COVER_SAFE_MARGIN + 0.3) * INCH
    c.setFillColor(white)
    c.roundRect(bl - 0.25 * INCH, 2.0 * INCH, bw + 0.5 * INCH, H - 3.0 * INCH, 0.25 * INCH, stroke=0, fill=1)
    y = H - 1.6 * INCH
    c.setFillColor(accent)
    c.setFont(bold, fit_size(cov["back_title"], bold, 30, bw))
    c.drawString(bl, y, cov["back_title"])
    y = text_block(c, cov["back_text"], bl, y - 0.55 * INCH, bw, reg, 16, 23) - 0.2 * INCH
    c.setFillColor(INK)
    c.setFont(bold, 18)
    c.drawString(bl, y, "Inside you'll find:")
    y -= 0.42 * INCH
    for item in cov["bullets"]:
        c.setFillColor(accent)
        c.circle(bl + 5, y + 5, 4, stroke=0, fill=1)
        y = text_block(c, item, bl + 18, y, bw - 18, reg, 16, 22) - 8
    sample = spec["puzzles"][0]
    grid, _ = make_puzzle(sample["words"], spec.get("grid", 15),
                          EASY_DIRS if spec.get("directions", "easy") == "easy" else ALL_DIRS, random.Random(spec.get("seed", 1)))
    room = y - 2.35 * INCH
    if room > 2 * INCH:
        cell = min(room - 0.5 * INCH, bw * 0.75) / len(grid)
        gx = bl + (bw - cell * len(grid)) / 2
        c.setFillColor(INK)
        c.setFont(bold, 13)
        c.drawCentredString(bl + bw / 2, y - 0.1 * INCH, f"Sample puzzle: {sample['title']}")
        draw_grid(c, grid, gx, y - 0.4 * INCH, cell, font, cell * 0.6)
    c.setFillColor(white)
    c.rect(back_w - (b + 0.25 + 2.0) * INCH, (b + 0.25) * INCH, 2.0 * INCH, 1.2 * INCH, stroke=0, fill=1)

    c.showPage()
    c.save()
    return dims


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec")
    p.add_argument("--pages", type=int, required=True)
    p.add_argument("--paper", default="white", choices=sorted(kdp.PAPER_THICKNESS))
    p.add_argument("-o", "--output", default="cover.pdf")
    a = p.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    dims = draw_cover(spec, a.pages, a.paper, a.output)
    print(json.dumps({"output": a.output, **{k: dims[k] for k in
                      ("full_cover_width_in", "full_cover_height_in", "spine_width_in", "pages", "paper")}}, indent=2))


if __name__ == "__main__":
    main()
