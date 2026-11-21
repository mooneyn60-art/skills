#!/usr/bin/env python3
"""
Invariant tests for the paper harness. Run before trusting any number it prints.

    python3 test_harness.py

Every test here encodes a property that, if it silently broke, would produce
*plausible wrong numbers* rather than an error -- which is the only kind of bug
that really matters in a measurement instrument. A crash gets noticed. A
momentum figure computed from a fabricated price does not.

Two real bugs shipped in this directory before these existed, both found by
reading rather than by failing: a hardcoded universe size that mislabelled every
single-stock result, and a strategy reading its calendar from a module-level
global that a previous run on a different dataset could leave stale. Neither
raised anything. Both are now covered below.

These tests were mutation-tested: code was deliberately broken to confirm each
test can actually fail. Five of six mutations were caught -- letting interpolated
bars through, letting `seasonal` guess a calendar, and shifting the moving-average
window forward one bar all turned the suite red.

ONE ESCAPED, and it is recorded rather than quietly fixed. A lookahead that
CLAMPS its own index (`closes[min(t+1, len-1)]`) reads legally when the series is
truncated, so the truncation test cannot see it. That shape is somewhat
artificial -- a real lookahead bug usually indexes past the end and crashes -- but
the gap is genuine: this suite proves the absence of *unclamped* lookahead, not of
all lookahead.

Note when mutation testing: clear __pycache__ between swaps. Stale bytecode
produced a phantom failure on already-restored code and briefly looked like a
real regression.

No network, no credentials, no market data required.
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"\n        {detail}" if detail and not cond else ""))


def series(start, drift, n, first="2006-01-01"):
    y, m = int(first[:4]), int(first[5:7])
    out, px = {}, start
    for _ in range(n):
        out[f"{y:04d}-{m:02d}-01"] = round(px, 4)
        px *= (1 + drift)
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


# ---------------------------------------------------------------- fetch_closes
def test_fetch():
    from fetch_closes import parse_bars, to_monthly, merge
    bars = [
        {"symbol": "X", "begins_at": "2026-01-05T00:00:00Z", "close_price": "10.0"},
        {"symbol": "X", "begins_at": "2026-01-06T00:00:00Z", "close_price": "999", "interpolated": True},
        {"symbol": "X", "begins_at": "2026-01-07T00:00:00Z", "close_price": "999", "interpolated": "true"},
        {"symbol": "X", "begins_at": "2026-01-08T00:00:00Z", "close_price": None},
        {"symbol": "X", "begins_at": "2026-01-09T00:00:00Z", "close_price": "0"},
        {"symbol": "X", "begins_at": "2026-01-12T00:00:00Z", "close_price": "abc"},
        {"symbol": "X", "begins_at": "2026-01-13T00:00:00Z", "close_price": "11.0"},
    ]
    got = parse_bars(bars)["X"]
    check("interpolated bars dropped (bool and string forms)",
          "2026-01-06" not in got and "2026-01-07" not in got)
    check("missing/zero/unparseable closes skipped, never defaulted",
          set(got) == {"2026-01-05", "2026-01-13"}, f"got {sorted(got)}")
    check("no price is invented to fill a gap", 999 not in got.values())

    m = to_monthly({"X": {"2026-01-05": 10.0, "2026-01-30": 12.0, "2026-03-02": 9.0}})["X"]
    check("monthly collapse takes the month's LAST close", m["2026-01-01"] == 12.0)
    check("a month with no data stays absent, not carried forward",
          "2026-02-01" not in m, f"got {sorted(m)}")

    merged = merge({"X": {"2026-01-01": 1.0, "2026-02-01": 2.0}}, {"X": {"2026-02-01": 99.0}})
    check("merge keeps prior history", merged["X"]["2026-01-01"] == 1.0)
    check("merge lets fresh data win per date", merged["X"]["2026-02-01"] == 99.0)


# ------------------------------------------------------------------ the signal
def test_signal():
    import signal_dual_momentum as sig
    up, down = series(100, 0.02, 40), series(100, -0.02, 40)
    uni = {"UP": up, "DOWN": down, "BIL": series(100, 0.0, 40)}

    elig, rej = sig.evaluate(uni, "2009-04-01")
    check("rising asset is eligible", any(a["symbol"] == "UP" for a in elig))
    check("falling asset is rejected", any(r["symbol"] == "DOWN" for r in rej))
    check("rejection states a reason rather than failing silently",
          all("reason" in r for r in rej))

    short = {"NEW": series(100, 0.02, 5), "BIL": series(100, 0.0, 5)}
    _, rej = sig.evaluate(short, "2006-05-01")
    check("insufficient history is reported, not estimated from a short window",
          any("insufficient" in r["reason"] for r in rej))

    alloc = sig.allocate([], 3)
    check("a month with nothing eligible allocates to cash", alloc[0]["symbol"] == sig.CASH)
    check("cash weight fills every empty slot", abs(alloc[0]["weight"] - 1.0) < 1e-9)

    recs = sig.ledger_lines(sig.allocate(elig, 3), "2009-04-01")
    check("emitted records are pre-registered (no outcome fields set)",
          all(r["closed"] is None and r["exit"] is None and r["realized_pnl"] is None
              for r in recs))
    check("emitted records carry a strategy tag", all(r["strategy"] for r in recs))

    # Same inputs must give the same answer, or no signal is reproducible.
    a, _ = sig.evaluate(uni, "2009-04-01")
    b, _ = sig.evaluate(uni, "2009-04-01")
    check("signal is deterministic for a fixed as-of date",
          [x["symbol"] for x in a] == [x["symbol"] for x in b])

    drift = sig.check_params(99, ["SPY"])
    check("parameter lock detects drift", bool(drift), f"got {drift}")


# ------------------------------------------------------------------- scoring
def test_benchmark():
    import benchmark as bm
    bench = {"2026-01-01": 100.0, "2026-02-01": 110.0}
    with tempfile.TemporaryDirectory() as d:
        led = os.path.join(d, "t.jsonl")
        with open(led, "w") as fh:
            # Up 10% while the index is up 10%: profitable, zero excess.
            fh.write(json.dumps({"id": "a", "symbol": "A", "opened": "2026-01-01T00:00:00Z",
                                 "closed": "2026-02-01T00:00:00Z", "entry": 100.0,
                                 "exit": 110.0, "exit_reason": "x"}) + "\n")
            fh.write(json.dumps({"id": "b", "symbol": "B", "opened": "2026-01-01T00:00:00Z",
                                 "closed": "2026-02-01T00:00:00Z", "entry": 100.0,
                                 "exit": 150.0, "exit_reason": "not_taken"}) + "\n")
            fh.write(json.dumps({"id": "c", "symbol": "C", "opened": "2026-01-01T00:00:00Z",
                                 "closed": "2099-01-01T00:00:00Z", "entry": 100.0,
                                 "exit": 110.0, "exit_reason": "x"}) + "\n")
        scored, unscoreable = bm.score(led, bench)
        check("a profitable trade that merely matched the index scores zero excess",
              len(scored) == 1 and abs(scored[0]["_excess"]) < 1e-9)
        check("declines are excluded from the statistics",
              all(t["id"] != "b" for t in scored))
        check("a trade the benchmark cannot cover is named unscoreable, not estimated",
              len(unscoreable) == 1 and unscoreable[0][0]["id"] == "c")

    check("short direction is sign-corrected",
          abs(bm.trade_return({"direction": "short", "entry": 100.0, "exit": 90.0}) - 0.10) < 1e-9)
    check("a missing price returns None rather than zero",
          bm.trade_return({"entry": 100.0, "exit": None}) is None)


def test_expectancy():
    import expectancy as ex
    with tempfile.TemporaryDirectory() as d:
        led = os.path.join(d, "t.jsonl")
        with open(led, "w") as fh:
            fh.write(json.dumps({"id": "1", "symbol": "A", "closed": "2026-02-01",
                                 "planned_risk": 10.0, "realized_pnl": 20.0}) + "\n")
            fh.write(json.dumps({"id": "2", "symbol": "B", "closed": "2026-02-01",
                                 "planned_risk": None, "realized_pnl": 5.0}) + "\n")
            fh.write(json.dumps({"id": "3", "symbol": "C", "closed": "2026-02-01",
                                 "exit_reason": "not_taken"}) + "\n")
        taken, skipped, unstopped = ex.load(led)
        check("R is computed as realized over planned risk", abs(taken[0]["R"] - 2.0) < 1e-9)
        check("an unstopped position is separated, never folded into R stats",
              len(unstopped) == 1 and len(taken) == 1)
        check("declines are counted but kept out of the statistics",
              len(skipped) == 1)


# ------------------------------------------------------------------ backtests
def test_backtest():
    import backtest as bt
    rising = [100 * (1.02 ** i) for i in range(40)]
    check("signal returns None before there is enough history", bt.signal(rising, 3) is None)
    check("signal is True in a sustained uptrend", bt.signal(rising, 30) is True)
    falling = [100 * (0.98 ** i) for i in range(40)]
    check("signal is False in a sustained downtrend", bt.signal(falling, 30) is False)

    # No lookahead, tested as a general property rather than at one point: for
    # EVERY t, the signal computed from data truncated at t must equal the signal
    # computed from the full series. A single monotonic sample is too coarse --
    # peeking one month ahead on a series that only rises gives the same boolean,
    # so a real lookahead bug survives it. The series below rises, crashes, then
    # recovers, so peeking actually changes the answer somewhere.
    mixed = ([100 * (1.03 ** i) for i in range(24)]
             + [240 * (0.88 ** i) for i in range(12)]
             + [60 * (1.04 ** i) for i in range(18)])
    leaks = [t for t in range(max(bt.LOOKBACK, bt.MA_WINDOW), len(mixed) - 1)
             if bt.signal(mixed[:t + 1], t) != bt.signal(mixed, t)]
    check("no lookahead: truncating the future never changes a past signal",
          not leaks, f"signal changed at t={leaks[:5]} when future data was added")

    check("max_drawdown of a monotonic rise is zero",
          abs(bt.max_drawdown([1, 2, 3, 4])) < 1e-12)
    check("max_drawdown catches a halving", abs(bt.max_drawdown([1, 2, 1]) + 0.5) < 1e-12)

    rows = [{"date": "2026-01-01", "strat": 1.0, "bh": 1.0}]
    check("a decline window with too little data is reported, not scored as 0.0%",
          len(bt.window(rows, "2008-01", "2009-01")) < 2)


def test_compare():
    import compare_strategies as cs
    uni = {"A": series(100, 0.02, 40), "B": series(100, -0.01, 40)}
    syms, dates, px = cs.prep(uni)
    try:
        cs.select("seasonal", syms, px, 20, 2)
        check("seasonal refuses to guess a calendar it was not given", False,
              "it silently accepted a missing `dates`")
    except ValueError:
        check("seasonal refuses to guess a calendar it was not given", True)
    book = cs.select("seasonal", syms, px, 20, 2, dates)
    check("seasonal works when dates are supplied", isinstance(book, list))
    check("momentum picks the riser over the faller",
          [s for s, _ in cs.select("momentum", syms, px, 20, 1)] == ["A"])
    check("reversion picks the faller over the riser",
          [s for s, _ in cs.select("reversion", syms, px, 20, 1)] == ["B"])
    w = sum(w for _, w in cs.select("volweight", syms, px, 20, 2))
    check("volweight allocates a full book, not more or less", abs(w - 1.0) < 1e-9)


def test_end_to_end():
    """The committed history must still produce the documented numbers."""
    hist = os.path.join(HERE, "history", "monthly.json")
    if not os.path.exists(hist):
        check("committed history present", False, f"missing {hist}")
        return
    out = subprocess.run([sys.executable, os.path.join(HERE, "backtest.py"), hist,
                          "--dual", "--top", "3"], capture_output=True, text=True).stdout
    check("ETF dual momentum still reports 8.14% CAGR", "8.14%" in out, out[:200])
    check("ETF dual momentum still reports -16.1% max drawdown", "-16.1%" in out)
    r = subprocess.run([sys.executable, os.path.join(HERE, "signal_dual_momentum.py"),
                        hist, "--top", "99", "--emit-ledger"], capture_output=True, text=True)
    check("lock blocks emission on drift (exit 2)", r.returncode == 2, f"exit {r.returncode}")


def main():
    for fn in (test_fetch, test_signal, test_benchmark, test_expectancy,
               test_backtest, test_compare, test_end_to_end):
        print(f"\n{fn.__name__}:")
        fn()
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
