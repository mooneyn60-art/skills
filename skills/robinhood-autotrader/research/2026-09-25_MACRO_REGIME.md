# Macro Regime: Do the Yield Curve, Fed Policy or Unemployment Condition Returns?

One-line: RESEARCH_AGENDA item 2. Test whether the three most-watched macro
signals say anything about the NEXT MONTH for stocks, and whether the curve
matters for banks.

Last Updated: 2026-09-25
Status: DONE. Prediction committed first (3bc58a8). No macro signal times next month's return.
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

## Answer first

- NONE OF THE FOUR MACRO SIGNALS PREDICTS NEXT MONTH'S STOCK RETURN.
  Every return difference has |t| < 1.3 over 38 years, and the signs flip
  from window to window.
- ONE THING DOES SHOW UP: when unemployment has started rising, the
  following month is MORE VOLATILE: 19.7% annualised against 14.2%,
  t = 3.87, still t = 3.39 without 2008 and 2020. Macro tells you how
  rough the ride will be, not which way it goes.
- The inverted curve, the most famous recession signal, came before
  slightly BETTER next months (+0.42pp, t = 0.68). Its lead is 12-18 months
  to a recession, and markets often rally in between.
- For banks, a steepening curve helps on average (+1.18pp a month over the
  S&P) but with t = 0.90, and positive in only 5 of 9 windows. Not a
  signal.

## Result

Script: paper/test_macro_regime.py. S&P 500 total return 1988-2026; banks
2006-2026. Monthly samples, forward 21 trading days.

    test                                  ON  OFF  diff     t      halves (t)      9 windows       w/o 2008+2020
    G1 curve inverted (T10Y3M<0)          60  404  +0.42pp +0.68  +0.64 / +0.42   + . - + + . . - +   +0.77pp t=+1.42
    G2 Fed cutting                        214 250  -0.49pp -1.20  -1.44 / -0.39   - - + - - + - + -   -0.32pp t=-0.81
    G3 unemployment rising: return        93  362  -0.44pp -0.74  -1.14 / -0.14   + - . - - - . + +   -0.26pp t=-0.45
    G3 unemployment rising: volatility    93  362  +5.44pt +3.87  +1.94 / +3.45   - + . + + + . + -   +3.62pt t=+3.39
    G4 steepening: BAC+C minus S&P        112 133  +1.18pp +0.90  +0.81 / +0.45   + + - - + - + + -   +2.31pp t=+1.71
    ("." = window with no ON months)

## Scored against the prediction

    G1 inverted slightly worse, |t|<2: |t|<2 RIGHT; direction WRONG (slightly better).
    G2 no meaningful difference, |t|<1.5: RIGHT (t=-1.20).
    G3 lower returns |t| 1-2: returns lower but t=-0.74, WEAKER than predicted;
       volatility clearly higher: RIGHT (t=3.87).
    G4 +0.3 to +0.8pp, t 1-2: bigger point estimate (+1.18pp), weaker t (0.90). Mixed.
    Overall "nothing clears as a one-month return signal": RIGHT.

G1's direction miss refutes part of a stated hypothesis, so R16 (c) is
on for the rest of this session. Nothing gets adopted.

## What this means for TARS (interpretation)

- Don't add a macro filter to entries. There is no return edge to capture.
- The unemployment-volatility link is real and fits volatility clustering.
  Its practical use would be SIZING (smaller positions when unemployment
  is turning up), not timing. It is a candidate for agenda item 10
  (sizing), not a rule. Any use of it would need the four hurdles run as
  a sizing test, plus the multiple-testing hurdle from item 8.
- For NWG and SOFI, "rates up/curve steeper is good for banks" is a
  reasonable story with weak evidence: +1.18pp a month, t=0.90.
