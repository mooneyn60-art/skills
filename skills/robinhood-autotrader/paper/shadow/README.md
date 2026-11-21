# Shadow Book

One-line: TARS's rules run mechanically on paper every trading day, so the
system builds a clean, forward-only, discretion-free track record at zero
risk.
Last Updated: 2026-09-27
Status: LIVE since 2026-09-25 close (day zero). Runs at the desk's 5:17pm ET close check.
Audience: Nolan, TARS sessions

## Overview

Why: 33 live trades can't judge a system. Most were hand-closed or
discretionary, and backtests carry survivorship bias. A forward paper book
has neither problem. Every future day is out of sample, and the universe is
whatever the market offers that day, dead-stocks-to-be included.

Universe: Robinhood saved scan "TARS shadow universe"
(scan_id 82b6b119-03ea-49ff-9e5b-4dc747bd2918): US stocks, market cap
> $10B, price > $5, 30-day average volume > 1M, above their 200-day. It
returns the top 200 by price / 200-day SMA (about 340 pass on 2026-09-25).

Two books, one snapshot per day:
- **tars1**: R2 entry (above the 200-day, no earnings within ~3 trading days,
  at most 2 per sector), ranked by distance above the 200-day (the momentum
  rule committed 2026-09-25), R3 sizing (20% per position, 15% cash floor, 8%
  risk budget), R4 exits (8% stop, breakeven at +8%, 20% trail) plus the
  200-day trend exit.
- **trend_only**: same entries and sizing, exits only on a close below the
  200-day.
- Benchmark: SPY from the same close.

Known simplifications: NAV weights, not whole shares (R12 isn't simulated).
Fills at the close with 0.10% cost per side. Stops judged on closes, not
intraday lows. R15 (the VIX >= 25 inversion) isn't simulated in v1; VIX is
logged so it can be added.

Files: shadow_book.py (engine), state.json (positions), nav.csv (daily NAV),
log.jsonl (every entry and exit), daily/DATE.json (the snapshot used; raw
scans are not committed).

## Predictions (committed before any forward data exists, R14.1)

P1 Over the first 3 months, tars1 trails SPY. Buying the most extended
   names is volatile, and the 8% stop gets hit a lot.
P2 trend_only beats tars1 over 3 months, matching the 2026-09-24 bracket
   research: tight stops cost more than they save.
P3 Both books are at least 1.5x as volatile as SPY day to day.
P4 Day-zero picks (MRNA +208% above its 200-day, TXG +160%) are extreme.
   At least 2 of the 4 exit tars1 within 30 trading days.
Scored at 2026-12-31 and at 63 trading days, whichever comes first.
