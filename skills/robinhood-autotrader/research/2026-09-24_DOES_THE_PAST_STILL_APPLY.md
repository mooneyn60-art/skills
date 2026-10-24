# Does the Past Still Apply? Pattern Decay and TARS's Live Rules

One-line: RESEARCH_AGENDA item 20. How fast do market patterns decay after
discovery, and which of TARS's live rules rest on evidence most at risk of
being out of date?

Last Updated: 2026-09-24
Status: DONE. Prediction committed first (cece5f9); mostly held.
Audience: Nolan, TARS sessions

## Data test (fixed before the run)

The rule everything rests on is R2's 200-day gate. Test it era by era on
paper/history/daily_stocks.json (14 names + SPY, 2006-2026), sampled on the
first trading day of each month (non-overlapping 21-day forward returns):
  D1  per stock: forward 21-day return when the close is ABOVE its 200-day
      minus when BELOW; per era (2007-2011, 2012-2016, 2017-2021,
      2022-2026), mean spread and t across months.
  D2  the same for SPY alone, plus the forward 21-day return volatility
      above vs below (the "avoid the crashes" half of the argument).

## PREDICTION

- D1: the above-minus-below spread is small and inconsistent across eras,
  |t| < 2 in most eras. A trend gate does not pick better stocks month to
  month on these names.
- D2: SPY's forward volatility is clearly HIGHER below the 200-day in every
  era (ratio > 1.3). Its forward RETURN is not reliably lower.
- Interpretation I expect: R2's value, if any, is avoiding high-volatility
  periods rather than adding return, and that part is the least likely to
  decay because it comes from volatility clustering, one of the most
  robust facts in finance.

## Answer first

- PATTERNS DO DECAY, AND FAST. Across 97 published return predictors,
  returns were 26% lower after the original sample ended and 58% lower
  after publication (McLean & Pontiff 2016). 65% of 452 published
  anomalies fail to replicate once tiny illiquid stocks are handled
  properly (Hou, Xue & Zhang 2020). What decays fastest: effects with the
  biggest in-sample t-stats, and effects living in illiquid corners.
- THE 200-DAY RULE ON OUR DATA: the "trend picks better stocks" part is
  mostly absent and inconsistent across eras. The "trend avoids volatile
  periods" part is robust in every era. It comes from volatility
  clustering, one of the most durable facts in finance.
- WHICH TARS RULES ARE MOST AT RISK (interpretation, ranked):
  1. R15 (buy weakness when VIX >= 25). HIGHEST. Its stressed half can't be
     re-tested since 2022, reversal effects are documented to weaken as
     markets get more liquid, and its t = 8.46 came from DAILY overlapping
     observations, which overstate t. Treat R15's first live firings as the
     real test (R15 already says so).
  2. R4's exits (8% stop, 20% trail): chosen on in-sample data and never
     walk-forwarded in the regime they run in. Item 17 showed the trail's
     cost on a real winner.
  3. R2's 200-day gate: the least at risk, but for a different reason than
     it's usually sold on. Expect it to cut volatility and drawdowns, not
     to add return.
  4. Any options-SELLING idea: a Chicago Fed paper (2025) reports the
     variance risk premium fell around 2010, which matches put-writing
     trailing the S&P since 2007 in item 15.

## Result

Script: paper/test_200d_decay.py. paper/history/daily_stocks.json, first
trading day of each month, forward 21 trading days (non-overlapping).

    D1  14 stocks, above-minus-below 200-day forward return
        2007-2011  53 months  -0.38pp  t=-0.33
        2012-2016  60 months  -0.15pp  t=-0.23
        2017-2021  57 months  +2.15pp  t=+2.98
        2022-2026  55 months  +0.28pp  t=+0.30

    D2  SPY alone      above 200-day            below 200-day          vol ratio
        2007-2011   n=35 fwd +0.30% vol 15.9%   n=25 fwd -0.63% vol 31.0%   1.96
        2012-2016   n=54 fwd +0.82% vol 11.5%   n= 6 fwd +2.77% vol 17.3%   1.50
        2017-2021   n=53 fwd +0.64% vol 14.1%   n= 7 fwd +6.87% vol 18.2%   1.29
        2022-2026   n=43 fwd +0.38% vol 13.2%   n=13 fwd +3.05% vol 24.1%   1.83

In 3 of 4 eras, SPY did BETTER in the month after closing below its
200-day than after closing above it, on small samples (6-13 months). That
is the rebound after a sell-off, which a trend gate sits out.

## Scored against the prediction

    D1 small and inconsistent, |t|<2 in most eras: RIGHT (3 of 4; 2017-2021 is the exception)
    D2 vol ratio >1.3 in every era: 3 of 4; 2017-2021 at 1.29, WRONG by a hair
    D2 forward return not reliably lower below: RIGHT, and it was higher in 3 of 4 eras

## Literature (sub-agent; items it marked as not checked against the primary source are flagged)

- McLean & Pontiff (2016), JF: -26% out of sample, -58% post-publication;
  larger declines for bigger in-sample effects. https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
- Hou, Xue & Zhang (2020), RFS: 65% of 452 fail at |t| < 1.96; 82% at
  |t| < 2.78. Microcaps are ~60% of stocks but ~3% of market value.
  https://academic.oup.com/rfs/article-abstract/33/5/2019/5236964
- Harvey, Liu & Zhu (2016), RFS: after hundreds of tests, a new factor
  should clear |t| > 3.0. (Sub-agent: "9 of 313 survive"; not checked.)
  This is the hurdle agenda item 8 should apply to R15 and every rule here.
- Faber (2007) 200-day timing, 1972-2005: CAGR 11.7%, max DD 9.5%.
  Out-of-sample update 2006-2025 (secondary source): CAGR 6.05%, max DD
  11.7%. The return fell sharply, the drawdown control held. Same pattern
  as D2 above. https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf
- Trend-following industry (CFM): "effectively flat or negative" for about
  15 years, rescued by 2014 and 2020. https://www.cfm.com/steady-trends-the-reality-of-cta-return-dispersion/
- Chicago Fed WP 2025-17: structural break around 2010, after which
  delta-hedged option strategy alphas converge towards zero.
  https://www.chicagofed.org/-/media/publications/working-papers/2025/wp2025-17.pdf
- Short-term reversal: described as having weakened sharply as liquidity
  improved (secondary wording, not checked against the primary PDFs).
