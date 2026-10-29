#!/usr/bin/env python3
"""Channel Brain issue scanner: find problems BEFORE anyone has to point them out.

Run at the start of every routine run, before any production work:
    python3 scan.py /path/to/skills/oh-meatball            (prints a ranked issue list)
    python3 scan.py /path/to/skills/oh-meatball --json out.json
Exit code 2 if any CRITICAL issue, 1 if any WARN, 0 if clean.

Every issue names: severity, the desk that owns it, what is wrong (with the numbers), and the fix.
Rule for the run that reads it: fix every CRITICAL and WARN in your own lane in this run; hand the rest to the
owning desk on the square; only Studio-only or money/policy items go to Nolan.

Checks (each one is cheap, local, and uses only files already in the repo):
  1. views.csv freshness, Shorts dying in the first 24 h, channel momentum falling
  2. posted.csv: queue gaps vs CADENCE for the next 48 h, the same file or title posted twice
  3. experiments.csv: duplicate ids, tests open too long without a result, missing baseline or metric,
     two tests running on the same format at once
  4. metrics.csv: zero subscribers gained in the last 7 days
  5. doc drift: routine docs that mention a retired format, an old branch, or contradict CADENCE
  6. expert playbooks over the 300-line cap
  7. focus (10/29 audit): share of the next 7 days of YouTube posts that are the shows, queue longer than 7 days,
     commits that never reach the queue, TikTok rewards and retention tracking gone stale
"""
import csv
import datetime as dt
import json
import os
import re
import statistics as st
import sys

# --- keep this in sync with OPERATIONS.md (the scanner flags docs that disagree with it) ---------------
CADENCE = {  # network: list of ET posting times per day
    "youtube-short": ["10:00", "13:00", "16:00"],
    "tiktok": ["10:00", "12:00", "18:00", "20:00"],
}
CURRENT_BRANCH = "claude/youtube-monetization-strategy-m9vz6i"
RETIRED = {  # phrase found in a routine doc -> why it is stale
    r"Oh Meatball Pt|story part|STORY PART|season1\.md": "the Oh Meatball story format was retired on 10/22",
    r"TRUE or FALSE quiz|quiz card": "the quiz format was retired for new videos on 10/24",
    r"Never mention cars": "a leftover rule from another project",
}
STALE_SNAPSHOT_H = 26
EXPERIMENT_MAX_DAYS = 10
PLAYBOOK_MAX_LINES = 300

issues = []


def add(sev, owner, what, fix):
    issues.append({"severity": sev, "owner": owner, "what": what, "fix": fix})


def rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def parse_ts(s):
    s = s.strip().replace("Z", "+00:00")
    for fmt in (None, "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            t = dt.datetime.fromisoformat(s) if fmt is None else dt.datetime.strptime(s, fmt)
            return t if t.tzinfo else t.replace(tzinfo=dt.timezone(dt.timedelta(hours=-4)))  # naive = ET
        except ValueError:
            continue
    return None


def check_views(root, now):
    vs = rows(os.path.join(root, "data", "views.csv"))
    if not vs:
        add("WARN", "intel", "data/views.csv is missing or empty, so nobody can see which videos work.",
            "Run tools/stats.py at the start of every run.")
        return
    snaps = sorted({r["ts"] for r in vs})
    last = parse_ts(snaps[-1])
    age = (now - last).total_seconds() / 3600
    if age > STALE_SNAPSHOT_H:
        add("CRITICAL", "intel", f"The last view snapshot is {age:.0f} h old ({snaps[-1]}). Every decision since then is blind.",
            "Run tools/stats.py now, then re-run this scan.")
    by = {}
    for r in vs:
        by.setdefault(r["id"], []).append((parse_ts(r["ts"]), int(r["views"] or 0), r["kind"], r["title"]))
    # Shorts that are at least 24 h old: compare views at their latest snapshot with the median
    shorts = []
    for vid, pts in by.items():
        pts.sort()
        if pts[-1][2] != "short":
            continue
        first_seen = pts[0][0]
        if (last - first_seen).total_seconds() / 3600 >= 24:
            shorts.append((pts[-1][1], vid, pts[-1][3]))
    if len(shorts) >= 6:
        med = st.median(v for v, _, _ in shorts)
        weak = [s for s in shorts if s[0] < 0.4 * med]
        for v, vid, title in sorted(weak)[:3]:
            add("INFO", "intel", f"Short {vid} '{title[:50]}' has {v} views, under 40% of the median Short ({med:.0f}).",
                "Note what is different about it (length, first frame, topic) in the intel playbook; do not re-use that pattern.")
    # momentum: total views gained in the last 24 h vs the 24 h before
    def total_at(t):
        best = None
        for s in snaps:
            ts = parse_ts(s)
            if ts <= t:
                best = s
        return sum(int(r["views"] or 0) for r in vs if r["ts"] == best) if best else None
    a, b, c = total_at(last), total_at(last - dt.timedelta(hours=24)), total_at(last - dt.timedelta(hours=48))
    if None not in (a, b, c) and (b - c) > 50:
        g1, g0 = a - b, b - c
        if g1 < 0.7 * g0:
            add("WARN", "mayor", f"Channel momentum fell: {g1} views in the last 24 h vs {g0} the day before ({(g1 / g0 - 1):+.0%}).",
                "Find the cause before changing anything: a missed post, a weaker topic, or a dead first frame. Post the finding as a decision.")


def check_queue(root, now):
    ps = rows(os.path.join(root, "data", "posted.csv"))
    if not ps:
        add("WARN", "postmaster", "data/posted.csv is missing or empty; the queue can't be checked.", "Log every scheduled post there.")
        return
    seen_files, seen_titles = {}, {}
    for r in ps:
        key = (r.get("episode", ""), r.get("file", ""), r.get("network", ""))
        if key in seen_files and r.get("file"):
            add("WARN", "postmaster", f"The same file {key[1]} from {key[0]} is queued twice on {key[2]} ({seen_files[key]} and {r['date']}).",
                "Replace one with an unused clip; reposting the same video looks reused to the platform.")
        seen_files[key] = r["date"]
        tkey = (r.get("network", ""), r.get("title", "").strip().lower())
        if tkey in seen_titles and tkey[1]:
            add("INFO", "packager", f"Title used twice on {tkey[0]}: '{r['title'][:50]}'.", "Give each post its own searched-question title.")
        seen_titles[tkey] = r["date"]
    et = dt.timezone(dt.timedelta(hours=-4))
    now_et = now.astimezone(et)
    have = {(r["network"], r["date"].strip()[:16]) for r in ps}
    net_alias = {"youtube-short": ("youtube-short", "yt-short", "youtube"), "tiktok": ("tiktok",)}
    for net, times in CADENCE.items():
        missing = []
        for d in range(0, 3):
            day = (now_et + dt.timedelta(days=d)).date()
            for t in times:
                slot = dt.datetime.combine(day, dt.time.fromisoformat(t), et)
                if not (now_et < slot <= now_et + dt.timedelta(hours=48)):
                    continue
                stamp = slot.strftime("%Y-%m-%d %H:%M")
                if not any((n, stamp) in have for n in net_alias[net]):
                    missing.append(stamp)
        if missing:
            sev = "CRITICAL" if any(parse_ts(m) - now_et < dt.timedelta(hours=12) for m in missing) else "WARN"
            add(sev, "postmaster", f"{len(missing)} {net} slot(s) in the next 48 h have nothing in posted.csv: {', '.join(missing[:6])}.",
                "Fill them from finished renders now (or log them if they are already in Metricool but not in posted.csv).")


def check_experiments(root, now):
    ex = rows(os.path.join(root, "data", "experiments.csv"))
    if not ex:
        add("WARN", "intel", "No experiments logged. Changes without a test teach nothing.", "Log every change in data/experiments.csv.")
        return
    ids, running = {}, {}
    for r in ex:
        rid = (r.get("id") or "").strip()
        if not re.fullmatch(r"E\d+", rid):
            add("WARN", "intel", f"Experiment row without a proper id (got '{rid[:20]}'): '{(r.get('hypothesis') or r.get('start') or '')[:60]}'.",
                "Give it the next free E-number and put each value in its column (id,start,hypothesis,change,metric,baseline,result,status).")
            continue
        if rid in ids:
            add("WARN", "intel", f"Experiment id {rid} is used twice ('{ids[rid][:40]}' and '{(r.get('hypothesis') or '')[:40]}').",
                "Renumber the newer one; results can't be traced when ids repeat.")
        ids[rid] = r.get("hypothesis") or ""
        status = (r.get("status") or "").strip().lower()
        start = parse_ts(r.get("start") or "")
        if status in ("open", "running") and start:
            days = (now - start).days
            if days > EXPERIMENT_MAX_DAYS and not (r.get("result") or "").strip():
                add("WARN", "intel", f"{rid} has run {days} days with no result: '{ids[rid][:60]}'.",
                    "Score it with tools/abtest.py today: write the result, then close it or extend it with a reason.")
            if not (r.get("baseline") or "").strip() or not (r.get("metric") or "").strip():
                add("WARN", "intel", f"{rid} has no baseline or no metric, so it can never be scored.", "Fill both before the next video in the test goes out.")
            fmt = "tiktok" if "tiktok" in (r.get("change", "") + r.get("hypothesis", "")).lower() else (
                "long" if re.search(r"long-?form|episode", r.get("change", "") + r.get("hypothesis", ""), re.I) else "short")
            running.setdefault(fmt, []).append(rid)
    # confounding: several changes that went live within the same 7 days can't be told apart
    live = []
    for r in ex:
        st_ = (r.get("status") or "").lower()
        t0 = parse_ts(r.get("start") or "")
        if t0 and not any(w in st_ for w in ("closed", "paused", "superseded", "replaced")) and (now - t0).days <= 21:
            live.append((t0, (r.get("id") or "?").strip(), (r.get("hypothesis") or "")))
    live.sort()
    for i, (t0, rid, _) in enumerate(live):
        window = [x for x in live if 0 <= (x[0] - t0).days <= 7]
        if len(window) >= 3:
            add("WARN", "mayor", f"{len(window)} experiments went live within 7 days of {t0:%m/%d} ({', '.join(x[1] for x in window)}). Their effects overlap, so none can be credited.",
                "Pick the one that matters most for the bottleneck metric; pause or stagger the rest by a week, or state in each row which other test it is read alongside and how.")
            break
    paid = [x[1] for x in live if re.search(r"promot|paid|\bads?\b|boost", x[2], re.I)]
    if paid:
        add("WARN", "intel", f"Paid promotion is live ({', '.join(paid)}) while organic tests are scored on views/subs. Paid followers and views contaminate those numbers.",
            "Score organic tests on organic traffic only (exclude promoted posts and their follower spike), or pause the paid test until the organic ones are read.")
    for fmt, rs in running.items():
        if len(rs) > 1:
            add("WARN", "mayor", f"{len(rs)} experiments are running on {fmt} videos at once ({', '.join(rs)}). Their effects mix and none can be read.",
                "Keep one, pause the rest (one change per format per week).")


SERIES = r"Living In Your House|Would Meatball Survive|Spider Venomous|Meatball vs Spiders"  # the shows (AUDIT_2026-10-29)
QUEUE_MAX_DAYS = 7
SHIP_WORDS = r"posted\.csv|queue|schedul|" + SERIES


def check_focus(root, now):
    """The loop audit (10/29): work that never reaches viewers, and a queue too long to learn from."""
    ps = rows(os.path.join(root, "data", "posted.csv"))
    week = [r for r in ps if r.get("network") == "youtube" and parse_ts(r.get("date", ""))
            and now < parse_ts(r["date"]) <= now + dt.timedelta(days=QUEUE_MAX_DAYS)]
    if week:
        series = sum(bool(re.search(SERIES, r.get("title", ""))) for r in week)
        share = series / len(week)
        if share < 0.8:
            add("CRITICAL", "postmaster", f"Only {series} of {len(week)} YouTube posts in the next {QUEUE_MAX_DAYS} days ({share:.0%}) are the shows; the rest are one-off facts that bring no one back (2.5% returning).",
                "Move one-off facts off YouTube (held.csv or TikTok) and fill with finished show episodes, newest first.")
    far = [r for r in ps if parse_ts(r.get("date", "")) and parse_ts(r["date"]) > now + dt.timedelta(days=QUEUE_MAX_DAYS)]
    if far:
        last = max(parse_ts(r["date"]) for r in far)
        add("WARN", "postmaster", f"{len(far)} posts are queued more than {QUEUE_MAX_DAYS} days out (to {last:%m/%d}). Anything learned this week reaches viewers weeks late.",
            "Unschedule them into held.csv; keep the queue at 7 days so new rules reach the screen next week.")
    # busywork: commits in the last 48 h that never touch the queue or a show
    try:
        import subprocess
        out = subprocess.run(["git", "-C", root, "log", "--since=48 hours ago", "--format=%s", "--", "."],
                             capture_output=True, text=True, timeout=20).stdout.splitlines()
    except Exception:
        out = []
    if len(out) >= 10:
        ship = sum(bool(re.search(SHIP_WORDS, s, re.I)) for s in out)
        if ship / len(out) < 0.5:
            add("WARN", "mayor", f"Only {ship} of {len(out)} commits in the last 48 h touched the queue or a show. The rest (re-renders, research, docs) never reach a viewer this week.",
                "Before any task, answer: which post in the next 7 days, or which scorecard number, does this change? No answer = don't do it.")
    for f, owner, what, days in (("tiktok-rewards.csv", "business", "TikTok Creator Rewards (the account that already pays)", 8),
                                 ("retention.csv", "intel", "Shorts retention curves (where viewers leave)", 7)):
        rs = rows(os.path.join(root, "data", f))
        stamps = [parse_ts(next(iter(r.values())) or "") for r in rs]
        stamps = [s for s in stamps if s]
        if not stamps or (now - max(stamps)).days > days:
            add("WARN", owner, f"data/{f} is {'empty' if not stamps else f'stale ({(now - max(stamps)).days} days)'}: {what} isn't being tracked.",
                f"Record it at least every {days} days; it is how you learn what actually works.")


def check_predictions(root, now):
    p = os.path.join(root, "data", "predictions.jsonl")
    if not os.path.exists(p):
        add("INFO", "mayor", "No data/predictions.jsonl yet, so nobody can check whether the town's judgement is any good.",
            "Every decision and experiment gets a probability it works, logged with tools/predict.py add.")
        return
    for line in open(p):
        if not line.strip():
            continue
        r = json.loads(line)
        due = parse_ts(r.get("settles", ""))
        if r.get("hit") is None and due and due < now - dt.timedelta(days=1):
            add("WARN", "intel", f"Prediction {r.get('id')} ('{r.get('what', '')[:50]}') was due {r['settles']} and is not settled.",
                f"Settle it today: tools/predict.py settle {r.get('id')} 1|0 \"what happened\".")


def check_subs(root, now):
    ms = rows(os.path.join(root, "data", "metrics.csv"))
    recent = [r for r in ms if parse_ts(r.get("date", "")) and (now - parse_ts(r["date"])).days <= 7]
    if recent:
        tracked = [r for r in recent if (r.get("subs_gained") or "").strip().lstrip("-").isdigit()]
        if not tracked:
            add("WARN", "business", "metrics.csv has no subs_gained values for the last 7 days, so subscriber growth is invisible.",
                "Record subscribers gained per video (vidIQ/Studio) every evening.")
            return
        subs = sum(int(r["subs_gained"]) for r in tracked)
        views = sum(int(r.get("views") or 0) for r in recent if (r.get("views") or "").strip().isdigit())
        if subs == 0 and views > 500:
            add("CRITICAL", "showrunner", f"0 subscribers from {views} views logged in the last 7 days. Nothing is giving viewers a reason to subscribe.",
                "Ship the recurring numbered series and a spoken subscribe reason in the last 3 s of every Short; log it as one experiment.")


def check_docs(root):
    for folder in ("routines", "."):
        d = os.path.join(root, folder)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".md"):
                continue
            text = open(os.path.join(d, name), encoding="utf-8", errors="ignore").read()
            rel = os.path.normpath(os.path.join(folder, name))
            for pat, why in RETIRED.items():
                m = re.search(pat, text)
                if m:
                    add("WARN", "mayor", f"{rel} still says '{m.group(0)}': {why}. A run that follows it does the wrong work.",
                        f"Rewrite or delete the stale part of {rel}.")
            for b in set(re.findall(r"claude/[a-z0-9-]+", text)):
                if b != CURRENT_BRANCH:
                    add("WARN", "mayor", f"{rel} points at branch {b}, not {CURRENT_BRANCH}.", f"Fix the branch name in {rel}.")
            m = re.search(r"(\d+|one|two|three|four|five)\s+TikToks?\s+a day", text, re.I)
            if m:
                words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
                n = int(m.group(1)) if m.group(1).isdigit() else words[m.group(1).lower()]
                if n != len(CADENCE["tiktok"]):
                    add("INFO", "mayor", f"{rel} says {n} TikToks a day; CADENCE says {len(CADENCE['tiktok'])}.",
                        "Make OPERATIONS.md, the routine prompts and CADENCE in scan.py agree.")


def check_playbooks(root):
    d = os.path.join(root, "research", "experts")
    if os.path.isdir(d):
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if name.endswith(".md"):
                n = sum(1 for _ in open(p, encoding="utf-8", errors="ignore"))
                if n > PLAYBOOK_MAX_LINES:
                    add("INFO", name[:-3], f"research/experts/{name} is {n} lines (cap {PLAYBOOK_MAX_LINES}).",
                        "Fold proven lessons into its Rules section and delete the rest.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(64)
    root = sys.argv[1]
    now = dt.datetime.now(dt.timezone.utc)
    for check in (lambda: check_views(root, now), lambda: check_queue(root, now), lambda: check_focus(root, now), lambda: check_experiments(root, now),
                  lambda: check_subs(root, now), lambda: check_predictions(root, now), lambda: check_docs(root), lambda: check_playbooks(root)):
        try:
            check()
        except Exception as e:  # a broken check is itself an issue, never a silent pass
            add("WARN", "studio", f"A scanner check crashed: {type(e).__name__}: {e}", "Fix the data file or the check.")
    order = {"CRITICAL": 0, "WARN": 1, "INFO": 2}
    issues.sort(key=lambda i: order[i["severity"]])
    if "--json" in sys.argv:
        json.dump({"ts": now.isoformat(), "issues": issues}, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    counts = {k: sum(i["severity"] == k for i in issues) for k in order}
    print(f"Channel scan {now:%Y-%m-%d %H:%M} UTC: {counts['CRITICAL']} critical, {counts['WARN']} warn, {counts['INFO']} info")
    for i in issues:
        print(f"[{i['severity']}] ({i['owner']}) {i['what']}\n    fix: {i['fix']}")
    sys.exit(2 if counts["CRITICAL"] else 1 if counts["WARN"] else 0)


if __name__ == "__main__":
    main()
