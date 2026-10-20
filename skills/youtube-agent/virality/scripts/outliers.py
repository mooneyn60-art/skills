#!/usr/bin/env python3
"""Find YouTube outliers: videos beating their own channel's median views.

Free, no API key: uses yt-dlp (flat extraction, no downloads).

  outliers.py "doorbell camera raccoon" ["caught on camera funny animals" ...]
      [--n 15] [--recent 15] [--shorts] [--min-score 3] [--max-duration 180] [--json]

score = video views / median views of the channel's ~RECENT latest uploads
(videos + shorts tabs merged, the candidate itself excluded).
"""
import argparse
import json
import os
import re
import statistics
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

try:
    import yt_dlp
except ImportError:  # fall back to the local source checkout
    for p in (os.environ.get("YTDLP_SRC"), "/home/user/yt-dlp"):
        if p and os.path.isdir(p):
            sys.path.insert(0, p)
    import yt_dlp

SHORTS_SP = "EgIQCQ%3D%3D"  # YouTube search filter: type = Shorts
_YDL = None


class _Quiet:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass  # callers catch and report the exception once


def flat(url, limit=None):
    opts = {"extract_flat": "in_playlist", "quiet": True, "no_warnings": True,
            "skip_download": True, "logger": _Quiet(), "socket_timeout": 30}
    if limit:
        opts["playlistend"] = limit
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return [e for e in (info or {}).get("entries") or [] if e]


def _get(url):
    """Fetch a page through yt-dlp's networking (proxy, CA bundle, headers)."""
    global _YDL
    _YDL = _YDL or yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "logger": _Quiet()})
    return _YDL.urlopen(url).read().decode("utf-8", "replace")


def _field(html, key, kind=str):
    m = re.search(r'"videoDetails":\{.*?"%s":(".*?(?<!\\)"|\d+)' % key, html, re.S)
    if not m:
        return None
    v = json.loads(m.group(1))
    return kind(v) if v not in ("", None) else None


def short_details(video_id):
    """Shorts search results carry no channel; read it from the public Shorts page."""
    try:
        h = _get(f"https://www.youtube.com/shorts/{video_id}")
    except Exception as ex:
        print(f"  ! short {video_id}: {str(ex)[:120]}", file=sys.stderr)
        return None
    cid = _field(h, "channelId")
    if not cid:
        return None
    return {"id": video_id, "channel_id": cid, "title": _field(h, "title"),
            "channel": _field(h, "author"), "view_count": _field(h, "viewCount", int),
            "duration": _field(h, "lengthSeconds", int)}


def search(query, n, shorts, workers=4):
    if not shorts:
        return flat(f"ytsearch{n}:{query}")
    # yt-dlp's search parser skips Shorts lockups, so scrape the Shorts-filtered results page.
    h = _get("https://www.youtube.com/results?search_query="
             f"{urllib.parse.quote_plus(query)}&sp={SHORTS_SP}")
    ids = list(dict.fromkeys(re.findall(r'"reelWatchEndpoint":\{"videoId":"([\w-]{11})"', h)))[:n]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return [d for d in pool.map(short_details, ids) if d]


def channel_views(channel_id, recent):
    """Return {video_id: views} for the channel's latest uploads (videos + shorts)."""
    views = {}
    for tab in ("videos", "shorts"):
        try:
            for e in flat(f"https://www.youtube.com/channel/{channel_id}/{tab}", recent):
                if e.get("view_count") is not None:
                    views[e["id"]] = e["view_count"]
        except Exception as ex:  # tab missing, blocked, rate-limited
            if "does not have a" not in str(ex):
                print(f"  ! {channel_id}/{tab}: {str(ex)[:120]}", file=sys.stderr)
    return views


def score_rows(entries, recent, workers):
    channels = {e["channel_id"] for e in entries if e.get("channel_id")}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        cache = dict(zip(channels, pool.map(lambda c: channel_views(c, recent), channels)))
    rows = []
    for e in entries:
        views, ch = e.get("view_count"), e.get("channel_id")
        others = [v for vid, v in cache.get(ch, {}).items() if vid != e["id"]]
        if views is None or len(others) < 3:
            continue  # not enough channel history to judge
        median = statistics.median(others) or 1
        rows.append({"title": e.get("title") or "", "url": f"https://www.youtube.com/watch?v={e['id']}",
                     "channel": e.get("channel") or e.get("uploader") or ch, "views": views,
                     "channel_median": int(median), "score": round(views / median, 1),
                     "duration": e.get("duration"), "sample": len(others)})
    return sorted(rows, key=lambda r: r["score"], reverse=True)


def fmt_n(n):
    return f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:.1f}k" if n >= 1e3 else str(n)


def print_table(query, rows):
    print(f"\n## {query}  ({len(rows)} scored)")
    print(f"{'score':>7} {'views':>7} {'median':>7} {'dur':>4}  title | channel | url")
    for r in rows:
        dur = f"{int(r['duration'])}s" if r["duration"] else "?"
        print(f"{r['score']:>6}x {fmt_n(r['views']):>7} {fmt_n(r['channel_median']):>7} {dur:>4}  "
              f"{r['title'][:60].replace('|', '/')} | {r['channel'][:24]} | {r['url']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--n", type=int, default=15, help="search results per query")
    ap.add_argument("--recent", type=int, default=15, help="recent uploads per channel tab")
    ap.add_argument("--shorts", action="store_true", help="search the Shorts tab (type=Shorts filter)")
    ap.add_argument("--min-score", type=float, default=0, help="hide rows below this score")
    ap.add_argument("--max-duration", type=int, default=0, help="hide videos longer than N s")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--json", action="store_true", help="print JSON instead of a table")
    a = ap.parse_args()
    out = {}
    for q in a.queries:
        try:
            entries = search(q, a.n, a.shorts, a.workers)
        except Exception as ex:
            print(f"search failed for {q!r}: {str(ex)[:200]}", file=sys.stderr)
            continue
        rows = [r for r in score_rows(entries, a.recent, a.workers)
                if r["score"] >= a.min_score
                and not (a.max_duration and r["duration"] and r["duration"] > a.max_duration)]
        out[q] = rows
        if not a.json:
            print_table(q, rows)
    if a.json:
        print(json.dumps(out, indent=2))
    if not any(out.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
