# Trading Psychology — Why the Rules Exist

The behavioral-finance research behind why a mechanical ruleset beats
discretion on this account specifically, with today's own incidents as the
receipts. Every claim below is sourced, not remembered — this file exists so
"why does R4 work that way" has a real answer instead of a vibe.

Last Updated: 2026-09-15 · Status: active · Audience: TARS, and Nolan when the
rules feel arbitrary

## Overview

`MARKET_MECHANICS.md` explains how the market works. `OPTIONS_EDUCATION.md`
explains how options work. Neither explains why a person operating either one
correctly still loses money — that gap is the account holder's own psychology,
and it is the single best-studied problem in finance. This file names the
five biases that showed up **today, on this account, in this session** and
the actual research behind each one, so the next time one shows up it gets
recognized instead of rationalized.

## 1. Loss aversion — losses hurt about twice as much as gains feel good

Kahneman and Tversky's prospect theory found responses to losses are
consistently stronger than to equivalent gains; experimental estimates of the
loss-aversion coefficient (λ) cluster **1.5–2.5, with 2.0 as the canonical
value** — losing $100 hurts roughly twice as much as gaining $100 feels good.
[Cogn-IQ: Loss Aversion](https://www.cogn-iq.org/learn/theory/loss-aversion/) ·
[NN/G: Prospect Theory](https://www.nngroup.com/articles/prospect-theory/)

**Today's receipt:** the F $14.50 put lost $6 and got closed calmly. But the
two follow-on legs — opened in the ten minutes right after, while the session
was disconnected — were opened with no thesis at all. That sequence (a real
loss, followed immediately by two new unresearched positions) is the textbook
signature of loss aversion pushing toward action to *undo* the feeling of a
loss rather than toward a good next decision. The size of the follow-on
mistake ($4 more, on two coin-flip legs) was smaller than the original loss
only by luck, not by process.

## 2. The disposition effect — selling winners early, holding losers long

Shefrin and Statman named this in their 1985 *Journal of Finance* paper: the
tendency to sell winning positions too early and ride losing ones too long,
driven by loss aversion, mental accounting against the purchase price, regret
avoidance, and a self-control failure.
[Shefrin & Statman, *J. Finance* 40(3), 777–790](https://www.researchgate.net/publication/294684138_The_disposition_to_ride_winners_too_long_and_sell_losers_too_soon_Theory_and_evidence)

**Today's receipt:** the ask to sell WBD/SIRI/PFE/S because they "aren't
moving at all" — every one of them was down under 1%, nowhere near its stop,
still passing R2 — is the mirror image of the disposition effect: not selling
a winner early, but wanting to sell a *quiet, still-valid* position early
because a big winner (TENB, +14%) made everything else look boring by
comparison. R4 exists precisely to remove this decision from the account
holder's hands: no fixed target, trail only, ride until the trend actually
breaks. Jesse Livermore's own line on this, from *Reminiscences of a Stock
Operator*: **"It was never my thinking that made the big money for me. It
was always my sitting."**
[Full quote and context](https://www.getrichslowly.org/reminiscences-of-a-stock-operator/)

## 3. Overconfidence and overtrading — activity is not a strategy

Barber and Odean's 2000 *Journal of Finance* study, "Trading Is Hazardous to
Your Wealth," tracked 66,465 households from 1991–1996: the most active
traders earned meaningfully lower net returns than buy-and-hold investors,
with **gross returns nearly identical across groups** — the entire gap came
from transaction costs and the accumulated cost of poorly timed decisions,
traced to overconfidence in one's own edge.
[Barber & Odean, *J. Finance* 55(2), 773–806](https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/individual_investor_performance_final.pdf)

**Today's receipt:** "fill the books," "just use it tars we need movement,"
and the reserve-dip pushes are the exact behavior this study measured —
wanting a trade to exist rather than waiting for a real one. The account's
own rules (R2's four conditions, R3's cash floor) are a mechanical stand-in
for the discipline this research says most people don't have without one.

## 4. Social proof and herding — "my friend's AI is up 20%"

A CFA Institute survey identified herding as **the single most significant
behavioral bias**, affecting an estimated 34% of investment decisions. Social
proof works hardest exactly when the right answer is ambiguous and the stakes
feel high — which describes almost every options decision on a small account.
[Fidelity: The Power of Social Proof](https://www.fidelity.com.au/insights/education/behavioural-finance-the-power-of-social-proof/) ·
[herding survey figure via CFA Institute, cited](https://study.com/academy/lesson/herd-behavior-and-investment-in-financial-markets.html)

**Today's receipt:** the repeated "my friend's AI is up 20%, same
parameters" pitch is social proof in its purest form — a real, checkable
number (someone else's account) used as evidence for a decision with none of
the underlying facts (their sizing, their account size, whether it survived
its next trade) actually checked. `reference/options.md` already logged this
exact pattern once (the AAPL research entry); it is the single most repeated
argument-shape this session, which is itself informative.

## 5. What separates the traders who actually last

Jack Schwager's *Market Wizards* interviews, across very different styles,
converge on the same handful of traits: **capital preservation over any
single win, mechanical adherence to a system regardless of how it feels in
the moment, and the flexibility to be wrong and change course without ego.**
The book's own conclusion is not a secret edge — it's "solid methodology plus
a disciplined mental approach," applied consistently.
[CFA Institute: What Makes a Great Trader?](https://rpc.cfainstitute.org/blogs/enterprising-investor/2014/what-makes-a-great-trader-an-interview-with-jack-schwager)

John Bogle's version of the same idea, aimed at a buy-and-hold investor
rather than a trader: **"Time is your friend; impulse is your enemy,"** and
his Cost Matters Hypothesis — "the miracle of compounding returns is
overwhelmed by the tyranny of compounding costs" — is the reason
`paper/benchmark.py` exists at all: a strategy has to beat the index net of
its own costs and mistakes, not just post a green number.
[Bogle quotes](https://www.dividendpower.org/john-bogle-quotes/)

## How this maps back to the actual rules

| Bias | Rule that exists to blunt it |
|---|---|
| Loss aversion (revenge-trading after a loss) | R6's circuit breaker: 2 stop-outs in 5 days halts new entries for 3 |
| Disposition effect (selling quiet winners, holding hope on losers) | R4: no fixed target, hard stop is symmetric and mechanical either way |
| Overconfidence / overtrading | R2's four hard conditions + R3's cash floor — no trade without a real signal, no matter how much action feels warranted |
| Social proof / anecdote pressure | `options.md` section 0's 8-step protocol — a pitch has to survive real research, not just a compelling story |
| No system, no discipline (the Schwager/Bogle finding) | The entire existence of `TARS_RULES.md` — mechanical because discretion is the thing the research says fails |

None of this is a claim that TARS is immune to these biases — a mechanical
ruleset is a structure for catching them, not a personality that doesn't have
them. The F strangle happened *inside* this same system, during a gap in
supervision, which is itself the data point: the rules work when they're
being checked against, and today's real gaps (NAVI's missing stop, the
disconnected-session strangle) are exactly where checking briefly stopped.
