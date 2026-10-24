# 33 — Scale plan: more shots at a breakout, without looking like a spam farm (The Ambassador, 2026-10-24)

Builds on research/23, 26-31. Doesn't repeat them. Legend: **[OFF]** platform's own page or announcement,
**[3P]** named third-party data, **[RED]** creator anecdote, **[I]** my inference, **[UNVERIFIED]** not confirmed.

## 0. The one-paragraph answer
On YouTube, volume isn't the constraint. A 40% stay rate and 0 subs per 1k views are (research/26). YouTube is also actively down-ranking mass-produced AI Shorts in 2026. So **we don't raise YouTube volume.** We buy extra shots where they're cheap and safe:
- **TikTok:** more volume, because the tail grows with volume there.
- **Other languages:** dubbed audio tracks on the *same* YouTube channel.
- **Meta and Pinterest:** our own masters, posted natively.
- **TikTok becomes the lab:** YouTube gets only the Shorts that already won on TikTok.

## 1. Posting volume: the evidence
**YouTube Shorts**
- Metricool, 799,718 videos from 71,177 accounts (published 29 Jul 2026) [3P](https://metricool.com/youtube-trends/):
  - "Each Short performs best **per post** at 2 to 4 uploads a week", but monthly volume has "no practical upper limit", so more uploads still raise total monthly views.
  - Channels posting about 5 Shorts a month had long-form averaging 8,789 views. At **35+ Shorts a month**, long-form fell back to the no-Shorts level (~4,364). Metricool flags this as correlation, not causation.
  - We post ~90 Shorts a month, which is in the zone where Shorts stop helping long-form.
- AI-pocalypse, 300 AI fact Shorts in 30 days: 131k views and 318 subs, with 228 of the 300 under 100 views (research/27 S3) [RED].
  - Kapwing's faceless test took 157 days to reach 1k subs (research/27 S1) [3P].
  - Volume without a better open is a lottery with bad odds.
- **Throttling and flagging of high-frequency AI channels:**
  - Neal Mohan's Jan 2026 letter calls "AI slop" a priority. YouTube is "building on our established systems that have been very successful in combatting spam and clickbait" to reduce low-quality repetitive content [OFF via Variety](https://au.variety.com/2026/digital/news/youtube-channels-using-ai-tools-reduce-slop-neal-mohan-letter-32190/), [eWeek](https://www.eweek.com/de/news/youtube-ai-slop-crackdown-creators/).
  - One report says 1 in 5 Shorts recommended to new users were mass-produced AI [3P](https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/) [UNVERIFIED wording].
  - In Dec 2025 and early 2026, YouTube terminated large AI channels (Screen Culture, KH Studio; Kapwing counts ~16 channels). YouTube's stated reason was "spam and deceptive practices", not AI as such [3P](https://hackernoon.com/youtubes-ai-slop-crackdown-cant-tell-a-directed-ai-film-from-a-bot-farm).
  - **No source shows a hard per-day upload limit that triggers a flag.** The risk is pattern-based (template sameness) and is judged channel-wide at YPP review (research/30 §1) [I].
- **Cannibalisation:** there's no clean study. Vendor claims say Shorts don't cannibalise long-form; Metricool's 35+ data point says heavy Shorts cadence goes with weaker long-form [3P, weak either way].

**TikTok (monetized)**
- Buffer, 11.4M posts from 150k+ accounts (Oct 2025) [3P](https://buffer.com/resources/how-often-should-you-post-on-tiktok/):

| Posts/week | Median views/post | 90th-pct views | Lift vs 1/week (fixed effects) |
  |---|---|---|---|

| 1 | 489 | 3,722 | baseline |
| 2-5 | 506 | 6,983 | +17% |
| 6-10 | 487 | 10,092 | +29% |
| 11+ | 459 | 14,401 | +34% |
  - The median post stays flat, but the **tail roughly doubles from 2-5 to 11+ a week**. On TikTok, volume buys more lottery tickets with little cannibalisation per post.
  - Our 3 a day is ~21 a week, above Buffer's top bucket. There's no published data above that [I].
- TikTok "historically recommended 1-4 a day" [UNVERIFIED, quoted secondhand].
- **Creator Rewards:** the program pays on videos **over 1 minute**, and pays only from qualified For You views [UNVERIFIED for 2026; check the Creator Rewards page in the app].
  - 2026 blogs say "fully AI-generated" or "minimal original input" content is ineligible, while edits held together by your own script and voice qualify [3P](https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/) [UNVERIFIED].
  - Our original scripts, real photos and an authored mascot are on the safe side [I].

### Recommended cadence
| Platform | Now | Next 14 days | Rule |
|---|---|---|---|
| YouTube Shorts | 3/day | **3/day, hard cap 3** | All three are originals or episode cut-downs with different hooks. No Short ships unless it passes the TikTok gate (§6). |
| YouTube long-form | 1/day | **1 every 2 days** (Nolan decides; research/31 #6) | One search-first episode beats two templated ones. |
| TikTok | 3/day | **5/day**: 3 short (20-35 s, reach) + 2 over 61 s (Rewards) | Never repeat a hook within 24 h. Rotate loop lines and CTAs (research/30 R2). |
| IG + FB Reels | 0 | 2/day each, the day's best two masters | Same file is fine (§3). |
| Pinterest | 0 | 1/day | Background drip. |
- Tripwire: if YouTube stayed-to-watch stays under 50% on day 7, *drop* to 2 Shorts a day. Never raise.

## 2. Multi-language: the decision
**Decision: no second YouTube channel before the YPP application.** Instead, add Spanish (then Portuguese) **audio tracks to our existing Shorts**, starting with the top 10 by engaged views. Revisit a separate channel at day 30.
- **What multi-language audio does** [OFF](https://support.google.com/youtube/answer/13338784):
  - It lets you upload extra audio tracks "to a single video **or Short**". Viewers get their language automatically.
  - It requires **Advanced features** (phone verification plus history; Nolan checks Studio > Settings > Channel > Feature eligibility).
  - It's added by hand in Studio desktop > Languages > Add language > Dub > upload audio. That is a Nolan task: Metricool can't do it.
  - Localized thumbnails are long-form only.
- **Auto-dubbing** went to all creators in Feb 2026 in 27 languages, with ~6M daily viewers in Dec 2025, and "won't hurt discovery" [3P](https://ppc.land/youtube-auto-dubbing-tops-6m-daily-viewers-expands-to-27-languages), [OFF help](https://support.google.com/youtube/answer/15569972).
  - YouTube may already be auto-dubbing our uploads. Nolan checks Studio > Languages for "Automatic dubbing".
  - If our edge-tts dub is better, delete the auto dub first, then upload ours (required order, per the help page).
- **Evidence that dubbing grows views:**
  - YouTube's pilot: >25% of watch time on dubbed videos came from non-primary languages. Jamie Oliver's views were up 3x [OFF via PPC Land](https://ppc.land/youtube-makes-multi-language-audio-available-to-millions-of-creators/). That was long-form.
  - **Nothing Shorts-specific is published.** Kids' and "faceless Hindi/Spanish facts" success stories come only from dubbing vendors (AIR "125M views") [3P, vendor, weak].
  - No case study of a dubbed faceless animal *Shorts* channel turned up [gap].
- **Why one channel and not two** [I]:
  - All dubbed views and subs accrue to the channel we're trying to monetize.
  - A second channel starts at 0 again, splits our tiny audience, needs its own 10M/4,000 h, and puts the same visuals on two channels. The reused-content policy allows "content that primarily features the uploading creator", but YouTube has no line on one owner's identical videos across two channels [OFF](https://support.google.com/youtube/answer/1311392) [UNVERIFIED either way].
  - It doubles the template footprint a reviewer could read as mass production.
- **Gate for a Spanish channel at day 30:** go only if dubbed tracks show ≥15% of a Short's views in Spanish *and* the main channel has applied for YPP. Then re-shoot the Spanish Shorts with Spanish-native hooks, not literal translations.
- **Licence:** a Spanish edge-tts voice carries the same commercial-use doubt as English (research/30 R6). Use Azure Speech free tier voices (es-MX/es-ES, pt-BR) for dubs.
- **Quality bar:** a native speaker or a back-translation check on 3 dubs before batching. A wrong "fact" in Spanish is still a wrong fact.

## 3. Cross-platform: reach and rollout order
**Crossposting our own file is fine; crossposting someone else's isn't.**
- Meta (Mar 2026) deprioritises "duplicative" content and "minor edits to another creator's post" and can mark repeat offenders non-recommendable. Original Reels views doubled in H2 2025 [OFF](https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/).
- Instagram (Apr 2026) stops recommending accounts that *mostly* share content they didn't create, judged over a rolling window, and deprioritises other apps' watermarks [3P PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/).
- Our masters are self-produced, so we pass both [I]. **Upload the clean render, never a TikTok download** (no watermark).

| Order | Platform | Real reach for a new faceless animal account? | Why |
|---|---|---|---|
| 1 | **Instagram Reels** | Yes, medium | Non-follower Reels distribution is the norm. Originality rules favour us. Same 9:16 file. |
| 2 | **Facebook Reels** | Yes, medium-high [I] | Meta says original Reels views doubled. Older audience suits "myths you still believe". FB Content Monetization is invite-based [UNVERIFIED]. |
| 3 | **Pinterest** | Low but long-lived | Intent and search audience. Video pins carry an outbound link. Pin long-form YouTube URLs (embedded plays). Hard reach data for 2026 is missing [3P weak]. |
| 4 | **Threads** | Low | Text-first. Use it for one daily "myth of the day" text post plus a clip. ~400-500M MAU (figures conflict) [3P]. |
| skip | Snapchat Spotlight | Unknown | Not in Metricool. Monetization needs 50k followers + 25 posts/month (+ view-time floor since May 2026), and fully AI videos are reportedly excluded from payouts [OFF](https://newsroom.snap.com/snapchat-new-creator-monetization) [3P](https://www.shortsync.app/resources/snapchat-spotlight-monetization-2026). Revisit at day 30. |
| skip | LinkedIn, Bluesky | No | Wrong audience. |

**Exact setup (Nolan, once, about 30 min; menu names may differ slightly [UNVERIFIED UI]):**
1. Instagram app: create @meatballmyths. Settings > Account type and tools > **Switch to professional > Creator**, category "Education" or "Science & Technology". Bio: "Animal myths, busted daily. Full quizzes ↓" plus the YouTube link.
2. Facebook: create a **Page** "Meatball Myths" (category Education). Link it to the Instagram account in Meta Accounts Center.
3. Metricool > the Meatball brand > **Connections**:
   - connect **Instagram** (log in via Facebook; approve every permission, including content publishing);
   - connect the **Facebook Page** (pick the Page, not the profile);
   - connect **Pinterest** (convert to a free Business account first), and create boards "Animal Myths Busted" and "Weird Animal Facts";
   - connect **Threads** (via the Instagram login).
4. Metricool post defaults:
   - IG type **Reel**, "Also share to feed" ON, autopublish (not notification);
   - Facebook type **Reel**;
   - turn OFF Instagram's in-app "share to Facebook" so the Page doesn't get the Reel twice.
5. Per post: write a platform-specific caption (it's text, so it's AUTO for the Scheduler), use 3-5 hashtags on IG, leave a first comment with the question, and no YouTube CTA inside Meta captions.
6. Stagger posting: TikTok first; IG/FB 2-4 h later; YouTube only after the TikTok gate (§6). Pinterest the next day.
7. Week 1 check: if IG stays under 200 views/Reel after 10 Reels, keep posting at 1/day as a drip and move the effort back to TikTok/YouTube.

## 4. Trend-jacking playbook (same-day Shorts)
There's no 2026 benchmark for how fast a trend Short must post. YouTube's own trend series calls newsjacking "tried and true" [3P](https://www.socialmediatoday.com/news/youtube-highlights-latest-shorts-trends/689510/). Our 2-minute render is the edge; scripting and fact-checking are the bottleneck.
1. **Scan, twice a day (08:00 and 15:00 ET), AUTO via a script plus a scout agent:**
   - Google Trends "Pets & Animals" and realtime searches;
   - the YouTube search autocomplete delta (research/29 §3);
   - TikTok Creative Center trending hashtags;
   - news RSS (AP, BBC Science, Reuters "animal"), plus Reddit r/nottheonion and r/natureisfuckinglit top/day (read-only).
2. **Filter** (all must pass):
   - two reputable outlets confirm it;
   - a myth or misconception angle exists ("Everyone's sharing the bear in the pool. Can you outrun a bear?");
   - no human death or injury is the hook;
   - no politics;
   - the species has CC0/CC BY photos on iNaturalist.
3. **Angle, not report:** we don't cover the news. We answer the myth the news raises.
   - Claim-first hook, with the animal in the first 2 words (research/28 §2).
   - Title = the exact phrase people are searching ("Can Octopuses Really Escape Tanks?").
4. **Never use** news photos, news video, or the real animal's photo from the article. Use iNat photos of the species only. No realistic AI footage.
5. **Ship within 6 h of detection**, and TikTok first. The trend Short takes one of the 3 YouTube slots (no extra upload). Max 1 trend Short a day.
6. **Fact gate:** a `sources` URL is required (research/30 R11). If the story turns out false, the Short becomes "This viral video is fake. Here's why", or we kill it.
7. **Follow-up:** if it beats 3x median at 24 h, apply research/31 #2 (3 more and a long-form Part 2 the same week).

## 5. Collab and community growth
- **YouTube reply-with-a-Short** to real comments (iOS/Android; the comment sticker shows on the video) [3P](https://www.socialmediatoday.com/news/youtube-adds-new-option-to-reply-to-video-comments-with-shorts/632011/):
  - 1 a day: "You asked: do sharks sleep?". It's the most authored-looking thing we can post, which helps at review.
  - It's a NOLAN step, because the pipeline renders and Nolan attaches it in the app.
  - Voice replies to comments are open to all creators (Feb 2026) [3P].
- **TikTok reply-to-comment videos:** the cheapest proven TikTok format, and personal stakes drive comments (research/28 §4). Seed the ask in the pinned comment: "Which myth did your grandma swear by?"
- **TikTok stitches:** stitch viral wrong animal claims ("this is a myth, here's the science"). The intro clip belongs to someone else, so **stitches stay on TikTok only**. Never repost them to YouTube, IG or FB (reused / unoriginal). Duets have little use.
- **Shorts "remix" (Green Screen, Cut) of other creators' animal Shorts:** allowed by YouTube's tools, but it puts others' footage on our channel ahead of review. **Skip until after YPP approval** [I].
- **Instagram Collab posts** with small animal-education accounts (5k-50k): cross-audience reach. Offer a free myth Short with their animal. 1 a week, Nolan DMs.
- **"Viewer myths" series:** a numbered "You Asked #N" that answers submitted myths. It gives a reason to subscribe (research/29 #2).

## 6. The single most leveraged bet for the next 14 days
**Make TikTok the lab and YouTube the showroom.**
- TikTok goes to 5 a day of claim-first originals (Buffer: the tail roughly doubles from 2-5 to 11+ posts a week).
- YouTube's 3 daily slots go only to the Shorts that won on TikTok.
- **Gate:** top third by 24 h TikTok completion rate and shares, measured against our 14-day median.
Why this one:
- It multiplies shots where volume is rewarded and paid (Creator Rewards). It also concentrates YouTube on proven hooks, attacking the 40% stay rate, which is the real YouTube bottleneck (research/26 §7).
- It keeps YouTube cadence flat and varied, which is the best defence against 2026's anti-slop systems and the channel-wide YPP review.
- It costs no new code, because the pipeline already renders both. The Scheduler just delays the YouTube post by 24 h and picks by the TikTok number.
- Each extra TikTok post is a measured hook experiment (research/27 F5 "tested ~20 hooks before popping off").
Measure:
- the YouTube stayed-to-watch % of TikTok-gated Shorts against ungated ones (target ≥55% at day 7);
- the TikTok p90 views per week.
[I] TikTok and YouTube audiences differ, so the gate is a filter, not a guarantee. Re-check the correlation on day 14.

Runner-up: Spanish audio tracks on the top 10 Shorts. It's cheap and adds no uploads, but its Shorts reach is [UNVERIFIED].

## 7. Risk notes
- **YPP review (P0):** every scale move must lower template sameness, not raise it. No second channel, no remixes of others, no stitches crossposted, and no more than 3 Shorts a day on YouTube before applying (research/30 R2/R3).
- **TikTok income (P1):** 5 a day risks repetitive-looking feeds.
  - Rotate hooks, loop lines and CTAs.
  - Keep the AI label on, since our voice is realistic (research/30 R4).
  - Never put YouTube asks inside TikToks.
  - If the 7-day average views per post drop more than 30%, go back to 3 a day.
- **Meta originality (P1):** only clean in-house renders. Never post TikTok-watermarked or stitched files.
- **Fact risk (P1):** trend Shorts are fastest and least checked, so the sources field is mandatory. Kill a Short rather than ship it unsourced.
- **Licence (P1):** edge-tts commercial rights are unverified in every language, so move to Azure Speech before scaling dubs (research/30 R6). Use CC0/CC BY photos only on new platforms (R5).
- **Made for kids (P1):** a cartoon mascot on IG and FB is fine, but YouTube's not-made-for-kids setting must already be set (R7).
- **Ops (P2):** a `data/posted.csv` ledger across 6 platforms, so nothing double-posts (R9).
- **Unverified in this file:**
  - TikTok's 2026 Creator Rewards length and AI rules;
  - Metricool's exact menu names;
  - Shorts-specific results of dubbed audio;
  - the Snapchat thresholds;
  - Pinterest and Threads 2026 reach data.

