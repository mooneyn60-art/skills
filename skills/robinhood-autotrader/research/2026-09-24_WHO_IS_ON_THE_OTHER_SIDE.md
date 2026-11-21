# Who Is on the Other Side? Market Structure for a Small Retail Account

One-line: RESEARCH_AGENDA item 19. Who fills this account's orders, how are
they paid, and which market-structure effects actually cost a ~$1-2k account
money?

Last Updated: 2026-09-24
Status: DONE. An understanding question: literature only, no test run.
        Measuring this account's actual fills against quotes is item 9.
Audience: Nolan, TARS sessions

## Answer first

- WHO: almost never another retail investor, and almost never an exchange.
  Robinhood sends orders to wholesalers (Citadel Securities, Virtu,
  Susquehanna, etc.), which pay Robinhood for the flow (payment for order
  flow, PFOF) and fill the order against their own inventory. Three or four
  firms handle the large majority of US retail market orders.
- WHY THEY PAY: retail orders are small and uninformed on average, so
  filling them is profitable. The wholesaler earns part of the bid-ask
  spread and shares some of it with the broker (PFOF) and some with the
  customer ("price improvement").
- WHAT IT COSTS THIS ACCOUNT ON STOCKS: very little in dollars. The best
  independent measurement (Schwarz, Barber, Huang, Jorion & Odean; matched
  identical orders across brokers, 2021-22) found round-trip costs of about
  0.07% to 0.46% depending on the broker, i.e. roughly 3.5-23 basis points
  each way. On a typical ~$200 position that's about $0.07-0.46 each way.
  Real, but small next to an 8% stop.
- BROKER CHOICE MATTERS MORE THAN PFOF ITSELF: the same wholesalers gave
  different prices to different brokers for identical orders. The SEC
  fined Robinhood $65M in 2020 for misleading customers about this; it
  found Robinhood customers got $34.1M worse prices, net of the commission
  savings, in 2018-19. A randomised trial (Lynch 2022, as reported) found
  far fewer Robinhood orders filled at or better than the midpoint than at
  TD Ameritrade. Whether that gap still exists in 2026 is unknown.
- OPTIONS ARE WHERE THIS BITES: PFOF on options is larger than on stocks
  across the industry, and retail options spreads are wide. Weekly options
  favoured by retail averaged a 12.6% bid-ask spread (Bryzgalova et al.
  2023, verified in item 15). This account measured 3-28% on small names
  (reference/options.md §5). On a $60 contract, 12.6% is ~$7.50 per round
  trip before anything else happens.
- INSTITUTIONAL FLOWS: mostly not a per-trade cost for this account.
  - The S&P 500 inclusion bump has nearly vanished: excess returns for
    additions fell from ~8% (late 1990s) to ~0 (2011-21) (Greenwood &
    Sammon). No edge left to chase there.
  - Options dealers' hedging moves prices: stocks cluster near big strikes
    on expiry days (Ni, Pearson & Poteshman 2005); hedging explains part of
    daily moves in optioned stocks; intraday momentum is stronger when
    dealers are "short gamma" (Baltussen et al. 2021). With same-day (0DTE)
    SPX options now close to half of SPX volume, this mostly shows up as
    intraday noise. It matters for WHEN a stop gets hit, not for a
    multi-week holding.
- REGULATION: the SEC's 2022 plan to force retail orders into auctions was
  never adopted and was withdrawn in June 2025 (as reported). PFOF
  continues as before.

## What this means for TARS (interpretation)

1. Stock execution costs are a rounding error at this size IF orders are
   limit orders or marketable orders in liquid large caps. They are not a
   reason to change strategy.
2. Options execution costs are NOT a rounding error. They are one more
   reason item 15 came out negative.
3. Stop orders fill at whatever the market is when triggered. In a fast,
   dealer-hedging-driven intraday move, a stop-market can fill well below
   the trigger. Item 3 (gaps through stops) should measure this on the
   account's own stops.
4. Item 9 should compare this account's actual fills in trades.jsonl with
   the quote at order time. That turns "3.5-23 bp" from someone else's
   average into this account's number.

## Sources (sub-agent; items it marked as secondary or not checked are flagged)

- SEC press release 2020-321 (Robinhood $65M settlement). https://www.sec.gov/newsroom/press-releases/2020-321
- Schwarz, Barber, Huang, Jorion & Odean, "The Actual Retail Price of Equity Trades" (SSRN 4189239; J. Finance 2025). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4189239
- Lynch (2022), PFOF randomised trial, SSRN 4189658 (via a Wharton summary; exact figures not checked).
- SEC Order Competition Rule proposal (2022-225) and withdrawal (2025). https://www.sec.gov/rules-regulations/2025/06/order-competition-rule
- Congressional Research Service on PFOF and wholesaler shares. https://www.congress.gov/crs-product/IF12594
- Bryzgalova, Pavlova & Sikorskaya (2023), J. Finance. https://onlinelibrary.wiley.com/doi/10.1111/jofi.13285
- Greenwood & Sammon, "The Disappearing Index Effect", NBER w30748. https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- Ni, Pearson & Poteshman (2005), JFE, expiry-date clustering. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=519044
- Baltussen, Da, Lammers & Martens (2021), JFE, hedging demand and intraday momentum.
- Cboe on 0DTE growth. https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf
- Options PFOF totals ($2.4B options vs $1.3B equities, 2021) from trade press; not checked.
