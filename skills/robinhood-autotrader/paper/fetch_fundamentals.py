#!/usr/bin/env python3
"""
Fetch point-in-time year-on-year growth for the backtest universe from SEC
EDGAR XBRL company facts, and write paper/history/fundamentals_yoy.json.

For every 10-Q / 10-K filing, and for each metric, this records the latest
period in that filing and the same period one year earlier AS REPORTED IN THE
SAME FILING, plus the filing date. Using the comparative from the same
document means later restatements never leak backwards.

Metrics:
  net_income  first tag present with both periods, in this order:
              NetIncomeLoss, NetIncomeLossAvailableToCommonStockholdersBasic,
              ProfitLoss (F and IBM switch tags partway through the history)
  revenue     first tag present with both periods, in this order:
              RevenueFromContractWithCustomerExcludingAssessedTax, Revenues,
              SalesRevenueNet, SalesRevenueGoodsNet

10-Q rows use 3-month periods (80-100 days), 10-K rows 12-month periods
(350-380 days). Amended filings (10-Q/A, 10-K/A) are skipped.

Usage: python3 paper/fetch_fundamentals.py [--cache DIR]
       --cache reads/writes raw companyfacts JSON there (default: a temp dir)
SEC asks for a descriptive User-Agent and at most 10 requests per second.
"""
import argparse, json, os, sys, tempfile, time, urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "history", "fundamentals_yoy.json")
UA = "TARS research script (personal non-commercial use)"

# Filer IDs (CIK). XOM lists two: Exxon's long-standing filer ID holds the
# history; the ticker file mapped XOM to a new entity in 2026 whose record
# holds only the latest filings. Both are read and merged.
CIKS = {
    "AAPL": [320193], "AMZN": [1018724], "BAC": [70858], "C": [831001],
    "CSCO": [858877], "F": [37996], "GE": [40545], "GOOGL": [1652044],
    "IBM": [51143], "MSFT": [789019], "NVDA": [1045810], "PFE": [78003],
    "T": [732717], "XOM": [34088, 2115436],
}
NI_TAGS = ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic", "ProfitLoss"]
REV_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
            "SalesRevenueNet", "SalesRevenueGoodsNet"]


def fetch(cik, cache):
    path = os.path.join(cache, f"CIK{cik:010d}.json")
    if not os.path.exists(path):
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
            f.write(r.read())
        time.sleep(0.25)
    return json.load(open(path))


def days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def by_filing(gaap, tag):
    """accn -> list of USD facts for this tag."""
    out = {}
    node = gaap.get(tag)
    if not node:
        return out
    for x in node["units"].get("USD", []):
        if x.get("form") not in ("10-Q", "10-K") or "start" not in x:
            continue
        out.setdefault(x["accn"], []).append(x)
    return out


def yoy(facts, form):
    lo, hi = (80, 100) if form == "10-Q" else (350, 380)
    rows = [x for x in facts if lo <= days(x["start"], x["end"]) <= hi]
    if not rows:
        return None
    cur = max(rows, key=lambda x: x["end"])
    prior = [x for x in rows if 345 <= days(x["end"], cur["end"]) <= 385]
    if not prior:
        return None
    p = max(prior, key=lambda x: x["end"])
    return {"end": cur["end"], "cur": cur["val"], "prior": p["val"]}


def first_yoy(tagmap, tags, accn, form):
    for t in tags:
        if accn in tagmap[t]:
            g = yoy(tagmap[t][accn], form)
            if g:
                return dict(g, tag=t)
    return None


def derive(gaap):
    ni = {t: by_filing(gaap, t) for t in NI_TAGS}
    rev = {t: by_filing(gaap, t) for t in REV_TAGS}
    everything = list(ni.values()) + list(rev.values())
    accns = {a for m in everything for a in m}
    rows = []
    for a in accns:
        sample = next(m[a] for m in everything if a in m)[0]
        form, filed = sample["form"], sample["filed"]
        row = {"accn": a, "form": form, "filed": filed}
        g = first_yoy(ni, NI_TAGS, a, form)
        if g:
            row["net_income"] = g
        g = first_yoy(rev, REV_TAGS, a, form)
        if g:
            row["revenue"] = g
        if row.get("net_income") or row.get("revenue"):
            rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    args = ap.parse_args()
    cache = args.cache or tempfile.mkdtemp(prefix="edgar_")
    os.makedirs(cache, exist_ok=True)

    result = {"_source": "SEC EDGAR XBRL companyfacts, data.sec.gov",
              "_fetched": date.today().isoformat(), "data": {}}
    for sym, ciks in CIKS.items():
        rows = {}
        for cik in ciks:
            gaap = fetch(cik, cache).get("facts", {}).get("us-gaap", {})
            for r in derive(gaap):
                rows[r["accn"]] = r
        rows = sorted(rows.values(), key=lambda r: r["filed"])
        result["data"][sym] = rows
        n_ni = sum(1 for r in rows if r.get("net_income"))
        n_rev = sum(1 for r in rows if r.get("revenue"))
        first = rows[0]["filed"] if rows else "-"
        print(f"{sym:<6} filings={len(rows):>3}  net_income={n_ni:>3}  revenue={n_rev:>3}  first={first}")
    json.dump(result, open(OUT, "w"), indent=0)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
