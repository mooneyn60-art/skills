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
