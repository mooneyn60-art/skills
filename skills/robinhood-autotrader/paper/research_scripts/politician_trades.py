#!/usr/bin/env python3
"""
Wednesday probe 2026-11-18: do disclosed congressional trades predict 21-day
excess returns a copier could capture? Prints data only (R14.1).
Design and prediction: research/2026-11-18_POLITICIAN_TRADES.md (committed first).
Data: paper/history/politician_trades.json (Tip Ranks via Robinhood; hand-transcribed
by a worker, MSFT 25/25 and NVDA 20/20 rows verified against raw pulls), daily_ohlcv*.json.
Usage: python3 paper/research_scripts/politician_trades.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(HERE, "..", "history")
MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
px = {}
for f in ("daily_ohlcv.json", "daily_ohlcv_volatile.json", "daily_ohlcv_holdings.json"):
    for s, rows in json.load(open(os.path.join(H, f))).items():
        px.setdefault(s, rows)
spy = px["SPY"]
dates = sorted(spy)
pt = json.load(open(os.path.join(H, "politician_trades.json")))
HOR = 21


def excess(sym, d):
    """21-day return of sym minus SPY, entering at the close of the first trading day AFTER d."""
    i = next((k for k, x in enumerate(dates) if x > d), None)
    if i is None or i + HOR >= len(dates):
        return None
    a, b = dates[i], dates[i + HOR]
    if a not in px[sym] or b not in px[sym]:
        return None
    return (px[sym][b][3] / px[sym][a][3] - 1) - (spy[b][3] / spy[a][3] - 1)


rows = []
for s, trades in pt.items():
    if s.startswith("_") or s not in px:
        continue
    for t in trades:
        if t["transaction_type"] not in ("BUY", "SELL"):
            continue
        rows.append(dict(s=s, side=t["transaction_type"], amt=t["amount_min"], party=t["party"],
                         dd=t["disclosure_date"], td=t["transaction_date"],
                         x_disc=excess(s, t["disclosure_date"]), x_tx=excess(s, t["transaction_date"])))


def mt(v):
    n = len(v)
    if n < 2:
        return float("nan"), float("nan"), n
    m = sum(v) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1))
    return m, m / (sd / math.sqrt(n)), n


def diff(label, R, key):
    b = [r[key] for r in R if r["side"] == "BUY" and r[key] is not None]
    s = [r[key] for r in R if r["side"] == "SELL" and r[key] is not None]
    mb, tb, nb = mt(b); ms, ts, ns = mt(s)
    if nb < 2 or ns < 2:
        print(f"  {label:<36} BUY n={nb} SELL n={ns} (too few)")
        return
    vb = sum((x - mb) ** 2 for x in b) / (nb - 1); vs = sum((x - ms) ** 2 for x in s) / (ns - 1)
    t = (mb - ms) / math.sqrt(vb / nb + vs / ns)
    print(f"  {label:<36} BUY n={nb:>3} {mb * 100:+.2f}% (t {tb:+.2f}) | SELL n={ns:>3} {ms * 100:+.2f}% (t {ts:+.2f}) | "
          f"BUY-SELL {(mb - ms) * 100:+.2f}pp Welch t={t:+.2f}")


usable = [r for r in rows if r["x_disc"] is not None]
print(f"source: politician_trades.json; {len(rows)} BUY/SELL trades on names with prices; "
      f"{len(usable)} with a full {HOR}-day window after disclosure (prices end {dates[-1]})")
print(f"disclosure dates {min(r['dd'] for r in usable)} .. {max(r['dd'] for r in usable)}; "
      f"median lag {sorted((int(r['dd'][:4])*372+int(r['dd'][5:7])*31+int(r['dd'][8:])) - (int(r['td'][:4])*372+int(r['td'][5:7])*31+int(r['td'][8:])) for r in usable)[len(usable)//2]} days (approx)")
print("\n21-day excess vs SPY, entering after DISCLOSURE (what a copier gets):")
diff("all", rows, "x_disc")
mid = sorted(r["dd"] for r in usable)[len(usable) // 2]
diff("1st half (disclosed before " + mid + ")", [r for r in rows if r["dd"] < mid], "x_disc")
diff("2nd half", [r for r in rows if r["dd"] >= mid], "x_disc")
diff("amount > $15k", [r for r in rows if r["amt"] > 15000], "x_disc")
diff("amount $1k-15k", [r for r in rows if r["amt"] <= 15000], "x_disc")
diff("Democrats", [r for r in rows if r["party"] == "DEMOCRAT"], "x_disc")
diff("Republicans", [r for r in rows if r["party"] == "REPUBLICAN"], "x_disc")
diff("megacaps", [r for r in rows if r["s"] in MEGA], "x_disc")
diff("non-megacaps", [r for r in rows if r["s"] not in MEGA], "x_disc")
print("\n21-day excess vs SPY, entering after the TRANSACTION date (not tradeable; what they got):")
diff("all", rows, "x_tx")
print("\nevents per symbol (usable):", ", ".join(f"{s} {sum(1 for r in usable if r['s'] == s)}"
                                            for s in sorted({r['s'] for r in usable})))
