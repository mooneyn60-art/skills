---
name: ai-fact-watch
description: Run "AI Fact Watch", a self-serve service that checks what AI answers (Google AI Overviews, Gemini, ChatGPT, a web-grounded Claude check) say about a local business, finds the wrong facts (closed, hours, address, phone, invented deals, false legal claims, same-name mix-ups), and delivers a dated evidence report plus a Fix Kit. Use when running the scheduled routine, checking a business, building a report, or answering a customer.
---

# AI Fact Watch

Owners find out AI is wrong about them only when customers complain. We check
on request, document every wrong answer with date and engine, and hand over the
corrected sources. We never promise that any vendor will change an answer.

## Pipeline
```
truth.py  ->  ask_ai.py  ->  compare.py  ->  report.py (+ fixkit.py)
own sources   AI answers     findings        HTML + PDF + fix-kit/
truth/<slug>  answers/<slug>/<date>.json      findings/<slug>/<date>.json
```
- `scripts/truth.py`: website (+ listings, social) -> facts with source URLs;
  flags conflicts between the site's text, its structured data and listings.
- `scripts/ask_ai.py`: six customer questions to each engine with a key
  (`SERPAPI_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`); skips missing keys;
  `--print-queries` / `--import` for the keyless claude-websearch mode.
- `scripts/compare.py`: deterministic findings with verbatim AI quotes,
  severity, score, flags, and changes since the last check.
- `scripts/report.py` / `report_pdf.py` / `fixkit.py`: report and Fix Kit
  (JSON-LD, official-facts page, llms.txt, Google Business Profile edits,
  AI feedback texts, listings, same-name statement).
- `scripts/ops.py`: requests, payments, cancellations, refunds, opt-outs;
  `preflight` gates all outbound email.
- `routines/RUN.md`: the zero-touch scheduled run. `routines/SETUP.md`: the
  owner's one-time setup. `templates/emails.md`: every email we send.
- `site/index.html`: landing page with the free-check form and pricing.
- `samples/`: two demo reports built from public news cases
  (`samples/rebuild.sh` reproduces them).

## Quick start (one business, no keys)
```bash
cd scripts
python3 truth.py --name "Biz" --town Town --region ST --website https://biz.example
python3 ask_ai.py --slug biz-town --print-queries     # run each with WebSearch, save verbatim
python3 ask_ai.py --slug biz-town --import answers.json
python3 compare.py --slug biz-town
python3 report.py --slug biz-town
```

## Rules
- Inbound only: email people who requested a check, paid, or wrote to us.
- Quotes are verbatim and dated; "observed on <date> via <engine>".
- Press-reported errors are "documented history" and do not count toward today's score.
- Customer data in `data/` is git-ignored. Never publish a customer's results.
