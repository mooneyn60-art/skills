# 91 · TikTok "view jail" (2026-11-12, read-only)
**Answer:** each video gets a small test batch (~250 views) and does not pass it; the account is still served (For You 80% of views), no restriction shows on 10 public pages. Likeliest reasons: weak finish/share signals in the batch, and a cartoon category label that picks the wrong test audience. Neither is proven; the owner's own screens (below) can settle the first checks today.

## 1. What TikTok says (fetched 11/12; quotes as the fetch returned them)
- Testing: no TikTok page describes a small first batch. Newsroom: the system gets "a better sense of what's popular among a wider range of audiences"; strong signals count most, e.g. "whether a user finishes watching a longer video from beginning to end"; "neither follower count nor whether the account has had previous high-performing videos are direct factors." https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- Followers first: not stated (Transparency page lists follow relationships only as one personalization input). https://www.tiktok.com/transparency/en/recommendation-system
- Posting often / deleting: not addressed on either page. Spam is ineligible: "videos seeking to artificially increase traffic"; "duplicated content" is not recommended (Newsroom, above).
- Ineligible video: FYF standards (effective 2026-09-24) say only "certain content that may not be suitable for a broad audience"; "If a video isn't getting many views, it also doesn't necessarily mean it broke a rule"; ineligible videos stay findable "through search or by going to a creator's account." https://www.tiktok.com/safety/en/policies-and-engagement/fyf-standards
- Unoriginal: "Content is also ineligible for the FYF if it includes unoriginal or reused material without anything new." AI: "we require creators to label AI-generated or significantly edited content that shows realistic-looking scenes or people"; unlabelled "may be removed, restricted, or labeled." No page says AI-labelled or animated content gets less reach. https://www.tiktok.com/community-guidelines/en/integrity-authenticity
- Account level: "accounts that don't break the rules still post a lot of content that's ineligible for the FYF" can be made "ineligible for the FYF and harder to find"; "Repeated rule violations" can ban. https://www.tiktok.com/safety/en/policies-and-engagement/accounts-features . Notice: "We will notify creators when their accounts have been restricted in this way" (https://newsroom.tiktok.com/cgupdate?lang=en-ZA); video-level notices "will appear in the TikTok analytics tool", appeals tracked in the in-app Safety Center (https://www.tiktok.com/community-guidelines/en/enforcement).
- Not readable: Creator Academy and Help Center pages are script-only; their steps below come from search summaries of them.

## 2. What is reported (ALL non-TikTok, UNVERIFIED)
- "200 views" is a first test batch that did not watch long enough; real holds look like 0-5 views for hours. Fixes offered: payoff in frame one, a new visual every ~3 s, one niche for 2-3 weeks, repost an improved cut. Vendor blogs (tokboostly.com, hookclone.com, viewlify.app, cut.pro, multilogin.com): they sell tools. No TikTok statement of a 200 limit.
- Followers not matching new content: explained as "niche confusion" by blogs; TikTok's own page says follower count is not a direct factor. Restored account: one 2025 forum anecdote of zero views after a successful appeal; nothing else found. AI-voiced animation: a blog says fully AI content is targeted; TikTok says transparency, not a downrank (Creator Academy, via summary). 3+ posts a day: Buffer (11M posts, observational) shows no harm and a median near 500 views at any frequency; "same-day suppression" is blog talk. New account: only warnings. TikTok: "you may not create or use another account to get around" a restriction (integrity page above).

## 3. Our numbers (81 posts 10/23-11/12, Metricool; data/91-tiktok-posts.csv)
- Median 229 (226 on the first 78); middle half 196-316; 90th percentile 677; 14 posts at 500+, 3 over 1,000 (5,984; 3,839; 2,542 now). All three are from 10/26-11/1; best since: 908.
- Not separated: 500+ posts by style 6 of 36 early photo/quiz, 8 of 41 drawn, 0 of 4 3D. Weekday, posting hour and length show nothing that survives the overlaps (morning slots were first-week photo posts; 15 s posts are the recent house bugs). Search-phrase caption opener: median 313 vs 220 (n=17, p 0.005 before correction, tied to house topics and 15 s). Label: Animals 5 of 7 reached 500, Cartoon 7 of 23, but those 32 were sampled top-first (46 unlabelled, none 500+), so biased.
- Posts per day: days with 5+ posts median 216 vs 260 (p 0.11); day median vs count correlation 0.04. No effect shown; the 8-9 post days (10/25-26) held the biggest post and the weakest day.
- Trend: weekly medians 222, 222, 305; later posts are younger and still growing. Older posts freeze (66 posts over 3 days old gained a median 1 view in 2 days; four gained 104-856, led by centipede part 2).
- Like rate: 2.18% overall; 2.50% on posts of 150-300 views; 2.33% under 500, 2.07% at 500+. Normal, not low. Comments 17 and shares 22 in 35,436 views (0.05%, 0.06%).
- Public pages (10 recent posts, 11/12 ~09:50 ET): isReviewing False, penaltyContext identical (status 102, display_penalty_type 0), indexed, no flag. Labels: 8 Cartoon (one is the sweary cut, 287 plays), 1 Games (3D window spider), 1 Education (3D roach). Meaning of 102 is undocumented.

## Most likely causes, ranked
1. Test batch fails on finishing and sharing. For: flat band for 3 weeks across lengths, styles, topics; shares 0.06%; finishing is TikTok's named strong signal. Against: likes normal; 15 s Shorts only slightly better. Not measurable here (reach, watch time are null).
2. Cartoon label picks a cartoon test audience. For: research 82 (Animals/Education median 615, n=10, vs Cartoon 340, n=20); the two biggest early posts. Against: biased sample, style and date move together; cartoon posts reached 2,542. Followers are a weak form of this (80% For You).
3. Account standing or moderation history. For: Rewards lost once; nothing over 908 since 11/1 (date of the loss unknown). Against: 80% of views are For You; no flag on 10 pages.

## Test plan (8 days; sizes from resampling the 50 posts since 10/28, median 260)
1. Owner checks standing today (below). Worked: any notice found = appeal; none = drop cause 3. Runs beside all others.
2. Real photo or footage of the animal in seconds 0-2 plus 2-3 more through the cut, 6 house-bug cuts at 12:00, one a day (needs the owner's yes; look is locked). Read the label 1 h after each; stop after 3 if none reads Animals or Education. Worked: label flips on 5 of 6 and median 400+ or 3 of 6 at 500+ (chance gives median 370 at the 95th percentile, 2 of 6 at 500+). 6 days plus 2.
3. Search-led, 6 posts at 19:00 beside test 2: the plain search phrase spoken and on screen in 0-2 s, payoff in second 2, 15-25 s, topics from research 75. Worked: median 400+ or 3 of 6 at 500+, or Search over 30% of their views (account 18%). Same days as test 2, different slots, so they do not spoil each other; leave the 20:15 sweary cuts alone as their own comparison.
4. Two posts a day (12:00, 19:00) for 7 days, alone, only if 2 and 3 fail; it would spoil them. Worked: 14 posts, median 350+ (chance 99th percentile 342) and daily total about 700 or more. Weakest evidence.
- Fresh account: last resort. Costs: 9,323 followers, Rewards history, restart at zero, and it counts as evasion if the account is restricted. No source shows it helps.

## What only the owner can check
- Profile > menu (three lines) > TikTok Studio > More tools > Account check; or Profile > menu > Settings and privacy > Support > Safety Center > Account check (Help Center "Your account status", via summary). Account status: Settings and privacy > Account > Account status (blog path, unverified).
- Open a low video > Performance/analytics: a bar "not eligible for For You" (reported, unverified). Inbox > notifications. Studio per video: watched-full %, average watch time, Search share, traffic sources.
- Ask: when and why Rewards was removed; whether any video was deleted or removed (Studio says 76 posts to 11/10, Metricool 78 over a shorter span).

## Could not measure
- Reach, watch time, completion, For You vs Search per video (Metricool nulls; Studio only).
- How the label is set and weighted; what penaltyContext 102 means; the test-batch size.
- Any cause from a restricted view only the owner sees. TikTok's FYF ineligible list was not on the pages that loaded.
