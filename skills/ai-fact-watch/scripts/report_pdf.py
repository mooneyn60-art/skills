"""PDF rendering for report.py (ReportLab, no browser needed).

Kept separate from report.py so each file stays small; it reads the same
context dict, so the PDF and HTML always show the same findings.
"""

from __future__ import annotations

import html
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)

from fixkit import hours_lines

INK = colors.HexColor("#14213d")
MUTED = colors.HexColor("#5b6475")
LINE = colors.HexColor("#e3e7ee")
BRAND = colors.HexColor("#0b6e6e")
SOFT = colors.HexColor("#f1f4f9")
SEV = {"critical": ("#c0392b", "#fdecea"), "high": ("#c0392b", "#fdecea"),
       "medium": ("#b9770e", "#fdf3e1"), "low": ("#7f8a99", "#eef1f5")}
FLAGC = {"red": ("#c0392b", "#fdecea", "Wrong"), "yellow": ("#b9770e", "#fdf3e1", "Gap"),
         "green": ("#1e8449", "#e8f6ee", "Correct"), "grey": ("#7f8a99", "#eef1f5", "Not seen")}

FONT_DIRS = ["/usr/share/fonts/truetype/crosextra", "/usr/share/fonts/truetype/dejavu",
             "/usr/share/fonts/truetype/liberation"]


def _register() -> tuple[str, str, str, str]:
    """Carlito (metric-compatible with Calibri) if installed, else DejaVu, else Helvetica."""
    for reg, bold, ital, name in [("Carlito-Regular.ttf", "Carlito-Bold.ttf", "Carlito-Italic.ttf", "Carlito"),
                                  ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans-Oblique.ttf", "DejaVu")]:
        paths = [next((os.path.join(d, f) for d in FONT_DIRS if os.path.exists(os.path.join(d, f))), None)
                 for f in (reg, bold, ital)]
        if all(paths):
            pdfmetrics.registerFont(TTFont(name, paths[0]))
            pdfmetrics.registerFont(TTFont(name + "-B", paths[1]))
            pdfmetrics.registerFont(TTFont(name + "-I", paths[2]))
            pdfmetrics.registerFontFamily(name, normal=name, bold=name + "-B", italic=name + "-I",
                                          boldItalic=name + "-B")
            mono = next((os.path.join(d, "DejaVuSansMono.ttf") for d in FONT_DIRS
                         if os.path.exists(os.path.join(d, "DejaVuSansMono.ttf"))), None)
            if mono:
                pdfmetrics.registerFont(TTFont("Mono", mono))
            return name, name + "-B", name + "-I", "Mono" if mono else "Courier"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"


REG, BOLD, ITAL, MONO = _register()


def st(name, **kw) -> ParagraphStyle:
    base = dict(fontName=REG, fontSize=9.5, leading=13, textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "brand": st("brand", fontName=BOLD, fontSize=10, textColor=BRAND),
    "h1": st("h1", fontName=BOLD, fontSize=22, leading=26, spaceAfter=2),
    "sub": st("sub", textColor=MUTED, fontSize=9.5),
    "h2": st("h2", fontName=BOLD, fontSize=14, leading=18, spaceBefore=14, spaceAfter=6),
    "h3": st("h3", fontName=BOLD, fontSize=11, leading=14, spaceBefore=8, spaceAfter=3),
    "body": st("body"), "small": st("small", fontSize=8, leading=10.5, textColor=MUTED),
    "quote": st("quote", fontName=ITAL, fontSize=9, leading=12),
    "cell": st("cell", fontSize=8.8, leading=11.5), "cellb": st("cellb", fontName=BOLD, fontSize=8.8, leading=11.5),
    "score": st("score", fontName=BOLD, fontSize=40, leading=42),
    "code": st("code", fontName=MONO, fontSize=6.8, leading=8.4, textColor=colors.HexColor("#1f2937")),
    "banner": st("banner", fontSize=8.5, textColor=colors.HexColor("#7a5b00")),
}


def clip(t: str, n: int) -> str:
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " \u2026"


def esc(t) -> str:
    t = html.escape(str(t or ""), quote=False)
    return re.sub(r"[​-‍﻿]", "", t)


def pill(text: str, fg: str, bg: str) -> Table:
    p = Paragraph(f'<font color="{fg}"><b>{esc(text)}</b></font>', st("pill", fontSize=8, leading=10))
    w = pdfmetrics.stringWidth(text, BOLD, 8) + 14
    t = Table([[p]], colWidths=[w], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
                           ("ROUNDEDCORNERS", [6, 6, 6, 6]), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def boxed(flowables, bg="#ffffff", border=LINE, pad=8) -> Table:
    t = Table([[flowables]], colWidths=[7.0 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg) if isinstance(bg, str) else bg),
                           ("BOX", (0, 0), (-1, -1), 0.6, border), ("ROUNDEDCORNERS", [8, 8, 8, 8]),
                           ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                           ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return t


def code(text: str, max_lines: int = 60) -> Table:
    lines = text.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["... (full file in the fix-kit folder)"]
    wrapped = []
    for ln in lines:
        while len(ln) > 118:
            wrapped.append(ln[:118])
            ln = "    " + ln[118:]
        wrapped.append(ln)
    return boxed(Preformatted("\n".join(wrapped), S["code"]), bg="#f5f7fa", pad=7)


def findings_table(items: list) -> Table:
    rows = [[Paragraph("<b>FINDING</b>", S["small"]), Paragraph("<b>WHAT AI SAID</b>", S["small"]),
             Paragraph("<b>THE TRUTH</b>", S["small"])]]
    for f in items:
        fg, bg = SEV[f["severity"]]
        left = [pill(f["severity"].title(), fg, bg), Spacer(1, 3), Paragraph(esc(f["title"]), S["cellb"])]
        mid = []
        for ev in f["evidence"][:2]:
            mid.append(Paragraph(f"“{esc(ev.get('ai_quote'))}”", S["quote"]))
            meta = f"{esc(ev.get('engine') or ev['provider'])} · {esc((ev.get('observed_at') or '')[:10])}"
            if ev.get("evidence_url"):
                meta += f" · {esc(ev['evidence_url'])}"
            mid.append(Paragraph(meta, S["small"]))
            mid.append(Spacer(1, 4))
        if not mid:
            mid = [Paragraph("Found on your own sources.", S["small"])]
        if len(f["evidence"]) > 2:
            mid.append(Paragraph(f"+{len(f['evidence']) - 2} more in the evidence log", S["small"]))
        right = [Paragraph(esc(f["true_value"]), S["cell"]),
                 Paragraph(f"Source: {esc(f['true_source'])}", S["small"]), Spacer(1, 3),
                 Paragraph(esc(f["explanation"]), S["small"])]
        rows.append([left, mid, right])
    t = Table(rows, colWidths=[1.55 * inch, 2.95 * inch, 2.5 * inch], repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def render_pdf(c: dict, path, sample: bool, promise: str) -> None:
    t, f, kit = c["truth"], c["f"], c["kit"]
    doc = BaseDocTemplate(str(path), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                          topMargin=0.85 * inch, bottomMargin=0.75 * inch,
                          title=f"What AI says about {t['name']}", author="AI Fact Watch")

    def frame_deco(canv, d):
        canv.saveState()
        canv.setFillColor(BRAND)
        canv.rect(0, letter[1] - 0.32 * inch, letter[0], 0.32 * inch, stroke=0, fill=1)
        canv.setFillColor(colors.white)
        canv.setFont(BOLD, 9)
        canv.drawString(0.75 * inch, letter[1] - 0.21 * inch, "AI FACT WATCH")
        canv.setFont(REG, 8.5)
        canv.drawRightString(letter[0] - 0.75 * inch, letter[1] - 0.21 * inch,
                             f"What AI says about {t['name']} · {f['date']}")
        canv.setFillColor(MUTED)
        canv.setFont(REG, 7.5)
        canv.drawString(0.75 * inch, 0.45 * inch,
                        "Observed on the dates shown. AI answers vary by location, account and time. "
                        "We document; we cannot change any AI vendor's answer.")
        canv.drawRightString(letter[0] - 0.75 * inch, 0.45 * inch, f"Page {d.page}")
        canv.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=frame_deco)])

    story = []
    if sample:
        story += [boxed(Paragraph("Sample report built from public sources and published news coverage to "
                                  "demonstrate the service. It has not been sent to the business.", S["banner"]),
                        bg="#fff8e1", border=colors.HexColor("#f0d58a"), pad=5), Spacer(1, 8)]
    story += [Paragraph(f"What AI says about {esc(t['name'])}", S["h1"]),
              Paragraph(f"{esc(t['town'])}, {esc(t.get('region', ''))} · Check date {f['date']} · "
                        f"Engines: {esc(', '.join(c['live_engines']) or 'none')}", S["sub"]), Spacer(1, 10)]

    gfg, gbg, _ = FLAGC[c["grade_color"]]
    counts = ", ".join(f"{n} {s}" for s, n in c["counts"].items() if n) or "no issues"
    left = [Paragraph(f"{f['score']}<font size=14 color='#5b6475'>/100</font>", S["score"]), Spacer(1, 4),
            pill(c["grade"], gfg, gbg)]
    right = [Paragraph(f"<b>Today: {esc(counts)}.</b>", S["body"]), Spacer(1, 3),
             Paragraph(esc(c["summary"]), S["body"])]
    if c["not_run"]:
        right += [Spacer(1, 4), Paragraph(f"Not queried in this run: {esc(', '.join(c['not_run']))} (no API key). "
                                          "Google AI Overview errors shown come from published news reports.",
                                          S["small"])]
    hero = Table([[left, right]], colWidths=[1.7 * inch, 5.3 * inch])
    hero.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                              ("ROUNDEDCORNERS", [10, 10, 10, 10]), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                              ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
    story += [hero, Spacer(1, 10)]

    cells = []
    for v in f["flags"].values():
        fg, bg, lab = FLAGC[v["flag"]]
        cells.append([Paragraph(f"<b>{esc(v['label'])}</b>", S["cell"]), Spacer(1, 3), pill(lab, fg, bg)])
    grid = Table([cells[:4], cells[4:8]], colWidths=[1.75 * inch] * 4)
    grid.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.6, LINE),
                              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 7),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    story += [grid]

    story += [Paragraph("Findings from today's check", S["h2"])]
    story += [findings_table(c["current"])] if c["current"] else [Paragraph("No errors in today's answers.", S["body"])]
    if c["history"]:
        story += [Paragraph("Documented history", S["h2"]),
                  Paragraph("Errors published by journalists, with the date reported. They show what customers "
                            "saw before this check. They do not count toward today's score.", S["sub"]),
                  Spacer(1, 6), findings_table(c["history"])]
    if f["confirmations"]:
        seen = []
        flagged = {e.get("ai_quote") for g in f["findings"] for e in g["evidence"]}
        per_field: dict = {}
        for x in f["confirmations"]:
            if x["ai_quote"] not in seen and x["ai_quote"] not in flagged and per_field.get(x["field"], 0) < 2:
                per_field[x["field"]] = per_field.get(x["field"], 0) + 1
                seen.append(x["ai_quote"])
        story += [Paragraph("What AI got right", S["h2"])]
        story += [Paragraph(f"✓ “{esc(q)}”", S["quote"]) for q in seen[:5]]

    # facts
    fa = t["facts"]
    hrs = Table([[Paragraph(d, S["cell"]), Paragraph(esc(h), S["cell"])] for d, h in hours_lines(fa["hours"]["value"])],
                colWidths=[1.1 * inch, 2.0 * inch])
    hrs.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE), ("TOPPADDING", (0, 0), (-1, -1), 2),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    facts = [Paragraph(f"<b>Address:</b> {esc(fa['address']['value'])}<br/><b>Phone:</b> {esc(fa['phone']['value'])}"
                       f"<br/><b>Website:</b> {esc(fa['website']['value'])}<br/><b>Status:</b> {esc(fa['status']['value'])}",
                       S["body"])]
    story += [KeepTogether([Paragraph("Your facts (from your own website)", S["h2"]),
                            Table([[facts, hrs]], colWidths=[3.7 * inch, 3.3 * inch],
                                  style=[("VALIGN", (0, 0), (-1, -1), "TOP")])])]
    for x in t.get("conflicts", []):
        story += [Paragraph(f"<b>Conflict in your own sources:</b> {esc(x['detail'])}", S["small"])]

    # fix kit
    story += [KeepTogether([Paragraph("Fix Kit", S["h2"]),
              boxed(Paragraph(esc(promise), S["body"]), bg="#eef8f7", border=BRAND, pad=7), Spacer(1, 6),
              Paragraph("1. Add structured data to your website", S["h3"]),
              Paragraph("Paste into the &lt;head&gt; of every page inside a &lt;script type=\"application/ld+json\"&gt; tag.",
                        S["body"]), code(kit["jsonld"], 70)]),
              Paragraph("2. Publish an “Official facts” page at /official-facts", S["h3"])]
    story += [Paragraph(f"<b>{esc(q)}</b> {esc(a)}", S["cell"]) for q, a in kit["faq"]]
    story += [KeepTogether([Paragraph("3. Upload llms.txt to your site root", S["h3"]), code(kit["llms_txt"])]),
              Paragraph("4. Google Business Profile edits", S["h3"])]
    story += [Paragraph(f"{i}. {esc(x)}", S["cell"]) for i, x in enumerate(kit["gbp"], 1)]
    story += [Paragraph("5. Correct these listings", S["h3"]),
              Paragraph("Paste this exact block everywhere:", S["body"]), code(kit["canonical"])]
    drows = [[Paragraph(f"<b>{esc(d['site'])}</b><br/><font size=7 color='#5b6475'>{esc(d['url'])}</font>", S["cell"]),
              Paragraph(esc(d["why"]), S["cell"])] for d in kit["directories"]]
    dt = Table(drows, colWidths=[3.0 * inch, 4.0 * inch])
    dt.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [Spacer(1, 4), dt, Paragraph("6. Report each wrong AI answer", S["h3"])]
    for k, steps in kit["feedback_howto"].items():
        story += [Paragraph(f"<b>{esc(k)}:</b> " + " ".join(f"({i}) {esc(s)}" for i, s in enumerate(steps, 1)),
                            S["cell"]), Spacer(1, 3)]
    story += [Paragraph("Pre-written feedback", S["h3"])]
    for x in kit["feedback"]:
        if x["severity"] in ("critical", "high", "medium"):
            story += [KeepTogether([Paragraph(f"<b>{esc(x['finding'])}</b> ({esc(x['engine'] or '')})", S["cell"]),
                                    code(x["text"]), Spacer(1, 4)])]
    if kit["disambiguation"]:
        story += [Paragraph("Same-name statement", S["h3"]), code(kit["disambiguation"])]

    # evidence log
    story += [Paragraph("Evidence log", S["h2"]),
              Paragraph("Every answer recorded for this check, verbatim, with the time observed (UTC).", S["sub"]),
              Spacer(1, 4)]
    rows = []
    for a in c["answers"]:
        body = [Paragraph(f"<b>{esc(a.get('query'))}</b>", S["cell"]),
                Paragraph(esc(clip(a.get("text") or a.get("note") or "", 2200)).replace("\n", "<br/>"), S["cell"])]
        if a.get("evidence_url"):
            body.append(Paragraph(f"Evidence: {esc(a['evidence_url'])}", S["small"]))
        if a.get("citations"):
            body.append(Paragraph("Sources cited: " + esc(", ".join(a["citations"][:4])), S["small"]))
        rows.append([Paragraph(f"{esc((a.get('observed_at') or '')[:16].replace('T', ' '))}<br/>"
                               f"<font color='#5b6475'>{esc(a.get('engine') or a['provider'])}</font>", S["cell"]), body])
    lt = Table(rows, colWidths=[1.45 * inch, 5.55 * inch])
    lt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [lt]
    doc.build(story)
