# World Markets and SPY — do Asia and Europe lead the US?

Tests whether Asian and European index moves line up with, or predict, SPY's gap and SPY's open-to-close move.

Last Updated: 2026-10-15
Status: done; no tradeable rule; knowledge added to the desk / Ask TARS; overnight board added to the journal
Audience: Nolan, TARS

## Overview
- Data: daily index levels 2006-2026 from Yahoo Finance (Nikkei 225, Hang Seng, KOSPI, ASX 200, Shanghai, DAX, FTSE 100, Euro Stoxx 50, VIX), SPY daily (2006-2026, 5,218 days), plus ~2 years of hourly DAX / SPY. Saved as `paper/history/world_daily.json`.
- Scripts: `paper/research_scripts/world_markets.py`, `world_robust.py`.
- Timing that matters: Asia trades and closes while the US sleeps (it closes before 9:30 ET). Europe opens ~3:00 ET and closes 11:30 ET, so it overlaps the first two US hours. Robinhood carries no foreign indexes.

## Findings
| Question | Result |
|---|---|
| Same-day co-movement with SPY | Europe strong: DAX +0.60, FTSE +0.57, Euro Stoxx +0.60. Asia weak: +0.11 (Shanghai) to +0.23 (Hang Seng). |
| Who leads? | **The US leads Asia**: yesterday's US close explains much of Asia's day (Nikkei +0.49, ASX +0.46). |
| Asia → SPY gap | Yes: +0.31 to +0.36. Asia's *own* news (the part not explained by the US) lines up with the gap at +0.40. |
| Asia → SPY open-to-close (what you trade) | **No usable edge.** Correlations −0.03 to +0.06. Hang Seng and KOSPI's small effect existed in 2006-15 and vanished after 2016. ASX kept a tiny one (t 2.9 post-2016), but the top 20% of ASX days gave only +0.04% open-to-close (56% up vs 54% base, t 1.1). |
| Big Asia selloff (Nikkei −2%+) | SPY gaps down ~0.5%, then open-to-close averaged +0.10-0.14% with 57-59% up days, in both halves. With a SPY gap down >0.6% too (2016-26, n=52): +0.26%, 60% up. A lean (the panic gap gets bought more often than not), not proven. |
| Big Asia rally (+2%) | Gap up ~0.45%, then nothing (52-53% up). |
| Europe's morning (3:00-9:30 ET) | Predicts the SPY gap (+0.27). Into SPY open-to-close: +0.09 (t 2.4, 2 years only): slight continuation. |
| Europe during the overlap (9:30-11:30 ET) | Moves with SPY at +0.55. It's the same flows, not a lead. |
| After Europe closes (11:30 ET) | DAX's last two hours tell nothing about the SPY afternoon (corr 0.00). SPY's own morning has a slight carry (+0.09, t 2.3). |
| Crisis coupling | DAX-SPY correlation rises from +0.53 (VIX < 20) to +0.64 (VIX ≥ 25). In stress everything moves together; diversifying across regions helps least when it's needed most. |

## What it means for trading SPY options
1. Overnight Asia and Europe tell you the **gap**, and SPY futures/premarket already show it. They don't tell you the **day** after the open.
2. A big Asia selloff that gaps SPY down has been bought slightly more often than not. That fits the gap-fill table. It's a lean.
3. From 9:30-11:30, watch Europe as a live confirm (DAX/Euro Stoxx moving with SPY). After 11:30 it's irrelevant.
4. When VIX is high, "the world is selling" isn't new information; correlation is already near its max.

## Forward tracking
MARKET_JOURNAL 10:00 calls now record the overnight board (Nikkei, Hang Seng, ASX, DAX morning % moves, Asia own-news) and score it at the close. If the Nikkei-selloff lean holds over ~40 cases it can be proposed to Nolan as a rule change.
