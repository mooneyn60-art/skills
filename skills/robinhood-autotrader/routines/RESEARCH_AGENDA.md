# Research Agenda

The queue of market topics TARS still needs to learn, set by Nolan on
2026-09-23 ("push all next"). The Wednesday probe and the Sunday research
block each take the TOP UNFINISHED item, work it, and update its status
here. One item per session. A finished item links to its research note.

| # | Topic | Why it matters | Status |
|---|---|---|---|
| 1 | Company fundamentals: earnings, revenue and guidance trends as signals | Biggest blind spot. Nolan read SOFI from how the business was doing; TARS only read the price. Does a stalled-earnings filter or an earnings-trend filter improve R2 entries? | TODO, TOP PRIORITY |
| 2 | Macro regime: yield curve (T10Y2Y, T10Y3M), fed funds, unemployment from FRED | Rates move nearly everything, especially banks (NWG, SOFI). Data reachable, completely untested. | TODO |
| 3 | Event reactions: earnings days, FOMC days, overnight gaps through stops | How often does a gap skip past an 8% stop? What do these holdings typically do on earnings? CVE carries war-headline gap risk. | TODO |
| 4 | Correlation inside the book | NVDA+INTC are both chips, NWG+SOFI both finance. Measure how concentrated the risk really is, and whether the sector cap is the right tool. | TODO |
| 5 | Survivorship-free universe | Every backtest uses 15 names chosen in 2026, none of which failed. Find a source of point-in-time index membership including delisted names. Hardest and most important for honest numbers. | TODO |
| 6 | The account's own record | 120+ ledger entries. When does TARS lose money: time of day, after what kind of day, after what kind of decision? Also score Nolan's gut calls as they resolve (notes/GUT_CALLS.md). | TODO |
| 7 | Calibration: knowing how sure to be | Covered by the curiosity block (weather forecasting redo). Bring any practical lesson back into how TARS states confidence. | IN CURIOSITY BLOCK |

## How to run an item cheaply (Nolan asked to save credits)

- USE SUB-AGENTS ON CHEAPER MODELS FOR THE GRUNT WORK. Spawn them with
  model "haiku" for web searches, fetching and summarising sources, or
  model "sonnet" when the reading needs judgement. Give each one a narrow
  question and ask for a short answer with sources.
- Keep the main session for the parts that need care: stating the
  hypothesis, designing the test, running it on the data, and checking
  agent claims against the data before trusting them.
- Don't spawn an agent for something one search or one script can do.
- Stop when the question is answered. A clean "no" is a finished item.

## Rules that still apply

The four hurdles (mechanism stated first, split sample, 9-window
walk-forward, drop the megacaps) and R14 (scripts print data, never a
pre-written conclusion; every number carries its provenance). NO TRADES.
