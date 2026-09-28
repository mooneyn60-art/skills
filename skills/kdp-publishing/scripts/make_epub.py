"""Build a reflowable Kindle eBook (EPUB 3) from the same manuscript used for the paperback.

KDP accepts EPUB uploads directly and converts them for Kindle. Preview the result
in Kindle Previewer before publishing.

Usage:
  python make_epub.py book.md --title "My Book" --author "Jane Doe" --cover cover.jpg -o book.epub
"""

import argparse
import datetime
import html
import json
import os
import uuid

from ebooklib import epub

from format_interior import load_manuscript

CSS = """
body { font-family: serif; line-height: 1.4; }
h1 { text-align: center; margin: 2em 0 1.5em; page-break-before: always; }
h2 { text-align: center; font-size: 1.1em; margin: 1.2em 0 0.6em; }
p { text-indent: 1.5em; margin: 0; text-align: justify; }
p.first, p.center { text-indent: 0; }
p.center, p.break { text-align: center; }
p.break { margin: 1em 0; text-indent: 0; }
"""


def chapters_from_blocks(blocks):
    chapters, current, first = [], None, False
    for kind, text in blocks:
        if kind == "chapter":
            current = {"title": text, "body": [f"<h1>{text}</h1>"]}
            chapters.append(current)
            first = True
        elif current is None:
            continue
        elif kind == "subhead":
            current["body"].append(f"<h2>{text}</h2>")
            first = True
        elif kind == "break":
            current["body"].append('<p class="break">* * *</p>')
            first = True
        else:
            current["body"].append(f'<p class="first">{text}</p>' if first else f"<p>{text}</p>")
            first = False
    return chapters


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("manuscript")
    p.add_argument("-o", "--output", default="book.epub")
    p.add_argument("--title", required=True)
    p.add_argument("--author", required=True)
    p.add_argument("--language", default="en")
    p.add_argument("--cover", help="front cover JPG/PNG (KDP recommends 1600x2560 px)")
    p.add_argument("--year", type=int)
    a = p.parse_args()

    book = epub.EpubBook()
    book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
    book.set_title(a.title)
    book.set_language(a.language)
    book.add_author(a.author)
    if a.cover:
        with open(a.cover, "rb") as f:
            book.set_cover("cover" + os.path.splitext(a.cover)[1].lower(), f.read())

    style = epub.EpubItem(uid="style", file_name="style.css", media_type="text/css", content=CSS)
    book.add_item(style)

    year = a.year or datetime.date.today().year
    copyright_page = epub.EpubHtml(title="Copyright", file_name="copyright.xhtml", lang=a.language)
    copyright_page.content = (f'<p class="center">Copyright © {year} {html.escape(a.author)}</p>'
                              '<p class="center">All rights reserved.</p>')
    copyright_page.add_item(style)
    book.add_item(copyright_page)

    items = []
    for i, ch in enumerate(chapters_from_blocks(load_manuscript(a.manuscript)), 1):
        item = epub.EpubHtml(title=html.unescape(ch["title"]), file_name=f"chapter_{i:03}.xhtml", lang=a.language)
        item.content = "\n".join(ch["body"])
        item.add_item(style)
        book.add_item(item)
        items.append(item)

    book.toc = items
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = (["cover"] if a.cover else []) + ["nav", copyright_page] + items
    epub.write_epub(a.output, book)
    print(json.dumps({"output": a.output, "chapters": len(items), "cover": bool(a.cover),
                      "next_step": "Open in Kindle Previewer, then upload on the KDP eBook Content page."}, indent=2))


if __name__ == "__main__":
    main()
