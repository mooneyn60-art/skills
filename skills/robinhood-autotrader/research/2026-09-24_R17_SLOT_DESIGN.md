# R17 Slot Design: Bracket vs Hold, and Which Contracts Lose Least

One-line: R17 is live. Does Nolan's bracket (-20% stop, +25% ratchet) help or
hurt 60+ DTE calls, and which expiry and delta lose the least?

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (060c26f).
Audience: Nolan, TARS sessions

## Overview

R16 trigger (c) is ON in the session that wrote this (the RSI test refuted
one of TARS's stated predictions). Under R16.3, nothing here is adopted
before the weekend re-read, whatever it finds.

Method: simulated option prices (Black-Scholes) on real daily stock paths,
paper/history/daily_stocks.json, 14 large caps, 2006-2026. IV = trailing
20-day realized vol x 1.15 (a volatility premium; real options are richer
than realized on average), plus a round-trip spread cost. The model has no
skew and no earnings IV crush, so absolute returns are only a rough guide.
The COMPARISONS between exits on the SAME paths are the point.
Survivorship: the universe is 2026's winners. That flatters calls.

## Predictions (written before the test)

P1 BRACKET vs HOLD: on the same paths, Nolan's bracket has a LOWER mean
   return per trade than holding to the 21-DTE time exit. A 60+ DTE option
   moves about 3x the stock in percent, so a -20% stop gets hit by ordinary
   noise, about a 6-7% stock dip. The bracket cuts the worst losses (stopped
   trades average near -25%, not -100%) but costs more in mean than it
   saves. Expect the bracket's win rate to be HIGHER, with smaller wins.
P2 EXPIRY: per trade, 120-180 DTE loses less to decay than 60 DTE and has a
   better mean return.
P3 DELTA: delta 0.50-0.60 has a better mean return per dollar than 0.30
   (less paid for lottery odds), once the volatility premium is priced in.
P4 TREND FILTER: buying calls only when the stock is above its 200-day
   changes the mean by less than the bracket-vs-hold difference.

What would prove P1 wrong: the bracket beats hold-to-time-exit on mean
return by 2pp+ per trade with t > 2, in both halves of the sample.

## Results

Simulation script: `paper/research_scripts/r17_slot_design.py`. 14 symbols x
519 entry dates per DTE (every 10th trading day, 2006-2026) = 7,266 trades
per (DTE, delta) cell, run through all three exit policies on the same
entries. Full run log kept alongside this doc's authoring session; anyone
can reproduce with `python3 paper/research_scripts/r17_slot_design.py`.

### Default cell (90 DTE, 0.45 delta)

| Policy | n | Mean | Median | Win% | Stop% |
|---|---|---|---|---|---|
| Hold (time exit) | 7266 | +8.37% | -52.18% | 33.9% | – |
| Bracket (Nolan's) | 7266 | -5.75% | -23.18% | 20.2% | 99.7% |
| No-stop ladder | 7266 | -2.39% | -6.68% | 39.5% | 60.1% |

Bracket's 99.7% "stopped" share splits into two very different mechanisms:

| Bracket, stopped trades (n=7247) | share | mean return |
|---|---|---|
| Loss stop (hit -20% floor / a ratchet level still below cost) | 80.0% | -26.15% |
| Gain stop (ratchet had already locked in a profit) | 20.0% | +74.81% |

33.7% of all bracket-stopped trades (2,445 of 7,247) would have shown a
*positive* return if simply held to the time exit instead (mean would-be
hold return of stopped trades: +8.20%, vs the -5.95% they actually banked
pooling both stop types).

Paired bracket-minus-hold, same entries, default cell:
- Full sample (n=7266): mean diff **-14.11 pp**, **t = -8.40**
- Pre-2016-06-01 (n=3640): mean diff **-8.67 pp**, **t = -3.84**
- Post-2016-06-01 (n=3626): mean diff **-19.58 pp**, **t = -7.87**

Trend filter (P4), default cell:

| Subset | n | Hold mean | Bracket mean | Bracket - Hold |
|---|---|---|---|---|
| Above 200-SMA at entry | 4384 | +16.78% | -4.36% | -21.14 pp |
| Below 200-SMA at entry | 2630 | -7.32% | -7.82% | -0.50 pp |

Trend swing in HOLD mean (above minus below) = **+24.10 pp** — bigger than
the -13.40 pp bracket-vs-hold diff on this same SMA-eligible subset (n=7014,
t=-7.83). Trend swing in BRACKET mean (above minus below) = **+3.46 pp** —
smaller than that -13.40 pp.

SPY benchmark, mean return over the same trade window:

| DTE | n | Mean SPY return | Median |
|---|---|---|---|
| 60 | 519 | +1.00% | +1.62% |
| 90 | 519 | +1.87% | +2.66% |
| 120 | 519 | +2.73% | +4.05% |
| 180 | 519 | +4.31% | +5.44% |

### Full grid (all DTE x delta x policy)

```
 DTE  delta   policy     n     mean   median   win%  stop%  stopmean stop_hold_mean  recov%
  60   0.30     hold  7266     4.56   -63.25   29.1    n/a       n/a            n/a     n/a
  60   0.30  bracket  7266    -7.82   -24.93   19.1   99.8     -8.11           4.29    28.9
  60   0.30   nostop  7266    -5.82   -14.79   35.6   55.1     46.52          65.37    47.3
  60   0.45     hold  7266     3.90   -42.68   34.9    n/a       n/a            n/a     n/a
  60   0.45  bracket  7266    -6.51   -23.71   20.1   98.9     -7.87           2.65    34.3
  60   0.45   nostop  7266    -3.72   -11.23   37.8   52.8     39.49          53.90    54.2
  60   0.60     hold  7266     3.53   -25.00   39.6    n/a       n/a            n/a     n/a
  60   0.60  bracket  7266    -5.32   -23.15   21.3   96.2     -9.43          -0.23    37.4
  60   0.60   nostop  7266    -1.50    -8.15   39.2   47.8     32.51          43.04    58.0
  90   0.30     hold  7266     8.95   -77.01   27.3    n/a       n/a            n/a     n/a
  90   0.30  bracket  7266    -6.67   -23.61   19.5  100.0     -6.68           8.94    27.3
  90   0.30   nostop  7266    -5.04    -9.21   38.2   60.4     45.11          68.26    42.8
  90   0.45     hold  7266     8.37   -52.18   33.9    n/a       n/a            n/a     n/a
  90   0.45  bracket  7266    -5.75   -23.18   20.2   99.7     -5.95           8.20    33.7
  90   0.45   nostop  7266    -2.39    -6.68   39.5   60.1     41.39          59.29    51.1
  90   0.60     hold  7266     8.10   -27.83   40.4    n/a       n/a            n/a     n/a
  90   0.60  bracket  7266    -5.10   -22.43   21.4   98.7     -6.36           7.02    39.7
  90   0.60   nostop  7266    -0.17    -4.51   41.5   57.4     36.39          50.79    57.9
 120   0.30     hold  7266    13.60   -84.96   27.1    n/a       n/a            n/a     n/a
 120   0.30  bracket  7266    -6.11   -23.25   19.6  100.0     -6.12          13.59    27.1
 120   0.30   nostop  7266    -4.13    -6.73   39.6   63.4     43.90          71.84    41.2
 120   0.45     hold  7266    12.89   -59.52   34.5    n/a       n/a            n/a     n/a
 120   0.45  bracket  7266    -5.28   -22.52   20.5   99.8     -5.48          12.72    34.5
 120   0.45   nostop  7266    -1.37    -4.47   41.2   63.8     40.80          63.13    50.5
 120   0.60     hold  7266    12.36   -30.91   41.0    n/a       n/a            n/a     n/a
 120   0.60  bracket  7266    -4.08   -22.08   21.9   99.2     -4.92          11.65    40.6
 120   0.60   nostop  7266     1.61    -3.26   43.0   62.0     37.58          54.91    58.1
 180   0.30     hold  7266    22.89   -91.87   25.5    n/a       n/a            n/a     n/a
 180   0.30  bracket  7266    -5.44   -22.41   20.3   99.9     -5.45          22.90    25.4
 180   0.30   nostop  7266    -2.84    -4.28   41.2   66.6     41.53          80.18    37.6
 180   0.45     hold  7266    20.35   -66.33   33.9    n/a       n/a            n/a     n/a
 180   0.45  bracket  7266    -4.65   -22.03   21.2   99.8     -4.69          20.35    33.9
 180   0.45   nostop  7266    -0.62    -2.76   43.0   67.3     38.65          69.82    48.3
 180   0.60     hold  7266    19.03   -31.17   41.1    n/a       n/a            n/a     n/a
 180   0.60  bracket  7266    -3.64   -21.62   21.8   99.6     -3.92          18.84    41.0
 180   0.60   nostop  7266     2.84    -2.01   44.1   66.3     37.46          61.89    56.7

Paired bracket-minus-hold, same entries, t-stat (all cells; full / pre-2016-06 / post-2016-06):
DTE=60  d=0.30: -12.39pp t=-6.35 | pre -7.21pp t=-2.69 | post -17.58pp t=-6.20
DTE=60  d=0.45: -10.41pp t=-7.61 | pre -6.27pp t=-3.44 | post -14.57pp t=-7.13
DTE=60  d=0.60:  -8.85pp t=-8.68 | pre -5.61pp t=-4.12 | post -12.10pp t=-7.98
DTE=90  d=0.30: -15.62pp t=-6.51 | pre -8.51pp t=-2.64 | post -22.75pp t=-6.40
DTE=90  d=0.45: -14.11pp t=-8.40 | pre -8.67pp t=-3.84 | post -19.58pp t=-7.87
DTE=90  d=0.60: -13.20pp t=-10.52| pre -8.91pp t=-5.21 | post -17.51pp t=-9.54
DTE=120 d=0.30: -19.71pp t=-7.46 | pre -11.94pp t=-3.32 | post -27.51pp t=-7.12
DTE=120 d=0.45: -18.17pp t=-9.73 | pre -12.01pp t=-4.71 | post -24.34pp t=-8.95
DTE=120 d=0.60: -16.44pp t=-11.79| pre -11.95pp t=-6.19 | post -20.95pp t=-10.43
DTE=180 d=0.30: -28.32pp t=-9.00 | pre -14.08pp t=-3.44 | post -42.63pp t=-8.93
DTE=180 d=0.45: -25.00pp t=-11.40| pre -15.43pp t=-5.31 | post -34.61pp t=-10.54
DTE=180 d=0.60: -22.67pp t=-13.98| pre -16.37pp t=-7.47 | post -28.99pp t=-12.15

Bracket "stopped" breakdown (loss-stop vs gain-stop), 90 DTE example (see script output for all 12 cells):
DTE=90 d=0.30: loss_stop%=80.5 loss_stop_mean=-27.27% gain_stop%=19.5 gain_stop_mean=+78.20%
DTE=90 d=0.45: loss_stop%=80.0 loss_stop_mean=-26.15% gain_stop%=20.0 gain_stop_mean=+74.81%
DTE=90 d=0.60: loss_stop%=79.6 loss_stop_mean=-25.05% gain_stop%=20.4 gain_stop_mean=+66.41%
```

## Verdict

Honest read of the numbers above against the predictions committed before
any test ran. Nothing here changes what predictions were made or how the
test was scored.

**P1 (BRACKET vs HOLD) — PARTLY CONFIRMED.** The core claim is confirmed,
and by more than the falsification bar: bracket beats hold by a LOWER mean
return in every one of the 12 grid cells, and the "prove wrong" bar (bracket
beats hold by 2pp+ with t>2 in both halves) is not just missed, it's
inverted — bracket UNDERPERFORMS hold by 8.7-42.6 pp with |t| from 2.64 to
13.98 across both halves of the sample. The "stopped trades average near
-25%, not -100%" sub-claim is also confirmed once loss-stops are separated
from ratchet gain-locks: pure loss-stops average -22.9% to -29.3% across the
grid, right where P1 said they'd land. But the "expect bracket's win rate to
be HIGHER" sub-claim is REFUTED: bracket's win rate (19.1-21.9%) is lower
than hold's (25.5-41.1%) in every single cell, not higher. Net: P1's central
mechanism (bracket caps upside more than it saves on the downside, net
negative in mean) is confirmed strongly; its win-rate side-prediction was
wrong.

**P2 (EXPIRY: 120-180 DTE beats 60 DTE) — CONFIRMED.** Hold mean return
rises monotonically with DTE at every delta (60->90->120->180 DTE: e.g. at
0.45 delta, 3.90% -> 8.37% -> 12.89% -> 20.35%), and bracket's mean loss
shrinks the same way (-6.51% -> -5.75% -> -5.28% -> -4.65% at 0.45 delta).
Caveat: longer DTE also means a longer calendar window, so part of this is
just more time for the underlying's positive drift to show up (SPY's own
mean benchmark return over the window rises the same way, 1.00% -> 4.31%
DTE 60->180) — this is a real result on this model, not proof the "decay"
mechanism specifically (vs. just "more time span") is what drives it.

**P3 (DELTA: 0.50-0.60 beats 0.30 on mean return) — REFUTED on this model.**
For HOLD, delta 0.30 has a HIGHER mean return than delta 0.60 at every DTE
(e.g. 90 DTE: 8.95% at 0.30 vs 8.10% at 0.60; 180 DTE: 22.89% at 0.30 vs
19.03% at 0.60) — the opposite of the prediction. Delta 0.60 does win on win
rate (safer) and, notably, DOES beat delta 0.30 under the BRACKET policy
(e.g. 90 DTE bracket: -5.10% at 0.60 vs -6.67% at 0.30) — so the direction
depends on which exit you evaluate it through. Important limitation: this
model applies the SAME 1.15x vol premium to every delta with no skew, so it
does not capture the real-market fact that low-delta (far OTM) calls are
usually priced richer (higher IV) than near-the-money calls. That missing
skew plausibly inflates delta-0.30's modeled returns here. Read as: REFUTED
as tested, but the test is not clean evidence against P3's real-market
premise, because the model omits the exact effect (skew) P3's reasoning
leans on.

**P4 (TREND FILTER changes mean less than bracket-vs-hold diff) —
PARTLY.** Depends entirely on which return the trend filter is applied to.
Applied to HOLD returns at the default cell, the above/below-200SMA swing is
+24.10 pp — LARGER than the -13.40 pp bracket-vs-hold diff on the same
subset, so P4 is REFUTED for hold. Applied to BRACKET returns, the swing is
only +3.46 pp — SMALLER than that same -13.40 pp, so P4 is CONFIRMED for
bracket. The prediction did not specify which exit to filter, so this is
scored PARTLY: true for the exit policy (bracket) actually under evaluation
in P1, false for the raw/hold return.

## Limits

Constant IV for the life of each trade (no term structure, no vol-regime
change, no realized-to-implied convergence); no skew (every delta priced off
the same 1.15x realized-vol multiplier, which likely overstates low-delta/
far-OTM returns relative to real markets); no earnings-date IV crush or
event risk; 14-symbol universe is survivorship-biased toward large caps that
are still trading in 2026. Absolute return numbers are a rough guide only;
the same-path bracket-vs-hold and trend-filter COMPARISONS are the more
trustworthy part of this test. Per R16.3, nothing in this document is
adopted before the weekend re-read (R16.3); this is a test result to be
weighed then, not a decision made now.
