# Event Reactions: Gaps Through Stops, Earnings Gaps, and Fed Days

One-line: RESEARCH_AGENDA item 3. How often does the market open BELOW a
stop so the stop fills worse than planned, how much of that happens on
earnings, and do Fed announcement days behave differently?
(Earnings-move SIZE and the SOFI option scenarios are item 24, a separate
note in progress; not repeated here.)

Last Updated: 2026-09-25
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
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

## Result

(not yet run)
