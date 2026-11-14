"""
TARS Data Farm: an event detector + backtest engine for intraday SPY setups,
modelled on the "LIT // DATA FARM" idea Nolan shared (2026-10-15).

What it does, per trading day of SPY 1-minute bars:
  1. Detects market-structure EVENTS: prior-day high/low (PDH/PDL), opening
     range (first 15 min) high/low, swing highs/lows (5-bar fractals),
     liquidity SWEEPS (pierce a level, close back inside within 2 bars),
     fair value gaps (FVG: 3-bar gap after an impulse), structure breaks.
  2. Runs SETUPS off those events with a fixed stop, a 2R target and a
     15:55 time exit, one position at a time per setup.
  3. Writes the OUTCOME BOOK (every trade, every field) and the event counts
     to paper/datafarm/farm_output.json for the dashboard, and prints DATA
     only (R14): n, win rate, profit factor, average R, by half and by week.

Costs: each trade is charged 1 cent per share each way on SPY stock, and the
script also reports what the same move would make as an ATM 0DTE option
(delta 0.5, 1% of premium spread each way) so the result is comparable to
how Nolan actually trades.

Honest limits: about 30 real trading days of minute bars (2026-09-02 ..
2026-10-14); Robinhood returned filler for earlier dates. Everything here is
IN-SAMPLE for those days. The video's numbers had no costs, no sample size
beyond 142 trades and no out-of-sample test; this script does show all three.
"""
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "history" / "spy_1min.json"
OUT = Path(__file__).resolve().parent / "farm_output.json"

SWEEP_MIN = 0.0003        # pierce a level by >= 0.03% (~$0.23 on SPY 775)
FVG_MIN = 0.0004          # gap >= 0.04% of price
STOP_PAD = 0.0002         # stop beyond the sweep extreme / gap edge
TARGET_R = 2.0
SETUPS = ["sweep_reversal", "fvg_retest", "sweep_fvg", "fvg_trend", "vwap_reclaim"]
LAST_ENTRY = "15:30"      # ET
TIME_EXIT = "15:55"       # ET
COST_PER_SHARE = 0.02     # round trip, dollars
OPT_SPREAD = 0.02         # 1% of premium each way, as a fraction
SPY_IV = 0.16             # for the ATM 0DTE premium estimate


def et(utc_key):
    h, m = int(utc_key[11:13]), int(utc_key[14:16])
    h -= 4  # EDT
    return f"{h:02d}:{m:02d}"


def load():
    raw = json.load(open(DATA))
    days = defaultdict(list)
    for k in sorted(raw):
        o, h, l, c, v = raw[k]
        days[k[:10]].append({"t": et(k), "o": o, "h": h, "l": l, "c": c, "v": v})
    return dict(sorted(days.items()))


def add_indicators(bars):
    """VWAP, EMA9, EMA21, RSI14 (Wilder), ATR14 on 1-minute bars, in place."""
    pv = vol = 0.0
    e9 = e21 = None
    gain = loss = None
    atr = None
    for i, b in enumerate(bars):
        tp = (b["h"] + b["l"] + b["c"]) / 3
        v = max(b.get("v", 0), 1)
        pv += tp * v; vol += v
        b["vwap"] = pv / vol
        e9 = b["c"] if e9 is None else e9 + (2 / 10) * (b["c"] - e9)
        e21 = b["c"] if e21 is None else e21 + (2 / 22) * (b["c"] - e21)
        b["ema9"], b["ema21"] = e9, e21
        if i:
            ch = b["c"] - bars[i - 1]["c"]
            g, l = max(ch, 0), max(-ch, 0)
            gain = g if gain is None else (gain * 13 + g) / 14
            loss = l if loss is None else (loss * 13 + l) / 14
            tr = max(b["h"] - b["l"], abs(b["h"] - bars[i - 1]["c"]), abs(b["l"] - bars[i - 1]["c"]))
        else:
            tr = b["h"] - b["l"]
        atr = tr if atr is None else (atr * 13 + tr) / 14
        b["atr"] = atr
        b["rsi"] = 50.0 if not loss else 100 - 100 / (1 + (gain or 0) / loss)
    return bars


def trend_of(b):
    """+1 up, -1 down, 0 mixed: price vs VWAP and EMA9 vs EMA21 must agree."""
    if b["c"] > b["vwap"] and b["ema9"] > b["ema21"]:
        return 1
    if b["c"] < b["vwap"] and b["ema9"] < b["ema21"]:
        return -1
    return 0


def detect(bars, pdh, pdl):
    """Return list of events (dicts) for one day."""
    ev = []
    orh = max(b["h"] for b in bars[:15]); orl = min(b["l"] for b in bars[:15])
    levels = [("PDH", pdh, "high"), ("PDL", pdl, "low"), ("ORH", orh, "high"), ("ORL", orl, "low")]
    swings_hi, swings_lo = [], []
    last_swing_hi = last_swing_lo = None
    for i, b in enumerate(bars):
        # swing points (confirmed 2 bars later)
        if 4 <= i:
            j = i - 2
            w = bars[j - 2:j + 3]
            if bars[j]["h"] == max(x["h"] for x in w):
                swings_hi.append((j, bars[j]["h"])); last_swing_hi = bars[j]["h"]
                ev.append({"i": j, "t": bars[j]["t"], "type": "swing_high", "px": bars[j]["h"]})
            if bars[j]["l"] == min(x["l"] for x in w):
                swings_lo.append((j, bars[j]["l"])); last_swing_lo = bars[j]["l"]
                ev.append({"i": j, "t": bars[j]["t"], "type": "swing_low", "px": bars[j]["l"]})
        # structure break
        if last_swing_hi and b["c"] > last_swing_hi and bars[i - 1]["c"] <= last_swing_hi:
            ev.append({"i": i, "t": b["t"], "type": "structure_break", "side": "up", "px": last_swing_hi})
        if last_swing_lo and b["c"] < last_swing_lo and bars[i - 1]["c"] >= last_swing_lo:
            ev.append({"i": i, "t": b["t"], "type": "structure_break", "side": "down", "px": last_swing_lo})
        # fair value gaps (bars i-2, i-1, i)
        if i >= 2:
            a, c3 = bars[i - 2], b
            if c3["l"] - a["h"] >= FVG_MIN * b["c"]:
                ev.append({"i": i, "t": b["t"], "type": "fvg", "side": "bull", "top": c3["l"], "bot": a["h"]})
            if a["l"] - c3["h"] >= FVG_MIN * b["c"]:
                ev.append({"i": i, "t": b["t"], "type": "fvg", "side": "bear", "top": a["l"], "bot": c3["h"]})
        # liquidity sweeps (after the opening range for OR levels)
        for name, lvl, kind in levels:
            if lvl is None or (name.startswith("OR") and i < 15):
                continue
            if kind == "high" and b["h"] >= lvl * (1 + SWEEP_MIN) and bars[i - 1]["h"] < lvl:
                for k in range(i, min(i + 3, len(bars))):
                    if bars[k]["c"] < lvl:
                        ext = max(x["h"] for x in bars[i:k + 1])
                        ev.append({"i": k, "t": bars[k]["t"], "type": "sweep", "level": name, "side": "high",
                                   "lvl": lvl, "ext": ext})
                        break
            if kind == "low" and b["l"] <= lvl * (1 - SWEEP_MIN) and bars[i - 1]["l"] > lvl:
                for k in range(i, min(i + 3, len(bars))):
                    if bars[k]["c"] > lvl:
                        ext = min(x["l"] for x in bars[i:k + 1])
                        ev.append({"i": k, "t": bars[k]["t"], "type": "sweep", "level": name, "side": "low",
                                   "lvl": lvl, "ext": ext})
                        break
    return ev, orh, orl


def simulate(bars, i_entry, side, stop, target):
    """Enter at the open of bar i_entry; return (exit_px, reason, i_exit)."""
    for k in range(i_entry, len(bars)):
        b = bars[k]
        if side == "long":
            if b["l"] <= stop:
                return min(b["o"], stop), "stop", k
            if b["h"] >= target:
                return max(b["o"], target), "target", k
        else:
            if b["h"] >= stop:
                return max(b["o"], stop), "stop", k
            if b["l"] <= target:
                return min(b["o"], target), "target", k
        if b["t"] >= TIME_EXIT:
            return b["c"], "time", k
    return bars[-1]["c"], "close", len(bars) - 1


def atm_0dte_premium(s, minutes_left):
    t = max(minutes_left, 5) / (252 * 390)
    return 0.4 * s * SPY_IV * math.sqrt(t)


def mk_trade(day, bars, setup, side, i_entry, stop, why):
    e = bars[i_entry]["o"]
    risk = abs(e - stop)
    if risk <= 0.01:
        return None
    target = e + TARGET_R * risk if side == "long" else e - TARGET_R * risk
    x, reason, k = simulate(bars, i_entry, side, stop, target)
    move = (x - e) if side == "long" else (e - x)
    r = (move - COST_PER_SHARE) / risk
    hh, mm = map(int, bars[i_entry]["t"].split(":"))
    prem = atm_0dte_premium(e, 16 * 60 - (hh * 60 + mm))
    opt_ret = (0.5 * move) / prem - 2 * OPT_SPREAD
    sig = bars[i_entry - 1] if i_entry else bars[i_entry]
    return {"day": day, "setup": setup, "side": side, "t_in": bars[i_entry]["t"], "t_out": bars[k]["t"],
            "vwap": round(sig["vwap"], 2), "ema9": round(sig["ema9"], 2), "ema21": round(sig["ema21"], 2),
            "rsi": round(sig["rsi"], 1), "atr": round(sig["atr"], 3), "trend": trend_of(sig),
            "entry": round(e, 2), "stop": round(stop, 2), "target": round(target, 2), "exit": round(x, 2),
            "reason": reason, "R": round(r, 3), "pts": round(move, 2), "opt_ret": round(opt_ret, 3),
            "why": why}


def run():
    days = load()
    names = list(days)
    trades, counts, per_day = [], Counter(), {}
    for n, day in enumerate(names):
        bars = add_indicators(days[day])
        if n == 0:
            continue
        prev = days[names[n - 1]]
        pdh, pdl = max(b["h"] for b in prev), min(b["l"] for b in prev)
        ev, orh, orl = detect(bars, pdh, pdl)
        per_day[day] = Counter(e["type"] for e in ev)
        counts.update(e["type"] for e in ev)
        busy = {"sweep_reversal": -1, "fvg_retest": -1, "sweep_fvg": -1, "fvg_trend": -1, "vwap_reclaim": -1}
        # S4: FVG retest only WITH the trend (price vs VWAP and EMA9/21 agree)
        for e in ev:
            if e["type"] != "fvg" or e["i"] <= busy["fvg_trend"]:
                continue
            want = 1 if e["side"] == "bull" else -1
            if trend_of(bars[e["i"]]) != want:
                continue
            for k in range(e["i"] + 1, len(bars)):
                if bars[k]["t"] > LAST_ENTRY:
                    break
                hit = bars[k]["l"] <= e["top"] if want == 1 else bars[k]["h"] >= e["bot"]
                if hit:
                    if k + 1 < len(bars):
                        stop = e["bot"] * (1 - STOP_PAD) if want == 1 else e["top"] * (1 + STOP_PAD)
                        tr = mk_trade(day, bars, "fvg_trend", "long" if want == 1 else "short", k + 1, stop, f"{e['side']} FVG retest with trend")
                        if tr:
                            trades.append(tr); busy["fvg_trend"] = bars.index(next(b for b in bars if b["t"] == tr["t_out"]))
                    break
        # S5: VWAP reclaim after 10:00 with EMA9>EMA21 (long) / VWAP loss with EMA9<EMA21 (short); stop 1.5 ATR
        for i in range(31, len(bars) - 1):
            if bars[i]["t"] > LAST_ENTRY or i <= busy["vwap_reclaim"]:
                continue
            a, b = bars[i - 1], bars[i]
            side = None
            if a["c"] <= a["vwap"] < b["c"] and b["ema9"] > b["ema21"]:
                side = "long"
            elif a["c"] >= a["vwap"] > b["c"] and b["ema9"] < b["ema21"]:
                side = "short"
            if side:
                stop = b["c"] - 1.5 * b["atr"] if side == "long" else b["c"] + 1.5 * b["atr"]
                tr = mk_trade(day, bars, "vwap_reclaim", side, i + 1, stop, "VWAP cross with EMA9/21 trend")
                if tr:
                    trades.append(tr); busy["vwap_reclaim"] = bars.index(next(x for x in bars if x["t"] == tr["t_out"]))
        # S1: sweep reversal
        for e in ev:
            if e["type"] != "sweep" or e["i"] + 1 >= len(bars) or bars[e["i"] + 1]["t"] > LAST_ENTRY:
                continue
            if e["i"] <= busy["sweep_reversal"]:
                continue
            side = "short" if e["side"] == "high" else "long"
            stop = e["ext"] * (1 + STOP_PAD) if side == "short" else e["ext"] * (1 - STOP_PAD)
            tr = mk_trade(day, bars, "sweep_reversal", side, e["i"] + 1, stop, f"sweep of {e['level']}")
            if tr:
                trades.append(tr); busy["sweep_reversal"] = names and bars.index(next(b for b in bars if b["t"] == tr["t_out"]))
        # S2: FVG retest (enter on first return into the gap, with the gap's direction)
        for e in ev:
            if e["type"] != "fvg" or e["i"] <= busy["fvg_retest"]:
                continue
            for k in range(e["i"] + 1, len(bars)):
                if bars[k]["t"] > LAST_ENTRY:
                    break
                if e["side"] == "bull" and bars[k]["l"] <= e["top"]:
                    if k + 1 < len(bars):
                        tr = mk_trade(day, bars, "fvg_retest", "long", k + 1, e["bot"] * (1 - STOP_PAD), "bull FVG retest")
                        if tr:
                            trades.append(tr); busy["fvg_retest"] = bars.index(next(b for b in bars if b["t"] == tr["t_out"]))
                    break
                if e["side"] == "bear" and bars[k]["h"] >= e["bot"]:
                    if k + 1 < len(bars):
                        tr = mk_trade(day, bars, "fvg_retest", "short", k + 1, e["top"] * (1 + STOP_PAD), "bear FVG retest")
                        if tr:
                            trades.append(tr); busy["fvg_retest"] = bars.index(next(b for b in bars if b["t"] == tr["t_out"]))
                    break
        # S3: sweep then FVG in the reversal direction within 10 bars (the video's "FVG + liquidity sweep")
        for e in ev:
            if e["type"] != "sweep" or e["i"] <= busy["sweep_fvg"]:
                continue
            want = "bear" if e["side"] == "high" else "bull"
            f = next((x for x in ev if x["type"] == "fvg" and x["side"] == want and e["i"] < x["i"] <= e["i"] + 10), None)
            if f and f["i"] + 1 < len(bars) and bars[f["i"] + 1]["t"] <= LAST_ENTRY:
                side = "short" if want == "bear" else "long"
                stop = e["ext"] * (1 + STOP_PAD) if side == "short" else e["ext"] * (1 - STOP_PAD)
                tr = mk_trade(day, bars, "sweep_fvg", side, f["i"] + 1, stop, f"sweep of {e['level']} + FVG")
                if tr:
                    trades.append(tr); busy["sweep_fvg"] = bars.index(next(b for b in bars if b["t"] == tr["t_out"]))
    return names, trades, counts, per_day


def summary(ts):
    if not ts:
        return {"n": 0}
    rs = [t["R"] for t in ts]
    w = [r for r in rs if r > 0]; l = [-r for r in rs if r < 0]
    sd = (sum((r - mean(rs)) ** 2 for r in rs) / max(1, len(rs) - 1)) ** 0.5
    return {"n": len(ts), "win": round(100 * len(w) / len(rs), 1),
            "pf": round(sum(w) / sum(l), 2) if l else None, "avgR": round(mean(rs), 3),
            "t": round(mean(rs) / (sd / math.sqrt(len(rs))), 2) if sd > 0 else None,
            "opt_avg": round(mean(t["opt_ret"] for t in ts), 3),
            "maxdd_R": round(max_dd(rs), 2)}


def max_dd(rs):
    eq = pk = dd = 0.0
    for r in rs:
        eq += r; pk = max(pk, eq); dd = min(dd, eq - pk)
    return dd


def main():
    names, trades, counts, per_day = run()
    days = names[1:]
    half = days[len(days) // 2]
    print(f"TARS DATA FARM  SPY 1-min  {days[0]}..{days[-1]}  ({len(days)} days, IN-SAMPLE)")
    print("events: " + ", ".join(f"{k} {v}" for k, v in counts.most_common()))
    print(f"\n  {'setup':<16} {'n':>4} {'win%':>5} {'PF':>5} {'avg R':>6} {'t':>6} {'maxDD R':>8} {'0DTE avg':>9} | first half / second half avg R")
    out = {"range": [days[0], days[-1]], "n_days": len(days), "events": counts, "setups": {}, "trades": trades,
           "per_day": {d: dict(c) for d, c in per_day.items()}}
    for s in SETUPS:
        ts = [t for t in trades if t["setup"] == s]
        a = summary(ts)
        h1 = summary([t for t in ts if t["day"] < half]); h2 = summary([t for t in ts if t["day"] >= half])
        weeks = defaultdict(list)
        for t in ts:
            weeks[t["day"][:8] + str((int(t["day"][8:]) - 1) // 7)].append(t["R"])
        pos_weeks = sum(1 for v in weeks.values() if sum(v) > 0)
        a.update({"h1": h1.get("avgR"), "h2": h2.get("avgR"), "weeks_pos": f"{pos_weeks}/{len(weeks)}"})
        out["setups"][s] = a
        if a["n"]:
            print(f"  {s:<16} {a['n']:>4} {a['win']:>5} {a['pf'] if a['pf'] is not None else '-':>5} {a['avgR']:>+6.2f} "
                  f"{a['t'] if a['t'] is not None else '-':>6} {a['maxdd_R']:>8} {100*a['opt_avg']:>+8.1f}% | "
                  f"{h1.get('avgR')} / {h2.get('avgR')}  weeks positive {pos_weeks}/{len(weeks)}")
    json.dump(out, open(OUT, "w"), indent=0)
    print(f"\noutcome book: {len(trades)} trades -> {OUT.relative_to(BASE.parent)}")


if __name__ == "__main__":
    main()
