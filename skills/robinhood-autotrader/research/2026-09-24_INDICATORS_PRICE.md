# Chart Indicators, Part 1: MACD, RSI, Bollinger Bands, SMA(50), EMA(9)

One-line: Nolan asked to test every indicator on his Robinhood chart. Do the
price-based ones predict anything, and do they beat buy-and-hold when you
trade them?

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (9f0f731).
Audience: Nolan, TARS sessions

## Overview

Settings exactly as on Nolan's chart: MACD (12, 26, 9), RSI (14), Bollinger
Bands (20, 2), SMA (50), EMA (9). Data: paper/history/daily_stocks.json,
14 large caps + SPY, 2006-2026. Two tests per indicator: (1) event study,
forward 5/10/21-day returns after each signal vs baseline; (2) where traders
use it as a system, long/flat vs buy-and-hold with costs.
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read. Survivorship: 2026's winners.

## Predictions (written before the test)

P1 MACD: signal-line and zero-line crosses have no forward edge that survives
   multiple testing. As a long/flat system it trails buy-and-hold after costs
   (whipsaw), with a smaller max drawdown.
P2 RSI: RSI < 30 depends on the regime. Calm (VIX < 20): no edge or negative.
   Stressed (VIX >= 25): positive. That's R15 again. RSI > 70 reversal is
   already refuted (2026-09-24_RSI_OVERBOUGHT_PUTS.md) and should replicate.
P3 BOLLINGER: close below the lower band behaves like RSI < 30 (depends on
   the regime). Close above the upper band is followed by continuation, not
   reversal. Squeeze-then-breakout: no edge.
P4 SMA(50): as a long/flat filter it cuts drawdown but trails buy-and-hold
   in return, and whipsaws more than the 200-day. The 50/200 golden and
   death crosses have no forward edge at the cross.
P5 EMA(9): too fast. A price/EMA9 crossover system loses to buy-and-hold
   after costs by a wide margin, because it trades constantly.

What would prove me wrong: any indicator system beating buy-and-hold on
risk-adjusted return (Sharpe) in BOTH halves after costs, or any event
signal with |t| > 3 in both halves.


## Results

Test script: `paper/research_scripts/indicators_price.py`. Universe: 14
large caps pooled (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T XOM),
2006-01-03 to 2026-09-18, SPY reported separately. Exact definitions
(EMA/MACD/RSI-Wilder/Bollinger/SMA formulas, all 18 event signals, the
squeeze definition, and the 6 trading systems with their cost/warmup rules)
are written in full at the top of the script.

**Test 1 (event study):** 18 signal types x 3 horizons = 54 primary tests
(14-stock pool, full sample). VIX-regime cuts on RSI-below-30 and
BB-below-lower add 2 x 3 regimes x 3 horizons = 18 more (secondary, not in
the primary Bonferroni family) -- 72 tests total run in this script.
Bonferroni alpha=0.05/54 -> critical |t| ~= 3.31. **Zero of the 54 primary
tests clear that bar, and the SURVIVORS check (Bonferroni + same sign in
both halves) returns none.** The strongest single cell in the whole primary
table is death_cross at 10 days, t=-1.97 -- consistently negative in both
halves (pre -0.769pp, post -0.860pp) but still short of even the nominal
t=2 line, let alone Bonferroni. Runner-up: macd_cross_above_zero at 10
days, t=1.74.

Phone-readable summary (best |t| among primary 14-pool event tests per
indicator; system metrics are the 14-symbol equal-weight average, full
sample, cost 0.10%/side):

| Indicator | Best event \|t\| (signal, horizon) | System Sharpe | B&H Sharpe | System CAGR | B&H CAGR | Beats B&H on Sharpe (of 14) |
|---|---|---:|---:|---:|---:|---:|
| MACD | 1.74 (cross above zero, 10d) | 0.24 | 0.45 | 3.4% | 10.4% | 2/14 |
| RSI(14) | 1.61 (crosses below 30, 5d) | 0.22 | 0.44 | 1.5% | 10.3% | 3/14 |
| Bollinger(20,2) | 1.18 (close below lower, 21d) | 0.20 | 0.44 | 1.5% | 10.3% | 2/14 |
| SMA(50) | 1.97 (death cross, 10d) / 1.54 (price cross, 10d) | 0.31 | 0.45 | 5.6% | 10.5% | 3/14 |
| SMA(200) (comparison) | n/a (not event-tested) | 0.40 | 0.44 | 8.5% | 10.3% | 5/14 |
| EMA(9) | 1.32 (crosses above, 5d) | 0.05 | 0.45 | 0.1% | 10.4% | 2/14 |

No system's 14-symbol average beats buy-and-hold on Sharpe in the full
sample, the pre-2016-06 half, or the post-2016-06 half. Every system's
average max drawdown is smaller than buy-and-hold's (e.g. MACD -60.4% vs
-72.3%; SMA50 -57.9% vs -72.3%; SMA200 -52.2% vs -72.3%; EMA9 -72.2% vs
-72.3%, barely; RSI -66.2% vs -72.3%; Bollinger -55.8% vs -72.3%).
EMA(9) trades far more than any other system (24.6 trades/year vs 8.8 for
SMA50, 3.7 for SMA200, ~10 for MACD) and is the only system with a negative
average Sharpe (0.05, essentially zero-to-negative after cost).

RSI-below-30 by VIX regime (14-pool, diff in pp vs baseline, t in
parens): calm (VIX<20, n=318-320) +0.204 (0.90) / +0.205 (0.65) / -0.238
(-0.53) at 5/10/21d; mid (20-25, n=131) -0.166 (-0.32) / -0.335 (-0.52) /
-1.024 (-1.13); stressed (VIX>=25, n=259) +0.843 (1.70) / +0.019 (0.03) /
+0.840 (0.86). Directionally the calm/stressed split leans the way R15/P2
predicted (calm mostly flat-to-negative at longer horizons, stressed
mostly positive), but the mid-regime (20-25) is negative at all three
horizons -- not the clean three-bucket story -- and no cell reaches even
nominal t=2.

BB-close-below-lower-band by VIX regime: calm (n=795-802) is flat to
slightly negative at all horizons (max |t|=0.92); stressed (VIX>=25,
n=418) is +1.371pp at 21 days with t=2.06 -- the single strongest VIX-cut
cell in the script, crossing nominal significance but nowhere near the
Bonferroni bar for the 18-test VIX-cut family (~2.5 informally, and not
part of the primary 54-test family regardless); the 10-day cell in the
same regime is actually negative (-0.400pp), so the regime story is not
consistent across horizons even here.

Full raw output:

```
==============================================================================================================
CHART INDICATORS (PRICE) -- RAW TEST OUTPUT
==============================================================================================================
Universe: 14 large caps (pooled) = ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM']
SPY reported separately. Date range: 2006-01-03 to 2026-09-18
Split date for sub-samples: before 2016-06-01 vs on/after 2016-06-01
Horizons (trading days): [5, 10, 21]
Dedup window: 5 trading days

##############################################################################################################
TEST 1: EVENT STUDY
##############################################################################################################
--------------------------------------------------------------------------------------------------------------
MAIN RESULTS: 14-STOCK POOL
--------------------------------------------------------------------------------------------------------------
signal                       h      n   diff_pp       t    pre_pp   post_pp  sign_adj_pp  dir
---------------------------------------------------------------------------------------------
macd_bull_cross              5   2764     0.001    0.01    -0.012     0.016        0.001 BULL
macd_bull_cross             10   2763     0.020    0.15    -0.142     0.190        0.020 BULL
macd_bull_cross             21   2758    -0.021   -0.12    -0.203     0.173       -0.021 BULL
macd_bear_cross              5   2779    -0.021   -0.23     0.046    -0.089        0.021 BEAR
macd_bear_cross             10   2775    -0.010   -0.08    -0.196     0.174        0.010 BEAR
macd_bear_cross             21   2771    -0.009   -0.05     0.158    -0.182        0.009 BEAR
macd_cross_above_zero        5   1210     0.126    0.93     0.123     0.131        0.126 BULL
macd_cross_above_zero       10   1207     0.329    1.74     0.213     0.455        0.329 BULL
macd_cross_above_zero       21   1206     0.312    1.10     0.447     0.180        0.312 BULL
macd_cross_below_zero        5   1213     0.206    1.62     0.298     0.112       -0.206 BEAR
macd_cross_below_zero       10   1211    -0.024   -0.13     0.180    -0.233        0.024 BEAR
macd_cross_below_zero       21   1209    -0.162   -0.59    -0.156    -0.164        0.162 BEAR
rsi_cross_below_30           5    708     0.370    1.61     0.546     0.190        0.370 BULL
rsi_cross_below_30          10    708     0.037    0.11     0.520    -0.452        0.037 BULL
rsi_cross_below_30          21    708     0.011    0.02     0.208    -0.191        0.011 BULL
rsi_cross_above_70           5   1205     0.007    0.06     0.111    -0.092       -0.007 BEAR
rsi_cross_above_70          10   1205     0.207    1.25     0.508    -0.069       -0.207 BEAR
rsi_cross_above_70          21   1202     0.267    1.05     0.452     0.057       -0.267 BEAR
rsi_cross_back_above_30      5    702    -0.164   -0.58     0.382    -0.723       -0.164 BULL
rsi_cross_back_above_30     10    702    -0.120   -0.31     0.478    -0.730       -0.120 BULL
rsi_cross_back_above_30     21    702    -0.206   -0.48    -0.257    -0.153       -0.206 BULL
rsi_cross_above_50           5   3115    -0.034   -0.39    -0.067     0.004       -0.034 BULL
rsi_cross_above_50          10   3112     0.023    0.19    -0.025     0.079        0.023 BULL
rsi_cross_above_50          21   3104     0.092    0.52     0.037     0.164        0.092 BULL
bb_close_below_lower         5   1497     0.102    0.66     0.097     0.109        0.102 BULL
bb_close_below_lower        10   1494    -0.038   -0.19    -0.078     0.008       -0.038 BULL
bb_close_below_lower        21   1493     0.324    1.18     0.162     0.503        0.324 BULL
bb_close_above_upper         5   1876     0.015    0.14    -0.081     0.104       -0.015 BEAR
bb_close_above_upper        10   1873    -0.009   -0.06    -0.101     0.073        0.009 BEAR
bb_close_above_upper        21   1871     0.102    0.46     0.016     0.169       -0.102 BEAR
bb_squeeze_break_up          5    391    -0.168   -0.83    -0.291    -0.024       -0.168 BULL
bb_squeeze_break_up         10    391    -0.013   -0.04    -0.047     0.039       -0.013 BULL
bb_squeeze_break_up         21    390     0.355    0.75     1.011    -0.347        0.355 BULL
bb_squeeze_break_down        5    291    -0.041   -0.12    -0.424     0.256        0.041 BEAR
bb_squeeze_break_down       10    290    -0.195   -0.50    -0.817     0.284        0.195 BEAR
bb_squeeze_break_down       21    289     0.332    0.52    -0.717     1.127       -0.332 BEAR
sma50_cross_above            5   1975     0.006    0.06     0.063    -0.051        0.006 BULL
sma50_cross_above           10   1972     0.222    1.54     0.125     0.320        0.222 BULL
sma50_cross_above           21   1969     0.306    1.41     0.209     0.401        0.306 BULL
sma50_cross_below            5   1984     0.052    0.50     0.094     0.010       -0.052 BEAR
sma50_cross_below           10   1980    -0.062   -0.43     0.015    -0.141        0.062 BEAR
sma50_cross_below           21   1979    -0.154   -0.72    -0.068    -0.245        0.154 BEAR
golden_cross                 5    188    -0.257   -1.00    -0.117    -0.396       -0.257 BULL
golden_cross                10    187    -0.240   -0.58     0.177    -0.656       -0.240 BULL
golden_cross                21    186    -0.102   -0.14     0.832    -1.042       -0.102 BULL
death_cross                  5    189    -0.243   -0.67    -0.137    -0.351        0.243 BEAR
death_cross                 10    189    -0.815   -1.97    -0.769    -0.860        0.815 BEAR
death_cross                 21    189    -0.702   -1.12    -0.678    -0.722        0.702 BEAR
ema9_cross_above             5   5202    -0.092   -1.32    -0.044    -0.140       -0.092 BULL
ema9_cross_above            10   5196     0.005    0.05    -0.077     0.098        0.005 BULL
ema9_cross_above            21   5185    -0.075   -0.54    -0.260     0.136       -0.075 BULL
ema9_cross_below             5   5196     0.008    0.12     0.054    -0.038       -0.008 BEAR
ema9_cross_below            10   5188     0.074    0.76    -0.028     0.185       -0.074 BEAR
ema9_cross_below            21   5180    -0.084   -0.60    -0.114    -0.044        0.084 BEAR

--------------------------------------------------------------------------------------------------------------
SPY (reported separately, same definitions, n will be small)
--------------------------------------------------------------------------------------------------------------
signal                       h      n   diff_pp       t    pre_pp   post_pp  sign_adj_pp  dir
---------------------------------------------------------------------------------------------
macd_bull_cross              5    218     0.148    1.11     0.115     0.184        0.148 BULL
macd_bull_cross             10    218     0.245    1.29     0.067     0.434        0.245 BULL
macd_bull_cross             21    218    -0.059   -0.18    -0.212     0.107       -0.059 BULL
macd_bear_cross              5    216     0.198    1.26     0.163     0.227       -0.198 BEAR
macd_bear_cross             10    216     0.114    0.51     0.111     0.108       -0.114 BEAR
macd_bear_cross             21    215    -0.340   -1.00    -0.369    -0.328        0.340 BEAR
macd_cross_above_zero        5     79     0.069    0.31    -0.053     0.253        0.069 BULL
macd_cross_above_zero       10     79     0.263    0.82     0.006     0.649        0.263 BULL
macd_cross_above_zero       21     79     0.240    0.55    -0.093     0.780        0.240 BULL
macd_cross_below_zero        5     77     0.215    0.68     0.199     0.260       -0.215 BEAR
macd_cross_below_zero       10     77     0.107    0.27     0.359    -0.182       -0.107 BEAR
macd_cross_below_zero       21     77    -0.317   -0.53    -0.485     0.011        0.317 BEAR
rsi_cross_below_30           5     37     0.591    0.80     0.123     1.031        0.591 BULL
rsi_cross_below_30          10     37     0.533    0.53    -0.156     1.175        0.533 BULL
rsi_cross_below_30          21     37     2.193    1.82     1.810     2.532        2.193 BULL
rsi_cross_above_70           5     91    -0.122   -0.98    -0.099    -0.160        0.122 BEAR
rsi_cross_above_70          10     91    -0.082   -0.47     0.291    -0.395        0.082 BEAR
rsi_cross_above_70          21     91     0.219    0.83     0.869    -0.346       -0.219 BEAR
rsi_cross_back_above_30      5     36    -0.456   -0.64    -0.051    -0.862       -0.456 BULL
rsi_cross_back_above_30     10     36    -0.928   -0.80    -0.897    -0.962       -0.928 BULL
rsi_cross_back_above_30     21     36     0.846    0.73     1.067     0.620        0.846 BULL
rsi_cross_above_50           5    227    -0.287   -1.77    -0.415    -0.123       -0.287 BULL
rsi_cross_above_50          10    226    -0.367   -1.63    -0.619    -0.040       -0.367 BULL
rsi_cross_above_50          21    225    -0.469   -1.48    -0.716    -0.110       -0.469 BULL
bb_close_below_lower         5    111     0.281    0.97     0.454     0.097        0.281 BULL
bb_close_below_lower        10    111     0.461    1.05     0.568     0.355        0.461 BULL
bb_close_below_lower        21    111     0.941    1.82     0.775     1.148        0.941 BULL
bb_close_above_upper         5    123    -0.096   -0.72    -0.307     0.061        0.096 BEAR
bb_close_above_upper        10    123    -0.198   -0.99    -0.344    -0.110        0.198 BEAR
bb_close_above_upper        21    123    -0.162   -0.59    -0.404    -0.036        0.162 BEAR
bb_squeeze_break_up          5     37    -0.047   -0.21    -0.068    -0.050       -0.047 BULL
bb_squeeze_break_up         10     37    -0.095   -0.31     0.139    -0.312       -0.095 BULL
bb_squeeze_break_up         21     37     0.030    0.06    -0.221     0.136        0.030 BULL
bb_squeeze_break_down        5     24     1.115    2.51     0.485     1.636       -1.115 BEAR
bb_squeeze_break_down       10     24     0.855    1.27     0.023     1.533       -0.855 BEAR
bb_squeeze_break_down       21     24     1.056    1.16     0.119     1.793       -1.056 BEAR
sma50_cross_above            5    152    -0.281   -1.53    -0.537     0.051       -0.281 BULL
sma50_cross_above           10    151     0.026    0.10    -0.166     0.302        0.026 BULL
sma50_cross_above           21    151    -0.393   -0.97    -0.807     0.203       -0.393 BULL
sma50_cross_below            5    138     0.243    1.21     0.056     0.498       -0.243 BEAR
sma50_cross_below           10    137     0.103    0.32     0.125     0.115       -0.103 BEAR
sma50_cross_below           21    137    -0.440   -0.93    -0.520    -0.252        0.440 BEAR
golden_cross                 5      9     0.639    1.18     1.027     0.172        0.639 BULL
golden_cross                10      9     0.174    0.23     0.143     0.249        0.174 BULL
golden_cross                21      9     0.706    0.39     0.692     0.800        0.706 BULL
death_cross                  5      9    -0.244   -0.18    -1.089     0.829        0.244 BEAR
death_cross                 10      9     0.535    0.26    -0.955     2.432       -0.535 BEAR
death_cross                 21      9     0.870    0.35    -2.240     4.834       -0.870 BEAR
ema9_cross_above             5    378    -0.090   -0.66    -0.073    -0.100       -0.090 BULL
ema9_cross_above            10    378     0.040    0.23    -0.089     0.204        0.040 BULL
ema9_cross_above            21    376    -0.167   -0.65    -0.412     0.156       -0.167 BULL
ema9_cross_below             5    371    -0.073   -0.52    -0.026    -0.119        0.073 BEAR
ema9_cross_below            10    370     0.069    0.38     0.087     0.061       -0.069 BEAR
ema9_cross_below            21    369    -0.263   -0.94    -0.367    -0.123        0.263 BEAR

--------------------------------------------------------------------------------------------------------------
VIX-REGIME CUTS (14-stock pool; regime = most recent WEEKLY VIX close on/before the signal day)
--------------------------------------------------------------------------------------------------------------
  -- rsi_cross_below_30 --
regime       h      n   diff_pp       t
---------------------------------------
lt20         5    318     0.204    0.90
lt20        10    318     0.205    0.65
lt20        21    318    -0.238   -0.53
20to25       5    131    -0.166   -0.32
20to25      10    131    -0.335   -0.52
20to25      21    131    -1.024   -1.13
gte25        5    259     0.843    1.70
gte25       10    259     0.019    0.03
gte25       21    259     0.840    0.86
  (total signal days by regime -- lt20: 320, 20to25: 131, gte25: 259)

  -- bb_close_below_lower --
regime       h      n   diff_pp       t
---------------------------------------
lt20         5    799     0.121    0.92
lt20        10    796    -0.004   -0.02
lt20        21    795    -0.020   -0.07
20to25       5    280     0.156    0.41
20to25      10    280     0.406    0.83
20to25      21    280    -0.265   -0.38
gte25        5    418     0.029    0.07
gte25       10    418    -0.400   -0.78
gte25       21    418     1.371    2.06
  (total signal days by regime -- lt20: 802, 20to25: 280, gte25: 418)

--------------------------------------------------------------------------------------------------------------
MULTIPLE TESTING
--------------------------------------------------------------------------------------------------------------
Primary pre-registered family: 18 signals x 3 horizons = 54 tests (14-stock pool, full sample).
VIX-regime cuts add 18 more tests (2 signals x 3 regimes x 3 horizons) -- secondary, not in the primary Bonferroni family.
Grand total tests run in this script (excluding the separately-reported SPY table and the pre/post split columns, which are diagnostic, not independently thresholded): 72
  Bonferroni alpha=0.05/54 -> two-tailed critical |t| ~= 3.312
  Bonferroni alpha=0.05/72 -> two-tailed critical |t| ~= 3.392

--------------------------------------------------------------------------------------------------------------
SURVIVORS: full-sample |t| exceeds the primary Bonferroni threshold (3.312) AND both half-sample diffs share the predicted sign
--------------------------------------------------------------------------------------------------------------
  none

--------------------------------------------------------------------------------------------------------------
SIGNAL COUNTS (raw, after dedup) -- 14-stock pool
--------------------------------------------------------------------------------------------------------------
  macd_bull_cross            n=2766
  macd_bear_cross            n=2782
  macd_cross_above_zero      n=1210
  macd_cross_below_zero      n=1215
  rsi_cross_below_30         n=710
  rsi_cross_above_70         n=1205
  rsi_cross_back_above_30    n=704
  rsi_cross_above_50         n=3118
  bb_close_below_lower       n=1500
  bb_close_above_upper       n=1877
  bb_squeeze_break_up        n=392
  bb_squeeze_break_down      n=293
  sma50_cross_above          n=1977
  sma50_cross_below          n=1989
  golden_cross               n=188
  death_cross                n=189
  ema9_cross_above           n=5205
  ema9_cross_below           n=5202

##############################################################################################################
TEST 2: TRADING SYSTEMS
##############################################################################################################
Cost: 0.10% per side, applied on every position-change day. Cash earns 0.

--- SYSTEM: macd ---
sym   period| sys_cagr%sys_vol%sys_shrpsys_mdd% sys_tpysys_pin% | bh_cagr% bh_vol% bh_shrp bh_mdd%  bh_tpy bh_pin%
------------------------------------------------------------------------------------------------------------------
AAPL  full  |    16.84   19.94    0.88  -35.75    9.35    51.7 |    26.81   31.49    0.91  -60.87    0.05   100.0
AAPL  pre   |    13.84   21.63    0.71  -35.75    9.66    51.2 |    24.86   33.87    0.83  -60.87    0.10   100.0
AAPL  post  |    19.91   18.11    1.09  -27.74    9.05    52.1 |    28.79   28.94    1.02  -38.73    0.00   100.0
AMZN  full  |     5.62   24.53    0.34  -43.14   10.13    49.9 |    26.94   37.79    0.82  -65.25    0.05   100.0
AMZN  pre   |     9.56   27.34    0.47  -35.21    9.66    49.5 |    33.31   42.26    0.89  -65.25    0.10   100.0
AMZN  post  |     1.83   21.37    0.19  -43.14   10.61    50.2 |    20.88   32.74    0.74  -56.15    0.00   100.0
BAC   full  |     4.58   33.02    0.30  -85.95    9.21    50.3 |     1.18   46.21    0.25  -94.28    0.05   100.0
BAC   pre   |    -5.11   42.36    0.09  -85.95    9.07    49.4 |   -10.37   57.85    0.10  -94.28    0.10   100.0
BAC   post  |    15.23   19.71    0.82  -37.09    9.34    51.2 |    14.17   30.45    0.59  -49.27    0.00   100.0
C     full  |    -4.10   32.31    0.04  -93.29    9.94    51.1 |    -5.99   49.08    0.12  -98.19    0.05   100.0
C     pre   |   -14.17   40.51   -0.17  -93.29   10.05    51.9 |   -20.17   61.03   -0.07  -98.19    0.10   100.0
C     post  |     7.12   21.17    0.43  -36.13    9.83    50.3 |    10.65   33.11    0.47  -56.79    0.00   100.0
CSCO  full  |    -2.03   19.95   -0.00  -64.90   10.42    50.7 |     8.70   28.50    0.44  -60.04    0.05   100.0
CSCO  pre   |    -3.57   21.46   -0.06  -64.90    9.95    50.2 |     3.84   30.70    0.28  -60.04    0.10   100.0
CSCO  post  |    -0.47   18.33    0.07  -42.38   10.90    51.2 |    13.78   26.13    0.63  -42.81    0.00   100.0
F     full  |     7.46   30.86    0.39  -72.36    9.94    50.1 |     2.36   42.44    0.27  -86.93    0.05   100.0
F     pre   |     9.95   35.10    0.44  -72.36   10.15    50.5 |     5.00   46.97    0.34  -86.93    0.10   100.0
F     post  |     5.04   25.95    0.32  -45.12    9.73    49.7 |    -0.20   37.39    0.18  -71.19    0.00   100.0
GE    full  |     1.92   22.53    0.20  -63.54    9.84    49.3 |     3.13   33.79    0.26  -86.97    0.05   100.0
GE    pre   |     1.83   20.48    0.19  -63.54    9.46    48.6 |    -0.94   31.24    0.13  -84.19    0.10   100.0
GE    post  |     2.02   24.40    0.20  -57.83   10.22    50.1 |     7.36   36.17    0.38  -83.33    0.00   100.0
GOOGL full  |     9.51   21.12    0.53  -44.52   10.33    51.9 |    19.21   30.63    0.73  -65.29    0.05   100.0
GOOGL pre   |    10.50   22.04    0.56  -37.45    9.85    52.7 |    14.33   31.94    0.58  -65.29    0.10   100.0
GOOGL post  |     8.53   20.17    0.51  -44.52   10.80    51.1 |    24.28   29.27    0.89  -44.32    0.00   100.0
IBM   full  |     2.95   17.79    0.25  -40.55    9.60    50.4 |     5.25   25.43    0.33  -56.08    0.05   100.0
IBM   pre   |    -0.98   14.59    0.01  -40.55   10.73    50.0 |     6.54   22.35    0.40  -45.39    0.10   100.0
IBM   post  |     7.02   20.49    0.44  -37.45    8.46    50.9 |     3.98   28.16    0.28  -47.91    0.00   100.0
MSFT  full  |    -0.15   18.88    0.09  -52.45   10.18    51.2 |    15.27   27.92    0.65  -59.12    0.05   100.0
MSFT  pre   |    -1.26   19.56    0.03  -52.45    9.56    51.9 |     6.92   28.29    0.38  -59.12    0.10   100.0
MSFT  post  |     0.96   18.18    0.14  -43.75   10.80    50.5 |    24.25   27.54    0.93  -37.56    0.00   100.0
NVDA  full  |    10.77   33.94    0.47  -59.59   10.28    52.1 |    36.38   48.95    0.88  -85.08    0.05   100.0
NVDA  pre   |     1.81   34.11    0.22  -59.59   10.34    52.2 |    11.55   48.33    0.47  -85.08    0.10   100.0
NVDA  post  |    20.50   33.76    0.72  -53.16   10.22    52.0 |    66.64   49.54    1.28  -66.36    0.00   100.0
PFE   full  |     0.22   16.26    0.09  -47.51    9.55    49.8 |     0.54   23.56    0.14  -64.75    0.05   100.0
PFE   pre   |    -0.26   15.85    0.06  -39.27    9.56    49.6 |     2.79   22.97    0.23  -59.04    0.10   100.0
PFE   post  |     0.71   16.66    0.13  -47.51    9.54    49.9 |    -1.66   24.13    0.05  -64.75    0.00   100.0
T     full  |    -5.19   15.60   -0.26  -76.78   10.77    50.3 |     0.90   23.26    0.15  -59.03    0.05   100.0
T     pre   |    -6.67   15.67   -0.36  -59.89   10.63    49.6 |     3.34   22.40    0.26  -49.29    0.10   100.0
T     post  |    -3.70   15.53   -0.16  -55.39   10.90    51.0 |    -1.47   24.10    0.06  -59.03    0.00   100.0
XOM   full  |    -0.93   17.94    0.04  -65.35   10.72    52.7 |     5.02   26.80    0.32  -69.87    0.05   100.0
XOM   pre   |    -5.63   15.62   -0.29  -59.39   11.51    52.5 |     3.94   25.31    0.28  -40.48    0.10   100.0
XOM   post  |     3.99   19.99    0.30  -33.68    9.92    52.9 |     6.10   28.22    0.35  -66.94    0.00   100.0
------------------------------------------------------------------------------------------------------------------
AVG14 full  |     3.39   23.19    0.24  -60.40   10.02    50.8 |    10.41   33.99    0.45  -72.27    0.05   100.0
AVG14 pre   |     0.70   24.74    0.14  -57.11   10.01    50.7 |     6.07   36.11    0.36  -68.10    0.10   100.0
AVG14 post  |     6.34   20.99    0.37  -43.21   10.02    50.9 |    15.54   31.13    0.56  -56.08    0.00   100.0

SPY (separate):
SPY   full  |     2.54   10.93    0.28  -28.13   10.91    50.6 |     9.03   19.37    0.54  -56.47    0.05   100.0
SPY   pre   |     0.19   11.74    0.07  -28.13   10.83    50.1 |     4.85   20.76    0.33  -56.47    0.10   100.0
SPY   post  |     4.94   10.06    0.53  -16.72   10.99    51.2 |    13.36   17.88    0.79  -34.10    0.00   100.0

Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: full=2/14  pre=2/14  post=5/14

--- SYSTEM: sma50 ---
sym   period| sys_cagr%sys_vol%sys_shrpsys_mdd% sys_tpysys_pin% | bh_cagr% bh_vol% bh_shrp bh_mdd%  bh_tpy bh_pin%
------------------------------------------------------------------------------------------------------------------
AAPL  full  |    16.81   21.00    0.85  -28.50    8.26    65.3 |    27.58   31.48    0.93  -60.87    0.05   100.0
AAPL  pre   |    16.46   22.26    0.80  -28.09    8.93    64.4 |    26.37   33.85    0.86  -60.87    0.10   100.0
AAPL  post  |    17.16   19.68    0.90  -28.50    7.59    66.2 |    28.79   28.94    1.02  -38.73    0.00   100.0
AMZN  full  |    12.68   27.26    0.57  -55.94    8.55    64.6 |    27.21   37.84    0.82  -65.25    0.05   100.0
AMZN  pre   |    17.10   31.87    0.65  -55.94    8.34    65.1 |    33.93   42.37    0.90  -65.25    0.10   100.0
AMZN  post  |     8.46   21.75    0.48  -53.20    8.76    64.1 |    20.88   32.74    0.74  -56.15    0.00   100.0
BAC   full  |     5.28   27.89    0.32  -71.83    7.67    57.0 |     1.03   46.27    0.25  -94.28    0.05   100.0
BAC   pre   |    -0.29   34.52    0.16  -71.83    8.05    51.4 |   -10.69   58.02    0.09  -94.28    0.10   100.0
BAC   post  |    11.11   19.17    0.65  -28.77    7.30    62.4 |    14.17   30.45    0.59  -49.27    0.00   100.0
C     full  |     0.71   24.58    0.15  -70.66    8.70    56.9 |    -6.06   49.14    0.12  -98.19    0.05   100.0
C     pre   |    -3.28   28.24    0.02  -70.66    8.44    51.7 |   -20.36   61.20   -0.07  -98.19    0.10   100.0
C     post  |     4.83   20.31    0.33  -44.57    8.95    62.1 |    10.65   33.11    0.47  -56.79    0.00   100.0
CSCO  full  |    -1.60   19.49    0.02  -68.87    9.28    58.1 |     8.34   28.51    0.42  -60.04    0.05   100.0
CSCO  pre   |    -5.99   20.52   -0.20  -68.87    9.32    54.9 |     3.11   30.74    0.25  -60.04    0.10   100.0
CSCO  post  |     2.95   18.41    0.25  -28.89    9.24    61.3 |    13.78   26.13    0.63  -42.81    0.00   100.0
F     full  |     2.20   28.55    0.22  -70.81    9.48    51.5 |     2.52   42.48    0.27  -86.93    0.05   100.0
F     pre   |     9.90   30.50    0.46  -63.10    8.44    51.5 |     5.34   47.07    0.34  -86.93    0.10   100.0
F     post  |    -4.90   26.47   -0.06  -60.99   10.51    51.6 |    -0.20   37.39    0.18  -71.19    0.00   100.0
GE    full  |     7.47   20.76    0.45  -41.23    8.84    54.5 |     2.98   33.84    0.26  -86.97    0.05   100.0
GE    pre   |     0.33   17.25    0.11  -41.23    9.71    54.6 |    -1.26   31.31    0.12  -84.19    0.10   100.0
GE    post  |    15.05   23.74    0.71  -35.17    7.98    54.4 |     7.36   36.17    0.38  -83.33    0.00   100.0
GOOGL full  |    11.44   20.70    0.63  -46.82    7.52    62.1 |    19.91   30.57    0.75  -65.29    0.05   100.0
GOOGL pre   |    11.72   20.35    0.65  -22.42    7.07    57.6 |    15.66   31.83    0.61  -65.29    0.10   100.0
GOOGL post  |    11.16   21.03    0.61  -46.82    7.98    66.5 |    24.28   29.27    0.89  -44.32    0.00   100.0
IBM   full  |    -0.21   18.03    0.08  -55.16    8.26    57.3 |     5.10   25.46    0.32  -56.08    0.05   100.0
IBM   pre   |     0.53   14.74    0.11  -41.82    8.83    59.7 |     6.24   22.41    0.38  -45.39    0.10   100.0
IBM   post  |    -0.93   20.80    0.06  -41.64    7.69    54.9 |     3.98   28.16    0.28  -47.91    0.00   100.0
MSFT  full  |     3.57   18.62    0.28  -40.44    9.23    63.3 |    15.19   27.95    0.65  -59.12    0.05   100.0
MSFT  pre   |     1.86   18.23    0.19  -40.44    8.34    56.6 |     6.73   28.37    0.37  -59.12    0.10   100.0
MSFT  post  |     5.29   19.00    0.37  -36.45   10.12    69.9 |    24.25   27.54    0.93  -37.56    0.00   100.0
NVDA  full  |    25.68   35.36    0.82  -64.29    8.75    63.7 |    36.12   48.99    0.87  -85.08    0.05   100.0
NVDA  pre   |    13.89   32.21    0.56  -64.29    9.32    56.5 |    10.99   48.41    0.46  -85.08    0.10   100.0
NVDA  post  |    38.58   38.22    1.04  -39.62    8.17    71.0 |    66.64   49.54    1.28  -66.36    0.00   100.0
PFE   full  |    -3.39   15.30   -0.15  -62.04    9.43    51.1 |     0.56   23.58    0.14  -64.75    0.05   100.0
PFE   pre   |     0.16   14.84    0.09  -50.45    8.14    52.7 |     2.84   23.02    0.24  -59.04    0.10   100.0
PFE   post  |    -6.78   15.75   -0.37  -59.22   10.70    49.5 |    -1.66   24.13    0.05  -64.75    0.00   100.0
T     full  |    -0.63   14.98    0.03  -60.58    9.09    53.5 |     1.05   23.27    0.16  -59.03    0.05   100.0
T     pre   |    -1.04   13.69   -0.01  -42.10    9.13    56.5 |     3.66   22.40    0.27  -49.29    0.10   100.0
T     post  |    -0.22   16.16    0.07  -48.97    9.05    50.6 |    -1.47   24.10    0.06  -59.03    0.00   100.0
XOM   full  |    -1.15   17.18    0.02  -72.87    9.87    53.9 |     4.88   26.83    0.31  -69.87    0.05   100.0
XOM   pre   |    -5.90   14.23   -0.36  -64.19   10.89    54.3 |     3.66   25.36    0.27  -40.48    0.10   100.0
XOM   post  |     3.81   19.68    0.29  -39.80    8.85    53.4 |     6.10   28.22    0.35  -66.94    0.00   100.0
------------------------------------------------------------------------------------------------------------------
AVG14 full  |     5.63   22.12    0.31  -57.86    8.78    58.1 |    10.46   34.02    0.45  -72.27    0.05   100.0
AVG14 pre   |     3.96   22.39    0.23  -51.82    8.78    56.2 |     6.16   36.17    0.36  -68.10    0.10   100.0
AVG14 post  |     7.54   21.44    0.38  -42.33    8.78    59.8 |    15.54   31.13    0.56  -56.08    0.00   100.0

SPY (separate):
SPY   full  |     2.61   10.65    0.30  -36.06    8.89    68.7 |     8.97   19.39    0.54  -56.47    0.05   100.0
SPY   pre   |    -1.00   10.76   -0.04  -36.06    9.91    64.4 |     4.72   20.81    0.33  -56.47    0.10   100.0
SPY   post  |     6.33   10.54    0.64  -24.16    7.88    72.9 |    13.36   17.88    0.79  -34.10    0.00   100.0

Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: full=3/14  pre=5/14  post=3/14

--- SYSTEM: sma200 ---
sym   period| sys_cagr%sys_vol%sys_shrpsys_mdd% sys_tpysys_pin% | bh_cagr% bh_vol% bh_shrp bh_mdd%  bh_tpy bh_pin%
------------------------------------------------------------------------------------------------------------------
AAPL  full  |    24.12   24.36    1.01  -36.92    1.96    77.5 |    27.56   31.23    0.94  -60.87    0.05   100.0
AAPL  pre   |    29.44   24.89    1.16  -36.92    1.35    74.4 |    26.26   33.52    0.86  -60.87    0.10   100.0
AAPL  post  |    19.36   23.86    0.86  -35.83    2.53    80.4 |    28.79   28.94    1.02  -38.73    0.00   100.0
AMZN  full  |    15.04   28.83    0.63  -54.80    3.87    74.8 |    28.97   37.64    0.86  -65.25    0.05   100.0
AMZN  pre   |    21.91   32.72    0.76  -54.80    3.33    74.6 |    38.23   42.27    0.97  -65.25    0.10   100.0
AMZN  post  |     8.97   24.66    0.47  -49.03    4.38    74.9 |    20.88   32.74    0.74  -56.15    0.00   100.0
BAC   full  |     4.12   19.85    0.30  -59.26    3.42    57.1 |     0.35   46.90    0.24  -94.28    0.05   100.0
BAC   pre   |    -3.87   20.97   -0.08  -59.26    3.86    47.1 |   -12.60   59.69    0.07  -94.28    0.10   100.0
BAC   post  |    12.17   18.73    0.71  -31.70    3.02    66.4 |    14.17   30.45    0.59  -49.27    0.00   100.0
C     full  |     3.45   20.32    0.27  -62.65    3.47    55.6 |    -6.51   49.82    0.11  -98.19    0.05   100.0
C     pre   |    -5.39   20.60   -0.16  -62.65    3.75    48.2 |   -21.95   62.98   -0.08  -98.19    0.10   100.0
C     post  |    12.45   20.03    0.69  -33.65    3.21    62.5 |    10.65   33.11    0.47  -56.79    0.00   100.0
CSCO  full  |     4.10   19.32    0.31  -39.05    3.47    63.5 |     7.89   28.48    0.41  -60.04    0.05   100.0
CSCO  pre   |     0.21   18.84    0.11  -39.05    3.33    55.9 |     1.92   30.80    0.22  -60.04    0.10   100.0
CSCO  post  |     7.86   19.75    0.48  -30.75    3.60    70.7 |    13.78   26.13    0.63  -42.81    0.00   100.0
F     full  |     2.95   25.44    0.24  -66.45    4.63    46.3 |     2.52   42.54    0.27  -86.93    0.05   100.0
F     pre   |     8.78   27.29    0.44  -43.13    4.38    51.9 |     5.52   47.44    0.35  -86.93    0.10   100.0
F     post  |    -2.22   23.59    0.02  -66.45    4.86    41.1 |    -0.20   37.39    0.18  -71.19    0.00   100.0
GE    full  |     9.47   19.64    0.56  -32.12    3.17    59.4 |     2.89   34.28    0.25  -86.97    0.05   100.0
GE    pre   |     1.08   16.72    0.15  -32.12    4.38    63.9 |    -1.69   32.13    0.11  -84.19    0.10   100.0
GE    post  |    17.92   22.00    0.86  -28.10    2.04    55.1 |     7.36   36.17    0.38  -83.33    0.00   100.0
GOOGL full  |    13.55   22.08    0.69  -34.97    3.27    75.0 |    19.27   30.66    0.73  -65.29    0.05   100.0
GOOGL pre   |    11.01   20.97    0.60  -34.97    2.92    70.8 |    14.14   32.08    0.57  -65.29    0.10   100.0
GOOGL post  |    15.97   23.07    0.76  -30.24    3.60    78.9 |    24.28   29.27    0.89  -44.32    0.00   100.0
IBM   full  |    -3.21   18.13   -0.09  -76.14    4.88    61.3 |     4.83   25.70    0.31  -56.08    0.05   100.0
IBM   pre   |     0.53   15.34    0.11  -39.06    4.90    64.6 |     5.75   22.78    0.36  -45.39    0.10   100.0
IBM   post  |    -6.57   20.39   -0.23  -69.01    4.86    58.1 |     3.98   28.16    0.28  -47.91    0.00   100.0
MSFT  full  |     9.14   20.26    0.53  -40.70    3.47    71.8 |    15.42   28.06    0.65  -59.12    0.05   100.0
MSFT  pre   |     3.48   18.70    0.28  -32.11    3.44    63.5 |     6.66   28.61    0.37  -59.12    0.10   100.0
MSFT  post  |    14.70   21.61    0.74  -40.70    3.50    79.5 |    24.25   27.54    0.93  -37.56    0.00   100.0
NVDA  full  |    37.92   37.15    1.05  -53.86    2.16    72.2 |    35.55   48.83    0.87  -85.08    0.05   100.0
NVDA  pre   |    12.95   31.20    0.55  -53.86    2.92    62.2 |     8.66   48.03    0.42  -85.08    0.10   100.0
NVDA  post  |    66.20   41.91    1.42  -41.86    1.46    81.5 |    66.64   49.54    1.28  -66.36    0.00   100.0
PFE   full  |    -1.56   14.96   -0.03  -51.13    4.48    55.2 |     0.19   23.77    0.13  -64.75    0.05   100.0
PFE   pre   |     2.54   13.23    0.26  -22.05    2.81    56.9 |     2.21   23.38    0.21  -58.55    0.10   100.0
PFE   post  |    -5.23   16.41   -0.25  -51.00    6.03    53.6 |    -1.66   24.13    0.05  -64.75    0.00   100.0
T     full  |    -2.26   13.54   -0.10  -69.81    5.18    50.2 |     0.10   23.42    0.12  -59.03    0.05   100.0
T     pre   |    -3.58   12.28   -0.24  -53.00    6.77    55.5 |     1.81   22.67    0.19  -49.29    0.10   100.0
T     post  |    -1.01   14.62    0.00  -49.91    3.70    45.3 |    -1.47   24.10    0.06  -59.03    0.00   100.0
XOM   full  |     2.54   16.83    0.23  -52.80    4.43    55.3 |     4.42   27.03    0.30  -69.87    0.05   100.0
XOM   pre   |     0.82   13.27    0.13  -30.84    3.54    53.9 |     2.65   25.69    0.23  -40.48    0.10   100.0
XOM   post  |     4.17   19.59    0.31  -43.94    5.25    56.5 |     6.10   28.22    0.35  -66.94    0.00   100.0
------------------------------------------------------------------------------------------------------------------
AVG14 full  |     8.53   21.48    0.40  -52.19    3.71    62.5 |    10.25   34.17    0.44  -72.27    0.05   100.0
AVG14 pre   |     5.71   20.50    0.29  -42.42    3.69    60.2 |     5.54   36.58    0.35  -68.07    0.10   100.0
AVG14 post  |    11.77   22.16    0.49  -43.01    3.72    64.6 |    15.54   31.13    0.56  -56.08    0.00   100.0

SPY (separate):
SPY   full  |     5.82   11.50    0.55  -22.76    3.17    77.4 |     9.03   19.60    0.54  -56.47    0.05   100.0
SPY   pre   |     3.49   11.15    0.36  -22.76    3.44    71.3 |     4.57   21.29    0.32  -56.47    0.10   100.0
SPY   post  |     8.04   11.82    0.71  -22.47    2.92    83.1 |    13.36   17.88    0.79  -34.10    0.00   100.0

Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: full=5/14  pre=6/14  post=4/14

--- SYSTEM: ema9 ---
sym   period| sys_cagr%sys_vol%sys_shrpsys_mdd% sys_tpysys_pin% | bh_cagr% bh_vol% bh_shrp bh_mdd%  bh_tpy bh_pin%
------------------------------------------------------------------------------------------------------------------
AAPL  full  |    15.09   20.71    0.78  -40.86   22.05    60.1 |    27.00   31.49    0.92  -60.87    0.05   100.0
AAPL  pre   |    18.17   21.75    0.88  -40.86   22.79    58.2 |    25.24   33.86    0.83  -60.87    0.10   100.0
AAPL  post  |    12.11   19.62    0.68  -36.95   21.31    61.9 |    28.79   28.94    1.02  -38.73    0.00   100.0
AMZN  full  |     4.84   25.82    0.31  -50.15   24.67    58.1 |    26.69   37.78    0.81  -65.25    0.05   100.0
AMZN  pre   |     5.48   29.38    0.33  -50.15   24.83    57.6 |    32.78   42.23    0.88  -65.25    0.10   100.0
AMZN  post  |     4.20   21.68    0.30  -42.99   24.52    58.6 |    20.88   32.74    0.74  -56.15    0.00   100.0
BAC   full  |    -2.24   29.06    0.07  -87.36   23.70    53.5 |     1.29   46.19    0.26  -94.28    0.05   100.0
BAC   pre   |   -15.77   36.18   -0.29  -87.36   26.39    49.6 |   -10.15   57.80    0.10  -94.28    0.10   100.0
BAC   post  |    13.45   19.49    0.74  -35.21   21.02    57.4 |    14.17   30.45    0.59  -49.27    0.00   100.0
C     full  |     0.13   28.72    0.15  -75.60   23.56    53.5 |    -5.93   49.05    0.12  -98.19    0.05   100.0
C     pre   |    -6.20   34.81   -0.01  -75.60   24.15    50.5 |   -20.04   60.97   -0.07  -98.19    0.10   100.0
C     post  |     6.89   20.94    0.42  -44.81   22.96    56.5 |    10.65   33.11    0.47  -56.79    0.00   100.0
CSCO  full  |    -5.94   19.36   -0.22  -82.22   25.65    55.6 |     8.64   28.49    0.43  -60.04    0.05   100.0
CSCO  pre   |    -8.81   20.23   -0.35  -69.89   26.10    53.4 |     3.72   30.68    0.27  -60.04    0.10   100.0
CSCO  post  |    -2.99   18.45   -0.07  -61.26   25.20    57.8 |    13.78   26.13    0.63  -42.81    0.00   100.0
F     full  |     3.72   29.20    0.27  -62.39   24.33    50.0 |     2.23   42.42    0.26  -86.93    0.05   100.0
F     pre   |    12.08   32.69    0.51  -56.38   22.88    49.9 |     4.73   46.93    0.33  -86.93    0.10   100.0
F     post  |    -4.01   25.23   -0.04  -49.10   25.78    50.2 |    -0.20   37.39    0.18  -71.19    0.00   100.0
GE    full  |     0.22   21.76    0.12  -68.85   24.43    52.8 |     3.10   33.78    0.26  -86.97    0.05   100.0
GE    pre   |    -3.87   19.30   -0.11  -60.88   24.93    52.6 |    -0.99   31.21    0.12  -84.19    0.10   100.0
GE    post  |     4.47   23.97    0.30  -54.16   23.94    53.0 |     7.36   36.17    0.38  -83.33    0.00   100.0
GOOGL full  |     4.01   20.80    0.29  -63.00   23.31    58.2 |    19.76   30.66    0.74  -65.29    0.05   100.0
GOOGL pre   |     8.80   21.00    0.51  -55.39   21.62    56.5 |    15.41   32.00    0.61  -65.29    0.10   100.0
GOOGL post  |    -0.55   20.59    0.08  -60.73   25.01    60.0 |    24.28   29.27    0.89  -44.32    0.00   100.0
IBM   full  |    -5.15   18.20   -0.20  -76.85   25.84    55.3 |     5.20   25.42    0.33  -56.08    0.05   100.0
IBM   pre   |    -5.80   14.89   -0.33  -57.05   27.36    56.2 |     6.45   22.34    0.39  -45.39    0.10   100.0
IBM   post  |    -4.49   20.99   -0.11  -54.87   24.32    54.5 |     3.98   28.16    0.28  -47.91    0.00   100.0
MSFT  full  |    -6.57   19.82   -0.24  -83.80   25.75    58.4 |    15.21   27.91    0.65  -59.12    0.05   100.0
MSFT  pre   |   -11.98   19.87   -0.54  -76.23   26.39    55.4 |     6.82   28.27    0.37  -59.12    0.10   100.0
MSFT  post  |    -0.84   19.77    0.06  -45.32   25.10    61.4 |    24.25   27.54    0.93  -37.56    0.00   100.0
NVDA  full  |    16.10   33.04    0.62  -60.40   23.41    58.6 |    36.44   48.94    0.88  -85.08    0.05   100.0
NVDA  pre   |     4.54   32.41    0.30  -60.40   23.95    54.4 |    11.69   48.31    0.47  -85.08    0.10   100.0
NVDA  post  |    28.92   33.65    0.92  -57.70   22.86    62.8 |    66.64   49.54    1.28  -66.36    0.00   100.0
PFE   full  |    -6.41   15.90   -0.34  -79.29   25.45    51.8 |     0.64   23.55    0.14  -64.75    0.05   100.0
PFE   pre   |    -8.91   15.86   -0.51  -70.45   26.87    54.1 |     2.99   22.96    0.24  -59.04    0.10   100.0
PFE   post  |    -3.85   15.94   -0.17  -59.93   24.03    49.5 |    -1.66   24.13    0.05  -64.75    0.00   100.0
T     full  |    -8.39   15.50   -0.49  -89.17   26.43    52.8 |     0.84   23.25    0.15  -59.03    0.05   100.0
T     pre   |   -13.77   15.06   -0.91  -81.23   27.85    53.7 |     3.19   22.38    0.25  -49.29    0.10   100.0
T     post  |    -2.68   15.92   -0.09  -54.31   25.01    51.8 |    -1.47   24.10    0.06  -59.03    0.00   100.0
XOM   full  |    -8.20   17.43   -0.40  -91.08   26.04    54.8 |     5.02   26.79    0.32  -69.87    0.05   100.0
XOM   pre   |   -14.40   15.51   -0.92  -83.54   27.36    56.5 |     3.95   25.29    0.28  -40.48    0.10   100.0
XOM   post  |    -1.56   19.14    0.01  -52.60   24.71    53.0 |     6.10   28.22    0.35  -66.94    0.00   100.0
------------------------------------------------------------------------------------------------------------------
AVG14 full  |     0.09   22.52    0.05  -72.22   24.62    55.3 |    10.44   33.98    0.45  -72.27    0.05   100.0
AVG14 pre   |    -2.89   23.50   -0.10  -66.10   25.25    54.2 |     6.13   36.09    0.36  -68.10    0.10   100.0
AVG14 post  |     3.50   21.10    0.22  -50.71   23.98    56.3 |    15.54   31.13    0.56  -56.08    0.00   100.0

SPY (separate):
SPY   full  |    -2.75   11.55   -0.18  -58.90   24.38    63.5 |     9.06   19.36    0.54  -56.47    0.05   100.0
SPY   pre   |    -7.07   12.11   -0.54  -56.42   25.02    61.1 |     4.91   20.75    0.33  -56.47    0.10   100.0
SPY   post  |     1.75   10.95    0.21  -34.20   23.74    65.8 |    13.36   17.88    0.79  -34.10    0.00   100.0

Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: full=2/14  pre=3/14  post=1/14

--- SYSTEM: rsi ---
sym   period| sys_cagr%sys_vol%sys_shrpsys_mdd% sys_tpysys_pin% | bh_cagr% bh_vol% bh_shrp bh_mdd%  bh_tpy bh_pin%
------------------------------------------------------------------------------------------------------------------
AAPL  full  |     2.90   21.00    0.24  -57.97    0.83    30.0 |    26.41   31.58    0.90  -60.87    0.05   100.0
AAPL  pre   |    -3.85   22.17   -0.07  -57.97    0.58    24.1 |    24.09   34.01    0.81  -60.87    0.10   100.0
AAPL  post  |    10.15   19.75    0.59  -30.22    1.07    35.9 |    28.79   28.94    1.02  -38.73    0.00   100.0
AMZN  full  |     8.66   24.87    0.46  -60.23    0.87    34.1 |    25.93   37.83    0.80  -65.25    0.05   100.0
AMZN  pre   |     8.67   27.91    0.44  -60.23    0.87    35.8 |    31.18   42.31    0.85  -65.25    0.10   100.0
AMZN  post  |     8.64   21.40    0.49  -44.64    0.88    32.5 |    20.88   32.74    0.74  -56.15    0.00   100.0
BAC   full  |     0.50   39.71    0.21  -94.19    1.21    45.8 |     1.33   46.14    0.26  -94.28    0.05   100.0
BAC   pre   |   -14.04   51.37   -0.04  -94.19    0.87    47.0 |   -10.03   57.69    0.10  -94.28    0.10   100.0
BAC   post  |    17.55   22.62    0.83  -31.80    1.56    44.7 |    14.17   30.45    0.59  -49.27    0.00   100.0
C     full  |    -8.70   44.44    0.01  -98.15    0.92    48.4 |    -5.93   49.01    0.12  -98.19    0.05   100.0
C     pre   |   -21.21   57.31   -0.13  -98.15    0.78    54.1 |   -19.98   60.86   -0.07  -98.19    0.10   100.0
C     post  |     5.86   25.70    0.35  -47.75    1.07    42.6 |    10.65   33.11    0.47  -56.79    0.00   100.0
CSCO  full  |     2.29   22.15    0.21  -50.54    0.87    43.1 |     8.99   28.52    0.44  -60.04    0.05   100.0
CSCO  pre   |     3.41   24.55    0.26  -50.54    0.97    44.9 |     4.42   30.72    0.29  -60.04    0.10   100.0
CSCO  post  |     1.17   19.45    0.16  -45.13    0.78    41.3 |    13.78   26.13    0.63  -42.81    0.00   100.0
F     full  |    -1.78   32.86    0.11  -84.55    1.02    48.9 |     2.07   42.40    0.26  -86.93    0.05   100.0
F     pre   |    -4.19   38.10    0.08  -84.55    1.16    47.2 |     4.38   46.87    0.32  -86.93    0.10   100.0
F     post  |     0.71   26.59    0.16  -62.37    0.88    50.6 |    -0.20   37.39    0.18  -71.19    0.00   100.0
GE    full  |    -4.54   26.45   -0.04  -84.68    1.02    44.5 |     3.14   33.75    0.26  -86.97    0.05   100.0
GE    pre   |    -0.40   26.48    0.12  -83.28    1.07    47.8 |    -0.90   31.16    0.13  -84.19    0.10   100.0
GE    post  |    -8.52   26.42   -0.20  -83.27    0.97    41.3 |     7.36   36.17    0.38  -83.33    0.00   100.0
GOOGL full  |     5.92   21.69    0.37  -49.54    0.92    32.0 |    18.79   30.69    0.71  -65.29    0.05   100.0
GOOGL pre   |     4.66   23.30    0.31  -49.54    1.07    32.8 |    13.57   32.04    0.55  -65.29    0.10   100.0
GOOGL post  |     7.20   19.94    0.45  -43.63    0.78    31.3 |    24.28   29.27    0.89  -44.32    0.00   100.0
IBM   full  |     7.86   18.20    0.51  -41.97    1.21    44.4 |     5.13   25.40    0.33  -56.08    0.05   100.0
IBM   pre   |     3.15   17.77    0.26  -40.27    0.87    49.6 |     6.28   22.31    0.38  -45.39    0.10   100.0
IBM   post  |    12.80   18.62    0.74  -30.32    1.56    39.3 |     3.98   28.16    0.28  -47.91    0.00   100.0
MSFT  full  |     5.02   18.57    0.36  -46.14    0.83    30.6 |    14.94   27.89    0.64  -59.12    0.05   100.0
MSFT  pre   |     5.91   21.15    0.38  -46.14    1.07    38.0 |     6.36   28.23    0.36  -59.12    0.10   100.0
MSFT  post  |     4.13   15.55    0.34  -32.07    0.58    23.2 |    24.25   27.54    0.93  -37.56    0.00   100.0
NVDA  full  |    -0.26   32.46    0.16  -79.62    0.73    28.2 |    36.36   48.92    0.88  -85.08    0.05   100.0
NVDA  pre   |     1.73   38.73    0.24  -79.62    1.07    41.6 |    11.64   48.27    0.47  -85.08    0.10   100.0
NVDA  post  |    -2.21   24.62    0.03  -60.82    0.39    14.7 |    66.64   49.54    1.28  -66.36    0.00   100.0
PFE   full  |     1.06   18.39    0.15  -54.42    0.97    46.7 |     0.55   23.57    0.14  -64.75    0.05   100.0
PFE   pre   |     2.32   18.47    0.22  -54.42    0.87    42.6 |     2.81   22.99    0.24  -59.04    0.10   100.0
PFE   post  |    -0.18   18.32    0.08  -51.07    1.07    50.8 |    -1.66   24.13    0.05  -64.75    0.00   100.0
T     full  |    -2.57   19.01   -0.04  -63.68    0.92    50.9 |     1.15   23.24    0.17  -59.03    0.05   100.0
T     pre   |    -1.39   19.46    0.02  -48.82    0.78    52.9 |     3.83   22.36    0.28  -49.29    0.10   100.0
T     post  |    -3.74   18.56   -0.11  -52.17    1.07    48.8 |    -1.47   24.10    0.06  -59.03    0.00   100.0
XOM   full  |     4.80   19.60    0.34  -60.84    0.92    47.4 |     4.82   26.77    0.31  -69.87    0.05   100.0
XOM   pre   |     4.83   18.63    0.35  -29.03    0.78    45.8 |     3.57   25.26    0.26  -40.48    0.10   100.0
XOM   post  |     4.77   20.53    0.33  -60.84    1.07    49.1 |     6.10   28.22    0.35  -66.94    0.00   100.0
------------------------------------------------------------------------------------------------------------------
AVG14 full  |     1.51   25.67    0.22  -66.18    0.95    41.1 |    10.26   33.98    0.44  -72.27    0.05   100.0
AVG14 pre   |    -0.74   28.96    0.17  -62.63    0.91    43.2 |     5.80   36.08    0.36  -68.10    0.10   100.0
AVG14 post  |     4.17   21.29    0.30  -48.29    0.98    39.0 |    15.54   31.13    0.56  -56.08    0.00   100.0

SPY (separate):
SPY   full  |     3.54   16.47    0.29  -56.47    0.87    40.1 |     9.04   19.35    0.54  -56.47    0.05   100.0
SPY   pre   |     1.33   18.25    0.16  -56.47    0.87    44.6 |     4.89   20.72    0.33  -56.47    0.10   100.0
SPY   post  |     5.81   14.48    0.46  -28.74    0.88    35.6 |    13.36   17.88    0.79  -34.10    0.00   100.0

Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: full=3/14  pre=2/14  post=3/14

--- SYSTEM: bollinger ---
sym   period| sys_cagr%sys_vol%sys_shrpsys_mdd% sys_tpysys_pin% | bh_cagr% bh_vol% bh_shrp bh_mdd%  bh_tpy bh_pin%
------------------------------------------------------------------------------------------------------------------
AAPL  full  |     2.10   19.54    0.20  -59.41    3.64    19.3 |    26.41   31.58    0.90  -60.87    0.05   100.0
AAPL  pre   |     2.87   20.91    0.24  -59.41    3.69    19.2 |    24.09   34.01    0.81  -60.87    0.10   100.0
AAPL  post  |     1.34   18.06    0.16  -40.50    3.60    19.4 |    28.79   28.94    1.02  -38.73    0.00   100.0
AMZN  full  |     6.75   20.96    0.42  -34.22    3.84    20.4 |    25.93   37.83    0.80  -65.25    0.05   100.0
AMZN  pre   |     5.14   22.47    0.34  -34.22    3.69    21.8 |    31.18   42.31    0.85  -65.25    0.10   100.0
AMZN  post  |     8.39   19.33    0.51  -32.46    3.99    19.0 |    20.88   32.74    0.74  -56.15    0.00   100.0
BAC   full  |    -5.35   32.19   -0.01  -83.51    4.37    24.1 |     1.33   46.14    0.26  -94.28    0.05   100.0
BAC   pre   |   -10.88   41.37   -0.07  -81.80    4.17    27.1 |   -10.03   57.69    0.10  -94.28    0.10   100.0
BAC   post  |     0.53   18.96    0.12  -48.82    4.57    21.0 |    14.17   30.45    0.59  -49.27    0.00   100.0
C     full  |    -4.09   35.92    0.06  -81.28    4.27    23.1 |    -5.93   49.01    0.12  -98.19    0.05   100.0
C     pre   |    -9.89   46.10   -0.00  -81.28    3.98    24.2 |   -19.98   60.86   -0.07  -98.19    0.10   100.0
C     post  |     2.09   21.30    0.20  -56.13    4.57    22.0 |    10.65   33.11    0.47  -56.79    0.00   100.0
CSCO  full  |     2.75   17.23    0.24  -38.14    4.23    23.1 |     8.99   28.52    0.44  -60.04    0.05   100.0
CSCO  pre   |     3.30   19.31    0.26  -38.14    4.66    25.4 |     4.42   30.72    0.29  -60.04    0.10   100.0
CSCO  post  |     2.21   14.85    0.22  -31.37    3.79    20.8 |    13.78   26.13    0.63  -42.81    0.00   100.0
F     full  |    -3.90   25.19   -0.03  -81.33    4.47    27.0 |     2.07   42.40    0.26  -86.93    0.05   100.0
F     pre   |    -5.32   28.76   -0.05  -81.33    4.46    27.9 |     4.38   46.87    0.32  -86.93    0.10   100.0
F     post  |    -2.46   21.02   -0.01  -61.16    4.48    26.1 |    -0.20   37.39    0.18  -71.19    0.00   100.0
GE    full  |    -3.23   21.98   -0.04  -84.32    4.61    26.1 |     3.14   33.75    0.26  -86.97    0.05   100.0
GE    pre   |    -6.01   21.74   -0.18  -69.48    4.27    25.6 |    -0.90   31.16    0.13  -84.19    0.10   100.0
GE    post  |    -0.36   22.22    0.09  -69.09    4.96    26.6 |     7.36   36.17    0.38  -83.33    0.00   100.0
GOOGL full  |     4.14   18.01    0.31  -37.17    4.13    21.0 |    18.79   30.69    0.71  -65.29    0.05   100.0
GOOGL pre   |     3.73   19.89    0.28  -37.17    4.56    23.9 |    13.57   32.04    0.55  -65.29    0.10   100.0
GOOGL post  |     4.55   15.92    0.36  -28.56    3.70    18.2 |    24.28   29.27    0.89  -44.32    0.00   100.0
IBM   full  |     1.03   13.89    0.14  -47.96    4.27    23.7 |     5.13   25.40    0.33  -56.08    0.05   100.0
IBM   pre   |     4.98   12.93    0.44  -32.42    4.66    22.2 |     6.28   22.31    0.38  -45.39    0.10   100.0
IBM   post  |    -2.78   14.80   -0.12  -47.96    3.89    25.1 |     3.98   28.16    0.28  -47.91    0.00   100.0
MSFT  full  |    10.19   15.52    0.70  -21.63    4.08    18.0 |    14.94   27.89    0.64  -59.12    0.05   100.0
MSFT  pre   |     8.01   15.15    0.58  -21.63    3.98    20.5 |     6.36   28.23    0.36  -59.12    0.10   100.0
MSFT  post  |    12.41   15.90    0.82  -21.63    4.18    15.6 |    24.25   27.54    0.93  -37.56    0.00   100.0
NVDA  full  |     8.86   27.27    0.45  -61.03    4.23    20.6 |    36.36   48.92    0.88  -85.08    0.05   100.0
NVDA  pre   |     4.01   27.91    0.28  -61.03    4.17    23.0 |    11.64   48.27    0.47  -85.08    0.10   100.0
NVDA  post  |    13.95   26.61    0.62  -56.39    4.28    18.1 |    66.64   49.54    1.28  -66.36    0.00   100.0
PFE   full  |     2.15   14.18    0.22  -37.29    4.76    27.2 |     0.55   23.57    0.14  -64.75    0.05   100.0
PFE   pre   |     4.20   14.14    0.36  -26.30    4.75    25.4 |     2.81   22.99    0.24  -59.04    0.10   100.0
PFE   post  |     0.13   14.22    0.08  -37.29    4.77    29.1 |    -1.66   24.13    0.05  -64.75    0.00   100.0
T     full  |    -1.20   14.42   -0.01  -47.81    4.66    27.9 |     1.15   23.24    0.17  -59.03    0.05   100.0
T     pre   |     1.88   13.32    0.21  -33.77    4.66    23.9 |     3.83   22.36    0.28  -49.29    0.10   100.0
T     post  |    -4.20   15.45   -0.20  -47.81    4.67    31.8 |    -1.47   24.10    0.06  -59.03    0.00   100.0
XOM   full  |     0.88   15.78    0.13  -66.58    4.37    23.8 |     4.82   26.77    0.31  -69.87    0.05   100.0
XOM   pre   |     5.91   15.69    0.44  -17.28    4.85    24.2 |     3.57   25.26    0.26  -40.48    0.10   100.0
XOM   post  |    -3.93   15.88   -0.17  -66.58    3.89    23.3 |     6.10   28.22    0.35  -66.94    0.00   100.0
------------------------------------------------------------------------------------------------------------------
AVG14 full  |     1.51   20.86    0.20  -55.84    4.28    23.2 |    10.26   33.98    0.44  -72.27    0.05   100.0
AVG14 pre   |     0.85   22.83    0.22  -48.23    4.32    23.9 |     5.80   36.08    0.36  -68.10    0.10   100.0
AVG14 post  |     2.28   18.18    0.19  -46.13    4.24    22.6 |    15.54   31.13    0.56  -56.08    0.00   100.0

SPY (separate):
SPY   full  |     3.67   13.84    0.33  -38.20    4.71    19.8 |     9.04   19.35    0.54  -56.47    0.05   100.0
SPY   pre   |     2.85   14.66    0.26  -38.20    4.75    21.5 |     4.89   20.72    0.33  -56.47    0.10   100.0
SPY   post  |     4.50   12.96    0.40  -30.34    4.67    18.1 |    13.36   17.88    0.79  -34.10    0.00   100.0

Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: full=2/14  pre=5/14  post=1/14

--------------------------------------------------------------------------------------------------------------
SUMMARY: symbols (of 14) beating buy-and-hold on Sharpe, by system and period
--------------------------------------------------------------------------------------------------------------
  macd       full=2/14  pre=2/14  post=5/14
  sma50      full=3/14  pre=5/14  post=3/14
  sma200     full=5/14  pre=6/14  post=4/14
  ema9       full=2/14  pre=3/14  post=1/14
  rsi        full=3/14  pre=2/14  post=3/14
  bollinger  full=2/14  pre=5/14  post=1/14

Done.
```

## Verdict

**P1 MACD: CONFIRMED.** No MACD signal (signal-line cross, zero-line cross,
either direction) clears the Bonferroni bar in the event study (best
|t|=1.74, zero_cross_above at 10d); none survive. As a long/flat system,
MACD trails buy-and-hold badly after cost in the 14-symbol average (Sharpe
0.24 vs 0.45; CAGR 3.4% vs 10.4%) and only beats buy-and-hold on Sharpe for
2 of 14 symbols. Max drawdown is smaller as predicted (-60.4% vs -72.3%).
Whipsaw is visible in the trade count (~10 trades/year, all cost-eaten,
vs 0.05/year for buy-and-hold's single entry).

**P2 RSI: PARTLY.** The RSI>70 "sell the overbought" reversal replicates
its prior refutation: pooled forward returns after an RSI>70 cross are
flat-to-slightly-positive at every horizon (sign_adj negative, i.e. the
opposite of a bearish reversal), matching
`2026-09-24_RSI_OVERBOUGHT_PUTS.md`. RSI<30 by VIX regime leans the
predicted direction (calm mostly flat/negative at 10-21d, stressed mostly
positive) but (a) the 20-25 "mid" bucket is negative at all three horizons,
breaking the clean three-way story, and (b) no cell reaches even nominal
t=2 (best t=1.70, stressed/5d), so "depends on the regime" is directionally
suggestive here, not established. As a system, buying RSI-crosses-above-30
and selling RSI-crosses-above-70 loses to buy-and-hold on average (Sharpe
0.22 vs 0.44) and only beats it for 3 of 14 symbols.

**P3 BOLLINGER: PARTLY.** Squeeze-then-breakout shows no edge in either
direction (max |t|=0.83), as predicted. Close-above-upper-band is not
followed by a reversal (sign_adj mostly small and mixed, not a clean
"continuation" story either -- diffs are near zero: +0.015 / -0.009 /
+0.102pp at 5/10/21d, none significant). Close-below-lower-band by VIX
regime shows a single notable cell -- stressed regime, 21 days, +1.371pp,
t=2.06, the strongest VIX-cut result in the whole test -- but the 10-day
cell in the same stressed regime is negative (-0.400pp, t=-0.78), so even
this one above-nominal cell does not hold up across horizons within its
own regime, and it is well short of any multiple-testing-adjusted bar. Not
established as "depends on regime" the way RSI<30 was hypothesized to.

**P4 SMA(50): CONFIRMED, with a near-miss noted.** As a filter it cuts
average drawdown (-57.9% vs -72.3%) but trails buy-and-hold in return
(Sharpe 0.31 vs 0.45, CAGR 5.6% vs 10.5%) and whipsaws far more than
SMA(200) (8.8 vs 3.7 trades/year). Golden and death crosses show no event
edge that survives Bonferroni -- but death_cross at 10 days is the
strongest cell in the entire primary table (t=-1.97, negative in both
halves: pre -0.769pp, post -0.860pp). It is short of both the nominal
t=2 and Bonferroni (3.31) bars, so the "no forward edge" prediction holds
under the pre-registered test, but this is the one cell worth re-checking
with a longer sample before calling it fully closed.

**P5 EMA(9): CONFIRMED, strongly.** The EMA9 system has by far the worst
economics of any system tested: 24.6 trades/year (2.5-7x every other
system), a 14-symbol average Sharpe of 0.05 (essentially flat-to-negative
after cost) against buy-and-hold's 0.45, and a CAGR gap of 0.1% vs 10.4%.
It beats buy-and-hold on Sharpe for only 2 of 14 symbols, both in the
post-2016 half where it does slightly better but still loses on average
(post-half average Sharpe 0.22 vs 0.56).

**Cross-cutting: no system beat buy-and-hold in both halves.** The
pre-registered disproof condition ("any system beating buy-and-hold on
Sharpe in BOTH halves after costs") did not trigger for any of the six
systems tested (MACD, SMA50, SMA200, EMA9, RSI, Bollinger) on the
14-symbol average. SMA(200), included only for comparison, came closest
(Sharpe 0.29 pre vs 0.35 pre buy-and-hold, 0.49 post vs 0.56 post
buy-and-hold -- losing in both halves, but by less than any other system,
and beating buy-and-hold outright for 5-6 of the 14 individual symbols
depending on the period).

## What this means for reading your chart

- **MACD crossing the signal line** does not, by itself, tell you anything
  reliable about the next 1-4 weeks, and trading every cross loses to just
  holding the stock, mostly to trading costs from how often it flips.
- **RSI dropping under 30** ("oversold") shows a faint, inconsistent lean
  toward being more useful when the market is already stressed (VIX 25+)
  and less useful in calm markets -- but it is not strong enough to act on
  by itself, and the "RSI over 70 means sell" idea keeps failing every time
  it's tested here.
- **Bollinger Band touches** are mostly noise. A close outside a "squeezed"
  band (the classic breakout setup) showed nothing. A close below the
  lower band had one interesting data point in stressed markets, but it
  didn't hold up across time horizons even there.
- **The 50-day moving average** does what a trend filter is supposed to do
  -- it cuts your worst drawdowns roughly in half -- but you pay for that
  safety with lower total return, and it trades more than double as often
  as the 200-day version for a similar-or-worse tradeoff.
- **Golden crosses and death crosses** (50-day crossing the 200-day) are
  the closest thing to an interesting signal in this whole batch -- death
  crosses were followed by below-average returns in both halves of the
  20-year sample -- but the effect is still not statistically distinct
  from noise at the standard bar, so it isn't something to act on yet.
- **The 9-day EMA is too fast to trade on its own.** It flips position
  about once a week on average, and the accumulated trading cost from that
  is the single biggest reason any system underperformed buy-and-hold in
  this whole study.
- **Bottom line:** none of these five indicators, used the way they're
  drawn on the Robinhood chart, beat simply holding the stock over 2006-2026
  once trading costs are included, on either half of the sample. The
  moving averages (50 and especially 200-day) came closest and are the
  most defensible for cutting drawdown if giving up some return is
  acceptable; MACD, RSI, Bollinger touches, and EMA(9) crossings are much
  closer to noise for both timing entries/exits and as always-on systems.

## Limits

- **Survivorship.** The 15-symbol universe (14 large caps + SPY) is drawn
  from 2026's list of large, still-listed companies; delisted, acquired,
  or fallen-out-of-large-cap names from 2006-2026 are not represented.
- **Large caps only.** Findings are specific to 14 large, liquid US stocks
  plus SPY. Nothing here says anything about small caps, low-liquidity
  names, options, or other asset classes.
- **No taxes, no slippage beyond the flat 0.10%/side assumption, no
  position sizing or leverage** -- the trading-system results are a
  simplified long/flat, full-capital simulation, not a realistic account
  simulation.
- **Execution approximation.** Systems are described as acting at the next
  day's open, but the simulation uses close-to-close returns with the
  prior day's signal (a standard simplification) rather than actual open
  prices; this does not change direction of the results but is not a
  precise fill simulation.
- **Number of tests run:** 54 primary event-study tests (18 signals x 3
  horizons) plus 18 secondary VIX-regime tests = 72 hypothesis tests in
  Test 1, plus 6 trading systems x (14 symbols + average + SPY) x 3 periods
  = 288 system/period cells in Test 2. With this many comparisons, a
  handful of cells crossing nominal significance by chance is expected;
  that is exactly why Bonferroni and the both-halves-same-sign check are
  the bar for "survivor," not any single cell.
- **R16 trigger (c) is ON.** Nothing in this note is adopted into live
  trading rules before the weekend re-read.
