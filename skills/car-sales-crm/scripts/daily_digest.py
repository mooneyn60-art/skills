#!/usr/bin/env python3
"""List customers due or overdue for follow-up, soonest first.

Reads every *.md file in ../customers relative to this script (i.e.
skills/car-sales-crm/customers/), parses the YAML front matter, and prints
anyone whose next_followup date is today or earlier. No third-party deps.
"""
import sys

from _common import CUSTOMERS_DIR, parse_date, parse_front_matter
from datetime import date


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
