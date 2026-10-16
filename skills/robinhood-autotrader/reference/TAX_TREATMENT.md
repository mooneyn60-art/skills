# US Tax Treatment of Active Equity and Options Trading

Sourced IRS rules underneath the "specified-lot selling" and "minimize
realized gains" practices this repo already recommends elsewhere, applied to
an account that has so far made exclusively short-term trades.

Last Updated: 2026-09-16 · Status: active · Audience: TARS, account owner —
general education, not tax advice

## ⚠️ Not tax advice — read this before anything else

**This file is general education about how US federal tax law treats active
trading. It is not tax advice, it is not personalized to anyone's situation,
and it must not be used as the sole basis for a real filing decision.** Tax
law changes (rates, thresholds, and forms are adjusted most years), state tax
treatment varies and is not covered here at all, and how these rules apply to
a specific person depends on facts this document has no way to know —
trader-tax-status eligibility, other income, filing status, what else is in
the household's accounts, and more. **Consult a real CPA or tax attorney
before making a filing decision based on anything below.** Every claim here
is sourced to a real, checkable reference; none of it is a substitute for
that conversation.

## Overview

Account #731951265 has made exclusively short-term trades — every position
opened and closed within days, per `TARS_RULES.md`. `paper/PROTOCOL.md`
already recommends "specified-lot selling" and minimizing realized gains as
good practice, and `live-mcp-architecture.md` documents the FIFO-vs-specified-lot
cost-basis mechanics for stops in detail. Neither file explains *why* those
practices matter — the actual IRS rules underneath them. This file closes
that gap: holding-period tax treatment, the wash sale rule (and how this
account's own stop-and-re-entry pattern could trigger it), lot-selection
rules, whether equity options get the same 60/40 blended treatment as index
options and futures (they do not), and what a trader in this position
actually needs to keep for tax time.

## 1. Short-term vs. long-term capital gains — and why this account should assume ordinary rates on everything

The holding-period line is exact and IRS-stated: **hold an asset one year or
less and any gain or loss is short-term; hold it more than one year (at least
a year plus a day) and it's long-term.** The holding period starts the day
*after* acquisition and ends on the date of sale.

- **Short-term gains are taxed as ordinary income** at the same graduated
  federal brackets (10%–37% for 2025/2026) as wages — there is no
  preferential rate at all.
- **Long-term gains get preferential rates** — 0%, 15%, or 20% depending on
  taxable income, with some exceptions (collectibles, certain small-business
  stock) taxed higher.
- The gap is not trivial: a $50,000 gain taxed at a 32% ordinary bracket
  instead of the 15% long-term rate is an $8,500 difference in tax owed on
  the *same dollar gain*, purely because of holding period.

[IRS Topic no. 409, Capital gains and losses](https://www.irs.gov/taxtopics/tc409) ·
[NerdWallet: 2025 and 2026 Capital Gains Tax Rates and Rules](https://www.nerdwallet.com/taxes/learn/capital-gains-tax-rates) ·
[Kiplinger: Capital Gains Tax Rates 2025 and 2026](https://www.kiplinger.com/taxes/capital-gains-tax/602224/capital-gains-tax-rates)

**Why this account specifically should model every gain as ordinary income,
not "capital gains":** every logged trade so far — TARS-1 equity swings,
the F options legs, RUM — has been opened and closed within days, nowhere
close to the one-year threshold. There is no partial credit for holding "a
while": one day past a year qualifies for long-term treatment, 364 days does
not, full stop. Until a position is actually held past that threshold, the
correct planning assumption is **ordinary income rates on the full gain**,
not the more favorable capital-gains number a casual reader might mentally
default to. This also means realized short-term gains stack on top of
whatever else is taxed as ordinary income (wages, etc.) and can push the
marginal rate on those gains higher than a quick mental estimate would
suggest.

## 2. The wash sale rule — mechanics, and how this account's own book could trigger it

**The rule (IRC §1091, detailed in IRS Publication 550):** if you sell a
security at a loss and, within a 61-day window — 30 calendar days before the
sale, the day of the sale itself, and 30 calendar days after — you buy the
same or a "substantially identical" security (or a contract/option to buy
one), the loss is disallowed for that tax year.

- **The loss is deferred, not destroyed.** The disallowed loss is added to
  the cost basis of the replacement shares, which lowers the eventual gain
  (or increases the eventual loss) whenever those replacement shares are
  finally sold for good. Example: sell stock at a $250 loss, buy substantially
  identical stock within 30 days for $800 — the new cost basis becomes
  $1,050 ($800 + the $250 disallowed loss), and the replacement position's
  holding period for the deferred amount effectively carries forward.
  **Exception:** if the replacement purchase happens inside an IRA/Roth IRA,
  the basis step-up does not apply (Rev. Rul. 2008-5) — the loss is
  effectively lost for good, not deferred.
- **"Substantially identical" is not limited to the literal same ticker.**
  Per Fairmark's options-focused analysis of the rule and IRS guidance, an
  **option or contract to buy the stock counts** — e.g., selling a stock at
  a loss and then buying a deep in-the-money call on that same stock within
  the window can wash the stock loss, because the option is treated as
  substantially identical to the underlying. Two options with the same
  underlying, strike, and expiration are unambiguously substantially
  identical to each other. The IRS has never published a bright-line
  numerical test for how close a strike/expiration has to be to count for
  option-vs-option or option-vs-stock comparisons — it's facts-and-circumstances.
- **The rule follows the taxpayer, not the account.** It legally applies
  across *all* accounts a person controls — a different broker, an IRA, even
  a spouse's account if filing jointly — but **brokers are only required to
  track and report wash sales within a single account under the same CUSIP**.
  Nothing stops a broker's 1099-B from looking clean while a wash sale
  technically occurred across two accounts; that reconciliation is the
  taxpayer's responsibility, not something the 1099-B guarantees.

[Fidelity: Wash-Sale Rules — Avoid this tax pitfall](https://www.fidelity.com/learning-center/personal-finance/wash-sales-rules-tax) ·
[Kiplinger: The Wash Sale Rule — What It Is and How to Avoid It](https://www.kiplinger.com/taxes/604947/stocks-and-wash-sale-rule) ·
[Fairmark: Wash Sales and Options](https://fairmark.com/investment-taxation/capital-gain/wash/wash-sales-and-options/) ·
[Mezzi: The Wash Sale Rule Follows You Everywhere. Your Broker Won't.](https://www.mezzi.com/blog/avoid-wash-sales-across-accounts)

**A concrete way this could already be happening on this account's own
book.** `trades.jsonl` shows a real pattern that is exactly the wash-sale
setup: a position is stopped out at a loss (R4 hard stop), and the strategy
or the user later re-enters the same name on a fresh signal. Two examples
already logged:

- **RUM**: opened 2026-09-14, stopped out 2026-09-15 for a **-$3.77 realized
  loss** (`R4_hard_stop`, corrected record `2026-09-15-RUM-EXIT-LIVE-CORRECTION`).
  If TARS re-signals RUM and the account re-enters *any* RUM position — stock
  or an option on RUM — before **2026-10-15** (30 calendar days after the
  stop), that RUM loss is a wash sale: the -$3.77 loss is disallowed for this
  tax year and rolled into the new position's cost basis instead.
- **F (Ford) options, 2026-09-15**: the account held a put spread/strangle-ish
  structure across multiple strikes and closed several legs at a loss the
  same day (`2026-09-15-F-P14.5...`, `-F-P14-0918-USER-EXIT` at -$1.00,
  `-F-C13.5-0918-USER-EXIT` at -$3.00 — total -$10 across three F-options
  legs per that record's own note). Because the wash-sale test is
  "substantially identical," not "identical contract," a put closed at a
  loss on one F strike/expiration followed within 30 days by acquiring a
  call or a different put on F **could** be scrutinized as substantially
  identical depending on strike/expiration proximity — the IRS gives no
  bright line here, which is exactly why the ambiguity matters for a book
  that trades the same handful of names repeatedly.

Nothing in `TARS_RULES.md` or `STRATEGY.md` currently encodes a wash-sale-aware
cooldown after a losing stop-out in the same symbol — the re-entry logic is
governed by signal freshness, not by whether the prior exit in that name was
a loss inside the trailing 30 days. That is a real gap between the trading
logic and the tax consequences of the trading logic, worth flagging even
though fixing it is a strategy-design decision, not something this file
should mandate.

## 3. Specified-lot vs. FIFO cost basis — the IRS rules behind the practice already documented

- **Default method is FIFO** (first-in-first-out) unless the taxpayer
  affirmatively elects and executes a different method. IRS and brokerage
  defaults both fall back to FIFO absent a specific identification.
- **Specific identification ("spec ID") is allowed, but only if done
  correctly and at the time of the trade.** The taxpayer must identify which
  lot is being sold *before or at the time of the sale* (not after the fact
  at tax time), and the broker must confirm that identification in a written
  record (electronic trade-ticket confirmation satisfies this for most
  retail brokers). Without that contemporaneous confirmation, the position
  reverts to FIFO by default.
- **The election is effectively locked in once the trade settles.** In
  practice this means the lot-selection window closes at settlement (T+1 for
  US equities since the 2024 move to T+1) — after that point the disposal
  method for those specific shares cannot be changed retroactively, including
  at tax-filing time. Multiple broker help-center sources (Fidelity, Schwab)
  describe changing the *account-level default* method going forward, but
  changing which lot was actually sold on an already-settled trade is not
  something the IRS specific-identification rule permits after the fact.

[Green Trader Tax: FIFO vs. Specific Identification Accounting Methods](https://greentradertax.com/fifo-vs-specific-identification-accounting-methods/) ·
[Fidelity: Trading Specific Shares (Help)](https://www.fidelity.com/webcontent/ap002390-mlo-content/19.09/help/learn_trading_specific_shares.shtml) ·
[Charles Schwab: Save on Taxes — Know Your Cost Basis](https://www.schwab.com/learn/story/save-on-taxes-know-your-cost-basis)

**How this connects to what `live-mcp-architecture.md` already documented.**
That file's "Cost basis: the position endpoint is not the tax lot" section
found, empirically, that (1) a broker's displayed blended average cost can
diverge sharply from the actual remaining tax lot after a partial sell, (2)
FIFO and a tax-efficient specified-lot choice can produce a materially
different realized P&L on the exact same exit (its own example: -$4.97
blended vs. -$3.50 actual FIFO, a 30% difference), and (3) **stop orders
reject the `tax_lots` parameter entirely at the API layer** — a resting stop
can never be told to sell a specific lot, it always liquidates oldest-lot-first.
The tax rule explains *why* that constraint matters: FIFO is not just "a"
accounting convention, it is the *IRS-default* method, so every stop-out on
a multi-lot position is, as a matter of law and not just broker plumbing,
locking in whichever gain or loss the oldest lot happens to carry — with no
after-the-fact way to elect a better lot once the stop has filled and
settled. The only lever available is choosing the lot *before* a manual
limit/market exit; a stop, by construction, forecloses that choice.

## 4. Section 1256 contracts vs. equity options — equity options do NOT get 60/40 treatment

This is the section most likely to be misread, so it is stated plainly:

**Standard equity options — including the long calls/puts on individual
stocks this account would eventually be allowed to trade under a higher
options tier — get NO special blended tax treatment. They are taxed exactly
like the underlying stock: ordinary short-term rates if the option (or the
stock received via exercise/assignment) was held one year or less, long-term
rates only if held more than a year.** There is no 60/40 split for them.

- **Section 1256 contracts** (regulated futures contracts, foreign currency
  contracts, "non-equity options," dealer equity options, and dealer
  securities futures contracts) get an automatic **60% long-term / 40%
  short-term blend on every gain or loss, regardless of actual holding
  period**, plus mark-to-market treatment (open positions are treated as sold
  at fair value on the last business day of the tax year, reported on IRS
  Form 6781).
- **"Non-equity option" is an IRS-defined term, per Publication 550: any
  listed option that is not an equity option** — this covers debt options,
  commodity futures options, currency options, and **broad-based stock index
  options** (e.g., SPX, NDX, RUT, XSP — cash-settled options on an index the
  SEC has determined is broad-based). Those get the 60/40 treatment.
- **Options on individual stocks and on non-broad-based ETFs are "equity
  options" by the same IRS definition and are explicitly excluded from
  Section 1256** — no 60/40, no mark-to-market. A long call or put on a
  single name like the F options already traded on this account is taxed the
  ordinary way: gain/loss on the option itself is short-term unless the
  option was held over a year, and if it's exercised, the option's cost
  basis rolls into the resulting stock position's basis with the stock's own
  new holding period starting fresh at exercise.

[IRS Publication 550 (2025), Investment Income and Expenses](https://www.irs.gov/publications/p550) ·
[TaxSlayer: What are Section 1256 Contracts? (Form 6781)](https://support.taxslayer.com/hc/en-us/articles/360017749751-What-are-Section-1256-Contracts-Form-6781) ·
[IRS Form 6781 (2025): Gains and Losses From Section 1256 Contracts and Straddles](https://www.irs.gov/pub/irs-pdf/f6781.pdf) ·
[TradeLog: How TradeLog Defines Section 1256 Non-Equity Options](https://tradelog.com/education/section-1256-non-equity-options/)

**Why getting this wrong would be a real, harmful error:** it is common
(and understandable) to hear "options get special 60/40 tax treatment" as a
blanket statement, because it's true for *index* options and futures, which
are heavily discussed in trading-tax content. Applying that blanket
statement to a single-stock option — which is what R9-tier trading on this
account would actually be — would misstate every gain as 60% long-term when
none of it qualifies for that treatment at all. The determining factor is
not "is it an option" but "is the underlying a broad-based index (1256) or
an individual equity/non-broad-based ETF (ordinary short/long-term rules)."

## 5. Practical bookkeeping — what tax time actually needs, and what `trades.jsonl` does and doesn't capture

**What a trader in an account like this needs at filing time:**

- **Form 1099-B** from the broker — the broker's own record of proceeds,
  cost basis (when known to the broker), and short/long-term characterization
  for each sale during the year. This is the starting point the IRS expects
  a return to reconcile against.
- **Form 8949** — every individual sale listed with description, date
  acquired, date sold (or "Various" for a multi-date lot), proceeds, cost
  basis, and any adjustment code/amount (e.g., a wash-sale disallowance uses
  code "W" and a positive adjustment in column (g)).
- **Schedule D** — the summary of all Form 8949 totals (short-term and
  long-term separately), which flows into the Form 1040 tax computation.
- For anyone trading Section 1256 contracts (not applicable to this account
  today, since it trades single-name equities and equity options, not
  broad-based index products) — **Form 6781** for the 60/40 split and
  mark-to-market.

[H&R Block: What Is IRS Form 1099-B?](https://www.hrblock.com/tax-center/irs/forms/1099-b/) ·
[IRS: 2025 Instructions for Form 8949](https://www.irs.gov/pub/irs-pdf/i8949.pdf) ·
[TradeLog: IRS Form 8949 & Schedule D Guide for Active Traders](https://tradelog.com/education/form-8949/)

**What `paper/trades.jsonl` already captures, mapped to those forms:**

| Tax-form need | Present in `trades.jsonl`? |
|---|---|
| Symbol / description | Yes — `symbol`, `instrument`, `contract` (strike/expiration for options) |
| Date acquired / date sold | Yes — `opened` / `closed` timestamps |
| Realized gain or loss | Yes — `realized_pnl` |
| Proceeds and cost basis separately (not just net P&L) | **No** — only net `realized_pnl` is logged, not the actual `entry`×`qty` cost and `exit`×`qty` proceeds as separate figures the way Form 8949 columns (d) and (e) require (though `entry`/`exit`/`qty` fields mean those can be *derived*, they are not stored as the form expects) |
| Which specific lot was sold (for a multi-lot position) | **No** — the ledger records aggregate `qty` and blended `entry`, not per-lot identification; it inherits the same FIFO-vs-blended ambiguity `live-mcp-architecture.md` already flagged at the broker level |
| Wash-sale flags / disallowed-loss tracking | **Partial** — as of `TARS_RULES.md` R8 (2026-09-16), a re-entry within 30 days of a same-symbol loss gets `"wash_sale_flag": true` and the id of the loss it washes against at the point of logging. This marks the record; it still does not check "substantially identical" instruments (e.g. an option vs. the underlying, or two different strikes) the way the IRS rule actually requires |
| Short-term vs. long-term characterization | Not stored explicitly, but derivable from `opened`/`closed` — moot in practice so far since every trade is a matter of days, not close to the one-year line |
| Broker-of-record 1099-B reconciliation | **No** — this is an internal research/paper ledger, not a broker tax record; the actual 1099-B from Robinhood is the authoritative source at filing time, and this ledger should never be treated as a substitute for it |

None of this is a defect in the ledger's actual purpose — `PROTOCOL.md` built
it to measure expectancy in R-multiples, not to do tax accounting, and it
does that job well. But it means **nobody should assume `trades.jsonl` is
tax-ready.** At minimum, real tax reporting for this account needs: the
broker's actual 1099-B (authoritative proceeds/basis/holding-period data),
a cross-account wash-sale review that accounts for the ambiguity in what
counts as "substantially identical" for options on the same underlying
(section 2, above), and a CPA's judgment call on anything genuinely
ambiguous — not an extension of this ledger's schema.

## Bottom line for this account

- Every trade logged so far is short-term by a wide margin — model every
  realized gain as taxed at ordinary income rates, never at the more
  favorable long-term rate, until a position is actually held past one year.
- The stop-and-re-entry pattern this book already uses (RUM, the F options
  legs) is precisely the pattern that creates wash sales — there is currently
  no rule anywhere in `TARS_RULES.md`/`STRATEGY.md` that checks for it before
  re-entering a recently-stopped-out name.
- Any single-stock option trading this account graduates into (the R9 path)
  gets **ordinary short/long-term treatment, not the 60/40 blend** — that
  blend is reserved for broad-based index options and futures, not
  individual equities.
- `trades.jsonl` is a good R-multiple ledger and an incomplete tax record;
  the broker's 1099-B, not this file, is the authoritative source at filing
  time, and a CPA should be the one connecting the two.
