# Swarm Memory

One-line: Shared memory for the research swarm; one line per tested variant.

Last Updated: 2026-10-15
Status: ACTIVE (append-only)
Audience: TARS research sessions (queen and workers)

## Overview

Every swarm run appends one line per variant: date | question | variant |
result (PASS/FAIL/UNVERIFIED) | the one number that decided it | note file.
Read this first so no run repeats a dead variant.

## Entries

(none yet)

## 2026-10-15 — Desk indicator study (31 days SPY 1-min, in-sample)
- No edge alone: EMA 9/21 cross, VWAP cross, trend state, FVG formation/retest, pool breaks, ORH/ORL, PDH break, first-hour direction (14/30).
- Fibonacci 50/61.8 first-touch bounce: negative, same as random control levels. Fib is not special (2nd confirmation).
- Candidates (|t|≥2, both halves same sign, ~45 tests so expect ~2 false): 1m RSI<30 dip-buy (+0.17 pts/30m, 57%), PDL break short (+0.79, n=17). Equal-lows sweep-reclaim +0.79 n=11 (too few).
- Midday 15-min SPY move median ~0.25 pts ≈ theta over 1-2h for ATM 0DTE. Movement is front-loaded (0.56 pts 09:30-10:00).

## 2026-10-15 — Intraday deep dig (133 OOS days of 5-min + 20y daily)
- Desk candidates FAILED out of sample: PDL break short −0.44 (flipped), equal-lows sweep-reclaim −0.20; dip-buys +0.07-0.12 pts (below option spread). No intraday direction edge. Don't re-test these without new data.
- Shape of day is reliable: 42% of range by 10:00, 77% by 11:30; day extremes print in the first 30 min (24% H / 32% L) or the last 30 (17/13).
- Gap fill: <0.1% 88%; 0.1-0.3% 64-76%; 0.3-0.6% 31-58%; >0.6% 21-38%; falling since 2016.
- VIX 1σ band holds 65% of days; realized ≈ 0.5-0.8× implied; tagging the edge closes beyond 55%.
- FOMC: 2× day range, ~4.6× 2-4pm range; first reaction unreliable. CPI/NFP priced in the gap.
- Robinhood has no real 5-min bars before 2026 (interpolated filler). Real intraday history grows only by saving bars daily.

## 2026-10-15 — Options-trader tools + Nolan's clock
- SPY pinning to $1 strikes at close: none (164 days). Intraday momentum (first 30m -> last 30m): weak, t 0.7. GEX: vendor-only evidence; collecting daily snapshots.
- Literature: retail 0DTE buyers lose on average (~60% costs); sellers profit after fees.
- Nolan's trips (226, Oct 8-15): before 10:30 negative 5/5 days, after 10:30 positive 5/6. Holds 2-5 min worst; 5-15 min best. 29% wins, +23%/−12% payoff (needs ~35%). Desk ticket warns pre-10:30.

## 2026-10-15 — World markets vs SPY (20y daily + 2y hourly)
- Europe co-moves 0.55-0.60 (overlap hours); Asia 0.1-0.23. US leads Asia (0.34-0.49). Asia/Europe predict the gap, not open-to-close (HSI/KOSPI effect died after 2016; ASX top-quintile +0.04%, t 1.1). After 11:30 ET DAX → SPY afternoon 0.00.
- Lean: Nikkei −2% days → SPY open-to-close +0.10-0.14%, 57-59% up, both halves. Tracking forward in the journal.
- Yahoo chart API works with a browser UA (query2); stooq blocked; Robinhood has no foreign indexes.
- 2026-10-16 Friday desk-study refresh (32 days, 09-02..10-16; ~45 tests, ~2 pass |t|>=2 by luck): no kills (none fell below t 1.5 or flipped). 1m RSI<30 buy weakened t 2.3 -> 2.0-2.1 (+0.10 pts, both halves still positive; still below the option spread per the deep dig). PDL broken -> short holds (30m +0.71, t 2.0). NEW |t|>=2, candidate only: 5m RSI>70 fade (short) 30m +0.23 pts, 70%, t 2.0, n=23/12 days. Intraday deep dig re-run: no GAPFILL/RANGE_DONE change (2 new days, far below the 40-day bar).

## 2026-10-18 — Momentum screen variants (first queen-led swarm, 3 sonnet workers)
- Baseline = live 12-1 screen (mom_screen_base.py): LONG 14 names 9.29% CAGR vs SPY 8.94%; WIDE 41 names 13.79% vs 11.47%. In-sample, survivorship-biased; baseline vs SPY not yet hurdle-tested.
- a. Pullback 3-8% entry: DEAD. LONG -2.95pp t=-3.02 (3/9); only 15% of monthly picks ever dip; waiting = missing the move.
- b. 6-1 lookback: DEAD. LONG -0.09pp t=-0.08 (3/9), WIDE -3.70pp (3/9); 69% top-8 overlap with 12-1.
- c. Top-3 sector rotation: DEAD. LONG -2.61pp t=-2.96 (2/9), cash drag (about 4 candidates for 8 slots).
- Harness lesson: pullback (daily-entry) mode needs a no-same-month-re-buy guard and a signal-day 200d recheck (fixed).
