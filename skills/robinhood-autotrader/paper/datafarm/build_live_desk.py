"""Fills the backtest records into live_desk.html -> live_desk.build.html (publish that)."""
import json
from pathlib import Path
here = Path(__file__).resolve().parent
rec = {k: {"n": v.get("n", 0), "win": v.get("win"), "avgR": v.get("avgR")}
       for k, v in json.load(open(here / "farm_output.json"))["setups"].items() if v.get("n")}
html = (here / "live_desk.html").read_text().replace("__RECORD__", json.dumps(rec))
(here / "live_desk.build.html").write_text(html)
print(rec)
