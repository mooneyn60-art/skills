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

## What does hold up
- Shape of the day: 42% of the range by 10:00, 77% by 11:30; highs/lows set in the first 30 min (24%/32%) or last 30 (17%/13%).
- Gap fill odds: < 0.1% 88%; 0.1-0.3% 64-76%; 0.3-0.6% 31-58%; > 0.6% 21-38%. Fewer fills since 2016.
- VIX expected move: SPY stays inside ±1σ ~65% of days; realized ≈ 0.5-0.8× implied. Tagging the edge continues 55%.
- FOMC: 2× day range, ~4.6× 2-4pm range; first move unreliable. CPI/jobs news lands in the gap.
- 0DTE buyers lose on average (~60% of it costs); sellers earn about the market's return with less risk (CBOE PUT/BXM).
- Momentum (12-1 month) and the 200-day filter: modest, the stock sleeve's basis.
- Leans worth tracking (not rules): big gap-ups close above the open ~60% (20y); Nikkei −2% days → SPY open-to-close up 57-59%.

## Data facts
- Robinhood has no real intraday bars before 2026 (5-minute requests return interpolated filler); real minute history grows only by saving bars daily.
- Option minute historicals are mostly interpolated; rebuild option prices from real SPY bars + Black-Scholes when needed.
- Yahoo's chart API works with a browser user-agent; stooq is blocked; Robinhood has no foreign indexes.
- Option IV is annualised on calendar time: 1σ move left = price × IV × √(minutes left / 525,600).

## Nolan-specific
- Before 10:30 ET: lost on 5/5 days. After: green 5/6. Holds of 2-5 min worst, 5-15 min best. 29% wins, +23%/−12% payoff (needs ~35%).
