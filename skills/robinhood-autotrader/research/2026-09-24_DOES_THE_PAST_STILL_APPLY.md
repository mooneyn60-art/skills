# Does the Past Still Apply? Pattern Decay and TARS's Live Rules

One-line: RESEARCH_AGENDA item 20. How fast do market patterns decay after
discovery, and which of TARS's live rules rest on evidence most at risk of
being out of date?

Last Updated: 2026-09-24
Status: PREDICTION COMMITTED, TEST NOT YET RUN
Audience: Nolan, TARS sessions

## Data test (fixed before the run)

The rule everything rests on is R2's 200-day gate. Test it era by era on
paper/history/daily_stocks.json (14 names + SPY, 2006-2026), sampled on the
first trading day of each month (non-overlapping 21-day forward returns):
  D1  per stock: forward 21-day return when the close is ABOVE its 200-day
      minus when BELOW; per era (2007-2011, 2012-2016, 2017-2021,
      2022-2026), mean spread and t across months.
  D2  the same for SPY alone, plus the forward 21-day return volatility
      above vs below (the "avoid the crashes" half of the argument).

## PREDICTION

- D1: the above-minus-below spread is small and inconsistent across eras,
  |t| < 2 in most eras. A trend gate does not pick better stocks month to
  month on these names.
- D2: SPY's forward volatility is clearly HIGHER below the 200-day in every
  era (ratio > 1.3). Its forward RETURN is not reliably lower.
- Interpretation I expect: R2's value, if any, is avoiding high-volatility
  periods rather than adding return, and that part is the least likely to
  decay because it comes from volatility clustering, one of the most
  robust facts in finance.

## Result

(not yet run)
