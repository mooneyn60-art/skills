#!/usr/bin/env python3
"""Rebuild the `const DATA = {...}` block in town.html from the agents' repos.

Every number on the dashboard comes from here. Sources are read with
`git show <branch>:<path>` so nothing is checked out or modified. If a value is
not in a repo it is emitted as None and the page renders an em dash.
No money or earnings figures are ever read or written.

Usage:
    python scripts/build_data.py            # read origin/* as they are now
    python scripts/build_data.py --fetch    # git fetch origin first
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/user/skills")
HERE = Path(__file__).resolve().parent.parent
TOWN = HERE / "town.html"

TARS_BR = "origin/claude/package-installation-setup-yv4j79"
TARS = "skills/robinhood-autotrader"
SITES_BR = "origin/claude/tiktok-automation-full-scale-8jisnq"
SITES = "skills/local-booking-sites"
KDP_BR = "origin/claude/dreamy-galileo-9cchpj"
KDP_BOOKS = "kdp-books"
DENT_BR = "origin/claude/dental-ai-visibility"
DENT = "skills/dental-ai-visibility"
MEAT = "skills/oh-meatball"

BEGIN, END = "/*DATA:BEGIN*/", "/*DATA:END*/"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ---------- git helpers ----------
def git(*args: str) -> str | None:
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def show(branch: str, path: str) -> str | None:
    return git("show", f"{branch}:{path}")


def ls(branch: str, path: str, recursive: bool = False) -> list[str]:
    args = ["ls-tree", "--name-only"] + (["-r"] if recursive else []) + [branch, path.rstrip("/") + "/"]
    out = git(*args)
    return out.split() if out else []


def commits(branch: str, path: str, n: int = 4) -> list[dict]:
    out = git("log", branch, f"-{n}", "--format=%cs\t%s", "--", path) or ""
    rows = []
    for line in out.splitlines():
        day, _, subj = line.partition("\t")
        rows.append({"when": short_date(day), "text": clip(subj, 92)})
    return rows


def short_date(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        return datetime.fromisoformat(iso[:10]).strftime("%b %-d")
    except ValueError:
        return iso[:10]


def clip(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def grid(hours_by_day: dict[int, list[int]], kind: str = "run") -> list[list]:
    return [[d, h, kind] for d, hs in hours_by_day.items() for h in hs]


# ---------- agents ----------
def tars() -> dict:
    raw = show(TARS_BR, f"{TARS}/paper/trades.jsonl") or ""
    rows = [json.loads(l) for l in raw.splitlines() if l.strip()]
    tradeable = [r for r in rows if str(r.get("instrument", "")).startswith(("equity", "option", "covered"))]
    taken = [r for r in tradeable if r.get("exit_reason") != "not_taken"]
    inst = Counter("options" if str(r.get("instrument")).startswith(("option", "covered")) else "equity" for r in taken)
    live_rows = sum(1 for r in rows if r.get("account") == "live")

    shadow = json.loads(show(TARS_BR, f"{TARS}/paper/shadow/state.json") or "{}")
    shadow_open = sum(len(b.get("pos", {})) for b in shadow.get("books", {}).values()) if shadow else None
    shadow_days = len([p for p in ls(TARS_BR, f"{TARS}/paper/shadow/daily") if p.endswith(".json")])
    desk = json.loads(show(TARS_BR, f"{TARS}/paper/datafarm/paper_book.json") or "{}")
    research = len([p for p in ls(TARS_BR, f"{TARS}/research") if p.endswith(".md")])
    routines = len([p for p in ls(TARS_BR, f"{TARS}/routines") if p.endswith(".md") and not p.endswith("README.md")])

    def stamp(r):
        v = r.get("closed") or r.get("opened")
        return v if isinstance(v, str) else ""

    recent = sorted((r for r in taken if stamp(r)), key=stamp)[-4:][::-1]
    activity = []
    for r in recent:
        kind = "option" if str(r.get("instrument")).startswith("option") else r.get("instrument", "")
        acct = r.get("account")
        tag = "LIVE" if acct == "live" else ("PAPER" if acct == "paper" else "")
        why = str(r.get("exit_reason") or "open").replace("_", " ")
        activity.append({"when": short_date(stamp(r)), "text": clip(f"{r.get('symbol', '?')} {kind} · {why}", 70), "tag": tag})
    activity += commits(TARS_BR, TARS, 3)

    # 17 13-21 * * 1-5 UTC = 9:17am-5:17pm ET; Friday refresh 30 21 * * 5 UTC = 5:30pm ET
    sched = grid({d: list(range(9, 18)) for d in range(5)}) + [[4, 17, "alt"]]
    return {
        "id": "tars", "name": "TARS", "title": "Trading desk",
        "role": "Researches markets with parallel read-only desks, then logs every trade, stop and pass to one ledger. All execution goes through rule gates and the owner's confirmation.",
        "status": {"text": "On duty · market hours", "tone": "green"},
        "chips": [{"text": "LIVE agentic account", "tone": "red"}, {"text": "PAPER shadow book", "tone": "blue"}, {"text": "PAPER intraday desk", "tone": "blue"}],
        "schedule": {
            "summary": "Hourly 9:17am–5:17pm ET, weekdays (9 checks/day) + Friday data refresh 5:30pm ET",
            "grid": sched,
        },
        "kpis": [
            {"label": "Trades logged", "value": len(taken), "note": f"{inst['equity']} equity · {inst['options']} options"},
            {"label": "Ledger rows", "value": len(rows), "note": f"{live_rows} tagged live account"},
            {"label": "Shadow book", "value": shadow_open, "note": f"open paper positions, 2 books · {shadow_days} daily snapshots"},
            {"label": "Desk paper trades", "value": len(desk.get("trades", [])) if desk else None, "note": "intraday sim since " + short_date(desk.get("forward_start"))},
            {"label": "Research notes", "value": research, "note": "studies in research/"},
            {"label": "Routines", "value": routines, "note": "scheduled playbooks"},
        ],
        "activity": activity,
        "source": f"{TARS_BR.removeprefix('origin/')} · {TARS}/paper/trades.jsonl",
        "note": "Live-account trades are real orders on a dedicated agentic sub-account; the shadow book and intraday desk are paper. Dollar P&L is deliberately not shown.",
    }


def sites() -> dict:
    examples = [p for p in ls(SITES_BR, f"{SITES}/examples") if p.endswith(".json")]
    leads_csv = show(SITES_BR, f"{SITES}/leads.csv")
    leads = len(list(csv.DictReader(io.StringIO(leads_csv)))) if leads_csv else None
    built = [p for p in ls(SITES_BR, SITES, recursive=True) if p.endswith(".html")]
    return {
        "id": "paige", "name": "Paige", "title": "Booking-site builder",
        "role": "Turns a local business's 'DM to book' Instagram or Google profile into a one-page mobile booking site, then drafts a personal pitch for the owner. Never invents prices, reviews or hours.",
        "status": {"text": "Ready · waiting on leads", "tone": "amber"},
        "chips": [{"text": "DEMO site only", "tone": "amber"}],
        "schedule": {"summary": "Hourly, every day", "grid": grid({d: list(range(24)) for d in range(7)})},
        "kpis": [
            {"label": "Real sites built", "value": len(built) if built else None, "note": "none committed to the repo yet"},
            {"label": "Demo sites", "value": len(examples), "note": "fictional test business"},
            {"label": "Leads logged", "value": leads, "note": "leads.csv not in repo"},
            {"label": "Pipeline stages", "value": 4, "note": "find → extract → build → pitch"},
        ],
        "activity": commits(SITES_BR, SITES, 4),
        "source": f"{SITES_BR.removeprefix('origin/')} · {SITES}",
        "note": "The builder and lead tracker exist; no real client site or lead list is committed yet.",
    }


def kdp() -> dict:
    files = ls(KDP_BR, KDP_BOOKS, recursive=True)
    books = sorted({p.split("/")[1] for p in files if p.endswith("_interior.pdf")})
    puzzles = 0
    titles = []
    for b in books:
        spec = json.loads(show(KDP_BR, f"{KDP_BOOKS}/{b}/book.json") or "{}")
        puzzles += len(spec.get("puzzles", []))
        meta = json.loads(show(KDP_BR, f"{KDP_BOOKS}/{b}/metadata.json") or "{}")
        titles.append(meta.get("title") or spec.get("title") or b)
    pins = sum(1 for p in files if "/pins/" in p and p.endswith(".png"))
    scripts = sum(1 for p in files if p.endswith("video_script.md"))
    return {
        "id": "pine", "name": "Hollow Pine Press", "title": "KDP puzzle-book publisher",
        "role": "Builds a large-print word-search book each week: puzzles, print-ready interior and cover PDFs, KDP listing copy, Pinterest pins and a short-video script.",
        "status": {"text": "Weekly build on track", "tone": "green"},
        "chips": [{"text": "Print-ready files", "tone": "green"}],
        "schedule": {"summary": "Weekly, Monday (next book in the series)", "grid": [[0, None, "day"]]},
        "kpis": [
            {"label": "Books built", "value": len(books), "note": "interior + cover PDFs"},
            {"label": "Puzzles", "value": puzzles, "note": "across all books"},
            {"label": "Pin images", "value": pins, "note": "Pinterest graphics"},
            {"label": "Video scripts", "value": scripts, "note": "promo shorts"},
            {"label": "Live on Amazon", "value": None, "note": "KDP status not tracked in repo"},
        ],
        "activity": commits(KDP_BR, KDP_BOOKS, 4),
        "titles": titles,
        "source": f"{KDP_BR.removeprefix('origin/')} · {KDP_BOOKS}/",
        "note": "Sales and royalties are not in the repo, so none are shown.",
    }


def dental() -> dict:
    cfg = json.loads(show(DENT_BR, f"{DENT}/config.json") or "{}")
    missing = [k for k in cfg.get("required_for_sending", []) if not cfg.get(k)]
    reports = [p for p in ls(DENT_BR, f"{DENT}/reports") if not p.endswith(".gitkeep")]
    leads_csv = show(DENT_BR, f"{DENT}/data/leads.csv")
    leads = len(list(csv.DictReader(io.StringIO(leads_csv)))) if leads_csv else 0
    sending = bool(cfg.get("send_enabled")) and not missing
    activity = commits(DENT_BR, DENT, 3)
    if missing:
        activity.insert(0, {"when": "now", "text": "Outreach locked until set: " + ", ".join(m.replace("_", " ") for m in missing)})
    return {
        "id": "doc", "name": "Doc", "title": "Dentist AI-visibility auditor",
        "role": "Scores independent dental practices' websites on the signals AI assistants use to recommend a local dentist, then emails a free audit with the top three gaps.",
        "status": {"text": "Sending" if sending else "Setup · outreach off", "tone": "green" if sending else "amber"},
        "chips": [{"text": "Outreach ON" if sending else "Outreach OFF", "tone": "green" if sending else "amber"}],
        "schedule": {"summary": "On demand (weekday daily-run routine is written, runs once enabled)", "grid": []},
        "kpis": [
            {"label": "Audits run", "value": len(reports), "note": "client report folders"},
            {"label": "Leads", "value": leads, "note": "data/leads.csv"},
            {"label": "Leads per day", "value": cfg.get("new_leads_per_day"), "note": "configured cap"},
            {"label": "Config gaps", "value": len(missing), "note": "fields before sending"},
        ],
        "activity": activity,
        "source": f"{DENT_BR.removeprefix('origin/')} · {DENT}",
        "note": "No audits or leads are committed yet; the auditor is built and waiting for its city and sender details.",
    }


def meatball() -> dict:
    path = REPO / MEAT / "data/log.csv"
    text = path.read_text(encoding="utf-8") if path.exists() else (git("show", f"HEAD:{MEAT}/data/log.csv") or "")
    rows = list(csv.DictReader(io.StringIO(text)))
    parts = sorted({r["part"] for r in rows if r.get("part", "").isdigit()}, key=int)
    recaps = {r["part"] for r in rows if r.get("part", "").startswith("recap")}
    credits = sum(int(r["credits"]) for r in rows if (r.get("credits") or "").isdigit())
    exp_text = (REPO / MEAT / "data/experiments.csv").read_text(encoding="utf-8") if (REPO / MEAT / "data/experiments.csv").exists() else ""
    exps = list(csv.DictReader(io.StringIO(exp_text)))
    met_text = (REPO / MEAT / "data/metrics.csv").read_text(encoding="utf-8") if (REPO / MEAT / "data/metrics.csv").exists() else ""
    metrics = list(csv.DictReader(io.StringIO(met_text)))
    views = sum(int(m["views"]) for m in metrics if (m.get("views") or "").isdigit()) if metrics else None
    queued = sum(1 for r in rows if r.get("status", "").startswith("awaiting"))

    def status(s: str) -> str:
        s = s or ""
        if s.startswith("awaiting"):
            return "queued, awaiting approval"
        return s.replace("_", " ")

    activity = []
    for r in rows[::-1][:5]:
        title = re.sub(r"\s*\|\s*Oh Meatball.*?(?=\(|$)", " ", r.get("title", "")).strip()
        title = re.sub(r"[^\w\s,.'’…()&!?-]", "", title).strip()
        label = f"Pt {r['part']}" if r.get("part", "").isdigit() else "Recap"
        activity.append({"when": short_date(r.get("date")), "text": clip(f"{label}: {title} · {status(r.get('status'))}", 84)})
    return {
        "id": "meatball", "name": "Meatball Studio", "title": "AI cat soap-opera studio",
        "role": "Writes, animates and schedules 'Oh Meatball', a vertical soap opera starring a very round orange cat. Every part ends on a cliffhanger.",
        "status": {"text": f"{queued} uploads awaiting approval" if queued else "Producing", "tone": "amber" if queued else "green"},
        "chips": [{"text": "Season 1: The Wedding", "tone": "pink"}],
        "schedule": {"summary": "Daily production run (+ nightly post check, weekly review)", "grid": [[d, None, "day"] for d in range(7)]},
        "kpis": [
            {"label": "Episodes made", "value": len(parts), "note": "story parts" + (f" + {len(recaps)} recap" if recaps else "")},
            {"label": "Uploads queued", "value": queued, "note": "awaiting owner approval"},
            {"label": "Gen credits used", "value": credits, "note": "video-model credits in log"},
            {"label": "Experiments", "value": len(exps), "note": f"{sum(1 for e in exps if e.get('status') == 'open')} open"},
            {"label": "Views", "value": views, "note": "metrics.csv has no rows yet" if views is None else "all platforms"},
        ],
        "activity": activity,
        "source": f"claude/off-the-lot · {MEAT}/data/log.csv",
        "note": "Views and follower numbers appear here once metrics.csv starts filling.",
    }


def night_owl() -> dict:
    return {
        "id": "owl", "name": "Night Owl", "title": "Dark Facts TikTok channel",
        "role": "A faceless TikTok channel run by two scheduled agents: a nightly generator makes the next Dark Facts video and a daily publisher posts it. Facts only, no fiction.",
        "status": {"text": "Scheduled", "tone": "purple"},
        "chips": [{"text": "Schedule only, no repo data", "tone": "purple"}],
        "schedule": {"summary": "Nightly generate 3:00am ET · publish 11:30am ET", "grid": grid({d: [3] for d in range(7)}) + grid({d: [11] for d in range(7)}, "alt")},
        "kpis": [
            {"label": "Runs per day", "value": 2, "note": "generate + publish"},
            {"label": "Generate", "value": "3:00", "note": "am ET, nightly"},
            {"label": "Publish", "value": "11:30", "note": "am ET, daily"},
            {"label": "Videos posted", "value": None, "note": "not tracked in a repo"},
        ],
        "activity": [
            {"when": "3:00am", "text": "Nightly generator run (creates the next Dark Facts video)"},
            {"when": "11:30am", "text": "Daily publisher run (posts to TikTok)"},
        ],
        "source": "trigger schedule (no repository data)",
        "note": "This agent has no data in the repos; only its schedule is shown.",
    }


def build() -> dict:
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "days": DAYS,
        "agents": [tars(), sites(), kdp(), dental(), meatball(), night_owl()],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fetch", action="store_true", help="git fetch origin before reading")
    ap.add_argument("--print", action="store_true", help="print DATA instead of writing town.html")
    args = ap.parse_args()
    if args.fetch:
        git("fetch", "-q", "origin")
    data = build()
    blob = json.dumps(data, ensure_ascii=False, indent=1)
    if args.print:
        print(blob)
        return 0
    html = TOWN.read_text(encoding="utf-8")
    if BEGIN not in html or END not in html:
        print(f"markers {BEGIN} / {END} not found in {TOWN}", file=sys.stderr)
        return 1
    head, rest = html.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    TOWN.write_text(f"{head}{BEGIN}const DATA = {blob};{END}{tail}", encoding="utf-8")
    print(f"wrote DATA ({len(blob)} bytes) to {TOWN}")
    for a in data["agents"]:
        print(f"  {a['name']:<18} " + " · ".join(f"{k['label']}={k['value'] if k['value'] is not None else '—'}" for k in a["kpis"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
