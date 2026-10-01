#!/usr/bin/env python3
"""
Agenda item 16: how much of each held name's daily variance is market,
sector, and company-specific, and how often large company-specific moves
coincide with an SEC filing. Prints data only (R14.1).
Design and prediction: research/2026-09-24_WHY_PRICES_MOVE.md.

Data (fetched once, cached to paper/history/book_daily.json):
  adjusted daily closes, Yahoo Finance chart API, 3 years
  filing dates (8-K / 6-K), SEC EDGAR submissions API
Usage: python3 paper/test_why_prices_move.py [--refresh]
"""
import json, math, os, sys, time, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "history", "book_daily.json")
BOOK = {  # name: (sector ETF, SEC filer ID)
    "NVDA": ("SMH", 1045810), "INTC": ("SMH", 50863),
    "SOFI": ("XLF", 1818874), "NWG": ("XLF", 844150),
    "CVE": ("XLE", 1475260), "ABBV": ("XLV", 1551152),
    "EXEL": ("XBI", 939767),
}
UA = {"User-Agent": "TARS research script (personal non-commercial use)"}


def get(url):
    for a in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read().decode()
        except Exception:
            if a == 2:
                raise
            time.sleep(2)


def fetch():
    out = {"_fetched": datetime.now(timezone.utc).date().isoformat(), "prices": {}, "filings": {}}
    syms = set(BOOK) | {s for s, _ in BOOK.values()} | {"SPY"}
    for s in sorted(syms):
        y = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=3y&interval=1d"))
        res = y["chart"]["result"][0]
        adj = res["indicators"]["adjclose"][0]["adjclose"]
        out["prices"][s] = {datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d"): c
                            for t, c in zip(res["timestamp"], adj) if c is not None}
    for s, (_, cik) in BOOK.items():
        sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))["filings"]["recent"]
        out["filings"][s] = sorted({d for f, d in zip(sub["form"], sub["filingDate"])
                                    if f in ("8-K", "6-K")})
        time.sleep(0.3)
    json.dump(out, open(CACHE, "w"))
    return out


def ols_r2(y, xs):
    """R-squared of y on columns xs (with intercept), via normal equations."""
    n, k = len(y), len(xs) + 1
    X = [[1.0] + [c[i] for c in xs] for i in range(n)]
    A = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    v = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    for c in range(k):  # Gauss-Jordan
        p = max(range(c, k), key=lambda r: abs(A[r][c]))
        A[c], A[p], v[c], v[p] = A[p], A[c], v[p], v[c]
        for r in range(k):
            if r != c:
                f = A[r][c] / A[c][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
                v[r] -= f * v[c]
    beta = [v[i] / A[i][i] for i in range(k)]
    fit = [sum(b * x for b, x in zip(beta, X[i])) for i in range(n)]
    my = sum(y) / n
    ss_res = sum((a - b) ** 2 for a, b in zip(y, fit))
    ss_tot = sum((a - my) ** 2 for a in y)
    return 1 - ss_res / ss_tot, [a - b for a, b in zip(y, fit)]


def main():
    data = fetch() if ("--refresh" in sys.argv or not os.path.exists(CACHE)) else json.load(open(CACHE))
    P, F = data["prices"], data["filings"]
    print(f"source: {os.path.basename(CACHE)} fetched {data['_fetched']} (Yahoo adjusted closes; SEC 8-K/6-K dates)")
    print(f"{'name':<5} {'sector':<5} {'days':>5} {'market':>7} {'+sector':>8} {'company':>8}  "
          f"{'>3sd moves':>10} {'w/ filing d0/d-1':>17} {'base rate':>9}")
    tot_big = tot_hit = 0
    for s, (etf, _) in BOOK.items():
        days = sorted(set(P[s]) & set(P["SPY"]) & set(P[etf]))
        r = lambda sym: [P[sym][b] / P[sym][a] - 1 for a, b in zip(days, days[1:])]
        y, m, e = r(s), r("SPY"), r(etf)
        d1 = days[1:]
        r2m, _ = ols_r2(y, [m])
        r2ms, resid = ols_r2(y, [m, e])
        sd = math.sqrt(sum(x * x for x in resid) / len(resid))
        filed = set(F[s])
        prev = {d1[i]: days[i] for i in range(len(d1))}
        near = lambda d: d in filed or prev[d] in filed
        big = [d for d, x in zip(d1, resid) if abs(x) > 3 * sd]
        hit = sum(1 for d in big if near(d))
        base = sum(1 for d in d1 if near(d)) / len(d1)
        tot_big += len(big)
        tot_hit += hit
        print(f"{s:<5} {etf:<5} {len(y):>5} {r2m * 100:6.1f}% {(r2ms - r2m) * 100:+7.1f}% "
              f"{(1 - r2ms) * 100:7.1f}%  {len(big):>10} {hit:>9} ({hit / len(big) * 100 if big else 0:4.0f}%) "
              f"{base * 100:8.1f}%")
    print(f"all names: {tot_big} moves beyond 3 sd, {tot_hit} with a filing on day 0 or -1 "
          f"({tot_hit / tot_big * 100:.0f}%)")


if __name__ == "__main__":
    main()
