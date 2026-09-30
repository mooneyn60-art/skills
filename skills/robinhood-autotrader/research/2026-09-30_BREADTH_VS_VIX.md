# Market Breadth: Does It Add Anything VIX Doesn't?

One-line: RESEARCH_AGENDA item 11. When fewer stocks are above their 200-day,
is the next month worse or rougher for the market, and does that tell us
anything VIX didn't already?

Last Updated: 2026-09-30
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
Audience: Nolan, TARS sessions

## Mechanism (stated before the test)

Breadth measures participation: a market held up by a few names is fragile,
so narrow breadth might come before weaker or more volatile months. The
case against: VIX already prices fear, and breadth mostly falls AFTER a
sell-off has started, so it may add nothing.

## Data and tests (fixed before running)

Breadth = share of the 14 backtest names closing above their own 200-day
SMA (paper/history/daily_stocks.json). This is a crude proxy for S&P 500
breadth: 14 survivors, not 500 stocks. VIX: vix_weekly.json, value dated
at least 7 days earlier. Sample: first trading day of each month, forward
21 trading days of SPY (non-overlapping), 2007-2026.

B1  Forward SPY RETURN regressed on breadth, then on breadth + VIX:
    breadth coefficient and t in each.
B2  Forward SPY realised VOLATILITY, same two regressions.
Hurdles for the breadth coefficient in the "+ VIX" regressions: split
halves, 9-window sign count, drop 2008 and 2020. Adoption would further
need |t| >= 3.9 (item 8); nothing is adopted this session.

## PREDICTION

B1: breadth alone |t| < 2 for returns; with VIX, |t| < 1.5. No return signal.
B2: breadth alone predicts volatility (low breadth -> higher vol, |t| > 2),
    but once VIX is in the regression breadth's t falls below 2: VIX
    already carries the information.
Verdict expected: breadth adds nothing R15 or TARS needs.

## Result

(not yet run)
