# Data Farm Paper Trading

One-line: Every hourly check, feed today's SPY minute bars to the data farm, which paper-trades its frozen setups and updates the dashboard.

Last Updated: 2026-10-15
Status: ACTIVE (paper only)
Audience: TARS trading desk (hourly check), Nolan

## Overview

Nolan (2026-10-15): "make one for me ... actually use it to learn and make
trades, make sure indicators are all set up". The data farm
(paper/datafarm/) detects SPY intraday setups (sweeps, fair value gaps,
VWAP/EMA9/EMA21 trend, RSI14, ATR14) and trades them on PAPER with frozen
rules. It never places a real order. Live-money trading of any setup needs
the OPTIONS_APPRENTICE gate (40+ forward paper trades over 4+ weeks,
positive with a bootstrap lower bound > 0 after costs, still positive
without the best day) and Nolan's yes.

Dashboard: https://claude.ai/artifact/CFnJAG4atRcXgURZPCs5D8

## Each hourly check, market hours only (10:17 .. 16:17 ET fires)

1. get_equity_historicals symbols ["SPY"], interval "minute",
   start_time = today 13:30Z (no end_time). The result is saved to a
   tool-results file; note its path.
2. cd skills/robinhood-autotrader/paper/datafarm
   python3 paper_trader.py --bars <that file>
   python3 datafarm.py          (refreshes the backtest on all stored days)
   python3 build_dashboard.py
3. Publish the dashboard: Artifact publish with file_path
   paper/datafarm/dashboard.html and url
   https://claude.ai/artifact/CFnJAG4atRcXgURZPCs5D8 (read it once per
   session first if the tool asks).
4. Commit paper/history/spy_1min.json, paper/datafarm/*.json and
   dashboard.html with the hourly push if there is one; otherwise at the
   5:17 close report. R13: no account balances in files or messages (paper
   equity is a paper number and is fine).
5. In the check note, one line: paper trades closed today, open now, today's
   paper R. Do not message Nolan about paper trades unless he asks.

## Rules are frozen

Do not edit datafarm.py during the week. A changed file changes its hash and
paper_trader.py restarts the forward book from that day, so the record stays
honest. Rule changes go through the weekend research swarm.
