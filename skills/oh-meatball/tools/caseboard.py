#!/usr/bin/env python3
"""Meatball's case board: a season arc (research/50 idea 4). Every finished case pins one polaroid to the cork
board behind Meatball's desk, so the host backdrop grows on screen from case to case. The data is
data/caseboard.json, a list of {case, title, myth, photo, obs, verdict, fork, added}.

Script field: spec "caseboard": true. Host shots then pin the last 4 past cases (every entry whose "case" is not
this Short's) as small labelled polaroids along the sides of the board (tools/host.py `backdrop(past=...)`).

The Fork thread ("Who keeps leaving the Fork at my crime scenes?", research/39 running gag): one gag beat every
4-5 cases. `fork-due` says whether this case should carry it (4+ cases pinned since the last Fork case). The beat
is a host line with "host": {"fork": true, ...}; `add` records it, so the count restarts.

Usage:
  caseboard.py add SCRIPT.json [MYTH ...]   append each hook beat's case (or only the named myth groups)
  caseboard.py show                         print the board
  caseboard.py fork-due                     exit 0 and print "due" when the next case should carry the Fork beat
Import: caseboard.past(case, n=4) -> entries to pin; caseboard.fork_due() -> bool.
"""
import datetime
import json
import os
import sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "caseboard.json")
EVERY = 4   # a Fork beat when this many cases have been pinned since the last one (so every 4-5 cases)


def load():
    try:
        return json.load(open(PATH))
    except FileNotFoundError:
        return []


def past(case, n=4):
    """The last n pinned cases other than `case` (oldest first)."""
    return [e for e in load() if e.get("case", "").upper() != (case or "").upper()][-n:]


def fork_due():
    board = load()
    last = max((k for k, e in enumerate(board) if e.get("fork")), default=None)
    return len(board) >= EVERY if last is None else len(board) - 1 - last >= EVERY


def entries(spec, only=()):
    """One entry per hook beat that carries a "case" (the Short; its deep cut shares the case and is skipped)."""
    out, seen = [], set()
    beats = spec["beats"]
    for b in beats:
        if not (b.get("hook") and b.get("case")) or (only and b["myth"] not in only):
            continue
        if b["case"] in seen:
            continue
        group = [x for x in beats if x.get("myth") == b["myth"]]
        same = {h["myth"] for h in beats if h.get("hook") and h.get("case") == b["case"]}   # Short + its deep cut
        seen.add(b["case"])
        shot = (b.get("shots") or [{}])[0]
        stamp = next((x["stamp"] for x in group if x.get("stamp")), None)
        stamp = stamp.get("text") if isinstance(stamp, dict) else stamp
        out.append(dict(case=b["case"], title=b.get("board_title") or b.get("headline") or b["myth"],
                        myth=b["myth"], photo=shot.get("photo", b["myth"]), obs=shot.get("obs"),
                        verdict=(stamp or "").replace("\n", " "),
                        fork=any(isinstance(x.get("host"), dict) and x["host"].get("fork")
                                 for x in beats if x.get("myth") in same),
                        added=datetime.date.today().isoformat()))
    return out


def add(spec, only=()):
    board = load()
    have = {(e["case"], e["myth"].removesuffix("deep")) for e in board}
    new = [e for e in entries(spec, only) if (e["case"], e["myth"].removesuffix("deep")) not in have]
    json.dump(board + new, open(PATH, "w"), indent=1, ensure_ascii=False)
    return new


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "add":
        for e in add(json.load(open(sys.argv[2])), tuple(sys.argv[3:])):
            print("pinned", e["case"], e["title"], e["verdict"], "(Fork)" if e["fork"] else "")
    elif cmd == "fork-due":
        due = fork_due()
        print("due" if due else "not due")
        sys.exit(0 if due else 1)
    else:
        for e in load():
            print(f'{e["case"]:>10}  {e["verdict"]:<12} {e["title"]}{"  (Fork)" if e.get("fork") else ""}')
