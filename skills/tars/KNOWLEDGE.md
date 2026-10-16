# TARS — What I've Learned

Tested findings with numbers. Use these over trading folklore. Sources are in skills/robinhood-autotrader/research/.

Last Updated: 2026-10-15
Status: living
Audience: TARS

## Overview
~650 ideas tested since Sept 2026. With that many tests, luck alone makes ~30 look good at |t| ≥ 2, so the bar for a real edge is out-of-sample proof and |t| ≥ 3.

## What doesn't work (don't sell these)
- Candlestick patterns, MACD, EMA crosses, Bollinger squeezes: no forward edge on 20 years of SPY / large caps.
- Fibonacci levels: no better than random levels (tested twice: 20 years daily and 31 days of 1-minute).
- Intraday chart patterns for direction (FVGs, VWAP crosses, liquidity-pool breaks, OR breaks): no edge; the 31-day "winners" failed out of sample on 133 days.
- Strike pinning in SPY: none. First half hour → last half hour: weak (t 0.7).
- Asia/Europe overnight predict the gap, not SPY's open-to-close.

- Spaced review 2026-10-16: the three lines above re-checked against tonight's desk work (the pool test found distance odds, not a break edge), still hold.

## What does hold up
- Shape of the day: 42% of the range by 10:00, 77% by 11:30; highs/lows set in the first 30 min (24%/32%) or last 30 (17%/13%).
- Gap fill odds: < 0.1% 88%; 0.1-0.3% 64-76%; 0.3-0.6% 31-58%; > 0.6% 21-38%. Fewer fills since 2016.
- VIX expected move: SPY stays inside ±1σ ~65% of days; realized ≈ 0.5-0.8× implied. Tagging the edge continues 55%.
- FOMC: 2× day range, ~4.6× 2-4pm range; first move unreliable. CPI/jobs news lands in the gap.
- 0DTE buyers lose on average (~60% of it costs); sellers earn about the market's return with less risk (CBOE PUT/BXM).
- Momentum (12-1 month) and the 200-day filter: modest, the stock sleeve's basis.
- Which liquidity pool gets hit first: the nearer one, in proportion to distance (random-walk odds). 30 days SPY 1-min, 1,668 checks: called 10/30/50/71/90% up → actual 9/27/52/69/88% (Brier 0.165 vs 0.25). Trend, MACD, VWAP side, RSI add nothing. Script: paper/research_scripts/pool_odds_test.js.
- S2 (dip below VWAP −2σ/RSI<30, then a turn) with its live exits (VWAP / new low / 60 min): −0.11 SPY pts/trade, 39% wins on 95 out-of-sample trades (Feb-Aug 2026); EMA9 ≥ EMA21 at the signal: 8% wins. Not an edge as traded.
- Leans worth tracking (not rules): big gap-ups close above the open ~60% (20y); Nikkei −2% days → SPY open-to-close up 57-59%.

## Data facts
- Robinhood has no real intraday bars before 2026 (5-minute requests return interpolated filler); real minute history grows only by saving bars daily.
- Option minute historicals are mostly interpolated; rebuild option prices from real SPY bars + Black-Scholes when needed.
- Yahoo's chart API works with a browser user-agent; stooq is blocked; Robinhood has no foreign indexes.
- Option IV is annualised on calendar time: 1σ move left = price × IV × √(minutes left / 525,600).

## Nolan-specific
- Before 10:30 ET: lost on 5/5 days. After: green 5/6. Holds of 2-5 min worst, 5-15 min best. 29% wins, +23%/−12% payoff (needs ~35%).
- Godmode-style structure signals (2026-10-16, `paper/research_scripts/godmode_test.py`): rebuilt BOS / CHoCH / liquidity sweep / sweep-then-CHoCH, without repainting, and tested on 164 days of SPY 5-min bars (10:30-14:30, stop at structure, 2R target, 60 min, after costs). BOS −0.05 pts (47% wins, n=241 OOS). CHoCH +0.01 (48%, n=257). Sweep −0.05 (34%, n=621). Sweep+CHoCH: +0.50 and 60% on n=20 in-sample, then −0.21 and 37% on n=81 out-of-sample. No edge. Paid "insider" indicators are this, plus cherry-picked screenshots. Kept as a map-only desk layer.
- Market lab (2026-10-16, `paper/research_scripts/market_lab.py`, 20y SPY daily + 164 days of 5-min bars; each split into two halves):
  - **Holds up.** Monthly-expiry Fridays: −0.21% close-to-close in BOTH 2006-15 (t −2.0) and 2016-26 (t −2.5, up only 38%). Gap fill depends on size: 0.1-0.3% gaps close the same day 71-77% of the time; gaps over 1% close only 24% (2016-26). They mostly run, which fits S1. Most of SPY's return comes overnight (2016-26 overnight +0.029%/day t 2.1 vs day session +0.020% t 1.3).
  - **No edge.** Intraday momentum (first 30 min → last 30 min) flips sign between halves. ORB30 −0.09. Squeeze release −0.13. Close-location buying pressure −0.03. Morning variance-ratio regime: noise.
  - **Not testable.** The "price pins to big strikes on expiry" claim: only 6 expiry days in the intraday sample, and a random walk drifts away from any fixed strike anyway. Removed from the desk.
- Market lab round 2 (same script, sections 11-19):
  - **Holds up.**
    - VIX sets the size of the day: average range 0.66% under 15, 1.01% at 15-20, 1.52% at 20-30, 2.72% at 30+ (2016-26; 2006-15 the same shape).
    - VIX also sets the lean: under 15, +0.13%/day, up 59% (t 7.6; 2006-15 t 4.8); 30+, −0.24%, up 44%.
    - After a <−1% day the next day bounces +0.16 to +0.22% (both halves, t 1.4-1.9). After a >+1% day it gives back 0.10-0.15%.
  - **No edge.** Day of week (flips between decades), time of day (half-hour means flip IS/OOS), last hour following the day, lunch reversal, fading VWAP ±1σ (−0.06 OOS), the week after expiry.
  - **On the desk.** The live "Edge board" panel shows these with VIX from the Robinhood index quote.
- Prediction engine v1 (2026-10-16, `predict_lab.py`, `day_model.json`; walk-forward, each year predicted only from earlier years):
  - **Accuracy.** Logistic and boosted models on 15 pre-open features (gap, past returns, distance from the 20-day average, VIX, Asia, DAX gap, put/call, calendar) don't beat "always up" (54%).
  - **The tails do sort days.** A lite 10-feature logit day score:
    - p≥0.60: up 65-67%, +0.50%/+0.64% open→close (2011-18 n=12, 2019-26 n=34; rare).
    - p<0.45: up 46%, −0.06% in both halves.
    - The full logit at p≥0.60 averaged +0.10/+0.21%.
  - **Overnight.** Logit p≥0.60 nights: up 58-61%, +0.10% (both halves).
  - **Strongest weights.** Above the 20-day average → lower score. Expiry Friday → lower. Gap up → higher. Big prior-day intraday gain → lower.
  - **On the desk.** Live as "Model day score" on the Edge board. 10/16 scored 44 (weak) and SPY fell from 773 to ~766.
