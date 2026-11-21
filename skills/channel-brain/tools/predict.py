#!/usr/bin/env python3
"""The town's prediction ledger and calibration (how TARS checks its own judgement).
Before a decision or experiment goes live, write down how likely it is to work. Later, settle it. Monthly, see whether
"70% sure" really comes true 70% of the time. A town whose 80% calls hit 40% should slow down and test more.
  predict.py add E19 "Case Shorts reach >= v4 animal median subs/1k at 48 h" 0.4 2026-10-29
  predict.py settle E19 1 "cases 1.1 subs/1k vs 0.2"      (1 = it happened, 0 = it didn't)
  predict.py report
File: data/predictions.jsonl (path from env PREDICTIONS or ../../data/predictions.jsonl next to this tool's brain folder)."""
import json, os, sys, datetime as dt
P = os.environ.get("PREDICTIONS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "predictions.jsonl")
rows = [json.loads(l) for l in open(P)] if os.path.exists(P) else []
cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
if cmd == "add":
    _, _, pid, what, p, settles = sys.argv[:6]
    if any(r["id"] == pid for r in rows):
        sys.exit(f"{pid} already exists; use a new id")
    rows.append(dict(id=pid, made=dt.date.today().isoformat(), what=what, p=float(p), settles=settles, hit=None))
elif cmd == "settle":
    pid, hit, note = sys.argv[2], int(sys.argv[3]), " ".join(sys.argv[4:])
    for r in rows:
        if r["id"] == pid:
            r.update(hit=hit, brier=round((r["p"] - hit) ** 2, 4), note=note, settled=dt.date.today().isoformat())
            break
    else:
        sys.exit(f"no prediction {pid}")
if cmd in ("add", "settle"):
    os.makedirs(os.path.dirname(P), exist_ok=True)
    with open(P, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
done = [r for r in rows if r.get("hit") in (0, 1)]
print(f"{len(rows)} predictions, {len(done)} settled")
for lo, hi, lab in ((0, .35, "<35%"), (.35, .5, "35-50%"), (.5, .65, "50-65%"), (.65, .8, "65-80%"), (.8, 1.01, "80%+")):
    b = [r for r in done if lo <= r["p"] < hi]
    if b:
        print(f"  said {lab:7s} n {len(b):2d}: said {sum(r['p'] for r in b) / len(b):.0%} on average, came true {sum(r['hit'] for r in b) / len(b):.0%}")
if done:
    brier = sum((r["p"] - r["hit"]) ** 2 for r in done) / len(done)
    print(f"Brier {brier:.3f} (coin flip 0.250; lower is better)" + ("  - too few to judge yet (<20)" if len(done) < 20 else ""))
