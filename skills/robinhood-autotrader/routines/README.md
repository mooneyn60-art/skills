# Routines

Each file here is the full instruction set for one scheduled TARS routine.
The scheduler only holds a short pointer ("read and carry out
routines/X.md"), so **editing a file here changes what the routine does
next time it fires.** No scheduler changes needed.

| File | When (ET) | Runs in |
|---|---|---|
| HOURLY_TRADING_CHECK.md | 9:17am-5:17pm weekdays | trading desk |
| FRIDAY_DATA_REFRESH.md | Fri 5:30pm | trading desk |
| WEDNESDAY_CONTRARIAN_PROBE.md | Wed 6pm | research runner |
| WEEKEND_RESEARCH.md | Sun 10am | research runner |
| CURIOSITY_BLOCK.md | 1st and 15th, 11am | research runner |
| MONTHLY_EXPECTANCY_AUDIT.md | 1st of month, 10am | research runner |
| QUARTERLY_RULE_AUDIT.md | 1st of Jan/Apr/Jul/Oct, 1pm | research runner |
| ONESHOT_R15_INTEGRATION.md | Sat 2026-09-26, 11am, once | research runner |
| WEEKLY_DESK_RESET.md | Sat 9am | main session (swaps in a fresh trading desk) |

Two sessions run the routines, both with this repo attached:

- **Trading desk**: the hourly checks, the Friday refresh, and the SOFI and
  gut-call one-shots. It starts small, so each check costs far less than
  running inside the long main conversation.
- **Research runner**: research, audits and the curiosity block.

Two more sessions exist for Nolan to TALK to (not scheduled):

- **TARS Chat** (routines/CHAT_SESSION.md): the everyday conversation
  thread. Trades only when Nolan names the trade.
- **TARS Idea Lab** (routines/IDEA_LAB.md): tests Nolan's ideas on demand.
  NO TRADES.

CORRECTION, 2026-09-23: an earlier version of this file said the research
runner has no broker access and therefore cannot trade. That was never
verified, and the trading desk test showed sessions created this way DO get
broker tools. Research routines are prevented from trading by their written
NO TRADES instructions, not by a technical block. That is weaker, and it is
why the NO TRADES lines must stay in every research routine.

Schedules are stored in UTC; times above are Eastern daylight time.

Nolan can edit any of these files. Keep the NO TRADES lines in research
routines.
