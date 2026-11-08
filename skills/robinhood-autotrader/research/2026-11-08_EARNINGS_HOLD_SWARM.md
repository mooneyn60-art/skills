# Hold Through Earnings or Sell Before? (Swarm Queue Item 4)

One-line: For names the momentum screen would hold (above the 200-day,
positive 12-1 momentum), is the earnings reaction worth sitting through, or
does selling the day before avoid more harm than it gives up?

Last Updated: 2026-11-08
Status: DESIGN + PREDICTION (committed before any result). Results below once run.
Audience: Nolan, TARS sessions

## Why now, and why not items 2 or the R15 task

- R15 task: skipped. R16 trigger (b) can't be verified OFF: no high-water-mark
  rebase row exists after the 10/15 R6 drawdown halt, and PLTR (11/2) and
  NVDA (11/5) both closed at a loss on stops within 5 days (owner positions;
  if R6 counts them, the circuit breaker runs to about 11/10).
- Item 2 (Options Apprentice Stage 2): still blocked; paper/history/owner_trips.json
  has not been committed.
- Item 4 is live-relevant: BE (10/22) and ASX (10/15 pre-market gap) both
  went straight through their stops on news, and the book holds names
  reporting soon.

## Data

- Earnings dates and timing: paper/history/earnings_reports.json (8 names)
  plus earnings_reports_wide.json (33 names, fetched 2026-11-08 via
  Robinhood get_earnings_results; trailing up to 8 quarters each, so about
  2024-2026 only). About 300 events at most. This is a 2-year sample.
- Prices: daily_ohlcv*.json.

## Test (fixed before running)

- Event day: for "am" reports the reaction is close(d-1) -> close(d); for
  "pm" it's close(d) -> close(d+1). "Sell before" exits at the last close
  before the reaction; "hold" keeps the position through it.
- Momentum names: at the pre-reaction close, close > 200-day SMA AND 12-1
  momentum > 0 (the live screen's core). Others are the control.
- Measures, per event: reaction return R (the gap day), the share of events
  where R would have gone through an 8% stop (R <= -8%), and post-event drift
  over the next 20 trading days (does a sell-before investor miss it?).
- Hold-through value = mean R (that's what selling before forgoes). With
  stops, the downside is capped only if there's no gap; the gap is the point.
- Splits: momentum vs not; first year vs second year; megacaps vs the rest;
  t on per-event R. Bootstrap the mean with 10,000 resamples clustered by date.

## PREDICTION

- Momentum names' mean reaction R between -0.5% and +1.5%, |t| < 2
  (earnings gaps are close to fair bets; there's a small positive drift in
  the literature for winners, e.g. post-earnings drift).
- About 10-15% of momentum-name events gap 8%+ against the holder (through
  the stop), more for the volatile names than for the megacaps.
- No reliable difference between momentum names and the rest (|t| < 2).
- Verdict expected: neither rule is clearly better on mean; selling before
  only cuts tail risk. That makes it a sizing question, not an edge, which goes
  to Nolan as information.
