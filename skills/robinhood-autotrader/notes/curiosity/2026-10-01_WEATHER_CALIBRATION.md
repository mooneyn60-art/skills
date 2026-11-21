# Curiosity block, 2026-10-01: how weather forecasters became calibrated

The redo of the 2026-09-23 session whose notes were lost. No trades.

Sources: a sub-agent read what it could open (marked [checked]). Nature,
Science and some journal pages were blocked, so a few figures come from
abstracts or search snippets [snippet]. Standard facts I'm confident of
but didn't re-open today are marked [memory]. My own reading is [mine].

## The question

Weather forecasters are the classic example of people who say "70%" and
are right about 70% of the time. How did a whole profession get there,
when most experts (and TARS, see below) are badly overconfident?

## What I found

**1. They score every forecast with a rule that punishes lying.** Glenn
Brier (1950) proposed scoring a probability forecast by the mean squared
gap between the forecast and what happened (0 or 1); lower is better
[checked]. The key property is that it's PROPER: the only way to
minimise your expected score is to report what you actually believe.
Shading 60% up to 80% to sound confident, or down to 40% to be safe,
costs you points on average [memory; standard result].

**2. The score splits into "honest" and "useful".** Allan Murphy's
decomposition breaks the Brier score into RELIABILITY (do 70% forecasts
come true 70% of the time?), RESOLUTION (do the forecasts separate rainy
days from dry ones, or always say the average?) and UNCERTAINTY (how hard
the weather is to begin with) [checked]. This was the most useful idea of
the session [mine]: a forecaster can be perfectly reliable and useless by
always forecasting the climate average. Reliability without resolution is
a coward's calibration.

**3. US forecasters were measured and found honest decades ago.** Murphy
and Winkler (1977) studied National Weather Service precipitation
forecasts in Chicago, 1972-76, and concluded forecasters "can formulate
such forecasts in a reliable manner" [snippet: I couldn't open the paper
for the per-bin numbers]. The NWS had been issuing probability-of-
precipitation forecasts since the mid-1960s [memory].

**4. They correct the computer statistically.** From 1968 the NWS ran
"Model Output Statistics" (MOS): regress what the weather model said
against what actually happened, then use that fitted relationship to
correct the model's known biases in new forecasts [checked]. The raw model
isn't trusted as-is; its track record is used to translate it.

**5. They run the forecast many times.** Since 1992, ECMWF and NCEP have
run ENSEMBLES: dozens of forecasts from slightly different starting
conditions. The share of runs that produce rain IS the probability of rain
[checked]. Uncertainty is measured by perturbing the inputs, not guessed.

**6. Steady progress, from many small fixes.** ECMWF credits better
observations, physics, ensembles and computing for decades of gains
[checked]; the well-known summary is about one day of useful lead time
gained per decade, so a 5-day forecast now is roughly as good as a 3-day
forecast was decades ago [memory; the Nature paper was blocked].

**7. The famous exception is deliberate: the "wet bias".** Commercial and
TV forecasters overstate rain. The Weather Channel's 20% forecasts came
true about 5% of the time; some local TV "100%" forecasts about 70%. The
NWS showed no such bias [checked, via Wikipedia's summary of Eric Floehr's
data and Nate Silver]. The reason given is asymmetric cost: people blame
the forecaster far more for unexpected rain than for an unexpected dry
day. A Weather Channel representative: "If the forecast was objective, if
it has zero bias in precipitation, we are in trouble" [checked, secondary].
An academic study (Bickel & Kim 2008) found the same pattern: good
calibration from 40-90%, poor below 30% [snippet].

**8. The machine-learning forecasters are being held to the same
standard.** GraphCast (2023) beat ECMWF's deterministic model on 90% of
1,380 targets but gives no probabilities [checked]. GenCast, a
probabilistic ensemble, beat ECMWF's ensemble on 97.4% of 1,320 targets
[checked, abstract]; whether its probabilities are calibrated is reported
in the full paper, which couldn't be opened [unverified]. ECMWF's own AI
ensemble is trained on a proper score (CRPS) and reportedly checked with
spread-versus-error tests [snippet].

## What surprised me

1. **Calibration is not a personality trait; it's a feedback system.** A
   proper score, a fast and unambiguous outcome every day, and a
   statistical correction of the raw model. Take those away and the same
   people would be as overconfident as anyone. Kahneman & Klein's
   "high-validity environment with rapid feedback" (item 21) is exactly
   this.
2. **The wet bias is intentional miscalibration for a business reason.**
   Being perfectly honest is not always what an audience rewards.
3. **Reliability vs resolution.** You can be perfectly calibrated by saying
   nothing interesting. That landed close to home (below).

## Applied to TARS: my own predictions, scored the same way [mine]

The 2026-09-24 note (research/2026-09-24_MY_OWN_CALIBRATION.md) found TARS
right 10/10 when saying "this doesn't work" and 1/17 when saying "this has
an edge". Scoring my research-runner predictions since then (16 notes,
2026-09-23 to 10-01) the same way:

    "no return edge here"                       9 right, 0 wrong
    "this rule won't change much"               0 right, 4 wrong
        (R15 inside TARS-1: made it worse; breadth vs VIX: some volatility
         information left; R6 breaker: costs ~2.5pp; 200-day last 12 months:
         reversed, t=-2.11)
    descriptive sizes (gaps, costs, volatility)  mostly right
    return-edge EFFECT calls                     mostly wrong (fundamentals sign, INTC capture)

So the 9/24 lesson needs refining. TARS is reliable about RETURN edges
(they almost never exist) and UNRELIABLE about how much its own RULES move
risk and return: four "no difference" calls in a row came back "yes,
noticeably". In Murphy's terms, "there's no edge" has high reliability
and low resolution. It's the climatology forecast. It's right because it
says the base rate, not because it sees anything.

## What I still don't know

- The per-bin numbers in Murphy & Winkler 1977, and whether GenCast's
  probabilities are well calibrated (both behind blocked pages).
- Whether "one day per decade" still holds in the AI-model era or is
  accelerating.
- How far a forecaster's calibration transfers to a new kind of question.
  This matters for whether TARS's calibration on return edges carries
  over to anything else (the evidence above says it doesn't, for rules).

## Worth bringing back to the trading work

1. **State predictions as probabilities, score them with Brier.** Range
   predictions ("+0.2 to +0.6pp") can't be scored properly. Add one line
   to each research note's prediction: "P(passes all four hurdles) = x%".
   After 20-30 notes, TARS gets a reliability diagram of its own.
2. **A MOS for TARS.** TARS's raw positive calls are biased (1/17). The
   weather fix isn't to stop forecasting; it's to correct the forecast
   with the track record. A "this has an edge" call should be reported
   alongside TARS's historical hit rate for that kind of call.
3. **Ensembles for backtests.** Instead of one backtest at one parameter
   set, run the rule across many perturbed settings and starting dates,
   and report the share that beat the baseline. That's what the
   walk-forward already does in a small way; the weather lesson is to make
   it the standard output.
4. **Watch for a wet bias in TARS's own incentives.** TARS is criticised
   more for a confident wrong "yes" than for a wrong "no", which pushes it
   towards always saying "no edge". That's a reliability-preserving,
   resolution-destroying bias. The "rule won't matter" misses are the
   symptom.
