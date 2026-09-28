"""Build a large-print word search book interior (8.5x11 by default) from a JSON book spec.

Every puzzle is verified: each listed word appears in the grid exactly once and
no filler letters spell an offensive word. Answer keys are printed at the back.

Spec (JSON):
  {
    "title": "Quilting Word Search", "subtitle": "...", "author": "...",
    "trim": "8.5x11", "grid": 15, "seed": 1,
    "directions": "easy",            # easy = right, down, diagonal (never backwards); hard adds backwards
    "series": ["Knitting & Crochet Word Search"],   # optional "more in this series" page
    "puzzles": [{"title": "Fabrics", "words": ["COTTON", "FLANNEL", ...]}, ...]
  }

Usage:
  python word_search_book.py quilting.json -o interior.pdf
"""

import argparse
import datetime
import json
import random
import re

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

import kdp_specs as kdp
from format_interior import register_fonts

INCH = 72
EASY_DIRS = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # (row step, col step): right, down, down-right, up-right
ALL_DIRS = EASY_DIRS + [(0, -1), (-1, 0), (-1, -1), (1, -1)]
BLOCKED = ["FUCK", "SHIT", "CUNT", "DICK", "COCK", "PISS", "SLUT", "WHORE", "FAG", "NIGGER", "NIGGA", "RAPE",
           "TWAT", "ASS", "KKK", "NAZI", "HELL", "DAMN", "PORN", "SEX", "TIT", "CUM", "JIZZ", "DAGO", "SPIC", "KIKE"]
MAX_WORDS = 18


def normalize(word):
    return re.sub(r"[^A-Z]", "", word.upper())


def lines_of(grid):
    n = len(grid)
    seqs = ["".join(r) for r in grid] + ["".join(grid[r][c] for r in range(n)) for c in range(n)]
    for d in range(-n + 1, n):
        seqs.append("".join(grid[r][r - d] for r in range(n) if 0 <= r - d < n))
        seqs.append("".join(grid[r][d + n - 1 - r] for r in range(n) if 0 <= d + n - 1 - r < n))
    return seqs + [s[::-1] for s in seqs]


def count_occurrences(grid, word):
    return sum(len(re.findall(f"(?={word})", line)) for line in lines_of(grid))


def try_place(n, words, dirs, rng):
    grid = [[None] * n for _ in range(n)]
    placements = {}
    for word in sorted(words, key=len, reverse=True):
        options = [(r, c, dr, dc) for dr, dc in dirs for r in range(n) for c in range(n)
                   if 0 <= r + dr * (len(word) - 1) < n and 0 <= c + dc * (len(word) - 1) < n]
        rng.shuffle(options)
        for r, c, dr, dc in options:
            cells = [(r + dr * i, c + dc * i) for i in range(len(word))]
            if all(grid[y][x] in (None, ch) for (y, x), ch in zip(cells, word)):
                overlaps = sum(grid[y][x] == ch for (y, x), ch in zip(cells, word))
                if overlaps > len(word) // 2:
                    continue
                for (y, x), ch in zip(cells, word):
                    grid[y][x] = ch
                placements[word] = cells
                break
        else:
            return None, None
    return grid, placements


def make_puzzle(words, n, dirs, rng, attempts=200):
    clean = [normalize(w) for w in words]
    for w, raw in zip(clean, words):
        if not 3 <= len(w) <= n:
            raise SystemExit(f"'{raw}' must be 3-{n} letters after removing spaces.")
    if len(set(clean)) != len(clean):
        raise SystemExit(f"Duplicate words in puzzle: {words}")
    for w in clean:
        if any(w != o and w in o for o in clean):
            raise SystemExit(f"'{w}' is contained in another word of the same puzzle; readers would find it twice.")
    letters = "".join(clean)
    # Words read backwards can spell a blocked word (GOSSIP -> PISS); only filler letters are policed.
    blocked = [b for b in BLOCKED if not any(b in w or b in w[::-1] for w in clean)]
    for _ in range(attempts):
        grid, placements = try_place(n, clean, dirs, rng)
        if grid is None:
            continue
        for _ in range(50):
            filled = [[ch or rng.choice(letters) for ch in row] for row in grid]
            if all(count_occurrences(filled, w) == 1 for w in clean) and \
                    not any(count_occurrences(filled, b) for b in blocked):
                return filled, placements
    raise SystemExit(f"Could not build a valid grid for: {words}. Use fewer or shorter words.")


def draw_grid(c, grid, x0, y_top, cell, font, size, placements=None):
    n = len(grid)
    if placements:
        c.setStrokeColor(Color(0.35, 0.35, 0.35))
        c.setLineWidth(cell * 0.62)
        c.setLineCap(1)
        c.setStrokeAlpha(0.35)
        for cells in placements.values():
            (r0, c0), (r1, c1) = cells[0], cells[-1]
            c.line(x0 + (c0 + 0.5) * cell, y_top - (r0 + 0.5) * cell, x0 + (c1 + 0.5) * cell, y_top - (r1 + 0.5) * cell)
        c.setStrokeAlpha(1)
    c.setStrokeColor(black)
    c.setLineWidth(1.2)
    c.roundRect(x0 - cell * 0.25, y_top - n * cell - cell * 0.25, n * cell + cell * 0.5, n * cell + cell * 0.5, cell * 0.3)
    c.setFillColor(black)
    c.setFont(f"{font}-Bold", size)
    for r, row in enumerate(grid):
        for col, ch in enumerate(row):
            c.drawCentredString(x0 + (col + 0.5) * cell, y_top - (r + 0.5) * cell - size * 0.35, ch)


class Book:
    def __init__(self, spec, out):
        self.spec = spec
        self.n = spec.get("grid", 15)
        self.font = register_fonts(sans=True)
        self.width, self.height = kdp.trim(spec.get("trim", "8.5x11"))
        self.c = canvas.Canvas(out, pagesize=(self.width * INCH, self.height * INCH), initialFontName=f"{self.font}-Regular")
        self.c.setTitle(spec["title"])
        self.c.setAuthor(spec["author"])
        self.page = 0
        self.gutter = 0.5 * INCH

    def frame(self):
        """(left, right) text bounds for the current page, mirrored for the gutter."""
        outside = 0.5 * INCH
        w = self.width * INCH
        return (self.gutter, w - outside) if self.page % 2 else (outside, w - self.gutter)

    def new_page(self, number=True):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.number = number

    def finish_page(self):
        if self.number:
            left, right = self.frame()
            self.c.setFont(f"{self.font}-Regular", 12)
            self.c.setFillColor(black)
            self.c.drawCentredString((left + right) / 2, 0.45 * INCH, str(self.page))

    def centered(self, text, y, size, style="Regular"):
        from reportlab.pdfbase.pdfmetrics import stringWidth

        left, right = self.frame()
        while size > 10 and stringWidth(text, f"{self.font}-{style}", size) > (right - left) * 0.92:
            size -= 1
        self.c.setFont(f"{self.font}-{style}", size)
        self.c.drawCentredString((left + right) / 2, y, text)

    def wrapped(self, text, y, size, leading=None, style="Regular"):
        from reportlab.lib.utils import simpleSplit

        left, right = self.frame()
        leading = leading or size * 1.35
        for line in simpleSplit(text, f"{self.font}-{style}", size, right - left):
            self.c.setFont(f"{self.font}-{style}", size)
            self.c.drawString(left, y, line)
            y -= leading
        return y

    def build(self, puzzles):
        s, h = self.spec, self.height * INCH
        self.new_page(number=False)
        self.centered(s["title"], h * 0.62, 34, "Bold")
        if s.get("subtitle"):
            self.centered(s["subtitle"], h * 0.62 - 44, 16)
        self.centered(s["author"], h * 0.4, 16)

        self.new_page(number=False)
        year = s.get("year") or datetime.date.today().year
        y = h * 0.3
        for line in [f"Copyright © {year} {s['author']}", "All rights reserved.",
                     "No part of this book may be reproduced without written permission from the publisher."]:
            y = self.wrapped(line, y, 11)

        self.new_page()
        y = h - 1.3 * INCH
        self.centered("How to Play", y, 28, "Bold")
        y -= 0.7 * INCH
        dirs_text = ("Words run left to right, top to bottom, or diagonally. None are backwards."
                     if s.get("directions", "easy") == "easy"
                     else "Words can run in any direction, including backwards and diagonally.")
        for para in ["Find every word from the list hidden in the grid, then circle it and tick it off the list.",
                     dirs_text, "Spaces and punctuation are left out of the grid, so FLYING GEESE appears as FLYINGGEESE.",
                     "Stuck? Every answer is at the back of the book."]:
            y = self.wrapped(para, y, 17, 25) - 14
        self.finish_page()

        cell = min(0.44 * INCH, (self.width - 1.4) * INCH / self.n)
        for i, (p, (grid, _)) in enumerate(zip(s["puzzles"], puzzles), 1):
            self.new_page()
            left, right = self.frame()
            top = h - 0.75 * INCH
            self.centered(f"#{i}  {p['title']}", top - 20, 24, "Bold")
            x0 = (left + right - self.n * cell) / 2
            grid_top = top - 0.75 * INCH
            draw_grid(self.c, grid, x0, grid_top, cell, self.font, cell * 0.62)
            words = sorted(p["words"])
            cols, rows = 3, -(-len(words) // 3)
            col_w = (right - left) / cols
            y0 = grid_top - self.n * cell - 0.55 * INCH
            self.c.setFont(f"{self.font}-Regular", 16)
            for k, w in enumerate(words):
                col, row = divmod(k, rows)
                x = left + col * col_w + 0.15 * INCH
                y = y0 - row * 0.33 * INCH
                self.c.rect(x, y - 1, 10, 10)
                self.c.drawString(x + 16, y, w.upper())
            self.finish_page()

        self.new_page()
        self.centered("Answers", h - 1.3 * INCH, 30, "Bold")
        self.finish_page()
        small = min(0.2 * INCH, (self.width - 1.6) * INCH / 2 / self.n)
        for start in range(0, len(puzzles), 4):
            self.new_page()
            left, right = self.frame()
            block_w, block_h = (right - left) / 2, (h - 1.5 * INCH) / 2
            for k, idx in enumerate(range(start, min(start + 4, len(puzzles)))):
                col, row = k % 2, k // 2
                bx = left + col * block_w
                by = h - 0.75 * INCH - row * block_h
                self.c.setFont(f"{self.font}-Bold", 13)
                self.c.drawCentredString(bx + block_w / 2, by - 16, f"#{idx + 1}  {s['puzzles'][idx]['title']}")
                grid, placements = puzzles[idx]
                draw_grid(self.c, grid, bx + (block_w - self.n * small) / 2, by - 0.45 * INCH, small, self.font,
                          small * 0.62, placements)
            self.finish_page()

        others = [t for t in s.get("series", []) if t != s["title"]]
        if others:
            self.new_page()
            y = h - 1.5 * INCH
            self.centered("More in This Series", y, 26, "Bold")
            y -= 0.8 * INCH
            for t in others:
                self.centered(t, y, 17)
                y -= 0.45 * INCH
            self.finish_page()
        self.new_page()
        y = h * 0.55
        self.centered("Thank You!", y, 28, "Bold")
        self.wrapped("If you enjoyed these puzzles, a short review on Amazon helps other puzzle lovers find this book.",
                     y - 0.8 * INCH, 16, 23)
        self.finish_page()
        if self.page % 2:
            self.new_page(number=False)
        self.c.showPage()
        self.c.save()
        return self.page


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec")
    p.add_argument("-o", "--output", default="interior.pdf")
    a = p.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)

    n = spec.get("grid", 15)
    dirs = EASY_DIRS if spec.get("directions", "easy") == "easy" else ALL_DIRS
    rng = random.Random(spec.get("seed", 1))
    for pz in spec["puzzles"]:
        if len(pz["words"]) > MAX_WORDS:
            raise SystemExit(f"Puzzle '{pz['title']}' has {len(pz['words'])} words; large print fits {MAX_WORDS}.")
    puzzles = [make_puzzle(pz["words"], n, dirs, rng) for pz in spec["puzzles"]]

    estimate = 4 + len(puzzles) + 1 + -(-len(puzzles) // 4) + 2
    book = Book(spec, a.output)
    book.gutter = kdp.gutter_margin(max(estimate, kdp.MIN_PAGES)) * INCH
    pages = book.build(puzzles)
    kdp.check_page_count(pages)
    if kdp.gutter_margin(pages) * INCH != book.gutter:
        raise SystemExit("Page count moved into a different gutter band; adjust the estimate.")
    print(json.dumps({"output": a.output, "pages": pages, "puzzles": len(puzzles), "trim": spec.get("trim", "8.5x11"),
                      "unique_words": len({normalize(w) for pz in spec["puzzles"] for w in pz["words"]}),
                      "next_step": f"python puzzle_cover.py {a.spec} --pages {pages}"}, indent=2))


if __name__ == "__main__":
    main()
