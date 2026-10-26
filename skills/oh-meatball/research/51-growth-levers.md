# 51 · Growth levers beyond "make more videos" (Growth desk, 2026-10-26)

**Brief (Nolan).** "We need to keep growing. Find ways we can grow differently." Then: "make all of those" (every YouTube
lever), and he's running a paid TikTok Promote campaign himself.
**Constraints.** YouTube and TikTok only. No spend beyond vidIQ credits (Nolan's own Promote budget is his). Honest,
policy-safe tactics only. Replies, comments and Community posts need Nolan's approval of the exact text. Gmail is drafts only.

**Credits: 30 vidIQ** (keyword_research ×4 = 20, similar_channels 5, channel_search 5). Balance 478 → 448; the reserve
floor of 400 holds. Free sources: yt-dlp (our live view counts, rivals' latest titles), Metricool (TikTok followers and
posts), Google's help pages and the Promote playbook.

## 0. What the data says (read first)

| Fact | Number | Source |
|---|---|---|
| YouTube Shorts, lifetime public views (17 live) | **~14,900**; median ~900; best 1,900 (daddy longlegs) | yt-dlp 10/26 |
| YouTube long-forms, lifetime views (4 live) | **102 in total** (wolves 55, animal-facts 39, extinct 4, 12-myths 4) | yt-dlp 10/26 |
| Long-form views as a share of Shorts views | **0.7%** | — |
| Subscribers gained per 1k views | 1.11 channel-wide (target 3) | research/46 |
| Case long-forms that are public | **0**. The case Shorts (20 of them, 10/26-11/4) can't send viewers anywhere relevant. `Conspiracy Theories That Turned Out To Be TRUE` is rendered but **not queued** | data/posted.csv, episodes/longform-turned-out-true |
| Long-form thumbnail for that episode | **missing** (release.json points at a thumb.jpg that didn't exist). Made today: §4 | episodes/longform-turned-out-true |
| TikTok followers | **9,319**, 681 short of 10K | Metricool 10/25 |
| TikTok views per post | **median 207** (17 posts since 10/23); best 763 | Metricool posts |
| TikTok traffic from search / followers | not reported yet for any post (Metricool fields empty) | Metricool |
| YouTube channel banner and description | still "MEATBALL MYTHS · TRUE OR FALSE? · Everything you know about animals is wrong" | brand/banner.jpg |

**Three conclusions:**
1. **Discovery works, conversion doesn't.** Shorts find ~1,000 strangers each. Almost none of them reach a long-form,
   subscribe, or come back. The levers with the most upside fix the *after-the-view* path: a long-form to send them to,
   a channel page that says what we are, playlists that chain cases, and a reason to subscribe.
2. **Long-form discovery has to come from search.** Browse has given our long-forms nothing. One search-matched
   episode at 5k-50k views and 3 min AVD is worth 250-2,500 watch hours. Hundreds of 20 s Shorts are worth 0 (Shorts-feed
   hours don't count, YouTube Help 72851).
3. **On TikTok, followers aren't the problem; views are.** 9.3K followers, ~200 views a post. Creator Rewards needs
   100K views in 30 days. Promote buys followers, not qualified views. The free levers there are TikTok search, Stitch
   and a profile that converts.

## 1. The levers, ranked (expected impact ÷ effort)

| # | Lever | Impact | Effort | Who | One-week test and success metric | Status |
|---|---|---|---|---|---|---|
| 1 | **Shorts → long-form funnel.** Publish the case long-form now, then set Related video on every Short (data/related-video-map.csv: all 80 YouTube Shorts mapped) | **High.** Our only path from ~1,000-view Shorts to watch hours. Case Shorts get ~20 posts in 9 days | Low (Nolan ~1 min per Short in Studio; postmaster queues the long-form) | postmaster, Nolan | From the day `Turned Out TRUE` is public: **≥ 300 views in 7 days** (our best long-form has 55 lifetime) and **≥ 30% of its views from Shorts** (Studio → Analytics → Traffic source "Shorts feed" / related video) | Map done; long-form not queued (owner: postmaster/mayor) |
| 2 | **Search-first long-forms** (research/51-search-slate.md: 8 titles with keyword numbers; Bermuda and Roanoke scripted, both pass retention.py) | **High** (the watch-hour path: one hit = 250-2,500 h) | High (a 5-7 min episode each; scripts done, render by studio) | showrunner, studio, packager | First slate episode: **YouTube search ≥ 20% of its views by day 7** and ≥ 500 views by day 14 | 2 scripts done |
| 3 | **Channel packaging:** name, banner, avatar, description, keywords, 4 playlists, home layout, 36 s trailer, watermark (§2) | **Medium-high.** Every Short viewer who taps our name lands on a page that still says "animal TRUE OR FALSE quiz" | Low (Nolan ~8 min) | Nolan; assets done | Week after vs week before: **subs per 1k views ≥ 1.5** (from 1.11); views from "Channel pages" and "Playlist" traffic sources > 0 | Assets done (episodes/branding/) |
| 4 | **TikTok profile and TikTok SEO** (research/51-tiktok-playbook.md §1-3): name, bio, pins, playlists, searched phrase as caption line 1 | Medium | Low | Nolan (profile, 3 min), postmaster (captions) | **TikTok search ≥ 5% of views** on the week's case posts (Metricool TKPO21); profile views up week over week (TKEV09) | Copy done |
| 5 | **Nolan's TikTok Promote (E-promote)**, used well: a case video with series identity, pins and daily cases while it runs, pause on cost per follower | Medium (closes the 681-follower gap; views gap stays) | His spend; our effort low | Nolan, intel | Cost per follower under Nolan's cap; **median views per post the week after ≥ 1.2x the week before** (~200), else the followers aren't an audience | Logged (experiments.csv) |
| 6 | **Weird-news fast lane:** a same-day "Meatball Investigates" Short on a strange discovery or declassified file (§5) | Medium-high, high variance (news Shorts ride search spikes) | Medium (one rush script a week) | intel, showrunner, factdesk, studio | **2 news Shorts in 7 days, ≥ 1.5x the case median at 48 h**, posted ≤ 8 h after the source story | Routine written (OPERATIONS, TOWN) |
| 7 | **Community posts + polls** and a pre-approved reply bank (research/51-community-posts.md) | Medium (wakes up the 956 old subscribers; polls are one-tap engagement) | Low (Nolan ~1 min a day) | host drafts, Nolan posts | **≥ 30 votes on each of the 3 polls**; channel comments/1k ≥ 3 | 7 posts ready |
| 8 | **Stitch the viral claim** for Verdict on the Viral One (TikTok, in-app) | Medium (the claim's audience is shown the reply) | Low (Nolan 2 min a week) | intel picks, Nolan posts | Stitch views at 48 h **≥** the un-stitched verdict deep cut's | Playbook §5 |
| 9 | **Collabs and shout-out swaps** with 10 small/mid channels (§6); 3 Gmail drafts | Medium, slow | Low | business, Nolan sends | **≥ 1 yes from 3 emails in 14 days**; a collab Short ≥ case median | 3 drafts in Gmail |
| 10 | **End screens + cards + subscribe watermark** on every long-form | Low-medium (only matters once long-forms get views; free) | Low | Nolan in Studio | End-screen click rate > 2% on the first case long-form (Studio → Analytics → Engagement) | Steps in checklist |
| 11 | **Part 2 chains and a weekly "Case Files" compilation** (research/50 idea 6) | Medium | Medium | showrunner | Existing double-down rule, applied to cases: any case at ≥ 3x the case median in 48 h gets a Part 2 Short within 7 days and a chapter in the next long-form. One Sunday compilation (new host links + one new case, never just stitched Shorts) | Proposal |
| 12 | **TikTok posting-time A/B** (18:00 vs 20:00 for Case B deep cuts, next pack only) | Low | Low | postmaster | Playbook §7 | Proposal |
| — | **YouTube Promote (paid)** | **Not now.** Promote subscribers and watch time don't count toward YPP (§7) | — | Nolan decides | Only if Nolan wants reach for its own sake: §7 | Not recommended |
| — | **Re-uploading Shorts that flopped** | **No.** Duplicates read as reused/repetitive content, the exact YPP rejection reason (research/27, 30). Instead: a *remake* with a new hook, new edit and new title, at most 1 a week, original left up | — | — | — | Rejected |

**Top 6 in one line each:** (1) put the case long-form live and link every Short to it; (2) win search with the slate;
(3) make the channel page say "Meatball Investigates"; (4) make TikTok findable and the profile convert; (5) use
Promote on a case video and judge it by later views, not by followers; (6) a same-day weird-news Short lane.

## 2. Channel packaging (assets in episodes/branding/)

### 2a. Name and handle: recommendation
**Display name: `Meatball Investigates`** on YouTube and TikTok. **Keep both handles (`@meatballmyths`).**
- Every case title already ends "Meatball Investigates", and the series tag on every frame says it. A viewer who searches
  that name should find a channel called that.
- "Myths" now frames us as the retired animal TRUE/FALSE quiz (research/42), and the new pillar is 75% non-animal.
- Keeping the handle keeps every link, the Metricool connection and the TikTok URL working. On YouTube a name change
  keeps subscribers and videos. YouTube limits name changes to a few per 14 days [YouTube Help: "Manage your channel's
  name & profile picture"], so do it once.
- For 30 days the About text says "(formerly Meatball Myths)" so returning viewers aren't confused.
- research/48 §4 recommended keeping "Meatball Myths" before the pivot had data. The difference now: the case series is
  the daily core (2 of 3 YouTube Shorts, OPERATIONS "Daily mix"). Nolan decides; it's a 1-minute change either way.

### 2b. Banner and avatar
- `episodes/branding/banner.jpg` (2560×1440). The title, tagline and PROVEN/BUSTED/UNSOLVED stamps sit inside the
  1546×423 all-device safe area (`banner_safe_preview.jpg` is what a phone shows). The cork wall and case cards outside
  it only show on desktop and TV. Rebuild: `PYTHONHASHSEED=7 python3 episodes/branding/make_branding.py`.
- `episodes/branding/avatar.png` (800×800): the same shocked Meatball face as before (recognition), on a manila case-file
  disc with a yellow lens ring. `avatar_96_preview.png` shows it at feed size.

### 2c. Channel trailer
`episodes/branding/trailer.mp4`: 16:9, ~36 s, theme `conspiracy`, music at −30 LUFS under the voice. Meatball at his
case desk says who he is. Then quick cuts from 6 real cases with their real verdicts: the Moon nuke (PROVEN), Roswell
(ALIENS BUSTED), the Bermuda Triangle (BUSTED), Kola "screams" (BUSTED), the Emu War (TRUE), the Mary Celeste
(UNSOLVED), MKUltra (PROVEN). Then the subscribe ask with the pill, and a Fork kicker. Script: `episodes/branding/trailer.json`.
**Upload as Unlisted**, so it doesn't post to subscribers' feeds as a "new video". Title "Meatball Investigates: what
this channel is". Then set it as the trailer for non-subscribers (checklist). [UNV: YouTube has accepted unlisted
trailers; if Studio refuses, upload it Public.]

### 2d. Channel description (Studio → Customization → Basic info → Description), paste exactly
```
Meatball investigates the weird: conspiracy theories, strange history, viral claims and very suspicious animals. Every case ends with a verdict (PROVEN, BUSTED or UNSOLVED), and the sources are in the description.

🔍 A new case every day (Shorts)
📂 Full investigations every Tuesday and Saturday
🕳️ The Verdict on the Viral One: every Wednesday
📨 Viewer Case Friday: comment a mystery on any video, and the top-liked one gets investigated

Real records, real sources, no fake "proof". Nothing is called true unless the evidence says so.
Animated with AI tools; the research and fact-checking are ours. (Formerly Meatball Myths.)
```

### 2e. Channel keywords (Studio → Settings → Channel → Basic info → Keywords), paste exactly
```
"meatball investigates" "meatball myths" "conspiracy theories" "conspiracy theories that turned out to be true" "strange history" "weird history" "historical mysteries" "unsolved mysteries" declassified "cold war secrets" "bermuda triangle" "mystery explained" mythbusting "weird animals" "animated history" debunked
```

### 2f. Playlists: create in this order (Studio → Content → Playlists → New playlist; Visibility Public)
Order matters: the first one created is the one we link most.

**1. `Meatball Investigates: Cases`**
Description: `Every case Meatball has opened, in order. Conspiracies, strange history and weird mysteries, each with a verdict (PROVEN, BUSTED or UNSOLVED) and real sources. New case every day.`
Videos, in case order (add each as it goes live; IDs fill in as they publish):
Case #1 Is the Bermuda Triangle Real? (10/27) · Nuke the Moon / A119 (10/26) · Roswell (10/26) · Operation Northwoods (10/26) ·
Dancing Plague (10/26) · #6 Lightning (10/27) · #7 Pig War (10/28) · #9 Bat Bombs (10/29) · #11 Gulf of Tonkin (10/30) ·
#12 Mary Celeste (10/30) · #13 Flannan Isles (10/31) · #16 Mike the Headless Chicken (10/31) · #10 CIA Spy Cat (11/1) ·
#15 Project Iceworm (11/1) · #18 Kola "Well to Hell" (11/2) · #17 Habakkuk (11/2) · #20 Laughter Epidemic (11/3) ·
#19 MKUltra (11/3) · #21 Emu War (11/4) · then the long-form `Conspiracy Theories That Turned Out To Be TRUE` as soon as it is public.
(#8 Glomar and #14 Cardiff Giant are TikTok-only.)

**2. `The Verdict on the Viral One`**
Description: `Every Wednesday Meatball takes the week's most viral mystery claim and rules on it: PROVEN, BUSTED or UNSOLVED, with the sources on screen. Send the next one in the comments.`
Videos: #1 Did 300 Years of History Never Happen? (Phantom Time, 10/28). Add each Wednesday.

**3. `Viewer Case Friday`**
Description: `You send the case, Meatball investigates. Comment a mystery, myth or viral claim on any video: the top-liked one gets investigated on Friday.`
Videos: empty until the first Viewer Case Friday posts. Create it now so the Home section and the pinned
comments can point to it.

**4. `Meatball vs Animals`**
Description: `The weirdest, deadliest and most suspicious animals on Earth, investigated by a meatball who'd rather not be eaten. Would Meatball Survive?, Meatball vs Spiders and more.`
Videos (live now, newest first): Pufferfish Poison (BPApE_A4SxE) · This Bird Fakes a Broken Wing (K9G9aHnurgs) ·
I Poked a Honey Badger (BbXgW3KPzdg) · Ghost Crabs Growl (OPeW46cLBOk) · I Tried to Outsmart a Box Jellyfish (TSAD-WKNAzs) ·
This Spider Hunts Other Spiders (A4-ltJOdto8) · I Tried to Befriend a Cassowary (nC1QZ1GqPxg) · Daddy Longlegs (Us0zIbxiR-A) ·
Elephants (Cy4Ap6Yak9A) · then the animal long-forms: How Wolves Became Dogs (Uqj0QL8G0d4), Animals Thought Extinct Found Alive (o9Emu9oMgCs).
Leave out the old "TRUE or FALSE" quiz Shorts. They're the retired format, and a playlist is a promise of what's next.
The scheduled animal Shorts (the 60 `pillar=animal` rows in data/related-video-map.csv) go in as they go live.

### 2g. Home tab layout (Studio → Customization → Layout)
- **Channel trailer for people who haven't subscribed:** the trailer (2c).
- **Featured video for returning subscribers:** the newest long-form; switch it to `Turned Out TRUE` when it's live.
- **Featured sections, top to bottom:** 1 Shorts · 2 Single playlist: Meatball Investigates: Cases · 3 Single playlist: The
  Verdict on the Viral One · 4 Videos (long-forms) · 5 Single playlist: Meatball vs Animals · 6 Single playlist: Viewer Case Friday.

### 2h. Watermark, end screens, cards
- **Watermark** (Studio → Customization → Branding → Video watermark → Upload `episodes/branding/avatar.png` → Display time: **Entire video**).
  It shows on long-forms (not Shorts) as a subscribe button on hover.
- **End screen on every long-form** (Studio → Content → the video → Editor → End screen → Add element): Video "Best for viewer"
  + Playlist "Meatball Investigates: Cases" + Subscribe, over the last 20 s (our outros tease the next case there).
- **One card per long-form** (Editor → Cards → Playlist → Cases) at the mid-video "hit like" beat.

## 3. Thumbnail Test & Compare (YouTube Studio, desktop)
Studio → Content → the video → Details → Thumbnail → **Test & compare** → upload 2-3 → Done. Run it until YouTube
picks a winner by watch-time share. Only test long-forms that are getting impressions. In order:

| Long-form | Goes live | Upload these files |
|---|---|---|
| Conspiracy Theories That Turned Out To Be TRUE | when queued (lever 1) | `episodes/longform-turned-out-true/thumb.jpg` (spy cat, "IT WAS REAL") · `thumb_b.jpg` (Northwoods memo, "CIA FILES") · `thumb_c.jpg` (MKUltra file, "PROVEN") |
| Zombie Animals Are Real (And One Might Be Inside You) | Sat 10/31 14:00 | `episodes/explains-03/thumb.jpg` · `thumb_b.jpg` · `thumb_c.jpg` |
| The Most Dangerous Animal in the World Isn't What You Think | Tue 11/3 14:00 | `episodes/explains-02/thumb.jpg` · `thumb_b.jpg` · `thumb_c.jpg` |
| Weird Animal Facts You Didn't Know (3 Are Fake…) | today 14:00 | `episodes/myths-05/thumb.jpg` · `thumb_b.jpg` · `thumb_v2.jpg` |

## 4. What was set up today
- data/related-video-map.csv (80 Shorts), episodes/branding/ (banner, avatar, trailer, the build script), 3 thumbnails for
  the case long-form (missing until now), research/51-search-slate.md + 2 retention-passing scripts, research/51-community-posts.md,
  research/51-tiktok-playbook.md, E-promote in data/experiments.csv, 3 collab drafts in Gmail, OPERATIONS "Growth levers", TOWN duties.

## 5. Weird-news fast lane (same-day "Meatball Investigates" Short)
**Why.** Strange-discovery and declassified-file news gets a search spike within hours, and the first explainer Shorts take
most of it. Our case shape (scene-first open, verdict stamp, sources) already fits news. "Nobody gives a verdict" is
as true for news as for viral claims (research/50).
- **Sources, checked at the 12:19 marketing desk (and 08:13 when there's time):** Smithsonian Magazine "Smart News",
  Live Science, Science/Nature news, EurekAlert! (embargo lifts), NASA and NOAA newsrooms, the National Archives (NARA) and
  CIA FOIA Reading Room "recently released", the FBI Vault "new", Atlas Obscura, the British Museum and other museum press
  pages. vidIQ `trending_videos` / `keyword_research mode=rising` for "mystery", "declassified", "discovered" when credits allow (5 each).
- **What qualifies:** strange discoveries (archaeology, odd fossils, deep-sea finds), newly declassified documents,
  odd science results ("scientists finally explain…"), and animal oddities. It must be *weird*, have a clear question,
  and allow a verdict (PROVEN / BUSTED / UNSOLVED / "TOO EARLY").
- **Turnaround target: source story → posted Short in ≤ 8 hours**, same day:
  intel flags it (≤ 30 min) → factdesk confirms with **2 independent reputable sources** (≤ 30 min) → showrunner writes an
  18-24 s v2 case script `scripts/news-NN.json` from the verdict-01 template (≤ 45 min) → studio renders and QAs the 2 fps
  sheet (≤ 2 h) → postmaster adds it as an **extra** post (YouTube 18:00 or the next free slot; TikTok 21:00). It never
  moves a queued post.
- **Safety rules (on top of the red list):** no deaths or tragedies from the last 12 months; no living private people; no
  medical or health claims; preliminary studies are stamped **TOO EARLY** and say "one study" out loud; never use news
  photos (copyright). Only PD/CC0/CC BY (NASA, NOAA, NARA, museum open access, Commons) or a host shot over the case board.
  Never show another creator's clip. The source names go on screen and in the description. If a fact changes after
  posting, pin a correction comment within 24 h (drafted by the host, approved by Nolan).
- **Packaging:** title = what people will search ("Scientists Found a ___ Under ___. Is It Real?"), with no "BREAKING" or fake
  urgency. Case number: the next daily CASE #, plus a small "NEW" tag in the headline only on day 1.
- **Score:** 48 h views vs the case median, and search as a traffic source. 2 news Shorts in a week ≥ 1.5x median keeps
  the lane; 3 under half the median kills it (OPERATIONS "Kill" rule).

## 6. Collab and shout-out targets (vidIQ similar_channels + channel_search, 10/26; latest titles via yt-dlp)
| # | Channel | Subs | Why it fits | First move |
|---|---|---|---|---|
| 1 | **Dumb History** (@dumbhistoryus) | 46.6K | sarcastic bizarre history; "111 Bizarre Coincidences From History That Actually Happened" | **Gmail draft 1** (case swap) |
| 2 | **PastLens** (UCwQOmeUdtNnH7F4CWXosqKw) | 15.9K, +17.8% subs/30d | "Mysteries From History We Didn't Realize Actually Had An Answer", "The vanishings that nobody has ever been able to explain": our thesis | **Gmail draft 2** (verdict collab) |
| 3 | **Origins Beyond** (UCklYqgIuMeQcfMFxDWcE5SA) | 4.3K, +30.3% | "U.S. Weapons in Orbit: What's Confirmed, What Isn't"; peer size, so the most likely yes | **Gmail draft 3** (peer swap) |
| 4 | Island_Survival / ONAH (@island_survival_0) | 41.4K | animated strange history, ghost ships, unsolved mysteries | next round |
| 5 | Circle Toon History (@circletoonhistory) | 156K, +13% | animated war oddities: our Bat Bombs and Habakkuk cases are its genre | stretch; after a first collab exists |
| 6 | ryranks (UCGGphAC6j4siUelxFzdIJxw) | 89.9K | strange facts + unusual animals + urban legends: bridges both our pillars | next round |
| 7 | Mysteries Unfolded (UCweZLvyUCi7NvhpWnwV03AA) | 7.0K | mysteries and internet mysteries | next round |
| 8 | Strange As It Seems (UCHcUOJoWvbYdtDlcVP1gkIQ) | 3.8K, +6% | historical mysteries; peer size | next round |
| 9 | Vibtastic (@vibtastic) | 3.3K | 3D-animated history and mysteries; peer size | next round |
| 10 | Cryptic Croaks (UCfCJPMWSoKDH8zoehGFpxgA) | 6.2K, +20% | mysteries and UFOs; check its honesty first (we never endorse "proof") | only after a content check |

Excluded: Archaix, Nullvein and The Theory Room (alternative history presented as fact: a collab would put our
verdict brand next to unverified claims); Story Crashers and GravityLore (vidIQ files them as animated history, but their
current uploads are axolotl stories and celebrity human-interest clips).

**Collab mechanics (research/36):** each side makes its own original video. Never re-upload the other's footage. Use YouTube
Collaborations (Studio → the video → Details → Show more → Collaboration) when both agree. A Community-post shout-out is the
zero-effort swap. TikTok duets and stitches of a partner earn $0 Creator Rewards, so on TikTok it's tag-in-caption only.

**Gmail drafts (in the connected Gmail account, no recipient set: Nolan adds each channel's business email from its
About page → "View email address", reads it, and sends himself):**
1. `Case swap? Dumb History x Meatball Investigates`
2. `Your "mysteries that had an answer" video, and a verdict collab idea`
3. `Collab idea: Origins Beyond x Meatball Investigates ("what's confirmed, what isn't")`

## 7. YouTube paid options (Nolan decides; we buy nothing)
- **What it is.** YouTube **Promote** (Studio app → Content → a video's ⋯ → Promote) runs a Google Ads campaign on one video.
  Goals: **Audience growth** (subscribers), **Video views**, or **Website visits**. A Google Ads account is created on the first campaign. Ads
  are reviewed for 1-2 days. The minimum is as low as $5, but Google "generally recommend[s] at least $100" because performance improves over
  time ([YouTube Promote Creator Playbook, Google](https://services.google.com/fh/files/misc/youtube_promote_creator_playbook_us.pdf)).
- **Does it count toward YPP? No.** The playbook says: *"Any subscribers and watch time gained from Promote spending will not
  count towards YouTube Partner Program (YPP) eligibility."* The YPP help page also excludes **"Ad campaigns"** from both qualified
  watch hours and qualified Shorts views ([YouTube Help 72851](https://support.google.com/youtube/answer/72851)). Organic views a
  promoted video earns *after* the campaign do count.
- **Recommendation: don't spend on YouTube Promote before YPP.** Our gate is watch hours and Shorts views, and paid ones don't
  count. Even the 44 subscribers we still need would not count if they came from Promote. The free levers above attack the
  same gap.
- **If Nolan wants a test anyway (reach for its own sake):** promote **the long-form**, not a Short: `Conspiracy Theories That
  Turned Out To Be TRUE` once it's public. A long-form viewer is worth watch time later, and its end screen and playlist can
  keep them. Goal: **Video views**, US + UK + CA + AU, **$5/day for 5 days = $25**. **Success metrics:** cost per view under
  $0.05; the video's **organic** (non-ad) views in the 7 days *after* the campaign ≥ 2x the 7 days before; subscribers gained from
  the video, organic only. If organic views don't move, the spend bought nothing that compounds. Stop.

## 8. Nolan's 15-minute checklist (only what needs you, in order)
**YouTube Studio (desktop: studio.youtube.com), ~10 min**
1. **Name** (1 min): Customization → Basic info → Name → `Meatball Investigates` → Publish. Leave the Handle as is.
2. **Description + keywords** (1 min): same page → Description → paste §2d → Publish. Then Settings → Channel → Basic info → Keywords → paste §2e → Save.
3. **Banner + picture + watermark** (1 min): Customization → Branding → Picture: Change → `episodes/branding/avatar.png` → Banner image: Change → `episodes/branding/banner.jpg` (accept the default crop) → Video watermark: Change → `avatar.png`, **Entire video** → Publish.
4. **Trailer** (2 min): Create → Upload videos → `episodes/branding/trailer.mp4`, title `Meatball Investigates: what this channel is`, Not made for kids, **Altered or synthetic content: No** (stylized animation), Visibility **Unlisted** → Save. Then Customization → Layout → Channel trailer for people who haven't subscribed → Add → pick it → Publish.
5. **Playlists** (3 min): Content → Playlists → New playlist, four times, in the order of §2f (copy each title and description; Public). Add the live videos listed there (in the playlist: ⋯ → Add videos → Your YouTube videos).
6. **Home sections** (1 min): Customization → Layout → Featured sections → Add section → the order in §2g → Publish.
7. **Related video on the live Shorts** (2 min, then 1 tap per new Short): Content → Shorts → a Short → Details → **Related video** → pick the long-form in its `best_longform` row of data/related-video-map.csv (open it in GitHub; filter by `short_video_id`). Today: the 9 Shorts with a `short_video_id`. From 10/26 14:00 most animal ones can use "Weird Animal Facts You Didn't Know".
8. **Test & Compare** (1 min per video, as each goes live): Content → the video → Thumbnail → Test & compare → upload the 3 files in §3.
9. **Community** (from Tue): YouTube app → Create (+) → Post → paste research/51-community-posts.md #1 (and the others on their days).

**TikTok app, ~4 min**
10. **Account type** (30 s): Profile → ☰ → Settings and privacy → Account → look for "Switch to Personal account". If that option shows, we're a **Business** account: Creator Rewards excludes Business accounts. Tell the Mayor which it is before switching anything (it changes Metricool and the music library).
11. **Profile** (1 min): Profile → Edit profile → Name `Meatball Investigates` → Bio: paste playbook §1 → Photo: `avatar.png` → Website: the YouTube channel URL.
12. **Pins** (1 min): open A119 (Nuke the Moon), Roswell and Northwoods → ⋯ → **Pin**. Swap them Thursday for the 3 case posts with the best full-watch rate (the Intel desk posts which).
13. **Playlists** (1 min): Profile → the videos tab → Create playlist → the 4 names in playlist §2 → add the case posts.
14. **Promote, next time:** don't re-promote the beetle. Promote **the case deep cut the Intel desk names on Monday** (highest full-watch rate, 48 h+ old, 300+ views). The default until then is **Case #8 "The CIA Stole a Soviet Submarine" (tt-glomar, posts Wed 10/28 20:00)**. Set a cost-per-follower cap (we suggest $0.10) and pause above it.

**Gmail (when you have 5 min):** open the 3 drafts in §6, add each channel's email from its YouTube About page, read, send if you're happy.
