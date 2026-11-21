# Intraday Deep Dig — out-of-sample patterns, gaps, expected move, news days

Re-tests the desk-study candidates on data they never saw, and measures the shape of SPY's day.

Last Updated: 2026-10-15
Status: done; desk updated (v4); daily journal loop started
Audience: Nolan, TARS, research swarm

## Overview
- Intraday: 164 days of real SPY 5-minute bars. 133 days (2026-02-23 → 09-01) are OUT-OF-SAMPLE for the 10-15 desk study; 31 days (09-02 → 10-15) are the same days it used. Robinhood has no real 5-min bars before 2026 (it returns interpolated filler), so this is all the real intraday history available.
- Daily: SPY 2006-2026 with weekly VIX. News: FOMC (fomc_dates.json + Oct 28 / Dec 9 2026), CPI and jobs-report dates from the BLS 2026 schedule (Apr-Jul jobs dates estimated as first Fridays).
- Script: `paper/research_scripts/intraday_deep.py`.

## A. The candidates did not survive
| Candidate (from 31 days) | Out-of-sample, 133 days (30-min forward) |
|---|---|
| PDL break → short | **−0.44 pts, 45%, t −1.8. Flipped.** Dead. |
| Equal lows swept & reclaimed → long | −0.20 pts, 47%. Dead. |
| RSI dip-buy (5-min analog) | +0.12 pts, 56%, t 1.6. Weak, and negative in the Sep-Oct period. |
| Close below −2σ VWAP → long | +0.07 pts, 57%, t 2.5. Real-looking but ~$0.04 of option premium: smaller than the spread. |
| OR / PDH / equal-highs breakouts | ±0.1 pts, no edge. |
| Daily trend filter (above 20-day) on the dip-buy | +0.15 vs +0.09 pts. Not a meaningful difference. |
This is what the multiple-testing note predicted: with ~45 tests, a couple look good by luck, and they fall apart on new data. **No intraday chart pattern has shown a reliable direction edge.**

## B. What IS reliable: the shape of the day
- **Range timing:** 42% of the day's high-low range is in by 10:00, 55% by 10:30, 77% by 11:30, 92% by 1:00.
- **Where the extremes print:** the day's high is set in the first 30 minutes on 24% of days and its low on 32%; in the last 30 minutes 17% / 13%; any single midday half hour 1-5%.
- Practical: big directional 0DTE moves are a morning thing. After 11:30 most days only add ~20% more range, while theta keeps charging.

## C. Opening gaps
| Gap size | Fills same day (2026) | 20-year SPY | Usually filled by |
|---|---|---|---|
| < 0.1% | 88% | — | 9:35 |
| 0.1-0.3% | 64% | 72-76% | ~9:50 |
| 0.3-0.6% | 31% | 52-58% | ~10:50 |
| > 0.6% | 21% | 30-38% | ~11:15 |
- Fills have gotten rarer since 2016 (e.g. >1.2% gaps: 37-46% before, 23% after).
- Direction after the gap is ~a coin flip, except big gap-ups (>0.6%) closed above the open 60-62% of the time over 20 years. That's a lean, not a rule.

## D. VIX expected move (20 years)
- SPY's whole day stays inside ±1σ (prior close × VIX/√252) on 65% of days.
- Actual close-to-close moves average 53% (VIX < 15) to 81% (VIX 30+) of what VIX implies. Options are usually priced for more movement than happens, which is the seller's edge and the buyer's headwind.
- When SPY tags the 1σ edge it **closes beyond it 55%** of the time. The band edge is not a reversal point; a tag is slightly more likely to keep going.

## E. News days
| Day type (2026) | Median day range | Median gap | 2-4pm range |
|---|---|---|---|
| Normal | 6.2 pts | 2.6 | 2.5 |
| FOMC (2pm) | **12.1** | 0.9 | **11.6** |
| CPI (8:30am) | 5.7 | 2.7 | 2.4 |
| Jobs report (8:30am) | 5.5 | 3.4 | 2.9 |
- FOMC is the one scheduled event that changes the *intraday* game: about 2× the day range and 4-5× the afternoon range. The first 20-minute reaction reversed by the close on 2 of 5 meetings (Apr, Jul) and continued on 3, so the first move isn't a signal.
- CPI and jobs reports land before the open: the news goes into the gap, and the rest of the day ran normal or quieter.
- 20 years: FOMC days range 1.20% vs 0.95% on other days; the day after is also wide (1.21%).

## What I learned
1. Reading a chart for *direction* hasn't produced a reliable edge for me intraday, and I've now tested it in and out of sample. I'll keep saying that plainly instead of dressing patterns up as signals.
2. Reading a chart for *structure* works: how big the day probably is, how much is left, whether a gap is likely to fill, which days are news days. That's what decides 0DTE strike, size and timing, and it's where Nolan's results already come from (exits and size, not calls).
3. "Breaking points": a tag of the expected-move edge more often keeps going (55%) than reverses, and big gaps mostly don't fill. Fading extremes isn't free money.

## Desk v4
Context now shows: news today, opening gap with fill odds, range so far vs typical and how much is usually done by now, expected move left (1σ from the ticket's ATM 0DTE IV, with dashed ±1σ lines), and the typical 15-min move. Ask TARS knows all of this.
