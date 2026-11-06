"""Fetch crypto candles from Coinbase Exchange's public API (300 per request, paged backward).
Daily since listing for BTC, ETH, SOL, DOGE; hourly BTC/ETH for ~3 years. Saved to paper/history/crypto/."""
import json, time, urllib.request, datetime as dt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "history" / "crypto"
def get(pid, gran, start, end):
    u = f"https://api.exchange.coinbase.com/products/{pid}/candles?granularity={gran}&start={start.isoformat()}&end={end.isoformat()}"
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "tars-research"}), timeout=30) as r: return json.load(r)
        except Exception as e: time.sleep(2 ** i)
    return []
def fetch(pid, gran, since):
    rows, end = {}, dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    while end > since:
        start = max(since, end - dt.timedelta(seconds=gran * 300))
        data = get(pid, gran, start, end)
        for t, lo, hi, op, cl, vol in data: rows[t] = [op, hi, lo, cl, vol]
        end = start; time.sleep(0.15)
        if not data and start == since: break
    return {dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d" if gran == 86400 else "%Y-%m-%dT%H:00Z"): v for t, v in sorted(rows.items())}
for pid, since in (("BTC-USD", "2015-07-20"), ("ETH-USD", "2016-05-18"), ("SOL-USD", "2021-06-17"), ("DOGE-USD", "2021-06-03")):
    d = fetch(pid, 86400, dt.datetime.fromisoformat(since).replace(tzinfo=dt.timezone.utc))
    json.dump(d, open(OUT / f"{pid.split('-')[0].lower()}_daily.json", "w")); print(pid, "daily", len(d), min(d), max(d))
for pid in ("BTC-USD", "ETH-USD"):
    d = fetch(pid, 3600, dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3 * 365))
    json.dump(d, open(OUT / f"{pid.split('-')[0].lower()}_hourly.json", "w")); print(pid, "hourly", len(d), min(d), max(d))
