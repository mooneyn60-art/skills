# 70 - Niche outliers for small channels (house and backyard creatures), 2026-11-10

Read-only research, nothing posted, nothing committed, vidIQ not used. Method: yt-dlp flat extraction.
40 searches (about 1,000 results), then uploads of 79 channels pulled from the /videos and /shorts tabs
(last 60 each, `approximate_date` for age). Result: **3,078 long-form and 2,408 Shorts rows, 49 channels under 150K subscribers, 30 above.**
Outlier score = views / that channel's own median for the same type (long or Short). Raw data:
`data/70-outliers.csv` (one row per video, with `video_id`, `url`, `outlier_score`, `on_topic`, `compilation_flag`).

## 0. Read this first: what is and is not in here

1. **Retention (heatmap) could not be pulled.** Every full `yt-dlp -j` watch-page call returned HTTP 429. I retried one video 4 times over
   about 15 minutes with 2.5, 5, 7.5 and 10 minute back-offs, after a first throttled burst; all failed. Flat tab and search calls kept working,
   so the block is specific to watch pages from this network. I did not try alternate player clients or other ways round the throttle.
   So **there is no "best holders" table, no 30 s / 60 s / last-half numbers and no likes per 1,000 views, and every candidate below rests on views only.**
   Ready to run from another network: `data/70-heatmap-pull.py` + `data/70-heatmap-ids.txt` (55 ids: 32 small-channel outliers, 23 big-channel
   and ranking/myth references). It writes `70-heatmap-metrics.csv` with the exact metrics requested. The CSV's `hm_*` columns are empty until then.
   Reminder for when it runs: "Most replayed" is a proxy (replays and seeks, normalised to each video's own peak), not the private retention graph.
   Shorts have no heatmap at all; their retention can't be measured from outside.
2. **Shorts evidence is thin.** Most small niche channels either have no Shorts shelf or have too few to give a median. Only about 20 usable
   small-channel Shorts outliers; the Shorts section leans on titles and on earlier work (research/63).
3. **Search skews big and old.** Raw-view search surfaces big channels; I corrected by pulling every channel's own uploads. Scores are
   relative to each channel's last 60 uploads, so a channel with one huge hit and a tiny median gets an enormous score (Sometimes Science 2,396x).
   Read the score together with raw views and age.
4. **Age:** long-form scores use lifetime views. Older videos had longer to collect them. Ages are in the table (flat extraction gives
   approximate dates only; Shorts have none).

## 1. Top finding in one paragraph

The small-channel long-form breakouts in this niche are overwhelmingly **faceless, illustrated or stock-image, AI-voiced explainers of 7 to 12
minutes** with one of two title shapes: **"Never Kill [house or garden creature] - [reason / it's hunting something worse]"** and
**"Every [creature group] explained in N minutes"**. Garden Whispers (19.8K subs) has 12 of its last 45 videos at 5x or more of its own median
(top: 1.7M views); Root Signal (4.4K subs) has 679K and 180K. Rankings do not carry small channels: five small-channel "house bugs ranked / harmless to
deadly" videos found got 3 to 688 views (section 5). That is the same story as your 426-view ranking.
The "never kill" shape is also what your one recommended long-form already is, but **it has been cloned by dozens of tiny channels, and most clones got
10 to 2,800 views**, so it is a proven but crowded lane.

## 2. (a) Small-channel outlier tables

### 2a. Long-form, channels under 150K subscribers, on-topic (top 25 by score; views of at least 1,000)

| # | Title | Channel (subs) | Views | Score | Min | Age | id |
|---|---|---|---|---|---|---|---|
| 1 | What Really Happens When A Fly Lands On Your Food? | Sometimes Science (9.3K) | 1,300,000 | 2,396x | 6.6 | 3.0y | 8kJS9LfdSPM |
| 2 | What's The Difference Between Bees, Wasps, Yellow Jackets, and Hornets? | Sometimes Science (9.3K) | 401,000 | 739x | 8.1 | 3.0y | qv1Er9c0bKY |
| 3 | Don't Kill That Silverfish - It Could Be Warning You About Your Home | Root Signal (4.4K) | 679,000 | 503x | 11.2 | 92d | 3bLrrgNtkik |
| 4 | Never Scrape This Off Your Wall - Here's What's Living Inside | Garden Whispers (19.8K) | 1,700,000 | 486x | 10.1 | 153d | u5ExDrh6NtI |
| 5 | Never Kill The Giant Mosquito - You've Misjudged It | Bug Tales (240) | 63,000 | 228x | 10.4 | 123d | pzeaYVCN6Ik |
| 6 | 5 Wasps That Look Dangerous But Really Aren't | Naji Explains Nature (1.5K) | 144,000 | 205x | 2.2 | 184d | RKT-ecVtkTk |
| 7 | Every House Fly Type Explained in 10 minutes | Factomni (5.4K) | 571,000 | 204x | 10.8 | 245d | KAMlZLzzEUU |
| 8 | Never Kill the House Centipede - It's Hunting Something Worse | Garden Whispers (19.8K) | 481,000 | 137x | 10.2 | 153d | -iOOX2DIK8c |
| 9 | Every Wasp You Fear Explained in 7 Minutes! | Xplain WILD (1.4K) | 349,000 | 134x | 7.8 | 31d | Bt0siyRrR40 |
| 10 | Never Put Salt on Giant African Snails - The Reason Will Shock You | Root Signal (4.4K) | 180,000 | 133x | 11.6 | 92d | NMcxerzjQdQ |
| 11 | The World's Deadliest Spiders Explained | Factomni (5.4K) | 331,000 | 118x | 8.9 | 92d | 5OntI-PglEA |
| 12 | Why You Should Never Kill the Roly-Poly Under Your Garden Pots | Garden Whispers (19.8K) | 360,000 | 103x | 10.6 | 153d | 46s8SDuRRWo |
| 13 | Why You Should Never Kill This Spider | Garden Whispers (19.8K) | 277,000 | 79x | 8.6 | 31d | YBWh0O3xvDc |
| 14 | Why You Should Never Kill the Spider in Your Corner (The Real Reason) | Garden Whispers (19.8K) | 258,000 | 74x | 10.6 | 184d | B3Tdjhtglc0 |
| 15 | Every Bee You Should NEVER Disturb Explained in 10 Minutes | Factomni (5.4K) | 106,000 | 38x | 10.1 | 123d | WVazsXwbMoQ |
| 16 | If a Toad Chose Your Garden, This Is What It Means | Garden Whispers (19.8K) | 124,000 | 35x | 11.5 | 153d | yRrvPBh93z0 |
| 17 | You Keep Squashing Her - She's Actually Helping You | The Hidden Wild (239) | 38,000 | 29x | 10.3 | 92d | FgWUptQWuc4 |
| 18 | The TRUTH! Ladybug vs Asian Lady Beetle | SciBugs (9.8K) | 17,000 | 28x | 2.5 | 4.0y | -wRpe8NZ7uY |
| 19 | Why Do Honey Bees Die After Stinging? | Sometimes Science (9.3K) | 15,000 | 28x | 5.2 | 3.0y | 3a9NOF64J2k |
| 20 | Every Level of Insect Bite Explained in 16 Minutes | Bug Blueprint (140) | 13,000 | 27x | 16.6 | 31d | bOUzMDx3_qw |
| 21 | The Most Dangerous Hornets in the World Ranked | Factomni (5.4K) | 69,000 | 25x | 10.5 | 153d | jILAwp-wlfs |
| 22 | Every Type of Wasp Explained in 7 Minutes | WiseFrog (74K) | 605,000 | 24x | 7.4 | 123d | FD7JvELQaP8 |
| 23 | If You Still See Fireflies at Night, Your Garden Has a Secret | Garden Whispers (19.8K) | 83,000 | 24x | 12.2 | 153d | wBkjLsm8mjg |
| 24 | Every Type of Mosquito Explained | Factomni (5.4K) | 63,000 | 22x | 12.5 | 184d | fEE70LqaO2c |
| 25 | 7 Early Signs of BED BUGS (How to Know if You Have Bed Bugs) | MMPC (2.0K) | 561,000 | 22x | 5.0 | 3.0y | juXj83aBMQA |

Notes on the table:
- Rows 1, 2, 18, 19 and 25 are 3 to 4 years old and come from channels whose current output sits near 500 to 1,000 views; they are one-offs (one hit, no repeat), not a repeatable channel pattern.
- Not in the table because the keyword filter missed "daddy longlegs" in the title: Garden Whispers "Never Kill the Daddy Longlegs - You Have Been Lied To" 184K and Root Signal "They Lied About Daddy Longlegs... Here's the Truth!" 173K (both appeared in search; same template).
- Mid-size reference (93.5K subs, so inside the small set): Travis McEnery "The Spiders in Your House - The Cellar Spider" 874K (9.5x, 9 min), "...The Brown Recluse" 682K (7.4x, 80 min), "...The Yellow Sac Spider" 647K (7.0x, 33 min), "...The Rustic Wolf Spider" 405K (4.4x, 45 min). A numbered-by-species series with the same title stem; median 92K views on his channel.
- Excluded as off-niche or not creator content: pest-control brand and local-news channels, plant/weed videos, fish/tadpole-catching videos, kids' compilations.
- Also notable: Dan The Bug Man (336K, so big) "Most Insane Cockroach (& Bed Bug) Infestation" 1.4M, 93x; Aaron Steele (46.9K) hornet-nest removal stunts reach 66M as a Short. Both are real-footage formats we cannot copy.

### 2b. Shorts, channels under 150K subscribers, on-topic (all I could score; only about 20 usable)

Shorts tabs give no upload date, so age is not available. "Typical" is the channel's median Short.

| # | Title | Channel (subs) | Views | Typical | Score | id |
|---|---|---|---|---|---|---|
| 1 | A massive HORNET nest hit and run! | Aaron Steele (46.9K) | 66,000,000 | 10.5K | 6,286x | H08RJejNZVI |
| 2 | The most venomous insects on the planet | WiseFrog (74K) | 7,300,000 | 42K | 174x | xFZ9A93X6is |
| 3 | Torching a MASSIVE HORNET Nest! | Aaron Steele (46.9K) | 1,000,000 | 10.5K | 95x | 6DiID52w0RM |
| 4 | Kids Talk Bugs in the House, Hiding Spots and What They'd Do | PestWorld (13.2K) | 19,000 | 271 | 70x | _fz8cvciwns |
| 5 | Diatomaceous Earth for Bed Bugs: The Grade Nobody Mentions | Bedbug HQ (44) | 5,600 | 134 | 42x | t969J3lBZ_Y |
| 6 | Should I Kill Spotted Lanternflies!? (in the US) | SciBugs (9.8K) | 11,000 | 598 | 18x | MOsv-5On3TQ |
| 7 | Does Vinegar Keep Ants Away? | PestWorld (13.2K) | 3,900 | 271 | 14x | C9qqFUVpvWU |
| 8 | One bed bug becomes hundreds | Bedbug HQ (44) | 1,200 | 134 | 9.0x | OxSMbE1lbj4 |
| 9 | These Friendly Spiders Aren't as Dangerous as You Think | Creatures Scoop (109K) | 278,000 | 31.5K | 8.8x | sVs0pUCx7zA |
| 10 | Warning Signs a Bee is About to Sting You | Sometimes Science (9.3K) | 4,000 | 469 | 8.5x | uJDbYNRLqSA |
| 11 | Giant Beetle! Megasoma actaeon | SciBugs (9.8K) | 5,100 | 598 | 8.5x | Ba9kKLvHS5M |
| 12 | Bed bugs can't fly - they crawl to you | Bedbug HQ (44) | 1,100 | 134 | 8.2x | 28DNvJAgHC4 |
| 13 | This Waiting Room Needed a Bed Bug Inspection | Doctor Sniffs Bed Bug Dogs (3.7K) | 14,000 | 1.8K | 7.8x | oEpa7c7MnY8 |
| 14 | It's 3 AM - that's when bed bugs feed | Bedbug HQ (44) | 1,000 | 134 | 7.5x | or7nEKPfV_U |
| 15 | Bed Bugs Don't Mean You're Dirty - It's Not Your Fault | Bedbug HQ (44) | 974 | 134 | 7.3x | 1HHnUo9IWWA |
| 16 | The Strongest Bug on Earth? Meet the Hercules Beetle! | Creatures Scoop (109K) | 189,000 | 31.5K | 6.0x | wi9P9kvjkIs |
| 17 | Shiny black wasp | Privileged Bug Facts (101K) | 11,000 | 2.1K | 5.2x | 6AJgrrsGiWU |
| 18 | Bed Bugs Can Survive a Long Time Without Feeding | Doctor Sniffs Bed Bug Dogs (3.7K) | 6,400 | 1.8K | 3.6x | I1vQoa3mdZE |
| 19 | The Biggest Insects in the World | WiseFrog (74K) | 101,000 | 42K | 2.4x | rzmD2mghAak |
| 20 | Stick Insect - Nature's Master of Disguise! | Creatures Scoop (109K) | 75,000 | 31.5K | 2.4x | hdmL_bGo-1Y |

Caveats specific to this table: rows 1 and 3 are stunt or removal footage; rows 5, 8, 12, 14 and 15 sit on a channel whose median is 134 views, so
"7x" means about 1,000 views, in the same range as your own stalled Shorts; PestWorld and Doctor Sniffs are pest-control businesses. Real signal here is
title shape (section 4), not the scores. From earlier work (research/63, different method): BioChok (4.7K subs) mosquito "what if" Short 2.7M (208x),
Hypothetica (796 subs) "What If Every Spider Disappeared? (But There's a Catch)" 3.5x.

## 3. (b) Big-channel reference table (150K subs and up; not in the outlier set)

| Channel (subs) | Video | Views | Score (vs own median) | Min | Note |
|---|---|---|---|---|---|
| TierZoo (3.95M) | The Insect Tier List | 10.1M | 2.9x | 28 | Median 3.45M; this is a normal-to-good TierZoo video, not a freak |
| TierZoo | Are Scorpions Overpowered? | 14M | 4.1x | 9.7 | |
| MyWildBackyard (355K) | The Worst Spider Bites on Earth Ranked | 3.5M | 16.9x | 33 | Median 207K |
| MyWildBackyard | Everything We Know About Widow Spiders | 1.5M | 7.3x | 31 | |
| MyWildBackyard | The Worst Insect Stings on Earth Ranked / Worst Stings in the US Ranked | 826K / 861K | 4.0x | 32 / 23 | Your first-pass 861K is about 4x its own median |
| MyWildBackyard | What Happens if a Daddy Long Legs BITES You? | 2.5M | n/a (search) | 8 | Myth angle on a house spider |
| What If (8.99M) | What If We Killed All Mosquitoes? / ...All Spiders? | 6.5M / 566K | about 1.0x for spiders | n/a | Spider version is a median What If video |
| Insider Science (3.06M) | What If All Insects Disappeared? | 204K | 0.3x | n/a | A "what if" long-form on a big channel is below its median |
| Deep Look (2.4M) | The 4 Most Ruthless Ants We've Ever Filmed | 3.5M | 7.0x | 18 | Earwig video 5.3M, silverfish 964K (search) |
| Brave Wilderness (21.8M) | STUNG by the Murder Hornet! | 4.2M | 13.2x | 14 | Real-person stunt |
| Hornet King (1.3M) | Subterranean Yellow Jacket Nest Removed | 4.6M | 25x | 6 | Real footage |
| Dan The Bug Man (336K) | Most Insane Cockroach Infestation | 1.4M | 93x | 31 | Real footage |
| SciShow (8.4M) | Why Don't We Use Mothballs Anymore? | 1.7M | 6.8x | 11 | |
| EXPLANATION-AVENUE (167K) | The fantastic anatomy of spiders (3D animation) | 4.7M | 102x | 5 | Best animated long-form hit found; 3D, 4 years old |
| Tsuki (174K) | Ranking Each of the 7 Continents By Their Largest Insect / Spider | 219K / 182K | 4.0x / 3.3x | 19 / 16 | Ranking works on a 174K channel with animation |
| BuzzFeed Multiplayer | Do You Really Swallow Spiders When You Sleep? | 3.9M | n/a | 4.5 | Old; the myth video that owns the query |
| LEMMiNO | The Eight Spiders | 3.9M | n/a | 10 | Same myth, documentary style |
| TikTak Draw | DO WE EAT 8 SPIDERS A YEAR AS WE SLEEP? (animated) | 1.35M | n/a | 3.7 | Animated myth video |
| Peekaboo Kidz | Earwigs! Are They Dangerous? | 8.7M | n/a | 5.5 | Kids' animation, 8.7M |

## 4. (c) Patterns

**Title structures among the top 60 small-channel long-form outliers (vs the same pattern across all 487 on-topic small-channel videos in my set):**

| Pattern | In top 60 | In all 487 | Read |
|---|---|---|---|
| "Never / Don't kill [creature]" (also "Never scrape / squash / step on") | 12 (20%) | 28 (6%) | Strongest lift. 12 of the 28 such videos are top-60 outliers. But my search queries aimed at this phrase, so the sample over-represents it |
| "Every [group] ... Explained (in N minutes)" | 11 (18%) | 56 (11%) | Mild lift; numbers in the title are minutes |
| "[Thing] in your house / wall / bed / kitchen / garden / corner" | 14 (23%) | 85 (17%) | Slight lift; many are "never kill" titles |
| X vs Y / "what's the difference" | 8 (13%) | 31 (6%) | Lift, mostly wasps/bees |
| Truth / lied / myth / "really" | 9 (15%) | 54 (11%) | Slight |
| Question title | 10 (17%) | 84 (17%) | **No lift.** Matches your quiz-hook finding |
| "Ranked" | 1 (2%) | 3 (1%) | Almost nobody small ranks; the one that did got 25x on a 5K channel (Factomni hornets) |
| Dangerous / deadly / venom word | 8 (13%) | 42 (9%) | Slight |

- **Two-part title with a reversal:** "Never Kill X - [it's hunting something worse / you've misjudged it / the real reason]". The dash promises a hidden reason. 9 of the top 25.
- **Topics:** wasps, hornets, bees (8 of the top 25), house flies and mosquitoes, spiders (6), silverfish, centipedes, roly-polies, bed bugs. Almost all are creatures people meet at home or in the garden. Wasps/bees/hornets is the single most repeated topic across small channels (Sometimes Science, Xplain WILD, WiseFrog, Naji, Factomni, Insecto Media).
- **Length:** median 8.7 min; 18 of the top 60 are under 5 min, 15 are 5 to 10, 23 are 10 to 20, 4 are 20+. The Garden Whispers / Root Signal run sits at 8.6 to 12.2 minutes. Our 4 to 6 minute videos are in the range but at the short end of the winners.
- **Thumbnails (top 12 viewed, described):**
  - Garden Whispers / Root Signal / Bug Tales / Hidden Wild: one big illustrated or AI-drawn creature filling about 60% of the frame on a plain white or light background, plus 2 to 4 big words on the right ("Don't Kill It", "Don't You Dare", "Never Step on It", "Looks Weak... But It Hunts") and a hand-drawn arrow. The centipede, silverfish and mosquito ones add a shoe sole about to crush the creature. The silverfish thumbnail adds a red X. Cartoon-ish, slightly friendly faces on the creature. Black text, one red or blue word.
  - Factomni / Xplain WILD / Dolphin Explain: a grid of 4 to 8 stock-style photoreal insects on white, each labelled in small caps ("House Fly", "Bluebottle Fly", "Drain Fly"). No headline words on the image; the title does the work.
  - Sometimes Science: bright blue 4-panel grid with BEE / WASP / YELLOW JACKET / HORNET and a "WHAT'S THE DIFFERENCE?" tag; the fly one is a close-up of a fly on food with a yellow headline bar "SHOULD YOU EAT IT?" and a red arrow.
  - Insecto Media (botfly): human face in shock plus a macro of a larva under skin and "PARASITE UNDER MY SKIN!". A medical-harm hook; on a 261-sub channel with a 111-view median it got 46K, but you have found that skin/medical hooks flop for you.
  - Common thread: **one creature, huge, high contrast, 2 to 4 words or a labelled grid, empty background.** No faces of people except the botfly one.
- **What conspicuously does NOT work for small channels:**
  - **House-bug rankings.** TheEarthsCreatures "I Ranked 5 Harmful Bugs in Your Home" 9 views; BenMadeThis "Deadliest Bugs on Earth, Ranked" 3; Animol Facts "8 Bugs Ranked From Harmless to DEADLY!" 244; Wild Index 333; Primal Roots "Every Insect Moving Into Your House This Fall - Ranked" 529; LethalbyNature 688; Fresh Home 24 (5.4K subs) "Every Bug in Your House Explained" 8,270 (about 0.8x its own median). Rankings win only at MyWildBackyard (355K, 30-minute productions) and Tsuki (174K), and TierZoo-reaction channels.
  - **"What if" long-form.** What If's spiders video is median for that channel; Insider Science's insects video is 0.3x. The what-if win is the Short (BioChok 208x).
  - **Myth and quiz questions as titles.** Question titles show no lift (above). "Do you really swallow spiders" has about 25 videos; section 6.
  - **Reaction-bait, gore, bite and medical-harm hooks:** consistent with your own flops.
  - **Plain "how to get rid of X" pest-control how-tos:** huge raw views (Dan The Bug Man roach Short 1M) but only for operators with real footage and a service; not our character-led format.
  - **Part-N or series labels on their own:** only works when the series has a repeating species list (Travis McEnery) or a repeating template (Garden Whispers).
- **Crowding and survivorship (important):** searching "Never Kill the Daddy Longlegs" alone returns about 25 videos, from channels with 3, 13, 14, 32, 57, 61, 115, 161, 1.7K views, against two winners (Garden Whispers 184K, Root Signal 173K). The winners were early (31 to 184 days old in my pull) and hold audience; the late clones mostly do not.
- **Inauthentic-content risk:** these winners are templated, faceless and AI-voiced, which is exactly what MONETIZATION_PLAN.md warns the review can reject. A "Meatball" character with a narrative arc in each episode is our differentiator, not our liability.

## 5. Length and watch hours (small channels, under 150K subs, long-form, on-topic)

You need 4,000 qualified long-form hours (8,000 for new applicants from 2027-02-01). Watch hours per upload =
views x length x hold. **I could not measure hold** (heatmap blocked), so I used an **assumed** average-percentage-viewed by length:
under 5 min 44% (your own number), 5-10 35%, 10-20 27%, 20-60 18%, 60+ 10%. These are assumptions, falling with length; treat every
"hours" figure as an order-of-magnitude estimate. Views and lengths are real.

| Length | n videos / channels | Median views | Median score | Share at 2x or more | Est. hours per video (median) | Est. hours (mean, outlier-driven) |
|---|---|---|---|---|---|---|
| Under 5 min | 331 / 22 | 1,300 | 1.01 | 26% | 28 | 243 |
| 5 to 10 | 295 / 35 | 1,000 | 1.01 | 33% | 49 | 1,172 |
| 10 to 20 | 191 / 27 | 3,500 | 1.04 | 30% | 182 | 2,345 |
| 20 to 60 | 64 / 10 | 13,000 | 1.03 | 27% | 1,112 | 8,842 |
| 60+ | 13 / 3 | 20,000 | 1.26 | 46% | 5,672 | 27,433 |

Same table restricted to channels under 25K subs (closer to you): under 5 min median 893 views / 20 h; 5-10 706 / 30 h; **10-20 1,500 / 75 h**; 20-60 3,600 / 305 h (n=35, 8 channels); 60+ n=6 from one channel, not usable.
Compilation-flagged titles ("every ... explained", "complete", "ranked", "N hours"; n=141): 5-10 min median score 1.00, 10-20 min 0.96, **20-60 min 0.57 (n=18, 3 channels)**, 60+ n=4 (2 channels, median score 2.25, one huge). Non-compilation 20-60 min: median 56,500 views (n=46, driven by mid-size channels such as Travis McEnery).
Within the same channel, median views barely change with length (under 5 min 0.94x of the channel's 5-20 min median across 12 channels; 20-60 min 1.31x across 4 channels; 60+ 5x across 2 channels). Views do not fall when videos get longer here.

What this supports:
- **Per upload, 10-20 minute videos earn about 3 to 4x the hours of 5-10 minute videos at the same views, and 20-60 minute videos about 4 to 6x more again** (at assumed hold). Our 4-6 minute length is the least hour-efficient length in the table.
- Views per video do not drop with length in this sample, so the length cost is only in production effort and hold. **Confidence: low to moderate.** Scores are about 1.0 in every bucket by construction; medians in the long buckets come from 3 to 10 channels; hold is assumed; compilations are not shown to outperform single-topic videos (20-60 min compilation titles are 0.57x their channel's norm, though they still yield hours).
- Cheapest hour path that is also an outlier format: **8 to 12 minute explainer** (the Garden Whispers / Factomni shape). At 10 min, 30% hold and 1,500 views you get 75 h, so 4,000 h would need about 53 such videos; at 3,500 views (all-small median) about 22; at a Garden Whispers-class hit (300K views) a single video is worth 15,000 h on paper. The plan is therefore many 10-minute tickets, not one 4-minute one.
- Confirms and checks MONETIZATION_PLAN "Path B": 16 compilations at 2,500 views each is close to the observed median for 20-60 min compilation-style small-channel videos (3,350 views, n=18), so the arithmetic is plausible. It also says compilations need about 8 to 10 views per hour at 6 to 8 minutes watched; my 18% assumption on a 40-minute video is 7 minutes, in the same range. I cannot confirm that our own re-cut Shorts would hold that long.

## 6. (d) Animated, cartoon, AI-voiced channels

| Channel (subs) | What it is | Growth evidence | Format |
|---|---|---|---|
| Garden Whispers (19.8K) | Illustrated, AI-voiced, faceless; house/garden creatures; 45 videos in 6 months | 12 of 45 at 5x or more; 1.7M, 481K, 360K, 277K, 258K, 184K | "Never kill X - [reason]", 8.6-12.2 min, new video about every 4 days |
| Root Signal (4.4K) | Same template, silverfish, giant snails, daddy longlegs | 679K, 180K, 173K; 5 of 46 at 5x+ | 11-12 min |
| Bug Tales (240), The Hidden Wild (239), Creepwise (395) | Clones | One hit each (63K, 38K, 16K) over medians of 276 to 1,300 | Same |
| Factomni (5.4K) | Stock-photo grid explainers, AI voice | 9 of 39 at 5x+; 571K, 331K, 106K | "Every X explained in 10 minutes" |
| Xplain WILD (1.4K), Wildly Explained (316), Bug Blueprint (140), AS ExplorerX (80), Wild Decode (846) | Same grid format, other animals | Xplain WILD wasps 349K; others 13K-28K | 4-17 min |
| WiseFrog (74K) | Same format, bigger, plus Shorts | Wasp video 605K; "most venomous insects" Short 7.3M | 7-8 min |
| Dolphin Explain (20.3K) | Marine "Every ... explained" at 24-28 min | 315K (63x) | 28 min |
| Naji Explains Nature (1.5K) | Short-form explainers | "5 Wasps That Look Dangerous But Really Aren't" 144K at 2.2 min | 2 min |
| EXPLANATION-AVENUE (167K) | 3D animation, hand-made quality | Spider anatomy 4.7M; mosquito 2.9M in 61 days | 5-10 min |
| Aestheticux (26K) | 3D size comparisons | Whale comparison Short 171K | Shorts |
| Creatures Scoop (109K) | AI-voiced animal-fact Shorts | Median 31.5K; 3.4M, 1.7M, 1.5M peaks; friendly spiders 278K | 15-40 s Shorts |
| Totally Kewl Toons (4.6K), Toonder, Micah Buzan Animation | Animated swallow-spiders videos | 1.2K, 1, 4.2K | Myth video, animated |

What they grow with: a faceless illustrated creature, a short rule or reversal in the title, 8 to 12 minute length, and a high upload rate. What they don't have: a recurring character. None of the winners is character-led, so **Meatball is untested in this lane.** KNOWLEDGE.md already says character-led channels break out on weird-facts; this data cannot confirm that for bugs. Risk: this lane is exactly the "AI, CGI or templates can make easily" category in the TechCrunch policy summary.

## 7. (e) Honest read on the two committed ideas

**House-bug ranking ("Every Bug in Your House Ranked, Harmless to Nightmare").** Weak case on this data.
- Six small-channel versions found got 3 to 8,270 views (median 340ish). Winners are MyWildBackyard (355K subs, 30-minute productions, 4 to 17x its median) and a 174K-sub channel. Fewer than 1% of small-channel videos in my set are rankings.
- 20-60 minute and "ranked/every" compilations show a median score of 0.57 for small channels.
- Your 426-view result is typical for the format at your size, not a bad execution signal.
- If you keep it, change the packaging, not the format: make the ranking the spine inside a "never kill" promise. Your own "3 Bugs in Your House You Should Never Kill (And 4 You Must)" is already a kill/keep ranking and is the only long-form YouTube recommends. Title like "Kill It, Keep It, Run: Every Bug in Your House" or "The House Bugs You Should Never Kill (Ranked)" carries the proven phrase. Aim for 8 to 12 minutes.
- Hold evidence for rankings: none; heatmap blocked.

**Swallow-spiders myth.** Also weak, for three reasons.
- About 25 videos already cover it. Small channels got 1 to 5K (best small: Sleep Is The Foundation 5K, Micah Buzan Animation 4.2K, SciManDan 25K on a 673K channel); the winners are old and big (BuzzFeed 3.9M, LEMMiNO 3.9M, TikTak Draw animated 1.35M, a Korean channel 377K, Extremely Decent 99K). Animated versions by tiny channels got 1 to 1.2K views.
- "Do you really..." question titles show no lift in my sample, and your Studio data says TRUE or FALSE and quiz hooks held 20-28% against 55-63% for house-creature hooks.
- It is a strong **search** title (people type it), and it fits the myth brand, so it is a low-risk filler, not a breakout bet. If you make it, do not use a question or quiz hook. Lead with the creepy fact and the house: "There Are Spiders in Your Bedroom Right Now (And This Is What They're Doing)", then land the myth as the payoff. The data cannot show whether that wins; it is untested.
- Choose a 3 to 4 minute (or Short) version for it and spend the longer slots on "never kill" and "every X explained".

## 8. Where this data confirms, updates or contradicts earlier research

| Earlier finding | Source | This data |
|---|---|---|
| Long-form: 5 views in 30 days; Shorts feed is 82% of views | KNOWLEDGE.md | **Updates.** Not contradicted for us, but small channels in this niche get most of their outliers from long-form 8 to 12 minutes, not Shorts. Their long-form outliers are 100 to 2,400x; their Shorts outliers are mostly under 20x |
| Titles phrased as the question people type win search | KNOWLEDGE.md | **Not supported for long-form outliers**: question titles are 17% of both outliers and all videos. Compatible with search driving Shorts views, which I could not measure |
| Character-led "weird true things" breaks out; topic-led quizzes do not | KNOWLEDGE.md | **Consistent** with the quiz flops (myth videos 1-5K); **untested** for characters here (the winners are faceless) |
| Numbered "Things Living In Your House" series is the steadiest format | KNOWLEDGE.md | **Confirms at long-form scale**: Travis McEnery's "The Spiders in Your House - The [species]" occupies 5 of his top 9 (4 to 9.5x on 93.5K subs) and Garden Whispers' repeating template does the same |
| Rival outliers don't lift a base; series and sequels repeat | KNOWLEDGE.md | **Confirms and splits**: one-offs (Sometimes Science 2,396x, Botfly 414x) did not lift the channel; repeatable templates (Garden Whispers 12 of 45 at 5x+) did |
| Small channels earn hours with long compilations (692x etc.) | MONETIZATION_PLAN Path B | **Partly confirms**: 60+ minute compilation-style videos can be huge (n=4, median score 2.25, 2 channels), 20-60 min compilations typically get about 3,350 views and score 0.57 (n=18). Hours per upload are the best of any bucket; views are not. Low sample |
| Stop 11-minute daily episodes (3 min watched) | MONETIZATION_PLAN | **Contradicts partly**: 8 to 12 minute is the winning length here. The problem is the topic and packaging of the episodes, not 11 minutes. I cannot say whether viewers watch to the end |
| Keep Shorts at 20 s with a loop | MONETIZATION_PLAN | Not testable: no small-channel Shorts lengths in flat data; research/63 says 30-52 s wins on YouTube |
| "What if" Shorts: removal and bug topics (mosquito 208x etc.) | research/63 | **Confirms for Shorts**, contradicts for long-form (What If spiders 1.0x, Insider Science insects 0.3x of channel medians) |
| Plain human-hygiene "what if" is saturated | research/63 | Consistent: the same crowding pattern shows up in "never kill" and myth videos |

## 9. (f) Candidates for Meatball Myths

Rule applied: house creatures first, then backyard. Declarative or creepy-specific titles, not TRUE or FALSE. Numbers in titles marked (verify) must be checked before scripting; I did not verify them. Every candidate here rests on **views only** (retention not measured).
Skin or medical-harm hooks are avoided. Production note from section 5: aim for 8 to 12 minutes; 4 to 6 minutes earns about a third of the hours per upload.

### 9a. 12 long-form

| # | Working title | Supporting outliers | Basis / risk |
|---|---|---|---|
| L1 | Never Kill the House Centipede - It's Hunting Something Worse (Meatball's version: what it eats in your house) | Garden Whispers 481K (137x); Root Signal centipede 27K (20x); your own "3 Bugs You Should Never Kill" | Views only. Crowded template; needs Meatball-specific story |
| L2 | Never Kill the Spider in Your Corner | Garden Whispers 258K (74x) and 277K (79x); daddy longlegs 184K and Root Signal 173K; Travis McEnery cellar spider 874K | Views only. Also supports your myth brand without a quiz hook |
| L3 | Don't Kill That Silverfish - What It's Telling You About Your House | Root Signal 679K (503x); Doctor Sniffs silverfish 16K | Views only. 92 days old; one channel |
| L4 | What's Actually Living Inside Your Walls | Garden Whispers "Never Scrape This Off Your Wall" 1.7M (486x) | Views only. I do not know which creature that video covers; check before copying |
| L5 | The Spiders in Your House #1: The Cellar Spider (then #2 ...) numbered series | Travis McEnery 874K / 682K / 647K / 405K; KNOWLEDGE.md numbered series | Views only. Best fit with your series structure; 9 to 12 min per species |
| L6 | 7 Flies in Your Kitchen Explained (Only 2 Matter) (verify) | Factomni house flies 571K (204x); NATURE ARCHIVE DOCS "7 Types of Flies in Your House" 7.3K (17x); Sometimes Science fly-on-food 1.3M | Views only. Kitchen angle; avoid the "should you eat it" disgust framing |
| L7 | 5 House Bugs That Look Scary But Really Aren't | Naji "5 Wasps That Look Dangerous But Really Aren't" 144K (205x, 2.2 min); Fresh Home 24 "Do Cockroaches Bite?" 156K (15x) | Views only. Short runtime outlier; fits the kill/keep brand |
| L8 | Kill It, Keep It, Run: Every Bug in Your House | Your own "3 Bugs... Never Kill (And 4 You Must)" (171 views in 3 days, CTR 5%); Fresh Home 24 "Every Bug in Your House Explained" 8.3K | Views plus your own CTR and average-viewed. Ranking packaged as a kill/keep promise; replaces the plain ranking |
| L9 | What's Living in Your Mattress (signs, not bites) | MMPC "7 Early Signs of Bed Bugs" 561K (22x); Doctor Sniffs "Early Signs" 51K (19x), carpet beetles 59K (22x); your best Shorts are bed mites | Views only. Keep to signs and where to look, no skin imagery |
| L10 | Wasp, Hornet, Yellowjacket, Bee: How to Tell Them Apart in Your Yard | Sometimes Science 401K (739x); Xplain WILD 349K; WiseFrog 605K; Naji 144K | Views only. Strongest topic repeat in the niche; also a Shorts mine |
| L11 | Never Kill the Roly-Poly Under Your Flower Pots | Garden Whispers 360K (103x); Hidden Wild "You Keep Squashing Her" 38K (29x) | Views only. First backyard step with a known template |
| L12 | The Spiders in Your Yard: Widow, Orb Weaver, Wolf (series follow-up) | MyWildBackyard widows 1.5M (7x); Travis McEnery orb weaver 342K (3.7x); Factomni deadliest spiders 331K | Views only. Use "everyday species", not a danger ranking |

### 9b. 24 Shorts

Shorts retention cannot be measured from outside; likes per 1,000 are not available either (watch pages blocked). Numbers below are views. Titles follow your Studio finding: creepy specific fact, "in your house / bed / kitchen / basement", no TRUE or FALSE.
Hold the strongest-evidence ones for the Shorts feed (section 2b is thin), and cut the long-form outliers into 20 to 35 s Shorts as a second route.

House creatures (16):

| # | Working title | Supporting evidence |
|---|---|---|
| S1 | There's a spider in your bedroom right now. It's on your side. | Zack D. "Why You Should Leave House Spiders Alone" 12M (research/63); Creatures Scoop "Friendly Spiders" 278K (8.8x); L2 |
| S2 | Your house centipede has 30 legs (verify) and it's eating your problems | Garden Whispers 481K (137x), long-form cut |
| S3 | It's 3 AM - that's when bed mites come out (verify) | Bedbug HQ "It's 3 AM - bed bugs feed" 7.5x; your bed-mite Shorts at about 1.9K |
| S4 | One bed bug becomes hundreds | Bedbug HQ 9.0x; keep to counts, not bites |
| S5 | Bed bugs can't fly. They crawl to you. | Bedbug HQ 8.2x |
| S6 | The silverfish in your bathroom is older than the dinosaurs (verify) | Root Signal 679K (503x) |
| S7 | Dust in your house is mostly this (dust mites) | Kurzgesagt dust Short 3M (research/63) |
| S8 | There are roaches in your walls even when your house is clean (verify) | Your roach Shorts at about 1.9K; Dan The Bug Man roach Short 1M (real footage) |
| S9 | 5 house bugs that look scary but won't hurt you | Naji 144K (205x); Creatures Scoop 278K |
| S10 | Never kill this one in your basement | "Never kill" template 12 of 28 in top 60; your own recommended long-form |
| S11 | What lives under your kitchen sink | Fresh Home 24 / Doctor Sniffs household-bug lane; no direct outlier; weakest of the set |
| S12 | The fly on your food is doing this (cut of the 1.3M video) | Sometimes Science 1.3M; keep to what it does, not disgust |
| S13 | Where the "you swallow 8 spiders a year" claim came from (verify) | Myth demand (about 25 videos; TikTak Draw 1.35M); phrase as a fact reveal, not a question |
| S14 | The cellar spider (daddy long legs) in your garage and the myth about it | MyWildBackyard daddy long legs 2.5M; Garden Whispers 184K; Root Signal 173K |
| S15 | 1 mosquito, 3 things it does in your bedroom (verify) | BioChok mosquito 2.7M (208x); Vin Explains 8.7M; research/63 |
| S16 | The bug in your bathtub drain (drain fly) | Factomni "Every House Fly Type" 571K; "Drain Fly" in its thumbnail; no direct Short outlier |

Backyard (8):

| # | Working title | Supporting evidence |
|---|---|---|
| S17 | Wasp, hornet, yellowjacket - spot the difference in 15 seconds | Sometimes Science 401K; WiseFrog wasp 605K; Naji 144K |
| S18 | A wasp nest under your deck (what to do, what not to) | Hornet King 4.6M (real footage; character version is untested) |
| S19 | The most painful sting in your backyard | MyWildBackyard worst stings 826K to 861K (4x); WiseFrog "most venomous insects" 7.3M |
| S20 | A roly-poly isn't a bug. It's this. | Garden Whispers 360K (103x); Hidden Wild 38K |
| S21 | Why you shouldn't squash backyard spiders | Garden Whispers 258K / 277K |
| S22 | The black widow living in your woodpile (verify) | MyWildBackyard widows 1.5M (7x) |
| S23 | A tick in your yard is smaller than this (verify) | Zack D. ticks 17M (research/63); search results show tick-yard how-tos with 5K to 640K |
| S24 | Ants in your yard are doing this under the grass | PestWorld "Does Vinegar Keep Ants Away?" 14x; many ant-yard how-tos at 100K+; Deep Look ants 3.5M |

## 10. Next steps I did not do
- Run `data/70-heatmap-pull.py` from a network not being rate-limited, then update section 0 and add the best-holders table (last-half metric), and re-weight the candidates.
- Pull Shorts-first channels (BioChok, Hypothetica, Zack D., Creatures Scoop) for a better Shorts base; my search tool returned mostly kids' channels for "shorts" queries.
- Ask for your own Studio retention curve for "3 Bugs You Should Never Kill" to replace the assumed hold factors in section 5.
