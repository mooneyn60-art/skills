#!/usr/bin/env python3
"""Generate a finished Etsy digital-download product from a spec JSON.

Outputs in products/<slug>/:
  <slug>-letter.pdf, <slug>-a4.pdf   print-ready files (the buyer downloads both)
  images/01-cover.jpg ... 05-how.jpg 2000x2000 listing images
  listing.json, listing.md           title (<=140), 13 tags (<=20), description, price
  preview/page-XX.png                every PDF page rendered, for visual QA

Usage:
  python scripts/make_product.py specs/christmas-word-search-large-print.json
  python scripts/make_product.py specs/*.json            # build several
  python scripts/make_product.py SPEC --no-preview       # skip the QA page renders

Spec "type" picks the renderer: wordsearch | bingo | cards | trivia | jobs | planner.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from factory import images, listing_copy, party, planners, puzzles  # noqa: E402
from factory.kit import Doc  # noqa: E402

RENDERERS = {
    "wordsearch": puzzles.render,
    "bingo": party.render_bingo,
    "cards": party.render_cards,
    "trivia": party.render_trivia,
    "jobs": planners.render_jobs,
    "planner": planners.render_planner,
}


def build(spec_path, preview=True):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    slug = spec["slug"]
    out = os.path.join(ROOT, "products", slug)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "images"))
    render = RENDERERS[spec["type"]]
    built = puzzles.build_puzzles(spec["content"], spec.get("seed", 1)) if spec["type"] == "wordsearch" else None

    pdfs, pages = {}, {}
    for size in ("letter", "a4"):
        path = os.path.join(out, f"{slug}-{size}.pdf")
        doc = Doc(path, size, spec["theme"], spec["product_name"])
        render(doc, spec, built)
        doc.save()
        pdfs[size], pages[size] = path, doc.pages
    if pages["letter"] != pages["a4"]:
        raise SystemExit(f"{slug}: letter has {pages['letter']} pages but A4 has {pages['a4']}")

    imgs = images.make_all(spec, pdfs["letter"], pdfs["a4"], os.path.join(out, "images"))
    rel = lambda p: os.path.relpath(p, out)  # noqa: E731
    listing = listing_copy.build(spec, out, {"pdf": [rel(p) for p in pdfs.values()], "images": [rel(p) for p in imgs]})
    if preview:
        prev = os.path.join(out, "preview")
        os.makedirs(prev)
        subprocess.run(["pdftoppm", "-png", "-r", "60", pdfs["letter"], os.path.join(prev, "page")], check=True)
    summary = {"slug": slug, "pages": pages["letter"], "price": listing["price"], "title_len": len(listing["title"]),
               "pdf": [rel(p) for p in pdfs.values()], "images": [rel(p) for p in imgs]}
    print(json.dumps(summary))
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("specs", nargs="+")
    p.add_argument("--no-preview", action="store_true")
    a = p.parse_args()
    for s in a.specs:
        build(s, preview=not a.no_preview)


if __name__ == "__main__":
    main()
