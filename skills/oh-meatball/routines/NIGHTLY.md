# Oh Meatball: nightly check (22:23 ET)

Work in /home/user/skills, branch claude/off-the-lot (git pull first). Read OPERATIONS.md.
Quiet run: only message Nolan if something failed or a video is breaking out.

1. Posts: `opusclip_list_scheduled_posts` for the last 48 h. Any `failed` -> note failure_reason,
   fix (resubmit or reschedule), and add the new approval token to the Control Room.
   Any duplicate of the same part on one platform -> list it for Nolan to delete (do not delete).
2. Stats: `vidiq_channel_videos` (short) for the YouTube channel; `vidiq_video_stats` on each part
   that is 24 h or 72 h old. Append rows to data/metrics.csv:
   date,platform,part,video_id,age_h,views,viewed_vs_swiped,avg_pct_viewed,likes,comments,shares,subs_gained
   (leave a cell blank if the tool does not return it; never invent numbers).
3. Comments: `vidiq_video_comments` on the newest 2 parts. Write the 3 strongest viewer theories /
   sides into story/comment_ideas.md (dated). The next DAILY run uses them in the plot.
4. Breakout check: if any video is >= 3x the channel median views at 24 h, PushNotification Nolan
   one line and add a "make the next part early" note to the top of story/comment_ideas.md.
5. Control Room: update DATA.kpis (subs, total views, best video, credits) and post statuses
   (queued -> live with the post_url); republish the Artifact
   https://claude.ai/artifact/GPv1McJbRu2M3SKE8oB7ds (same file path).
6. Commit + push.
