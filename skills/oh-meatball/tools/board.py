#!/usr/bin/env python3
"""Build data/board/board.json: the numbers behind Nolan's one-screen scoreboard page.

Run from skills/oh-meatball:   python3 tools/board.py [--offline]

Reads
  data/posted.csv            what is scheduled and posted (times are ET)
  data/tiktok-stats.csv      public TikTok counts (postkit.py ttpage --csv); newest row per video
  data/board/notes.json      hand-kept: long-video hours, read dates, the open ask
  YouTube public listings    yt-dlp flat listings of the channel's Shorts and videos (views, subscribers)
  TikTok public profile      follower count

Writes data/board/board.json with five lists: kpis, recent, queue, dates, asks.
Every number the page shows is a cell in one of them, so all arithmetic is here.
--offline skips the network and reuses /dev/shm copies of the listings if they exist.
"""
import csv, datetime, json, os, re, statistics, subprocess, sys, urllib.request

OM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(OM, "data", "board")
CHANNEL = "https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg"
TT_PROFILE = "https://www.tiktok.com/@meatballmyths"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
ET = datetime.timedelta(hours=-5)          # Eastern Standard Time (in force until March 2027)
MIN_AGE_H = 20                              # a post counts toward a median once it is this old
WINDOW = 12                                 # posts in a median
DAYS = "Mon Tue Wed Thu Fri Sat Sun".split()


def now_et():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + ET


def day_label(t):
    return f"{DAYS[t.weekday()]} {t.month}/{t.day}"


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()[:45]


def listing(tab, n, cache, offline):
    if not offline:
        try:
            out = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "--playlist-end", str(n), f"{CHANNEL}/{tab}"],
                                 capture_output=True, text=True, timeout=180).stdout
            if out.strip().startswith("{"):
                open(cache, "w", encoding="utf-8").write(out)
        except Exception as e:                                   # keep the last copy
            print(f"warn: yt-dlp {tab}: {e}", file=sys.stderr)
    try:
        return json.load(open(cache, encoding="utf-8"))
    except Exception:
        return {}


def tiktok_followers(offline):
    if offline:
        return None
    try:
        req = urllib.request.Request(TT_PROFILE, headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
        m = re.search(r'"followerCount":(\d+)', html)
        return int(m.group(1)) if m else None
    except Exception as e:
        print(f"warn: TikTok profile: {e}", file=sys.stderr)
        return None


def median_pair(rows):
    """(median of the newest WINDOW posts old enough, median of the WINDOW before them)."""
    old = [r["views"] for r in rows if r["age_hours"] >= MIN_AGE_H]
    a, b = old[:WINDOW], old[WINDOW:2 * WINDOW]
    return (round(statistics.median(a)) if a else None, round(statistics.median(b)) if len(b) >= 6 else None, len(a))


def main():
    offline = "--offline" in sys.argv
    now = now_et()
    posted = list(csv.DictReader(open(os.path.join(OM, "data", "posted.csv"), encoding="utf-8")))
    for r in posted:
        r["t"] = datetime.datetime.strptime(r["date"][:16], "%Y-%m-%d %H:%M")
        r["long"] = r["network"] == "youtube" and ("longform" in r["episode"] or "longform" in r["file"])
    notes = json.load(open(os.path.join(BOARD, "notes.json"), encoding="utf-8"))

    # ---- YouTube: public views, matched to the log by title
    yt_log = {}
    for r in posted:
        if r["network"] == "youtube" and r["t"] <= now:
            yt_log[norm(r["title"])] = r                      # a later row for the same title wins
    recent, subs, unmatched = [], None, 0
    for kind, tab, n, cache in (("Short", "shorts", 60, "/dev/shm/board-yt-shorts.json"),
                                ("Long video", "videos", 12, "/dev/shm/board-yt-videos.json")):
        d = listing(tab, n, cache, offline)
        subs = d.get("channel_follower_count") or subs
        for e in d.get("entries") or []:
            if not e or not e.get("id"):                      # yt-dlp leaves a hole for an entry it could not read
                continue
            p = yt_log.get(norm(e.get("title")))
            if not p:
                unmatched += 1
                continue
            url = ("https://youtube.com/shorts/" if kind == "Short" else "https://youtube.com/watch?v=") + e["id"]
            recent.append({"network": "YouTube", "kind": kind, "posted_et": p["date"][:16], "title": e.get("title") or "",
                           "views": int(e.get("view_count") or 0),
                           "age_hours": round((now - p["t"]).total_seconds() / 3600, 1), "url": url})

    # ---- TikTok: newest public count per video; the post time is inside the video id
    tt_latest = {}
    try:
        for r in csv.DictReader(open(os.path.join(OM, "data", "tiktok-stats.csv"), encoding="utf-8")):
            if r.get("plays", "").isdigit():
                tt_latest[r["video_id"]] = r                  # rows are appended in time order
    except FileNotFoundError:
        pass
    tt_log = [r for r in posted if r["network"] == "tiktok"]
    for vid, r in tt_latest.items():
        t = datetime.datetime.fromtimestamp(int(vid) >> 32, datetime.timezone.utc).replace(tzinfo=None) + ET
        near = min(tt_log, key=lambda p: abs((p["t"] - t).total_seconds()), default=None)
        title = near["title"] if near and abs((near["t"] - t).total_seconds()) <= 25 * 60 else "TikTok post"
        recent.append({"network": "TikTok", "kind": "TikTok", "posted_et": t.strftime("%Y-%m-%d %H:%M"),
                       "title": title.replace(";", ","), "views": int(r["plays"]),
                       "age_hours": round((now - t).total_seconds() / 3600, 1), "url": r["url"],
                       "likes": int(r.get("likes") or 0), "counted": r["date_utc"][:10]})
    recent.sort(key=lambda r: r["posted_et"], reverse=True)
    for r in recent:
        t = datetime.datetime.strptime(r["posted_et"], "%Y-%m-%d %H:%M")
        r["day"], r["time"] = day_label(t), t.strftime("%H:%M")
        r["fresh"] = r["age_hours"] < MIN_AGE_H            # too new to count in a median

    shorts = [r for r in recent if r["kind"] == "Short"]
    longs = [r for r in recent if r["kind"] == "Long video"]
    tts = [r for r in recent if r["network"] == "TikTok"]
    ys, ys_prev, ys_n = median_pair(shorts)
    ts, ts_prev, ts_n = median_pair(tts)
    followers = tiktok_followers(offline) or notes["tt_followers"]["value"]
    lf = notes["longform_hours"]
    today = now.strftime("%Y-%m-%d")
    win = f"newest {WINDOW} posts at least {MIN_AGE_H} hours old"

    def pct(v, target):
        return round(100 * v / target, 1) if v is not None and target else None

    kpis = [
        {"key": "yt_shorts_median", "label": "YouTube Shorts", "unit": "median views", "value": ys, "prev": ys_prev,
         "target": None, "pct": None, "window": win, "as_of": today, "source": "YouTube public counts"},
        {"key": "tt_median", "label": "TikTok", "unit": "median plays", "value": ts, "prev": ts_prev,
         "target": None, "pct": None, "window": win, "as_of": today, "source": "TikTok public counts"},
        {"key": "lf_hours", "label": "Long-video hours", "unit": "hours watched", "value": lf["value"], "prev": None,
         "target": 4000, "pct": pct(lf["value"], 4000), "window": lf["window"], "as_of": lf["as_of"], "source": lf["source"]},
        {"key": "tt_followers", "label": "TikTok followers", "unit": "followers", "value": followers, "prev": None,
         "target": 10000, "pct": pct(followers, 10000), "window": "now", "as_of": today, "source": "TikTok public profile"},
        {"key": "yt_subs", "label": "YouTube subscribers", "unit": "subscribers", "value": subs or notes["yt_subs"]["value"],
         "prev": None, "target": 1000, "pct": pct(subs or notes["yt_subs"]["value"], 1000), "window": "now",
         "as_of": today, "source": "YouTube public count (rounded by YouTube)"},
    ]

    # ---- the next 7 days from the log
    end = (now + datetime.timedelta(days=7)).replace(hour=23, minute=59)      # whole days, so the last one is not cut short
    queue = []
    for r in sorted((r for r in posted if now < r["t"] <= end), key=lambda r: r["t"]):
        kind = "TikTok" if r["network"] == "tiktok" else ("Long video" if r["long"] else "Short")
        queue.append({"when_et": r["date"][:16], "day": day_label(r["t"]), "time": r["t"].strftime("%H:%M"),
                      "network": "TikTok" if r["network"] == "tiktok" else "YouTube", "kind": kind,
                      "title": r["title"].replace(";", ",")})

    dates = [d for d in notes["dates"] if d["date"] >= today]
    for d in dates:
        t = datetime.datetime.strptime(d["date"], "%Y-%m-%d")
        d["day"] = day_label(t)
    board = {"generated_et": now.strftime("%Y-%m-%d %H:%M"),
             "kpis": kpis,
             "recent": shorts[:8] + longs[:3] + tts[:8],
             "queue": queue, "dates": dates, "asks": notes["asks"]}
    out = os.path.join(BOARD, "board.json")
    json.dump(board, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {out}: {len(shorts)} Shorts, {len(longs)} long, {len(tts)} TikToks matched "
          f"({unmatched} YouTube titles not in the log); Shorts median {ys} (n={ys_n}, before {ys_prev}), "
          f"TikTok median {ts} (n={ts_n}, before {ts_prev}); followers {followers}; subscribers {subs}; "
          f"{len(queue)} posts in the next 7 days")


if __name__ == "__main__":
    main()
