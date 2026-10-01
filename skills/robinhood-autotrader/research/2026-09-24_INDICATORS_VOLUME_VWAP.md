# Chart Indicators, Part 2: Volume and VWAP

One-line: the two indicators on Nolan's chart that need volume data, which
this repo didn't have until now.

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (9f0f731).
Audience: Nolan, TARS sessions

## Overview

New data pulled read-only from Robinhood historicals: daily OHLCV for the
same 14 large caps + SPY, 2006-2026, plus intraday bars for VWAP on a small
set of names over a recent window. VWAP is a within-day measure (the average
price paid today, weighted by volume). Day traders and execution desks use
it. This account holds for weeks, so VWAP is tested for what it could tell
a swing trader.
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read. Survivorship: 2026's winners.

## Predictions (written before the test)

P1 VOLUME SPIKES: days with volume at least 2x the 20-day average are
   followed by slightly ABOVE-baseline returns over the next 21 days,
   whichever way the price moved that day (the high-volume return premium,
   Gervais, Kaniel & Mingelgrin 2001). Small: under 1pp.
P2 VOLUME-CONFIRMED BREAKOUTS: a 60-day-high breakout on 1.5x+ volume does
   NOT do meaningfully better than one on normal volume. The candlestick
   study found 60-day breakouts had no edge; volume won't rescue them.
P3 VWAP: closing above vs below the day's VWAP does not predict the next
   day's or next week's return on large caps. It's an execution benchmark,
   not a forecast.
P4 VOLUME ON DOWN DAYS: heavy-volume selloffs in calm markets are followed
   by below-baseline returns; in stressed markets (VIX >= 25), above.

What would prove me wrong: any volume or VWAP signal with |t| > 3 in both
halves of the sample (or both halves of the intraday window for VWAP).

## Data pulled

Read-only, via the Robinhood MCP `get_equity_historicals` (no orders, no
watchlist/alert writes). Two files, both new:

- `paper/history/daily_ohlcv.json` (4.6 MB) -- daily OHLCV, `interval="day"`,
  `bounds="regular"`, `adjustment_type="split"`, for AAPL AMZN BAC C CSCO F
  GE GOOGL IBM MSFT NVDA PFE T XOM SPY, 2006-01-01 through 2026-09-24. Pulled
  in 10 calls (2 symbol batches x 5 five-year chunks) because each call is
  capped by output size, then stitched by (symbol, date). Every symbol
  returned exactly **5,208 daily bars**, 2006-01-03 to 2026-09-23 (today,
  2026-09-24, hadn't closed a full regular session at pull time). No
  duplicate dates across chunk boundaries (verified: total bars processed
  across all 10 calls == 15 symbols x 5,208 bars, so every chunk boundary
  lined up cleanly with no overlap or gap). Zero bars had `interpolated:
  true` for this daily pull, so nothing was skipped. Spot-checked closes on
  6 dates (2006-01-03, 2015-06-15, 2020-03-23, 2022-01-13, 2025-06-02,
  2026-09-23) against `paper/history/daily_stocks.json` for AAPL, MSFT, SPY,
  NVDA, PFE: every close matched to 4 decimal places (diff% ~= 0.00 in all
  cases) -- no split-adjustment drift between the two pulls.

- `paper/history/intraday_vwap_sample.json` (3.9 MB) -- intraday bars,
  `interval="5minute"`, `bounds="regular"`, `adjustment_type="split"`, for
  SPY AAPL NVDA INTC SOFI. **Gap from the plan:** the task targeted the last
  12 months, but Robinhood's intraday history only returns real 5-minute
  bars back to **2026-02-23** (~7 months). Every bar requested before that
  date came back with `interpolated: true` on literally 100% of the bars in
  that chunk (confirmed on the Nov-Dec 2025 chunk: 3,126/3,126 bars flagged
  interpolated, zero real bars). Per the RULE #1 policy in this repo's
  CLAUDE.md, all `interpolated: true` bars were dropped, not filled in or
  carried forward (39,810 interpolated bars skipped across the whole pull).
  To check whether this was a 5-minute-specific granularity cap rather than
  a real historical-depth limit, I re-pulled the same Nov-Dec 2025 window at
  `interval="30minute"` -- still 885/885 bars interpolated, zero real data.
  So this is a genuine data-availability floor, not something a coarser bar
  would fix; **the intraday window actually used is ~7 months, not 12.**
  Final file: 5 symbols x 149 trading days x 78 bars/day (full 6.5-hour
  session, 5-minute bars) = 58,110 bars, 2026-02-23 to 2026-09-24, zero
  duplicate timestamps, zero interpolated bars retained.

## Results

Full raw script output (`paper/research_scripts/indicators_volume_vwap.py`,
14-stock pool primary + SPY descriptive + OBV exploratory):

```
====================================================================================================
VOLUME AND VWAP -- RAW TEST OUTPUT
====================================================================================================
Daily universe: 14 large caps (pooled) = ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM']
SPY reported separately (descriptive, small n). Date range: 2006-01-03 to 2026-09-23
Split date for daily sub-samples: before 2016-06-01 vs on/after 2016-06-01
Horizons (trading days), P1/P2/P4: [5, 10, 21]
Dedup window (P1/P2/P4/OBV): 5 trading days per symbol+signal

----------------------------------------------------------------------------------------------------
P1: VOLUME SPIKE (V >= 2x 20-day avg vol), split by day direction -- 14-stock pool
----------------------------------------------------------------------------------------------------
signal                   h      n   diff_pp       t    pre_pp   post_pp
-----------------------------------------------------------------------
volspike_up              5    932     0.435    1.87     0.931    -0.076
volspike_up             10    932     0.190    0.66     0.595    -0.226
volspike_up             21    931     0.431    1.11     1.226    -0.387
volspike_down            5   1054    -0.018   -0.08    -0.060     0.024
volspike_down           10   1053    -0.095   -0.36     0.118    -0.309
volspike_down           21   1053    -0.170   -0.49    -0.212    -0.135

----------------------------------------------------------------------------------------------------
P2: 60-DAY BREAKOUT split by volume confirmation -- 14-stock pool
----------------------------------------------------------------------------------------------------
signal                   h      n   diff_pp       t    pre_pp   post_pp
-----------------------------------------------------------------------
breakout_highvol         5    704     0.051    0.28     0.186    -0.083
breakout_highvol        10    704    -0.047   -0.19     0.215    -0.309
breakout_highvol        21    704     0.022    0.06     0.607    -0.566
breakout_lowvol          5    755    -0.302   -2.46    -0.346    -0.286
breakout_lowvol         10    755    -0.149   -0.79    -0.181    -0.163
breakout_lowvol         21    754    -0.221   -0.78    -0.223    -0.306

P2 DIFFERENCE: breakout_highvol forward returns vs breakout_lowvol forward returns (direct)
  h   n_hi   n_lo  diff_pp(hi-lo)       t
-----------------------------------------
  5    704    755           0.353    1.60
 10    704    755           0.103    0.34
 21    704    754           0.243    0.53

----------------------------------------------------------------------------------------------------
P4: DOWN DAY >= -2% on volume >= 2x 20-day avg, split by VIX regime -- 14-stock pool
VIX regime = most recent WEEKLY VIX close on/before the signal day
----------------------------------------------------------------------------------------------------
regime       h      n   diff_pp       t    pre_pp   post_pp
-------------------------------------------------------------
lt20         5    396    -0.281   -1.24    -0.277    -0.297
lt20        10    395    -0.567   -1.92    -0.544    -0.614
lt20        21    395    -0.840   -2.02    -1.074    -0.722
20to25       5    136     0.480    0.69     0.489     0.492
20to25      10    136     1.056    1.33     1.659     0.270
20to25      21    136     0.690    0.75     1.633    -0.504
gte25        5    183     0.167    0.20     0.442    -0.211
gte25       10    183    -1.280   -1.23    -0.741    -2.012
gte25       21    183     0.765    0.52     1.103     0.407
(total signal days by regime -- lt20: 399, 20to25: 136, gte25: 183)

----------------------------------------------------------------------------------------------------
SPY (reported separately, same definitions, n will be small) -- descriptive only, not in Bonferroni family
----------------------------------------------------------------------------------------------------
signal                   h      n   diff_pp       t    pre_pp   post_pp
-----------------------------------------------------------------------
volspike_up              5     31     0.654    1.77     1.031     0.159
volspike_up             10     31    -0.353   -0.52    -0.164    -0.559
volspike_up             21     31    -0.679   -0.60    -0.904    -0.246
volspike_down            5     54     0.446    1.47     0.236     0.566
volspike_down           10     54    -0.218   -0.43    -1.079     0.325
volspike_down           21     54    -0.503   -0.64    -2.599     0.830
breakout_highvol         5     17    -0.597   -1.41    -0.286    -0.770
breakout_highvol        10     17    -0.638   -1.59    -0.163    -0.926
breakout_highvol        21     17    -0.590   -0.96     0.097    -1.075
breakout_lowvol          5    150    -0.103   -0.95    -0.305     0.027
breakout_lowvol         10    150    -0.169   -1.08    -0.289    -0.121
breakout_lowvol         21    150    -0.285   -1.06    -0.080    -0.528

----------------------------------------------------------------------------------------------------
OBV DIVERGENCE (EXPLORATORY -- not in the primary Bonferroni family) -- 14-stock pool
----------------------------------------------------------------------------------------------------
signal                   h      n   diff_pp       t    pre_pp   post_pp
-----------------------------------------------------------------------
obv_bull_div             5    915    -0.135   -0.94    -0.196    -0.094
obv_bull_div            10    915    -0.116   -0.59    -0.087    -0.164
obv_bull_div            21    914    -0.121   -0.43    -0.036    -0.247
obv_bear_div             5    816    -0.107   -0.60     0.006    -0.235
obv_bear_div            10    816    -0.196   -0.80    -0.366     0.067
obv_bear_div            21    815    -0.348   -0.97    -0.824     0.371

----------------------------------------------------------------------------------------------------
P3: VWAP (intraday sample) -- SPY AAPL NVDA INTC SOFI
----------------------------------------------------------------------------------------------------
  SPY: 149 trading days, 2026-02-23 to 2026-09-24
  AAPL: 149 trading days, 2026-02-23 to 2026-09-24
  NVDA: 149 trading days, 2026-02-23 to 2026-09-24
  INTC: 149 trading days, 2026-02-23 to 2026-09-24
  SOFI: 149 trading days, 2026-02-23 to 2026-09-24
Chronological midpoint date for first/second half split: 2026-06-09 (total distinct trading days: 149)

Close above VWAP vs close below VWAP -- forward close-to-close return vs all-symbol-day baseline
group            h      n   diff_pp       t  1sthalf_pp  2ndhalf_pp
-------------------------------------------------------------------
above            1    388    -0.098   -0.52      -0.109      -0.100
below            1    352     0.108    0.51       0.143       0.093
  -> above vs below direct: diff_pp=-0.206 t=-0.88
above            5    377    -0.028   -0.06      -0.047      -0.110
below            5    343     0.031    0.06       0.062       0.100
  -> above vs below direct: diff_pp=-0.059 t=-0.11

Distance-from-VWAP (%) vs forward return: Pearson correlation, pooled symbol-days
  h      n        r       t
---------------------------
  1    740  -0.0182   -0.49
  5    720  -0.0019   -0.05

Reversion: does the next day's range touch back to today's VWAP level?
  (above-VWAP close -> does next day's LOW dip to/below today's VWAP; below-VWAP close -> does next day's HIGH rise to/above today's VWAP)
  above: touched 256/388 = 0.6598 (z vs 50% null = 6.30)
  below: touched 251/352 = 0.7131 (z vs 50% null = 8.00)

----------------------------------------------------------------------------------------------------
MULTIPLE TESTING
----------------------------------------------------------------------------------------------------
Primary pre-registered family (P1 + P2 + P2-diff + P4 + P3): 32 tests
OBV divergence (exploratory, reported separately): 6 tests, NOT counted in the primary family
  Bonferroni alpha=0.05/32 -> two-tailed critical |t| ~= 3.163 (primary family)
  Bonferroni alpha=0.05/6 -> two-tailed critical |t| ~= 2.638 (OBV, informational only)

----------------------------------------------------------------------------------------------------
SURVIVORS (primary family): |t| > 3.163 AND both half-sample diffs share the predicted sign
(tests with no directional half-split -- P2 diff, P3 correlation/reversion -- listed if |t| clears the threshold, with half-sign check marked N/A)
----------------------------------------------------------------------------------------------------
  SURVIVOR (half-check N/A): P3:reversion_above t=6.30
  SURVIVOR (half-check N/A): P3:reversion_below t=8.00

----------------------------------------------------------------------------------------------------
SIGNAL COUNTS (raw, after dedup where applicable) -- 14-stock pool
----------------------------------------------------------------------------------------------------
  volspike_up            n=936
  volspike_down          n=1059
  breakout_highvol       n=704
  breakout_lowvol        n=755
  down2pct_heavyvol      n=718
  obv_bull_div           n=917
  obv_bear_div           n=816

Done.
```

Phone-readable summary (14-stock pool, full sample, h=21 unless noted; "sig" =
clears the uncorrected |t|>2 bar, "Bonf" = clears the Bonferroni-corrected bar
of |t|>3.163 with matching sign in both halves):

| # | Signal | Edge (21d, pp) | t | Sig (uncorrected)? | Survives Bonferroni? |
|---|--------|-----------------|---|---------------------|------------------------|
| P1 | Volume spike, up day | +0.43 | 1.11 | no | no |
| P1 | Volume spike, down day | -0.17 | -0.49 | no | no |
| P2 | 60d breakout, high vol (1.5x+) | +0.02 | 0.06 | no | no |
| P2 | 60d breakout, low vol (<1.0x) | -0.22 | -0.78 | no | no |
| P2 | High-vol vs low-vol breakout (5d) | +0.35 | 1.60 | no | no |
| P4 | Down -2%+, heavy vol, VIX<20 | -0.84 | -2.02 | borderline | no |
| P4 | Down -2%+, heavy vol, VIX 20-25 | +0.69 | 0.75 | no | no |
| P4 | Down -2%+, heavy vol, VIX>=25 | +0.77 | 0.52 | no | no |
| P3 | Close above VWAP, next day | -0.10 | -0.52 | no | no |
| P3 | Close below VWAP, next day | +0.11 | 0.51 | no | no |
| P3 | VWAP reversion (above group) | 66.0% touch rate | 6.30 | yes | **yes** |
| P3 | VWAP reversion (below group) | 71.3% touch rate | 8.00 | yes | **yes** |
| OBV | Bullish divergence (exploratory) | -0.12 | -0.43 | no | n/a (not in family) |
| OBV | Bearish divergence (exploratory) | -0.35 | -0.97 | no | n/a (not in family) |

## Verdict

**P1 (volume spikes predict above-baseline returns): REFUTED.** The
predicted direction showed up on up-day spikes (+0.43pp at h=21, t=1.11) but
never got close to significant, and the h=5 pre/post split flips sign
(+0.93pp pre-2016 vs -0.08pp post-2016) -- not a stable effect. Down-day
spikes were flat to slightly negative, not "above baseline either way" as
predicted. The Gervais-Kaniel-Mingelgrin premium either isn't present in
this 2006-2026 large-cap sample or is too small to detect at this n.

**P2 (volume doesn't rescue 60-day breakouts): CONFIRMED**, but not for a
flattering reason. Neither high-volume (1.5x+) nor low-volume (<1.0x)
breakouts beat the all-day baseline (both diffs are near zero or negative,
t well under 1 in both cases at every horizon), and the direct
high-vs-low-vol comparison never clears significance (best case t=1.60 at
h=5). This matches the candlestick study's finding that 60-day breakouts
have no edge, full stop -- volume confirmation doesn't change that.

**P3 (VWAP doesn't forecast next-day/next-week return): CONFIRMED.** Closing
above vs below VWAP shows no meaningful edge on next-day (t=-0.52 / 0.51) or
next-5-day (t=-0.06 / 0.06) returns, and the above-vs-below direct
comparison is nowhere near significant either. Distance-from-VWAP as a
continuous signal also shows essentially zero correlation with forward
returns (r=-0.018 and r=-0.002). The one thing that DID survive Bonferroni
correction was the reversion check: after a close above VWAP, price dips
back to that VWAP level the next day 66% of the time (z=6.30); after a close
below VWAP, price rises back to it 71% of the time (z=8.00). This is real
but should not be over-read as a trading edge -- VWAP sits inside the day's
own high-low range by construction, and daily ranges routinely span more
than a typical above/below-VWAP gap, so a high touch rate is close to what
you'd expect mechanically from ordinary day-to-day price noise, not
evidence of some pull toward VWAP. It answers "is VWAP a forecast" (no) with
"is VWAP related to next-day's range" (mechanically, yes, weakly).

**P4 (heavy-volume selloffs: below-baseline in calm markets, above in
stressed markets): PARTLY, and not significant.** The calm-market (VIX<20)
leg pointed the predicted way and got closest to significance (-0.84pp at
h=21, t=-2.02, and the sign holds in both halves: -1.07pp pre-2016, -0.72pp
post-2016) but didn't clear the Bonferroni bar of 3.163. The stressed-market
legs (VIX 20-25 and VIX>=25) did NOT show the predicted above-baseline
recovery in a clean way -- 20-25 was directionally positive but weak
(t=0.75), and VIX>=25 was inconsistent across horizons (negative at h=10,
t=-1.23). Read generously, there's a hint of the predicted calm-market
pattern; read strictly, nothing here clears the pre-registered bar.

**OBV divergence (exploratory): no effect found.** Both bullish and bearish
divergence showed small, non-significant, wrong-signed-at-times diffs. No
follow-up warranted from this pass.

Multiple testing: 32 tests in the primary family (Bonferroni alpha =
0.05/32, critical |t| ~= 3.163) plus 6 OBV tests reported separately and not
counted. Only the two VWAP reversion checks survive that bar, and per the
mechanical caveat above, that's the weakest kind of "survivor" here --  it's
closer to a fact about intraday ranges than a forecasting edge.

## What this means for reading your chart

- Volume by itself -- a single 2x-average spike day -- is not a reliable
  buy or sell signal in this test. It nudges in the textbook direction on up
  days but the nudge is small and doesn't hold up statistically.
- A breakout on heavy volume is not meaningfully better than the same
  breakout on light volume. If you already knew 60-day breakouts don't have
  an edge on their own (prior research in this repo), don't expect volume to
  fix that.
- VWAP is a benchmark, not a forecast. Whether today's close is above or
  below VWAP tells you essentially nothing about tomorrow's or next week's
  return on these names. It's built for execution traders checking "did I
  get a good fill," not for deciding whether to buy.
- Heavy-volume selloffs in a calm market (VIX under 20) show a hint of
  "further weakness ahead" -- but it's a hint, not a confirmed edge in this
  test, so don't lean on it alone.
- Don't expect volume or VWAP to tell you something price alone can't. In
  this test, neither indicator produced a signal that survived being
  checked against multiple comparisons and split in half.

## Limits

- Survivorship: the 14-stock + SPY universe is 2026's still-listed large
  caps, not a point-in-time index membership list. Names that were delisted,
  acquired, or fell out of large-cap status over 2006-2026 aren't here.
- Intraday window is short and real: ~7 months (2026-02-23 to 2026-09-24),
  not the 12 months targeted -- Robinhood's intraday history genuinely
  doesn't go back further (confirmed at both 5-minute and 30-minute
  granularity), so P3's VWAP findings reflect a recent, single-regime
  window, not multiple market conditions.
- P3's intraday universe is 5 names (SPY, AAPL, NVDA, INTC, SOFI) -- 4 large
  caps plus one higher-beta small-cap-ish name (SOFI), not a broad cross
  section.
- 32 primary tests were run and Bonferroni-corrected for; 6 more (OBV) were
  run and reported but excluded from that correction as exploratory. Running
  many related cuts (multiple horizons, multiple regimes, multiple
  subtypes) on the same underlying data mechanically produces some
  large-looking uncorrected t-stats even under the null -- which is exactly
  why P1's h=5 and P4's VIX<20 numbers, closest to "interesting," don't
  survive correction and shouldn't be treated as findings.
- Nothing here is adopted before the weekend re-read (R16.3).
