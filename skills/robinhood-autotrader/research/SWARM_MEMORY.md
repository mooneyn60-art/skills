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
