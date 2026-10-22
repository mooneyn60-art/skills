#!/usr/bin/env python3
"""Split an episode beats JSON into one Short script per myth (beats tagged with "myth").

Usage: shorts_split.py EPISODE.json OUTDIR   -> OUTDIR/<myth>.json for every myth except intro/outro
Each Short opens on the myth's own quiz beat and ends on a card pointing to the full episode.
"""
import json
import os
import sys

# Ends on a comment prompt (drives the engagement the Shorts feed rewards), then points to the episode.
END = {"say": "Did you guess right? Comment true or false, and the full quiz is on the channel.", "pose": "wave",
       "text": "COMMENT:\nDID YOU GUESS\nRIGHT?"}


def main():
    ep, out = json.load(open(sys.argv[1])), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    groups = {}
    for b in ep["beats"]:
        groups.setdefault(b.get("myth", "misc"), []).append(b)
    for name, beats in groups.items():
        if name in ("intro", "outro", "misc"):
            continue
        json.dump({"voice": ep.get("voice", "en-US-AndrewNeural"), "beats": beats + [END]},
                  open(f"{out}/{name}.json", "w"), indent=1, ensure_ascii=False)
        print(name, len(beats) + 1)


if __name__ == "__main__":
    main()
