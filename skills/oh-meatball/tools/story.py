#!/usr/bin/env python3
"""Story Cut gate (75-120 s TikTok stories). Story engine 2026-10-26 (research/52).

Why: the outliers we watched frame by frame (Voggle's Mike the Headless Chicken 2.8M/347x, @danocracy Area 51 Ep 2
1.1M/301x, @mrdeepdive 565K, @realmelanieking 10M) are stories, not quizzes: someone wants something, every answer
opens the next question within 2 lines, the stakes climb in steps, a false calm sits at 80-90%, and the ending is
an ironic kicker or a cliffhanger. Our case format has none of these. This tool fails a Story Cut that skips one.

A Story Cut is a myth group (beats sharing one "myth"; "intro"/"outro" skipped) whose first beat has
"_len": "story". Rules:
  S1 protagonist  one of the first 3 beats is marked "want": true and names a person or group (a capitalised
                  name or acronym after the first word: "The CIA wanted that sub").
  S2 loop chain   after every beat marked "resolves": true, a beat marked "opens": true, or a line with a
                  question/tease cue ("?", but, until, then, wait, problem, the catch, except, it gets worse),
                  comes within the next 2 beats. The resolving beat itself counts when it is also "opens": true.
                  The last resolving beat (the final payoff) is exempt.
  S3 escalation   at least 3 beats marked "step": true (or numbered "step": 1, 2, 3...; numbers must rise in
                  beat order).
  S4 false calm   exactly one beat marked "calm": true starts at 70-90% of the spoken words, and one of the
                  next 2 beats is the drop ("drop": true, or a cue: until, then, but, suddenly, except).
  S5 ending       the last spoken beat that is not an ask (no "ask"/"sub", no Subscribe/Comment/Follow/"guess
                  right") is "kicker": true or "cliffhanger": true.
  S6 host resets  no stretch over 20 s without a host beat ("host" set): from 0 s to the first, between host
                  beats, and from the last to the end.
  W1 length       warns outside 75-120 s.
Seconds are estimated from spoken words at 2.9 words/s (same basis as openloop.py and coldopen.py); the themed
voices run 2.4-2.6 words/s once rendered, so the real cut is 10-20% longer than the estimate.

Usage:  story.py SCRIPT.json [SCRIPT.json ...] [--json]      exit 1 when any Story Cut fails
        story.py --self-test                                  runs the built-in fixture checks
Import: story.check(spec) -> list of per-myth reports (dicts with "fails" and "warns").
"""
import copy
import json
import re
import sys
from collections import OrderedDict

WPS = 2.9
CALM_WINDOW = (0.70, 0.90)
MAX_HOST_GAP_S = 20.0
MIN_STEPS = 3
LENGTH_S = (75, 120)
TEASE = re.compile(r"\?|\bbut\b|\buntil\b|\bthen\b|\bwait\b|\bproblem\b|\bthe catch\b|\bexcept\b|"
                   r"\bit gets worse\b|\bhere's the thing\b", re.I)
DROP = re.compile(r"\buntil\b|\bthen\b|\bbut\b|\bsuddenly\b|\bexcept\b", re.I)
ASK = re.compile(r"\bsubscribe\b|\bcomment\b|\bguess right\b|\bfollow\b", re.I)
NAMED = re.compile(r"\b(?:[A-Z][a-z]+|[A-Z]{2,})\b")


def words(b):
    return len(re.findall(r"[\w'.,-]+", b.get("say", "")))


def groups(spec):
    g = OrderedDict()
    for b in spec.get("beats", []):
        if b.get("myth") in (None, "intro", "outro"):
            continue
        g.setdefault(b["myth"], []).append(b)
    return g


def is_story(beats):
    return beats[0].get("_len") == "story"


def names_someone(say):
    """A capitalised name or acronym anywhere but the first word ("The CIA wanted..." -> CIA)."""
    toks = say.split(None, 1)
    return bool(len(toks) > 1 and NAMED.search(toks[1]))


def is_ask(b):
    return bool(b.get("ask") or b.get("sub") or ASK.search(b.get("say", "")))


def check_myth(name, beats):
    total = sum(words(b) for b in beats) or 1
    starts, acc = [], 0
    for b in beats:
        starts.append(acc / total)
        acc += words(b)
    est = total / WPS
    fails, warns = [], []

    want = [b for b in beats[:3] if b.get("want")]
    if not want:
        fails.append("S1 no \"want\": true beat in the first 3 lines (who wants what?)")
    elif not any(names_someone(b.get("say", "")) for b in want):
        fails.append("S1 the want beat names no person or group: %r" % want[0].get("say", ""))

    res = [i for i, b in enumerate(beats) if b.get("resolves")]
    for i in res[:-1]:
        win = ([i] if beats[i].get("opens") else []) + list(range(i + 1, min(i + 3, len(beats))))
        if not any(beats[j].get("opens") or TEASE.search(beats[j].get("say", "")) for j in win):
            fails.append("S2 beat %d resolves (%r) and nothing opens a new question within 2 beats"
                         % (i, beats[i].get("say", "")[:50]))
    if not res:
        warns.append("S2 no \"resolves\": true beats marked, so the loop chain was not checked")

    steps = [(i, b["step"]) for i, b in enumerate(beats) if b.get("step")]
    nums = [s for _, s in steps if not isinstance(s, bool)]
    if len(steps) < MIN_STEPS:
        fails.append("S3 %d escalation step(s); need %d" % (len(steps), MIN_STEPS))
    elif nums and nums != sorted(nums):
        fails.append("S3 numbered steps out of order: %s" % nums)
    elif nums and len(set(nums)) != len(nums):
        fails.append("S3 repeated step numbers: %s" % nums)

    calm = [i for i, b in enumerate(beats) if b.get("calm")]
    calm_at = None
    if len(calm) != 1:
        fails.append("S4 needs exactly one \"calm\": true beat (found %d)" % len(calm))
    else:
        i = calm[0]
        calm_at = starts[i]
        lo, hi = CALM_WINDOW
        if not lo <= calm_at <= hi:
            fails.append("S4 false calm starts at %d%% of the words; window is %d-%d%%" % (calm_at * 100, lo * 100, hi * 100))
        nxt = beats[i + 1:i + 3]
        if not any(b.get("drop") or DROP.search(b.get("say", "")) for b in nxt):
            fails.append("S4 nothing drops within 2 beats of the false calm (%r)" % beats[i].get("say", "")[:50])

    spoken = [b for b in beats if b.get("say") and not is_ask(b)]
    if not (spoken and (spoken[-1].get("kicker") or spoken[-1].get("cliffhanger"))):
        fails.append("S5 last story line is neither \"kicker\" nor \"cliffhanger\": %r"
                     % (spoken[-1]["say"] if spoken else ""))

    host_t = [starts[i] * est for i, b in enumerate(beats) if b.get("host")]
    marks = [0.0] + host_t + [est]
    gap = max(b - a for a, b in zip(marks, marks[1:]))
    if gap > MAX_HOST_GAP_S:
        k = max(range(len(marks) - 1), key=lambda j: marks[j + 1] - marks[j])
        fails.append("S6 %.0f s without a host beat (%.0f-%.0f s); max %.0f s" % (gap, marks[k], marks[k + 1], MAX_HOST_GAP_S))

    lo, hi = LENGTH_S
    if not lo <= est <= hi:
        warns.append("W1 ~%.0f s estimated; a Story Cut runs %d-%d s" % (est, lo, hi))
    return {"myth": name, "beats": len(beats), "words": total, "est_s": round(est, 1), "steps": len(steps),
            "calm_at": None if calm_at is None else round(calm_at, 2), "host_gap_s": round(gap, 1),
            "fails": fails, "warns": warns}


def check(spec):
    """Reports for every Story Cut in a script; other groups are skipped."""
    return [check_myth(m, bs) for m, bs in groups(spec).items() if is_story(bs)]


# A minimal Story Cut that passes; each mutation below must trip exactly the rule it names.
FIXTURE = {"beats": [dict(myth="t", **b) for b in [
    {"_len": "story", "say": "The rope snapped and the boat slid into the dark water of the bay."},
    {"say": "The Navy wanted that boat back. Would they get it? Guess.", "want": True, "host": True, "ask": {"q": "?"}},
    {"say": "Subscribe. I open a new case every day.", "sub": {"at": "Subscribe"}},
    {"say": "See, in 1950, it was the fastest boat in the whole fleet and it was full of secrets.", "host": True},
    {"say": "Divers found it on the bottom, right where it sank, in one piece.", "resolves": True},
    {"say": "Problem: the bottom was a mile down. So how do you lift a whole boat?", "step": 1},
    {"say": "They built a crane barge the size of a city block, and towed it out to sea.", "step": 2, "host": True},
    {"say": "It hooked the boat and pulled, and the boat came up off the mud, inch by inch.", "resolves": True},
    {"say": "Then the cable started to twist, and the whole crew backed away from the edge of the deck.", "step": 3},
    {"say": "They winched it the rest of the way, slowly, and it broke the surface at last at dawn.", "host": True},
    {"say": "The boat sat on the barge, dripping. Everyone cheered and went to bed.", "calm": True},
    {"say": "Until the night watch saw the hatch open by itself.", "drop": True, "host": True},
    {"say": "Nobody ever found out who was inside it.", "resolves": True},
    {"say": "Did you guess right? Comment."},
    {"say": "And the barge is still parked in that bay, rusting, with the boat still on it.", "kicker": True}]]}
MUTATIONS = {
    "S1": lambda bs: bs[1].pop("want"),
    "S2": lambda bs: (bs[5].update(say="The bottom was a mile down."), bs[6].update(say="They built a barge.")),
    "S3": lambda bs: bs[8].pop("step"),
    "S4": lambda bs: bs[11].update(say="The night watch saw the hatch open by itself.", drop=False),
    "S5": lambda bs: bs[14].pop("kicker"),
    "S6": lambda bs: [b.pop("host", None) for b in bs[1:12]],
}


def self_test():
    base = check(FIXTURE)[0]
    ok = not base["fails"]
    print(("ok  " if ok else "FAIL") + " fixture passes: %s" % (base["fails"] or "no fails"))
    for rule, mutate in MUTATIONS.items():
        spec = copy.deepcopy(FIXTURE)
        mutate(spec["beats"])
        got = sorted({f[:2] for f in check(spec)[0]["fails"]})
        good = got == [rule]
        ok &= good
        print(("ok  " if good else "FAIL") + f" {rule} mutation trips {got}")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
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
            print(f"## {p}: {len(reps)} Story Cut(s)")
            for r in reps:
                status = "FAIL" if r["fails"] else "ok"
                ca = "-" if r["calm_at"] is None else f"{r['calm_at']:.0%}"
                print(f"  {status:4} {r['myth']:16} {r['beats']:2} beats {r['words']:3} words ~{r['est_s']:.0f}s "
                      f"steps={r['steps']} calm@{ca} max-host-gap={r['host_gap_s']:.0f}s")
                for f in r["fails"] + r["warns"]:
                    print(f"       - {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
