#!/usr/bin/env python3
"""Retention gate for story long-forms (16:9 "Meatball Explains"). Retention desk, 2026-10-25 (research/47).

Why: our only long-form with retention data (gFhrONKK0rI, 2:15 quiz pilot, 11 viewers) lost a viewer at 2 s (quiz
framing), at 4 s (it answered its own opening question), two at 14 s on the agenda line ("Today we're fixing the
animal facts..."), one at 18 s re-stating the answer, then one per long single-myth stretch (28 s, 46 s, 72 s).
Breakout small-channel animal long-forms (vidIQ outliers 10/25, research/47) open on the first animal at 0:00,
never introduce themselves, and change animal every 40-95 s under a structure the viewer can count.

Rules (R1-R7 fail the script; W-lines only warn). Times are estimated from spoken words (WPS, calibrated on
the 10/25 Kokoro renders: 3.35 words/s incl. pauses, +0.12 s a line + "hold"), or read exactly from a render's
timeline.json with --timeline.
  R1 cold open    a beat starting in the first 30 s promises the payoff ("at the end", "I'll show you",
                  "the last one", "number one", or beat "promise": true); frame 0 is an unblurred photo with no
                  label; no intro, welcome or agenda line ("I'm Meatball", "today we", "welcome", "in this
                  video") before 30 s.
  R2 loops        from 30 s to the payoff chapter, an open loop or re-hook (a tease of what's next, a cliffhanger,
                  a countdown step; beat "rehook": true or a matching line) at least every 75 s (aim 45-60 s).
  R3 structure    every story chapter opens on a beat with "counter": {"n": k, "of": N} (drawn on screen as
                  "k OF N" by tools/v3.py), numbered 1..N in order, and spec "progress": true (progress bar).
  R4 segments     no stretch over 75 s without a new animal (first photo of a species), a twist (beat
                  "twist": true or a twist line) or a Meatball jeopardy beat ("jeopardy": true).
  R5 save best    exactly one chapter opens on a beat with "payoff": true; it is the last counted chapter (only an
                  uncounted wrap-up may follow), starts
                  in the back 35% of the runtime, the "outro" wrap-up runs <= 60 s, and it is teased in the
                  first 30 s (R1) and again mid-video (W).
  R6 expectation  the title's (and spec "thumb_text"'s) key words are said or labelled in the first 60 s (at
                  least half of them), and story chapter 1 starts by 60 s.
  R7 length       5:00-7:00 total while average view duration is under 2:00 (mid-rolls need 8:00+; that trade
                  is taken on purpose until AVD improves; research/47 §4).

Usage:  retention.py SCRIPT.json [...] [--timeline WORK/timeline.json] [--json]   exit 1 if any script fails
Import: retention.check(spec, timeline=None) -> report dict ({"fails": [...], "warns": [...], ...}).
Applies to long-forms only (spec "aspect": "16:9" without "vertical"); other scripts are skipped.
"""
import json
import re
import sys

WPS, GAP = 3.35, 0.12
OPEN_S, EXPECT_S = 30.0, 60.0
LOOP_MAX, LOOP_AIM = 75.0, 60.0
SEG_MAX = 75.0
PAYOFF_FROM = 0.65
WRAP_MAX = 60.0
LEN_RANGE = (300.0, 420.0)
INTRO_OK_AFTER = 30.0

PROMISE = re.compile(r"\bat the end\b|\bby the end\b|\bi'll show you\b|\bthe last one\b|\bnumber one\b|"
                     r"\bsaved? (?:it|the \w+) for last\b|\bstick around\b|\bwait (?:till|until)\b|\bit's at the end\b"
                     r"|\bthat one's at the end\b|\bcoming up\b", re.I)
INTRO = re.compile(r"\bi'm meatball\b|\btoday we\b|\btoday[:,]|\bwelcome\b|\bin this video\b|\bhey guys\b|"
                   r"\blet's get started\b|\bhi everyone\b", re.I)
REHOOK = re.compile(r"\bnext one\b|\bthe next\b|\bcoming up\b|\bstill to come\b|\bnumber (?:one|two|three|four|five|"
                    r"six|seven)\b|\bbut first\b|\bin a minute\b|\b(?:it|this) gets worse\b|\bis worse\b|\beven worse\b"
                    r"|\bstick around\b|\bthe last one\b|\bat the end\b|\bhere's the twist\b|\bi promised\b"
                    r"|\bremember (?:that|this)\b|\bwait\b|\bbut\b.*\?$", re.I)
TWIST = re.compile(r"\bhere's the (?:thing|twist|creepy part|weird part|catch)\b|\bplot twist\b|\bbut here's\b|"
                   r"\bthen it went wrong\b|\bit gets worse\b|\bthe twist\b|\bnow here's\b", re.I)
STOP = set("a an and are at be by for from how i in is isn't it its it's of on one or that the this to was what "
           "with you your (and) why who not think thought really".split())
STORY_SKIP = ("intro", "outro")


def words(b):
    return len(re.findall(r"[\w'.,-]+", b.get("say", "")))


def times(spec, timeline=None):
    """(start, duration) per beat: exact from a render's timeline.json, else estimated from words."""
    if timeline:
        return [(e["start"], e["dur"]) for e in timeline]
    out, t = [], 0.0
    for b in spec["beats"]:
        d = words(b) / WPS + GAP + float(b.get("hold", 0))
        out.append((t, d))
        t += d
    return out


def chapters(spec, ts):
    """[(title, start, first beat index, beat)] for every beat with a "chapter"."""
    return [(b["chapter"], ts[i][0], i, b) for i, b in enumerate(spec["beats"]) if b.get("chapter")]


def species(b):
    from_shots = [s.get("photo") for s in (b.get("shots") or [b]) if s.get("photo")]
    return from_shots


def is_long(spec):
    return spec.get("aspect") == "16:9" and not spec.get("vertical")


def _terms(text):
    return [w[:5] for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP and len(w) > 2]


def check(spec, timeline=None):
    beats = spec["beats"]
    ts = times(spec, timeline)
    total = ts[-1][0] + ts[-1][1]
    chs = chapters(spec, ts)
    # story chapters: after the cold open, up to and including the payoff; later ones are the wrap-up
    body = chs[1:]
    p = next((k for k, c in enumerate(body) if c[3].get("payoff")), None)
    story = body[:p + 1] if p is not None else [c for c in body if c[3].get("myth") not in STORY_SKIP]
    fails, warns = [], []
    start = lambda i: ts[i][0]

    # R1 cold open
    head = [i for i in range(len(beats)) if start(i) < OPEN_S]
    if not any(beats[i].get("promise") or PROMISE.search(beats[i].get("say", "")) for i in head):
        fails.append("R1 no payoff promise in the first 30 s (say what they'll see at the end)")
    b0 = beats[0]
    s0 = (b0.get("shots") or [b0])[0]
    if not s0.get("photo") or s0.get("blur") or (b0.get("label") and not (isinstance(b0["label"], dict)
                                                                           and b0["label"].get("at"))):
        fails.append("R1 frame 0 must be the best animal photo, unblurred, no text card")
    for i in range(len(beats)):
        if start(i) < INTRO_OK_AFTER and INTRO.search(beats[i].get("say", "")):
            fails.append(f"R1 intro/agenda line at {start(i):.0f}s (beat {i}): {beats[i]['say'][:60]!r}")

    # R5 payoff chapter (needed by R2)
    pay = [c for c in body if c[3].get("payoff")]
    pay_t = total
    if len(pay) != 1:
        fails.append(f"R5 needs exactly one story chapter opening on \"payoff\": true (found {len(pay)})")
    else:
        pay_t = pay[0][1]
        wrap = [c for c in body[p + 1:] if c[3].get("myth") == "outro"]
        if wrap and total - wrap[0][1] > WRAP_MAX:
            fails.append(f"R5 wrap-up after the payoff runs {total - wrap[0][1]:.0f}s (max {WRAP_MAX:.0f}): "
                         "viewers leave once the promise is paid")
        late = [c[0] for c in body[p + 1:] if c[3].get("counter")]
        if late:
            fails.append(f"R5 counted chapters after the payoff {late}: the strongest story goes last")
        if pay_t < PAYOFF_FROM * total:
            fails.append(f"R5 payoff starts at {pay_t:.0f}s = {pay_t / total:.0%}; keep it in the back "
                         f"{1 - PAYOFF_FROM:.0%}")
        mid = [i for i in range(len(beats)) if 0.3 * total <= start(i) <= 0.7 * total
               and (beats[i].get("tease") or re.search(r"\bat the end\b|\bthe last one\b|\bnumber one\b|"
                                                       r"\bi promised\b|\bsaving\b|\bstill coming\b|\bto go\b", beats[i].get("say", ""), re.I))]
        if not mid:
            warns.append("W5 the payoff isn't teased again between 30% and 70%")

    # R2 open loops / re-hooks between the cold open and the payoff
    hooks = [start(i) for i, b in enumerate(beats)
             if OPEN_S <= start(i) <= pay_t and (b.get("rehook") or b.get("counter") or REHOOK.search(b.get("say", ""))
                                             or TWIST.search(b.get("say", "")))]
    marks = [OPEN_S] + hooks + [pay_t]
    gaps = [(a, z) for a, z in zip(marks, marks[1:]) if z - a > LOOP_MAX]
    for a, z in gaps:
        fails.append(f"R2 {z - a:.0f}s without an open loop or re-hook ({a:.0f}-{z:.0f}s; max {LOOP_MAX:.0f})")
    wide = [(a, z) for a, z in zip(marks, marks[1:]) if LOOP_AIM < z - a <= LOOP_MAX]
    for a, z in wide:
        warns.append(f"W2 {z - a:.0f}s between re-hooks ({a:.0f}-{z:.0f}s; aim 45-{LOOP_AIM:.0f})")

    # R3 visible structure
    nums = [c[3].get("counter") for c in story]
    if not spec.get("progress"):
        fails.append("R3 spec needs \"progress\": true (progress bar on screen)")
    if any(not isinstance(n, dict) for n in nums):
        miss = [c[0] for c, n in zip(story, nums) if not isinstance(n, dict)]
        fails.append(f"R3 story chapters without an on-screen counter: {miss}")
    else:
        N = {n.get("of") for n in nums}
        if [n.get("n") for n in nums] != list(range(1, len(nums) + 1)) or len(N) != 1:
            fails.append(f"R3 counters must run 1..N with one N; got {[(n.get('n'), n.get('of')) for n in nums]}")

    # R4 segment length
    seen, events = set(), [0.0]
    for i, b in enumerate(beats):
        new = [p for p in species(b) if p not in seen]
        seen.update(new)
        if new or b.get("twist") or b.get("jeopardy") or TWIST.search(b.get("say", "")) or b.get("chapter"):
            events.append(start(i))
    events.append(total)
    for a, z in zip(events, events[1:]):
        if z - a > SEG_MAX:
            fails.append(f"R4 {z - a:.0f}s with no new animal, twist or jeopardy beat ({a:.0f}-{z:.0f}s)")

    # R6 expectation match
    terms = list(dict.fromkeys(_terms(spec.get("title", "") + " " + spec.get("thumb_text", ""))))
    said = " ".join(b.get("say", "") + " " + str((b.get("label") or {}).get("text", "") if isinstance(b.get("label"), dict)
                                                  else b.get("label") or "")
                    for i, b in enumerate(beats) if start(i) < EXPECT_S)
    got = set(_terms(said))
    hit = [t for t in terms if t in got]
    if terms and len(hit) < len(terms) / 2:
        fails.append(f"R6 first 60 s pays off only {len(hit)}/{len(terms)} title/thumbnail words "
                     f"(missing {[t for t in terms if t not in got]})")
    if story and story[0][1] > EXPECT_S:
        fails.append(f"R6 story chapter 1 starts at {story[0][1]:.0f}s (by {EXPECT_S:.0f}s)")

    # R7 length
    if not LEN_RANGE[0] <= total <= LEN_RANGE[1]:
        fails.append(f"R7 runtime {total / 60:.1f} min; target 5-7 min until AVD > 2:00")

    return {"title": spec.get("title"), "total_s": round(total, 1), "chapters": [(c[0], round(c[1])) for c in chs],
            "rehooks": [round(t) for t in hooks], "payoff_at": None if not pay else round(pay_t),
            "est": timeline is None, "fails": fails, "warns": warns}


def main(argv):
    as_json = "--json" in argv
    tl = None
    if "--timeline" in argv:
        k = argv.index("--timeline")
        tl = json.load(open(argv[k + 1]))
        argv = argv[:k] + argv[k + 2:]
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print(__doc__)
        return 2
    out, bad = {}, 0
    for p in paths:
        spec = json.load(open(p))
        if not is_long(spec):
            continue
        r = check(spec, tl)
        out[p] = r
        bad += bool(r["fails"])
    if as_json:
        print(json.dumps(out, indent=1))
    else:
        for p, r in out.items():
            print(f"## {p}: {'FAIL' if r['fails'] else 'ok'} {r['total_s'] / 60:.1f} min "
                  f"({'estimated' if r['est'] else 'timeline'}), payoff@{r['payoff_at']}s, re-hooks {r['rehooks']}")
            for c in r["chapters"]:
                print(f"   {c[1] // 60}:{c[1] % 60:02d} {c[0]}")
            for f in r["fails"] + r["warns"]:
                print(f"   - {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
