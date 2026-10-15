#!/usr/bin/env python3
"""Render the "What AI says about <business>" report as HTML and PDF, with
the Fix Kit, plus the Fix Kit files themselves.

Usage:
  python report.py --slug X [--date YYYY-MM-DD] [--out DIR] [--sample]

Output (default DIR = samples/<slug>/):
  report.html, report.pdf, fix-kit/*
--sample adds a "sample prepared from public sources, not sent" banner.
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from common import ANSWERS_DIR, FINDINGS_DIR, ROOT, TRUTH_DIR, hours_to_text, load_json
from fixkit import build_kit, hours_lines, write_kit
from report_pdf import render_pdf

E = html.escape
SEV_LABEL = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}
FLAG_LABEL = {"red": "Wrong", "yellow": "Gap", "green": "Correct", "grey": "Not seen"}
ALL_ENGINES = {"serpapi": "Google AI Overview", "gemini": "Gemini", "openai": "ChatGPT",
               "claude-websearch": "Claude web search"}
PROMISE = ("We detect and document what AI answers say, and we give you corrected sources. "
           "We cannot make Google, OpenAI or any AI vendor change an answer, and we never promise that.")


def grade(score: int) -> tuple[str, str]:
    if score >= 80:
        return "Mostly accurate", "green"
    if score >= 50:
        return "Needs attention", "yellow"
    return "At risk", "red"


def context(slug: str, date: str | None) -> dict:
    truth = load_json(TRUTH_DIR / f"{slug}.json")
    files = sorted((FINDINGS_DIR / slug).glob("????-??-??.json"))
    fpath = FINDINGS_DIR / slug / f"{date}.json" if date else files[-1]
    findings = load_json(fpath)
    answers = load_json(ANSWERS_DIR / slug / f"{findings['date']}.json")["answers"]
    current = [f for f in findings["findings"] if f["current"]]
    history = [f for f in findings["findings"] if f["history_only"]]
    providers = {a["provider"] for a in answers}
    live = sorted({a.get("engine") for a in answers if a.get("mode") != "press-report"})
    not_run = [v for k, v in ALL_ENGINES.items() if k not in providers]
    g, gc = grade(findings["score"])
    counts = {s: sum(1 for f in current if f["severity"] == s) for s in SEV_LABEL}
    top = next((f for f in current if f["severity"] in ("critical", "high")), None) or \
        (current[0] if current else None)
    if top:
        summary = f"Most important today: {top['title']}."
    else:
        summary = "No errors found in today's answers."
    if history:
        summary += (f" Published reports also document {len(history)} earlier error"
                    f"{'s' if len(history) != 1 else ''} (shown under Documented history).")
    return {"truth": truth, "f": findings, "answers": answers, "current": current, "history": history,
            "kit": build_kit(truth, findings), "grade": g, "grade_color": gc, "counts": counts,
            "summary": summary, "live_engines": live, "not_run": not_run}


# ------------------------------------------------------------------- HTML
CSS = """
:root{--ink:#14213d;--muted:#5b6475;--line:#e3e7ee;--bg:#f6f7fb;--card:#fff;--brand:#0b6e6e;
--red:#c0392b;--red-bg:#fdecea;--amber:#b9770e;--amber-bg:#fdf3e1;--green:#1e8449;--green-bg:#e8f6ee;
--grey:#7f8a99;--grey-bg:#eef1f5}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 "Inter","Segoe UI",system-ui,-apple-system,sans-serif}
.wrap{max-width:960px;margin:0 auto;padding:24px 16px 64px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:.02em;color:var(--brand)}
.brand .dot{width:28px;height:28px;border-radius:8px;background:var(--brand);color:#fff;display:grid;
place-items:center;font-size:14px}
.sample{background:#fff8e1;border:1px solid #f0d58a;color:#7a5b00;padding:8px 12px;border-radius:8px;
font-size:13px;margin:14px 0}
h1{font-size:30px;line-height:1.15;margin:18px 0 4px}h2{font-size:20px;margin:36px 0 12px}
h3{font-size:16px;margin:20px 0 8px}.sub{color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
.hero{display:grid;grid-template-columns:170px 1fr;gap:20px;align-items:center;margin-top:18px}
.score{font-size:54px;font-weight:800;line-height:1}.score small{font-size:18px;color:var(--muted)}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:700;
white-space:nowrap}
.red{background:var(--red-bg);color:var(--red)}.yellow{background:var(--amber-bg);color:var(--amber)}
.green{background:var(--green-bg);color:var(--green)}.grey{background:var(--grey-bg);color:var(--grey)}
.critical,.high{background:var(--red-bg);color:var(--red)}.medium{background:var(--amber-bg);color:var(--amber)}
.low{background:var(--grey-bg);color:var(--grey)}
.flags{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}
.flag{border-radius:12px;padding:10px 12px;border:1px solid var(--line);background:#fff}
.flag b{display:block;font-size:13px}.flag .pill{margin-top:6px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;
overflow:hidden;font-size:14px}th,td{text-align:left;vertical-align:top;padding:10px 12px;
border-bottom:1px solid var(--line)}th{background:#f1f4f9;font-size:12px;text-transform:uppercase;
letter-spacing:.04em;color:var(--muted)}
blockquote{margin:0;padding:8px 12px;border-left:3px solid var(--red);background:#fffafa;
border-radius:0 8px 8px 0;font-style:italic}
.meta{color:var(--muted);font-size:12px;margin-top:6px}.src{font-size:12px;word-break:break-all}
pre{background:#0f172a;color:#e2e8f0;padding:14px;border-radius:10px;overflow:auto;font-size:12px;
line-height:1.45;white-space:pre-wrap;word-break:break-word}
ol li,ul li{margin:4px 0}.log{font-size:13px}.log td{padding:8px 10px}
.promise{border-left:4px solid var(--brand);background:#eef8f7;padding:12px 14px;border-radius:0 10px 10px 0}
.kit-step{display:flex;gap:10px;align-items:baseline}.n{background:var(--brand);color:#fff;border-radius:50%;
min-width:24px;height:24px;display:inline-grid;place-items:center;font-size:12px;font-weight:700}
footer{margin-top:40px;color:var(--muted);font-size:12px}
@media (max-width:700px){.hero{grid-template-columns:1fr}.flags{grid-template-columns:repeat(2,1fr)}
table.findings thead{display:none}table.findings tr{display:block;border-bottom:8px solid var(--bg)}
table.findings td{display:block;border:none}h1{font-size:25px}}
@media print{body{background:#fff}.card,table{break-inside:avoid}}
"""


def link(url: str | None) -> str:
    if not url:
        return ""
    return f'<a class="src" href="{E(url)}">{E(url)}</a>'


def findings_rows(items: list) -> str:
    rows = []
    for f in items:
        quotes = []
        for ev in f["evidence"][:3]:
            q = ev.get("ai_quote") or ""
            meta = f'{E(ev.get("engine") or ev["provider"])} &middot; {E((ev.get("observed_at") or "")[:10])}'
            if ev.get("query"):
                meta += f' &middot; asked: &ldquo;{E(ev["query"])}&rdquo;'
            if ev.get("evidence_url"):
                meta += f' &middot; {link(ev["evidence_url"])}'
            qh = E(q) if q.startswith("(") else f"&ldquo;{E(q)}&rdquo;"
            quotes.append(f"<blockquote>{qh}</blockquote><div class='meta'>{meta}</div>")
        said = "".join(quotes) or "<span class='meta'>Found on your own sources (no AI quote).</span>"
        if len(f["evidence"]) > 3:
            said += f"<div class='meta'>+{len(f['evidence']) - 3} more in the evidence log</div>"
        rows.append(
            f"<tr><td><span class='pill {f['severity']}'>{SEV_LABEL[f['severity']]}</span>"
            f"<div style='margin-top:6px;font-weight:600'>{E(f['title'])}</div></td>"
            f"<td>{said}</td><td>{E(f['true_value'])}<div class='meta'>Source: {link(f['true_source'])}</div>"
            f"<div class='meta'>{E(f['explanation'])}</div></td></tr>")
    return ("<table class='findings'><thead><tr><th style='width:22%'>Finding</th><th style='width:43%'>"
            "What AI said</th><th>The truth</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>")


def render_html(c: dict, sample: bool) -> str:
    t, f, kit = c["truth"], c["f"], c["kit"]
    flags = "".join(f"<div class='flag'><b>{E(v['label'])}</b><span class='pill {v['flag']}'>"
                    f"{FLAG_LABEL[v['flag']]}</span></div>" for v in f["flags"].values())
    counts = " &middot; ".join(f"{n} {SEV_LABEL[s].lower()}" for s, n in c["counts"].items() if n) or "no issues"
    current = findings_rows(c["current"]) if c["current"] else "<p>No errors in today's answers.</p>"
    history = ""
    if c["history"]:
        history = ("<h2>Documented history</h2><p class='sub'>Errors published by journalists, with the date "
                   "they were reported. They show what customers saw before this check and are kept in the "
                   "evidence log. They do not count toward today's score.</p>" + findings_rows(c["history"]))
    right = ""
    if f["confirmations"]:
        seen = []
        for x in f["confirmations"]:
            if x["ai_quote"] not in seen:
                seen.append(x["ai_quote"])
        right = ("<h2>What AI got right</h2><ul>" + "".join(f"<li>&ldquo;{E(q)}&rdquo;</li>" for q in seen[:6])
                 + "</ul>")
    hrs = "".join(f"<tr><td>{d}</td><td>{E(h)}</td></tr>" for d, h in hours_lines(t["facts"]["hours"]["value"]))
    fb = "".join(
        f"<li><b>{E(x['finding'])}</b> <span class='pill {x['severity']}'>{SEV_LABEL[x['severity']]}</span>"
        f"<div class='meta'>Where: {E(x['engine'] or '')}</div><pre>{E(x['text'])}</pre></li>"
        for x in kit["feedback"] if x["severity"] in ("critical", "high", "medium"))
    howto = "".join(f"<h3>{E(k.title())}</h3><ol>" + "".join(f"<li>{E(s)}</li>" for s in v) + "</ol>"
                    for k, v in kit["feedback_howto"].items())
    dirs = "".join(f"<tr><td><b>{E(d['site'])}</b><div class='src'>{link(d['url'])}</div></td>"
                   f"<td>{E(d['why'])}</td></tr>" for d in kit["directories"])
    faq = "".join(f"<p><b>{E(q)}</b><br>{E(a)}</p>" for q, a in kit["faq"])
    disamb = (f"<h3>Same-name statement</h3><p>Use on your About page, Google profile description and "
              f"directory listings:</p><pre>{E(kit['disambiguation'])}</pre>") if kit["disambiguation"] else ""
    log = "".join(
        f"<tr><td>{E((a.get('observed_at') or '')[:16].replace('T', ' '))} UTC<div class='meta'>"
        f"{E(a.get('engine') or a['provider'])}</div></td><td><b>{E(a.get('query') or '')}</b>"
        f"<div style='white-space:pre-wrap;margin-top:4px'>{E((a.get('text') or a.get('note') or '')[:1400])}</div>"
        + (f"<div class='meta'>Evidence: {link(a['evidence_url'])}</div>" if a.get("evidence_url") else "")
        + ("<div class='meta'>Sources cited: " + " ".join(link(u) for u in a.get("citations", [])[:5]) + "</div>"
           if a.get("citations") else "") + "</td></tr>"
        for a in c["answers"])
    not_run = (f"<p class='meta'>Not queried in this run: {E(', '.join(c['not_run']))} (no API key configured). "
               "Google AI Overview errors above come from published news reports.</p>") if c["not_run"] else ""
    banner = ("<div class='sample'>Sample report built from public sources and published news coverage to "
              "demonstrate the service. It has not been sent to the business.</div>") if sample else ""
    conflicts = "".join(f"<li>{E(x['detail'])}</li>" for x in t.get("conflicts", []))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>What AI says about {E(t['name'])} | AI Fact Watch</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="brand"><span class="dot">&#10003;</span>AI Fact Watch</div>{banner}
<h1>What AI says about {E(t['name'])}</h1>
<div class="sub">{E(t['town'])}, {E(t.get('region', ''))} &middot; Check date {E(f['date'])} &middot;
Engines: {E(', '.join(c['live_engines']) or 'none')}</div>
<div class="card hero"><div><div class="score">{f['score']}<small>/100</small></div>
<span class="pill {c['grade_color']}">{c['grade']}</span></div>
<div><b>Today: {counts}.</b><p style="margin:6px 0 0">{E(c['summary'])}</p>{not_run}</div></div>
<div class="flags">{flags}</div>
<h2>Findings from today's check</h2>{current}
{history}{right}
<h2>Your facts (from your own website)</h2>
<div class="card"><p><b>Address:</b> {E(t['facts']['address']['value'] or '')}<br><b>Phone:</b>
{E(t['facts']['phone']['value'] or '')}<br><b>Website:</b> {link(t['facts']['website']['value'])}<br>
<b>Status:</b> {E(t['facts']['status']['value'])}</p><table>{hrs}</table>
{('<p><b>Conflicts in your own sources:</b></p><ul>' + conflicts + '</ul>') if conflicts else ''}
<p class="meta">Collected {E(t['collected_at'][:16].replace('T', ' '))} UTC from {link(t['facts']['website']['value'])}</p></div>
<h2>Fix Kit</h2>
<div class="promise">{E(PROMISE)}</div>
<div class="card" style="margin-top:12px">
<div class="kit-step"><span class="n">1</span><div><b>Add structured data to your website.</b> Paste into the
&lt;head&gt; of every page, inside <code>&lt;script type="application/ld+json"&gt;</code>:</div></div>
<pre>{E(kit['jsonld'])}</pre>
<div class="kit-step"><span class="n">2</span><div><b>Publish an "Official facts" page</b> at
/official-facts and link it in your footer. Text (the file in the kit includes the FAQ schema):</div></div>
<div style="padding-left:34px">{faq}</div>
<div class="kit-step"><span class="n">3</span><div><b>Upload llms.txt</b> to your site root:</div></div>
<pre>{E(kit['llms_txt'])}</pre>
<div class="kit-step"><span class="n">4</span><div><b>Google Business Profile edits</b>, in order:</div></div>
<ol>{''.join(f'<li>{E(x)}</li>' for x in kit['gbp'])}</ol>
<div class="kit-step"><span class="n">5</span><div><b>Correct these listings.</b> Paste this exact block:</div></div>
<pre>{E(kit['canonical'])}</pre><table>{dirs}</table>
<div class="kit-step" style="margin-top:14px"><span class="n">6</span><div><b>Report each wrong AI answer.</b>
Log the date of every submission.</div></div>{howto}<h3>Pre-written feedback</h3><ol>{fb}</ol>{disamb}
</div>
<h2>Evidence log</h2><p class="sub">Every answer recorded for this check, verbatim, with the time it was observed.
AI answers vary by location, account and time; findings are stated as "observed on" these dates.</p>
<table class="log"><thead><tr><th style="width:22%">When / engine</th><th>Question and answer</th></tr></thead>
<tbody>{log}</tbody></table>
<footer>AI Fact Watch &middot; Report generated {E(f['generated_at'][:16].replace('T', ' '))} UTC &middot; {E(PROMISE)}</footer>
</div></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--date")
    ap.add_argument("--out")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()
    c = context(a.slug, a.date)
    out = Path(a.out) if a.out else ROOT / "samples" / a.slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.html").write_text(render_html(c, a.sample))
    render_pdf(c, out / "report.pdf", a.sample, PROMISE)
    write_kit(c["kit"], out / "fix-kit")
    print(f"Wrote {out/'report.html'}, {out/'report.pdf'}, {out/'fix-kit'}/  (score {c['f']['score']})")
    print("Hours on file:", hours_to_text(c["truth"]["facts"]["hours"]["value"] or {}))


if __name__ == "__main__":
    main()
