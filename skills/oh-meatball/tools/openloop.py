#!/usr/bin/env python3
"""Open-loop gate for TikTok deep dives (61-75 s). Night shift R&D, 2026-10-25 (research/40, rotation a).

Why: the 62 s cartoon explainer that hit 1.6M (10.3x, @lilpotatestiktok T. rex, vidIQ watch 10/25) promises
"exactly one weakness" at 0:03 and holds the answer until 0:43 (69% of the runtime), walking through two wrong
guesses first. Every one of our 8 deep dives (packs 1-2) states its whole fact in line 1 and promises nothing
for the back half. This tool fails a deep dive that does the same.

Rules for a deep dive (a myth group whose first beat has "_len": "deep", or with 25+ beats):
  R1 promise   one of the first 3 beats withholds something: "promise": true, or a cue such as
               "one weakness", "one thing", "except", "but", "the catch", "secret", or a question mark.
  R2 payoff    exactly one beat has "payoff": true, and it starts 50-80% of the way through the spoken words.
  R3 decoys    at least 2 beats marked "decoy": true (wrong guesses) come before the payoff.
  R4 rehook    a re-hook line ("now the weird part", "but", "here's the thing", "wait") lands in 30-60%.
R1-R3 fail the check; R4 only warns. Shorts (under 25 beats, no "_len": "deep") are skipped: claim-first
openings win there (research/38).

Position is measured in spoken words, which tracks seconds at a fixed voice rate (Andrew +10% speaks about
2.9 words/s including pauses), so the rule does not depend on the voice.

Usage:  openloop.py SCRIPT.json [SCRIPT.json ...] [--json]      exit 1 when any deep dive fails
Import: openloop.check(spec) -> list of per-myth reports (dicts with "fails" and "warns").
"""
import json
import re
import sys
from collections import OrderedDict

PROMISE = re.compile(r"\?|\bone (?:weakness|thing|problem|flaw|mistake|rule)\b|\bexcept\b|\bbut\b|\bthe catch\b"
                     r"|\bsecret\b|\bhere's why\b|\buntil\b|\bnobody knows\b", re.I)
REHOOK = re.compile(r"\bweird part\b|\bhere's the thing\b|\bbut\b|\bwait\b|\bplot twist\b|\bthe catch\b", re.I)
DEEP_MIN_BEATS = 25
PAYOFF_WINDOW = (0.50, 0.80)
REHOOK_WINDOW = (0.30, 0.60)
MIN_DECOYS = 2


def words(b):
    return len(re.findall(r"[\w'.,-]+", b.get("say", "")))


def groups(spec):
    g = OrderedDict()
    for b in spec.get("beats", []):
        if b.get("myth") in (None, "intro", "outro"):
            continue
        g.setdefault(b["myth"], []).append(b)
    return g


def is_deep(beats):
    return beats[0].get("_len") == "deep" or len(beats) >= DEEP_MIN_BEATS


def check_myth(name, beats):
    total = sum(words(b) for b in beats) or 1
    starts, acc = [], 0
    for b in beats:
        starts.append(acc / total)
        acc += words(b)
    fails, warns = [], []
    head = beats[:3]
    if not any(b.get("promise") or PROMISE.search(b.get("say", "")) for b in head):
        fails.append("R1 no open loop in the first 3 lines (line 1: %r)" % beats[0].get("say", ""))
    pay = [i for i, b in enumerate(beats) if b.get("payoff")]
    pay_at = None
    if len(pay) != 1:
        fails.append("R2 needs exactly one \"payoff\": true beat (found %d)" % len(pay))
    else:
        pay_at = starts[pay[0]]
        lo, hi = PAYOFF_WINDOW
        if not lo <= pay_at <= hi:
            fails.append("R2 payoff starts at %d%% of the words; window is %d-%d%%" % (pay_at * 100, lo * 100, hi * 100))
    decoys = sum(1 for i, b in enumerate(beats) if b.get("decoy") and (not pay or i < pay[0]))
    if decoys < MIN_DECOYS:
        fails.append("R3 %d decoy beat(s) before the payoff; need %d" % (decoys, MIN_DECOYS))
    lo, hi = REHOOK_WINDOW
    if not any(lo <= starts[i] <= hi and REHOOK.search(b.get("say", "")) for i, b in enumerate(beats)):
        warns.append("R4 no re-hook line between %d%% and %d%%" % (lo * 100, hi * 100))
    return {"myth": name, "beats": len(beats), "words": total, "est_s": round(total / 2.9, 1),
            "payoff_at": None if pay_at is None else round(pay_at, 2), "decoys": decoys,
            "fails": fails, "warns": warns}


def check(spec):
    """Reports for every deep dive in a script; shorts are skipped."""
    return [check_myth(m, bs) for m, bs in groups(spec).items() if is_deep(bs)]


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print(__doc__)
        return 2
    out, bad = {}, 0
    for p in paths:
        reps = check(json.load(open(p)))
        out[p] = reps
        bad += sum(1 for r in reps if r["fails"])
    if as_json:
        print(json.dumps(out, indent=1))
    else:
        for p, reps in out.items():
            print(f"## {p}: {len(reps)} deep dive(s)")
            for r in reps:
                status = "FAIL" if r["fails"] else "ok"
                pa = "-" if r["payoff_at"] is None else f"{r['payoff_at']:.0%}"
                print(f"  {status:4} {r['myth']:16} {r['beats']:2} beats {r['words']:3} words ~{r['est_s']:.0f}s "
                      f"payoff@{pa} decoys={r['decoys']}")
                for f in r["fails"] + r["warns"]:
                    print(f"       - {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
