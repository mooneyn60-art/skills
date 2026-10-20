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
- Connections tests (2026-10-16, `predict_lab2.py`, `setup_x_score.py`):
  - **Cross-market inputs don't help.** Adding 14-stock breadth, tech/bank/oil relative moves, the 10y-2y yield curve and put/call to the day model did not improve the tails: v2 ≥0.60 days were +0.08%/+0.18% vs v1-lite's +0.50%/+0.64%. Simple wins.
  - **Next hour from 10:30: no edge.** A 9-feature intraday model with the day score had no edge in either half.
  - **Dip-buy × day score:** still −0.07 pts at score ≥0.50 (n=106).
  - **Gap-up × day score (20y proxy):** score ≥0.55, +0.24%/+0.06% (n=118/212). Weak.
  - All linked in CONNECTIONS.md.
- What moves SPY (2026-10-16, `spy_drivers.py`; R² = share of SPY's daily move explained, 2006-15 → 2016-26):
  - **Mega-caps.** The 5 mega-caps' average move went 59% → 72%. MSFT 41→57%, AAPL 31→54%, GOOGL 31→50%. Old-economy names lost pull: XOM 55→23%, T 47→15%, PFE 41→17%.
  - **VIX.** VIX change explains ~53% in both decades.
  - **The open.** The DAX opening gap explains 19→31% of SPY's gap; Asia 8-18%.
  - **No influence.** Yield-curve change and yesterday's SPY move: R² ≈ 0.
  - **Fed days.** Only ~6% bigger day moves (2016-26), but the 2-4pm range is ~4.6×.
  - **Takeaway.** Watch the giants and VIX intraday. Watch Europe for the open.
- Overnight slot (2026-10-16, `overnight_slot.py`, 2016-26; options repriced with that night's VIX as IV and the real calendar gap):
  - **Short-dated options give the edge back.** Buying at the close and selling at the open loses with 1DTE calls (−22.6%/night, win 28%) and 7DTE (−5.7%). Time decay plus the volatility premium eat the small overnight drift. My first pass, with a fixed 10% IV, wrongly showed +24%/night (see SELF_REVIEW).
  - **Strong nights.** On overnight-model nights with p≥0.60 (n=318, ~32/yr): SPY shares +0.12%/night (up 61%); 30DTE ATM calls +0.85%/night (win 54%). Small but positive.
  - **Takeaway.** The overnight edge belongs to shares, or to slow 30-day options on strong nights only.
- BE earnings (2026-10-16): the last 4 reports gapped UP at the open +14.1%, +12.2%, +22.2%, +10.0% (closes +18.0%, +4.7%, +27.2%, −1.9%). The 10/23 straddle prices ±12.3% (IV 112%). The stop at 211.85 is 4.3% below 221.34, so a miss of the same size would open ~8% under the stop. Holding through earnings is a choice to make before 10/22's close, not after.
- Crypto (2026-10-20, `crypto_lab.py`, full write-up in CRYPTO.md):
  - **Cost.** Robinhood's crypto spread is ~1.9% round trip (market-maker routing).
  - **Returns have shrunk.** BTC buy & hold +141%/yr 2015-20 vs +19%/yr 2021-26 (DD −77%).
  - **Slow vs fast rules.** The 200-day filter cuts drawdowns every time but trails buy & hold on BTC. Fast rules lose to the spread (BTC above-20d −24%/yr in 2021-26). Dip-buying after −5% faded (63% → 48% next-day up).
  - **Off-hours.** No off-hours drift: ≈0 bp/h in both US and closed hours.
  - **Correlation.** BTC-SPY correlation rose to 0.42-0.56.
  - **Verdict.** No short-term crypto edge after cost. Only a small slow trend-filtered hold is defensible.
- IBIT (2026-10-20, `ibit_session.py`, `ibit_dayscore.py`): crypto via IBIT/ETHA options costs ~2% of premium vs 1.9% round trip on spot.
  - **Direction: no edge.** BTC's off-hours move doesn't predict the US session (flat in the recent half), and a 12-feature walk-forward day score has no edge in either half.
  - **Size: real.** The overnight range predicts the session range (corr 0.40; quiet/normal/wild night → 2.44/2.71/3.43%).
- Crypto round 2 (2026-10-20, `crypto_lab2.py`):
  - **Holds.** The monthly trend rule cut max drawdown in all 16 BTC/ETH cases and beat holding in 2021-26 (BTC L=12 +25.9 vs +17.1%/yr, DD −41 vs −73%), but lagged in 2016-20's bull run. Run it on IBIT shares (0.02% spread).
  - **Fails.** BTC/ETH rotation; SPY's trend as a BTC filter.
  - **Weak or no effect.** Weekend drift is just normal drift. Fed days lean positive (t ≈ 1).
- Small coins (2026-10-20, `alt_basket.py`, 40 2021-era Coinbase alts): bought Jan 2022, median −94% (25/32 down 80%+). Bought Jan 2023 near the bottom, median −58%. 0 of 33 went 5×, 0 beat BTC (+395%), 7/40 delisted. "Cheap coins that could jump" lost to plain BTC.
- **Crypto 2h flips (10/20, crypto_flips.py, 3y hourly, halves):** BTC reaches +1.9% (the RH spot round-trip cost) within 2h on only 1.8–3.5% of hours. Dip, breakout, RSI<25 and momentum setups have gross edges within ±10bp. After RH spot cost each loses ~190bp per trade. Don't flip RH spot crypto; use IBIT/ETHA in market hours if anything.
