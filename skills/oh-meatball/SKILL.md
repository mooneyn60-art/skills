---
name: oh-meatball
description: Run "Meatball Myths" (YouTube UCw98RQD81t_339LX5EJqcrg, TikTok @meatballmyths). The channel is a stick-figure meatball who explains weird true things: story long-forms on Tuesday and Saturday, daily Shorts and TikToks. Use it to script, render (tools/episode.py), package (tools/thumbnail.py), schedule (Metricool) and review the channel.
---

# Meatball Myths

**The show:** Meatball, a meatball who's scared of being eaten, explains the weirdest true things about animals, food, history and the human body. Meatball himself never changes (look, voice, persona). Everything else gets tested.

The old cat soap opera (numbered serial episodes, Veo shots, OpusClip) was retired on 10/22. Its leftovers live in `story/`, `caught-on-camera/` and `new-format/` and are never used.

## Read these, in this order
1. `brain/SKILL.md`: scan first, fix the top 3 issues, and act without asking. Run `python3 brain/tools/scan.py .`.
2. `OPERATIONS.md`: Nolan's standing orders, cadence, voice, the "Meatball is the star" rule, the asks, and the long-form reset.
3. `TOWN.md`: the 10 desks, the daily rhythm, and the square on the town artifact.
4. `research/42-growth-reset.md` (niche, thumbnails, repeat audience), `research/39-meatball-show-bible.md` (persona) and `research/41-stickman-reference.md` (animation).
5. `KNOWLEDGE.md` (tested findings) and `SELF_REVIEW.md` (mistakes and the checks that catch them).

## Pipeline
- **Script:** `scripts/<slug>.json`.
  - Long-form: one story, 6-8 min.
  - Shorts: claim-first with a photo at frame 0.
  - Photos come from iNaturalist and must be CC0 or CC BY.
- **Voice:**
  - Shorts use Bill via `tools/premium_voice.py`.
  - Long-form uses edge-tts Andrew until a free replacement passes (research/39-voice-tests).
- **Render:** `cd tools && python3 episode.py ../scripts/<slug>.json <slug> --work <scratchpad>/rel [--skip-long|--skip-shorts|--skip-existing]`.
  - The Meatball 2.0 rig (`mascot.py`) and the shot grammar (`explainer.py`) are built in.
  - Check the frames before scheduling.
- **Thumbnail:** `tools/thumbnail.py`. Make 3 variants and score them with `vidiq_score_thumbnail`.
- **Ship:**
  - Commit and push, then use raw GitHub URLs pinned to the commit SHA (check each returns 200).
  - Schedule with Metricool `createScheduledPost` (brand 7521392, America/New_York) and log it in `data/posted.csv`.
- **Measure:**
  - vidIQ `channel_analytics`: retention, traffic and subscribers.
  - `brain/tools/abtest.py` scores experiments.
  - Each change gets an `E<n>` row in `data/experiments.csv`.
