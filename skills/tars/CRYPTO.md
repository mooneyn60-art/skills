# TARS Crypto Book — how crypto works, and what tested out

What TARS knows about crypto: the mechanics, and the tested results with numbers. General knowledge is labelled as such; "tested" means TARS ran it on real data.

Last Updated: 2026-10-20
Status: research (no live crypto trading; needs Nolan's words and a written rule first)
Audience: TARS, Nolan

## Overview
Nolan (2026-10-20): "do deep research I want you to be just as versed in crypto as you are stocks and that opens up money making at anytime whil market closed". Data: Coinbase daily candles (BTC 2015-, ETH 2016-, SOL/DOGE 2021-) and 3 years of hourly BTC/ETH (`paper/history/crypto/`, `research_scripts/fetch_crypto.py`). Tests: `research_scripts/crypto_lab.py`, each in two halves.

## How it trades (mechanics)
- **Hours.** 24/7/365, no open or close. A "day" here is the UTC midnight close.
- **Robinhood's cost: about 1.9% per round trip.** Live quote 2026-10-20, account 731951265, "Market Maker Routing": BTC bid 81,542 / ask 83,080; ETH, SOL and DOGE all ~1.9%. That's ~0.95% each way, roughly 100× SPY's cost. **This one fact rules out short-term trading.**
- **Stops.** Robinhood crypto has no stop-market. Stop-limits can be skipped in a fast drop, including at 3am. Protection is weaker than on stocks.
- **Volatility.** BTC realized ~57-76%/yr, ETH 71-112%, SOL/DOGE 80-112% (tested), vs SPY ~15-18%. Same dollars, 4-6× the swings.
- **Drawdowns are normal.** Every coin fell 76-96% from a peak at least once in the sample (tested). Size for that.
- **General knowledge, not tested here.** The BTC "halving" cycle (~every 4 years) is often credited for the big cycles: only 3-4 cycles exist, too few to test. Spot ETFs (2024) tied BTC more closely to US markets.

## What tested out (BTC/ETH/SOL/DOGE, after Robinhood's 1.9% round trip)
- **The glory days are over.** BTC buy & hold: +141%/yr in 2015-20 → **+19%/yr in 2021-26** (max drawdown −77%). ETH: +268%/yr → **−1.5%/yr** (−79%).
- **Slow trend filters = drawdown insurance, not extra return.** Holding only above the 200-day average cut the max drawdown every time: BTC −84→−73% and −77→−69%; ETH −94→−84% and −79→−42%. But it trailed buy & hold on BTC in both halves (125 vs 141%; 9.6 vs 19.4%). It helped ETH in 2021-26 (+11.7% vs −1.5%).
- **Fast rules are killed by cost.** Above-20-day-average: BTC 2021-26 −24%/yr (244 trades); 30-day momentum −6%/yr. Every rule with 100+ trades lost in the recent half.
- **20-day breakout:** strong on SOL/DOGE recently (+53%, +34%/yr), weak on BTC/ETH (−1%, −8%). Inconsistent: not an edge.
- **Buying the dip after a −5% day:** 2015-20 next day +0.83%, up 63%. 2021-26 +0.32%, up 48%. **Faded away.**
- **Day of week: noise** (signs flip between halves).
- **"Make money while the stock market is closed": no.** BTC hourly 3y: US-hours vs closed-hours drift +0.94 vs +1.00 bp/h (first half), +0.08 vs +0.04 (second). Crypto doesn't earn more off-hours, and both are ~0 lately.
- **No longer a hedge.** BTC-SPY daily correlation 0.07 (2018) → 0.42-0.56 (2022-26). It mostly falls when stocks fall.
- **Volatility targeting** (40%/yr): cut BTC's drawdown −84→−62% and −77→−65%; Sharpe mixed (1.57→1.66, 0.60→0.52).

## What this means for TARS
1. Never day-trade crypto on Robinhood: the 1.9% spread beats every short-term rule we tested.
2. If Nolan wants crypto, the only defensible shape is a **small, slow position**: BTC (or BTC+ETH), held only above its 200-day average, sized so a 70% drop is survivable, checked weekly, not hourly.
3. Crypto does not add a 24/7 money machine: off-hours drift ≈ 0, and it now moves with stocks.

## Who actually makes money in crypto (web research 2026-10-20; sources noted, figures checked only as far as said)
- **Most retail buyers lose.** A BIS working paper (2022, updated 2023), using app data from 95 countries 2015-22, estimated 73-81% of retail bitcoin buyers lost money. The median lost about half (modeled on $100 a month of buying). Most bought after BTC passed $20k; large holders were selling while small buyers bought.
- **Leveraged day traders.** Most lose. Academic day-trading studies (Brazil: ~97% of persistent day traders lose; Taiwan: <1% consistently profitable) are cited widely but were seen only secondhand here. Liquidation days wipe out billions (e.g. ~$19B on 2025-10-10, per CoinDesk via a compilation).
- **What the winners do:**
  - **Market makers and exchanges earn the spread.** Robinhood's ~1.9% is that income.
  - **Basis / funding traders** hold spot and short the perpetual to collect funding, delta-neutral, often with 20-50× leverage on a thin spread. The funding can flip negative. It needs futures/perps, which Robinhood's tools here don't offer.
  - **Early long-term holders** sat through 80-90% drawdowns. The ones you hear about are the survivors.
  - **Insiders and early token allocations** are not available to us.
- **Trend following.** Academic papers find time-series momentum in crypto. One large study says it largely disappeared after BTC futures launched (2017). Long-only versions held up better than long-short. That matches TARS's test: trend rules worked 2015-20 and failed after cost in 2021-26.
- **Takeaway for Nolan.** The big crypto winners are mostly the spread-takers, the funding collectors and the early holders who survived, not the chart traders. From a Robinhood account, the realistic edge is the slow one: a small BTC/ETH position held through a trend filter, never day-traded.

## Options-style crypto: IBIT / ETHA options (2026-10-20)
- **Costs.** Nolan wants crypto traded "more like options then hold". The cheap route is options on the spot ETFs, not Robinhood spot crypto. IBIT (BTC ETF) shares: spread 1¢ on $46.60 (0.02%). IBIT 10/30 47C: 0.88/0.90 (2.2% of premium, ~$89 a contract), IV 34%, open interest 35k. ETHA similar on shares. Stop-market works on the options, in market hours.
- **Gap risk.** BTC trades 24/7 but IBIT only in US hours. The night or weekend move arrives as a gap at the open, and a stop can't stop it.
- **Tested** (`ibit_session.py`, 3y hourly BTC): does BTC's move while US markets are closed (20:00→13:30 UTC) predict the US-session move (the IBIT-option day)? First half there were hints (after a >2% overnight drop the session was +0.76%, t 2.1), but **every bucket is flat in the second half** (−0.23% to +0.02%, |t| < 1). No edge: the setup doesn't hold.
- **Next tests:** apply the SPY tools to IBIT (VIX/IV regime, gap size, day score built on BTC's overnight move) before any rule.
- **IBIT day score** (`ibit_dayscore.py`; 781 sessions, 512 walk-forward out-of-sample; logit on overnight BTC move, ETH vs BTC, overnight range, BTC 1/5/20-day returns, distance to 20/200-day averages, 7-day vol, SPY's prior day, VIX, weekday):
  - **Direction: no edge.** High-score sessions: −0.05% then −0.32%, up 53% / 44%. Low-score: +0.27% then −0.20%. The tails don't sort days, unlike SPY's day score.
  - **Size: real.** The overnight range predicts the session's range (corr 0.40): after a quiet night (<2.1% range) BTC's US-session range averaged 2.44%, normal 2.71%, wild (>3.3%) 3.43%. An IBIT session swings ~2.5-3.5%, 2.5-3.5× SPY's ~1% day. Use it to size stops and premium, not to pick direction.

## Round 2: slow ideas (`crypto_lab2.py`, 2026-10-20; halves 2016-20 / 2021-26; 0.95%/side on every switch)
- **Monthly trend rule** (hold next month only if the last L months were up). Max drawdown lower in all 16 cases: BTC −75 → −41…−67%; ETH −90 → −55…−86% and −77 → −51…−72%.
  - Recent half: it beat holding with L=1 (BTC 22.6 vs 17.1%/yr; ETH 18.2 vs 11.2) and L=12 (BTC 25.9 vs 17.1, maxDD −41 vs −73).
  - 2016-20 bull years: it lagged (BTC 73-121 vs 134%/yr).
  - **Verdict: it trades some upside for much smaller crashes.** The one consistent, positive result in crypto.
- **BTC/ETH rotation** (stronger 3-month return): 170 / 18.4%/yr with −90 / −82% max drawdown. No better than holding BTC: fails.
- **Weekends** (Fri 20:00 → Mon 13:30 UTC): +0.29% / +0.38%, up 56% / 62% (n 75/81). That's about BTC's normal drift for 3 days, not a special weekend effect. Average size 2-2.7%, the gap an IBIT holder carries.
- **Fed days:** BTC +0.85% / +0.44% on FOMC days vs +0.30 / +0.09 otherwise (n 39/46, t ≈ 1). Same sign in both halves, weak: a lean, not a trade.
- **SPY's trend as a BTC filter:** helped in 2016-20 (+0.57 vs −0.18%/day), not in 2021-26 (+0.12 vs +0.16). Requiring both trends up failed recently too: fails.
- **Cheapest way to run the monthly trend rule: IBIT shares** (0.02% spread vs 1.9% on spot BTC), checked once a month. That removes the cost problem entirely.
