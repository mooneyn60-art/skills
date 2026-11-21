# Candlesticks and Chart Lines: Can They Call a Breakout or a Breakdown?

One-line: RESEARCH_AGENDA item 23, Nolan's request ("how to read candles and
lines to see how the stock is going to break or boom"). Do classic
candlestick patterns and support/resistance breaks predict the next move?

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (060c26f).
Audience: Nolan, TARS sessions

## Overview

R16 trigger (c) is ON in the session that wrote this. Nothing here is
adopted before the weekend re-read.

Data: paper/history/daily_stocks.json, 14 large caps + SPY, daily OHLC,
2006-2026. Survivorship: 2026's winners. Forward returns measured against
the same names' unconditional baseline. Every pattern tested counts toward
multiple testing; the count is reported.

Patterns: hammer, shooting star, bullish/bearish engulfing, doji, morning
star, evening star, three white soldiers, three black crows. Lines:
breakout above the 60-day and 252-day high ("boom"), breakdown below the
60-day low ("break"), bounce off a prior 60-day swing low, and a
volume-free version of each (no volume data stored).

## Predictions (written before the test)

P1 CANDLESTICKS: no single or multi-bar candlestick pattern has a forward
   5 or 10-day edge that survives multiple testing AND holds in both halves
   of the sample. Most will show |t| < 2. At most one or two cross t = 2 by
   chance, and they won't replicate in the other half.
P2 BREAKOUTS ("boom"): new 252-day highs are followed by slightly
   ABOVE-baseline returns (the 52-week-high effect, George & Hwang 2004).
   Small: under 1pp over 21 days.
P3 BREAKDOWNS: new 60-day lows are followed by below-baseline returns when
   VIX is calm (< 20) and above-baseline when VIX >= 25. That's the R15
   finding again, from a different angle.
P4 SUPPORT BOUNCES: no edge.

What would prove P1 wrong: any candlestick pattern with a forward edge of
|t| > 3 in BOTH halves of the sample.

## Results

Test script: `paper/research_scripts/candlesticks.py`. Universe: 14 large
caps pooled (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T XOM),
2006-01-03 to 2026-09-18, SPY reported separately. Mechanical definitions
are written in full at the top of the script (hammer, shooting star, doji,
bullish/bearish engulfing, morning/evening star, three white
soldiers/crows, 60-day and 252-day breakout, 60-day breakdown, support
bounce), each with the trend-context requirement the classic definition
calls for (5-day decline before a hammer, 5-day rise before a shooting
star, etc; doji and the two 3-candle continuation shapes are defined
without a forced prior-trend filter, per the standard Nison definitions,
and that's called out as a simplification below).

39 pattern x horizon tests were run in the primary pre-registered family
(13 signals x 3 horizons, full 14-stock sample). The P3 VIX-regime cut on
60-day breakdowns adds 9 more (3 regimes x 3 horizons) = 48 total. Bonferroni
critical |t| at alpha=0.05/39 is ~3.22 (~3.28 for the 48-test count). **Zero
signals cleared that bar.** The largest full-sample |t| in the 14-stock pool
was hammer at the 10-day horizon (t=-2.36, i.e. hammers were followed by
*worse* forward returns than baseline, the opposite of the bullish
prediction) and bearish engulfing at 5 days (t=2.51, also the wrong sign:
forward returns ran *above* baseline). Both are well short of 3.22 and
neither is a "survivor" under the pre-registered rule (Bonferroni pass AND
same-sign in both halves).

Compact table, 10-day horizon, 14-stock pool (diff = signal mean forward
return minus baseline mean forward return, in percentage points; t = Welch
t-stat vs baseline; pre/post = same diff computed only before/on-or-after
2016-06-01):

| pattern | n | diff (pp) | t | pre-2016 diff (pp) | post-2016 diff (pp) |
|---|---:|---:|---:|---:|---:|
| hammer | 2236 | -0.361 | -2.36 | -0.284 | -0.436 |
| shooting_star | 2329 | -0.081 | -0.61 | -0.161 | -0.011 |
| doji | 4927 | -0.010 | -0.10 | -0.013 | -0.013 |
| bullish_engulfing | 1082 | -0.198 | -1.01 | -0.252 | -0.133 |
| bearish_engulfing | 1420 | 0.180 | 1.07 | 0.341 | 0.017 |
| morning_star | 469 | 0.302 | 0.94 | 0.164 | 0.451 |
| evening_star | 513 | -0.066 | -0.25 | -0.108 | -0.033 |
| three_white_soldiers | 161 | 0.521 | 1.40 | 0.971 | 0.109 |
| three_black_crows | 154 | -0.827 | -1.36 | -0.966 | -0.736 |
| breakout_60d | 1586 | -0.028 | -0.19 | 0.008 | -0.077 |
| breakout_252d | 915 | -0.019 | -0.10 | -0.260 | 0.100 |
| breakdown_60d | 867 | 0.073 | 0.24 | 0.066 | 0.085 |
| support_bounce | 1168 | 0.250 | 1.10 | 0.372 | 0.126 |

P3 breakdown-by-VIX-regime headline (60-day breakdown, most recent weekly
VIX close on/before the signal day): calm (VIX<20, n=405/403/403 at
5/10/21d) diffs are -0.135pp / -0.063pp / -0.491pp (t = -0.73 / -0.23 /
-1.12) — negative, the direction P3 predicted. Elevated (VIX>=25,
n=298) diffs are +0.610pp / -0.184pp / +0.877pp (t = 1.29 / -0.26 / 1.02) —
positive at 2 of 3 horizons, the direction P3 predicted, but flips sign at
10 days and no cell reaches even a nominal t=2, let alone Bonferroni.

Full raw output:

```
====================================================================================================
CANDLESTICKS AND CHART LINES -- RAW TEST OUTPUT
====================================================================================================
Universe: 14 large caps (pooled) = ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM']
SPY reported separately. Date range: 2006-01-03 to 2026-09-18
Split date for sub-samples: before 2016-06-01 vs on/after 2016-06-01
Horizons (trading days): [5, 10, 21]
Dedup window: 5 trading days (no repeat signal within window, per symbol+pattern)

----------------------------------------------------------------------------------------------------
MAIN RESULTS: 14-STOCK POOL
----------------------------------------------------------------------------------------------------
pattern                  h      n   diff_pp       t    pre_pp   post_pp  sign_adj_pp  dir
-----------------------------------------------------------------------------------------
hammer                   5   2240    -0.052   -0.48     0.007    -0.112       -0.052 BULL
hammer                  10   2236    -0.361   -2.36    -0.284    -0.436       -0.361 BULL
hammer                  21   2234    -0.274   -1.30    -0.184    -0.357       -0.274 BULL
shooting_star            5   2332    -0.055   -0.60    -0.068    -0.045        0.055 BEAR
shooting_star           10   2329    -0.081   -0.61    -0.161    -0.011        0.081 BEAR
shooting_star           21   2327    -0.210   -1.11    -0.388    -0.055        0.210 BEAR
doji                     5   4930    -0.004   -0.06    -0.019     0.008           NA NEUT
doji                    10   4927    -0.010   -0.10    -0.013    -0.013           NA NEUT
doji                    21   4918    -0.023   -0.17    -0.039    -0.020           NA NEUT
bullish_engulfing        5   1083    -0.221   -1.58    -0.303    -0.130       -0.221 BULL
bullish_engulfing       10   1082    -0.198   -1.01    -0.252    -0.133       -0.198 BULL
bullish_engulfing       21   1081    -0.281   -0.96    -0.574     0.047       -0.281 BULL
bearish_engulfing        5   1421     0.309    2.51     0.285     0.328       -0.309 BEAR
bearish_engulfing       10   1420     0.180    1.07     0.341     0.017       -0.180 BEAR
bearish_engulfing       21   1419     0.225    0.88     0.355     0.083       -0.225 BEAR
morning_star             5    469    -0.002   -0.01     0.296    -0.313       -0.002 BULL
morning_star            10    469     0.302    0.94     0.164     0.451        0.302 BULL
morning_star            21    468     0.423    0.92    -0.293     1.188        0.423 BULL
evening_star             5    513    -0.087   -0.44     0.014    -0.188        0.087 BEAR
evening_star            10    513    -0.066   -0.25    -0.108    -0.033        0.066 BEAR
evening_star            21    513    -0.156   -0.39    -0.033    -0.292        0.156 BEAR
three_white_soldiers     5    161     0.308    1.28     0.397     0.221        0.308 BULL
three_white_soldiers    10    161     0.521    1.40     0.971     0.109        0.521 BULL
three_white_soldiers    21    160     0.667    1.16     0.746     0.554        0.667 BULL
three_black_crows        5    154    -0.139   -0.39     0.355    -0.562        0.139 BEAR
three_black_crows       10    154    -0.827   -1.36    -0.966    -0.736        0.827 BEAR
three_black_crows       21    154    -1.465   -1.59    -1.252    -1.701        1.465 BEAR
breakout_60d             5   1586    -0.018   -0.17    -0.016    -0.027       -0.018 BULL
breakout_60d            10   1586    -0.028   -0.19     0.008    -0.077       -0.028 BULL
breakout_60d            21   1585    -0.078   -0.35    -0.032    -0.157       -0.078 BULL
breakout_252d            5    915    -0.032   -0.26    -0.222     0.076       -0.032 BULL
breakout_252d           10    915    -0.019   -0.10    -0.260     0.100       -0.019 BULL
breakout_252d           21    915    -0.058   -0.21    -0.488     0.130       -0.058 BULL
breakdown_60d            5    869     0.294    1.42     0.550     0.029       -0.294 BEAR
breakdown_60d           10    867     0.073    0.24     0.066     0.085       -0.073 BEAR
breakdown_60d           21    867     0.226    0.57     0.288     0.171       -0.226 BEAR
support_bounce           5   1171     0.229    1.26     0.511    -0.071        0.229 BULL
support_bounce          10   1168     0.250    1.10     0.372     0.126        0.250 BULL
support_bounce          21   1168     0.123    0.39     0.279    -0.025        0.123 BULL

----------------------------------------------------------------------------------------------------
SPY (reported separately, same definitions, n will be small)
----------------------------------------------------------------------------------------------------
pattern                  h      n   diff_pp       t    pre_pp   post_pp  sign_adj_pp  dir
-----------------------------------------------------------------------------------------
hammer                   5    160     0.071    0.31     0.144    -0.003        0.071 BULL
hammer                  10    160     0.077    0.27     0.202    -0.043        0.077 BULL
hammer                  21    159     0.253    0.64    -0.006     0.665        0.253 BULL
shooting_star            5    146    -0.117   -0.66     0.179    -0.407        0.117 BEAR
shooting_star           10    145     0.092    0.35     0.649    -0.461       -0.092 BEAR
shooting_star           21    145     0.285    0.90     0.371     0.189       -0.285 BEAR
doji                     5    363     0.026    0.21    -0.053     0.106           NA NEUT
doji                    10    362    -0.016   -0.09    -0.088     0.056           NA NEUT
doji                    21    361    -0.091   -0.33    -0.374     0.195           NA NEUT
bullish_engulfing        5     52    -0.689   -2.05    -0.402    -1.135       -0.689 BULL
bullish_engulfing       10     52    -0.295   -0.81     0.556    -1.666       -0.295 BULL
bullish_engulfing       21     52    -0.182   -0.27     1.182    -2.314       -0.182 BULL
bearish_engulfing        5    109     0.260    1.49     0.364     0.157       -0.260 BEAR
bearish_engulfing       10    109     0.182    0.75     0.321     0.040       -0.182 BEAR
bearish_engulfing       21    109    -0.036   -0.09     0.139    -0.220        0.036 BEAR
morning_star             5     44    -0.341   -0.95    -0.406    -0.263       -0.341 BULL
morning_star            10     44    -1.064   -1.55    -1.908    -0.128       -1.064 BULL
morning_star            21     44    -1.492   -1.87    -2.349    -0.528       -1.492 BULL
evening_star             5     43     0.093    0.33    -0.031     0.148       -0.093 BEAR
evening_star            10     43    -0.351   -0.82    -0.272    -0.458        0.351 BEAR
evening_star            21     43    -0.232   -0.44    -0.291    -0.313        0.232 BEAR
three_white_soldiers     5     13    -0.049   -0.11    -0.553     0.800       -0.049 BULL
three_white_soldiers    10     13     0.521    0.88     0.392     0.817        0.521 BULL
three_white_soldiers    21     13    -0.141   -0.18     0.109    -0.349       -0.141 BULL
three_black_crows        5      8     2.050    2.73     1.817     2.895       -2.050 BEAR
three_black_crows       10      8     2.571    2.79     2.464     3.191       -2.571 BEAR
three_black_crows       21      8     3.632    3.70     3.819     3.722       -3.632 BEAR
breakout_60d             5    177    -0.061   -0.63    -0.207     0.054       -0.061 BULL
breakout_60d            10    177    -0.200   -1.34    -0.342    -0.101       -0.200 BULL
breakout_60d            21    177    -0.182   -0.71    -0.201    -0.217       -0.182 BULL
breakout_252d            5    128    -0.108   -0.98    -0.360     0.026       -0.108 BULL
breakout_252d           10    128    -0.349   -1.93    -0.589    -0.251       -0.349 BULL
breakout_252d           21    128    -0.516   -1.64    -0.777    -0.474       -0.516 BULL
breakdown_60d            5     46     0.310    0.45     0.507     0.074       -0.310 BEAR
breakdown_60d           10     46     0.127    0.14     0.500    -0.316       -0.127 BEAR
breakdown_60d           21     46     0.937    0.83     0.613     1.451       -0.937 BEAR
support_bounce           5     64    -0.293   -0.49     0.246    -1.094       -0.293 BULL
support_bounce          10     64    -0.373   -0.56     0.193    -1.174       -0.373 BULL
support_bounce          21     64     0.032    0.04     0.620    -0.707        0.032 BULL

----------------------------------------------------------------------------------------------------
P3: 60-DAY BREAKDOWNS SPLIT BY VIX REGIME AT SIGNAL DAY (14-stock pool)
VIX regime = most recent WEEKLY VIX close on/before the signal day
----------------------------------------------------------------------------------------------------
regime       h      n   diff_pp       t
---------------------------------------
lt20         5    405    -0.135   -0.73
lt20        10    403    -0.063   -0.23
lt20        21    403    -0.491   -1.12
20to25       5    166     0.777    1.57
20to25      10    166     0.864    1.35
20to25      21    166     0.794    0.91
gte25        5    298     0.610    1.29
gte25       10    298    -0.184   -0.26
gte25       21    298     0.877    1.02
(total signal days by regime -- lt20: 405, 20to25: 166, gte25: 298)

----------------------------------------------------------------------------------------------------
MULTIPLE TESTING
----------------------------------------------------------------------------------------------------
Primary pre-registered family: 13 patterns x 3 horizons = 39 tests (14-stock pool, full sample).
P3 VIX-regime cut adds 9 more tests (3 regimes x 3 horizons) on the breakdown-60d signal specifically.
Grand total tests run in this script (excluding the separately-reported SPY table and the pre/post split columns, which are diagnostic, not independently thresholded): 48
  Bonferroni alpha=0.05/39 -> two-tailed critical |t| ~= 3.220
  Bonferroni alpha=0.05/48 -> two-tailed critical |t| ~= 3.279

----------------------------------------------------------------------------------------------------
SURVIVORS: full-sample |t| exceeds the primary Bonferroni threshold (3.220) AND both half-sample diffs share the predicted sign
----------------------------------------------------------------------------------------------------
  none

----------------------------------------------------------------------------------------------------
SIGNAL COUNTS (raw, after dedup) -- 14-stock pool
----------------------------------------------------------------------------------------------------
  hammer                 n=2242
  shooting_star          n=2333
  doji                   n=4936
  bullish_engulfing      n=1083
  bearish_engulfing      n=1421
  morning_star           n=469
  evening_star           n=513
  three_white_soldiers   n=161
  three_black_crows      n=154
  breakout_60d           n=1587
  breakout_252d          n=915
  breakdown_60d          n=869
  support_bounce         n=1171

Done.
```

## Verdict

**P1 CANDLESTICKS: CONFIRMED.** Zero of the 39 primary pattern x horizon
tests clear the Bonferroni bar (|t| > 3.22). Exactly two individual cells
cross the nominal |t| = 2 line the prediction flagged as the expected false-
positive count (hammer at 10 days, t=-2.36; bearish engulfing at 5 days,
t=2.51) — matching "at most one or two cross t=2 by chance." Both of those
two are also *wrong-signed* relative to the textbook reading (the "bullish"
hammer precedes below-baseline returns; the "bearish" engulfing precedes
above-baseline returns), which is itself evidence against, not for, the
textbook story. No pattern reaches |t| > 3 in both halves, the explicit
disproof condition. Nothing here says a candlestick pattern predicts the
next move.

**P2 BREAKOUTS ("boom"): REFUTED.** The predicted small *positive* 52-week-
high effect (under 1pp at 21 days) is not there. 252-day breakout diff at
21 days is -0.058pp (t=-0.21) — flat, and if anything slightly negative,
not positive. Small in magnitude as predicted, but the direction called for
did not show up in this sample.

**P3 BREAKDOWNS BY VIX REGIME: PARTLY.** The direction matches the
prediction more often than not — calm-VIX breakdowns are followed by
below-baseline returns at all three horizons, and elevated-VIX (>=25)
breakdowns are followed by above-baseline returns at 2 of 3 horizons — but
no single cell in the VIX-regime cut reaches even a nominal t=2 (max
|t|=1.57), so none of it is statistically distinguishable from noise on its
own. Directionally consistent with the R15 finding it was designed to
re-probe; not independently confirmed here.

**P4 SUPPORT BOUNCES: CONFIRMED.** No edge that clears significance:
diffs of 0.229 / 0.250 / 0.123pp at 5/10/21 days, t = 1.26 / 1.10 / 0.39 —
small, positive, and well short of both the nominal-2 and Bonferroni bars.

## What this means for reading charts

Watching for hammers, dojis, engulfing bars, morning/evening stars, or
three-soldier/crow runs on a daily chart of a large-cap stock did not, in
this 20-year sample, tell you anything reliable about what happens over the
next 1-4 weeks. Treat them as noise, not signals, for timing entries or
exits. New 52-week highs also carried no detectable edge here, despite the
academic "52-week-high effect" some traders cite — don't lean on a
breakout above the year's high by itself. The one thing that showed a
directionally consistent (though not statistically proven) pattern was new
60-day lows: they tended to keep falling when the market was calm (VIX
under 20) and tended to bounce when the market was already stressed (VIX
25+) — the same "don't fight a calm downtrend, don't chase a panic low"
idea R15 found before. That's the only item here worth a second look, and
even that one isn't strong enough to act on by itself. Support "bounces"
off a recent low showed no edge either way. Bottom line: for this account,
chart patterns are much weaker evidence than the price/volatility regime
signals already in use.

## Limits

- **Survivorship.** The 15-symbol universe (14 large caps + SPY) is drawn
  from 2026's list of large, still-listed companies. Names that were
  delisted, acquired, or fell out of the large-cap set over 2006-2026 are
  not represented, which biases the sample toward survivors.
- **No volume data.** Classic candlestick and breakout reading often uses
  volume confirmation (e.g. a breakout "on volume"). `daily_stocks.json`
  has no volume field, so every signal here is OHLC-only.
- **Large caps only.** All findings are specific to 14 large, liquid,
  well-covered US stocks plus SPY. Nothing here says anything about small
  caps, low-liquidity names, or other asset classes, where candlestick
  patterns are sometimes claimed to work better (or worse).
- **R16 trigger (c) is ON.** Nothing in this note is adopted into live
  trading rules before the weekend re-read.
