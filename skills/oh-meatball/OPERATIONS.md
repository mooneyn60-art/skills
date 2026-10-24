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

Cadence: one long-form a day at 2 PM (Saturdays: the "Meatball Explains" history episode instead of a myth episode, never both); YouTube Shorts 10 AM, 1 PM and 4 PM (from the newest episode that is
already live, so Related video can point at it); TikToks 4 a day from 10/25: 10 AM, 12 PM, 6 PM, 8 PM, all over 60 s and freshly rendered (Creator Rewards pays only 60 s+; research/32). The 11/1 summit moves it to 5 if qualified views per post hold, or back to 3 if they fall 25%+; TikTok is the lab and YouTube the showroom (research/33). Times follow Metricool best-time data
(checked 2026-10-24): YouTube peaks 3-5 PM (4 PM top) with a second peak at 10 AM, so the episode goes live at 2 PM, ahead of the
big wave; TikTok peaks 10 AM, 12 PM and 6 PM every day.

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
- Full authority (Nolan, 10/24): the Mayor decides and acts on anything that helps the channel, without asking.
  Nolan's own actions are the exception: logins, connecting accounts, and payments, which stay zero beyond what's already paid.
- Only Meatball stick-figure info/quiz videos (long-form and Shorts). No door-cam, trail-cam or other
  fake camera clips, ever; the old ones stay as drafts in Metricool.
- Long-form explainers run ~10 minutes (12 myths, or a history story with 3-4 checkpoints), never 2-3 minute pilots.
  Each episode is cut into one vertical Short per myth (`explainer.py --vertical`).
- Like counts hidden on every video. The YouTube API and Metricool can't set this, so it lives in
  YouTube Studio: Settings > Upload defaults > Advanced settings > untick "Show how many viewers
  like this video" (new uploads), and Content > select all > Edit (existing ones).

## Shorts v3 is the format (Nolan approved 10/24)
- Every new Short uses `"style": "v3"` (tools/v3.py, research/44).
- **Meatball in jeopardy:** something happens to him, he doesn't narrate it.
- **Pacing:**
  - action moves on every line
  - a punch-in zoom on key words
  - a whip pan or new picture every 2.5 s or less
  - SFX under the voice
  - a joke or escalation every 4-6 s
- **Length:** 20-25 s on YouTube. TikTok deep dives run 61-75 s.
- **Voice:** Bill on YouTube Shorts; Kokoro C on TikTok-only videos.
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
- One long-form episode a day at 2 PM ET; 4 TikToks a day (10 AM, 12 PM, 6 PM, 8 PM), every one
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

**Long-form**
- **Subscribe ask 1:** a spoken line right after the first payoff (about 0:45-1:30), e.g. "If watching a meatball panic is your thing, subscribing genuinely keeps me off the menu."
- **Like ask:** a spoken line at the midpoint, tied to the story, e.g. "If that one got you, hit like so I know to find more."
- **Comment ask:** a specific question with an easy answer, e.g. "Which one would you eat first? Wrong answers only." Say the best answer gets read out next episode.
- **End:** subscribe ask 2, plus "New Meatball every Tuesday and Saturday", plus the tease for the next episode.

**Shorts**
- Never put an ask in the first 3 seconds; the hook comes first.
- **Comment question:** the last spoken line before the loop is a short question (e.g. "Would you survive this? Comment.") on about 1 in 2 Shorts.
- **Follow line:** "Follow for part 2" on Shorts that are part of a series.
- **Captions and pinned comment:** every caption ends with a question, and every pinned first comment ends with "Follow Meatball for more 🍝".

**TikTok:** the caption ends with a question and "Follow for Part N+1".

**Description:** the first line asks a question. The last line is "Subscribe: new Meatball every Tuesday and Saturday".

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
- **Bill (vidIQ credits) is for YouTube Shorts only**, while the credits we already have last.
- **No paid voices beyond the vidIQ credits we already have (Nolan, 10/24).** Bill runs until those credits are gone; no extra credits and no ElevenLabs. The free replacement is being tested: Chatterbox (open source, runs locally) with our own Meatball voice made from a Kokoro blend. Samples are in `research/39-voice-tests/`. One character, one voice is still the goal.
