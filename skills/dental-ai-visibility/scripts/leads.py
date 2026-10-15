#!/usr/bin/env python3
"""Pipeline tracker for dental-ai-visibility. One CSV, one row per practice.

Usage:
    python leads.py add "Bright Smile Dental" --website brightsmile.com --email hi@brightsmile.com --city Orlando
    python leads.py set "Bright Smile Dental" emailed --score 45 --note "audit sent"
    python leads.py list [--status emailed]
    python leads.py due            # who needs a follow-up today
    python leads.py optout hi@brightsmile.com
    python leads.py can-email hi@brightsmile.com   # exit 1 if suppressed or already contacted twice
    python leads.py stats

Only public business facts and pipeline status go in this file; the repo is
public. Never store the text of anyone's email reply here.
"""

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data"
LEADS = ROOT / "leads.csv"
OPTOUT = ROOT / "optout.txt"
FIELDS = ["name", "website", "email", "phone", "city", "score", "status",
          "first_contact", "last_contact", "touches", "notes"]
STATUSES = ["new", "audited", "emailed", "followed_up", "replied", "interested",
            "client", "lost", "optout", "skip"]
FOLLOW_UP_AFTER_DAYS = 4
MAX_TOUCHES = 2  # first email + one follow-up, then stop


def load() -> list[dict]:
    if not LEADS.exists():
        return []
    with LEADS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(rows: list[dict]) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    with LEADS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def optouts() -> set[str]:
    if not OPTOUT.exists():
        return set()
    return {l.strip().lower() for l in OPTOUT.read_text().splitlines() if l.strip()}


def suppressed(email: str) -> bool:
    email = email.lower()
    blocked = optouts()
    return email in blocked or ("@" + email.split("@")[-1]) in blocked


def find(rows: list[dict], name: str) -> dict:
    for r in rows:
        if r["name"].lower() == name.lower():
            return r
    sys.exit(f"error: no lead named {name!r}")


def norm_site(s: str) -> str:
    return s.lower().removeprefix("https://").removeprefix("http://").removeprefix("www.").rstrip("/")


def cmd_add(a, rows):
    site = norm_site(a.website or "")
    for r in rows:
        if r["name"].lower() == a.name.lower() or (site and norm_site(r["website"]) == site):
            sys.exit(f"exists: {r['name']}")
    rows.append({"name": a.name, "website": a.website or "", "email": a.email or "",
                 "phone": a.phone or "", "city": a.city or "", "status": "new", "touches": "0"})
    save(rows)
    print(f"added {a.name}")


def cmd_set(a, rows):
    if a.status not in STATUSES:
        sys.exit(f"status must be one of {STATUSES}")
    r = find(rows, a.name)
    today = date.today().isoformat()
    if a.status in ("emailed", "followed_up"):
        if r.get("email") and suppressed(r["email"]):
            sys.exit(f"refused: {r['email']} opted out")
        r["touches"] = str(int(r.get("touches") or 0) + 1)
        r["first_contact"] = r.get("first_contact") or today
        r["last_contact"] = today
    r["status"] = a.status
    for f in ("score", "email", "phone", "website"):
        if getattr(a, f, None):
            r[f] = getattr(a, f)
    if a.note:
        r["notes"] = (r.get("notes", "") + f" | {today}: {a.note}").strip(" |")
    save(rows)
    print(f"{r['name']} -> {a.status}")


def cmd_list(a, rows):
    for r in rows:
        if not a.status or r["status"] == a.status:
            print(f"{r['status']:<12} {r['score'] or '-':>3}  {r['name']}  <{r['email']}>  {r['website']}")


def cmd_due(a, rows):
    cutoff = date.today() - timedelta(days=FOLLOW_UP_AFTER_DAYS)
    for r in rows:
        if (r["status"] == "emailed" and int(r.get("touches") or 0) < MAX_TOUCHES
                and r.get("last_contact") and date.fromisoformat(r["last_contact"]) <= cutoff
                and not suppressed(r.get("email", ""))):
            print(f"{r['name']}\t{r['email']}\tlast {r['last_contact']}")


def cmd_optout(a, rows):
    ROOT.mkdir(parents=True, exist_ok=True)
    with OPTOUT.open("a") as f:
        f.write(a.email.lower() + "\n")
    for r in rows:
        if r.get("email", "").lower() == a.email.lower():
            r["status"] = "optout"
    save(rows)
    print(f"suppressed {a.email}")


def cmd_can_email(a, rows):
    if suppressed(a.email):
        sys.exit(f"no: {a.email} opted out")
    for r in rows:
        if r.get("email", "").lower() == a.email.lower() and int(r.get("touches") or 0) >= MAX_TOUCHES:
            sys.exit(f"no: {a.email} already contacted {r['touches']} times")
    print("yes")


def cmd_stats(a, rows):
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    today = date.today().isoformat()
    sent_today = sum(1 for r in rows if r.get("last_contact") == today)
    print(f"total {len(rows)} | sent today {sent_today} | " +
          " ".join(f"{k}={v}" for k, v in sorted(counts.items())))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add"); s.add_argument("name")
    for f in ("website", "email", "phone", "city"):
        s.add_argument(f"--{f}")
    s = sub.add_parser("set"); s.add_argument("name"); s.add_argument("status")
    for f in ("score", "email", "phone", "website", "note"):
        s.add_argument(f"--{f}")
    s = sub.add_parser("list"); s.add_argument("--status")
    sub.add_parser("due")
    s = sub.add_parser("optout"); s.add_argument("email")
    s = sub.add_parser("can-email"); s.add_argument("email")
    sub.add_parser("stats")
    a = p.parse_args()
    {"add": cmd_add, "set": cmd_set, "list": cmd_list, "due": cmd_due, "optout": cmd_optout,
     "can-email": cmd_can_email, "stats": cmd_stats}[a.cmd](a, load())


if __name__ == "__main__":
    main()
