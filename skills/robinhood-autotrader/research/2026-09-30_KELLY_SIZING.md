# Kelly / Fractional Kelly: is R3's 20% per-position cap right?

One-line: Does growth-optimal (Kelly) position sizing say R3's 20%-per-name
cap is far too big, far too small, or about right?

Last Updated: 2026-09-30
Status: PREDICTIONS COMMITTED (results pending this same commit's script run)
Audience: Nolan, TARS sessions
Research agenda item #10.

## Why this now

R3 caps each position at 20% of the account by judgement, never measured.
Yesterday SOFI (shares + 3 calls + puts) reached ~23% of the account and one
-4% SOFI day dragged the whole book. So the practical question isn't abstract:
is a ~20% single-name cap defensible, and does Kelly say anything about it?

## Method (stated before running)

A "trade" = enter at a month-end where close > SMA200 (R2 gate), hold with R4
exits (hard -8%, breakeven at +8%, 20% trail below highest close, 200-day
trend exit), on the same daily data used everywhere else (large caps excl.
SPY, 2006-2026; volatile names, 2006-2026). Record each RESOLVED trade's net
return (exit/entry - 1) minus a round-trip cost of 0.001 (matches the shadow
book's COST and is conservative vs the +2.7bp/side measured in item 9).
Censored (unresolved at data end) trades are excluded and counted, per RULE #1
(don't treat an open trade as closed).

From the per-trade return distribution R:
- win rate p, avg win, avg loss, payoff ratio b = avg_win / |avg_loss|
- BINARY Kelly: f = p - (1-p)/b
- CONTINUOUS Kelly: the f that maximises g(f) = mean(log(1 + f*R)), solved
  numerically. This is the growth-optimal fraction of bankroll in ONE such
  trade if it were rebet iid.
- Bootstrap CI (resample entry-MONTH clusters, per item 8's clustering) for
  the continuous Kelly: report 5th-95th percentile.
- Four hurdles: both sample halves, and drop the megacaps (NVDA, AAPL, MSFT,
  GOOGL, AMZN). A single-name cap that Kelly "justifies" only on megacaps is
  not a rule.
- Concurrency: R3 governs ONE position while several run at once. Item 4
  measured N_eff ~= 3.9 independent bets. So the portfolio can't run at
  per-name Kelly x (number of names); the per-name figure must be read
  against how many bets share the bankroll.

R14: the script prints raw numbers only, no hardcoded conclusion. R16: if a
result below refutes a prediction I stated here, the pressure state is on for
the rest of this session and nothing here is adopted; item 10 proposes, it
never adopts a rule mid-session anyway.

## Predictions (written BEFORE the script ran)

P1 MAGNITUDE. Full continuous Kelly for a single 200-day/R4 trade will point
   ABOVE 20% (I expect well above 50%, possibly >100% i.e. leverage), because
   per-trade volatility is moderate and R4 caps the left tail. So naive Kelly,
   taken literally, calls 20% CONSERVATIVE, not too big.

P2 UNCERTAINTY (the real answer). The bootstrap CI on Kelly will be very wide
   and its LOWER bound will sit at or below 0 (bet nothing), because per item
   8 no positive return edge in this repo survives the multiple-testing
   hurdle. So Kelly cannot show 20% is "too small"; its point estimate is not
   trustworthy on this sample.

P3 HALF-KELLY + CONCURRENCY. After the standard halving for estimation error
   AND dividing across the ~3.9 effective simultaneous bets, the per-position
   figure lands roughly in the 10-25% range. Conclusion I expect: 20% is in
   the right ballpark as a cap, and the thing Kelly clearly does NOT justify
   is loading >20% into a single name (the SOFI mistake).

What would REFUTE these: full Kelly point estimate coming out BELOW 20% with a
CI that excludes large values (=> 20% is too big on the point estimate), or
the half-Kelly/concurrency figure landing far outside 10-30%.

## Results

Script: `paper/research_scripts/kelly_sizing.py` (run 2026-09-30, after the
predictions above were committed at 331b301). 200d gate + R4 exits, round-trip
cost 0.001. Large caps: 2046 resolved trades (50 censored); volatile: 1552
(23 censored). Mean hold 90d (large) / 51d (volatile). Fractions are of
bankroll in ONE such position.

| Cut | n | win% | mean/trade | payoff b | binary Kelly | full cont. Kelly | boot 90% CI | half-K / N_eff(3.9) |
|---|---|---|---|---|---|---|---|---|
| Large ALL | 2046 | 32.3% | +7.4% | 6.51 | **0.219** | 2.27 | [1.74, 2.83] | 0.29 |
| Large pre-2016 | 974 | 31.1% | +5.4% | 5.62 | 0.189 | 1.71 | [1.09, 2.46] | 0.22 |
| Large post-2016 | 1072 | 33.3% | +9.1% | 7.23 | 0.241 | 2.69 | [1.97, 3.41] | 0.35 |
| Large ex-megacap | 1170 | 26.6% | +1.5% | 3.92 | **0.078** | 0.76 | [0.24, 1.28] | 0.10 |
| Volatile ALL | 1552 | 29.6% | +16.5% | 10.29 | **0.228** | 1.24 | [1.20, 2.41] | 0.16 |
| Volatile pre-2016 | 368 | 30.7% | +22.9% | 13.15 | 0.254 | 1.19 | [1.04, 2.65] | 0.15 |
| Volatile post-2016 | 1184 | 29.3% | +14.5% | 9.39 | 0.218 | 2.05 | [1.49, 2.63] | 0.26 |
| Volatile ex-megacap | 1381 | 28.0% | +13.4% | 9.28 | 0.203 | 1.23 | [1.14, 2.15] | 0.16 |

Shape of the bet: low win rate (~27-33%), large payoff ratio (b ~ 4-13). R4
makes it a lottery — small frequent losses (avg -5% to -7%, the -8% hard stop
plus the trail), rare large winners (avg +19% to +90%). That fat right tail is
what drives the continuous log-optimal Kelly so high.

Prediction scorecard:
- P1 MAGNITUDE — CONFIRMED. Full continuous Kelly 0.76-2.69 (mostly >1, i.e.
  leverage); binary Kelly ~0.20-0.25. Naive Kelly, read literally, calls 20%
  conservative, not too big. As predicted.
- P2 UNCERTAINTY — **REFUTED.** I predicted the bootstrap CI's LOWER bound
  would sit at or below 0. It does not: every month-clustered bootstrap CI
  lower bound is well above 0 (+1.74 large ALL; +0.24 even ex-megacap). The
  in-sample per-trade mean is reliably positive here, so log-optimal Kelly is
  reliably positive. My "Kelly could be zero" claim was wrong for THIS
  estimand.
- P3 HALF-KELLY + CONCURRENCY — CONFIRMED. Half-Kelly divided by N_eff 3.9
  lands 0.10-0.35 (mostly 0.15-0.29); binary Kelly itself is ~0.20-0.25 full
  universe, ~0.08-0.20 ex-megacap. 20% sits inside the range.

R16 NOTE: P2 was refuted by this session's own test, so the pressure state is
ON for the rest of this session under R16.3. Nothing here is adopted; this is
a proposal to be re-read cold at the weekend. (Item 10 never adopts a rule
mid-session anyway.)

Why P2 being refuted does NOT contradict item 8 (important, and the honest
caveat): item 8 tested a DIFFERENT quantity — the cross-sectional above/below-
200d return difference on overlapping monthly data against a strict |t|>3.9
multiple-testing hurdle — and found no edge that clears it. This script
measures the actual trade-P&L distribution of the gate+R4 strategy on a
universe of 15+22 names chosen in 2026 (survivorship, item 5). Its positive
in-sample mean is real but FLATTERED by survivorship and not proof of a live
edge. So the Kelly point estimates here are an UPPER BOUND on what to size to,
not a discovered edge. Treat them as "even taking the in-sample numbers at
face value, here's what Kelly says," then haircut hard.

## Verdict

**20% is about right — arguably slightly generous — and Kelly clearly does NOT
justify going above it in one name. Keep R3's cap; do not raise it.**

Reasoning, honestly:
1. The one Kelly figure that is robust to the fat tail is the BINARY Kelly, and
   it lands uncannily close to 20%: 0.219 (large), 0.228 (volatile), 0.19-0.25
   across both halves. For non-megacap names it drops to ~0.08-0.20 — i.e. 20%
   is if anything a touch generous for ordinary names.
2. The continuous full Kelly (1-2.7x) is real in-sample but the WRONG number to
   trade: it's fat-tail-driven, assumes you rebet iid forever, ignores
   estimation error, and rests on a survivorship-flattered universe. Standard
   practice is quarter-to-half Kelly precisely because full Kelly's drawdowns
   and parameter-sensitivity are brutal; here half-Kelly is still >0.6 for one
   name, which is obviously too much concentration.
3. The binding constraint is CONCURRENCY, not per-name Kelly. The book runs
   several positions at once and item 4 measured only ~3.9 independent bets.
   Dividing half-Kelly across 3.9 lands at 0.10-0.35 per name — 20% is in the
   middle. Running 20% x several correlated names is how yesterday's SOFI
   stack (~23% in one name across shares+calls+puts) became a whole-book risk.
4. So Kelly supports the cap's EXISTENCE and its rough level. It does not
   support raising it, and it quietly argues for (a) treating option premium +
   shares in the same name as ONE position against the cap, and (b) a lower
   cap (~10-15%) for lower-conviction / non-core names, matching the ex-megacap
   Kelly of ~0.08-0.20.

Proposed (NOT adopted — weekend re-read, and R16 is on): keep R3 at 20% as the
hard single-name cap; add that a name's cap counts shares + option premium
together; consider a 15% soft cap for non-core names. This lines up with the
SOFI-concentration fix already queued for the weekend.

Feeds: R3 (position cap), the queued SOFI exposure-cap discussion, item 4
(N_eff), item 5 (survivorship caveat), item 8 (multiple-testing caveat).

