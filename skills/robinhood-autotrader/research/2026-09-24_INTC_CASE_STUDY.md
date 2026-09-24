# Case Study: How INTC Went From ~$29 to ~$124 With Negative Earnings

One-line: RESEARCH_AGENDA item 17. What did the market price in, which days
did the move actually happen on, and could anything have told TARS in advance?

Last Updated: 2026-09-24
Status: PREDICTION COMMITTED, TEST NOT YET RUN
Audience: Nolan, TARS sessions

## Method (fixed before the run)

1. Price anatomy: daily INTC closes (Yahoo, adjusted), from the 52-week low
   to the high. What share of the total log gain came from the 5 and the
   10 biggest up-days? What share from days INTC moved with SMH vs on its own?
2. R2 test: the first close above the 200-day SMA after the low, and the
   share of the low-to-high log move captured from that close to the high
   (and to today).
3. Events: a dated timeline from sources (sub-agent, checked where
   possible), matched to the biggest days.
4. Earnings: point-in-time net income from SEC filings over the period.

## PREDICTION

- The 5 biggest up-days deliver more than 40% of the total log gain; the
  10 biggest, more than 60%. The move was a handful of event days.
- Those days line up with deal news (government stake, Nvidia investment,
  foundry customers), not with earnings reports.
- R2's 200-day cross came within 1-3 months of the low and captured 50-75%
  of the low-to-high log move.
- Nothing in TARS's toolkit would have predicted the deals themselves.
  The honest answer to "what would have told TARS in advance" is: nothing
  about the news, but the trend rule would have caught most of the move
  afterwards.

## Result

(not yet run)
