# Do Congress Members' Disclosed Trades Predict Returns We Could Capture?

One-line: Wednesday contrarian probe. Members of Congress disclose trades
up to 45 days late (STOCK Act). If their buys beat their sells after the
DISCLOSURE date, a copycat could profit. Never tested here.

Last Updated: 2026-11-18
Status: DESIGN + PREDICTION (committed before any data was fetched). Results below once run.
Audience: Nolan, TARS sessions

## Mechanism and literature (written before the test)

Lawmakers may trade on policy knowledge (Ziobrowski et al. 2004, JFQA: Senate
portfolios beat the market by about 12% a year in 1993-98). Against:
Eggers & Hainmueller 2013 (J. Politics): 2004-08 House portfolios
underperformed, and later studies found little. Copycat apps and ETFs
(NANC/KRUZ) exist, which is a sign the easy version is crowded. And the
disclosure lag means a copier buys up to 45 days late.

## Test (fixed before running)

- Data: Robinhood get_politician_trades (source: Tip Ranks, STOCK Act
  disclosures) for the 41 names in our price files, one call each. That's about 25
  most recent trades per name, roughly 2025-10 to 2026-11. Saved to
  paper/history/politician_trades.json.
- Event: each disclosed BUY or SELL. Entry = close of the first trading day
  AFTER disclosure_date (what a copier could do). Outcome = the stock's 21-
  trading-day return minus SPY's over the same days.
- Statistic: mean excess for BUYs, for SELLs, and BUY minus SELL (Welch t).
  Also the same from transaction_date (what the politician got, not tradeable),
  to see whether any edge exists before the lag eats it.
- Subgroups: amount above vs at $1k-15k (bigger bets more informed?); party;
  megacaps vs rest. Split halves by disclosure date.
- Caveats fixed now: about 1 year of data, overlapping windows (events on the
  same stock days apart share returns), so t is optimistic. Prices end
  2026-11-13, so events need disclosure before about 2026-10-13.

## PREDICTION

- Copy-at-disclosure: BUY minus SELL 21-day excess within +/-1.5pp, |t| < 1.5.
- From transaction date: slightly larger, still |t| < 2.
- Large-amount trades: no different from small ones (|t| < 1.5).
- Dead for TARS.
