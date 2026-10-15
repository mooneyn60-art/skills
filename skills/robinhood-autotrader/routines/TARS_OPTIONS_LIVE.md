# TARS Options Live — rules v1

The rules TARS trades SPY options by, with a $500 buffer Nolan authorized. Frozen by hash; changed only with Nolan's words.

Last Updated: 2026-10-15
Status: ACTIVE from 2026-10-16
Audience: TARS (this session's hourly fires), Nolan

## Overview
- Authorization, Nolan's exact words (2026-10-15): "I want you do it and show me how you do it what you look for and how to become profitable how about sell $500 of stock and you use that as your buffer if you want I'm good with 750 I authorize and explain it all for me". He also confirmed the sale of VLO and FRO to fund it.
- This overrides the OPTIONS_APPRENTICE paper gate for a capped live slot only. TARS chose $500 (not $750).
- Honest expectation, said up front: TARS's research found no reliable intraday direction edge. These rules use the two leans that held up best, keep costs low and losses capped. The slot is a measured experiment; it may lose.

## Money rules
1. Buffer: $500. Every trade is sized from what's left of it.
2. Max premium per trade: $100 (normally 1 contract). One position at a time. Max 2 entries per day.
3. Day stop: after −$100 realized in a day, no more entries that day.
4. Hard stop: if the buffer falls to $300 or less, stop trading and report to Nolan. Only Nolan restarts it.
5. No size increase before 40 trades AND a positive bootstrap 90% lower bound after costs.

## What TARS trades
- SPY options expiring the NEXT trading day (1DTE). Why: about half the hourly time decay of 0DTE at midday, less whipsaw, no 3:45 force-close. Positions are still closed the same day.
- Strike: at the money or one strike in the money (delta 0.50-0.60). Spread no wider than $0.03 and 3% of mid, else skip.
- Orders: limit at mid; may raise by $0.01 twice; never chase further. After a fill, a stop_market sell-to-close at −35% of the fill goes in right away.

## When
- Entries only 10:30-14:30 ET. (Nolan's own record: before 10:30 he lost on 5 of 5 days; the open sets the day's high/low and has the widest spreads.)
- FOMC days: no entries after 13:00. CPI and jobs days: normal (the news is in the gap).
- Everything is closed by the 15:35 ET check. Nothing held overnight.

## Setups (the only two reasons to buy; anything else = no trade)
S1 GAP-AND-GO (calls). Evidence: 20 years of SPY, gap-ups over 0.6% closed above the open 60-62% of the time (about 600 days); gap-downs were a coin flip, so there's no put version.
- Gap up ≥ 0.6% vs prior close, and at the 10:35 check SPY is above both the open and VWAP → buy a call.
- Exit: SPY trades below the open (invalidation), the −35% stop, or the 15:35 time exit. No profit target (the edge is open-to-close).

S2 STRETCHED DIP IN AN UPTREND (calls). Evidence: weak but out-of-sample (133 days): a 5-min close below VWAP −2σ bounced +0.07 pts over 30 min, 57% of the time (t 2.5); RSI(14, 5-min) under 30 was +0.12 pts (t 1.6). Small, so cost control decides it.
- SPY's prior close is above its 20-day average; within the last 10 minutes a 5-min bar closed below VWAP −2σ OR 5-min RSI(14) went under 30; and the latest 5-min bar closed above the previous bar's high (the turn) → buy a call.
- Exit: +40% on the option, SPY back to VWAP, a new low below the dip low, the −35% stop, or 60 minutes after entry, whichever first.

No put setups: none of the downside ideas held up out of sample (+2σ fades and RSI > 70 shorts were flat or negative).

## How checks happen (updated 2026-10-15)
Scheduled, unattended checks were refused by the session's safety check (creating a recurring trigger or a timed follow-up for live options trading). TARS does not work around that. So checks run only when Nolan is in the conversation: he messages "TARS check" (or anything) during market hours and TARS runs the check below, live, with him watching. An open position always has its −35% stop resting at Robinhood, so it is protected between checks; at the last check of the day TARS closes it, and if no check happens after 15:00 ET the stop and the 1DTE expiry (not same-day) limit the damage. If Nolan wants unattended checks, he can add a permission rule allowing scheduled tasks in his Claude Code settings.

## Each check
1. Read buffer state from `paper/live_options/state.json`; read SPY minute bars (get_equity_historicals) and the prior day; compute VWAP ±2σ, 5-min RSI, open, gap, 20-day average (daily bars).
2. If a position is open: apply the exit rules; if exiting, cancel the stop first, then sell at mid (walk $0.01 twice, then bid).
3. If flat, inside the entry window, under the day/hard stops: check S1 then S2. If one fires: get_option_instruments for the 1DTE ATM strike, get_option_quotes, check the spread, review_option_order, place_option_order (fresh UUID ref_id), then place the −35% stop.
4. Log every check in one line to `paper/live_options/checks.jsonl` (also "no trade, because ..."). Log every trade to `paper/live_options/trades.jsonl` with setup, SPY context, prices, fees, result.
5. Tell Nolan after each entry and exit: what I saw, why the rule fired, what I bought, where the exits are, what happened. Plain words.

## Review
- After 20 trades or 4 weeks: report net result after costs, win rate, avg win/loss, each setup separately. If the net is negative after 20 trades, pause and propose changes for Nolan to decide.
- R13: no account balances in repo files; buffer and trade P&L are slot figures and are fine.
