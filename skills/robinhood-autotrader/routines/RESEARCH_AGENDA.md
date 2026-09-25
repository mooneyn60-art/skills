# Research Agenda

The queue of market topics TARS still needs to learn, set by Nolan on
2026-09-23 ("push all next"). The Wednesday probe and the Sunday research
block each take the TOP UNFINISHED item, work it, and update its status
here. One item per session. A finished item links to its research note.

| # | Topic | Why it matters | Status |
|---|---|---|---|
| 1 | Company fundamentals: earnings, revenue and guidance trends as signals | Biggest blind spot. Nolan read SOFI from how the business was doing; TARS only read the price. Does a stalled-earnings filter or an earnings-trend filter improve R2 entries? | DONE 2026-09-23, DEAD: net income YoY sign -0.30pp t=-0.68; revenue +0.63pp t=1.31, vanishes without megacaps. [note](../research/2026-09-23_FUNDAMENTALS_EARNINGS_TREND.md). Untested: surprise vs estimates, release dates, small caps. |
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

## Added 2026-09-24: things TARS said it does not understand

Nolan asked "what don't you understand?" and then "research all of those, do
deep research so you really understand." Each gets its own note in
research/. These are understanding questions, not strategy hunts: the goal
is a correct explanation, and "we can't know this" is an acceptable answer
if it's argued properly.

| # | Topic | Status |
|---|---|---|
| 15 | OPTIONS, Nolan's priority: do options beat SPY? Separate BUYING (calls, puts, LEAPs) from SELLING (covered calls, cash-secured puts). Evidence to find: the volatility risk premium literature, the long history of the CBOE BuyWrite (BXM) and PutWrite (PUT) indexes against the S&P 500, retail options-trader outcome studies, and what is actually feasible at ~$1,500-2,000 of capital (collateral for one cash-secured put on a $15 stock is ~$1,500). If historical index data is reachable (CBOE publishes BXM/PUT values), test it with the four hurdles. Report honestly in either direction. | DONE 2026-09-24: NOT SUPPORTED. Buying: calls-instead-of-index -0.35%/yr vs S&P TR +11.37% (1991-2026); OTM calls lose 70-77% of premium. Selling: PUT 7.17% vs 11.04% (2007-2026, t=-2.26); 30-delta buy-write ~S&P minus 0.6pp with less risk since 1988. Nothing feasible at level 2 / $2k. [note](../research/2026-09-24_OPTIONS_VS_SPY.md) |
| 16 | Why prices move on a given day: how much of daily movement is market-wide, sector-wide and company-specific? Decompose this book's daily returns against SPY and sector ETFs. How often is there actual news behind a move? | DONE 2026-09-24: depends on the name. Company-specific share 61-88% for EXEL/NWG/INTC/SOFI/ABBV; NVDA 64% market+semis; CVE 63% market+energy. 57% of >3sd company moves had a filing day 0/-1 vs ~10% base rate. Fat tails: 4-7x the normal count of 3sd days. [note](../research/2026-09-24_WHY_PRICES_MOVE.md) |
| 17 | Case study: why INTC went from ~$29 to ~$124 in a year with negative earnings. What did the market price in? Foundry, government deals, AI, turnaround? Use sources, separate fact from narrative. What would have told TARS this in advance, if anything? | DONE 2026-09-24: 7.3x from $19.31 (Aug 2025). Outside money (US gov 10%, Nvidia $5B, SoftBank) + earnings beats + foundry customers; GAAP losses mostly one-offs incl. a warrant mark-to-market. Unpredictable news, but R2's 200-day cross came 7 days after the low and caught 94%; R4's trail sold at +95% in Jan 2026. [note](../research/2026-09-24_INTC_CASE_STUDY.md) |
| 18 | Is TARS adding value at all? Compare the account's actual record, deposits excluded, against SPY over the same days, and state how many trades are needed before the answer is statistically meaningful. Overlaps item 6 and item 8. | DONE 2026-09-24: unknowable for years. Live TARS n=6 -0.41R t=-1.35. Backtest vs SPY IR 0.11 (t=0.50 over 20 yrs), ~312 live years for t=2; 124 trades at the backtest's per-trade edge. Positive trades are not beating SPY. [note](../research/2026-09-24_IS_TARS_ADDING_VALUE.md) |
| 19 | Who is on the other side: market structure for a retail account. Payment for order flow, market makers, institutional flows, index rebalancing, options-driven hedging. What of this actually affects a small account's fills and returns? | DONE 2026-09-24: wholesalers (Citadel, Virtu, Susquehanna) fill retail orders and pay PFOF. Stock costs ~3.5-23bp one-way, small at this size; broker choice matters more than PFOF. Options spreads (~12.6% on retail weeklies) are the real cost. Index-inclusion effect has vanished. Literature only; item 9 measures our fills. [note](../research/2026-09-24_WHO_IS_ON_THE_OTHER_SIDE.md) |
| 20 | Does the past still apply? Evidence on how quickly market patterns decay (post-publication decay, regime shifts). Which of TARS's live rules rest on evidence most at risk of being out of date? Overlaps the monthly decay check. | DONE 2026-09-24: patterns decay fast (-58% post-publication; 65% of anomalies fail to replicate). 200-day gate: no reliable return edge by era, but robust volatility avoidance. Most at risk: R15, then R4 exits. [note](../research/2026-09-24_DOES_THE_PAST_STILL_APPLY.md) |
| 21 | How gut feel and intuition work in trading: what research says about expert intuition (when it's reliable, when it isn't), and how to score Nolan's gut calls fairly. Links to notes/GUT_CALLS.md. | DONE 2026-09-24: stock picking is a low-validity environment for intuition (Kahneman & Klein). Score calls against the market's probability; a +10pt edge needs ~100 calls for 50% detection, ~200 for 81%. Proposed: log Nolan's confidence too. [note](../research/2026-09-24_GUT_FEEL_AND_INTUITION.md) |

Item 22, calibration (knowing when TARS is actually right), is already item 7
and runs in the curiosity block.

## Added 2026-09-24: reading the chart

| # | Topic | Status |
|---|---|---|
| 23 | Candlesticks and chart lines, Nolan's request: "how to read candles and lines to see how the stock is going to break or boom." Two parts. (a) Candlestick patterns: hammer, engulfing, doji, morning/evening star and the other common ones. (b) Lines: support and resistance, trendlines, and breakouts from ranges or highs. For each, explain how traders read it AND test whether it actually predicts anything. The daily OHLC in paper/history/daily_stocks.json (15 symbols, 2006-2026) is exactly the data candle patterns are built from, so this is directly testable. Define every pattern mechanically BEFORE testing (no eyeballing charts), measure forward returns after each pattern against the unconditional average, and apply the four hurdles and a multiple-testing correction, since there are dozens of patterns and some will look good by luck. Also find the academic studies on candlesticks and support/resistance and report what they found, including any failures to replicate. Teach Nolan the ones that hold up, in plain language. | DONE 2026-09-24: 39 primary pattern x horizon tests, zero survive Bonferroni + both-halves. P1 candlesticks CONFIRMED (no edge), P2 breakouts REFUTED, P3 VIX-split breakdowns PARTLY (directionally consistent, not significant), P4 support bounces CONFIRMED (no edge). [note](../research/2026-09-24_CANDLESTICKS_AND_CHART_LINES.md) |

## Carried over 2026-09-25 (agent hit a usage limit)

| 24 | Earnings moves + SOFI call scenarios (research/2026-09-24_EARNINGS_MOVES.md) | Data and script already exist (paper/research_scripts/earnings_moves.py). Run it, verify, and write Results/Verdict. Needed before SOFI's 2026-10-27 report. | HIGH, PARTIAL |
