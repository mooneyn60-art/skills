# Sell Before Earnings, Rebuy After: 20-Year Backtest

One-line: Follow-up to research/2026-11-08_EARNINGS_HOLD_SWARM.md (2 years,
lean: sit out earnings). This rebuilds 20 years of earnings dates from SEC 8-K
Item 2.02 filings and backtests the live momentum screen with and without an
earnings exit.

Last Updated: 2026-11-15
Status: DESIGN + PREDICTION (committed before the data was built or run). Results below once run.
Audience: Nolan, TARS sessions

## Housekeeping this run

- R15 task skipped a 3rd week: still no high-water-mark rebase row after the
  10/15 R6 halt, so R16 (b) can't be verified OFF. This needs the desk (log the
  rebase) or Nolan (decide R15 directly). Flagged to Nolan.
- Swarm queue: item 2 still blocked (owner_trips.json not committed); item 5
  (ICT sweep / FVG) is already answered by earlier tests (desk study 133-day OOS:
  FVG/PDL/equal-lows sweeps no edge; godmode_test 10/16: sweep -0.05 pts,
  34% wins, n=621 OOS; sweep+CHoCH failed OOS), so it's marked covered and not
  re-derived. This item is added as 4b.

## Data (built this run)

- Earnings dates: SEC EDGAR submissions (data.sec.gov), 8-K filings whose
  items include 2.02 ("Results of Operations"), 2006-2026, for the 14 LONG
  names. Timing from the acceptance time: before 09:30 ET = "am" (reaction
  close d-1 -> close d), at or after 16:00 ET = "pm" (reaction close d ->
  close d+1), during the session = "am" (reaction already in day d's close).
  Saved to paper/history/earnings_8k.json.
- Prices: daily_ohlcv.json. Harness: paper/research_scripts/mom_screen_base.py.

## Variants (live momentum screen, LONG 14 names, 2007-2026)

- A: baseline harness, no earnings handling.
- B: live rule, no new entry if a reaction falls within the next 3 trading days.
- C: B plus an exit: sell at the close before each reaction, and rebuy at the next
  open after the reaction day if the name is still eligible (above the
  200-day, momentum > 0) and a slot is free.

## PREDICTION

- B vs A: within +/-1pp CAGR (the entry skip changes little).
- C vs B: CAGR within +/-1.5pp; max drawdown slightly shallower (removes gap
  tail); daily t < 2; walk-forward 3-6 of 9. Not a rule.
- Event level (all 14 names, 20 years, momentum-eligible events): mean
  reaction between -0.5% and +0.5%, and about 8-12% of events with a reaction
  of -8% or worse. That's fewer than the 2025-26 volatile set (14.8%), because these
  are mostly megacaps.
