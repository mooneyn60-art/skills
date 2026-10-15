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
7-day test (2026-10-15 to 10-22): ONE clip per day on YouTube at 17:00 ET,
queued 3 days ahead so there is never a gap. After the test, if median
engaged views beat 1,654, scale to 2/day and add TikTok Story Vault.
Schedule with `opusclip_schedule_publish`. Record every returned `approval_token` in `data/posted.csv`
(status `awaiting_approval`). Combine all of the day's tokens into ONE link
for Nolan: `https://clip.opus.pro/agent-approvals#<token>,<token>,...`.
On days with no new Joe video, use the next-best unposted clip (<=25 s) from
the latest project, so there is never a gap day.

## 5. Update results
`opusclip_list_scheduled_posts` for the last 10 days: set rows to `posted` or
`failed`. For our clips posted 7+ days ago, look up views with
`vidiq_channel_videos` on `UCw98RQD81t_339LX5EJqcrg` (short, popular=false) and
fill `views_7d`. Store a learning for each finished clip:
`npx -y ruflo@latest memory store --namespace bart-clips --key "<clip_id>" --value "<views_7d> views | <title>"`.

## 6. Weekly self-review (Mondays only)
- Score the week: median engaged views per clip vs the baseline (1,654 views
  median of the last 50 before 2026-10-15). Top 3 and bottom 3: what do
  winners share (title format A/B/C, length, moment type)?
- Store one line per finding: `npx -y ruflo@latest memory store --namespace bart-clips --key "week-<date>" --value "<finding>"`.
- Change SKILL.md packaging ONLY when at least 3 clips support the change;
  write the evidence next to the rule. Note what was tried and dropped.
- Write `research/weekly/<date>.md` (10 lines max) and include its 3-line
  summary in Nolan's message.
- Check https://contentrewards.com/c/discover/clipping for a Joe Bartolozzi
  or matching campaign; report any with budget left.

## 7. Wrap up
Commit and push (`git add skills/bart-clips && git commit -m "bart-clips: daily run <date>" && git push -u origin claude/bart-clips`, retry on network errors).
Message Nolan, max 6 lines: the 3 titles, ONE line with the approval links,
yesterday's views, credits left. If approvals from earlier days are still
pending, remind him once.
