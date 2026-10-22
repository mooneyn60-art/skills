#!/usr/bin/env python3
"""Free view tracker (no API key, no vidIQ credits): snapshot the channel's public view counts with
yt-dlp, append them to data/views.csv, and print each video's views gained since the last snapshot.

Usage: stats.py [CHANNEL_URL]      (default: our channel)
Run it once a day (or more); velocity = views gained per hour between snapshots.
"""
import csv
import datetime
import os
import sys

sys.path.insert(0, "/home/user/yt-dlp")  # local checkout when the package isn't installed
import yt_dlp  # noqa: E402

CHANNEL = "https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg"
CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "views.csv")


def fetch(channel):
    rows = []
    with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True, "skip_download": True}) as ydl:
        for tab, kind in (("videos", "long"), ("shorts", "short")):
            try:
                info = ydl.extract_info(f"{channel}/{tab}", download=False)
            except yt_dlp.utils.DownloadError:
                continue  # a channel with no Shorts (or no videos) has no such tab
            for e in info.get("entries") or []:
                rows.append({"id": e["id"], "kind": kind, "title": e.get("title") or "",
                             "views": e.get("view_count") or 0})
    return rows


def last_snapshot():
    if not os.path.exists(CSV):
        return {}, None
    prev, ts = {}, None
    for r in csv.DictReader(open(CSV)):
        if r["ts"] != ts:
            ts, prev = r["ts"], {}
        prev[r["id"]] = int(r["views"])
    return prev, ts


def main():
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    rows = fetch(sys.argv[1] if len(sys.argv) > 1 else CHANNEL)
    prev, prev_ts = last_snapshot()
    hours = (now - datetime.datetime.fromisoformat(prev_ts)).total_seconds() / 3600 if prev_ts else None
    new = not os.path.exists(CSV)
    with open(CSV, "a", newline="") as f:
        w = csv.DictWriter(f, ["ts", "id", "kind", "views", "title"])
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({"ts": now.isoformat(), **r})
    print(f"{len(rows)} videos at {now.isoformat()}" + (f", {hours:.1f} h since last snapshot" if hours else ""))
    for r in sorted(rows, key=lambda r: r["views"] - prev.get(r["id"], 0), reverse=True):
        gained = r["views"] - prev.get(r["id"], 0) if r["id"] in prev else None
        vph = f"{gained / hours:7.1f}/h" if gained is not None and hours else "    new"
        print(f"{r['kind']:5} {r['views']:7d} views  +{gained if gained is not None else '-':>6}  {vph}  {r['title'][:60]}")


if __name__ == "__main__":
    main()
