#!/usr/bin/env python3
"""TARS shadow book: runs TARS's rules mechanically on paper, every trading day.

Why: 33 live trades can't tell us whether the rules work. A shadow book adds a
clean, forward-only, discretion-free record at zero risk. Forward-only means
no survivorship bias: the universe is whatever the market offers each day.

Two books run from the same daily snapshot:
  A "tars1"      : R2 entries + R3 sizing + R4 exits (8% stop, breakeven at
                   +8%, 20% trail below the highest close) + the 200-day trend exit.
  B "trend_only" : same entries and sizing, exits ONLY on a close below the
                   200-day. It tests, forward and live, the research finding
                   that tight stops cost more than they save.
Benchmark: SPY, same start.

All values are NAV ratios (start = 1.0), never dollars (R13).
Fills: at the day's close, 0.10% cost per side. Stops are judged on
CLOSES, not intraday lows. That flatters stops slightly on gap-down days
and is stated here so nobody mistakes it for a real fill.

Usage (the desk runs this at the 5:17pm ET close check):
  1. run_scan on scan 82b6b119-03ea-49ff-9e5b-4dc747bd2918 ("TARS shadow
     universe") and save the raw JSON result to a file.
  2. python3 shadow_book.py plan --scan SCAN.json
       -> prints the symbols to quote (held + top eligible + SPY) and the
          held symbols that need a 200-day SMA.
  3. get_equity_quotes for those symbols -> save the raw JSON to a file.
     For each held symbol: get_equity_technical_indicators(type sma,
     period 200, interval day, output latest).
  4. python3 shadow_book.py run --date YYYY-MM-DD --scan SCAN.json
       --quotes QUOTES.json --vix 15.3 --sma NVDA=190.1 --sma INTC=88.2 ...
  5. python3 shadow_book.py report   (NAV vs SPY, positions, trades)
"""
import argparse, json, os, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state.json")
LOG = os.path.join(HERE, "log.jsonl")
NAV = os.path.join(HERE, "nav.csv")
DAILY = os.path.join(HERE, "daily")

COST = 0.001          # per side
POS_W = 0.20          # R3 per-position cap (fraction of NAV)
FLOOR = 0.15          # R3 cash floor
RISK_BUDGET = 0.08    # R3 total risk budget
HARD = 0.92; BE_TRIG = 1.08; TRAIL = 0.80   # R4
EARN_DAYS = 5         # ~3 trading days, in calendar days (conservative)
QUOTE_TOP = 15        # candidates quoted each day for official closes
SECTORS = {"101":"Basic Materials","102":"Consumer Cyclical","103":"Financial Services",
  "104":"Real Estate","205":"Consumer Defensive","206":"Healthcare","207":"Utilities",
  "308":"Communication Services","309":"Energy","310":"Industrials","311":"Technology","":"Unknown"}
BOOKS = ("tars1", "trend_only")

def load_json(p):
    with open(p) as f: return json.load(f)

def unwrap(d):
    """Accept raw MCP output ({data:{result:..}}), a list of MCP content blocks, or bare."""
    if isinstance(d, list) and d and isinstance(d[0], dict) and "text" in d[0]:
        d = json.loads(d[0]["text"])
    if isinstance(d, dict) and "data" in d: d = d["data"]
    if isinstance(d, dict) and "result" in d: d = d["result"]
    return d

def parse_scan(path):
    r = unwrap(load_json(path))
    out = []
    for x in r["results"]:
        c = x["columns"]
        try:
            ed = c.get("Earnings date")
            ed = dt.datetime.strptime(str(int(float(ed))), "%Y%m%d").date() if ed not in (None, "") else None
        except Exception:
            ed = None
        try:
            out.append({"sym": x["ticker"], "last": float(c["Last"]), "sma200": float(c["SMA200"]),
                        "vs200": float(c["vs200"]), "sector": SECTORS.get(str(c.get("Sector", "")), str(c.get("Sector"))),
                        "earnings": ed.isoformat() if ed else None})
        except (KeyError, ValueError, TypeError):
            continue
    out.sort(key=lambda z: -z["vs200"])
    return out

def parse_quotes(path, date):
    r = unwrap(load_json(path))
    px = {}
    for e in r["results"]:
        q = e.get("quote", {}); c = e.get("close") or {}
        sym = q.get("symbol") or c.get("symbol")
        if c.get("date") == date and c.get("price"):
            px[sym] = float(c["price"])
        elif q.get("last_trade_price"):
            px[sym] = float(q["last_trade_price"])
    return px

def new_state(date):
    s = {"start": date, "last_run": None, "spy_start": None, "books": {}}
    for b in BOOKS: s["books"][b] = {"cash": 1.0, "pos": {}, "closed": []}
    return s

def load_state():
    return load_json(STATE) if os.path.exists(STATE) else None

def stop_for(p):
    e, h = p["entry"], p["high"]
    s = e * HARD
    if h >= e * BE_TRIG: s = max(s, e)
    return max(s, h * TRAIL)

def nav_of(book, px):
    return book["cash"] + sum(p["units"] * px.get(sym, p["last"]) for sym, p in book["pos"].items())

def eligible(cands, book, date):
    d0 = dt.date.fromisoformat(date)
    held = set(book["pos"])
    sect = {}
    for p in book["pos"].values(): sect[p["sector"]] = sect.get(p["sector"], 0) + 1
    out = []
    for c in cands:
        if c["sym"] in held: continue
        if c["earnings"]:
            dd = (dt.date.fromisoformat(c["earnings"]) - d0).days
            if 0 <= dd <= EARN_DAYS: continue
        if sect.get(c["sector"], 0) >= 2: continue
        out.append(c)
    return out

def cmd_plan(a):
    s = load_state()
    cands = parse_scan(a.scan)
    held = set()
    if s:
        for b in BOOKS: held |= set(s["books"][b]["pos"])
    # quote the top candidates that could actually be entered: earnings
    # blackout applied, and at most 2 per sector counting what's held
    fake = {"pos": {}}
    if s:
        for b in BOOKS: fake["pos"].update(s["books"][b]["pos"])
    date = dt.date.today().isoformat()
    top, sect = [], {}
    for p in fake["pos"].values(): sect[p["sector"]] = sect.get(p["sector"], 0) + 1
    for c in eligible(cands, fake, date):
        if sect.get(c["sector"], 0) >= 2: continue
        top.append(c["sym"]); sect[c["sector"]] = sect.get(c["sector"], 0) + 1
        if len(top) >= QUOTE_TOP: break
    syms = sorted(held) + top + ["SPY"]
    print("QUOTE:", ",".join(syms))
    print("SMA200 NEEDED FOR:", ",".join(sorted(held)) or "(none)")

def log(ev):
    with open(LOG, "a") as f: f.write(json.dumps(ev) + "\n")

def cmd_run(a):
    date = a.date
    s = load_state() or new_state(date)
    if s["last_run"] and s["last_run"] >= date:
        sys.exit(f"already ran for {s['last_run']}; refusing to double-run {date}")
    cands = parse_scan(a.scan)
    px = parse_quotes(a.quotes, date)
    sma = {}
    for kv in a.sma or []:
        k, v = kv.split("="); sma[k.upper()] = float(v)
    if "SPY" not in px: sys.exit("SPY missing from quotes")
    if s["spy_start"] is None: s["spy_start"] = px["SPY"]
    cand_by = {c["sym"]: c for c in cands}
    for c in cands:
        if c["sym"] not in px: px.setdefault("_scan_" + c["sym"], c["last"])
    snap = {"date": date, "vix": a.vix, "spy": px["SPY"], "px": px, "sma": sma,
            "top": [c for c in cands[:40]]}
    with open(os.path.join(DAILY, f"{date}.json"), "w") as f: json.dump(snap, f)

    for bname in BOOKS:
        book = s["books"][bname]
        # 1. exits
        for sym in list(book["pos"]):
            p = book["pos"][sym]
            if sym not in px:
                log({"date": date, "book": bname, "event": "NO_PRICE", "sym": sym}); continue
            c = px[sym]; p["last"] = c
            p["high"] = max(p["high"], c)
            below = sym in sma and c < sma[sym]
            if sym not in sma:
                log({"date": date, "book": bname, "event": "NO_SMA", "sym": sym})
            reason = None
            if bname == "tars1" and c <= stop_for(p): reason = "R4_stop"
            if below and not reason: reason = "trend_exit_200d"
            if reason:
                proceeds = p["units"] * c * (1 - COST)
                book["cash"] += proceeds
                ret = c * (1 - COST) / (p["entry"] * (1 + COST)) - 1
                rec = {"date": date, "book": bname, "event": "EXIT", "sym": sym, "reason": reason,
                       "entry_date": p["entry_date"], "entry": p["entry"], "exit": c, "ret": round(ret, 5)}
                book["closed"].append(rec); log(rec); del book["pos"][sym]
        # 2. entries
        nav = nav_of(book, px)
        risk = sum(p["units"] * max(0.0, p["entry"] - stop_for(p)) for p in book["pos"].values()) / nav if bname == "tars1" else 0.0
        for c in eligible(cands, book, date):
            if c["sym"] not in px: continue      # only enter at an official quote
            if sum(1 for p in book["pos"].values() if p["sector"] == c["sector"]) >= 2: continue
            size = POS_W * nav
            if book["cash"] - size * (1 + COST) < FLOOR * nav: break
            if bname == "tars1" and risk + POS_W * (1 - HARD) > RISK_BUDGET + 1e-9: break
            price = px[c["sym"]]
            units = size / (price * (1 + COST))
            book["cash"] -= size
            book["pos"][c["sym"]] = {"entry": price, "units": units, "high": price, "last": price,
                                     "entry_date": date, "sector": c["sector"]}
            risk += POS_W * (1 - HARD)
            log({"date": date, "book": bname, "event": "ENTRY", "sym": c["sym"], "price": price,
                 "vs200": round(c["vs200"], 3), "sector": c["sector"], "weight": POS_W})
        book["nav"] = nav_of(book, px)
    s["last_run"] = date
    spy_nav = px["SPY"] / s["spy_start"]
    with open(STATE, "w") as f: json.dump(s, f, indent=1)
    new = not os.path.exists(NAV)
    with open(NAV, "a") as f:
        if new: f.write("date,tars1,trend_only,spy,vix\n")
        f.write(f"{date},{s['books']['tars1']['nav']:.5f},{s['books']['trend_only']['nav']:.5f},{spy_nav:.5f},{a.vix}\n")
    report(s)

def report(s=None):
    s = s or load_state()
    if not s: print("no shadow book yet"); return
    rows = open(NAV).read().strip().splitlines()[1:] if os.path.exists(NAV) else []
    last = rows[-1].split(",") if rows else None
    print(f"SHADOW BOOK since {s['start']}, last run {s['last_run']}, {len(rows)} trading day(s)")
    if last:
        print(f"  NAV  tars1 {float(last[1]):.4f} | trend_only {float(last[2]):.4f} | SPY {float(last[3]):.4f}")
    for b in BOOKS:
        bk = s["books"][b]
        cl = bk["closed"]
        wins = sum(1 for c in cl if c["ret"] > 0)
        avg = sum(c["ret"] for c in cl) / len(cl) if cl else 0
        pos = ", ".join(f"{k}({(v['last']/v['entry']-1)*100:+.1f}%)" for k, v in bk["pos"].items())
        print(f"  [{b}] cash {bk['cash']/bk.get('nav',1):.0%} | open: {pos or 'none'} | closed {len(cl)}, wins {wins}, avg {avg*100:+.2f}%")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--scan", required=True)
    r = sub.add_parser("run"); r.add_argument("--date", required=True); r.add_argument("--scan", required=True)
    r.add_argument("--quotes", required=True); r.add_argument("--vix", type=float, required=True)
    r.add_argument("--sma", action="append")
    sub.add_parser("report")
    a = ap.parse_args()
    {"plan": cmd_plan, "run": cmd_run, "report": lambda a: report()}[a.cmd](a)
