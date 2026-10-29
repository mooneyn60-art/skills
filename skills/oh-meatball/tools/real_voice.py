#!/usr/bin/env python3
"""Voice a realistic-look outline (scripts/real/<slug>.yaml) line by line with Kokoro fenrir and join the lines into
one wav. Prints each line's duration so realcut.py shot durs can match the narration.

    python3 real_voice.py scripts/real/<slug>.yaml episodes/real/vo/<slug>.wav
Writes <out>.json: [{"say": line, "dur": seconds incl. the gap}, ...]; the last entry is "Subscribe. <next>".
"""
import json
import subprocess
import sys

import yaml

import free_voice

GAP = 0.10


def main(outline, out):
    o = yaml.safe_load(open(outline))
    says = [v for item in o["yt"] for k, v in item.items() if isinstance(v, str) and k not in ("scene", "pose", "prop", "mood")]
    says.append(f"Subscribe. {o['next']}")
    rows, parts = [], []
    for s in says:
        mp3 = free_voice.make("kokoro:fenrir", s)
        d = free_voice.pv_duration(mp3) + GAP
        rows.append({"say": s, "dur": round(d, 3)})
        parts.append(mp3)
    inputs, labels = [], []
    for i, p in enumerate(parts):
        inputs += ["-i", p]
        labels.append(f"[{i}:a]aresample=24000,apad=pad_dur={GAP}[a{i}]")
    graph = ";".join(labels) + ";" + "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]", out], check=True)
    json.dump(rows, open(out + ".json", "w"), indent=1)
    for r in rows:
        print(f"{r['dur']:5.2f}  {r['say']}")
    print(f"total {sum(r['dur'] for r in rows):.2f} s")


if __name__ == "__main__":
    main(*sys.argv[1:3])
