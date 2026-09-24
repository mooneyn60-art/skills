#!/usr/bin/env python3
"""Track prospects for the local-booking-sites workflow in a CSV file.

Usage:
    python leads.py add "Maple & Fade" --instagram @mapleandfade --city Riverton
    python leads.py list [--status built]
    python leads.py status "Maple & Fade" sent --note "DM'd Tue"
    python leads.py dm "Maple & Fade" --link https://example.com/site.html

`dm` only drafts the message for you to review and send by hand. Nothing is
sent automatically: personalised one-to-one outreach works better, and bulk
automated DMs break Instagram's rules and get accounts restricted.
"""

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

FIELDS = ["name", "instagram", "city", "category", "status", "price", "updated", "notes"]
STATUSES = ["new", "built", "sent", "replied", "won", "lost", "skip"]


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def find(rows: list[dict], name: str) -> dict:
    matches = [r for r in rows if r["name"].lower() == name.lower()]
    if not matches:
        sys.exit(f"error: no lead named {name!r}")
    return matches[0]


def draft_dm(lead: dict, link: str, sender: str) -> str:
    first_line = f"Hi {lead['name']} team!"
    return "\n".join([
        first_line,
        "",
        "I noticed your bio says \"DM to book\", so every appointment goes through "
        "your inbox. I put together a free sample website for you where clients "
        "can pick a service, day and time themselves:",
        link,
        "",
        "It uses your own services, prices and reviews. If you like it, I can set it "
        "up on your own domain and connect it to your calendar. If not, no worries, "
        "it's yours to keep either way.",
        "",
        f"— {sender}" if sender else "",
    ]).rstrip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", type=Path, default=Path("leads.csv"), help="CSV path (default leads.csv)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add a lead")
    a.add_argument("name")
    a.add_argument("--instagram", default="")
    a.add_argument("--city", default="")
    a.add_argument("--category", default="")
    a.add_argument("--notes", default="")

    ls = sub.add_parser("list", help="list leads")
    ls.add_argument("--status", choices=STATUSES)

    st = sub.add_parser("status", help="update a lead's status")
    st.add_argument("name")
    st.add_argument("status", choices=STATUSES)
    st.add_argument("--price", default=None)
    st.add_argument("--note", default=None)

    dm = sub.add_parser("dm", help="draft an outreach message to send by hand")
    dm.add_argument("name")
    dm.add_argument("--link", required=True, help="where the sample site is hosted")
    dm.add_argument("--sender", default="", help="your name for the sign-off")

    args = ap.parse_args()
    rows = load(args.file)
    today = date.today().isoformat()

    if args.cmd == "add":
        if any(r["name"].lower() == args.name.lower() for r in rows):
            sys.exit(f"error: {args.name!r} is already in {args.file}")
        rows.append({"name": args.name, "instagram": args.instagram, "city": args.city,
                     "category": args.category, "status": "new", "updated": today,
                     "notes": args.notes})
        save(args.file, rows)
        print(f"added {args.name}")
    elif args.cmd == "list":
        shown = [r for r in rows if not args.status or r["status"] == args.status]
        for r in shown:
            print(f"{r['status']:<8} {r['name']:<32} {r['instagram']:<24} {r['city']:<16} {r['price']}")
        print(f"{len(shown)} lead(s)")
    elif args.cmd == "status":
        lead = find(rows, args.name)
        lead["status"] = args.status
        lead["updated"] = today
        if args.price is not None:
            lead["price"] = args.price
        if args.note:
            lead["notes"] = (lead.get("notes", "") + f" | {today}: {args.note}").strip(" |")
        save(args.file, rows)
        print(f"{lead['name']} -> {args.status}")
    elif args.cmd == "dm":
        print(draft_dm(find(rows, args.name), args.link, args.sender))
    return 0


if __name__ == "__main__":
    sys.exit(main())
