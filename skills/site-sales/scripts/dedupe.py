#!/usr/bin/env python3
"""Validate and de-duplicate data/leads.csv in place (or to --out).

A lead is a duplicate when it shares a normalised email, Instagram handle,
phone number, or business name + town with an earlier row. The earliest row
wins, but empty fields in it are filled from the later duplicate. Rows with an
unknown status or no public contact route are reported, not dropped.

Usage:
    python dedupe.py                       # data/leads.csv, rewrite in place
    python dedupe.py leads.csv --out clean.csv --dry-run
"""

import argparse
import csv
import re
import sys
from pathlib import Path

COLUMNS = ["business", "category", "town", "state", "public_email", "phone", "instagram",
           "website_status", "source_url", "found_at", "status"]
STATUSES = {"new", "researched", "preview_built", "approved_to_contact", "contacted",
            "followed_up", "replied", "won", "lost", "opted_out", "skip"}
DEFAULT = Path(__file__).resolve().parent.parent / "data" / "leads.csv"


def norm_name(s: str) -> str:
    words = re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("&", " and ")).split()
    return " ".join(w for w in words if w not in {"the", "llc", "inc", "co"})


def keys(row: dict) -> list[str]:
    out = []
    if row["public_email"].strip():
        out.append("e:" + row["public_email"].strip().lower())
    if row["instagram"].strip():
        out.append("i:" + row["instagram"].strip().lstrip("@").lower())
    digits = re.sub(r"\D", "", row["phone"])[-10:]
    if len(digits) == 10:
        out.append("p:" + digits)
    town = re.sub(r"\s*\(.*\)", "", row["town"]).strip().lower()
    out.append(f"n:{norm_name(row['business'])}|{town}|{row['state'].strip().lower()}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", nargs="?", type=Path, default=DEFAULT)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with args.csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            print(f"error: missing columns {missing}", file=sys.stderr)
            return 1
        rows = [{c: (r.get(c) or "").strip() for c in COLUMNS} for r in reader]

    kept, seen, dropped = [], {}, 0
    for i, row in enumerate(rows, start=2):
        hit = next((seen[k] for k in keys(row) if k in seen), None)
        if hit is not None:
            dropped += 1
            for c in COLUMNS:
                if not hit[c] and row[c]:
                    hit[c] = row[c]
            print(f"dup: line {i} '{row['business']}' merged into '{hit['business']}'")
            continue
        for k in keys(row):
            seen[k] = row
        kept.append(row)

    for row in kept:
        if row["status"] not in STATUSES:
            print(f"warn: '{row['business']}' has unknown status '{row['status']}'")
        if not (row["public_email"] or row["instagram"]):
            print(f"warn: '{row['business']}' has no public email or Instagram")
        if not row["source_url"].startswith("http"):
            print(f"warn: '{row['business']}' has no source_url")

    print(f"{len(rows)} rows -> {len(kept)} kept, {dropped} duplicate(s)")
    if args.dry_run:
        return 0
    out = args.out or args.csv
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(kept)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
