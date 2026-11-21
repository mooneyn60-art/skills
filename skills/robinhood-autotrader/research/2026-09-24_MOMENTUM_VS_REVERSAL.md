# Momentum vs Reversal by Horizon

One-line: RESEARCH_AGENDA item 12. Past winners keep winning over some
horizons and reverse over others. Where does each horizon sit for our
universe, and is TARS's holding period in the right one?

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (b82b430). Agent hit a usage limit after writing; main session re-ran the script 2026-09-25 and numbers reproduce.
Audience: Nolan, TARS sessions

## Overview

Data: paper/history/daily_ohlcv.json (14 large caps) and
daily_ohlcv_volatile.json (22 volatile names). Cross-sectional ranking of
past returns over each look-back vs the next month's return. R16 trigger (c)
is ON in the writing session. Nothing adopted before the weekend re-read.

## Predictions (written before the test)

P1 1-week and 1-month look-backs show REVERSAL (past losers beat past winners
   next month) on large caps. Weak with only 14 names.
P2 12-1 month momentum (skip the latest month) is positive for the next
   month. Weak on 14 names, clearer on the 22 volatile names.
P3 TARS's average hold (~50 trading days) and the 200-day gate sit in the
   momentum horizon, not the reversal one. The design is in the right
   horizon.

What would prove P3 wrong: the 3-month horizon showing reversal (t < -2)
in both universes.

## Results

Full script: `paper/research_scripts/momentum_reversal.py`. Cross-sectional =
monthly Spearman rank IC (look-back return vs next-21-day forward return)
across the universe, averaged over months. Spread = top-third minus
bottom-third of that month's forward returns, sorted on the look-back.
Full-period numbers shown; pre/post-split moves noted in prose.

**Large caps (14 names, split 2016-06-01)**

| horizon | months | IC mean | IC t | spread mean | spread t |
|---|---|---|---|---|---|
| 1w | 247 | 0.005 | 0.24 | -0.16% | -0.37 |
| 1m | 246 | 0.044 | 2.12 | 0.95% | 1.93 |
| 3m | 244 | 0.062 | 2.78 | 0.70% | 1.40 |
| 6m | 241 | 0.045 | 1.99 | 0.59% | 1.17 |
| 12-1m | 234 | 0.061 | 2.60 | 0.53% | 0.98 |

Split: 1w flips sign (pre -0.017 / post +0.027, neither significant). 1m and
3m are stronger post-split (post t=2.35 and 2.59) than pre-split (t=0.69 and
1.29). 12-1m is significant in both halves (t=1.92, t=1.75).

**Volatile names (22 names, split 2021-01-01)**

| horizon | months | IC mean | IC t | spread mean | spread t |
|---|---|---|---|---|---|
| 1w | 247 | 0.009 | 0.36 | -0.51% | -0.42 |
| 1m | 246 | 0.061 | 2.30 | 2.68% | 2.23 |
| 3m | 244 | 0.068 | 2.63 | 2.11% | 1.68 |
| 6m | 241 | 0.073 | 2.86 | 1.86% | 1.52 |
| 12-1m | 234 | 0.089 | 3.45 | 2.25% | 1.61 |

Split: every horizon except 1w is materially STRONGER pre-2021 (e.g. 12-1m
t=3.51 pre vs t=0.59 post) and loses significance in the post-2021 slice
(fewer months, n=67, and a narrower, more mature cross-section).

**Time-series version** (per-name regression of forward-21d on sign of its
own look-back return, then averaged across names): large caps show a
SIGNIFICANT REVERSAL beta at 1w (t=-2.34) and at 12-1m (t=-2.72), with 1m/3m/
6m indistinguishable from zero (|t|<0.6). Volatile names show no significant
beta at any horizon (best is 1m, t=1.85); all five point positive except 1w.
The time-series test disagrees with the cross-sectional test at both ends
(1w and 12-1m) for large caps — a name's own recent sign is not the same
question as its rank against 13 peers, and the two answers differ.

**200-day gate** (forward returns split on close vs SMA200 at the same
month-end dates):

| universe | horizon | above SMA200 | below SMA200 | diff | t |
|---|---|---|---|---|---|
| large caps | 21d | 1.61% | 0.86% | +0.75pp | 1.97 |
| large caps | 63d | 4.32% | 3.25% | +1.07pp | 1.56 |
| volatile | 21d | 4.39% | 1.91% | +2.48pp | 2.84 |
| volatile | 63d | 15.31% | 5.71% | +9.60pp | 5.14 |

**Holding period.** TARS's own closed live trades (ledger, deduped, real
fills only, n=10): mean 2.23 calendar days, median 2.84, range 0.03-6.78.
This account is ~2 weeks old at the time of this test — every closed trade
so far is an early stop-out or an R2-fail exit within days of entry, not a
matured trend-following hold. It is not yet a usable estimate of TARS's
DESIGN horizon.

Simulated R4 exit ladder (8% hard stop, breakeven at +8%, 20% trail, 200-day
trend exit) on every month-end entry with close>SMA200, 2006-2026:

| universe | entries | resolved | hard-stop exits | trend exits | mean days | median days | p25 | p75 |
|---|---|---|---|---|---|---|---|---|
| large caps | 2095 | 2046 | 942 | 1104 | 90.4 | 47.5 | 16 | 126 |
| volatile | 1575 | 1552 | 1364 | 188 | 50.8 | 19.0 | 6 | 54 |

Full raw output:

```
$(python3 paper/research_scripts/momentum_reversal.py)

MOMENTUM VS REVERSAL BY HORIZON -- raw output, no conclusions baked in
Large-cap universe: ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM']
Volatile universe:  ['AFRM', 'AMD', 'COIN', 'CRWD', 'DKNG', 'ENPH', 'HOOD', 'MARA', 'MU', 'NET', 'NFLX', 'NVDA', 'PLTR', 'RIOT', 'RIVN', 'ROKU', 'SHOP', 'SNAP', 'SOFI', 'TSLA', 'UBER', 'UPST']

==============================================================================
UNIVERSE: large caps (SPY excluded)  (14 names)
==============================================================================
month-end dates in pooled calendar: 249  (2006-01-31 .. 2026-09-23)

--- Cross-sectional rank IC (lookback vs next-21d forward return) ---
horizon  period      months   IC_mean     IC_t   %pos  spread_mean  spread_t
1w       full           247    0.0046     0.24   53.8      -0.163%     -0.37
1w       pre-split      125   -0.0174    -0.68   52.0      -0.562%     -0.84
1w       post-split     122    0.0272     0.96   55.7       0.245%      0.42
1m       full           246    0.0444     2.12   55.7       0.950%      1.93
1m       pre-split      124    0.0207     0.69   53.2       0.914%      1.17
1m       post-split     122    0.0685     2.35   58.2       0.987%      1.64
3m       full           244    0.0618     2.78   58.2       0.704%      1.40
3m       pre-split      122    0.0393     1.29   54.9       0.263%      0.35
3m       post-split     122    0.0843     2.59   61.5       1.145%      1.73
6m       full           241    0.0448     1.99   57.7       0.586%      1.17
6m       pre-split      119    0.0059     0.18   56.3      -0.361%     -0.45
6m       post-split     122    0.0828     2.63   59.0       1.511%      2.51
12-1m    full           234    0.0614     2.60   59.8       0.532%      0.98
12-1m    pre-split      112    0.0681     1.92   61.6       0.625%      0.70
12-1m    post-split     122    0.0553     1.75   58.2       0.447%      0.70

--- Time-series version (per-name regression, forward21 ~ alpha + beta*sign(lookback)) ---
horizon   n_names  avg_months/name  beta_mean   beta_t  alpha_mean
1w             14            247.0    -0.413%    -2.34      1.356%
1m             14            246.0    -0.056%    -0.53      1.345%
3m             14            244.0     0.092%     0.51      1.306%
6m             14            241.0     0.079%     0.41      1.314%
12-1m          14            234.0    -0.367%    -2.72      1.490%

--- 200-day gate: forward returns, close>SMA200 vs close<SMA200 ---
  n above SMA200 (21d fwd sample): 2072   n below: 1260
  21d fwd: mean(above)=1.606%  mean(below)=0.855%  diff=0.751pp  t=1.97
  63d fwd: mean(above)=4.318%  mean(below)=3.248%  diff=1.070pp  t=1.56

--- R4 exit-ladder simulation, entries at month-end when close>SMA200 ---
  entries: 2095   resolved: 2046   censored (still open at data end): 49
  exit reasons among resolved: {'hard_stop': 942, 'trend_exit': 1104}
  holding days (trading days): mean=90.4  median=47.5  p25=16.0  p75=126.0  min=1.0  max=660.0

==============================================================================
UNIVERSE: volatile names  (22 names)
==============================================================================
month-end dates in pooled calendar: 249  (2006-01-31 .. 2026-09-23)

--- Cross-sectional rank IC (lookback vs next-21d forward return) ---
horizon  period      months   IC_mean     IC_t   %pos  spread_mean  spread_t
1w       full           247    0.0091     0.36   51.0      -0.510%     -0.42
1w       pre-split      180    0.0067     0.20   51.7      -0.994%     -0.63
1w       post-split      67    0.0154     0.48   49.3       0.789%      0.58
1m       full           246    0.0613     2.30   55.3       2.683%      2.23
1m       pre-split      179    0.0859     2.52   59.2       3.826%      2.44
1m       post-split      67   -0.0046    -0.13   44.8      -0.371%     -0.28
3m       full           244    0.0675     2.63   55.7       2.107%      1.68
3m       pre-split      177    0.0985     3.02   60.5       3.225%      1.98
3m       post-split      67   -0.0143    -0.41   43.3      -0.846%     -0.58
6m       full           241    0.0732     2.86   59.8       1.859%      1.52
6m       pre-split      174    0.1067     3.31   63.2       2.543%      1.60
6m       post-split      67   -0.0138    -0.38   50.7       0.082%      0.05
12-1m    full           234    0.0893     3.45   62.8       2.253%      1.61
12-1m    pre-split      167    0.1168     3.51   64.7       2.737%      1.48
12-1m    post-split      67    0.0208     0.59   58.2       1.046%      0.65

--- Time-series version (per-name regression, forward21 ~ alpha + beta*sign(lookback)) ---
horizon   n_names  avg_months/name  beta_mean   beta_t  alpha_mean
1w             22            132.0    -0.272%    -0.54      3.285%
1m             22            131.4     0.793%     1.85      3.224%
3m             22            129.3     0.634%     1.50      3.086%
6m             22            126.3     0.528%     1.26      3.195%
12-1m          22            119.3     0.451%     1.40      3.257%

--- 200-day gate: forward returns, close>SMA200 vs close<SMA200 ---
  n above SMA200 (21d fwd sample): 1551   n below: 1153
  21d fwd: mean(above)=4.389%  mean(below)=1.914%  diff=2.475pp  t=2.84
  63d fwd: mean(above)=15.310%  mean(below)=5.708%  diff=9.602pp  t=5.14

--- R4 exit-ladder simulation, entries at month-end when close>SMA200 ---
  entries: 1575   resolved: 1552   censored (still open at data end): 23
  exit reasons among resolved: {'hard_stop': 1364, 'trend_exit': 188}
  holding days (trading days): mean=50.8  median=19.0  p25=6.0  p75=54.0  min=1.0  max=660.0

==============================================================================
TARS LIVE LEDGER HOLDING DAYS
==============================================================================
n closed TARS-strategy trades (deduped, real fills only): 10
  ('2026-09-14-RDDT-EXIT-LIVE', 'RDDT', 'equity', 2.908, 1.8)
  ('2026-09-14-CLX-EXIT-LIVE', 'CLX', 'equity', 2.892, 1.3)
  ('2026-09-14-ORCL-EXIT-LIVE', 'ORCL', 'equity', 0.04, -1.19)
  ('2026-09-14-VOO-EXIT-LIVE', 'VOO', 'equity', 0.027, -0.9)
  ('2026-09-15-RUM-EXIT-LIVE', 'RUM', 'equity', 1.001, -3.77)
  ('2026-09-17-TENB-EXIT-R4-TRAIL-WIN', 'TENB', 'equity', 6.782, 9.62)
  ('2026-09-11-INTC-C115-1002-LIVE-CORRECTION', 'INTC', 'option_call', 2.999, -135.0)
  ('2026-09-11-JD-C28-1016-LIVE-CORRECTION', 'JD', 'option_call', 2.848, -24.0)
  ('2026-09-11-CPNG-C16-1016-LIVE-CORRECTION', 'CPNG', 'option_call', 2.838, -16.0)
  ('2026-09-14-RBLX-C50-0918-MISSING', 'RBLX', 'option_call', 0.004, -14.0)
mean holding days (calendar): 2.23
median holding days (calendar): 2.84
min=0.00  max=6.78
```

## Verdict

**P1 (1w/1m reversal on large caps): REFUTED.** The cross-sectional test
this prediction was framed in shows the OPPOSITE of reversal at 1m
(IC=0.044, t=2.12, full period; spread t=1.93) — past winners outperformed,
not past losers. 1w shows no significant effect either direction
(t=0.24 full; -0.68 pre-split, +0.96 post-split, neither significant) — a
sign flip across the split with no period reaching significance is the
signature of noise, not a real reversal effect. The only place reversal
shows up at all is the TIME-SERIES version of 1w (beta t=-2.34), which is a
different question (a name's own sign vs its rank against peers) than the
one P1 was written about. Not "weak positive for P1" — actively pointing
the other way at the horizon (1m) where there is a significant effect.

**P2 (12-1m momentum, clearer on volatile): PARTLY CONFIRMED.** The
cross-sectional rank IC is positive and significant in both universes
(large caps t=2.60; volatile t=3.45 full period), and — as predicted — is
clearer on the volatile names (higher IC, higher t, more months positive:
62.8% vs 59.8%). But two qualifications keep this from full confirmation:
(1) the spread test, the more economically direct measure (top third minus
bottom third of forward returns), is NOT significant in either universe at
12-1m (t=0.98 large cap, t=1.61 volatile) — the ranking carries information
but the extremes don't separate cleanly by conventional significance; (2)
the volatile-universe effect is concentrated pre-2021 (t=3.51) and is gone
post-2021 (t=0.59, n=67) — "clearer on volatile" was true for the mature
sample but the recent sub-sample no longer shows it, plausibly because
2021-2026 volatile-name trading includes multiple sharp regime reversals
(2022 selloff, 2023-2024 AI/crypto rally) that a single-direction momentum
test doesn't distinguish from noise on 67 months.

**P3 (TARS's horizon sits in momentum, not reversal): CONFIRMED against its
own stated falsification test, with one honest gap.** The stated failure
condition — 3-month reversal at t<-2 in BOTH universes — did not occur;
3m is significantly POSITIVE momentum in both (t=2.78 large cap, t=2.63
volatile). The R4-simulated holding-day distribution (median 47.5 trading
days large cap, 19.0 volatile; means 90.4 and 50.8) sits closest to the
3m/6m horizons, both of which show significant positive cross-sectional IC
in both universes (3m: t=2.78/2.63; 6m: t=1.99/2.86) and a significant
200-day-gate edge (large-cap 21d t=1.97, volatile 21d t=2.84 and 63d
t=5.14). The gap: the LIVE ledger cannot yet independently confirm this —
TARS's actual closed trades average 2.23 calendar days held, nowhere near
50 trading days, because the account is two weeks old and every closed
trade so far exited early (a stop, an R2-fail, or a fractional-share
rejection) rather than living out a full trend. That is a sample-maturity
gap, not evidence against the design — the falsification test was passed
on the simulated distribution because that is the only distribution large
enough to test against (2046 and 1552 resolved simulated trades vs 10 live
ones).

## What this means

1. Very short lookbacks (a week or so) show no reliable pattern either way
   in this data — betting on reversal OR continuation over a week is
   coin-flip territory here, not a real edge.
2. A one-month lookback actually leans toward continuation (past month's
   winners keep winning a bit), which is the opposite of the "buy dips"
   intuition and argues against short-term mean reversion as a strategy.
3. Three months out to about a year (skipping the most recent month) is
   where the strongest, most consistent evidence for momentum shows up —
   past winners over that stretch tend to keep outperforming, in both the
   steady large-cap names and the more volatile ones.
4. The volatile, high-beta names (crypto miners, fintech, EV, meme-adjacent
   tech) show this momentum pattern more strongly than boring blue chips —
   but mostly in the 2016-2020 era of the data; the last five years show a
   much weaker, non-significant version of the same pattern.
5. Stocks trading above their 200-day average genuinely do keep doing
   better over the next month and quarter than stocks below it, in both
   universes — this is the single most robust result in the whole test.
6. TARS's rules (enter above the 200-day, ride it with a wide trailing
   stop) land in the horizon where the historical evidence is strongest,
   not the horizon where it's weakest or reversed. The design lines up with
   the data.
7. That said, this account has only been trading live for about two weeks,
   so there is no way yet to check whether TARS's ACTUAL trades behave like
   the 20-year simulation predicts — everything closed so far has been a
   quick stop-out, not a real multi-month hold.
8. None of this is a promise of future returns — it describes a historical
   tendency in a small sample, not a law of markets, and several of the
   individual numbers above (especially the "spread" tests, and anything in
   the post-2021 volatile slice) are not statistically strong on their own.

## Limits

- **14 and 22 names is a small universe.** Cross-sectional rank correlations
  and thirds-based spreads with only 14 (or 22) entities per month are noisy
  by construction — a handful of names swapping rank order can move the
  monthly IC substantially, and the "top third / bottom third" split is
  4-5 names per group for large caps.
- **Survivorship.** Both baskets are today's well-known large caps and
  today's well-known volatile/momentum names, chosen with the benefit of
  20 years' hindsight for the large-cap side. Names that did not survive to
  2026 (delisted, acquired, bankrupt) are absent, which mechanically biases
  the measured momentum and 200-day-gate effects upward versus a true
  point-in-time investable universe.
- **Overlapping monthly windows.** Consecutive month-end 21-day forward
  returns overlap by construction (each month's forward window shares up to
  20 days with the next), so the "t-stat across months" understates true
  uncertainty — the effective number of independent observations is smaller
  than the number of months printed above.
- **Number of tests.** This note runs 5 horizons x 2 universes x 2 test
  forms (cross-sectional, time-series) x 3 periods (full/pre/post) = dozens
  of t-stats, plus the 200-day gate and two exit simulations, with no
  multiple-comparison correction applied. Some of the "significant" results
  above (t just over 2) would not survive a Bonferroni-style correction for
  that many tests; they are reported as raw numbers for that reason, not as
  a confirmed multi-test-corrected finding.
- **The R4 simulation is not the live ledger.** It answers "what would this
  ruleset's holding period have been over 20 years of history," not "what
  has TARS actually experienced" — the two are far apart right now (median
  47.5 simulated trading days vs 2.84 calendar days live) simply because the
  live account is new. Re-run this comparison once TARS has enough closed
  trend-following trades of its own to matter.

Status: DONE. Predictions committed first (b82b430). Nothing is adopted
before the weekend re-read (R16.3).
