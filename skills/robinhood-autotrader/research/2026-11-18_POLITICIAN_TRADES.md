# Do Congress Members' Disclosed Trades Predict Returns We Could Capture?

One-line: Wednesday contrarian probe. Members of Congress disclose trades
up to 45 days late (STOCK Act). If their buys beat their sells after the
DISCLOSURE date, a copycat could profit. Never tested here.

Last Updated: 2026-11-18
Status: DONE. Dead for copying: after disclosure, their buys did WORSE than their sells (-0.83pp over 21 days, t=-0.38, n=171). From the trade date (not copyable): +2.41pp, t=+1.35. Prediction committed first (6e36dce); all lines right.
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

## Data check

257 BUY/SELL trades on 25 of our names (14 names had none; ROKU not found),
2025-09 to 2026-11, 171 with a full 21-day window after disclosure. A
worker transcribed the tool output by hand (the tool couldn't write raw
files), so two names were checked against raw pulls made in this session:
MSFT 25/25 and NVDA 20/20 rows identical.

## Results (python3 paper/research_scripts/politician_trades.py)

21-day return minus SPY, entering at the first close after the date.
Overlapping windows (many trades on the same few megacaps within weeks), so
the t-stats are optimistic.

| Cut (after disclosure) | BUY n / mean | SELL n / mean | BUY - SELL | t |
|---|---|---|---|---|
| **All** | 73 / +2.05% | 98 / +2.87% | **-0.83pp** | **-0.38** |
| 1st half | 39 / +3.30% | 46 / +5.09% | -1.79pp | -0.50 |
| 2nd half | 34 / +0.61% | 52 / +0.92% | -0.31pp | -0.12 |
| Amount > $15k | 11 / +0.49% | 26 / +4.34% | -3.85pp | -0.86 |
| Amount $1k-15k | 62 / +2.32% | 72 / +2.35% | -0.02pp | -0.01 |
| Democrats | 48 / +4.12% | 47 / +4.13% | -0.01pp | -0.00 |
| Republicans | 25 / -1.93% | 51 / +1.71% | -3.65pp | -1.65 |
| Megacaps | 34 / +0.81% | 45 / +2.51% | -1.70pp | -0.97 |
| Non-megacaps | 39 / +3.13% | 53 / +3.18% | -0.05pp | -0.01 |
| **From transaction date (not tradeable)** | 91 / +3.69% | 123 / +1.28% | **+2.41pp** | +1.35 |

## Reading it

- Nothing to copy. After disclosure, buys and sells did about equally well;
  if anything the stocks they SOLD did better.
- Both buys and sells beat SPY by 2-3%. That's not their skill: it's
  the names they trade (big tech, AMD, MU) outrunning the index this year.
  The BUY-minus-SELL column removes that and finds nothing.
- From the actual trade date there's a +2.4pp hint (t=1.35), which is
  consistent with a small, maybe-real information edge that the 27-day
  disclosure lag gives away. Not significant on 1 year.
- The "large trades are smarter" idea runs backwards here (-3.85pp), on only 11
  large buys.
- Limits: 1 year, one page per stock from one vendor, overlapping windows,
  mostly megacaps. A clean null for a copier on this data, not a final word.

## Prediction scorecard

- Copy-at-disclosure BUY-SELL within +/-1.5pp, |t| < 1.5: RIGHT (-0.83pp, t=-0.38).
- From the transaction date slightly larger, |t| < 2: RIGHT (+2.41pp, t=+1.35).
- Large trades no different, |t| < 1.5: RIGHT (t=-0.86).
- Dead for TARS: RIGHT.
