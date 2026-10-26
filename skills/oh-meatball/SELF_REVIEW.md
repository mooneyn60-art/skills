# Self-review (seed)

Every mistake, and the check that now catches it. Copy to skills/oh-meatball/SELF_REVIEW.md.
Seeded by TARS on 2026-10-24 from the first scan of the channel.

- **Format churn.** Story parts, then quiz, then explainer within ~a week, so no format got a fair test.
  Check: the experiment rule in channel-brain/SKILL.md (full pivot only after a lost test on ≥15 videos, or Nolan says so).
- **Experiment log unusable.** E3-E6 each used twice; four rows have dates in the id column; six tests running on Shorts at once.
  Check: scan.py experiment checks; one change per format per week.
- **Stale routine docs.** routines/DAILY.md, NIGHTLY.md and WEEKLY.md still pointed at an old branch and described the retired
  cat soap-opera format (plus a car rule from another project). A run that reads them does the wrong work.
  Check: scan.py doc-drift check; fix or delete those files.
- **Nolan had to call things out.** Check: the scan runs first every run, and the top 3 issues get fixed before production.
- **Posting log drift (10/24).** posted.csv had 35 of 73 queued posts, so queue gaps were invisible (11 YT Shorts and 28 TikTok slots were empty from 10/31 on). Fixed: rebuilt from Metricool, and the gaps were filled from myths-07.
  Check: every post goes into posted.csv in the same step as createScheduledPost; scan.py check_queue flags any gap.
- **Metricool time drift (10/24).** Posts set for 10/24 at 20:00 ET or later saved 2 hours late (probably Europe's DST change; the account was created in Madrid time). Check: read publicationDate back after every create/update; US DST ends 11/1, so verify the times of posts after that date.
- **Invented viewer answers (10/24).** The Explains #2 script had Meatball read out "your answers" (mammoth, dodo) from an episode that hadn't aired yet. The Mayor caught it before it posted and replaced the line with a real ask.
  Check: a read-out beat may only quote comments that exist. The Host desk pulls them with vidiq_video_comments, and the Showrunner fills the beat from that pull, never from imagination. With no comments yet, use an ask instead of a read-out.
- **Scan false alarm from Metricool drift (10/24 evening).** The 10/24 20:00 TikTok showed as a CRITICAL gap because the post saved at 22:00. Fixed: scan.py check_queue now fills a slot with the closest post within 2 h, each post used once.
- **Old live stream still public (10/24 evening).** "Moondog88 Live Stream" (2021) is still public 5 h after the Mayor asked Nolan to hide it. Check: the evening Red Team runs vidiq_user_videos (public) every night and re-raises it to Nolan until it's gone.
- **vidIQ burn went unnoticed (10/24).** Balance fell 1,285 → 838 between 12:28 and the evening (447 credits, mostly Bill voiceovers), and no run posted it. Check: every run posts the vidiq_balance delta since the last run.
- **Queue gaps hidden past 48 h (10/25 morning).** The scan only looked 48 h ahead, so 10 empty YouTube Shorts slots and 10 empty TikTok slots on 10/28-10/31 (left when the old-style Shorts were held as drafts) were invisible, and the 10/25 10:00 TikTok gap was reported as 12:00 because a single greedy pass let the 12:00 post fill the 10:00 slot. Long-forms (ep.mp4 at 14:00) also counted as Shorts. Fixed in scan.py: 7-day horizon (days 3-7 = WARN), exact-time matches first, long-forms excluded.
  Check: scan.py check_queue; every morning run fills the WARN list before rendering anything else.
- **No 60 s+ TikTok on 10/25.** All four 10/25 TikToks were ~22-25 s v3 Shorts, under the Creator Rewards floor. Fixed by moving the tarantula hawk deep dive (62 s) from 11/9 20:00 into the empty 10/25 10:00 slot. Check: posted.csv has no duration column yet, so the postmaster checks each day has one `_len: deep` render before signing off the queue.
- **73 s render in a YouTube Shorts slot (10/25 evening).** The v4-spiders pack rendered bolas at 73.2 s and it was queued at 19:30 on YouTube, where the rule is 20-25 s (43 s+ Shorts got 98-239 views). The scan only checked that slots were filled. Caught 45 min before it posted and set to draft. Check: scan.py check 7 ffprobes every non-long-form post in the next 3 days (YouTube over 35 s, or a TikTok day with no 60 s+ cut = WARN).
- **"Standard" on paper, absent on screen (10/25 evening).** The early ask kit was declared standard, and E18 was logged as running on every new v4 Short, but no queued Short has the guess card or sub pill (only the raven sample and two long-forms). Check: before marking a format change live, grep the queued scripts for its beat fields and count them.

## 10/26: TikToks drifted under 60 s (Nolan: "TikTok was always supposed to be this way")
OPERATIONS said from 10/25 that every TikTok runs over 60 s, because Creator Rewards pays only for 60 s+. Pack 1, the v3/v4 cross-posts and the pilot cases still went out at 20-25 s, and the only check was "at least one 60 s+ TikTok a day". Fix: scan.py now flags any queued TikTok under 60 s as CRITICAL across the whole future queue, and the morning prompt and OPERATIONS say every TikTok is 61-75 s. Lesson: when Nolan states a rule, encode it as a hard check the same day, not a soft daily minimum.
