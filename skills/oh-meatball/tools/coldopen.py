#!/usr/bin/env python3
"""Cold-open check: does each Short open on a SCENE, rewind, and end on a kicker? Night shift R&D 2026-10-26
(research/40, rotation b: competitor teardown of Voggle).

Why: Voggle (60.9K subs, Shorts only, cut-out characters with cartoon faces, the closest rival to Meatball in the
weird-history niche) has 27 Shorts with a 27K median; its top 5 did 2.7M, 1.44M, 846K, 374K and 350K. All 5 open
on the most physical moment of the story, mid-action, in the past tense, with no topic label and no verdict:
  "The axe cut off the rooster's head, but as it dropped into the dirt..."      (Mike, 2.7M, 363x)
  "They took a slug into the trenches and put the sloppy little slime ball on lookout." (1.44M, 530x)
  "The horse tapped out the answer to each maths problem with his hoof..."      (846K, 186x)
  "30 men sprinted back and forth across the deck of the brand new warship..."  (374K, 40x)
  "The trains smashed head-on at full speed, and both boilers exploded..."      (350K, 8.8x)
then rewind ("See, in 1896...") at 0:09-0:22, and end on an ironic kicker with no CTA ("...killed his golden
goose"; "they quietly hired him back"). Our 6 weird-pilot hooks open on a label or a verdict instead
("Ships vanish in the Bermuda Triangle. Supposedly."; "The Roswell cover-up was real.").

Rules, per myth group (the beats sharing one "myth"; "intro"/"outro" skipped):
  C1 scene   the first sentence of the first beat is a scene: it has a past-tense verb, and no "?", no verdict or
             stance word (real, true, fake, wrong, supposedly, seriously, myth, cover-up, never, always...), no
             date-first opening ("In 1518," / "1945:"), and no "stamp" on that beat. FAIL for 45 s+ groups (every Voggle hit is 86-173 s),
             WARN for shorter ones: research/38 found claim-first wins at 20-25 s, so short Shorts are only
             counted, not blocked. "cold_open": "claim" on the first beat marks a deliberate claim-first open.
  C2 rewind  a rewind cue ("See,", "Opening the file", "in 1958", "years earlier", "it started", "back in")
             starts at 5-40% of the spoken words. FAIL for 45 s+ groups, WARN for shorter ones.
  C3 kicker  the last spoken beat that is not an ask line (Subscribe / Comment / "guess right") has
             "kicker": true. FAIL for 45 s+ groups, WARN for shorter ones.
Length is estimated from spoken words at 2.9 words/s (Andrew +0%, atempo 1.10; same basis as openloop.py).

Usage:  coldopen.py SCRIPT.json [...] [--json]     exit 1 when any group fails
Import: coldopen.check(spec) -> list of per-myth reports.
"""
import json
import re
import sys
from collections import OrderedDict

WPS = 2.9
LONG_S = 45
STANCE = re.compile(r"\b(?:real|really|true|truth|fake|false|wrong|supposedly|seriously|myth|myths|conspiracy|"
                    r"cover-?up|busted|proven|hoax|never|always|everyone thinks|actually)\b", re.I)
DATE_FIRST = re.compile(r"^\s*(?:in\s+)?(?:the\s+)?\d{3,4}s?\b", re.I)
IRREGULAR = ("went came took saw ran fell flew sank shot struck broke threw drove rode wrote spoke began stood "
             "sat held hit cut got gave made found heard told left lost won built caught dug fought hung kept "
             "led put shook slid split stole swam swung tore woke burst blew drew froze rose bit chose")
PAST = re.compile(r"\b(?:\w{2,}ed|" + "|".join(IRREGULAR.split()) + r")\b", re.I)
REWIND = re.compile(r"\bsee,|\bopening the file\b|\bin \d{4}\b|\byears (?:earlier|before|ago)\b|"
                    r"\bit (?:all )?started\b|\bback in\b|\bit began\b", re.I)
COPULA_ADJ = re.compile(r"\b(?:is|are|am|be|been|being|looks?|seems?|gets?)\s+\w+ed\b", re.I)  # "is armored"
ASK = re.compile(r"\bsubscribe\b|\bcomment\b|\bguess right\b|\bfollow\b", re.I)


ADJ_ED = set("barbed armored armoured banded spotted striped horned winged legged toed eyed haired shaped sized "
             "colored coloured named called cleared based related feathered scaled hooded crested hundred red bed seed speed need shed".split())


def has_past(s):
    s = COPULA_ADJ.sub(" ", s)
    for m in PAST.finditer(s):
        w = m.group(0).lower()
        if w in ADJ_ED or (m.start() and s[m.start() - 1] == "-"):
            continue  # "barbed wire", "FDA-cleared": adjectives, not actions
        return True
    return False


def words(b):
    return len(re.findall(r"[\w'.,-]+", b.get("say", "")))


def first_sentence(text):
    m = re.match(r"(.+?[.!?])(?:\s|$)", text.strip())
    return (m.group(1) if m else text).strip()


def groups(spec):
    g = OrderedDict()
    for b in spec.get("beats", []):
        if b.get("myth") in (None, "intro", "outro"):
            continue
        g.setdefault(b["myth"], []).append(b)
    return g


def scene_problems(beat):
    s = first_sentence(beat.get("say", ""))
    out = []
    if not has_past(s):
        out.append("no past-tense action verb")
    if "?" in s:
        out.append("opens on a question")
    m = STANCE.search(beat.get("say", ""))
    if m:
        out.append("verdict/stance word %r" % m.group(0))
    if DATE_FIRST.search(s):
        out.append("date-first opening")
    if beat.get("stamp"):
        out.append("verdict stamp on the hook beat")
    return s, out


def check_myth(name, beats):
    total = sum(words(b) for b in beats) or 1
    est = total / WPS
    long_ = est >= LONG_S
    starts, acc = [], 0
    for b in beats:
        starts.append(acc / total)
        acc += words(b)
    fails, warns = [], []
    line1, probs = scene_problems(beats[0])
    claim_ok = beats[0].get("cold_open") == "claim"
    if probs and not claim_ok:
        (fails if long_ else warns).append("C1 line 1 is not a scene (%s): %r" % ("; ".join(probs), line1))
    elif probs and claim_ok:
        warns.append("C1 claim-first by choice (cold_open: claim): %r" % line1)
    rew = [starts[i] for i, b in enumerate(beats) if i and REWIND.search(b.get("say", ""))]
    if not any(0.05 <= r <= 0.40 for r in rew):
        (fails if long_ else warns).append("C2 no rewind cue at 5-40%% of the words (found at %s)"
                                           % ([f"{r:.0%}" for r in rew] or "none"))
    spoken = [b for b in beats if b.get("say") and not ASK.search(b["say"])]
    if not (spoken and spoken[-1].get("kicker")):
        (fails if long_ else warns).append("C3 last story line has no \"kicker\": true (%r)"
                                           % (spoken[-1]["say"] if spoken else ""))
    return {"myth": name, "beats": len(beats), "words": total, "est_s": round(est, 1), "line1": line1,
            "scene": not probs, "fails": fails, "warns": warns}


def check(spec):
    return [check_myth(m, bs) for m, bs in groups(spec).items()]


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
        return 1 if bad else 0
    for p, reps in out.items():
        n = sum(r["scene"] for r in reps)
        print(f"## {p}: {len(reps)} group(s), scene-first {n}/{len(reps)}")
        for r in reps:
            st = "FAIL" if r["fails"] else "ok"
            print(f"  {st:4} {r['myth']:16} ~{r['est_s']:.0f}s  {r['line1'][:70]!r}")
            for f in r["fails"] + r["warns"]:
                print(f"       - {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
