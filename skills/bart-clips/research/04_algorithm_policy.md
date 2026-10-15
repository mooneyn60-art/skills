# 04 — YouTube Shorts algorithm and policy for a Joe Bartolozzi fan/clip channel (researched 2026-10-15)

Legend: **[OFFICIAL]** = YouTube/Google/Meta/Whop first-party. **[SECONDARY]** = press/blog reporting. **[UNVERIFIED]** = vendor blog, user content or unconfirmed. **[OLD]** = source predates 2025.

---

## 0. The biggest news for this project (read first)

- **Oct 1, 2026: YouTube is changing Shorts recommendations to favor original content and cut reach for re-uploads.** In a TeamYouTube Help Community post titled "Prioritizing original content on Shorts", YouTube says it will "reduce the reach of content re-uploaded from other creators without adding anything of your own". It also says "channels identified as primarily aggregating or re-uploading other creators' videos without significant changes" will "likely see less distribution". Changes that don't count: "minor technical edits or template-based changes simply to alter a video". [OFFICIAL, quoted via SECONDARY] — https://ppc.land/re-uploaded-shorts-lose-reach-as-youtube-favours-original-clips/ ; https://www.dexerto.com/youtube/youtube-cracks-down-on-clipping-channels-in-shorts-update-prioritizing-original-content-3415700/ (2026-10-05)
- **Oct 1, 2026: Rene Ritchie (Creator Liaison) explained it on Creator Insider.** Someone remixing another creator's clip has to add their own value, "not just VO descriptions of what's happening on screen, minor technical edits, or template-based bulk changes". Ritchie said a channel that shifts toward original content gets its reach re-evaluated. To share someone else's video, he suggested the Posts tab. [OFFICIAL video, via SECONDARY] — https://www.youtube.com/watch?v=XS2A6aExLaA ; https://searchenginejournal.com/youtube-original-shorts-reposted-clips-reach/591774/
- **No start date has been published.** YouTube hasn't said how much change is "significant", and affected channels get no notice. The only sign is falling Shorts-feed reach. [SECONDARY] — https://outlierkit.com/resources/youtube-shorts-original-content-update/
- **Whether permission protects a clip is unclear.** The October post doesn't mention permission or clipping programs. The reused-content monetization policy says it "applies even if you have permission from the original creator" (see section 2). **Assume Joe's permission doesn't exempt raw re-uploads from either the reach cut or demonetization.**

---

## 1. How Shorts are distributed (2026)

| Claim | Date | Source | Grade |
|---|---|---|---|
| Each Short is shown to a small "seed" group first, and reach widens or narrows based on how they respond. Todd Sherman (Shorts product lead): "Find a set of people that may enjoy your video"; "The audience is the algorithm." | 2023-08-23 | https://www.youtube.com/watch?v=n3jsYK_-aRU (summary: https://outlierkit.com/resources/youtube-shorts-algorithm/) | OFFICIAL, **[OLD]**, still the most recent official explanation found |
| YouTube has **not published** Shorts signal weights. Third-party claims like "40% swipe-away in 3s kills reach" or "70% watch-through" are not confirmed. | 2026 | https://outlierkit.com/resources/youtube-shorts-algorithm/ ; https://vidiq.com/blog/post/youtube-shorts-algorithm/ | SECONDARY / UNVERIFIED benchmarks |
| Studio shows "Viewed vs. Swiped away" (the share of viewers who stayed past the opening rather than swiping), the best available proxy for the first-seconds filter. | ongoing | https://www.creatoressentials.com/glossary/stayed-to-watch/ | SECONDARY |
| **Views count from the first frame (Aug 24, 2026).** A view counts the moment playback starts, across Shorts, long-form and live. Shorts already worked this way from **Mar 31, 2025**. The old stricter metric stays in Analytics (Advanced) as **"engaged views"**. Monetization and YPP eligibility still use **engaged/qualified** views. | announced 2026-08-17, effective 2026-08-24 | https://support.google.com/youtube/thread/433409976 (TeamYouTube) ; https://ppc.land/youtube-counts-views-from-the-first-frame-across-all-formats-on-august-24/ ; https://daringfireball.net/linked/2026/09/18/youtube-view-counts | OFFICIAL via SECONDARY |
| Practical upshot: public view counts are inflated. Judge performance by **engaged views, the viewed/swiped ratio and average % viewed**, not public views. | 2026-08 | same | inference |
| **Posting frequency:** there is no hidden threshold. "There is nothing in our systems that's like when you hit the five video or 10 short threshold…" Deleting and re-posting a Short "risks being seen as spam". | 2023-08-23 | https://www.youtube.com/watch?v=n3jsYK_-aRU&t=345s ; &t=443s | OFFICIAL **[OLD]** |
| **Time of day:** "not something that we think about optimizing for." | 2023-08-23 | &t=327s | OFFICIAL **[OLD]** |
| **Length:** there's no ideal length ("To what length do you need to tell your story?"). The maximum is **3 minutes** for Shorts uploaded on/after **Oct 15, 2024**. | 2023-08-23 / 2024-10-15 | https://support.google.com/youtube/answer/15424877 | OFFICIAL |
| **Shorts over 60s with any active Content ID claim are blocked globally:** they can't be played, recommended or monetized, though the channel isn't penalized. Shorts of 60s or less are not affected by this rule. | current Help page | https://support.google.com/youtube/answer/15424877 | OFFICIAL — **key reason to keep clips ≤60s** |
| Likes, shares, comments and subs as ranking signals: no official weighting published. Third-party guides assert them. | 2026 | vidIQ / quso.ai blogs above | UNVERIFIED |

---

## 2. Monetization: YPP thresholds and the reused/inauthentic content policy

**Current thresholds** (Help page, checked 2026-10-15): 1,000 subs plus either 4,000 qualified watch hours in 12 months or **10M qualified Shorts views in 90 days**. — https://support.google.com/youtube/answer/72851 [OFFICIAL]

**Changes announced 2026-08-10, effective 2027-02-01** — https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/ [OFFICIAL]:
- New applicants need 1,000 subs plus **8,000 watch hours/365d** or **20M qualified Shorts views/90d** (double the current figures).
- **Every channel, including existing partners,** needs **10M qualified Shorts views per trailing 90 days** to earn Shorts ad and Premium revenue share. Below that, the channel stays in YPP and keeps long-form earnings.
- Existing partners must accept the updated modules in Studio by **2027-01-31**.
- Revenue split is unchanged: 45% for Shorts, 55% for long-form.
- Incentives (Shopping bonuses, brand deals, trend boosts) for channels under 10M are promised but not detailed.
- Activity test from 2027-02-01: the channel needs one of 1,000 watch hours/365d, 1M Shorts views/90d, or 2 long-form or 5 Shorts uploads per 90d. [SECONDARY] — https://outlierkit.com/resources/youtube-partner-program-changes-2027/
- The fan-funding tier (500 subs plus activity) is reported unchanged. [SECONDARY, same]

**Reused content policy** — https://support.google.com/youtube/answer/1311392 [OFFICIAL; latest dated notice on the page is 2025-07-15]:
- The policy targets channels that "repurpose content that's already on YouTube or another online source" without meaningful added value. The test is whether "viewers can tell that there's a meaningful difference".
- "This policy applies **even if you have permission** from the original creator." It is separate from copyright, so a channel can be demonetized with zero claims.
- Allowed: clips used for critical review, and reactions where you comment on the original.
- Not allowed: moments "edited together with little or no narrative", compilations of short videos from other social sites, and reactions that are mostly non-verbal.
- **July 15, 2025:** YouTube renamed "repetitious content" to **"inauthentic content"**, covering mass-produced/templated, near-duplicate, and slideshow/scrolling-text content with minimal narrative or commentary. YouTube called it a clarification, not a new rule. Clips, compilations and reactions still fall under reused content. [OFFICIAL + SECONDARY] — https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/ ; https://www.exchange4media.com/digital-news/youtube-issues-clarification-on-monetisation-policy-update-after-creator-backlash-145327.html

**Shorts monetization policy** — https://support.google.com/youtube/answer/12504220 [OFFICIAL]:
- Views that don't earn revenue include "reuploading other creators' content from YouTube or other platform", "unedited clips" and "compilations with no original content added".
- Bot/artificial views are also excluded.
- Views earned before you accept the Shorts Monetization Module don't count.

**What a Joe clip channel has to add, per YouTube's own wording:** your own commentary or voice, a critique or perspective, narrative or storytelling (setup, context, punchline framing), or meaningfully unique editing. These don't qualify: plain captions and reframing, voice-over that only narrates what's on screen, minor technical edits (crop, speed, mirror, zoom), template-based bulk edits, or stitching moments together with no narrative.

---

## 3. Copyright

- **Content ID claim vs. copyright strike.** A claim usually blocks or redirects monetization and doesn't cause a strike. A strike comes from a legal removal request. Three active strikes within 90 days means the channel is terminated. A strike expires after 90 days, provided Copyright School is done. If removal was "scheduled", you have 7 days to delete and avoid the strike. Disputing a claim without a valid reason can lead to a takedown and a strike. — https://support.google.com/youtube/answer/2814000 [OFFICIAL]
- **Fair use.** Content ID can't decide fair use; only courts can. A claim stops monetization "even if you only use a few seconds". Dispute → appeal → DMCA counter-notification. — https://support.google.com/youtube/answer/9783148 [OFFICIAL]. Raw clips with captions are weak fair use. Commentary or critique is the defensible shape. (General law; not legal advice.)
- **Shorts over 60s with an active claim are blocked globally** (see section 1). — https://support.google.com/youtube/answer/15424877 [OFFICIAL]
- **Third-party music:** Shorts of 60s or less can use the Shorts audio library. For longer Shorts, use the royalty-free YouTube Audio Library. — https://support.google.com/youtube/answer/13486873 [OFFICIAL]. Joe's stream VODs may contain copyrighted music or game audio that triggers claims from third parties, not from Joe.
- **How official/approved clipping programs work** (Whop and similar): the creator funds a campaign and sets per-1k-view rates, eligible platforms and requirements. Clippers submit, the creator approves, then payment follows. — https://docs.whop.com/memberships-and-access/third-party-apps/content-rewards [OFFICIAL Whop, undated]. Campaigns usually require credit tags and clipping only from authorized sources, and they reject miscredited clips. [UNVERIFIED vendor] — https://openclip.app/guides/get-paid-to-clip-streamers.md
  - A program gives you a **license against strikes from that creator**. It does **not** exempt you from YouTube's reused-content monetization policy ("applies even if you have permission") or, apparently, from the Oct 2026 originality ranking change.
- **Joe Bartolozzi's stated position on clip channels:** **none found** (searched 2026-10-15). There's no public statement, official clip channel, or clipping campaign from him or his team.
  - Fan channels exist: "Clip That Joe Bart" (https://www.youtube.com/@ClipThatJoeBart/shorts) advertises "manually selected, cut, and edited… no reuploads"; "jynxzi&bartolozziclips" (https://vling.net/channel/UC6BfARTPllDG1IjDJvM7dMg/channel-info); and an unofficial VOD re-upload podcast (https://open.spotify.com/show/033TwuoMbfw6gMOV740Wt6).
  - A TikTok claims a "Joe Bartolozzi copyright lawsuit" (https://www.tiktok.com/@joeclipper0/video/7642186767336066318). **[UNVERIFIED]**, with no article or court record found.
  - His main channel is @joebartolozzi. Social Blade shows ~5.44M subs (https://socialblade.com/youtube/handle/joebartolozzi/videos); the "6M" figure is unverified. His Twitch is Joe_Bartolozzi.
  - **Action:** contact his team for written permission or an official campaign before monetizing; record his response.

---

## 4. Titles, cover frames, hashtags, captions

- **Hashtags** — https://support.google.com/youtube/answer/6390658 [OFFICIAL]:
  - Content with more than 60 hashtags has all of them ignored.
  - Up to 3 hashtags show near the title.
  - Unrelated or misleading hashtags and over-tagging can get content removed from search or uploads.
  - In Shorts, YouTube suggests hashtags as you type #.
  - Hashtags are "not required" for Shorts. — Todd Sherman, 2023-08-23 [OFFICIAL **OLD**]
  - Practice: 1–3 accurate tags, e.g. #joebartolozzi #shorts plus one topic tag. Using Joe's name is accurate and not misleading, provided the channel is clearly labeled as a fan channel (see Rules).
- **Thumbnails / cover frames:**
  - "Most thumbnails are never seen because people are in the feed." — Sherman, 2023-08-23 [OFFICIAL **OLD**]
  - **Custom Shorts thumbnails began rolling out 2026-07-25.** They're YPP-only at first and uploaded on desktop. They appear on Home and on the channel's Shorts/Home tabs, **not in the Shorts feed**, and A/B testing isn't available. — https://ppc.land/youtube-ends-2-year-wait-for-shorts-thumbnails-but-blocks-a-b-testing/ (2026-07-26) [SECONDARY citing Creator Insider]
  - Non-YPP channels choose a frame in the app. → The **first frame/hook matters more than the cover**.
- **Titles:** no YouTube official found any title guidance specific to Shorts. Vendor advice is to front-load the first ~50 characters shown on mobile. [UNVERIFIED] — https://hashtagtools.io/blog/youtube-shorts-character-limits-title-description-hashtags-2026
- **On-screen captions:** no official ranking evidence. They help retention in sound-off viewing (industry consensus, unverified). Under the Oct 2026 rules, captions alone **do not** count as added value.

---

## 5. Cross-posting to TikTok and Instagram Reels

- **YouTube:** no official statement found that cross-posting the same clip, or a TikTok watermark, lowers Shorts reach. YouTube watermarks Shorts downloaded from Studio for attribution, not ranking (2022 **[OLD]**). — https://techcrunch.com/2022/08/18/youtube-shorts-will-start-adding-watermarks-to-discourage-cross-platform-sharing/amp/. The Oct 2026 rule targets **re-uploading other creators'** content, not your own cross-posts.
- **Instagram:**
  - Since 2021 [OLD], Reels carrying other apps' watermarks are not recommended (they still reach followers). Mosseri says your own logo is fine. — https://www.socialmediatoday.com/news/instagram-clarifies-that-including-your-own-logo-on-a-reel-is-ok/730852/
  - **April 2026:** Instagram extended its anti-aggregator rule platform-wide. Accounts that mostly share content they didn't create or "meaningfully transform" aren't recommended to non-followers. — https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/ [SECONDARY; page returned 403, summary via search]
- **TikTok:** the Community Guidelines include "FYF Ineligible" content (not recommended, but stays up). Unoriginal or low-quality reuploads from other platforms, and watermarked reposts, are reported as FYF-ineligible. — https://conductatlas.com/platform/tiktok/tiktok-community-guidelines/for-you-feed-eligibility-exclusion/ ; https://onlineoptimism.com/blog/updates-tiktoks-community-guidelines [SECONDARY; verify on tiktok.com/community-guidelines]
- **Practice:** export a **clean master with no watermark** from the editor and upload it natively to each platform. Never download from one platform and re-upload to another. Vary the hook text or caption per platform. All three platforms now penalize the "aggregator" pattern, so the transformation requirement applies everywhere.

---

## 6. Paid clipping marketplaces (Oct 2026)

- **Whop Content Rewards:** the creator sets a per-1k-view rate, a budget and a per-video cap. Payout follows approval. Platforms are TikTok, YouTube Shorts, X and IG Reels. — https://docs.whop.com/memberships-and-access/third-party-apps/content-rewards [OFFICIAL]
  - Live rates are typically ~$0.50–$1.50/1k (Whop advertises an ~$1 average). The range is roughly $0.20–$6, and streamer campaigns usually run $1–3. A ~7–10% fee and a hold period are reported. — https://www.clipaffiliates.com/blog/clipping-cpm-rates-2026 ; https://www.clipspeed.ai/blog/whop-content-rewards-clipping-guide.html ; https://openclip.app/guides/get-paid-to-clip-streamers.md [UNVERIFIED vendors]
- **Kick streamer campaigns:**
  - N3on reportedly paid $1.4M to 303 clippers over 5 weeks (~$40/100k views). — https://www.tubefilter.com/2026/04/29/n3on-spending-millions-stream-clippers-tiktok-kick/amp/ (2026-04-29) [SECONDARY]
  - Clavicular says Kick spent ~$700k on his clips in one month. — https://www.dexerto.com/kick/clavicular-says-kick-spent-nearly-700000-promoting-his-clips-in-a-single-month-3393030/ [SECONDARY, self-reported]
- **Joe Bartolozzi campaign:** **none found** on Whop, ClipAffiliates or in press (searched 2026-10-15). The Whop discover page didn't render campaign listings to the fetcher, so manually check whop.com Content Rewards and clipaffiliates.com for "Bartolozzi" before concluding.
- **Twitch-specific campaigns:** no confirmed October 2026 Twitch-streamer campaign found. Coverage is dominated by Kick and by brand/casino campaigns (e.g. Roobet ~$1.50/1k [UNVERIFIED]).
- **Caveat:** the Oct 2026 YouTube originality change will likely reduce Shorts-feed reach for raw campaign clips too. Campaign approval doesn't override YouTube ranking.

---

## Rules we must follow

1. **Never post raw or near-raw re-uploads.** Every Short needs our own commentary or voice, critique, narrative framing, or substantive original editing. Captions, reframing, crop, zoom, speed changes, mirroring, templates and narrate-what-you-see voice-over do **not** count (YouTube 2026-10-01; Reused Content policy).
2. **Keep each Short ≤60 seconds** unless we're certain there are no third-party claims. Over 60s, any active Content ID claim blocks the Short globally.
3. **Don't let the channel be "primarily" re-uploads.** Track the mix of raw, transformed and original content. Use the Posts tab, not Shorts, to point viewers to Joe's own videos.
4. **Permission ≠ monetization.** Get written permission or join an official campaign to avoid strikes, but meet the reused-content standard anyway, because that policy applies even with permission.
5. **Avoid strikes:** don't file bad-faith disputes, take Copyright School after any strike, and take down within 7 days when YouTube offers it. Three strikes in 90 days terminates the channel.
6. **Label clearly as a fan/clip channel** (e.g. "Fan clips — not affiliated with Joe Bartolozzi"), credit and link Joe in every description, and never impersonate his branding or name.
7. **Hashtags:** 1–3 relevant ones, never misleading, never more than 60.
8. **Don't delete and re-post Shorts** to "retry" them. YouTube says this risks spam classification.
9. **Measure with engaged views**, viewed vs. swiped away, and average % viewed. Public views are inflated by first-frame counting since 2026-08-24.
10. **Watch Shorts-feed reach weekly** in Studio, since YouTube sends no notice when the originality demotion applies.
11. **Cross-post clean masters natively** with no other platform's watermark, and vary hooks per platform. IG and TikTok also demote aggregators.
12. **No view botting or engagement buying.** Artificial views are excluded from monetization and violate spam policy.
13. **Plan monetization around the 2027 rules:** 20M qualified Shorts views/90d to join, and 10M/90d to keep Shorts revenue from 2027-02-01. Consider long-form commentary compilations as the long-form path.
14. **Avoid third-party music** in edits except from the YouTube Audio Library or Shorts audio library within its limits. Trim copyrighted music that appears in stream VOD audio.
