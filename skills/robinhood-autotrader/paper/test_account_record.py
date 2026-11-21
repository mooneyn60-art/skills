#!/usr/bin/env python3
"""
Agenda item 6: slice the live account's closed trades. Prints data only.
Design: research/2026-09-25_ACCOUNT_RECORD.md (committed first).
Usage: python3 paper/test_account_record.py
"""
import json, math, os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SPY = json.load(open(os.path.join(HERE, "history", "book_daily.json")))["prices"]["SPY"]
STREAK_ON = ("2026-09-14T14:09:13", "2026-09-17T13:32:17")  # 3rd consecutive TARS loss -> TENB win
RULE_EXITS = {"R4_hard_stop", "R4_trail", "stop_fired"}


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def welch(a, b):
    if len(a) < 3 or len(b) < 3:
        return "t n/a (a side has n<3)"
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return f"diff {ma - mb:+.2f}R t={(ma - mb) / math.sqrt(va / len(a) + vb / len(b)):+.2f}"


def main():
    rows = {}
    for line in open(os.path.join(HERE, "trades.jsonl")):
        if line.strip():
            d = json.loads(line)
            rows[d["id"].replace("-CORRECTION", "")] = d
    T = []
    for d in rows.values():
        if (d.get("account") == "live" and d.get("realized_pnl") is not None and d.get("planned_risk")
                and d.get("exit_reason") not in (None, "not_taken") and d.get("opened") and d.get("closed")):
            T.append(dict(id=d["id"], r=d["realized_pnl"] / d["planned_risk"],
                          owner="TARS" if str(d.get("strategy") or "").startswith("TARS") else "Nolan",
                          opt=str(d.get("instrument", "")).startswith("option") or "contract" in d,
                          o=ts(d["opened"]), c=ts(d["closed"]), exit=d["exit_reason"]))
    spy_days = sorted(SPY)
    print(f"source: paper/trades.jsonl, {len(T)} closed live trades with planned_risk, "
          f"{min(t['o'] for t in T):%Y-%m-%d} to {max(t['c'] for t in T):%Y-%m-%d}")

    def slice_(name, f, a_lab, b_lab):
        a = [t["r"] for t in T if f(t)]
        b = [t["r"] for t in T if not f(t)]
        fm = lambda x: f"n={len(x):>2} mean {sum(x) / len(x):+.2f}R" if x else "n= 0"
        print(f"  {name:<34} {a_lab}: {fm(a)} | {b_lab}: {fm(b)} | {welch(a, b)}")

    def prev_spy_down(t):
        d = t["o"].strftime("%Y-%m-%d")
        prior = [x for x in spy_days if x < d]
        return SPY[prior[-1]] < SPY[prior[-2]]

    slice_("A1 owner", lambda t: t["owner"] == "TARS", "TARS", "Nolan")
    slice_("A1 instrument", lambda t: t["opt"], "option", "equity")
    slice_("A2 holding time", lambda t: (t["c"] - t["o"]).total_seconds() < 3600, "<1 hour", ">=1 hour")
    slice_("A3 entry in first hour (UTC 13:30-14:30)",
           lambda t: 13.5 <= t["o"].hour + t["o"].minute / 60 < 14.5, "first hour", "later")
    slice_("A4 exit type", lambda t: t["exit"] in RULE_EXITS, "rule exit", "discretionary")
    on = (ts(STREAK_ON[0] + "Z"), ts(STREAK_ON[1] + "Z"))
    slice_("A5 opened during TARS streak>=3", lambda t: on[0] <= t["o"] < on[1], "during", "not")
    slice_("A6 entered after SPY down day", prev_spy_down, "after down", "after up")
    print("  holding times: " + ", ".join(f"{(t['c'] - t['o']).total_seconds() / 3600:.1f}h" for t in
                                            sorted(T, key=lambda t: t["o"])))


if __name__ == "__main__":
    main()
