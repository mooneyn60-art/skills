# 81 · TikTok: For You vs Search, and whether captions are the lever (2026-11-11)

Read-only research. Nothing was changed in Metricool. Sources are TikTok's own pages (fetched 2026-11-11), Metricool brand 7521392 (per-post TikTok data pulled 2026-11-11), `research/80-scoreboard-1111.md`, `research/data/80-tiktok.csv` and `skills/channel-brain/MASTER_ORDERS.md`.

## The answer
Probably not captions or hashtags. TikTok lists captions and hashtags only as "video information", a minor input; its named strong signal is viewers finishing a video, and our own data shows no caption or hashtag pattern that survives topic, length and the three outlier posts. Also, TikTok Studio says 80% of our views are already For You and 18% Search (28 days to 11/10, from MASTER_ORDERS), so the problem is how many For You viewers each video gets, not a search-versus-For-You mix.

Recommendation: no caption or hashtag change. The files carry new_text equal to old_text.

## 1. What TikTok itself says (verified from TikTok pages)

**Ranking signals and where captions sit**
- TikTok Newsroom, "How TikTok recommends videos #ForYou", dated June 18, 2020 (old page, still the main public explanation). https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
  - Three signal groups: user interactions (likes, shares, follows, comments, content created), video information, device and account settings.
  - Video information "might include details like captions, sounds, and hashtags." No weight is given for any of them.
  - Factors are "weighted based on their value to a user." Strong signals such as finishing a longer video get more weight than weak ones. Device and account settings carry "lower weight."
  - "neither follower count nor whether the account has had previous high-performing videos are direct factors."
- TikTok Transparency, "Introduction to the TikTok recommendation system" (footer 2025, no page date). https://www.tiktok.com/transparency/en/recommendation-system
  - Hashtags appear as a video signal ("The hashtags associated with the video."). Captions are not mentioned on that page. The page does not describe how new videos are tested on a small audience.
  - "content created by an account aged under 16 is not eligible for recommendation to the FYF"; content "not suitable for a broad audience is made ineligible for recommendation."

**For You eligibility and profanity**
- TikTok Community Guidelines, "For You feed Eligibility Standards", released August 25, 2026, "Effective September 24, 2026." https://www.tiktok.com/community-guidelines/en/fyf-standards
  - "We make ineligible for the FYF certain content that may not be suitable for a broad audience."
  - Profanity, swearing, offensive language, AI-generated content, unoriginal content and low-quality content: not mentioned in the text we could retrieve. The page text we got did not include the list of ineligible categories (it points to "FYF Ineligible" sections elsewhere), so a profanity rule inside those sections is not ruled out.
  - Ineligible content can still be found through search or the creator's account (search-result summary of the same standards, https://www.tiktok.com/safety/en/policies-and-engagement/fyf-standards). This matches the owner's pattern (search views, little For You), but nothing on any page says our videos are ineligible. We have no TikTok notice saying so.
- Creator Rewards Program Terms, "Last Update: Apr 2025". https://www.tiktok.com/legal/page/global/tiktok-creator-rewards-program-eea/en
  - Profanity: not mentioned. AI-generated content: not mentioned. For You feed: not mentioned. Search: not mentioned.
  - A qualifying video must be "one minute or longer", "reach at least 1,000 qualified views", be original ("original content and produced entirely by the creator and/or adds new ideas to preexisting content"), and not violate "these Creator Rewards Program Terms, the Terms of Service, Community Guidelines". Qualified views "are those that a user views for five seconds or more, are not marked by the viewer as 'not interested'".

**Creator Rewards: For You only? What does search value do?**
- TikTok Newsroom, "Introducing the New Creator Rewards Program", dated March 18, 2024. https://newsroom.tiktok.com/introducing-the-new-creator-rewards-program?lang=en
  - "Originality refers to quality content unique to the creator." "Play duration accounts for both watch time and finish rate." "Search value is a metric assigned to content based on popular search terms." "Audience engagement includes likes, comments and shares."
  - So the reward factors are originality, play duration, search value and engagement. Search value is one input to what a video earns, not a barrier.
- Reported but NOT confirmed by reading the page: TikTok Creator Academy articles (creator-academy/article/monetization-creativity-program-qualified-view and creator-rewards-program) are JavaScript pages, our fetch returned only the menu. Search-result summaries of them say qualified views "include Search views with watch times of at least 30 seconds", that qualified views only count from US, Mexico, Brazil, South Korea, Japan, Germany, UK and France, and that a video "should rack up at least 1,000 views on the For You feed". Treat as probable, not verified. If the 30-second rule is right, search views count toward the 1,000, so "Creator Rewards pays only on For You views" (the assumption in our notes) is not settled. Check the Creator Rewards tab in TikTok Studio.

**Hashtags, keywords, placement, generic tags**
- Reported by search summaries of the TikTok Creator Academy "Getting discovered with Search" article (page text could not be loaded, so UNVERIFIED): it recommends Creator Search Insights for keywords, warns that unrelated text "can get your video flagged for spam", and says overloading a caption with loosely related keywords or hashtags "can actually work against you." https://www.tiktok.com/creator-academy/article/Getting-discovered-with-Search
- No official TikTok page we could read gives a number of hashtags, says where to put keywords (caption, on-screen text, spoken words), or says whether #fyp or #learnontiktok helps or hurts. "Not found".
- Third-party blogs (UNVERIFIED, leads only): 3 to 5 relevant hashtags; keyword in caption, on-screen text and spoken audio; claims of "20 to 40% reach" from keywords with no source. Not used for any decision here.

**Why search views but little For You reach**
- Nothing official found on early-retention tests, follower mismatch or restored accounts. The only official mechanism is the general one: viewer actions (such as finishing a video) weigh more than device settings, and follower count is not a direct factor. Anything beyond that is inference.

## 2. Our own data

**What Metricool can and cannot see.** The TikTok posts connector has these fields: published time, URL, description, duration, views, likes, comments, shares, reach (TKPO11), engagement, full video watched rate (TKPO13), total time watched (TKPO14), average time watched (TKPO15), For You (TKPO16), Follow (TKPO17), Hashtag (TKPO18), Sound (TKPO19), Personal profile (TKPO20), Search (TKPO21), type. For all 78 posts pulled, reach, full video watched rate, total time watched, For You, Follow, Hashtag, Sound, Personal profile and Search came back null (also null on a one-day re-test with the metrics requested alone). So the search versus For You split, retention and reach cannot be measured from Metricool. Only the owner's TikTok Studio shows them.

**Pull.** 78 TikTok posts, 10/23 to 11/10 (the earliest post Metricool returned; its timestamps appear to be UTC). Total 33,240 views and 715 likes. Cross-check: Studio says 33,653 views for 76 posts over 28 days to 11/10 (MASTER_ORDERS), close enough. Median 226 views. Only 3 posts reached 1,000: bombardier beetle 5,980, house centipede 3,761, house centipede part 2 1,900. Those 3 hold 35% of all views.

**Top quartile (3rd quartile cut 313 views, n = 20) against the rest (n = 58).** Caption openers were classified by me from the text: "search phrase first" means the caption opens with the plain phrase people type (for example "house centipede in bathroom:"), "hook first" means it opens with the fact.

| Measure | Top quartile (n=20) | Rest (n=58) |
|---|---|---|
| Median views | 615 | 208.5 |
| Search phrase opens the caption | 7 (35%) | 8 (14%) |
| Average hashtags | 4.35 | 4.52 |
| Under 60 s | 7 (35%) | 7 (12%) |
| House-creature topic | 9 (45%) | 21 (36%) |
| Like rate (likes / views) | 2.06% | 2.32% |

Other splits (all n shown, view medians):
- Caption opener: search first n=15, median 296; hook first n=63, median 218. 13 of the 15 search-first posts are house creatures, so opener and topic are mixed together. Inside house creatures of 60 s or more: search first n=7 (median 279) against hook first n=16 (median 227.5). Group of 7 is under the 8-post bar, so no claim.
- Hashtag count: 3 tags n=9 median 224; 4 tags n=32 median 222; 5 tags n=28 median 258; 6 tags n=9 median 214. No pattern.
- Length: 30 s or under n=13 median 301; over 30 s n=65 median 221. 64 of 78 posts are 60 s or longer (median 220.5).
- Topic: house creatures n=30 median 261; other animals n=48 median 211.5.
- Posts old enough to have settled (before 11/8 UTC, n=69): median 225. The recent 9 are not the cause of the low median.

**Reading.** The search-first opener sits about 80 views higher at the median (296 against 218), which is inside the noise on an account where three posts carry a third of the views and the same group is mostly house topics and 15 s loopers. The caption cannot be separated from topic and length with this sample. There is no hashtag-count effect and no like-rate gap. This agrees with TikTok's own framing: captions and hashtags are minor inputs. The three breakouts were all 60 s or longer on a creature topic (bombardier beetle, house centipede).

## Could not be measured
- Search versus For You views per post, reach, average watch time, finish rate, traffic by hashtag: all null in Metricool.
- Whether any post was made ineligible for For You (no notice on file; Studio would show it).
- Whether our 1-minute swearing cuts (spoken f-word, "f**k" on screen) are treated differently: no official text mentions profanity, and none of those cuts has posted yet. Compare their views against the clean cuts after a week.
- Whether search views count toward the 1,000 qualified views (see section 1).
- Anything about posts older than 10/23.

## Recommendation
**Caption and hashtag template: no change justified.** The current queue captions already follow the rules we can verify: a plain keyword phrase or the creature name in the caption and hashtags, 4 to 5 relevant hashtags (including #meatballmyths and #learnontiktok, no #fyp), an opinion prompt (stay or squish, yes or no), no "follow for part 2", no profanity. If a template is wanted in writing: [creature fact or search phrase, one fact line] + [opinion prompt] + [4 to 5 tags: creature, category, #meatballmyths, #learnontiktok].

Why not change them now: (a) the evidence cannot show a caption effect, (b) this week's swearing cuts launch at the same time, so a caption change would make any difference impossible to attribute, (c) captions are not what limits For You reach per the sources above.

**Single most valuable non-caption change.** Put the proven house-creature topics, not one-off animals, in every 12:00, 19:00 and 21:30 slot (this is already the standing order in MASTER_ORDERS), and read the Studio retention graph for the three breakouts against a median post to see where viewers leave. Basis: the three breakouts are all house or bug topics, house topics have a higher median (261 against 211.5, n=30 and 48, small), and TikTok names finishing a video as a strong signal. The queue below is 13 of 27 non-house animals, 1 borderline. This is inference from small numbers, not proof.

**Small hygiene flags (not for reach).** 11/13 19:00 silverfish carries #booktok, a different community's tag, with the Creator Academy spam warning in mind (UNVERIFIED, minor). Nothing else in the queue captions needs editing.

## Queue check (TikTok, 11/11 to 11/18, non-draft only)
- 27 posts, not 19: three a day at 12:00, 19:00, 21:30 plus four 20:15 cuts (11/12, 11/14, 11/15, 11/18). 11/18 has no 21:30 post (12:00, 19:00 and 20:15 only). Drafts ignored (11/15 20:00 sea cucumber, 11/16 20:00 gila monster, 11/17 20:00 turkey vulture, 11/18 12:00 shrike and 20:00 bullet ant).
- Not house or backyard (13): 11/14 giant water bug 19:00 and honey badger 21:30; 11/15 skunk, polar bear, woodpecker; 11/16 naked mole rat, platypus, electric eel; 11/17 cassowary, wombat, hummingbird; 11/18 sea otter, Greenland shark. Borderline: 11/14 tardigrade ("moss on your roof"). Gecko 11/13 is fine.
- Repeats: house centipede TikTok 11/7, 11/12 21:30 and 11/15 20:15 (the 11/12 and 11/15 captions both say it eats roaches or drops a leg, different facts but the same creature three times in nine days); bed bugs 11/9 and 11/12. Same creature on YouTube the same day: silverfish and house fly 11/13, cellar spider 11/14.
- No exact duplicate captions.

## Scheduled TikTok posts: old and new captions
New caption equals the old one for every post (no change justified). Payloads with only `text` as the field to change are in `/tmp/claude-0/-home-user-skills/3d99d9ba-2ee2-5f03-bfdc-24a033361343/scratchpad/tt81-payloads.json`; because new_text equals old_text there is nothing to send.

| Date and time (ET) | Title | Old caption | New caption |
|---|---|---|---|
| 11/11 12:00 | The Fuzzy Fly on Your Bathroom Wall Grew Up in Your Drain 🚿 | the fuzzy little fly on my bathroom wall grew up inside my drain 🚿 and its babies breathe through a snorkel. What's the weirdest thing that ever came out of your drain? 👇 #meatballmyths #learnontiktok #animalfacts #drainfly | same as old |
| 11/11 19:00 | Your Roach Is Carrying 40 Babies 🪳 | the roach on your counter is carrying up to 40 babies 🪳 it fits in a 1/16 inch crack and eats soap, glue and hair. Have you ever seen one carrying its egg case? Where was it? 👇 #cockroach #roaches #bugsinyourhouse #meatballmyths #learnontiktok | same as old |
| 11/11 21:30 | Your Window Spider Has 8 Eyes on You 👀 | the little spider on your window has 8 eyes and it's watching you 👀 no web, it stalks and pounces. Do you let it stay or jar it outside? 🕷️ stay / 🫙 jar 👇 #jumpingspider #spiders #bugsinyourhouse #meatballmyths #learnontiktok | same as old |
| 11/12 12:00 | The Moth in Your Kitchen Isn't Eating Your Cereal. Its Babies Are 🥣 | the moth flying around my kitchen isn't the one eating my cereal 🥣 its caterpillars are, and they can chew through plastic bags. What's the worst thing you've found in your pantry? 👇 #meatballmyths #learnontiktok #animalfacts #pantrymoth | same as old |
| 11/12 19:00 | Bed Bugs Numb You So You Don't Feel Them 🛏️ | bed bugs are apple-seed size and hide in your mattress seams 🛏️ they numb you so you don't feel a thing, and they're not known to spread disease. Would you still sleep in that bed tonight? yes or no 👇 #bedbugs #bugsinyourbed #bugsinyourhouse #meatballmyths #learnontiktok | same as old |
| 11/12 20:15 | Wolf Spider, Stink Bug, Earwig: Stay or Squish? 5 House Bugs | wolf spider, stink bug, earwig, carpenter ant, camel cricket 🪲 which house bugs should stay and which should go? Wolf spider, earwig and camel cricket: stay. Stink bug and carpenter ant: out. Which one is in YOUR house? 🕷️ stay or 👟 squish? #bugsinhouse #wolfspider #stinkbug #learnontiktok #meatballmyths | same as old |
| 11/12 21:30 | Don't Squish the 30-Legged Bug in Your Bathroom 🐛 | there's a 30-legged bug in your bathroom and you should NOT squish it 🐛 it eats your roaches, even bed bugs, and it can drop a leg to escape and grow it back. Be honest: what did you do the last time one ran across your floor? 👇 #housecentipede #centipede #bugsinyourhouse #meatballmyths #learnontiktok | same as old |
| 11/13 12:00 | The Lizard on Your Ceiling Can't Blink, So It Licks Its Eyes 🦎 | the lizard on my ceiling can't blink so it licks its own eyeballs 🦎 and its toes stick with no glue at all. Would you let one live in your house? 🦎 yes / 🚪 no #meatballmyths #learnontiktok #animalfacts #housegecko | same as old |
| 11/13 19:00 | A Silverfish Is Eating Your Book 📚 | a silverfish is eating your book 📚 it eats glue, paper and cereal, can go months without food, and its family is older than the dinosaurs. What's the oldest book in your house? 👇 #silverfish #bugsinyourhouse #booktok #meatballmyths #learnontiktok | same as old |
| 11/13 21:30 | That Fly Is Tasting Your Sandwich With Its Feet 🪰 | that fly is tasting your sandwich with its feet 🪰 then it turns your food to soup with its spit. What's the grossest place you've watched a fly land right before your food? 👇 #housefly #flies #bugsinyourhouse #meatballmyths #learnontiktok | same as old |
| 11/14 12:00 | The Moss on Your Roof Hides an Animal That Survived Outer Space 🐻 | the moss on my roof is full of tiny animals that survived outer space 🐻🚀 one came back to life after 30 years frozen. Would you look at your moss under a microscope? 🔬 yes / 🙅 no #meatballmyths #learnontiktok #animalfacts #tardigrade | same as old |
| 11/14 19:00 | This Bug Melts Its Prey From the Inside and Drinks It 🪲 | this bug melts its prey from the inside and drinks it 🫠 it eats turtles, snakes and ducklings and they call it the toe biter. Would you eat one? 🍽️ yes / 🤢 never / 🦶 it'd eat me first  #meatballmyths #learnontiktok #giantwaterbug #insects #animalfacts | same as old |
| 11/14 20:15 | Cellar Spider in Your Corner: What It Eats, and Is It Venomous? | cellar spider in the corner of your ceiling 🕷️ In one English shed, all 102 leftovers in its webs were spiders, and it has been recorded eating giant house spiders. Stay or squish? 🕷️✅ or 👟💥 #cellarspider #spiderinhouse #learnontiktok #thingslivinginyourhouse #meatballmyths | same as old |
| 11/14 21:30 | Grab a Honey Badger and It Turns Around Inside Its Own Skin 🦡 | grab a honey badger and it twists around inside its own skin to bite you 🦡 and it shrugs off bee stings. Would you try to keep one as a pet? 🦡 yes / 🏃 no way #meatballmyths #learnontiktok #honeybadger #animalfacts | same as old |
| 11/15 12:00 | A Skunk Can Hit You in the Face From 10 Feet Away 🦨 | a skunk can hit you in the face from 10 feet away 🦨 it has about a dozen shots and can aim backwards. Would you pet one? 🖐️ yes / 🏃 run / 🧼 only with a gallon of peroxide  #meatballmyths #learnontiktok #skunk #animalfacts | same as old |
| 11/15 19:00 | A Polar Bear's Fur Isn't White, and Its Skin Is Black 🐻‍❄️ | polar bear fur isn't actually white and the skin under it is black 🐻‍❄️ and one swam for nine days straight. Would you swim with one? 🐻‍❄️ yes / 🥶 no #meatballmyths #learnontiktok #polarbear #animalfacts | same as old |
| 11/15 20:15 | House Centipede: The Leg It Drops and Where It Hides | house centipede in your bathroom 🐛 it can drop a leg to escape and usually regrows it by its next molt. Seeing lots of them may mean you have lots of other bugs. Stay or squish? 🐛✅ or 👟💥 #housecentipede #bugsinhouse #learnontiktok #thingslivinginyourhouse #meatballmyths | same as old |
| 11/15 21:30 | A Woodpecker Slams Its Face Into Wood Up to 20 Times a Second 🪵 | a woodpecker slams its face into wood up to 20 times a second 🪵 and its tongue wraps around its skull. Would you want one drumming outside your window at 6am? 🥁 yes / 😴 no / 🪵 only on the neighbor's house  #meatballmyths #learnontiktok #woodpecker #birds #animalfacts | same as old |
| 11/16 12:00 | A Naked Mole Rat Can Last 18 Minutes Without Any Oxygen 🐀 | a naked mole rat survived 18 minutes with zero oxygen 🐀 and it can live over 30 years. Would you hold one? 🤲 yes / 🙅 no #meatballmyths #learnontiktok #nakedmolerat #animalfacts | same as old |
| 11/16 19:00 | The Platypus Has No Stomach, and It Glows Under Blacklight 🦆 | the platypus has no stomach, lays eggs, and glows under a blacklight 🦆 and the males are venomous. Would you pet one? 🤚 yes / ☠️ no #meatballmyths #learnontiktok #platypus #animalfacts | same as old |
| 11/16 21:30 | The Electric Eel Isn't an Eel, and It Can Hit 860 Volts ⚡ | the electric eel isn't even an eel ⚡ one species can hit 860 volts, and it leaps out of the water to zap you. Would you swim in its river? 🏊 yes / ⚡ no way #meatballmyths #learnontiktok #electriceel #animalfacts | same as old |
| 11/17 12:00 | The Cassowary Has a 4-Inch Dagger on Each Foot 🦶 | the cassowary has a four inch dagger claw on each foot 🦶 and dad raises the babies alone. Would you walk through its rainforest? 🌴 yes / 🏃 no #meatballmyths #learnontiktok #cassowary #animalfacts | same as old |
| 11/17 19:00 | Wombats Poop Cubes, Up to 100 a Night 🟫 | wombats poop cubes, up to 100 a night 🟫 and their pouch opens backwards. Would you want one as a neighbor? 🏡 yes / 🙅 no #meatballmyths #learnontiktok #wombat #animalfacts | same as old |
| 11/17 21:30 | A Hummingbird's Heart Can Beat Over 1,200 Times a Minute 🐦 | a hummingbird's heart can beat over 1,200 times a minute 🐦 and it's the only bird that can really fly backwards. Would you hand-feed one? 🌺 yes / 😳 too fast #meatballmyths #learnontiktok #hummingbird #animalfacts | same as old |
| 11/18 12:00 | Sea Otters Have a Skin Pocket for Their Favorite Rock 🦦 | sea otters keep their favorite rock in a skin pocket under their arm 🦦 and they have the thickest fur of any animal. Would you share your snacks with one? 🐚 yes / 🙅 mine #meatballmyths #learnontiktok #seaotter #animalfacts | same as old |
| 11/18 19:00 | Some Greenland Sharks Alive Today Were Born Before the USA Existed 🦈 | some Greenland sharks swimming right now were born before the USA existed 🦈 they grow about 1 cm a year and might live 400 years. Would you want to live that long? ⏳ yes / 🙅 no #meatballmyths #learnontiktok #greenlandshark #animalfacts | same as old |
| 11/18 20:15 | Bugs in Your Christmas Tree: Mantis Egg Case and Fake Ticks | bugs in your christmas tree 🎄 check for a toasted-marshmallow blob: a praying mantis egg case with about 100 to several hundred eggs. Clip the twig and tuck it into an evergreen outside, never spray the tree. Will you check yours? ✅ or ❌ #christmastree #prayingmantis #bugsinhouse #learnontiktok #meatballmyths | same as old |
