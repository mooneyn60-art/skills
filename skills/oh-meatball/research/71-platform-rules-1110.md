# 71 — Platform rules check (TikTok Creator Rewards, YouTube YPP / Shorts / Hype), as of 2026-11-10

Channel: Meatball Myths (about 1,000 YouTube subs; TikTok @meatballmyths; AI-assisted animation, TTS voices, every upload flagged AI).
Method: each page below was fetched directly on 2026-11-10 and read in full. YouTube Help pages and TikTok Support pages show **no "last updated" date**, so "date seen" means "no date shown; fetched 2026-11-10". Where a page does show a date, it is given. Search-engine summaries were used only to find URLs, never as evidence.
Tiers: **[PRIMARY]** = the platform's own page. **[SECONDARY]** = third party. Anything not opened is marked "not opened".

## Contradictions with the working assumptions

| Assumption | Verdict |
|---|---|
| (a) CRP needs 10K followers + 100K views/30d, pays only on videos over 1 min | **Confirmed**, with extra conditions (Q1): videos must be at least 1 minute, reach 1,000 qualified For You views, and be posted after approval. |
| (b) YPP = 1,000 subs + 4,000 hours; Shorts-feed views don't count toward hours | **Confirmed**, but incomplete. (1) The bar for NEW applicants rises on **2027-02-01** to 8,000 hours or 20M Shorts views. (2) A separate 500-sub tier exists (fan funding and Shopping, no ad revenue). (3) Shorts-feed watch time does not count toward hours, as you assumed. |
| (c) A Short needs about 70% "stayed to watch" to get past about 1,000 viewers | **No official basis.** YouTube publishes no threshold and no benchmark, and says to compare your own Shorts with each other. |
| (d) Related video link is Studio-only, channel owner only, not API | **Half right.** Studio-only is consistent with the docs, and the Data API `videos` resource documents no related-video field. But no page says "owner only". It needs advanced-features access. |
| Claim: long-form views count from the first frame from 2026-08-27 | **Date is wrong.** The Help page and YouTube Blog say **2026-08-24**. "August 27, 2026" is the date of the Data API changelog entry. It covers all formats, not just long-form. |

---

## 1. TikTok Creator Rewards Program (US) and other TikTok money

**Answer.** Eligibility is unchanged: at least 18, personal account in good standing (no Business or political accounts), at least 10,000 authentic followers, at least 100,000 authentic video views in the 30 days before applying, a linked payment account and tax onboarding, and residency in an eligible country (the US is one). Only videos of **1 minute or longer**, posted **after approval**, earn. They must be original, reach 1,000 qualified For You feed views, and not be a Duet, Stitch, Photo Mode post or sponsored. A qualified view is a unique view from the For You feed with at least 5 seconds watched (search views need 30 seconds or more), excluding "not interested", paid, promoted and artificial views; repeat views from one account count once. Neither the US terms nor the Creator Academy/Support pages **name AI-generated or TTS content as excluded**. The exclusion that matters is "Unoriginal: copied or minimal original input or edits", plus "Low quality: split screens, meaningless reactions, low-quality images, slide videos". Where the exact line falls for AI-assisted animation is not published, and the Creator Academy "Understanding TikTok's Originality Policy" article was not opened.
No successor program found; the Creator Rewards terms were last updated **2026-07-20**. Payout minimum conflicts between sources: US terms say $50, the Support page says $10; the US terms are the legal text.
Below-threshold money: **LIVE Gifts** needs no follower minimum (18+, eligible to go LIVE, good standing, available location). **Series** (paywalled playlist): 18+, account 30+ days old, 3+ public posts in 30 days, 10,000+ followers, 1,000+ views in 30 days, original content; under 10K followers you can apply with a link to premium content sold elsewhere. **Subscription**: 18+, good standing, 10K followers and 100K views in the past calendar month, or specific LIVE eligibility (from a 2024 newsroom post; current numbers should be checked in TikTok Studio, Monetization). TikTok One (branded content) videos cannot also earn Creator Rewards.
TikTok AI label: for fully AI-generated content that is realistic, labeling is required; the post-time setting "won't affect the distribution of your video as long as it doesn't violate our Community Guidelines". Stylized animation is "AI-generated content" under TikTok's definition (it lists cartoons and anime) but the **mandatory** label applies to realistic content.

**Sources**
- Creator Rewards US terms, "Last Update: July 20, 2026": https://www.tiktok.com/legal/page/global/creator-rewards-program-us/en [PRIMARY]
- Creator Academy, Creator Rewards Program, "Last updated: Sep 10, 2026" (rendered with headless Chrome): https://www.tiktok.com/creator-academy/article/creator-rewards-program [PRIMARY]
- TikTok Support, How rewards work, no date shown: https://www.tiktok.com/support/faq_detail?id=7543897461245450808 (redirect target of https://support.tiktok.com/en/business-and-creator/creator-rewards-program/how-rewards-work) [PRIMARY]
- Newsroom, "Introducing the New Creator Rewards Program", March 18, 2024: https://newsroom.tiktok.com/introducing-the-new-creator-rewards-program?lang=en [PRIMARY]
- TikTok Support, About AI-generated content, no date shown: https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content [PRIMARY]
- Community Guidelines, Integrity and Authenticity, no date shown: https://www.tiktok.com/safety/en/policies-and-engagement/integrity-authenticity [PRIMARY]
- LIVE Gifts, no date shown: https://www.tiktok.com/support/faq_detail?id=7543897462415579704&category=web_account [PRIMARY]
- Series eligibility, no date shown: https://www.tiktok.com/support/faq_detail?id=7639210131833756180&category=web_account [PRIMARY]
- Subscription expansion, Newsroom, September 23, 2024: https://newsroom.tiktok.com/en-us/empowering-creators-and-fostering-communities-with-the-expanded-subscription-feature [PRIMARY]

**What this means for us:** TikTok Rewards needs 10K followers first, so the near-term TikTok job is follower growth plus 1-minute-plus originals; the AI/TTS question is a grey zone that only an application will answer.
**Confidence:** Thresholds, qualified view, 1-minute rule: confirmed by primary source. AI/TTS eligibility: could not confirm (not named either way; originality rule is the only hook). Subscription current thresholds: primary but 2024-dated, needs in-app check.

---

## 2. YouTube Partner Program thresholds

**Answer.** Full tier (ads, Premium revenue): 1,000 subscribers plus either 4,000 qualified watch hours in 12 months or 10M qualified Shorts views in 90 days, plus no active strikes, 2-Step Verification, and an AdSense link. Early tier (US is on the country list): 500 subscribers plus 3 valid public uploads in 90 days plus either 3,000 qualified watch hours in 12 months or 3M qualified Shorts views in 90 days; it unlocks fan funding, Shopping and creator partnerships, **not ad revenue**. **Shorts-feed watch time does not count toward the 4,000 hours**; qualified hours come from public long-form videos (including podcasts and archived livestreams) only, and qualified Shorts views must be engaged views (not loops). YouTube has **no explicit statement** about long-form watch that starts from a Short's related-video link. By the written definition (public long-form watch time) it would count, but that is inference.
**New since your assumption:** starting **2027-02-01**, new-applicant ad thresholds become 1,000 subs plus 8,000 qualified hours (365 days) or 20M qualified Shorts views (90 days). The 500-sub tier is explicitly unchanged. Existing members are not affected. Also from 2027-02-01, existing members need 10M qualified Shorts views per 90 days to earn from the Shorts Creator Pool each month. Review takes about a month; a rejected channel can re-apply after 30 days (90 days if repeated).

**Sources**
- YPP overview & eligibility (banner about 2027-02-01 terms), no date shown: https://support.google.com/youtube/answer/72851?hl=en [PRIMARY]
- Changes to the YPP (2027-02-01 updates), no date shown: https://support.google.com/youtube/answer/12843009?hl=en [PRIMARY]
- Overview of the expanded YPP (500-sub tier, country list incl. US), no date shown: https://support.google.com/youtube/answer/13429240?hl=en [PRIMARY]
- YouTube Blog, "What are qualified watch hours and Shorts views", Rene Ritchie, Aug 12, 2026: https://blog.youtube/news-and-events/youtube-monetization-qualified-watch-hours-shorts-views/ [PRIMARY]

**What this means for us:** At ~1,000 subs, the hours path is the only realistic one, and there is a deadline: reaching 4,000 qualified hours and applying before 2027-02-01 avoids the 8,000-hour bar (check the Earn tab for status; whether a pending application is grandfathered is not stated).
**Confidence:** Confirmed by primary source, except the related-link watch-hours question (not addressed officially).

---

## 3. Inauthentic / repetitious / reused content; AI disclosure

**Answer.** The July 15, 2025 update renamed "repetitious" to "inauthentic" and clarified it covers "repetitive or mass-produced" content. It is a clarification, not a new rule. The newest dated entry in the channel-monetization changelog is still that one; nothing later is listed. Reviewers look at the channel as a whole, focusing on main theme, most viewed, newest, biggest watch-time share, metadata and About section. A channel is rejected when videos look templated and interchangeable. Listed examples include "characters put in the same situation over and over with the same outcome", "templated storylines with minimal narrative, commentary or educational value", and "AI-generated content made with generic or unoriginal templates giving the impression of mass production". What YouTube says is acceptable: same intro/outro with a different bulk, a series with recurring characters where each video has "a distinct storyline, focus, or concept", and "using AI to visualize a unique character and narrative you invented" or to edit scripts/make backgrounds. **TTS voice is not mentioned** as a problem; the page tests substance and variation, not tools. "AI Personas on sensitive topics" (health/legal/finance/politics) bans monetization; house-bug myths are outside it.
Disclosure: YouTube **requires** disclosure only for realistic AI content. Non-realistic animation need not be flagged (the page's own example: "AI-generated or altered animation in a fully animated video"). Over-disclosing is allowed. YouTube states: "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money." Animated/non-photorealistic AI content gets a label in the expanded description, not on the player. YouTube may auto-label (C2PA metadata, its own AI tools) and some auto-labels cannot be removed.

**Sources**
- YouTube channel monetization policies (July 15, 2025 entry shown at top; page otherwise undated): https://support.google.com/youtube/answer/1311392?hl=en [PRIMARY]
- Disclosing use of GenAI content, no date shown: https://support.google.com/youtube/answer/14328491?hl=en [PRIMARY]

**What this means for us:** The "TRUE or FALSE myth, verdict" quiz skeleton is the exact risk the policy describes, so vary the angle, story and evidence per episode; flagging every upload as AI is harmless to reach and money but unnecessary for non-realistic cartoons.
**Confidence:** Confirmed by primary source. How a human reviewer applies it to a given channel is not published.

---

## 4. Shorts distribution in 2026

**Answer.** Official ranking signals (Search & discovery tips, Shorts): when a Short is recommended, do viewers choose to watch, ignore it, or tap "not interested"; then "% of viewers who chose to view, avg. view duration and avg. % viewed to inform ranking"; then likes and post-watch survey results. Shares, loops/replays and comments are **not listed**. Ranking also depends on personalization, topic interest, competition and seasonality, and the Shorts feed "may tune up on the recency of content". **No benchmark exists** for viewed-vs-swiped (Studio calls it "How many chose to view" / "Stayed to watch"); YouTube only advises comparing your best and worst Shorts and same-format videos. The 70% figure is not from YouTube.
View counting: since 2025-03-31 a Short view counts every start or replay. From **2026-08-24** a view counts from the first frame for all formats (Shorts, long-form, podcasts, live; thumbnail hover-autoplay counts too). The old definition is renamed "engaged view" (clicked to watch or stayed past the initial seconds, not counting loops). YouTube says recommendations and YPP are unchanged, and CTR/AVD/retention still use engaged views.
Cadence and weak uploads: "There is no minimum posting cadence required"; "Shorts performance doesn't negatively impact long form Video recommendations"; "An individual video's underperformance does not penalize a channel overall" (long-term effect only if a given viewer keeps skipping your videos). Very short looping Shorts: **no official differential treatment found**. The only official point is that loops do not count as engaged views or qualified Shorts views.

**Sources**
- Search & discovery tips, Shorts, no date shown: https://support.google.com/youtube/answer/11914225?hl=en&co=YOUTUBE._YTVideoType%3Dshorts [PRIMARY]
- Content tab analytics tips, Shorts, no date shown: https://support.google.com/youtube/answer/12942217?hl=en&co=YOUTUBE._YTVideoType%3Dshorts [PRIMARY]
- Understand your content performance (engaged views, "Stayed to watch" = "past the initial seconds"), no date shown: https://support.google.com/youtube/answer/12220281?hl=en [PRIMARY]
- How engagement metrics are counted ("Beginning August 24, 2026"), no date shown: https://support.google.com/youtube/answer/2991785?hl=en [PRIMARY]
- YouTube Blog, "What are 'Engaged' Views", Aug 19, 2026: https://blog.youtube/inside-youtube/engaged-views-youtube-explained/ [PRIMARY]
- Data API revision history (2025-03-31 Shorts change; entry dated August 27, 2026): https://developers.google.com/youtube/v3/revision_history [PRIMARY]
- Good to know about recommendations, no date shown: https://support.google.com/youtube/answer/16559651?hl=en [PRIMARY]

**What this means for us:** Optimize the first seconds and average % viewed, not a magic percentage, and judge Shorts by engaged views since raw views now include every swipe-past.
**Confidence:** Confirmed by primary source for signals, counting change and cadence statements; "no benchmark" and "no loop treatment" are absence-of-evidence in official pages (Creator Insider videos were not opened).

---

## 5. Shorts "Related video" link

**Answer.** Still available in 2026 and still called **"Related video"** in Studio (Content, open the Short, pick a Related video, Save). It links to your Videos, Shorts or Live and appears as a clickable link under the channel handle. The target must be public or unlisted and follow Community Guidelines; the feature needs **advanced features access**. The YouTube Blog (Jul 14, 2026) recommends it, with a verbal/visual CTA in the last 5 seconds and a payoff in the first 5-10 seconds of the long video. The help page does not say who can set it (owner vs. Studio manager), so "channel owner only" is not documented. The Data API `videos` resource documents no related-video field, so API setting is not documented (cannot prove a negative). No official click-through data found.
Not verified from a page I opened: a search summary said the Clips and Shorts tool auto-adds the source video as the related video.

**Sources**
- Add a related video to your Shorts, no date shown: https://support.google.com/youtube/answer/14075157?hl=en [PRIMARY]
- YouTube Blog, "How to convert YouTube Shorts views into long-form channel growth", Jul 14, 2026: https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/ [PRIMARY]
- Data API videos resource (searched for a related-video property, none): https://developers.google.com/youtube/v3/docs/videos [PRIMARY]

**What this means for us:** Put a Related video on every Short that has a matching long-form, and measure it ourselves (Traffic source: Shorts / Suggested), since YouTube publishes no CTR.
**Confidence:** Availability, name, how to set: confirmed. API absence and owner-only: could not confirm (not documented either way). Click-through: couldn't confirm.

---

## 6. Test & Compare (now "A/B test titles & thumbnails")

**Answer.** It now tests **titles, thumbnails, or both**: up to 3 variants, desktop YouTube Studio only, needs advanced features. **Not available** for Shorts, scheduled lives, Premieres (until they convert to regular videos), made-for-kids, mature-audience or private videos; live archives work. The winner is chosen by **watch time share**, not CTR; results are Winner / Performed Same / Inconclusive (the first upload stays on "inconclusive"), usually done in a few days to 2 weeks. Changing the title or thumbnail mid-test stops it. YouTube suggests testing older videos first, and uses a small control group.

**Sources**
- A/B test titles & thumbnails, no date shown: https://support.google.com/youtube/answer/16391400?hl=en (same text at https://support.google.com/youtube/answer/13861714?hl=en) [PRIMARY]

**What this means for us:** Use it on the 4-6 minute long-forms only (never Shorts), and give each test clearly different packaging so it can declare a winner.
**Confidence:** Confirmed by primary source.

---

## 7. Hype, and recommendations for small/new channels

**Answer.** Hype lets viewers spend a limited number of free hypes (3 per week per blog) on a video within **7 days of publishing**; hype points rank videos on a weekly **country leaderboard** (top 100) in Explore, with a "small creator bonus" multiplier for fewer subscribers and a "Hyped" badge and Home filter. Eligibility: channel **in the YPP** with **500 to 500,000 subscribers**, in a listed country (US included). Ineligible videos: **Shorts**, unlisted/private, **made for kids**, age-restricted, copyright-claimed, "misleading, clickbait or sensational", live/Premiere while live. Creators can opt out in Studio. A ~1,000-subscriber channel qualifies if it is in YPP (the Hype card suggests it is; confirm in Earn). YouTube's own 2024 post says hyping "won't influence your YouTube recommendations and search results", so any reach comes from fans hyping plus leaderboard/badge exposure; **no data on reach gained** was found, and nothing 2026-specific from Creator Insider or the blog. Latest official Hype post found is Aug 26, 2025; promised interest leaderboards (gaming, style) were not confirmed shipped.
Small/new channel recommendations (official, undated): systems evaluate each video individually; one weak video does not penalize the channel; viewers are drawn to a niche and a "critical mass" of content, which helps the algorithm recommend the channel; monetization status does not affect recommendations; experimenting across formats does not confuse the algorithm.

**Sources**
- Hyping videos eligibility, availability & policies, no date shown: https://support.google.com/youtube/answer/15509925?hl=en [PRIMARY]
- YouTube Blog, "Hype: Giving fans a stake...", Sep 18, 2024: https://blog.youtube/news-and-events/youtube-hype/ [PRIMARY]
- YouTube Blog, "Hype goes global!", Aug 26, 2025: https://blog.youtube/news-and-events/hype-global-expansion/ [PRIMARY]
- Good to know about recommendations, no date shown: https://support.google.com/youtube/answer/16559651?hl=en [PRIMARY]

**What this means for us:** Hype is a small, fan-powered nudge for 4-6 minute long-forms in their first 7 days, so ask the audience to hype in the video and Short CTA, and confirm no video is marked made-for-kids.
**Confidence:** Eligibility and mechanics: confirmed by primary source. Actual reach effect and any 2026 change: couldn't confirm.

---

## Open items (not resolved)
- Whether the channel is in YPP (early or full tier) and whether any video is flagged "made for kids": check Studio, Earn tab and video settings.
- TikTok "Understanding TikTok's Originality Policy" article and any AI-and-rewards statement: not opened (slug not found).
- Creator Insider videos (e.g. "Viewed vs Swiped Away", community-video 273390203) were not opened; no staff benchmark found on the written pages.
