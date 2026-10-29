# How the Market Actually Works

Market structure, price discovery, and the macro machinery that moves everything
at once — the layer underneath both the equity rules and the options catalog.
Last updated: 2026-09-14 · Status: active · Audience: TARS, and anyone reading
over its shoulder

## Overview

`TARS_RULES.md` is the ruleset. `OPTIONS_EDUCATION.md` is the options textbook.
This file is one level further down: how a stock exchange, an order, a price,
and an index actually work mechanically — the plumbing that both of those
other files assume the reader already understands.

---

## 1. What a stock exchange actually is

An exchange (NYSE, Nasdaq, and dozens of smaller ones) is not a single physical
place where trades happen anymore — it's a matching engine. Buyers submit
**bids** (the price they'll pay), sellers submit **asks/offers** (the price
they'll take), and the exchange matches compatible orders. The **bid-ask
spread** — the gap between the best bid and best ask — is the toll for
trading immediately rather than waiting for a better price; it widens when
liquidity is thin (this account watched it happen live today: NAVI's spread
blew out right at the close, T's option spread widened as volume thinned into
Friday's expiry).

**Consolidated tape**: a stock doesn't trade on just one exchange. Trades
across all venues get reported to a single consolidated feed (SIP), which is
where "the price" of a stock actually comes from — not any one exchange's
own book.

### Order types, what they actually promise

| Order type | Promises | Does NOT promise |
|---|---|---|
| **Market** | Fills immediately | The price — you get whatever the book offers right now |
| **Limit** | The price (or better) | That it fills at all — it can sit unfilled forever |
| **Stop** | Becomes a market order once the trigger price trades | The fill price after triggering — it can gap past the trigger |
| **Stop-limit** | Becomes a limit order once triggered | That it fills — same risk as any limit in a fast market |

This is the exact reasoning behind R5 (limit orders for entries, stop-market
for exits) and `options.md` §4's "a stop is best-effort, not a floor" — both
rules are just this table applied to real money.

### Market makers and liquidity

A **market maker** commits to continuously quoting both a bid and an ask,
profiting from the spread in exchange for providing liquidity — someone to
trade with even when no organic buyer/seller is currently present. Thin
volume (a small-cap, after-hours, or the last minute before close, all
observed on this account today) means fewer market makers actively quoting
tight markets, which is mechanically *why* spreads widen exactly when it
feels riskiest to trade.

---

## 2. Indices — what they actually are, and aren't

An index like the **S&P 500**, **Nasdaq-100**, or **Dow Jones** is not a fund
you can buy directly — it's a formula. An index fund (SPY tracks the S&P 500,
QQQ tracks the Nasdaq-100) is a real, tradeable product built to replicate
that formula's return.

- **Market-cap weighted** (S&P 500, Nasdaq-100): each company's influence on
  the index is proportional to its total market value (share price × shares
  outstanding). A handful of the largest companies can move the whole index
  more than dozens of smaller ones combined — "the market was up today" can
  mean five mega-caps rallied while most stocks fell.
- **Price weighted** (Dow Jones Industrial Average): a stock's influence is
  proportional to its *share price* alone, regardless of company size — a
  $500 stock moves the Dow more than a $2,000 market-cap-larger stock trading
  at $50. This is a historical quirk (the Dow predates modern computing) more
  than a design choice anyone would pick today.
- **Sector indices / sector ETFs** (XLE for energy, XLF for financials, etc.)
  slice the market by the same sector classification this account's own
  scanner uses (`FILTER_TYPE_SECTOR`) — this is why the sector-concentration
  finding earlier today (5 of 8 positions in Communication Services) is a
  real, quantifiable risk category and not a vibe.

**Benchmark-relative thinking**: a stock up 5% in a week the S&P was up 6% has
actually *underperformed*, even though the raw number looks positive. This
account's own `paper/benchmark.py` exists specifically to catch this — the
account's earlier NANC-strategy lesson (real gains that turned out to just be
beta, not skill) is this exact mistake, made and corrected once already.

---

## 3. What actually moves prices, in order of how directly

1. **Company-specific news** — earnings, guidance, an upgrade/downgrade, an
   FDA decision, a contract win. The most direct driver, and the reason R2
   checks earnings dates before ever entering a position.
2. **Sector-wide moves** — one company's news (or macro data specific to a
   sector, like oil inventory reports for energy) drags peers with it, because
   investors reprice the whole group's assumptions at once. Today's live
   example: SentinelOne's earnings-adjacent pop dragged the entire
   cybersecurity group up together, TENB included, without TENB having its
   own news that morning.
3. **Macro data** — Fed rate decisions, CPI (inflation) prints, jobs reports,
   GDP. These move nearly everything simultaneously because they change the
   backdrop every company operates in (borrowing costs, consumer spending
   power, corporate margins). `options.md` §0 step 4 exists because a clean
   single-stock thesis can still lose to a bad macro week.
4. **Flows and positioning** — index rebalancing (a stock added to or removed
   from the S&P 500 forces funds tracking it to buy/sell regardless of
   opinion), quarterly options expiration effects, large fund
   repositioning. Not driven by any new information at all — pure
   mechanical buying/selling pressure.

### The Federal Reserve, briefly

The Fed sets the **federal funds rate** — the rate banks lend to each other
overnight — which ripples out to mortgage rates, credit card APRs, and the
"risk-free" rate every other asset gets priced against. Higher rates make
borrowing more expensive (pressures growth-stock valuations, which rely on
future earnings discounted back to today) and make safe bonds relatively more
attractive versus stocks. Lower rates work in reverse. Fed decisions land on
a published schedule (FOMC meetings, roughly every 6 weeks) — this is
exactly the kind of scheduled macro event `options.md` §0 step 4 says to
check independent of any single stock's own news.

---

## 4. Corporate actions that change what a position actually is

- **Stock splits**: a company divides each share into more shares at a
  proportionally lower price (a 2-for-1 split turns one $100 share into two
  $50 shares) — the total position value is unchanged, only the share count
  and per-share price. `lumibot`'s own `BACKTESTING_ARCHITECTURE.md` and this
  account's own research repeatedly flag unadjusted historical data as a
  source of fake gains/losses around split dates — the same caution applies
  live: a sudden 50%+ "move" that doesn't match any news is worth checking
  for a split before treating it as signal.
- **Dividends**: a cash payment per share, on a scheduled **ex-dividend
  date** — the stock's price mechanically drops by roughly the dividend
  amount on that date (the company is literally worth less cash after paying
  it out), which is not a "loss," just an accounting reality easy to
  mis-read as one.
- **Buybacks**: a company repurchases its own shares, reducing shares
  outstanding — mechanically increases earnings-per-share (same profit,
  fewer shares) without the company actually growing.
- **Mergers/acquisitions**: can force a position to convert into cash, a
  different company's stock, or a mix — worth knowing if a held name is ever
  the subject of takeover talk.

---

## 5. Short selling and short interest

Selling short means borrowing shares and selling them, betting the price
falls so they can be bought back cheaper later and returned. It flips the
long option's own asymmetry from §1's options table on its head: max profit
is capped (the stock can only fall to zero), max loss is theoretically
unlimited (the stock can rise forever) — the mirror image of a covered call's
risk, and the reason short selling is a fundamentally different risk shape
than anything in this account's current playbook.

**Short interest** (the percentage of a stock's float currently sold short)
matters because of **short squeezes**: if a heavily-shorted stock rises, short
sellers facing mounting losses are forced to buy back shares to close their
position, and that forced buying itself pushes the price higher, which
forces more covering — a positive feedback loop that can produce moves far
larger than any fundamental news would predict on its own.

---

## 6. Trading halts and circuit breakers

- **Single-stock halts**: an exchange pauses trading in one name, usually
  pending material news (an earnings surprise, an FDA decision, a merger
  announcement) so the market can digest it before trading resumes —
  designed to prevent a stale price from trading while real news is still
  unpriced.
- **Market-wide circuit breakers**: if the S&P 500 falls 7%, 13%, or 20% in a
  session, trading halts market-wide for a set period (or the rest of the
  day at 20%) — a mechanical brake distinct from any single stock's own
  halt rules, and one no options or equity position in this account is
  exempt from if it's ever triggered.

---

## 7. Extended hours — what's actually different

- **Pre-market** (before 9:30am ET) and **after-hours** (after 4:00pm ET)
  trading exist, but with a fraction of regular-hours volume and far wider
  spreads — exactly the mechanism behind today's NAVI order landing right at
  the close with an unusually wide bid/ask.
- Stop and market orders generally do not execute outside regular hours on
  this account (R5's own note, and confirmed live today when the NAVI limit
  order came back `queued` rather than filled at exactly 20:00 UTC) — only
  a marketable limit order in an extended-hours-enabled session would.
- Earnings are very commonly released before the open or right after the
  close specifically so the market has a session boundary to digest the
  news — which is exactly why `options.md` §0 step 5 checks the earnings
  date against the option's life, not just against "today."

---

## 8. How this connects back to the account's own rules

Every rule in `TARS_RULES.md` is downstream of something in this file:

- **R2's trend filter** exists because sector and macro moves (§3) can lift
  or sink a stock regardless of its own merits — riding with the tide (above
  its 200d/50d MA) is a bet the prevailing macro/sector wind, whatever it is,
  keeps blowing a little longer.
- **R2's earnings check** and `options.md`'s macro-calendar step both come
  straight from §3's ranked list of what actually moves prices — company
  news first, because it's the most direct and the most controllable to
  check for.
- **R12 (no fractional shares)** is a direct collision with §1's order-type
  table: Robinhood's fractional-share mechanics simply don't support the
  stop-order type this account requires for every position.
- **The sector-concentration finding** (5 of 8 in Communication Services)
  is §2's benchmark logic applied to this account's own book instead of to
  an index.
