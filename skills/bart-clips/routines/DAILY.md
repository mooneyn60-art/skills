# Daily clip run

Complete instruction set for the scheduled daily session. Work in
`/home/user/skills` on branch `claude/bart-clips`.

## 0. Sync
`git fetch origin claude/bart-clips && git checkout claude/bart-clips && git pull`.
Read `skills/bart-clips/SKILL.md`. Recall what has worked:
`cd skills/bart-clips/data && npx -y ruflo@latest memory search --namespace bart-clips -q "best titles" 2>/dev/null | grep -v "npm notice" | head -30`
(ruflo is a helper: if it fails, continue without it).

## 1. Check credits
`opusclip_get_usage`. If `remaining_minutes` < 40, do not submit new videos;
tell Nolan credits are low and keep working from clips already made.

## 2. Pick source video
`vidiq_channel_videos` for `UCGRryxFxjXbVAtBPE9EbyMg`, long, popular=false.
Take the newest video not already in `data/posted.csv` (`source_video` column).
Prefer the higher-`vph` one if two are new. Skip videos over 60 minutes
unless credits > 150 (cost is ~1 credit per minute).

## 3. Clip it
`opusclip_submit_project` with that YouTube URL, clipDurationsSec [[15,35]],
portrait, captions on, and the customPrompt:
"Find Joe Bartolozzi's funniest, most shocking or most quotable reactions:
roasts, disbelief, hot takes, dark-humor punchlines. Each clip must start on
the hook and make sense with no context."
Poll `opusclip_list_clips` every ~60s (max 25 min). Then pick the top 3 by
score whose transcript works with no context.

## 4. Title + queue
For each picked clip write a title with the formula in SKILL.md. Description:
`<title> | Full video: youtube.com/@joebartolozzi #joebartolozzi #shorts`.
Schedule with `opusclip_schedule_publish` for today (ET): 12:00, 17:00, 21:00,
on the YouTube account; the same clip to TikTok Story Vault and Instagram
StoryVaults. Record every returned `approval_url` in `data/posted.csv`
(status `awaiting_approval`).

## 5. Update results
`opusclip_list_scheduled_posts` for the last 10 days: set rows to `posted` or
`failed`. For our clips posted 7+ days ago, look up views with
`vidiq_channel_videos` on `UCw98RQD81t_339LX5EJqcrg` (short, popular=false) and
fill `views_7d`. Store a learning for each finished clip:
`npx -y ruflo@latest memory store --namespace bart-clips --key "<clip_id>" --value "<views_7d> views | <title>"`.

## 6. Weekly (Mondays only)
- Top 3 and bottom 3 clips of the week: what do winners share? Update the
  title formula in SKILL.md if the data clearly says so.
- Check https://contentrewards.com/c/discover/clipping for a Joe Bartolozzi
  or matching campaign; report any with budget left.

## 7. Wrap up
Commit and push (`git add skills/bart-clips && git commit -m "bart-clips: daily run <date>" && git push -u origin claude/bart-clips`, retry on network errors).
Message Nolan, max 6 lines: the 3 titles, ONE line with the approval links,
yesterday's views, credits left. If approvals from earlier days are still
pending, remind him once.
