# 97 · TikTok view jail, round 2: checked and ranked (2026-11-12, read-only)
**Answer:** nothing on any public page points to a block. The likeliest reason is that our videos earn less from the people in the first batch than comparable drawn accounts do (likes 2.2% against 4 to 10%, the fewest comments of any account read), so TikTok stops showing them. The closest peer (lianna_anima, drawn stick-figure pets, 10.3K followers) gets a median of 2,232 with videos three times as long as ours.
**Next:** the owner's one Studio screenshot (open ask 1) tells us whether people leave early. Keep the running 19:00 search test clean. With his one yes, test six drawn 2.5 to 3.5 minute TikToks at 12:00.

## Asked by Nolan 11/12
"Keep digging like this it's good focus on TikTok also not just yt we're still in a TikTok view jail"

## Method
- Read research 91, 96, and the three round-2 files (data/97-tiktok-own-posts.csv, 97-tiktok-comparable-accounts.csv, 97-tiktok-comparable-videos.csv, 97-tiktok-platform-notes.md).
- Pulled again myself (11/13 about 02:30 UTC): yt-dlp flat listings of the newest 30 posts for 5 accounts (lianna_anima, randomfact_06, hypothetical.animation, animatales5, lazllc); postkit ttpage on 6 of our posts (the three 1,000+ posts, the 10/30 lizard, the 11/11 sweary cut, the 11/12 12:02 pantry moth); 5 quoted TikTok pages with curl (FYF standards, the newsroom AI content page, Creator Academy AI label, two developer pages).
- Recomputed from the CSVs with pandas and scipy: the search-phrase opener test, plays over time, weekly medians, label medians, totals, 5x breakout counts, 500+ counts, share posts, and the comparable accounts' like, share and comment rates on ordinary posts.
- About 17 TikTok requests in all, at least 1 second apart, no sign of blocking. No video was downloaded. Nothing posted or changed.

## What held when re-pulled
- Account medians (yt-dlp, 11/13): lianna_anima 2,232 (CSV 2,222), randomfact_06 862 (862), hypothetical.animation 732 (732), animatales5 5,353 (5,353), lazllc 158.5 (158). Breakouts at 5x the median: 4, 8, 1, 5, 0, same as the CSV.
- Our 6 posts (ttpage, 11/13): bombardier beetle 5,998 (CSV 5,989), centipede 3,892 (3,869), centipede part 2 2,944 (2,793), lizard 201 (201), 11/11 sweary cut 311 (299). Labels and the flag fields match: is_reviewing False, penalty status 102, display type 0.
- Search-phrase caption opener since 10/28: median 321 (n=14) against 223.5 (n=32), permutation p 0.006 (I got 0.006, they got 0.007).
- Weekly medians 221.5, 224, 299; posts at 500+ by week 8, 2, 4; 3 posts at 5x the 229 median.
- Comparable like, share and comment rates on ordinary posts recompute to the same values (animatales5 4.94%, lianna 5.43%, hypothetical 4.14%, randomfact 9.90%).
- Quotes on TikTok's pages: "If a video isn't getting many views, it also doesn't necessarily mean it broke a rule" (FYF standards); the AIGC control in Manage topics "rather than removing or replacing content in feeds entirely" (newsroom, page dated 2025-11-24); "Applying the label will not have an impact on organic engagement" (Creator Academy AI label page, not the newsroom page); "typically around 15 posts per day/ creator account" (content sharing guidelines); "All content posted by unaudited clients will be restricted to private viewing mode" (get started page).

## Numbers that did not hold
1. "Medians 732 to 2,222 for the 4 with 10K or more followers." Only 3 active accounts under 100K have 10K+ followers (lianna_anima, randomfact_06, hypothetical.animation). jeremy_bearimy1 has 560.
2. "6 active animated fact accounts." One of them, lazllc, is a skit account, not facts.
3. "Our middle half 196 to 316, ratio 1.72." The CSV row has 191 to 329 (ratio 1.72). 196 to 316 would be 1.61. Two pulls are mixed. On all 82 posts it is 188.5 to 323.5.
4. "Spearman of plays against post order rho +0.23, p 0.038" on the 77 posts at least 48 h old. On those 77 it is +0.20, p 0.08. The +0.23 only comes back on 81 posts. So "the median rose a little" is weak.
5. "The 11/12 12:02 post has 11 plays at 4.8 h." It had 116 at 9.5 h. A slow start, not a drop.
6. "Likes are normal" (own-posts audit and research 91). Within our account, yes. Against peers, no: 2.2% is lower than 6 of the 7 accounts I recomputed (only lazllc is lower, 1.8%). Comments (0.05%) are the lowest of all of them (others 0.06% to 0.69%).
7. Totals called "overall" (34,779 plays, likes 2.11%, 23 shares, 62 saves) are the 77 older posts. All 82: 36,083 plays, 795 likes (2.20%), 17 comments, 24 shares, 65 saves.
8. "Cartoon 260 (n=53)." The CSV gives 249 (n=51) on the 77 older posts, 254.5 (n=54) on all 82. Same conclusion: no label difference.
9. Small drift on the comparables since their pull (lianna spread now 2.6, not 3.5, because new posts entered the window). Not wrong, just moving.

## Ranked causes of the 250-view ceiling
| # | Cause | For | Against | How sure |
|---|---|---|---|---|
| 1 | The first batch does not like, comment on or (probably) finish our videos, so TikTok stops there | Likes 2.2% against 4.1 to 9.9% on drawn peers' ordinary posts; comments 0.05%, lowest read (yt-dlp, 11/13). Tight band, 1.7x, through every change. TikTok names finishing as a strong signal (research 91). The two tiny AI-labelled accounts sit at 158 to 175, the same as us: our 9,300 followers add nothing, like a new account | Like rate does not track plays inside our account (rho -0.05, own-posts audit). Watch time not measured | Medium |
| 2 | Our videos are short for this niche. The drawn animal accounts that break out at our size run 2.5 to 4 minutes | lianna_anima (drawn stick-figure pets, 10.3K) median 2,232 at 195 s; animatales5 5,353 at 164.5 s; their breakouts are 150 to 247 s on 6 of 7. Ours 64 s, new cuts 20 to 26 s | Others break out at 15 to 65 s (incrediville, randomfact_06, dinoeggpro). Search-picked sample. Our 15 to 30 s posts did a little better than 60 to 90 s (301 against 221) | Low to medium |
| 3 | Topic and words: posts get a bigger first batch when the caption and video say what people search | Search-phrase opener 1.7x with topic, length and date held (p 0.006, t 2.2); posts showing TikTok's suggested searches 304.5 against 213; top 5 posts are scary bugs people search | Tied to house bugs and 15 s cuts in November; 28 tests run; owner moved off bugs (11/11) | Low to medium |
| 4 | An account-level limit (standing, moderation history) | Nothing we change moves the band; no post over 1,000 since 11/1 | No flag on any of 82 pages; posts reached 5,998 before; chance of no 1,000+ in 34 posts is 0.28; TikTok says restrictions show in analytics and Account check | Low |
| 5 | The AI label, through viewers' AIGC setting in Manage topics. Ruled out by the owner (label stays on) | The setting exists (newsroom, 2025-11-24); only 1 of 14 drawn breakouts read carries the flag; the 2 small flagged accounts sit near 170 | TikTok says the label has no effect on organic engagement; hypothetical.animation broke out at 24x with it; slider use unknown | Low |
| 6 | Drawn look and the Cartoon label. Ruled out by the owner (stays drawn) | Research 82's early sample | 13 of 14 drawn breakouts carry Comics & Cartoon, Anime, up to 992,700; our label medians 249, 222, 214 | Low |
| 7 | Posting 3 to 4 a day | We post more than any peer (3.86 a day) | Research 91: no day-count effect; lazllc posts 2 a day at 158; Buffer: no harm at any frequency | Low |
| 8 | Posting through Metricool (the API) | None found in TikTok's docs | All 3 winners went through Metricool; the one possible hand upload did not do better | Very low |

A Business account has no evidence for it either way and is ruled out by the owner.

## Tests (cheapest first; nothing here is posted yet)
1. **Owner screenshot, already open ask 1 (1 day).** One screenshot of a recent ordinary post (about 250 views) in TikTok Studio: average watch time, watched full video, traffic sources. My pass marks, set now (TikTok gives no benchmark): watched full under 15% or average watch under half the length means cause 1 leads, go to test 3. Watched full 35% or more and views still under 316 means causes 1 to 3 drop and cause 4 rises; only then is the next single ask the Account check screen. Needs: that one screenshot.
2. **The running 19:00 search-led test, kept clean (free, verdict Fri 11/20).** Change nothing in the 19:00 slot until then. Pass mark already set: median 400 or more, or 3 of 6 at 500+. A pass supports cause 3. It cannot separate search words from the jokes and the short length, which change at the same time. Needs nothing.
3. **Six drawn TikToks of 2.5 to 3.5 minutes (8 days).** One a day at 12:00 for six days, each its own vertical script from a checked fact pack (house cat 87, pets and survival 84, polar bear 98), funny-first with Noodle and Sauce, second-model check, same look and voice, same caption standard. The queued 12:00 cuts move back six days. Pass mark, set now: median of the six 370 or more at 48 h (chance alone about 1 in 20), or 2 of 6 at 1,000+, with likes at 3.5% or more. A pass supports causes 1 and 2 together. They also count for Creator Rewards (over 1 minute). Needs: Nolan's one-tap yes, since it is a format change (orders allow new one-minute cuts only on proven topics).

## Could not measure
- Watch time, finish rate, first-batch size and For You against Search for any video, ours or theirs (Studio only, Personal account).
- Account check, Performance warnings and how many viewers use the AIGC setting (owner screens only).
- Whether the comparable accounts use AI voices; whether hypothetical.animation carries the AI flag on all posts (only its breakout was read).
- Whether peers post by hand or through an API.
- Losing accounts: the comparables came from web search, so they lean to winners.
- Growth curve of a post over its first hours: two reads only (11 at 4.7 h, 116 at 9.5 h, 11/12 12:02 post).
- Not re-checked: TikTok's Direct Post sound field, the Creator Academy line on anime style and TTS, Buffer's figures, the regression and the topic-family test.
