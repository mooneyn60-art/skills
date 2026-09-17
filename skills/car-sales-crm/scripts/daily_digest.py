#!/usr/bin/env python3
"""List customers due or overdue for follow-up, soonest first.

Reads every *.md file in ../customers relative to this script (i.e.
skills/car-sales-crm/customers/), parses the YAML front matter, and prints
anyone whose next_followup date is today or earlier. No third-party deps.
"""
import re
import sys
from datetime import date
from pathlib import Path

CUSTOMERS_DIR = Path(__file__).resolve().parent.parent / "customers"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.split("#", 1)[0].strip()
    return fields


def parse_date(value: str):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def main():
    if not CUSTOMERS_DIR.exists():
        print(f"No customers directory found at {CUSTOMERS_DIR}")
        return

    today = date.today()
    due = []

    for path in sorted(CUSTOMERS_DIR.glob("*.md")):
        fields = parse_front_matter(path.read_text(encoding="utf-8"))
        status = fields.get("status", "")
        if status in ("sold", "lost") and not fields.get("next_followup"):
            continue
        followup = parse_date(fields.get("next_followup", ""))
        if followup is None or followup > today:
            continue
        due.append(
            {
                "file": path.name,
                "name": fields.get("name") or path.stem,
                "followup": followup,
                "channel": fields.get("next_followup_channel", "").strip() or "(unset)",
                "status": status or "(unset)",
                "stage": fields.get("stage", "").strip() or "(unset)",
                "overdue_days": (today - followup).days,
            }
        )

    due.sort(key=lambda c: (-c["overdue_days"], c["name"]))

    if not due:
        print("Nothing due today. Nobody's falling through the cracks.")
        return

    print(f"Follow-ups due as of {today.isoformat()}:\n")
    for c in due:
        when = "today" if c["overdue_days"] == 0 else f"{c['overdue_days']}d overdue"
        print(
            f"- {c['name']} [{c['file']}] — {when} — {c['channel']} — "
            f"status: {c['status']}, stage: {c['stage']}"
        )


if __name__ == "__main__":
    sys.exit(main())
