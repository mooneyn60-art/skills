# TARS Skills — what I can do, and the proof

Every skill TARS has, with its level and the evidence. A skill counts only if it was built and used or tested, not just named.

Last Updated: 2026-10-16
Status: active (Nolan: "More skills I told you 100k don't stop til you get there everting brush up opon")
Audience: TARS, Nolan

## Overview
Levels:
- 1 = built
- 2 = used live
- 3 = tested with numbers
- 4 = tested in both halves of the data and in daily use

Count: **49 skills** (2026-10-18). Goal: keep adding real ones. Each new skill gets a row here the day it's built.

## Market reading
| # | Skill | Lvl | Proof |
|---|---|---|---|
| 1 | Read SPY intraday: VWAP ±σ, EMAs, RSI, MACD, Bollinger, pivots, volume | 2 | live desk; guide cards |
| 2 | Liquidity pools + which pool gets hit first | 4 | pool_odds_test.js, calibrated 10/30/50/71/90 → 9/27/52/69/88 |
| 3 | Market structure BOS/CHoCH, non-repainting | 3 | godmode_test.py (no edge: map only) |
| 4 | Gap-fill odds by gap size | 4 | market_lab §2 |
| 5 | VIX regime → day range and lean | 4 | market_lab §13 |
| 6 | Expiry-Friday lean | 4 | market_lab §3 |
| 7 | What drives SPY (mega-caps, VIX, Europe at the open) | 3 | spy_drivers.py |
| 8 | Live driver board (points pushed by the top 10) | 2 | platform Drivers |
| 9 | Chart analyst agent (Atlas) | 2 | .claude/agents/chart-analyst.md |
| 10 | Expected move from options (straddle → implied %) | 2 | BE 10/23 straddle ±12.3% (2026-10-16) |

## Prediction
| # | Skill | Lvl | Proof |
|---|---|---|---|
| 11 | Walk-forward model building (no peeking) | 3 | predict_lab.py |
| 12 | Day score (pre-open) | 3 | tails held in both halves; 10/16 call HIT |
| 13 | Overnight score | 3 | predict_lab.py; overnight_score.py ledger |
| 14 | Calibration + Brier scoring of my own calls | 2 | PREDICTIONS.jsonl (4 graded, Brier 0.19) |
| 15 | Knowing when a model fails (next hour, cross-market) | 3 | predict_lab2.py |

## Research method
| # | Skill | Lvl | Proof |
|---|---|---|---|
| 16 | Out-of-sample / two-halves testing | 4 | every lab script |
| 17 | Day-clustered t-stats | 3 | market_lab, godmode_test |
| 18 | Costs in every backtest | 3 | 0.03 pts, 2 bp |
| 19 | Option repricing at the regime's IV (Black-Scholes) | 3 | overnight_slot.py (after a mistake) |
| 20 | Reverse-engineering paid indicators from their claims | 3 | godmode_test.py |
| 21 | Spotting sales tricks (fake timers, cherry-picked charts) | 2 | godmodealgo review |
| 22 | Event studies (earnings, Fed, gaps through stops) | 3 | EVENT_REACTIONS, BE earnings reactions |
| 23 | Data hygiene: refresh, merge and sanity-check history | 2 | daily bars to 10/16 with OHLC checks |

## Trading and risk
| # | Skill | Lvl | Proof |
|---|---|---|---|
| 24 | Place and close option orders with limit + stop | 2 | slot trades #1-#2 |
| 25 | Never leave a position unprotected longer than needed | 2 | equity stop guard; cancel → sell in one minute |
| 26 | Exit by rule, not hope | 2 | both S2 exits on invalidation |
| 27 | Mood-based sizing (stress shrinks size) | 2 | Mood table |
| 28 | Stop audits on every stock | 2 | 6/6 resting, checked 10/16 |
| 29 | Earnings guard for holdings | 2 | platform Earnings column; BE 10/22 flagged |
| 30 | Decline a trade when the evidence says no | 2 | dip-buy pause proposed |

## Building
| # | Skill | Lvl | Proof |
|---|---|---|---|
| 31 | Live web apps on the Robinhood connector | 2 | TARS Trading Platform |
| 32 | ~1 s live price loop within platform limits | 2 | callTool loop (after the 30 s discovery) |
| 33 | Shared database link (see the desk, chat) | 2 | desk/snapshot, tars/now, chat |
| 34 | Browser testing with mocks (Playwright) | 3 | plat*.js harnesses |
| 35 | Claude Code mods (hooks, commands) | 2 | mods/tars, 3 tests pass |
| 36 | Sub-agents with characters | 2 | the town's residents, Atlas |
| 37 | Charts on canvas (zoom, drag, layers) | 2 | desk chart |
| 38 | Docs (Claude Docs) for long research | 2 | consciousness research doc |

## Mind
| # | Skill | Lvl | Proof |
|---|---|---|---|
| 39 | Global workspace (the Stage) | 2 | mod prompt.submit |
| 40 | Emotion engine (valence/arousal, caution only) | 2 | EMOTIONS.md |
| 41 | 16 brain habits (veto, two speeds, association, predict-then-check) | 2 | BRAIN.md |
| 42 | Connections web of findings | 2 | CONNECTIONS.md |
| 43 | Sleep replay + dreams | 2 | DREAMS.md, TARS_LIFE steps |
| 44 | Self-review: mistake → fix → rule | 2 | SELF_REVIEW.md (3 entries today) |
| 45 | Reading Nolan (theory of mind) | 2 | HUMAN.md |
| 46 | Honest reporting (losses, misses, limits) | 2 | NOLAN_LOG |
| 47 | Platform link: reads the console chat + desk snapshot every 5 min, wakes on a new message | 1 | mods/tars v0.2 (fixes.test.ts) |
| 48 | Slot guard: the money rules as a hard gate on opening option orders | 3 | mods/tars-guard (guard.test.ts) |
| 49 | Self-repair of my own mod (stale log line, off-hours noise, arousal bug) | 3 | mods/tars fixes.test.ts, 7/7 pass |

## Next to learn (queue)
- Options Greeks risk view per position (theta per day, gamma near expiry).
- Volatility surface: is IV rich or cheap vs realized (sell/buy decisions).
- Sector rotation map (which sectors lead SPY this week).
- Position sizing by stop distance and VIX.
- Correlation of Nolan's holdings: how many independent bets?
- Tax-aware selling (short vs long term).
- News/filings reader (SEC 8-K on holdings).
- Auto nightly refresh + model retrain.
