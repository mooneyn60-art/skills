# Case Study: How INTC Went From ~$29 to ~$124 With Negative Earnings

One-line: RESEARCH_AGENDA item 17. What did the market price in, which days
did the move actually happen on, and could anything have told TARS in advance?

Last Updated: 2026-09-24
Status: DONE. Prediction committed first (3256ca9); the trend-rule part was too pessimistic.
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

## Answer first

- THE MOVE WAS BIGGER THAN "$29 TO $124". The adjusted low was $19.31 on
  2025-08-01 and the high $140.94 on 2026-06-22: 7.3x in 222 trading days.
  $29 is where it was in late September 2025, right after the Nvidia deal.
- WHAT THE MARKET PRICED IN (facts): a chain of outside money and
  customers for a strategic asset. SoftBank $2B (Aug 18, 2025); the US
  government taking ~10% at $20.47 (Aug 22); Nvidia $5B plus a
  co-development deal (Sep 18, +22.8%, Intel's best day since 1987); the
  first 18A product shipping (Jan 2026); Tesla/Terafab choosing 14A (Apr
  2026); results beating estimates every quarter from Q3 2025 (Q1 2026:
  +23.6% in a day); a reported, never jointly confirmed Apple foundry
  deal (Jun 2026).
- WHY "NEGATIVE EARNINGS" MISLEADS HERE: adjusted (non-GAAP) earnings beat
  estimates every quarter. The GAAP losses were largely restructuring,
  impairments and, in Q2 2026, a $12.5B mark-to-market charge on the
  government's warrant shares. The stock going UP made the reported loss
  BIGGER. The market was pricing the foundry's future, not trailing GAAP
  earnings. (This also partly explains item 1's null result: GAAP net
  income growth is a noisy signal.)
- NARRATIVE (interpretation, from commentators): a national-security
  premium ("the West's insurance against TSMC"), AI data-center CPU
  demand, and a turnaround under CEO Lip-Bu Tan. Skeptics note few
  confirmed outside foundry customers and price-to-sales around 8x
  against a 3-year average near 3x.
- COULD TARS HAVE KNOWN IN ADVANCE? Not the news. Every catalyst was a
  negotiated deal announced without warning. But the plain trend rule
  would have caught it: INTC closed above its 200-day 7 trading days
  after the low and NEVER closed below it again (282 of 282 closes). An R2
  entry at $21.81 on 2025-08-12 was positioned before every catalyst
  above.
- THE CATCH IS THE EXIT, NOT THE ENTRY: R4's 20% trail would have sold on
  2026-01-26 at $42.49 (+95%) after the -17% guidance drop, about a third
  of the full log move. R2 allowed re-entry the next day, since the trend
  never broke. Nolan's own INTC position (entered 2026-09-16 at ~$101.70)
  came in after most of the move.

## Result

Script: paper/test_intc_case.py (prices from book_daily.json, Yahoo adjusted;
net income from SEC EDGAR). Timeline: sub-agent from CNBC, Intel and Nvidia
newsrooms and others (links below). I checked its dates and figures against
the price data and SEC filings where they overlap, and they matched.

    low 2025-08-01 $19.31 -> high 2026-06-22 $140.94, 7.30x, log gain 1.988, 222 days
    top  5 up-days: 39.4% of the log gain
    top 10 up-days: 66.2%
    top 20 up-days: 107.5% (the rest of the days net slightly negative)
    SMH's summed log move over the same days: 0.860, less than half of INTC's 1.988

    10 biggest up-days                   what happened (sub-agent timeline)
    2026-04-24 +23.6%  SMH +5.1%         Q1 2026 results, big beat (GAAP loss -$3.7B)
    2025-09-18 +22.8%  SMH +3.8%         Nvidia $5B investment + x86/NVLink deal
    2026-05-08 +14.0%  SMH +4.9%         May run to record high (Apple/Terafab reports)
    2026-05-05 +12.9%  SMH +3.1%         same run
    2026-04-29 +12.1%  SMH +1.7%         post-earnings / Terafab 14A (reported Apr 22-23)
    2026-01-21 +11.7%  SMH +3.0%         run-up into Q4 results (reversed -17% on Jan 23)
    2026-04-08 +11.4%  SMH +5.8%         Intel joins Terafab (~Apr 7); strong sector day
    2026-06-08 +11.2%  SMH +5.0%         Computex/Foxconn partnership week
    2026-01-28 +11.0%  SMH +2.3%         not identified
    2026-01-09 +10.8%  SMH +2.7%         CES week, first 18A product (Panther Lake)

    R2: first close above the 200-day 2025-08-12 at $21.81, 7 trading days after the low;
        93.9% of the low->high log move came after it; 282/282 closes stayed above.
    R4 replay (supplementary, not pre-registered, daily closes): 8% stop,
        breakeven at +8%, 20% trail -> exit 2026-01-26 at $42.49 (highest close $54.32).

    INTC net income as filed (SEC): Q2'25 -2.92B, Q3'25 +4.06B, FY25 -0.27B,
    Q1'26 -3.73B, Q2'26 -11.03B.

## Scored against the prediction

    top 5 days >40%: 39.4%, WRONG by a hair. Top 10 >60%: 66.2%, RIGHT.
    big days = deal news, not earnings: PARTLY WRONG. The #1 day was an
        earnings report; #2 was a deal. Earnings beats mattered as much as deals.
    R2 cross within 1-3 months, capturing 50-75%: WRONG, and in TARS's
        favour: 7 trading days, 93.9%.
    nothing predicts the deals; the trend rule catches the move: RIGHT.

## Lessons for TARS (interpretation)

1. Trend-following did exactly what it's for on the biggest winner of the
   year. The entry wasn't the weak point.
2. The 20% trail is where a move like this leaks. It sold at +95% on a
   one-day earnings shock inside an intact uptrend. This is one case, not
   evidence (R14.2): R15_EXIT_SOLVED and the TARS-2 notes already weigh the
   trail's cost against its crash protection. Flag it for the next exit
   review rather than change anything.
3. GAAP earnings can point the wrong way for a company whose accounts are
   full of one-off and mark-to-market items. If fundamentals are ever
   revisited (item 1's untested variants), use adjusted figures or
   revenue, not GAAP net income.

## Sources (via sub-agent)

CNBC on the government stake (2025-08-22), the Nvidia investment (2025-09-18),
SoftBank (2025-08-18), Q4 2025 (2026-01-23), Q1 2026 (2026-04-23), the Apple
claim (2026-06-18); Intel newsroom (government agreement, SoftBank, $20B
offering 2026-08-10); NVIDIA newsroom; TrendForce (Terafab 14A, 2026-04-23);
Bloomberg (2026-05-12); tikr and Substack pieces on the Q1 and Q2 2026 GAAP
items. Full links are in the session transcript summary; the
Apple deal and the June 2026 CHIPS grant amounts remain unverified.
