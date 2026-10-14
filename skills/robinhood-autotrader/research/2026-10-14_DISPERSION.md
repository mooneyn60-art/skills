# Dispersion: Does How Far Apart the Names Move Predict Anything?

One-line: Wednesday contrarian probe. Not the level of returns or volatility,
but their SPREAD across the 14 names. Does it predict the market, its
volatility, or whether TARS's 200-day selection pays?

Last Updated: 2026-10-14
Status: DONE. Nothing becomes a rule. The best result (dispersion -> weaker 200-day payoff, t=-3.03) passes the committed hurdles but misses |t|>=3.9 and disappears without 2008-09 (t=-0.98). Prediction committed first (afee93f).
Audience: Nolan, TARS sessions

## Overview

The research agenda (items 1-24) is complete, so the Wednesday probe is free
to choose. Dispersion has never been tested here (grep of research/: only an
incidental mention). It is not a moving average, a momentum ranking or a
price channel. It is close to a volatility measure, which is why every test
below controls for VIX.

## Mechanism (written before the test)

High dispersion means the names are moving on their own news rather than
together. Two published claims (from memory, being checked by a sub-agent,
UNVERIFIED until then):
1. Dispersion is a proxy for idiosyncratic risk and uncertainty, so it
   predicts higher future market volatility (Stivers 2003 and successors).
2. Lagged high dispersion is followed by a WEAKER momentum premium (Stivers &
   Sun 2010). TARS's 200-day gate is a trend/momentum filter, so if this
   holds, the gap between names above and below their 200-day should shrink
   after high-dispersion months. That would be a reason to size down.

## Test (fixed before running)

- Data: paper/history/daily_stocks.json (14 names + SPY, 2006-2026),
  vix_weekly.json (value dated at least 7 days before, as in item 11).
- Monthly samples, first trading day. Signal D = mean over the prior 21
  trading days of the cross-sectional standard deviation of the 14 daily
  log returns.
- Outcomes over the next 21 trading days:
  (a) SPY return;
  (b) SPY realised volatility (annualised);
  (c) the 200-day spread: mean forward return of names above their 200-day
      SMA minus names below (the same construction as audit Q4).
- OLS of each outcome on D alone, then on D + VIX. Classical t (monthly
  samples don't overlap).
- Hurdles: split halves; sign of the D coefficient (with VIX) across 9
  windows (>= 5/9 the same sign as the full-sample one); drop the megacaps
  (D and the spread recomputed on the 9 non-megacap names);
  multiple-testing bar |t| >= 3.9 for anything that would become a rule.

## PREDICTION

- (a) Market return: nothing. |t| < 2 with VIX, and probably alone too.
- (b) Volatility: D predicts forward vol alone (t > 3), but adding VIX
  absorbs most of it (D's t < 2 with VIX).
- (c) 200-day spread: negative coefficient (high dispersion, weaker trend
  payoff), t between -1 and -2.5. Does NOT clear |t| >= 3.9.
- Overall: nothing becomes a rule.

## Results (python3 paper/test_dispersion.py, run 2026-10-14)

238 monthly samples, 2006-12 to 2026-09, 14 names. D averages 1.47% a day
(range 0.70-4.78). corr(D, VIX) = +0.74, so the controlled column matters.
Coefficients are per 1pp of D. All in-sample OLS, mechanical construction,
nothing fitted.

| Outcome | D alone t | D with VIX t | 1st half / 2nd half (with VIX) | Megacaps dropped (with VIX) | 9-window sign |
|---|---|---|---|---|---|
| (a) SPY fwd 21d return | -0.32 | -2.21 | -1.38 / -1.14 | -1.20 | 6 of 9 negative |
| (b) SPY fwd 21d vol | +10.43 | +2.82 | +2.98 / +0.01 | +1.77 | 7 of 9 positive |
| (c) 200-day spread | -2.90 | **-3.03** | -2.52 / -2.05 | -2.93 | 6 of 9 negative |

Post hoc (added after the first run, labelled as such in the script):

| Check | (a) return | (b) vol | (c) 200d spread |
|---|---|---|---|
| excluding 2008-2009 | -1.50 | +0.97 | **-0.98** |
| excluding 2020 | -2.36 | +3.89 | -2.92 |

Spread by D tercile (no VIX control): low D +1.45pp a month (t=+2.72),
middle +1.14pp (t=+1.47), high D -1.15pp (t=-1.27).

## Reading it

- (c) is the interesting one. It runs in the direction Stivers & Sun (2010,
  JFQA) report: after high dispersion, the trend/momentum payoff is weaker.
  On the pre-committed hurdles it passes the halves (both negative,
  |t| > 2), walk-forward (6 of 9) and the megacap drop (t=-2.93). It fails the
  multiple-testing bar (|t| 3.03 < 3.9). The post hoc check is decisive:
  **without 2008-09 the t falls to -0.98.** The effect is the 2009 momentum
  crash (the 200-day losers rebounded hardest just as dispersion peaked).
  That's a documented crash, and the literature says it happens, but it's
  one episode in our data, not a monthly regularity we can size on.
- (b) Dispersion carries some volatility information that VIX doesn't, but
  only in 2006-2016. In 2016-2026 it adds nothing (t=+0.01), and without
  2008-09 it adds nothing (t=+0.97). VIX already does this job.
- (a) The full-sample t=-2.21 with VIX doesn't hold in either half, the
  megacap drop, or without 2008-09. Noise. (Maio 2016, J. Financial Markets,
  reports a negative sign; Garcia et al. 2014 reportedly a positive one.
  The literature doesn't agree either.)

## Prediction scorecard

- (a) return |t| < 2 with VIX: WRONG on the full sample (-2.21), right in
  every robustness cut. Scored wrong.
- (b) vol t > 3 alone: RIGHT (+10.43). VIX absorbs it (t < 2): WRONG on the
  full sample (+2.82), right for the second half and the megacap drop. Scored
  wrong.
- (c) negative, t between -1 and -2.5: sign RIGHT, size WRONG (-3.03, stronger).
- Nothing becomes a rule: RIGHT.

## What to keep

- Dispersion joins the list of things tested and not usable as a rule.
- One practical note, not a rule: in a crash-and-rebound like 2009, the
  200-day gate keeps TARS out of the names that bounce hardest. Dispersion
  spiking well above 3% a day (it reached 4.78 in 2008) marks that kind of
  market. Any future crash-regime work should start from this note.

## Literature (haiku sub-agent, abstracts only, not full texts)

Stivers & Sun 2010 JFQA 45(4) (negative dispersion -> momentum, confirmed in
abstract); Stivers 2003 J. Financial Markets (dispersion -> future vol);
Maio 2016 J. Financial Markets (negative -> equity premium, OOS claimed);
Garcia, Mantilla-Garcia & Martellini 2014 JFQA (sign UNVERIFIED). No study
was found that races dispersion against VIX. No failed replications were found.
