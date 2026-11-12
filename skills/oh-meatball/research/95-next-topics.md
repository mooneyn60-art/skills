# 95. Next 12 topics, checked by a second model (2026-11-12)

**Answer, in order (6 pets, 6 survival). Every fact below was opened at its primary source today.**
1. cat-lilies: lilies are toxic to cats, even the pollen and vase water (FDA).
2. dog-chocolate: mild signs from 9 mg theobromine per pound, severe near 18 (FDA).
3. bison-yellowstone: stay 25 yards away; bison run 3x faster than you (NPS).
4. dog-years: in 104 Labradors a 1-year-old dog is about 31 in human years (Cell Systems 2020).
5. cat-falls: 96.5% of 119 fallen cats survived, 46.2% broke limbs (J Feline Med Surg 2004).
6. cat-slow-blink: cats were more likely to come over after a slow blink, in one study (Sci Rep 2020).
7. mountain-lion: do not run, make yourself big; fewer than a dozen deaths in 100+ years (Colorado Parks and Wildlife).
8. croc-bite: one saltwater croc bit at 3,689 lbs, the highest bite force measured in any animal (PLoS ONE 2012).
9. dog-head-tilt: in 40 dogs only those that knew toy names tilted often (Anim Cogn 2022).
10. black-bear: black bear attack, fight back; grizzly, play dead (NPS).
11. wolf-distance: Yellowstone says 100 yards from wolves, 4x the bison rule (NPS).
12. hippo-airborne: running hippos briefly lift all four feet off the ground; 169 strides from 32 hippos (PeerJ 2024).

Rows for the build: `research/data/95-topic-queue.csv` (status=open). Seasonal note: lilies and chocolate fit the holidays; post them first.

## Asked by Nolan 11/12
"Not working is there anything you can build or make to help us out or any updates to repos or skills or anything else grow yourself." This file is the topic step: two researchers listed 24 candidates, and this second check keeps the 12 whose facts hold.

## Method
- Opened every top-12 source myself on 11/12. PubMed abstracts came word for word through NCBI's E-utilities (the PubMed web page needs cookies). The dog-years formula and hippo text came from the PMC full text. FDA, ASPCA, NPS, CPW, FWS and PLoS pages came through a fetch tool that returns quotes; I asked for verbatim sentences.
- Re-pulled YouTube and Google suggestions for 14 seeds with `postkit.py kw` (11/12). Ranks only, no volumes.
- Re-ran 7 `ytsearch15` flat listings and 1 channel Shorts pull (10 yt-dlp calls in all, 1.5 s apart). No YouTube watch pages, no vidIQ.
- Checked `data/posted.csv` and the TikTok queue list for repeats.
- Ranked by: fact confirmed with a number, real top suggestion, small-channel outlier (views divided by that channel's own Shorts median), room for a drawn gag, low risk.

## Table
| # | Topic | Searched phrase (rank, 11/12) | Confirmed fact (source) | Outlier evidence | Risk |
|---|---|---|---|---|---|
| 1 | Lilies and cats | "are lilies poisonous to cats" YT 1; Google "are lilies toxic to cats" 1 | Whole plant toxic incl. pollen and vase water; fatal kidney failure in under 3 days; delay of 18 h or more makes it hard to reverse (FDA lily page) | Cummings vet school Short 1,415 views, ratio 10.4 on 16 Shorts (researcher; views re-seen 11/12) | Safety topic; say true lilies and daylilies, not peace or calla lily |
| 2 | Chocolate and dogs | "can dogs eat chocolate" YT 1, Google 1 | 9 mg/lb mild, about 18 mg/lb severe; dark 227 mg/oz vs milk 57 mg/oz (FDA) | AumSum 754,914, ratio 8.1, 4.8M subs (big) | Owned by big channels; never give a "safe" amount |
| 3 | Bison | Google "what to do if a bison charges you" 1; YT "...attacks you" 1 | 25 yards; "3x faster than humans"; injured more people in Yellowstone than any other animal (NPS) | News clips only (CBS LA 409,032); no small ratio | Yellowstone-only claims; no mph |
| 4 | Dog years | "how old is my dog in human years" YT 1, Google 1 | 104 Labradors; human age = 16 ln(dog age) + 31, so 1 yr is about 31 (Cell Systems 2020, full text) | 1 Short (app advert, 730); big channels win | Labradors only |
| 5 | Cat falls | "do cats always land on their feet" YT 6 | 119 cats: 96.5% survived, 46.2% broke limbs; 7th floor up worse (Vnuk 2004). 132 cats: 90% of treated cats survived (Whitney 1987) | donjgm Short 22,335 (29 s), median not measurable | Only cats that reached a vet; never "falls are fine" |
| 6 | Slow blink | "why do cats slow blink" YT 1 (own seed), Google 1-10 | Cats more likely to approach after a slow blink than a neutral face (Sci Rep 2020) | Rebecca's Cats 161,134, ratio about 199 on 4 Shorts (thin); Bobbie & Fos 631,705, ratio 55 | No number; not "proof of love" |
| 7 | Mountain lion | YT 1, Google 1 "what to do if a mountain lion approaches you" | Avoid running, look larger, fight back; fewer than a dozen deaths in North America in 100+ years (CPW) | 0 Shorts of 15 (re-run 11/12) | No Short proof |
| 8 | Croc bite | "crocodile bite force" YT 1 (own seed) | 16,414 N (3,689 lbs), one saltwater croc, highest measured in any animal; hyena 4,500 N (PLoS ONE 2012) | 1 Short, Australian Reptile Park 4.93M (big) | One animal, not every croc |
| 9 | Head tilt | "why do dogs tilt their head" YT 1 | 40 dogs; only dogs that knew toy names tilted often; side stable for months (Anim Cogn 2022) | Best Short 787, ratio 1.3 | Link, not proof of understanding |
| 10 | Black bear | "what to do if a black bear attacks you" YT 3, Google 2 | Black bear: do not play dead, escape or fight back at face. Grizzly: play dead (NPS) | 0 Shorts; WGN News Short 362,874 | Overlaps our grizzly Shorts; name the species every time |
| 11 | Wolf | "what to do if you see a wolf" YT 1, Google 1 | 100 yards from wolves and cougars vs 25 for bison (NPS Yellowstone) | Cascade Hiker 97,869, ratio 559 on 3 Shorts (weak) | Google rank 4 is "wolf spider"; only one source |
| 12 | Hippo | "can you outrun a hippo" Google 4 | Hippos only trot but at top speed have brief aerial phases; 169 strides, 32 hippos (PeerJ 2024) | Africa Freak 412,550, no ratio | No top speed in the paper; the fact does not answer "can you outrun" |

## Researcher numbers that did not hold, or changed
- Lilies: the researcher found no amount. The FDA lily page gives it: pollen and vase water count, failure in under 3 days, 18 h treatment window. Added.
- Dog years: the formula 16 ln(age) + 31 is now confirmed in the full text (the researcher had not opened it).
- Cat falls: Whitney's 90% is of treated cats (67% of the 132), not all cats.
- Cat falls outlier: the plain search now shows donjgm "Cats don't always land on their feet" at 22,335 views, which the researcher did not list. Its channel median could not be pulled.
- "can dogs eat turkey bones" is YouTube rank 2 today, not 3. "can you outrun a polar bear" is also YouTube rank 9 today.
- Hippo: the 0.3 s and 15.5 mph figures are not in the abstract or the PMC full text I searched. Dropped those numbers.
- Everything else re-pulled (slow blink, lilies, do cats, chocolate, dog age, head tilt, bison, black bear, mountain lion, wolf, crocodile, can you outrun a) held.

## Dropped
- Do cats love their owners: the abstract has no percentages; the 64% figures are from news only. Not confirmed.
- Why do dogs eat grass: primary paper not found. Not confirmed.
- How cold is too cold for dogs: no number from a primary page.
- Do dogs understand words: no dog count in the abstract; overlaps the made "cats know their names".
- Poinsettia: confirmed (ASPCA "generally over-rated in toxicity") but no number and no Short outlier. Reserve for December.
- Turkey bones: confirmed (ASPCA "poultry bones can be a major choking hazard") but no number and 0 Shorts. Reserve only if a Thanksgiving post is wanted by 11/24.
- Can you outrun an alligator: no speed at any agency page. Not confirmed.
- Polar bear: FWS "Do not run from or approach polar bears" confirmed, but polar bear fur is already queued on TikTok and "you can't outrun a grizzly" is made. Too close to a repeat.
- Wild turkey attack, elephant, kangaroo, gorilla: primary source not opened or not found.

## Could not measure
- Search volume: suggestion rank only.
- TikTok wording and TikTok suggested searches for any topic.
- Seasonal rise: no Trends data; the holiday angle for lilies and chocolate is reasoned.
- Channel medians: I re-pulled none successfully (the donjgm Shorts tab returned nothing). Ratios quoted are the researchers' 11/12 pulls; several rest on 3 to 16 Shorts.
- Most outliers are real-footage clips. No drawn small channel has a proven outlier on any of these 12.
- FDA, NPS, CPW, ASPCA and PLoS quotes came through a fetch tool; PubMed and PMC text came word for word.
- Whether any of these beats our own pet baseline: not measurable until they post.

## Added by the main session: search demand from Google Trends (new tool, 11/12)
Nolan 11/12, about 16:00 ET: "you have full control download whatever you neex". `pytrends` was installed and wrapped as `postkit.py trends`. Rows: `data/95-trends.csv` (262 rows). YouTube search, US, 3 months to 2026-11-12. A value is relative to the top search for the same seed (100), not a count, and seeds cannot be compared with each other.
- "why do cats": purr 100, hate water 64, bite 61, like catnip 54, meow 51, knead 44 (and "do biscuits" 40), hiss 33, chatter at birds 32. Rising: chatter at birds, land on their feet, have 9 lives, knock things over, trill.
- "why does my cat": bite me 100, keep throwing up 54, sleep on me 48, follow me to the bathroom 36, watch me sleep 33, hate me 27, knead me 25.
- "why do dogs": lick you 100, hump 42, howl 42, bark 34, pant 34, sleep with you 25, wag their tails 23, get zoomies 21. Rising: pant, sleep with you, zoomies, tilt their heads.
- "why does my dog": lick me 100, eat poop 95, stare at me 74, chatter his teeth 46, lick his paws 38.
- "can dogs eat": what can dogs eat 100, bananas 26, cheese 20, eggs 17, strawberries 17, chocolate 17, apples 16.
- "can you outrun", "what to do if a [animal]", "would you survive [animal]": nothing shown. Survival phrases have no measurable YouTube search volume, so those Shorts live on the feed (93.7% of our Shorts views come from the feed anyway, research 94).
- Seasons (Google web search, US, 5 years, mean by month): "can dogs eat turkey" 13 in November against 2 in every other month; "dog chocolate" 34 in December and 32 in April against 17 to 26; "polar bear" 73 in December and 71 in January against 43 in summer; "poinsettia cats" shows only in November and December; "are lilies toxic to cats" is flat.
- What this changes: the checked list above was ranked without volumes. Two of the biggest searches were not on it (purr, the dog stare), and two it ranked low are rising (land on their feet, head tilt). The turkey topic, dropped for having no number, has the clearest season of all.

## The first batch (started 11/12 about 16:15 ET) and why
The YouTube Shorts queue is empty from Sat 11/21 (`data/posted.csv`), so the next Shorts are due then. Four topics went into the saved `shorts-batch` workflow (fact pack, script pair, second-model check, render with voice check, lint):
1. cat-purr (#68): the top cat search. Facts to confirm at the source: Herbst 2023 and McComb 2009, both Current Biology.
2. dog-stare (#69): the third biggest "why does my dog" search. Fact to confirm: Nagasawa 2015, Science.
3. dog-turkey (#70): the November spike; ASPCA and FDA pages, already opened by the checker. Post before Thanksgiving (11/26).
4. bison-wms (Would Meatball Survive? #5): the top survival topic on the checked list; two NPS numbers.
Next, in this order unless the first reads change it: cat-falls, dog-head-tilt, croc-bite, mountain-lion, catnip (not yet checked), dog-chocolate (for December), cat-lilies.
TikTok cuts of the same four are built too but not scheduled before the Fri 11/20 verdict on the search-led test.

## TikTok watch time: what works for a Personal account (asked because the Windsor link failed for Nolan on 11/12)
- Windsor's own guide asks for "A TikTok Business or Creator account you manage" (https://windsor.ai/how-to-connect-tiktok-organic-to-claude/). Its field list has an `is_business_account` field. Not confirmed as the cause of the failure, but the likely one.
- Metricool lists the metrics (full video watched rate, average time watched, For You, Search) and returned null for all of them on 21 posts from 11/05 to 11/12. Its help page says: "The metrics available for personal TikTok accounts are limited compared to business accounts." (https://help.metricool.com/en/article/tiktok-metrics-1hnbc9r)
- Other connector vendors (Adriel, 2MinuteReports, Fivetran, Adverity) say the same API serves Business and Creator accounts only. TikTok's own reference page did not load, so the rule is quoted from vendors.
- Supermetrics says a Personal account with 100 or more followers works and gives average watch time per video (https://docs.supermetrics.com/docs/tiktok-organic-connection-guide.md). Price not found; not tried, because spending is Nolan's call.
- So: the only free route is the app. Profile, TikTok Studio, Analytics, Content, tap a video: average watch time, watched full video, where views came from (taps per Buffer and TikTok's newsroom tutorial, not confirmed on a Personal account). One screenshot per test video. This is now open ask 1 in MASTER_ORDERS. The account stays Personal.

## Could not measure (added)
- Real search counts: Trends gives relative values only, and long phrases often read 0.
- Whether a Personal account sees the analytics screen described above.
- Whether the four topics beat the bug baseline: not until they post.
