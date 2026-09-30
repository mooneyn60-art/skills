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

(pending — script run recorded in the next step)

## Verdict

(pending)
