# VIX as a Macro Regime Signal — Suggestive, Sample Too Thin

One-line: the first non-price variable ever tested here; VIX above 30
precedes a +24.65% average year with an 89.4% win rate, but on only 15
independent episodes, two of which supply more than half the evidence.

Last Updated: 2026-09-23
Status: OPEN — promising, NOT adopted, sample inadequate
Audience: TARS sessions, Nolan

## Why this was run

Nolan asked "did you even look into economics yet, it's a huge part of the
market." HE WAS RIGHT AND THE ANSWER WAS NO. Six strategy families had been
tested by this point -- momentum rotation, concentration, volatility
targeting, trend-gated volatility targeting, channel mean reversion,
range-regime mean reversion -- AND EVERY ONE OF THEM USED PRICE AND NOTHING
ELSE. Four days of research had never once asked what the economy was
doing. This file exists because the account owner spotted a blind spot the
system could not see in itself.

A correction also belongs here: Nolan connected the Anthropic Economic
Index expecting market data. It is a dataset about how Claude is used by
occupation and geography. It carries no market, rate, or macro series and
its own documentation forbids labour-market inference. It cannot serve this
purpose and was not used.

## What is actually reachable

The broker exposes VIX, SPX, NDX, DJX, XSP, XND and a set of crypto
reference indices. NO yield curve, NO rates, NO inflation, NO employment.
VIX is therefore the only macro variable available through current tooling.
Real macro requires an external source such as FRED, which is public and
free but needs web access that has not been tested.

Data pulled: VIX weekly closes, 2006-01-09 to 2026-09-14, 974
non-interpolated bars, stored at paper/history/vix_weekly.json. Forward
returns measured on SPY from paper/history/daily_stocks.json.

## Result

Forward SPY return by VIX bucket. PROVENANCE: weekly observations, OUT of
sample in the sense that no parameter was fitted, but the buckets are round
numbers chosen a priori rather than optimised.

    VIX 10-15   3mo +2.03%   1yr +10.98%   win 85.6%   n=319
    VIX 15-20   3mo +1.95%   1yr  +8.29%   win 78.4%   n=273
    VIX 20-25   3mo +2.15%   1yr  +6.75%   win 74.7%   n=158
    VIX 25-30   3mo +4.51%   1yr  +6.88%   win 74.4%   n=78
    VIX 30+     3mo +4.32%   1yr +24.65%   win 89.4%   n=85

The relationship is U-SHAPED, not monotonic. Calm is good, middling is
mediocre, panic is extraordinary. This matches the published volatility
risk premium literature.

## The disqualifying caveat, found before the result was reported

THE 85 OBSERVATIONS ARE NOT 85 INDEPENDENT FACTS. They are weekly snapshots
of a ONE-YEAR forward return, so they overlap almost completely. Counting
distinct episodes (gaps over 60 days) gives FIFTEEN in twenty years, and
two of them dominate: 2008-09 to 2009-05 contributes 34 weeks and 2020-02
to 2020-06 contributes 14. MORE THAN HALF THE EVIDENCE IS "YOU WOULD HAVE
BOUGHT THE MARCH 2009 AND MARCH 2020 BOTTOMS."

Effective sample: 15. Not adopted. R14.2 requires provenance to travel with
every number, and this number's provenance disqualifies it as a basis for a
rule.

## What it is good for anyway

VIX above 30 occurs roughly once every 16 months. That frequency makes it
useless as a trading system and potentially valuable as a RARE HIGH
CONVICTION TRIGGER -- the signal to deploy cash aggressively rather than
incrementally. Worth carrying as a standing alert rather than a rule.

VIX at the time of writing: 14.73, the bottom bucket. No signal.

## Next

1. Establish whether FRED or an equivalent is reachable. If it is, the
   yield curve (10y minus 2y), unemployment claims and inflation surprise
   are the standard regime variables and all have published mechanisms.
2. Test whether any macro regime variable improves the R2 entry gate,
   rather than acting as a standalone strategy. Six price-only families
   have failed; the conditioning variable may matter more than the rule.
3. Re-test VIX bucketing on a longer history if one becomes reachable.
   1990-2026 would roughly double the episode count.
