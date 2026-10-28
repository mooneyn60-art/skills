# 03. Subscriber conversion: what gets small channels the most subs per 1,000 views

Meatball Research Lab, 2026-10-27. Data: `data/channels_conversion.csv` (46 channels). A web-research subagent also gathered benchmarks.
vidIQ spent on this item: **5 credits** (1 channel batch).

## Bottom line
1. **Subscribers are not the YPP bottleneck.** The channel has 959 subs and needs +41. At ~6K Shorts views a day and 0.2-1.0 subs per 1K, that is **7-43 days** (corrected 10/28 after the Mayor's HW1; I first wrote "1-2 weeks", which is only the optimistic end).
   - Do not trade views or watch hours for sub tricks. Do not trade watch hours for anything.
   - P(1,000 subs by Nov 30 with no special effort): **70%** (was 85% before the HW1 correction).
2. **Format decides conversion, and long compilations convert about 5x better than Shorts.** Lifetime subs per 1K views, 46 channels from this research:

| Archetype | n | Median subs / 1K views | Range |
|---|---|---|---|
| Long-form fact compilations (Dumb History, Atlas To Ashes, Morbid...) | 11 | **5.04** | 0.51-12.5 |
| Host-character animated Shorts (Useless Truths, Floptoon, Squire Explains, Old Oops) | 4 | 1.01 | 0.95-3.72 |
| Text/photo history Shorts | 7 | 1.04 | 0.14-1.70 |
| Animated, no host | 7 | 0.84 | 0.28-2.29 |
| Real-clip compilations (AFKnow, Infinite Fact...) | 15 | 0.83 | 0.21-4.54 |

   Caveat: this is a lifetime ratio. Long-form views are fewer and deeper, so part of the gap is mechanical. The direction matches the published benchmark: Galloway/Gileta 2023, 5,400 Shorts, Shorts 1.69 vs long-form 2.27 subs per 1K.
3. **A recurring host adds a little, about +0.2 subs/1K over hostless animation** (1.01 vs 0.84 median). With n=4 vs 7, that is within noise. **I can't confirm the "series convert 2-3x" claim.** The subagent found no source for it, only blogs.
4. **Since 31 Mar 2025, Shorts "views" count every replay**, so today's per-1K figures read lower than older benchmarks. A re-based healthy median is about **0.9-1.0 subs per 1K public views**.
   - The channel's 0.2-2.1 range is **normal**, not broken.
   - The 0.2 on 10/25 came from one high-replay day. Don't build a crisis around it.

## What the channel is doing wrong here
- **Treating subs per 1K as the bottleneck** (Channel Brain v2's "subs 4% of pace").
  - It is the bottleneck for the town's own goal of +25 subs by 10/31. It is not the YPP bottleneck. **Watch hours are**, at ~0 of 4,000.
  - Every "does this raise subs/1K?" question should become **"does this add watch hours?"**
- **Early subscribe pills at 6-10 s (the ask kit).**
  - The subagent found no evidence that early asks convert better. Most guides and YouTube's own July 2026 Related-video guide put the CTA in the **last 5 s**.
  - TARS's review saw pills at 0:03-0:07 next to polls. None of the 6 breakout Shorts I watched has any ask.
  - P(an early pill reduces stayed-to-watch by ≥2 pts): **50%** (was 55%).
  - **Correction (10/28, Mayor HW7):** "0 of 6 breakouts ask" is survivorship (n=6, winners only), and "no evidence early asks convert" is no evidence *either way*. Neither shows that the early pill hurts. **This is a coin flip to test, not a rule to adopt.**

## Ranked levers for subs per 1K (estimates; low confidence unless stated)
| # | Lever | Effect on subs/1K | Probability it's positive on this channel |
|---|---|---|---|
| 1 | **Put long-form in front of viewers**: compilations, plus Related video on every Short | Compilation viewers convert ~5/1K vs ~1/1K | **75%** |
| 2 | **Recurring identity**: same drawn Meatball, same banner, "#14" on screen, the next episode named at the end | +0.3 to +1.0 | 60% |
| 3 | **One series-tied ask at the payoff** ("#15 tomorrow: the bird that kicks"), spoken plus on screen, last 3-5 s only | +0.2 to +0.5 | 55% |
| 4 | **Retention**: more viewers reach the end, so more see the ask | +0.1 to +0.3 | 60% |
| 5 | Pinned comment and channel trailer | ~0 | 30% |

**Not available yet:**
- **Shorts Series** (YouTube, Sept 2026) is YPP-only.
- **Hype** is long-form only, and its eligibility reports conflict.

## Recommendations
1. **Re-aim the town's north-star metric from subs/1K to "qualified watch hours per week".**
   - Keep subs/1K as a guard rail: alarm only if it stays under 0.5 for 7 days.
   - P(this re-aim raises the YPP odds): **70%**.
2. **Test the subscribe ask, don't decide it** (changed 10/28 after the Mayor's HW7). Run the Mayor's design: 6 vs 6, pill at ~7 s vs ask in the last 3-5 s only, same pillar, scored on stayed-to-watch and subs/1K at 72 h. Keep whatever wins.
   - P(subs/1K is not worse and stayed-to-watch is better after 2 weeks): **55%**.
   - Score it as one test, not alongside four others.
3. **Every compilation ends with a 10 s "the next compilation is..." card**, and every Short's Related video points at a compilation.
   - P(compilations convert at least 3 subs/1K): **60%**.
