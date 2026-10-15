"""Turn a manuscript (.md, .txt or .docx) into a KDP print-ready paperback interior PDF.

- Trim-sized pages (optionally with bleed), fonts embedded.
- Mirrored margins with the gutter KDP requires for the final page count.
- Title page, copyright page, chapters opening on right-hand pages.
- Page numbers and running heads (author left, title right).

Manuscript conventions:
  .md   "# Chapter title" starts a chapter; "***" or "* * *" is a scene break;
        **bold** and *italic* are supported.
  .txt  a line starting with "Chapter" (or "CHAPTER") starts a chapter.
  .docx paragraphs styled Heading 1 start chapters; bold/italic runs are kept.

Usage:
  python format_interior.py book.md --title "My Book" --author "Jane Doe" --trim 6x9 -o interior.pdf
"""

import argparse
import datetime
import glob
import html
import json
import os
import re

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer
from reportlab.platypus.flowables import Flowable

import kdp_specs as kdp

INCH = 72
SANS_FONT_CANDIDATES = [
    ("LiberationSans", "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf",
     {"Regular": "Regular", "Bold": "Bold", "Italic": "Italic", "BoldItalic": "BoldItalic"}),
    ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf",
     {"Regular": "", "Bold": "-Bold", "Italic": "-Oblique", "BoldItalic": "-BoldOblique"}),
    ("Arial", "/Library/Fonts/Arial{}.ttf", {"Regular": "", "Bold": " Bold", "Italic": " Italic", "BoldItalic": " Bold Italic"}),
    ("Arial", "C:/Windows/Fonts/arial{}.ttf", {"Regular": "", "Bold": "bd", "Italic": "i", "BoldItalic": "bi"}),
]
FONT_CANDIDATES = [
    ("LiberationSerif", "/usr/share/fonts/truetype/liberation/LiberationSerif-{}.ttf",
     {"Regular": "Regular", "Bold": "Bold", "Italic": "Italic", "BoldItalic": "BoldItalic"}),
    ("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif{}.ttf",
     {"Regular": "", "Bold": "-Bold", "Italic": "-Italic", "BoldItalic": "-BoldItalic"}),
    ("TimesNewRoman", "/Library/Fonts/Times New Roman{}.ttf",
     {"Regular": "", "Bold": " Bold", "Italic": " Italic", "BoldItalic": " Bold Italic"}),
    ("TimesNewRoman", "C:/Windows/Fonts/times{}.ttf",
     {"Regular": "", "Bold": "bd", "Italic": "i", "BoldItalic": "bi"}),
]


def register_fonts(font_dir=None, sans=False):
    """Register an embeddable TTF family. KDP rejects PDFs with non-embedded fonts."""
    if font_dir:
        files = {s: glob.glob(os.path.join(font_dir, f"*{s}*.ttf")) for s in ("Regular", "Bold", "Italic", "BoldItalic")}
        files["Italic"] = [f for f in files["Italic"] if "BoldItalic" not in f]
        if not all(files.values()):
            raise SystemExit(f"{font_dir} needs Regular, Bold, Italic and BoldItalic .ttf files.")
        candidates = [("Custom", None, {s: f[0] for s, f in files.items()})]
    else:
        table = SANS_FONT_CANDIDATES if sans else FONT_CANDIDATES
        candidates = [(n, pattern, {s: pattern.format(v) for s, v in m.items()}) for n, pattern, m in table]
    for name, _, paths in candidates:
        if all(os.path.exists(p) for p in paths.values()):
            for style, path in paths.items():
                pdfmetrics.registerFont(TTFont(f"{name}-{style}", path))
            pdfmetrics.registerFontFamily(name, normal=f"{name}-Regular", bold=f"{name}-Bold",
                                          italic=f"{name}-Italic", boldItalic=f"{name}-BoldItalic")
            return name
    raise SystemExit("No embeddable TTF family found. Pass --font-dir with Regular/Bold/Italic/BoldItalic .ttf files.")


def inline_markdown(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])[*_](.+?)[*_](?![\w*])", r"<i>\1</i>", text)
    return text


def parse_markdown(raw):
    blocks, para = [], []

    def flush():
        if para:
            blocks.append(("para", inline_markdown(" ".join(para))))
            para.clear()

    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("# "):
            flush()
            blocks.append(("chapter", html.escape(s[2:].strip(), quote=False)))
        elif re.fullmatch(r"(\*\s*){3,}|(-\s*){3,}|#", s):
            flush()
            blocks.append(("break", None))
        elif s.startswith("## "):
            flush()
            blocks.append(("subhead", inline_markdown(s[3:].strip())))
        elif not s:
            flush()
        else:
            para.append(s)
    flush()
    return blocks


def parse_text(raw):
    blocks = []
    for chunk in re.split(r"\n\s*\n", raw):
        s = " ".join(chunk.split())
        if not s:
            continue
        if re.match(r"(chapter|CHAPTER)\b", s) and len(s) < 80:
            blocks.append(("chapter", html.escape(s, quote=False)))
        elif re.fullmatch(r"(\*\s*){3,}|#", s):
            blocks.append(("break", None))
        else:
            blocks.append(("para", html.escape(s, quote=False)))
    return blocks


def parse_docx(path):
    import docx

    blocks = []
    for p in docx.Document(path).paragraphs:
        text = p.text.strip()
        if not text:
            continue
        style = (p.style.name or "").lower()
        if style.startswith("heading 1") or style == "title":
            blocks.append(("chapter", html.escape(text, quote=False)))
        elif style.startswith("heading"):
            blocks.append(("subhead", html.escape(text, quote=False)))
        elif re.fullmatch(r"(\*\s*){3,}|#", text):
            blocks.append(("break", None))
        else:
            parts = []
            for r in p.runs:
                t = html.escape(r.text, quote=False)
                if r.bold:
                    t = f"<b>{t}</b>"
                if r.italic:
                    t = f"<i>{t}</i>"
                parts.append(t)
            blocks.append(("para", "".join(parts)))
    return blocks


def load_manuscript(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        blocks = parse_docx(path)
    else:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        blocks = parse_markdown(raw) if ext in (".md", ".markdown") else parse_text(raw)
    if not any(kind == "chapter" for kind, _ in blocks):
        raise SystemExit("No chapters found. Mark chapters with '# Title' (.md), 'Chapter ...' (.txt) or Heading 1 (.docx).")
    return blocks


class RectoBreak(Flowable):
    """Marker: start the next content on a right-hand (odd) page."""

    def wrap(self, *_):
        return 0, 0

    def draw(self):
        pass


class _BlankIfVerso(Flowable):
    """Evaluated once the new page has begun: leave an even page blank."""


class ChapterStart(Flowable):
    """Zero-size marker recording which page a chapter opens on (no running head there)."""

    def __init__(self, doc):
        super().__init__()
        self.doc = doc

    def wrap(self, *_):
        return 0, 0

    def draw(self):
        self.doc.chapter_pages.add(self.canv.getPageNumber())


class BookDoc(BaseDocTemplate):
    def __init__(self, path, *, page_w, page_h, gutter, outside, top, bottom, title, author, font, **kw):
        super().__init__(path, pagesize=(page_w, page_h), title=title, author=author,
                         initialFontName=f"{font}-Regular", **kw)
        self.front_matter_pages = 0
        self.chapter_pages = set()
        self.blank_pages = set()
        self.running_title, self.running_author, self.font = title, author, font
        fw, fh = page_w - gutter - outside, page_h - top - bottom
        self.addPageTemplates([
            PageTemplate("recto", [Frame(gutter, bottom, fw, fh, 0, 0, 0, 0, id="r")], onPageEnd=self.decorate),
            PageTemplate("verso", [Frame(outside, bottom, fw, fh, 0, 0, 0, 0, id="v")], onPageEnd=self.decorate),
        ])
        self.header_y = page_h - top + 0.3 * INCH
        self.footer_y = bottom - 0.4 * INCH
        self.recto_center = gutter + fw / 2
        self.verso_center = outside + fw / 2

    def handle_pageBegin(self):
        self.pageTemplate = self.pageTemplates[0 if (self.page + 1) % 2 else 1]
        super().handle_pageBegin()

    def handle_flowable(self, flowables):
        head = flowables[0]
        if isinstance(head, RectoBreak):
            flowables.pop(0)
            page_started = self._curPageFlowableCount or not self.frame._atTop
            flowables[0:0] = [PageBreak(), _BlankIfVerso()] if page_started else [_BlankIfVerso()]
            return
        if isinstance(head, _BlankIfVerso):
            flowables.pop(0)
            if self.page % 2 == 0:
                self.blank_pages.add(self.page)
                self.handle_pageBreak()
            return
        super().handle_flowable(flowables)

    def decorate(self, canv, doc):
        page = canv.getPageNumber()
        if page <= self.front_matter_pages or page in self.blank_pages:
            return
        center = self.recto_center if page % 2 else self.verso_center
        canv.saveState()
        canv.setFont(f"{self.font}-Regular", 9)
        canv.drawCentredString(center, self.footer_y, str(page))
        if page not in self.chapter_pages:
            canv.setFont(f"{self.font}-Italic", 9)
            canv.drawCentredString(center, self.header_y, self.running_title if page % 2 else self.running_author)
        canv.restoreState()


def build(blocks, meta, out, pages_estimate, args, font):
    width, height = kdp.trim(args.trim)
    page_w = (width + (kdp.BLEED if args.bleed else 0)) * INCH
    page_h = (height + (2 * kdp.BLEED if args.bleed else 0)) * INCH
    gutter = kdp.gutter_margin(max(pages_estimate, kdp.MIN_PAGES)) * INCH
    outside = max(args.outside, kdp.OUTSIDE_MARGIN_BLEED if args.bleed else kdp.OUTSIDE_MARGIN_NO_BLEED) * INCH
    doc = BookDoc(out, page_w=page_w, page_h=page_h, gutter=gutter, outside=outside,
                  top=0.75 * INCH, bottom=0.75 * INCH, title=meta["title"], author=meta["author"], font=font)

    body = ParagraphStyle("body", fontName=f"{font}-Regular", fontSize=args.font_size,
                          leading=args.font_size * 1.4, alignment=TA_JUSTIFY, firstLineIndent=0.3 * INCH)
    first = ParagraphStyle("first", parent=body, firstLineIndent=0)
    center = ParagraphStyle("center", parent=body, alignment=TA_CENTER, firstLineIndent=0)
    chap = ParagraphStyle("chap", parent=center, fontName=f"{font}-Bold", fontSize=args.font_size * 1.8,
                          leading=args.font_size * 2.2, spaceAfter=0.4 * INCH)
    sub = ParagraphStyle("sub", parent=center, fontName=f"{font}-Bold", spaceBefore=12, spaceAfter=6)
    title_s = ParagraphStyle("title", parent=chap, fontSize=args.font_size * 2.6, leading=args.font_size * 3.2)
    small = ParagraphStyle("small", parent=center, fontSize=args.font_size * 0.8, leading=args.font_size * 1.2)

    story = [Spacer(1, page_h * 0.25), Paragraph(html.escape(meta["title"]), title_s)]
    if meta.get("subtitle"):
        story.append(Paragraph(f"<i>{html.escape(meta['subtitle'])}</i>", center))
    story += [Spacer(1, 0.6 * INCH), Paragraph(html.escape(meta["author"]), center), PageBreak(),
              Spacer(1, page_h * 0.55)]
    year = meta.get("year") or datetime.date.today().year
    copyright_lines = [f"Copyright © {year} {html.escape(meta['author'])}", "All rights reserved.",
                       "No part of this book may be reproduced in any form without written permission "
                       "from the author, except for brief quotations in reviews."]
    if meta.get("isbn"):
        copyright_lines.append(f"ISBN: {html.escape(meta['isbn'])}")
    story += [Paragraph(line, small) for line in copyright_lines]
    front = 2
    if meta.get("dedication"):
        story += [PageBreak(), Spacer(1, page_h * 0.3), Paragraph(f"<i>{html.escape(meta['dedication'])}</i>", center)]
        front = 3
    doc.front_matter_pages = front + (front % 2)

    after_heading = False
    for kind, text in blocks:
        if kind == "chapter":
            story += [RectoBreak(), ChapterStart(doc), Spacer(1, page_h * 0.18), Paragraph(text, chap)]
            after_heading = True
        elif kind == "subhead":
            story.append(Paragraph(text, sub))
            after_heading = True
        elif kind == "break":
            story.append(Paragraph("*&nbsp;&nbsp;*&nbsp;&nbsp;*", center))
            after_heading = True
        else:
            story.append(Paragraph(text, first if after_heading else body))
            after_heading = False
    doc.build(story)
    return doc.page, gutter / INCH


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("manuscript")
    p.add_argument("-o", "--output", default="interior.pdf")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle")
    p.add_argument("--author", required=True)
    p.add_argument("--isbn")
    p.add_argument("--dedication")
    p.add_argument("--year", type=int)
    p.add_argument("--trim", default="6x9")
    p.add_argument("--font-size", type=float, default=11)
    p.add_argument("--outside", type=float, default=0.5, help="outside margin in inches (KDP minimum enforced)")
    p.add_argument("--bleed", action="store_true", help="for interiors with images that run to the page edge")
    p.add_argument("--font-dir", help="folder with Regular/Bold/Italic/BoldItalic .ttf files")
    a = p.parse_args()

    font = register_fonts(a.font_dir)
    blocks = load_manuscript(a.manuscript)
    meta = {"title": a.title, "subtitle": a.subtitle, "author": a.author, "isbn": a.isbn,
            "dedication": a.dedication, "year": a.year}

    estimate = 100
    for _ in range(4):
        pages, gutter = build(blocks, meta, a.output, estimate, a, font)
        if kdp.gutter_margin(max(pages, kdp.MIN_PAGES)) == gutter:
            break
        estimate = pages

    warnings = []
    if pages < kdp.MIN_PAGES:
        warnings.append(f"Only {pages} pages; KDP paperbacks need at least {kdp.MIN_PAGES}. Increase --font-size or add content.")
    if pages > kdp.MAX_PAGES:
        warnings.append(f"{pages} pages exceeds KDP's {kdp.MAX_PAGES}-page maximum. Use a larger trim or smaller font.")
    print(json.dumps({"output": a.output, "pages": pages, "trim": a.trim, "bleed": a.bleed,
                      "gutter_in": gutter, "font": font, "chapters": sum(k == "chapter" for k, _ in blocks),
                      "next_step": f"python cover_calc.py --trim {a.trim} --pages {pages} --paper cream",
                      "warnings": warnings}, indent=2))


if __name__ == "__main__":
    main()
