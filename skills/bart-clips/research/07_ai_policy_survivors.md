# 07 — AI content policy on YouTube / TikTok / Instagram, and what separates AI channels that get paid from "AI slop" (researched 2026-10-15)

Companion to `04_algorithm_policy.md`. That file covers the YouTube reused-content policy, the Oct 1 2026 Shorts originality re-rank, YPP thresholds and the 2027 changes, and the IG/TikTok aggregator demotion. Those topics are not repeated here; this file is about **AI-generated content** specifically.

Legend: **[OFFICIAL]** = platform first-party. **[PRESS]** = reputable press. **[SECONDARY]** = blogs, vendors, SEO sites. **[UNVERIFIED]** = single source, self-reported or contradicted. **[OLD]** = predates 2025.

---

## 0. TL;DR

- **No platform bans AI.** All three punish four things:
  - **mass production / templates**
  - **deception** (realistic fakes left unlabeled, fake trailers, fake "true" stories)
  - **manipulation / shock bait**
  - **AI "experts" giving health, finance or legal advice**
- **Disclosure doesn't cost reach or money on YouTube.** YouTube says so in writing. Not disclosing does cost you.
- **YouTube's 2026 rule set has three named monetization killers** (Tubefilter, 2026-07-13):
  - "generic or repetitive"
  - "unsatisfying or off-putting"
  - AI personas on sensitive topics
- **AI channels that survive look like shows, not feeds.** They have a named recurring character or IP, human-written jokes and arcs, a consistent world, a modest posting cadence, disclosure, and revenue beyond AdSense (brand deals, Cameo, licensing).
- **AI channels that get killed look like factories:**
  - near-identical episodes several times a day
  - stolen IP (Dragon Ball, Marvel trailers)
  - fake realism, pseudo-religious or emotional bait, kids-content spam

---

## 1. YouTube

### 1.1 Policy (current text)

| Claim | Date | Source | Grade |
|---|---|---|---|
| **Disclosure rule.** Creators must disclose *realistic* altered or synthetic content: a real person saying or doing something they didn't, altered footage of real events or places, a realistic scene that never happened, or AI music that is the focus of the video. Unrealistic content (e.g. "a unicorn in a fantasy world"), beauty filters, captions, cloning your *own* voice, and AI-written scripts, titles or thumbnails **don't need disclosure**. | page live 2026-10-15 (no effective date shown) | https://support.google.com/youtube/answer/14328491 | OFFICIAL |
| **Disclosure is neutral for reach and money.** "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money." | same | same | OFFICIAL |
| **Not disclosing is penalized.** Creators who consistently fail to disclose may get a label applied by YouTube, content removal, or **suspension from YPP**. YouTube also auto-labels content made with its own GenAI tools, content carrying C2PA metadata, and content it detects as AI. | same | same | OFFICIAL |
| **Where the label shows.** Photorealistic or music content gets a label on the player. Animated or non-photoreal content gets it in the expanded description. | same | same | OFFICIAL |
| **2025 rename.** "Repetitious content" became **"inauthentic content"**: mass-produced, templated, near-duplicate content. TeamYouTube called it "a minor update to our longstanding guideline". | 2025-07-15 | https://support.google.com/youtube/answer/1311392 (dated notice on page) | OFFICIAL |
| **2026 clarification: three demonetizable categories.** (1) **"Generic or Repetitive"**: templated, minimal variation, "image slideshows, templated storylines, or scrolling text with minimal or no narrative", "stitching together unrelated or inconsistent AI clips", AI "made with generic or unoriginal templates giving the impression of mass production". (2) **"Unsatisfying or Off-putting"**: "emotionally manipulative, disturbing, nonsensical, shocking", e.g. animals in exaggerated distress, realistic fake celebrity deaths or disasters, violence or loss with no cohesive story. (3) **AI personas presented as human experts** on health, legal, financial or political topics (an AI "doctor", AI finance podcast hosts). | 2026-07-13 (Tubefilter) / 2026-07-15 (Dexerto); TechCrunch says 07-16 | https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/ ; https://www.dexerto.com/youtube/youtube-cracks-down-on-unsatisfying-or-off-putting-videos-with-demonetization-3387786/ ; policy text at https://support.google.com/youtube/answer/1311392 | OFFICIAL (page text) + PRESS. Exact date varies by outlet; YouTube called it a clarification, not a new policy. |
| **Uses the policy page explicitly allows:** "using AI to visualize a unique character and narrative you invented", and using AI to edit scripts or generate unique backgrounds. Automated tools are OK when the result shows creative vision and value. | live 2026-10-15 | https://support.google.com/youtube/answer/1311392 | OFFICIAL. **This is the safe harbor to design around.** |
| A human-written script or an AI disclosure does **not** rescue an "AI expert" persona format. | 2026 | https://www.tunepocket.com/how-youtube-decides-what-channels-can-be-monetized/ | SECONDARY |
| Enforcement is reported to be **channel-level**: a pattern across recent uploads demonetizes the whole channel, not single videos. | 2026 | https://letsdatascience.com/news/youtube-cracks-down-on-faceless-creators-monetization-e3bb5892 ; https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/ | SECONDARY / UNVERIFIED mechanism ("last 30 uploads" is not official) |

### 1.2 Neal Mohan on AI slop (2026)

- **2026-01-21, annual letter.** Mohan: "The rise of AI has raised concerns about low-quality content, aka 'AI slop'." YouTube is "actively building on our established systems that have been very successful in combating spam and clickbait, and reducing the spread of low quality, repetitive content." He also said that "with this openness comes a responsibility to maintain the high quality viewing experience". [OFFICIAL via PRESS] — https://au.variety.com/2026/digital/global/youtube-channels-using-ai-tools-reduce-slop-neal-mohan-letter-32190/ (Variety, 2026-01-22); https://www.tubefilter.com/2026/01/21/neal-mohans-2026-letter-to-creators-a-lot-of-ai-a-tiktok-shop-competitor-and-beautifully-produced-tv-to-compete-with-netflix/
- **Other points in the same letter:**
  - More than 1M channels used YouTube's AI creation tools daily in December 2025.
  - Creators will be able to make Shorts with their own likeness.
  - Content ID is being extended to manage likeness in AI content.
  - YouTube supports the NO FAKES Act. [PRESS, same]
- **2026-09-23, Made on YouTube.** The announcements were mostly AI tooling: full-video A/B tests, dynamic thumbnails, Custom Feeds. YouTube's GenAI report said 72% of US uploaders aged 14–44 used AI. **There was no new slop policy.** [PRESS] — https://www.tubefilter.com/2026/09/23/made-on-youtube-2026-ai-personalization-creator-tools/
- **Read:** YouTube is pro-AI-tool and anti-slop at the same time. It sells Veo in Shorts and AI avatars (2026-04-10, with SynthID/C2PA labels; https://www.tubefilter.com/2026/04/10/youtube-creator-ai-avatar-shorts-deepfakes/) while demonetizing templated output.

### 1.3 Can AI Shorts join YPP?

- **Yes, subject to the policies above.** No YouTube rule excludes AI-made Shorts from YPP or Shorts revenue share.
- **Disclosure is explicitly neutral** (section 1.1).
- **Category matters.** "Using AI to visualize a unique character and narrative you invented" is listed as monetizable. Mass-produced, generic or shock AI clips are not.
- **No official statement was found that is specific to AI Shorts and YPP.** A 2025 report said Veo-in-Shorts monetization was "still being ironed out" [SECONDARY, gsmarena 2025]. Treat it as allowed but channel-reviewed.
- **Oct 2026 Shorts originality re-rank:** see `04` §0. It targets re-uploads of *other creators'* content, not AI as such. But "template-based bulk changes" is the same language as the inauthentic-content rules, so templated AI farms are exposed to both.

### 1.4 Enforcement waves and named channels hit

| Date | What | Channels | Why | Source | Grade |
|---|---|---|---|---|---|
| **2025-01/02** | Terminated | **True Crime Case Files** (~150 videos) | Fabricated AI "true crime" murders with no disclosure. A Denver Post reporter got calls about a murder that never happened. | https://www.tubefilter.com/2025/02/14/youtube-true-crime-case-files-ai-crime-channel-terminated/ | PRESS |
| **2025-03 → 2025-12** | Demonetized in 2025, then **terminated in December 2025** | **Screen Culture** (~1.4M subs) and **KH Studio** (~680K); ~2M subs and >1B views combined | Fake AI movie trailers, spam and misleading metadata. They regained monetization after adding "fan-made" labels, then dropped the labels and were terminated. | https://www.thewrap.com/?p=7915970 ; https://heise.de/-11121072 ; https://gigazine.net/gsc_news/en/20251223-youtube-shuts-down-ai-fake-movie-trailers-channels | PRESS |
| **2025-11/12** | Study, not enforcement | Kapwing "AI Slop Report": 21–33% of a new account's first 500 Shorts were slop or brainrot. Top channels were **Bandar Apna Dost** (2.07B views, est. $4.25M/yr), **CuentosFacinantes** (5.95M subs), **Three Minutes Wisdom** (2.02B views). | Data as of 2025-10 | https://www.kapwing.com/blog/ai-slop-report-the-global-rise-of-low-quality-ai-videos/ | SECONDARY (vendor study, widely cited by press) |
| **2026-01** | **At least 18 channels deleted or hidden** (OutlierKit: 11 terminated, 5–6 wiped; ~35M subs, ~4.7B views) | **CuentosFacinantes** (Dragon Ball-themed AI, >1.2B views), **Imperio de Jesus** (religious AI serials, ~5.9M subs), **Super Cat League** (AI animals, ~4.2M), **Three Minute Wisdom** (content wiped) | Spam and deceptive practices policies. Per OutlierKit, "not a new anti-AI rule". | https://tubefilter.com/2026/01/29/youtube-ai-slop-channel-crackdown-bans/ (2026-01-29) ; https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/ | PRESS (Tubefilter names CuentosFacinantes and Imperio de Jesus); SECONDARY for the other names and counts |
| **2026-07** | Demonetizations under the new wording | **HPad** (225K subs; appliance-destruction videos): reason switched from "inauthentic" to "unsatisfying or off-putting". Claims ≥$15K lost over 3 months. | Off-putting / repetitive | Dexerto 2026-07-15 (above) | PRESS (self-reported loss) |
| 2026 ongoing | Collateral damage claims | **Doctor NOS** (1.7M) says many faceless creators are being demonetized | Faceless / templated signal | https://hackernoon.com/youtubes-ai-slop-crackdown-cant-tell-a-directed-ai-film-from-a-bot-farm (via Hollywood Reporter) | SECONDARY (opinion piece) |
| observed 2026-10-15 | Data point | A Korean "funny AI videos" Shorts channel (@핫딜쇼핑채널) still shows **862K subs** but **1 video and 242 views**: a −99.85% 1-year view drop | Consistent with content wiped or removed. **Reason unknown.** | vidIQ channel search, 2026-10-15 | UNVERIFIED (inference) |

**Still standing (as of the cited dates):**
- Tubefilter's 2026-01-29 article listed AI-slop channels **Riki TV** and **Rbrain Project** still on its Global Top 50.
- Whether Bandar Apna Dost is still live is **unverified**: it didn't appear in a vidIQ index search on 2026-10-15.
- Copycat "AI monkey comedy" channels are active, e.g. @aalupyaj39, 183K subs, created 2025-12. [vidIQ 2026-10-15]
- Enforcement is clearly partial.

### 1.5 Likeness and deepfakes

- **Likeness detection** went to YPP creators in Sept 2025 [PRESS, Axios 2025-09-16] and to **all creators 18+** around 2026-05. It requires ID plus a selfie, and flagged deepfakes can be removed. Voice detection is "planned later 2026". [PRESS] — https://petapixel.com/2026/05/18/youtube-will-help-you-find-videos-featuring-your-ai-clone/
- **Implication for a fan channel:** an AI likeness of a real streamer (e.g. Joe Bartolozzi) can be flagged by him and removed. **Never synthesize a real creator's face or voice.**

---

## 2. TikTok

| Claim | Date | Source | Grade |
|---|---|---|---|
| **Labels are mandatory for realistic AI.** Creators must label AI-generated or significantly edited content showing realistic scenes or people. Unlabeled content "may be removed, restricted, or labeled by our team". | live 2026 | https://www.tiktok.com/safety/en/policies-and-engagement/integrity-authenticity (page didn't render to fetcher; quoted via search snippet) | OFFICIAL via snippet |
| **Scale and spam targets.** >3B videos labeled AIGC (C2PA, creator toggle, invisible watermark). 86M fake accounts removed in Q1 2026. TikTok is testing detection of "accounts dedicated to posting AI-generated spam", starting with politics and current events, financial advice and medical content. | **2026-07-10** | https://newsroom.tiktok.com/helping-people-spot-and-understand-ai-generated-content-on-tiktok?lang=en-GB | OFFICIAL |
| **Viewers can turn AI down.** "Manage Topics" has an AI-content slider, and TikTok uses invisible watermarks on content made with its tools or carrying C2PA. | 2025-11 | https://www.techspot.com/news/110315-sick-ai-slop-feed-tiktok-finally-you-turn.html | PRESS |
| **Q1 2026 removals.** 32,504 videos removed under the edited-media/AIGC policy. | Q1 2026 | https://storrito.com/resources/tiktok-removed-51000-ai-videos-creators-feeling-it/ | SECONDARY (cites enforcement report; not verified on tiktok.com) |
| **Aug 2025 guideline rewrite.** TikTok removed the long explicit list of FYF-ineligible content and reworded deepfake rules to "misleading about matters of public importance or harmful to individuals". | 2025-08-15 | https://techcrunch.com/2025/08/15/tiktoks-new-guidelines-add-subtle-changes-for-live-creators-ai-content-and-more/ | PRESS |
| **Creator Rewards: originality is scored.** Unoriginal content is ineligible, and "originality" is a key metric in the rewards formula. Videos must be **>1 min** for the program; reported eligibility is 10K followers, 100K views in 30 days, 18+, a personal account, and an eligible country. | live 2026 | https://www.tiktok.com/creator-academy/article/tiktok-originality-policy (snippet; page didn't render) ; blogs | OFFICIAL via snippet + SECONDARY |
| **AI persona removed from Creator Rewards in practice.** **Granny Spills** (AI persona, ~400K TikTok followers in weeks) had videos flagged "unoriginal" and was removed from Creator Rewards. TikTok cited its "unoriginal or low-quality content" policy. | **2025-11-19** | TIME (Andrew R. Chow), syndicated at https://www.aol.com/ai-influencers-coming-feeds-175525745.html | PRESS |
| **Unconfirmed claim that fully AI videos are banned from Creator Rewards.** It comes from a single vendor blog and contradicts other blogs. Creator anecdotes (e.g. @historydad_ai, 2025) report AI-visual videos flagged unoriginal with no payout. | undated / 2025 | https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/ | UNVERIFIED. **Working assumption:** TikTok Creator Rewards is the *least* reliable payout for AI-visual content. |
| **Kapwing on new TikTok feeds.** **59%** of the first 500 videos shown to a new TikTok account were AI slop, versus 21% on YouTube Shorts. The Kids category was 57%. | 2026-06 (data May 2026) | https://www.tubefilter.com/?p=192734 ; https://thenextweb.com/news/tiktok-ai-slop-59-percent-new-users-kapwing-study | PRESS citing vendor study |

---

## 3. Instagram and Facebook (Meta)

| Claim | Date | Source | Grade |
|---|---|---|---|
| **Facebook "unoriginal content" crackdown.** Accounts that repeatedly reuse others' content lose monetization for a period and lose reach. Duplicates are demoted. Watermarks and stitching are not "meaningful enhancements". ~10M impersonator profiles removed in H1 2025. | 2025-07-14 | https://techcrunch.com/2025/07/14/following-youtube-meta-announces-crackdown-on-unoriginal-facebook-content | PRESS |
| **"Rewarding Original Creators on Facebook."** The original source gets more distribution and reposts get less. "Original" means self-produced or "meaningfully transform[ed]". Views of original Reels on FB roughly doubled in H2 2025 vs H2 2024. >20M impersonator accounts removed in 2025. | **2026-03-13** | https://www.exchange4media.com/digital-news/meta-updates-policies-to-reward-original-creators-and-limit-reposted-content-152931.html | PRESS (reporting Meta post) |
| **Creator Fast Track (bonus program).** Up to $3,000/month for established creators who start posting Reels and FB video; $1,000/month at ≥100K followers on IG, TikTok or YouTube. | 2026-03-18 | https://www.tubefilter.com/2026/03/18/meta-creator-fast-track-payouts/ | PRESS. No AI-specific exclusion found, but the originality rules apply. |
| **Instagram opt-in "AI creator" label (test).** An account-level label for creators who frequently use AI. Post-level "AI info" tags take priority. No ranking impact during the test. | 2026-05 | https://yourstory.com/ai-story/instagram-ai-creator-label-test | PRESS |
| **Label renamed to "AI-generated profile".** Profiles featuring **AI-generated people without the label get reduced reach**. Labeled profiles are **not** penalized for having an AI person. AI used for edits, captions or graphics doesn't need the label. | **2026-08-31** | https://techcrunch.com/2026/08/31/instagram-puts-new-limits-on-undisclosed-ai-profiles/ ; https://mediapost.com/publications/article/417580/instagram-limits-reach-for-creator-profiles-withou.html | PRESS |
| **Mosseri year-end posts.** "Authenticity is becoming infinitely reproducible". It will be "more practical to fingerprint real media than fake media". For creators, the bar is shifting to whether you can "make something that only you could create". | ~2025-12-31 / reported 2026-01-06 | https://www.tubefilter.com/2026/01/06/adam-mosseri-instagram-warning-generative-ai-deepfakes/ ; https://www.techradar.com/ai-platforms-assistants/ai-slop-won-in-2025-fingerprinting-real-content-might-be-the-answer-in-2026 | OFFICIAL (Threads) via PRESS |
| **IG anti-aggregator rule extended platform-wide** (accounts that mostly share others' content aren't recommended). | 2026-04-30 | see `04` §5 | SECONDARY |
| **Regulatory driver.** EU AI Act Art. 50 transparency obligations apply from 2026-08-02. | 2026 | https://www.etvbharat.com/en/technology/ai-generated-profile-label-instagram-ai-transparency-instagram-enn26090203875 | PRESS (legal detail not independently checked) |

**Meta takeaway:** AI isn't excluded from monetization. What gets punished is unoriginal or reposted content and **unlabeled synthetic people**. A labeled AI character is OK.

---

## 4. Case studies

### 4.1 AI channels and accounts that grew and stayed monetized or commercially viable (2025–2026)

| # | Account | Platform / size (date) | What they do | Why it survives | Grade |
|---|---|---|---|---|---|
| 1 | **Neural Viz** (Josh Wallace Kerrigan, ex-screenwriter) | YT **238K subs, 14.9M views, 57 videos** (vidIQ 2026-10-15; +6K subs and +2M views over 12 months). IG ~860K (CreatorDB 2026-10-02). | A shared fictional universe (the "Monoverse") with a recurring protagonist (Tiggy Skibbles), mockumentary and talk-show formats. Human-written comedy; Midjourney/Runway/Sora/ElevenLabs pipeline. | **Low volume** (5 uploads/yr), a human author, a coherent world and characters, transformative and absurdist rather than realistic. Fits "AI to visualize a unique character and narrative you invented" exactly. Live and growing, with no enforcement reported. | vidIQ data + SECONDARY profiles (https://creatordb.app/creatorstats/neuralviz/ ; https://www.creativebloq.com/ai/how-one-creator-is-using-ai-to-build-an-entire-transmedia-sci-fi-universe). Monetization status not publicly confirmed. |
| 2 | **Granny Spills** (Blur Studios: Eric Suerez, Adam Vaserstein) | ~1M IG in weeks, ~400K TikTok (TIME 2025-11-19). Later ~2M IG claimed. | One persona (a blunt grandma in pink suits) with a recurring voice. Claude drafts scripts, which humans refine, then Veo renders. Dozens of videos a month. | Persona = IP. Revenue moved **off** TikTok Creator Rewards (which flagged it "unoriginal") to brand deals (Kurt Geiger, Papi Steak [SECONDARY]), Cameo, FB and YT. **A lesson in platform risk.** | PRESS (TIME); brand names SECONDARY |
| 3 | **HarperCollins × Toonstar** AI-animated series (first title: *Friendship List*) | YouTube, announced 2026-04-03 | Licensed book IP, 2–10-minute episodes. Human artists' work goes through Toonstar's "Ink & Pixel" AI, and authors are consulted and paid royalties. | Real IP, human art direction, episodic narrative, long-form. Corporate-grade "not slop". | PRESS — https://www.tubefilter.com/2026/04/03/youtube-harpercollins-toonstar/amp/ |
| 4 | **Animaj** (owner of *Pocoyo*) | 242M unique monthly YouTube viewers (company claim); Google AI Futures Fund backing, 2026-03 | An AI-accelerated kids'-animation pipeline (concept to release in under 5 weeks) on established characters. | Owned IP, a studio pipeline, a brand-safe kids' format. | SECONDARY / company claim — https://www.animaj.com/post/animaj-joins-googles-ai-futures-fund-to-redefine-how-kids-content-gets-made |
| 5 | ***On This Day… 1776*** (Darren Aronofsky's Primordial Soup with DeepMind) | Weekly on TIME's YouTube channel through 2026 | Historical anthology series, made with AI under a named director. | Human direction, research and an editorial brand. | SECONDARY — https://www.letsdatascience.com/news/aronofsky-creates-ai-recreated-american-revolution-series-3b6d0ef3 |
| 6 | **Bigfoot vlogs, e.g. "Speedilla"** (creator Mo, Hamburg) | TikTok/IG/YT, tens of thousands of followers and brand offers (2025) | A recurring character in POV "vlog" format (Veo 3), obviously fictional. | A character with continuity and clearly unrealistic content (no deception). Earnings claims for the format come mostly from guide-sellers. | SECONDARY / UNVERIFIED — https://hackernoon.com/bigfoot-was-just-the-beginning-of-the-content-revolution-an-ai-renaissance |
| 7 | **FUNTASTIC** (AI kitten and dad, Philippines) | ~600K YT subs (NPR, 2025) | 1–2 clips a day on one recurring premise. | A recurring cast, but it sits **close to the "repetitive" line**. Status after the July 2026 clarification is unknown. | PRESS (NPR via excerpt), status UNVERIFIED |
| 8 | **Riki TV, Rbrain Project** | On Tubefilter's Global Top 50 (2026-01-29) | Mass-appeal AI animation. | Shows that enforcement is uneven, **not** that the model is safe. | PRESS |
| — | ***Fruit Love Island*** (anonymous "Ai Cinema") | TikTok, ~10M views/episode, 300M+ total (2026-03) | A serialized dating-show parody with fruit characters, cliffhangers and audience votes on outcomes. | **Proved** that story, recurring characters and audience participation can scale AI content. **But** ITV threatened action over its trademark and the creator ended the series after mass reports. **Lesson: borrowing someone else's brand caps the upside.** | PRESS — https://the-decoder.com/ai-generated-dating-show-pulls-10-million-views-per-episode-on-tiktok/ (2026-03-30); https://thetriangle.org/article/the-rise-and-fall-of-fruit-love-island |

### 4.2 AI channels that got hit, and why

| Account | Action | Root cause |
|---|---|---|
| **Screen Culture / KH Studio** | Demonetized in 2025, **terminated December 2025** | **Deceptive** fake trailers built on real studio IP, misleading metadata, and **relapse** after reinstatement. |
| **CuentosFacinantes** (~6M subs) | Removed, January 2026 | **Someone else's IP** (Dragon Ball) and **templated episodes** that differed only in names and plot fragments. |
| **Imperio de Jesus** (~5.9M) | Removed, January 2026 | **Several uploads a day** of near-identical AI-narrated religious serials (mass production plus emotional bait). |
| **True Crime Case Files** | Terminated 2025 | **Fabricated "true" events** with no disclosure; real-world confusion. |
| **Granny Spills on TikTok** | Removed from Creator Rewards, 2025 | Platform judged AI-visual persona content "unoriginal or low-quality". The account survived; **the payout didn't**. |
| **HPad** (not AI, same rule) | Demonetized, July 2026 | Repetitive destruction format → "unsatisfying or off-putting". Same rule bucket AI shock clips fall into. |
| *Fruit Love Island* | Self-ended, 2026 | Trademark conflict (ITV) and mass reporting. |

**Pattern:**
- The **survivors** all have an author, a named character or owned/licensed IP, a world with continuity, a pace measured in episodes not hourly drops, and diversified income.
- The **casualties** were deceptive, IP-infringing, templated, or shock/emotional bait, and published at factory volume.

---

## 5. Checklist: "not slop", monetizable AI channel (Oct 2026)

**Identity and IP**
1. **Own a recurring character, cast or world.** Name the characters and keep their look, voice and personality consistent. Never use someone else's franchise, brand or format name (Dragon Ball, Marvel, *Love Island*).
2. **Never synthesize a real person's face or voice**, including the streamer you cover. YouTube likeness detection now covers every adult creator.
3. Never put an AI persona in the role of a human **doctor, lawyer, financial advisor or political expert**. A disclosure or human script doesn't make it monetizable.

**Human authorship (the "only you could make this" test)**

4. A human writes or approves every script, with a setup → turn → payoff arc. Keep drafts and notes as proof of authorship in case you need to appeal.
5. Add a human layer viewers can perceive: your own narration, voice-over of your own cloned voice (no disclosure needed), commentary or perspective, or hand-directed editing.
6. Each episode must have a **distinct premise**. The title test is: "could this video have come from any channel?" If yes, don't post it.

**Format hygiene**

7. **No slideshows, scrolling text, stitched unrelated AI clips, or "AI-voice narrates stock footage"** formats.
8. **No shock or manipulation bait.** That rules out animals in distress, fake disasters, fake celebrity deaths, and staged suffering without a story.
9. **No fabricated "real" events** (fake true crime, fake news, fake trailers presented as real).

**Disclosure and labels**

10. Tick YouTube's "altered or synthetic" box for anything **realistic**. It doesn't cost reach or money; failing to disclose risks YPP suspension.
11. Use TikTok's AIGC label for realistic AI. On Instagram, apply "AI-generated profile" if the persona is an AI person. Unlabeled AI people get reach cut since 2026-08-31.
12. Keep C2PA/SynthID metadata intact. Don't strip it to dodge labels.

**Cadence and volume**

13. Publish at a sustainable "show" pace, **not** several near-identical uploads a day. Volume plus sameness is the main channel-level demonetization trigger.
14. Review the last ~20–30 uploads as a set. If they look templated together, change the format before YouTube does it for you.

**Revenue and platform risk**

15. Treat TikTok Creator Rewards as **unreliable** for AI-visual content. Flags for "unoriginal" are common. Plan on YouTube YPP (long-form especially), Meta, brand deals, licensing, Cameo and merch.
16. Build owned IP (the character), so the business survives one platform demonetizing it.
17. After any demonetization: fix the pattern and the labels, then appeal. **Never relapse after reinstatement.** That is what turned Screen Culture's demonetization into termination.

**Applying this to the bart-clips project**
- AI may be used as *editing/visual tooling* on top of clips with real commentary (see `04` Rules).
- An AI-generated version of Joe himself (face or voice) is off-limits.
- An original AI mascot or host character that comments on clips is the compliant way to add a "face" to a faceless channel. It should be human-written, consistently designed, and labeled where realistic.

---

## Gaps / not verified
- TikTok's own Creator Rewards and Community Guidelines pages didn't render to the fetcher. AI-eligibility wording is from search snippets and press.
- Whether Bandar Apna Dost, FUNTASTIC, Riki TV and Rbrain are currently monetized is unknown; only liveness or chart presence was checked.
- There is no official YouTube statement on Veo/AI Shorts and YPP beyond the general policy text.
- Neural Viz monetization and deals are not publicly confirmed.
- Granny Spills revenue is undisclosed.
