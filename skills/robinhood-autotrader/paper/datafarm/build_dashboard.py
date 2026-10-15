"""Builds dashboard.html from farm_output.json + spy_1min.json (run datafarm.py first)."""
import json
from pathlib import Path
here = Path(__file__).resolve().parent
raw = json.load(open(here.parent / "history" / "spy_1min.json"))
f = json.load(open(here / "farm_output.json"))
bars = {}
for k in sorted(raw):
    d = k[:10]
    if f["range"][0] <= d <= f["range"][1]:
        o, h, l, c, v = raw[k]
        bars.setdefault(d, []).append([round(h, 2), round(l, 2), round(c, 2)])
data = {k: f[k] for k in ("range", "n_days", "events", "setups", "trades", "per_day")}
data["bars"] = bars; data["candles"] = sum(len(v) for v in bars.values())
html = (here / "dashboard_template.html").read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
(here / "dashboard.html").write_text(html)
print("wrote", here / "dashboard.html", len(html))
