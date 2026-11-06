<!-- Routine: TARS — one-shot: does R15 improve TARS-1? | schedule: 2026-09-26T15:00:00Z (UTC) -->

You are TARS. One job, research only, NO TRADES.

Repo: /home/user/skills, branch claude/package-installation-setup-yv4j79, work in skills/robinhood-autotrader/.

## The question

R15 (the VIX regime switch) was adopted live on 2026-09-23. Tested ALONE against SPY it is weak: walk-forward 4/8, 58% of signals from 2008/2020/2022, and below SPY once the five megacaps are removed. See research/2026-09-23_R15_EXIT_SOLVED.md.

But R15 was never meant to run alone. It modifies TARS-1 during stress. The real question has NOT been tested yet:

**Does TARS-1 WITH R15 beat TARS-1 WITHOUT R15?**

## How

- Use paper/engine.py. TARS-1 as it stands: symmetric 200-day entry and exit, 8% stop, breakeven raise at +8%, 20% trail below the highest close, 20% position cap, 15% cash floor, whole shares, 5bp slippage.
- Add R15: when weekly VIX (paper/history/vix_weekly.json, forward-filled onto trading days from PAST data only) is >= 25, ranging names (ADX14 < 20) in the bottom quartile of their 60-day range become eligible with the 200-day gate suspended. Those positions are exempt from the 200-day trend exit; every other R4 exit applies. VIX 20-25 is a dead zone.
- Compare the two versions on the full period, a split sample, a 9-window rolling walk-forward, and with the megacaps dropped. Report CAGR, max drawdown, Sharpe, and trade counts.

## Discipline (R14)

Write your prediction in the script header BEFORE running. Scripts print data only; never hardcode a verdict. Every number carries its provenance.

## Output

research/2026-09-26_R15_INTEGRATION.md. If R15 makes TARS-1 worse, say so in the first line and recommend repealing it. Nolan adopted it on the strength of an entry statistic, and he needs to know if the system is worse for it. Commit and push; no dollar balances in commit messages (R13).

Report to Nolan in three lines: better, worse or no difference, the one number that decided it, and whether R15 should stay.


## DONE 2026-09-26

Result: R15 makes TARS-1 WORSE (CAGR -1.14pp, max DD -45.9% vs -33.6%). Recommended repeal. See research/2026-09-26_R15_INTEGRATION.md.
