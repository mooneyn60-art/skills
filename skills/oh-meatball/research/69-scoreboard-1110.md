# 69 · Performance scoreboard (2026-11-10, 10:15 ET)

Read-only research. Nothing was scheduled, posted or edited. Sources: Windsor.ai YouTube connector (account 34639), Metricool brand 7521392 (YouTube and TikTok analytics), and `data/posted.csv` for style labels only. Joined rows: `research/data/69-youtube.csv` (74 rows) and `research/data/69-tiktok.csv` (75 rows). "†" marks any group resting on fewer than 5 videos.

## Read this first: what the data can and cannot say
- **Public view counts are live (10:15 ET, 11/10). Retention numbers are not.** Windsor's per-video analytics end at 11/7 (the channel's daily series stops there), and Metricool's YouTube per-video list stops at 11/4. So **every Short posted 11/8 or later has views and likes but no average view duration or % viewed** (7 Shorts). The Kill-or-Keep long-form shows 177 public views but only 22 in the analytics window, so its retention rests on 22 views.
- **YouTube retention curves are not exposed.** Windsor's YouTube field list has no `audienceWatchRatio`, `elapsedVideoTimeRatio` or `relativeRetentionPerformance`, no thumbnail impressions, no impression click-through rate, and no "stayed to watch" number. It does expose `average_view_duration`, `average_view_percentage`, `estimated_minutes_watched`, `engaged_views`, `subscribers_gained`, and traffic source (channel-level only: it cannot be combined with `video`). So there is no per-video curve and no timestamp of steepest drop for any video.
- **TikTok retention is not available.** Metricool returns `null` for reach, full-video-watched rate, total and average time watched, and For You share on all 75 posts (the columns exist in the CSV, empty). Windsor has only the YouTube connector. TikTok below is views, likes, comments, shares and duration only.
- vidIQ and Higgsfield were not used (credits).
- **Average % viewed** is YouTube's own `average_view_percentage` (Windsor). The CSV also carries `avd_over_len_pct` (average view duration / length) as a cross-check; they agree within a few points and differ mostly through rounded lengths. Values above 100% mean viewers loop or rewatch.
- **Views** are YouTube's current public lifetime count. **Likes** are lifetime. **Comments and shares** come from the analytics window (through 11/7) and are blank for the newest videos; lifetime comment count is 1 on nearly every video (our own pinned comment), so comments are not a useful signal.
- Windows: "age" is hours from publish to 10:15 ET today. Grouped medians use only Shorts at least 48 h old (58 of 64 Shorts). Videos before 10/22 are left out (older, unrelated channel content, the "Oh Meatball" Shorts of 10/15-10/18 at under 40 views each, and deleted videos).
- Labels follow your rules from the CSV episode and file. Titles were matched exactly on YouTube; TikTok posts were matched to the CSV by schedule slot (all within 10 minutes, checked against the caption). **Not in the CSV (older channel work from 10/22-10/24 on YouTube, and 8 TikToks 10/23-10/24):** labeled "older experiments", family "other animal". Topic family rule: house creature = the "Things Living In Your House" and "Is This Spider Venomous?" house shows, tier and house lists, house pests; other animal = drawn-tt, animal-fact and myth work; case file / other = case files, conspiracies, the Azorian long-form and teaser. Two judgement calls: "This Spider Went to Space" (jumping spider, folder `real`) is "other animal"; the 3D loop and v6/banner formats all count as house creature.

---

## Retention (ranked by average % viewed)

### YouTube Shorts, top 15 and bottom 15 (min 100 views; n = 52 Shorts with analytics)
**Top 15**

| Avg % viewed | AVD s | Style | Topic / creature | Len s | Views | Title |
|---|---|---|---|---|---|---|
| 161 | 43.2 | older experiments | other animal | 25 | 1,223 | I Poked a Honey Badger 🦡 (Would Meatball Survive?) |
| 149 | 25.0 | drawn v6 | dust mites | 16 | 1,948 | Your Bed Mites Die at 130°F 😬 (Things Living In Your H… |
| 122 | 19.3 | drawn banner (older) | house centipede | 15 | 1,129 | Turn On Your Bathroom Light at 3 A.M. 🐛 (Things Living… |
| 120 | 29.3 | older experiments | other animal | 22 | 1,214 | Do Elephants Drink Through Their Trunks Like a Straw? 🐘 |
| 103 | 25.2 | drawn banner (older) | dust mites | 23 | 1,646 | Millions of Mites Can Live in Your Mattress 😬 (Things … |
| 99 | 17.2 | drawn v6 | house spider | 16 | 1,078 | 2 Spiders in Your House to Fear 🕷️ (Is This Spider Ven… |
| 95 | 34.4 | older experiments | other animal | 34 | 411 | Can Owls REALLY Spin Their Heads 360°? 🦉 TRUE or FALSE |
| 94 | 19.6 | older experiments | other animal | 20 | 2,363 | Are Daddy Longlegs the Most Venomous Spiders? 🕷️ |
| 93 | 18.4 | 3D explainer | house centipede | 19 | 1,158 | 30 Legs in Your Bathroom 🐛 (Things Living In Your Hous… |
| 92 | 24.5 | older experiments | other animal | 23 | 1,267 | This Spider Hunts Other Spiders 🕷️ (Meatball vs Spider… |
| 92 | 14.2 | drawn banner (older) | house centipede | 15 | 1,325 | Never Squish the 30-Legged Bug in Your House 🐛 (Things… |
| 89 | 16.6 | drawn v6 | pillbug | 17 | 1,214 | 14 Legs in Your Basement 🦀 (Things Living In Your Hous… |
| 83 | 14.7 | drawn v6 | cockroach | 16 | 1,343 | 30K Roaches in Your Kitchen 🪳 (Things Living In Your H… |
| 82 | 14.4 | drawn v6 | house centipede | 16 | 1,158 | 150 Babies in Your Bathroom 🐛 (Things Living In Your H… |
| 82 | 14.5 | drawn banner (older) | bed bugs | 16 | 1,143 | Bed Bugs Drink Your Blood While You Sleep 🩸 (Things Li… |

**Common thread (top 15):** median length 17 s (bottom 15: 28 s). 10 of the 15 are house creatures, and all 10 of those are 15-23 s (the Things Living In Your House #N format); five rows are above 100% (honey badger 161%, bed mites 149%, bathroom light 122%, elephant straw 120%, mattress mites 103%), meaning viewers loop. Five of the 15 are older-experiment animal Shorts at 20-34 s. Median views of the top 15 is 1,214 against 936 for the bottom 15.

**Bottom 15**

| Avg % viewed | AVD s | Style | Topic / creature | Len s | Views | Title |
|---|---|---|---|---|---|---|
| 29 | 26.2 | older experiments | other animal | 88 | 285 | Disney Lied To You About Lemmings 😱 TRUE or FALSE? |
| 37 | 13.3 | drawn other-animal | other animal | 30 | 936 | This Animal Fakes Its Own Death and Smells Like a Corp… |
| 37 | 12.5 | drawn other-animal | other animal | 30 | 1,016 | This Caterpillar Turns Itself Into a Fake Snake 🐍 |
| 47 | 12.0 | older experiments | case file / other | 23 | 169 | The Dancing Plague of 1518 Was REAL 🔍 |
| 48 | 25.4 | older experiments | other animal | 49 | 574 | TRUE or FALSE: Ostriches Bury Their Heads in the Sand?… |
| 48 | 12.7 | older experiments | other animal | 23 | 967 | Yes, It Can Actually Rain Spiders 🕷️ (Meatball vs Spid… |
| 50 | 17.5 | older experiments | other animal | 29 | 896 | Sharks in the RIVER?! 🦈 TRUE or FALSE |
| 51 | 16.0 | drawn other-animal | other animal | 28 | 949 | An Owl Can Turn Its Head 270 Degrees Without Choking I… |
| 52 | 15.7 | older experiments | case file / other | 23 | 432 | Is the Bermuda Triangle Real? 🔍 Case #1 Meatball Inves… |
| 52 | 13.8 | older experiments | other animal | 23 | 1,024 | I Tried to Outsmart a Box Jellyfish 👀 (Would Meatball … |
| 55 | 13.8 | drawn banner (older) | jumping spider | 24 | 1,282 | The Spider on Your Window Is Watching You Back 👀 (Thin… |
| 55 | 17.2 | drawn banner (-cut) | stink bug | 28 | 989 | 26,205 Stink Bugs in One House 🪲 (Things Living In You… |
| 55 | 19.6 | older experiments | other animal | 29 | 665 | Cartoons Lied To You About Porcupines 🦔 TRUE or FALSE? |
| 55 | 15.8 | older experiments | other animal | 25 | 1,254 | I Tried to Befriend a Cassowary 🦶 (Would Meatball Surv… |
| 58 | 13.7 | older experiments | jumping spider | 19 | 850 | This Spider Went to Space and Kept Hunting (Is This Sp… |

**Common thread (bottom 15):** 14 of 15 are 23 s or longer (one is 88 s); 13 are other-animal or case-file topics. The drawn other-animal Shorts (opossum, caterpillar, owl) hold 37-51% at 28-30 s, and the TRUE or FALSE and case-file Shorts sit at 29-52%. The only two house Shorts in the list are the window jumping spider (55%, 24 s) and the stink bug cut (55%, 28 s).

### Grouped median average % viewed (Shorts at least 48 h old, at least 100 views; full tables with views are in section A)
| Group | n | Median avg % viewed |
|---|---|---|
| drawn v6 | 6 | 86.1 |
| drawn banner (older) | 11 | 75.3 |
| 3D explainer | 5 | 75.1 |
| older experiments | 24 | 62.2 |
| drawn banner (-cut) | 1 † | 55.1 |
| drawn other-animal | 5 | 51.0 |
| House creature | 24 | 77.3 |
| Other animal | 26 | 61.9 |
| Case file / other | 2 † | 49.2 |
| 11-20 s | 19 | 81.8 |
| 21-35 s | 30 | 61.2 |
| >35 s | 3 † | 48.2 |
| <=10 s | 0 | (the one 8 s Shorts loop is 0 h old) |

Style, family and length are tangled together (the 11-20 s Shorts are nearly all the newer house format), so these are descriptions, not separate effects.

### Do higher % viewed and more views go together here?
Spearman rank correlation of average % viewed with lifetime views, Shorts at least 48 h old with at least 100 views: **rho = 0.54 (n = 52)**. By family: house creature 0.41 (n = 24), other animal 0.26 (n = 26). Among Shorts with 900+ views: 0.63 (n = 35). Shorts at 75% viewed or more: median 1,214 views (n = 21); below 75%: median 936 (n = 31). Average view duration in seconds versus views: rho = 0.03 (n = 52), so views here track the percentage, not the seconds. Caveat: 37 of 58 Shorts sit between 850 and 2,000 views, so many ranks are close ties, and the correlation is partly the case-file and skin-topic flops pulling both numbers down.

### Long-forms (10 videos; views in the analytics window; retention from Windsor)
Retention curves are not available (see above), so I cannot give timestamps of drops or flat stretches. What exists is average duration and % viewed. Windsor figures for Kill-or-Keep rest on 22 views and 3 other long-forms have 2-5 views (†).

**Ranked by average % viewed**

| Published ET | Age h | Title | Len | Views (public) | Views in analytics | Watch min | AVD | Avg % viewed | Avg min watched / view | Likes | Cmts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-27 14:02 | 333 | Conspiracy Theories That Turned Out To Be TRUE | 5:40 | 5 | 5 | 7 | 3:30 | 68.9 | 3.50 | 1 | 0 |
| 11-05 17:04 | 113 | Why the CIA Says "We Can Neither Confirm Nor Deny" | 8:38 | 3 | 2 | 8 | 4:00 | 51.3 | 4.00 | 0 | 0 |
| 10-22 10:32 | 457 | Everything You Know About Animals Is WRONG | 2:15 | 43 | 43 | 22 | 0:52 | 41.8 | 0.88 | 2 | 1 |
| 11-07 08:04 | 74 | 3 Bugs in Your House You Should Never Kill (And 4 You Mus… | 4:34 | 177 | 22 | 38 | 1:43 | 37.8 | 1.73 | 2 | 0 |
| 10-29 17:04 | 282 | 6 Creatures Living In Your House Right Now (You Never See… | 6:33 | 2 | 2 | 1 | 1:00 | 21.9 | 1.00 | 1 | 0 |
| 10-24 10:31 | 409 | How Wolves Became Dogs (The Funny History of Man's Best F… | 8:21 | 162 | 162 | 76 | 1:43 | 20.8 | 1.73 | 2 | 0 |
| 10-25 14:04 | 381 | Animals Thought Extinct Found Alive (One Was Hiding on a … | 7:04 | 125 | 124 | 114 | 1:05 | 15.7 | 1.09 | 2 | 0 |
| 10-26 14:01 | 357 | Weird Animal Facts You Didn't Know (3 Are Fake. Can You S… | 10:17 | 134 | 134 | 141 | 1:06 | 11.0 | 1.11 | 0 | 0 |
| 11-01 17:03 | 209 | I Ranked Every Creature Living In Your House From Harmles… | 8:58 | 5 | 4 | 3 | 0:45 | 9.9 | 0.75 | 0 | 0 |
| 10-23 11:10 | 432 | 12 Animal Myths You've Believed Your Whole Life (Disney F… | 11:18 | 5 | 5 | 1 | 0:12 | 4.8 | 0.20 | 0 | 0 |

**Ranked by average minutes watched per view**

| Published ET | Age h | Title | Len | Views (public) | Views in analytics | Watch min | AVD | Avg % viewed | Avg min watched / view | Likes | Cmts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-05 17:04 | 113 | Why the CIA Says "We Can Neither Confirm Nor Deny" | 8:38 | 3 | 2 | 8 | 4:00 | 51.3 | 4.00 | 0 | 0 |
| 10-27 14:02 | 333 | Conspiracy Theories That Turned Out To Be TRUE | 5:40 | 5 | 5 | 7 | 3:30 | 68.9 | 3.50 | 1 | 0 |
| 10-24 10:31 | 409 | How Wolves Became Dogs (The Funny History of Man's Best F… | 8:21 | 162 | 162 | 76 | 1:43 | 20.8 | 1.73 | 2 | 0 |
| 11-07 08:04 | 74 | 3 Bugs in Your House You Should Never Kill (And 4 You Mus… | 4:34 | 177 | 22 | 38 | 1:43 | 37.8 | 1.73 | 2 | 0 |
| 10-26 14:01 | 357 | Weird Animal Facts You Didn't Know (3 Are Fake. Can You S… | 10:17 | 134 | 134 | 141 | 1:06 | 11.0 | 1.11 | 0 | 0 |
| 10-25 14:04 | 381 | Animals Thought Extinct Found Alive (One Was Hiding on a … | 7:04 | 125 | 124 | 114 | 1:05 | 15.7 | 1.09 | 2 | 0 |
| 10-29 17:04 | 282 | 6 Creatures Living In Your House Right Now (You Never See… | 6:33 | 2 | 2 | 1 | 1:00 | 21.9 | 1.00 | 1 | 0 |
| 10-22 10:32 | 457 | Everything You Know About Animals Is WRONG | 2:15 | 43 | 43 | 22 | 0:52 | 41.8 | 0.88 | 2 | 1 |
| 11-01 17:03 | 209 | I Ranked Every Creature Living In Your House From Harmles… | 8:58 | 5 | 4 | 3 | 0:45 | 9.9 | 0.75 | 0 | 0 |
| 10-23 11:10 | 432 | 12 Animal Myths You've Believed Your Whole Life (Disney F… | 11:18 | 5 | 5 | 1 | 0:12 | 4.8 | 0.20 | 0 | 0 |

Reading it: the two highest percentages (conspiracy list, CIA case file) and the highest minutes per view come from videos with 2-5 views (†). Among long-forms with 20+ views, average minutes watched per view is 1.73 for Wolves and Kill-or-Keep, about 1.1 for Weird Animal Facts and Extinct Found Alive, and 0.88 for the 2:15 "Everything You Know". The only drop data on file is the earlier Studio read quoted in research 67 (Wolves 95% to 40% by 0:30, Weird Animal Facts 103% to 36% by 0:31, flat around 14-16% after 1:00); I could not refresh it here.

### TikTok retention
Not available: full-watched rate, average time watched and For You share are empty for all 75 posts in Metricool. Nothing was substituted.

---

## A. YouTube Shorts, per video (64 Shorts, newest first)
Views are public lifetime counts as of 10:15 ET 11/10. "AVD s" and "Avg % viewed" blank = newer than the analytics data (11/8 on) or under the data lag. Style and creature come from the CSV.

| Published ET | Age h | Title | Style | Creature / family | Len s | Views | AVD s | Avg % viewed | Likes | Cmts | Shares |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-10 10:10 | 0 | It Lives in Your Walls All Winter 🪲 (Things Living … | 3D loop | stink bug | 8 | 0 |  |  | 0 |  |  |
| 11-09 19:04 | 15 | 4-Inch Spider Legs on Your Floor 🕷️ (Things Living … | hook-test re-cut | giant house spider | 27 | 1,086 |  |  | 16 |  |  |
| 11-09 16:03 | 18 | 3 'Mommy Longlegs' in Your Home 🕷️ (Is This Spider … | drawn v6 | mommy longlegs | 16 | 1,193 |  |  | 2 |  |  |
| 11-09 10:05 | 24 | Your Kitchen: 200 Mouse Meals 🐭 (Things Living In Y… | drawn v6 | house mouse | 16 | 1,094 |  |  | 5 |  |  |
| 11-08 19:03 | 39 | The CIA Tried to Steal a Soviet Sub With a Giant Cl… | teaser (long-form) | case file / other | 32 | 76 |  |  | 2 |  |  |
| 11-08 14:03 | 44 | 1 Fake Bug in Your Basement 🕷️ (Things Living In Yo… | drawn v6 | cellar spider / daddy longlegs | 16 | 1,137 |  |  | 5 |  |  |
| 11-08 08:03 | 50 | 100 Feet a Night to Your Bed 🩸 (Things Living In Yo… | drawn v6 | bed bugs | 16 | 1,783 |  |  | 12 |  |  |
| 11-07 19:03 | 63 | 26,205 Stink Bugs in One House 🪲 (Things Living In … | drawn banner (-cut) | stink bug | 28 | 989 | 17.2 | 55.1 | 21 | 0 | 0 |
| 11-07 14:03 | 68 | Your Bed Mites Die at 130°F 😬 (Things Living In You… | drawn v6 | dust mites | 16 | 1,948 | 25.0 | 149.2 | 19 | 0 | 0 |
| 11-07 10:03 | 72 | 30K Roaches in Your Kitchen 🪳 (Things Living In You… | drawn v6 | cockroach | 16 | 1,343 | 14.7 | 82.8 | 8 | 0 | 0 |
| 11-06 19:04 | 87 | 8 Legs Live In Your Pillow 😬 (Things Living In Your… | 3D explainer | dust mites | 20 | 462 | 15.2 | 66.3 | 11 | 0 | 0 |
| 11-06 16:03 | 90 | 40x Jumps From Your Window 🕷️ (Things Living In You… | drawn v6 | jumping spider | 17 | 1,759 | 14.7 | 79.0 | 15 | 0 | 0 |
| 11-06 10:06 | 96 | 150 Babies in Your Bathroom 🐛 (Things Living In You… | drawn v6 | house centipede | 16 | 1,158 | 14.4 | 82.1 | 6 | 0 | 0 |
| 11-05 19:04 | 111 | Your Window Spider Has 8 Eyes 👀 (Things Living In Y… | 3D explainer | jumping spider | 20 | 355 | 17.1 | 69.5 | 4 | 0 | 0 |
| 11-05 10:06 | 120 | 14 Legs in Your Basement 🦀 (Things Living In Your H… | drawn v6 | pillbug | 17 | 1,214 | 16.6 | 89.4 | 7 | 0 | 0 |
| 11-04 21:03 | 133 | 3 Bites From Your Mattress 🩸 (Things Living In Your… | 3D explainer | bed bugs | 20 | 1,119 | 16.0 | 75.1 | 23 | 0 | 0 |
| 11-04 19:03 | 135 | Your Roach Has 40 Babies 🪳 (Things Living In Your H… | 3D explainer | cockroach | 20 | 1,984 | 16.3 | 75.4 | 16 | 0 | 0 |
| 11-04 16:03 | 138 | 2 Spiders in Your House to Fear 🕷️ (Is This Spider … | drawn v6 | house spider | 16 | 1,078 | 17.2 | 98.9 | 16 | 0 | 0 |
| 11-04 10:08 | 144 | 8 Weeks of Mites in Your Skin 🦠 (Things Living In Y… | drawn v6 | scabies mites | 16 | 55 | 9.5 | 91.8 | 3 | 0 | 0 |
| 11-03 21:03 | 157 | 30 Legs in Your Bathroom 🐛 (Things Living In Your H… | 3D explainer | house centipede | 19 | 1,158 | 18.4 | 92.9 | 13 | 0 | 0 |
| 11-03 16:03 | 162 | Turn On Your Bathroom Light at 3 A.M. 🐛 (Things Liv… | drawn banner (older) | house centipede | 15 | 1,129 | 19.3 | 121.6 | 16 | 1 | 0 |
| 11-03 12:03 | 166 | This Spider Hides in Your Shoes and Its Venom Can K… | drawn banner (older) | brown recluse | 17 | 46 | 20.8 | 146.3 | 2 | 0 | 0 |
| 11-02 16:02 | 186 | Never Squish the 30-Legged Bug in Your House 🐛 (Thi… | drawn banner (older) | house centipede | 15 | 1,325 | 14.2 | 91.5 | 12 | 0 | 1 |
| 11-02 12:07 | 190 | One Mouse Leaves 75 Droppings a Day in Your Kitchen… | drawn banner (older) | house mouse | 16 | 441 | 13.9 | 79.7 | 10 | 0 | 0 |
| 11-01 12:04 | 214 | This Bird Hides a 4-Inch Dagger Claw on Each Foot 🦶… | drawn other-animal | other animal | 19 | 432 | 13.8 | 62.1 | 8 | 0 | 0 |
| 10-31 12:04 | 239 | A Cockroach Can Live for Weeks Without Its Head 🪳 (… | drawn banner (older) | cockroach | 16 | 1,361 | 12.8 | 75.3 | 11 | 0 | 0 |
| 10-30 16:03 | 259 | This Spider Went to Space and Kept Hunting (Is This… | older experiments | jumping spider | 19 | 850 | 13.7 | 57.5 | 11 | 0 | 0 |
| 10-30 12:06 | 263 | Bed Bugs Drink Your Blood While You Sleep 🩸 (Things… | drawn banner (older) | bed bugs | 16 | 1,143 | 14.5 | 81.8 | 14 | 0 | 0 |
| 10-29 14:01 | 285 | The Spider on Your Window Is Watching You Back 👀 (T… | drawn banner (older) | jumping spider | 24 | 1,282 | 13.8 | 54.9 | 13 | 0 | 1 |
| 10-29 09:53 | 289 | This Beetle Gets Swallowed by a Toad and Makes It T… | drawn other-animal | other animal | 33 | 393 | 22.5 | 66.5 | 6 | 0 | 0 |
| 10-28 16:03 | 307 | The Spider in Your Basement Hunts Black Widows 🕷️ (… | drawn banner (older) | cellar spider / daddy longlegs | 24 | 1,099 | 14.8 | 59.3 | 15 | 0 | 0 |
| 10-28 15:02 | 308 | An Owl Can Turn Its Head 270 Degrees Without Chokin… | drawn other-animal | other animal | 28 | 949 | 16.0 | 51.0 | 10 | 0 | 0 |
| 10-28 13:06 | 310 | This Caterpillar Turns Itself Into a Fake Snake 🐍 | drawn other-animal | other animal | 30 | 1,016 | 12.5 | 37.3 | 11 | 0 | 0 |
| 10-28 09:31 | 314 | This Animal Fakes Its Own Death and Smells Like a C… | drawn other-animal | other animal | 30 | 936 | 13.3 | 37.1 | 13 | 0 | 0 |
| 10-27 21:02 | 326 | A Bug Older Than Dinosaurs Is Eating Your Books 📚 (… | drawn banner (older) | silverfish | 24 | 1,222 | 15.6 | 61.4 | 18 | 0 | 1 |
| 10-27 18:31 | 329 | Tiny Mites Live in Your Face Right Now 😳 (Things Li… | drawn banner (older) | face mites | 23 | 1,031 | 15.5 | 58.8 | 10 | 0 | 0 |
| 10-27 15:02 | 332 | Millions of Mites Can Live in Your Mattress 😬 (Thin… | drawn banner (older) | dust mites | 23 | 1,646 | 25.2 | 103.1 | 7 | 0 | 0 |
| 10-27 13:05 | 334 | House Flies Throw Up on Your Food 🪰 | older experiments | house fly | 21 | 1,100 | 17.2 | 75.6 | 4 | 0 | 0 |
| 10-27 12:45 | 334 | A 30-Legged Hunter Lives in Your House 🐛 (Things Li… | drawn banner (older) | house centipede | 24 | 1,073 | 17.7 | 70.4 | 8 | 0 | 0 |
| 10-27 09:31 | 338 | Is the Bermuda Triangle Real? 🔍 Case #1 Meatball In… | older experiments | case file / other | 23 | 432 | 15.7 | 51.7 | 5 | 0 | 0 |
| 10-26 20:31 | 351 | The Dancing Plague of 1518 Was REAL 🔍 | older experiments | case file / other | 23 | 169 | 12.0 | 46.7 | 2 | 0 | 0 |
| 10-26 19:31 | 352 | Yes, It Can Actually Rain Spiders 🕷️ (Meatball vs S… | older experiments | other animal | 23 | 967 | 12.7 | 48.2 | 10 | 0 | 0 |
| 10-26 17:31 | 354 | Operation Northwoods: The Conspiracy That Was TRUE 🔍 | older experiments | case file / other | 23 | 1 | 0.0 | 42.1 | 0 | 0 | 0 |
| 10-26 16:03 | 355 | Stonefish Are the Most Venomous Fish, and They Look… | older experiments | other animal | 21 | 1,043 | 15.1 | 65.0 | 9 | 0 | 0 |
| 10-26 15:02 | 356 | What REALLY Crashed at Roswell? 🔍 Meatball Investig… | older experiments | case file / other | 27 | 27 | 0.0 | 40.6 | 0 | 0 | 0 |
| 10-26 13:06 | 358 | This Beetle Survives Being Run Over by a Car 🪲 | older experiments | other animal | 24 | 1,035 | 18.4 | 65.4 | 8 | 0 | 0 |
| 10-26 11:07 | 360 | The US Planned to Nuke the Moon. It's REAL 🌕 Meatba… | older experiments | case file / other | 25 | 10 | 0.0 | 69.6 | 0 | 0 | 0 |
| 10-26 09:31 | 362 | Pufferfish Poison Is Deadlier Than Cyanide 🐡 | older experiments | other animal | 23 | 147 | 14.6 | 66.4 | 2 | 0 | 0 |
| 10-25 17:31 | 378 | This Bird Fakes a Broken Wing to Trick You 🐦 | older experiments | other animal | 23 | 515 | 17.4 | 62.7 | 9 | 0 | 1 |
| 10-25 16:02 | 379 | I Poked a Honey Badger 🦡 (Would Meatball Survive?) | older experiments | other animal | 25 | 1,223 | 43.2 | 161.2 | 13 | 0 | 0 |
| 10-25 15:04 | 380 | Ghost Crabs Growl With Teeth in Their Stomach 👻 | older experiments | other animal | 22 | 1,216 | 18.0 | 71.0 | 14 | 0 | 0 |
| 10-25 13:05 | 382 | I Tried to Outsmart a Box Jellyfish 👀 (Would Meatba… | older experiments | other animal | 23 | 1,024 | 13.8 | 52.2 | 3 | 0 | 0 |
| 10-25 11:31 | 384 | This Spider Hunts Other Spiders 🕷️ (Meatball vs Spi… | older experiments | other animal | 23 | 1,267 | 24.5 | 92.4 | 14 | 0 | 0 |
| 10-25 09:50 | 385 | I Tried to Befriend a Cassowary 🦶 (Would Meatball S… | older experiments | other animal | 25 | 1,254 | 15.8 | 55.3 | 14 | 0 | 0 |
| 10-24 16:02 | 403 | Are Daddy Longlegs the Most Venomous Spiders? 🕷️ | older experiments | other animal | 20 | 2,363 | 19.6 | 93.8 | 16 | 1 | 0 |
| 10-24 13:04 | 406 | Do Elephants Drink Through Their Trunks Like a Stra… | older experiments | other animal | 22 | 1,214 | 29.3 | 119.5 | 15 | 0 | 0 |
| 10-24 10:51 | 408 | Do Bulls Really Hate the Color Red? 🐂 TRUE or FALSE | older experiments | other animal | 43 | 396 | 28.2 | 61.6 | 5 | 1 | 0 |
| 10-23 16:03 | 427 | Disney Lied To You About Lemmings 😱 TRUE or FALSE? | older experiments | other animal | 88 | 285 | 26.2 | 28.5 | 3 | 0 | 0 |
| 10-23 13:04 | 430 | TRUE or FALSE: Goldfish Have a 3-Second Memory? 🤔 #… | older experiments | other animal | 33 | 1,107 | 22.9 | 61.0 | 10 | 0 | 0 |
| 10-23 10:55 | 432 | Can Owls REALLY Spin Their Heads 360°? 🦉 TRUE or FA… | older experiments | other animal | 34 | 411 | 34.4 | 95.2 | 3 | 1 | 0 |
| 10-22 19:31 | 448 | Cartoons Lied To You About Porcupines 🦔 TRUE or FAL… | older experiments | other animal | 29 | 665 | 19.6 | 55.2 | 4 | 0 | 0 |
| 10-22 18:15 | 449 | You STILL Believe This Camel Myth 💀 TRUE or FALSE? | older experiments | other animal | 27 | 228 | 19.2 | 63.1 | 2 | 0 | 0 |
| 10-22 16:56 | 450 | Sharks in the RIVER?! 🦈 TRUE or FALSE | older experiments | other animal | 29 | 896 | 17.5 | 49.9 | 12 | 0 | 0 |
| 10-22 12:07 | 455 | TRUE or FALSE: Ostriches Bury Their Heads in the Sa… | older experiments | other animal | 49 | 574 | 25.4 | 48.2 | 7 | 0 | 0 |

### Grouped medians (Shorts at least 48 h old: n = 58; each video's age is in the table above)
"n (APV)" counts Shorts with analytics and at least 100 views. Likes per 1,000 views use Shorts with 100+ views.

**By style label**

| style | n | Median views | Range | n (APV) | Median avg % viewed | Median AVD s | Median likes /1k views |
|---|---|---|---|---|---|---|---|
| drawn v6 | 8 | 1,278 | 55-1,948 | 6 | 86.1 | 15.7 | 6.7 |
| drawn banner (older) | 12 | 1,136 | 46-1,646 | 11 | 75.3 | 14.8 | 10.1 |
| 3D explainer | 5 | 1,119 | 355-1,984 | 5 | 75.1 | 16.3 | 11.3 |
| drawn banner (-cut) | 1 † | 989 | 989-989 | 1 † | 55.1 | 17.2 | 21.2 |
| drawn other-animal | 5 | 936 | 393-1,016 | 5 | 51.0 | 13.8 | 13.9 |
| older experiments | 27 | 850 | 1-2,363 | 24 | 62.2 | 18.2 | 10.8 |

"Older experiments" (27) is a mix: the 10/22-10/24 true-or-false and myth Shorts not in the CSV, plus Would Meatball Survive, Meatball vs Spiders, tiktok-pack, case files and the real-footage spider. The Azorian teaser (n = 1, 76 views, 32 s) and the 3D loop (n = 1, 0 h old) are left out of the style table.

**By topic family**

| topic family | n | Median views | Range | n (APV) | Median avg % viewed | Median AVD s | Median likes /1k views |
|---|---|---|---|---|---|---|---|
| house creature | 27 | 1,143 | 46-1,984 | 24 | 77.3 | 15.8 | 9.8 |
| other animal | 26 | 942 | 147-2,363 | 26 | 61.9 | 18.2 | 10.9 |
| case file / other | 5 | 27 | 1-432 | 2 † | 49.2 | 13.9 | 11.7 |

The 5 case-file Shorts are 1, 10, 27, 169 and 432 views. The 5 under 100 views among all 58 are: Northwoods (1), nuke the moon (10), Roswell (27), the shoes spider "venom can kill skin" (46) and "8 weeks of mites in your skin" (55); the last two are the skin-damage topics flagged in research 67.

**By length bucket** (<=10 s has no Short that is 48 h old)

| length bucket | n | Median views | Range | n (APV) | Median avg % viewed | Median AVD s | Median likes /1k views |
|---|---|---|---|---|---|---|---|
| 11-20 s | 22 | 1,150 | 46-2,363 | 19 | 81.8 | 15.2 | 10.5 |
| 21-35 s | 33 | 1,016 | 1-1,646 | 30 | 61.2 | 17.2 | 10.7 |
| >35 s | 3 † | 396 | 285-574 | 3 † | 48.2 | 26.2 | 12.2 |

**By post hour (ET, publish time)** (most hours have under 5 Shorts; treat as anecdote)

| post hour et | n | Median views | Range | n (APV) | Median avg % viewed | Median AVD s | Median likes /1k views |
|---|---|---|---|---|---|---|---|
| 8 | 1 † | 1,783 | 1,783-1,783 | 0 † |  |  | 6.7 |
| 9 | 5 | 432 | 147-1,254 | 5 | 55.3 | 15.7 | 13.6 |
| 10 | 6 | 784 | 55-1,343 | 5 | 82.8 | 16.6 | 6.0 |
| 11 | 2 † | 638 | 10-1,267 | 1 † | 92.4 | 24.5 | 11.0 |
| 12 | 7 | 574 | 46-1,361 | 6 | 72.9 | 14.2 | 12.2 |
| 13 | 6 | 1,068 | 1,016-1,214 | 6 | 63.2 | 17.8 | 8.4 |
| 14 | 2 † | 1,615 | 1,282-1,948 | 2 † | 102.1 | 19.4 | 9.9 |
| 15 | 4 † | 1,082 | 27-1,646 | 3 † | 71.0 | 18.0 | 10.5 |
| 16 | 11 | 1,099 | 285-2,363 | 11 | 79.0 | 17.2 | 10.6 |
| 17 | 2 † | 258 | 1-515 | 1 † | 62.7 | 17.4 | 17.5 |
| 18 | 2 † | 630 | 228-1,031 | 2 † | 61.0 | 17.3 | 9.2 |
| 19 | 6 | 816 | 355-1,984 | 6 | 60.8 | 16.7 | 10.8 |
| 20 | 1 † | 169 | 169-169 | 1 † | 46.7 | 12.0 | 11.8 |
| 21 | 3 † | 1,158 | 1,119-1,222 | 3 † | 75.1 | 16.0 | 14.7 |

Slot detail: the five 3D explainers went up at 19:00 ET (three) and 21:00 ET (two: 11/3 and 11/4); their views were 1,984 (roach), 1,158 (centipede), 1,119 (bed bugs), 462 (dust mites) and 355 (jumping spider). All Shorts posted in the 19:00 and 21:00 hours: n = 9. The 10:00 slot is v6 on 11/4-11/7: 55, 1,214, 1,158, 1,343.

Subscribers gained, from Windsor (Shorts at least 48 h old with analytics, n = 57, 47 subscribers total over 50,363 views; n = 57 with analytics): house creature 27 per 27,342 views (n = 26, 1.0 per 1,000), other animal 20 per 22,382 (n = 26, 0.9), case file / other 0 per 639 (n = 5). By style: drawn banner 1.4 per 1,000 (n = 12), v6 0.6 (n = 7), 3D explainer 0.6 (n = 5), older experiments 0.6 (n = 27). These are tiny counts (1-4 per video); treat as direction only.

---

## B. Hook-test status (numbers and n, no verdict)
Live today, as of 10:15 ET:

| Item | Slot (ET) | Age | Len | Public views | Avg % viewed | Likes |
|---|---|---|---|---|---|---|
| Hook-test re-cut: giant house spider | Mon 11/9 19:04 | 15 h | 27 s | 1,086 | not yet | 16 |
| 3D loop: stink bug "It Lives in Your Walls All Winter" | Tue 11/10 10:10 | 5 min | 8 s | 0 | not yet | 0 |

Hook-test re-cuts live: **1 of 9** on YouTube (the other eight are scheduled 11/11-11/13: wolf spider, camel cricket, termite, false widow, carpenter ant, earwig, silverfish, house fly; the TikTok silverfish hook is 11/13 14:30). 3D loops live: **1** (clothes moth and fruit fly loops are 11/16-11/17). So there is no group to compare yet; these are single data points.

Where they sit against section A (Shorts at least 48 h old):
- Giant house spider: 1,086 views at 15 h, inside the house-creature range (median 1,143, n = 27, range 46-1,984) and below the v6 median (1,278, n = 8; 1,343 without the skin-topic flop). Its 27 s length is longer than the 16-17 s v6 Shorts. Likes per 1,000 views: 14.7 versus a house-creature median of 9.8. No retention or "stayed to watch" yet; Windsor's retention data for it will likely show up around 11/12-11/13 given the 2-3 day lag.
- Stink bug 3D loop: 0 views at 5 minutes, so nothing to compare. For length reference, the shortest live Short before it was 15 s.
- **3D explainers (already live, 5 on YouTube, 11/3-11/6):** median 1,119 views (range 355-1,984), median 75.1% viewed (range 66-93), median AVD 16.3 s. Against the house-creature median of 1,143 views and 77.3% viewed. Two of the five (jumping spider 355, dust mites 462) are among the lowest house-creature Shorts; only the two skin-topic flops (46, 55) and the house mouse banner Short (441) are in that range.
- **3D on TikTok (11/3):** the centipede doubling test (59 s) 447 views and the Meatball centipede explainer cut (64 s) 242 views, against 266 median views for drawn house TikToks at least 48 h old (n = 18). n = 2; the 11/11-11/13 3D TikTok test (roach, jumping spider, bed bugs, centipede, silverfish hook, house fly) has not started.
- v6 reference, for the A/B in research 68: median 1,278 views (n = 8), 86.1% viewed (n = 6); banner-style 1,136 views (n = 12), 75.3% (n = 11).

---

## C. Long-forms, per video (10 videos, newest first)
Views are public lifetime; "views in analytics" is what Windsor had through 11/7 (retention is computed on those).

| Published ET | Age h | Title | Len | Views (public) | Views in analytics | Watch min | AVD | Avg % viewed | Avg min watched / view | Likes | Cmts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-07 08:04 | 74 | 3 Bugs in Your House You Should Never Kill (And 4 You Mus… | 4:34 | 177 | 22 | 38 | 1:43 | 37.8 | 1.73 | 2 | 0 |
| 11-05 17:04 | 113 | Why the CIA Says "We Can Neither Confirm Nor Deny" | 8:38 | 3 | 2 | 8 | 4:00 | 51.3 | 4.00 | 0 | 0 |
| 11-01 17:03 | 209 | I Ranked Every Creature Living In Your House From Harmles… | 8:58 | 5 | 4 | 3 | 0:45 | 9.9 | 0.75 | 0 | 0 |
| 10-29 17:04 | 282 | 6 Creatures Living In Your House Right Now (You Never See… | 6:33 | 2 | 2 | 1 | 1:00 | 21.9 | 1.00 | 1 | 0 |
| 10-27 14:02 | 333 | Conspiracy Theories That Turned Out To Be TRUE | 5:40 | 5 | 5 | 7 | 3:30 | 68.9 | 3.50 | 1 | 0 |
| 10-26 14:01 | 357 | Weird Animal Facts You Didn't Know (3 Are Fake. Can You S… | 10:17 | 134 | 134 | 141 | 1:06 | 11.0 | 1.11 | 0 | 0 |
| 10-25 14:04 | 381 | Animals Thought Extinct Found Alive (One Was Hiding on a … | 7:04 | 125 | 124 | 114 | 1:05 | 15.7 | 1.09 | 2 | 0 |
| 10-24 10:31 | 409 | How Wolves Became Dogs (The Funny History of Man's Best F… | 8:21 | 162 | 162 | 76 | 1:43 | 20.8 | 1.73 | 2 | 0 |
| 10-23 11:10 | 432 | 12 Animal Myths You've Believed Your Whole Life (Disney F… | 11:18 | 5 | 5 | 1 | 0:12 | 4.8 | 0.20 | 0 | 0 |
| 10-22 10:32 | 457 | Everything You Know About Animals Is WRONG | 2:15 | 43 | 43 | 22 | 0:52 | 41.8 | 0.88 | 2 | 1 |

- **"3 Bugs in Your House You Should Never Kill (And 4 You Must)"** (11/7 08:04, 74 h old): 177 public views, the most of any long-form on the channel (next: Wolves 162, Weird Animal Facts 134, Extinct 125, all 14-17 days old). The two house long-forms before it got 2 and 5 views. Retention shown (1:43 average on a 4:34 video, 37.8%) rests on only the 22 views in the analytics window; about 155 views have come since 11/7 with no retention data. YouTube's traffic-source report cannot be split per video here, so I cannot confirm where the 177 came from. Channel-wide, Related video traffic is 291 views and 339 watch minutes (0.5% of views, 4.5% of minutes).
- The other recent long-forms: CIA "Neither Confirm Nor Deny" 3 views (113 h), house ranked list 5 views (209 h), 6 Creatures 2 views (282 h).

---

## D. TikTok @meatballmyths (75 posts, 10/23-11/9)
Metrics available: views, likes, comments, shares, duration. No reach, completion or For You share (see top). Total 31,093 views, median 225 per post. Grouped medians use posts at least 48 h old (n = 69). **63 of 75 posts (84%) are 60 s or longer** (27,370 views, median 218); the 12 under 60 s have median 290 (7 early 21-24 s tests on 10/25-10/26, four 15-16 s v6 cuts on 11/7-11/9, one 59 s 3D test). Posts 60 s and longer: house creature 22, median 242; other animal 35, median 216. Under 60 s: house creature 5, median 296; other animal 7, median 229. The under-60 s group is confounded by date (two different eras).

Three posts carry 37% of all views: bombardier beetle 5,972 (10/26), house centipede part 1 3,728 (10/27), house centipede part 2 1,686 (11/1). Nothing since 11/1 passes 760.

**By topic family**

| topic family | n | Median views | Range | Mean views | Median likes % of views |
|---|---|---|---|---|---|
| house creature | 23 | 252 | 135-3,728 | 488 | 2.7 |
| other animal | 40 | 222 | 123-5,972 | 431 | 1.7 |
| case file / other | 6 | 132 | 86-164 | 132 | 1.6 |

**By style (drawn vs 3D vs older experiments)**

| coarse | n | Median views | Range | Mean views | Median likes % of views |
|---|---|---|---|---|---|
| 3D | 2 † | 344 | 242-447 | 344 | 2.8 |
| drawn | 31 | 252 | 123-3,728 | 427 | 2.4 |
| older experiments | 36 | 208 | 86-5,972 | 426 | 1.5 |

Finer split:

| style | n | Median views | Range | Mean views | Median likes % of views |
|---|---|---|---|---|---|
| 3D TikTok test | 1 † | 447 | 447-447 | 447 | 1.8 |
| drawn v6 | 6 | 286 | 218-760 | 361 | 2.0 |
| drawn banner (older) | 12 | 258 | 135-3,728 | 651 | 2.8 |
| 3D TikTok cut (explainer) | 1 † | 242 | 242-242 | 242 | 3.7 |
| drawn other-animal | 13 | 208 | 123-573 | 250 | 2.4 |
| older experiments | 36 | 208 | 86-5,972 | 426 | 1.5 |

**By duration bucket**

| dur bucket | n | Median views | Range | Mean views | Median likes % of views |
|---|---|---|---|---|---|
| <=30 s | 9 | 296 | 181-510 | 303 | 1.6 |
| 31-59 s | 1 † | 447 | 447-447 | 447 | 1.8 |
| 60-75 s | 45 | 218 | 86-5,972 | 491 | 2.2 |
| >75 s | 14 | 226 | 155-679 | 284 | 1.6 |

**By post hour (ET, nearest hour; most hours under 5)**

| post hour et | n | Median views | Range | Mean views | Median likes % of views |
|---|---|---|---|---|---|
| 10 | 5 | 670 | 212-5,972 | 1,615 | 0.7 |
| 11 | 2 † | 416 | 154-679 | 416 | 1.6 |
| 12 | 15 | 229 | 123-573 | 269 | 2.4 |
| 13 | 2 † | 140 | 125-155 | 140 | 2.5 |
| 14 | 3 † | 301 | 301-3,728 | 1,443 | 1.3 |
| 15 | 12 | 244 | 135-760 | 278 | 2.2 |
| 17 | 14 | 246 | 86-447 | 262 | 1.9 |
| 18 | 4 † | 182 | 162-224 | 188 | 1.5 |
| 19 | 5 | 222 | 134-1,686 | 551 | 2.3 |
| 20 | 3 † | 193 | 181-242 | 205 | 2.8 |
| 21 | 1 † | 164 | 164-164 | 164 | 0.6 |
| 22 | 2 † | 141 | 128-154 | 141 | 1.8 |
| 23 | 1 † | 131 | 131-131 | 131 | 0.8 |

**Every post, newest first**

| Published ET | Title / caption | Style | Family | Creature | Dur s | Views | Likes | Cmts | Shares |
|---|---|---|---|---|---|---|---|---|---|
| 11-09 17:02 | Your Kitchen: 200 Mouse Meals 🐭 | drawn v6 | house creature | house mouse | 15 | 284 | 9 | 0 | 0 |
| 11-09 14:32 | 1 Fake Bug in Your Basement 🕷️ | drawn v6 | house creature | cellar spider / daddy longlegs | 15 | 265 | 8 | 0 | 0 |
| 11-09 12:03 | Bed Bugs Crawl 100 Feet a Night to Reach Your Bed… | drawn v6 | house creature | bed bugs | 63 | 206 | 2 | 0 | 0 |
| 11-08 17:02 | This Fuzzy Ant Is Actually a Wasp Called the Cow … | drawn other-animal | other animal |  | 69 | 698 | 49 | 1 | 1 |
| 11-08 14:31 | The Tiny Beetle on Your Window Has Babies Eating … | drawn banner (older) | house creature | carpet beetle | 64 | 176 | 4 | 0 | 0 |
| 11-08 12:05 | This Fish Latches On to Other Fish and Drinks The… | drawn other-animal | other animal |  | 73 | 216 | 5 | 2 | 0 |
| 11-07 17:02 | 30K Roaches in Your Kitchen 🪳 | drawn v6 | house creature | cockroach | 15 | 365 | 7 | 0 | 1 |
| 11-07 14:31 | House Centipede: 150 Babies From One in Your Bath… | drawn v6 | house creature | house centipede | 64 | 760 | 7 | 0 | 0 |
| 11-07 12:04 | 40x Jumps From Your Window 🕷️ | drawn v6 | house creature | jumping spider | 16 | 296 | 6 | 0 | 0 |
| 11-06 17:02 | Is the Spider in Your House Venomous? 🕷️ | drawn v6 | house creature | house spider | 65 | 275 | 11 | 0 | 0 |
| 11-06 14:30 | This Bug's Bite Can Be Worse Than a Hornet Sting … | drawn other-animal | other animal |  | 76 | 309 | 3 | 0 | 0 |
| 11-06 12:10 | The Bug Named After Your Ear: 1 Ear Case in 10 Ce… | drawn v6 | house creature | earwig | 64 | 252 | 12 | 2 | 0 |
| 11-05 17:02 | You Can See This Frog's Guts. It Hides 90% of Its… | drawn other-animal | other animal |  | 61 | 169 | 1 | 0 | 0 |
| 11-05 14:31 | Tiny Animals That Kill 💀 | older experiments | other animal |  | 88 | 303 | 4 | 0 | 0 |
| 11-05 12:07 | Bugs Are Breeding in Your Old Books Every 25 Days… | drawn v6 | house creature | booklice | 62 | 218 | 4 | 0 | 0 |
| 11-04 17:02 | This Worm Can Drink 8x Its Weight in Your Blood 🩸 | drawn other-animal | other animal |  | 61 | 311 | 6 | 0 | 0 |
| 11-04 14:32 | Top 5 Deadliest Creatures In Your House 🕷️ | older experiments | house creature |  | 66 | 158 | 6 | 0 | 0 |
| 11-04 12:03 | Every Creature In Your House Ranked From Harmless… | older experiments | house creature |  | 183 | 182 | 8 | 0 | 0 |
| 11-03 20:03 | Meatball explains the 30-legged bug in your bathr… | 3D TikTok cut (explainer) | house creature | house centipede | 64 | 242 | 9 | 0 | 0 |
| 11-03 17:02 | What if a house centipede doubled every 2 seconds… | 3D TikTok test | house creature | house centipede | 59 | 447 | 8 | 1 | 0 |
| 11-03 14:30 | The Moth in Your Closet Never Eats. Its Babies Ea… | drawn banner (older) | house creature | clothes moth | 67 | 264 | 8 | 0 | 0 |
| 11-03 12:05 | This Tortoise Can Go a Whole Year Without Food or… | drawn other-animal | other animal |  | 62 | 573 | 23 | 0 | 0 |
| 11-02 21:02 | The US Really Built Bat Bombs 🦇 Meatball Investig… | older experiments | case file / other |  | 67 | 164 | 1 | 0 | 0 |
| 11-02 19:03 | Turn On Your Bathroom Light at 3 A.M. 🐛 (Part 3) | drawn banner (older) | house creature | house centipede | 62 | 203 | 7 | 0 | 1 |
| 11-02 17:02 | This Caterpillar Turns Itself Into a Fake Snake 🐍 | drawn other-animal | other animal |  | 72 | 204 | 9 | 0 | 0 |
| 11-02 14:30 | Grossest Things Living in Your House 🤢 | older experiments | house creature |  | 82 | 229 | 3 | 0 | 0 |
| 11-02 12:07 | One Mouse Leaves 75 Droppings a Day in Your Kitch… | drawn banner (older) | house creature | house mouse | 64 | 242 | 12 | 0 | 0 |
| 11-01 19:03 | Never Squish the 30-Legged Bug in Your House 🐛 (P… | drawn banner (older) | house creature | house centipede | 63 | 1686 | 75 | 7 | 5 |
| 11-01 17:01 | This Bird Falls Face-First Into the Swamp to Hunt… | drawn other-animal | other animal |  | 72 | 202 | 4 | 0 | 0 |
| 11-01 14:32 | This Bat Drinks So Much Blood It Pees While It Ea… | drawn other-animal | other animal |  | 75 | 258 | 9 | 0 | 1 |
| 11-01 12:04 | A Cockroach Can Live for Weeks Without Its Head 🪳… | drawn banner (older) | house creature | cockroach | 68 | 226 | 8 | 0 | 0 |
| 10-31 17:03 | Real Halloween Animals 🎃 | older experiments | other animal |  | 94 | 207 | 3 | 0 | 0 |
| 10-31 14:31 | A 1233 Pope's Letter Accused People of Worshippin… | drawn other-animal | other animal |  | 75 | 208 | 7 | 0 | 0 |
| 10-31 12:04 | Black Widow Venom Is 15 Times More Toxic Than a R… | drawn other-animal | other animal |  | 71 | 294 | 7 | 0 | 1 |
| 10-30 17:02 | This Lizard Drinks Water Through Its Feet 🦎 | drawn other-animal | other animal |  | 68 | 196 | 5 | 0 | 0 |
| 10-30 14:31 | Bed Bugs Drink Your Blood While You Sleep 🩸 (Part… | drawn banner (older) | house creature | bed bugs | 66 | 207 | 6 | 0 | 0 |
| 10-30 12:05 | An Owl Can Turn Its Head 270 Degrees Without Chok… | drawn other-animal | other animal |  | 72 | 181 | 6 | 0 | 0 |
| 10-29 17:03 | The Beetle That Makes Toads Throw It Up Alive (Bo… | drawn other-animal | other animal |  | 73 | 225 | 2 | 0 | 0 |
| 10-29 14:34 | The Spider on Your Window Is Watching You Back 👀 … | drawn banner (older) | house creature | jumping spider | 61 | 135 | 3 | 0 | 0 |
| 10-29 12:06 | This Animal Fakes Its Own Death and Smells Like a… | drawn other-animal | other animal |  | 73 | 123 | 2 | 0 | 0 |
| 10-28 17:02 | The Spider in Your Basement Hunts Black Widows 🕷️… | drawn banner (older) | house creature | cellar spider / daddy longlegs | 63 | 268 | 4 | 0 | 0 |
| 10-28 15:01 | Animals That Refuse to Die 💀 | older experiments | other animal |  | 101 | 284 | 5 | 0 | 0 |
| 10-28 13:34 | A Bug Older Than Dinosaurs Is Eating Your Books 📚… | drawn banner (older) | house creature | silverfish | 65 | 301 | 4 | 0 | 0 |
| 10-28 12:07 | Tiny Mites Live in Your Face Right Now 😳 (Part 3) | drawn banner (older) | house creature | face mites | 64 | 252 | 3 | 0 | 1 |
| 10-27 16:32 | Millions of Mites Can Live in Your Mattress 😬 (Pa… | drawn banner (older) | house creature | dust mites | 63 | 295 | 8 | 0 | 1 |
| 10-27 13:34 | A 30-Legged Hunter Lives in Your House 🐛 (Part 1) | drawn banner (older) | house creature | house centipede | 66 | 3728 | 61 | 2 | 2 |
| 10-27 12:07 | Moray Eels Have a Second Set of Jaws | older experiments | other animal |  | 62 | 201 | 2 | 0 | 0 |
| 10-27 11:09 | Is the Bermuda Triangle Real? 🔍 Case #1 | older experiments | case file / other |  | 62 | 154 | 3 | 0 | 0 |
| 10-27 09:31 | Horned Lizards Squirt Blood From Their Eyes | older experiments | other animal |  | 62 | 670 | 4 | 1 | 0 |
| 10-26 22:30 | The Ghost Ship Mary Celeste 👻 Case #12 | older experiments | case file / other |  | 61 | 131 | 1 | 0 | 0 |
| 10-26 21:31 | Yes, It Can Actually Rain Spiders 🕷️ (Meatball vs… | older experiments | other animal |  | 68 | 128 | 2 | 0 | 0 |
| 10-26 20:02 | Stonefish Are the Most Venomous Fish, and They Lo… | older experiments | other animal |  | 71 | 193 | 5 | 1 | 0 |
| 10-26 19:02 | The CIA Really Built a Spy Cat 🐈 Case #10 | older experiments | case file / other |  | 62 | 134 | 3 | 0 | 0 |
| 10-26 18:03 | This Beetle Survives Being Run Over by a Car | older experiments | other animal |  | 68 | 162 | 2 | 0 | 0 |
| 10-26 16:31 | The CIA Stole a Soviet Submarine 🔍 Case #8 | older experiments | case file / other |  | 64 | 86 | 1 | 0 | 0 |
| 10-26 13:07 | The Cardiff Giant: America's Greatest Hoax 🗿 Case… | older experiments | case file / other |  | 63 | 125 | 3 | 0 | 0 |
| 10-26 12:04 | Pufferfish Poison Is Deadlier Than Cyanide | older experiments | other animal |  | 22 | 229 | 7 | 0 | 0 |
| 10-26 09:32 | Bombardier Beetles Fire Boiling Spray From Their … | older experiments | other animal |  | 63 | 5972 | 90 | 0 | 3 |
| 10-25 21:30 | The Spider That Fishes for Moths 🎣 | older experiments | other animal |  | 73 | 154 | 3 | 0 | 0 |
| 10-25 20:02 | I Poked a Honey Badger 🦡 | older experiments | other animal |  | 24 | 181 | 5 | 0 | 0 |
| 10-25 19:03 | This Bird Fakes a Broken Wing to Trick You 🐦 | older experiments | other animal |  | 22 | 510 | 8 | 0 | 0 |
| 10-25 18:03 | I Tried to Outsmart a Box Jellyfish 👀 | older experiments | other animal |  | 22 | 224 | 2 | 0 | 0 |
| 10-25 16:31 | Ghost Crabs Growl With Teeth in Their Stomach 👻 | older experiments | other animal |  | 21 | 412 | 3 | 0 | 0 |
| 10-25 13:31 | This Spider Hunts Other Spiders 🕷️ (Meatball vs S… | older experiments | other animal |  | 22 | 301 | 4 | 0 | 0 |
| 10-25 12:05 | I Tried to Befriend a Cassowary 🦶 | older experiments | other animal |  | 24 | 209 | 3 | 0 | 0 |
| 10-25 09:50 | Tarantula Hawks Are Wasps That Hunt Tarantulas | older experiments | other animal |  | 62 | 940 | 7 | 0 | 1 |
| 10-24 19:04 | Part 1: Do You Really Swallow Spiders in Your Sle… | older experiments | other animal |  | 102 | 222 | 5 | 0 | 0 |
| 10-24 18:02 | Part 6: Are Sloths Really Lazy? | older experiments | other animal |  | 142 | 196 | 6 | 0 | 0 |
| 10-24 12:06 | Part 5: Do Hippos Really Sweat Blood? | older experiments | other animal |  | 89 | 558 | 4 | 0 | 1 |
| 10-24 10:40 | [caption not in CSV] elephant chameleon tf a | older experiments | other animal |  | 89 | 679 | 9 | 0 | 0 |
| 10-24 10:03 | [caption not in CSV] elephant chameleon tf b | older experiments | other animal |  | 89 | 279 | 8 | 0 | 0 |
| 10-23 18:03 | [caption not in CSV] porcupine tf | older experiments | other animal |  | 115 | 168 | 3 | 0 | 0 |
| 10-23 15:02 | [caption not in CSV] camel tf | older experiments | other animal |  | 66 | 221 | 5 | 0 | 0 |
| 10-23 12:58 | [caption not in CSV] jellyfish bear tf | older experiments | other animal |  | 111 | 155 | 4 | 0 | 0 |
| 10-23 09:47 | [caption not in CSV] lemmings tf | older experiments | other animal |  | 94 | 212 | 1 | 0 | 0 |

---

## E. Inventory gaps (house creatures, matched by creature keyword)
Source: titles live on each platform; file names from `posted.csv`.

**Live on TikTok, no YouTube Short**

| Creature | TikTok file (live) | TikTok views | Notes |
|---|---|---|---|
| booklice | `drawn-house/tt-booklice-v6.mp4` | 218 | no YouTube file in the CSV (a `yt-` version would need making) |
| carpet beetle | `drawn-house/tt-carpet-beetle.mp4` | 176 | no YouTube file in the CSV |
| clothes moth | `drawn-house/tt-clothes-moth-v4.mp4` | 264 | already scheduled: `sim3d/yt-clothesmoth-explainer.mp4` 11/16 10:00 and `yt-clothesmoth-loop.mp4` 11/17 10:00 |
| earwig | `drawn-house/tt-earwig-v6.mp4` | 252 | already scheduled: `hook-test/yt-earwig-hook.mp4` 11/12 19:00 |

Also scheduled on TikTok only, not yet live: fruit fly, drain fly, pantry moth, house gecko, tardigrade (`tt-*.mp4`, 11/10-11/14), none with a YouTube row in the CSV.

**Live on YouTube, no TikTok post**

| Creature | YouTube file (live) | YouTube views | Notes |
|---|---|---|---|
| pillbug | `drawn-house/yt-pillbug-v6.mp4` | 1,214 | no TikTok row |
| stink bug | `drawn-house/yt-stink-bug-cut.mp4` (989), `sim3d/yt-stinkbug-loop.mp4` (0, new) | | no TikTok row (`sim3d/yt-stinkbug-explainer.mp4` is a YouTube row, 11/16) |
| giant house spider | `hook-test/yt-giant-house-spider-hook.mp4` | 1,086 | no TikTok row |
| brown recluse | `drawn-house/yt-brown-recluse-v4.mp4` | 46 | skin-harm hook; flop on YouTube, so probably not a TikTok candidate as is |
| scabies mites | `drawn-house/yt-scabies-v6.mp4` | 55 | skin-harm topic; same caution |
| house fly | `tiktok-pack-01/short-housefly.mp4` | 1,100 | TikTok row exists for the 3D version: `sim3d/yt-housefly-explainer.mp4` 11/13 17:00 |
| mommy longlegs | `drawn-house/yt-mommy-longlegs-v6.mp4` | 1,193 | TikTok row exists: same file, today 11/10 14:30 (not posted yet) |

Everything else live on both: bed bugs, cellar spider / daddy longlegs, cockroach, dust mites, face mites, house centipede, house mouse, house spider, jumping spider, silverfish.

---

## F. Top 10 and bottom 10 (observations only)
Shorts lists use videos at least 48 h old; the TikTok lists use all 75 posts.

**YouTube, top 10 by views**

| Views | Published ET | Title | Style | Len s | Avg % viewed |
|---|---|---|---|---|---|
| 2,363 | 10-24 16:02 | Are Daddy Longlegs the Most Venomous Spiders? 🕷️ | older experiments | 20 | 93.8 |
| 1,984 | 11-04 19:03 | Your Roach Has 40 Babies 🪳 (Things Living In Your House #… | 3D explainer | 20 | 75.4 |
| 1,948 | 11-07 14:03 | Your Bed Mites Die at 130°F 😬 (Things Living In Your Hous… | drawn v6 | 16 | 149.2 |
| 1,783 | 11-08 08:03 | 100 Feet a Night to Your Bed 🩸 (Things Living In Your Hou… | drawn v6 | 16 |  |
| 1,759 | 11-06 16:03 | 40x Jumps From Your Window 🕷️ (Things Living In Your Hous… | drawn v6 | 17 | 79.0 |
| 1,646 | 10-27 15:02 | Millions of Mites Can Live in Your Mattress 😬 (Things Liv… | drawn banner (older) | 23 | 103.1 |
| 1,361 | 10-31 12:04 | A Cockroach Can Live for Weeks Without Its Head 🪳 (Things… | drawn banner (older) | 16 | 75.3 |
| 1,343 | 11-07 10:03 | 30K Roaches in Your Kitchen 🪳 (Things Living In Your Hous… | drawn v6 | 16 | 82.8 |
| 1,325 | 11-02 16:02 | Never Squish the 30-Legged Bug in Your House 🐛 (Things Li… | drawn banner (older) | 15 | 91.5 |
| 1,282 | 10-29 14:01 | The Spider on Your Window Is Watching You Back 👀 (Things … | drawn banner (older) | 24 | 54.9 |

Common thread: 9 of 10 are house-creature Shorts at 15-24 s from the numbered house format, with "your bed / window / kitchen / house" in the title and, in most, a number; four are v6; the roach 3D explainer is the one 3D entry; the one non-house entry is the older daddy-longlegs-venom Short (2,363).

**YouTube, bottom 10 by views**

| Views | Published ET | Title | Style | Len s | Avg % viewed |
|---|---|---|---|---|---|
| 1 | 10-26 17:31 | Operation Northwoods: The Conspiracy That Was TRUE 🔍 | older experiments | 23 | 42.1 |
| 10 | 10-26 11:07 | The US Planned to Nuke the Moon. It's REAL 🌕 Meatball Inv… | older experiments | 25 | 69.6 |
| 27 | 10-26 15:02 | What REALLY Crashed at Roswell? 🔍 Meatball Investigates | older experiments | 27 | 40.6 |
| 46 | 11-03 12:03 | This Spider Hides in Your Shoes and Its Venom Can Kill Sk… | drawn banner (older) | 17 | 146.3 |
| 55 | 11-04 10:08 | 8 Weeks of Mites in Your Skin 🦠 (Things Living In Your Ho… | drawn v6 | 16 | 91.8 |
| 147 | 10-26 09:31 | Pufferfish Poison Is Deadlier Than Cyanide 🐡 | older experiments | 23 | 66.4 |
| 169 | 10-26 20:31 | The Dancing Plague of 1518 Was REAL 🔍 | older experiments | 23 | 46.7 |
| 228 | 10-22 18:15 | You STILL Believe This Camel Myth 💀 TRUE or FALSE? | older experiments | 27 | 63.1 |
| 285 | 10-23 16:03 | Disney Lied To You About Lemmings 😱 TRUE or FALSE? | older experiments | 88 | 28.5 |
| 355 | 11-05 19:04 | Your Window Spider Has 8 Eyes 👀 (Things Living In Your Ho… | 3D explainer | 20 | 69.5 |

Common thread: 7 of 10 are older experiments (case files, history, true-or-false/myth, and the pufferfish fact); the other three are the two skin-harm house topics (46 and 55 views) and the 3D jumping-spider explainer (355).

**TikTok, top 10 by views**

| Views | Published ET | Title / caption | Style | Dur s | Likes |
|---|---|---|---|---|---|
| 5972 | 10-26 09:32 | Bombardier Beetles Fire Boiling Spray From Their Butts | older experiments | 63 | 90 |
| 3728 | 10-27 13:34 | A 30-Legged Hunter Lives in Your House 🐛 (Part 1) | drawn banner (older) | 66 | 61 |
| 1686 | 11-01 19:03 | Never Squish the 30-Legged Bug in Your House 🐛 (Part 2) | drawn banner (older) | 63 | 75 |
| 940 | 10-25 09:50 | Tarantula Hawks Are Wasps That Hunt Tarantulas | older experiments | 62 | 7 |
| 760 | 11-07 14:31 | House Centipede: 150 Babies From One in Your Bathroom 🐛 | drawn v6 | 64 | 7 |
| 698 | 11-08 17:02 | This Fuzzy Ant Is Actually a Wasp Called the Cow Kille… | drawn other-animal | 69 | 49 |
| 679 | 10-24 10:40 | [caption not in CSV] elephant chameleon tf a | older experiments | 89 | 9 |
| 670 | 10-27 09:31 | Horned Lizards Squirt Blood From Their Eyes | older experiments | 62 | 4 |
| 573 | 11-03 12:05 | This Tortoise Can Go a Whole Year Without Food or Wate… | drawn other-animal | 62 | 23 |
| 558 | 10-24 12:06 | Part 5: Do Hippos Really Sweat Blood? | older experiments | 89 | 4 |

Common thread: all 10 are 62-89 s; 6 of the 10 were posted 10/24-10/27; only three are house creatures and all three are house centipede (parts 1 and 2 and the v6 "150 Babies"); the rest are the bombardier beetle, tarantula hawk, velvet ant, horned lizard, tortoise and two true-or-false/myth quizzes.

**TikTok, bottom 10 by views**

| Views | Published ET | Title / caption | Style | Dur s | Likes |
|---|---|---|---|---|---|
| 86 | 10-26 16:31 | The CIA Stole a Soviet Submarine 🔍 Case #8 | older experiments | 64 | 1 |
| 123 | 10-29 12:06 | This Animal Fakes Its Own Death and Smells Like a Corp… | drawn other-animal | 73 | 2 |
| 125 | 10-26 13:07 | The Cardiff Giant: America's Greatest Hoax 🗿 Case #14 | older experiments | 63 | 3 |
| 128 | 10-26 21:31 | Yes, It Can Actually Rain Spiders 🕷️ (Meatball vs Spid… | older experiments | 68 | 2 |
| 131 | 10-26 22:30 | The Ghost Ship Mary Celeste 👻 Case #12 | older experiments | 61 | 1 |
| 134 | 10-26 19:02 | The CIA Really Built a Spy Cat 🐈 Case #10 | older experiments | 62 | 3 |
| 135 | 10-29 14:34 | The Spider on Your Window Is Watching You Back 👀 (Part… | drawn banner (older) | 61 | 3 |
| 154 | 10-27 11:09 | Is the Bermuda Triangle Real? 🔍 Case #1 | older experiments | 62 | 3 |
| 154 | 10-25 21:30 | The Spider That Fishes for Moths 🎣 | older experiments | 73 | 3 |
| 155 | 10-23 12:58 | [caption not in CSV] jellyfish bear tf | older experiments | 111 | 4 |

Common thread: all are 61-111 s; 5 of the 10 are case files (Azorian, Cardiff Giant, spy cat, Mary Celeste, Bermuda); the rest are the possum, rain spiders, bolas spider, the window jumping spider and a true-or-false quiz.

---

## G. Channel totals
- **Subscribers now:** 995 (Windsor snapshot 11/10; Metricool shows 993 on 11/10). 942 on 10/19 (Metricool), so +51 to +53 in 22 days. Channel-wide gained minus lost, 10/13-11/7: +64 gained, 19 lost, net +45 (1.1 gross per 1,000 views, 0.8 net).
- **Last 28 days (10/11-11/7, the latest complete analytics day):** 56,432 views and 7,567 watch minutes, **126.1 watch hours**. Daily views ranged from 707 (11/1) to 4,570 (11/7) over 10/30-11/7; the peaks were 7,097 on 10/25 and 6,269 on 10/27 (Metricool).
- **Shorts vs long-form (same window):** Shorts 55,880 views (99.1%), 7,136 min = 118.9 h (94.3%), 47 subscribers attributed; long-form 503 views (0.9%), 420 min = 7.0 h (5.6%), 1 subscriber attributed.
- **Traffic sources, 28 days (views, share of views, minutes):**

| Source | Views | Share of views | Watch minutes |
|---|---|---|---|
| Shorts feed | 52,058 | 92.3% | 6,560 |
| YouTube search | 3,301 | 5.9% | 483 |
| Channel pages | 307 | 0.5% | 50 |
| Related video | 291 | 0.5% | 339 |
| Other YouTube pages | 193 | 0.3% | 14 |
| Subscriber feed | 187 | 0.3% | 50 |
| Hashtags, sound page, playlists, external, notifications, other | 40 | 0.1% | 15 |

- The animal/house-bug Shorts began 10/22. Daily views were under 100 through 10/18 (about 330 in total on 10/11-10/18) and ~1,300-2,000 from 10/19, so the "28 days" is effectively the last three weeks.

---

## Findings (descriptive; none are verdicts)
1. 28 days: 56.4K views, 126 watch hours, 995 subscribers; Shorts are 99% of views and 94% of watch time, and the Shorts feed is 92% of views.
2. Shorts at 48 h+ cluster tightly: 37 of 58 sit between 850 and 2,000 views; the best is 2,363. Outcomes depend more on topic than on style so far.
3. House-creature Shorts: median 1,143 views (n = 27), 77% viewed; other animals 942 (n = 26), 62% viewed; case-file Shorts 27 (n = 5†).
4. v6 (1,278, n = 8) edges drawn banner (1,136, n = 12) and 3D explainer (1,119, n = 5), but the ranges overlap; 3D explainers range 355-1,984 and all went up at 19:00-21:00.
5. 11-20 s Shorts: median 81.8% viewed (n = 19); 21-35 s: 61.2% (n = 30); the top 15 by % viewed have a 17 s median length, the bottom 15 28 s.
6. % viewed and views move together modestly (Spearman 0.54, n = 52; 0.41 within house creatures); seconds watched do not (0.03).
7. The only sub-100-view Shorts are five: three case files and the two skin-harm house topics (46 and 55 views).
8. Hook test: 1 of 9 re-cuts live (giant house spider, 1,086 views at 15 h, inside the house range); the 3D loop is 5 minutes old; no retention numbers exist yet for either.
9. Long-forms: Kill-or-Keep is at 177 views after 74 h versus 2-5 for the two house long-forms before it; its 37.8% / 1:43 rests on 22 analytics views. Related-video traffic channel-wide is 0.5% of views but 4.5% of minutes.
10. TikTok: 75 posts, median 225 views; 84% are 60 s or longer; three posts hold 37% of views; house creature median 252 vs other animal 222 (n = 23 vs 40); nothing since 11/1 passes 760.
11. Gaps: booklice and carpet beetle have a TikTok file but no YouTube row; pillbug, stink bug, giant house spider, brown recluse and scabies are on YouTube without TikTok.
12. Not obtainable: YouTube retention curves, impressions/CTR, per-video traffic source, any TikTok retention or reach.
