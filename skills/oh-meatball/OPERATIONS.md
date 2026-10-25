# Meatball Myths: operating system

Claude runs the channel; Nolan owns the accounts, gives direction, and does the few Studio-only
taps. This file is the team, the daily routine, the numbers we steer by, and the rules for change.

## Goal ladder (money)
| Stage | Target | Unlocks |
|---|---|---|
| 1 Seed | 1 episode > 1k views; 30 s retention > 70% | proof the format holds strangers |
| 2 Traction | YouTube 1,000 subs; TikTok follower growth | YPP eligibility path |
| 3 Monetize | YouTube Partner Program: 1,000 subs + 4,000 long-form watch hours / 12 months (~1,300 episode views/week at 3.5 min AVD) | ad revenue |
| 4 Scale | Part 2s of every winner, 30-50 myth compilations, second series | more revenue lines |

## Team (Claude spawns these as agents; one writer per file)
| Role | Owns | When |
|---|---|---|
| Showrunner (Claude) | priorities, final QA of scripts/frames/thumbs, posting, Nolan updates | every run |
| Analyst | tools/stats.py, Metricool + vidIQ analytics, HQ "Daily report", experiment scoring | evening run |
| Scout | tools/rivals.py, competitor outliers, research/19-topic-backlog.md | evening run |
| Writer | next episode script (cold open, 12 myths, jokes, ~1,600-1,700 words) | morning run, 2 days ahead |
| Photo editor | iNaturalist candidate sheets, live/unharmed/right-species picks | morning run |
| Producer | episode.py (long + Shorts), tiktok.py, thumb3 + thumb2 | morning run |
| Scheduler | Metricool queue: 1 episode, 3 Shorts, 4 TikToks a day, first comments; re-check best times weekly | morning run |
| Inbox | Nolan's chat messages + comments on the HQ page; acts on them first | every run |

## Daily routine (scheduled tasks fire into this session; all ET)
| When | Run | Output |
|---|---|---|
| 08:13 | Production: inbox, build the episode for 2 days out, fill the queue | episode + 3 Shorts + 4 TikToks queued 2 days ahead |
| 18:41 | Review: stats, analytics, rivals, HQ report, next topics | HQ Daily report + rivals, backlog updated |

Cadence: one long-form a day at 2 PM (Saturdays: the "Meatball Explains" history episode instead of a myth episode, never both); YouTube Shorts 9:30 AM, 1 PM and 4 PM (from the newest episode that is
already live, so Related video can point at it); TikToks 4 a day from 10/25: 9:30 AM, 12 PM, 6 PM, 8 PM, all over 60 s and freshly rendered (Creator Rewards pays only 60 s+; research/32). The 11/1 summit moves it to 5 if qualified views per post hold, or back to 3 if they fall 25%+; TikTok is the lab and YouTube the showroom (research/33). Times follow Metricool best-time data
(checked 2026-10-24): YouTube peaks 3-5 PM (4 PM top) with a second peak at 10 AM, so the episode goes live at 2 PM, ahead of the
big wave; TikTok peaks 10 AM, 12 PM and 6 PM every day.
**First slot is 9:30 AM ET (Nolan, 10/25).** vidIQ subscriber activity runs about even at 9 and 10 AM; Metricool favors 10. Nolan chose 9:30. Put the week's strongest Short at Thursday 4 PM: vidIQ's busiest subscriber window is Thursday 3-6 PM.

## Numbers we steer by
Episodes: impressions CTR, 30 s retention, average view duration, views in 48 h.
Shorts: engaged views / views, average view %, subs gained. TikTok: views, average watch time,
qualified views. Channel: subs, weekly long-form watch hours vs the 4,000 h pace.
- Double down: any video at 3x our median in 48 h gets a Part 2 within a week.
- Kill: a topic or title style whose 3 videos all land under half our median.

## How we change things (no guessing)
1. Every change is an experiment row in data/experiments.csv: hypothesis, change, metric, start date.
2. Change one variable at a time (hook, title pattern, thumbnail style, voice pace, length).
3. Score after 3 videos or 7 days against the median of the 3 before: keep, kill, or extend.

## What needs Nolan
- Studio-only: Related video on each Short, end screens, Test & Compare thumbnails, hiding likes,
  the Episode 1 title/thumbnail (vidIQ edits need YouTube MFA).
- Anything that spends real money or deletes videos.

## Standing orders from Nolan
- **Platforms (Nolan, 10/24): YouTube and TikTok only.** Don't connect or ask about Instagram, Facebook, Pinterest or Threads again. Their crossposting steps are retired.
- Full authority (Nolan, 10/24): the Mayor decides and acts on anything that helps the channel, without asking.
  Nolan's own actions are the exception: logins, connecting accounts, and payments, which stay zero beyond what's already paid.
- Only Meatball stick-figure info/quiz videos (long-form and Shorts). No door-cam, trail-cam or other
  fake camera clips, ever; the old ones stay as drafts in Metricool.
- Long-form explainers run ~10 minutes (12 myths, or a history story with 3-4 checkpoints), never 2-3 minute pilots.
  Each episode is cut into one vertical Short per myth (`explainer.py --vertical`).
- Like counts hidden on every video. The YouTube API and Metricool can't set this, so it lives in
  YouTube Studio: Settings > Upload defaults > Advanced settings > untick "Show how many viewers
  like this video" (new uploads), and Content > select all > Edit (existing ones).

## Shorts v4 is the format (Nolan approved 10/25: "Wayyy better in the new ones do that")
- Every new Short and TikTok uses `"style": "v4"`: all of v3 below, plus moving animal cut-outs (research/45).
  - Give each acting beat an `"animal": "<move>@<word>"` (lunge, kick, charge, strike, sting, shake, turn, drift).
  - Set `"contact": true` only when Meatball should touch the animal.
- **Whole animal or nothing (Nolan: outlines, "some of the animal is missing"):**
  - Photos must show the WHOLE animal, uncropped (CC0/CC BY).
  - A failed cut-out falls back to the v3 still; the render fails if a cut-out breaks the rules.
  - The factdesk eyeballs every new cut-out: the automatic check can't catch a matte that stops short.
- **Bigger animals (Nolan approved 10/25, "Better"):** tools-v4-bigger.diff is merged. Animals are fitted by their real outline, Meatball tucks left at size 760 (down to 547 when it lets the animal grow 8%+), and the opening shot is animal-only until Meatball peeks in.
- Already-scheduled v3 posts stay up. Don't re-render them.

## Weird pivot: "Meatball investigates the weird" (Nolan 10/25; Sunday Summit decisions)
Nolan turned the channel toward conspiracy theories (debunked or proven), strange history, strange facts and myths, with animals as one pillar, and mysterious music. Pilot: research/48 and episodes/weird-pilot/ (6 Shorts + 1 long-form). Character layer: research/39 "Weird pivot" (scared investigator, "Opening the file.", verdict stamp, case-file structure).
- **Rollout is an experiment, not a switch (E19).** From the first pilot post (target 10/27): the 9:30 AM YouTube Short and its TikTok 2 h later are a numbered "Case of the Day". The 1 PM and 4 PM Shorts stay v4 animal jeopardy. Widen to 2 slots only if 6 cases land at or above the v4 animal median on 48 h views; kill if all 6 land under half of it. Long-form: one weird case (proven-true Cold War secret first; research/27 §7) in a Tue/Sat slot once it passes tools/retention.py.
- **Every case ends on a verdict stamp:** PROVEN, DEBUNKED or UNSOLVED, shown on screen, with the primary source named on screen. The verdict is spoken over a moving picture, never a bare card.
- **Red list (factdesk owns it; research/38 summit problem 3):** no vaccines or medical cures, elections, recent tragedies, living private people, or secret-society theories that target a group. Fabricated "proof" (time travelers, AI fakes) is never shown as real. When in doubt, pick the declassified-document case.
- **Topic test (research/38 summit problem 2):** lead with the case most viewers haven't heard of. A famous debunk everyone knows (moon landing, flat Earth) is our "camel" (227 views vs 1,800 for the same template on a surprising topic).
- **Music:** one mysterious bed (low synth or pizzicato), vidIQ-generated or our own, ducked under the voice; one sting for the file opening and one for the stamp.
- Everything else holds: v4 style, bigger animals, the early ask kit ("Real or fake?" guess card), 20-25 s YouTube / 61-75 s open-loop TikTok, AI label on, YouTube and TikTok only.

## Shorts endings (Sunday Summit 10/25, research/38 problem 1)
The goldfish curve loses half its remaining viewers between 47% and 75% of the video, where we park a text-only punchline card and an ask. From 10/26 renders:
- The punchline is spoken over a moving cut-out or a new picture, never a bare text card.
- Any CTA ("Part 2 tomorrow", "follow") overlays picture; it never gets its own seconds after the punchline.
- The Short ends no more than 1.5 s after the punchline, then the loop line.
- 60 s+ deep dives are saved as `tt-*.mp4`, never `short-*.mp4` (two 65-67 s renders reached 11/10 YouTube Shorts slots; scan.py check 7 now covers the whole ledger).

## TikTok deep dives: open loop (night shift proposal 10/25, research/40; Mayor to adopt or reject)
- A 61-75 s deep dive promises one withheld answer in lines 1-3 ("...but it has exactly one weakness"), walks through 2+
  wrong guesses (`"decoy": true`), and pays off (`"payoff": true`) at 50-80% of the words. Shorts keep claim-first.
- `python3 tools/openloop.py SCRIPT.json` checks it; `research/40-openloop-gate.diff` makes episode.py enforce it.
- Template: `scripts/v4-one-weakness-pangolin.json`. Rival evidence: 62 s T. rex cartoon explainer, 1.6M (10.3x), answer at 69%.

## Shorts v3 (the base v4 builds on; approved 10/24)
- `"style": "v3"` (tools/v3.py, research/44).
- **Meatball in jeopardy:** something happens to him, he doesn't narrate it.
- **Pacing:**
  - action moves on every line
  - a punch-in zoom on key words
  - a whip pan or new picture every 2.5 s or less
  - SFX under the voice
  - a joke or escalation every 4-6 s
- **Length:** 20-25 s on YouTube. TikTok deep dives run 61-75 s.
- **Voice (Nolan, 10/24):** v3 Shorts and TikToks use the prototype voice, edge-tts en-US-AndrewMultilingualNeural at +10%. Nolan preferred it to Bill on v3, and it's free. Bill is retired from v3.
- **ONLY v3 Shorts and TikToks get posted (Nolan, 10/24).**
  - Every queued non-v3 Short or TikTok is set to draft (held, never published) and replaced by v3 nearest-first.
  - An empty slot is better than an old-style post.
  - Long-form keeps the story format.
- **Every v3 Short posts twice:** to YouTube, then to TikTok 1-2 h later. TikTok-only deep dives (61-75 s, Kokoro voice) fill the 60 s+ Creator Rewards slots.

## Meatball is the star (Nolan, 10/24)
- Meatball is the biggest thing on screen in every shot that isn't a full-bleed animal photo.
  - **Long-form:** about 85% of the frame height, head high, beside a narrower photo panel.
  - **Shorts:** about half the frame on text cards; on photo shots he stands in the scene, cut at the waist.
- He drives every video:
  - every line is his voice and his opinion (first person, research/39 persona)
  - he reacts to every reveal
  - he points at the animal
  - he gets the last word before the loop
- No shot leaves him in a corner. The animal photo is his co-star and never replaces him for more than one cut.
- Thumbnails always show his face reacting.
- The Red Team rejects any render or thumbnail that breaks these rules.

## Long-form rules (learned 2026-10-23)
- Cold open every episode: the first line is the hook for a stranger (the myths, the twist, the
  stakes), then straight into myth 1. Never open with "Last time..." since nearly every viewer is new.
- Post the episode first, then its Shorts, so every Short can carry a Related video link to it
  (Studio only, no API). A Short that goes out before its episode sends its viewers nowhere.
- Check Metricool and stats.py before queueing a Short so the same Short never posts twice.
- Retention rules (research/20-retention-and-swipe.md, 2026-10-23): every script sets "style": "classic" (Nolan, 10/23).
  Shorts are one myth, about 20-25 s: animal photo + claim at frame 0, 1.5 s countdown, reveal, the "why" beat, punchline card,
  then a rotating loop line that runs into the opening (research/23, research/30). Long-form: strongest
  myth teased in the cold open, myth #1 by ~15 s, re-hooks near 1, 3 and 6 minutes ("the last one fooled
  scientists"), MYTH n/12 badge, best myth saved for last.
- Narration: en-US-AndrewMultilingualNeural at +15% everywhere (Nolan picked it 2026-10-23) with the light music bed
  (`brand/music/quiz-bed.m4a`, original vidIQ track, ducked under the voice). Set per script:
  `"rate"`, `"short_rate"`, `"music"`.
- One long-form episode a day at 2 PM ET; 4 TikToks a day (9:30 AM, 12 PM, 6 PM, 8 PM), every one
  over 60 s (Creator Rewards floor) with the AI-content label on.

## Guardrails
- Original characters and stories only; label AI content where the platform asks.
- Keep >= 400 vidIQ credits in reserve. No paid tools without Nolan's yes.
- Never post the same video twice to one platform (check opusclip_list_scheduled_posts first).

## Opening rules (Contrarian review, research/38; Mayor 10/24)
- **Long-form:** every beat in the first 30 s shows an animal photo, and each animal appears as it is named. Text-only cards come no earlier than 15 s. Myth #1 starts by 25 s.
- **Shorts and TikToks (Shorts v2):**
  - Frame 0 is a full-screen, moving photo of the animal doing the thing the line describes.
  - The first line states the claim as a fact or a correction. No "TRUE OR FALSE?" card and no countdown.
  - The picture changes every 3 s or less, and every photo matches what is being said.
- **Captions:** unique per post and built from the searched question (tools/tiktok.py `title()`/`caption()`). Never use file-nickname hashtags.

## Niche, thumbnails, repeat audience (Nolan, 10/24; research/42)
- **Quiz format retired for new long-form.** Meatball explains weird true things.
- **Topic pillars:**
  - Animals (70% of videos)
  - Food (Meatball *is* food)
  - Weird history and the human body
- **New pillars:** one test (a long-form plus 3 Shorts) at a time. Keep it only if it performs as well as the animal average.
- **Thumbnails follow the Meatball system in research/42 §2:**
  - a huge reacting Meatball face
  - one subject
  - at most 3 words
  - brand colors
  - 3 variants, each scored with vidIQ
- **Repeat audience:**
  - fixed Tuesday/Saturday days
  - named series with their own playlists
  - running gags
  - read commenters' answers on screen
  - tease the next episode at the end
  - Community polls (drafted by the Host desk, posted by Nolan)

## Always ask: likes, comments, subscribes (Nolan, 10/24)
Never assume viewers will engage. Every video asks, in Meatball's voice and with a joke, never as a generic "smash that like button".

**Long-form: v3/v4 style + early asks (Nolan 10/25: "keep that up, and for long form also"; "more v3 in long form, too dry")**
- **Style:** story long-forms render with `"style": "v4", "aspect": "16:9"` (tools/v3.py `landscape()`, 1920x1080): Meatball in jeopardy (an action move at least once a minute, a gag or escalation every 15-20 s), punch-ins on key words, a whip or new picture every 3-4 s at most, SFX under the voice, moving cut-outs where the photo shows the whole animal (v3 stills otherwise). Text cards become `"label"`s over a blurred photo; `"aside"` footnotes still work. Still 6-8 min and one story; facts unchanged, jokes in the research/39 voice only. Samples: `scripts/explains-0{2,3}-*.json`.
- **0:00-~0:20 cold open: hook only, no ask.**
- **~0:20-0:35 guess-first comment card** (beat `ask` with `choices`): "Comment your guess before I tell you", 2-3 emoji choices tied to the episode's big question (zombies: "WHICH ONE COULD BE INSIDE YOU? 🐜 / 🐌 / 🐀"), held ~2 s. The episode must answer it.
- **~0:30-0:50 one subscribe pill** (beat `sub`): "Subscribe. A new Meatball story every Tuesday and Saturday." Meatball points, the SUBSCRIBE pill pops and is pressed. This is the ONLY subscribe ask: no second one later.
- **One like ask mid-video** (a spoken line + "HIT LIKE" label).
- **Ending:** "So, were you right? ... Tell me in the comments." (reminder card "WERE YOU RIGHT? 👇"), then the tease for the next episode. No extra in-story comment asks.
- **First comment / pinned:** the same emoji guess question. The description's first question line matches it.
- The v3 gate warns (long-form): any ask before 15 s, a guess card outside 15-40 s, a pill outside 28-55 s or more than one pill, the reminder earlier than the last 90 s, a picture held over 3.5 s, nothing new for over 4 s.

**Shorts: the ask kit is standard on every new Short (Nolan 10/25: "do it in the beginning so people will actually be watching"; research/46)**
- **0-3 s: hook only.** Never an ask in the first 3 seconds.
- **~3-6 s: guess-first comment card** (beat `"ask": {"q", "choices", "at"}`): one short voiced line ("Guess before I tell you. Comment.") and 2-3 emoji choices on screen ("🦈 or 🐊", "👍 / 👎"). One word or one emoji to answer. The Short must answer it later, and the question must be true to the video: never a wrong fact to bait corrections.
- **~6-10 s: subscribe pill** (beat `"sub"`): one quick line with a concrete, true reason ("Subscribe. I face a new animal every day."). No "sub4sub", no "smash that button".
- **Before the loop: one-line reminder** ("Did you guess right? Comment.", card without choices). The loop still ends on frame 0.
- `tools/v3.py` gate warns when an ask lands before 3 s, the guess card after 7 s, or the pill outside 5.5-10.5 s. Sample: `episodes/ask-kit/`.
- **Series:** number them in the title ("Meatball vs Spiders #1 of 3"). "Follow for Part 2" only when Part 2 is already made or queued; "Part 2 at N comments" only if we will really make it.

**First comment (YouTube) and caption (TikTok):** lead with ONE binary or pick-one question with 2-3 emoji choices, tied to that video's animal and accurate to it ("Would you pick it up? 👍 yes / 👎 no / 💀 only with gloves"). On ask-kit Shorts use the same guess question as the card. YouTube first comment ends with "Follow Meatball for more 🍝"; TikTok caption = question first, then the fact and hashtags, then "Follow Meatball for more 🍝" (or the real "Follow for Part N").

**Description:** the first line is the same question when it fits. The subscribe line gives the concrete reason: "Subscribe: Meatball faces a new animal every day 🍝" (long-forms keep "new Meatball every Tuesday and Saturday").

**Comment replies (10/24):** vidIQ can now post replies as the channel. The tool requires Nolan to approve the exact text, so the Host drafts replies in Meatball's voice, sends them to Nolan, and posts them on his "post them". The first 4 went live 10/24.

**Host desk (evening):**
- reply to every comment as Meatball (drafts go to Nolan)
- heart the best comments
- collect the answers that get read out next episode

**Intel desk (weekly):** check subscribers per 1,000 views and comments per 1,000 views by video. Keep the asks that move the numbers; rewrite the rest.

- **Read-outs quote only real comments** (vidiq_video_comments). With no comments yet, use an ask, never invented answers or names.

## Long-form reset (Nolan + Mayor, 10/24 evening)
Data, last 30 days:
- Long-form got 5 views, averaging 28 seconds watched.
- Shorts got 6,002 views.
- The 10/23 long-form has 0 views; the wolves history episode has 8.
- Diagnosis: YouTube isn't showing our long-form to anyone. The few people who click leave within half a minute, because the 12-card quiz with countdowns repeats the same pattern. Shorts carry discovery; long-form carries watch hours and RPM. Both need to work.

Rules from 10/30:
- **Cadence (Nolan, 10/24):** start at TWO story long-forms a week, Tuesday and Saturday at 2 PM. Episodes already queued through 10/29 stay.
  - Go to THREE (adding Thursday) as soon as one episode clears the retention gate below.
  - Long-form pays a much higher RPM than Shorts, and the 3,000/4,000 watch-hour path needs it.
- **Format: one story, not 12 cards.**
  - 6-8 minutes about one searched question, e.g. "Which spider bite can actually kill you?", "How did wolves become dogs?", "Animals scientists thought were extinct".
  - Meatball is the host and the story's guide.
  - At most 3 quiz checkpoints, and no countdown cards.
  - Something new (a reveal, a photo, a joke) at least every 20 seconds.
  - Payoffs are promised in the first 15 seconds and delivered at the end.
- **Title equals the search phrase:** the title must match a keyword vidIQ shows with search volume. No "12 Myths" listicle titles.
- **Thumbnail:** one animal, Meatball's face, and at most 3 words. Test two in Studio "Test & Compare" (Nolan).
- **Bridge from Shorts:**
  - Each long-form is cut into 6-12 Shorts.
  - Every one of those Shorts gets the long-form as its YouTube "Related video" (Nolan, in Studio; the API can't set it).
  - Pinned comment: "Full story: <title>".
- **Freed render time goes to Shorts:** 3 YouTube Shorts a day; 4 TikToks a day; a "Would Meatball Survive?" series in the 1 PM slot.
- **Judge by retention:** keep a format only if average view duration is above 2:00 and retention at 30 seconds is above 60%. Check after each episode with vidIQ audience_retention.

## Narrator voice (Nolan, 10/24): Bill
- **Shorts:** every new Short uses `"voice": "vidiq:pqHfZKP75CvOlQylNhV4"` (vidIQ premium voice "Bill - Wise, Mature, Balanced").
- **Generating Bill's audio:**
  1. Run `tools/premium_voice.py prep SCRIPT OUTDIR`.
  2. Send each chunk to `vidiq_voiceover_generate` and save the MP3 as `chunk-NN.mp3`.
  3. Run `premium_voice.py split SCRIPT OUTDIR`, then render.
  4. If a render stops on missing lines (hooks and loop lines built at render time), run `prep-missing VOICE OUTDIR`, voice them, split, and render again.
- **Cost:** about 14 vidIQ credits per Short.
- **Free voice (Nolan, 10/24): Kokoro blend C, `"voice": "kokoro:eric-michael"`.**
  - Used for long-forms and TikTok-only videos.
  - Runs locally at no cost, through `tools/free_voice.py`: lines are generated on demand, studio-processed (EQ, compression, loudness) and aligned with whisper.
  - The model files live in ~/.cache/kokoro.
- **Bill is not used on v3 Shorts** (Nolan preferred the prototype voice). vidIQ credits now go to research and packaging.
- **No paid voices beyond the vidIQ credits we already have (Nolan, 10/24).** Bill runs until those credits are gone; no extra credits and no ElevenLabs. The free replacement is being tested: Chatterbox (open source, runs locally) with our own Meatball voice made from a Kokoro blend. Samples are in `research/39-voice-tests/`. One character, one voice is still the goal.

## Long-form retention (Retention desk, 10/25; research/47)
Autopsy: our one long-form with a curve (gFhrONKK0rI, 2:15 quiz pilot, 11 viewers, 53 s AVD) lost people at 0:02 (the opening question card), 0:04 (it answered its own question), 0:14 (agenda line "Today we're fixing..."), 0:18 (re-stated answer), and wherever one item ran 25-45 s with no tease (0:28, 0:46, 1:12). Small-channel breakouts open on the animal, never introduce themselves, and change animal every 75-100 s under a countable structure.

**`tools/retention.py` gates every 16:9 story long-form; episode.py refuses to build one that fails** (`--no-retention` only for old episodes). It estimates times from words (3.35 words/s, Kokoro +0%) or reads a render's timeline.json (`--timeline`).
- **R1 Cold open (first 30 s):** promise the payoff ("...and the last one might be you", "I'll show you the winner at the end"). Frame 0 is the best animal photo, unblurred, no text card. No intro, welcome or agenda line ("I'm Meatball", "Today:", "welcome") before 0:30; Meatball says his name in the subscribe line.
- **R2 Loops:** a tease of what's next ("Number two walks its victim on a leash"), a cliffhanger, a countdown step or a twist at least every 75 s up to the payoff (aim 45-60 s).
- **R3 Visible structure:** each story chapter's first beat has `"counter": {"n": 2, "of": 5}` (optional `"text": "#4"`); the spec has `"progress": true`. tools/v3.py draws the "2 OF 5" badge with dots top right and a progress bar with chapter ticks along the top (16:9 only, never shakes). `"counter": false` or an outro chapter hides it.
- **R4 Segments:** never more than 75 s without a new animal, a twist (`"twist": true`) or Meatball jeopardy (`"jeopardy": true`).
- **R5 Best story last:** one `"payoff": true` chapter, the last counted one, starting in the back 35%, teased in the cold open and again mid-video (`"tease": true`). The outro after it runs 60 s at most.
- **R6 Expectation match:** at least half the title/thumbnail words (`"thumb_text"`) are said or shown in the first 60 s, and chapter 1 starts by 0:60.
- **R7 Length 5:00-7:00** (supersedes the ~10 min and 6-8 min lengths above) until long-form AVD clears 2:00. We give up mid-rolls (8:00+) on purpose: we aren't monetized, and watch hours grow faster from a held 6 min than from an abandoned 10. Test one 8:30 with a chapter-break mid-roll after 3 straight episodes over 2:00 AVD and 50% at 0:30.
- **Every evening (Intel):** pull audience_retention for each long-form older than 48 h, log the drops in data/retention.csv, and send the top drop cause to the Showrunner.
