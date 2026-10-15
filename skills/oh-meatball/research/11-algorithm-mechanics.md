# 11 — Algorithm Mechanics: YouTube Shorts + TikTok (as of 2026-10-15)

Scope: how the two feeds distribute a new channel's 16-32 s "Part N" AI-animated cat soap opera, and how to get out of the seed bucket.
Confidence key: **H** = primary or official source, recent. **M** = official but old (pre-2025), or multiple credible secondary sources agree. **L** = vendor blog or creator heuristic, or sources disagree.
Rule: nobody publishes ranking weights. Anything numeric below that is not a policy threshold is a heuristic. Use it to compare our own videos against each other, not as a pass/fail line.

---

## 1. YouTube Shorts

### 1.1 Distribution model
| Rule | Source (date) | Conf |
|---|---|---|
| A new Short goes to a small set of viewers "that may enjoy your video," and reach grows or shrinks with their response. "The audience is the algorithm." | Todd Sherman (Shorts product lead), Creator Insider Q&A, 2023-08-23, quoted by OutlierKit | M (old but not contradicted) |
| The Shorts feed is ranked on viewer response, not follower count. Subscribers are one seed pool among others. Non-subscribers make up most Shorts reach for small channels. | Same Q&A; YouTube Help, Shorts analytics | M |
| Main early metric: **Viewed vs. Swiped away**, the share of feed impressions where people stayed instead of swiping. YouTube publishes no target. | YouTube Help, Shorts analytics (undated, live 2026) | H (definition) |
| Second metric: **average % viewed**. Above 100% means loops/rewatches. A loop is a strong signal on a 16-32 s video. | YouTube Help + creator guides | M |
| Heuristic thresholds: viewed-vs-swiped of 70-80%+ for breakouts, under 50% means the hook is broken. Average % viewed of 70-80%+. Shorts over 1M views averaged ~76% retention. | Subscribr, Shortimize, creatoressentials (2025) | L |
| Thumbnails mostly don't matter in the feed ("most thumbnails are never seen"). Posting time is "not something we optimize for." Hashtags are not required. | Sherman 2023-08-23 | M |

### 1.2 How views count (March 31, 2025 change)
- Since 2025-03-31, every start **or replay** counts as a public Shorts view, with no minimum watch time. The old metric is now called **engaged views** (watched past the first few seconds, loops excluded). Engaged views drive YPP eligibility and revenue. Sources: Tubefilter 2025-03-26, MediaPost, YouTube blog on engaged views (2026-08-19). **H**
- So a public view count overstates real reach. Track engaged views in Studio (Advanced mode, metric "Engaged views").

### 1.3 Posting frequency
- "There is nothing in our systems" that penalizes a channel for posting 5 or 10 Shorts a day (Sherman 2023). Frequency mostly matters as **more tests**: each upload is another seed-audience test. **M**
- There is a quality catch. The spam policy's "automated or synthetic mass-production" category covers high-volume AI content with minimal variation. Volume of near-identical AI clips is risky. Volume of distinct episodes is fine. Source: YouTube spam policy, summarized by PPC Land 2026-10. **H**

### 1.4 Duplicate uploads (we posted Part 1 four times today)
- Sherman (2023) on deleting and re-uploading the same video: "There is a risk there that that gets seen as spam in our systems." **M**
- The spam policy explicitly says "posting a few variations of a video is ok." Four identical copies on day 1 of a new channel is an accident, not a pattern. Strike risk is low. The real cost is **self-competition**: the four copies split the same seed audiences and dilute each copy's signal. **M**
- Oct 1, 2026: YouTube is moving Shorts reach further toward original content and away from re-uploads. It targets re-uploads of *other creators'* work, but it also shows that duplicate detection is active. Source: TeamYouTube community post, via PPC Land 2026-10. **H**
- **Action:** keep ONE public copy, chosen by the best viewed-vs-swiped (or the most engaged views if they are close). Set the other three to **Private, not Delete**. Private takes them out of the feed right away and can be undone. Deleting removes data and may count against you if it becomes a habit (Sherman). Never reupload the same file again to "retry." Make a new edit with a different hook instead. **M**

### 1.5 AI content and monetization safety
| Rule | Source (date) | Conf |
|---|---|---|
| July 15, 2025: YPP's "repetitious content" became **"inauthentic content"**, covering mass-produced or repetitive videos (template slop, near-identical batches). YouTube called it a clarification ("minor update", Rene Ritchie). Penalties can hit single videos or the whole channel. | Gulf News, Daily Star, Plagiarism Today (Jul 2025) | H |
| The reused-content standard: just adding music, changing speed, or cropping does not make content original. Ritchie (Oct 2026): voice-over, minor technical edits, and template bulk changes don't make something original. | Plagiarism Today 2025-07; PPC Land 2026-10 | H |
| The **altered/synthetic disclosure** is required only for *realistic* content that could be mistaken for a real person, place, or event. Clearly animated or unrealistic content is exempt from the prominent label. Some coverage says the disclosure for animated work appears in the description. | YouTube Help (2024-03), AIR Media-Tech 2026 | M-H |
| May 2026: YouTube auto-labels content it detects as significantly *photorealistic* AI. Labels on video made with YouTube's own Veo or Dream Screen tools are permanent. | Minimatters 2026-05, TweakTown | M |
| Safe posture for our cat series: original recurring characters, written scripts, voice acting, a continuing plot, a different scene in every episode, and visible human creative choices. This is the opposite of "mass-produced." Do not batch near-identical variants. Do not reuse the same footage across episodes beyond a 1-2 s "previously on" recap. Tick the AI disclosure box if any shot looks photoreal. Stylized Pixar-look is unlikely to need it, but disclosing has no reach penalty, so disclose when in doubt. | Synthesis | M |

### 1.6 YPP thresholds
- Current full YPP: **1,000 subs + 10M engaged Shorts views / 90 days** (or 4,000 watch hours / 12 months). The lower fan-funding tier is 500 subs + 3 uploads in 90 days + 3M Shorts views / 90 days, and it does **not** include Shorts ad revenue. Source: YouTube blog / Help, current 2026. **H** (lower tier **M**)
- **From 2027-02-01**, new applicants need 1,000 subs + **20M Shorts views / 90 days** or 8,000 hours. Existing partners are grandfathered. All partners need 10M qualified Shorts views over a rolling 90 days to keep *Shorts ad revenue*; dropping below pauses it. Source: YouTube announcement 2026-08-10, via Tubefilter, NewscastStudio, PPC Land. **H**
- Implication: to qualify under the cheaper rules we would need 10M engaged views in under ~3.5 months. That is unrealistic for a seed-stage channel, so plan for the 20M bar. Shorts revenue is not our near-term business model. Subscribers, IP, and TikTok are.

### 1.7 Series tools on YouTube
- **Related video link** (Studio desktop, Details): one link per Short to any video on our channel, shown under the handle. YouTube itself suggests using it to "link multiple Shorts in a series." Source: YouTube via SEJ/vidIQ, 2023-09. **M**
  - Workflow: when Part N+1 goes live, edit Part N so its related link points to Part N+1, and point Part 1 to the newest part or a playlist. This is the only on-feed click path we have.
- **Playlist** "Oh Meatball - Season 1" in episode order. It feeds the Shorts playlist and series surfaces. No published click-through data exists. Verify with Reach reports. **L** on impact
- **Pinned comment**: Shorts descriptions and comments can't hold external links (2023 anti-spam change). Pin a comment that asks a story question ("Who sent the fish? Wrong answers only") to lift comments, and name the next part. **M**
- Titles and hashtags: titles show in the feed overlay and in search. Use plain searchable words like "cat soap opera Part 3", plus 1-3 relevant tags such as #shorts #catdrama #animation. Hashtags are optional, mostly for context and search. **M**

---

## 2. TikTok

### 2.1 For You feed mechanics
| Rule | Source (date) | Conf |
|---|---|---|
| Ranking combines user interactions (likes, shares, comments, follows, watching), video info (captions, sounds, hashtags), and device/account settings, which are weighted lowest. "Whether a user finishes watching a longer video from beginning to end" is called a strong signal. | TikTok Newsroom "How TikTok recommends videos #ForYou", 2020-06-18 | M (old, official) |
| "Neither follower count nor whether the account has had previous high-performing videos are direct factors." A brand-new account can go viral on any post. | Same | M |
| New videos go to a small test batch. Strong completion and rewatch rates unlock bigger batches. The feed avoids showing two videos in a row from the same creator or with the same sound. | TikTok 2020 + creator consensus | M |
| Videos just uploaded or under review may not be recommended yet. Don't judge a post in its first ~30 min. | TikTok 2020 | M |
| First-hour engagement matters because it is the test batch's response. No official "golden hour" rule exists. | Secondary consensus | L |

### 2.2 Search, captions, keywords
- TikTok indexes caption text, on-screen text, and the spoken audio (speech recognition). Phrasing people actually search for ("cat drama", "animated cat story", "cat soap opera") helps search and also the "search value" part of rewards. Sources: Sotrender 2025-08, Sked 2025. **M-L**
- Use 3-5 hashtags, specific to the niche rather than #fyp spam. Burned-in text "Part 3" plus the character name is indexed. **L**

### 2.3 Creator Rewards (the account is monetized)
| Rule | Source (date) | Conf |
|---|---|---|
| Eligibility: 18+, 10k followers, 100k views in the last 30 days (a rolling window, so you can drop out), personal account, eligible country. | Multiple 2026 guides (Toptal, MakeInfluence, Benly); TikTok support page not machine-readable | M |
| **Only original videos longer than 1 minute earn.** Our 16-32 s episodes earn **$0** from Creator Rewards no matter how many views they get. | Every 2025-26 source agrees | H (consensus) |
| Qualified view: For You feed only, watched 5 s or more, unique per viewer, not paid, not marked "Not interested". Often only ~50% of public views qualify. | Soundstripe 2026, Metricool | M |
| Payout formula weighs **originality, play duration, search value, audience engagement**. Duets, stitches, and repurposed third-party clips are not original. | TikTok newsroom via Metricool / passionfru 2025-26 | M |
| RPM: no official rate. Typically $0.40-1.00 per 1,000 qualified views. One mid-2026 analysis found ~$362-1,035 per million qualified views. | Elev8or 2026, Stack Influence 2026-06 | L |
| US Creator Rewards terms were updated July 2026. Details were not verifiable. Re-read the terms in TikTok Studio. | Benly 2026 | L |

### 2.4 AI content rules on TikTok
- AI content that is realistic or significantly AI-edited **must be labeled**, using the upload toggle "AI-generated", a sticker, or a caption. TikTok also auto-labels via C2PA/detection. Unlabeled realistic AI can be removed. Deepfakes of private people and misleading real-world events are banned. Sources: TikTok guidelines (Mar 2025 rule, enforcement tightened; CG update effective 2025-09-13), Social Media Today. **H**
- No found source says that labeling AI disqualifies a video from Creator Rewards. TikTok's stance is "anti-deception, not anti-AI." The originality test (own concept, own edit) is what matters. Fully original characters and story pass that test. **M**
- **Policy for us: always switch on the AI-generated label on TikTok.** It costs nothing, and skipping it risks removal or demonetization.

### 2.5 Series, playlists, length, cadence
- **Playlists** (free, from the profile): group "Oh Meatball S1" in order. Each video can be in only one playlist. Access is not universal. **M-L**
- **TikTok Series** is a paid paywall product (up to 80 videos, each up to 20 min, $1-190). It needs 10k followers, an account at least 30 days old, 1k views in 30 days, and 3-4 public posts in 30 days. It's useful later for a bonus "director's cut" season, not now. Sources: Tech.co, Search Engine Land 2023-24. **M** (possibly stale)
- Length: completion beats length. TikTok does say "finishing a longer video" is a stronger signal than finishing a short one. Our 16-32 s episodes are built for completion and loops. **M**
- Cadence: TikTok's "post 1-4 times a day" advice (Creator Portal, ~2021-22) is widely quoted but not verified on a live page. Consistency matters more than volume. Space posts several hours apart. **L**

---

## 3. Cross-posting (YT + TikTok via OpusClip)
- Posting the same original video to both platforms is allowed. Originality rules target *other people's* content. **M**
- **Never upload a file carrying another platform's watermark.** Instagram confirmed it doesn't recommend Reels with other apps' logos, and YouTube's Oct 2026 originality push points the same way. OpusClip publishes clean renders. Never download from TikTok and re-upload to YouTube. Our own logo or bug is fine. Source: Mosseri via Social Media Today (2021-24). **M**
- Use native text and title per platform. TikTok captions are search keywords. YouTube titles are the feed overlay. Use each platform's own sound picker only if we add trending audio. Our original score is safer for rewards and Content ID.
- Timing: neither platform ranks on posting time. Post when our audience is active (check analytics after ~2 weeks). Post TikTok first if both go up the same day, because rewards make it the revenue platform. Keep at least 30-60 min between platforms so you can watch the hook metric on one and fix the caption on the other. **L**
- OpusClip scheduler risk: today's 4x duplicate came from the scheduler. Before every publish, check `opusclip_list_scheduled_posts` for duplicates. Schedule one post per platform per episode.

---

## Breakout playbook for Oh Meatball (ranked by expected impact)
1. **Clean up Part 1 today.** Keep the strongest copy public and set the other 3 to Private (don't delete). Add a pre-publish duplicate check in the OpusClip workflow. Fixes self-competition and removes spam risk.
2. **Win the first 1-2 seconds.** Open on motion plus conflict (a slap, a gasp, the cliffhanger line), with burned-in text "Part N: <hook>". No logo card or slow pan. This raises viewed-vs-swiped, the main gate on both feeds.
3. **Make every episode stand on its own.** A 1-line "previously" in on-screen text, then a payoff, then the cliffhanger. Most seed viewers have never seen Part N-1. Confusion means a swipe.
4. **Design for the loop.** Make the last frame cut cleanly back to the first, ending on the cliffhanger line, so replays push average % viewed past 100%.
5. **Add 61-90 s TikTok "omnibus" cuts** (e.g. Parts 1-3 with new connective scenes and narration) so TikTok views can earn Creator Rewards. Shorts-only content earns $0 there. Add genuinely new material so it isn't treated as a repurposed compilation.
6. **Post 1-2 new episodes a day on each platform, every day.** More seed tests. Use distinct episodes, never variants of the same clip.
7. **Chain the series on YouTube:** a Related-video link on each Part pointing to the next, Part 1 pointing to the newest, an ordered Season playlist, and an ordered TikTok playlist.
8. **Use comment bait in a pinned comment** (a "Team Meatball vs Team Whiskers" vote, or "guess what's in the box"), and reply to early comments within the first hour. Comments and shares are top TikTok signals.
9. **Use search-friendly captions and titles:** "cat soap opera", "animated cat drama", the character names, "Part N". 3-5 niche hashtags on TikTok, 1-3 on YouTube.
10. **AI hygiene:** the TikTok AI label always on. YouTube disclosure ticked if any shot looks photoreal. Original music, voices, and script, with no reused footage.
11. **Double down on what wins.** After 48 h, compare every episode's viewed-vs-swiped and completion rate. Copy the hook *format* (not the clip) of the top 20%. Retire hooks under 50%.
12. **Plan for the IP, not YPP.** YouTube Shorts ad revenue needs 10M (then 20M from Feb 2027) engaged views in 90 days. Track subscribers and returning viewers as the leading indicator, and keep TikTok Series and paid extras as later options.

### Daily metrics and targets (heuristic: compare against our own median first)
| Metric | Where | Target | Red flag |
|---|---|---|---|
| Viewed vs swiped away | YT Studio > Shorts > Engagement | >= 70% (breakout 80%+) | < 50% means fix the hook |
| Average % viewed | YT Studio | >= 80%; >100% = looping | < 60% |
| Engaged views / views | YT Studio Advanced | >= 60% | < 40% |
| Subs gained per 1k engaged views | YT Studio | >= 3 | ~0 means no series pull |
| Related-video link clicks / playlist views | YT Reach + playlist report | Rising daily | 0 means the link is missing |
| Completion rate (watched full video) | TikTok Studio > video analytics | >= 50% for 16-32 s | < 30% |
| Average watch time vs length | TikTok | >= 90% of length (loops push it over 100%) | < 60% |
| % of traffic from For You | TikTok | >= 80% | Low means not being tested |
| Shares + comments per 1k views | Both | >= 10 | < 2 |
| Follows per 1k views | TikTok | >= 5 | < 1 |
| Qualified views (61 s+ cuts only) | TikTok Studio > Creator Rewards | Rising; RPM $0.4-1.0 | 0 means length or originality fail |
| Duplicates in scheduler | OpusClip | 0 | Any |

Sources used: YouTube Help (Shorts analytics, altered content, YPP); TeamYouTube community post 2026-10-01 (via ppc.land); YouTube 2026-08-10 YPP announcement (Tubefilter, NewscastStudio, ppc.land, metricool); Tubefilter 2025-03-26 (views change); Gulf News / Daily Star / Plagiarism Today 2025-07 (inauthentic content); OutlierKit (Sherman Creator Insider 2023-08-23); TikTok Newsroom 2020-06-18; Social Media Today (TikTok AI labels; Mosseri watermarks); Metricool, Soundstripe, Elev8or, Stack Influence, MakeInfluence (Creator Rewards 2026); Tech.co / Search Engine Land (TikTok Series); SEJ / vidIQ 2023 (Related video link).
