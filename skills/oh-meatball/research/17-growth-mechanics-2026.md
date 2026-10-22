# 17 — Growth mechanics for a small faceless quiz channel (2025–2026)

Channel: **Meatball Myths**. Format: stick-figure mascot, real wildlife photos, AI voice. Each long-form episode is a 10–11 min "TRUE or FALSE?" quiz, and each myth is also cut as a 45–90 s Short. Posting goes through Metricool.
Goal: YPP, meaning 1,000 subscribers plus either 4,000 public watch hours in 12 months or 10M Shorts views in 90 days.
Measured problem: Shorts get 1–2k views in about 12 h, then stop. Likes run about 1%, with roughly 0 comments, shares, or subscribers.

Evidence tiers: **[YT]** = YouTube's own Help pages, blog, developer docs, or a named YouTube employee. **[3P]** = a reputable creator-economy analysis. **[SPEC]** = inference or unverified.

---

## 0. The diagnosis in one paragraph

1–2k views followed by a flat line is the normal end of the Shorts **exploration test**. YouTube's Shorts product lead, Todd Sherman, said a new Short gets "a few hundred or a few thousand views" while the system looks for an audience. It only keeps distributing when that seed audience responds [YT, via SEJ 2023]. The ~1% like rate and zero comments or shares say the seed audience swiped or watched passively. The fix is the first 1–2 seconds and a reason to rewatch, not posting time or hashtags. Separately, 10M Shorts views in 90 days is not a realistic path for this channel. **Go for the 4,000 watch-hours path and use Shorts as a funnel into long-form.**

Math check: 4,000 h = 240,000 min. At about 3.5 min average view duration (AVD) on an 11-min video, that is **~69k long-form views in 12 months, or ~1,300/week**. Shorts views do **not** count toward watch hours [YT, YPP policy].

---

## 1. How the Shorts feed decides to keep distributing

**What YouTube has said**
- Shorts are mostly discovered by swiping, not chosen. YouTube wants a view to "encode for your intent of watching that thing" and keeps the exact thresholds private [YT: Todd Sherman, SEJ 2023](https://www.searchenginejournal.com/youtube-explains-how-shorts-algorithm-works/494953/).
- "The audience is the algorithm." There is no magic posting frequency, and better beats more [YT: same interview].
- **Viewed vs. swiped away** is the analytics metric for that first decision: the share of feed impressions where the viewer stayed instead of swiping [YT Studio metric; definition via 3P guides]. Find it in Studio → Analytics → Content → Shorts, and on each Short's Reach tab.
- **Since 31 Mar 2025** a Shorts "view" counts every start or replay with no minimum. The old measure is now **engaged views**, and engaged views are what count for the YPP 10M path and revenue [YT dev revision history; 3P](https://vidiq.com/blog/post/youtube-view-count-update/). **Compare engaged views, not views.** Raw views include swipe-pasts.
- Shorts can be up to 3 min since 15 Oct 2024. YouTube said it would "improve recommendations for longer Shorts" [YT blog](https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/).

**What moves those numbers (3P consensus, plus SPEC on weights)**
1. **Viewed %** is the gate. Common targets are ≥70–80% viewed [3P: Subscribr; the Paddy Galloway dataset found top Shorts at 70–90%](https://insights.vaizle.com/?p=3156). YouTube publishes no threshold, so compare against your own Shorts [3P ByteCap].
2. **APV (average percentage viewed) and loops.** Galloway's 5,400-Short study found Shorts that more than 60% of viewers finished did much better [3P](https://www.blogdumoderateur.com/youtube-shorts-criteres-favorisent-performances-videos/). Replays now count as views, so a seamless loop raises both views and APV.
3. **Likes, comments, shares, and subscribes after the Short** act as satisfaction signals [3P; YouTube has never published the weights, SPEC].

**Ideal length for a quiz Short**
- Galloway found 50–60 s Shorts averaged the most views in his dataset [3P]. Nate Black's 35B-view study found peaks at about 13 s and about 60 s [3P, vidIQ](https://vidiq.com/blog/post/youtube-shorts-algorithm/).
- For "TRUE or FALSE?": **25–45 s for one myth.** Use this structure: claim on screen at frame 0 → 2–3 s "pause and guess" countdown → reveal plus one surprising fact → a last line that loops back into the claim. Go past 60 s only if APV stays ≥70%. **Your 45–90 s cuts are probably too long. Cut padding before cutting facts.**
- **Frame 0 rule:** the myth text and the most striking wildlife photo must be on screen in the first frame. No mascot intro, logo, or "Did you know…" wind-up.

---

## 2. Do Shorts help or hurt long-form? And how to convert

**Evidence**
- YouTube's Todd Beaupré (2023): if the formats serve the same audience, keep them on one channel. At VidCon he announced that recommendations now take into account recent long-form videos from channels a viewer watches in Shorts [YT via 3P](https://vidiq.com/blog/post/youtube-recommends-long-form-videos-shorts-viewers/).
- YouTube's Rene Ritchie: performance is evaluated per video and per audience, so a weak Short does not drag down the next long video [YT via 3P, unverified quote].
- Galloway: Shorts converted 16.9 subs per 10k views, versus 22.7 for long-form [3P]. **The channel gains no subscribers right now**, which points to weak content-to-channel fit (no reason to want more), not a penalty.
- Risk [SPEC, widely reported]: Shorts-acquired subscribers watch long-form at lower rates, which can thin the subscription signal. This matters little when the Shorts and long-form are about the same topic, as here.

**Conversion playbook (official, YouTube blog, 14 Jul 2026)** [YT](https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/)
1. **Related video link on every Short** (Studio → Content → Short → Details → Related video). Point it at the exact episode containing that myth [YT Help](https://support.google.com/youtube/answer/14075157). Description and comment links in Shorts are no longer clickable [3P SEJ].
2. **Last ~5 s CTA, both verbal and visual.** For example: "Myth #3 is even weirder — tap the link above," with an arrow toward the link or the episode thumbnail.
3. **Reward the click.** The long video must deliver the promised myth within 5–10 s. For linked traffic, consider opening the episode with the hardest myth cold.
4. Each clip must still work on its own.

**Other levers**
- **End screens** on long-form: "best for viewer" plus one specific next episode, from about 20 s before the end. Make the outro an end screen, not filler.
- **Playlists:** keep a "Meatball Myths — every episode" playlist plus themed ones (Ocean / Predators / Pets). Link to episodes **within the playlist** so autoplay continues the session [3P standard practice].
- **Pinned comment** on long-form: an answer key or score tally prompt (see §5). Comment links in Shorts don't work.
- **"Shorts that remix long-form":** making Shorts from your own long-form is fine. The risk is the inauthentic-content policy (§7), so vary the hooks and edits instead of producing identical template cuts.

---

## 3. Long-form retention for list/quiz videos

**Benchmarks (no official numbers exist)**
- vidIQ (2026): platform average APV is in the low-to-mid 20s, and **~30% is a good target for 6–9 min education videos** [3P](https://vidiq.com/blog/post/increase-audience-retention-youtube/). Other tools quote 40–60%, but those figures are unsourced and inflated.
- **For a 10–11 min quiz: aim for ≥35% APV (~3.5–4 min AVD) and ≥70% still watching at 0:30.** Use `relativeRetentionPerformance` in the Analytics API, or "typical retention" in Studio, to compare against videos of similar length [YT dev docs].

**First 30 seconds**
- 0–3 s: the most absurd myth on screen with a photo ("Goldfish have a 3-second memory. TRUE or FALSE?").
- 3–15 s: stakes and rules: "10 myths, keep score — most people get 4 or fewer."
- By 0:20: myth #1 starts. **No channel intro, logo sting, or "welcome back"** (YouTube's own July 2026 guidance on landing viewers says the same).

**Mid-video mechanics**
- **Keep-score loop:** an on-screen score counter, plus "pause now and guess" countdowns. Ask viewers to comment their score at the end. This gives comments a reason to exist.
- **Open loops:** "the #1 myth is one your teacher told you" in the intro, then a reminder at about 40% and 70% of the runtime.
- **Pattern interrupt every 20–40 s:** change the visual (photo → mascot reaction → map/diagram → zoom), change the audio sting, and add a "bonus fact" card. Reuse templates for these, but vary them [SPEC on exact interval; 3P consensus].
- **Order myths by strength:** strongest first, second-strongest last, weakest in the middle (minutes 4–7). Expect dips there and keep those myths short.
- **Chapters:** add timestamps from 0:00 with at least 3 chapters of ≥10 s [YT Help]. They help search and key moments. They may reduce linear watch-through, so use myth-hiding names ("Myth 4: Bats & blindness") and not answer-revealing ones [SPEC].

---

## 4. Packaging (title + thumbnail)

- **Test & Compare** (Studio → video → thumbnail/title "Test"): up to 3 variants. YouTube picks the winner by **watch time share**, not CTR, to discourage clickbait [YT, quoted in 3P](https://thumbnailtest.com/news/youtube-releases-title-test-compare/). Title testing has been rolling out since 2025; check whether your Studio shows it. Low-traffic videos can take up to ~2 weeks or end "inconclusive" [3P]. **Use it on every long-form upload anyway, since it costs nothing.**
- **Curiosity-quiz patterns that work [3P consensus]:**
  - Title: one specific, surprising claim plus a challenge. "Can You Spot the FAKE Animal Facts? (Most Get 4/10)" / "Sharks Don't Get Cancer?! 10 Animal Myths You Still Believe". Keep it under ~55 characters, front-load the animal, use one "?" or "!", and no ALL CAPS sentences.
  - Thumbnail: 1 striking animal photo (face or eyes, high contrast) + mascot reacting + a big **TRUE / FALSE** stamp or a "?" over the key element. At most 3 words. Make it readable at phone size. Don't repeat the title text.
  - Make title and thumbnail **complement** each other (the thumbnail shows the claim, the title adds the challenge).
- Shorts: the title matters for search and suggested surfaces. **#Shorts is unnecessary** [3P vidIQ]. Pick a frame-0 that works as a thumbnail.

---

## 5. Engagement levers: real vs. myth

| Lever | Verdict |
|---|---|
| Asking for a **specific, low-effort comment** ("Comment your score /10", "Which one fooled you?") | **Real.** Comments become a natural survey response. It turns the ~0 comments into data. YouTube has not published how much comments weigh [SPEC]. |
| **Replying to comments in the first hours** | Moderate. It drives return visits and reply threads. No YouTube statement says replies boost ranking [SPEC]. |
| **Pinned comment** with the answer key or a "which myth next?" question | Useful for community and comments. Low algorithmic impact. |
| **Posts / polls** ("TRUE or FALSE: owls can turn their heads 360°?") | Available without a subscriber minimum once the channel has advanced features (verified) [3P](https://buffer.com/resources/youtube-community-posts/). Posts are shown mainly to existing subscribers, so they matter little at 0 subs. **Start once you have ~100+ subs.** |
| "Like and subscribe" begging at the start | **Myth / harmful.** It costs retention in the first seconds. Ask once, after a payoff. |
| Hashtags, tags, ideal description length | Mostly myth. Small contextual help only [3P vidIQ]. |
| Deleting and re-uploading underperforming Shorts | Myth / risky. It can look like repetitive content. Rework the hook into a **new** Short instead. |
| Sub-for-sub, engagement pods, buying views | Harmful: fake engagement policy, plus it pollutes the seed audience. |
| Likes (~1% now) | A symptom, not a lever. Expect about 3–5% on well-received Shorts [3P, varies by niche]. |

YouTube says it uses satisfaction signals: surveys, likes and dislikes, and "not interested" [YT, via 3P summaries]. Satisfaction outweighs raw engagement counts.

---

## 6. Cadence, consistency, timing

- [YT, Sherman] There is no magic frequency, and quality beats volume.
- [3P vidIQ] Channels with 200+ Shorts show steadier growth. That is correlation: it reflects learning reps, not a reward for volume.
- Timing: there is no official YouTube claim that the hour matters. Publish about 1–2 h before your audience's peak. Use Studio → Audience → "When your viewers are on YouTube" once data exists, or Metricool's `getBestTimeToPostByNetwork`. **The effect on a tiny channel is noise.** Don't optimize timing before fixing the hook.
- **Recommended sustainable cadence:** 1 long-form/week (same day each week is fine) plus 1 Short/day, each with a distinct hook. Fewer, better Shorts beat 3/day of the same template (§7 risk).

---

## 7. Policy risks for an AI-voiced, template-driven channel

**July 15, 2025 YPP update** [YT Help — YPP monetization policies](https://support.google.com/youtube/answer/1311392): the "repetitious content" policy was renamed and clarified as **"inauthentic content"**, meaning content that is "mass-produced or repetitive." Exact text:
- Not allowed: "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos"; "content that looks like it's made with a template"; "AI-generated content made with generic or unoriginal templates"; "Content that exclusively features readings of other materials you did not originally create."
- Allowed: "Same intro and outro for your videos, but the bulk of your content is different"; "using AI to edit your video scripts or generate a unique background visual."
- Reused content (stock or wildlife photos) needs "a meaningful difference" from the source. Permission alone does not satisfy it.
- AI voice is **not named** in the policy. Reviewers assess the channel as a whole at YPP application, so a fully templated AI-voice channel is the profile being targeted [SPEC, widely reported].

**AI disclosure label** ("altered or synthetic content", Studio checkbox, since Mar 2024) [YT blog](https://blog.youtube/news-and-events/disclosing-ai-generated-content): required for **realistic** content a viewer could mistake for real people, places, or events, and for synthetic voices of real people. Not required for clearly unrealistic or animated content, or production assistance. A generic, non-cloned narrator voice over a cartoon mascot generally doesn't require it [3P interpretation]. **Disclose if you use AI-generated photoreal animal images or video presented as real**, and prefer real licensed photos.

**Hidden like counts:** there is no confirmed 2026 YouTube policy. March 2026 reports of missing like counts were unconfirmed or a glitch, and a Shorts dislike/"Not interested" merge test ran in Dec 2025 [3P](https://www.tubefilter.com/2025/12/19/youtube-dislike-button-hidden-not-interested/). Nothing to act on.

**How to show "meaningful original value"**
1. Original script per episode with real research: cite 1–2 sources on screen or in the description, one per myth.
2. A recurring character with personality: give the mascot reactions, opinions, and running jokes, not just a logo.
3. Vary structure across episodes: themed episodes, "vs" episodes, viewer-submitted myths, and a "myths we got wrong" follow-up.
4. Use your own photo edits, annotations, and diagrams instead of raw image dumps. Credit photographers and use CC-licensed or public-domain images properly.
5. Shorts must differ from each other: unique hooks and edits, not one template with swapped text.
6. Consider a custom or premium-quality TTS voice with consistent character delivery. The risk is a generic voice reading generic text, not TTS itself [SPEC].

---

## 8. Free tools and APIs to automate

| Need | Available? | Notes |
|---|---|---|
| Upload video | **Yes**: Data API `videos.insert` | Now 1 unit/call, capped at **100 calls/day** [YT dev quota table](https://developers.google.com/youtube/v3/determine_quota_cost). **Unverified API projects created after Jul 28 2020 can only upload private videos** until they pass an audit [3P, matches YT ToS]. Metricool already handles this. |
| Custom thumbnail | **Yes**: `thumbnails.set` (50 units, ≤50 MB) [YT](https://developers.google.com/youtube/v3/docs/thumbnails/set) | Channel must be verified for custom thumbnails. |
| Playlists | **Yes**: `playlistItems.insert` (50 units) | Automate adding each episode and Short to the right playlists. |
| Pinned / auto comment | Partly: `commentThreads.insert` (50 units) posts a comment | **Pinning is not in the API**, so pin manually. |
| Chapters | Yes, indirectly: write timestamps into the description via `videos.update` | |
| End screens, cards | **No API** | Manual in Studio. Copy end screens from a previous video ("Import from video"). |
| Shorts related-video link | **No API** [3P, tool vendors] | Manual in Studio, about 20 s per Short. Do it every time. |
| Test & Compare | **No API** | Manual. |
| Posts / polls | **No API** | Manual, or a scheduler that supports YouTube Posts, if any. |
| Metrics | Analytics API: `views`, **`engagedViews`**, `averageViewDuration`, `averageViewPercentage`, `audienceWatchRatio` (retention curve), `relativeRetentionPerformance`, `subscribersGained`, `cardClickRate` [YT](https://developers.google.com/youtube/analytics/metrics) | **"Viewed vs. swiped away" is not exposed in the API.** Read it in Studio. Approximate it with `engagedViews / views`, which is close to the stayed-to-watch rate [SPEC]. |
| Already connected here | Metricool MCP (scheduling, best-time, analytics), vidIQ MCP (keyword/outlier research, title/thumbnail scoring, comment replies) | Use vidIQ `outliers` on animal-myth / quiz niches to find packaging that already works. |

**Suggested free weekly report script:** pull per-video `engagedViews/views`, `averageViewPercentage`, `subscribersGained`, and `audienceWatchRatio`. Flag Shorts with an engaged ratio <0.7 and long-form with 30 s retention <70%.

---

## 9. Ranked checklist

### DO THIS (highest expected impact first)
1. **Rebuild the Short hook:** myth text plus best photo at frame 0, a 2–3 s "guess" beat, reveal, and a last line that loops back to the start. Target **≥70% viewed** and **≥70% APV**.
2. **Shorten Shorts to 25–45 s, one myth each.** Keep >60 s only when the data justifies it.
3. **Set a Related video link on every Short** to the matching episode, plus a 5 s verbal and visual CTA.
4. **Commit to the watch-hours path:** long-form is the product, and Shorts are the funnel. Track toward ~1,300 long-form views/week at ≥3.5 min AVD.
5. **Long-form cold open:** strongest myth by 0:20, no intro, and a stated keep-score challenge. Target ≥70% retention at 0:30 and ≥35% APV.
6. **Keep-score mechanics plus a "comment your score" ask at the end**, with a pinned comment and answer key.
7. **Test & Compare on every long-form upload** (3 thumbnails, and titles if available). Follow the patterns in §4.
8. **Defend against the inauthentic-content policy:** original researched scripts with on-screen sources, a mascot with personality, structural variety across episodes, unique Short edits, and credited photos. Disclose only realistic AI imagery.
9. **End screens plus playlists** on every long video, linking to episodes within the playlist.
10. **Weekly analytics loop:** `engagedViews/views`, APV, and the 0:30 retention point, then change one variable at a time.
11. Reply to every comment within the first 24 h. Start Posts/polls at ~100 subs.

### STOP DOING THIS
1. **Stop judging Shorts by raw "views".** Use engaged views and viewed %.
2. **Stop 60–90 s multi-beat Shorts with slow openings** (mascot intros, "Did you know").
3. **Stop expecting Shorts views to count toward the 4,000 hours.** They don't.
4. **Stop mass-producing identical-template Shorts** (same voice line, layout, and pacing with swapped text). This is the July 2025 policy's exact target and hurts YPP review.
5. **Stop optimizing posting time and hashtags** before the hook is fixed.
6. Stop "like and subscribe" asks at the start of videos.
7. Stop deleting and re-uploading flops. Make a new Short with a new hook instead.
8. Never buy views or subs, or use sub-for-sub.

---

### Gaps and caveats
- YouTube has never published ranking weights. Everything about the relative weight of APV, likes, and comments is 3P or SPEC.
- I could not find a 2025–26 YouTube-official statement on upload timing or on Shorts hurting long-form. The positions above rest on 2023 statements and the July 2026 YouTube blog.
- The Test & Compare title-testing rollout status varies by account.
