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
| 6 | The account's own record | 120+ ledger entries. When does TARS lose money: time of day, after what kind of day, after what kind of decision? Also score Nolan's gut calls as they resolve (notes/GUT_CALLS.md). ADDED 2026-09-23: are decisions made during a losing streak worse than the rest? That result decides whether R16 stays or goes. | TODO |
| 7 | Calibration: knowing how sure to be | Covered by the curiosity block (weather forecasting redo). Bring any practical lesson back into how TARS states confidence. | IN CURIOSITY BLOCK |
| 8 | Multiple testing: how many ideas have we tried? | Every "t=8.46" in research/ was one of many tests run on the same 15 names. Count the hypotheses tested so far, then apply a correction (Bonferroni, Harvey-Liu-Zhu "t > 3", or the deflated Sharpe ratio) and re-state which adopted findings survive. Affects R15 and every future rule. | TODO, HIGH: do before any new rule is adopted |
| 9 | Execution cost: spreads, slippage, fill quality | Backtests assume the close price. Compare actual fills in trades.jsonl against the quote at order time, and estimate the spread on each universe name. If costs eat a meaningful share of a +0.77R trade, the edge is smaller than the backtests say. | TODO |
| 10 | Position sizing theory: Kelly and fractional Kelly | R3 caps each position at 20% by judgement. Given the measured win rate and payoff, what does fractional Kelly say, and how wide is the uncertainty? Mainly to check that 20% is not far too big or far too small. | TODO |
| 11 | Market breadth as a regime signal | R15 uses VIX alone. Does breadth (share of the universe or S&P above its 200-day, advance/decline) add anything VIX doesn't? Price data we already have is enough to test the universe version. | TODO |
| 12 | Momentum vs reversal by horizon | 1-month reversal and 12-1 month momentum are the two best-documented stock anomalies, and they point opposite ways. Where does R2's 200-day gate sit between them, and is our holding period in the right horizon? | TODO |
| 13 | Sentiment and positioning (put/call ratio, AAII survey, short interest) | Test whether any of these adds information beyond VIX for our names. Expect mostly no. A clean "no" still closes the question. | TODO |
| 14 | Taxes: after-tax return of short holding periods | Everything is short-term gains taxed as income. Measure the after-tax gap between TARS and buy-and-hold SPY using reference/TAX_TREATMENT.md. The hurdle may be higher than the pre-tax numbers show. | TODO |

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

Items 8-14 were added 2026-09-23 at Nolan's request ("more topics you need
to understand the market"). They sit below Nolan's original 1-7 and don't
jump the queue, EXCEPT item 8, which should run before any new rule is
adopted: it tells us how much to trust everything else.

R16 applies to research sessions too. If a test in this session refutes the
hypothesis you stated before it, the pressure state is on for the rest of
the session: commit every prediction before running its test, and adopt
nothing from this session.

The four hurdles (mechanism stated first, split sample, 9-window
walk-forward, drop the megacaps) and R14 (scripts print data, never a
pre-written conclusion; every number carries its provenance). NO TRADES.
