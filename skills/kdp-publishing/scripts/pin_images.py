"""Make Pinterest-size (1000x1500 px) sample-puzzle images for a word search book.

Each pin shows one real puzzle from the book with a "Can you find them all?" hook,
the book's cover pattern as a header band, and a footer naming the book.

Usage:
  python pin_images.py book.json --puzzles 1 13 48 -o pins/
"""

import argparse
import json
import os
import random

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

from format_interior import register_fonts
from puzzle_cover import INK, PATTERNS, clip_rect, fit_size
from word_search_book import ALL_DIRS, EASY_DIRS, draw_grid, make_puzzle

W, H = 1000, 1500


def draw_pin(spec, index, font, path_pdf):
    cov = spec["cover"]
    rng = random.Random(spec.get("seed", 1))
    dirs = EASY_DIRS if spec.get("directions", "easy") == "easy" else ALL_DIRS
    # Rebuild puzzles in book order so each pin shows the exact grid printed in the book.
    puzzles = [make_puzzle(p["words"], spec.get("grid", 15), dirs, rng) for p in spec["puzzles"][:index]]
    grid, _ = puzzles[index - 1]
    puzzle = spec["puzzles"][index - 1]

    c = canvas.Canvas(path_pdf, pagesize=(W, H), initialFontName=f"{font}-Regular")
    c.setFillColor(HexColor("#FBF6EC"))
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.saveState()
    clip_rect(c, 0, H - 260, W, 260)
    PATTERNS[cov["pattern"]](c, 0, H - 260, W, 260, cov["palette"], random.Random(index))
    c.restoreState()

    c.setFillColor(white)
    c.roundRect(60, H - 230, W - 120, 170, 24, stroke=0, fill=1)
    c.setFillColor(HexColor(cov["palette"][0]))
    hook = f"Can you find all {len(puzzle['words'])} words?"
    c.setFont(f"{font}-Bold", fit_size(hook, f"{font}-Bold", 58, W - 180))
    c.drawCentredString(W / 2, H - 135, hook)
    c.setFillColor(INK)
    c.setFont(f"{font}-Regular", 34)
    c.drawCentredString(W / 2, H - 195, puzzle["title"])

    n = len(grid)
    cell = 54
    x0 = (W - n * cell) / 2
    draw_grid(c, grid, x0, H - 330, cell, font, cell * 0.6)

    words = sorted(w.upper() for w in puzzle["words"])
    cols, rows = 3, -(-len(words) // 3)
    col_w = (W - 120) / cols
    y0 = H - 330 - n * cell - 70
    for k, w in enumerate(words):
        col, row = divmod(k, rows)
        c.setFont(f"{font}-Regular", fit_size(w, f"{font}-Regular", 26, col_w - 20))
        c.drawString(60 + col * col_w, y0 - row * 40, w)

    c.setFillColor(HexColor(cov["palette"][0]))
    c.rect(0, 0, W, 110, stroke=0, fill=1)
    c.setFillColor(white)
    footer = f"{spec['title']}  •  Large Print  •  on Amazon"
    c.setFont(f"{font}-Bold", fit_size(footer, f"{font}-Bold", 36, W - 80))
    c.drawCentredString(W / 2, 42, footer)
    c.showPage()
    c.save()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec")
    p.add_argument("--puzzles", type=int, nargs="+", default=[1, 2, 3], help="1-based puzzle numbers")
    p.add_argument("-o", "--outdir", default="pins")
    a = p.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    import pymupdf

    font = register_fonts(sans=True)
    os.makedirs(a.outdir, exist_ok=True)
    out = []
    for idx in a.puzzles:
        pdf = os.path.join(a.outdir, f"pin_{idx:02}.pdf")
        draw_pin(spec, idx, font, pdf)
        png = pdf[:-4] + ".png"
        pymupdf.open(pdf)[0].get_pixmap(dpi=72).save(png)
        os.remove(pdf)
        out.append(png)
    print(json.dumps({"pins": out}, indent=2))


if __name__ == "__main__":
    main()
