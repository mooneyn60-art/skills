# Fundamentals: Does Earnings or Revenue Growth Improve R2 Entries?

One-line: RESEARCH_AGENDA item 1. Among stocks that pass R2's trend gate
(close above the 200-day), do names whose latest reported earnings or
revenue grew year-on-year outperform names whose did not?

Last Updated: 2026-09-23 (Wednesday contrarian probe)
Status: PREDICTION COMMITTED, TEST NOT YET RUN
Audience: TARS sessions, Nolan

## Why this question

Nolan read SOFI from how the business was doing. TARS reads only price.
The agenda ranks this as the biggest blind spot.

## Mechanism (stated before the test)

Post-earnings-announcement drift and earnings momentum. Investors react too
little to fundamental news, so a company reporting year-on-year growth keeps
drifting up for weeks to months, and one reporting a decline keeps drifting
down. This is one of the oldest anomalies in the academic literature (Ball &
Brown 1968; Bernard & Thomas 1989). If it holds here, an above-the-200-day
stock whose earnings are falling is a trend running on fumes, and R2 should
skip it.

Why it might NOT show up here: these are 14 heavily followed large caps.
The drift is documented as strongest in small, neglected stocks and has
weakened since the 1990s.

## Data (point-in-time)

- Fundamentals: SEC EDGAR XBRL company facts (data.sec.gov), fetched
  2026-09-23. Every value carries the date it was FILED with the SEC. A
  value becomes usable the trading day AFTER its filing date. Nothing is
  used before the public could see it.
- Growth is computed WITHIN ONE FILING: the latest period in that filing
  against the same period a year earlier, as reported in the same document
  (10-Qs: 3-month periods; 10-Ks: 12-month periods). This avoids
  look-ahead from later restatements.
- Metrics: NetIncomeLoss (earnings) and revenue (first available of
  RevenueFromContractWithCustomerExcludingAssessedTax, Revenues,
  SalesRevenueNet, SalesRevenueGoodsNet). Net income, not EPS, because
  CSCO does not tag diluted EPS after 2010.
- A signal older than 200 calendar days is treated as missing.
- Prices: paper/history/daily_stocks.json, 14 symbols. XBRL coverage runs
  2009 onwards. GOOGL only from 2015, because Alphabet's filer ID starts
  there.
- Survivorship is REAL AND UNFIXED (agenda item 5): all 14 names survived.

## Test design (fixed before the run)

Sample on the FIRST TRADING DAY OF EACH MONTH, not every day, so forward
windows don't overlap and the t-statistics aren't inflated.

On each sample day, the eligible set = names with close > 200-day SMA
(R2 rule 1). Split it into GROWING (latest YoY growth > 0) and NOT GROWING
(<= 0). Forward return = close 21 trading days later / today's close - 1.

Statistic: for each month with at least one name on each side, take the
mean forward return of GROWING minus NOT GROWING. Report the mean of those
monthly spreads in pp and the t-statistic across months.

Tests, and ONLY these (two metrics × one split, to keep the multiple-testing
count honest for agenda item 8):
  T1  net income YoY growth sign
  T2  revenue YoY growth sign

Hurdles (same as every other note):
  1. |t| >= 2 on the full sample
  2. Split sample: 2009-2017 and 2018-2026 both positive
  3. Walk-forward: 9 equal windows, positive in >= 5 of 9
  4. Drop the megacaps (AAPL, MSFT, NVDA, GOOGL, AMZN): still positive

## PREDICTION (committed before the script exists)

T1 (earnings): spread positive but small, +0.2 to +0.6pp per month, t
between 1 and 2. PASSES hurdle 1: NO. I expect the filter to be real in
sign but too weak on 14 heavily followed names to clear |t| >= 2.

T2 (revenue): weaker than T1, near zero, |t| < 1.

What would prove me wrong: T1 with t >= 2 that also passes the split, 5/9
walk-forward and the megacap drop. That would be a genuine candidate for an
R2 filter. A NEGATIVE spread with |t| >= 2 would also prove me wrong, in the
direction nobody expects.

R16 note: if the result contradicts this prediction, R16 trigger (c) is on
for the rest of this session. Nothing from this session gets adopted
either way; this is a Wednesday probe.

## Result

(not yet run)
