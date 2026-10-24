#!/usr/bin/env python3
"""
Fetch the daily series used by paper/test_options_vs_spy.py and write
paper/history/options_indices.json as {series: {YYYY-MM-DD: value}}.

  PUT, BXM, BXMD, SPX, VIX  CBOE daily index history
                            cdn.cboe.com/api/global/us_indices/daily_prices/
  SPTR                      S&P 500 total return (^SP500TR), Yahoo chart API
  DTB3                      3-month T-bill, percent, FRED

Usage: python3 paper/fetch_options_indices.py
"""
import csv, io, json, os, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "history", "options_indices.json")
UA = {"User-Agent": "Mozilla/5.0 (TARS research script)"}
CBOE = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{}_History.csv"
YAHOO = ("https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR"
         "?period1=473385600&period2=4102444800&interval=1d")
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3&cosd=1985-01-01"


def get(url, headers=UA):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                return r.read().decode()
        except Exception:
            if attempt == 2:
                raise


def cboe(sym):
    out = {}
    rows = list(csv.reader(io.StringIO(get(CBOE.format(sym)))))
    head = [h.strip().upper() for h in rows[0]]
    col = head.index("CLOSE") if "CLOSE" in head else 1
    for r in rows[1:]:
        if len(r) <= col or not r[col].strip():
            continue
        d = datetime.strptime(r[0].strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
        out[d] = float(r[col])
    return out


def main():
    data = {s: cboe(s) for s in ("PUT", "BXM", "BXMD", "SPX", "VIX")}
    y = json.loads(get(YAHOO))["chart"]["result"][0]
    closes = y["indicators"]["quote"][0]["close"]
    data["SPTR"] = {datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d"): c
                    for t, c in zip(y["timestamp"], closes) if c is not None}
    data["DTB3"] = {}
    for r in list(csv.reader(io.StringIO(get(FRED, headers={}))))[1:]:
        if r[1] not in ("", "."):
            data["DTB3"][r[0]] = float(r[1])
    for k, v in data.items():
        ks = sorted(v)
        print(f"{k:<5} {len(ks):>6} days  {ks[0]} -> {ks[-1]}")
    json.dump({"_fetched": datetime.now(timezone.utc).date().isoformat(), "series": data},
              open(OUT, "w"))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
