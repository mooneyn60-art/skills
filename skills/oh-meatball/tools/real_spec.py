#!/usr/bin/env python3
"""Build a realcut.py spec from an outline, its voice timings (real_voice.py) and a shot plan.

    python3 real_spec.py <slug>          reads scripts/real/<slug>.yaml, episodes/real/vo/<slug>.wav.json,
                                         scripts/real/<slug>.shots.json and footage/<slug>/credits.json;
                                         writes scripts/real/<slug>.spec.json
Shot plan: one entry per narration line (5 lines + the end line), each {"clip", "in", "focus", "zoom", "big", "bubble_at"};
dur and say come from the voice file, so every shot lasts exactly as long as its line.
"""
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main(slug):
    o = yaml.safe_load(open(f"{ROOT}/scripts/real/{slug}.yaml"))
    vo = json.load(open(f"{ROOT}/episodes/real/vo/{slug}.wav.json"))
    plan = json.load(open(f"{ROOT}/scripts/real/{slug}.shots.json"))
    credits = json.load(open(f"{ROOT}/footage/{slug}/credits.json"))
    if len(plan) != len(vo):
        sys.exit(f"{slug}: {len(plan)} shots for {len(vo)} narration lines")
    shots = []
    for p, v in zip(plan, vo):
        s = {"clip": f"../../footage/{slug}/{p['clip']}", "in": p.get("in", 0), "dur": v["dur"], "say": v["say"],
             "zoom": p.get("zoom", "in"), "focus": p.get("focus", [0.5, 0.5])}
        for k in ("big", "bubble_at"):
            if k in p:
                s[k] = p[k]
        shots.append(s)
    spec = {"banner": f"{o['series'].upper()} #{o['part']}", "voice": f"../../episodes/real/vo/{slug}.wav",
            "bubble": "../../brand/real/meatball_shock_bubble.png", "shots": shots, "credits": [c["credit"] for c in credits]}
    out = f"{ROOT}/scripts/real/{slug}.spec.json"
    json.dump(spec, open(out, "w"), indent=1)
    print(f"wrote {out} ({sum(s['dur'] for s in shots):.2f} s)")


if __name__ == "__main__":
    main(sys.argv[1])
