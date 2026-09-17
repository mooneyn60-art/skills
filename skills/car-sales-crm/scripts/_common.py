"""Shared helpers for the car-sales-crm scripts. No third-party deps."""
import re
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CUSTOMERS_DIR = SKILL_DIR / "customers"
APPOINTMENTS_DIR = SKILL_DIR / "calendar" / "appointments"

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
        value = value.split("#", 1)[0].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def parse_date(value: str):
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None
