# Macro Regime: Do the Yield Curve, Fed Policy or Unemployment Condition Returns?

One-line: RESEARCH_AGENDA item 2. Test whether the three most-watched macro
signals say anything about the NEXT MONTH for stocks, and whether the curve
matters for banks.

Last Updated: 2026-09-25
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
Audience: Nolan, TARS sessions

## Data

- FRED (fetched 2026-09-25, paper/history/fred_macro.json): T10Y3M and
  T10Y2Y (daily), FEDFUNDS and UNRATE (monthly).
- Monthly series are used with a TWO-MONTH lag: on the first trading day of
  month X only month X-2's value is used, because month X-1's figure may
  not be published yet (unemployment comes out on the first Friday).
  Daily curve values: the prior trading day's.
- S&P 500 total return (^SP500TR, paper/history/options_indices.json),
  1988-2026. Banks: BAC and C from paper/history/daily_stocks.json, 2006+.

## Tests (only these four; fixed before running)

Monthly samples, first trading day, forward 21 trading days (non-overlapping).
G1  Curve inverted (T10Y3M < 0) vs not: S&P forward return.
G2  Fed cutting (FEDFUNDS lower than 6 months earlier) vs not.
G3  Unemployment rising (UNRATE at least 0.5pt above its trailing 12-month
    low, a Sahm-style trigger) vs not: S&P forward return AND forward
    realised volatility.
G4  Curve steepening (T10Y2Y up over the prior 63 trading days) vs not:
    mean of BAC and C forward return MINUS the S&P's.
Each: difference in means, Welch t; split halves; 9-window walk-forward
(sign of the difference); drop 2008 and 2020 (the two crash years) as the
"drop the big ones" hurdle.

## PREDICTION

G1: inverted months slightly worse, |t| < 2. The curve's known lead is
    12-18 months to recession, not one month to returns.
G2: no meaningful difference, |t| < 1.5. Cuts often come in crises, so
    "cutting" mixes rescues with panics.
G3: rising unemployment -> lower returns and higher volatility; return
    |t| 1-2, volatility difference clearly positive.
G4: steepening helps banks by +0.3 to +0.8pp a month, t about 1-2.
Overall: NOTHING clears the four hurdles as a one-month trading signal.
Macro describes the weather; it doesn't time next month.

## Result

(not yet run)
