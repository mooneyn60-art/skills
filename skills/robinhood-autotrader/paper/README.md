# Paper harness — how the pieces fit

Operating guide for the measurement apparatus in this directory.
Last updated: 2026-09-11 · Status: built, not yet fed real data · Audience: any session touching this ledger

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
fetch_closes.py  →  closes.json  →  signal_dual_momentum.py  →  trades.jsonl
                                                                     ↓
                                              expectancy.py  +  benchmark.py
```

**`fetch_closes.py`** — the only component that touches the network. Pulls daily
closes and merges them into `closes.json`, accumulating history rather than
rebuilding it. Drops interpolated bars and skips missing/zero/unparseable ones
instead of defaulting them. Needs `ROBINHOOD_*` credentials in the environment
(see `../scripts/.env.example`), so it runs where that `.env` lives.

**`signal_dual_momentum.py`** — the monthly rule from `../reference/STRATEGY.md`:
12-1 momentum, absolute filter requiring both positive momentum *and* price above
the 200d MA, top 3 equal weight, unfilled slots to cash. Reads the stored series,
never a live quote, so a signal regenerated for a past date reproduces what it
produced then. `--emit-ledger` writes pre-registered records.

**`expectancy.py`** — R-multiples (realized ÷ planned_risk) with a 95% CI. Answers
"did this make money against what was risked."

**`benchmark.py`** — excess return versus the benchmark held over each trade's
identical window. Answers the *different* question "did picking these beat just
owning the index." Both are needed: the NANC congressional ETF beat the S&P
purely on tech concentration, and raw return scores that as skill.

## Running it

```bash
python3 fetch_closes.py                                   # refresh closes.json
python3 signal_dual_momentum.py closes.json               # inspect the signal
python3 signal_dual_momentum.py closes.json --emit-ledger >> trades.jsonl
python3 expectancy.py
python3 benchmark.py --strategy dual-momentum             # needs benchmark_spy.json
```

## What the harness guarantees, and what it does not

**Guarantees.** Signals are reproducible from stored data. Fabricated prices
cannot enter the series. Declines are logged but excluded from statistics.
Unscoreable trades are named, not estimated. Both scorers report a confidence
interval and say plainly when a result is indistinguishable from random.

**Does not guarantee anything about returns.** The apparatus measures; it does
not predict. A correct, well-run experiment returning "no edge" is a success of
the instrument, not a failure of it — see the stopping rules in `PROTOCOL.md`,
which are commitments rather than guidelines.

## Known gaps

- **`closes.json` does not exist yet.** Nothing runs until `fetch_closes.py` is
  run somewhere with credentials.
- **`benchmark_spy.json` does not exist yet.** Same shape, `{"YYYY-MM-DD": close}`.
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
