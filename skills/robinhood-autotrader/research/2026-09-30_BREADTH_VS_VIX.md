# Market Breadth: Does It Add Anything VIX Doesn't?

One-line: RESEARCH_AGENDA item 11. When fewer stocks are above their 200-day,
is the next month worse or rougher for the market, and does that tell us
anything VIX didn't already?

Last Updated: 2026-09-30
Status: DONE. Prediction committed first (37980e7); the volatility half was wrong.
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

## Answer first

- BREADTH SAYS NOTHING ABOUT NEXT MONTH'S RETURN, with or without VIX
  (t = +0.19 alone, +1.43 with VIX; the sign flips window to window).
- BREADTH DOES SAY SOMETHING ABOUT NEXT MONTH'S ROUGHNESS, and a little of
  it is not in VIX. On its own, low breadth predicts higher volatility
  (t = -8.77). With VIX in the same regression most of that goes to VIX
  (VIX t = +8.32), but breadth keeps t = -2.80, negative in 8 of 9 windows
  and t = -3.22 without 2008 and 2020.
- It is SMALL and FADING: the breadth effect is t = -2.29 in 2006-2016
  and -1.48 in 2016-2026. Going from 90% of names above their 200-day to
  30% adds about 5 points of annualised volatility beyond what VIX says.
- It does not clear the |t| >= 3.9 hurdle from item 8. Nothing adopted.
  If it's ever used, it belongs in SIZING (smaller positions when breadth
  is narrow), not timing, alongside item 2's unemployment-volatility link.

## Result

Script: paper/test_breadth_vs_vix.py. 238 months, 2006-11 to 2026-08. Breadth
averaged 0.62; below 0.30 in 33 months, above 0.70 in 117.

                             forward return                      forward volatility
                             breadth alone   breadth (+VIX)      breadth alone   breadth (+VIX)   VIX t
    full                     t=+0.19         t=+1.43             t=-8.77         t=-2.80          +8.32
    first half               t=+0.80         t=+1.20             t=-7.47         t=-2.29          +5.71
    second half              t=-0.80         t=+0.56             t=-4.55         t=-1.48          +5.70
    without 2008 and 2020    t=-0.84         t=+0.23             t=-8.44         t=-3.22          +8.15
    9 windows, sign (+VIX)   + - + - + - + + +                   - - - - - + - - -

    Volatility coefficient with VIX: -0.083 per unit of breadth (1.0 = all 14 above).

Side note, not pre-registered and not tested for robustness: in the return
regression VIX itself has t = +2.09 (higher VIX, higher next month), the
familiar "fear is paid" pattern. It's recorded, not claimed.

## Scored against the prediction

    B1 returns: breadth alone |t|<2 RIGHT (0.19); with VIX |t|<1.5 RIGHT (1.43).
    B2 volatility: breadth alone |t|>2 RIGHT (8.77); with VIX |t|<2 WRONG (2.80).
    "Breadth adds nothing": WRONG for volatility, a little is left over. RIGHT for returns.

R16 trigger (c) is on for the rest of this session.

## Caveats

Breadth from 14 surviving large caps is a crude stand-in for S&P 500
breadth (item 5 describes the free point-in-time membership data that
would allow a proper version). R15 is recorded in TARS_RULES.md as live;
research/2026-09-26_R15_INTEGRATION.md recommends repealing it, pending
Nolan.
