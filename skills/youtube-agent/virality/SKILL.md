---
name: virality
description: Find outlier videos in the caught-on-camera / funny-animal niche (videos beating their own channel's median views) and turn each into an "our version" brief for Oh Meatball. Use when asked what is going viral, for outliers, competitor research, trend ideas, or "what should we copy".
---

# Virality: outliers -> our version

An outlier is a video doing far better than its own channel normally does. A 900k video on a 10M-sub channel is
noise; 900k on a channel whose median is 2k is a format signal. Free, no API key.

## Run
```bash
cd skills/youtube-agent/virality
# Shorts tab search (recommended for us)
python3 scripts/outliers.py "doorbell camera raccoon" "caught on camera funny animals" --shorts --n 10
# Regular search, only strong outliers, only Shorts-length
python3 scripts/outliers.py "animals caught on security camera" --n 15 --min-score 5 --max-duration 60
python3 scripts/outliers.py "dashcam animal" --shorts --json > /tmp/outliers.json
```
Needs `yt_dlp` (pip) or the source checkout at `/home/user/yt-dlp` (auto-added to `sys.path`; override with `YTDLP_SRC`).

How it works: search (yt-dlp `ytsearchN:`; with `--shorts` it scrapes the type=Shorts results page and reads each
Short's public page for channel/views/length) -> for every channel, flat-list the latest `--recent` (15) items of its
`/videos` and `/shorts` tabs -> **score = views / median(channel's other recent views)**. Channels with fewer than 3
other uploads are skipped. Missing tabs, bot checks and timeouts are skipped with a stderr note; exit 1 only if
nothing could be scored. ~20 s for 2 queries x 10.

Sample (2026-10-20, `--shorts --n 10`):
```
  23.6x    1.4k      59  10s  Unexpected midnight visitor! A raccoon caught on the doorbel | Animal_kingdom
 983.0x   62.9M   64.0k  10s  Cat Pranks Doorbell — Hilarious Doorbell Prank Caught on Cam | Rx Furqan
```

## Read the table
- **score >= 10 on a channel median < 10k** = strongest signal (small channel, format did the work).
- Big-network compilations (Pet Collective, AFV) with huge scores on old uploads = evergreen, lower priority.
- Ignore real news/brand footage for format ideas only; never reuse their footage.
- Prefer 8-15 s results (our length). Note title pattern, camera type, twist, and loop.
- If vidIQ is connected, `vidiq_outliers` is a second source; cross-check, don't replace.

## "Our version" brief (one per outlier, pick the top 3-5)
```
Outlier: "Unexpected midnight visitor! A raccoon caught on the doorbell" 1.4k / median 59 = 23.6x, 10 s
Why it works: IR doorbell look, animal looks into the lens at ~1 s, ends on a stare (loop).
Our version (change >= 2 of animal/camera/location/twist; never copy the scene):
  animal: possum   camera: doorbell_night   location: back porch   twist: plays dead when the light snaps on, then peeks
  hook: #15 "Wait for the porch light"     length: 9 s, twist at 7 s, loop on the dark porch
  title draft: "Possum Thought No One Was Watching… 😳"
Safety: no distress (playing dead is comedic, no threat shown) — OK
```
Rules: transform, don't clone (different animal or twist at minimum; no reuse of their audio, footage, title text or
characters); everything stays inside [algorithm.md §3-4](../../oh-meatball/playbook/algorithm.md) policy. Hand the briefs
to [weekly-plan](../weekly-plan/SKILL.md) and [script-prompt](../script-prompt/SKILL.md).
