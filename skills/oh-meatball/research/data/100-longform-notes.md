# 100 longform: long videos, daily totals, audience (label: longform)

Pulled 2026-11-13. Windsor youtube, account 34639. The last day with data is 2026-11-10. Public view counts are from yt-dlp /videos on 11/13.
Files: `100-longform-table.csv`, `100-longform-traffic-sources.csv`, `100-channel-daily.csv`, `100-audience.csv`.
Check: Windsor's long-video views for 10/14 to 11/10 add to 683, the same as Studio's 28-day figure (11/11). Hours: Windsor 10.4, Studio 10.6.

## Answer first (five lines)
1. The long videos earn about 0.37 hours a day (10.4 h in 28 days, Windsor). That is 135 hours a year, 3.4% of 4,000. One long view lasts about 0.9 minutes, not the 6 minutes the 40,000-view plan assumed.
2. Half of long-video views (47%) and 70% of their minutes come from "Related video". Search is 3.5% of views and under 1% of minutes. Subscribers are 46% of views but only 25% of minutes. Windsor cannot say whether Related came from our Shorts links.
3. Windsor has no impressions or click-through field. The 2.5% is Studio's only. At 2.5%, 4,000 hours is about 10 million impressions (arithmetic below).
4. Three honest scenarios all need 6 to 23 times what we do today. The best Short-to-long funnel (5% of Shorts viewers click through) still needs 6 times today's Shorts reach.
5. Subscribers: 81 gained and 25 lost in 28 days (channel total). Shorts gained 0.96 per 1,000 views, long videos 2.9 per 1,000, but the long figure rests on 2 subscribers and does not differ from Shorts (p 0.14).

## 1. Where long-video hours come from
Source: Windsor, `traffic_source` with `video` filter, one call per video, 10 channel long videos, 10/1 to 11/10. The 683 views and 607 minutes (10.1 h) are every long view. The private 14-second video is left out.

| Source | Views | Minutes | Share of views | Share of minutes | Minutes per view |
|---|---|---|---|---|---|
| Related video | 322 | 422 | 47.1% | 69.5% | 1.31 |
| Subscribers | 313 | 154 | 45.8% | 25.4% | 0.49 |
| Search | 24 | 5 | 3.5% | 0.8% | 0.21 |
| Channel page | 10 | 7 | 1.5% | 1.2% | 0.70 |
| Other YouTube page | 5 | 0 | 0.7% | 0.0% | 0 |
| No link / other | 8 | 11 | 1.2% | 1.8% | 1.38 |
| Playlist | 1 | 8 | 0.1% | 1.3% | 8.0 |

Not found for long videos: Shorts feed, browse home, external. The channel-wide traffic call mixes Shorts in (61,728 Shorts-feed views). Windsor ignored the long-form filter there, so I did not use it.

Per video (all in `100-longform-table.csv`):

| Video (published) | Length | Views | Hours | Min per view | Avg viewed | Main source |
|---|---|---|---|---|---|---|
| 3 Bugs You Should Never Kill (11/7) | 4:34 | 199 | 4.02 | 1.21 | 42.8% | subscribers 137, related 51 |
| Weird Animal Facts (10/26) | 10:17 | 134 | 2.35 | 1.05 | 11.0% | related 126 |
| Animals Thought Extinct (10/25) | 7:04 | 125 | 1.90 | 0.91 | 15.7% | related 101 |
| How Wolves Became Dogs (10/24) | 8:21 | 162 | 1.27 | 0.47 | 20.8% | subscribers 135 |
| Everything You Know About Animals (10/22) | 2:15 | 43 | 0.37 | 0.51 | 41.8% | related 18, subscribers 18 |

Six more videos have 2 to 5 views each (under 0.15 h together); their percentages mean nothing. Part 2 of "3 More Bugs" (11/11) has no Windsor row yet; public count 59 on 11/13.

Which earned the most hours per view: "3 Bugs You Should Never Kill" (1.21 minutes per view, 4.0 hours, 39% of all long hours). Why, as far as the numbers go:
- It is the shortest of the big four (4:34) and has the best percent viewed (42.8%).
- Its 51 Related views were watched 2.33 minutes each. Its 137 subscriber views were watched 0.77 minutes each.
- Topic (house bugs, our best Shorts topic), length and title all differ from the others, and the sample is four videos. I cannot say which one did it.
- Length did not buy minutes. Average view duration was 66 s on the 10:17 video and 118 s on the 4:34 one (n 4, no test run).

## 2. Do Shorts send anyone to long videos?
Not provable from Windsor. Related video is 322 views over 28 days. Our Shorts got 65,778 views in the same 28 days, so Related is at most 0.49% of Shorts views (an upper bound, because YouTube's own suggestions are in it too).
Evidence is mixed (`data/related-video-map.csv`, which says what was planned, not what was set in Studio):
- For: Weird Animal Facts (24 Shorts mapped to it) got 126 Related views and almost nothing else. Animals Thought Extinct (the backup for 24 Shorts) got 101 Related views.
- Against: Conspiracy Theories (14 Shorts mapped) got 1 Related view of 5. The wolves video is not a target in the map and still got 15 Related views.
- The map's best_longform_id column is empty, so I matched by title only.
Clean test: set Related video on a batch of Shorts to one new long video and read its Related views by day in Windsor.

## 3. Impressions and click-through
Windsor youtube has no impressions or click-through field (get_fields checked 11/13; it lists only card and annotation impressions). Studio's 2.5% (11/11, MASTER_ORDERS) is the only figure.
What it implies, as arithmetic and not a measurement: views = impressions x click-through.
- 683 views at 2.5% would be about 27,000 impressions in 28 days. But 46% of the views came from subscribers and Related, so not all were impression clicks.
- 4,000 hours is 240,000 minutes. At 0.91 minutes per view that is about 263,000 views: 10.5 million impressions at 2.5%, 5.3 million at 5%.
- Raising click-through from 2.5% to 4% cuts the impressions needed by 37%. It does not change the hours per view.

## 4. The arithmetic of 4,000 hours
Counted so far: 10.4 h in 28 days (Windsor). Left: about 3,990 h. Only hours from the last 12 months count, so the pace is judged per year.
- **Today's pace:** 0.37 h a day. 135 h in a year (3.4%). 3,990 h would take about 29 years.
- **Pace since the Shorts rise on 10/19:** 0.45 h a day (623 minutes in 23 days). 165 h a year.
- **Scenario A, one video breaks out:** needs about 198,000 views at the best video's 1.21 min per view, 263,000 at the channel's 0.91. It needs 80,000 views only if each view lasts 3 minutes. We have never had 3 minutes: the best was 118 s, on a 4.5 minute video. The orders line "40,000 views at 6 minutes" needs 6 minutes per view, about 75% viewed on an 8-minute video. Our best on a 7+ minute video is 20.8%.
- **Scenario B, a weekly video that repeats our best:** 4.0 h each (first four days) x 52 = 208 h, 5.2%. To reach 4,000 h each video would need 77 h, 19 times the best. And 69% of that best video's views were subscribers, who are the same 1,000 people each week.
- **Scenario C, a Shorts funnel:** 4,000 h a year is 658 minutes a day, about 723 long views a day at 0.91 min. At today's 0.49% hand-off, that needs about 148,000 Shorts views a day, 63 times today's 2,349. At 5% it needs 14,450 a day, 6.2 times today's.
Each scenario needs a larger audience than we have. What would have to be true: a click-through hand-off from Shorts of 5% or more (never measured), and 2 or more minutes per view (best so far 1.2).

## 5. Who watches
Source: Windsor, 10/14 to 11/10 (pulled with date range to 11/13), all content, Shorts included. Country rows cover 51,671 of about 66,500 views (78%); the rest has no country. Age and gender are percentages of all viewers. Windsor ignored the long-form filter for country, and age and gender cannot be split by content type.

| Country | Views | Share | Minutes per view |
|---|---|---|---|
| United States | 12,018 | 23.3% | 0.179 |
| Ireland | 7,630 | 14.8% | 0.141 |
| United Kingdom | 6,252 | 12.1% | 0.165 |
| Philippines | 5,775 | 11.2% | 0.138 |
| Canada | 1,373 | 2.7% | 0.132 |
| Indonesia | 1,349 | 2.6% | 0.142 |
| Germany | 1,337 | 2.6% | 0.099 |
| Malaysia | 1,216 | 2.4% | 0.108 |
| Vietnam | 1,178 | 2.3% | 0.090 |

- US, UK, Ireland, Canada, Australia and New Zealand together: 54.7% of views and 62.8% of minutes (0.22 minutes per view against 0.12 for the rest).
- Age: 25 to 44 is 58.7% (25-34 28.8%, 35-44 29.9%). 13 to 17 is 14.5%. 18 to 24 is 8.7%. 45 and up is 18.0%.
- Gender: 56.9% male, 43.1% female.
- Subscribed against not: no field. The only proxy is the Subscribers traffic source: 45.8% of long views, 0.5% of channel-wide views.
What this suggests (leads, not causes): English-speaking viewers watch longer, so keep English titles and topics that work in the US, UK and Ireland. Posting hours: Windsor has no hour field, so I cannot say when viewers are online. Ireland, the UK and the Philippines are 38% of views, so the 08:00 ET slot is 13:00 in the UK and 21:00 in the Philippines. Studio's "When your viewers are on YouTube" card would settle it.

## 6. Subscribers
Channel totals, 10/14 to 11/10 (Windsor `subscribers_gained_channel`): 81 gained, 25 lost, net 56. Attributed to videos: Shorts 63, long videos 2 (3 Bugs 1, Animals Thought Extinct 1). The other 16 gains are not tied to a video.
- Best days: 10/28 (9), 11/8 (8), 11/10 (8), 10/21 (7), 10/25 (5). Those are not the biggest Shorts-view days: gains and daily Shorts views have a correlation of 0.15 over 23 days (since 10/19), which is weak.
- Gain per 1,000 views: Shorts 0.96 (63 on 65,778 views, 95% interval 0.74 to 1.23). Long 2.9 (2 on 683, interval 0.35 to 10.6). If the 65 attributed gains were spread by views alone, long videos would get 2 or more with probability 0.14. No evidence they differ.
- Shorts with the most gains per 1,000 views (only Shorts with a gain were pulled, so this is picked after the fact): "The Bug You Squish Is Protecting You" 7 on 1,327 (5.3), "26,205 Stink Bugs" 5 on 986 (5.1), "Fakes Its Own Death" 4 on 921 (4.3). One-off counts, not a pattern yet.
- 34 Shorts had at least one gain. Their gains add to 64 (the daily total says 63; one Short posted 11/10 evening).
Comparisons run: 2 Poisson intervals, 1 exact binomial split, 1 correlation (4 in total).

## Could not measure
- Impressions and click-through per video (no Windsor field; Studio only).
- Where Related-video views came from (our Shorts links or YouTube suggestions).
- Subscribed against not subscribed viewers, device type, playback location, hour of day: no Windsor field.
- Country, age and gender for long videos alone (Windsor ignored the long-form filter on country; age and gender are channel-wide).
- Part 2 of "3 More Bugs" (11/11) and anything after 11/10: no Windsor rows yet.
- Retention curves (Studio or vidIQ on 11/24).
- A private 14-second video ("Modern Dating Has Become Impossible", published 6/15, 1,162 views, 559 minutes, almost all external links) sits in Windsor's all-time totals. Whether Studio counts it toward the 4,000 hours was not checked; it is left out of every figure above.
- 60 days asked, 58 days returned (9/14 to 11/10): Windsor has nothing after 11/10.
- The 10/19 jump in Shorts views is in `100-channel-daily.csv` but its cause is research 90's job.
