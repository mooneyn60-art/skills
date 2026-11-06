# Monthly Expectancy Audit, October 2026

One-line: WE CANNOT SAY WHETHER THE ACCOUNT BEATS SPY SINCE INCEPTION,
because no deposit-adjusted account value is recorded anywhere. What can be
measured is negative: closed trades average -0.11R (n=27, ex-SOFI shares),
TARS-1's own trades -0.32R (n=10), the option slot -0.29R (n=6).

Last Updated: 2026-10-01
Status: DONE. Audit script committed before running (8ff111b); two predictions wrong.
Audience: Nolan, TARS sessions

## 1. Expectancy (paper/trades.jsonl, closed live trades with a recorded risk)

Script: paper/audit_2026_10.py. SOFI SHARE trades excluded as the carve-out
requires (1 closed row). Option trades closed 2026-09-24 onward are the R17
slot book, reported separately.

    ALL (ex-SOFI shares, ex-slot)   n=27  mean -0.11R  total -2.98R  t=-1.02
    by exit:  user_closed/discretionary  n=24  -0.06R  (t=-0.60)
              stop                       n=2   -1.19R
              trail                      n=1   +0.77R  (TENB)
    by source: user_discretionary        n=15  +0.03R  (t=+0.18)
               TARS-1                    n=10  -0.32R  (t=-1.73)
               other                     n=2   -0.21R / +0.01R
    by hold:   < 1 day                   n=12  +0.08R
               1-5 days                  n=11  -0.37R  (t=-2.70)
               >= 5 days                 n=1   +0.77R

    R17 OPTION SLOT BOOK                 n=6   mean -0.29R  total -1.71R
       SOFI $19C Dec18 -0.21R (stop-limit hit; full premium at risk, computed
       by hand because its planned_risk field is text), SOFI $17.5C Sep25
       expired -1.00R, NVDA 0DTE -0.33R, three SOFI rolls -0.01 to -0.13R.

Not enough trades for any of this to mean much (item 18: ~124 needed). The
one slice with |t| > 2, "held 1-5 days", is a post-hoc cut among several
and is noted, not believed.

LEDGER GAPS FOUND: (a) Nolan's 2026-09-30 sales of the SOFI Oct-23 $15.50C
and Dec-18 $16C have no closing rows, so they're missing from the slot book
(NOLAN_LOG puts them at -14% and -24% of premium). (b) No slot trade records
spy_same_window_pct, so R17's "slot vs SPY" comparison can't be made.

## 2. Is the account beating SPY since inception?

UNKNOWN, AND THAT IS THE FINDING. The repository holds no daily account
value. There are only three anchors (the 9/17 close, 9/18 and 9/21 around
deposits), and the 9/25 deposit row has no before/after values. A
deposit-adjusted (time-weighted) return can't be rebuilt from it.

PROPOSED FIX (tightening, allowed under R16): the 5:17pm close report logs
one number per day, a NAV index = previous index x (today's account value
minus today's deposits) / yesterday's account value. It's a ratio, so it
satisfies R13, and with it this question has an answer next month.

2a. SHADOW BOOK (paper/shadow/nav.csv, rules-only, since 2026-09-25):
tars1 +1.00% vs SPY -1.16% over 4 trading days. Too short to mean anything.
The shadow and trend_only books are identical so far.

## 3. Which rule costs the most? R6's circuit breaker, by a wide margin

Engine, 14 names, 2006-2026, today's TARS-1 config. The engine gained an
optional loss-only breaker (default off, default output verified unchanged)
so the LIVE version of R6 could be measured.

    TARS-1, old any-stop breaker     CAGR 11.74%  maxDD -33.6%  breaker-blocked days 155
    TARS-1, LIVE loss-only breaker   CAGR 12.21%  maxDD -31.0%  breaker-blocked days 113
    no circuit breaker               CAGR 14.67%  maxDD -35.3%
    no drawdown halt (breaker kept)  CAGR 11.81%  maxDD -35.0%
    neither                          CAGR 12.15%  maxDD -39.0%

The live breaker costs about 2.5pp a year of CAGR and buys about 4pp less
maximum drawdown. That is ONE full-period run: no split sample, no
walk-forward, no megacap drop yet. It has not cleared the hurdles.

BECAUSE MY Q3 PREDICTION WAS WRONG (predicted under 0.5pp), R16 trigger (c)
is on and R16 forbids PROPOSING a loosening in this session. So this is
reported, not proposed. For the weekend block: run the breaker test through
all four hurdles, and remember the drawdown it buys may matter more to
Nolan than the return it costs.

## 4. Has anything decayed? The last 12 months (2025-09-23 to 2026-09-24)

    TARS-1 (engine) +14.85%   SPY +15.68%   equal-weight hold of the 14 names +17.40%
    200-day above-minus-below forward 21-day spread: n=11 months, -3.86pp, t=-2.11

In the last year, names above their 200-day did WORSE next month than names
below it. With 11 months that's weak evidence, but it points the same way
as item 20 and the 200-day re-measure: R2's 200-day gate is a risk control,
not a return edge, and over the past year even the return sign flipped.
R15 (recommended for repeal 2026-09-26) had no stressed period to test.

## 5. Positions held over 6 months that have gone nowhere

None. The live account's oldest position dates from September 2026.

## Predictions scored

    Q3 breaker < +/-0.5pp, halt < +/-1pp: breaker WRONG (+2.5pp live, +2.9pp old); halt RIGHT (+0.07pp)
    Q4 TARS-1 trails SPY by 2-8pp in the last 12 months: WRONG on size (trails by 0.8pp)
       trails equal-weight hold: RIGHT (by 2.6pp)
       200-day spread |t| < 2: WRONG (t=-2.11, n=11)
