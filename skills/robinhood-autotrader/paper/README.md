# Paper harness — how the pieces fit

Operating guide for the measurement apparatus in this directory.
Last updated: 2026-09-11 · Status: built and running on 248 months of real history · Audience: any session touching this ledger

## ⚠️ Read this first: four writers, one ledger

As of 2026-09-11 **three scheduled Routines and at least one independent session**
all have write access to this account and this ledger:

| Routine | Fires | Trigger |
|---|---|---|
| market-hours | 14:00 / 17:00 / 20:00 UTC, weekdays | `trig_01MyLJEvxvZWWbi4nX1PrUfe` |
| post-close review | ~20:35 UTC | `trig_0119jh2dh1VLnPLH1KvYe27d` |
| off-hours check-in | ~21:00 UTC | `trig_017fdwDVyPkPBCzd5ChQZGoF` |

Plus sessions started directly, which answer to none of the above.

This has already caused real incidents. On 2026-09-11 one session sold ACHR and
VOOG roughly 45 minutes after the owner bought them manually; another closed the
NVDA call and opened three new positions while a third was mid-conversation with
the owner about whether to trade at all. A fourth logged a position that
self-flagged as exceeding the standing options capacity.

**Therefore:** verify live state from the broker before acting on any briefed
position list, including the ones in Routine prompts. Assume this ledger has
moved since you last read it — `git pull` before writing, and expect to merge.
A Routine prompt is a snapshot written by a past session, not current truth.

## The pipeline

```
fetch_closes.py  →  history/monthly.json  →  signal_dual_momentum.py  →  trades.jsonl
                            ↓                                                    ↓
                       backtest.py                       expectancy.py  +  benchmark.py
```

**`fetch_closes.py`** — the only component that touches the network. Pulls daily
bars, collapses them to one close per month (the month's LAST real close, keyed
`YYYY-MM-01`), and merges into `history/monthly.json`, accumulating history
rather than rebuilding it. Drops interpolated bars and skips missing/zero/unparseable ones
instead of defaulting them. Needs `ROBINHOOD_*` credentials in the environment
(see `../scripts/.env.example`), so it runs where that `.env` lives.

**`signal_dual_momentum.py`** — the monthly rule from `../reference/STRATEGY.md`:
12-1 momentum, absolute filter requiring both positive momentum *and* price above
the 10-month MA, top 3 equal weight, unfilled slots to cash. Runs on a MONTHLY
basis (12/1/10) because that is the parameterisation `backtest.py` actually
measured; the earlier daily set (252/21/200) was never tested and was removed. Reads the stored series,
never a live quote, so a signal regenerated for a past date reproduces what it
produced then. `--emit-ledger` writes pre-registered records.

**`expectancy.py`** — R-multiples (realized ÷ planned_risk) with a 95% CI. Answers
"did this make money against what was risked."

**`backtest.py`** — runs the same rule over 235 months of committed history, so a
result exists now rather than in three years. `--dual` tests the full rotation.

**`benchmark.py`** — excess return versus the benchmark held over each trade's
identical window. Answers the *different* question "did picking these beat just
owning the index." Both are needed: the NANC congressional ETF beat the S&P
purely on tech concentration, and raw return scores that as skill.

## Running it

```bash
python3 fetch_closes.py                                    # refresh history/monthly.json
python3 signal_dual_momentum.py history/monthly.json       # inspect the signal
python3 signal_dual_momentum.py history/monthly.json --emit-ledger >> trades.jsonl
python3 expectancy.py
python3 benchmark.py --strategy dual-momentum --bench history/monthly.json --bench-symbol SPY
python3 backtest.py history/monthly.json --dual --top 3    # 235 months of real history
```

A signal only emits when parameters match `params.lock.json`. If it refuses,
that is the guard working — read the drift it prints before changing anything.

## What the harness guarantees, and what it does not

**Guarantees.** Signals are reproducible from stored data. Fabricated prices
cannot enter the series. Declines are logged but excluded from statistics.
Unscoreable trades are named, not estimated. Both scorers report a confidence
interval and say plainly when a result is indistinguishable from random.

**Does not guarantee anything about returns.** The apparatus measures; it does
not predict. A correct, well-run experiment returning "no edge" is a success of
the instrument, not a failure of it — see the stopping rules in `PROTOCOL.md`,
which are commitments rather than guidelines.

## Live positions as of 2026-09-11 close

Recorded here because the Routine prompts carry a stale list and a correction to
them was blocked. **Verify against the broker before acting** — this is a
snapshot too, just a more recent one.

| | |
|---|---|
| TENB | 4 sh @ $32.3143, stop $29.18 GTC |
| RDDT | 1 sh @ $157.48, stop $143.20 GTC |
| CLX | 1 sh @ $87.53, stop $83.50 |
| INTC | Oct-2 $115 call x1, stop $1.20 GTC |
| JD | Oct-16 $28 call x2, stop $0.36 / target $1.45 |
| CPNG | Oct-16 $16 call x2, stop $0.23 / target $0.95 — ⚠️ over the 2-position options capacity and never run through the 8-step protocol |

Account $951.00. **Closed 2026-09-11:** NVDA Oct-2 $235 call (−$46.00), ALOY
calls, and ACHR/VOOG — the latter two bought manually by the owner and sold by an
agent session 45 minutes later.

## Known gaps

- **Backtest history is real and committed** (`history/monthly.json`, 7 assets ×
  248 months). `fetch_closes.py` extends it; nothing blocks a signal today.
- **`2026-09-11-NVDA-C235-1002-LIVE` is permanently unscoreable** against a
  benchmark: it records `limit_price` with `entry: null`. Left uncorrected on
  purpose — the ledger is append-only and the realized −$46.00 covers a
  two-contract episode that cannot be cleanly split after the fact. Future
  records must put the actual fill in `entry`.
- **Existing records carry no `strategy` tag**, so they score as one
  undifferentiated group. New records should always be tagged.
- **The off-hours Routine prompt is stale** — it still lists NVDA and ALOY as
  live and repeats the disproved "no stop possible on a long option" claim. A
  correction was drafted 2026-09-11 but blocked by the permission classifier.
