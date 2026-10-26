#!/usr/bin/env python3
"""You Submit, Meatball Investigates (research/50 idea 3): turn YouTube comments into a ranked case docket.

The run that uses this calls `vidiq_video_comments` (channelId UCw98RQD81t_339LX5EJqcrg, order "time", or one
videoId per case Short) and saves each response as JSON. This tool never calls vidIQ itself (no credits here).
It reads those files, keeps viewer comments and replies that suggest a case, drops anything on the OPERATIONS red
list, ranks the rest by likes (then newest), and merges them into data/submissions.csv. Rows already in the CSV
keep their `status` and `permission`; likes are refreshed.

What counts as a submission: a viewer comment (not by the channel) that names something to investigate: "investigate
X", "case: X", "do X next", "what about X?", "you should cover X", "is X real?", or "#case X". Plain guesses
("✅", "True 🎉") and chat ("Hello", "First") are skipped.

Red list (OPERATIONS.md, factdesk): vaccines or medical cures; elections; recent tragedies (shootings, bombings,
attacks, disasters with victims who are alive or mourned now); living private people (anyone named who is not a
public historical figure, "my neighbour", @mentions); secret-society theories that target a group; fabricated
"proof" (time travellers, AI fakes). The filter is a keyword screen: it removes the obvious ones; the factdesk
still reads the top row before it becomes a script.

Columns: rank, likes, suggestion, text, author, permission, status, video_id, video_title, comment_id, published_at
  permission  ask (default) | yes | no. Viewer Case Friday shows the handle only on "yes"; otherwise no handle.
  status      new | picked (being made) | done (posted; date) | skip (factdesk said no; reason)

Usage:  submissions.py COMMENTS.json [...] [--out data/submissions.csv] [--rejected]   (--rejected lists drops)
Import: submissions.extract(response_dict) -> [row], submissions.red(text) -> reason or None
"""
import csv
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "submissions.csv")
COLS = ["rank", "likes", "suggestion", "text", "author", "permission", "status", "video_id", "video_title",
        "comment_id", "published_at"]

ASK = re.compile(
    r"(?:investigate|look into|check out|do a (?:video|case|short) (?:on|about)|you should (?:do|cover|investigate)"
    r"|can you (?:do|cover|investigate)|please (?:do|cover|investigate)|next case|case(?: idea)?\s*[:#-]|#case"
    r"|cover(?![-\w])|what about|how about)\s*[:\-]?\s*(?P<s>[^.!?\n]{3,90})", re.I)
REAL = re.compile(r"\b(?:is|was|are|were|did)\s+(?P<s>(?:the\s+)?[A-Z0-9][^?\n]{3,80})\s+(?:real|true|fake|a hoax)\s*\?", re.I)
RED = {
    "vaccines or medical cures": r"vaccin|vax|cure[sd]?\b|cancer|autism|covid|ivermectin|chemtrail|fluorid|big pharma|5g",
    "elections": r"elect(?:ion|ed|oral)|ballot|voter|rigged|stolen vote|president(?:ial)? race|campaign",
    "recent tragedies": r"shooting|massacre|bombing|terror|9/?11|sandy hook|school shoot|crash victims|"
                        r"false flag|crisis actor|genocide|pandemic|war in (?:ukraine|gaza|israel)",
    "living private people": r"\bmy (?:neighbou?r|teacher|boss|ex|friend|mom|dad|brother|sister|uncle|aunt|cousin)\b|"
                             r"(?<![\w])@\w+",
    "secret societies that target a group": r"illuminati|new world order|\bnwo\b|reptilian|rothschild|soros|"
                                            r"zionist|jews?\b|jewish|freemason|globalist|great replacement|cabal",
    "fabricated proof": r"time travell?er|from the future|ai (?:video|footage|photo)|deepfake",
}
RED_RE = {k: re.compile(v, re.I) for k, v in RED.items()}
LEAD = re.compile(r"^(?:\s*@[\w.-]+)+\s*")
JUNK = re.compile(r"^\W*(?:first|hello|hi|hey|lol|true|false|yes|no+|real|fake)\W*$", re.I)


def clean(t):
    t = html.unescape(re.sub(r"<br\s*/?>", "\n", t or ""))
    return re.sub(r"<[^>]+>", "", t).replace("​", "").strip()


def red(text):
    text = LEAD.sub("", text)   # "@MeatballMyths investigate..." is a reply to us, not a named person
    for reason, rx in RED_RE.items():
        if rx.search(text):
            return reason
    return None


def suggestion(text):
    """The thing to investigate, or None when the comment doesn't suggest a case."""
    text = LEAD.sub("", text)
    if JUNK.match(text) or len(text) < 6:
        return None
    m = REAL.search(text) or ASK.search(text)
    if not m:
        return None
    s = re.sub(r"\s+", " ", m.group("s")).strip(" -:,'\"")
    s = re.sub(r"^(?:the case of|a video on|about|on)\s+", "", s, flags=re.I)
    return s[:90] if len(s) >= 3 and not JUNK.match(s) else None


def extract(resp):
    """Rows from one vidiq_video_comments response (top-level comments and replies by viewers)."""
    rows = []
    for th in resp.get("comments", []):
        items = [th.get("topComment") or {}] + list(th.get("replies") or [])
        for k, c in enumerate(items):
            if c.get("byChannelOwner") or not c:
                continue
            text = clean(c.get("text"))
            rows.append(dict(likes=int(c.get("likeCount") or 0), text=text, author=c.get("author", ""),
                             video_id=th.get("videoId", ""), video_title=th.get("videoTitle", ""),
                             comment_id=th.get("commentId", "") + ("" if k == 0 else f".r{k}"),
                             published_at=c.get("publishedAt", "")))
    return rows


def main(argv):
    out, show_rej = OUT, "--rejected" in argv
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    files = [a for k, a in enumerate(argv) if not a.startswith("--") and (k == 0 or argv[k - 1] != "--out")]
    if not files:
        sys.exit(__doc__)
    old = {}
    if os.path.exists(out):
        old = {r["comment_id"]: r for r in csv.DictReader(open(out, newline=""))}
    found, rej = {}, []
    for f in files:
        data = json.load(open(f))
        for resp in (data if isinstance(data, list) else [data]):
            for r in extract(resp):
                s = suggestion(r["text"])
                if not s:
                    continue
                why = red(r["text"])
                if why:
                    rej.append((why, r["text"][:80]))
                    continue
                prev = old.get(r["comment_id"], {})
                found[r["comment_id"]] = dict(r, suggestion=s, permission=prev.get("permission") or "ask",
                                              status=prev.get("status") or "new")
    merged = {**old, **found}   # rows seen before but not in this pull stay (with their last like count)
    rows = sorted(merged.values(), key=lambda r: (-int(r.get("likes") or 0), r.get("published_at", "")), reverse=False)
    rows = sorted(rows, key=lambda r: r.get("status") in ("done", "skip"))   # open cases first
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for k, r in enumerate(rows, 1):
            w.writerow(dict(r, rank=k))
    top = next((r for r in rows if r.get("status") == "new"), None)
    print(f"{len(found)} submissions this pull, {len(rej)} red-listed, {len(rows)} on the docket -> {out}")
    if top:
        print(f"top safe case: {top['suggestion']!r} ({top['likes']} likes, permission {top['permission']})")
    if show_rej:
        for why, t in rej:
            print(f"  red list ({why}): {t}")
    return rows


if __name__ == "__main__":
    main(sys.argv[1:])
