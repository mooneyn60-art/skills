# Oh Meatball: daily run (complete instruction set)

Work in /home/user/skills on branch `claude/off-the-lot`, folder `skills/oh-meatball`.
Read SKILL.md first (cast descriptions, arc, format). Never mention cars.

## 0. Sync + budget
Budget math: 2 parts/day = 4 lite shots = ~320 credits/day; vidIQ renews 6,000 on the 22nd each month.
If the balance would not last until the next renewal at 320/day, drop to 1 story part + 2 extras and say so.
- `git fetch origin claude/off-the-lot && git checkout claude/off-the-lot && git pull`.
- `vidiq_balance`. Shots use veo-3.1-lite (80 credits / 8 s). Budget rule:
  keep >= 400 credits in reserve; if below, make 1 part instead of 2 and tell Nolan.
- Read `data/log.csv` for the last part number and what was scheduled.

## 1. Learn from yesterday (2 min)
- `vidiq_channel_videos` on the channel (short, popular=false): views on each part.
- `vidiq_video_comments` on the newest part: what are people arguing about? Who do they side with?
  Use the strongest comment theme in today's plot (that's the engagement loop).

## 2. Plan today's 3 YouTube posts
- 1 STORY PART of 4 shots (punch up the next part(s) from story/season1.md per SKILL.md's updated format; merge two scripted parts into one if needed) + 2 ZERO-CREDIT EXTRAS (pick a format
  from story/extras.md, cut from existing clips in the scratchpad or re-downloaded via their URLs in data/log.csv).
- Slots (ET): 12:00 extra, 16:00 extra, 20:00 story part. Budget: 4 lite shots = ~320 credits/day.

## 2b. Write/adjust the 2 new parts
- Continue the arc in SKILL.md; each part = 2 shots x 8 s, ends on a cliffhanger.
- Write `episodes/NN.json`: {part, shot1_prompt, shot2_prompt, dialogue lines, title, description}.
- Every prompt repeats the cast descriptions word-for-word + the style line.
- Tags (YouTube, comma-separated, <= 450 chars): always "oh meatball, meatball cat, cat soap opera,
  cat drama, animated cat, ai cat, cat story, funny cats, chubby cat, orange cat, cartoon cats,
  ai animation, pixar style animation, cat shorts" + 3-5 episode-specific tags (the twist, the setting).
  Use `vidiq_keyword_research` once a week to swap in rising terms. Put them in the post's `tags`
  field in control-room.html, and pass them to scripts/post.sh / the YouTube uploader when available.
- Titles: draft 3, `vidiq_score_title` (type short), keep the best >= 85, format `<hook> | Oh Meatball Pt N`.

## 3. Make
- Submit all 4 shots in parallel (`vidiq_generate_video`, model veo-3.1-lite, 720p, 8 s, 9:16).
- Poll `vidiq_job_poll`. Download, check 3 frames per shot, transcribe dialogue with faster-whisper
  (decode audio via ffmpeg to float32 first). If a character looks wrong or a line is garbled,
  regenerate that ONE shot with a corrected prompt (max 1 retry per shot).
- AUDIO IS MANDATORY (Nolan 2026-10-15: voices + background music on every video, like competitors).
  Local master: `python scripts/finish.py --shots s1.mp4 s2.mp4 --part N -o clips/ptNN.mp4 --expect "<line 1>" "<line 2>"`
  (mixes voices + brand/theme.m4a ducked under dialogue + brand/sting.wav on the cliffhanger,
  -14 LUFS, then QA: audio present, loudness, no silent gaps, every line heard). If it exits non-zero,
  fix (re-render the shot) before anything is posted. Save raw shots as clips/ptNN_s1.mp4 / _s2.mp4.
- Post copy via vidiq_compose: music = {audioUrl: theme https://ai-music-tracks.s3.us-east-1.amazonaws.com/OfWcrmF_PzqcGLg8z7HR-g/c4b820d0-99d9-498a-aee4-4d59079f23ca.wav,
  volume 0.3, duckTo 0.18, fadeMs 300}; voiceover = sting https://ai-music-tracks.s3.us-east-1.amazonaws.com/OfWcrmF_PzqcGLg8z7HR-g/e030bc24-6fb7-43d4-8ed8-3604a109076d.wav
  at startAtSeconds total-1.5, durationSeconds 1.5, volume 0.7. Download the compose output and run the
  same QA (volumedetect mean between -26 and -9 dB, transcript has the lines) before posting.
- `vidiq_compose` each part (keepNativeAudio) with overlays "PART N" (0-2 s) and
  "PART N+1 TOMORROW" (last 1.7 s). Keep the returned URL.

## 4. Post (YOUTUBE ONLY for now, Nolan's call 2026-10-15)
- PREFERRED (no human tap): if env UPLOAD_POST_API_KEY is set, download each composed MP4 and run
  `scripts/post.sh <mp4> "<title>" "<description>" youtube instagram` (add `tiktok` once on a paid plan).
  Free plan = 10 uploads/month: spend them on YouTube first. Check the JSON response for success and
  log the returned post ids. Instagram can also go through `vidiq_instagram_publish_reel` if Instagram
  is connected in vidIQ (publishingAvailable=true).
- FALLBACK (needs Nolan's one tap):
- `opusclip_submit_project` with the composed URL, skipSlicing true, enableCaption false.
- When ready, `opusclip_schedule_publish` each part to:
  YouTube 69dbd6d3074f7631e21a2343 only. Use the 3 slots above. The extra goes through the same
  OpusClip submit (skipSlicing) -> schedule flow.
- Combine ALL approval tokens into ONE link: https://clip.opus.pro/agent-approvals#<t1>,<t2>,...
- Append rows to `data/log.csv`: date, part, title, shots, credits, opus project, tokens.

## 5. Weekly (Sundays)
- Build "Season 1 so far" long-form compilation (all parts back-to-back, 16:9 letterboxed or 9:16)
  with ffmpeg; send to Nolan for upload as a regular video (watch hours for monetization).
- Score the week: views per part, subs gained, which cliffhangers got the most comments.
  Update SKILL.md arc notes. Store lessons: `npx -y ruflo@latest memory store --namespace oh-meatball --key "week-<date>" --value "<lesson>"`.

## 5b. Update the Control Room page
Edit the `DATA` block in `control-room.html` (updated time, credits, approveUrl = today's combined
approval link, posts with status queued/live/draft, titles, descriptions) and republish it with the
Artifact tool using `url: https://claude.ai/artifact/GPv1McJbRu2M3SKE8oB7ds` (read it first if this
session did not publish it). Nolan uses that page as his one-tap daily screen.

## 6. Wrap up
Commit + push. Message Nolan in <= 6 lines: today's 2 titles, the ONE approval link,
yesterday's views, credits left.
