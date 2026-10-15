"""Builds dashboard.html from farm_output.json, paper_book.json and spy_1min.json.
Run datafarm.py (backtest) and paper_trader.py (forward book) first."""
import json
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import datafarm as farm  # noqa: E402
f = json.load(open(here / "farm_output.json"))
book = json.load(open(here / "paper_book.json")) if (here / "paper_book.json").exists() else {"trades": []}
days = farm.load()
bars = {}
for d, bs in days.items():
    farm.add_indicators(bs)
    bars[d] = [[round(b["h"], 2), round(b["l"], 2), round(b["c"], 2), round(b["vwap"], 2), round(b["ema9"], 2),
                round(b["ema21"], 2), round(b["rsi"], 1)] for b in bs]
data = {k: f[k] for k in ("range", "n_days", "events", "setups", "trades", "per_day")}
data["bars"] = bars
data["candles"] = sum(len(v) for d, v in bars.items() if f["range"][0] <= d <= f["range"][1])
data["paper"] = book
html = (here / "dashboard_template.html").read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
(here / "dashboard.html").write_text(html)
print("wrote", here / "dashboard.html", len(html))
