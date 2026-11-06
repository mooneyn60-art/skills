# R15 MAKES TARS-1 WORSE. RECOMMEND REPEALING IT.

One-line: tested inside the full TARS-1 system for the first time, R15 (the
VIX regime switch) cuts CAGR by 1.14pp and deepens the worst drawdown from
-33.6% to -45.9% over 2006-2026. It is worse in both halves of the sample
and with the megacaps removed, and it wins only 4 of 9 walk-forward windows.

Last Updated: 2026-09-26
Status: DONE. Prediction committed first (fb0274e, in the script header). It was WRONG.
Audience: Nolan, TARS sessions

## The question

R15 was adopted live on 2026-09-23 on the strength of an entry statistic
(+4.95pp/month, t = 8.46). Tested alone it was already weak
(research/2026-09-23_R15_EXIT_SOLVED.md). But it was never meant to run
alone; it modifies TARS-1 during stress. This asks the question that
matters: does TARS-1 WITH R15 beat TARS-1 WITHOUT it?

## Method

paper/engine.py gained an optional R15 switch (off by default; the engine's
built-in comparison output was checked byte-for-byte unchanged with it off).
TARS-1 as it stands: symmetric 200-day entry and exit, 8% stop, breakeven
at +8%, 20% trail, 20% position cap, 15% cash floor, whole shares, 5bp
slippage, R5 sector cap and R6 breaker at engine defaults. With R15: when
weekly VIX (value dated at least 7 days before the day, so no look-ahead)
is 25 or more, ranging names (ADX14 < 20) in the bottom quartile of their
60-day range become eligible with the 200-day gate suspended; those
positions are tagged and exempt from the trend exit, with every other R4
exit applying. Script: paper/test_r15_integration.py. 14 names,
2006-2026, price returns, survivors only.

## Result

                            CAGR     max DD   Sharpe  trades  R15 entries
    FULL 2006-2026
      TARS-1               11.74%   -33.6%    0.77     443      0
      TARS-1 + R15         10.60%   -45.9%    0.70     411     56     diff -1.14pp
    2006-2015
      TARS-1                7.68%   -33.6%    0.55     216      0
      TARS-1 + R15          5.82%   -45.9%    0.43     202     36     diff -1.86pp
    2016-2026
      TARS-1               15.84%   -23.4%    1.00     242      0
      TARS-1 + R15         15.31%   -25.3%    0.96     233     21     diff -0.53pp
    MEGACAPS DROPPED (9 names)
      TARS-1                4.45%   -32.9%    0.41     540      0
      TARS-1 + R15          4.05%   -37.2%    0.36     482     69     diff -0.39pp

    WALK-FORWARD (9 windows, each run fresh)    without   with     diff    R15 entries
      2006-10 to 2009-01                         -7.38%   -9.96%   -2.58pp   23
      2009-01 to 2011-03                         17.59%   25.53%   +7.94pp   13
      2011-03 to 2013-06                          9.95%   12.38%   +2.42pp    4
      2013-06 to 2015-08                          2.28%    2.28%    0.00pp    0
      2015-08 to 2017-11                         31.77%   31.77%    0.00pp    0
      2017-11 to 2020-01                          6.21%    6.55%   +0.34pp    1
      2020-01 to 2022-04                         20.00%   27.12%   +7.11pp    4
      2022-04 to 2024-07                         18.32%    8.94%   -9.38pp   16
      2024-07 to 2026-09                         13.40%   13.40%    0.00pp    0
      R15 version ahead: 4 of 9 (3 windows with no R15 entries at all)

## What happened (interpretation)

- THE DRAWDOWN IS THE STORY. The -45.9% comes from 2008. VIX stayed above
  25 for months, R15 kept buying ranging names at the bottom of their
  ranges with the 200-day gate off, and with the trend exit disabled for
  those positions only the 8% stop stood between the book and a falling
  market. That is the "falling knife" R15's own text warned about.
- R15 WORKS WHEN THE STRESS IS SHORT: 2009-2011 (+7.9pp) and the 2020 crash
  and rebound (+7.1pp). It hurts when the stress is long: 2008 (-2.6pp) and
  the 2022 bear market (-9.4pp). No one can tell which kind of stress
  they're in at the time it starts.
- This agrees with item 8 (research/2026-09-25_MULTIPLE_TESTING.md): R15's
  entry statistic falls from t = 8.46 to t = 2.21 once overlapping samples
  are handled, and 56 entries in 20 years is too few to tell a real edge
  from the three or four stress episodes that happen to be in the sample.

## Scored against the prediction

    CAGR diff within +/-1pp:           WRONG (-1.14pp)
    max DD within +/-3pp:              WRONG (-12.3pp)
    ahead in 3-6 of 9 windows:         RIGHT (4)
    megacaps dropped within +/-1pp:    RIGHT (-0.39pp)
    R15 entries "a few dozen":         RIGHT (56)
    verdict "no meaningful difference": WRONG. It is worse.

R16 trigger (c) is on for the rest of this session.

## Recommendation (Nolan decides; nothing changed in TARS_RULES.md)

REPEAL R15. The system is worse with it on the two measures that matter
most for this account, return and worst loss. The evidence that justified
it has shrunk from t = 8.46 to t = 2.21. Repealing R15 TIGHTENS the rules
(it restores the 200-day gate at all times), so it is consistent with R16,
which forbids only loosening while the pressure state is on.

If Nolan wants to keep R15 anyway, the smallest defensible change is to
restore the 200-day trend exit for R15-tagged positions (so a stressed-market
entry can't ride a falling market down with only the 8% stop). That
variant was NOT tested here, and it must be tested before it goes live.

## Caveats

14 surviving names; price returns only; R15 as coded here, not as a
human would apply it on the day; the VIX alignment is conservative (a
week's close is only used after the week has ended). None of these changes
the direction of the result, and the drawdown gap (12pp) is far larger
than any of them could plausibly explain.
