# 85 - Which long-form shape for the new direction? Pets and big dangerous animals (2026-11-12)

Read-only research. Nothing posted, nothing scheduled, no git, no vidIQ, no Metricool changes. YouTube was touched only through `yt-dlp --flat-playlist` (search lists and channel `/videos` tabs, at least 0.35 s apart) and the public autocomplete endpoint. Google Trends came from pytrends. No watch page was opened. Only generic animal words were sent out. Rows: `data/85-longform-shapes.csv` (3,103 rows, one per video checked).

## 0. The answer in plain words

1. Pick S6, "Why It Sucks to Be Born as a [animal]", on a polar bear, 9 to 11 minutes, for Sat 11/28. Small drawn or animated channels run this one template and win with it: 26 small channels, 147 videos, 41% over 10,000 views and 17% over 100,000 (all long uploads from the same small channels: 23% and 5.5%).
2. Pets and big animals both work in S6. The "would you survive" shape (S1) has almost no small-channel base to measure, and the pet list and "your cat is telling you" shapes (S4, S5) win rarely (about 15% over 10,000, the same as any pet video).
3. Weakest point: under 20,000 subscribers, S6 is not better than normal (8% over 10,000 views, median 1,000 views). The big numbers come from channels at 20,000 to 100,000 that already won with it.
4. Polar bear is in season: YouTube Trends has "polar bear" at 201 (Nov) and 158 (Dec) against about 60 in summer.
5. Confidence: low to medium. Second choice: the same S6 shape on a house cat, to cover the pet half.

## 1. Method, and what leans to winners

- **Shapes and word lists were fixed before any view count was read** (appendix A). A title gets the first shape that matches, in this order: S3, S7, S2, S1, S6, S5, S4, then two extras I added in advance, S8 ("what if you...") and S9 ("most dangerous", "ranked", "top N"). Every shape needs an animal or pet word in the title. The S4 list is loose on purpose (any pet title that starts with a number or says "explained"), so S4 is close to "a normal pet list".
- **Finding channels (search leans to winners).** 100 `ytsearch40` lists came back (a first pass of 69 planned searches, then 38 more added because the first pass found too few S1 and S6 users; some names repeated; 5 planned searches failed three times with HTTP 403 and are missing, see section 10). Every channel with at least one long title in a shape (2 minutes or more) became a candidate: 753 channels, 752 pulled. Search ranks by relevance and popularity, so every channel here has at least one search-visible video. Treat every rate below as an upper bound for a random small channel.
- **Neutral base rate.** For each pulled channel I took its `/videos` tab, last up to 60 uploads (median 43 came back: 45% of tabs reached 60, 39% came back under 30), kept long uploads (2 minutes or more), and classified every title. A channel counts for a shape only if it uses it at least twice in that window. All the shape's videos from those channels are counted, in tab order, whatever their views. "Own median" is that channel's median views over all its long uploads. Channels need a public subscriber count, at least 8 long uploads and an own median of at least 100 (496 of 752 pass; 222 are 100K or bigger; 48 had no subscriber count).
- **The 20K row is the closest to us** (we have about 1,000 subscribers). Subscriber counts are today's counts, so a channel that grew on a shape is counted as "small". That inflates the 20K to 100K row.
- **Views are lifetime views** from flat listings, rounded to two digits above 1,000. Older videos had more time. Upload dates are not in flat listings.
- **Size effect.** Channels with 20K to 100K subscribers get about 6x the views of channels under 20K for any title. Compare a shape with the baseline in the same size band, not across bands.

Baselines (all long uploads of the 276 usable channels under 100K, found through the same searches; Pull A):

| Band | Channels | Videos | Over 10K | Over 100K | 5x own median or more | Median views |
|---|---|---|---|---|---|---|
| Under 100K | 276 | 10,840 | 22.9% | 5.5% | 13.8% | 1,400 |
| Under 20K | 191 | 6,679 | 14% | 3% | 14% | 716 |
| 20K to 100K | 85 | 4,161 | 38% | 10% | 13% | 4,700 |
| Under 100K, big-animal titles | 180 | 1,712 | 30.4% | 8.2% | 17.9% | n/a |
| Under 100K, pet titles | 166 | 3,581 | 14.2% | 3.5% | 14.3% | n/a |

## 2. Neutral base rate per shape (the main table)

Channels under 100K that use the shape at least twice. "x own median" is the median of views divided by that channel's own long-form median. Because a template channel's median is itself template videos, this number is muted (near 1) for channels that use one shape all the time. Read the shares and the 5x share. Source: Pull A, flat `/videos` tabs, 2026-11-12, `data/85-longform-shapes.csv` rows with sample `neutral`.

| Shape | Channels | Videos | Over 10K | Over 100K | 5x or more | Median views | Median x own median | Typical min |
|---|---|---|---|---|---|---|---|---|
| S1 Would you survive | 9 | 25 | 16% | 0% | 8% | 1,000 | 1.17 | 14.4 |
| S2 X vs Y | 84 | 851 | 33% | 8% | 17% | 3,600 | 1.29 | 8.1 |
| S3 What to do if / survive an attack | 21 | 79 | 20% | 5% | 22% | 1,000 | 1.28 | 5.5 |
| S4 N weird pet behaviors | 86 | 966 | 14% | 4% | 16% | 1,100 | 1.04 | 9.8 |
| S5 If your cat does X / why does my cat | 71 | 715 | 15% | 4% | 13% | 979 | 1.05 | 9.3 |
| **S6 Why it sucks to be / your life as** | **26** | **147** | **41%** | **17%** | **20%** | **3,900** | **1.28** | **8.7** |
| S7 Never run from / pet / touch | 15 | 36 | 14% | 3% | 11% | 934 | 0.93 | 10.3 |
| S9 (extra) most dangerous / ranked / top N | 47 | 209 | 30% | 11% | 20% | 2,100 | 1.00 | 10.0 |

Same, channels under 20K only (Pull A):

| Shape | Channels | Videos | Over 10K | Over 100K | 5x or more | Median views | Typical min |
|---|---|---|---|---|---|---|---|
| S1 | 6 | 19 | 0% | 0% | 11% | 454 | 9.6 |
| S2 | 61 | 633 | 24% | 5% | 17% | 2,400 | 7.0 |
| S3 | 17 | 69 | 14% | 6% | 22% | 580 | 5.1 |
| S4 | 55 | 513 | 9% | 2% | 18% | 526 | 8.6 |
| S5 | 46 | 396 | 8% | 3% | 13% | 362 | 8.9 |
| S6 | 17 | 83 | 8% | 1% | 16% | 1,000 | 7.9 |
| S7 | 8 | 19 | 0% | 0% | 5% | 346 | 10.0 |
| S9 | 35 | 144 | 17% | 6% | 18% | 1,200 | 9.2 |

Split by subject, channels under 100K (Pull A). "Base" is the baseline for that subject.

| Shape and subject | Channels | Videos | Over 10K | Over 100K | 5x or more | Median views | Min |
|---|---|---|---|---|---|---|---|
| Base, big animals | 180 | 1,712 | 30% | 8% | 18% | n/a | n/a |
| Base, pets | 166 | 3,581 | 14% | 3.5% | 14% | n/a | n/a |
| S2 big animals | 68 | 525 | 32% | 9% | 18% | 2,600 | 8.0 |
| S2 pets | 28 | 98 | 20% | 3% | 17% | 2,950 | 6.2 |
| S3 big animals | 8 | 19 | 37% | 16% | 26% | 4,800 | 8.5 |
| S3 pets | 13 | 52 | 15% | 2% | 19% | 757 | 5.2 |
| S6 big animals | 22 | 106 | 39% | 15% | 21% | 3,800 | 8.3 |
| S6 pets | 12 | 22 | 36% | 14% | 18% | 2,600 | 9.9 |
| S4 pets | 86 | 952 | 15% | 4% | 16% | 1,100 | 9.8 |
| S5 pets | 71 | 715 | 15% | 4% | 13% | 979 | 9.3 |
| S7 pets | 14 | 33 | 15% | 3% | 12% | 943 | 10.5 |
| S1 big animals | 8 | 13 | 23% | 0% | 0% | 1,100 | 16.7 |

By size band for S6 (Pull A): big animals, 20K to 100K: 8 channels, 41 videos, 88% over 10,000, 39% over 100,000, median 52,000 (baseline for that band and subject: 49% and 14%). Big animals under 20K: 14 channels, 65 videos, 8% over 10,000, 0% over 100,000, median 1,000 (baseline 19% and 5%). Pets, 20K to 100K: 6 channels, 11 videos, 55% over 10,000. Pets under 20K: 6 channels, 11 videos, 18%.

How to read these tables:
- **S6 has the biggest margin over its baseline in both subjects** (over 10,000 views: 39% against 30% in big animals, 36% against 14% in pets). It does not beat the baseline under 20K, and the 5x share (16% to 20%) is close to the baseline (14%). What it does is set the channel's typical video high: the S6 big-animal channels at 20K to 100K have a median video of 52,000 views against 9,300 for all big-animal channels in that band. Survivorship is part of that (channels that grew on S6 sit in the band).
- **S2 is real but half of it is games and compilations** (Roblox, Animal Revolt, "Animal Race" tournaments). Without those words (a post-hoc filter): big animals under 100K, 65 channels, 468 videos, 29% over 10,000, 8% over 100,000, 7.3 minutes.
- **S4, S5 and S7 are the pet baseline.** Most pet channels title most videos this way, so there is no lift: 13% to 16% reach 5x, the same as any pet video (14%). S7 on pets is slightly below. The shape that bug long-forms won with ("Never Kill X") has no small-channel base on pets or big animals in this pull (15 channels, 36 videos, 11% at 5x).
- **S1 cannot be measured.** The 25 videos from 9 channels are mostly not "would you survive [big animal]". I judged by title: Roblox "Survive The Swarm" guides (7), "Could [animal] survive [a prehistoric era or place]" (7), "How did ancient humans survive [predators]" (6), "Can one elephant survive giraffe attacks" (3), and 2 real-footage African wildlife videos. No small channel in this pull uses "would you survive [animal]" with the viewer in the scene more than once. The one search-first example is Lanternstick (25 subscribers, stickman explainer): "Could You Survive a Night Near a Lion Pride?", 766 views.
- Single-use channels (they use the shape once, so they are not in the table above; Pull A): S1 21 channels, 9% over 10,000; S2 35 channels, 37%; S3 29 channels, 37%; S6 20 channels, 30%; S7 39 channels, 20%.

### Shapes I did not plan that small channels also use (found after looking at the winners, so post-hoc)

Pull A, channels under 100K with at least two uses:
- **X1 "Your DOG/CAT ... (Don't ignore this)" and "this is what you're doing to their brain":** 34 channels, 181 videos, 16% over 10,000, 6% over 100,000, 10% at 5x, median 846. Individual hits: "Your Dog Doesn't See You as Human" 3.7M (Dogunee, 48K subs), "Your CAT Waits Their WHOLE LIFE For You to DO THIS" 232K (KittyTips, 88K). A guilt hook, real footage, 9 to 12 minutes.
- **X2 "Every [animal group] ... explained in N minutes":** 6 channels, 44 videos, 50% over 10,000, 25% over 100,000, 36% at 5x, median 9,900, 8.5 minutes. Small, but the best 5x share of anything in the pull (Tillow 18K subs, Factomni, Animated Earth). Not tested on pets or on danger.
- **X3 "How dogs/cats recognize a bad person: 12 silent signs":** 6 channels, 16 videos, 18% over 10,000. Too small to read.
- **S9 (planned extra) "most dangerous / ranked / top N":** see table. Big animals: 28 channels, 92 videos, 41% over 10,000. Our own bug ranking got 5 views (research 70), so I would not lead with it.

## 3. Search-first examples (upper bound)

Pooled search rank (rank 1 of every query, then rank 2, and so on), channels under 100K, at most 2 per channel, long videos only, channel own median at least 100. This sample leans to winners: it is the best results YouTube search returns for these words. Source: Pull B, 100 `ytsearch40` lists, 2026-11-12. Rows in the CSV with sample `search_first`.

**S1 Would you survive** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| How Did Ancient Inuit Survive Nights Surrounded by POLAR BEARS? | Before Us YT | 10 | 1,099 | 12.9 | 10.37 |
| Could Moose Survive the Cretaceous Arctic? - Antlers in the Age of Dinosaurs - | CreatureArchives | 56,600 | 54,228 | 15.4 | 0.72 |
| How Did Ancient Humans Survive Predators? | Ink Speculator | 49 | 282 | 26.7 | 1.54 |
| Could You Survive a Night Near a Lion Pride? | Lanternstick | 25 | 766 | 7.6 | 5.7 |
| How Did Ancient Humans Survive Predator Attacks at Night? | Nemo Explainer | 172 | 152 | 18.4 | 0.36 |
| How Did Ancient Inuit Survive Nights Surrounded by POLAR BEARS? | Primitive Minds • 32m vi | 103 | 411 | 3.2 | 1.28 |
| Can You Survive 1 Year In an Underwater Billionaire Bunker | StickDread | 986 | 14,991 | 19.2 | 2.42 |
| Could You Survive Every Crocodile With Just a Rambo Knife? | Thomas Blackridge | 598 | 409 | 10.8 | 1.04 |
| How Did Ancient Inuit Survive Nights in a World Full of POLAR BEARS? | Why Humans | 88 | 148 | 8.0 | 0.93 |
| Can You Survive The Rhino? - AutoFlux Games 2 (Event 3) | automotiveflux | 66,500 | 13,526 | 25.4 | 4.23 |

**S2 X vs Y** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| Wolf vs Dog. Who is stronger Wolf or Dog? | ANIMALS VERSUS | 1,200 | 5,190 | 3.2 | 6.06 |
| Steppe Wolf VS Volkosob dog - Who Will Win the Fight? | ANIMALS VERSUS | 1,200 | 611 | 3.3 | 0.71 |
| 1 Wolf vs 10 Guard Dogs: Who Actually Wins? | Amazing Dogs | 55,900 | 2,086 | 8.4 | 3.48 |
| GRIZZLY BEAR vs LION - Who Would Win? | Creature Challenge | 95,200 | 289,095 | 12.7 | 4.63 |
| LION vs GORILLA - Not Even Close | Creature Challenge | 95,200 | 445,143 | 11.6 | 7.12 |
| ALIEN RHINO & BLACK RHINO IS HUNTING #1! Who Will Survive?  ARBS - Animal Revo | GamerNoob | 3,960 | 1,052 | 10.0 | 0.39 |
| Joe Rogan: Lions VS Tigers - Who is the real king? - Andrew Dice Clay / JRE #1 | JRE BEST Clips | 8,200 | 44,475 | 3.8 | 16.17 |
| Who Would Win?  Lion vs. Tiger | Kelly Gant | 299 | 12,532 | 9.2 | 4.82 |
| 💀🐘 ALIEN ELEPHANT Is HUNTING Everyone! 😱🔥 WHO WILL SURVIVE? / Animal Revolt Ba | Legend Arbs gaming | 18,000 | 8,999 | 15.9 | 0.75 |
| Dinosaur vs. Animal Size Comparison / #dinosaur #animation #gaming | funnymation | 12,200 | 1,038,293 | 2.8 | 27.32 |

**S3 What to do if / how to survive an attack** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| How to Defend Against Dog Attack | Athletic Engineering | 28,000 | 3,727,419 | 17.7 | 9080.19 |
| Shark Safety - What to do if you see a shark | California State Univers | 4,650 | 69,513 | 2.6 | 237.25 |
| How To Survive Every Wild Animal Attacks / Stick Figure Animation Survival | Jake Explains Everything | 17 | 114 | 19.8 | 0.42 |
| How to Survive Every Bear Attack... | Mr. Amazing | 16,400 | 1,470 | 8.6 | 0.19 |
| If a bear charges at you, DON'T run: do THIS | Panic Proof | 121 | 154 | 9.1 | 0.72 |
| How to survive a crocodile attack | Survival Edge | 743 | 186 | 4.5 | 1.65 |
| What to do if you meet a moose | The Denver Post | 72,000 | 17,510 | 2.2 | 48.77 |
| What To Do If You Encounter A Bear: It's Not What You Think | Wilderness Grandpa | 16,100 | 324,798 | 18.0 | 324.8 |
| WHAT TO DO IF YOU ENCOUNTER A MOOSE!!! | William 180 | 18,700 | 9,217 | 12.4 | 3.29 |
| How To Deal With A Moose Encounter [WARNING SIGNS] And How To Survive | YoYo Survivor | 605 | 17,721 | 5.3 | 41.5 |

**S4 N weird dog or cat behaviors** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| Why Do Cats Stare at Nothing ? 6 Reasons for This Behavior | Animal Kingdom | 341 | 1,806 | 5.3 | 9.95 |
| 30 Dog Man Facts You Didn’t Know (2026) | DORIAN'S WORLD | 69,900 | 21,195 | 8.2 | 1.25 |
| 15 Weird Dog Behaviors Explained | Doggy Drifts | 27,200 | 1,268,849 | 8.4 | 2130.73 |
| Weird Dog Behaviors Explained - Be surprised | Dogs are Legend | 2,900 | 109 | 6.5 | 0.45 |
| 60 Strange Dog Behaviors Finally Explained | Happy Dogs Place | 48,000 | 782,737 | 49.8 | 504.99 |
| 10 Weirdest Dog Behaviors Finally Explained | INFORAMA | 20,100 | 943 | 9.2 | 1.32 |
| 10 Brutal Differences Between a Wolf and German Shepherd | Memedogs Tv | 5,750 | 465 | 14.4 | 0.26 |
| Cat Behavior Explained: Shocking Truth Behind 20 Strange Things Cats Do | Meowtopia | 67,200 | 5,641 | 30.2 | 5.66 |
| 11 Weirdest Dog Behaviors Explained - The Surprising Science Behind Your Dog's | PetSpotlight | 1,280 | 4,017 | 8.6 | 7.12 |
| 7 Signs That Your Dog Has Imprinted on You (Not Every Dog Owner) | Smelly Belly | 74,800 | 3,130,067 | 8.7 | 2158.67 |

**S5 If your cat does X / why does my cat** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| If Your Dog Ever Speaks A Language You Don't Know… DON'T ANSWER | Bradikinin | 58,700 | 25,264 | 8.9 | 0.18 |
| 12 Things Your Cat is Trying To Tell You | Cat Curiosity | 2,510 | 22,654 | 11.4 | 39.33 |
| If Your Cat Does This, They Have Officially Adopted You as Their Mother | Cats Insider | 96,600 | 415,834 | 17.9 | 127.95 |
| Your Dog Doesn’t See You as Human – (Here’s What You Really Are to Them) | Dogunee | 48,400 | 3,688,000 | 9.8 | 498.38 |
| Why Your Dog Follows You Everywhere and 9 Other Weird Dog Behaviours Explained | INFORAMA | 20,100 | 3,811 | 8.7 | 5.34 |
| If Your MALE Cat Sleeps With You, He's Trying To Tell You Something | KittyTips | 88,000 | 100,344 | 27.1 | 18.93 |
| If Your Cat Does This, DON'T Get Angry - They’re Showing Love | Leo Bennett | 26,000 | 1,637 | 12.8 | 0.22 |
| If Your Cat Does These 10 Things, You're Doing Everything Right | Steve Cooper | 59,300 | 24,963 | 15.6 | 0.83 |
| Why Does My Dog Follow Me Everywhere?🐶5 Surprising Reasons | Woof & Whiskers | 2,860 | 59 | 3.0 | 0.29 |
| If Your Cat Does This… Don’t Get Angry - They’re Showing Love | caiamecat | 8,610 | 310,105 | 8.5 | 731.38 |

**S6 Why it sucks to be / your life as** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| Why It Sucks To Be Born As A Wolf | Dodo Diaries | 25,400 | 67,732 | 8.2 | 1.2 |
| Why It Sucks To Be Born As A Cat | Dodo Diaries | 25,400 | 218,376 | 8.6 | 3.87 |
| why it sucks to be born as a lion. | Mr scribbles | 26,400 | 686,673 | 5.7 | 114.45 |
| Your Life as a Black Cat in the Middle Ages | Reaperology | 6,940 | 158,457 | 9.1 | 31.07 |
| Your Life as a Hunting Dog in the Middle Ages | Reaperology | 6,940 | 71,498 | 11.3 | 14.02 |
| Why It Sucks to Be a Savlar Chem Dog? (Warhammer 40K Lore) | Scribe 40k | 12,200 | 8,768 | 14.3 | 1.0 |
| Why it Sucks to be Born as a Normal Dog in 2026 #dog | Sketching the Wild | 38,300 | 75,037 | 19.8 | 2.94 |
| Why It Sucks To Be Born As a Grolar Bear | Sketching the Wild | 38,300 | 19,312 | 12.3 | 0.76 |
| Your Life as Every Wolf Pack Rank | The Animal Person | 46,200 | 335,065 | 14.8 | 6.44 |
| Why It Sucks To Be Born As a Cat | Zoozle | 35,400 | 365,165 | 9.9 | 5.99 |

**S7 Never run from / pet / touch** (first 10 by pooled search rank, channels under 100K, at most 2 per channel)

| Title | Channel | Subs | Views | Min | x own median |
|---|---|---|---|---|---|
| Never Play Dead With a Polar Bear. It Plays Dead Better Than You. | Ghoxt | 79 | 431 | 9.5 | 4.1 |
| WHY YOU SHOULD NEVER PLAY DEAD WITH THE WRONG BEAR | Abyson | 2,940 | 120 | 7.0 | 0.07 |
| Read Aloud Book - Never Touch a Grumpy Bat | Book Reading with Sammy | 45,500 | 66,445 | 2.2 | 4.29 |
| If Your Dog Ever Stops Moving... DONT PET IT | Final Sight | 32,800 | 530,703 | 6.5 | 2.03 |
| Jim Stafford   Don't Pet The Dog | Hippety Hop | 9,870 | 906,677 | 3.1 | 6.43 |
| Never Punish Your Dog | Jake Folger | 24,500 | 713 | 6.1 | 3.04 |
| Moose - This River Will Never Run Dry | MarkTurver1990 | 24,300 | 16,203 | 6.4 | 1.25 |
| NEVER Play Dead When a Grizzly Does THIS - Native American Survival Advice | Mr. Whitaker (The Morti | 1,250 | 124 | 12.9 | 0.5 |
| Why You Should Never Run From a Bear | Mystellect | 84 | 56 | 4.8 | 0.37 |
| Never Approach a Bear That Stands Still in Appalachia | not my stories | 21,800 | 70 | 24.6 | 0.23 |


For S1 the search returns almost no "would you survive [animal]" videos from small channels; most rows are history or paleo videos and games that share the words (see section 2). For S7 the first page is mostly kids' read-alouds and bear survival stories. These rows show what YouTube hands a searcher, not what a new channel can expect.

## 4. Length of the winners

Winners are videos at 5x their own channel's median or more (Pull A and Pull B, de-duplicated; 511 videos, shapes S1 to S7 and S9). Source: `data/85-longform-shapes.csv`.

| Group | Winners | Under 5 min | 5 to 8 | 8 to 12 | 12 to 20 | 20+ | Median min |
|---|---|---|---|---|---|---|---|
| All shapes | 511 | 79 | 110 | 160 | 104 | 58 | 8.9 |
| Big-animal titles | 149 | 21 | 38 | 41 | 23 | 26 | 8.8 |
| Pet titles | 305 | 43 | 64 | 111 | 66 | 21 | 8.9 |
| S2 X vs Y | 150 | 43 | 36 | 28 | 23 | 20 | 7.2 |
| S3 attack how-to | 22 | 8 | 2 | 4 | 8 | 0 | 8.4 |
| S4 pet list | 160 | 14 | 39 | 48 | 44 | 15 | 9.4 |
| S5 pet one behavior | 98 | 7 | 22 | 46 | 18 | 5 | 9.3 |
| S6 sucks to be | 30 | 0 | 5 | 19 | 5 | 1 | 9.7 |
| S7 never | 5 | 2 | 0 | 1 | 1 | 1 | 8.0 |

For comparison, all 3,066 distinct videos in the file have a median of 9.1 minutes, and the videos over 10,000 views have a median of 11.1 minutes (longer videos collect more views over time, so that is partly an age and length effect).

Answer: 8 to 12 minutes holds as the most common bin for S4, S5 and S6 (and S6 has no winner under 5 minutes), but it is only about 31% of all winners, and 5 to 12 minutes is 53%. Pet and big-animal winners do not run shorter or longer overall (median 8.9 and 8.8). S2 winners run shorter (median 7.2, many 3 to 5 minute clips) and S3 winners are bimodal (under 5 and 12 to 20). S1 and S7 have too few winners (4 and 5) to say.

## 5. Search demand

### 5a. YouTube autocomplete (rank order only, no volumes)

Source: `suggestqueries.google.com`, `client=youtube`, US and English, pulled 2026-11-12, 35 seed phrases, 0.5 s apart. Echoes of the seed itself are dropped. The endpoint returns at most 14 and gives fewer for narrow phrases.

| Seed | Top suggestions in rank order |
|---|---|
| would you survive | a zombie apocalypse; as a sephora employee; as a kpop idol; these katseye mvs; as a nail tech; as a girl; as a billionaire's daughter; (role-play and game phrases, no animal) |
| would you survive a bear | can you survive a bear attack; can you survive a polar bear attack; how do you survive a bear attack; how to survive against a bear |
| would you survive a grizzly | would you survive a grizzly bear attack (only one) |
| what to do if a bear | approaches you; attacks you; attacks you funny video; is outside your tent; is chasing you; charges you; attacks; climbs a tree; charges; (what to do) when a bear is near you |
| what to do if a dog | is choking; is chasing you; bites you; charges at you; has a seizure; eats chocolate; attacks your dog; tries to attack you; eats a grape; barks at you |
| why does my cat | bite me; lick me; sleep on me; meow so much; follow me everywhere; stare at me; lick me then bite me; bite me when i pet him; keep meowing; sleep next to me |
| why does my dog | lick me all the time; lick me; follow me everywhere; stare at me; walk sideways; eat grass; lick my feet; lick his paws; keep licking his paws; eat poop |
| bear vs | tiger; gorilla; moose; lion; shark; bear; bison; dog; wolf; man |
| lion vs | tiger; hyena; crocodile; gorilla; tiger real fight; bear; hippo; lion; tiger roar; elephant |
| how to survive a | zombie apocalypse; as a wandering knight; tornado; a quiet place; blackout; hantavirus; tsunami; nuclear attack; bear attack; alma doors |
| how to survive a bear | attack; encounter; attack meme; attack zack d films; attack rdr2; attack animated; attack sonic; funny; attack abc news; sloth bear attack |
| never run from | a whooping; a niger; a police dog; a fade; a bear; the call; gsp; big d randy; fear; fear face everything and rise |
| never run from a bear | "this is why you never run from a kodiak bear" (only one) |
| never pet a | burning dog; dog; chimpanzee; (then song and meme phrases) |
| if your cat | sleeps with you; could talk; is misbehaving do a scoop; does this; smiles run; is staring at you; walks on you at night; jumps on your chest; can sing; grew to the size of a tiger |
| if your dog | ever stands on two legs... act normal; stands on two legs; starts laughing; sits facing away from you meme; stretches when they see you; stops blinking; stands up; starts barking at night; does this |
| a day as a | teacher; electrician apprentice; nurse; hvac technician; homeschooler; firefighter; lion; police officer; (other jobs) |
| why it sucks to be | born as (only one) |
| weird dog behaviors | explained; funny dog behaviors (only two) |
| weird cat behaviors | explained; strange cat behavior; funny cat behaviors; odd cat behaviors explained; odd cat behaviors; strange cat behavior at night; weird cat habits |
| who would win | books; books read aloud; in a fight; a rabbit; animal fights; animals; gojo or goku; brain break; lion vs tiger; ultimate snake rumble |

What it says (rank order, so no volumes):
- Pets (S5): the phrases are the ones the shape uses ("why does my cat lick me", "if your cat walks on you at night", "weird dog behaviors explained"). Strongest demand evidence of the seven shapes.
- Big animals: people type "bear vs [animal]", "lion vs [animal]", "what to do if a bear/shark/moose [attacks, charges]" and "how to survive a bear attack". "Would you survive" returns role-play and game phrases, and "never run from a [bear]" almost nothing (one suggestion). So S1 and S7 titles are not typed searches; S2 and S3 are.
- "Why it sucks to be born as" is one phrase, which fits a browse-and-suggested shape, not a search one. Its views would come from Browse and Suggested, like Part 1 (96% from those).

### 5b. Google Trends (US, 5 years, web and YouTube search)

Source: pytrends, 2026-11-12, `timeframe today 5-y`, geo US, one term per request. Monthly index = month average of the weekly values divided by the term's own mean, times 100; November 2026 is left out (partial). An index compares months of ONE term, never two terms. YouTube Trends is noisy for narrow terms (the last row is 95% zero weeks: ignore it).

| Term | Web Nov | Dec | Jan | Feb | Web peak | YT Nov | Dec | Jan | Feb | YT peak | YT zero weeks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| why does my cat | 97 | 104 | 110 | 98 | Jan | 94 | 100 | 95 | 86 | Jul | 15% |
| why does my dog | 96 | 105 | 106 | 98 | Jul | 100 | 100 | 99 | 88 | Jun | 9% |
| cat behavior | 91 | 88 | 98 | 124 | Feb | 78 | 86 | 87 | 94 | Jun | 6% |
| dog behavior | 91 | 86 | 95 | 125 | Feb | 83 | 101 | 92 | 88 | Aug | 8% |
| bear attack | 86 | 74 | 82 | 70 | May | 100 | 102 | 100 | 86 | Jul | 0% |
| grizzly bear | 91 | 87 | 89 | 88 | Jul | 102 | 104 | 97 | 92 | Jun | 0% |
| shark attack | 42 | 85 | 66 | 89 | Jun | 72 | 83 | 88 | 104 | Jun | 0% |
| polar bear | 108 | 133 | 129 | 113 | Dec | 201 | 158 | 96 | 74 | Oct | 0% |
| would you survive | 93 | 73 | 96 | 120 | Apr | 85 | 102 | 90 | 82 | Jul | 8% |
| lion vs tiger | 90 | 101 | 106 | 104 | Apr | 97 | 117 | 118 | 101 | Jan | 0% |
| what to do if a bear | 82 | 67 | 73 | 88 | May | 78 | 0 | 0 | 0 | Aug | 95% |

Winter read (November to February):
- **Polar bear is high season.** Web 108, 133, 129, 113; YouTube 201, 158, 96, 74 (summer YouTube about 60). Best fit of anything here for 11/28.
- **Grizzly and bear attack are flat to slightly low** (web 87 to 91 and 70 to 86; peak May to July).
- **"Would you survive"** web: Nov 93, Dec 73, Jan 96, Feb 120. Dip in December, up from February.
- **Pet terms are flat** all year (web 86 to 110; the one rise is "cat behavior" and "dog behavior" in February, 124 and 125). Winter is not low season for pets.
- **Shark attack** is the one summer-only term (web Nov 42).
- **"Lion vs tiger"** is flat (90 to 106).

## 6. Crowding

How many of the first 20 flat search results come from channels over 1 million subscribers. One query per shape, Pull B, 2026-11-12 (channels whose subscriber count YouTube did not show are counted as not big and listed as unknown).

| Shape | Query | Of 20 from channels over 1M | Unknown |
|---|---|---|---|
| S1 | would you survive a polar bear | 4 | 2 |
| S2 | lion vs tiger who would win | 4 | 0 |
| S3 | what to do if a bear attacks | 13 | 1 |
| S4 | weird dog behaviors explained | 5 | 1 |
| S5 | why does my cat | 12 | 1 |
| S6 | why it sucks to be a lion | 0 | 2 |
| S7 | never run from a dog | 11 | 0 |

S6 is the least crowded of the seven at the head of the results. S3, S5 and S7 are crowded (11 to 13 of 20). Research 83 got 12 of 20 for "why does my cat" too. Crowded does not mean closed: caiamecat (8.6K subscribers) has 310K on an "If Your Cat Does This" title. But S6 has bigger channels above the first page (Dinzo 475K subscribers; James Toland 386K, "Your Life as a Polar Bear" 1.1M views).

## 7. Fit: small drawn, animated, stick-figure or narrator-with-jokes channels winning with each shape

Judged from channel descriptions (Pull A, first 300 characters) and titles. I could not watch a single video, so "drawn" and "funny" are unverified for all of them.

| Shape | Small channel | Subs | What the description says | What it wins with |
|---|---|---|---|---|
| S6 | Sketching the Wild | 38.3K | "tells animated stories about animals born into unfair biology" | "Why it Sucks To Be Born As a Jaglion" 1.5M; white tiger 311K; wolfdog 615K; own median 25.5K |
| S6 | Zoozle | 35.4K | "Ever thought being an animal is easy? Yeah, no." | Komodo dragon 812K, cat 365K; own median 61K |
| S6 | Mr scribbles | 26.4K | "an animation channel ... with some jokes here and there" | "why it sucks to be born as a lion." 686K, hyena 449K |
| S6 | The Animal Person | 46.2K | "funny animal POV adventures ... how they survive" | King cobra 373K, rattlesnake 301K, "Your Life as Every Wolf Pack Rank" 335K |
| S6 | Dodo Diaries | 25.4K | (no description) | "Why It Sucks To Be Born As A Cat" 218K, wolf 68K |
| S6, above the 100K cut | Dinzo 475K, James Toland 386K ("Animated videos") | | | 8 to 14 minute videos at 1M to 7M |
| S1 | Lanternstick | 25 | "stickman explainer channel" | one video, 766 views. No real winner. |
| S1 (nearest) | StickDread | 986 | "stickman survival stories" | "Billionaire Bunker Survival: 1 Year" 193K, but it is human survival, not animals |
| S3 | Panic Proof | 121 | "animated breakdowns ... with a stick figure who keeps making the wrong move" | bug content, 154 views on a bear video. No winner. |
| S2 | Creature Challenge | 95.2K | "a biologist dude talking about animals and deep diving into wildlife hypotheticals" | "Lion vs Gorilla" 445K, "Grizzly Bear vs Lion" 289K (narrator, not drawn) |
| S2 | Animalikeus, funnymation | 56.9K, 12.2K | animated animal characters | millions of views, but they are short funny clips and size comparisons, not narrated vs videos |
| S4, S5, S7 | none found | | | all the winners are real-footage pet channels (Dogunee, Cat Club, Smelly Belly, caiamecat) |

So S6 is the only shape of the seven where small drawn or animated channels with a joke voice are winning, and several of them run it as their whole channel. Nothing in this pull is a small drawn pet channel winning on S4, S5 or S7. Meatball's lane (a recurring character with facts and jokes) still has no direct match: all of these are narrated or POV with no recurring character.

## 8. Options for the 11/28 long-form

Hours arithmetic (mine, not measured): a 9.7 minute video (the S6 winner median) at 40% average viewed (Part 1 got 38 to 44%) gives about 3.9 minutes per view. 4,000 hours is 240,000 minutes, so about 62,000 views. One S6 hit at the median of the 20K to 100K channels (52,000 views) is most of the way. A video at our recent long-form level (5 to 180 views) is not.

All four options keep the long-form checklist (research 72): narration from 0.0 s on the animal, no joke before 0:25, a count and an order in the first 15 s, part of the promise paid before 1:00, a new peak every 20 to 30 s, a mid-point re-hook, a character beat every 30 to 40 s, an ending that calls back to the open. Every option needs a fact pack, a script from the pack only, and a live-source check by a different model before it is built. Three titles go into Test & Compare.

### Option 1 (my pick): S6 on a polar bear

- **Shape and working title:** "Why It Sucks to Be Born as a Polar Bear". The viewer is the animal; each chapter is one more way the life is unfair, and the facts carry the jokes. Alternate title for the same video in Test & Compare: "Why Being Born a Polar Bear Is a Terrible Deal" (see the note on "sucks" below).
- **Length:** 9 to 11 minutes (S6 winners: median 9.7, none under 5, 19 of 30 at 8 to 12).
- **Evidence for:** the highest share over 10,000 (41%) and over 100,000 (17%) of the shapes with a base rate, and the widest margin over its subject baseline (39% against 30% in big animals, 36% against 14% in pets); 20% reach 5x. Five small animated channels with a joke voice run it (section 7). Least crowded head of results (0 of 20 over 1M). In season (YouTube Trends polar bear Nov 201, Dec 158). Polar bears are a good S6 subject because the facts are harsh. A 470-subscriber channel got 6,700 views (7x its median) on the polar bear one (Brinzo).
- **Evidence against:** under 20K subscribers the shape is not better than normal (8% over 10,000, median 1,000). The big numbers are channels that were already winning. The template is cloned (Dinzo, Zoozle, Dodo Diaries, Sketching the Wild all run it; James Toland has "Your Life as a Polar Bear" at 1.1M). It is not a search shape (Browse and Suggested only). It is not "Would Meatball Survive?". Our own earlier non-bug long-forms got 5 to 162 views, so a good shape does not guarantee a result, and the same shape can do 3,500 or 679,000 on packaging (research 70).
- **Cost:** a new polar bear fact pack (sources to pull: a government or university polar bear study, a polar bear conservation group, a sea-ice record; I did not check any of them). Polar bear is in the drawing kit. The structure is new for us (a day or year as the animal, no shoe meter), so it needs a new chapter plan, but not new tooling.
- **Note on "sucks":** the 11/11 rule keeps mild words out of titles ("never in a title"). "Sucks" is not on that list but is the same kind of word. Test both titles and let Nolan decide.

### Option 2: S6 on a house cat (the pet half)

- **Shape and working title:** "Why It Sucks to Be Born as a House Cat". Same skeleton as Option 1, so it could go on 12/5 and reuse the script frame.
- **Length:** 9 to 11 minutes.
- **Evidence for:** S6 pets 12 channels, 22 videos, 36% over 10,000, 14% over 100,000 (pet baseline 14% and 3.5%). Zoozle has the cat one at 365K and Dodo Diaries 218K; the dog one on Sketching the Wild got 75K. Flat demand in winter. A cat owner is the widest audience (YouGov: 35% of Americans have a cat, via research 83).
- **Evidence against:** the base is thin (22 videos) and under 20K it is 11 videos. The two best cat videos already exist on bigger channels. Our pet Short results are not read yet.
- **Cost:** a cat fact pack (new). Cat is in the kit.

### Option 3: S5 on a cat, second person

- **Shape and working title:** "If Your Cat Sleeps on Your Chest, She Is Telling You This".
- **Length:** 9 to 10 minutes (S5 winner median 9.3).
- **Evidence for:** the strongest search demand (autocomplete "if your cat walks on you at night", "jumps on your chest", "why does my cat sleep on me"). Flat in winter. Small winners exist: caiamecat (8.6K subs) 310K, Cat Curiosity (2.5K) 22.7K, Cats Insider 416K.
- **Evidence against:** 15% over 10,000 and 13% at 5x, the same as any pet video, so no lift. 12 of 20 results are from channels over 1M. All the winners are real-footage channels, none drawn. Weakest fit of the four.
- **Cost:** cat behaviour fact pack from vet and behaviour papers (new). Cat in the kit.

### Option 4: S3 on a moose, safety how-to

- **Shape and working title:** "What to Do If a Moose Charges You (And Why Bears Are Not the Real Danger)".
- **Length:** 8 to 9 minutes.
- **Evidence for:** typed queries exist ("what to do if a moose charges you", "attacks you"). Big-animal S3: 37% over 10,000, 26% at 5x (8 channels, 19 videos, thin). Small hits: YoYo Survivor (605 subs) 17.7K on a moose encounter, Wilderness Grandpa (16K) 325K on bears. The moose Short already has fact-checked sources (MASTER_ORDERS 11/11 says it was checked against live sources), so part of the pack exists.
- **Evidence against:** 13 of 20 bear-attack results are from channels over 1M. S3 winners are bimodal and 8 of 22 are under 5 minutes. No drawn winner. Medical and attack advice is close to the topics that flopped for us, and every safety claim needs an official source. Bear-attack interest is lower in winter (web 70 to 86).
- **Cost:** a moose pack that extends the Short's sources; moose is in the kit.

### Not chosen

- **S2 "X vs Y":** the share over 10,000 is good (33%), but half the sample is games and animal-race compilations, winners run short (median 7.2), and the clean narrated winners are one biologist channel (Creature Challenge, 95K). Keep S2 for Shorts.
- **S1 "Would you survive":** no base rate. Not a typed search. Keep it as the show name for Shorts; do not build a long-form on it first.
- **S7 "Never run from / pet / touch":** the shape that works for bugs is below the baseline here (11% at 5x, 15 channels, 36 videos).

## 9. Pick

**Option 1, S6 on a polar bear, Sat 11/28 08:00.** Confidence: low to medium (my guess, one in four that it passes 1,000 views in a week, one in ten that it passes 10,000). Reasons: it is the only shape with a small, animated, joke-voice winner set and a base rate above its baseline; it fits the half of the direction that is big dangerous animals without leaning on a shape with no base (S1); it is least crowded; it is in season; and it keeps the 8 to 12 minute length the bug long-forms already use. The main risk is the under-20K row.

**Second choice: Option 2** (the same shape on a house cat) for the pet half, on 12/5 or midweek. Option 3 is third. If the polar bear video gets under 3% click-through at 72 hours, change title and thumbnail the same day (the rule in MASTER_ORDERS), and do not build the cat version until the polar bear one has been read.

Queue change this proposes: replace the 11/28 08:00 slot's planned "Don't squish it" silverfish or mice episode with the polar bear S6 episode (or put it on the 11/25 midweek slot if Night Shift moves), and start the polar bear fact pack now. I changed nothing.

### Six more title candidates for S6 (none uses a banned word; "sucks" versions have a milder twin)

1. Why It Sucks to Be Born as a Grizzly Bear / Why Being Born a Grizzly Bear Is a Terrible Deal
2. Why It Sucks to Be Born as a Moose / Why Being a Moose Is Harder Than It Looks
3. Why It Sucks to Be a Mother Polar Bear
4. Your Life as a Polar Bear: A Year of Trying Not to Starve
5. Why It Sucks to Be Born as a Hippo (The Most Dangerous Animal With the Worst Life)
6. Why It Sucks to Be Born as a House Cat

(Check each claim in a title against the fact pack before use; "most dangerous" in 5 and "trying not to starve" in 4 are examples that need a source or a rewrite.)

## 10. Could not be measured

- **Retention, most-replayed, click-through and subscribers gained for any video.** Watch pages were not opened. Everything is views.
- **Whether any channel is actually drawn, animated or funny.** Judged from the first 300 characters of descriptions and titles. I did not watch a video.
- **Structure of the S6 winners** (how each chapter is built, how long the cold open is). Not visible from titles.
- **A true neutral sample.** Every channel came from a search, so each has at least one search-visible video. The channel set is not random.
- **Survivorship in subscriber counts.** Counts are today's; a channel that grew on S6 is counted as "small". The under 20K rows reduce this but do not remove it.
- **Upload age.** Flat listings give no dates, so lifetime views are not adjusted for age.
- **The first 60 uploads only.** 39% of tabs came back with fewer than 30 entries (some channels have fewer uploads, some tab continuation requests returned HTTP 403 and I did not work around that). 45% reached 60.
- **Search depth.** Each search list held 40 results, but 5 planned searches failed three times with HTTP 403 and are missing: "strange dog habits", "if your dog does this it means", "your life as a", "never run from a", "never stare at a". Lists beyond the first 20 results may differ by day.
- **S1 and S7 base rates** (too few small channels using them; see section 2) and any base rate for S1 on pets.
- **Shape classification is by title words.** Some videos are wrong by shape (S1 hits include games and paleo videos; S4 includes any pet title that starts with a number). Domain (big animals or pets) is also by title words.
- **Channels with no public subscriber count** (48), and 1 channel whose tab failed to pull, are left out of every rate.
- **Autocomplete and Trends show rank and shape of the curve, not volume.** Google Trends and YouTube Trends scale each term to its own peak. "What to do if a bear" on YouTube Trends is 95% zero weeks and is not usable.
- **Crowding** is one query per shape, first page only, and 0 to 2 channels per query had no subscriber count.
- **TikTok.** Not touched. Everything here is YouTube long-form.
- **Whether the shape works for a 1,000 subscriber channel with a recurring character.** No match in this pull. Episode 1 is the test, as research 70 said for the bug format.

## Appendix A. Shape word lists (fixed before looking at views)

A title needs an animal or pet word (bear, grizzly, polar, lion, tiger, shark, crocodile, alligator, snake, python, anaconda, cobra, wolf, hippo, elephant, rhino, moose, buffalo, bison, gorilla, leopard, cheetah, jaguar, cougar, mountain lion, komodo, orca, whale, octopus, boar, cassowary, hyena, panther, ostrich, jellyfish, coyote, elk, badger, wolverine, eagle, "animals", "predator"; dog, cat, puppy, kitten, pet, and common breeds). Order of matching: S3, S7, S2, S1, S6, S5, S4, S8, S9. S4 and S5 need a pet word.

- **S3:** "what to do if/when", "how to survive", "how to escape/fight/stop/deal with/defend", "survive a ... attack", "[animal] attacks ... do/survive/escape", "survival guide".
- **S7:** "never run/pet/touch/feed/approach/ignore/play/leave/let/punish/wake/stare/look/hug/swim/try/turn/corner/scare/climb/hike/camp/get/go/walk", "don't run/pet/touch/feed/approach/ignore/punish/stare/wake/play dead/turn/look", "should never", "never, ever".
- **S2:** "vs", "versus", "who would/will/wins/can", "who is stronger", "fight(s)", "battle".
- **S1:** "would/could/can/do/will you (actually) survive/outrun/outswim/beat/fight/win", "survive a/an/the/one/N/[time] ...", "night with", "night in/at/alone", "trapped/locked with/in", "survive ... ?".
- **S6:** "it sucks/sucked/would suck/is hard to be", "a day as", "a day in the life of", "life as a", "your life as", "if you were a", "you are/become a", "being a", "what if you were/became a", "I became/lived as a", "as a [animal]".
- **S5:** "why does/do/is/are my/your [pet]", "if your [pet]", "your [pet] is/does/wants/keeps/knows/...", "what/when your [pet]", "[pets] do this", "secretly telling", "telling you", "trying to tell/say you", "my [pet] keeps/does/is/...".
- **S4:** a title that starts with a number, or contains a number with weird/strange/odd/surprising/signs/things/facts/reasons/habits/behaviors/secrets/mistakes/quirks, or "behaviors/habits/quirks explained", or "explained".
- **S8 (extra):** "what if / what would happen if / what happens if you/a/an/the". **S9 (extra):** "most dangerous/deadly/powerful/terrifying/scary", "deadliest", "ranked", "top N", "N animals/predators", "every animal/predator/shark/bear/snake/dog/cat".
- Subject (big animals or pets) in the tables is a second title-word check (big-animal words only, or dog/cat/puppy/kitten words only; titles with both are left out of the subject splits). Gaming filter on S2 (post hoc): roblox, minecraft, arbs, animal revolt, gaming, gameplay, game, race, racing, tournament, simulator, spore, alien, gta.
- Long video = 2 minutes or more in the `/videos` tab. Own median = median views over those videos of that channel. Winner = 5x own median or more.

## Appendix B. Sources

- Pull A: 752 channel `/videos` tab flat listings (`yt-dlp --flat-playlist -J --playlist-end 60`), 2026-11-12.
- Pull B: 100 `ytsearch40:` flat lists, 2026-11-12.
- Autocomplete: `suggestqueries.google.com/complete/search?client=youtube`, 2026-11-12.
- Trends: pytrends, US, 5 years, web and `gprop=youtube`, 2026-11-12.
- Own history: MASTER_ORDERS "Scoreboard 11/10", "Watch hours", "Direction change". Method and channels: research 70, 75, 83.
- Scripts and raw pulls (not in the repo): `/tmp/claude-0/-home-user-skills/3d99d9ba-2ee2-5f03-bfdc-24a033361343/scratchpad/r85/`.
