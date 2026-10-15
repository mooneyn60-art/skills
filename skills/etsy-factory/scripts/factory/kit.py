"""Shared PDF drawing kit: fonts, themes, page sizes and small drawing helpers.

Every product renderer draws through a Doc so both paper sizes (US Letter and A4) share one
layout written in relative units.
"""

import datetime
import math
import os

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

INCH = 72
SIZES = {"letter": (8.5 * INCH, 11 * INCH), "a4": (595.28, 841.89)}
SIZE_LABELS = {"letter": "US Letter 8.5 x 11 in", "a4": "A4 210 x 297 mm"}
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "fonts")

FONTS = {
    "Display": "YoungSerif-Regular.ttf",
    "Head": "BricolageGrotesque-Bold.ttf",
    "HeadRegular": "BricolageGrotesque-Regular.ttf",
    "WorkSans-Regular": "WorkSans-Regular.ttf",
    "WorkSans-Bold": "WorkSans-Bold.ttf",
    "WorkSans-Italic": "WorkSans-Italic.ttf",
    "WorkSans-BoldItalic": "WorkSans-BoldItalic.ttf",
    "Lora-Regular": "Lora-Regular.ttf",
    "Lora-Italic": "Lora-Italic.ttf",
    "Lora-Bold": "Lora-Bold.ttf",
}

THEMES = {
    "christmas": dict(primary="#1F4D3A", secondary="#B23A3A", accent="#C9A227", paper="#FBF6EC",
                      ink="#1E2A24", muted="#7A857F", tint="#E7EFE9", ornament="snowflake"),
    "thanksgiving": dict(primary="#9C4A26", secondary="#6B7A3A", accent="#D9A441", paper="#FBF4E8",
                         ink="#3B2A20", muted="#8C7B6E", tint="#F4E6D6", ornament="leaf"),
    "seniors": dict(primary="#22385C", secondary="#5E8A6E", accent="#D9A441", paper="#F6F3EC",
                    ink="#1D2433", muted="#7C8494", tint="#E6ECF3", ornament="sprig"),
    "classroom": dict(primary="#22577A", secondary="#E76F51", accent="#E9C46A", paper="#FDFBF5",
                      ink="#1F2933", muted="#7B8794", tint="#E8F1F5", ornament="star",
                      cycle=["#2A9D8F", "#E76F51", "#457B9D", "#E9A23B", "#7B5EA7", "#D1495B"]),
    "budget": dict(primary="#3F6152", secondary="#C98B74", accent="#D8B26E", paper="#F7F3EE",
                   ink="#24302B", muted="#808A85", tint="#E9EFEB", ornament="dot"),
    "meal": dict(primary="#B4583E", secondary="#6E7D4B", accent="#E0A458", paper="#FBF5EE",
                 ink="#33251F", muted="#8E7F75", tint="#F5E7DD", ornament="sprig"),
}

_registered = False


def register_fonts():
    global _registered
    if _registered:
        return
    for name, fname in FONTS.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fname)))
    pdfmetrics.registerFontFamily("WorkSans", normal="WorkSans-Regular", bold="WorkSans-Bold",
                                  italic="WorkSans-Italic", boldItalic="WorkSans-BoldItalic")
    _registered = True


def hexc(value, alpha=1.0):
    c = HexColor(value)
    return Color(c.red, c.green, c.blue, alpha) if alpha < 1 else c


def mix(a, b, t):
    """Blend two hex colors; t=0 gives a, t=1 gives b."""
    ca, cb = HexColor(a), HexColor(b)
    return Color(ca.red + (cb.red - ca.red) * t, ca.green + (cb.green - ca.green) * t, ca.blue + (cb.blue - ca.blue) * t)


class Doc:
    """One PDF in one paper size. Coordinates are points, origin bottom-left."""

    def __init__(self, path, size, theme, product_name, year=None):
        register_fonts()
        self.size = size
        self.w, self.h = SIZES[size]
        self.t = THEMES[theme]
        self.theme = theme
        self.m = 0.5 * INCH
        self.c = canvas.Canvas(path, pagesize=(self.w, self.h))
        self.c.setTitle(product_name)
        self.c.setAuthor("Original printable design")
        self.product_name = product_name
        self.year = year or datetime.date.today().year
        self.pages = 0
        self.open = False

    # ---- page lifecycle -------------------------------------------------
    def new_page(self, footer=True):
        if self.open:
            self.end_page()
        self.pages += 1
        self.open = True
        self.footer = footer

    def end_page(self):
        if self.footer:
            self.text(self.w / 2, 0.32 * INCH, f"{self.product_name}  ·  for personal use  ·  © {self.year}",
                      "WorkSans-Regular", 7.5, self.t["muted"], "center")
        self.c.showPage()
        self.open = False

    def save(self):
        if self.open:
            self.end_page()
        self.c.save()

    # ---- text -----------------------------------------------------------
    def fit(self, s, font, size, max_w, min_size=6):
        while size > min_size and stringWidth(s, font, size) > max_w:
            size -= 0.5
        return size

    def text(self, x, y, s, font, size, color=None, align="left", max_w=None):
        if max_w:
            size = self.fit(s, font, size, max_w)
        self.c.setFillColor(hexc(color) if isinstance(color, str) else (color or hexc(self.t["ink"])))
        self.c.setFont(font, size)
        {"left": self.c.drawString, "center": self.c.drawCentredString, "right": self.c.drawRightString}[align](x, y, s)
        return size

    def lines(self, s, font, size, width):
        return simpleSplit(s, font, size, width)

    def para(self, x, y, s, font, size, width, leading=None, color=None, align="left"):
        leading = leading or size * 1.35
        for line in self.lines(s, font, size, width):
            ax = {"left": x, "center": x + width / 2, "right": x + width}[align]
            self.text(ax, y, line, font, size, color, align)
            y -= leading
        return y

    def para_fit(self, x, y_top, s, font, size, width, height, color=None, align="center", leading=1.25, min_size=7):
        """Wrap s into a box, shrinking until it fits; text is vertically centred in the box."""
        while True:
            ls = self.lines(s, font, size, width)
            block = len(ls) * size * leading
            if block <= height or size <= min_size:
                break
            size -= 0.5
        y = y_top - (height - block) / 2 - size * 0.95
        for line in ls:
            ax = {"left": x, "center": x + width / 2}[align]
            self.text(ax, y, line, font, size, color, align)
            y -= size * leading
        return size

    # ---- shapes ---------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, stroke=None, width=1, radius=0, dash=None):
        c = self.c
        c.saveState()
        if fill:
            c.setFillColor(hexc(fill) if isinstance(fill, str) else fill)
        if stroke:
            c.setStrokeColor(hexc(stroke) if isinstance(stroke, str) else stroke)
            c.setLineWidth(width)
        if dash:
            c.setDash(*dash)
        if radius:
            c.roundRect(x, y, w, h, radius, stroke=1 if stroke else 0, fill=1 if fill else 0)
        else:
            c.rect(x, y, w, h, stroke=1 if stroke else 0, fill=1 if fill else 0)
        c.restoreState()

    def line(self, x1, y1, x2, y2, color, width=1, dash=None):
        c = self.c
        c.saveState()
        c.setStrokeColor(hexc(color) if isinstance(color, str) else color)
        c.setLineWidth(width)
        c.setLineCap(1)
        if dash:
            c.setDash(*dash)
        c.line(x1, y1, x2, y2)
        c.restoreState()

    def circle(self, x, y, r, fill=None, stroke=None, width=1):
        c = self.c
        c.saveState()
        if fill:
            c.setFillColor(hexc(fill) if isinstance(fill, str) else fill)
        if stroke:
            c.setStrokeColor(hexc(stroke) if isinstance(stroke, str) else stroke)
            c.setLineWidth(width)
        c.circle(x, y, r, stroke=1 if stroke else 0, fill=1 if fill else 0)
        c.restoreState()

    def checkbox(self, x, y, s, color=None):
        self.rect(x, y, s, s, stroke=color or self.t["muted"], width=0.9, radius=s * 0.18)

    # ---- ornaments (original vector motifs) -----------------------------
    def ornament(self, x, y, r, color, kind=None):
        kind = kind or self.t["ornament"]
        c = self.c
        col = hexc(color) if isinstance(color, str) else color
        c.saveState()
        c.setStrokeColor(col)
        c.setFillColor(col)
        c.setLineCap(1)
        if kind == "snowflake":
            c.setLineWidth(max(0.6, r * 0.13))
            for k in range(6):
                a = math.pi / 3 * k + math.pi / 2
                ex, ey = x + r * math.cos(a), y + r * math.sin(a)
                c.line(x, y, ex, ey)
                for f in (0.55,):
                    bx, by = x + r * f * math.cos(a), y + r * f * math.sin(a)
                    for s in (-1, 1):
                        b = a + s * math.pi / 4
                        c.line(bx, by, bx + r * 0.32 * math.cos(b), by + r * 0.32 * math.sin(b))
        elif kind == "star":
            p = c.beginPath()
            for k in range(10):
                a = math.pi / 2 + k * math.pi / 5
                rr = r if k % 2 == 0 else r * 0.45
                (p.moveTo if k == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
            p.close()
            c.drawPath(p, stroke=0, fill=1)
        elif kind == "leaf":
            p = c.beginPath()
            p.moveTo(x - r * 0.75, y - r * 0.75)
            p.curveTo(x - r * 0.9, y + r * 0.4, x + r * 0.2, y + r * 0.95, x + r * 0.8, y + r * 0.8)
            p.curveTo(x + r * 0.95, y - r * 0.2, x - r * 0.4, y - r * 0.9, x - r * 0.75, y - r * 0.75)
            p.close()
            c.drawPath(p, stroke=0, fill=1)
            c.setStrokeColor(white)
            c.setLineWidth(max(0.5, r * 0.08))
            c.line(x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6)
        elif kind == "sprig":
            c.setLineWidth(max(0.6, r * 0.1))
            c.line(x, y - r, x, y + r)
            for k, fy in enumerate((-0.5, 0.0, 0.5)):
                s = -1 if k % 2 else 1
                p = c.beginPath()
                bx, by = x, y + r * fy
                p.moveTo(bx, by)
                p.curveTo(bx + s * r * 0.2, by + r * 0.45, bx + s * r * 0.7, by + r * 0.45, bx + s * r * 0.75, by + r * 0.3)
                p.curveTo(bx + s * r * 0.6, by + r * 0.05, bx + s * r * 0.2, by - r * 0.05, bx, by)
                c.drawPath(p, stroke=0, fill=1)
        else:
            c.circle(x, y, r * 0.45, stroke=0, fill=1)
        c.restoreState()

    def ornament_rule(self, y, width, color=None):
        """Thin rule with an ornament in the middle, used under titles."""
        cx = self.w / 2
        color = color or self.t["secondary"]
        self.line(cx - width / 2, y, cx - 14, y, self.t["accent"], 1.1)
        self.line(cx + 14, y, cx + width / 2, y, self.t["accent"], 1.1)
        self.ornament(cx, y, 7, color)

    def header(self, title, subtitle=None, size=30, top=None):
        """Centred page header; returns the y just below it."""
        y = (top or self.h - self.m) - size * 0.95
        self.text(self.w / 2, y, title, "Display", size, self.t["primary"], "center", max_w=self.w - 2 * self.m)
        y -= size * 0.55
        self.ornament_rule(y, min(self.w * 0.42, 260))
        y -= 12
        if subtitle:
            y -= 14
            self.text(self.w / 2, y, subtitle, "WorkSans-Italic", 12, self.t["muted"], "center", max_w=self.w - 2 * self.m)
            y -= 8
        return y - 10

    # ---- shared cover page ---------------------------------------------
    def cover(self, lines, subtitle, badges):
        """Printable title page (also used as the hero of listing image 1)."""
        t, w, h, m = self.t, self.w, self.h, self.m
        self.new_page(footer=False)
        self.rect(m, m, w - 2 * m, h - 2 * m, fill=t["paper"])
        self.rect(m + 10, m + 10, w - 2 * m - 20, h - 2 * m - 20, stroke=t["accent"], width=1.4)
        self.rect(m + 15, m + 15, w - 2 * m - 30, h - 2 * m - 30, stroke=t["accent"], width=0.5)
        # scattered ornaments in the top and bottom bands (deterministic layout)
        for i in range(9):
            fx = (i + 0.5) / 9
            for band, dy in ((h - m - 70, 0), (m + 70, 0)):
                r = 7 + (i * 7 % 5)
                col = [t["primary"], t["secondary"], t["accent"]][i % 3]
                self.ornament(m + 30 + fx * (w - 2 * m - 60), band + (12 if i % 2 else -12) + dy, r, col)
        size = 64 if len(lines) <= 2 else 54
        n = len(lines)
        y = h * 0.6 + (n - 1) * size * 0.55
        for i, ln in enumerate(lines):
            color = t["primary"] if i % 2 == 0 else t["secondary"]
            self.text(w / 2, y, ln, "Display", size, color, "center", max_w=w - 2 * m - 90)
            y -= size * 1.08
        y += size * 0.35
        self.ornament_rule(y - 6, 230)
        self.para(m + 60, y - 42, subtitle, "WorkSans-Regular", 17, w - 2 * m - 120, 23, t["ink"], "center")
        bw = (w - 2 * m - 120) / max(1, len(badges))
        for i, b in enumerate(badges):
            cx = m + 60 + bw * (i + 0.5)
            self.rect(cx - bw / 2 + 6, h * 0.25, bw - 12, 34, fill=t["primary"], radius=17)
            self.text(cx, h * 0.25 + 12, b.upper(), "WorkSans-Bold", 11, "#FFFFFF", "center", max_w=bw - 26)
        self.end_page()
