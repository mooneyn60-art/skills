# 83 - Which topics reach the majority? (2026-11-12)

Read-only research. Nothing posted, nothing scheduled, no git, no vidIQ, no Metricool changes, no YouTube watch pages (yt-dlp flat listings and web search only, the method of research 70). Rows: `data/83-topic-outliers.csv` (320 rows, one per video checked).

Nolan's question: which topic families do the most people find interesting or funny, in a form a small animated, character-led, joke-heavy facts channel can break out with? I assumed no topic. The short answer is in section 0.

## 0. The answer in plain words

1. No family clearly beats the others. The data says "wider families have a higher ceiling" (more small-channel videos pass 10,000 views), not "bugs are holding us back".
2. Highest ceilings in this pull: space and "what if", big dangerous animals, the myths and misconceptions family (polluted, see 4), pets, food, history. Lowest: everyday objects, money and jobs, human body, house bugs (long-form).
3. Our own bug Shorts (about 1,550 median views at 48 h, research 80) sit above the typical small-channel Short in every family tested when typical means the median of the channels' own medians (106 to 1,400 views); in the 12-Short neutral samples only pets (2,100) and myths (3,300) are higher. So the bug Shorts are not weak. What a wider topic may buy is a bigger tail (a few Shorts over 10,000), not a higher floor.
4. The survey evidence says about 1 in 4 Americans fear insects and spiders. That means most people do not. It does not show that bugs limit an audience.
5. Confidence: low to medium. The sample is small and search ranking leans to winners (section 1).

## 1. Method, and how I avoided picking only winners

- **Searches:** 223 `ytsearchN` searches on 12 families (129 in a first pass, 94 in a second pass; 5 of the second pass came back empty once and were re-run). Each base query was run plain (25 to 50 results) and with " animated" added (15 to 30). A third variant with " shorts" added mostly returned long videos, only 70 of 2,340 first-pass rows were 60 s or shorter. Plus 15 searches for section 3 and 1,406 channel pulls (each channel's /videos and /shorts tab, last 50 to 60 uploads, `channel_follower_count`, `view_count`).
- **Three samples, because one is biased:**
  - **Search-first (long-form, winner-leaning).** The first 12 videos in a fixed pooled search order (rank 1 of every list, then rank 2, and so on) from channels under 100,000 subscribers, with at most 2 per channel, on-topic by a title word list fixed before looking at views, channel median at least 100 views and at least 8 uploads in the tab. YouTube ranks by relevance and popularity, so this sample over-represents hits. Treat the "median multiple" in it as an upper bound. Videos with a title that was clearly off-topic (a film trailer, kids read-alouds, a different meaning of the word) were dropped by hand, by title only, before the first 12 were taken (list in the scratch method, about 55 titles; d and f ended at 9 videos).
  - **Recent Shorts (neutral).** From the same small channels, skip each channel's 3 newest Shorts, then take the first 2 on-topic ones in tab order. Chosen by position, not views. 12 per family (10 for myths). The multiple is against that channel's own Shorts median, so it hovers near 1 by design; the useful number is raw views.
  - **Channel base rate (neutral).** For up to 40 small channels per family, every upload in the tab (up to 50): share at 10,000 views or more, at 100,000 or more, and at 5x the channel's own median. Channels were found through search, so they lean to channels with one search-visible video.
- **Format:** the search-first sample is all long-form (flat search returns almost no Shorts). Shorts come only from the neutral samples.
- **Rounding:** flat views above 1,000 are rounded to 2 digits, so 10,000 cut-offs are fuzzy by about 5 percent.
- **Style:** only 29 of 138 search-first videos came from channels whose description or title says animated, cartoon, stick, drawn or faceless (`animated_style_flag`). Most of the sample is stock footage, slides and talking channels, not our style.

## 2. Topic families: small-channel breakout rate

Search-first long-form videos, channels under 100K subscribers (n videos, median of views divided by that channel's own long-form median, share at 10,000 views or more, share at 100,000 or more). Source: `data/83-topic-outliers.csv`, sample `search_first`.

| Family | n | Median multiple | Over 10K | Over 100K | Two example titles (views, multiple) |
|---|---|---|---|---|---|
| a. Pets (cats, dogs) | 12 | 24.1 | 9 of 12 | 7 | "15 Weird Dog Behaviors Explained" (1.27M, 2,410x of a 527 median); "If Your Cat Walks On You At Night, They're Secretly Telling You THIS" (502K, 17x) |
| b. Cute or funny animals | 12 | 5.6 | 6 | 2 | "15 Raccoon Facts That Will Blow Your Mind" (810K, 289x); "Top 10 Facts About Penguins" (WWF UK, 66K, 31x) |
| c. Big dangerous animals, who would win | 12 | 14.8 | 8 | 6 | "Tiger vs Lion - Animated Fight" (671K, 610x); "How Inuit Survive Polar Bear Attacks" (847K, 217x) |
| d. Human body | 9 | 1.9 | 4 | 3 | "Every USELESS Human Organ Evolution Left Behind" (638K, 37.5x); "Why you don't actually exist inside your body" (654K, 2.3x) |
| e. Food and kitchen | 12 | 4.3 | 8 | 2 | "Kitchen Sinks Got WEIRD (And Here's Why)" (27K, 4.1x); "5 Shocking Food Facts" (52K, 6.1x) |
| f. Everyday objects, "why is X like that" | 9 | 0.9 | 1 | 0 | "50 Things You Own Have a Feature You Were NEVER Shown" (18K, 9.2x); "The Hidden Lock Inside a Zipper" (600, 4.3x) |
| g. Psychology and everyday behavior | 12 | 48.7 | 11 | 8 | "80 Interesting Psychology Facts About Human Behaviour" (1.8M, 927x); "7 Strange Habits of People With 140+ IQ" (137K, 966x) |
| h. History, odd or funny stories | 12 | 1.0 | 6 | 5 | "The Weirdest Deaths in History" (263K, 10.5x); "33 History Facts That Sound Too Weird to Be True" (66K, 6.9x) |
| i. Space and "what if" | 12 | 3.5 | 11 | 5 | "What Would Happen If an Asteroid Hit the Ocean?" (1.7M, 12x); "What Would Happen If You Woke Up 20,000 Years Ago?" (14K, 24x) |
| j. Money, jobs, how things work | 12 | 0.9 | 3 | 1 | "How the Internet Works in 5 Minutes" (4.9M, 2,230x); "How Bank Actually Works. (3d animation)" (984, 4.1x) |
| k. General myths and misconceptions | 12 | 5.6 | 9 | 4 | "Every COMMON MISCONCEPTION Debunked in 10 Minutes" (628K, 22x); "25 Things You Were Taught in School That Were Wrong" (35K, 34x) |
| l. House bugs (baseline, as in research 70) | 12 | 2.9 | 2 | 2 | "What Really Happens to a Spider After You Throw It Outside?" (2.3M, 171x); "Never Kill the House Centipede, Here's the Real Reason" (1.7K, 15x) |

Why the multiples look huge: a channel with a tiny median (527 views) and one hit scores in the thousands. Read the "over 10K" column and the neutral tables below, not the multiple. The sample leans to winners: the family with the most winners here (g) is mostly generic psychology listicles on 30K to 80K subscriber channels, not drawn or character-led channels.

### 2b. The neutral view (what a normal upload from a small channel gets)

Channel base rate: every upload (up to 50) of up to 40 small channels per family. "Channels" and "videos" are counts in that pull. Source: scratch pull, tab flat listings 2026-11-12.

| Family | Long: channels / videos | Long: share over 10K | Long: share over 100K | Long: median of channel medians | Shorts: channels / videos | Shorts: share over 10K | Shorts: median of channel medians |
|---|---|---|---|---|---|---|---|
| a. Pets | 30 / 1,091 | 22.6% | 6.1% | 1,050 | 15 / 504 | 35.7% | 1,400 |
| b. Cute or funny animals | 33 / 1,235 | 16.4% | 3.9% | 386 | 23 / 841 | 5.5% | 521 |
| c. Big dangerous animals | 31 / 1,055 | 28.7% | 6.1% | 1,000 | 19 / 650 | 13.2% | 1,200 |
| d. Human body | 14 / 292 | 12.0% | 4.1% | 27 | 25 / 854 | 9.3% | 106 |
| e. Food and kitchen | 30 / 1,111 | 24.1% | 2.8% | 358 | 24 / 926 | 3.3% | 513 |
| f. Everyday objects | 20 / 678 | 3.1% | 0.1% | 25 | 22 / 543 | 0.9% | 261 |
| g. Psychology | 28 / 977 | 16.2% | 4.2% | 721 | 13 / 360 | 1.1% | 106 |
| h. History | 21 / 649 | 19.6% | 8.8% | 135 | 17 / 533 | 2.3% | 321 |
| i. Space and what if | 22 / 615 | 35.3% | 14.6% | 608 | 18 / 486 | 5.6% | 1,125 |
| j. Money, jobs, how | 30 / 984 | 10.5% | 2.7% | 86 | 21 / 833 | 3.6% | 437 |
| k. Myths | 29 / 1,049 | 33.4% | 8.2% | 1,000 | 18 / 582 | 19.9% | 1,350 |
| l. House bugs | 28 / 897 | 12.5% | 4.5% | 437 | 7 / 283 | 3.5% | 1,000 |

Neutral Shorts sample (the 2 on-topic Shorts per channel, positions 4 onward, n = 12 per family; 10 for k): median views and count over 10,000.

| Family | Median views | Over 10K | Over 100K |
|---|---|---|---|
| a. Pets | 2,100 | 4 | 3 |
| b. Cute or funny | 1,200 | 0 | 0 |
| c. Big dangerous | 1,300 | 4 | 1 |
| d. Body | 971 | 1 | 0 |
| e. Food | 1,100 | 0 | 0 |
| f. Objects | 1,250 | 0 | 0 |
| g. Psychology | 526 | 0 | 0 |
| h. History | 317 | 0 | 0 |
| i. Space and what if | 935 | 2 | 0 |
| j. Money and jobs | 468 | 1 | 0 |
| k. Myths | 3,300 | 2 | 0 |
| l. House bugs | 1,100 | 1 | 0 |

How to read it:
- Our own drawn house-bug Shorts: about 1,550 median views at 48 h (n = 4, research 80), 1,100 to 1,900 each. That is above the median of channel medians in every family (106 to 1,400). In the 12-Short neutral samples it is above 10 of 12 medians; only pets (2,100) and myths (3,300) are higher.
- The families where more than 1 in 5 small-channel long videos passed 10,000 views: space and what if (35%), myths (33%, but see 4), big dangerous animals (29%), food (24%), pets (23%). House bugs are at 12.5%.
- For Shorts, only pets (36%), myths (20%) and big dangerous animals (13%) show a real share above 10,000. Bugs are 3.5% (7 channels only, so weak).
- Everyday objects, money and jobs, and the human body are the weakest families on every neutral measure.

## 3. How crowded each family is

For one typical query per family, how many of the first 20 flat-search results come from channels over 1 million subscribers. Rough: one query each, subscribers read from the channel tab, 1 to 2 channels had no public count and are not counted as big.

| Family | Query | Results from channels over 1M subs (of 20) |
|---|---|---|
| a. Pets | why does my cat | 12 |
| b. Cute or funny animals | cute animals weird facts | 14 |
| c. Big dangerous animals | would you survive animal attack | 14 |
| d. Human body | why your body does weird things | 3 |
| e. Food and kitchen | weird food facts | 8 |
| f. Everyday objects | why are everyday things shaped like that | 6 |
| g. Psychology | why do we do weird things psychology | 9 |
| h. History | weirdest true stories in history | 7 |
| i. Space and what if | what would happen if | 14 |
| j. Money, jobs, how | how money works explained | 14 |
| k. Myths | common myths people believe | 9 |
| l. House bugs | bugs in your house | 6 |

Crowded (14 of 20): cute animals, big dangerous animals, space and what if, money. Pets 12. Least crowded: body (3), objects (6), bugs (6), history (7). Crowding and ceiling go together: the families with the highest ceilings are also the most crowded, and the big names there (Kurzgesagt, TED-Ed, What If, BuzzFeed) are the audience's habit. Small channels still get through in them (section 2b).

## 4. Small channels like ours that grew (drawn or simple animation, a character or a narrator, jokes)

Style judged from channel descriptions and titles. I could not watch the videos (YouTube blocks watch pages from here), and a web search could not confirm the style of StickTory or Professor Stickman. Treat "funny" as unverified for all of them. Numbers: flat tab listings 2026-11-12, last 50 to 60 uploads, multiple = views over the channel's own median for that tab.

| Channel (subs) | Style (from description) | Top 5 videos by topic | Typical length | Title shape |
|---|---|---|---|---|
| StickTory (147K) | "An animation channel covering interesting historical topics" | All five are "Why it sucked to be a [medieval executioner, blacksmith, assassin, pharaoh, concubine]": 2.1M, 1.4M, 1.3M, 1.2M, 1.0M; 26x to 54x its 39K median; 15 of 55 videos at 5x or more | 10 to 14 min (median 12.5) | "Why It Sucked to Be a [job] in [era]" (a fixed template, the viewer is the subject) |
| Professor Stickman (29.8K) | Stick-figure style by name; "why your body does strange things" | Body oddities and evolution: rule-breaking people 781K, "useless human design" 535K, "weird habits reveal" 524K, DNA "errors" 391K, diseases you can smell 382K; 23x to 46x its 17K median; 11 of 50 at 5x or more | 16 to 58 min (median 16) | "Every [weird body thing] ..." and "What Your 'Weird' Habits Reveal" |
| Hour Seven (8.2K) | "Through animation and storytelling, we explore fascinating what if scenarios" | What if an immortal snail chased you (1.5M, 183x), what if it rained acid (362K), what if you were the snail (160K), house upgraded daily (152K), broke every law (134K); 5 of 16 at 5x or more | 4 to 14 min (median 9) | "What If You / The ___ Chased You and Never Stopped?" |
| Jeremy Bearimy (52.8K) | Animated what-if comedy (description is a joke about time) | What if you could see who has a crush on you (1.9M), only guy at a girls school (983K), infinite money (982K), creative mode in real life (828K); 12 of 50 at 5x | 10 to 11 min (median 10.7) | "What IF You ..." wish-fulfilment |
| The Last Day (36K) | Animated disaster explainers | Glacier disaster 5.2M, moon crashing into Earth 2.0M, asteroid in the ocean 1.7M, giant wave 1.5M, humans disappear 967K; 7x to 37x its 140K median | 12 to 19 min | "What Would Happen If [disaster]?" Not a joke channel |
| Animated Earth (35.8K) | "Animated videos about prehistoric life on Earth" | "The Insane Evolution of Spiders" 1.9M (91x), "...of Snakes" 816K, humans as prey 95K to 165K | 10 to 11 min | "The Insane Evolution of [animal]" Not a joke channel |
| Unhinged History (2.9K) | History "this weird", humorous framing in the description | "21 [historical people who never existed / criminals who were complete idiots / biggest idiots in US history]": 382K, 358K, 174K; 79x to 174x its 2.2K median; 16 of 50 at 5x | 18 to 23 min | "21 [Dumbest / Worst] ... in History" (a fixed number plus an insult) |
| PEANUT (156K, Shorts) | "Animated stories, facts, and things you didn't need to know" | Shorts: can you die from holding your breath 13M, how not to get caught committing a crime 10M, why your brain has random violent thoughts 3.6M, you'd join a cult and not notice 3.5M, urge to jump from a height 3.5M; median Short 562K | Shorts (length not in the flat listing) | "Why Your Brain / Body ..." second-person psychology and body |

What funny plus facts looks like when it works, from these 8 (inference from titles, not watched):
- The winners put the viewer inside the scenario ("you", "if you were", "why it sucked to be a ...") and use a repeatable template.
- Topics are people, bodies, survival, disasters and history, not a creature at home. The one bug-like winner (Animated Earth, spiders and snakes) is an evolution story, 1.9M and 816K.
- The very big Short channel (PEANUT, above my 100K cut but under 300K) is psychology and body, second person, a fear or taboo hook (violent thoughts, jumping, crime).
- Long-form hits run 10 to 14 minutes with a template. The two that look like our "narrator joke" style most (StickTory, Unhinged History) are history with a rude title word ("sucked", "idiots").
- Not found: a small channel whose recurring character does house or pet facts with jokes and a clear outlier. Meatball's lane is still untested, as research 70 said.

## 5. Is the premise right? Evidence on what broad audiences like and dislike

| Source (URL, date) | What it says | n |
|---|---|---|
| Chapman University, Survey of American Fears 2022 and 2023 compared, https://chapman.edu/Wilkinson/research-centers/babbie-center/_files/2023%20Fear/23chapman-survey-of-american-fears-2022_23-compared.pdf (file created July 2023) | "Insects/arachnids (spiders, bees, etc.)": 23.8% afraid or very afraid in 2022, 25.3% in 2023. "Reptiles (snakes, lizards)": 27.2%, 25.9%. "Animals (dogs, rats, etc.)": 6.5%, 6.0%. Heights 33.2% (2023). | Sample size not in the table; I did not find it |
| YouGov, Americans fear snakes, heights, spiders (poll), https://yougov.com/en-us/articles/42863-americans-fear-snakes-heights-spiders-poll (published 2022-06-17, fieldwork 2022-06-08 to 06-13) | Snakes "nearly one in three". Spiders among the most feared, no percentage on the page I read; women much more likely than men to fear spiders and insects. Secondary reports of the same poll (iHeart and others) quote spiders 24% and insects 15%; I did not verify those on YouGov's page. | 1,000 US adult citizens |
| Gallup, "Snakes Top List of Americans' Fears", https://news.gallup.com/poll/1891/Snakes-Top-List-Americans-Fears.aspx (2001) | 38% of women and 15% of men afraid of spiders and insects (as quoted by a search summary; old) | not read |
| YouGov, pets poll (via a search summary, https://yougov.com/en-us/articles/42665-pets-yougov-poll-may-6-10-2022, fieldwork 2022-05-06 to 05-10) | 69% of Americans have a pet: dogs 45%, cats 35%, fish 9%. 40% call themselves a dog person, 20% a cat person. | not read |
| TubeBuddy, 10 YouTube Shorts niches, https://www.tubebuddy.com/blog/10-youtube-shorts-niches/ (date not stated; its example is Nov 2022) | Shorts views by category over 90 days: entertainment first (over 17%), food and drink 2nd, video games 3rd, sports 4th, crafting 5th, family 6th, animals and pets 7th, science and tech 9th. Education not listed. Only entertainment has a percentage; method not explained. | "millions of videos", no count |

Not found: a primary YouTube Culture and Trends report or a TikTok category view ranking with a method. The category lists above are vendor blogs.

Our own evidence:
- House-bug Shorts hold 77% average viewed against 62% for other animals; 1.8 subscribers per 1,000 views against 0.7 for exotic (research 69 and MASTER_ORDERS 11/3). Would Meatball Survive gave 1.2.
- TikTok: 13 of 27 queued posts were non-house animals and the house median (261) against non-house (211.5) was inside the noise (MASTER_ORDERS 11/11).
- TikTok labels the drawn videos "Comics & Cartoon, Anime" (median 340, n = 20) and the old real-photo ones "Animals" or "Education" (median 615, n = 10) (research 82). That is about the look, not the topic.
- Quiz and TRUE or FALSE titles, and case files, flopped (KNOWLEDGE, research 64).

Verdict:
- "Bugs scare many people" is supported: about 1 in 4 Americans are afraid or very afraid of insects and spiders (Chapman 2023, 25.3%), and women far more so (YouGov 2022, Gallup 2001).
- "Bugs limit the audience" is not supported and cannot be settled here. Three in four are not afraid. Fear and disgust also drive watching (the best bug Short numbers above, and the 1.3M to 2.3M bug videos in research 70 and in section 2 are strong). Our bug Shorts beat the typical small-channel Short in almost every family. The only support for "limit" is the tail: in this pull, small-channel long videos in space, big animals, pets and food pass 10,000 views more often than bug ones (23% to 35% against 12.5%), and pets and big animals do so for Shorts (36% and 13% against 3.5%, bugs only 7 channels). That is a ceiling story, with a small sample.
- Our drawn house-bug Shorts already sit above the small-channel median, so a move would have to be judged by tail and by long-form hours, not by the Short median.

## 6. Ranking the families for us

Ranked on: small-channel ceiling (2b), crowding (3), fit with an animated character-led joke style (4), our own history (5). Confidence is high, medium or low.

1. **c. Big dangerous animals, "would you survive" or "who would win"** (medium). Ceiling: 29% of long and 13% of Shorts over 10K; 6 of 12 search-first videos over 100K. Fits the style: animated fight channels (Versus 79K, StickMania, BEAST WARS) and "survive" stick-figure videos exist at small size. It is already a show of ours (Would Meatball Survive?), brought viewers back best and gave 1.2 subscribers per 1,000 views. Against: crowded (14 of 20 from big channels), and our exotic-animal Shorts held 62% against 77% for house creatures. Level is medium because both the ceiling and our own retention point different ways.
2. **a. Pets people own** (medium to low). Best Shorts ceiling in the pull (36% over 10K, median Short 2,100, one example at 1.6M on a 4.5K channel) and the widest audience (69% own a pet). Against: crowded (12 of 20), the winners found are not character-led, and our brief says pets' bugs stay out. Low on style evidence, medium on audience.
3. **i. Space and "what if"** (medium to low). Highest long-form ceiling (35% over 10K, 15% over 100K), and the clearest drawn-style hits (Hour Seven, StickMania, Jeremy Bearimy, The Last Day). Against: the biggest crowd, research 70 found what-if long-form at median or below for big channels, and the what-if win was Shorts (BioChok 208x).
4. g. Psychology and body, second person ("why your brain ..."): high ceiling for one channel (PEANUT, 3.5M to 13M Shorts) but the small-channel base rate for psychology Shorts is 1.1% over 10K and 526 median views. Low.
5. k. Myths: high numbers but the pull is polluted by religion and fandom "myths"; our own quiz and myth titles flopped and the banned-word rule stands. Low.
6. e, h: food and history have middling ceilings and, for history, our case files flopped. Low.
7. l. House bugs: lowest long-form ceiling of the animal families, but our Short floor is already above the field. Keep as the base.
8. d, f, j: body, objects, money: weak on every neutral measure. Skip.

Video ideas for the top three (Shorts, titles only, 45 to 65 characters before any series tag; every number is a scenario or format number, no claim; every fact must be sourced and checked by a second model before a script).

c. Big dangerous animals
1. Would You Survive 60 Seconds Inside a Hippo's River?
2. Lion vs Tiger: Who Wins a 1 on 1 Fight in Your Backyard?
3. Could You Outrun a Grizzly Bear Over 100 Meters?
4. Would You Survive a Night Next to a Crocodile Swamp?
5. Polar Bear vs Orca: Who Wins a 1 on 1 Fight in the Water?
6. Gorilla vs 10 Grown Men: Who Actually Wins This Fight?

a. Pets
1. Why Your Cat Stares at You at 3 AM (Cat Owners Know)
2. 5 Things Your Cat Does That Actually Mean Something
3. Why Your Dog Circles Before Lying Down on Your Bed
4. 7 Weird Things Your Dog Does and What They Mean
5. Why Your Cat Brings You Dead Things as Little Gifts
6. What Your Cat Does During the 8 Hours You Are Out

i. Space and what if
1. What If the Moon Vanished for 24 Hours? Day by Day
2. What If Earth Stopped Spinning for 10 Seconds Today?
3. What If You Fell Into the Sun? The First 1 Second
4. What If You Could Jump on Mars With Just 1 Hop?
5. What If Every Planet Lined Up Over Your House Tonight?
6. What If the Sun Went Out for 1 Week? Hour by Hour

## 7. Could not be measured

- Retention or "most replayed" for any video (watch pages blocked, as in research 70).
- Subscribers gained per video for other channels; likes; comments.
- Whether the channels in the samples are animated, character-led or funny. Only 29 of 138 search-first videos carry an animated flag, and that flag is a word match on the channel description, not a look at the videos.
- Upload age: flat listings give no dates for Shorts and approximate ones for long videos. Long videos had more time to collect views than the recent Shorts.
- True search volume per family (no volume tool used, vidIQ not touched).
- Shorts search-first sample: the flat search returns almost no Shorts, so the neutral Shorts samples carry all the Shorts numbers (12 per family, small).
- A family's real size: the family word lists are loose (myths includes religion and fandom; psychology includes "high IQ habits" listicles). The numbers describe the sample, not the whole family.
- The Chapman sample size and an exact YouGov spider percentage (the YouGov page I read gave none).
- A primary YouTube or TikTok category ranking. TikTok For You versus Search per family.
- Whether our look (cartoon label on TikTok) or our voice matter more than the topic; this pull cannot separate them.

## 8. Options for the channel

**Option 1: stay on house bugs (current plan).**
- For: our Shorts floor is at or above every family tested (1,550 against 106 to 1,400 channel medians); house creatures hold 77% viewed; the "never kill X" long-form lane is proven (research 70); the queue is built.
- Against: bugs have the lowest long-form ceiling of the animal families in this pull (12.5% over 10K against 23% to 35%); search demand falls 40 to 60% in winter (research 75); Nolan asked to widen.

**Option 2: keep the "in your house" hook, move to non-bug subjects (pets, house animals, mice, attic animals, body in your home).**
- For: keeps the proven hook and the 45 to 65 character title shape; moves toward pets, the widest audience (69% own a pet) and best Shorts ceiling (36%); mice and attic animals are rising in winter search (research 75).
- Against: pets are crowded (12 of 20 from big channels); no character-led pet winner found; our 11/3 data had exotic animals at 62% viewed, though pets and house mammals were not tested.

**Option 3: move to the top-ranked family, big dangerous animals ("Would Meatball Survive?").**
- For: highest evidence-weighted ceiling and a fit with the character (the viewer is put in the scene, as StickTory, Hour Seven and Jeremy Bearimy do); an existing show with 1.2 subscribers per 1,000 views.
- Against: most crowded tier; retention of non-house animals was lower (62% against 77%); a single family is the "templated" risk if every video has the same shape (policy 1311392).

**Option 4: split YouTube and TikTok.**
- For: the two platforms want different things (YouTube Shorts and long-form for hours, TikTok for 61 s+ cuts of topics that passed 1,000 views); TikTok labels the drawn videos "cartoon" so a topic that suits cartoon viewers may do better there; bug long-form can feed watch hours while wider Shorts test the tail.
- Against: two topic plans double the work; the TikTok numbers (median about 220 to 340) are too small to read a topic effect; research 82 is still a lead, not proof.

**My pick: Option 2 first, with a controlled slice of Option 3, and the bug queue kept running at a lower share.** Confidence: low to medium (about 55%). Reasons: the data does not show bugs hold us back, so there is no case to drop a working floor; the data does show wider families have a higher ceiling, and the cheapest honest test is a measured slice. Concretely (a suggestion, nothing was built): for two weeks, about 1 in 3 YouTube Shorts on pets or "would you survive" with the same drawn look, voice, jokes and 45 to 65 character titles, judged against the bug Shorts median (about 1,550) and by the share over 5,000, not the median alone. Everything here is inference from a small, winner-leaning sample, which is why the test comes before any change to the queue.
