# Chart Indicators on Volatile Growth Stocks

One-line: every indicator test so far used blue chips. Nolan trades SOFI-type
names. Do the same indicators behave differently on volatile growth stocks?

Last Updated: 2026-09-24
Status: DONE. Predictions committed first (52bed82).
Audience: Nolan, TARS sessions

## Overview

Same indicators and settings as 2026-09-24_INDICATORS_PRICE.md (MACD 12/26/9,
RSI 14, Bollinger 20/2, SMA 50, SMA 200, EMA 9), on higher-volatility growth
names pulled read-only from Robinhood. Many of these listed recently, so
histories are short and uneven. Survivorship is WORSE here than in the
large-cap set: names that crashed and delisted aren't in the data. That
flatters buy-and-hold, and it flatters "buy the dip" signals most of all.
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read.

## Predictions (written before the test)

P4 TREND SYSTEMS (SMA 50/200 long/flat): on volatile names they cut the max
   drawdown by much more than on blue chips (those names fall 70-90%), and
   come CLOSER to buy-and-hold on Sharpe than on blue chips. Some names beat
   buy-and-hold on Sharpe. Still not most of them.
P5 OSCILLATOR SYSTEMS (RSI 30/70, Bollinger lower-band buy): still lose to
   buy-and-hold, and fail worse than on blue chips, because "oversold" keeps
   getting more oversold on names in a real downtrend.
P6 EVENTS: no event signal survives multiple testing in both halves.

What would prove me wrong: any indicator system beating buy-and-hold on
Sharpe in a MAJORITY of the volatile names, in both halves of each name's
own history.

## Data pulled

Pulled fresh via Robinhood `get_equity_historicals` (daily bars, split-adjusted,
regular hours, 2006-01-01 through today), chunked into 2006-2016 / 2016-today
date ranges and batches of <=10 symbols per call (server caps ~5000 bars/call).
Interpolated bars (`interpolated: true`, i.e. synthesized gap-fill with no real
trade behind them) were dropped before storage, never counted as real data.
Saved to `paper/history/daily_ohlcv_volatile.json`
(schema `{SYMBOL: {"YYYY-MM-DD": [open, high, low, close, volume]}}`, 3.0MB).

| Symbol | First date | Bar count |
|---|---|---:|
| SOFI | 2020-11-30 | 1460 |
| PLTR | 2020-09-30 | 1502 |
| HOOD | 2021-07-29 | 1294 |
| COIN | 2021-04-14 | 1368 |
| RIVN | 2021-11-10 | 1221 |
| AFRM | 2021-01-13 | 1430 |
| UPST | 2020-12-16 | 1448 |
| SNAP | 2017-03-02 | 2404 |
| ROKU | 2017-09-28 | 2258 |
| SHOP | 2015-05-21 | 2852 |
| TSLA | 2010-06-29 | 4083 |
| AMD  | 2006-01-03 | 5212 |
| NVDA | 2006-01-03 | 5212 |
| MU   | 2006-01-03 | 5212 |
| ENPH | 2012-03-30 | 3641 |
| NFLX | 2006-01-03 | 5212 |
| UBER | 2019-05-10 | 1853 |
| DKNG | 2019-07-25 | 1801 |
| CRWD | 2019-06-12 | 1831 |
| NET  | 2019-09-13 | 1766 |
| MARA | 2013-07-22 | 3314 |
| RIOT | 2006-01-03 | 5212 |

No symbol failed to fetch. **Excluded from the tests (< 750 bars, ~3 years of
history): none** -- all 22 names clear the bar, though several (RIVN, HOOD,
COIN, AFRM, UPST, SOFI, PLTR) only barely (1200-1500 bars, ~5-6 years),
which matters for the "own-history halves" system test below (see Limits).

## Results

Test script: `paper/research_scripts/indicators_volatile.py`. Universe: the
22 names above, each tested over its own full history (2006-09-18 through
2026-09-23/24 for the four names that go back to 2006; much shorter for the
2020-21 IPOs). Large-cap comparison universe for the volatility check is the
same 14 names + SPY from `2026-09-24_INDICATORS_PRICE.md`
(`paper/history/daily_stocks.json`).

**Volatility check:** median annualized volatility across the 22 volatile
names is **70.6%**, vs **31.2%** for the 14 large caps (SPY alone: 19.3%).
That's 2.3x. Every single volatile name has higher annualized vol than every
large cap except NVDA (48.9% large-cap vs the volatile set's low of 48.9%
for NVDA itself, tested fresh here too -- it's the same stock, expected to
match). Confirms the universe really is more volatile, as the note's
one-line premise assumed.

**Test 1 (event study, pooled across 22 names, split at 2021-01-01):** 18
signal types x 3 horizons = 54 tests. Bonferroni alpha=0.05/54 -> critical
|t| ~= 3.31. **One survivor**, unlike the blue-chip test (zero survivors):
`macd_cross_below_zero` at 5 days, t=-3.83, diff=-1.077pp, same sign in both
halves (pre -0.819pp, post -1.276pp, n=975). Interpretation: when MACD
crosses below zero on one of these volatile names, the next 5 trading days
average about 1.1pp worse than the pool's baseline 5-day return -- a real,
Bonferroni-surviving, both-halves-consistent bearish continuation signal.
No other signal/horizon cell clears the bar (`bb_close_above_upper` at 21d
is the runner-up, t=2.40, and `rsi_cross_back_above_30` at 21d is
t=-2.75 with a NEGATIVE sign_adj_pp -- i.e. it moves opposite the
textbook-bullish reading -- but neither reaches Bonferroni).

**Test 2 (trading systems, per name, own-history halves), headline table:**

| System | Beats B&H on Sharpe: full | first half | second half | Median max-drawdown cut vs B&H |
|---|---:|---:|---:|---:|
| MACD | 6/22 (27%) | 8/22 (36%) | 4/22 (18%) | 9.8pp (full) |
| SMA(50) | 7/22 (32%) | 14/22 (64%) | 2/22 (9%) | 19.5pp (full) |
| SMA(200) | 9/22 (41%) | 16/22 (73%) | 4/22 (18%) | 24.4pp (full) |
| EMA(9) | 2/22 (9%) | 15/22 (68%) | 2/22 (9%) | 14.7pp (full) |
| RSI(30/70) | 4/22 (18%) | 7/22 (32%) | 4/22 (18%) | 8.6pp (full) |
| Bollinger | 4/22 (18%) | 6/22 (27%) | 4/22 (18%) | 20.1pp (full) |

For comparison, the blue-chip (14-name) full-sample beat-rates from
`2026-09-24_INDICATORS_PRICE.md` were: MACD 2/14 (14%), SMA50 3/14 (21%),
SMA200 5/14 (36%), EMA9 2/14 (14%), RSI 3/14 (21%), Bollinger 2/14 (14%).
Blue-chip average (mean, not median) max-drawdown cuts (full sample):
MACD 11.9pp, SMA50 14.4pp, SMA200 20.1pp, EMA9 0.05pp (essentially none),
RSI 6.1pp, Bollinger 16.4pp.

So on the volatile universe: (a) drawdown cuts are bigger for every system
except MACD (roughly flat) -- most strikingly EMA9, which cut almost nothing
on blue chips (0.05pp) but cuts a median 14.7pp here; (b) full-sample
Sharpe beat-rates are somewhat higher for the trend systems (SMA50 32% vs
21%, SMA200 41% vs 36%) but still a minority in every case; (c) the
oscillators (RSI, Bollinger) do NOT clearly fail worse here -- RSI is about
the same (18% vs 21%) and Bollinger is actually a bit better (18% vs 14%).

The **first half vs second half split is the most important pattern in the
whole table**, and it is not a story about the indicators -- it is a story
about *when* these names' histories start. Most of the 22 names' full
histories run roughly 2019/2020/2021 through 2026, so each name's own
midpoint typically falls close to the 2021-2022 growth-stock crash. "First
half" for most names is dominated by that crash (buy-and-hold got destroyed:
e.g. PLTR bh first-half CAGR -7.8%, HOOD -35.8%, RIVN -66.3%, NET +42.6% only
because NET IPO'd right before the crash and its "first half" barely
overlaps it); trend/momentum systems that go flat in a downtrend look great
against that specific buy-and-hold line. "Second half" for most names is
dominated by the 2023-2025 recovery/AI-and-rate-cut rally (buy-and-hold wins
big: PLTR +139%, HOOD +130%, NET +69%, CRWD +89% CAGR) and systems that
were flat or late back in lag badly. This is a single historical episode
appearing in slightly different date windows for 22 different names, not 22
independent replications -- see Limits.

Full raw output is long (~600 lines: volatility table, 54-row event table,
signal counts, Bonferroni/survivors, then 6 systems x 22 names x 3 periods).
It is preserved in full at `paper/research_scripts/indicators_volatile.py`'s
output; representative excerpt:

```
TEST 0: ANNUALIZED VOLATILITY -- volatile-name universe vs large-cap universe
sym    first_date   n_bars     ann_vol%
SOFI   2020-11-30   1460          71.09
UPST   2020-12-16   1448         111.66
MARA   2013-07-22   3314         129.96
RIOT   2006-01-03   5212         103.14
...
Median annualized vol -- volatile-name universe (22 names): 70.59%
Median annualized vol -- large-cap universe (14 names, SPY excluded from median): 31.22%
SPY annualized vol (separate): 19.32%

SURVIVORS: full-sample |t| exceeds the primary Bonferroni threshold (3.312) AND both half-sample diffs share the predicted sign
  SURVIVOR: macd_cross_below_zero h=5 t=-3.83 diff_pp=-1.077 pre_pp=-0.819 post_pp=-1.276

HEADLINE SUMMARY: names (of 22) beating buy-and-hold on Sharpe, by system and period; median max-drawdown cut vs B&H
  macd       full=6/22 (mdd_cut=9.8pp)  first=8/22 (mdd_cut=12.0pp)  second=4/22 (mdd_cut=9.9pp)
  sma50      full=7/22 (mdd_cut=19.5pp)  first=14/22 (mdd_cut=20.7pp)  second=2/22 (mdd_cut=8.6pp)
  sma200     full=9/22 (mdd_cut=24.4pp)  first=16/22 (mdd_cut=31.3pp)  second=4/22 (mdd_cut=8.9pp)
  ema9       full=2/22 (mdd_cut=14.7pp)  first=15/22 (mdd_cut=20.8pp)  second=2/22 (mdd_cut=6.2pp)
  rsi        full=4/22 (mdd_cut=8.6pp)  first=7/22 (mdd_cut=10.4pp)  second=4/22 (mdd_cut=13.9pp)
  bollinger  full=4/22 (mdd_cut=20.1pp)  first=6/22 (mdd_cut=20.0pp)  second=4/22 (mdd_cut=19.5pp)
```

**Robustness check on the macd_cross_below_zero survivor (coordinator
follow-up, before accepting it).** The naive pooled test above treats every
signal instance as an independent observation, but instances cluster on the
same calendar dates (22 names often cross their own MACD zero line within
days of each other, especially in a shared selloff), which overstates the
effective sample size and therefore the t-stat. Four checks were added to
`indicators_volatile.py` and run on the flagged signal plus its natural
control (`macd_cross_above_zero`, same indicator, opposite sign, no prior
reason to expect it survives), at all three horizons. Full raw output:

```
ROBUSTNESS CHECK ON THE MACD-ZERO-CROSS SURVIVOR (coordinator follow-up)
Episode gap threshold: 10 trading days. Excluded year for check (3): 2022.
Sector-neutral benchmark (check 4): equal-weight avg fwd return across the
22-name pool, same start date, same horizon.

  -- macd_cross_below_zero h=5 --
    n_instances=975  n_distinct_dates=798  n_episodes(gap<10d)=169
    (1) naive pooled (uncorrected, matches primary table):      diff_pp=-1.077  t=-3.83
    (1) date-clustered (one obs/date, n=798):              diff_pp=-0.917  t=-3.16
    (3) 2022 removed, naive pooled (n=891, n_dates=736): diff_pp=-1.202  t=-4.11
    (3) 2022 removed, date-clustered:                            diff_pp=-1.051  t=-3.53
    (4) sector-neutral (vs 22-name equal-weight bench), naive (n=975): diff_pp=-0.669  t=-2.97
    (4) sector-neutral, date-clustered (n_dates=798):    diff_pp=-0.607  t=-2.61

  -- macd_cross_below_zero h=10 --
    n_instances=972  n_distinct_dates=797  n_episodes(gap<10d)=169
    (1) naive pooled:                                            diff_pp=-1.300  t=-3.30
    (1) date-clustered (n=797):                                  diff_pp=-1.251  t=-3.12
    (3) 2022 removed, naive pooled (n=888, n_dates=735):          diff_pp=-1.426  t=-3.53
    (3) 2022 removed, date-clustered:                             diff_pp=-1.408  t=-3.45
    (4) sector-neutral, naive (n=972):                            diff_pp=-0.805  t=-2.47
    (4) sector-neutral, date-clustered (n_dates=797):             diff_pp=-0.906  t=-2.69

  -- macd_cross_below_zero h=21 --
    n_instances=967  n_distinct_dates=794  n_episodes(gap<10d)=169
    (1) naive pooled:                                            diff_pp=-0.483  t=-0.68
    (1) date-clustered (n=794):                                  diff_pp=-0.657  t=-0.89
    (3) 2022 removed, naive pooled (n=883, n_dates=732):          diff_pp=-0.199  t=-0.27
    (3) 2022 removed, date-clustered:                             diff_pp=-0.586  t=-0.76
    (4) sector-neutral, naive (n=967):                            diff_pp=-0.183  t=-0.32
    (4) sector-neutral, date-clustered (n_dates=794):             diff_pp=-0.275  t=-0.47

  -- macd_cross_above_zero h=5 (control) --
    n_instances=977  n_distinct_dates=801  n_episodes(gap<10d)=175
    (1) naive pooled:                                            diff_pp=-0.441  t=-1.41
    (1) date-clustered (n=801):                                  diff_pp=-0.253  t=-0.74
    (3) 2022 removed, naive pooled (n=900, n_dates=752):          diff_pp=-0.415  t=-1.29
    (3) 2022 removed, date-clustered:                             diff_pp=-0.340  t=-0.97
    (4) sector-neutral, naive (n=977):                            diff_pp=0.093   t=0.35
    (4) sector-neutral, date-clustered (n_dates=801):             diff_pp=0.130   t=0.44

  -- macd_cross_above_zero h=10 (control) --
    n_instances=976  n_distinct_dates=800  n_episodes(gap<10d)=175
    (1) naive pooled:                                            diff_pp=-0.036  t=-0.08
    (1) date-clustered (n=800):                                  diff_pp=0.055   t=0.11
    (3) 2022 removed, naive pooled (n=899, n_dates=751):          diff_pp=0.016   t=0.03
    (3) 2022 removed, date-clustered:                             diff_pp=-0.028  t=-0.05
    (4) sector-neutral, naive (n=976):                            diff_pp=0.228   t=0.60
    (4) sector-neutral, date-clustered (n_dates=800):             diff_pp=0.248   t=0.59

  -- macd_cross_above_zero h=21 (control) --
    n_instances=970  n_distinct_dates=795  n_episodes(gap<10d)=175
    (1) naive pooled:                                            diff_pp=1.191   t=1.64
    (1) date-clustered (n=795):                                  diff_pp=1.119   t=1.46
    (3) 2022 removed, naive pooled (n=893, n_dates=746):          diff_pp=1.447   t=1.92
    (3) 2022 removed, date-clustered:                             diff_pp=1.100   t=1.40
    (4) sector-neutral, naive (n=970):                            diff_pp=0.551   t=0.94
    (4) sector-neutral, date-clustered (n_dates=795):             diff_pp=0.604   t=0.98
```

Reading it: (1) clustering is real but modest at h=5/10 -- 975-972 raw instances
collapse to only 797-798 distinct dates (169 distinct episodes when dates
within 10 trading days are merged), and de-clustering pulls the h=5 t from
-3.83 to -3.16 and the h=10 t from -3.30 to -3.12 -- both now BELOW the 3.31
Bonferroni bar. (3) Removing all of 2022 does NOT kill the signal -- it gets
slightly STRONGER (h=5 clustered t goes to -3.53, h=10 to -3.45, both still
above 3.31), so this is not simply "the 2022 selloff, pooled." (4) The
sector-neutral cut is the most damaging: benchmarking each name's forward
return against the equal-weight 22-name pool's forward return over the same
window (netting out whatever the pool did in general) drops h=5 to t=-2.97
naive / -2.61 clustered and h=10 to t=-2.47 naive / -2.69 clustered -- both
comfortably below 3.31 either way. The control signal (`macd_cross_above_zero`)
never approaches significance under any of the four checks, at any horizon,
which is the expected null result and a basic sanity check that the pipeline
isn't finding effects everywhere.

Net: the effect is directionally consistent (negative, i.e. bearish, at
h=5/10 in every one of the eight naive/clustered/2022-excluded/sector-neutral
combinations) and is not simply a 2022 artifact, but it does NOT clearly
survive once BOTH date-clustering and sector-neutrality are applied together
-- the two most conservative variants (sector-neutral naive and sector-neutral
clustered) both land at |t| < 3.0, below the pre-registered 3.31 Bonferroni
bar. Some of the original "survivor" apparently reflects several of the 22
names crossing zero within days of each other during a common pool-wide move,
which the naive pooled test double-counts as if it were many independent
observations.

## Verdict

**P4 (trend systems SMA50/SMA200) -- PARTLY CONFIRMED.** Drawdown cuts ARE
bigger on these names than on blue chips for SMA50 (median 19.5pp vs
blue-chip mean 14.4pp) and SMA200 (24.4pp vs 20.1pp), as predicted -- these
names really do fall 60-99% in the bad stretches (e.g. RIOT -99.9%, MARA
-96.6%, UPST -93.9% peak-to-trough buy-and-hold) and a flat-in-downtrend
system avoids a lot of that. Full-sample Sharpe beat-rates are also somewhat
higher than blue chips (SMA50 32% vs 21%, SMA200 41% vs 36%) -- directionally
"comes closer," though "closer" here is doing a lot of work: 41% of 22 is
still a minority, exactly as predicted ("still not most of them"). The
first/second-half split, however, is NOT the clean "trend systems help more
in a real downtrend" story it looks like at first glance -- it is one
specific 2021-2022 crash landing in the "first half" bucket for most names
by construction (see Limits), so the P4 confirmation should be read mostly
off the full-sample column, which supports it, weakly.

**P5 (oscillator systems RSI/Bollinger) -- PARTLY REFUTED.** The "still lose
to buy-and-hold" half holds (RSI 18%, Bollinger 18% full-sample beat-rate,
both minorities). The "fail WORSE than on blue chips" half does NOT hold:
RSI's beat-rate (18%) is almost identical to blue chips (21%), and
Bollinger's (18%) is actually better than blue chips (14%). Bollinger's
median drawdown cut here (20.1pp) is bigger than blue chips' mean (16.4pp),
the opposite of "oversold keeps getting more oversold" making things worse.
The mechanism in the prediction (real downtrends punish dip-buying more) may
still be true in some of these names' worst individual drawdowns, but it
does not show up as a universe-wide "worse than blue chips" effect in either
the beat-rate or the drawdown numbers.

**P6 (events) -- MOSTLY CONFIRMED, walked back from the earlier draft of
this note.** The naive pooled test initially flagged one survivor
(`macd_cross_below_zero` at 5 days, t=-3.83, both-halves-consistent), which
an earlier version of this section called a refutation of P6. On the
coordinator's follow-up, that survivor does NOT hold up once the pooling
is corrected for two things the naive test ignores: (a) signals cluster on
the same dates (975 instances at h=5 collapse to 798 distinct dates, only
169 distinct episodes), and (b) part of any pooled-vs-unconditional-baseline
effect can just be "the whole 22-name pool moved together," not something
specific to this signal. Date-clustering alone drops the h=5/h=10 t-stats
to -3.16/-3.12 (below the 3.31 bar); benchmarking sector-neutrally (each
name's forward return vs. the equal-weight pool's forward return over the
same window, instead of vs. an unconditional historical baseline) drops them
further to -2.97/-2.47 naive and -2.61/-2.69 clustered -- all four below
3.31. Excluding 2022 entirely does NOT kill it (if anything it strengthens
slightly, to -3.53/-3.45 clustered), so this specific signal is not simply an
artifact of the 2022 growth-stock crash, but it is not robust to the more
important correction (date-clustering + sector-neutrality together). Revised
conclusion: **no event signal in this universe survives a Bonferroni-plus-
robustness bar in both halves** -- the same outcome P6 originally predicted.
The MACD-below-zero result is downgraded from "survivor" to "a directionally
consistent but not clearly independent-of-clustering signal, worth a fresh
replication on a different universe/date range before being taken
seriously, not evidence P6 is refuted." The control signal
(`macd_cross_above_zero`) never came close to significance under any of the
four checks, which is the expected null and increases confidence that the
robustness pipeline itself isn't just finding effects everywhere.

## What this means for trading names like SOFI

- These names really are roughly 2-2.5x as volatile as the large caps
  (70% vs 31% annualized), so any position sizing, stop distance, or options
  premium expectation carried over from blue-chip intuition will be wrong by
  that factor -- widen stops and cut size, don't just apply the same %.
- A 200-day (or 50-day) moving-average filter does meaningfully cut the size
  of the worst drawdowns on these names (median ~20-24 percentage points less
  drawdown than buy-and-hold) -- if the goal is "survive the crash," that is
  the one piece of this test with the most support.
- That same filter still loses to buy-and-hold on risk-adjusted return
  (Sharpe) in roughly 6 of 10 names, full-sample -- it is a drawdown-control
  tool, not a return-boosting one, on this universe just as it was on blue
  chips.
- "Buy the dip" (RSI < 30, or below the Bollinger lower band) is not
  obviously worse here than it is on blue chips -- the R15/R14 regime logic
  (calm vs stressed VIX) from the blue-chip note is a more promising lever to
  test on these names specifically than "avoid oversold buying on volatile
  names," which this test does not support as a blanket rule.
- The one signal that initially looked like a survivor (MACD crossing below
  its zero line, ~1pp of extra 5-day downside) did NOT hold up under a
  closer look -- once corrected for names clustering their signals on the
  same dates and for whether the whole pool moved together, it drops below
  the significance bar. Directionally it's still negative every way it was
  sliced, so it's not nothing, but it should be treated as "maybe, needs a
  fresh replication," not "a bearish tell you can act on."
- The biggest pattern in the whole test (trend systems looking great in
  "first half," terrible in "second half") is mostly an artifact of when
  these particular 22 stocks happen to have IPO'd relative to the 2021-2022
  crash and the recovery that followed it -- it is a lesson about this
  specific market cycle, not a durable property of trend-following on
  volatile names. Don't over-read it as "trend-following works great early
  and fails late."

## Limits

- **Heavy survivorship, worse than the blue-chip test.** This universe is
  22 names that are still trading and still liquid enough to be commonly
  discussed today. Names in the same 2020-2021 SPAC/IPO cohort that went to
  zero or got taken private (there were many) are not in this data at all --
  they cannot be, Robinhood only serves history for symbols that still
  trade. That mechanically flatters every buy-and-hold column and, more
  subtly, flatters every "buy the dip" oscillator column too, since a name
  that never recovered from its dip is excluded by construction.
- **Short and uneven histories.** Seven of the 22 names (SOFI, PLTR, HOOD,
  COIN, RIVN, AFRM, UPST) have under 1500 bars (~6 years or less), and the
  own-history-midpoint split for those names puts the entire 2021-2022 crash
  and 2023+ recovery into two very short, very lopsided halves -- these are
  not independent tests of "does trend-following work" so much as one
  specific 18-24 month drawdown-and-recovery episode, sliced in half 22
  different ways depending on IPO date. Treat the first/second-half columns
  with much more caution than the full-sample column.
- **Mostly one bull market, one crash, one recovery.** Even the four names
  with full 2006-2026 histories (AMD, NVDA, MU, RIOT) still spend most of
  their explanatory weight on the same 2020-2022-2023 period as the short-
  history names, because that period is where the volatility (and therefore
  the variance in the Sharpe/drawdown numbers) is concentrated. This is not
  22 independent market cycles.
- **Number of tests.** Same primary family size as the blue-chip note (18
  signals x 3 horizons = 54, Bonferroni threshold ~3.31), run once on this
  universe. One survivor at ~1.1pp effect size, out of 54 tests, is worth
  taking seriously but not worth trading alone -- it wants an independent
  replication (a different universe or a later date range) before being
  treated as durable, per R16.

Nothing here is adopted into any live or paper strategy before the weekend
re-read (R16.3). This is a single run against a single pre-registered
prediction file; it has not been checked for a second time with fresh eyes.
