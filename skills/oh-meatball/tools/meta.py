#!/usr/bin/env python3
"""Generate YouTube title/description/tags JSON from tools/templates.json.

meta.py --type doorbell|security|dashcam|phone|compilation --animal raccoon --hook "stole a package" [--n 6] [--seed 1]
"""
import argparse
import json
import os
import random
import sys

TITLE_MAX, TAGS_MAX = 70, 480
HERE = os.path.dirname(os.path.abspath(__file__))


SMALL = {"a", "an", "the", "and", "or", "of", "on", "in", "at", "to", "for", "by", "with"}


def title_case(text):
    words = text.split()
    return " ".join(w if w.isupper() and len(w) > 1 else (w.lower() if i and w.lower() in SMALL else w[:1].upper() + w[1:].lower())
                    for i, w in enumerate(words))


def fill(tpl, ctx):
    return tpl.format(**ctx).replace("  ", " ").strip()


def pick_title(templates, ctx, rng):
    options = templates[:]
    rng.shuffle(options)
    fitting = [t for t in (fill(o, ctx) for o in options) if len(t) <= TITLE_MAX]
    if fitting:
        return fitting[0]
    shortest = min((fill(o, ctx) for o in options), key=len)
    return shortest[: TITLE_MAX - 1].rstrip() + "…"


def build_tags(groups, animal):
    tags, seen, total = [], set(), 0
    extra = [animal, f"{animal} caught on camera", f"funny {animal}", f"{animal} video"] if animal else []
    for tag in extra + groups:
        key = tag.lower()
        # YouTube counts a comma separator per tag; quoted multi-word tags add 2.
        cost = len(tag) + 1 + (2 if " " in tag else 0)
        if key in seen or total + cost > TAGS_MAX:
            continue
        seen.add(key)
        tags.append(tag)
        total += cost
    return tags


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", required=True, choices=["doorbell", "security", "dashcam", "phone", "compilation"])
    ap.add_argument("--animal", default="", help="e.g. raccoon (optional for compilation)")
    ap.add_argument("--hook", default="", help="short verb phrase, e.g. 'stole a package'")
    ap.add_argument("--n", type=int, default=10, help="clip count for compilation titles")
    ap.add_argument("--seed", type=int, help="make the pick reproducible")
    ap.add_argument("--templates", default=os.path.join(HERE, "templates.json"))
    a = ap.parse_args()
    if a.type != "compilation" and not (a.animal and a.hook):
        sys.exit("meta: --animal and --hook are required unless --type compilation")
    with open(a.templates) as f:
        tpl = json.load(f)
    rng = random.Random(a.seed)
    animal = a.animal.strip().lower()
    hook = a.hook.strip().rstrip(".")
    ctx = {"animal": animal, "Animal": title_case(animal), "ANIMAL": animal.upper(),
           "hook": (hook or "went too far").lower(), "Hook": title_case(hook or "went too far"), "n": a.n}
    title = pick_title(tpl["titles"][a.type], ctx, rng)
    line1 = fill(rng.choice(tpl["description_line1"][a.type]), ctx)
    line2 = rng.choice(tpl["description_line2"])
    hs = tpl["hashtags"]["common"] + tpl["hashtags"][a.type]
    if animal:
        hs = hs[:3] + ["#" + animal.replace(" ", "")] + hs[3:]
    hashtags = list(dict.fromkeys(hs))[:7]
    tags = build_tags(tpl["tags"][a.type] + tpl["tags"]["common"], animal)
    out = {"title": title, "title_len": len(title),
           "description": f"{line1}\n{line2}\n\n{' '.join(hashtags)}",
           "tags": tags, "tags_chars": sum(len(t) + 1 + (2 if ' ' in t else 0) for t in tags)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
