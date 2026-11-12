---
name: oh-meatball
description: Run "Meatball Myths" (YouTube UCw98RQD81t_339LX5EJqcrg, TikTok @meatballmyths). The channel is a stick-figure meatball who explains weird true things, fully drawn: a long-form Saturday 08:00 plus one Wednesday or Thursday 17:00, three YouTube Shorts a day, TikTok 12:00, 19:00 and 21:30 ET. Use it to make (.claude/skills/make-short), write text (post-metadata), schedule (Metricool) and read the numbers (scoreboard).
---

# Meatball Myths

**The show:** Meatball, a meatball who's scared of being eaten, explains the weirdest true things about animals, food, history and the human body. Meatball himself never changes (look, voice, persona). Everything else gets tested.

The old cat soap opera (numbered serial episodes, Veo shots, OpusClip) was retired on 10/22. Its leftovers live in `story/`, `caught-on-camera/` and `new-format/` and are never used.

## Read these, in this order
1. `skills/channel-brain/MASTER_ORDERS.md`: the standing orders and the rules in force. Read it first, every session. Then `skills/channel-brain/KNOWLEDGE.md` and the newest files in `research/` (highest number).
2. `python3 skills/channel-brain/tools/scan.py skills/oh-meatball` (read-only): the queue, cadence and stale-file check. It writes nothing unless you pass `--json FILE`.
3. `OPERATIONS.md`: the team, the numbers we steer by and the older standing orders. Its Cadence and Gate sections are current; the long blocks below them are history and say so.
4. `TOWN.md`, `KNOWLEDGE.md` (tested findings) and `SELF_REVIEW.md` (mistakes and the checks that catch them).

## What is true today (2026-11-12)
- Fully drawn, no real photos or footage. Voice: edge-tts `en-US-AndrewMultilingualNeural`, +10%, +3Hz.
- YouTube: three Shorts a day at least 3 hours apart (weekdays 10:00, 16:00, 19:00 ET; weekends 08:00 or 11:00 after a long-form, 14:00 or 15:00, 19:00). Long-form Saturday 08:00 plus Wednesday or Thursday 17:00.
- TikTok: 12:00, 19:00, 21:30 ET. The 19:00 slot carries the 20 to 26 second search-led cuts through 11/19; one-minute sweary cuts go at 20:15.
- New videos are pets or Would Meatball Survive. No new bug episodes, no case files. Research is continuous and every run ends in a queue or script change.
- The bottleneck is views on both platforms, then 4,000 long-form hours.

## Gate (permanent)
No Short is scheduled unless `postkit.py render` (or `voicecheck`) passed on its mp4 and `postkit.py lint` passed on its spec. Post bodies come from `postkit.py payload`, not from typing.

## Pipeline
Spec JSON -> second-model check -> `postkit.py render` -> contact sheet -> `lint` -> push and `rawurl` -> `payload` -> Metricool -> `rehost` -> `log`. The steps and commands are in `.claude/skills/make-short`; text is in `.claude/skills/post-metadata`.
- **Thumbnails (long-form):** `tools/thumb_dontkill.py`.
- **Measure:** `.claude/skills/scoreboard` (Windsor, Metricool, `postkit.py ttpage`). vidIQ only after its credits return on 11/24.
- Each test gets an `E<n>` row in `data/experiments.csv`.
