# Routines

Each file here is the full instruction set for one scheduled TARS routine.
The scheduler only holds a short pointer ("read and carry out
routines/X.md"), so **editing a file here changes what the routine does
next time it fires.** No scheduler changes needed.

| File | When (ET) | Runs in |
|---|---|---|
| (hourly trading check, prompt lives in the scheduler) | 9:17am-5:17pm weekdays | main TARS session |
| FRIDAY_DATA_REFRESH.md | Fri 5:30pm | main TARS session (needs broker access for price data) |
| WEDNESDAY_CONTRARIAN_PROBE.md | Wed 6pm | research runner |
| WEEKEND_RESEARCH.md | Sun 10am | research runner |
| CURIOSITY_BLOCK.md | 1st and 15th, 11am | research runner |
| MONTHLY_EXPECTANCY_AUDIT.md | 1st of month, 10am | research runner |
| QUARTERLY_RULE_AUDIT.md | 1st of Jan/Apr/Jul/Oct, 1pm | research runner |
| ONESHOT_R15_INTEGRATION.md | Sat 2026-09-26, 11am, once | research runner |

The **research runner** is a dedicated session with this repo attached and
no broker access, so research routines cannot place trades. Schedules are
stored in UTC; times above are Eastern daylight time.

Nolan can edit any of these files. Keep the NO TRADES lines in research
routines.
