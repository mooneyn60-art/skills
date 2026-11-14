# The Regime Switch — Buy Strength When Calm, Buy Weakness When Stressed

One-line: the range-reversal edge and the VIX finding are the same effect;
buying weakness earns +4.95pp/month above buying strength when VIX is 25 or
higher (t=8.46) and is neutral-to-negative below VIX 20.

Last Updated: 2026-09-23
Status: PROPOSED as R15 — passes all four hurdles, NOT YET ADOPTED,
        and untestable in the most recent two years
Audience: TARS sessions, Nolan

## How this was found

Nolan made two points on 2026-09-23 that the system could not have reached
on its own. First, that TARS was applying a trend filter to a range-bound
stock. Second: "make sure you research all the way to present times, not to
get stuck on something that used to work but might have stopped."

The decay test he asked for produced the finding. Testing the range edge
year by year showed it was not steady but EPISODIC -- large in 2008, 2009,
2020, 2022 and 2026, and NEGATIVE in 2012, 2015, 2016 and 2017. Those are
stressed years against calm years. Conditioning on VIX confirmed it.

## The result

Forward 1-month return, buying the bottom quartile of a stock's 60-day
range minus buying the top quartile, inside ranging conditions (ADX<20),
14 symbols, 2006-2026. VIX bucketed from weekly closes, forward-filled
onto trading days using past data only.

    VIX <15   calm       +0.07pp   t= 0.29   n= 976   nothing
    VIX 15-20            -0.71pp   t=-2.48   n=1420   BUY-HIGH WINS
    VIX 20-25            +1.43pp   t= 2.92   n= 846
    VIX 25+   stressed   +4.95pp   t= 8.46   n=1081   BUY-LOW WINS BIG

THE TWO RULES ARE BOTH CORRECT, IN DIFFERENT REGIMES. In calm markets a
falling price is information -- the company is deteriorating, and buying it
loses. In stressed markets a falling price is liquidation -- indiscriminate
forced selling that reverses.

## Hurdles, VIX>=25 regime

SPLIT SAMPLE: 2006-2016 +2.66pp t=3.15; 2016-2026 +7.82pp t=9.41. Wins both.

WALK-FORWARD: 5 of 6 windows that contained a measurable stressed period.
The failure is real and is recorded: 2015-03 to 2017-06 returned -5.73pp at
t=-4.05 on n=67.

DROP THE BIG WINNERS: holds in all five universes and STRENGTHENS as they
are removed -- full 14 +4.95pp, minus the five megacaps +6.03pp at t=8.02.
This is the opposite of the momentum result and is the strongest evidence
in this repository.

CALM REGIME CHECK: VIX<20 gives -1.16pp t=-3.98 in 2006-2016 and +0.06pp
t=0.23 in 2016-2026. Buying weakness in calm markets is neutral at best.

## The limit, which is the point Nolan raised

THE MOST RECENT TWO YEARS CANNOT TEST THE STRESSED HALF. Three of nine
walk-forward windows had too few stressed observations to measure, and one
of them is 2024-05 to 2026-09. The March 2026 VIX spike lasted a single
week. The edge is confirmed through 2022 and is UNVERIFIED in the current
regime, because the current regime has not been stressed.

A LABELLING ERROR IS RECORDED HERE TOO: the diagnostic printed "no stressed
period in window" for those three windows when the truth was "too few
observations to measure." Those are different claims and the script
overstated. R14.2 applies to labels as much as to numbers.

## Proposed R15 — NOT ADOPTED, requires Nolan's decision

While VIX < 20: R2 stands unchanged. Enter above the 200-day. Buying
weakness is not permitted.

While VIX >= 25: the entry condition INVERTS for ranging names (ADX<20).
Buy the bottom quartile of the 60-day range. The 200-day gate is suspended
for these entries only.

Between 20 and 25: no change, no inversion. A deliberate dead zone so the
rule cannot flip-flop on noise around a threshold.

Open questions before adoption: what the exit rule should be (no exit
tested so far monetises this entry -- see 2026-09-23_RANGE_REGIME.md);
whether position sizing should change when the trigger fires, given it
occurs roughly once every 16 months; and whether the 25 threshold survives
being moved, which has not been tested.

## Status of the running tally

Seven strategy families tested. This is the first with a signal that
survives all four hurdles AND has a stated economic mechanism AND
strengthens when survivorship is stripped out. It is still not a strategy,
because no exit has been shown to capture it.
