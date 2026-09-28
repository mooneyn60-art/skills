"""Calculate KDP paperback full-wrap cover dimensions and optionally draw a guide template.

Usage:
  python cover_calc.py --trim 6x9 --pages 240 --paper cream
  python cover_calc.py --trim 6x9 --pages 240 --paper cream --template cover_template.pdf
"""

import argparse
import json

import kdp_specs as kdp


def cover_dimensions(trim_name, pages, paper):
    kdp.check_page_count(pages)
    width, height = kdp.trim(trim_name)
    spine = kdp.spine_width(pages, paper)
    total_w = kdp.BLEED + width + spine + width + kdp.BLEED
    total_h = kdp.BLEED + height + kdp.BLEED
    return {
        "trim": trim_name,
        "pages": pages,
        "paper": paper,
        "trim_width_in": width,
        "trim_height_in": height,
        "spine_width_in": round(spine, 4),
        "full_cover_width_in": round(total_w, 4),
        "full_cover_height_in": round(total_h, 4),
        "full_cover_px_at_300dpi": [round(total_w * kdp.MIN_DPI), round(total_h * kdp.MIN_DPI)],
        "spine_text_allowed": pages >= kdp.SPINE_TEXT_MIN_PAGES,
        "front_cover_ebook_px": [1600, 2560],
    }


def draw_template(dims, path):
    from reportlab.lib.colors import Color, black, red
    from reportlab.pdfgen import canvas

    inch = 72
    b, w, h, s = kdp.BLEED, dims["trim_width_in"], dims["trim_height_in"], dims["spine_width_in"]
    total_w, total_h = dims["full_cover_width_in"], dims["full_cover_height_in"]
    c = canvas.Canvas(path, pagesize=(total_w * inch, total_h * inch))

    c.setFillColor(Color(1, 0, 0, alpha=0.15))
    c.rect(0, 0, total_w * inch, b * inch, stroke=0, fill=1)
    c.rect(0, (total_h - b) * inch, total_w * inch, b * inch, stroke=0, fill=1)
    c.rect(0, 0, b * inch, total_h * inch, stroke=0, fill=1)
    c.rect((total_w - b) * inch, 0, b * inch, total_h * inch, stroke=0, fill=1)

    c.setStrokeColor(black)
    c.setLineWidth(0.75)
    c.rect(b * inch, b * inch, (total_w - 2 * b) * inch, h * inch)
    spine_left, spine_right = b + w, b + w + s
    c.line(spine_left * inch, 0, spine_left * inch, total_h * inch)
    c.line(spine_right * inch, 0, spine_right * inch, total_h * inch)

    m = kdp.COVER_SAFE_MARGIN
    c.setStrokeColor(red)
    c.setDash(4, 3)
    c.rect((b + m) * inch, (b + m) * inch, (w - 2 * m) * inch, (h - 2 * m) * inch)
    c.rect((spine_right + m) * inch, (b + m) * inch, (w - 2 * m) * inch, (h - 2 * m) * inch)
    if dims["spine_text_allowed"]:
        sm = kdp.SPINE_TEXT_MARGIN
        c.rect((spine_left + sm) * inch, (b + m) * inch, (s - 2 * sm) * inch, (h - 2 * m) * inch)
    c.setDash()

    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    mid_y = total_h / 2 * inch
    c.drawCentredString((b + w / 2) * inch, mid_y, "BACK COVER")
    c.drawCentredString((spine_right + w / 2) * inch, mid_y, "FRONT COVER")
    c.setFont("Helvetica", 7)
    c.drawCentredString((spine_right + w / 2) * inch, mid_y - 14, "Red dashes = safe area. Shaded edge = bleed (trimmed off).")
    c.drawCentredString((b + w / 2) * inch, (b + 0.4) * inch, "Leave ~2 x 1.2 in. clear bottom-right for the barcode")
    c.saveState()
    c.translate((spine_left + s / 2) * inch, mid_y)
    c.rotate(-90)
    c.drawCentredString(0, -3, f"SPINE {s:.4f} in" + ("" if dims["spine_text_allowed"] else " (no text <80 pages)"))
    c.restoreState()
    c.showPage()
    c.save()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--trim", required=True, help="e.g. 6x9, 5.5x8.5, 8.5x11")
    p.add_argument("--pages", type=int, required=True)
    p.add_argument("--paper", default="white", choices=sorted(kdp.PAPER_THICKNESS))
    p.add_argument("--template", help="write a PDF guide template to this path")
    a = p.parse_args()

    dims = cover_dimensions(a.trim, a.pages, a.paper)
    if a.template:
        draw_template(dims, a.template)
        dims["template"] = a.template
    print(json.dumps(dims, indent=2))


if __name__ == "__main__":
    main()
