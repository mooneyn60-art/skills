#!/usr/bin/env python3
"""Sameness gate for drawn outlines (YouTube "inauthentic content" bucket 1: template videos with little variation).

Compares each outline's yt/tt shot skeleton (macro order) and its wording against every other outline:
  S1 skeleton twin: exactly the same macro sequence as 3+ other outlines of the same cut
  S2 opener rut:    hook's first two words shared by 25%+ of outlines ("This animal...", "This fish...")
  S3 title rut:     title's first two words shared by 25%+ of outlines
  S4 stock line:    same non-subscribe sentence appears in 3+ outlines

Usage:
  sameness.py                       # report on every drawn outline
  sameness.py OUTLINE.yaml [...]    # gate only these (others are the comparison pool); exit 1 on S1 fail
"""
import collections
import difflib
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POOL = ["scripts/drawn-tt/outlines/*.yaml", "scripts/drawn-house/outlines/*.yaml"]
SKIP = {"hero_moves", "mb", "dur", "sfx", "music", "at"}
TWIN, TWIN_N, RUT = 1.0, 3, 0.25


def load(path):
    d = yaml.safe_load(open(path)) or {}
    out = {"path": os.path.relpath(path, ROOT), "title": d.get("title", ""), "lines": [], "seq": {}}
    for cut in ("yt", "tt"):
        seq = []
        for step in d.get(cut) or []:
            if not isinstance(step, dict):
                continue
            k = next((k for k in step if k not in SKIP), None)
            if k:
                seq.append(k)
                if isinstance(step[k], str):
                    out["lines"].append(step[k])
        out["seq"][cut] = seq
    hook = next((s["hook"] for s in d.get("yt") or [] if isinstance(s, dict) and isinstance(s.get("hook"), str)), "")
    out["hook"] = hook
    return out


def head(text, n=2):
    return " ".join(re.findall(r"[a-z']+", text.lower())[:n])


def sentences(text):
    return [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) >= 4]


def main(argv):
    pool_paths = sorted(p for g in POOL for p in glob.glob(os.path.join(ROOT, g)) if "-tiny" not in p)
    gate = [os.path.abspath(a) for a in argv]
    docs = [load(p) for p in sorted(set(pool_paths) | set(gate))]
    targets = [d for d in docs if not gate or os.path.join(ROOT, d["path"]) in gate]
    n = len(docs)
    fails = 0

    hooks = collections.Counter(head(d["hook"]) for d in docs if d["hook"])
    titles = collections.Counter(head(d["title"]) for d in docs if d["title"])
    stock = collections.Counter()
    for d in docs:
        for s in {s for line in d["lines"] for s in sentences(line)}:
            if "subscribe" not in s:
                stock[s] += 1

    for d in targets:
        notes = []
        for cut, seq in d["seq"].items():
            if len(seq) < 3:
                continue
            twins = [o["path"] for o in docs if o is not d and o["seq"].get(cut)
                     and difflib.SequenceMatcher(None, seq, o["seq"][cut]).ratio() >= TWIN]
            if len(twins) >= TWIN_N:
                fails += 1
                notes.append(f"FAIL S1 {cut} skeleton {'-'.join(seq)} matches {len(twins)} others "
                             f"(e.g. {os.path.basename(twins[0])}); reorder beats or swap a macro")
        h = head(d["hook"])
        if h and hooks[h] / n >= RUT:
            notes.append(f"WARN S2 hook opens '{h} ...' like {hooks[h]}/{n} outlines")
        t = head(d["title"])
        if t and titles[t] / n >= RUT:
            notes.append(f"WARN S3 title opens '{t} ...' like {titles[t]}/{n} outlines")
        for s in {s for line in d["lines"] for s in sentences(line)}:
            if stock.get(s, 0) >= 3:
                notes.append(f"WARN S4 stock line in {stock[s]} outlines: \"{s[:60]}\"")
        if notes or gate:
            print(d["path"])
            for x in notes or ["ok"]:
                print("  " + x)

    if not gate:
        for cut in ("yt", "tt"):
            skel = collections.Counter("-".join(d["seq"][cut]) for d in docs if d["seq"].get(cut))
            top, k = skel.most_common(1)[0]
            print(f"\n{cut}: {len(skel)} distinct skeletons across {n} outlines; most common x{k}: {top}")
        print(f"hook openers top 3: {hooks.most_common(3)}")
        print(f"title openers top 3: {titles.most_common(3)}")
    print(f"\n{fails} skeleton-twin failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
