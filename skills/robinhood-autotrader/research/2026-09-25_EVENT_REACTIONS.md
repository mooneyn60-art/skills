# Event Reactions: Gaps Through Stops, Earnings Gaps, and Fed Days

One-line: RESEARCH_AGENDA item 3. How often does the market open BELOW a
stop so the stop fills worse than planned, how much of that happens on
earnings, and do Fed announcement days behave differently?
(Earnings-move SIZE and the SOFI option scenarios are item 24, a separate
note in progress; not repeated here.)

Last Updated: 2026-09-25
Status: DONE. Prediction committed first (482e01e); mostly held.
Audience: Nolan, TARS sessions

## Tests (fixed before running)

E1  Overnight gaps. Gap = open / prior close - 1. For a stop sitting k%
    below the prior close (k = 2, 4, 6, 8%): the share of days the open is
    already below it, and the average shortfall (how far below the stop
    the open was) when it happens. Two samples: 14 names 2006-2026
    (daily_stocks.json) and the current holdings 2022-2026
    (daily_ohlcv_holdings.json).
E2  For the holdings: of all gaps of -8% or worse, the share that were
    earnings reaction days (earnings_reports.json: report day if before
    the open, next trading day if after the close).
E3  Fed statement days (list compiled from federalreserve.gov) 2006-2026:
    S&P 500 TR close-to-close return on statement day, and on the day
    before, against all other days. Welch t; split halves.

## PREDICTION

E1 14 names: open below a 4% stop on 0.3-0.8% of days, below an 8% stop
   on 0.05-0.2% of days; average shortfall when it happens 2-4%. Holdings:
   2-3x more often.
E2 More than half of the holdings' -8% gaps are earnings days.
E3 Statement day about +0.2 to +0.4pp better than other days, t < 2 over
   2006-2026; the day-before drift (Lucca & Moench) weak in 2016-2026.

## Answer first

- STOPS DO GET SKIPPED, RARELY, AND IT COSTS ABOUT 3% WHEN THEY DO. On the
  14 long-history names, the market opened below a stop sitting 8% under
  the prior close on 0.17% of days (about once every 2.3 years per name);
  the average fill was 3.3% worse than the stop, and the worst 31%. For the
  more volatile current holdings it's about twice as often (0.32%), average
  3.7% worse. A tighter stop gets skipped far more often: 4% below the
  prior close, 0.8% of days (holdings 1.4%).
  So R4's "8% stop" really means "8%, occasionally 11-12%, very rarely 30%+".
- MOST BIG GAPS ARE EARNINGS OR MARKET SHOCKS. Of the holdings' 12 opening
  gaps of -8% or worse (2025-2026), 7 were earnings reaction days, and 4 of
  the other 5 were the April 2025 tariff crash (Apr 3-7) or its week. Only
  one (EXEL, 2025-10-20) had neither. R2's "no entry within 3 trading days
  of earnings" rule is aimed at the right risk; nothing protects a
  position ALREADY held through earnings.
- FED DAYS: the statement day used to be a good day and isn't any more.
  2006-2015: +0.49pp above other days (t = 3.08). 2016-2026: -0.03pp
  (t = -0.26). The documented "pre-FOMC drift" on the day before is
  absent throughout. A textbook case of a published pattern fading (item 20).

## Result

Script: paper/test_event_reactions.py. FOMC dates: paper/history/fomc_dates.json
(165 scheduled statement days 2006-2026, compiled by a sub-agent from
federalreserve.gov; spot-checked against 8 known dates, all correct).

    E1 open already below a stop k% under the prior close
       k     14 names 2006-2026 (72,912 name-days)     holdings 2022-2026 (7,119)
       2%    3.12% of days, avg shortfall 1.76%         5.68%, 1.76%
       4%    0.83%,        2.70%  (worst 33.9%)         1.43%, 2.86%
       6%    0.36%,        3.16%                        0.60%, 3.58%
       8%    0.17%,        3.31%  (worst 31.1%)         0.32%, 3.68% (worst 17.9%)

    E2 holdings, gaps <= -8% since each name's first listed report (2025-26):
       SOFI 4 (2 earnings), INTC 3 (3), TGT 1 (1), EXEL 2 (1), NWG 1 (0),
       CVE 1 (0), ABBV 0. Total 12, 7 on earnings reaction days.
       Non-earnings: SOFI 2025-04-03, 2025-04-07, NWG 2025-04-04 (tariff
       crash), CVE 2026-04-08, EXEL 2025-10-20.

    E3 S&P 500 TR on Fed statement days vs other days
       2006-2026  +0.263% vs +0.041%  diff +0.222pp  t=+2.20  (n=165)
       2006-2015  +0.509% vs +0.018%  diff +0.491pp  t=+3.08
       2016-2026  +0.031% vs +0.062%  diff -0.031pp  t=-0.26
       day before, all periods: diff +0.03 to +0.07pp, t < 0.5

## Scored against the prediction

    E1 4% stop 0.3-0.8% of days: 0.83%, RIGHT at the edge. 8% stop 0.05-0.2%:
       0.17% RIGHT. Shortfall 2-4%: RIGHT. Holdings 2-3x: 1.7-1.9x, slightly WRONG.
    E2 more than half on earnings days: RIGHT (7 of 12).
    E3 statement day +0.2-0.4pp: RIGHT (+0.22pp). t < 2: WRONG (2.20).
       Day-before drift weak after 2016: RIGHT (absent in both halves).

## What this means for TARS (interpretation)

- Size positions assuming the stop can fail by ~4 percentage points, and
  in a crash by much more. R3's risk budget treats the stop as exact; the
  honest planned loss at an 8% stop is closer to 8% x 1.4 once in a while.
- Holding through earnings is where the stop is least reliable. Whether to
  trim before earnings is a sizing question (item 10); item 24 has the
  earnings-move sizes to decide it.
- Don't trade around Fed days. The edge that existed is gone.
