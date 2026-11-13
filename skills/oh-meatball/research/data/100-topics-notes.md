# 100 topics: next long-video topics and outside benchmarks (2026-11-13)

Label: topics. Read-only. Nothing posted, scheduled or changed. No vidIQ, no Metricool, no watch pages (yt-dlp flat listings only), no video downloads. Rows: `100-longform-topic-candidates.csv` (20 rows).

## Answer first (five lines)
1. Make these five next, after the polar bear and the house cat: lion, house dog, wolf, crocodile (all "Why It Sucks to Be Born as a [animal]"), then "Why Does My Dog Lick Me" as the explainer. Order is demand times winnability (section 3). It is a sort of small samples, not a test.
2. The channels with the best medians do one thing: Zoozle (35.5K subs, median 73,500 views) and Dodo Diaries (25.4K, 56,500) made 20 of their last 20 long videos in the "Why It Sucks To Be Born As" shape, each 9 to 13 minutes. Our last 11 long videos: median 43 views, 2.2 to 11.3 minutes, five different shapes (research 100, `100-longform-table.csv`, public counts 11/13).
3. The animal is not the lever. Those two channels run the shape on ladybugs, goldfish, mantises, megalodon and clone troopers, and the same title gets 300K or 60K. Search demand for the animal does not drive it: the phrase "why it sucks to be born as a [animal]" returns no YouTube suggestions at all (checked 11/13, `postkit.py kw`). So demand here means "the animal is searched" and nothing more.
4. No top-five pick is seasonal. Elephant (December) and penguin (September to January) look seasonal but the word probably means something else (white elephant gifts, hockey); unverified, so neither is ranked high. The polar bear (December) is already built.
5. Weak spots: the sample is tiny (2 to 10 small channels per animal), search lists lean to winners, and I could not measure upload pace, retention or click-through for anyone.

## 1. How the candidates were measured
- **Candidates:** 13 in the "born as" shape (animals not yet built: lion, dog, wolf, crocodile, octopus, elephant, hippo, hamster, goldfish, rabbit, grizzly, penguin, moose) and 7 pet or survival explainers (dog licks, cat bites, cat sleeps on me, dog eats grass, can dogs eat chocolate, dog years, bison charge). Grizzly and moose are in the CSV although both already have Shorts.
- **Searched phrase.** `postkit.py kw` (YouTube suggestions, 11/13): "why it sucks to be a [animal]" and "why it sucks to be born as a" return nothing; "your life as a" returns only role-play and game phrases; "life as a wolf" and "life as a hippo" return a few. So for the born-as shape there is no typed phrase. Explainer phrases are the ones in research 95 (suggestion ranks 11/12).
- **Demand.** Google Trends through `postkit.py trends compare --yt --months 12` (YouTube search, US, relative values). Values are relative inside one call. To put the animals on one scale I put "lion" in every call and rescaled to lion = 58 (the "lion" value in calls 1 to 3). The last call had lion at 15.9, so its terms (dog, cat) are multiplied by 58 / 15.9. This chain assumes the lion term is stable between calls; I did not test that. One-word terms mix meanings (lion, wolf, bat, horse, "pet hamster" read 0). Explainer phrases are long, so they read about 0 when put next to "dog years" (48); I used each phrase's rank inside its own seed from research 95 instead, and these cannot be compared across seeds.
- **Seasons.** `postkit.py trends season --web --years 5` (Google web search, US, mean by month), five terms per call.
- **Competition.** `ytsearch20:` flat lists, 20 searches (13 "why it sucks to be born as a [animal]", 7 explainer phrases; one retried because the first came back without channel names). Then each result channel's last 20 long uploads (`/videos`, flat) to get subscribers and the channel's own median views. Where research 85's file already had the channel, I used that median. I pulled channels only for the top 3 new channels per query (65 pulls), so many results have unknown subscribers (column `subs_unknown`). "Small" means under 50,000 subscribers. "Winnable" counts small-channel results over 10,000 views.
- **Score.** Winnability = (small results over 10,000 + 0.5) / (small results + 2). Score = log10(1 + demand index) x winnability. Compared: 13 animals in one sort. No permutation test: the samples are 2 to 10 channels, too small for one, so ranks one or two places apart mean nothing.
- **Requests.** About 125 in all (23 YouTube searches, 77 channel pages, 12 Trends calls, 3 suggestion calls, 6 thumbnail images, 4 more). That is a little over the 120 cap; the extra were six channel pulls to fill the cat-bite explainer and one retry. No block or 429 appeared from YouTube. No Trends call failed.

## 2. Candidates, ranked (demand x winnability)
Source: `ytsearch20` flat lists and channel `/videos` last 20, pulled 11/13; Trends 11/13. "Over 10K" counts on-topic long results (3 minutes or more) from channels under 50,000 subscribers.

| Rank | Topic | Demand (lion = 58) | Season | On-topic long results | Small channels / of those over 10K | Median and best small view count | Score |
|---|---|---|---|---|---|---|---|
| 1 | Lion | 58 | flat (Dec 36 vs 30) | 15 | 7 / 4 | 22,729 / 686,684 | 0.89 |
| 2 | House dog | 264 (the word "dog") | flat | 10 | 6 / 2 | 4,529 / 75,051 | 0.76 |
| 3 | Wolf | 64 | flat | 16 | 10 / 4 | 3,992 / 616,349 (a wolfdog) | 0.68 |
| 4 | Crocodile | 12 | flat | 18 | 4 / 3 | 19,881 / 40,314 | 0.65 |
| 5 | Why does my dog lick me (explainer) | "lick me" top of its seed | flat | 14 | 4 / 3 | 181,528 / 1,350,141 | n/a |
| 6 | Octopus | 9 | flat | 18 | 4 / 2 | 10,694 / 36,645 | 0.42 |
| 7 | Elephant | 22 | December 70 vs 38 to 48, likely "white elephant" | 18 | 8 / 2 | 1,577 / 20,822 | 0.34 |
| 8 | Why does my cat sleep on me | 48 in its seed | flat | 15 | 2 / 1 | 272,496 / 541,457 | n/a |
| 9 | Why does my cat bite me | top of its seed | flat | 16 | 6 / 2 | 3,657 / 66,361 | n/a |
| 10 | Can dogs eat chocolate | 17 in its seed | Dec 3 vs 2 (tiny) | 11 | 0 / 0 (4 channels over 1M) | none | n/a |
| 11 | Bison charge (survival explainer) | no volume shown | May to Sep 20 to 22 vs 16 to 17 | 4 | 0 / 0 | none | n/a |
| 12 | Hippo | 4 | flat | 15 | 2 / 1 | 31,871 / 58,119 | 0.27 |
| 13 | Pet hamster | 10 | "pet hamster" reads 0 | 12 | 4 / 1 | 963 / 115,707 | 0.26 |
| 14 | Dog eats grass | below 1 in its seed | flat | 12 | 3 / 0 | 2,051 / 3,063 | n/a |
| 15 | Dog years | 48 (alone on its scale) | flat | 11 | 3 / 0 | 250 / 639 | n/a |
| 16 | Goldfish | 4 | flat | 11 | 4 / 1 | 120 / 287,554 (Zoozle) | 0.18 |
| 17 | Pet rabbit | 27 | flat | 10 | 2 / 0 | 1,033 / 1,896 | 0.18 |
| 18 | Grizzly bear | 2 | flat (May to Jul 47 to 50 vs 36 to 37) | 19 | 7 / 2 | 1,143 / 81,867 (a polar bear) | 0.13 |
| 19 | Penguin | 15 | Sep to Jan 28 to 30 vs 19 to 20, maybe hockey | 19 | 4 / 0 | 51 / 9,535 | 0.10 |
| 20 | Moose | 11 | flat | 11 | 4 / 0 | 109 / 2,706 | 0.09 |

Notes on the table:
- The explainer rows have no common demand scale, so they carry no score; the order of rows 5 and 8 to 15 is by small-channel winnability and my judgment, not a formula.
- The dog row uses the plain word "dog" (264), which is the biggest term by far and also the vaguest. The pet half of our direction has the biggest audience; the demand number says that and nothing about the shape.
- Lion has the most small-channel evidence: Mr scribbles (26.4K subs) 686,684 views and JustJNR (5.6K subs) 139,648. It is also taken: 7 small channels already have the shape on lion, and 16 of 20 results are on-shape. Same for wolf (16 of 20) and crocodile (18 of 20).
- Moose and penguin look worst: small channels' median is 109 and 51 views. Grizzly also looks weak (median 1,143) while our grizzly Shorts exist.
- "Dog licks" is a real-footage shape: Jack Cole (41.9K subs) 1,350,141 views and Animalcabinet (631 subs) 309,264. Research 85 found no drawn small channel winning with this shape (S4, S5). Treat it as a test of our character in that shape, not a copy.
- Alex Planet (17 subs) has "Why It Sucks To Be Born As Salt Water Crocodile" at 21,822 views and Animation Nerd (259 subs) has a goldfish video at 161 views: the small-channel results run from 100 to 800,000 for the same title.
- Seasonal ones: none among the top five. Chocolate (December) and turkey (November, research 95: "can dogs eat turkey" 13 in November vs 2) are holiday explainers; turkey is already a Short. No long video fits the 11/28 or 12/5 slots on season except the polar bear.

## 3. Top five after the polar bear and the house cat
1. **Lion, "Why It Sucks to Be Born as a Lion".** 4 of 7 small-channel results are over 10,000; best 686,684 (Mr scribbles) and 139,648 (JustJNR, 5.6K subs). Flat season. Crowded, so the packaging has to be ours.
2. **House dog, "Why It Sucks to Be Born as a Dog" (pet half; Noodle).** Biggest demand word in the file; the shape on a dog has 75,051 (Sketching the Wild) and 41,389 (Zoozle). 2 of 6 small results over 10,000. Wait for the cat result first (research 85 said so).
3. **Wolf.** 4 of 10 small results over 10,000: Dodo Diaries wolf 67,752. The 616,349 is a wolfdog, so I do not count it for the wolf. Survival half of the direction.
4. **Crocodile.** 3 of 4 small results over 10,000: Dodo Diaries alligator 40,314, Alex Planet (17 subs) 21,822. Median of the 3 is 0.71 times those channels' own medians, so they are normal, not outliers.
5. **"Why Does My Dog Lick Me", the explainer.** Top suggestion in "why does my dog" (research 95) and 3 of 4 small results over 10,000 (Animalcabinet, 631 subs, 309,264). Real-footage winners only, so this is the one test of a drawn character in that shape. Tie it to the dog-stare Short.

Not picked on purpose: octopus (4 small results, 2 over 10K, but neither pet nor danger), elephant and penguin (the season looks like another word), hippo (small demand, one winning channel), moose and grizzly (weak small-channel numbers).

## 4. Benchmarks: eight small channels that make drawn animal long videos
Source: each channel's last 20 long uploads (`/videos`, flat, 2 minutes or more), pulled 11/13 (MuGen 10 and JustJNR 5, because that is all they returned). Views are lifetime counts, rounded to two digits above 1,000, so older videos had longer. "Drawn" confirmed by eye on the thumbnails of Zoozle, Dodo Diaries, PaleoBloke, Sketching the Wild, Mr scribbles and The Animal Person (a drawing in each). Others judged from titles only. Median of the channel's own long uploads, so "x median" for a video is its views over that number.

| Channel | Subs | Median views, last 20 | Median of newest 10 | Typical length (middle quarter to max) | "Born as" or "life as" titles | Two best titles (views) |
|---|---|---|---|---|---|---|
| Zoozle | 35.5K | 73,500 | 57,500 | 10.1 to 12.7 min | 20 of 20 | Ladybug 299K; Goldfish 287K |
| Dodo Diaries | 25.4K | 56,500 | 34,000 | 8.8 to 10.4 min | 20 of 20 | Megalodon 314K; Praying Mantis 188K |
| PaleoBloke | 23.0K | 29,000 | 24,500 | 9.7 to 13.3 min | 14 of 20 (their median 55,500 vs 522 for the other 6) | Rhinoceros 805K; Humpback Whale 488K |
| The Animal Person | 46.2K | 23,500 | 6,600 | 11.6 to 57.6 min | 9 of 20 (68,000 vs 7,900) | Your Life as Every Ant Colony Rank 981K; ... Bee Hive Rank 615K |
| Sketching the Wild | 38.3K | 18,500 | 18,500 | 8.6 to 19.8 min | 17 of 20 (21,000 vs 6,100) | Leopon 350K; White Tiger 312K |
| The Curious Kid | 20.5K | 5,450 | 3,100 | 8.1 to 19.6 min | 0 of 20 | What Hunted Humans Before We Became the Apex Predator 1.0M; Every Deadliest Mantis Explained in 8 Minutes 194K |
| Mr scribbles | 26.4K | 3,900 | 1,950 | 8.8 to 61.1 min | 13 of 19 (6,000 vs 2,300) | Lion 686K; Honeybee 483K |
| MuGen | 3.1K | 4,500 | 4,500 | 8.2 to 10.0 min | 10 of 10 | Clone Trooper 441K; Octopus 36K |

Upload pace: not measurable (flat lists have no dates). Compare: our last 11 long videos, median 43 views, 2.2 to 11.3 minutes (`100-longform-table.csv`, 11/13).

What the best medians do that we do not:
- **One shape, every time.** Zoozle and Dodo Diaries: 20 of 20. PaleoBloke's other shapes median 522. Our long videos are five different shapes in a month.
- **Length held at 9 to 13 minutes.** Their middle quarter starts at 8.8 to 10.1 minutes. Our median is 7.1.
- **Topic spread inside the shape.** Insects, fish, extinct animals, fictional ones; the big hits are not the dangerous mammals. A ladybug and a goldfish got 299K and 287K. The drawn kit can do that.
- **Title and thumbnail recipe is fixed** (research 85 addendum: plain background, one big crying or screaming animal, one cursed fact in hand lettering). Seen on 6 of 6 thumbnails I looked at.
- **Mr scribbles (3,900 median, 6,000 for born-as, 61 minutes max)** and **MuGen (441K on a clone trooper, 36K on octopus)** show the other side: one hit lifts the average but the median stays low. A 5,000-view median with a 500,000 outlier is the usual shape, not a rule.
- **The Curious Kid** is the one non-born-as winner: "Every Deadliest Mantis Explained in 8 Minutes" (194K) fits research 85's X2 shape (every [group] explained). Not tested on pets.

Selection bias: all eight were found because they ranked in a search for the shape, so their medians are the upper bound for a channel that picks the shape.

## 5. Could not measure
- **Upload pace** for any channel (no dates in flat listings). I have no way to say how often they post.
- **Retention, click-through, impressions, "most replayed"** for any video: needs watch pages or Studio.
- **Real search volume.** Trends gives relative values only; long phrases read 0 beside a big term; one-word animal terms mix meanings (lion, wolf, bat, horse); "pet hamster" reads 0. Seasonal peaks for elephant and penguin are probably other topics; unverified.
- **The demand chain.** I assumed "lion" gives the same value in each call. Calls 1 to 3 agreed (58.0); the last call is a different window and I rescaled it.
- **Subscribers for many results.** `subs_unknown` is 3 to 13 per query because I pulled only the top 3 new channels per query. Those are left out of every small-channel count, so the counts are lower bounds; they could also be the winners.
- **A permutation p or interval.** Samples are 2 to 10 small channels per animal; I ran one sort over 13 animals and none of the differences between neighbours is testable.
- **Whether a channel is "drawn".** Verified by eye on 6 of the 8; the other two (The Curious Kid, MuGen) are judged from titles and my reading of the search lists.
- **TikTok:** not touched; this file is YouTube long video only.
- **Our own result on the shape:** none yet. The house cat video posts 11/28 and the polar bear is not built.
- **A cause.** Everything here is a link between a shape and views, from channels that rank in search.
