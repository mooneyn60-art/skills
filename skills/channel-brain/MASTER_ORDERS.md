# Master orders: Meatball Myths

The whole operating plan for the channel agent in one page. From here on, the job is: make, check, post, measure.

Last Updated: 2026-11-12
Status: ACTIVE; replaces every older plan where they disagree (Nolan's words win over this page)
Audience: Meatball Town (all desks), Nolan

## How to use this page
- One Read covers the whole page. Keep it under 50,000 bytes (`wc -c` after every edit; a Read stops at about 64,000). If a Read says it was cut off, read the rest before acting.
- Every rule in force is here. `MASTER_ORDERS_LOG.md` (same folder) holds the history under the same headings: research findings, what was done when, old plans, retired sections. Read it when a rule's reason matters. If the two disagree, this page wins.
- Nolan (10/29): "set the channel up to the point all he has to do is make and post." This page is that setup.
- A new order from Nolan goes in the same day: his words, my reading, the rule. When its work is done, the story moves to the log and the rule stays here.
- Commands and the order of work: `.claude/skills/` (`make-short`, `post-metadata`, `scoreboard`). This page wins over them.

## Where we are (11/12)
- **YouTube:** 1,000 subscribers reached 11/11. Long-form: 683 views and 10.6 hours in 28 days, against 4,000 hours needed (Nolan's Studio paste, 11/11).
- **TikTok:** 9,323 followers (TikTok Studio, 28 days to 11/10). Median about 226 views a post (78 posts, 10/23-11/10, Metricool). Creator Rewards was restored 11/11 but cannot be joined yet: it needs 10,000 followers and 100,000 views in 30 days.
- **The two jobs:** get views unstuck on both platforms (Nolan 11/12) and earn the 4,000 long-form hours.
- The 10/28 numbers are in the log under "Overview".

## Open asks of Nolan (one at a time, in this order)
1. **Tap the Windsor TikTok link sent in chat 11/12 and approve.** The account stays Personal, never Business (TikTok says Business accounts are not eligible for Creator Rewards). The link is signed: never write it into this repo. **Do not ask for anything else until he has answered this.**

Then, only if still needed:

2. Yes or no on the word "sucks" in the house-cat long-form title (see "Watch hours").
3. On 11/23: Chrome open with the vidIQ extension signed in to the channel, for the 11/24 read.
4. The Studio screenshots (TikTok Account check, the termite Short's Reach tab, a retention screenshot of the cat Short, Creator Search Insights) are no longer asked for one by one. Take them if he offers.

## Read dates and live tests
Read each test on its date, not before.
- **Thu 11/12 21:25:** today's three Shorts against Wednesday's; the funnier dog TikTok's label and early views; then the 07:37 scoreboard.
- **Sat 11/14:** Windsor will have the engaged share for the 11/10-11/11 Shorts: under 0.39 means viewers swiped, 0.40 or more with tiny views means YouTube did not show them. Read the Fri 11/13 dog Short's public thumbnail (cover test, "Tags and everything").
- **Sat 11/14 to Sun 11/15:** Windsor youtube, one call per video with the filter [["video","eq",ID]], fields date, traffic_source, views, engaged_views, for the five 11/10-11/11 Shorts and the 11/12 cat and moose Shorts; compare with 11/07-11/09 (feed 4,338 / 3,650 / 3,536 views a day; search 161 / 150 / 132).
- **Sun 11/15:** the funnier seven's average % viewed and engaged share; decide whether the queued bug Shorts get the funnier pass ("Make them funnier").
- **Wed 11/18:** first read of the pet and survival Shorts ("Direction change").
- **Fri 11/20:** verdict on the TikTok search-led test ("Views are stuck on both platforms").
- **Tue 11/24:** vidIQ credits return ("Develop yourself"); the house-cat structure check ("Watch hours").
- **Every long-form at 72 hours:** the thresholds in "The YouTube play". Part 2 posted Wed 11/11 17:00; the spider posts Sat 11/14 08:00.
- **Live tests with no date above:** the TikTok 20:15 sweary cuts against the clean ones after a week; the YouTube joke test and hook test (new openings); the TikTok label of each new-direction cut an hour after it posts.

## Develop yourself (Nolan, 11/12 about 12:58 ET)
- **His words:** "And Delvin yourself and skills mcps or repositories you want to help us grow whatever you need".
- **What it means (my reading):** develop yourself. Build or connect whatever tools, skills, connectors and repositories the channel needs to grow, without asking first. The work gate still holds: each thing has to change a post in the next seven days or a scorecard number. Anything that needs his login or his approval is still his to do, and he gets asked for one thing at a time.
- **From 11/12:** the gate in "The production line" holds for every video; post bodies come from `postkit.py payload`, not from typing.
- **Built 11/12:** `oh-meatball/tools/postkit.py` (with `selftest`), `tools/setup_env.sh` and three skills in `.claude/skills/`; the rules stay on this page. Two rounds of review by other models; this page was split from its log the same day so one Read covers it. New daily files: `oh-meatball/data/tiktok-stats.csv` (`postkit.py ttpage --csv`) and `data/longform-hours.csv`.
- **The Windsor TikTok ask (open ask 1):** Its field list has per-video watch time, finish rate, the For You and search split, and retention by second; whether it accepts a personal account is untested, and the tap is the test.
- **On Tue 11/24 (vidIQ credits return; reminder set):** read "stayed to watch" and feed impressions for the last 50 Shorts and retention curves for about a dozen videos through vidIQ. It reads through Nolan's Chrome with the vidIQ extension signed in (open ask 3).
- **Decided against (reasons in the log):** a setup script on the cloud environment; the Google Cloud route to YouTube retention (only if the vidIQ read fails); Supermetrics for TikTok (only if Windsor refuses the personal account).
- What the audit found: `oh-meatball/research/94-capability-audit.md` and the log, same heading.

## Tags and everything, from every angle (Nolan, 11/12 about 12:25 ET)
- **His words:** "And make sure your tags and everything are also updated to be the best look at All angles".
- **What it means (my reading):** every piece of text around a video (title, description, tags, hashtags, TikTok caption, first comment, category, cover) is checked against evidence and set to the best version, starting with the funnier cuts that go out today, and it becomes the standard for every post after.
- **The standard for every new post from 11/12:**
  1. YouTube title: the searched words in the first 40 characters, the hedge kept, one specific odd fact, one emoji, the series tag last, 100 characters at most, statement form.
  2. YouTube description: the first sentence is the question people type (from the search suggestions), then the checked facts, then four hashtags (two for the topic, #meatballmyths, #shorts last), then Sources.
  3. YouTube tags: 8 to 12 phrases taken from the search suggestions, each 30 characters or fewer, each one answered by the video. No tag that promises advice the video does not give.
  4. TikTok caption: the search phrase that is on screen, the checked fact with its condition, the Meatball gag in the video's own words without the swearing, a question, five topic hashtags. No #fyp, no #learnontiktok, no brand tag. The TikTok "title" field can hold anything; nobody sees it.
  5. Unchanged on purpose: the category (no stated effect), the AI label (stays on), first comments (open questions).
  6. Any change of wording goes through the second-model check like a script.
- **Not changed:** the bug Shorts and the other TikToks in the queue. They get the standard when they are next touched.
- **One test:** the Fri 11/13 dog Short has a cover frame set (the card GUILTY LOOK / MAY NOT BE A CONFESSION at 1.9 s; Metricool key `videoCoverMilliseconds`). Read the public thumbnail on Sat 11/14: if it shows that frame, set a card frame as the cover on every Short.
- **For the next scripts:** say the searched phrase in the first spoken sentence (YouTube matches search against "video content"; the cat cut says "sugar" where people type "sweet"), and read TikTok's `suggestedWords` on a few top videos of the topic before fixing the on-screen phrase.
- What the research found, what was changed on the 14 posts and what could not be measured: `oh-meatball/research/93-metadata-all-angles.md` and the log, same heading.

## Make them funnier (Nolan, 11/12 about 10:20 ET, after watching the short dog cut)
- **His words:** "Ok make them funnier we hold no retention". (The message arrived twice. It is one order.)
- **What it means (my reading):** the videos read like a study summary and people leave. Every Short and TikTok cut must be funny first: the fact-check hedges stay true but they may not be the whole script. Starts with the seven pet and survival cuts on both platforms; then it is the rule for every new script.
- **The rule for every new Short and TikTok cut from 11/12:**
  1. Funny first. The hook is the fact; line 2 is a Meatball gag acted out on screen with a prop or a card.
  2. After that, every fact line either is the joke or is followed by one. A line that is only a study detail is cut. Keep at least two sourced facts.
  3. Jokes are on Meatball. Never on the viewer or a group, and a joke never adds a number, a danger or health claim, an animal's feeling or motive, or a safety instruction. Hedges stay ("probably", "may", "in one small study").
  4. YouTube: mild words, one or two. TikTok: about one swear a line. Attributions and safety instructions are said clean, with the reaction after.
  5. A second model checks the jokes (`oh-meatball/research/92-factcheck-funnier-cuts.md` is the pattern). Then every render is transcribed and compared with its script.
- **Traps found doing it:** write "his cat" and "his dog" in full (the voice swallows a bare "his" and a speech model hears "is"); "let out a meow", never "meowed"; `tools/drawn.py` exits with an error and leaves the old mp4 in place when the voice service returns no audio, so check the exit code and trust only the transcript.
- **How it will be judged, and what cannot be:** YouTube: average % viewed and engaged share of these seven from Windsor (2 to 3 days behind, so today's two read on Sun 11/15) against the Shorts that reached 1,000 to 2,000 views (engaged share 0.50, average viewed 81%, research 90). TikTok: likes, comments and shares per view on the seven 19:00 cuts against the account's 2.2%, 0.05% and 0.06% (research 91). TikTok watch time and finish rate are in Studio only. Not separable: none of the seven posts in its plain version, so the jokes and the new topics move together, and the TikTok 19:00 test now changes three things at once (short, search phrase on screen, sweary jokes).
- **"Ok try these today" (Nolan, 11/12 about 11:45 ET, after the two samples: the funnier dog TikTok and the YouTube cat Short).** My reading: post those two today. Both were set for Thu 11/12 (slot moves in the log). Nothing else was moved up: three Shorts a day stays the limit on YouTube.
- **The bug Shorts already in the queue (Fri 11/13 to Fri 11/20) stay as they are for now:** they are the plain comparison, and four of them are the YouTube joke test. Decide at the Sun 11/15 read: if the funnier seven hold better (average % viewed and engaged share), the bug Shorts not yet posted get the same pass (gag in line 2, joke check, re-render, swap); if not, look at the hook and the first two seconds next, not at more jokes.
- What was done 11/12 and what changed in each cut: the log, same heading.

## Views are stuck on both platforms (Nolan, 11/12 about 09:35 ET)
- **His words:** "Shorts did terrible yesterday and TikTok we need more views we're stuck in a view jail figure how we can fix both".
- **What it means (my reading):** two jobs, both about reach. (1) Find out why Wednesday's YouTube Shorts fell (four of five under 350 views, research 89) and stop it happening again. (2) Get TikTok out of the 200-to-300-view band it has sat in since the first post (median 226 over 78 posts; only three posts ever passed 1,000).
- **What the research found:** `oh-meatball/research/90-shorts-drop-1111.md` for YouTube, `91-tiktok-view-jail.md` for TikTok; summary in the log, same heading.
- **YouTube is back to three Shorts a day, at least three hours apart** (slots in "Posting"): Nolan's 3-a-day order of 11/6, which every good day in November had. Pets and Would Meatball Survive now sit at Thu 16:00 cat and 19:00 moose, Fri 16:00 dog and 19:00 grizzly, Sat 19:00 cat name, Sun 14:00 shark, Mon 10:00 tail wag; a bug Short leads the other weekdays at 10:00. The bug Shorts that were pushed out run Tue 11/17 to Fri 11/20. **Do not go above three a day again without numbers that say it is safe.**
- **TikTok search-led test (built, reviewed and scheduled 11/12):** seven short cuts (17 to 19 s, files `oh-meatball/episodes/drawn-house/tts-<slug>.mp4`, specs `scripts/drawn-house/tts-<slug>.json`) of the new pet and survival Shorts, with the phrase people type on screen for the first 2 to 2.5 seconds (spec key `search_top`, new and opt-in in `tools/drawn.py`; kept 150 px down so TikTok's top bar does not cover it) and leading the title and caption ("why does my dog look guilty"). The 19:00 slot, after Nolan's "try these today": Thu 11/12 dog guilty look, Fri 11/13 cat sugar, Sat moose, Sun cat name, Mon shark, Tue tail wag, Thu 11/19 grizzly. Wed 11/18 19:00 is the bed-bug post.
- **Pass mark, read Fri 11/20:** the test cuts' median is 400 or more, or three of six reach 500 (by chance alone the median passes 370 one time in twenty, research 91). The 20:15 sweary cuts stay as their own comparison. **Later on 11/12 the seven were replaced by the funnier sweary versions (20.7 to 25.8 s; same slots, titles and captions; see "Make them funnier"), so their spoken lines are no longer the YouTube ones and the test reads short + search phrase + sweary jokes together.**
- **His answer (11/12 about 10:05 ET, with the 615-against-340 numbers in front of him): "No, keep it all drawn".** So no real photos or footage on TikTok either; the look stays fully drawn. Do not propose it again unless he raises it; the cartoon label stays a noted lead, not a test.

## Direction change (Nolan, 11/11 evening): speak to the majority, steer away from bugs
- **His words:** "Maybe we try to steer away from bugs", then, after I pointed at the bug numbers: "No but people don't really like bugs, we need to speak [to] the majority of people that find [it] interesting or funny, we need to speak [to] the majority."
- **What it means (my reading):** topics most people like, told so they are interesting or funny. Bugs are a narrow taste, so no new video is built about bugs. Everything else stays: the drawn look, the Andrew voice, the jokes (heavy on TikTok, mild on YouTube), sourced facts and the second-model check.
- **What happens to the bug videos already made:** they keep their slots (the spider long-form Sat 11/14, Christmas tree Wed 11/18, centipede Sat 11/21, the queued Shorts and TikToks). They cost nothing more and keep the upload count up while the new videos are built. If Nolan wants them pulled, pull them.
- **What I told him the data says, so the next session knows it was said:** our house-bug videos beat our other animals so far (numbers in the log). He heard that and chose the wider audience anyway. Do not argue it again; measure the new topics against the bug baseline and report the numbers.
- **Research first (Nolan 11/11, about 19:30, after I built and scheduled a cat Short and a moose Short on my own guess of what "the majority" likes): "No wait do research don't jump to conclusions you need to do this every time. Stop and look at my message and continue."** The rule: nothing new is built or scheduled on a new direction until the research is in and he has seen the options. Research 83 (`oh-meatball/research/83-majority-topics.md`) answered this one; its numbers are in the log.
- **His pick (11/11 20:00, from four options with the numbers in front of him): "Pets + Would You Survive".** All new videos: about half are cats and dogs in your house (best odds for a Short: about 1 in 3 small-channel pet Shorts pass 10,000 views), half are "Would Meatball Survive?" with big dangerous animals (about 1 in 3 long videos and 1 in 8 Shorts pass 10,000; the viewer or Meatball is put in the scene). Judge by the share of new Shorts over 5,000 views and by long-form hours, not by the median alone (the bug median is already good). Every new one still goes fact pack, script, live-source check by a second model, then build.
- **How it is judged:** each new-topic Short against the bug Shorts' median (about 1,550 views at 48 h, about 104% average viewed for drawn v6); each long-form against the thresholds in "The YouTube play". Report after the first four.
- **The seven Shorts built on it** (`oh-meatball/research/84`, `86`, `92`; slots under "Views are stuck on both platforms"): the first read is Wed 11/18, when six are 48 hours old: the share over 5,000 views against the bug median of about 1,550.
- **Rules the 11/12 check added for pet and survival scripts (21 wordings softened, none wrong on safety):** (1) "your cat" or "your dog" plus a lab result needs "probably", "likely" or "may" (only the cats that settled down were analysed; a wag direction is a lean, not a rule). (2) A reaction must not carry a feeling or a motive: "Poor bastards" and "lazy" are claims, "Unfair as hell" and "Tough damn crowd" are not. (3) A safety card carries its condition on the card ("PLAY DEAD / ONLY IF IT KNOCKS YOU DOWN"), and "play dead" is never a bare line: only once a surprised grizzly has knocked you down, fight back if it keeps going, stalked you or is in your tent, and the black-bear rule is credited to the Park Service (Alaska's guide calls the species rule a myth and says judge the bear's motive). (4) No single bear speed and no single bear-spray distance: the agencies differ. (5) Shark counts say "confirmed" and the year. (6) Bear advice and shark advice never share a line (eye contact is advised for sharks and disputed for bears). (7) No ending says a tactic saved Meatball: "Meatball lived. Nothing's guaranteed."
- **TikTok on the new direction:** two one-minute sweary-joke cuts from the same facts, checked twice by the second model (`research/86`, second part): the grizzly cut Fri 11/13 20:15 and the dog guilty-look cut Mon 11/16 20:15. **One more swearing rule from this check: a safety instruction is said clean, like an attribution, and the swear is the reaction after it** ("...stop and hold your ground. Scary as fuck.", never "hold your fucking ground"). That is why a safety-heavy cut carries fewer f-words than the 20 to 25 ordered; do not pad it. "Be fucking honest." as the closing prompt is fine (a prompt, not an insult). Every bear cut must say when to use bear spray ("only on a charging or attacking bear") if it mentions spray at all.
- Drawing options for dogs, big animals and underwater scenes: `.claude/skills/make-short/references/spec.md` (and the log, same heading).

## The YouTube play (11/11, from Nolan's Studio paste; numbers in KNOWLEDGE)
- **Where it stands:** numbers in "Where we are". At that pace the 4,000 hours never arrive, so the plan needs one long-form to break out, not a slow climb: 40,000 views at 6 minutes each is the whole 4,000.
- **The play (unchanged, now with numbers to beat):** two long-forms a week in the one-creature "Don't squish it" format, white thumbnails, three thumbnails or titles in the A/B test, and Shorts as 16-20 s trailers with Related video set to the long-form. From the evening of 11/11, new long-forms follow "Direction change" (see "Watch hours").
- **How each long-form is judged at 72 hours (my thresholds, not Studio's):** click-through 4% or more (now 2.5%), 100 views or more (Part 1 had 177 at 74 h), average viewed 35% or more. Under 3% click-through: new thumbnail and title the same day (the same video can do 3,500 or 679,000 on packaging alone, research 70). Good click-through but under 25% viewed: rebuild the first 30 seconds.
- **Taken from Studio's AI:** the 0:04-0:06 drop. The second line of every Short is about the viewer's house or an action, never a life-cycle or anatomy line. From 11/12 that line is the Meatball gag ("Make them funnier", rule 1).
- **Not taken (reasons in the log):** the "Every Bug Ranked" compilation of Shorts, and live-action or macro footage in the first 3 seconds. The one piece that fits the locked look is keeping Meatball out of the first 3 seconds (animal only); that is the next hook test, after the current one reads out.
- **Jokes on YouTube, with a little spice (Nolan 11/11, after the TikTok joke cuts: "that's really good, what about yt, what should we do there"; then, on the clean sample: "Ok maybe for yt spice it up a little bit as much as TikTok though"; my reading: a little, not as much as TikTok).** Same joke style as TikTok with mild words only: damn, hell, ass, badass, bastards. One or two per Short; in a long-form about one every 25 s, and nothing before 0:25. No f-word, nothing stronger, and never in a title, description, thumbnail or pinned comment. Why not TikTok's level: YouTube's ad rules on profanity (the log), and ads are what the 4,000 hours are for.
- **Joke test:** jokes plus mild words in four Shorts (#53 roach and #51 boxelder, both posted Wed 11/11; #54 mice, Sun 11/15 08:00; #57 fungus gnats, Tue 11/17 10:00) against the four plain ones (#52 cluster flies, #55 booklice, #56 dust mites, #58 carpet beetle). Read views at 48 h and average % viewed when Windsor has it; if the joke four are level or better, every Short and every long-form script gets them. Still true: do not read the joke test or the hook test from Wednesday's raw views.

## TikTok orders (Nolan, 11/11)
- **TikTok Creator Rewards: RESTORED 11/11** (Nolan appealed; TikTok's notice is in the log). Rewards pays only on original videos of 1 minute or more that reach 1,000 qualified For You views, and our median TikTok gets about 220. So a one-minute cut (61-75 s) is built only on a topic that has already passed 1,000 there (house centipede 3,728 and 1,686; bombardier beetle 5,972) or a close cousin, with a stay/squish or yes/no prompt in the caption. Shorter cuts, the two exceptions and the sweary-cut length: see "Posting". Keep the AI-generated label ON (the voice and scripts are AI; TikTok asked Nolan to confirm it 11/10-11/11): never remove it to chase reach. Never use follow-for-follow or any engagement tool: the account has already been disqualified once.
- **TikTok narrator swears (Nolan 11/11: "make the narrator curse frequently, it helps hold attention and humor").** The heavy version is for TikTok cuts only; YouTube gets a little (mild words, see "Jokes on YouTube" in the YouTube play).
- **Harsher words are ordered (Nolan 11/11: "Use harsher cursing like fuck and shit"), and then more of them (Nolan 11/11, after hearing the 7-f-word cut: "Note frequently I want like one a sentence"; my reading: not frequent enough, about one swear per sentence).** So every narration line carries at least one swear, as a reaction to the fact: lead with fuck, fucking, fucker and shit (20-25 f-words per one-minute cut), with damn, ass, bastard, badass and bullshit for variety. A fact sentence may stay clean only when the swearing reaction follows it in the same line. One line stays fully clean on purpose: any line that names a nationality, ethnicity or other group of people (e.g. "Asian camel crickets").
- **Jokes (Nolan 11/11: "make them joke more using the cursing, like this thing has enough venom to fucking kill a small village or something like that").** Six to nine sweary jokes per cut, in place of the bare reactions ("Fuck yes.", "Thank fuck."). A joke is a simile ("like a tiny fucking cowboy"), a roast ("Giant, my ass"), an order ("Just hand them the fucking keys") or a looks-like line that the real fact answers in the next breath ("It looks like it could fucking kill a small village. It can't."). My guardrail, checked by a second model on every cut: a joke never adds a number, a venom, danger or health claim, a behavior, or a "free pest control" claim that the fact-checked line does not support, because on a channel that corrects myths a made-up venom line said straight would be a new myth. To make room, each cut loses its one or two slowest facts and runs 85-92 s. Never aimed at a person or group, no slurs, never inside a sourced attribution ("Penn State says..." and "scientists tested..." stay clean; the reaction comes after), and the facts do not change.
- Two traps the 11/11 second-model check caught: an insult with "you" can sound aimed at the viewer (write "Verdict: the ugly bastard stays", not "stay, you ugly bastard"), and a reaction must be a pure exclamation ("holy shit", "fuck no", "fucking wild"), not a new claim ("easy as shit", "confuse the shit out of", "basically bullshit", "dumbasses").
- Captions soften the spelling with the spec key `cap_swap` (every spelling used needs its own entry); the voice says the word. Titles, captions under the post and hashtags stay clean.
- TikTok's Community Guidelines and For You standards (effective 2026-09-24) do not mention profanity, only "content that may not be suitable for a broad audience", so the risk is unmeasured: compare the swearing cuts' views with the clean ones after a week. If TikTok views drop, cut beats, not swears.
- **For You vs Search (research 81, 11/11; Nolan: "a lot of views on TikTok from search but not fyp so maybe the descriptions or hashtags need a little change").** Captions and hashtags are not the lever. What puts a video on For You is people finishing it. The caption standard is now in "Tags and everything, from every angle". Not measurable from here: the For You/Search split and retention per video (Metricool returns nulls; only TikTok Studio shows them).
- **TikTok category label (research 82; a lead, not a test):** TikTok files our drawn videos under "Comics & Cartoon, Anime" (numbers in the log). Nolan said no to a real-photo test ("Views are stuck on both platforms"). The label is readable on a video's public page within an hour of posting, so any test reads fast.
- First read: Nolan asked for one joke cut "posted asap to see how it does", so it went out Wed 11/11 11:32. Its numbers and the other first reads: the log under "Overview".

## STYLE LOCK (Nolan, 11/1): no more style changes
- **The look is locked:** the drawn style with stick-figure Meatball and TARS's species-accurate animals (`art/drawn_anatomy.py`). Nolan approved it on 10/30 ("way better, continue this style"). Fully drawn, on YouTube and TikTok: no real photos or footage (Nolan 11/12: "No, keep it all drawn").
- **The voice is locked:** Andrew (edge-tts `en-US-AndrewMultilingualNeural`, rate +10%, pitch +3Hz), approved by Nolan 11/1 on House Centipede Part 2 v2; that approval supersedes the older voice line of this section (now in the log under "Retired").
- **Locked for 8 weeks from 11/1.** No style tests, no photo/realistic/hybrid samples, no new render pipelines.
- **Allowed to change, one per week:** hooks, titles, topics, and new animals built with the same anatomy kit.
- **Nolan, 11/1:** "I like the style we have going. Only changes: more animations, more visibly exciting and engaging." That means more movement inside the SAME look: the animal acts out every line (walks, lunges, turns), camera punch-ins on the oh-no beat, more scene changes, a visual gag on each wow fact. It is not a new look.
- **Every Short (Nolan 11/1, approved on House Centipede Part 2 v2):** the Andrew voice (+10%, +3Hz), animals that hop and lunge, and **at least 3 locations**. Give each middle line its own `scene:`; the hook and the last line share a room so the loop is seamless.
- **Anyone proposing a style change must bring numbers to Nolan first.** Never send a sample instead.

## The shows (nothing else on YouTube)
**From 11/11 (Nolan's pick, see "Direction change" near the top):** every NEW video is either a pet in your house (cats and dogs; they run as Things Living In Your House #N with "Your cat" or "Your dog" leading the title) or a Would Meatball Survive? #N with a big dangerous animal. No new bug or spider episodes are built; the ones already made keep their slots.
1. **Things Living In Your House #N**: house bugs and mites (the best first-second hold: 58.6%).
2. **Is This Spider Venomous? #N**: spiders (the top search terms: daddy long legs, venomous spider).
3. **Would Meatball Survive? #N**: big dangerous animals (the best at bringing viewers back).

Any pet or survival Short that beats 2x the median gets a Part 2 within 48 h. A bug winner gets none ("Direction change": no new bug videos).

## The Short template and title rules (from "Studio data 11/3" and "Scoreboard 11/10")
- **No "TRUE or FALSE" / quiz-style titles or hooks on YouTube** (20-28% stayed vs 55-63% for house creatures). Banned title words: TRUE or FALSE, Myth, Believe, Cartoons, Lied, "Did you know".
- **The v6 template (every render from 11/3):** narration from 0.00 s; frame 0 is the animal close-up already moving (Meatball hops in at ~2.3 s, smaller); a visceral "you" + number hook; line 2 (3-7 s) is the Meatball gag ("Make them funnier", rule 1), never the name or anatomy; no spoken or visual outro (no Subscribe, Part X, Follow or end card); the last line flows into the hook in the hook's room; the comment question is a top-corner pill on the last line and the pinned comment; a new fact or visual every second, cuts every 1.5-2.5 s, keyword cards in seconds 1-4, center captions. YT 16-20 s; TikTok lengths are in "Posting".
- **No Short under 15 s (Nolan 11/10, on the 7-second stink-bug loop: "a little too short, we need a little more info").** YouTube Shorts run 16-20 s with at least two sourced facts plus a payoff.
- **Only two kinds of Short flop outright (under 100 views):** case files, and skin-harm house topics.
- TikTok lengths today are in "Posting". The rest of both sections: the log, under those two headings and "Retired".

## The production line (one Short, every time, in this order)
Commands and details: `.claude/skills/make-short`. Run them from `skills/oh-meatball`.
1. Research: `postkit.py kw` and `ttpage`; a fact pack with a source for every number.
2. Spec JSON: `scripts/drawn-house/<slug>-v6-yt.json` and `tts-<slug>.json` (copy the newest pair).
3. A second model checks every changed line.
4. `postkit.py render SPEC OUT --work DIR` (the voice check is inside).
5. Look at the contact sheet.
6. `postkit.py lint SPEC --mp4 OUT`.
7. `git add --sparse`, commit, push, `postkit.py rawurl`.
8. `postkit.py payload`, Metricool create or update, `postkit.py rehost`, `postkit.py log`.

**Gate:** no video is scheduled unless postkit.py render or voicecheck passed on that file and postkit.py lint passed on its spec.

**Voice check:** tools/drawn.py refuses stored takes that fail the check; after every render run postkit.py voicecheck SPEC MP4 and schedule only a pass.

## Posting
- **YouTube (Nolan 11/6):** three Shorts a day, at least 3 hours apart. Weekdays 10:00, 16:00, 19:00 ET. Weekends 08:00 or 11:00 after a long-form, 14:00 or 15:00, 19:00 ET. Never above three a day without numbers that say it is safe. Never a Short in the long-form's slot: on a midweek long-form day (17:00) the queue holds two Shorts, 10:00 and 19:00.
- **TikTok:** 12:00, 19:00, 21:30 ET, plus the 20:15 one-minute sweary cuts already scheduled. The 19:00 slot carries the 20 to 26 second search-led cut through Thu 11/19 (verdict Fri 11/20). One-minute cuts only on proven topics, except the grizzly and dog 20:15 cuts already scheduled ("Direction change"). Sweary one-minute cuts run 85-92 s; 61-75 s is for clean cuts.
- **Cuts under a minute** are still for YouTube, except in that one TikTok 19:00 test slot, where views come first because Rewards pays nothing until the account can join.
- **Titles, descriptions, tags, captions:** the standard in "Tags and everything, from every angle"; `postkit.py lint` checks it.
- **Pinned comment (Studio AI, 11/5):** an open question that pulls a story or a debate ("What's the weirdest bug you've found in your room?", "Did you actually check your mattress after this?"), not yes/no. Yes/no prompts got skipped: most comments were our own. Once real replies come in, pin the funniest viewer reply instead of our prompt.
- The AI label stays on. Every scheduling change goes into `oh-meatball/data/posted.csv` the same day. Older slot lists: the log, "Retired".

## Watch hours (the hard part of YPP)
**11/11: the subscriber half is done (1,000).** What is left is 4,000 long-form watch hours (8,000 for anyone applying from 2027-02-01). Long-form decisions are judged on long-form hours; Shorts and TikTok on views (Nolan 11/12, "Where we are").
**Nolan, 11/5 (overrides the 10/30 case-file plan and the Sunday compilation; detail in `oh-meatball/research/65-longform-reset.md`):**
- **One show:** every long-form is a **Things Living In Your House** long edition, about the creatures our Shorts already win with (house centipede, house spiders, cockroach, bed bugs, dust mites, mice). Same locked look, Andrew voice (+10%, +3Hz), 16:9.
- **From 11/11:** new long-forms follow "Direction change" (first one: the house cat, Sat 11/28). The bug long-forms already made keep their slots.
- **A full episode, never Shorts put together.** It is scripted and rendered as its own video (like `scripts/longform-kill-or-keep.json`):
  - one promise in the title, paid off in the first 5 s, with narration starting on the creature at 0.0 s
  - no joke, intro or comment ask before 0:25
  - its own arc, with a new peak every 20-30 s and a payoff at the end that the cold open set up
  - never a stitch, compilation, recut of posted Shorts, or blurred-side vertical
  - target 8-12 min once retention holds; 5-7 min is fine until then
- **Two slots (Nolan 11/10: "push more long form"):** **Saturday 08:00 ET** plus a midweek long-form (**Wed or Thu 17:00 ET**).
- **Long-form queue (order set 11/10 from the scoreboard, fact-checks and our own retention curve; research 69, 72-74):**
  - Wed 11/11 17:00, posted (Nolan 11/11: "I want a long form yt to go out today on top of the shorts so push that"): **Kill-or-Keep Part 2** ("3 More Bugs in Your House You Should Never Kill (And 5 You Must)").
  - Sat 11/14 08:00: **"Don't squish it" episode 1, the spider in your corner** ("Don't Kill the Spider in Your Corner. It Eats Bigger Spiders", 8:17, thumbnail `cellarspider_b.jpg`).
  - Wed 11/18 17:00: **Christmas-tree episode** ("Never Bring a Christmas Tree Inside Before You Check for This", 7:13, thumbnail `xmas_a.jpg`; challengers `xmas_b.jpg`, `xmas_c.jpg`).
  - Sat 11/21 08:00: 3D house centipede v2 (fact-fixed; "Don't Squish the 30-Legged Bug in Your Bathroom (Here's Why)", thumbnail `centipede_a.jpg`). Episode 1 ends by pointing at it.
  - Wed 11/25 17:00: Night Shift (v2, fact-fixed), moved twice to make room for the two new-format episodes. The swallow-spiders episode (rendered, 4:16) waits as a spare; it still needs a different-model check of its two new stories.
  - Sat 11/28 08:00: **"Your Life as a House Cat: 8 Ways It Goes Wrong"** (9:16, thumbnail `cat_a.jpg`), the first long-form on the new direction, in the "born as" shape Nolan picked from the options and numbers (next bullet).
- **The house cat long-form (research 85, `oh-meatball/research/85-longform-pets-survive-format.md`; its numbers and the build story are in the log):**
  - **His pick (11/11 about 21:10, with the numbers in front of him; I had recommended the polar bear): "Born as a house cat".** The shape is "Why It Sucks to Be Born as a [animal]": the viewer lives the animal's life.
  - Checker rules from its second-model check (`research/88`): **the checker must open the paper, not the pack; a percentage needs what it is a share of; a survival figure needs the count put down; a safety line needs the trigger a viewer can act on.**
  - **Title:** the post carries "Your Life as a House Cat: 8 Ways It Goes Wrong". "Why It Sucks to Be Born as a House Cat" joins the A/B test only with Nolan's yes to the word (open ask 2; with it the description's first sentence, one tag and thumbnail `cat_s` change too).
  - **Thumbnails** (`oh-meatball/episodes/thumbs-bornas/`): `cat_a` is on the post; `cat_b` and `cat_c` are the challengers for Nolan's A/B test after it posts; `cat_s` waits for his yes.
  - Files: `oh-meatball/episodes/longform-born-as-house-cat/`.
  - Still to do: on 11/24 compare its structure with three winners' transcripts and re-cut the first 30 seconds if they open very differently; judge it at 72 hours by the thresholds in "The YouTube play".
  - The verdict of the video is a sweet deal with conditions, so no title may promise only misery. The polar bear is the next one in this shape if the cat one earns it. Whatever he picks: fact pack, script from the pack, second-model check, one opus build, three titles in the A/B test. A title with "sucks" needs his yes (the mild-word rule keeps such words out of titles); the milder twin is "Why Being Born a Polar Bear Is a Terrible Deal".
- **Long-form format from 11/10 (research 70), the "Don't squish it" bug episodes already made:** one creature, one story, a shoe meter (SQUISH to SPARE) on screen, the verdict at the end. Full format, title shape and data: the log. Still used:
  - **Thumbnail recipe (`tools/thumb_dontkill.py`):** white background, one huge illustrated creature, a shoe sole about to squish it, 2-4 hand-lettered words with one in red, a hand-drawn arrow. Nothing else.
  - **A/B challengers for Nolan (`oh-meatball/episodes/thumbs-dontkill/`):** Part 2 `kk2_c.jpg` and the old `thumb_a.jpg`; centipede `centipede_b.jpg`; cellar spider `cellarspider_a.jpg`. Skip the Meatball-in-thumbnail variant: he is a brown dot at 168 px.
  - **Length:** 8-12 minutes. At the same views a 10-minute video earns 3-4x the watch hours of our 4-6 minute ones.
  - **Shorts feed it:** in the week of each long-form, two or three 16-20 s Shorts on the same creature (different facts, at least a day apart), each with Related video set to the long-form.
- **Script pipeline from 11/10 (three different models):** a sourced fact pack first (`research/76`, `77`) -> the script written only from the pack, every factual line tagged with its fact IDs -> a line-by-line check against the live source pages (`research/78`, `79`) -> build. The checker must open the original pages, not trust the pack.
- **Every long-form script (from research 72's checklist):** every claim in the hook is still true when the video reaches that item; a count and an order in the first 15 s; part of the promise paid before 1:00; the first item is never the dullest one; no more than two items in a row with the same shape; each item ends on the next item's stake; a re-hook at the midpoint; a character beat every 30-40 s; no spoken 3-2-1 countdowns (a short pause-and-reveal at real twists only, three at most); ending = callback + "watch this next".
- **Case files are DROPPED** (Nolan 11/9: the Azorian teaser Short did terribly). No case-file Shorts, long-forms or teasers. Don't propose them again unless Nolan asks.
- **No Sunday compilation** until a weekly long-form passes 500 views.
- **The bridge (Nolan, Studio):** every on-topic Short's Related video points at the newest long-form, and that Short's pinned question ("Posting") ends with "Full list in the Related video 👆". Re-point the links every Saturday.
- **Cadence rule (updated 11/10):** two a week now (Nolan's call). If midweek long-forms average under 50 views at 7 days for 3 weeks running, drop back to Saturday only.
- What the data said, what was built when, and the retired Expansion and Packaging lines: the log.

## Nolan's jobs (Studio only)
Standing Studio jobs, not new asks. Do not chase them while an open ask is waiting.
1. Make 3 playlists (one per show). Set each on-topic Short's **Related video** to the newest long-form ("The bridge" in "Watch hours"), any other Short to its show's playlist.
2. Pin the 11/1 house tier list.
3. After a long-form posts: add its challenger thumbnails in the A/B test ("Watch hours").
4. Optional: one Community poll a week (creature against creature); nothing else new in Studio.

## Agent routing (Nolan 11/10: "pick the cook by the order")
- **Usage limit (11/10):** five agents in one afternoon (two opus builds, an opus fact-check, sonnet builders) used up Nolan's 5-hour plan limit and stopped a build mid-way. Run one opus build at a time, give sonnet the fix passes and research, and do reviews in the main session. A stopped agent keeps its work: resume it with a message after the limit resets, don't start over.

Match each background agent to its job: cheap models for chores, the strongest for hard or high-stakes work. Forks always run on the main model, so use fresh agents (general-purpose, with a full brief) wherever a cheaper model fits.

| Job | Model | Examples |
|---|---|---|
| Chores / prep | **haiku** | WIP commits, posted.csv logging, schedule listings, yt-dlp research pulls, transcriptions, contact sheets, Metricool reads |
| Routine builds | **sonnet** | Shorts from existing templates (drawn v6, 3D explainer with an existing ep module), hook re-cuts, captions/descriptions, batch scheduling |
| Hard builds / bugs | **opus** | new long-forms, pipeline code changes (drawn_keepkill, sim3d), render failures nobody can find |
| Planning / strategy | **fable** | channel strategy, format plans, script structure for engagement |
| Review | **a different model than the builder** | fact-check scripts against `_sources`, QA contact sheets before anything is scheduled |

Each Short or long-form gets a second pass by a different model before it's scheduled.

**Agents never change the repo with git** (11/12: a reviewer's failed `cd` ran a commit and a checkout in the real repo and wiped four uncommitted files; they were rebuilt from the session log). Every brief says: no add, commit, checkout, restore, reset, stash, clean or sparse-checkout; the main session commits, and commits before it starts any agent.

## Research loop (Nolan 11/10: "look at outliers and how they hold their retention… keep running research like this")
Decisions come from data, retention first. For big format changes Nolan wants the evidence and the options before anything is built.
- **Before any new format or long-form:** small-channel outliers for the idea (views ÷ that channel's own median, never raw views), our own retention for the nearest thing we've posted, and the search demand for the title (research 75).
- **Every script:** research 72's checklist before the render; a fact-check by a different model against the cited sources before scheduling (research 73 and 74 found 7-10 overstated lines in every one of five long-forms that had only been checked by their writer).
- **Daily, 07:37 ET (scheduled check "Daily channel scoreboard"):** refresh research 69's tables; every video at 48 h against its style's median; winners (2x the median) get a sequel within 48 h (pets and survival only); fix queue gaps and off-niche posts.
- **What works for data:** Metricool analytics (YouTube per-video views, watch minutes, average view duration; TikTok views, likes, comments, shares, duration); Windsor.ai (Nolan's YouTube: average % viewed, engaged views and subscribers gained per video, 2-3 days behind); yt-dlp flat listings (public views, channel medians, subscriber counts); web search. From 11/12 also: Windsor `traffic_source` per video (one call per video with the filter `[["video","eq",ID]]`), `shares` and `country`; public TikTok pages with `tools/postkit.py ttpage` (plays, label, TikTok's suggested searches); YouTube and Google search suggestions with `tools/postkit.py kw`. The `scoreboard` skill has the table.
- **What doesn't:** retention curves for our videos (Windsor has none; vidIQ's `audience_retention` report costs 5 credits a video, so wait for the 2,000-credit reset on 2026-11-24, or Nolan's Studio screenshots if he offers them, open ask 4); TikTok retention (Metricool returns nulls); other channels' "Most replayed" graphs and transcripts (YouTube blocks full video-page extraction from the cloud machine with a bot check; don't route around it); Higgsfield (0 credits).

## The work gate (every task)
"Which post in the next 7 days, or which scorecard number, does this change?" No answer → `skills/channel-brain/later.md` (create it if missing), don't do it. Research is continuous (Nolan 11/10: "keep running research like this"; this replaces the once-a-week cap), but every research run must still end in a queue or script change.

## Weekly scorecard (Sunday, 3 numbers only)
| Number | Now | 4-week target |
|---|---|---|
| Returning viewers (7 days) | ~2,847 per 90 days | 2x |
| Subs per 1,000 views | ~0.3 | 1.0 |
| Stayed-to-watch, show Shorts | 39.5% channel | ≥ 50% |

Plus watch hours (12-month) and TikTok rewards. One change per week, picked from the worst number. (The "Now" column was filled 10/29; those three need Studio.)

Read first from 11/12, because they can be pulled every day (`scoreboard` skill): views per post on each platform (YouTube Shorts median about 1,100, research 93; TikTok about 226, research 91), long-form hours against 4,000 (10.6 in 28 days, Studio 11/11; kept in `oh-meatball/data/longform-hours.csv`), and the engaged share of new Shorts (0.50 on Shorts that reached 1,000 to 2,000 views, research 90).

## Verified platform facts (2026-11-10, primary sources; research 71)
- **YPP:** 1,000 subs + 4,000 qualified long-form hours in 12 months, or 10M qualified Shorts views in 90 days. Shorts-feed watch time doesn't count toward hours; loops don't count as qualified Shorts views. **From 2027-02-01 new applicants need 8,000 hours or 20M Shorts views** (checked on YouTube's help page). The 500-sub tier (fan funding and Shopping, no ads: 3,000 hours or 3M Shorts views) is unchanged.
- **Shorts ranking, official signals:** chose-to-view vs swiped, average view duration, average % viewed, likes, surveys. **No official stayed-to-watch benchmark exists** (the "70%" figure is folklore: compare our Shorts with each other). Each video is judged on its own; a weak upload doesn't penalize the channel and no posting cadence is required.
- **Views** count from the first frame since 2026-08-24 on all formats; the old definition is now "engaged views".
- **Related video on a Short:** set in Studio (needs advanced features); no documented API field.
- **"A/B test titles & thumbnails"** (was Test & Compare): up to 3 variants, desktop Studio, long-form only, winner by watch-time share.
- **Hype** needs YPP membership, so we can't use it yet.
- **Inauthentic-content policy:** the risk is sameness (same situation, same outcome, a template). A recurring-character series is fine when each video has its own concept. The synthetic-content label is required only for realistic content, and YouTube says it doesn't limit reach or earnings.
- **TikTok Creator Rewards:** 10K followers + 100K views in 30 days to join; pays only on original videos of 1 minute or more that reach 1,000 qualified For You views (a qualified view is a unique For You view watched 5+ s). TikTok says the AI label doesn't affect distribution.
