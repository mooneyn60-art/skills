#!/usr/bin/env python3
"""
Agenda item 9: execution cost. Prints data only (R14.1).
Design and prediction: research/2026-09-27_EXECUTION_COST.md (committed first).

X1  Corwin-Schultz (2012) high-low spread estimate, 2024-09-25 onward,
    daily_stocks.json and daily_ohlcv_holdings.json.
X2  live equity fills (paper/trades.jsonl) vs the close of the Yahoo
    1-minute bar containing the fill time. Minute bars cached to
    paper/history/minute_bars_fills.json (Yahoo keeps ~30 days of 1m data).
X3  round-trip cost expressed in R at an 8% stop.
Usage: python3 paper/test_execution_cost.py [--refresh]
"""
import json, math, os, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

from engine import load, H, L, C

HERE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(HERE, "history")
CACHE = os.path.join(HIST, "minute_bars_fills.json")
UA = {"User-Agent": "Mozilla/5.0 (TARS research script)"}
START = "2024-09-25"


def cs_spread(bars):
    """Corwin-Schultz two-day estimator; negative estimates set to 0.
    bars: list of (high, low, close). Returns median spread (fraction)."""
    k = 3 - 2 * math.sqrt(2)
    out = []
    for i in range(1, len(bars)):
        h0, l0, c0 = bars[i - 1]
        h1, l1, _ = bars[i]
        if c0 < l1:  # overnight gap adjustment (Corwin-Schultz sec. 3)
            h1, l1 = h1 - (l1 - c0), c0
        elif c0 > h1:
            h1, l1 = c0, l1 + (c0 - h1)
        if min(h0, l0, h1, l1) <= 0:
            continue
        beta = math.log(h0 / l0) ** 2 + math.log(h1 / l1) ** 2
        gamma = math.log(max(h0, h1) / min(l0, l1)) ** 2
        alpha = (math.sqrt(2 * beta) - math.sqrt(beta)) / k - math.sqrt(gamma / k)
        s = 2 * (math.exp(alpha) - 1) / (1 + math.exp(alpha))
        out.append(max(s, 0.0))
    out.sort()
    return out[len(out) // 2], sum(out) / len(out), len(out)


def fills():
    rows = {}
    for line in open(os.path.join(HERE, "trades.jsonl")):
        if line.strip():
            d = json.loads(line)
            rows[d["id"].replace("-CORRECTION", "")] = d
    out = []
    for d in rows.values():
        if d.get("account") != "live" or d.get("instrument") != "equity":
            continue
        if d.get("entry") and d.get("opened"):
            out.append((d["symbol"], d["opened"], float(d["entry"]), "buy", d["id"]))
        if d.get("exit") and d.get("closed") and d.get("exit_reason") not in (None, "not_taken"):
            out.append((d["symbol"], d["closed"], float(d["exit"]), "sell", d["id"]))
    return out


def minute_bars(sym, day):
    d0 = datetime.fromisoformat(day + "T00:00:00+00:00")
    p1, p2 = int(d0.timestamp()), int((d0 + timedelta(days=1)).timestamp())
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           f"?period1={p1}&period2={p2}&interval=1m")
    for a in range(3):
        try:
            y = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
            res = y["chart"]["result"][0]
            q = res["indicators"]["quote"][0]
            return {str(t): c for t, c in zip(res.get("timestamp", []), q["close"]) if c is not None}
        except Exception:
            time.sleep(2)
    return {}


def main():
    print("=== X1 Corwin-Schultz spread estimate, daily bars from", START, "===")
    dates, bars, syms = load()
    for s in syms:
        b = [(x[H], x[L], x[C]) for d, x in zip(dates, bars[s]) if d >= START]
        med, mean, n = cs_spread(b)
        print(f"  {s:<5} median {med * 1e4:6.1f}bp  mean {mean * 1e4:6.1f}bp  days {n}  (daily_stocks.json)")
    hold = json.load(open(os.path.join(HIST, "daily_ohlcv_holdings.json")))
    for s in sorted(k for k in hold if not k.startswith("_")):
        ks = [k for k in sorted(hold[s]) if k >= START]
        b = [(hold[s][k][1], hold[s][k][2], hold[s][k][3]) for k in ks]
        med, mean, n = cs_spread(b)
        print(f"  {s:<5} median {med * 1e4:6.1f}bp  mean {mean * 1e4:6.1f}bp  days {n}  (daily_ohlcv_holdings.json)")

    print("\n=== X2 live equity fills vs the 1-minute bar close at the fill time ===")
    cache = json.load(open(CACHE)) if (os.path.exists(CACHE) and "--refresh" not in sys.argv) else {}
    fl = fills()
    got, seen = [], set()
    for sym, ts, px, side, fid in sorted(fl, key=lambda x: x[1]):
        dkey = (sym, ts[:16], side, round(px, 2))
        if dkey in seen:  # exit rows repeat their entry's price and time
            continue
        seen.add(dkey)
        t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        key = f"{sym}|{t:%Y-%m-%d}"
        if key not in cache:
            cache[key] = minute_bars(sym, f"{t:%Y-%m-%d}")
            time.sleep(0.5)
        mb = cache[key]
        if not mb:
            print(f"  {ts[:16]} {sym:<5} {side:<4} no minute data")
            continue
        minute = int(t.timestamp()) // 60 * 60
        cands = [int(k) for k in mb if int(k) <= minute]
        if not cands or minute - max(cands) > 300:
            print(f"  {ts[:16]} {sym:<5} {side:<4} fill {px:.4f}: no bar within 5 minutes (outside regular hours?)")
            continue
        ref = mb[str(max(cands))]
        cost = (px / ref - 1) * (1 if side == "buy" else -1)
        got.append((cost, sym))
        print(f"  {ts[:16]} {sym:<5} {side:<4} fill {px:.4f} minute close {ref:.4f}  cost {cost * 1e4:+7.1f}bp  {fid}")
    json.dump(cache, open(CACHE, "w"))
    if got:
        tenb_avg = [c for c, sym in got if sym == "TENB" and abs(c) > 0.01]
        print(f"  TENB rows with |cost| > 100bp (blended average entry after the 2026-09-16 top-up, "
              f"not a fill): {len(tenb_avg)}")
        for lab, vals in (("all fills", [c for c, _ in got]),
                          ("excluding the TENB average-price rows", [c for c, sym in got
                                                                      if not (sym == "TENB" and abs(c) > 0.01)])):
            s_ = sorted(vals)
            n_ = len(s_)
            m_ = sum(s_) / n_
            sd_ = math.sqrt(sum((x - m_) ** 2 for x in s_) / (n_ - 1))
            print(f"  {lab}: n={n_}  mean cost {m_ * 1e4:+.1f}bp  t={m_ / (sd_ / math.sqrt(n_)):+.2f}  "
                  f"median {s_[n_ // 2] * 1e4:+.1f}bp  median |gap| {sorted(abs(x) for x in s_)[n_ // 2] * 1e4:.1f}bp  "
                  f"90th pct |gap| {sorted(abs(x) for x in s_)[int(n_ * 0.9)] * 1e4:.1f}bp")
        got = [c for c, sym in got if not (sym == "TENB" and abs(c) > 0.01)]
        s = sorted(got)
        n = len(s)
        m = sum(s) / n
        sd = math.sqrt(sum((x - m) ** 2 for x in s) / (n - 1)) if n > 1 else float("nan")
        absmed = sorted(abs(x) for x in s)[n // 2]
        print(f"  n={n}  mean cost {m * 1e4:+.1f}bp  t={m / (sd / math.sqrt(n)):+.2f}  "
              f"median {s[n // 2] * 1e4:+.1f}bp  median |gap| {absmed * 1e4:.1f}bp")
        print("\n=== X3 round trip in R at an 8% stop ===")
        for lab, oneway in (("engine assumption 5bp", 0.0005), ("measured mean", max(m, 0.0)),
                            ("measured median |gap|", absmed)):
            print(f"  {lab:<24} one-way {oneway * 1e4:5.1f}bp  round trip {2 * oneway * 1e4:5.1f}bp  "
                  f"= {2 * oneway / 0.08:.4f}R")


if __name__ == "__main__":
    main()
