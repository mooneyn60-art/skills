# 29 — Distribution and funnel (The Connector, 2026-10-24)

Question: how do the ~5,600 views we already get turn into subscribers and long-form watch hours?
Builds on research/11, 17, 22 and 24; it doesn't repeat them. Evidence tiers: **[YT]** YouTube/platform
help or blog, **[3P]** named third-party data, **[SPEC]** inference. **AUTO** = we can do it (code,
Metricool, API). **NOLAN** = Studio or app by hand.

## 0. Reality check (read first)
- **The bar doubles on 1 Feb 2027.** From that date new YPP applicants need 8,000 watch hours in 12 months or 20M Shorts views in 90 days. Partners already in the program keep their status [3P: Shacknews, Relevant Audience, reporting YouTube's Aug 2026 announcement](https://www.relevantaudience.com/youtube/youtube-partner-program-thresholds-double-february-2027/). The real deadline is **31 Jan 2027, 99 days away**, and the 30-day goal is a stretch target inside it.
- **What counts** [YT Help 72851](https://support.google.com/youtube/answer/72851), [YT blog 2026-08-12](https://blog.youtube/news-and-events/youtube-monetization-qualified-watch-hours-shorts-views/):
  - Counts: watch hours from **public long-form** videos (podcasts included) and **archived** live streams.
  - Doesn't count: private, unlisted or deleted videos, ad views, Shorts, and live streams that weren't archived.
  - Shorts count only as **engaged views**, and loops don't count.
- **The 30-day math:** 4,000 h ÷ 30 days ≈ 133 h/day.
  - At 3.5 min AVD that is about 2,300 long-form views a day. Today we get about 0.
  - With 1-hour compilations at about 10 min AVD it drops to about 800/day.
  - **Raise watch time per viewer as well as views.** That is why compilations rank high below.
- **Subscribers:** Galloway's benchmark is 16.9 subs per 10k Shorts views and 22.7 per 10k long-form views [3P](https://insights.vaizle.com/?p=3156).
  - At that rate, 1,000 subs needs about 600k Shorts views. We are at 0 subs from 5.6k views.
  - **Subscriber conversion is the binding constraint, ahead of reach.** Fix the reason to subscribe first.
- **The vidIQ reserve is breached:** 3 credits left against the ≥400 standing order, renewing 10 Nov. This research used no vidIQ credits.
  - Keyword work below uses free YouTube autocomplete (`suggestqueries.google.com`, `ds=yt`).

## 1. Ranked plan (impact ÷ effort, highest first)
| # | Action | Who | Effort | Impact | Evidence |
|---|---|---|---|---|---|
| 1 | Related video on **every** Short → the episode that contains that myth; the Short ends on a verbal + visual "full quiz, tap above" CTA | NOLAN (link, 20 s each) + AUTO (CTA in `explainer.py --vertical`) | XS | H | [YT blog Jul 2026](https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/); [3P Spotter](https://spottercommunity.beehiiv.com/p/increase-views-from-related-shorts) +10–20% long-form views |
| 2 | A reason to subscribe inside the video: numbered series + YOU vs MEATBALL score, plus **one** CTA after the reveal ("Follow — tomorrow's score resets") | AUTO (script/render) | S | H | [3P] Galloway: big channels' stronger CTAs beat long-form sub rates; research/22 |
| 3 | 1-hour compilation "Animal Myths You Still Believe (1 Hour)" with new narration that links the segments, a new cold open, a running score and chapters | AUTO (episode.py) | M | H | [YT] reused-content test is "meaningful difference" (§3) |
| 4 | Search-question titles on long-form (autocomplete-harvested) + description first line + chapters | AUTO | S | M-H | [YT Help](https://support.google.com/youtube/answer/146402): title, thumbnail and description matter; tags are "minimal" |
| 5 | Playlists: "Every Meatball Myth" (in order) + 3 themed playlists. Every link points into a playlist | AUTO if we have Data API OAuth (`playlistItems.insert`, 50 units); else NOLAN once a week | S | M | [3P] standard practice; playlist autoplay chains watch time |
| 6 | End screen on every episode: the next episode + a playlist + subscribe. Use "Import from video" | NOLAN (1 min each) | XS | M | research/17 §2 |
| 7 | Pinned score/answer-key comment on long-form + first comment on Shorts | AUTO (Metricool first comment) + NOLAN (pin) | XS | L-M | Comments are a satisfaction signal [SPEC] |
| 8 | Cross-post the same masters to IG Reels + FB Reels via Metricool. Native upload, no TikTok watermark | NOLAN connects accounts once, then AUTO | S | L for YPP, M for reach/revenue | §4 |
| 9 | TikTok profile → YouTube link; pinned TikTok "full 10-myth quizzes on YouTube" | NOLAN once | XS | L | §4 |
| 10 | Pinterest: pin each long-form YouTube URL (it plays embedded) to "Animal Myths" boards | AUTO (Metricool) after NOLAN connects a Business account | S | L | Embedded plays count as watch time [YT] |
| 11 | Archived live stream ≤12 h (test once, hosted, not a loop) | NOLAN | L | L-M, risky | §3 |
| 12 | Reddit / Quora / FB groups | NOLAN, sparingly | M | L, ban risk | §5 |
| — | Premieres | skip | — | ~0 at 0 subs | §3 |

**This week:** 1, 2, 6 and 7 cost Nolan about 10 min a day and us one render change. Start 3 and 4 next, then 5.

## 2. Shorts → subscriber, and Shorts → long-form
**What YouTube says**
- The Related video link can point to any long-form video, live stream or Short on the channel [YT blog].
- YouTube names three viewer types:
  - Shorts-only viewers, who "may never naturally click on a 10-minute video."
  - Context-dependent viewers.
  - Exploratory viewers, who browse Shorts to find new channels.
- Its playbook is a CTA in the last 5 s, a Short that stands alone, and a long video that pays off in 5–10 s with no logo or intro [YT blog].

**What the third-party data adds**
- Spotter's study covers only two channels [3P].
  - Shorts posted **within 3 days** of the long video drove the most long-form views.
  - Shorts whose title and theme **closely match** the long video converted best.
  - Our "Shorts from the newest live episode" rule already fits this. Keep the Short's question word-for-word in the episode title or chapter.
- "Edit into a Short" (cut in the YouTube app from our own long-form) **links back to the source automatically** [3P, 2022 launch coverage: SMT, 9to5Google](https://www.socialmediatoday.com/news/youtubes-added-a-new-option-to-cut-your-long-form-videos-into-shorts/628416/).
  - Use it as a fallback when Nolan can't set Related video. It is a 60 s cap and needs the app (NOLAN).

**Subscribe-rate levers, ranked by how much evidence they have**
1. **Content-to-channel fit plus a recurring promise** ("Animal Lie #14", a running score). There is no clean public study; the support is Galloway's CTA note and research/22's character-led outliers [3P, SPEC].
2. **One CTA after the payoff, never before.** Asking first costs retention (research/17 §5).
3. **"Part 2" hooks:** good for return views and series surfaces [SPEC]. Use them only when the Part 2 already exists, so the Related video link can deliver it the same day. A broken promise burns trust.
4. **Pinned-comment CTAs:** comment links in Shorts aren't clickable [3P SEJ], so their value is comments, not clicks.

**Measure:** subs per 1k engaged views per Short (`subscribersGained`/`engagedViews`, AUTO via stats.py), and Related-video clicks from the Short's Reach tab (Studio only, NOLAN screenshot weekly).

## 3. Long-form watch hours without subscribers
- **Search beats suggested at our size.** Search is already our 2nd-biggest source (886 views at 64% viewed, research/24). YouTube autocomplete shows what people type:
  - "are bats blind"; "do sharks sleep / have bones / smell blood"; "do goldfish sleep"
  - "do owls fly silently"; "do animals dream / grieve / laugh / have souls"; "can animals laugh"
  - "animal myths busted"; "animal myths you still believe" (both real autocomplete phrases)
  - Title one episode per cluster ("Are Bats Actually Blind? 9 Animal Myths Busted"). Answer the title question in the first myth.
  - AUTO: a 20-line script that loops seed words through `suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=` and writes to research/19.
- **Compilations of our own episodes**, policy check against [YT Help 1311392](https://support.google.com/youtube/answer/1311392):
  - The reused-content test is whether viewers can see "a meaningful difference" from the original. The policy names compilations explicitly.
  - Not allowed: "clips … edited together with little or no narrative" and "content downloaded or copied from another online source without any substantive modifications".
  - The inauthentic-content section bars "AI-generated content made with generic or unoriginal templates giving the impression of mass production."
  - No official line covers a creator compiling **their own** uploads. vidIQ's guide lists own footage as allowed [3P, unconfirmed by YouTube].
  - **Verdict:** compiling our own videos isn't the risk; a bare stitch is. Each compilation gets:
    - a new cold open and new links between segments
    - a cumulative score ("you're on 31/50")
    - a "hardest of the hour" finale
    - chapters, plus a new title and thumbnail
  - Keep compilations at 1 per 10+ episodes so the channel doesn't look mass-produced at YPP review.
- **Playlist binge loops:** a series playlist + end screen → playlist + episode descriptions that say "next myth episode" = autoplay chains. Low effort, and AUTO through the API if OAuth exists.
- **Live streams** [YT blog, YT Help]:
  - Only **archived, public** streams count. Streams over 12 h "may not be captured at all", so a 24/7 stream doesn't archive and **doesn't count** [YT Archive help, via 3P quotes](https://upstream.so/blog/is-24-7-live-streaming-allowed-on-youtube/).
  - Vertical lives appear in the Shorts feed with "Watch Live" [YT blog], so they are a real Shorts → long-form bridge.
  - Mobile live needs 50 subs; desktop/OBS needs a verified channel and a 24 h enable wait [3P].
  - Looping prerecorded episodes as "live" risks the inauthentic/misleading flags [SPEC].
  - Only worth it as a hosted 1–2 h "beat Meatball" chat-poll stream once we have ~50+ subs. NOLAN, rank 11.
- **Premieres:** after premiering, the video becomes a normal public video and its watch time counts [3P](https://www.notelm.ai/blog/youtube-premiere-guide). The benefit is notifying subscribers, and we have none, so skip until ~300 subs.

## 4. Cross-platform
- **IG Reels / FB Reels via Metricool:** cheap (AUTO once Nolan connects the accounts).
  - Instagram (Apr 2026) stops recommending accounts that mainly share content they didn't create or meaningfully change. It deprioritizes other apps' watermarks [3P PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/).
  - Meta's Facebook originality rules treat self-produced content as original [3P].
  - **Upload our own masters, never TikTok downloads.** That is already how the pipeline works.
  - Direct YPP value is ~0: views there are not YouTube views. The value is a second monetization line (FB Content Monetization; eligibility is invite/dashboard-based, figures unverified) and bio links. Rank it below the YouTube levers.
- **"YouTube Shorts remixes":** "Edit into a Short" from our own long-form gives an automatic back-link (§2). It is the only remix that helps the funnel.
- **TikTok → YouTube:**
  - Put the YouTube URL in the TikTok Website field. Sources disagree on whether personal accounts need 1,000 followers [3P Outfy vs UniLink](https://www.outfy.com/blog/how-to-add-a-link-to-your-tiktok-bio/), so Nolan checks Edit profile.
  - TikTok's For You eligibility rule targets reused or watermarked content [3P quoting TikTok CG](https://www.post-bridge.com/blog/does-cross-posting-hurt-engagement). Saying "YouTube" in a video has no documented penalty, but it gives TikTok viewers nothing and costs retention on a monetized account.
  - Keep the ask to the bio and one pinned TikTok. Expect a low conversion rate [SPEC]. **Don't risk TikTok Creator Rewards income for it.**

## 5. Community (all NOLAN; I could not fetch live subreddit rules because reddit.com blocks this sandbox)
- **Reddit sitewide** [Content Policy, quoted by 3P](https://redship.io/blog/reddit-self-promotion-rules):
  - "Post authentic content into communities where you have a personal interest… do not cheat or engage in content manipulation (including spamming…)."
  - The "10% rule" is old reddiquette, not policy. **Each subreddit's sidebar rules decide.**
- **Content subreddits** (Awwducational, todayilearned, Damnthatsinteresting, likeus):
  - TIL requires a *reliable source* for the claim. Its archived rules accept video only from reputable outlets [3P archive](https://webarchive.library.unt.edu/web/20121206222307mp_/http://www.reddit.com/r/todayilearned). Our own video won't qualify as the source.
  - **Allowed and effective:** post the myth with the scientific source as a text or link post, and mention the video once in a comment if asked [SPEC].
  - **Gets you banned:** link-dropping the same YouTube URL across subs from a fresh account. Reddit can ban the channel's domain [SPEC].
- **Creator subreddits** (r/NewTubers "Self-Introduction Saturday", r/YouTubePromo): allowed in their threads [3P mirror](https://reddit.sudovanilla.org/r/NewTubers).
  - **Don't.** The viewers are other creators, not animal-myth fans. They pollute the seed audience that the Shorts algorithm learns from (research/17 §5).
- **Quora:** I couldn't confirm Quora's link policy. The norm on Q&A sites is to disclose affiliation and link only when it answers the question [3P, Stack Overflow/Codidact].
  - At most 1 answer a week on "Are bats really blind?"-type questions: a full text answer, then the video. Low yield.
- **Facebook groups:** each group's admin rules decide; most ban promo except in threads [SPEC]. Low yield.
- **Pinterest:** organic video pins allow outbound links [3P Sprout](https://sproutsocial.com/insights/pinterest-videos/), and pinned YouTube URLs play embedded. Embedded-player watch time counts [3P vidIQ calculator].
  - AUTO through Metricool once a **Business** account is connected [3P SocialKit]. Low effort and low yield, so run it as a background drip.

## 6. Search SEO checklist (AUTO in episode.py and the Metricool payload)
1. Title = the exact autocomplete question, ≤60 characters, animal first.
2. The description's first 2 lines restate the question and answer it. Add "Full quiz: [episode]" and "All myths: [playlist]" on long-form.
3. Chapters from 0:00, ≥3 chapters of ≥10 s each. Name each chapter as the searched question ("Do sharks sleep?"). Chapters can also surface as key moments in Google search [3P].
4. Tags: 3–5 tags, including common misspellings ("porcupine quils"). YouTube says tags are minimal except for misspellings [YT Help](https://support.google.com/youtube/answer/146402).
5. Category Pets & Animals, not made for kids (brand/CHANNEL.md). Nolan confirms both in Studio once (playbook/algorithm.md): "made for kids" would disable end screens, cards and comments.
6. Each week, check the "How viewers find your video" search terms (Studio, NOLAN screenshot) [YT Help 12948449](https://support.google.com/youtube/answer/12948449). Retitle Shorts that rank for a different phrasing.

## 7. Experiments to log (data/experiments.csv, one change at a time)
- E1 Related video + end-of-Short CTA → long-form views from "Shorts feed" source and Related-video clicks per 1k engaged views.
- E2 After-reveal subscribe line on Shorts → subs per 1k engaged views (baseline 0).
- E3 First 1-hour compilation → AVD and hours per view vs. the 10-min episodes.
- E4 Autocomplete-titled episode vs. quiz-styled title → search impressions at 7 days.

## Gaps
- No public study isolates the subscribe effect of series, character or CTA on Shorts. The ranking there is judgment.
- Reddit, Quora and Facebook group rules are unverified live. Read each sidebar before posting.
- The YouTube Help text doesn't mention Premieres; that rests on 3P sources.
- The FB monetization thresholds conflict between sources.
