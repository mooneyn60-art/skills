# What Options Traders Watch, Tested — and Nolan's Own Clock

Checks the tools experienced 0DTE traders talk about, and finds the clearest pattern so far in Nolan's own trades.

Last Updated: 2026-10-15
Status: done; desk v5 warns on pre-10:30 entries; GEX collection started in the journal
Audience: Nolan, TARS

## Overview
- Sources: vendor material (SpotGamma, FlashAlpha) on dealer gamma (GEX), gamma flip and pin risk; academic: Beckmeyer, Branger & Gayda (2023) on retail 0DTE; Gao, Han, Li & Zhou (2018) and Baltussen et al. (2021) on intraday momentum; Ni, Pearson & Poteshman (2005) on pinning.
- Tests: `paper/research_scripts/hedging_flows.py` (164 days of real SPY intraday bars), `paper/research_scripts/owner_timing.py` (Nolan's 226 round trips, Oct 8-15).

## What the evidence says
| Idea traders use | Evidence | TARS test |
|---|---|---|
| 0DTE buying | Retail 0DTE buyers lose on average, ~60% of it costs; sellers profit after fees (Beckmeyer et al. 2023; Bryzgalova et al. 2022) | Our 20-year check: realized moves are 55-80% of what VIX implies |
| Dealer gamma (GEX), gamma flip | Vendor claims only; no independent backtest found. Vendors themselves say it describes volatility, not direction | Can't backtest (no history of open interest by strike). Daily snapshot collection started |
| Pinning to strikes at expiry | Found for single stocks on monthly expiries (Ni et al. 2005) | **None in SPY**: closes sit 0.254 from a $1 strike vs 0.250 by chance; 25% of near-strike days stayed pinned (= chance) |
| First half hour predicts last half hour | Published for SPY 1993-2013 (Gao et al.) | Weak here: corr +0.05 (t 0.7); reversed in Sep-Oct |

## Nolan's own clock (226 round trips, 6 trading days)
- **Before 10:30: lost on 5 of 5 days** that had trades, win rate 12-19%. **After 10:30: net positive on 5 of 6 days.**
- Hold time: 2-5 minute holds were the worst bucket (win 29%); 5-15 minute holds the best (win 42%, +6% per trip).
- First 6 trips of each day were net losers; later trips net positive.
- Overall: 29% winners, avg winner +23%, avg loser −12%. Break-even needs ~35% winners at that payoff.
- Without the best day (Oct 13) the record is negative. Six days is a small sample, but the before/after-10:30 split repeated every day, which is unusual for noise.
- Why it fits the market data: the first 30 minutes set the day's high or low on ~25-30% of days, spreads are widest and moves whip back and forth. Entries there catch both.

## What changes
- Desk v5: the ticket warns (never blocks) on buy-to-open before 10:30 with this record. Ask TARS knows it.
- MARKET_JOURNAL: daily GEX snapshot (±6 strikes around the price, 0DTE, open interest + gamma) so a real test is possible after ~40 days.
- Re-run `owner_timing.py` every Friday; if the before-10:30 pattern breaks for 2 straight weeks, drop the warning.
