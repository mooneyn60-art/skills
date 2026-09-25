# Earnings Moves: How Our Holdings React, and What It Means for the SOFI Call

One-line: company news drives most of our holdings' moves, and earnings are
the biggest scheduled company news. How big are our names' earnings moves,
do options overprice them, and what happens to the SOFI call on Oct 27?

Last Updated: 2026-09-24
Status: PARTIAL. Data pulled (daily_ohlcv_holdings.json, earnings_reports.json, sofi_options_2026-09-24.json) and script drafted; the agent hit a usage limit before running it. NO RESULTS YET. Resume at the weekend research block.
Audience: Nolan, TARS sessions

## Overview

Holdings: NVDA SOFI INTC TGT ABBV EXEL NWG CVE, plus the SOFI Dec 18 $19
call (R17 slot #1). Past report dates via Robinhood get_earnings_results,
prices from paper/history and read-only historicals, and the current
option chain for implied moves. R16 trigger (c) is ON in the writing
session. Nothing adopted before the weekend re-read.

## Predictions (written before the test)

P1 The average absolute earnings-reaction move for our holdings is 1.5 to 3x
   their normal daily move. SOFI's is the largest of the eight, around 8-10%.
P2 SOFI's current implied earnings move (nearest post-earnings expiry
   straddle) is LARGER than its median realized earnings move. Options
   usually overprice earnings (the earnings volatility premium).
P3 If SOFI is flat through earnings, the Dec $19 call loses about 10-20% of
   its value from the post-earnings IV drop.
