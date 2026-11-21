# RSI(2) "Buy the Dip in an Uptrend", and a Pooled Test of Panic Dips

One-line: the best-documented indicator strategy (Connors RSI(2)), tested for
decay since publication, plus one pooled test of the "oversold only works in
a panic" pattern that four separate studies hinted at.

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (52bed82).
Audience: Nolan, TARS sessions

## Overview

RSI(2) rule (Connors & Alvarez, "Short Term Trading Strategies That Work",
2008): price above its 200-day SMA, RSI(2) closes below 10 -> buy next open;
sell when the close is above the 5-day SMA. Published 2008, so 2009-2026 is
out of sample for the original authors.
Pooled panic test: the RSI < 30, lower-Bollinger-Band, new-60-day-low and
heavy-volume-selloff results each leaned positive at VIX >= 25 without being
significant. Signals on the same dates aren't independent, so the pooled
test must cluster by date.
Data: paper/history/daily_ohlcv.json (15 symbols, 2006-2026) and
vix_weekly.json. R16 trigger (c) is ON in the writing session. Nothing
adopted before the weekend re-read. Survivorship: 2026's winners.

## Predictions (written before the test)

P1 RSI(2) on SPY: a high win rate (60-75%) and a positive average trade. As a
   system it trails buy-and-hold on CAGR (invested only ~15-30% of the time),
   with a Sharpe near or above buy-and-hold's. The edge is smaller in
   2016-2026 than 2006-2015 (published patterns decay).
P2 RSI(2) on single large caps: weaker than on SPY. Index-level mean
   reversion is the documented version; single stocks carry news risk.
P3 POOLED PANIC DIPS: directionally positive at VIX >= 25. Once signals are
   clustered by date, the t-stat stays below 3. Four weak results pointing
   the same way are less than they look, because they are mostly the same
   days.

What would prove P1 wrong: RSI(2) on SPY beating buy-and-hold on BOTH CAGR
and Sharpe in the 2016-2026 half, after costs.


## Results

Full script: `paper/research_scripts/rsi2_panic.py`. All numbers below are
after 0.10%/side costs (0.20% round trip). "sys" = the RSI(2) system,
"BH" = buy-and-hold over the identical warmed-up window.

### Part A -- RSI(2) system, base rule (RSI(2)<10, exit close>SMA5)

**SPY**

| period    | trades | win% | avg trade% | hold days | t (avg trade) | sys CAGR% | sys Sharpe | sys maxDD% | % invested | BH CAGR% | BH Sharpe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| full      | 158 | 66.5 | 0.209 | 3.4 | 1.63 | 1.57  | 0.28 | -15.25 | 10.7 | 9.08  | 0.54 |
| 2006-2015 | 65  | 64.6 | 0.193 | 3.6 | 0.84 | 1.25  | 0.22 | -15.25 | 10.2 | 4.58  | 0.32 |
| 2016-2026 | 93  | 67.7 | 0.220 | 3.2 | 1.48 | 1.84  | 0.33 | -14.00 | 11.2 | 13.10 | 0.78 |

**14-stock equal-weight average** (pooled trade count and pooled per-trade
t-stat across all 14 stocks' trades; other columns are the mean across the
14 symbols)

| period    | trades (pooled) | win% | avg trade% | hold days | t (pooled) | sys CAGR% | sys Sharpe | sys maxDD% | % invested | BH CAGR% | BH Sharpe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| full      | 1894 | 63.1 | 0.327 | 4.0 | 4.66 | 2.08 | 0.23 | -31.72 | 10.7 | 10.23 | 0.44 |
| 2006-2015 | 880  | 62.8 | 0.320 | 4.1 | 3.06 | 2.04 | 0.26 | -23.02 | 11.1 | 5.55  | 0.34 |
| 2016-2026 | 1014 | 62.8 | 0.289 | 3.9 | 3.51 | 2.20 | 0.19 | -25.28 | 10.4 | 15.14 | 0.55 |

Per-symbol range (full sample): win rate 55.8-73.9% (all 14 positive-side of
50%); average trade% ranges from -0.298 (PFE) to +0.819 (NVDA); 2 of 14
stocks (PFE, XOM) have a negative average trade over the full sample; 5 of 14
(BAC, F, IBM, PFE, XOM) go negative specifically in 2016-2026. Full per-symbol
table is in the raw output block below.

### Sensitivity variants (extra tests, full sample only)

| variant | 14avg trades | 14avg win% | 14avg avg trade% | 14avg pooled t | 14avg sys CAGR% | 14avg sys Sharpe | SPY trades | SPY win% | SPY avg trade% | SPY t | SPY sys CAGR% | SPY sys Sharpe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RSI(2)<5, exit SMA5   | 943  | 61.5 | 0.371 | 3.98 | 1.28 | 0.19 | 88  | 70.5 | 0.317 | 1.62 | 1.34 | 0.28 |
| RSI(2)<15, exit SMA5  | 2610 | 62.9 | 0.249 | 4.22 | 2.12 | 0.20 | 236 | 68.2 | 0.207 | 2.19 | 2.36 | 0.36 |
| RSI(2)<10, exit SMA10 | 1727 | 67.4 | 0.434 | 4.34 | 2.25 | 0.22 | 147 | 72.1 | 0.225 | 1.03 | 1.39 | 0.20 |

All three variants point the same direction as the base rule: positive win
rate in the 60-75% band, positive average trade, system CAGR and Sharpe well
below buy-and-hold's (BH full-sample CAGR/Sharpe unchanged across variants:
14avg 10.23%/0.44, SPY 9.08%/0.54, since buy-and-hold does not depend on the
system's parameters). Not one lucky setting.

### Part B -- pooled panic dips

Raw signal counts (pre-union, summed over all 15 symbols, pre-dedup):
rsi14_cross_below_30=894, bb_below_lower=4121, new_60d_low=3723,
down2pct_heavyvol=909. Union after per-symbol 5-day dedup: **2151** symbol-day
instances, **1327** distinct calendar dates, **104** episodes (dedup-window-10
gap rule).

**Main result, full sample, all instances pooled, unconditional baseline**

| h (days) | n instances | n dates | diff (pp) | naive t | clustered excess (pp) | clustered t |
|---|---|---|---|---|---|---|
| 5  | 2149 | 1325 | +0.107 | 0.90  | +0.033 | 0.23  |
| 10 | 2145 | 1322 | -0.052 | -0.32 | -0.013 | -0.07 |
| 21 | 2141 | 1320 | +0.135 | 0.60  | +0.160 | 0.61  |

**VIX-regime split (crisis windows included, unconditional baseline)**

| regime | n inst | n dates | episodes | h=5 clustered t | h=10 clustered t | h=21 clustered t |
|---|---|---|---|---|---|---|
| <20   | 1185 | 808 | 105 | -0.11 | -1.14 | -1.34 |
| 20-25 | 407  | 239 | 68  | 0.17  | 1.52  | 0.73  |
| >=25  | 559  | 280 | 48  | 0.32  | -0.12 | **1.81** |

Max clustered |t| anywhere in the crisis-included VIX-regime split: 1.81
(gte25, h=21). Bonferroni critical value for the full 48-test Part B family:
|t| ~= 3.279 -- nothing in the crisis-included analysis clears it.

**Robustness cut: 2008-09-01..2009-03-31 and 2020-02-01..2020-04-30 removed**
(114 of 2151 instances removed, from both the signal side and the baseline)

| regime | n inst | n dates | episodes | h=5 clustered t | h=10 clustered t | h=21 clustered t |
|---|---|---|---|---|---|---|
| overall (all regimes) | 2037 | 1266 | 101 | 0.06 | 0.48 | 1.17 |
| <20   | 1180 | 805 | 105 | -0.39 | -1.50 | -1.62 |
| 20-25 | 399  | 236 | 67  | 0.11  | 1.46  | 0.68  |
| >=25  | 458  | 225 | 43  | 0.52  | 1.60  | **3.95** (naive t=3.71) |

With the two big crashes removed, the >=25 / h=21 cell clears both |t|=3 and
the Bonferroni-adjusted threshold for the whole 48-test family (3.279). This
is the ONE cell, out of the 48 tests run across all of Part B, that survives
multiple-testing correction -- and it only appears after excluding the two
biggest historical crashes, at one specific horizon, in one specific regime.

### Full raw script output

```
======================================================================================================================
RSI(2) AND POOLED PANIC DIPS -- RAW TEST OUTPUT
======================================================================================================================
Universe: 14 large caps + SPY = ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM', 'SPY']
Date range: 2006-01-03 to 2026-09-23
Cost: 0.10% per side (0.20% round trip). Cash earns 0.
Part A split: 2006-01-01..2015-12-31 vs 2016-01-01..2026-09-23

######################################################################################################################
PART A: RSI(2) SYSTEM
######################################################################################################################

----------------------------------------------------------------------------------------------------------------------
VARIANT: BASE RULE (RSI(2)<10, exit SMA5)  (RSI(2) < 10.0, exit close > SMA(5))
----------------------------------------------------------------------------------------------------------------------
sym   period    | trades    win%  avgtrd%   holdd      t |    cagr%    vol%    shrp    mdd%    pin% | bh_cagr% bh_vol% bh_shrp bh_mdd% bh_pin%
----------------------------------------------------------------------------------------------------------------------------------------------
AAPL  full      |    179    70.4    0.489     4.1   2.12 |     4.03   12.88    0.37  -29.19    14.8 |    27.59   31.24    0.94  -60.87   100.0
AAPL  2006-2015 |     88    73.9    0.645     4.1   1.85 |     5.80   13.77    0.48  -29.19    15.5 |    28.62   33.74    0.92  -60.87   100.0
AAPL  2016-2026 |     91    67.0    0.337     4.2   1.11 |     2.53   12.06    0.27  -16.14    14.1 |    26.71   28.92    0.96  -38.73   100.0
AMZN  full      |    164    68.3    0.644     3.7   2.35 |     4.92   13.27    0.43  -23.25    12.1 |    28.87   37.67    0.86  -65.25   100.0
AMZN  2006-2015 |     76    67.1    0.744     3.6   1.61 |     5.64   15.07    0.44  -16.56    11.8 |    39.57   42.39    0.99  -65.25   100.0
AMZN  2016-2026 |     88    69.3    0.557     3.8   1.74 |     4.30   11.51    0.42  -23.25    12.3 |    20.34   33.08    0.72  -56.15   100.0
BAC   full      |    128    63.3    0.245     4.1   0.61 |     0.46   11.88    0.10  -55.69    10.5 |     0.20   46.91    0.24  -94.28   100.0
BAC   2006-2015 |     56    73.2    0.963     3.9   2.49 |     5.76    9.16    0.66  -14.52     9.4 |   -11.77   60.54    0.09  -94.28   100.0
BAC   2016-2026 |     72    55.6   -0.314     4.2  -0.49 |    -3.87   13.79   -0.22  -55.69    11.5 |    11.77   30.73    0.52  -49.27   100.0
C     full      |    126    61.9    0.367     4.0   1.14 |     1.92   10.24    0.24  -25.46    10.0 |    -6.50   49.82    0.11  -98.19   100.0
C     2006-2015 |     48    60.4   -0.012     4.6  -0.02 |    -0.48    9.85    0.00  -24.31     9.5 |   -21.84   63.89   -0.07  -98.19   100.0
C     2016-2026 |     78    62.8    0.600     3.6   1.56 |     4.01   10.56    0.43  -25.46    10.5 |     9.04   33.32    0.43  -56.79   100.0
CSCO  full      |    134    63.4    0.194     4.2   0.85 |     1.08    8.90    0.16  -36.51    11.2 |     7.74   28.51    0.40  -60.04   100.0
CSCO  2006-2015 |     63    65.1    0.145     4.2   0.42 |     0.74    9.12    0.13  -29.89    11.5 |     1.42   30.93    0.20  -60.04   100.0
CSCO  2016-2026 |     71    62.0    0.238     4.2   0.77 |     1.36    8.70    0.20  -30.65    11.0 |    13.48   26.26    0.61  -42.81   100.0
F     full      |    100    56.0    0.211     4.5   0.41 |     0.40   10.90    0.09  -35.29     9.0 |     2.42   42.55    0.27  -86.93   100.0
F     2006-2015 |     55    61.8    0.660     4.7   0.79 |     2.90   13.45    0.28  -35.29    11.1 |     6.35   48.15    0.37  -86.93   100.0
F     2016-2026 |     45    48.9   -0.337     4.3  -0.62 |    -1.69    8.10   -0.17  -20.42     7.2 |    -0.85   37.08    0.16  -71.70   100.0
GE    full      |    132    65.2    0.498     3.7   2.02 |     3.08    9.12    0.38  -27.17     9.8 |     2.99   34.27    0.26  -86.97   100.0
GE    2006-2015 |     68    60.3    0.340     4.0   1.29 |     2.37    7.96    0.33  -12.08    11.7 |    -1.47   32.59    0.12  -84.19   100.0
GE    2016-2026 |     64    70.3    0.665     3.5   1.57 |     3.70   10.02    0.41  -26.93     8.2 |     6.97   35.65    0.37  -83.33   100.0
GOOGL full      |    168    64.9    0.578     3.9   2.82 |     4.68    9.86    0.51  -22.73    12.9 |    19.08   30.68    0.72  -65.29   100.0
GOOGL 2006-2015 |     73    61.6    0.590     4.2   1.66 |     4.41    9.89    0.49  -22.73    13.3 |    15.52   32.39    0.60  -65.29   100.0
GOOGL 2016-2026 |     95    67.4    0.568     3.6   2.36 |     4.91    9.83    0.54  -15.13    12.6 |    22.23   29.13    0.83  -44.32   100.0
IBM   full      |    129    61.2    0.097     3.9   0.50 |     0.47    7.00    0.10  -24.96    10.1 |     4.91   25.71    0.32  -56.08   100.0
IBM   2006-2015 |     64    62.5    0.255     3.9   1.22 |     1.69    6.60    0.29   -9.51    10.9 |     4.90   22.73    0.32  -44.82   100.0
IBM   2016-2026 |     65    60.0   -0.059     3.9  -0.18 |    -0.56    7.32   -0.04  -24.96     9.5 |     4.92   28.03    0.31  -47.91   100.0
MSFT  full      |    142    61.3    0.549     3.7   2.49 |     3.74   10.15    0.41  -20.68    10.5 |    15.51   28.07    0.65  -59.12   100.0
MSFT  2006-2015 |     62    51.6    0.397     4.1   1.03 |     2.40    9.39    0.30  -20.68    10.9 |     7.69   28.67    0.40  -59.12   100.0
MSFT  2016-2026 |     80    68.8    0.667     3.4   2.62 |     4.89   10.76    0.50  -13.86    10.1 |    22.68   27.55    0.88  -37.56   100.0
NVDA  full      |    154    64.9    0.819     4.0   2.01 |     5.46   18.12    0.38  -56.86    12.3 |    35.67   48.85    0.87  -85.08   100.0
NVDA  2006-2015 |     59    49.2   -0.632     4.6  -0.99 |    -4.77   14.98   -0.25  -56.36    11.8 |     5.16   48.36    0.35  -85.08   100.0
NVDA  2016-2026 |     95    74.7    1.720     3.6   3.37 |    15.12   20.43    0.79  -26.76    12.8 |    68.83   49.23    1.31  -66.36   100.0
PFE   full      |    120    55.8   -0.298     4.3  -1.42 |    -1.94    6.84   -0.25  -39.89    10.3 |     0.29   23.78    0.13  -64.75   100.0
PFE   2006-2015 |     58    62.1    0.079     4.0   0.28 |     0.35    7.04    0.08  -17.67    10.0 |     1.68   23.54    0.19  -58.51   100.0
PFE   2016-2026 |     62    50.0   -0.649     4.6  -2.15 |    -3.87    6.66   -0.56  -37.55    10.5 |    -0.89   23.98    0.08  -64.75   100.0
T     full      |    105    70.5    0.298     3.6   1.55 |     1.48    5.72    0.29  -15.57     7.5 |     0.09   23.43    0.12  -59.03   100.0
T     2006-2015 |     56    71.4    0.441     3.5   1.88 |     2.62    5.41    0.51   -8.53     8.4 |     0.58   23.01    0.14  -49.29   100.0
T     2016-2026 |     49    69.4    0.135     3.7   0.43 |     0.51    5.98    0.11  -15.57     6.8 |    -0.34   23.79    0.11  -59.03   100.0
XOM   full      |    113    55.8   -0.108     4.0  -0.41 |    -0.73    7.73   -0.06  -30.79     9.0 |     4.35   27.04    0.29  -69.87   100.0
XOM   2006-2015 |     54    59.3   -0.130     4.0  -0.39 |    -0.94    6.51   -0.11  -24.92     9.3 |     1.33   25.83    0.18  -40.48   100.0
XOM   2016-2026 |     59    52.5   -0.087     3.9  -0.22 |    -0.54    8.64   -0.02  -21.59     8.7 |     7.01   28.03    0.38  -66.94   100.0
SPY   full      |    158    66.5    0.209     3.4   1.63 |     1.57    6.31    0.28  -15.25    10.7 |     9.08   19.60    0.54  -56.47   100.0
SPY   2006-2015 |     65    64.6    0.193     3.6   0.84 |     1.25    6.66    0.22  -15.25    10.2 |     4.58   21.51    0.32  -56.47   100.0
SPY   2016-2026 |     93    67.7    0.220     3.2   1.48 |     1.84    5.98    0.33  -14.00    11.2 |    13.10   17.81    0.78  -34.10   100.0
----------------------------------------------------------------------------------------------------------------------------------------------
AVG14 full      |   1894    63.1    0.327     4.0   4.66 |     2.08   10.19    0.23  -31.72    10.7 |    10.23   34.18    0.44  -72.27   100.0   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)
AVG14 2006-2015 |    880    62.8    0.320     4.1   3.06 |     2.04    9.87    0.26  -23.02    11.1 |     5.55   36.91    0.34  -68.02   100.0   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)
AVG14 2016-2026 |   1014    62.8    0.289     3.9   3.51 |     2.20   10.31    0.19  -25.28    10.4 |    15.14   31.06    0.55  -56.12   100.0   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)

SPY (separate):
SPY   full      |    158    66.5    0.209     3.4   1.63 |     1.57    6.31    0.28  -15.25    10.7 |     9.08   19.60    0.54  -56.47   100.0
SPY   2006-2015 |     65    64.6    0.193     3.6   0.84 |     1.25    6.66    0.22  -15.25    10.2 |     4.58   21.51    0.32  -56.47   100.0
SPY   2016-2026 |     93    67.7    0.220     3.2   1.48 |     1.84    5.98    0.33  -14.00    11.2 |    13.10   17.81    0.78  -34.10   100.0
(still holding an open position at end of sample, excluded from trade-level stats: ['BAC', 'XOM'])

----------------------------------------------------------------------------------------------------------------------
SENSITIVITY VARIANTS (extra tests, compact report: full sample only, SPY + 14-stock avg + pooled trade t)
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
VARIANT: SENSITIVITY: RSI(2)<5, exit SMA5  (RSI(2) < 5.0, exit close > SMA(5))
----------------------------------------------------------------------------------------------------------------------
sym   period    | trades    win%  avgtrd%   holdd      t |    cagr%    vol%    shrp    mdd%    pin% | bh_cagr% bh_vol% bh_shrp bh_mdd% bh_pin%
----------------------------------------------------------------------------------------------------------------------------------------------
AVG14 full      |    943    61.5    0.371     4.0   3.98 |     1.28    7.33    0.19  -25.91     5.4 |    10.23   34.18    0.44  -72.27   100.0   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)

SPY (separate):
SPY   full      |     88    70.5    0.317     3.3   1.62 |     1.34    5.19    0.28  -16.15     5.7 |     9.08   19.60    0.54  -56.47   100.0
(still holding an open position at end of sample, excluded from trade-level stats: ['BAC'])

----------------------------------------------------------------------------------------------------------------------
VARIANT: SENSITIVITY: RSI(2)<15, exit SMA5  (RSI(2) < 15.0, exit close > SMA(5))
----------------------------------------------------------------------------------------------------------------------
sym   period    | trades    win%  avgtrd%   holdd      t |    cagr%    vol%    shrp    mdd%    pin% | bh_cagr% bh_vol% bh_shrp bh_mdd% bh_pin%
----------------------------------------------------------------------------------------------------------------------------------------------
AVG14 full      |   2610    62.9    0.249     3.9   4.22 |     2.12   11.76    0.20  -37.61    14.6 |    10.23   34.18    0.44  -72.27   100.0   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)

SPY (separate):
SPY   full      |    236    68.2    0.207     3.3   2.19 |     2.36    7.16    0.36  -14.73    15.6 |     9.08   19.60    0.54  -56.47   100.0
(still holding an open position at end of sample, excluded from trade-level stats: ['BAC', 'T', 'XOM'])

----------------------------------------------------------------------------------------------------------------------
VARIANT: SENSITIVITY: RSI(2)<10, exit SMA10  (RSI(2) < 10.0, exit close > SMA(10))
----------------------------------------------------------------------------------------------------------------------
sym   period    | trades    win%  avgtrd%   holdd      t |    cagr%    vol%    shrp    mdd%    pin% | bh_cagr% bh_vol% bh_shrp bh_mdd% bh_pin%
----------------------------------------------------------------------------------------------------------------------------------------------
AVG14 full      |   1727    67.4    0.434     6.6   4.34 |     2.25   13.15    0.22  -42.49    16.3 |    10.23   34.18    0.44  -72.27   100.0   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)

SPY (separate):
SPY   full      |    147    72.1    0.225     5.4   1.03 |     1.39    9.26    0.20  -36.27    15.9 |     9.08   19.60    0.54  -56.47   100.0
(still holding an open position at end of sample, excluded from trade-level stats: ['BAC', 'C', 'XOM'])

----------------------------------------------------------------------------------------------------------------------
MULTIPLE TESTING (Part A)
----------------------------------------------------------------------------------------------------------------------
Base rule: 45 symbol-period system runs (15 symbols x 3 periods)
Sensitivity variants: 45 additional symbol runs (3 variants x 15 symbols, full sample)
Total Part A runs: 90

######################################################################################################################
PART B: POOLED PANIC DIPS
######################################################################################################################
Universe: all 15 symbols pooled = ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM', 'SPY']
Date range: 2006-01-03 to 2026-09-23
Forward-return horizons (trading days): [5, 10, 21]
Dedup: 5-trading-day window on the per-symbol UNION of the four signals

----------------------------------------------------------------------------------------------------------------------
RAW SIGNAL COUNTS (pre-union, pre-dedup, per symbol summed) -- informational only
----------------------------------------------------------------------------------------------------------------------
  rsi14_cross_below_30     n=894
  bb_below_lower           n=4121
  new_60d_low              n=3723
  down2pct_heavyvol        n=909
  UNION signal-day instances after per-symbol 5-day dedup (all 15 symbols): 2151

======================================================================================================================
MAIN RESULT -- ALL SIGNAL INSTANCES POOLED, FULL SAMPLE
======================================================================================================================
ALL INSTANCES (unconditional baseline):
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 2151
  distinct calendar dates: 1327   episodes (gap >= 10 trading days starts a new one): 104
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5    2149    1325     0.107     0.90       0.033        0.23
   10    2145    1322    -0.052    -0.32      -0.013       -0.07
   21    2141    1320     0.135     0.60       0.160        0.61

----------------------------------------------------------------------------------------------------------------------
VIX-REGIME SPLIT (regime = most recent WEEKLY VIX close on/before the signal day; baseline stays
the UNCONDITIONAL baseline computed above -- not a regime-specific baseline)
----------------------------------------------------------------------------------------------------------------------
VIX regime lt20:
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 1185
  distinct calendar dates: 808   episodes (gap >= 10 trading days starts a new one): 105
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5    1183     806     0.093     0.79      -0.014       -0.11
   10    1179     803    -0.059    -0.36      -0.209       -1.14
   21    1175     801    -0.102    -0.43      -0.357       -1.34

VIX regime 20to25:
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 407
  distinct calendar dates: 239   episodes (gap >= 10 trading days starts a new one): 68
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5     407     239     0.110     0.44       0.059        0.17
   10     407     239     0.588     1.65       0.706        1.52
   21     407     239    -0.072    -0.13       0.533        0.73

VIX regime gte25:
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 559
  distinct calendar dates: 280   episodes (gap >= 10 trading days starts a new one): 48
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5     559     280     0.136     0.41       0.147        0.32
   10     559     280    -0.502    -1.15      -0.065       -0.12
   21     559     280     0.785     1.35       1.320        1.81


======================================================================================================================
ROBUSTNESS CUT -- 2008-09-01..2009-03-31 and 2020-02-01..2020-04-30 REMOVED
(removed from BOTH the signal instances AND the baseline pool)
======================================================================================================================
Instances removed by the exclusion windows: 114 (of 2151)
ALL INSTANCES, crisis windows excluded (unconditional baseline, also crisis-excluded):
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 2037
  distinct calendar dates: 1266   episodes (gap >= 10 trading days starts a new one): 101
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5    2035    1264     0.101     0.97       0.008        0.06
   10    2031    1261     0.183     1.29       0.079        0.48
   21    2027    1259     0.328     1.60       0.288        1.17

----------------------------------------------------------------------------------------------------------------------
VIX-REGIME SPLIT, crisis windows excluded
----------------------------------------------------------------------------------------------------------------------
VIX regime lt20 (crisis-excluded):
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 1180
  distinct calendar dates: 805   episodes (gap >= 10 trading days starts a new one): 105
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5    1178     803     0.062     0.53      -0.053       -0.39
   10    1174     800    -0.109    -0.67      -0.273       -1.50
   21    1170     798    -0.137    -0.60      -0.422       -1.62

VIX regime 20to25 (crisis-excluded):
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 399
  distinct calendar dates: 236   episodes (gap >= 10 trading days starts a new one): 67
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5     399     236     0.099     0.38       0.037        0.11
   10     399     236     0.610     1.69       0.686        1.46
   21     399     236    -0.021    -0.04       0.502        0.68

VIX regime gte25 (crisis-excluded):
  distinct signal instances (symbol-days, after per-symbol 5-day dedup): 458
  distinct calendar dates: 225   episodes (gap >= 10 trading days starts a new one): 43
    h  n_inst n_dates   diff_pp  t_naive clustexc_pp t_clustered
  --------------------------------------------------------------
    5     458     225     0.204     0.75       0.197        0.52
   10     458     225     0.559     1.63       0.696        1.60
   21     458     225     1.823     3.71       2.582        3.95


----------------------------------------------------------------------------------------------------------------------
MULTIPLE TESTING (Part B)
----------------------------------------------------------------------------------------------------------------------
Main pooled result: 6 tests (3 horizons x {naive, clustered})
VIX-regime split: 18 more tests (3 horizons x {naive, clustered} x 3 regimes)
Robustness cut (crisis windows removed, overall + regime split): 24 more tests
Total Part B tests: 48
  Bonferroni alpha=0.05/48 -> two-tailed critical |t| ~= 3.279
  (This threshold applies to the CLUSTERED t, which is the number that should be judged against it --
   see docstring for why the naive t is not the headline.)

Done.
```

## Verdict

**P1 (RSI(2) on SPY) -- PARTLY CONFIRMED.** Win rate (66.5% full, 64.6%/67.7%
by half) sits inside the predicted 60-75% band, and the average trade is
positive in both halves (0.193%, 0.220%). The system trails buy-and-hold on
CAGR in both halves and by a wide margin (1.25% vs 4.58% in 2006-2015; 1.84%
vs 13.10% in 2016-2026) -- confirmed, though time invested (10.2%/11.2%) came
in below the predicted 15-30% range, not inside it. The specific stated
falsification test -- "RSI(2) on SPY beating buy-and-hold on BOTH CAGR and
Sharpe in 2016-2026" -- did NOT happen (system loses on both: 1.84% vs
13.10% CAGR, 0.33 vs 0.78 Sharpe), so P1 survives that literal test. But the
"Sharpe near or above buy-and-hold's" clause is REFUTED: system Sharpe is
clearly below buy-and-hold's in every period checked (0.28 vs 0.54 full,
0.22 vs 0.32 in 2006-2015, 0.33 vs 0.78 in 2016-2026) -- "near" is generous
for a roughly 2x gap. The edge-decay claim ("smaller in 2016-2026") is mixed:
avg trade % and win rate barely moved between halves, but the CAGR gap to
buy-and-hold widened (SPY's own CAGR nearly tripled from 2006-2015 to
2016-2026 while the system's CAGR stayed flat), so on a relative basis the
system's disadvantage did grow, consistent with decay, even though the
system's own absolute numbers didn't obviously weaken.

**P2 (weaker on single large caps) -- PARTLY CONFIRMED.** On raw average
trade return, the 14-stock equal-weight average (0.327% full sample) is
numerically HIGHER than SPY's (0.209%), which cuts against a plain reading of
"weaker." But every other angle supports "weaker/noisier": system Sharpe
(0.23 vs 0.28), much deeper average max drawdown (-31.72% vs -15.25%), wide
per-symbol dispersion (avg trade% from -0.298% to +0.819%), and 5 of 14
stocks (BAC, F, IBM, PFE, XOM) turning net-negative in 2016-2026 while SPY
stayed positive in both halves. Single stocks show a noisier, more
drawdown-prone, more decay-prone version of the same pattern rather than a
uniformly weaker one.

**P3 (pooled panic dips) -- PARTLY CONFIRMED / PARTLY REFUTED.** In the
crisis-included main analysis, the VIX>=25 result is directionally positive
at 2 of 3 horizons (h=5, h=21) but negative at h=10, and the date-clustered
t-stat never exceeds 1.81 -- comfortably under 3, consistent with the
prediction. The "four weak results are mostly the same days" framing is
directly confirmed by the numbers: 2151 signal-day instances collapse to only
1327 distinct dates and 104 episodes, i.e. a signal fires more than once on
the same date about 39% of the time, and naive vs. clustered t-stats differ
by roughly 3-4x in most cells (e.g. h=21/gte25: naive t=1.35 vs clustered
t=1.81 -- clustered was actually higher there, but elsewhere, e.g. h=10/lt20,
naive t=-0.36 vs clustered t=-1.14, clustering can also inflate |t| when the
per-date signs agree; the direction of the naive-vs-clustered gap is not
uniform, but the two numbers are consistently different, which is the
point). However, the "stays below 3" clause is REFUTED once the two biggest
crashes (2008-09..2009-03, 2020-02..2020-04) are removed from both the
signal side and the baseline: the VIX>=25, h=21 cell then shows clustered
t=3.95 (naive t=3.71), which clears both |t|=3 and the Bonferroni-corrected
threshold for the full 48-test Part B family (3.279). This is exactly one
cell out of 48 tests, appears only in the crisis-excluded cut, and only at
one horizon in one regime -- it should be read as a lead worth re-examining,
not as confirmed pooled-panic-dip alpha.

## What this means

- RSI(2) on SPY behaves close to how the 2008 book described it: you buy
  dips in an uptrend, you win most of the time, but you're only invested
  about a tenth of the time, so your total return badly trails just buying
  and holding SPY the whole time.
- The "risk-adjusted" story is weaker than hoped: this system's Sharpe ratio
  (return per unit of risk) is clearly below buy-and-hold's, not close to it,
  in every period we checked.
- On individual big-name stocks the same pattern shows up, but noisier: some
  stocks (NVDA, AMZN) did great with this rule, a few (PFE, XOM, and more in
  the recent decade) lost money on it. It is not a strategy you'd want to run
  on a single stock without expecting some of them to fail.
- Three different tweaks to the RSI(2) rule (different RSI cutoffs, a
  different exit average) all told the same basic story, so this isn't a
  fluke of one specific setting.
- For "buy the dip when the market panics" (RSI oversold, price below its
  Bollinger band, a new 60-day low, or a heavy-volume selloff): these four
  signals overlap heavily -- they mostly fire on the same handful of scary
  days, not on 2000+ independent days. Once you account for that overlap,
  the historical edge in high-VIX ("panicky") periods is small and not
  statistically convincing.
- There is one narrower result -- panics during high-VIX periods, looking 21
  trading days out, with the two biggest crashes (2008-09 and 2020's COVID
  crash) excluded -- that does clear a strict statistical bar. But it's a
  single result out of 48 things we checked, and it only appears after
  deliberately removing the two most extreme historical events, so it needs
  more scrutiny before anyone should trust it.
- Bottom line: nothing here is a green light to trade. It's a faithful replay
  of a well-known book strategy (decayed, as expected) plus one interesting
  but fragile lead worth re-checking, not a validated trading rule.

## Limits

- **Survivorship**: the universe is 14 large-cap "2026 winners" (AAPL AMZN
  BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T XOM) plus SPY, chosen because
  they are recognizable, liquid, long-history names -- not because they were
  drawn from an unbiased cross-section of all stocks that existed in 2006.
  Any stock that would have been delisted, gone bankrupt, or otherwise
  dropped out of a "large cap" universe over 2006-2026 is absent by
  construction. Results should not be read as "what RSI(2) would have done
  on the average stock," only "what it did on 14 stocks that happened to
  survive and thrive."
- **Number of tests / variants tried**: Part A ran 90 symbol-period system
  evaluations (15 symbols x 3 periods for the base rule, plus 3 sensitivity
  variants x 15 symbols for the full sample). Part B ran 48 distinct
  (horizon x naive/clustered x regime x crisis-in/out) statistical tests.
  That is 138 total looks at the data across this one research note. No
  formal Bonferroni correction was applied to Part A (it is a system
  backtest, not an event-study t-test family), but Part B's one interesting
  survivor (VIX>=25, h=21, crisis-excluded, clustered t=3.95) is reported
  against the full 48-test Bonferroni threshold (3.279) precisely because of
  how many looks were taken -- one survivor out of 48 tests is close to what
  you'd expect from chance alone at the 5% level (48 * 0.05 = 2.4 expected
  false positives), so it should not be over-weighted.
- **Costs assumed**: 0.10% per side (0.20% round trip), applied to every
  entry and every exit, cash earns 0% while flat. No slippage, no bid-ask
  spread beyond the flat cost, no financing cost, no tax. Real-world
  execution costs for a system that trades this frequently (roughly 60-160
  round trips per symbol over 20 years) could plausibly run higher or lower
  than this flat assumption depending on the broker and order size.
- **R16.3 weekend re-read**: per the note's own design, nothing here is
  adopted into any live or paper strategy before the scheduled weekend
  re-read. This is a raw-numbers writeup for review, not a decision.
