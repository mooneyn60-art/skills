# 28 — Shorts virality: topics, hooks, formats, 40 ranked concepts (The Hitmaker, 2026-10-24)

**Legend.** [M] measured here (yt-dlp, 2026-10-24). [3P] third-party. [I] my inference. View counts are public counts on 10/24.
Raw data (not in repo): `/tmp/claude-0/-home-user/f2581a8c-fe42-5876-b5f9-d941a863a7fa/scratchpad/viral/` (`s1.json`, `s2.json` = 55 Shorts-filtered searches; `chans.json` = Shorts tabs of 20 animal channels; `meta.json` + `subs/` = 43 Shorts with date, likes, comments and auto-captions).

## 0. Method and limits
- vidIQ had **no credits** on 10/24 (every call refused), so this is yt-dlp only.
- `ytsearch50:` flat results contain **zero** Shorts. What works: the search URL with the Shorts filter `&sp=EgIQCQ%3D%3D` (or `EgIYAQ%3D%3D`, under 4 min) plus `extract_flat`. Ran 55 queries (all 12 required terms, plus format terms).
  - The raw search is dominated by kids' content (Cocomelon, Spider-Man); I filtered it out by regex. Results: 411 Shorts, 287 kept.
- Channel Shorts tabs (`/channel/<id>/shorts`, flat) give newest-first titles and views: 20 channels, about 1,500 Shorts.
- **Bot-block workaround** [M]: full extraction fails with "Sign in to confirm you're not a bot". It works with `extractor_args={'youtube':{'player_client':['mweb','web_embedded']}}` and `ignore_no_formats_error=True`, which return upload date, likes, comments and English auto-captions. That is how the opening lines in §2 were read.
- Bias: the query mix over-samples spiders and bears (240 results each). Read the topic table as "which topics have breakouts", not as market share.

## 1. Topic demand (what is blowing up now)
Channel baselines (median views of the latest 60 Shorts) [M]: Zack D. Films 9.45M, **More Parz 9.85M (Australian animal facts)**, The Outliners 1.8M, Bunzy Trove 2.2M (prehistoric "Evolution of…"), Kelvin Wiley 276k (bugs), Coyote Peterson 47k, Nature Archive 30k, Odd Species 21.5k, What Gives? 14k, WildNature Lab 238.

Recent animal breakouts (upload date → views on 10/24) [M]:
| Short | Uploaded | Views | Hook type |
|---|---|---|---|
| Why Baby Koalas Eat Their Mom's Poop (Zack D.) | 10-18 | 15.1M in 6 days | gross cold open |
| Why Cats Rub Against Your Laptop (Zack D.) | 10-17 | 14.2M | "You know when your cat…" |
| Why Animals Have Different Eye Positions (Zack D.) | 10-12 | 15.1M | "If your eyes were moved…" |
| How Harris's Hawks Hunt Together (Zack D.) | 10-15 | 11.4M | mid-action |
| Every Big Cat, Ranked By How Many People It Killed (Nature Archive) | 09-25 | 1.4M (47x channel) | ranked, last-one tease |
| The worlds worst parent is a bird (More Parz) | 09-15 | 8.9M | "This bird throws its kids off a cliff" |
| Why You Should Leave House Spiders Alone (Zack D.) | 09-11 | 11.8M | mid-action |
| Australian Eagles are built DIFFERENT (More Parz) | 09-08 | 18.8M | "…a bird so big it eats kangaroos" |
| Deadliest spider (Doctor NOS) | 08-03 | 13.1M | "Your first thought is the black widow…" |
| What You're Not Told About Black Widows (Kelvin Wiley) | 07-27 | 2.3M (8x) | misconception callout |
| One Tick Bite = Meat Allergy FOREVER (Kelvin Wiley) | 05-27 | 1.4M | personal stakes, **4.8 comments/1k views** |
| Satan's greatest Seal (More Parz, leopard seal) | 06-25 | 24.9M | what-if |

Topic buckets across the 287 search results plus the channels' latest 60 Shorts, median views [M]:
- **Australian/marsupial: 9.3M** (n=23; inflated by More Parz)
- **Spiders: 2.2M** (n=126)
- **Prehistoric/extinct: 1.45M** (n=48)
- Frogs 140k
- Sharks 243k (n=9)
- Insects/bugs 99.5k
- Birds 83k
- Bears 63k (but the top bear Shorts reach 18-23M)
- Crocs 57k
- Big cats 25k
- Dogs 22k
- Cats 15k (but Zack's cat Short reached 14M)

**Read** [I]: what wins is **danger to you** (spiders, bears, ticks, sharks), **body horror or gross** (poop, broken bones, parasites), **"nature is absurd"** (shrimp gun, useless fish, worst parent), and **prehistoric scale**.
- Cute-only and pure anatomy trivia lose. Our own data agrees: river shark 769, goldfish 661, porcupine 575 (danger and surprise); owl 133, camel 170, lemming 188 (trivia).
- **Nothing titled "TRUE or FALSE" appeared among the breakouts.** The "animal true or false" query returned only kids' content. Myths that win are framed as **"what you're not told"** or **"your first guess is wrong"**.

## 2. The hook: opening lines of 43 top animal Shorts (auto-captions, first ~4 s) [M]
| Hook class | n | Median views | Comments /1k | Example opening (verbatim) |
|---|---|---|---|---|
| A. Shocking statement: "This X does Y" | 10 | 15.1M | 0.82 | "This shrimp has a gun." / "This frog deliberately breaks its own bones." / "Australia has a bird so big it eats … kangaroos." |
| G. What-if hypothetical | 2 | 21.1M | 0.54 | "If a spider grew to 1,500 lb and had 15 ft legs it could theoretically hunt a…" |
| C. Second-person scenario | 6 | 15.7M | 0.51 | "If you encounter a grizzly bear and try to run…" / "You know when your cat climbs onto your keyboard…" |
| B. Mystery with an open loop | 1 | 27.3M | 0.40 | "Aussie farmers thought they were being attacked by aliens. But what was actually causing it is so much funnier." |
| E. Mid-action cold open (no setup) | 8 | 10.7M | 0.46 | "It crawls underneath its mother to eat her poop…" / "Place a cup over it and slide in a spatula…" |
| H. Visual only, no voice | 3 | 9.3M | 0.63 | Bunzy "Evolution of Megalodon"; ArS jumping-spider close-up |
| D. Misconception callout | 4 | 7.7M | **1.36** | "Who's the deadliest spider? Your first thought is probably the black widow…" / "If I asked you what spider this is, your answer might be black widow…" |
| F. Ranked list, last-one tease | 8 | 1.6M | 0.14 | "Every shark that has killed a person, ranked … and the last one has killed more…" |
| Plain question "TRUE or FALSE?" | 0 | — | — | none in the sample |

Caveats: class A is mostly More Parz, so class and channel are confounded. Still, every one of the 43 Shorts puts the **specific, surprising content in the first 5 words**, and none opens with a format label.

**Hook formats that beat a plain "TRUE or FALSE?"**, keeping our quiz beat at about 1.5 s [I from the table]:
1. **Claim as an outrageous statement, then the question:** "This shrimp shoots a bubble hotter than the sun." followed by "True or false?" over the countdown. The claim is the hook; the quiz is the commitment.
2. **Misconception callout ("your first guess is wrong"):** "Name the deadliest spider. You said black widow, didn't you?" It has the best comment rate (1.36/1k) and is our brand.
3. **Second-person stakes:** "A bear is chasing you. Run downhill. True or false?" Survival content gets shares.
4. **What-if / scale:** "If a flea were your size…", but only with numbers that survive checking.
5. **Gross or absurd cold open:** start on the action word ("It eats its mom's poop.").
- Rules for all five:
  - Never open on the word "True"; put the animal noun in the first 2 words.
  - The spoken line and the on-screen text say the same 5-7 words.
  - Show the animal's face full-bleed from frame 1 (already done 10/24).

## 3. Formats beyond single myths
| Format | Evidence [M] | Fit for calm quiz brand |
|---|---|---|
| **"Which is deadlier / older / faster?" A-or-B quiz** (shark vs cow) | Nature Archive "ranked by kills" 1.4M (47x); Polar vs Grizzly 2.3M | **High**: same countdown, two photos split-screen, real data answer |
| **"Your first guess is wrong" superlative** (deadliest spider, most painful sting) | Doctor NOS 13.1M; Jack's "MOST PAINFUL STING?!" 17.8x | **High**: a myth disguised as a superlative |
| **"Spot the animal / spot the fake"** camouflage photo | Wild Fact Zoo "Can You Spot the Hidden Animals?" 51.7x; Odd Species "Spot the Fake Ant" 3.7x | **High**: pure quiz, iNat has great camouflage photos, the loop is natural |
| **"Worst / most useless / laziest animal"** superlatives | More Parz worst parent 8.9M, useless fish 14M; What Gives? worst mating 10.7x | Medium-high: punchline-friendly; reframe as "TRUE: this bird…" |
| **"If X were human-sized"** | Zack "What If Spiders Hunted Humans" 17.4M | Medium: physics claims are often wrong; use only measured ratios |
| **Ranked list with last-one tease** (Top 5, every X ranked) | Loopix giant spiders 16.9M, Vigo 1.7M, but median only 1.6M and 0.14 comments/1k | Low-medium: needs 40-90 s; breaks our 20 s loop |
| "Which would win" fights | most results are AI or kids', tiny views (6, 4) | Low: unfalsifiable, so it conflicts with fact-checking |
| POV "you're a…" | 1 hit in 287, no breakouts | Low |
| Evolution / types-of montages (no voice) | Bunzy 15-46M, Skur 9.2M (2023) | Low for us: needs drawn art, not photos |

## 4. Comment and share triggers
- **Comments come from personal stakes and correctable wrongness**, not from "comment your score".
  - Tick meat allergy: 4.8/1k. Black widow and arachnophobia: 1.8/1k. More Parz statements: 0.8-1.3/1k. Ranked lists: 0.14/1k.
  - Triggers:
    - "Is this in my house or yard?"
    - "I was told the opposite."
    - "My uncle got bitten by one."
    - Contested or surprising numbers people want to argue with.
  - Our pinned comment should ask **"Who told you this one?"** or **"Have you seen one?"** rather than "what's your score?".
- **Shares**:
  - Fear and safety: "send this to someone scared of spiders"; bear advice.
  - Gross-out: koala poop.
  - Dinner-table facts with a number: "sharks are older than trees".
- **Likes**: More Parz gets 5-8% likes against Zack D.'s 2-4%. The difference is a voice with opinions ("this bird SUCKS at being a bird").
  - [I] Meatball's punchline card should *judge* the animal, not restate the fact.
- **Loops**: the "Did you really think" loop line already works (128% viewed). Keep it.

## 5. Forty concepts, ranked by expected views
Not already covered in `scripts/` (64 existing titles checked). Facts are checked against the source named in each entry.

1. **Goliath birdeater.** Hook: "The world's biggest spider eats birds." Answer: **FALSE, mostly.** Birds are rare prey; it eats worms, insects, frogs and rodents (Natural History Museum). Why: giant spiders are the biggest bucket (Loopix 16.9M, Vigo 1.7M) and the myth is in the name. Photo: *Theraphosa blondi*.
2. **Black widow.** Hook: "Deadliest spider? You said black widow." Answer: **FALSE.** Bites are painful but deaths are extremely rare, and antivenom exists. Why: Doctor NOS 13.1M, Kelvin Wiley 2.3M; misconception class with top comments. Photo: *Latrodectus mactans*.
3. **Pistol shrimp.** Hook: "This shrimp shoots a bubble almost as hot as the sun." Answer: **TRUE.** The collapsing cavitation bubble reaches about 4,700 °C against about 5,500 °C at the sun's surface (Lohse et al., *Nature* 2001). Why: More Parz "This shrimp has a GUN" 16.1M. Photo: *Alpheus heterochaelis*.
4. **Grizzly bear.** Hook: "A bear is chasing you. Run downhill." Answer: **FALSE.** Bears run downhill fine, at up to about 56 km/h (NPS). Why: Zack D. grizzly escape 23.5M and bear spray 18.5M; survival content gets shares. Photo: *Ursus arctos*.
5. **Shark.** Hook: "Sharks are older than trees." Answer: **TRUE.** Sharks date back about 400-450 Myr; the first trees about 385 Myr. Why: shark is our best topic (river shark 769) and the fact is pure share-bait. Photo: *Carcharodon carcharias*.
6. **Turtle.** Hook: "A turtle can crawl out of its shell." Answer: **FALSE.** The shell is its fused ribs and spine. Why: "Empty Turtle Shell Isn't What You Think" 5.2M at 106x (research/23); cartoon myth. Photo: *Chrysemys picta*.
7. **Lone star tick.** Hook: "One tick bite can make you allergic to steak." Answer: **TRUE.** Alpha-gal syndrome (CDC). Why: 4.8 comments/1k, the highest measured; personal stakes. Photo: *Amblyomma americanum*.
8. **Koala.** Hook: "Baby koalas eat their mom's poop." Answer: **TRUE.** "Pap" seeds the joey's gut microbes for digesting eucalyptus. Why: Zack D. 15.1M in 6 days (10-18), trending now. Photo: *Phascolarctos cinereus*.
9. **Camel spider.** Hook: "This spider screams and chases you." Answer: **FALSE.** It is a solifuge, not a spider; it isn't venomous and chases your *shadow* for shade. Why: spider, fear and a myth together; the soldier-photo legend. Photo: Solifugae (*Eremobates*).
10. **Cow vs shark.** Hook: "Cows kill more Americans than sharks." Answer: **TRUE.** About 20 a year from cattle (CDC 2003-08) against about 1 a year from sharks (ISAF). Why: A-or-B format, shark demand, argument bait. Photo: *Bos taurus*.
11. **Praying mantis.** Hook: "Female mantises always eat the male." Answer: **FALSE.** It happens in a minority of wild matings, roughly 1 in 4 or fewer (Lawrence 1992). Why: "Why Being A Male Spider Is Unlucky" 10M. Photo: *Mantis religiosa*.
12. **Wedge-tailed eagle.** Hook: "Australia has an eagle that hunts kangaroos." Answer: **TRUE.** It takes joeys and young wallabies and kangaroos. Why: More Parz 18.8M (09-08); Australian bucket 9.3M. Photo: *Aquila audax*.
13. **Brown recluse.** Hook: "One recluse bite rots your flesh off." Answer: **FALSE, mostly.** Most bites heal without severe necrosis, and many "bites" are misdiagnosed (Vetter). Why: "How DEADLY is the brown recluse REALLY?" 2.6M. Photo: *Loxosceles reclusa*.
14. **Polar bear.** Hook: "Polar bears aren't white." Answer: **TRUE.** The skin is black and the hairs are unpigmented and translucent. Why: bear demand, plus a visual reveal. Photo: *Ursus maritimus*.
15. **Tiger.** Hook: "Shave a tiger and it's still striped." Answer: **TRUE.** The skin itself is striped. Why: big-cat ranked 1.4M; instant visual payoff. Photo: *Panthera tigris*.
16. **Cockroach.** Hook: "A cockroach can live for a week with no head." Answer: **TRUE.** It breathes through spiracles and dies of thirst. Why: gross-out share trigger. Photo: *Periplaneta americana*.
17. **Wolf spider.** Hook: "Don't squash this spider. Hundreds of babies run out." Answer: **TRUE.** Females carry the spiderlings on their back. Why: "If You See This Spider… Don't Kill It" 867k at 75x; house-spider Short 11.8M. Photo: *Hogna carolinensis*.
18. **Huntsman.** Hook: "Australia's dinner-plate spider is deadly." Answer: **FALSE.** Its bite isn't dangerous to people. Why: Australia + giant spider + home invader. Photo: *Isopeda / Heteropoda*.
19. **Barnacle goose.** Hook: "These chicks jump off a 100 m cliff before they can fly." Answer: **TRUE.** Goslings leap from cliff nests to reach food. Why: "worst parent is a bird" 8.9M. Photo: *Branta leucopsis*.
20. **Cassowary.** Hook: "This bird has killed a man." Answer: **TRUE.** In 1926 in Australia and in 2019 in Florida. Why: danger to you; dinosaur-looking. Photo: *Casuarius casuarius*.
21. **Mosquito.** Hook: "The deadliest animal on Earth weighs 2 milligrams." Answer: **TRUE.** It spreads malaria (about 600k deaths a year, WHO) and other diseases. Why: deadliest-animal searches; number hook. Photo: *Aedes aegypti*.
22. **Hognose snake.** Hook: "This snake fakes its death, badly." Answer: **TRUE.** It rolls belly-up, and flips back over if you right it. Why: "I can fix your fear of snakes" 16.4M; funny and calm. Photo: *Heterodon platirhinos*.
23. **Rattlesnake.** Hook: "A dead snake can still bite you." Answer: **TRUE.** Severed heads keep a bite reflex for up to about an hour. Why: danger to you; counter-intuitive. Photo: *Crotalus atrox*.
24. **Octopus.** Hook: "Two-thirds of an octopus's brain is in its arms." Answer: **TRUE.** About 350M of its 500M neurons. Why: octopus is a required term and the claim is brainy-weird. Photo: *Octopus vulgaris*.
25. **Orca.** Hook: "Killer whales aren't whales." Answer: **TRUE-ish.** They are the largest dolphin (Delphinidae). Note that dolphins are toothed whales, so phrase it as "they're dolphins". Why: name myth. Photo: *Orcinus orca*.
26. **Crocodile.** Hook: "Crocodile tears are real." Answer: **TRUE.** Crocodilians tear while eating (Shaner & Vliet 2007). Why: an idiom people say; surprise answer. Photo: *Alligator mississippiensis*.
27. **Ants.** Hook: "All the ants on Earth outweigh all humans." Answer: **FALSE.** Ants make up about 20% of human biomass (Schultheiss et al., *PNAS* 2022). Why: famous "fact" busted, with a number. Photo: *Camponotus pennsylvanicus*.
28. **Cat.** Hook: "Cats only meow at humans." Answer: **TRUE, mostly.** Adult cats rarely meow at each other. Why: Zack D. cat 14.2M (10-17); pet audience. Photo: *Felis catus*.
29. **Dog.** Hook: "Dogs only sweat through their tongues." Answer: **FALSE.** They have sweat glands in their paw pads. Why: pet myth; Zack D. format. Photo: *Canis familiaris*.
30. **Megalodon.** Hook: "Megalodon is still alive in the deep sea." Answer: **FALSE.** Extinct about 3.6 Mya; no teeth younger than that. Why: prehistoric bucket 1.45M; Bunzy 15.3M. Photo: *C. carcharias* as a size reference.
31. **Chicken.** Hook: "T. rex's closest living relatives are in your fridge." Answer: **TRUE.** Birds; collagen grouped T. rex with chickens and ostriches (*Science* 2008). Why: prehistoric plus everyday object. Photo: *Gallus gallus domesticus*.
32. **Hippo vs pig.** Hook: "A hippo's closest relative is a whale, not a pig." Answer: **TRUE.** Whippomorpha. Why: A-or-B quiz format. Photo: *Hippopotamus amphibius*.
33. **Spot the animal.** Hook: "There's a bird in this photo. Find it in 3 seconds." Answer: a common potoo posing as a branch. Why: Wild Fact Zoo spot-the-animal 51.7x; native quiz format. Photo: *Nyctibius griseus*.
34. **Spot the animal 2.** Hook: "Find the gecko." Answer: a leaf-tailed gecko on bark. Why: series #2 of the hit format. Photo: *Uroplatus fimbriatus*.
35. **Jumping spider.** Hook: "This spider twitches in its sleep like it's dreaming." Answer: **TRUE.** REM-like sleep, with its retinas moving (Rößler et al., *PNAS* 2022); whether it dreams is unknown. Why: ArS jumping spider 8.3M; cute spider. Photo: *Phidippus regius*.
36. **Wood frog.** Hook: "This frog freezes solid and comes back to life." Answer: **TRUE.** Its heart stops and about 65% of its body water freezes. Why: frog bucket 140k; "breaks its own bones" 12.7M. Photo: *Lithobates sylvaticus*.
37. **Platypus.** Hook: "The cutest animal in Australia is venomous." Answer: **TRUE.** Males have hind-leg spurs whose venom causes weeks of pain. Why: Australia + danger + cute contrast. Photo: *Ornithorhynchus anatinus*.
38. **Crow.** Hook: "Crows remember your face and hold a grudge." Answer: **TRUE.** In the UW mask study (Marzluff) crows scolded the mask for years. Why: relatable; "has a crow hated you?" comments. Photo: *Corvus brachyrhynchos*.
39. **Capybara.** Hook: "The world's biggest rodent is heavier than your dog." Answer: **TRUE.** Up to about 65 kg. Why: capybara trend ("Why Every Animal Loves the Capybara" 18.5x). Photo: *Hydrochoerus hydrochaeris*.
40. **Pig.** Hook: "Pigs can't look up at the sky." Answer: **FALSE.** Their neck limits it but they can. Why: classic schoolyard myth; low risk. Photo: *Sus scrofa domesticus*.

Ranking logic [I]: topic-bucket median × closeness to a ≥10M recent breakout × comment trigger (personal stakes or correctable wrongness) × visual payoff on our photo-only stack.
Photo checks before scripting:
- #1 *Theraphosa* and #9 Solifugae have fewer research-grade photos.
- #33-34 need a full-frame camouflage photo, not a close-up.

## 6. Do next (one change per week, per research/24)
1. Week 1: script #1-#5 with **hook type 1** (statement, then "True or false?" at about 1.2 s). Measure stayed-to-watch against our 40%.
2. Week 2: the same, but with hook type 2 (misconception callout) on #2, #13 and #11. Pin "Who told you this one?".
3. Week 3: launch "Spot the animal #1/#2" (#33-34) as the second series, giving a reason to subscribe.
4. Titles stay as search questions ("Does the Goliath Birdeater Really Eat Birds?"). The hook lives in the voice and on-screen text, not in the title.
