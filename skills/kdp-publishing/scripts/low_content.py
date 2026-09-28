"""Generate low-content book interiors (journals, notebooks, planners, logs) as KDP-ready PDFs.

Page styles:
  lined     ruled lines with a header line
  dot       dot grid
  grid      square grid (graph paper)
  blank     sketchbook pages
  planner   dated-free daily planner: date, top 3 priorities, schedule, notes
  gratitude "Today I am grateful for" prompt journal

Usage:
  python low_content.py --style lined --pages 120 --trim 6x9 --title "Notebook" -o notebook.pdf
"""

import argparse
import json

from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

import kdp_specs as kdp
from format_interior import register_fonts

INCH = 72
INK = Color(0.55, 0.55, 0.55)


def draw_lines(c, x0, x1, y_top, y_bottom, spacing):
    y = y_top
    while y >= y_bottom:
        c.line(x0, y, x1, y)
        y -= spacing


def style_lined(c, box, font):
    x0, y0, x1, y1 = box
    c.setFont(f"{font}-Regular", 8)
    c.drawString(x0, y1 - 10, "Date: ____________________")
    draw_lines(c, x0, x1, y1 - 0.5 * INCH, y0, 0.28 * INCH)


def style_dot(c, box, font, step=0.2 * INCH):
    x0, y0, x1, y1 = box
    y = y1
    while y >= y0:
        x = x0
        while x <= x1:
            c.circle(x, y, 0.6, stroke=0, fill=1)
            x += step
        y -= step


def style_grid(c, box, font, step=0.2 * INCH):
    x0, y0, x1, y1 = box
    draw_lines(c, x0, x1, y1, y0, step)
    x = x0
    while x <= x1:
        c.line(x, y0, x, y1)
        x += step


def style_blank(c, box, font):
    pass


def style_planner(c, box, font):
    x0, y0, x1, y1 = box
    c.setFont(f"{font}-Bold", 11)
    c.drawString(x0, y1 - 12, "Date: ______________")
    c.drawString(x0, y1 - 0.55 * INCH, "Top 3 Priorities")
    c.setFont(f"{font}-Regular", 10)
    for i in range(3):
        y = y1 - (0.85 + i * 0.3) * INCH
        c.rect(x0, y - 2, 8, 8)
        c.line(x0 + 14, y - 2, x1, y - 2)
    top = y1 - 2.0 * INCH
    c.setFont(f"{font}-Bold", 11)
    c.drawString(x0, top, "Schedule")
    c.setFont(f"{font}-Regular", 8)
    for i, hour in enumerate(range(6, 22)):
        y = top - 0.18 * INCH - i * 0.22 * INCH
        c.drawString(x0, y + 2, f"{hour % 12 or 12}{'am' if hour < 12 else 'pm'}")
        c.line(x0 + 0.4 * INCH, y, x1, y)
    notes = top - 0.18 * INCH - 16 * 0.22 * INCH - 0.3 * INCH
    if notes > y0 + 0.5 * INCH:
        c.setFont(f"{font}-Bold", 11)
        c.drawString(x0, notes, "Notes")
        draw_lines(c, x0, x1, notes - 0.25 * INCH, y0, 0.25 * INCH)


def style_gratitude(c, box, font):
    x0, y0, x1, y1 = box
    c.setFont(f"{font}-Regular", 10)
    c.drawString(x0, y1 - 12, "Date: ______________")
    sections = ["Today I am grateful for...", "What would make today great?", "Something good that happened"]
    height = (y1 - y0 - 0.4 * INCH) / len(sections)
    for i, label in enumerate(sections):
        top = y1 - 0.4 * INCH - i * height
        c.setFont(f"{font}-Italic", 11)
        c.drawString(x0, top - 14, label)
        draw_lines(c, x0, x1, top - 0.45 * INCH, top - height + 0.15 * INCH, 0.3 * INCH)


STYLES = {"lined": style_lined, "dot": style_dot, "grid": style_grid, "blank": style_blank,
          "planner": style_planner, "gratitude": style_gratitude}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--style", required=True, choices=sorted(STYLES))
    p.add_argument("--pages", type=int, required=True, help="total interior pages, including the title page")
    p.add_argument("--trim", default="6x9")
    p.add_argument("--title", default="")
    p.add_argument("--author", default="")
    p.add_argument("--no-page-numbers", action="store_true")
    p.add_argument("-o", "--output", default="low_content.pdf")
    a = p.parse_args()

    kdp.check_page_count(a.pages)
    font = register_fonts()
    width, height = kdp.trim(a.trim)
    gutter = kdp.gutter_margin(a.pages) * INCH
    outside, top, bottom = 0.5 * INCH, 0.6 * INCH, 0.6 * INCH
    w, h = width * INCH, height * INCH
    c = canvas.Canvas(a.output, pagesize=(w, h), initialFontName=f"{font}-Regular")
    c.setTitle(a.title or f"{a.style} notebook")

    c.setFont(f"{font}-Bold", 24)
    c.drawCentredString(w / 2, h * 0.6, a.title)
    c.setFont(f"{font}-Regular", 12)
    c.drawCentredString(w / 2, h * 0.6 - 30, a.author)
    c.drawCentredString(w / 2, h * 0.3, "This book belongs to: ______________________")
    c.showPage()

    for page in range(2, a.pages + 1):
        left = gutter if page % 2 else outside
        right = w - (outside if page % 2 else gutter)
        box = (left, bottom + 0.25 * INCH, right, h - top)
        c.setStrokeColor(INK)
        c.setFillColor(INK)
        c.setLineWidth(0.5)
        STYLES[a.style](c, box, font)
        if not a.no_page_numbers:
            c.setFont(f"{font}-Regular", 8)
            c.drawCentredString((left + right) / 2, bottom - 0.2 * INCH, str(page))
        c.showPage()
    c.save()
    print(json.dumps({"output": a.output, "pages": a.pages, "style": a.style, "trim": a.trim,
                      "next_step": f"python cover_calc.py --trim {a.trim} --pages {a.pages} --paper white"}, indent=2))


if __name__ == "__main__":
    main()
