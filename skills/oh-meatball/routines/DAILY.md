# Oh Meatball: daily run (complete instruction set)

Work in /home/user/skills on branch `claude/off-the-lot`, folder `skills/oh-meatball`.
Read SKILL.md first (cast descriptions, arc, format). Never mention cars.

## 0. Sync + budget
- `git fetch origin claude/off-the-lot && git checkout claude/off-the-lot && git pull`.
- `vidiq_balance`. Shots use veo-3.1-lite (80 credits / 8 s). Budget rule:
  keep >= 400 credits in reserve; if below, make 1 part instead of 2 and tell Nolan.
- Read `data/log.csv` for the last part number and what was scheduled.

## 1. Learn from yesterday (2 min)
- `vidiq_channel_videos` on the channel (short, popular=false): views on each part.
- `vidiq_video_comments` on the newest part: what are people arguing about? Who do they side with?
  Use the strongest comment theme in today's plot (that's the engagement loop).

## 2. Write 2 new parts
- Continue the arc in SKILL.md; each part = 2 shots x 8 s, ends on a cliffhanger.
- Write `episodes/NN.json`: {part, shot1_prompt, shot2_prompt, dialogue lines, title, description}.
- Every prompt repeats the cast descriptions word-for-word + the style line.
- Titles: draft 3, `vidiq_score_title` (type short), keep the best >= 85, format `<hook> | Oh Meatball Pt N`.

## 3. Make
- Submit all 4 shots in parallel (`vidiq_generate_video`, model veo-3.1-lite, 720p, 8 s, 9:16).
- Poll `vidiq_job_poll`. Download, check 3 frames per shot, transcribe dialogue with faster-whisper
  (decode audio via ffmpeg to float32 first). If a character looks wrong or a line is garbled,
  regenerate that ONE shot with a corrected prompt (max 1 retry per shot).
- `vidiq_compose` each part (keepNativeAudio) with overlays "PART N" (0-2 s) and
  "PART N+1 TOMORROW" (last 1.7 s). Keep the returned URL.

## 4. Post (YouTube + TikTok + Instagram)
- PREFERRED (no human tap): if env UPLOAD_POST_API_KEY is set, download each composed MP4 and run
  `scripts/post.sh <mp4> "<title>" "<description>" youtube instagram` (add `tiktok` once on a paid plan).
  Free plan = 10 uploads/month: spend them on YouTube first. Check the JSON response for success and
  log the returned post ids. Instagram can also go through `vidiq_instagram_publish_reel` if Instagram
  is connected in vidIQ (publishingAvailable=true).
- FALLBACK (needs Nolan's one tap):
- `opusclip_submit_project` with the composed URL, skipSlicing true, enableCaption false.
- When ready, `opusclip_schedule_publish` each part to:
  YouTube 69dbd6d3074f7631e21a2343, TikTok 69dbd6fe074f7631e21a2350,
  Instagram 69ee71f1da7dbfe118f6e80e (subAccountId 17841429829712746).
  Times (ET): part A 12:00, part B 18:00. Same title; TikTok/IG caption = description.
- Combine ALL approval tokens into ONE link: https://clip.opus.pro/agent-approvals#<t1>,<t2>,...
- Append rows to `data/log.csv`: date, part, title, shots, credits, opus project, tokens.

## 5. Weekly (Sundays)
- Build "Season 1 so far" long-form compilation (all parts back-to-back, 16:9 letterboxed or 9:16)
  with ffmpeg; send to Nolan for upload as a regular video (watch hours for monetization).
- Score the week: views per part, subs gained, which cliffhangers got the most comments.
  Update SKILL.md arc notes. Store lessons: `npx -y ruflo@latest memory store --namespace oh-meatball --key "week-<date>" --value "<lesson>"`.

## 6. Wrap up
Commit + push. Message Nolan in <= 6 lines: today's 2 titles, the ONE approval link,
yesterday's views, credits left.
