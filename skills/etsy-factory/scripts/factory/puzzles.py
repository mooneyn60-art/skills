"""Word-search products, built on the KDP puzzle-book generator (vendored, unmodified).

The vendored make_puzzle() verifies every word appears exactly once and that filler letters never
spell a blocked word; draw_grid() draws the letter grid and the highlighted answer keys.
"""

import os
import random
import sys

VENDOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vendor")
if VENDOR not in sys.path:
    sys.path.insert(0, VENDOR)

import word_search_book as wsb  # noqa: E402  (vendored from skills/kdp-publishing)

from .common import closing_page  # noqa: E402
from .kit import INCH  # noqa: E402


def build_puzzles(content, seed):
    n = content.get("grid", 15)
    dirs = wsb.EASY_DIRS if content.get("directions", "easy") == "easy" else wsb.ALL_DIRS
    rng = random.Random(seed)
    out = []
    for pz in content["puzzles"]:
        if len(pz["words"]) > wsb.MAX_WORDS:
            raise SystemExit(f"Puzzle '{pz['title']}' has {len(pz['words'])} words; large print fits {wsb.MAX_WORDS}.")
        out.append(wsb.make_puzzle(pz["words"], n, dirs, rng))
    return out


def render(doc, spec, built):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    content = spec["content"]
    puzzles = content["puzzles"]
    n = content.get("grid", 15)
    doc.cover(spec["cover_lines"], spec["subtitle"], spec["badges"])

    # How to play + contents
    doc.new_page()
    y = doc.header("How to Play", size=34)
    easy = content.get("directions", "easy") == "easy"
    tips = [
        "Find each word from the list hidden in the grid. Circle it, then tick its box.",
        "Words run left to right, top to bottom, or diagonally. None are spelled backwards."
        if easy else "Words can run in any direction, including backwards and diagonally.",
        "Spaces are left out of the grid, so a two-word answer is written as one long word.",
        "Stuck? Every answer is highlighted in the answer key at the back.",
    ]
    for tip in tips:
        doc.ornament(m + 22, y - 6, 6, t["secondary"])
        y = doc.para(m + 40, y, tip, "WorkSans-Regular", 16, w - 2 * m - 60, 22, t["ink"]) - 10
    y -= 8
    doc.text(w / 2, y - 6, "Puzzles in This Pack", "Display", 22, t["primary"], "center")
    y -= 34
    cols = 2
    rows = -(-len(puzzles) // cols)
    row_h = min(21, (y - m - 30) / rows)
    col_w = (w - 2 * m - 40) / cols
    for i, pz in enumerate(puzzles):
        col, row = divmod(i, rows)
        x = m + 20 + col * col_w
        yy = y - row * row_h
        doc.text(x, yy, f"{i + 1:>2}", "WorkSans-Bold", 12, t["secondary"])
        doc.text(x + 26, yy, pz["title"], "WorkSans-Regular", 12.5, t["ink"], max_w=col_w - 40)

    # Puzzle pages
    cell = min(0.44 * INCH, (w - 2 * m - 0.4 * INCH) / n)
    for i, (pz, (grid, _)) in enumerate(zip(puzzles, built), 1):
        doc.new_page()
        top = h - m
        doc.text(w / 2, top - 12, f"PUZZLE {i}", "WorkSans-Bold", 10, t["secondary"], "center")
        doc.text(w / 2, top - 42, pz["title"], "Display", 27, t["primary"], "center", max_w=w - 2 * m)
        doc.ornament(w / 2 - doc.c.stringWidth(pz["title"], "Display", 27) / 2 - 22, top - 34, 7, t["accent"])
        doc.ornament(w / 2 + doc.c.stringWidth(pz["title"], "Display", 27) / 2 + 22, top - 34, 7, t["accent"])
        grid_top = top - 80
        x0 = (w - n * cell) / 2
        wsb.draw_grid(doc.c, grid, x0, grid_top, cell, "WorkSans", cell * 0.6)
        words = sorted(pz["words"])
        cols = 3
        rows = -(-len(words) // cols)
        list_w = n * cell
        col_w = list_w / cols
        y0 = grid_top - n * cell - 38
        row_h = min(23, (y0 - m - 12) / max(1, rows - 1)) if rows > 1 else 23
        for k, word in enumerate(words):
            col, row = divmod(k, rows)
            x = x0 + col * col_w + 4
            yy = y0 - row * row_h
            doc.checkbox(x, yy - 1, 11, t["primary"])
            doc.text(x + 18, yy, word.upper(), "WorkSans-Regular", 15, t["ink"], max_w=col_w - 24)

    # Answer key, six per page
    per = 6
    small = min(13.0, (w - 2 * m - 40) / 2 / n)
    for start in range(0, len(built), per):
        doc.new_page()
        y_top = doc.header("Answer Key", size=24) + 6
        block_w = (w - 2 * m) / 2
        block_h = (y_top - m - 10) / 3
        for k, idx in enumerate(range(start, min(start + per, len(built)))):
            col, row = k % 2, k // 2
            bx = m + col * block_w
            by = y_top - row * block_h
            doc.text(bx + block_w / 2, by - 12, f"{idx + 1}.  {puzzles[idx]['title']}", "WorkSans-Bold", 11,
                     t["primary"], "center", max_w=block_w - 20)
            grid, placements = built[idx]
            wsb.draw_grid(doc.c, grid, bx + (block_w - n * small) / 2, by - 26, small, "WorkSans", small * 0.62, placements)
    closing_page(doc, spec)
