# 02 — Competitor analysis: Joe Bartolozzi clip channels (Shorts)

Pulled 2026-10-15 via vidIQ MCP (channel_search, similar_channels, get_channels_by_ids, channel_stats, channel_videos). About 305 credits spent.
Tags: **[M]** = measured (taken straight from vidIQ output). **[I]** = inference or interpretation. Neither is a guess: every [I] names the [M] data it rests on.

Notes on method:
- "30d growth" is vidIQ's `subsGrowth30d` / `viewsGrowth30d` (%) unless a channel_stats daily series is cited.
- "Shorts/30d" is vidIQ's `shortVideoCount30d`. "Avg views" is vidIQ's lifetime `avgViews` (total views ÷ videos).
- Best and worst Shorts come from `channel_videos` with popular=true for best and popular=false (the last ~50 uploads) for worst. Worst picks skip uploads under 3 days old.
- Zinkk's popular=true call was rate-limited twice and never returned. Its "best" comes from the recent list only. BartaliniClips' video lists were not pulled (vidIQ search metrics only).

---

## 1. Comparison table

| Channel | Subs [M] | Subs 30d [M] | Views 30d [M] | Shorts/30d [M] | Avg short len 30d [M] | Avg views (lifetime) [M] | Last upload [M] | Status [I] |
|---|---|---|---|---|---|---|---|---|
| **Certified Bart** (us) | 943 | **−2 subs** (945→943, channel_stats) | +1,776 views in 30d | 1 (Sep 15, 0 views) | ~22s (Aug–Sep uploads) | ~1.9k (304k/161) | 2026-09-15 | Stalled |
| JB Highlights @jbarthighlights | 31,600 | +13.26% | +12.58% | 31 | 22.8s | 664k | 2026-10-15 | Winner |
| quikraid @quikraid | 24,200 | +3.86% | +6.67% (16.05M short views/30d) | 26 | 39.6s | 573k | 2026-10-15 | Winner (mature) |
| Zinkk @zinkzx | 25,800 | **+175.94%** | +95.13% | 45 | 11.9s | 542k | 2026-10-15 | Winner (moved off Joe) |
| Not The Real Joe Bart @nottherealjoebart | 22,200 | +10.45% | −0.11% | 24 | 56.2s | 502k | 2026-10-12 | Winner, plateauing |
| jynxzi&bartolozziclips @jynxzibart | 5,830 | **+362.7%** | +104.02% | 34 | 26.6s | 164k | 2026-10-15 | Breakout winner |
| BartaliniClips @bartaliniclips | 8,570 | +10.72% | +11.81% | 87 | 44.6s | 103k | 2026-10-13 | Volume grinder |
| Q Memes @q_memes | 8,410 | +1.20% | +2.28% | 9 | 8.4s | 52k | 2026-10-10 | Slowing |
| Joe Clipolozzi @joe-clipolozzi | 9,450 | +53.41% | +71.48% | 0 | — | 274k | 2026-09-03 | Stalled after one viral hit |
| TopDawg43 @topdawg43 | 5,700 | +1.42% | +2.44% (909k short views/30d from back catalog) | 0 | — | 122k | 2026-01-22 | Abandoned |
| _JoeBartolozzi_Clips_ (known competitor) | 4,320 | +30 subs (4,290→4,320) | +99,147 views | 0 | — | 27k (5.43M/198) | 2026-01-19 | Abandoned |
| JoeBartolozziClipz⚡ (known competitor) | 1,170 | −10 subs (1,180→1,170, Sep 15→Oct 15) | ~+5k views | 0 | — | 21k | 2026-09-08 | Stalled |
| Joe Bartolozzi Shorts @joebartshorts (Joe's own) | 203,000 | n/a | n/a | 0 | — | 264k (43.1M/163) | **2025-05-03** | Dormant 17+ months |

Other Joe-clip channels found but not profiled [M]: JoeBartClipped 4.8k (last upload Aug 11), Joebart Highlights 5.54k (1 short/30d), Bart_clips99 3.7k (+5.11%, 29 shorts/30d), Jynxzi & Joe Moments 2.66k (last upload Sep 15), SiteOfClips 19.9k (+2.05%). The similar-channels call on the known competitor also returned small Joe channels under 1k subs: Joe Bart Moments 292 (+53.7%), JoeMomentsMedia 437, PrxtigeClips 739 (+51.4%), TheJoeBartPage 397, Joint Bart Clips 278, JoeBartClips 136.

Fast-growing **general** streamer-clip Shorts channels (breakout, created after 2024-10-15, 1k+ subs, sorted by 30d sub growth) [M]:

| Channel | Subs | Subs 30d | Shorts/30d | Avg len 30d | Focus |
|---|---|---|---|---|---|
| ABESON CLIPS | 2,310 | +402% | 59 | 16.5s | multi-streamer |
| YtClipsOnly | 1,510 | +228% | 27 | 31.2s | one streamer (shakyboats) |
| Yonna Cuts | 1,660 | +206% | 56 | 19.3s | one streamer (Yonna Jay) |
| RankifyLoL | 4,210 | +194% | 19 | 97.6s | ranked compilations |
| ClipThatToo | 2,620 | +185% | 30 | 35.3s | Kai Cenat and others |
| Aura Clips | 21,400 | +124% | 40 | 48.1s | IShowSpeed/MrBeast/viral |
| brenduh.extras | 1,800 | +89% | 59 | 18.3s | one streamer (Brenduh) |
| PerfectCl1ps | 2,700 | +89% | 46 | 32.5s | multi-streamer |
| ClipWise | 6,260 | +76% | 36 | 19.8s | multi-streamer |
| Pixly Edits | 2,710 | +74% | 46 | 21.7s | Jynxzi |

[I] What the breakout set has in common: 27–59 Shorts a month (about 1–2 a day), an average length of 16–35s (RankifyLoL is the exception), and often a single creator as the focus.

---

## 2. Best and worst Shorts per channel [M]

**Certified Bart.** Best: "Joe Bartolozzi Roasts People Who Fake Smile at TikToks" 71,384 (21s, Aug 18); "Can't Decide Erase Worst Memory or Relive Best" 24,147; "Comforts Fan Who Has Type 1 Diabetes" 22,078; "Drops $50K on Charities Chat Picked" 20,857. Worst: "Gambling Quits & Goat Dilemmas" **0 views** (Sep 15, latest upload); re-uploads "Reacts to Drunk Driver Who Forgot How to Talk" 69 (the original got 1,605), "Most Unhinged Bar Ever" 3, "Friends Try Scorpion Shots" 4, "Swinger Setup" 21, "Almost Cries Talking About His Grandpa" 53. Off-topic uploads (Mater/Cars theories, Boltzmann brain, "Serial Killers vs Mass Shooters", "Facing Mortality") each landed at ~430–1,100.

**JB Highlights.** Best: "\"We really got him good\" 😭🥀 | Joe Bartolozzi" 30.77M (33s); "Bro's tryna aura farm ☠️" 12.78M (20s); "\"No biggie we wipe\"" 10.78M (8s); "Simon is rigged" 5.98M; "Mcdonalds is not a 5/5 💔" 5.53M. Worst (recent): "Dude is a weirdo ☠️" 21,507; "Jumpscare so bad it turned bros camera off" 24,375; "Tiktok was not this bad" 30,603. Floor of the last 50 uploads is about 18k–37k.

**quikraid.** Best: "Joe advertises an awesome diaper brand" 15.70M; "Joe Bart frame mogging Ron" 10.82M; "HORRIBLE misread😭😭" 10.77M; "Joe bans an innocent chatter" 8.81M; "\"Your gonna get an easy one\"" 7.32M. Worst: "\"Just make sure the toaster is unplugged first\"😭💔" 1,747 (no "|| Joe Bartolozzi" tag); "Joe uses a blow dart" 5,000; "Joe flexing to start the stream" 13,820.

**Zinkk.** Best (recent list only): "blind vs deaf vs mute 💀" 37.49M (14s, Oct 8); "she got caught 🥀✌️" 5.28M; "#sing" 4.06M; "Someone watch lil bro" 1.55M. Worst: "Lil bro is getting lonely" 4,458; "Useful cat" 5,692. [M] None of the last 50 titles mention Joe. [I] The channel is filed under Joe Bartolozzi but now posts general memes.

**Not The Real Joe Bart.** Best: "Joe Bart Reacts To Ludwig Targetting The CEO Of Twitch!!!" 47.19M; "…Pokimane Eliminating Arky!!!" 39.33M; "…Jasontheween Going Band For Band" 7.73M; "Joe Bart And Lacy Get Flamed" 5.72M; "Joe Bart Investigates Weird Sound In Airbnb (storytime)" 3.73M (1m25s); "Explains How Horrifying The T-Rex Actually Was" 2.09M (1m22s). Weakest in its top-50: "Reacting To British Kids Trying Takis" 55k. Milestones in the channel description: 2k subs Apr 22 → 10k Jun 23, 2026.

**jynxzi&bartolozziclips.** Best: "Joe Bart & Deji Took This Spelling Battle TOO Far 🤬😭" 9.24M (2m3s, Oct 4); "Ludwig Got Elite Ball Knowledge" 2.09M; "Joe Bart EDITOR Salary EXPLAINED" 1.99M; "Joe Take On Streamer University" 1.93M. Worst: "USA Top SECRET Mission In North Korea" 1,889 (no Joe in the title); "Joe Barts CRAZIEST Bus Ride Story" 1,956; "Joe Bart Was DISGUSTED…" 568 after 3 days.

**Joe Clipolozzi.** Best: "Joe Bart plays VOICE CHOICER😮" 11.98M (Aug 14). Every other upload: 1,206–69,798. It posted twice a day (11:00 and 17:00 UTC) from Aug 7, then **stopped on Sep 3**, 20 days after the hit.

**TopDawg43.** Best (in the last-50 list): "\"What's with all the meat man\"" 3.00M; "Joe Bart loves Abby" 1.27M; "Joe = 😐" 806k. Worst: "Joe reacts to his most angry clip" 2,757; "Joe attempts to break pencils" 2,776. It posted 2–4 a day Jan 1–22, 2026, then has posted nothing since. Titles carried 6–9 hashtags.

**_JoeBartolozzi_Clips_.** Best: "August 5th Incident #joebartolozzi #twitchclips" 2.57M; "I been in the hill" 1.83M; everything else at 134k or below. Worst: "Say that again Joe" 4,014; "Joe caked up all on wall" 1,644. It batch-uploaded 5–14 clips on a single day (Sep 14, Sep 22, Oct 4, Oct 17, Nov 1 2025; Jan 19 2026), then went silent.

**JoeBartolozziClipz⚡.** Best: "Cursed Costco guys animation 💀" 735,669; "funniest fake Gta 6 moments" 90,203; "Joe Ranks His Most Painful Tattoos" 84,147. Worst: "Joe Bart Core 😂" 1,585; "What is bro doing 😂" 1,666; "Joe explains larping" 1,285.

---

## 3. @joebartshorts: Joe's own top Shorts [M]

203k subs, 163 videos, **last upload 2025-05-03**. Top by views:

| Rank | Title | Views | Published | Length |
|---|---|---|---|---|
| 1 | Jumping on boats | 26,195,108 | 2022-02-21 | 30s |
| 2 | Slim shady in old house | 4,541,485 | 2022-04-26 | 30s |
| 3 | I counted | 652,670 | 2022-11-07 | 49s |
| 4 | What | 525,608 | 2022-02-28 | 30s |
| 5 | Oh no | 366,396 | 2022-11-01 | 21s |
| 6 | Selling snacks in school | 229,746 | 2022-02-12 | 36s |
| 7 | Why | 203,891 | 2022-11-07 | 20s |
| 8 | February 13, 2023 | 200,274 | 2023-02-14 | 58s |
| 9 | How do they live | 187,585 | 2023-02-14 | 23s |
| 10 | May 3, 2025 | 185,479 | 2025-05-03 | 52s |
| 11 | Road rage | 185,412 | 2022-04-26 | 24s |

Measured patterns: 10 of the top 11 were posted in 2022–Feb 2023. The 2024–2025 uploads (stream-clip style, e.g. "It's way worse" 55k, "Impossible to win" 56k, "Still gave 5 stars" 74k) mostly sit at 11k–85k. Joe's own titles are 1–4 words with no context ("Why", "What", "Bro").
[I] From the titles alone, the outliers are IRL skit/stunt moments ("Jumping on boats", Eminem in an old house, "Selling snacks in school", soccer/mascot pranks), not stream reactions. We did not watch the clips, so this describes the topic, not a verified moment. [I] Fan channels win partly because they add context Joe's own titles leave out (a quoted line plus a creator tag).

---

## 4. Winners vs stalled: what differs

**Cadence and consistency [M]**
- Every channel growing now posted 24–87 Shorts in the last 30d: JB Highlights about 1 a day, usually around 23:00 UTC; quikraid about 1 a day at 01:00–03:00 UTC.
- Every stalled channel posted 0 in the last 30d: TopDawg43, _JoeBartolozzi_Clips_, Joe Clipolozzi, JoeBartolozziClipz. Certified Bart posted 1, and that one has 0 views.
- Certified Bart's own record: about daily Jul 2–24, a **24-day gap** (Jul 24 → Aug 17), daily Aug 17–Sep 12, then nothing since Sep 15.

**When they stalled [M]**
- Joe Clipolozzi: 20 days after a 12M hit. Its follow-ups did 2k–70k, then it stopped.
- JoeBartolozziClipz: 115 → 1,010 subs Jul 1–Aug 11 while posting ~60 Shorts in July. On Aug 13–14 its videos went 94→87 and total views 3.23M→1.29M. Uploads then dropped to about one every few days, and it stopped Sep 8. [I] The removed videos held most of its views, so this was likely takedowns or deletions, not a gradual decline.
- TopDawg43 stopped after 3 weeks of 2–4 a day, despite several 0.5–3M hits.
- _JoeBartolozzi_Clips_ batch-uploaded and went silent after Jan 19.

**Titles [M]**
- Winners lead with a hook built from Joe's own words or a reaction, then add a creator tag and 1–2 emojis:
  - JB Highlights: `"We really got him good" 😭🥀 | Joe Bartolozzi`
  - quikraid: `HORRIBLE misread😭😭 || Joe Bartolozzi`
  - Not The Real Joe Bart: `Joe Bart Reacts To X!!!`
  - jynxzibart: `Joe Bart & Deji Took This … TOO Far 🤬😭`
- Stalled channels used vague or hashtag-stuffed titles ("What what #joebartolozzi #twitchclips"; TopDawg43's 6–9 hashtags), or a rigid template. Certified Bart repeats `Joe Bartolozzi Can't Decide/Can't Believe …` (11 of its Aug 17–Sep 3 uploads).
- [I] Template titles probably aren't the main problem. Certified Bart's best upload (71k) used the same `Joe Bartolozzi Roasts…` structure. Cadence and topic explain more of the gap.

**Length [M]**
- Winners' 30d average length runs 11.9s (Zinkk) to 39.6s (quikraid). Not The Real Joe Bart is the exception at 56s, and its 1–2 min storytime/"Joe Bart Explains" clips reach 1.4–3.7M.
- Certified Bart's July uploads ran 1m07s–1m29s and got ~430–1,170 views. Its Aug 17–28 uploads ran 17–25s and include all four of its 20k+ Shorts.
- [I] Length alone doesn't decide it: long clips work for Not The Real Joe Bart when they are a story told by Joe, and fail for Certified Bart when the topic isn't about Joe.

**Topics [M]**
- The biggest hits are streamer-world crossovers or a single quotable Joe moment:
  - Ludwig/Twitch CEO 47M and Pokimane 39M (Not The Real Joe Bart)
  - Deji spelling battle 9.2M (jynxzibart)
  - Jynxzi/Ron moments (quikraid 10.8M "frame mogging Ron")
  - Relatable rants: "Mcdonalds is not a 5/5" 5.53M on JB Highlights
- Certified Bart's off-niche philosophy/Pixar/true-crime uploads got about 1k each.

**Same moment, several channels, speed matters [M]**

| Moment | First poster | Later poster |
|---|---|---|
| "McDonald's is not a 5/5" | JB Highlights, Sep 3: 5.53M | quikraid, Sep 6: 968k |
| "Boy shut the freak up" | quikraid, Aug 30: 44.6k | JB Highlights, Sep 14: 685k |
| "Type in chat" recreation | JB Highlights: 1.43M and 555k | Joe Clipolozzi: 27.9k |

[I] Posting first helps but doesn't settle it. In the second row the later post won by 15x, and JB Highlights' size (31.6k subs) probably carries part of it.

**Upload hygiene [M]**
- Certified Bart has at least 5 duplicate or re-uploaded Shorts that drew 3–69 views, and a latest upload with 0 views.
- [I] Duplicates may be suppressed as reused content. Check this in YouTube Studio; vidIQ can't confirm it.

---

## 5. Gap and opportunity for Certified Bart

1. **Joe's own Shorts feed is empty [M].** @joebartshorts hasn't posted since 2025-05-03, while Joe's main channel has 6.07M subs. Fan channels are serving all of the Shorts demand.
2. **Shelf space is opening [M].** Five Joe clip channels went quiet in 2026: TopDawg43 (Jan 22), _JoeBartolozzi_Clips_ (Jan 19), JoeBartClipped (Aug 11), Joe Clipolozzi (Sep 3), JoeBartolozziClipz (Sep 8). TopDawg43 still draws 909k Short views a month from its back catalog [M]. [I] That audience has nowhere new to go.
3. **Formats the leaders don't own [I, from the measured top lists]:**
   - JB Highlights and quikraid own short quote-hook clips under 35s.
   - Not The Real Joe Bart owns "Joe Bart Explains/storytime" at 1–2 min.
   - jynxzibart owns collab/crossover moments.
   - Nobody profiled owns **Joe's philosophy/"deep thoughts" side tied directly to Joe.** Certified Bart's channel description already promises this. Its attempts failed because the clips weren't framed around Joe (Boltzmann brain, Mater ≈1k). Joe-framed "Can't Decide" hypotheticals did 2.5k–24k.
   - Not The Real Joe Bart's "Explains" clips (T-Rex 2.09M, "Worst Time Period To Be Alive" 277k) show Joe-explains-a-big-idea can scale.
4. **Fix the basics first [M → I]:**
   - (a) Post daily without gaps. Every channel growing in the last 30d posted 24+ times; Certified Bart posted 1.
   - (b) Keep it to 15–35s unless the clip is a full story.
   - (c) Stop duplicate re-uploads.
   - (d) Use a quote or reaction hook plus a "| Joe Bartolozzi" tag.
   - (e) Clip new stream moments within 24–72h; the McDonald's/"Boy shut the freak up" pairs show the payoff isn't automatic.
5. **Risk [M → I]:** JoeBartolozziClipz lost 7 videos and ~60% of its total views overnight (Aug 13–14). [I] Likely takedowns. Lean on transformative edits (captions, context, commentary) the way jynxzibart and Yonna Cuts describe in their channel descriptions.
6. **Benchmarks to hit [M]:**
   - Floor: JB Highlights' last 50 uploads bottom out at about 18–37k. Most of Certified Bart's last 50 uploads sit at 1–6k [M]; the exact median was not computed.
   - Ceiling: the breakout channels reached +75–400% subs in 30d by posting 27–59 Shorts in that 30d.
