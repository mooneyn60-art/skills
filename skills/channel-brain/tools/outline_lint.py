#!/usr/bin/env python3
"""Check a drawn_quick.py outline BEFORE rendering: catch the template Short before it costs a render.

    python3 outline_lint.py scripts/drawn-house/outlines/*.yaml

Rules (from CONTENT_REVIEW_2026-10-29.md and Nolan's channel data):
  length    the YouTube act (+ "Subscribe." + next) <= 52 words: about 18-20 s at the measured 2.75-3.25 words/s
  action    >= 2 lines use an action macro (chase, xray, scale, shrink, tiny, calm, count): Meatball DOES something
  facts     <= 1 plain "fact" and <= 1 "solo" in the YouTube act: facts are what makes them a slideshow
  shape     the first line is a hook; a punch exists; no line over 14 words
  ending    the punch doesn't deflate ("harmless", a bare "Yes."), and the tease names what's next (not "soon")
  series    series + part are set (the show banner is the follow engine)
Exit 1 if any outline fails. Fix the outline, then render.
"""
import re
import sys

import yaml

ACTION = {"chase", "xray", "scale", "shrink", "tiny", "calm", "count"}
MAX_WORDS, MAX_LINE = 52, 14
DEFLATE = r"\bharmless\b|^\s*(would meatball survive\?\s*)?yes\b[.!]?\s*$|completely safe|nothing to worry"


def lines(act):
    for item in act or []:
        m = next((k for k in item if isinstance(item[k], str) and k not in ("scene", "pose", "prop", "mood")), None)
        if m:
            yield m, item[m]


def lint(path):
    o = yaml.safe_load(open(path))
    yt = list(lines(o.get("yt")))
    fails = []
    words = sum(len(s.split()) for _, s in yt) + 1 + len(str(o.get("next", "")).split())
    if words > MAX_WORDS:
        fails.append(f"{words} words (max {MAX_WORDS}, about 20 s): cut the facts that don't push the story")
    acts = [m for m, _ in yt if m in ACTION]
    if len(acts) < 2:
        fails.append(f"{len(acts)} action line(s) ({', '.join(acts) or 'none'}); need 2+ of chase/xray/scale/shrink/tiny/calm/count")
    for m, cap in (("fact", 1), ("solo", 1)):
        n = sum(1 for k, _ in yt if k == m)
        if n > cap:
            fails.append(f"{n} '{m}' lines (max {cap}): turn them into action lines or cut them")
    if not yt or yt[0][0] != "hook":
        fails.append("the first line isn't a hook")
    if not any(m == "punch" for m, _ in yt):
        fails.append("no punch line (the twist / verdict)")
    for m, s in yt:
        if len(s.split()) > MAX_LINE:
            fails.append(f"{m} line has {len(s.split())} words (max {MAX_LINE}): '{s[:50]}...'")
        if m == "punch" and re.search(DEFLATE, s, re.I):
            fails.append(f"the punch deflates: '{s}'. End on a twist, not 'harmless' or a bare 'Yes'")
    nxt = str(o.get("next", ""))
    if not nxt or re.search(r"\bsoon\b|more things", nxt, re.I):
        fails.append(f"the tease is vague ('{nxt}'): name the next creature and the scary thing it does")
    if not o.get("series") or not o.get("part"):
        fails.append("no series/part: the show banner and number go on every episode")
    return words, fails


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        try:
            words, fails = lint(p)
        except Exception as e:  # a broken outline is a fail, not a crash
            words, fails = 0, [f"can't read: {e}"]
        bad += bool(fails)
        print(f"{'FAIL' if fails else 'PASS'}  {p.split('/')[-1]} ({words} words)")
        for f in fails:
            print(f"   - {f}")
    sys.exit(1 if bad else 0)
