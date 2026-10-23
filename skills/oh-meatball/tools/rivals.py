#!/usr/bin/env python3
"""Free competitor tracker (no API key, no vidIQ credits): snapshot the newest videos of the niche's
breakout channels with yt-dlp, log them to data/rivals.csv, and print each channel's outliers
(views over 3x its own median), which is where the next episode topics come from.

Usage: rivals.py [--n 20] [--json OUT]   (run daily; --json writes rows for the HQ dashboard)
"""
import argparse
import csv
import datetime
import json
import os
import statistics
import sys

sys.path.insert(0, "/home/user/yt-dlp")  # local checkout when the package isn't installed
import yt_dlp  # noqa: E402

# Channels whose videos topped research/16-myths-niche-outliers.md, plus the biggest true/false quiz channel.
RIVALS = {
    "Oddly Factual": "UC8bguWRNrfvhZBiZqmlsdYg",
    "Lying Pie": "UCk82OCa1tR2sodOsR5hqlEw",
    "What Gives?": "UC1kQHKdz40IIiV1ZFL7vPTg",
    "Myths-creature": "UCWbM5p20UDzs1VLGa9ku2Jw",
    "Mysterious-Fact": "UCib8z9RWBK1xucFXG_q-Siw",
    "Quiz Madness": "UCEGC6iQjjJNCLkvLdi12BIg",
    "WildNature Lab": "UCWbPAXwejAeCr8eGd1LVOOw",
}
CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "rivals.csv")


def fetch(cid, n):
    rows = []
    with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True, "no_warnings": True, "playlistend": n}) as ydl:
        for tab, kind in (("videos", "long"), ("shorts", "short")):
            try:
                info = ydl.extract_info(f"https://www.youtube.com/channel/{cid}/{tab}", download=False)
            except yt_dlp.utils.DownloadError:
                continue
            for e in (info.get("entries") or [])[:n]:
                rows.append({"id": e["id"], "kind": kind, "title": e.get("title") or "", "views": e.get("view_count") or 0})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--json")
    a = ap.parse_args()
    ts = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    out, new = [], not os.path.exists(CSV)
    with open(CSV, "a", newline="") as f:
        w = csv.DictWriter(f, ["ts", "channel", "id", "kind", "views", "title"])
        if new:
            w.writeheader()
        for name, cid in RIVALS.items():
            rows = fetch(cid, a.n)
            for kind in ("long", "short"):
                vids = [r for r in rows if r["kind"] == kind and r["views"]]
                if not vids:
                    continue
                med = statistics.median(r["views"] for r in vids)
                print(f"\n{name} [{kind}] median {med:,.0f} over newest {len(vids)}")
                for r in sorted(vids, key=lambda r: r["views"], reverse=True):
                    x = r["views"] / med if med else 0
                    w.writerow({"ts": ts, "channel": name, **r})
                    out.append({"ts": ts, "channel": name, **r, "x_median": round(x, 1)})
                    if x >= 3:
                        print(f"  {x:5.1f}x {r['views']:>10,}  {r['title'][:80]}")
    if a.json:
        json.dump(out, open(a.json, "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
