# Multiple Testing: How Many Ideas Have We Tried, and What Survives?

One-line: RESEARCH_AGENDA item 8. Count every hypothesis tested in this
repository, correct for it, and re-check the evidence behind live rules,
starting with R15's t = 8.46.

Last Updated: 2026-09-25
Status: PARTIAL. M2 run (below); M1 inventory pending from a sub-agent.
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

## Result (partial: M2 only)

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

Against the prediction: (a) RIGHT (+5.67pp, t=7.85); (b) RIGHT (t=2.21, in
the predicted 1.5-3). R15's evidence fails |t| >= 3.
