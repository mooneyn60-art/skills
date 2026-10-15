"""Pieces shared by every product type."""


def closing_page(doc, spec):
    t, w, h, m = doc.t, doc.w, doc.h, doc.m
    doc.new_page()
    y = doc.header("Thank You!", size=36, top=h * 0.72)
    body = [
        spec.get("closing_note", "Thank you for choosing this printable. We hope it brings a little extra joy to your table."),
        "Print as many copies as you need for your own home, family gathering, or classroom. "
        "Please do not resell, share, or redistribute the file.",
        "Printing tip: choose \"Fit to page\" or \"Actual size\" and print on plain paper or light card stock.",
        "Enjoyed it? A short review helps other buyers find this design.",
    ]
    for p in body:
        y = doc.para(m + 60, y, p, "WorkSans-Regular", 14, w - 2 * m - 120, 20, t["ink"], "center") - 14
    for i in range(5):
        doc.ornament(w / 2 + (i - 2) * 34, y - 20, 7, [t["primary"], t["secondary"], t["accent"]][i % 3])


def cut_grid(doc, cols, rows, top, bottom, gap=0):
    """Yield (x, y, w, h) boxes for cards laid out between top and bottom, with dashed cut lines."""
    m = doc.m
    cw = (doc.w - 2 * m - gap * (cols - 1)) / cols
    ch = (top - bottom - gap * (rows - 1)) / rows
    boxes = []
    for r in range(rows):
        for c in range(cols):
            boxes.append((m + c * (cw + gap), top - (r + 1) * ch - r * gap, cw, ch))
    return boxes


def cut_lines(doc, cols, rows, top, bottom):
    m, w = doc.m, doc.w
    cw = (w - 2 * m) / cols
    ch = (top - bottom) / rows
    col = doc.t["muted"]
    for c in range(cols + 1):
        doc.line(m + c * cw, bottom, m + c * cw, top, col, 0.6, dash=(3, 3))
    for r in range(rows + 1):
        doc.line(m, bottom + r * ch, w - m, bottom + r * ch, col, 0.6, dash=(3, 3))
