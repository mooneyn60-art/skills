# Earnings Moves: How Our Holdings React, and What It Means for the SOFI Call

One-line: company news drives most of our holdings' moves, and earnings are
the biggest scheduled company news. How big are our names' earnings moves,
do options overprice them, and what happens to the SOFI call on Oct 27?

Last Updated: 2026-09-25
Status: DONE. Predictions committed first (b82b430).
Audience: Nolan, TARS sessions

## Overview

Holdings: NVDA SOFI INTC TGT ABBV EXEL NWG CVE, plus the SOFI Dec 18 $19
call (R17 slot #1). Past report dates via Robinhood get_earnings_results,
prices from paper/history and read-only historicals, and the current
option chain for implied moves. R16 trigger (c) is ON in the writing
session. Nothing adopted before the weekend re-read.

## Predictions (written before the test)

P1 The average absolute earnings-reaction move for our holdings is 1.5 to 3x
   their normal daily move. SOFI's is the largest of the eight, around 8-10%.
P2 SOFI's current implied earnings move (nearest post-earnings expiry
   straddle) is LARGER than its median realized earnings move. Options
   usually overprice earnings (the earnings volatility premium).
P3 If SOFI is flat through earnings, the Dec $19 call loses about 10-20% of
   its value from the post-earnings IV drop.

## Results

Script: `paper/research_scripts/earnings_moves.py` (extended 2026-09-25 with
PART 3B for the now-two-leg position; PART 1/2 and the original single-leg
PART 3 are unchanged from the 2026-09-24 draft). Data: `daily_ohlcv.json`,
`daily_ohlcv_holdings.json`, `earnings_reports.json`,
`sofi_options_2026-09-24.json`, and a new refresh,
`sofi_live_quotes_2026-09-25.json` (live SOFI stock + both call quotes,
2026-09-25 14:29 UTC, via `get_equity_quotes`/`get_option_quotes`,
read-only, no orders placed). am/pm timing check: verified by hand for
SOFI (all 7 reports "am" -> prior-close-to-report-day-close, e.g.
2026-07-28 close 8.90 -> 2026-07-29 close, correct) and for NVDA/INTC/EXEL
(all "pm" -> report-day-close-to-next-day-close). TGT/ABBV/CVE/NWG are all
"am" too and check out the same way. No am/pm mismatches found.

**Table 1 -- earnings move vs normal day (n=7 reports each, 2025-01 to
2026-08)**

| Sym | median\|move\| | mean\|move\| | normal day | ratio |
|---|---|---|---|---|
| EXEL | 7.94% | 8.83% | 1.03% | 7.71x |
| INTC | 7.89% | 9.57% | 1.74% | 4.52x |
| ABBV | 3.15% | 3.13% | 0.76% | 4.13x |
| TGT | 4.28% | 4.60% | 1.07% | 4.00x |
| SOFI | 6.57% | 7.66% | 2.24% | 2.94x |
| CVE | 3.96% | 3.79% | 1.39% | 2.85x |
| NVDA | 3.25% | 4.52% | 1.55% | 2.09x |
| NWG | 2.34% | 3.02% | 1.18% | 1.99x |

Median ratio across the 8 names: **3.47x** (mean 3.78x).

**Table 2 -- SOFI implied vs realized earnings move**

| | value |
|---|---|
| ATM straddle, 10-23 expiry (pre-report, 29d) | 10.18% of spot |
| ATM straddle, 10-30 expiry (spans report, 36d) | 12.83% of spot |
| Baseline (10-23 straddle scaled by sqrt(time)) | 11.35% of spot |
| **Implied earnings-only move (quadrature)** | **6.00%** |
| Implied earnings-only move (linear, lower bound) | 1.49% |
| Realized median \|earnings move\| (n=7) | 6.57% |
| Realized mean \|earnings move\| (n=7) | 7.66% |

**Table 3 -- SOFI position, day after the assumed 2026-10-27 (am) report**
(spot grid off the live 2026-09-25 quote of $16.685; valuation 2026-10-28;
8-point IV crush applied to both calls)

| Move | Spot | $19C px (vs cost 0.82) | $19C stop? | $18C px (vs cost 1.22) | $18C stop? | 10 shares | Shares stop? |
|---|---|---|---|---|---|---|---|
| -15% | 14.18 | 0.05 (-94%) | GAP-THROUGH | 0.09 (-92%) | GAP-THROUGH | $141.82 | HIT, ~14.18 |
| -8% | 15.35 | 0.15 (-82%) | GAP-THROUGH | 0.26 (-79%) | GAP-THROUGH | $153.50 | HIT, ~15.35 |
| 0% | 16.68 | 0.39 (-52%) | GAP-THROUGH | 0.63 (-48%) | GAP-THROUGH | $166.85 | no |
| +8% | 18.02 | 0.84 (+3%) | no | 1.24 (+2%) | no | $180.20 | no |
| +15% | 19.19 | 1.42 (+73%) | no | 1.97 (+62%) | no | $191.88 | no |

"GAP-THROUGH" = the modeled price opens below the stop-LIMIT (0.60 for the
$19C, 0.90 for the $18C), so the resting sell-limit order could not have
filled there -- it would sit unfilled, exposed, until price recovers to the
limit or Nolan/TARS cancels and re-routes it. "HIT" for the shares = the
open gaps below the 15.75 trigger; that stop has no separate limit on
record so it is treated as a stop-market, filling near the gap price
(with the usual slippage caveat) rather than going unfilled.

Extra finding not asked for directly but load-bearing for the verdict:
holding SOFI's price and IV exactly at today's live level (no earnings
move assumed at all), pure theta decay alone pushes the $18C through its
0.98 trigger around **2026-10-16** and the $19C through its 0.66 trigger
around **2026-10-20** -- both **before** the 2026-10-27 report. IV-crush
only (spot unchanged, today's T, IV -8pts): $19C -25.7%, $18C -20.9%.
Time-decay only (34 days, IV unchanged): $19C -38.8%, $18C -31.7%.

Full script output:

```
==============================================================================
PART 1 -- EARNINGS REACTION MOVES
==============================================================================

NVDA  n=7  median|move|=3.25%  mean|move|=4.52%  normal_day_median|move|=1.55%  ratio=2.09x
    2025-02-26 (pm) 2025-02-26->2025-02-27 move=-8.48%  surprise=+0.050 dir_match=False
    2025-05-28 (pm) 2025-05-28->2025-05-29 move=+3.25%  surprise=+0.210 dir_match=True
    2025-08-27 (pm) 2025-08-27->2025-08-28 move=-0.79%  surprise=+0.060 dir_match=False
    2025-11-19 (pm) 2025-11-19->2025-11-20 move=-3.15%  surprise=+0.080 dir_match=False
    2026-02-25 (pm) 2026-02-25->2026-02-26 move=-5.46%  surprise=+0.120 dir_match=False
    2026-05-20 (pm) 2026-05-20->2026-05-21 move=-1.77%  surprise=+0.110 dir_match=False
    2026-08-26 (pm) 2026-08-26->2026-08-27 move=+8.74%  surprise=+0.130 dir_match=True

SOFI  n=7  median|move|=6.57%  mean|move|=7.66%  normal_day_median|move|=2.24%  ratio=2.94x
    2025-01-27 (am) 2025-01-24->2025-01-27 move=-10.27%  surprise=+0.010 dir_match=False
    2025-04-29 (am) 2025-04-28->2025-04-29 move=+0.53%  surprise=+0.020 dir_match=True
    2025-07-29 (am) 2025-07-28->2025-07-29 move=+6.57%  surprise=+0.020 dir_match=True
    2025-10-28 (am) 2025-10-27->2025-10-28 move=+5.53%  surprise=+0.030 dir_match=True
    2026-01-30 (am) 2026-01-29->2026-01-30 move=-6.36%  surprise=+0.010 dir_match=False
    2026-04-29 (am) 2026-04-28->2026-04-29 move=-15.44%  surprise=+0.000 
    2026-07-29 (am) 2026-07-28->2026-07-29 move=-8.90%  surprise=+0.010 dir_match=False

INTC  n=7  median|move|=7.89%  mean|move|=9.57%  normal_day_median|move|=1.74%  ratio=4.52x
    2025-01-30 (pm) 2025-01-30->2025-01-31 move=-2.90%  surprise=+0.010 dir_match=False
    2025-04-24 (pm) 2025-04-24->2025-04-25 move=-6.70%  surprise=+0.120 dir_match=False
    2025-07-24 (pm) 2025-07-24->2025-07-25 move=-8.53%  surprise=-0.050 dir_match=True
    2025-10-23 (pm) 2025-10-23->2025-10-24 move=+0.31%  surprise=+0.270 dir_match=True
    2026-01-22 (pm) 2026-01-22->2026-01-23 move=-17.03%  surprise=+0.110 dir_match=False
    2026-04-23 (pm) 2026-04-23->2026-04-24 move=+23.60%  surprise=+0.300 dir_match=True
    2026-07-23 (pm) 2026-07-23->2026-07-24 move=-7.89%  surprise=+0.230 dir_match=False

TGT  n=7  median|move|=4.28%  mean|move|=4.60%  normal_day_median|move|=1.07%  ratio=4.00x
    2025-03-04 (am) 2025-03-03->2025-03-04 move=-3.00%  surprise=+0.150 dir_match=False
    2025-05-21 (am) 2025-05-20->2025-05-21 move=-5.21%  surprise=-0.350 dir_match=True
    2025-08-20 (am) 2025-08-19->2025-08-20 move=-6.33%  surprise=+0.000 
    2025-11-19 (am) 2025-11-18->2025-11-19 move=-2.77%  surprise=+0.050 dir_match=False
    2026-03-03 (am) 2026-03-02->2026-03-03 move=+6.74%  surprise=+0.280 dir_match=True
    2026-05-20 (am) 2026-05-19->2026-05-20 move=-3.86%  surprise=+0.360 dir_match=False
    2026-08-19 (am) 2026-08-18->2026-08-19 move=+4.28%  surprise=+0.210 dir_match=True

ABBV  n=7  median|move|=3.15%  mean|move|=3.13%  normal_day_median|move|=0.76%  ratio=4.13x
    2025-01-31 (am) 2025-01-30->2025-01-31 move=+4.70%  surprise=-0.100 dir_match=False
    2025-04-25 (am) 2025-04-24->2025-04-25 move=+3.15%  surprise=+0.080 dir_match=True
    2025-07-31 (am) 2025-07-30->2025-07-31 move=-0.15%  surprise=+0.070 dir_match=False
    2025-10-31 (am) 2025-10-30->2025-10-31 move=-4.45%  surprise=+0.080 dir_match=False
    2026-02-04 (am) 2026-02-03->2026-02-04 move=-3.79%  surprise=+0.050 dir_match=False
    2026-04-29 (am) 2026-04-28->2026-04-29 move=+3.14%  surprise=-0.010 dir_match=False
    2026-07-31 (am) 2026-07-30->2026-07-31 move=-2.51%  surprise=-0.120 dir_match=True

EXEL  n=7  median|move|=7.94%  mean|move|=8.83%  normal_day_median|move|=1.03%  ratio=7.71x
    2025-02-11 (pm) 2025-02-11->2025-02-12 move=-0.03%  surprise=+0.060 dir_match=False
    2025-05-13 (pm) 2025-05-13->2025-05-14 move=+20.84%  surprise=+0.180 dir_match=True
    2025-07-28 (pm) 2025-07-28->2025-07-29 move=-16.78%  surprise=+0.140 dir_match=False
    2025-11-04 (pm) 2025-11-04->2025-11-05 move=+6.52%  surprise=+0.150 dir_match=True
    2026-02-10 (pm) 2026-02-10->2026-02-11 move=-0.09%  surprise=+0.180 dir_match=False
    2026-05-05 (pm) 2026-05-05->2026-05-06 move=+9.64%  surprise=+0.130 dir_match=True
    2026-08-05 (pm) 2026-08-05->2026-08-06 move=-7.94%  surprise=+0.070 dir_match=False

NWG  n=7  median|move|=2.34%  mean|move|=3.02%  normal_day_median|move|=1.18%  ratio=1.99x
    2025-02-14 (am) 2025-02-13->2025-02-14 move=-2.34%   
    2025-05-02 (am) 2025-05-01->2025-05-02 move=+1.80%   
    2025-07-25 (am) 2025-07-24->2025-07-25 move=+4.20%   
    2025-10-24 (am) 2025-10-23->2025-10-24 move=+5.65%   
    2026-02-13 (am) 2026-02-12->2026-02-13 move=-1.59%  surprise=+0.103 dir_match=False
    2026-05-01 (am) 2026-04-30->2026-05-01 move=-3.33%  surprise=+0.040 dir_match=False
    2026-07-31 (am) 2026-07-30->2026-07-31 move=+2.21%  surprise=+0.069 dir_match=True

CVE  n=7  median|move|=3.96%  mean|move|=3.79%  normal_day_median|move|=1.39%  ratio=2.85x
    2025-02-20 (am) 2025-02-19->2025-02-20 move=-2.18%  surprise=-0.130 dir_match=True
    2025-05-08 (am) 2025-05-07->2025-05-08 move=+8.50%  surprise=+0.040 dir_match=True
    2025-07-31 (am) 2025-07-30->2025-07-31 move=+1.06%  surprise=+0.130 dir_match=True
    2025-10-31 (am) 2025-10-30->2025-10-31 move=+1.01%  surprise=+0.120 dir_match=True
    2026-02-19 (am) 2026-02-18->2026-02-19 move=+3.96%  surprise=+0.080 dir_match=True
    2026-05-06 (am) 2026-05-05->2026-05-06 move=-4.70%  surprise=+0.050 dir_match=False
    2026-07-29 (am) 2026-07-28->2026-07-29 move=+5.10%  surprise=+0.190 dir_match=True

==============================================================================
PART 2 -- SOFI IMPLIED VS REALIZED EARNINGS MOVE
==============================================================================
  spot: 16.7918
  atm_strike: 17.0000
  straddle_before_dollars: 1.7100
  straddle_after_dollars: 2.1550
  straddle_before_pct: 0.1018  (10.18%)
  straddle_after_pct: 0.1283  (12.83%)
  days_before: 29
  days_after: 36
  baseline_scaled_pct: 0.1135  (11.35%)
  implied_earnings_move_linear_pct: 0.0149  (1.49%)
  implied_earnings_move_quadrature_pct: 0.0600  (6.00%)
  realized_median_abs_move_pct: 0.0657  (6.57%)
  realized_mean_abs_move_pct: 0.0766  (7.66%)

==============================================================================
PART 3 -- SOFI DEC 18 2026 $19 CALL, BLACK-SCHOLES SCENARIOS
==============================================================================
  current mark: 0.98  IV: 0.5320  delta: 0.3762  gamma: 0.0881  theta: -0.0102  vega: 0.0308
  BS price today (sanity check vs mark): 0.9789

  Unchanged-stock IV scenarios (valuation date 2026-10-28, day after report):
    current_iv (sanity check, S unchanged, only time passes): IV=0.5320  price=0.6026  chg_vs_current_mark=-38.51%
    jan2027_$19c_iv_proxy: IV=0.5256  price=0.5884  chg_vs_current_mark=-39.95%
    current_iv_minus_8pts: IV=0.4520  price=0.4306  chg_vs_current_mark=-56.07%
    current_iv_minus_15pts: IV=0.3820  price=0.2916  chg_vs_current_mark=-70.25%

  Scenario table (IV drop of 8 points to 0.4520, valuation date 2026-10-28):
     move     spot  call_px  delta  vs_mark  stop_trig(>0.66) stop_lim(>0.60) ratchet(>1.03)
     -15%    14.27    0.056  0.058  -94.31%             False           False          False
      -8%    15.45    0.164  0.134  -83.23%             False           False          False
      +0%    16.79    0.431  0.270  -56.07%             False           False          False
      +8%    18.14    0.904  0.437   -7.80%              True            True          False
     +15%    19.31    1.505  0.585   53.58%              True            True           True

==============================================================================
PART 3B -- FULL POSITION (2 calls + 10 shares), LIVE 2026-09-25 QUOTES
==============================================================================
  SOFI live spot 2026-09-25 14:29 UTC: 16.685
  19C sanity: BS_now=0.916 vs live_mark=0.915 delta=0.363
  18C sanity: BS_now=1.205 vs live_mark=1.210 delta=0.444
  Today's mark-to-market position value (2 calls x100 + 10 shares): 379.35

  Decomposition (spot unchanged): pure IV-crush-only vs pure time-decay-only vs combined:
    19C: now=0.916  IV-crush-only=0.680 (-25.74%)  decay-only(34d)=0.560 (-38.81%)
    18C: now=1.205  IV-crush-only=0.954 (-20.88%)  decay-only(34d)=0.823 (-31.74%)

  Pure time-decay stop-crossing check (S and IV held at today's live values -- does theta ALONE push the
  price through the stop trigger before the 2026-10-27 report?):
    19C: YES -- crosses trigger around 2026-10-20 (px=0.652), i.e. before earnings even happens
    18C: YES -- crosses trigger around 2026-10-16 (px=0.971), i.e. before earnings even happens

  Scenario table (valuation 2026-10-28, IV drop 8pts, spot grid off live 16.685):
    move=-15%  S=14.18
        19C: px=0.048 (-94.12% vs cost)  delta=0.05  [GAP-THROUGH (unfilled, exposed)]
        18C: px=0.094 (-92.26% vs cost)  delta=0.09  [GAP-THROUGH (unfilled, exposed)]
        10sh value=141.82  [STOP HIT, market fill ~14.18 (gap below 15.75)]
    move=-8%  S=15.35
        19C: px=0.146 (-82.15% vs cost)  delta=0.12  [GAP-THROUGH (unfilled, exposed)]
        18C: px=0.260 (-78.70% vs cost)  delta=0.20  [GAP-THROUGH (unfilled, exposed)]
        10sh value=153.50  [STOP HIT, market fill ~15.35 (gap below 15.75)]
    move=+0%  S=16.68
        19C: px=0.393 (-52.02% vs cost)  delta=0.25  [GAP-THROUGH (unfilled, exposed)]
        18C: px=0.632 (-48.16% vs cost)  delta=0.37  [GAP-THROUGH (unfilled, exposed)]
        10sh value=166.85  [no stop hit]
    move=+8%  S=18.02
        19C: px=0.842 (2.71% vs cost)  delta=0.42  [no stop hit]
        18C: px=1.244 (1.94% vs cost)  delta=0.55  [no stop hit]
        10sh value=180.20  [no stop hit]
    move=+15%  S=19.19
        19C: px=1.422 (73.37% vs cost)  delta=0.57  [no stop hit]
        18C: px=1.971 (61.57% vs cost)  delta=0.69  [no stop hit]
        10sh value=191.88  [no stop hit]
```

## Verdict

**P1 -- PARTLY REFUTED.** Direction holds (every name's earnings move beats
its normal day, ratio 1.99x-7.71x, all >1.5x), but the specific numbers are
off on both counts. The median ratio across the 8 names is **3.47x**
(mean 3.78x) -- above the predicted 1.5-3x band, driven by INTC (4.52x),
TGT (4.00x), ABBV (4.13x) and especially EXEL (7.71x). And SOFI is **not**
the largest mover: EXEL (7.94% median) and INTC (7.89% median) both beat
SOFI's 6.57% median / 7.66% mean, which itself falls short of the
predicted 8-10% range. SOFI ranks 3rd of 8 by median move, not 1st.

**P2 -- REFUTED.** The quadrature-based implied earnings-only move is
**6.00%** of spot, which is *below* SOFI's realized median (6.57%) and
clearly below its realized mean (7.66%). Options are not currently
overpricing SOFI's earnings move by this method -- if anything they are
priced roughly in line with (slightly under) the historical median. This
is the opposite of the predicted earnings-volatility premium. (The linear
lower-bound estimate, 1.49%, is even further below realized, but per the
script's own caveat that's not the primary estimate.)

**P3 -- PARTLY CONFIRMED, badly understates the practical loss.** Isolating
just the "post-earnings IV drop" component the prediction names (spot
unchanged, 8-point IV crush, no extra time passing): the $19C loses 25.7%
and the $18C loses 20.9% -- close to, but above, the predicted 10-20% band.
But that isolation is not what an investor actually experiences by the day
after earnings: once the realistic 34 days of theta between now and
2026-10-28 are included, a *flat* SOFI costs the $19C **52%** of its value
and the $18C **48%**, roughly 2.5-3x the predicted range. Worse, pure theta
decay alone (no IV change, no earnings) would carry both calls through
their stop triggers **before the report even happens** (18C around
2026-10-16, 19C around 2026-10-20) if SOFI simply sits still until then.

## What this means for Oct 27

- If SOFI is flat or down through earnings, both calls are structurally
  expected to be worth far less than their cost even without any
  disaster -- ordinary time decay plus a garden-variety IV crush would
  take the $19C to roughly 0.39-0.15 and the $18C to roughly 0.63-0.26,
  well under either cost basis.
- In the -8% and -15% scenarios, both calls' modeled value gaps straight
  through their stop-limit floors (0.60 and 0.90). The resting stop-limit
  orders would not fill there; they would sit open and unfilled while the
  actual mark sat below the limit, so the position would carry the full
  modeled loss until the market trades back up to the limit or someone
  intervenes manually.
- At 0% move the same thing happens: modeled value (0.39 / 0.63) is
  already below both limits purely from the IV crush plus 34 days of
  decay, with no adverse stock move required at all.
- Only the +8% and +15% scenarios keep both calls above their stops, and
  by +15% the $19C is worth about 73% more than its cost and the $18C
  about 62% more -- the position needs a real rally, not just "okay
  earnings," to come out ahead of cost by the day after the report.
- The 10 shares are unaffected by the option math: they lose value
  1:1 with SOFI and only trip the 15.75 stop in the -8% and -15%
  scenarios (spot would be 15.35 and 14.18); at 0%, +8% and +15% the
  share stop is untouched.
- Separately from the earnings scenario: if SOFI just sits at today's
  price with no news at all, plain time decay is on pace to carry the
  $18C through its stop around 2026-10-16 and the $19C around
  2026-10-20 -- roughly one to one-and-a-half weeks *before* the report,
  with no earnings reaction involved.
- No stop change is proposed here; whether and how to react to any of
  this is Nolan's call, and nothing here is adopted before the weekend
  re-read (R16.3).

## Limits

- Small samples: n=7 reports per symbol (about 1.75 years of quarters).
  Ratios and medians, especially EXEL's 7.71x and INTC's 23.6% one-quarter
  move, are driven by a handful of observations and could shift a lot with
  one more or one fewer data point.
- The 2026-10-27 report date/timing comes from Robinhood
  `get_earnings_results` with `verified=false` on record
  (`sofi_options_2026-09-24.json`); if the date or am/pm timing changes,
  the whole PART 3B reaction-window logic (and the "before the report"
  decay-crossing dates) shifts with it.
- The 8-point IV crush used throughout PART 3/3B is a mid-case assumption,
  not measured from SOFI's own post-earnings IV history; a shallower or
  deeper crush would move the scenario table meaningfully, especially at
  0% move where the position is already close to the stop lines.
- Standard Black-Scholes, no skew/smile, no dividend (correct, SOFI pays
  none), r=4% flat. Real market-maker pricing around an earnings gap can
  differ from BS, especially right at the open when liquidity is thin.
- "Gap-through" is a modeled-price statement, not a guarantee of what a
  live order book would do; actual fills depend on realized liquidity and
  where market makers actually quote the contract at the open, not just
  the theoretical value.
- The implied-vs-realized comparison (P2) uses a single day's straddle
  snapshot (2026-09-24) and a specific quadrature method; a different
  day, a different pair of expiries, or a linear (not quadrature) method
  gives a different answer, as shown by the 1.49% vs 6.00% spread between
  the two methods computed here.
- Position sizing assumed 1 contract per call leg and 10 shares, per
  `routines/HOURLY_TRADING_CHECK.md` and the task's own figures; if actual
  size differs, the dollar columns (not the percentages) would scale
  accordingly.
- SOFI live quotes are a single 2026-09-25 mid-morning snapshot, not an
  intraday range; spreads and marks can move materially before 10-27.
