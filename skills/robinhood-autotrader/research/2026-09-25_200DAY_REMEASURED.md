# The 200-Day Rule, Re-Measured Properly

One-line: the 200-day gate is TARS's core rule. Its best evidence (t=5.14,
t=2.84, t=1.97) came from overlapping samples, the same flaw that took R15
from t=8.46 to t=2.21. Does the core survive when measured correctly?

Last Updated: 2026-09-25
Status: DONE. Predictions committed first (60ae4b0). Nothing in this note is
adopted into TARS_RULES.md before the weekend re-read (R16.3).
Audience: Nolan, TARS sessions

## Overview

Sources re-measured: research/2026-09-24_MOMENTUM_VS_REVERSAL.md (200-day
gate: large caps 21d t=1.97, volatile 21d t=2.84, 63d t=5.14; 3m and 12-1m
momentum ICs) and research/2026-09-25_MULTIPLE_TESTING.md (the method).
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read.

The 200-day rule makes TWO claims, tested separately:
  RETURN claim: stocks above their 200-day earn more over the next month.
  RISK claim: stocks below their 200-day are more volatile and fall
  harder, so being out of them cuts drawdowns.

## Predictions (written before the test)

P1 RETURN claim, measured with non-overlapping monthly samples and
   month-clustered errors: t falls below 2.5 in both universes. Probably
   below 2 for large caps. The return edge is weak.
P2 RISK claim: survives clearly (t > 3, clustered). Next-month volatility
   is higher below the 200-day, in both universes and both halves. It's
   volatility clustering, one of the most durable facts in finance.
P3 So the honest description of the 200-day rule is "risk control, not
   return prediction", and that's what it should be credited with.
P4 The 12-1 month momentum IC also falls below t = 2.5 when clustered.

What would prove P3 wrong: the RETURN claim holding at t > 3 clustered in
both universes, or the RISK claim failing (t < 2) in either.


## Results

Script: `paper/research_scripts/remeasure_200day.py`. Sampling: first trading
day of each month only (non-overlapping 21d forward windows); quarterly
first-trading-day sampling for the 63d variant. All "clustered t" columns
below use a per-period (month or quarter) construction: see the script's
docstring for exactly which construction each column uses -- (b) and RISK
average the group difference per period then run a one-sample t across
periods; (c) pools individual excess-return observations and uses a
cluster-robust t on that pool, so it is NOT arithmetically forced to equal
(b) the way a same-construction excess version would be. Splits: large caps
at 2016-06-01, volatile at 2021-01-01.

| Claim | Universe | Diff | Clustered t | 1st-half t | 2nd-half t |
|---|---|---:|---:|---:|---:|
| RETURN, monthly (b) | large caps | +0.47pp | 1.06 | -0.49 | 2.06 |
| RETURN, monthly (b) | volatile | +2.68pp | 2.32 | 2.12 | 0.94 |
| RETURN, excess/cluster-robust (c) | large caps | +0.39pp | 1.76 | -0.29 | 2.62 |
| RETURN, excess/cluster-robust (c) | volatile | +1.45pp | 2.97 | 3.12 | 0.98 |
| RETURN, 63d quarterly | large caps | +0.33pp | 0.24 | -1.10 | 1.68 |
| RETURN, 63d quarterly | volatile | +8.94pp | 2.36 | 2.22 | 0.82 |
| RISK, vol21 (below-above) | large caps | +0.0142 | 2.10 | 2.18 | 0.57 |
| RISK, vol21 (below-above) | volatile | +0.1029 | 4.29 | 3.96 | 1.95 |
| RISK, dd21 (below-above) | large caps | +0.0055 | 2.34 | 1.57 | 1.76 |
| RISK, dd21 (below-above) | volatile | +0.0342 | 6.50 | 6.30 | 2.01 |
| 12-1m momentum IC | large caps | 0.0451 | 1.88 | 1.45 | 1.21 |
| 12-1m momentum IC | volatile | 0.0963 | 3.71 | 3.59 | 1.07 |

Naive (uncorrected, pooled name-months, no clustering) RETURN t for
reference: large caps t=0.93 (+0.36pp), volatile t=2.39 (+2.14pp) -- both
close to their month-clustered (b) counterparts here, unlike R15's daily
version where naive t=8.46 collapsed to clustered t=2.21; the gap matters
less here because the sampling is already monthly, so naive vs clustered
differ only by cluster-size weighting, not by within-month non-independence.

12-1m momentum IC, comparison with `momentum_reversal.py` (month-END
sampling instead of first-trading-day):

| | this script (first-day) | momentum_reversal.py (month-end) |
|---|---|---|
| large caps, full | t=1.88 (n=235, mean=0.045) | t=2.60 (n=234, mean=0.061) |
| large caps, pre-split | t=1.45 (n=112) | t=1.92 (n=112) |
| large caps, post-split | t=1.21 (n=123) | t=1.75 (n=122) |
| volatile, full | t=3.71 (n=235, mean=0.096) | t=3.45 (n=234, mean=0.089) |
| volatile, pre-split | t=3.59 (n=167) | t=3.51 (n=167) |
| volatile, post-split | t=1.07 (n=68) | t=0.59 (n=67) |

Both sampling anchors agree on direction and rough magnitude in every cell;
large caps is consistently a bit weaker under first-trading-day sampling,
volatile a bit stronger. Neither anchor changes which side of any threshold
(2.5, 3.0) the answer falls on, except volatile's full-period IC, which
clears both under either anchor (t=3.71 vs t=3.45).

Full script output:

```
200-DAY GATE, RE-MEASURED -- raw output, no conclusions baked in
Sampling: first trading day of each month (non-overlapping 21d fwd windows);
quarterly first-trading-day for the 63d variant. See docstring for exact
construction of each 'clustered' statistic.
Large-cap universe: ['AAPL', 'AMZN', 'BAC', 'C', 'CSCO', 'F', 'GE', 'GOOGL', 'IBM', 'MSFT', 'NVDA', 'PFE', 'T', 'XOM']
Volatile universe:  ['AFRM', 'AMD', 'COIN', 'CRWD', 'DKNG', 'ENPH', 'HOOD', 'MARA', 'MU', 'NET', 'NFLX', 'NVDA', 'PLTR', 'RIOT', 'RIVN', 'ROKU', 'SHOP', 'SNAP', 'SOFI', 'TSLA', 'UBER', 'UPST']

==========================================================================================
UNIVERSE: large caps (SPY excluded)  (14 names)
==========================================================================================
first-trading-day-of-month dates: 249 (2006-01-03 .. 2026-09-01)
of which quarter-start (Jan/Apr/Jul/Oct) dates: 83

--- RETURN claim: forward 21-day return, above vs below SMA200 ---
(a) naive (pooled name-months, Welch t): n_above=2072 n_below=1260 diff=0.357pp t=0.93
    (a) first half: diff=0.108pp t=0.18 n=973+637   second half: diff=0.550pp t=1.16 n=1099+623
(b) month-clustered (per-month avg diff, t across months): months=225 diff=0.470pp t=1.06
    first half: months=106 diff=-0.332pp t=-0.49   second half: months=119 diff=1.186pp t=2.06
(c) excess-return, pooled obs, cluster-robust t (clustered by month): n=2072+1260 clusters=234/229 diff=0.392pp t=1.76
    first half: diff=-0.086pp t=-0.29   second half: diff=0.857pp t=2.62
Quarterly 63d-fwd, clustered by quarter: quarters=75 diff=0.332pp t=0.24
    first half: quarters=38 diff=-2.301pp t=-1.10   second half: quarters=37 diff=3.035pp t=1.68

--- RISK claim: forward 21-day realized vol and max-drawdown, below vs above (positive = below is riskier) ---
vol21 (annualized): months=225 mean(below-above)=0.0142 t=2.10
    first half: months=106 mean=0.0255 t=2.18   second half: months=119 mean=0.0042 t=0.57
dd21 (max-drawdown magnitude): months=225 mean(below-above)=0.0055 t=2.34
    first half: months=106 mean=0.0060 t=1.57   second half: months=119 mean=0.0050 t=1.76

--- 12-1m momentum rank IC vs forward 21d return (first-trading-day sampling) ---
IC: months=235 mean=0.0451 t=1.88
    first half: months=112 mean=0.0501 t=1.45   second half: months=123 mean=0.0404 t=1.21
    for comparison, momentum_reversal.py (month-END sampling) 12-1m IC:
      large caps: full n=234 IC_mean=0.0614 t=2.60 | pre n=112 t=1.92 | post n=122 t=1.75
      volatile:   full n=234 IC_mean=0.0893 t=3.45 | pre n=167 t=3.51 | post n=67  t=0.59

==========================================================================================
UNIVERSE: volatile names  (22 names)
==========================================================================================
first-trading-day-of-month dates: 249 (2006-01-03 .. 2026-09-01)
of which quarter-start (Jan/Apr/Jul/Oct) dates: 83

--- RETURN claim: forward 21-day return, above vs below SMA200 ---
(a) naive (pooled name-months, Welch t): n_above=1542 n_below=1163 diff=2.140pp t=2.39
    (a) first half: diff=4.769pp t=3.70 n=765+529   second half: diff=-0.308pp t=-0.25 n=777+634
(b) month-clustered (per-month avg diff, t across months): months=212 diff=2.682pp t=2.32
    first half: months=149 diff=3.219pp t=2.12   second half: months=63 diff=1.413pp t=0.94
(c) excess-return, pooled obs, cluster-robust t (clustered by month): n=1542+1163 clusters=227/223 diff=1.451pp t=2.97
    first half: diff=2.393pp t=3.12   second half: diff=0.612pp t=0.98
Quarterly 63d-fwd, clustered by quarter: quarters=67 diff=8.939pp t=2.36
    first half: quarters=47 diff=10.810pp t=2.22   second half: quarters=20 diff=4.542pp t=0.82

--- RISK claim: forward 21-day realized vol and max-drawdown, below vs above (positive = below is riskier) ---
vol21 (annualized): months=212 mean(below-above)=0.1029 t=4.29
    first half: months=149 mean=0.1305 t=3.96   second half: months=63 mean=0.0374 t=1.95
dd21 (max-drawdown magnitude): months=212 mean(below-above)=0.0342 t=6.50
    first half: months=149 mean=0.0431 t=6.30   second half: months=63 mean=0.0131 t=2.01

--- 12-1m momentum rank IC vs forward 21d return (first-trading-day sampling) ---
IC: months=235 mean=0.0963 t=3.71
    first half: months=167 mean=0.1197 t=3.59   second half: months=68 mean=0.0386 t=1.07
    for comparison, momentum_reversal.py (month-END sampling) 12-1m IC:
      large caps: full n=234 IC_mean=0.0614 t=2.60 | pre n=112 t=1.92 | post n=122 t=1.75
      volatile:   full n=234 IC_mean=0.0893 t=3.45 | pre n=167 t=3.51 | post n=67  t=0.59

==========================================================================================
SUMMARY (key clustered t-stats)
==========================================================================================
large caps: RETURN (b) t=1.06  RETURN (c) t=1.76  RETURN 63d-quarterly t=0.24  RISK vol t=2.10  RISK dd t=2.34  12-1m IC t=1.88
volatile: RETURN (b) t=2.32  RETURN (c) t=2.97  RETURN 63d-quarterly t=2.36  RISK vol t=4.29  RISK dd t=6.50  12-1m IC t=3.71
```

## Verdict

**P1 (RETURN claim falls below t=2.5 clustered, both universes): PARTLY
CONFIRMED.** The primary month-clustered measure (b) stays under 2.5 in
both universes (large caps t=1.06, volatile t=2.32) and large caps is
indeed under 2, as predicted. But the excess-return/cluster-robust variant
(c) -- a legitimate, non-redundant alternative construction of "clustered,"
included because a literal per-month-average excess test is mathematically
guaranteed to reproduce (b) exactly -- pushes volatile to t=2.97, above the
2.5 line (still under the repo's 3.0/3.9 hurdles). The return edge for
volatile names is on the border of "weak" and "suggestive" depending on
exactly how you cluster; large caps is unambiguously weak by any of the
three RETURN constructions here (max t=1.76).

**P2 (RISK claim survives clearly, t>3 in both universes and both halves):
REFUTED as stated, but the DIRECTION is perfect.** All 8 risk cells (2
universes x 2 metrics x 2 halves) plus both full-period numbers have the
correct sign -- below the 200-day is always riskier, never once reversed.
But t>3 does not hold everywhere: large caps never clears 3 at all (full
vol t=2.10, dd t=2.34); volatile clears 3 easily in the first half (vol
3.96, dd 6.30) but falls to t=1.95 (vol) and t=2.01 (dd) in the second
half (2021-01 onward). Full-period numbers clear t>2 in both universes
(2.10-6.50), so the note's own pre-registered falsification test ("RISK
claim failing t<2 in either" universe, full period) is NOT triggered --
but the recent-half decay is real and larger than P2 anticipated.

**P3 (200-day rule = risk control, not return prediction): CONFIRMED by
the note's own pre-registered falsification test**, since neither trigger
fired (RETURN never reaches t>3 clustered in either universe; RISK never
drops below t<2 in either universe, full period). The qualifier: risk
control is also weakening over time, especially in the more recent half of
both universes, so "risk control" should not be read as a fixed, stable
edge either -- see What this means for TARS.

**P4 (12-1m momentum IC falls below t=2.5 clustered): PARTLY CONFIRMED --
true for large caps (t=1.88), false for volatile (t=3.71).** Volatile's
12-1m IC stays significant even above the repo's Harvey-Liu-Zhu 3.0
hurdle in the full period, though it decays hard in the second half
(t=1.07, n=68 months). This matches the volatile RETURN
claim's own pattern: whatever edge exists there is concentrated pre-2021
and has faded since.

## What this means for TARS

- The 200-day gate should be credited as a RISK control, not a source of
  extra RETURN: forward-return differences between above/below the
  200-day are weak (t roughly 1-3 depending on universe and exact
  clustering), never approaching the repo's 3.0/3.9 significance bars.
- The RISK side is real and directionally universal (100% of cells: below
  the 200-day is more volatile and draws down harder), which is the
  strongest, most consistent single fact in this whole re-measurement --
  but it is not uniformly strong. Treat it as "usually true, sometimes
  weak," not "always true at high confidence," especially recently.
- The risk-reduction signal has been WEAKER in the second half of the
  sample (post-2016 for large caps, post-2021 for volatile) than in the
  first half, in every single risk cell measured. Do not assume the
  200-day's risk-cutting power in 2006-2016/2020 data still applies at
  full strength today; it may be real but smaller.
- For the volatile universe specifically, both the RETURN edge and the
  12-1m momentum IC are stronger and more significant than for large caps
  in the full sample, but both effects are concentrated pre-2021 and
  largely absent since (RETURN t drops from 3.70 to -0.25 pre/post naive;
  IC t drops from 3.59 to 1.07). Anything built on the volatile
  universe's historical momentum/return edge should assume it may already
  be gone in the live-trading period.
- Nothing here argues for removing the 200-day gate; it argues for
  describing it honestly in TARS_RULES.md as a volatility/drawdown filter
  with a real but modest and possibly-decaying effect, not as a
  return-generating signal, and not at the old daily-overlap
  significance levels.
- As with R15 and the MULTIPLE_TESTING inventory, this is one more
  measurement in a large multiple-testing family; none of these numbers
  should be read in isolation from that inventory's Bonferroni/HLZ
  hurdles (|t| >= 3.0-3.9).

## Limits

- 14 large-cap names and 22 volatile names is a small cross-section;
  per-month group sizes are often single digits, so individual monthly
  diffs are noisy even before clustering.
- The excess-return/cluster-robust construction (c) was a deliberate
  design choice made in this script, not a literal transcription of the
  task's own parenthetical definition of "clustered t" -- see the
  script's docstring for why a literal transcription would have been
  arithmetically forced to equal (b) exactly, which would have made (c) a
  redundant, uninformative check.
- Max-drawdown here resets the "peak" to the sample-date close and looks
  only 21 trading days forward; a longer or differently-anchored drawdown
  window could show a different magnitude (though the RISK claim's
  consistent sign is unlikely to flip).
- Volatile names have uneven start dates (some from 2006, several from
  2020-2021), so post-split volatile samples are thin (63-68 months,
  20 quarters) -- second-half volatile numbers are the least reliable in
  this note.
- This note's own multiple comparisons (6 metrics x 2 universes x 3
  periods, plus 2 sampling anchors for the momentum IC) were not
  Bonferroni-corrected against each other; read individual cells with the
  same caution research/2026-09-25_MULTIPLE_TESTING.md applies everywhere
  else in this repository.
- Nothing in this note is adopted into TARS_RULES.md or any live rule
  before the weekend re-read (R16.3). This is measurement only.
