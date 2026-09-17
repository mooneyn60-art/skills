#!/usr/bin/env python3
"""Unified agenda: scheduled appointments + follow-up reminders, by day.

Usage:
    python3 calendar_view.py          # today through the next 6 days
    python3 calendar_view.py 1        # today only
    python3 calendar_view.py 30       # today through the next 29 days

Reads calendar/appointments/*.md and customers/*.md relative to this
skill's folder. No third-party deps.
"""
import sys
from collections import defaultdict
from datetime import date, timedelta

from _common import APPOINTMENTS_DIR, CUSTOMERS_DIR, parse_date, parse_front_matter


def load_appointments():
    items = []
    if not APPOINTMENTS_DIR.exists():
        return items
    for path in sorted(APPOINTMENTS_DIR.glob("*.md")):
        f = parse_front_matter(path.read_text(encoding="utf-8"))
        d = parse_date(f.get("date", ""))
        if d is None:
            continue
        confirmed = f.get("confirmed", "").strip().lower() in ("true", "yes")
        items.append(
            {
                "date": d,
                "kind": "appointment",
                "file": path.name,
                "who": f.get("customer") or path.stem,
                "detail": f.get("type", "").strip() or "appointment",
                "time": f.get("time", "").strip(),
                "confirmed": confirmed,
            }
        )
    return items


def load_followups():
    items = []
    if not CUSTOMERS_DIR.exists():
        return items
    for path in sorted(CUSTOMERS_DIR.glob("*.md")):
        f = parse_front_matter(path.read_text(encoding="utf-8"))
        status = f.get("status", "")
        if status in ("sold", "lost") and not f.get("next_followup"):
            continue
        d = parse_date(f.get("next_followup", ""))
        if d is None:
            continue
        items.append(
            {
                "date": d,
                "kind": "followup",
                "file": path.name,
                "who": f.get("name") or path.stem,
                "detail": f.get("next_followup_channel", "").strip() or "(channel unset)",
                "time": "",
                "confirmed": True,
            }
        )
    return items


def format_item(item):
    if item["kind"] == "appointment":
        mark = "" if item["confirmed"] else " [UNCONFIRMED]"
        when = f" @ {item['time']}" if item["time"] else ""
        return f"    - [appt] {item['who']}{when} — {item['detail']}{mark} ({item['file']})"
    return f"    - [follow-up] {item['who']} — {item['detail']} ({item['file']})"


def main():
    days = 7
    if len(sys.argv) > 1:
        try:
            days = max(1, int(sys.argv[1]))
        except ValueError:
            print(f"Ignoring invalid days argument {sys.argv[1]!r}, using 7.")

    today = date.today()
    all_items = load_appointments() + load_followups()

    by_date = defaultdict(list)
    overdue = []
    for item in all_items:
        if item["date"] < today:
            overdue.append(item)
        else:
            by_date[item["date"]].append(item)

    if overdue:
        overdue.sort(key=lambda i: (i["date"], i["who"]))
        print(f"OVERDUE ({len(overdue)}):")
        for item in overdue:
            print(f"  {item['date'].isoformat()}:")
            print(format_item(item))
        print()

    end = today + timedelta(days=days - 1)
    print(f"Agenda {today.isoformat()} to {end.isoformat()}:\n")
    cursor = today
    found_any = False
    while cursor <= end:
        day_items = sorted(by_date.get(cursor, []), key=lambda i: (i["kind"], i["who"]))
        if day_items:
            found_any = True
            label = "Today" if cursor == today else cursor.strftime("%A")
            print(f"{label} ({cursor.isoformat()}):")
            for item in day_items:
                print(format_item(item))
        cursor += timedelta(days=1)

    if not found_any and not overdue:
        print("Nothing scheduled. Clean calendar.")


if __name__ == "__main__":
    sys.exit(main())
