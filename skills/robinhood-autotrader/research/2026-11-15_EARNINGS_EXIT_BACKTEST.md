# Sell Before Earnings, Rebuy After: 20-Year Backtest

One-line: On 20 years of the 14 large names, holding through earnings PAID.
The reaction averaged +0.38% with only 4.4% of reactions at -8% or worse. Selling
before and rebuying after cost 3.8pp a year: about 2pp from missing
reactions and about 1.8pp from resetting stops on the rebuy.

Last Updated: 2026-11-15
Status: DONE. Sitting out earnings COSTS on 20 years of large caps: sell-before/rebuy-after -3.78pp CAGR (t=-3.26), both halves, 3/9 windows. Last week's 2-year 'sit out' lean does not generalise. Prediction committed first (cf8343a); mostly WRONG.
Audience: Nolan, TARS sessions

## Housekeeping this run

- R15 task skipped a 3rd week: still no high-water-mark rebase row after the
  10/15 R6 halt, so R16 (b) can't be verified OFF. This needs the desk (log the
  rebase) or Nolan (decide R15 directly). Flagged to Nolan.
- Swarm queue: item 2 still blocked (owner_trips.json not committed); item 5
  (ICT sweep / FVG) is already answered by earlier tests (desk study 133-day OOS:
  FVG/PDL/equal-lows sweeps no edge; godmode_test 10/16: sweep -0.05 pts,
  34% wins, n=621 OOS; sweep+CHoCH failed OOS), so it's marked covered and not
  re-derived. This item is added as 4b.

## Data (built this run)

- Earnings dates: SEC EDGAR submissions (data.sec.gov), 8-K filings whose
  items include 2.02 ("Results of Operations"), 2006-2026, for the 14 LONG
  names. Timing from the acceptance time: before 09:30 ET = "am" (reaction
  close d-1 -> close d), at or after 16:00 ET = "pm" (reaction close d ->
  close d+1), during the session = "am" (reaction already in day d's close).
  Saved to paper/history/earnings_8k.json.
- Prices: daily_ohlcv.json. Harness: paper/research_scripts/mom_screen_base.py.

## Variants (live momentum screen, LONG 14 names, 2007-2026)

- A: baseline harness, no earnings handling.
- B: live rule, no new entry if a reaction falls within the next 3 trading days.
- C: B plus an exit: sell at the close before each reaction, and rebuy at the next
  open after the reaction day if the name is still eligible (above the
  200-day, momentum > 0) and a slot is free.

## PREDICTION

- B vs A: within +/-1pp CAGR (the entry skip changes little).
- C vs B: CAGR within +/-1.5pp; max drawdown slightly shallower (removes gap
  tail); daily t < 2; walk-forward 3-6 of 9. Not a rule.
- Event level (all 14 names, 20 years, momentum-eligible events): mean
  reaction between -0.5% and +0.5%, and about 8-12% of events with a reaction
  of -8% or worse. That's fewer than the 2025-26 volatile set (14.8%), because these
  are mostly megacaps.

## Data check

paper/fetch_earnings_8k.py: 86-134 item-2.02 8-Ks per name, 2005-07 to
2026-11 (IBM, XOM and C have extra 2.02 filings for pre-announcements and
guidance). Timing matches what each company is known to do (AAPL, AMZN,
MSFT, NVDA after the close; GE, BAC, PFE before the open). Validity: the
assigned reaction day averages |return| 4.09% vs 1.51% the day before and
1.68% the day after (n about 1,270 each), so the dates are right.

## Results (python3 paper/research_scripts/earnings_exit_test.py)

Event level, momentum-eligible names at the pre-reaction close, 20 years:
**n=611, mean reaction +0.38% (t=+1.74), 4.4% at -8% or worse.**

Portfolio, live momentum screen, LONG 14 names 2007-2026 (in-sample, price
returns, survivorship-biased; SPY 8.86%):

| Variant | CAGR | maxDD | vs |
|---|---|---|---|
| A baseline | 9.12% | -17.3% | |
| B live 3-day entry skip | 9.43% | -17.3% | B - A **+0.31pp, daily t +2.28** |
| C B + sell before, rebuy after | 5.65% | -16.8% | C - B **-3.78pp, t -3.26** (378 exits) |
| D (post hoc) B + reaction day neutralised, stops kept | 7.48% | -18.2% | D - B -1.95pp, t -2.42 |

C vs B: 1st half 4.99% vs 7.94% (DD -13.8 vs -17.2%), 2nd half 6.20% vs
10.98%, megacaps dropped 2.38% vs 2.96%, walk-forward C ahead 3 of 9.

## Reading it

- For these names, the earnings reaction is on average a small GAIN for a
  momentum holder (+0.38%), and big gaps against you are rare (4.4%, about 1 in
  23). Sitting it out gives that up: about -2pp a year from missing reactions alone
  (D). Rebuying adds about -1.8pp more, because the position restarts with a
  fresh 8% stop and no trail history (C - D).
- The only thing C buys is a slightly shallower worst drawdown in the first
  half (-13.8% vs -17.2%), at a large cost in return. Not worth it.
- Last week (2025-26, 41 names, many volatile): -0.78% average reaction and
  14.8% gap-throughs. The two results are consistent with "it depends on
  the stock". Large, steady companies reward holding through; small,
  volatile ones may not. That second half isn't proven (t=-1.13 on 2 years).
- The live 3-day entry skip (B) is mildly positive (+0.31pp, t=+2.28), so it stays.
- For the live book, which now holds volatile names (SOFI, NVTS, HALO and others),
  this does NOT say "hold everything through earnings". It says sitting out isn't
  free, and the case for it depends on how gap-prone the name is. A per-name
  rule would need a gap-history test on the volatile names, with more than 2
  years of their earnings (the 8-K method extends to them; future item).

## Prediction scorecard

- B vs A within +/-1pp: RIGHT (+0.31pp), though I didn't expect t=+2.28.
- C vs B within +/-1.5pp: **WRONG** (-3.78pp). Drawdown slightly shallower:
  half right (full -16.8 vs -17.3%, yes; but -18.2% for D). t < 2: **WRONG**
  (-3.26). Walk-forward 3-6/9: RIGHT (3). Not a rule: RIGHT.
- Event mean between -0.5% and +0.5%: RIGHT (+0.38%). 8-12% at -8% or worse: **WRONG**
  (4.4%, much tamer than I guessed).
