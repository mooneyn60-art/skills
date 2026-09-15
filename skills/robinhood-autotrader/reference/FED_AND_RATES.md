# The Fed and Interest Rates — the Mechanics Behind Tomorrow's Decision

`MARKET_MECHANICS.md` gave the Fed one paragraph. This is timely enough to
deserve its own file: FOMC decides tomorrow, 2pm ET, ~93% priced for a hike.
Sourced, not recalled.

Last Updated: 2026-09-15 · Status: active · Audience: TARS, ahead of a real
scheduled event this account is exposed to

## Overview

Every trade thesis logged today mentioned "Fed hike odds" or "10-year yield"
without ever explaining the actual mechanism connecting a Fed vote to a stock
price. This closes that gap, timed to matter: tomorrow's decision is a real
input to every position in this book, not an abstraction.

## The Fed doesn't just "set" a rate — it enforces a band mechanically

The federal funds rate is what banks charge each other for overnight loans.
The FOMC doesn't dictate an exact number, it targets a **range** and holds
the real, traded rate inside it using a floor-and-ceiling system:

- **The floor:** interest on reserve balances (IORB) — what the Fed pays
  banks to park cash with it overnight. No bank lends cash for less than it
  can risklessly earn parking it at the Fed instead. Non-bank lenders (money
  market funds) get the same floor via the **overnight reverse repo
  facility (ON RRP)** — the Fed borrows their cash overnight at a set rate,
  which stops market rates from leaking below the target band.
- **The ceiling:** the **standing repo facility** — the Fed will lend cash
  overnight against safe collateral, capping how high overnight rates can
  spike.
- The Fed's own trading desk runs both operations most business days to keep
  the *actual* traded rate inside the announced band, not just publish a
  number and hope.

[NY Fed: Repo and Reverse Repo Agreements](https://www.newyorkfed.org/markets/domestic-market-operations/monetary-policy-implementation/repo-reverse-repo-agreements) ·
[GovFacts: How the Fed Sets Interest Rates](https://govfacts.org/money/broader-economy/monetary-fiscal-policy/how-the-federal-reserve-sets-interest-rates/)

## The dot plot — what tomorrow's real surprise risk actually is

The rate decision itself (a quarter-point hike) is **already priced at 93%**
— not the real source of volatility. What moves markets is the **Summary of
Economic Projections (SEP)**, published quarterly (March, June, September,
December), which includes the "dot plot": up to 19 anonymous FOMC
participants each mark where they think the fed funds rate should sit at the
end of each of the next few years, plus a "longer run" neutral estimate.

**This is why tomorrow is a two-part event, not one:** the hike itself is
close to fully priced, but whether the dot plot shows *more* hikes coming
before year-end is the part with real information content — it's the
difference between "this was an isolated adjustment" and "this is the
opening move of a real tightening cycle." The SEP also carries the Fed's own
inflation, growth, and unemployment forecasts, which frame *why* the dots
moved wherever they moved.
[Federal Reserve: Anchored to the Dot Plot](https://www.federalreserve.gov/econres/feds/anchored-to-the-dot-plot-central-bank-projections-and-interest-rate-expectations.htm) ·
[Fidelity: What Is the Fed's Dot Plot?](https://www.fidelity.com/learning-center/trading-investing/federal-reserve-dot-plot)

## QE and QT — the other lever, working through the balance sheet, not the rate

Separate from the fed funds rate itself, the Fed can expand or shrink its own
balance sheet:

- **Quantitative easing (QE):** the Fed creates reserves to buy Treasuries
  and mortgage-backed securities, pushing down *longer-term* rates directly
  (the fed funds rate only really controls the short end) and injecting
  liquidity — used to stimulate when short rates are already near zero.
- **Quantitative tightening (QT):** the reverse — letting bonds roll off the
  balance sheet without reinvesting (or selling them), pulling liquidity out
  and letting long-term rates drift up.

Simple framing: **the fed funds rate is the accelerator/brake pedal, QE/QT
is the size of the engine itself.** [CBO: How QE Affects the Federal Budget](https://www.cbo.gov/publication/58457) ·
[Congress.gov: The Fed's Balance Sheet and QT](https://www.congress.gov/crs-product/IF12147)

## Why a hike actually hurts stock prices — the mechanism, not just "rates up, stocks down"

Two separate channels, both real:

1. **The discount-rate channel.** A stock's price is (roughly) the present
   value of its future cash flows, discounted back to today. Raise the
   discount rate and every future dollar is worth less today — hitting
   longest-duration cash flows hardest, which is exactly why high-growth,
   long-payback names (unprofitable tech, biotech) fall more than value
   names on the same rate move. This is the same mechanism `MARKET_MECHANICS.md`
   gestures at and `FUNDAMENTAL_ANALYSIS.md`'s moat discussion assumes.
2. **The competing-asset channel.** When risk-free Treasuries yield 5%
   (today's real level, highest since 2007), investors need a much better
   reason to hold a riskier stock instead — every equity is now competing
   against a genuinely attractive, safe alternative in a way it wasn't at
   near-zero rates.

**What history actually says about the first hike of a cycle** (LPL
Financial, studying six tightening cycles since 1994, cited in today's own
news flow): stocks post **negative average returns in each of the first four
months** after a first hike, but **average +6.7%/median +10.7% a year
later** — rate hikes historically don't end bull markets on their own; it's
whether a hike arrives *with* recession risk that decides the outcome. 2022
(hike into already-high inflation, 25% drawdown) is the bad-outcome
precedent; 1997 (hike absorbed by a real growth story, +42% a year later) is
the good-outcome one. Which one this looks like depends on tomorrow's growth
and inflation projections, not the hike itself.

## What this means for tomorrow, mechanically, for this book

- The hike itself is nearly fully priced — the dot plot and Warsh's press
  conference (2:30pm ET, 30 minutes after the decision) are where real
  volatility is more likely to show up.
- R4's stops are triggers, not prices — if something gaps on the
  announcement, the stop fires and fills at whatever the market gives it,
  not at the stop level. That's not a defect to fix, it's what a stop is
  (`MARKET_MECHANICS.md`'s order-type table, same finding).
- Long-duration, growth-flavored names in this book (TENB especially, given
  tonight's run) are mechanically more rate-sensitive than the
  defensive-leaning names (VZ, T, PFE) by the discount-rate channel above —
  worth knowing which positions are more exposed to tomorrow's surprise, not
  a reason to act on it tonight.
