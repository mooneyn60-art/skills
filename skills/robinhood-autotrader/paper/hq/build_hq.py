"""Builds hq.build.html (TARS Town) from hq.html + repo state (research, paper book, options slot, journal).
Live account data is fetched by the page itself through the Robinhood connector."""
import json, re, hashlib
from pathlib import Path
here = Path(__file__).resolve().parent; root = here.parent.parent
mem = (root / "research/SWARM_MEMORY.md").read_text()
entries = re.findall(r"^## (\d{4}-\d\d-\d\d) — (.+?)\n((?:- .+\n?)+)", mem, re.M)
lab = {"studies": len(list((root / "research").glob("20*.md"))),
       "latest": [{"date": d, "title": t.strip(), "points": [p[2:].strip() for p in b.strip().split("\n")][:3]} for d, t, b in entries[-4:]][::-1]}
book = json.load(open(root / "paper/datafarm/paper_book.json"))
tr = book.get("trades", [])
farm = {"equity": book["equity"], "start": book["start_equity"], "trades": len(tr), "as_of": book.get("as_of"), "rules_hash": book.get("rules_hash")}
slot = json.load(open(root / "paper/live_options/state.json"))
slot["rules_hash"] = hashlib.sha256((root / "routines/TARS_OPTIONS_LIVE.md").read_bytes()).hexdigest()[:16]
jdir = root / "paper/journal"
journal = {"days": sum(1 for f in jdir.glob("*.jsonl") for _ in open(f)) if jdir.exists() else 0}
data = {"lab": lab, "farm": farm, "slot": slot, "journal": journal}
html = (here / "hq.html").read_text().replace("__STATIC__", json.dumps(data))
(here / "hq.build.html").write_text(html)
print(json.dumps(data)[:400])
