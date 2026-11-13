# 100 Shorts: one table of every Short, and what goes with what

Run 11/12 about 23:40 ET (label: shorts). Table: `research/data/100-shorts-table.csv` (76 rows, one per public Short posted 10/22 to 11/12).

## Answer first
1. Views barely move with anything we choose. Among drawn and 3D bug and spider Shorts posted 10/27 to 11/09 (Windsor, n=39) the middle half is 850 to 1,283 views, and 59% sit between 900 and 1,400. Title number, hour, weekday, Shorts that day and the gap since the last Short all fail to separate views (every p above 0.09, every rank correlation under 0.25). "Your" in the headline shows a gap across all Shorts (1,150 against 873) but it is the same split as new drawn Shorts against the older ones, so it is not a separate effect.
2. The big gap is topic, and it is old news: house bug and spider Shorts median 1,145 to 1,146 views, other animals 474 (Windsor, 11/12). Engaged share 0.46 to 0.48 against 0.33, average % viewed 72 to 78 against 58.
3. Subscribers: 63 from 66 Shorts, 1.04 per 1,000 views (Windsor). That already meets the 1.0 target in the scorecard (the old "0.3" was a channel-wide number from a different window). Ten Shorts gave 33 of the 63. They follow likes (rank r 0.51), not average % viewed (0.01). 9 of the 10 are house bug or spider Shorts; 6 of 10 have "your" in the headline (the part before the series tag).
4. Decay: the median Short gets 72% of its views on day 0 and about 97% by day 2. Only 3.0% (middle half 1.8 to 3.7%) arrive after day 2 (observed only to day 5, so this is a floor). Search is the only slow earner: spider Shorts get 10.8% of their views from search against 3.6% for bugs (p 0.0014). The daddy longlegs Short still gets 10 to 20 views a day two weeks on.
5. Pets and survival cannot be judged yet. Pet n=3, all under 8 hours old. The cat sugar Short has 1,000 views at 7.6 hours and the moose 493 at 4.6 hours; the 9 bug and spider Shorts posted 11/10 to 11/12 have a median of 495 public views, so the new ones are level or ahead of the current bug days, not of the 1,150 bug median from before 11/10.

## Method and sources
- List and public views: `yt-dlp --flat-playlist -J` on the channel Shorts tab, 11/12 23:3x ET. 76 Shorts. Public counts above 1,000 are rounded to two digits.
- Windsor.ai, connector `youtube`, account 34639, one call for 2026-10-20 to 2026-11-13, fields video, video_title, published_at, creator_content_type, views, engaged_views, average_view_percentage, subscribers_gained, likes, comments, shares. No traffic_source. 66 of the 76 Shorts have rows. Columns that start `w_` come from this call. Windsor is 2 to 3 days behind, so Shorts posted 11/09 and 11/10 are short of their final count (mommy longlegs 1,415 in Windsor against 1,800 public). The 10 Shorts posted 11/11 and 11/12 have no Windsor row.
- Post time: Windsor `published_at` (UTC, changed to ET); for the 11/11 and 11/12 Shorts, `data/posted.csv`. The Joe Bartolozzi Shorts in the Windsor result are another channel's old rows with 0 views and are dropped.
- Show, style, jokes: my labels from the title and `posted.csv` episode. Style: drawn v6 = episode drawn-house (31), 3D explainer = sim3d (6), hook test (5), photo (1, the space spider), other (older) = the true or false, case file, drawn-tt and first-week Shorts (32), teaser (1). Jokes: "mild jokes" = the 11/11 roach crack and boxelder Shorts; "funnier" = the four 11/12 pet and survival Shorts; all other 70 are plain. None of the six joke Shorts has a Windsor row yet, so the joke effect is not measurable here.
- Length (s): `96-hold-joined.csv` (50), `69-youtube.csv` (14), ffprobe on files on disk (6). 6 blank. `length_source` says which.
- Hours since the previous Short and Shorts that day count public Shorts only, ET calendar day.
- Tests: difference of medians with a permutation p (5,000 shuffles), rank correlation with a permutation p (3,000 shuffles). Comparison set A = Shorts with Windsor rows posted by 11/09 (n=63). "Modern" set H = bug and spider Shorts in drawn v6, 3D or hook-test style (n=30). Set D = drawn v6 bug and spider (n=24).
- Comparisons run: 144 median tests (3 sets, 12 features, 4 measures, some skipped for n under 3 per side) plus 20 rank correlations plus 2 search tests = about 166. At p 0.05 about 8 would pass by luck. Treat p above 0.001 as a lead, not a finding. Nothing here proves a cause.

## Table 1: views at like-for-like age (Windsor views, set A unless said; medians)
| Feature | With (n) | Without (n) | p |
|---|---|---|---|
| "your" in the headline (series tag ignored) | 1,150 (29) | 873 (34) | 0.007, but the "your" Shorts are the newer drawn or 3D era; inside set H 28 of 30 have it, so it cannot be separated from era |
| Number in title | 1,121 (27) | 993 (36) | 0.15 |
| Number in title, set D | 1,155 (16) | 1,185 (8) | 0.89 |
| Title over 44 characters | 802 (30) | 1,121 (33) | 0.005, older long titles; in set H 1,146 against 1,158, p 0.77 |
| Weekend | 1,216 (17) | 1,024 (46) | 0.09; set H 1,358 (6) against 1,138 (24), p 0.095 |
| Posted before 12:00 | 938 (15) | 1,059 (48) | 0.26 |
| Posted 18:00 or later | 991 (14) | 1,079 (49) | 0.43 |
| 3 or more Shorts that day | 1,043 (53) | 998 (10) | 0.77 |
| 3 hours or more since the last Short | 1,077 (38) | 1,035 (25) | 0.75 |
| Length 18 s or more | 991 (46) | 1,159 (17) | 0.10 |
| 3D explainer (all bug and spider) | 1,119 (5) | 1,159 (25) | 0.54 |
| Spider against bug, set H | 1,145 (8) | 1,154 (22) | 0.92 |
Versus: only 2 Shorts have it in the title (1,118 and 1,043 views is not testable). Emoji: 65 of 66 have one, so no test.
Rank correlations with views in set H (n=30): hour -0.11, Shorts that day -0.08, gap -0.16, title length -0.23, seconds -0.10. All p above 0.23.

By show (set A, Windsor): house bug 25 Shorts, median 1,146; spider 12, 1,145; survival 4, 1,124; other 22, 474.
By style: drawn v6 24, 1,155; 3D explainer 5, 1,119; other (older) 32, 781; hook test 1, 1,188 (the other four hook tests are 11/11 and 11/12, no Windsor yet; public: 1,000, 87, 74, 519).
The 9 Shorts under 500 views posted 10/27 to 11/09 with Windsor rows: the mouse droppings Short (444), the shoes recluse (48), mites in your skin (58) (skin and body topics, which MASTER_ORDERS already lists as flops), two 3D explainers at 19:00 (356 and 464), and four older Shorts (Bermuda case file, toad beetle, dagger-claw bird, CIA claw 87).

## Table 2: engaged share and average % viewed (Windsor, medians, Shorts with 100+ views)
| Group | Engaged share | Avg % viewed |
|---|---|---|
| House bug (25) | 0.477 | 77.8 |
| Spider (12) | 0.459 | 72.4 |
| Survival (4) | 0.377 | 58.6 |
| Other animals (22) | 0.326 | 58.1 |
| Drawn v6 (24) | 0.477 | 81.8 |
| 3D explainer (5) | 0.498 | 75.0 |
| Other (older) (32) | 0.337 | 61.8 |
Inside set D (drawn v6 bug and spider, n=24, hold show and style roughly fixed):
- Title with a number: engaged 0.459 (16) against 0.534 (8), p 0.018; average % viewed 89 against 68, p 0.032. Mixed signs, so a lead at most.
- "your" in the headline, all of set A: engaged 0.475 against 0.373 (p 0.001), average % viewed 82 against 59 (p under 0.001). It is the same era gap as drawn against older, not a "your" effect.
- Title over 36 characters: engaged 0.526 (12) against 0.456 (12), p 0.015.
- Spider against bug: engaged 0.548 (6) against 0.467 (18), p 0.029.
- Length 18 s or more: average % viewed 59 (7) against 89 (17), p 0.007. Rank correlation of seconds with average % viewed in set H: -0.68 (p under 0.001). This is the replay effect: 14 to 16 s Shorts loop and read above 100%. It is not a quality gap. Engaged share rises a little with length (rho 0.36, p 0.065).
- Posted 18:00 or later: average % viewed 59 (3) against 89 (21), p 0.078 (3 Shorts).
None of these survive 166 comparisons on their own. The robust gap is show and era (Table 1).

## Table 3: subscribers per 1,000 views (Windsor, 11/12; subscribers are whole numbers, so every group is noisy)
| Group | Shorts | Subs | Views | Subs per 1,000 (95% bootstrap) |
|---|---|---|---|---|
| All | 66 | 63 | 60,436 | 1.04 (0.73 to 1.41) |
| House bug | 28 | 36 | 30,475 | 1.18 (0.68 to 1.81) |
| Other animals | 22 | 15 | 12,329 | 1.22 (0.59 to 1.93) |
| Spider | 12 | 10 | 13,698 | 0.73 (0.39 to 1.11) |
| Survival | 4 | 2 | 3,934 | 0.51 |
| Drawn v6 | 25 | 31 | 28,107 | 1.10 (0.67 to 1.62) |
| 3D explainer | 6 | 3 | 5,567 | 0.54 (0.17 to 1.02) |
| Other (older) | 32 | 19 | 23,397 | 0.81 (0.43 to 1.29) |
| "your" in the headline | 31 | 28 | 33,588 | 0.83 (0.53 to 1.16) |
| No "your" in the headline | 35 | 35 | 26,848 | 1.30 (0.74 to 2.00) |
All intervals overlap. 33 of 66 Shorts gained no subscriber at all.

The ten Shorts that gained the most (subs, views, posted ET):
| Subs | Views | Per 1,000 | Posted | Title |
|---|---|---|---|---|
| 7 | 1,327 | 5.3 | 11/10 19:02 | The Bug You Squish Is Protecting You (the Kill-or-Keep teaser file) |
| 5 | 1,013 | 4.9 | 11/07 19:03 | 26,205 Stink Bugs in One House (27.5 s) |
| 4 | 938 | 4.3 | 10/28 09:31 | This Animal Fakes Its Own Death (opossum, 29.7 s) |
| 3 | 1,848 | 1.6 | 11/08 08:03 | 100 Feet a Night to Your Bed |
| 3 | 1,362 | 2.2 | 10/31 12:04 | A Cockroach Can Live for Weeks Without Its Head |
| 3 | 1,129 | 2.7 | 11/03 16:03 | Turn On Your Bathroom Light at 3 A.M. |
| 2 | 1,772 | 1.1 | 11/06 16:03 | 40x Jumps From Your Window |
| 2 | 1,354 | 1.5 | 11/07 10:03 | 30K Roaches in Your Kitchen |
| 2 | 1,326 | 1.5 | 11/02 16:02 | Never Squish the 30-Legged Bug in Your House |
| 2 | 1,223 | 1.6 | 10/27 21:02 | A Bug Older Than Dinosaurs Is Eating Your Books |
What they share: 9 of 10 are house bug or spider; 6 of 10 have "your" in the headline (the top three do not); 6 of 10 are the 14 to 16 s drawn v6 cut; every one has 900+ views (the 55 Shorts with 300+ views are the only ones that can show a link). The top three are the only ones above 4 per 1,000 and two of them are the longer cuts (27.5 and 29.7 s) and the third is a teaser file. That is three Shorts, so it is a lead for a test, not a rule.
Link with subscribers (Shorts with 300+ views, n=55, rank correlation): likes 0.51, shares 0.31, engaged share 0.24, views 0.20, comments 0.09, average % viewed 0.01. Shorts with 2+ subscribers had a median 13.6 likes per 1,000 views against 9.9 for the rest (17 against 38). Subscribers go with likes, not with how much of the Short was watched.

## Table 4: posting time, weekday, count and gap (see Table 1 for views)
- Rank correlation of average % viewed: hour -0.32 (p 0.085), gap since last Short +0.31 (p 0.09). Engaged share against gap -0.30 (p 0.11). Subscribers per 1,000 against Shorts that day -0.27 (p 0.15). All weak, none clear.
- Weekend is the only view lead (1,216 against 1,024 in set A, 1,358 against 1,138 in set H, both p about 0.09, and only 6 weekend Shorts in set H).
- Not measurable here: five Shorts in one day (11/11 and 11/12). Windsor has no rows for them yet and the Shorts that day are a mix of hook tests and joke tests.
- 3 Shorts that day is 53 of 63 Shorts, so "1 or 2 a day" has only 10 Shorts to compare with.

## Table 5: decay and search
Source: `research/data/90-youtube-video-day.csv` (Windsor by video and day, to 11/09, day 0 is the Windsor date) and `research/data/94-shorts-source-shares.csv` (Windsor traffic_source per video, 11/12).
| Share of views by day | Median share (19 Shorts with 300+ views and 6 observed days) |
|---|---|
| Day 0 | 0.72 (range 0.08 to 0.98) |
| Day 1 | 0.14 |
| Day 2 | 0.04 |
| Day 3 | 0.01 |
| Day 4 | 0.005 |
| Day 5 | 0.002 |
- On day 2 or later: median 6.8% (middle half 4.4 to 13.3%). After day 2 (day 3 on): median 3.0% (middle half 1.8 to 3.7%). Observed only to day 5, so the real late share is a little higher. Late views per Short after day 2: median 33; only 4 of 19 had 50 or more.
- Day 0 is the Windsor date, so an evening post can spill onto day 1 (the 11/02 to 11/04 evening Shorts show it). The 72% is therefore a low-side figure.
- The 14 earliest Shorts with day 7 data: median 2 views on day 7 against 954 on day 0.
- Searches: 63 Shorts, 3,173 search views of 57,906 (5.5%). Median search share per Short 3.9%. The five best Shorts hold 38% of all search views.
| Show | Shorts | Search views | Share of its views |
|---|---|---|---|
| Spider | 12 | 1,431 | 10.8% |
| Survival | 4 | 232 | 5.9% |
| Other animals | 22 | 483 | 3.9% |
| House bug | 25 | 1,027 | 3.6% |
Spider against house bug, median search share 8.0% against 3.0%, p 0.0014 (spider against all else p 0.0078).
- Shorts that keep earning from search: the daddy longlegs Short (631 search views, 26.7%; 10 to 64 views a day on days 5 to 16, 321 views after day 2, 14% of its total), the window spider (201, 15.7%), the Short about the spider that hunts spiders (163, 12.9%), the basement spider (123, 11.2%), the stonefish (82 after day 2). Per-day search for each is not pulled (that needs one Windsor call per video with the video filter; not run, to save calls).

## Pets and survival against bugs (item 6)
- Pets so far: cat sugar (11/12 16:00): 1,000 public at 7.6 h. Dog turkey (21:47): 2 at 1.8 h. Cat purr (22:20): 52 at 1.2 h. Turkey and purr are too young to read.
- Survival: the four 10/25 to 11/01 Shorts have 1,254, 1,224, 1,024 and 433 Windsor views (median 1,124); moose (11/12 19:00): 493 public at 4.6 h.
- Bug and spider Shorts posted 11/10 to 11/12 have a median of 495 public views (9 Shorts: 530, 295, 2,100, 1,000, 818, 495, 87, 74, 519, ages 4 to 52 hours). The drawn v6 bug and spider median before 11/10 is 1,155 (Windsor). So the channel itself fell after 11/10 (research 90). The cat and moose are not behind that new level, but they have not reached 1,155 either, and at under 8 hours old they have not finished.
- Ages differ: the new Shorts are hours old, the baseline is final. Day 0 holds a median 72% of views, so a Short at 8 hours old is likely not above half its final count. A fair read needs Windsor at 3 days (Sat 11/14 or Sun 11/15) and the same count of Shorts. At n=3 pets and n=5 survival Shorts nothing here is a result.

## Could not measure
- The 10 Shorts from 11/11 and 11/12 have no Windsor data (2 to 3 days behind); the 11/09 and 11/10 Shorts are partly counted.
- Jokes, plain against funnier: 0 of the 6 joke Shorts have Windsor rows.
- A "your" effect apart from era: 28 of the 30 modern Shorts have "your" in the headline. I read "your" in the headline only, so the "(Things Living In Your House)" series tag does not count.
- A versus effect (2 Shorts) and an emoji effect (65 of 66 have one).
- Retention curves, swipe-away, impressions and click-through per Short (Studio only; vidIQ again on 11/24).
- Per-day search for each Short (not pulled).
- Windsor day buckets may be Pacific days; day 0 share is a low-side figure.
- Length is blank for 6 Shorts; hold-joined and 69 lengths are as measured in those files, not re-measured here.
- I labelled show, style and jokes by hand from titles and `posted.csv`; a different reader could move a few Shorts.
- The brief said about 105 Shorts. posted.csv has 100 YouTube Shorts rows, but the 24 dated 11/13 or later are not out yet; 76 are public, and the 4 earliest 10/22 and 10/23 true or false Shorts are not in posted.csv (they come from the channel list and Windsor).
