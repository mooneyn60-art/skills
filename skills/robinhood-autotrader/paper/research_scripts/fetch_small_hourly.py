"""Hourly candles (~2y) for small/meme coins on Coinbase, for the small-coin flip test. Saved to paper/history/crypto/<coin>_hourly.json."""
import json, datetime as dt
from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location("fc", Path(__file__).with_name("fetch_crypto.py"))
src = open(Path(__file__).with_name("fetch_crypto.py")).read().split("for pid, since in")[0]
ns = {"__file__": str(Path(__file__).with_name("fetch_crypto.py"))}; exec(src, ns)
OUT = ns["OUT"]
for pid in ("DOGE-USD", "SHIB-USD", "PEPE-USD", "BONK-USD", "WIF-USD", "SOL-USD", "AVAX-USD", "XRP-USD"):
    d = ns["fetch"](pid, 3600, dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=2 * 365))
    if d: json.dump(d, open(OUT / f"{pid.split('-')[0].lower()}_hourly.json", "w"))
    print(pid, len(d), min(d) if d else "-", max(d) if d else "-")
