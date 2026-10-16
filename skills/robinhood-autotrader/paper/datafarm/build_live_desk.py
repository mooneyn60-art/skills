"""Builds the TARS Trading Platform: live_desk.html -> live_desk.build.html (publish that).
Bakes in the data-farm records, the SPY driver study, the options-slot book and the research library."""
import json, datetime
from pathlib import Path
here = Path(__file__).resolve().parent; paper = here.parent; rs = paper / "research_scripts"; lo = paper / "live_options"
rec = {k: {"n": v.get("n", 0), "win": v.get("win"), "avgR": v.get("avgR")}
       for k, v in json.load(open(here / "farm_output.json"))["setups"].items() if v.get("n")}
study = json.load(open(rs / "spy_drivers.json"))
trades = [json.loads(l) for l in open(lo / "trades.jsonl") if l.strip()]
keep = ("slot_trade_no", "date", "setup", "contract", "entry", "exit", "result")
slot = {"state": json.load(open(lo / "state.json")), "trades": [{k: t.get(k) for k in keep} for t in trades], "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
research = json.load(open(rs / "research_index.json"))
html = (here / "live_desk.html").read_text()
for k, v in (("__RECORD__", rec), ("__DRIVERS_STUDY__", study), ("__SLOT__", slot), ("__RESEARCH__", research)):
    html = html.replace(k, json.dumps(v))
(here / "live_desk.build.html").write_text(html)
print("built", len(html), "bytes;", len(research), "research entries;", len(slot["trades"]), "slot trades")
