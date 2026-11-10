# 75 — Search demand and seasonality map (2026-11-10)

Built for: Meatball Myths (house bugs now, backyard creatures next). Read-only research; nothing posted.
Raw data: `research/data/75-autocomplete.csv` (6,122 suggestion rows), `75-seasonality-monthly-index.csv`, `75-supply-check.csv`.

## 0. How to read this (what the data is, and is not)

- **YouTube autocomplete** (pulled 11/10, `client=youtube`, US/English, 677 queries, 0.35 s apart) gives the exact wording people type and a **rank order, not a volume**. A rank-1 suggestion is a strong signal; it is not a search count. No volume numbers appear below because none were measured. (research/51 used vidIQ volume estimates for the long-form slate; this file does not duplicate that.)
- **Echoes:** when I sent "why are there german cockroach in my house", autocomplete often handed my own sentence back (117 rows, flagged `echo_of_input=1` in the CSV). Those are NOT evidence of demand, and I excluded them from every table. Rows are also flagged for game/media/non-English noise (650 rows): "silverfish" is mostly Minecraft, "stink bug" is Grounded/Rivals, "daddy long legs" is Poppy Playtime, "black widow" is Marvel, "yellowjackets" is the TV show, "hornets" is the NBA. Those queries are not our audience.
- **Google Trends (pytrends worked, no throttling):** US, last 5 years, weekly, both web and `gprop=youtube`. Each term is scaled to its own peak, so **an index (annual mean = 100) compares months of ONE term, never two terms to each other.** Monthly averages exclude November 2026 (partial). `gprop=youtube` is noisy for low-volume terms (lots of zero weeks and single-week spikes, e.g. "boxelder bug" shows 1,200 in Oct and 0 elsewhere); I used **web Trends as the primary seasonal read** and YouTube-Trends only where the curve is smooth (bed bugs, cockroach, dust mites, house centipede, fruit/drain flies, earwig, wolf spider all agree with web within a month). Ambiguous terms (moles, grubs, possums, raccoons, hornets, yellowjackets, black widow) are contaminated by other meanings and are marked.
- **Supply check:** `yt-dlp --flat-playlist` on 38 queries. It returns title, channel, views and duration only. **It does not return upload date or subscriber count**, so "small channel with lots of views" is judged from channel name + views and "old" is not measurable. Treat competition reads as a first pass; re-check top results by hand before committing a long-form.
- **posted.csv has 184 rows and includes scheduled dates through 11/28.** I treat anything in it, posted or scheduled, as covered.

## 1. The headline: search demand for house bugs falls off a cliff exactly when we are leaning into it

Most house-pest search interest peaks May-August and is **40-60% lower in December-February** than in a typical month (web Trends, index vs each term's annual mean):

| Term | Peak | Nov | Dec | Jan | Feb | Nov to Feb |
|---|---|---|---|---|---|---|
| house centipede | Jun | 74 | 43 | 39 | 41 | -45% |
| wolf spider | Aug | 63 | 43 | 37 | 39 | -38% |
| brown recluse | Jun | 66 | 44 | 36 | 41 | -38% |
| drain flies | Jul | 85 | 55 | 42 | 40 | -53% |
| fleas | Jul | 91 | 62 | 50 | 47 | -48% |
| camel cricket | Oct | 132 | 72 | 48 | 45 | -66% |
| cluster flies | Jul | 86 | 61 | 50 | 57 | -34% |
| cockroach | Jun | 83 | 69 | 72 | 72 | -13% |
| bed bugs | Jul | 79 | 68 | 67 | 73 | -8% |
| silverfish (web) | Jun | 73 | 72 | 69 | 75 | +3% |
| **dust mites** | Jun | 90 | 86 | 91 | 95 | **+6% (flattest curve: range 86-116 all year)** |

**What does not fall much:** dust mites (86-96), silverfish (69-75), cockroach (66-73) and bed bugs (65-73) stay at roughly 65-95% of their annual mean in winter, versus 25-45% for centipede, wolf spider and recluse, **mice** (peak Oct-Nov, 111/106 in Nov/Dec, and the 5-year trend is rising: the Nov-Dec index for "mouse in house" went from 29 in 2021 to 52 in 2025 on the 0-100 raw scale), **squirrels in attic** (peak Jan, 136), **stink bug** (secondary winter plateau 83-91 after the October spike), and a few **short bursts** that are timed to the calendar (Asian lady beetle, boxelder, camel cricket, Christmas-tree bugs; see section 3).
Implication: in Dec-Feb, search-led titles should lean on the flat/rising set (dust mites, bed bugs, cockroach, silverfish, mice, attic animals, pantry/carpet pests heading into spring), and the summer-peaking creatures (centipede, wolf spider, recluse) should be framed as evergreen Feed Shorts, not search plays, until March.

## 2. (a) Per-creature tables

Intent codes: **ID** identify it, **DANGER** is it dangerous / does it bite, **WHY** why is it in my house, **RID** get rid of it, **WEIRD** weird-fact / what-happens-if / versus. "Peak" is web Trends (US, 5 yr). Competition read comes from the supply check: **Crowded** = top results are multi-million-view or major-network videos; **Opening** = results are mixed, pest-control and local-news clips with modest views; **Gap** = best direct match is small (under about 20K) or the top results are tangential; **n/c** = not checked. Queries are in autocomplete wording, exactly.

### House centipede
Peak Jun (Nov 74, Feb 41, -45%). Autocomplete is the richest of any creature: bare seed returns "house centipede fast", "house centipede in house", "house centipede scary" at rank 1-2 on 13-17 different prefixes.
| Query | Intent | Competition |
|---|---|---|
| house centipede fast | WEIRD | n/c |
| house centipede in house | WHY | n/c |
| house centipede in bathroom | WHY | **Gap**: top result 16K views (Bug of the Week, 61 s); rest under 3.1K; several 5-10 min "Never kill the centipede in your bathroom" clones with 18-336 views |
| are house centipedes dangerous / house centipede dangerous to humans | DANGER | Crowded: Deep Look 3.5M, Stone 1.5M, Crawl Space Ninja 443K |
| do house centipedes bite / do house centipedes bite humans | DANGER | Crowded: Peekaboo Kidz 5.5M, Deep Look 3.5M; a 134 s explainer at 53K |
| why you should not kill house centipedes / what happens if you kill a house centipede | WEIRD | Crowded (1.85M Facts Verse, 2.6M Bright Side) **and a wave of identical clone titles ("Never Kill the House Centipede ...") at 300-3,000 views**. Our #21/#44 Shorts already cover this angle. Do not copy the clone template (sameness risk, KNOWLEDGE.md / policy 1311392). |
| house centipede vs roach / vs spider / vs praying mantis / vs wolf spider / vs brown recluse / vs black widow | WEIRD | vs roach: Opening (390K live-feeding video; the rest are the same big explainers). **vs spider: Gap** (top direct match 920 views, 1.5M is a generic "Spiders Vs Centipedes"). vs mantis/wolf/recluse/widow: n/c |
| what do house centipedes eat / house centipede infestation / house centipede trap | RID/ID | n/c |

### Silverfish
Peak Jun, flat in winter (Nov 73, Feb 75). Autocomplete is polluted by Minecraft ("silverfish xp farm", "mining minecraft"). Real queries only:
| Query | Intent | Competition |
|---|---|---|
| silverfish infestation | RID | n/c |
| silverfish bugs in house | ID/WHY | Opening: pest-control how-to videos 130K-431K; no entertainment/explainer channel in the top 6 |
| silverfish vs house centipede | WEIRD | **Gap** (no direct match; results are generic centipede videos) |
| silverfish trap / silverfish jar trap / silverfish real life / silverfish irl | RID/ID | n/c |

### Cockroach / German cockroach
Peak Jun, Nov 83 to Feb 72 (-13%, flat). Autocomplete mixes meme/pop-culture ("cockroach janata party", "cockroach dancing meme").
| Query | Intent | Competition |
|---|---|---|
| cockroach infestation / cockroach trap / cockroach repellent | RID | n/c |
| cockroach flying | WEIRD/ID | n/c |
| cockroach in ear | WEIRD/DANGER | n/c |
| cockroach lands on face / cockroach came out my | WEIRD | n/c |
| german cockroach vs american cockroach / german roaches vs american roaches | ID | n/c |
| what do german cockroaches look like | ID | n/c |

### Bed bugs
Peak Jul (Nov 79, Feb 73). Holiday travel hook: **no bump** in Trends ("bed bugs travel" is Jun-Jul and a small Oct bump 122; Nov 90, Dec 82, Jan 66). The hook is supported by extension guidance, not by search data (section 4).
| Query | Intent | Competition |
|---|---|---|
| bed bugs look like / what do bed bugs look like | ID | Opening: Shorts 4.7K-89K, doctor explainers 1.0M (Doctor O'Donovan) and 565K |
| bed bugs in hotel | WHY/DANGER | Crowded by news: Inside Edition 4.8M and 4.1M, Town & Country 2.8M. Hotel-check how-tos 15K-201K |
| bed bugs on mattress / bed bugs coming out at night / bed bugs dying from heat | ID/RID | n/c |
| bed bugs vs fleas / bed bugs vs mosquito bites / carpet beetle vs bed bug | ID | carpet beetle vs bed bug: **Gap** (top direct match 19K, next 11K) |
| bed bugs how to get rid of them | RID | n/c |

### Dust mites
The flattest seasonal curve of any creature (86-116 all year). Strongest evergreen.
| Query | Intent | Competition |
|---|---|---|
| dust mites in bed / dust mites in mattress / dust mites in carpet | WHY/ID | Opening for Shorts: medical/news clips 90K-260K, nothing character-led |
| dust mites on skin / dust mites on eyelashes / dust mites in hair | WEIRD/ID | Crowded for eyelash mites (CBS Miami 2.6M) but the **dust-mite-vs-eyelash-mite (Demodex) distinction is unclaimed**; our #3 Short covers face mites |
| dust mite infestation / dust mites how to get rid of them | RID | n/c |
| dust mites bites / dust mites bites pictures / dust mites rash | DANGER/ID | n/c (health-claims care: CDC/clinic sources only) |
| dust mites vs bed bugs | ID | n/c |

### Daddy long legs / cellar spider
Peak Jul (Nov 74, Feb 63); YouTube-Trends peak is spring (Mar-May). Autocomplete is half Poppy Playtime; real queries below.
| Query | Intent | Competition |
|---|---|---|
| daddy long legs vs black widow spider / daddy long legs kills black widow | WEIRD | Opening: DGK 737K, Specimen 174K, then 12K-30K |
| daddy long legs not a spider / daddy long legs facts | WEIRD | n/c |
| daddy long legs bite / daddy long legs and mommy long legs | DANGER/ID | n/c (our Mommy Longlegs Short is queued 11/9) |
| cellar spider vs brown recluse / cellar spider vs black widow / cellar spider vs house spider | ID | **Gap**: direct matches 4K-7K; big results are tangential (2.0M MyWildBackyard "EVERY Spider in Your House", 683K Travis McEnery) |

### Wolf spider / jumping spider
Peak Aug / May (Nov 63 / 73; Feb 39 / 56). Autocomplete is heavy on game ("Grounded") and pet-keeping.
| Query | Intent | Competition |
|---|---|---|
| wolf spider in house | WHY | Crowded: Travis McEnery 405K, MyWildBackyard, 165K pest how-to |
| wolf spider vs brown recluse / wolf spider vs black widow | ID/WEIRD | Opening: MyWildBackyard 111K; rest small |
| wolf spider babies on back scatter / wolf spider eyes at night | WEIRD | n/c |
| jumping spider intelligence / jumping spider looking at me / jumping spider recognizes owner | WEIRD | n/c (pet-keeper audience, not pest audience) |

### Brown recluse / black widow / false widow
Recluse peaks Jun (Nov 66, Feb 41). **"Black widow" web Trends is the Marvel film**; do not use its curve. False widow peaks Sep, UK-heavy ("false widow spider uk").
| Query | Intent | Competition |
|---|---|---|
| brown recluse bite stages / brown recluse bite symptoms / brown recluse bite timelapse | DANGER | Crowded and medical-adjacent: CTV News 1.0M, Brave Wilderness 3.8M, Chubbyemu 2.1M. CDC/university sourcing and "see a doctor" phrasing only (MASTER_ORDERS 11/3) |
| brown recluse look alike / brown recluse identification / brown recluse infested house | ID | n/c |
| can a brown recluse kill you / are brown recluse spiders deadly | DANGER | n/c |
| false widow vs black widow / false widow spider bite | ID/DANGER | n/c (our 11/12 Short covers false vs black) |

### Stink bug / Asian lady beetle / boxelder bug / cluster flies (the fall-invader set)
Web Trends: Asian lady beetle peaks **Nov** (Nov-1H index 382, then 142 in Nov-2H, 83 by Dec-1H); boxelder peaks **Oct** (221, then 123 in Nov-1H, 61 by Nov-2H); stink bug peaks Oct (146) and stays near 75-92 all winter; cluster flies peak Jul with an Oct YouTube bump.
| Query | Intent | Competition |
|---|---|---|
| why are stink bugs in my house | WHY | Opening below one giant: Nature at Your Door 2.6M, all others under 25K |
| stink bug in house / stink bugs how to get rid of / stink bug infestation / stink bug killer home remedy | WHY/RID | n/c |
| stink bug nymphs | ID | Gap: direct results 34 to 33K, one 217K terrarium video |
| stink bug bite on human | DANGER | n/c |
| asian lady beetle vs ladybug | ID | **Gap/Opening**: local news 184K, rest 4.6K-24K. (Already covered once: #44 "10,000s of Bugs in Your Walls", 11/10. The "vs ladybug / bite" angle is new.) |
| asian lady beetles bite / asian lady beetle infestation / how do ladybugs get in your house | DANGER/WHY | n/c |
| boxelder bug infestation | RID/WHY | Opening: pest how-tos 78K-286K, news 6.7K-15K |
| boxelder bug vs stink bug / boxelder bug vs kissing bug / boxelder bug life cycle | ID | n/c |
| cluster flies vs house flies | ID | **Gap**: direct "vs" video 12 views; the top result is a 643K how-to |
| cluster flies in house / cluster flies in attic / where do cluster flies come from | WHY | n/c (partial: 17K news clip) |
| why are there so many flies in my house | WHY | **Gap**: top 46K, rest under 20K, several "spiritual meaning" results |

### Fruit flies / drain flies / house fly
Peak Sep / Jul (Nov 92 / 85; Feb 57 / 40, -38% / -53%).
| Query | Intent | Competition |
|---|---|---|
| fruit flies vs drain flies / drain flies vs fruit flies | ID | Mixed: WTHR 1.25M, 548K, 1.28M; direct ID clips 9K-45K |
| drain flies in bathroom / drain flies in shower / what do drain flies look like | WHY/ID | n/c |
| fruit flies in sink drain / fruit flies in kitchen how to get rid of them / fruit flies in fridge | WHY/RID | n/c |
| house fly infestation / do house flies bite / where do house flies come from | RID/DANGER | n/c |

### Pantry moth / clothes moth / carpet beetle
Pantry moths: peak Aug (Nov 84, Dec 70, Feb 69; **no baking-season bump in search**; Oct is the autumn peak at 112 in Oct-2H). Clothes moth peak May. Carpet beetles peak **Mar** (Feb-2H 100, Mar-1H 195, Mar-2H 221): ramps from mid-February.
| Query | Intent | Competition |
|---|---|---|
| pantry moth infestation / pantry moth larvae / pantry moths | ID/RID | n/c |
| pantry moth vs clothes moth | ID | **Gap**: direct matches 686-13.7K |
| where do pantry moths come from | WHY | n/c |
| clothes moth larvae / clothes moth life cycle / clothing moths how to get rid of them | ID/RID | n/c |
| carpet beetle larvae / carpet beetle larvae infestation / what do carpet beetles look like | ID | Opening: a 45 s Short at 82K, pest how-tos 134K-542K |
| carpet beetle rash / carpet beetle on bed / carpet beetle vs bed bug | DANGER/ID | vs bed bug: **Gap** |
| tiny bugs in kitchen cupboards / tiny bugs in flour / tiny bugs in rice / tiny bugs in pantry | ID | Opening: Solutions Pest & Lawn 361K and 236K, a Short at 72K; low-view tail |
| small brown bugs in my house | ID | Opening: mixed, tangential (water bugs 149K, springtails 84K) |

### Earwig / camel cricket
Earwig peak Jun (Nov 54, Feb 40). Camel cricket peaks Oct (Nov-1H 133, Nov-2H 130, then 77 in Dec-1H, 42 by Jan-2H).
| Query | Intent | Competition |
|---|---|---|
| what happens if an earwig gets in your ear / do earwigs go in your ear / earwig in ear | WEIRD/DANGER | Crowded at the top (Peekaboo Kidz 8.7M); others 2.6K-91K. Already covered ("1 Ear Case in 10 Centuries"). |
| pincher bugs in the house / earwig infestation | ID/WHY | n/c |
| camel cricket jumping / camel cricket infestation | WEIRD/WHY | Opening: CBS New York 510K, rest 9K-67K. Already covered (11/11 "Hunchback Cricket"). |

### Mice and attic animals (winter-rising)
Mouse in house peaks Oct-Nov, rising yearly; squirrels in attic peak Jan; bats in attic peak Aug.
| Query | Intent | Competition |
|---|---|---|
| how does mice get in your house | WHY | Crowded: Plunkett's 680K, Solutions Pest 3.3M (how-to), Inside Edition 607K |
| house mouse vs deer mouse / house mouse vs field mouse | ID | n/c |
| mouse droppings vs (rat / bat) | ID | Gap/Opening: top 14K |
| squirrels in attic / squirrels in attic in winter / what do squirrels in the attic sound like | WHY/ID | **Gap**: top 22K, rest under 22K |
| bats in attic sound / bats in my attic / bats in attic noise | ID/WHY | n/c |

### Termites / ants
Peak May (termites), Jul (sugar ants), May (carpenter ants); all at their low in Dec-Jan (index 23-50) and climb from mid-Feb (carpenter ants 39 Feb-1H, 63 Mar-1H, 87 Mar-2H).
| Query | Intent | Competition |
|---|---|---|
| termites in house / termites vs ants / carpenter ants vs termites / carpenter ants in wall | ID/WHY | n/c |
| sugar ants in house / sugar ants in kitchen | WHY | n/c |
| do carpenter ants bite / are termites dangerous to humans | DANGER | n/c |

### Backyard set (Mar-Jun preview; Nov-Feb demand is low; supply not checked)
Autocomplete wording is dominated by "how to get rid of ...", "are ... dangerous" and "... vs ..." shapes.
| Creature | Peak (web) | Nov to Feb | Real queries (exact) | Note |
|---|---|---|---|---|
| carpenter bees | Apr (331) | 15 to 24 | "carpenter bees vs bumblebee", "carpenter bees in wall sound", "do carpenter bees sting" | Window opens in March (monthly index 120; Mar-2H half-month 162) |
| ticks | May (241) | 60 to 48 | "ticks in hair", "do ticks jump", "how to get rid of ticks in yard" | |
| mosquitoes | Jun (194) | 43 to 42 | "do mosquitoes like certain blood types" | Low demand winter |
| wasps / hornets / yellowjackets | Jul / see note | | "wasps vs hornets", "wasps in wall", "do wasps remember you", "do hornets remember you" | **Hornets = NBA, yellowjackets = TV show**; their winter peak is not insects |
| orb weaver / garden spider | Sep (257) / Sep | | "orb weaver vs black widow", "garden spider vs wasp", "what do garden spiders eat" | Late-summer play, not spring |
| roly poly / pill bug | May (141) | 81 to 84 | "pill bugs in house", "roly poly vs ants", "what do roly-polys eat" | Flat, evergreen-ish |
| millipede | May (139) | 81 to 68 | "millipede vs centipede", "millipede infestation" | |
| slugs | May (137) | 109 to 75 | "slugs in my house", "why are slugs coming in my house at night" | Nov bump (109) |
| moles / grubs | contaminated | | "moles vs voles", "grubs in lawn" | skin moles / game; low confidence |
| possums / raccoons | May / Jun | | "possums vs opossums", "difference between possum and opossum", "do possums have rabies" | |
| squirrels / bats in attic | Jan / Aug | | see above | Bridge to winter |

## 3. Extension-source seasonality (when each pest moves indoors)

Trends tells us when people search. Extension sources tell us why, and cover the months where search is thin. Pages read 11/10 via search results; the Purdue item is dated 10/2026.
- **Fall invaders (lady beetles, boxelder, stink bugs, cluster flies):** they find the house in fall, overwinter in wall voids and attics, and become active again on mild winter days, often near sunny windows. Cluster flies "survive the winter indoors and are often noticed on mild winter days. They do not reproduce indoors." Asian lady beetles are "more likely than other lady beetles to seek this protection in homes", can bite, and stain when handled. BMSB overwinters in homes and smells when squished. Sources: [SDSU Extension, Insects Are Being a Nuisance This Fall](https://extension.sdstate.edu/insects-are-being-nuisance-fall), [Purdue Extension, Fall Home Invaders (Oct 2026)](https://extension.purdue.edu/news/county/whitley/2026/10/fall-home-invaders.html), [UNH Extension, Seasonal Insect Invaders](https://extension.unh.edu/resource/seasonal-insect-invaders-new-hampshire-homes-fact-sheet), [NDSU, Fall-invading insects](https://www.ag.ndsu.edu/news/newsreleases/2023/october/watch-for-fall-invading-insects-in-the-home), [Alabama Extension](https://www.aces.edu/blog/topics/home/unwelcome-houseguests-in-fall-invasive-insect-pests/). Pattern in Trends agrees (Oct-Nov bursts, then low), and Feb-Mar boxelder/lady beetle re-emergence shows in Trends (Mar-1H 141 / 142).
- **Mice:** house mice move indoors in autumn when nights turn cold; people notice them most in winter; gaps of 1/4 inch are enough; exclusion is the lasting fix. Sources: [UC IPM, House Mouse](https://ipm.ucanr.edu/home-and-landscape/house-mouse/), [Arizona IPM newsletter](https://acis.cals.arizona.edu/community-ipm/home-and-school-ipm-newsletters/ipm-newsletters/2022/01/06/house-mice-signs-of-uninvited-four-legged-visitors), [UGA, keep mice and rats from coming indoors](https://fieldreport.caes.uga.edu/news/take-steps-to-keep-mice-and-rats-from-coming-indoors-for-the-winter/). Caveat from Iowa State: the fall "move-in" is mostly outdoor house mice and deer/white-footed mice; indoor house-mouse colonies persist all year.
- **Christmas-tree bugs (holiday hook, supported):** praying-mantis egg cases (about 100 eggs, laid on twigs in fall) hatch when warmed indoors; aphids and spider mites also ride in; extension advice is to inspect for egg cases and shake the tree outdoors. Most hitchhikers are a nuisance, not a danger. Sources: [Illinois Extension, Christmas tree hitchhikers](https://extension.illinois.edu/news-releases/christmas-tree-hitchhikers), [Missouri Extension](https://extension.missouri.edu/news/dr-bug-talks-pokemon-and-why-your-christmas-tree-may-be-bugged), [NC State, post-harvest pests](https://christmastrees.ces.ncsu.edu/badbugs/), [Oklahoma State](https://extension.okstate.edu/articles/2023/christmas_tree_pests.html), [WSU](https://archive.news.wsu.edu/press-release/2015/12/08/among-xmas-lights-and-garland-bugs/). Trends agrees: "christmas tree bugs" and "bugs in christmas tree" are near zero until mid-Nov, peak Dec-1H (index 811-947), and are gone by mid-January. This is the only holiday hook where both sources say yes.
- **Firewood pests (weakly supported):** wood-borer adults can emerge from firewood stored indoors even in mid-winter; they do not attack dried wood in the house; powderpost beetles are the exception; bring in a few days' supply and shake logs outside. Sources: [Purdue E-67](https://extension.entm.purdue.edu/publications/E-67/E-67.html), [UMaine](https://extension.umaine.edu/ipm/ipddl/publications/5019e/), [Purdue, Enjoy Firewood but Insects May Emerge](https://extension.purdue.edu/news/county/whitley/2022/02/enjoy-firewood,-but-insects-may-emerge.html). **Search demand is essentially nil**: "firewood bugs" Trends is zero in 4 of 5 years (one low spike in Sep and Nov 2025). Use as a hook inside a winter-pests long-form, not as its own Short.
- **Pantry pests in baking season (supported by extension, not by search):** Indian meal moth is the most common stored-product pest; holiday-baking flour pushed to the back of a cabinet turns into spring moth sightings ([Illinois Extension](https://extension.illinois.edu/news-releases/preventing-uninvited-guests-aka-pantry-pests)); moths can keep flying up to 3 weeks after infested food is thrown out; heat 130-150 F for 30 min or freezer at 0 F for 7-10 days kills them ([Oklahoma State](https://extension.okstate.edu/programs/digital-diagnostics/insects-and-arthropods/indianmeal-moth-plodia-interpunctella)); most infestations start from products bought already infested ([CSU Extension](https://extension.colostate.edu/topic-areas/insects/insect-pests-of-home-stored-foods-5-501/)). Search is flat Nov-Feb (index 84 to 69), so frame as "why is the moth still flying" in Dec-Jan. Note: Illinois says flour causes spring sightings; CSU says flour is rarely infested. Do not claim flour specifically is the source.
- **Holiday-travel bed bugs (supported by extension, not by search):** inspect mattress seams, headboard and nearby furniture before unpacking; keep luggage off the bed; bag dirty clothes; hot-wash and hot-dry 30+ min; heat or freezing is more reliable than inspecting suitcases. Sources: [UC ANR, Tips for a Bed Bug-Free Holiday](https://ucanr.edu/blog/pests-urban-landscape/article/tips-bed-bug-free-holiday), [Texas A&M IPM](https://ipm.tamu.edu/2017/12/entomologists-to-holiday-travelers-dont-let-the-bedbugs-bite/), [MSU Extension](https://www.canr.msu.edu/news/keep_bed_bugs_from_moving_in_after_travel). Trends does NOT show a Thanksgiving/December bump (Nov 90, Dec 82, Jan 66). Treat the hook as a nice-to-have on an evergreen topic.

## 4. (b) Calendar, November through February

Windows use half-month Trends indices (web, 5-yr average, annual mean = 100) plus the extension timing above. Existing queue note: the scheduled slate (posted.csv) already contains lady beetle (11/10), stink bug (11/10, 11/16, 11/7), drain/fruit fly (11/11, 11/15, 11/16), clothes moth (11/16, 11/17, TikTok carpet beetle/pantry 11/8, 11/12), centipede, mice and spider shows. See the sameness warning in section 6.

| Window | Peaking now (index) | Rising | Falling / drop | Holiday or seasonal hook |
|---|---|---|---|---|
| **Nov 10-14** | Asian lady beetle (Nov-1H 382), camel cricket 133, mouse 107, fruit flies 105, black widow n/a (Marvel) | Christmas-tree bugs (112, small) | boxelder (123, down from 221), stink bug 88, house centipede 82, spiders ~70-78 | Fall-invader tail; Veterans Day week; last window for lady beetle / boxelder search |
| **Nov 15-30** | Mouse 113, camel cricket 130, lady beetle 142 (falling), slugs 104 | **Christmas-tree bugs 690-708** (tree buying starts), pantry moth 78 | boxelder 61, centipede 67, wolf spider 57, drain flies 76, cluster flies 77 | **Thanksgiving Thu Nov 26:** holiday-baking pantry moths; holiday-travel bed bugs (extension only); real-tree purchase weekend Nov 27-29 |
| **Dec 1-15** | **Christmas-tree bugs 811-947**, mouse 110, squirrels in attic 118, silverfish 71, bed bugs 68, dust mites 85 | squirrels in attic (118 to 126), stink bug 75-91 | camel cricket 77, drain flies 58, centipede 44, spiders 42-58, fleas 63 | Peak for tree-hatching mantis egg cases; first real cold = mice, attic noise |
| **Dec 16-31** | Squirrels in attic 126, mouse 101, Christmas-tree bugs 390-537 (tail), dust mites 88, cockroach 66 | squirrels (126), stink bug (91) | most pests at annual trough: centipede 41, wolf spider 45, drain flies 52 | Post-Christmas: tree removal, "it hatched" stories; holiday guests/travel return |
| **Jan 1-15** | Squirrels in attic **143 (peak)**, dust mites 91, cockroach 71, bed bugs 69, pantry moth 72 | stink bug 90, yellowjackets/hornets (TV/NBA noise, ignore) | centipede 40, brown recluse 37, wolf spider 40, orb weaver 33 | Cold snap = attic/mouse; indoor air = dust mites; cluster flies on sunny days (extension) |
| **Jan 16-31** | Squirrels 130, dust mites 91, silverfish 71, cockroach 71 | | centipede 38, cellar spider 50, cluster flies 45 | Lowest-demand fortnight for spiders and flies |
| **Feb 1-14** | Dust mites 94, silverfish 72, cockroach 73, bed bugs 65, mouse 92 | boxelder 78, carpet beetles 59, carpenter ants 39, termites 60 | centipede 39 | Warm-day boxelder/lady beetle wake-ups (extension); Valentine travel |
| **Feb 15-28** | Dust mites 96, silverfish 78, mouse 81 | **Carpet beetles 100**, boxelder 88, lady beetle 92, termites 68, carpenter ants 49, carpenter bees 33, ticks 52 | | Spring-cleaning ramps; carpet beetle larvae season starts |

### The next four weeks (11/10-12/7): recommended topic order
| Week | Lead topics (query) | Why now |
|---|---|---|
| **Nov 10-16** | Asian lady beetle vs ladybug ("asian lady beetle vs ladybug"); boxelder bugs ("boxelder bug infestation"); cluster flies ("cluster flies vs house flies", "why are there so many flies in my house") | Lady beetle search peaks Nov-1H (382); boxelder tail; cluster flies are the gap query with the weakest supply (a 12-view direct match). Fall-invader window closes by about Nov 30. |
| **Nov 17-23** | Bugs in Christmas trees ("bugs in christmas trees", mantis egg case) as a Short, then the long-form; mice ("how does mice get in your house"); camel cricket tail | Christmas-tree query ramps now (index 155 in Nov-1H, 700 in Nov-2H); best-supported holiday hook; supply is a gap (top 41K, many results under 5K). Mouse peaks Oct-Dec and is rising yearly; this long-form slot must be published by 11/24. |
| **Nov 24-30** | Thanksgiving week: pantry moth / tiny bugs in kitchen cupboards ("pantry moth infestation", "pantry moth vs clothes moth", "tiny bugs in kitchen cupboards"); holiday-travel bed bugs ("bed bugs in hotel"); one carry-over Christmas-tree Short | Baking season and Thanksgiving travel (Nov 26); search for pantry moths is flat not rising, so the pull is the holiday hook plus the gap on "vs clothes moth". |
| **Dec 1-7** | Christmas-tree bugs peak (Dec-1H 811-947); squirrels/bats in attic ("squirrels in attic in winter", "what do squirrels in the attic sound like"); dust mites ("dust mites on eyelashes", "dust mites in bed") as the evergreen | Last strong seasonal spike before the winter trough; after Dec 7 default to the flat set (dust mites, silverfish, bed bugs, cockroach) and mice/attic. |

### March-June backyard preview
Search for the backyard set turns on in March and peaks April-June. Targets, with the window to publish about 3-4 weeks ahead of the half-month where the index crosses 100:
| Creature | Index crosses 100 | Peak | Publish by |
|---|---|---|---|
| carpet beetle (house) | Feb-2H | Mar (210) | Feb 1-15 |
| termites (swarm) | Mar-1H (88), Mar-2H 106 | May (192) | Mar 1-15 |
| carpenter bees | Mar-2H (162) | Apr (331) | Mar 1-10 |
| carpenter ants | Mar-2H (87), Apr 139 | May (217) | Mar 15-Apr 1 |
| ticks | Apr (150) | May (241) | Mar 15-Apr 1 |
| wasps / hornets (insects) | May (124) | Jul (195) | Apr 15-May 1 |
| mosquitoes | May (157) | Jun (194) | Apr 20-May 5 |
| roly poly / millipede / slugs | Mar-Apr (101-137) | May | Mar 20 |
| brown recluse / wolf spider / house centipede (back to search) | Apr (93-118) | Jun-Aug | Mar 25-Apr 15 |
Source: 5-yr web Trends monthly index (`75-seasonality-monthly-index.csv`).

## 5. (c) 30 title candidates

Rules applied: 45-65 characters (I counted the title text only, excluding the creature emoji and the "(Things Living In Your House #N)" / show tag, which the MASTER_ORDERS 11/3 rule says are added on top); a "Your house / bed / kitchen / basement" phrase; a concrete number or specific fact; none of the banned words (TRUE or FALSE, Myth, Believe, Cartoons, Lied, "Did you know"). Add one creature emoji and the series tag when scripting. Titles lead with the real autocomplete phrase where grammar allows. **"Fact status" tells you what still needs a source before scripting**; "ext" means the fact comes from an extension page cited in section 3.

### Shorts (20)
| # | Title (text only, characters) | Targets (real query) | Window | Fact status | Supply |
|---|---|---|---|---|---|
| S1 | House Centipede vs Roach in Your Kitchen: 30 Legs vs 6 (54) | house centipede vs roach | Nov 10-Dec 15 (evergreen; trough Dec-Feb) | roach 6 legs; centipede 30 legs (channel already uses 30) | Opening (390K live-feed; big explainers) |
| S2 | House Centipede vs Spider in Your Basement: 30 Legs vs 8 (56) | house centipede vs spider | Nov 10-30 | spider 8 legs; verify who wins claim, no 'wins' without source | Gap (direct match 920 views) |
| S3 | Cellar Spider vs Brown Recluse in Your House: 8 Eyes vs 6 (57) | cellar spider vs brown recluse | Nov 15-Dec 15, again Apr-Jul | verify eye counts | Gap (4K-7K) |
| S4 | Cluster Flies in Your House: 0 Babies Born Indoors in Winter (60) | cluster flies in house | Nov 10-Dec 15; warm-day bursts Jan-Feb | ext (SDSU/NDSU/UNH) | Gap (12-view direct match) |
| S5 | Why Are There So Many Flies in Your House? Blame 1 Fly (54) | why are there so many flies in my house | Nov 15-Jan 31 | ext; link to cluster fly | Gap (top 46K) |
| S6 | Boxelder Bugs in Your House: 1 Warm Day Wakes Them Up (53) | boxelder bug infestation | Nov 10-30; again Feb 15-Mar 31 | ext (mild days) | Opening (pest how-tos 78K-286K) |
| S7 | Asian Lady Beetle vs Ladybug in Your House: Only 1 Bites (56) | asian lady beetle vs ladybug | Nov 10-30 (peak is now) | ext says Asian beetles bite; verify 'only 1' | Gap/Opening (news 184K) |
| S8 | A Christmas Tree Brought 100 Mantis Eggs Into Your House (56) | bugs in christmas trees | Nov 20-Dec 15 (peak Dec 1-15) | ext (Missouri ~100 eggs/case) | Gap (top 41K) |
| S9 | Christmas Tree Bugs in Your House: 1 Tree in 100,000 (52) | bugs in christmas trees | Nov 20-Dec 15 | verify NC State figure | Gap (top 41K) |
| S10 | Pantry Moths Keep Flying in Your Kitchen 3 Weeks Later (54) | pantry moth infestation | Nov 20-Jan 15 (baking season) | ext (OSU, up to 3 weeks) | n/c (pantry moth: gap on vs) |
| S11 | 2 Moths in Your House: Pantry Moth vs Clothes Moth (50) | pantry moth vs clothes moth | Nov 20-Jan 15 | ext (pest ID) | Gap (686-13.7K) |
| S12 | Carpet Beetle vs Bed Bug in Your Bed: 1 Bites, 1 Doesn't (56) | carpet beetle vs bed bug | Nov 15-Dec 15; ramps Feb 15-Apr 15 | verify bite claim | Gap (19K) |
| S13 | Small Brown Bugs in Your House: 1 Is Eating Your Carpet (55) | small brown bugs in my house | Dec 1-Apr 15 | verify | Opening (mixed) |
| S14 | Tiny Bugs in Your House Plants: 1 Gnat Lays 200 Eggs (52) | tiny bugs in plant soil | Nov 15-Feb 28 (plants indoors) | verify 200 eggs | Opening (48K-174K) |
| S15 | How Do Mice Get in Your House? Through a 1/4-Inch Gap (53) | how does mice get in your house | Nov 10-Jan 15 | ext (UC IPM 1/4 inch) | Crowded (680K, 3.3M) |
| S16 | Why Mice Move Into Your House in November (3 Entry Points) (58) | mouse in house (Trends); how does mice get in your house | Nov 10-Dec 31 | ext (UC IPM entry points) | Crowded (see #15) |
| S17 | Silverfish vs House Centipede in Your Basement: 1 Hunts (55) | silverfish vs house centipede | Nov 10-Jan 31 (silverfish flat all year) | verify | Gap (no direct match) |
| S18 | Dust Mites on Eyelashes vs in Your Bed: 2 Different Mites (57) | dust mites on eyelashes | any week (flattest curve, 86-116) | verify (Demodex vs dust mite) | Crowded eyelash (2.6M); distinction open |
| S19 | Stink Bug Nymphs in Your House: 5 Stages Before Adult (53) | stink bug nymphs | Nov 10-Dec 15; again Mar-Apr | verify instars | Gap (34-33K) |
| S20 | Bed Bugs in a Hotel Can Follow You to Your Bed: 3 Checks (56) | bed bugs in hotel | Nov 18-Jan 3 (holiday travel) | ext (UC ANR/TAMU/MSU) | Crowded news; how-tos 15K-201K |

### Long-form (10)
| # | Title (text only, characters) | Targets (real query) | Window | Fact status | Supply |
|---|---|---|---|---|---|
| L1 | Bugs in Your House in Winter: 7 Pests That Moved In (51) | bugs in my house / bugs in winter | Nov 10-Jan 31 | ext | n/c |
| L2 | House Centipede vs 3 Rivals in Your Basement: Who Wins? (55) | house centipede vs praying mantis / roach / spider | Nov 17-Dec 15 | verify | Gap/Opening |
| L3 | Brown Recluse vs Cellar vs Wolf: 3 Spiders in Your House (56) | brown recluse vs wolf spider / cellar spider vs brown recluse | Dec 1-Jan 31 (spider trough; evergreen comparison) | verify | Gap |
| L4 | Is It a Bed Bug? 5 Bugs in Your Bed That Look Like One (54) | what bug is this / carpet beetle vs bed bug / bed bugs look like | Dec 1-Mar 15 | verify | Opening |
| L5 | Bugs in Your Christmas Tree: 6 Hitchhikers in Your House (56) | bugs in christmas trees | publish by Nov 24; window Nov 20-Dec 20 | ext | Gap |
| L6 | Tiny Bugs in Your Kitchen: 8 Pantry Pests Explained (51) | tiny bugs in kitchen cupboards / pantry / flour / rice | Nov 24-Jan 15 | ext (CSU/OSU) | Opening |
| L7 | 3 Fall Invaders in Your House: Stink Bug, Lady Beetle, Boxelder (63) | why are stink bugs in my house | Nov 10-Dec 5 (Feb 15 rerun) | ext | Opening |
| L8 | Animals in Your House in Winter: 5 Sounds in the Attic (54) | squirrels in attic in winter / bats in attic sound | Dec 8-Feb 15 (peak Jan) | verify sounds | Gap |
| L9 | 12 Months of Pests in Your House, From Mice to Carpenter Ants (61) | seasonal (this report) | Dec 1 onward, evergreen | Trends + ext | n/a |
| L10 | Mice in Your House: 3 Ways In and How to Block Them (51) | how does mice get in your house | Nov 10-Dec 31 | ext (UC IPM) | Crowded |

## 6. (d) The ten strongest questions we have NOT covered yet

Checked against posted.csv (all 184 rows, including scheduled to 11/28) by title and by script filenames in `scripts/drawn-house/`. "Covered" means a title in posted.csv; a script file that has not been posted does not count as posted. Ranked by autocomplete strength x seasonal fit x thin supply.

| # | Question (real wording) | Why it ranks | Posted.csv check | Supply |
|---|---|---|---|---|
| 1 | **why are there so many flies in my house** / cluster flies vs house flies / cluster flies in house | Only generic-seed result about flies; cluster flies re-emerge on mild winter days (extension); weakest supply of any query checked | 0 cluster-fly titles; "House Flies Throw Up on Your Food" (10/27) is about house fly vomit, not winter flies | Gap |
| 2 | **bugs in christmas trees** (mantis egg cases) | Only holiday hook confirmed by both Trends and extension; index 700-947 in Nov-2H/Dec-1H | 0 titles mention Christmas/tree/firewood | Gap (top 41K) |
| 3 | **house centipede vs spider / vs roach / vs praying mantis** | "house centipede vs roach" and "vs spider" are top-4 suggestions on the bare seed; the centipede is our best-retaining animal (62% stayed) | Centipede Parts 1-4 and "squish" angle posted; no "vs" matchup | vs spider: Gap; vs roach: Opening |
| 4 | **tiny bugs in kitchen cupboards / flour / rice / pantry** (pantry moth larvae, weevils) | "tiny bugs in ..." is a generic-seed autocomplete family with 6 kitchen variants; holiday baking | Only TikTok has pantry moth (11/12); YouTube has none | Opening |
| 5 | **small brown bugs in my house** / carpet beetle larvae / carpet beetle vs bed bug | Identification query that cross-links to bed bugs (our best-performing topic); carpet beetle peaks Mar | TikTok-only ("Tiny Beetle on Your Window", 11/8); no YouTube title | Gap (vs bed bug) |
| 6 | **cellar spider vs brown recluse** / vs black widow | Direct-match supply is 4K-7K; our recluse and daddy-longlegs Shorts are search sources; the poll for it exists (research/64) but not a video | Recluse (3 Shorts), daddy longlegs, "Mommy Longlegs"; no cellar-vs-recluse | Gap |
| 7 | **how does mice get in your house** (1/4-inch gap) | Mouse is the one house pest that stays at or above average all winter and is rising each year; extension-confirmed entry facts | Mouse droppings (11/2) and "200 mouse meals" (11/9); neither covers entry | Crowded (680K, 3.3M); win on the number, in Short form |
| 8 | **tiny bugs in plant soil / houseplants** (fungus gnats, springtails) | "tiny bugs in plant soil" and "flying bugs in my houseplants" are suggestions on "bugs in my house"; plants are indoors Nov-Mar | 0 titles | Opening (48K-174K) |
| 9 | **why are boxelder bugs in my house / boxelder bug vs stink bug** | Boxelder peaks Oct, re-emerges Feb-Mar (extension and Trends); pest-control-only supply | 0 titles ("It Lives in Your Walls All Winter" is a stink bug loop) | Opening |
| 10 | **squirrels in attic in winter / what do squirrels in the attic sound like** (+ bats in attic sound) | Peak Jan (143); bridges house-pest content to the backyard-creature expansion; supply is a gap | 0 titles | Gap |
Honorable mentions not covered: "silverfish vs house centipede" (gap, low weight), "stink bug nymphs", "dust mites on eyelashes vs dust mites in bed", "asian lady beetle vs ladybug do they bite" (angle on the 11/10 Short), "bed bugs in hotel" holiday check, "what bug is this" ID series (generic seed; the suggestion list is short).
Already covered and so excluded: earwig-in-ear, camel cricket, termites, carpenter ants, false widow vs black widow, drain/fruit flies, clothes moth, bed bugs x4, dust mites x3, silverfish/books, cockroach x4, mouse droppings, stink bug.

## 7. Cautions for the plan

1. **Sameness risk in the queue.** posted.csv (scheduled) has "Tiny Flies on Your Banana Breed in Your Drain" (11/15) and "Tiny Flies on Your Banana. Again." (11/16), "The Moth Isn't Eating Your Sweater" (11/16) and "The Moth Can't Eat Your Sweater" (11/17), and the 3 Bugs You Should Never Kill title three times (11/7, 11/21, 11/28). Same topic, near-identical title, two days apart is the pattern KNOWLEDGE.md flags under policy 1311392. Spread these or give each its own storyline and title.
2. **The "Never kill the X" clone wave** (hundreds of 5-10 min videos at 18-3,000 views on "house centipede in bathroom" and "stink bug") means that exact template is already saturated by low-effort channels; our #21/#44 centipede Shorts are different because they are numbers-first Shorts.
3. **Health queries (brown recluse bite stages, dust mite bites, bed bug bites, carpet beetle rash):** CDC/university sources and "see a doctor" phrasing only.
4. **Not measured:** actual monthly search volume, upload dates, channel subscriber counts. If you want volume, the vidIQ keyword tool used in research/51 can be run on the 10 questions in section 6; I did not touch it (read-only brief).
5. **Titles that still need a source check before scripting:** "8 eyes vs 6" (cellar spider/recluse), "30 legs" and the centipede-vs facts, "only 1 bites" (Asian lady beetle vs ladybug; extension supports that Asian beetles can bite, not that no ladybug can), "1 tree in 100,000" (NC State figure; read the page), "1 gnat lays 200 eggs", "carpet beetle: 1 bites, 1 doesn't", "5 stages" (stink bug instars), "silverfish: 1 hunts" (centipede eats silverfish).
