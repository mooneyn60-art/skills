#!/usr/bin/env python3
"""
Build 20 years of earnings-release dates from SEC EDGAR 8-K filings whose items
include 2.02 (Results of Operations and Financial Condition).
Source: data.sec.gov/submissions/CIK##########.json plus its older pages.
Timing from the filing's acceptance time (US Eastern):
  before 09:30 -> "am"; 09:30-15:59 -> "during" (treated like am); 16:00+ -> "pm".
Writes paper/history/earnings_8k.json. Generic User-Agent (no personal details).
Usage: python3 paper/fetch_earnings_8k.py
"""
import json, os, time, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "history", "earnings_8k.json")
UA = "TARS research script (personal non-commercial use)"
NY = ZoneInfo("America/New_York")
CIKS = {
    "AAPL": [320193], "AMZN": [1018724], "BAC": [70858], "C": [831001],
    "CSCO": [858877], "F": [37996], "GE": [40545], "GOOGL": [1288776, 1652044],
    "IBM": [51143], "MSFT": [789019], "NVDA": [1045810], "PFE": [78003],
    "T": [732717], "XOM": [34088, 2115436],
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        time.sleep(0.15)
        return json.load(r)


def rows(block):
    keys = ("form", "filingDate", "acceptanceDateTime", "items")
    n = len(block.get("form", []))
    for i in range(n):
        yield {k: block.get(k, [""] * n)[i] for k in keys}


def main():
    out = {"_source": "SEC EDGAR submissions, 8-K with item 2.02; timing from acceptanceDateTime (ET)",
           "_fetched": datetime.now(NY).date().isoformat()}
    for sym, ciks in CIKS.items():
        ev = {}
        for cik in ciks:
            sub = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
            blocks = [sub["filings"]["recent"]] + [get(f"https://data.sec.gov/submissions/{f['name']}")
                                                   for f in sub["filings"].get("files", [])]
            for b in blocks:
                for r in rows(b):
                    if r["form"] not in ("8-K", "8-K/A") or "2.02" not in str(r["items"]):
                        continue
                    if r["form"] == "8-K/A":
                        continue
                    acc = datetime.fromisoformat(r["acceptanceDateTime"].replace("Z", "+00:00")).astimezone(NY)
                    d = acc.date().isoformat()
                    if d < "2005-06-01":
                        continue
                    m = acc.hour * 60 + acc.minute
                    timing = "am" if m < 570 else ("pm" if m >= 960 else "during")
                    ev.setdefault(d, dict(date=d, timing=timing, accepted=acc.strftime("%H:%M")))
        out[sym] = [ev[k] for k in sorted(ev)]
        print(f"{sym}: {len(out[sym])} item-2.02 8-Ks, {out[sym][0]['date'] if out[sym] else '-'} .. "
              f"{out[sym][-1]['date'] if out[sym] else '-'}; timing "
              f"am {sum(e['timing']=='am' for e in out[sym])} / during {sum(e['timing']=='during' for e in out[sym])} / "
              f"pm {sum(e['timing']=='pm' for e in out[sym])}")
    json.dump(out, open(OUT, "w"), indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
