# Overnight paper test

Paper only. No money until it earns it.

Last Updated: 2026-10-16
Status: PAPER from 2026-10-16
Audience: TARS, Nolan

## Overview
SPY's gains come mostly overnight (market_lab §1). The overnight model's strong nights (p≥0.60) were up 61%, +0.12%/night in shares, and +0.85%/night for 30-day ATM calls (overnight_slot.py, 2016-26, n=318). Short-dated options lose overnight at real IV.

## Each evening (after 16:00 ET)
1. Add the day's SPY bar to history/daily_ohlcv.json (Robinhood day bar) and get the VIX close (get_index_quotes).
2. `python3 research_scripts/overnight_score.py <vix>` appends tonight's score to `ledger.jsonl`.
3. Next morning: fill `result` with the open vs the close (shares, %), and mark whether p≥0.60 was right.
4. Review after 20 strong nights: paper net vs "every night" vs nothing. Nolan decides if it gets real money.
