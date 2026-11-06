# How a Swarm Picks a Home: Collective Decisions in Bees and Ants

One-line: About 10,000 honeybees with no leader pick a new nest site, and
usually pick the best one. How, and what does that say about deciding well
under uncertainty?

Last Updated: 2026-10-15
Status: DONE (curiosity block)
Audience: Nolan, TARS sessions

## The question

A honeybee swarm hanging from a branch has a few days to choose among a
dozen or more possible cavities, kilometres apart. No bee sees them all. The
queen doesn't decide. Yet the swarm usually ends up in the best one. I wanted
to know the actual mechanism, step by step, and whether it is really "good"
decision-making or just a story we tell about insects.

## What I found (sources first, my reading after)

Source: a sonnet sub-agent working from abstracts and a few full pages, plus
my own background. Items marked UNVERIFIED weren't confirmed in a retrieved
source.

**Honeybees (Thomas Seeley and colleagues):**
- A few hundred scouts (UNVERIFIED, about 5% of the swarm) search and come
  back to dance for what they found.
- **Dance strength scales with quality.** A scout dances longer for a better
  site. One report gives roughly 100 dance circuits for a first-rate site
  versus about 12 for a mediocre one (Cornell News 2006, reporting Seeley &
  Visscher).
- **Dancing fades.** Each time a scout revisits and dances again, she dances
  less, and eventually stops (Seeley & Buhrman 1999/2001; modelled by Passino
  & Seeley 2006, Behav Ecol Sociobiol). This matters a lot: support for a poor
  site dies out on its own unless new recruits keep arriving.
- **A quorum, not a consensus.** The decision isn't made by everyone
  agreeing. It's made when about 15 scouts (10-20) are at the same site at the
  same time (Seeley & Visscher 2004, Behav Ecol Sociobiol). Then they "pipe"
  to warm the swarm up, and it lifts off about an hour later. Splitting the
  scouts across five equal boxes delayed this, which is the evidence for a
  quorum rule.
- **Stop signals.** Scouts for site A head-butt dancers for site B with a
  short buzz, and vice versa (Seeley et al. 2012, Science 335:108). This
  cross-inhibition breaks ties. In models without it, the swarm stays split
  between two equal sites.
- Swarms usually choose the best site, including finding one good box among
  four medium ones (Seeley & Buhrman). I couldn't retrieve an exact hit rate.

**Temnothorax ants (Franks, Pratt, Sumpter and colleagues):**
- Colonies of about 100 workers in a rock crevice. Scouts lead each other to a
  candidate site by "tandem running", which is slow but teaches the route.
- When about 10-20 ants are at a new site (the quorum), they switch to
  carrying nest-mates. Carrying is about 3x faster but the carried ants don't
  learn the way (Franks et al. 2009, Phil Trans R Soc B).
- **The colony tunes its own quorum.** Under harsh conditions (old nest
  destroyed, exposed), colonies use a lower quorum, so they decide faster with
  less evidence and make more mistakes. It's a speed-accuracy dial set by
  urgency.
- Ants aren't counting. Franks et al. 2006 (Proc R Soc B) found ants told 1
  entrance from 3 but not 1 from 2, or 2 from 6. They seem to use light level
  as a proxy for entrance size.

**The brain link:** Marshall et al. 2009 (J R Soc Interface) showed that the
swarm's rule, with competing groups accumulating support until one crosses a
threshold, is mathematically the same family as the drift-diffusion model of
how primate brains choose between options. Drift-diffusion can be the
statistically optimal way to trade speed for accuracy. Seeley et al. 2012
explicitly compares stop signals to inhibition between pools of neurons.

**Failures:**
- Ant colonies split between two sites when the options are close in
  quality (Sasaki, Briner & Pratt 2020), and more often in spring (23 of 40
  trials in one test). They usually reunite at the queen's site (Doering &
  Pratt 2016).
- With weak cross-inhibition, the models deadlock on equal options. With a
  very high quorum plus stop signals, they can get stuck on a mediocre option
  (Laomettachit et al. 2016, modelling only).
- I found no good measurement of swarms dying from a bad choice. One weak
  source says about a third of swarms die, mostly in winter. UNVERIFIED.

## What surprised me

1. **Forgetting is what makes it work.** I expected the clever part to be the
   dance. It's actually the decay: every scout's enthusiasm runs down on its
   own, so a site keeps support only if it keeps winning fresh recruits.
   Early momentum doesn't last unless new evidence keeps confirming it.
   Without decay, the first site found would win just because it got a head
   start.
2. **They don't wait for agreement.** Consensus would be slow and fragile.
   A quorum of about 15 out of 10,000 is enough, because by the time 15 are
   at one site at once, the competition has effectively been run.
3. **The threshold is set by urgency, deliberately.** The ants lower their
   bar when staying put is dangerous and accept more errors. They aren't
   "being less careful" in a bad sense. It's the right trade when waiting
   itself costs something.
4. Individual insects are poor judges (the ants can't tell 1 from 2), and the
   group is still good. Accuracy comes from the process, not from any member.

## What I still don't know

- The actual accuracy rate of swarms, and how it was measured. I got
  qualitative claims only.
- Whether real colonies set their quorum optimally, or just roughly.
- Whether the brain analogy is deep (same computation) or just a family
  resemblance in the maths. The papers argue the former; I'm not sure.

## Anything to bring back to the trading work (honest, not forced)

- **Decaying conviction.** A TARS position kept alive by one old signal is
  like a scout still dancing for a site no one has re-checked. The R4
  trailing stop and the 200-day exit already decay support mechanically, and
  that's a good thing. Gut calls should get the same treatment: they should
  need fresh confirmation, not just be held because they were made.
- **Quorum over consensus.** TARS waits for many conditions to all agree
  before acting. The bee version would be: act when enough INDEPENDENT signals
  agree, and make sure they're truly independent. The bees enforce
  independence because each scout visits the site herself. Our 15 names are
  about 3.9 effective bets (agenda item 4), so a "quorum" of 15 green names is
  really about 4.
- **The urgency dial is R16, the other way round.** The ants lower their bar
  under pressure, correctly, because waiting is dangerous for them. For
  TARS, waiting is almost never dangerous (cash is safe), so the right
  response to pressure is to RAISE the bar. That's what R16 does. The ants
  show why: the threshold should follow the cost of waiting, not how anxious
  you feel.
- None of this is a tested rule. It's how I'd think about it.
