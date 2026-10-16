# Multiple Testing: How Many Ideas Have We Tried, and What Survives?

One-line: RESEARCH_AGENDA item 8. Count every hypothesis tested in this
repository, correct for it, and re-check the evidence behind live rules,
starting with R15's t = 8.46.

Last Updated: 2026-09-25
Status: DONE. Predictions committed first (de08755). No positive return edge in the repository survives the correction.
Audience: Nolan, TARS sessions

## Two separate problems

1. MANY TESTS. With N independent tests at the usual |t| >= 2 (5%), about
   N/20 look significant by luck alone. Corrections: Bonferroni (required
   |t| rises with N), and Harvey, Liu & Zhu's |t| >= 3 for any new finding.
2. OVERLAPPING SAMPLES. R15's evidence used DAILY observations of a
   21-DAY forward return, across 14 stocks on the same days. Consecutive
   days share 20 of their 21 return days, and stocks crash together, so
   the observations are far from independent, and the usual t-statistic
   overstates the evidence. A rough correction divides t by sqrt(21);
   the clean fix is to sample once a month.

## Tests (fixed before running)

M1  Inventory: count distinct tests across research/ (sub-agent reads,
    I check), then compute the Bonferroni |t| hurdle for that N.
M2  Rebuild R15's finding from its note (2026-09-23_VIX_CONDITIONAL_
    REVERSAL.md): ranging names (ADX(14) < 20), forward 21-trading-day
    return, bottom quartile of the 60-day range minus top quartile, VIX
    weekly forward-filled from past data only, VIX >= 25 bucket.
    (a) daily, name-day observations as the original;
    (b) same, t from month-clustered standard errors (all name-days in a
        calendar month count as one cluster);
    (c) first trading day of each month only: per month, mean fwd return
        of bottom-quartile names minus top-quartile names, t across months.

## PREDICTION

M1: 100-250 distinct tests. Bonferroni hurdle at 5% for that N: |t| about
    3.5-3.9.
M2 (a) reproduces the original within ~1pp: about +4-6pp, t about 7-9.
M2 (b) and (c): the spread stays positive, but t falls to about 1.5-3.
    R15 FAILS the Bonferroni hurdle and probably Harvey-Liu-Zhu's 3.0.
Consequence I expect: R15's evidence is "suggestive", not "t = 8.46".
Its first live firings remain the real test, as R15 already says.

## Answer first

- WE HAVE TRIED ABOUT 500-650 IDEAS. A sub-agent inventoried every test in
  research/, TARS_RULES.md and STRATEGY.md: ~500 counting each pre-planned
  family once, ~650 counting every split and robustness variant. Five big
  indicator/pattern sweeps alone are ~350. (I checked three of its
  counts against the source notes: RSI2's "138 total looks", R17's
  t = -6.35 to -13.98 range, and indicators' "72 tests"; all matched.)
- AT THAT COUNT, LUCK ALONE SHOULD PRODUCE 25-33 RESULTS WITH |t| >= 2.
  The honest hurdle (Bonferroni, 5%) is |t| >= 3.9 (3.89 for N=500, 3.95
  for N=650). Harvey-Liu-Zhu's rule of thumb, |t| >= 3.0, is a softer floor.
- NO POSITIVE RETURN EDGE CLEARS 3.9 once its t is measured properly.
  R15's t = 8.46 becomes 2.21 with month-clustered errors (below). The
  other big positive t-stats in the repository come from the same kind of
  overlapping daily or 63-day samples (range regime t=5.20, 200-day gate
  63d t=5.14, RSI-2 pooled t=4.66). None was re-measured with clustered
  errors here, but they share the inflation, and by the R15 example it
  can be 3-4x.
- WHAT DOES SURVIVE is almost all NEGATIVE, "don't do this" evidence:
  buying OTM options loses (t = -17), the R17 bracket underperforms holding
  (t = -6 to -14 in every cell), put-writing and buy-writes trail the S&P
  since 2007. Plus one descriptive fact: volatility clusters (unemployment
  -> volatility, t = 3.87). The repository is good at killing ideas and
  has not yet found a robust one.

## What this means for live rules (interpretation; proposals only)

- R2 (200-day gate): its case rests on portfolio backtests and walk-forward
  counts (7/9), not a single t. Item 20 found its robust effect is
  avoiding volatile periods, which fits the one thing that DOES survive
  here (volatility clustering). Keep reading R2 as a risk control, not an
  edge.
- R15: the entry evidence is SUGGESTIVE (clustered t = 2.21, 53 stressed
  months). R15's own text already calls its first live firings an
  out-of-sample test. This result argues for keeping R15's position size
  at the normal cap, never larger, until those firings are scored.
- R17 (the option slot): not this item's question, but the inventory flags
  it. R17's chosen exit (a -20% stop / +25% ratchet bracket) underperformed
  plain holding in all 12 simulated cells, the most consistent result in
  the repository (research/2026-09-24_R17_SLOT_DESIGN.md). Nolan should see
  that before the next R17 trade.
- PROPOSED STANDING RULE (not adopted): any future rule change must report
  (1) a t-statistic from non-overlapping or cluster-robust errors, never a
  daily-overlap t, and (2) either |t| >= 3.9 or a single pre-registered
  test run once. Otherwise it goes in as "suggestive", with sizing to
  match.

## Result, M2

Script: paper/test_multiple_testing_r15.py.

    VIX bucket  (a) daily name-days          (b) month-clustered t   (c) monthly samples
    <15         -0.47pp t=-1.88 n=1005+3074  t=-0.67                 -1.08pp t=-0.85, 22 months
    15-20       -0.30pp t=-0.97 n=1254+2247  t=-0.32                 -0.48pp t=-0.23, 27 months
    20-25       -0.18pp t=-0.32 n=569+1088   t=-0.10                 +2.00pp t=+0.59, 13 months
    25+         +5.67pp t=+7.85 n=779+872    t=+2.21 (53/55 clusters) +5.92pp t=+0.70, 4 months

(a) reproduces R15's headline (+4.95pp, t=8.46) within 1pp. Clustered by
month, the t falls to 2.21. (c) catches only 4 stressed months on the first
trading day, too few to mean anything; (b) is the informative correction.
The lower VIX buckets don't match the original note (-0.71pp t=-2.48 and
+1.43pp t=2.92 there). The likely cause is VIX alignment: this rebuild uses
only weekly values at least 7 days old; the original's alignment wasn't
recorded.

## Result, M1 (inventory)

Sub-agent inventory of research/ (25 notes), TARS_RULES.md (TARS-2,
R2'/R3'/R4'/R6', Tested and REJECTED, R15) and STRATEGY.md. Low ~500 /
high ~650 distinct tests. The largest contributors, per each note's own
count: RSI2_AND_PANIC_DIPS 138, INDICATORS_PRICE 72, INDICATORS_VOLATILE_NAMES
54 (+36 robustness), CANDLESTICKS 48, INDICATORS_VOLUME_VWAP 38,
MOMENTUM_VS_REVERSAL ~34, R17_SLOT_DESIGN 36.

    Bonferroni |t| hurdle (two-sided 5%):  N=1 1.96 | N=20 3.02 | N=100 3.48 | N=500 3.89 | N=650 3.95

Largest reported positive-edge t-stats and how they were sampled:
    R15 VIX>=25 reversal   8.46   daily overlapping 21d fwd  -> 2.21 clustered (M2)
    range regime           5.20   daily overlapping 21d fwd  (not re-measured)
    200-day gate, 63d fwd  5.14   monthly, overlapping 63d   (not re-measured)
    RSI-2 pooled trades    4.66   pooled trades              (not re-measured)
    panic dips, crisis-excl 3.95  date-clustered             (1 of 48; fragile)
    backtest trade R        3.77  trades, not vs SPY         (item 18: IR 0.11 vs SPY)

## Scored against the prediction

    M1 100-250 tests, hurdle 3.5-3.9: count WRONG (500-650, 2-3x more than I
       guessed); hurdle RIGHT at the top of the range (3.9).
    M2 (a) reproduces within ~1pp, t 7-9: RIGHT (+5.67pp, t=7.85).
    M2 (b)/(c) t 1.5-3: RIGHT for (b) (2.21); (c) had only 4 months, uninformative.
    R15 fails Bonferroni and |t|>=3: RIGHT.
