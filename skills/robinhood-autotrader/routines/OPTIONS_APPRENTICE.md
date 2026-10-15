# Options Apprentice

One-line: How TARS learns options from Nolan's own trades, and the gate it must pass before it trades options with real money.

Last Updated: 2026-10-15
Status: ACTIVE (learning phase, no live TARS options trades)
Audience: TARS sessions (desk, Friday refresh, weekend research), Nolan

## Overview

Nolan (2026-10-15): "I want you to be able to trade options eventually to
miss my mistakes." His options trades are the richest data we have on what
works and what doesn't in this account: 170 round trips logged in one month
(2026-09-14 .. 2026-10-14). TARS learns from them in three stages and does
not place an options trade of its own until the gate at the bottom is passed.

## Stage 1 - Mistake map (weekly, Friday refresh)

Run `python3 paper/research_scripts/owner_options_mistakes.py`. It prints
net, per-trade average, win rate and average win/loss by: days to expiry,
size, exit hour, the day's running P/L before the trade, sizing up after a
loss, SPY vs single names, exit reason, and per day. Paste the changed
lines into the Friday report. Read it as DATA (R14); with one month of
trades, almost every split is driven by one or two days.

First run, 2026-10-15 (n=170, net positive but ~all of it from 2026-10-13):
- Losing buckets: single names (n=49, -10.5/trade), 1-3 DTE (n=26),
  exits 10:00-10:59 ET (n=43, -13.5/trade), exits after 15:00 (n=10, 0 wins),
  the first trade of the day (n=14, -27.9/trade), premium $150-400 (n=62).
- Winning buckets: SPY 0DTE, exits 12:00-14:59, and larger trades - BUT
  the +1,277 day (10/13) sits inside all of them. Without 10/13 the month
  is negative. Treat the "big size wins" split as unproven, not a lesson.
- TARS's own earlier claim that "sizing up after a loss is the mistake" is
  NOT supported so far (n=32, positive). Recorded at full strength; keep
  measuring before saying it again.

## Stage 2 - Rule filter (monthly, research swarm)

Write a candidate rule set (example: SPY only, 0DTE, no entries before
10:30 or after 14:30, max N trades/day, fixed premium per trade, daily
stop). Apply it to Nolan's history: which trades would the rules have
allowed, and what would they have made? Everything on past trades is
IN-SAMPLE; label it. Then FREEZE the rules (commit hash) before Stage 3.

## Stage 3 - Paper book (live quotes, no orders)

With the frozen rules, the desk logs every setup the rules would take,
using real quotes at the time, to paper/options_paper.jsonl (entry,
exit, P/L). Nolan's own trades keep being logged separately, so we can
compare TARS-rules vs Nolan on the same days.

## The gate (all required before any live TARS options trade)

1. Rules frozen, with commit hash, before the paper book started.
2. At least 40 closed paper trades over at least 4 weeks.
3. Paper per-trade average > 0 with a bootstrap 90% interval whose lower
   end is above 0, after a realistic fill cost (0.02/contract each way).
4. Paper results not driven by one day: still positive with the best day
   removed.
5. Nolan says yes in his own words.
Then: live at a fixed ~$100 premium per trade inside the R17 slot, same
rules, every trade logged, reviewed monthly. Any 4-week live stretch below
zero sends it back to paper.

## Never

- No TARS options trade outside these rules, no averaging down, no
  holding a 0DTE option past 15:25 ET, no naked stops loosened.
- Nolan's own trades stay his; TARS never trades in his name to "fix" one.
