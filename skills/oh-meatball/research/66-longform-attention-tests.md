# 66 · Long-form attention tests (2026-11-05)

Nolan, 11/5: "we need to test long form more to hold more attention." The Shorts got better because each change was
measured at 48 h, and the next video fixed the weakest moment. This page does the same for long-form.
It builds on research 65 (one show, one slot, one bridge) and MASTER_ORDERS (Watch hours).

## What we measure (Studio, per long-form, at 48 h and 7 days)
1. **% still watching at 30 s** (Studio "Intro"): target 60%+. This is the hook.
2. **Average % viewed** and **average view duration**: target 35%+ for a 5-min video. This is the hold.
3. **The retention curve's dips**: the timestamps where it drops faster than the line around it. Each dip is one fix for the next script.
4. Impressions, CTR, and traffic from Related video (the distribution check from research 65).
Log them in `data/retention.csv` with the video, date, the four numbers and the top 2 dips (time + what was on screen/said).
From 11/24 the vidIQ credits reset (2,000). `vidiq_channel_analytics report=audience_retention filters=video==ID` then pulls
the curve directly (5 credits a video), so the dips no longer need screenshots.

## The test ladder (one variable per week; YouTube can't A/B the video itself, so we test episode against episode)
| Week | Long-form | Variable tested | Compared with |
|---|---|---|---|
| Thu 11/5 | Azorian v3 (8:38, case file) | lane: history vs house | Kill-or-Keep |
| Sat 11/7 | Kill-or-Keep v2 (4:33) | format: ranked list with a board | Night Shift |
| Sat 11/14 | Night Shift (~5:30) | format: one story spine (a night, hour by hour) + Meatball gags | Kill-or-Keep |
| Sat 11/21 | winner format, new topic | Meatball gag density (one per chapter vs one per 30 s) | the winner |
| Sat 11/28 | winner format | length: ~5 min vs ~8 min (watch hours) | the winner |
Every upload also runs Test & Compare on 3 titles (or 2-3 thumbnails). It's free and tests packaging, not the video.

## Rules that already come from the Shorts data (apply to every script, no test needed)
- Voice at 0.0 s on the creature; the title's promise is paid off in 5 s; no intro, joke or ask before 0:25.
- No subscribe/like/comment asks mid-video (cliffs on the Shorts at every "Subscribe"); the guess poll lives in the pinned comment.
- A new picture every ~1.5-2.5 s (Azorian 1.4 s avg, Kill-or-Keep 1.9 s: already fine) and a new peak every 20-30 s.
- Never name-and-list: the line after a creature's name is action or danger, not anatomy or dates (the 4-6.5 s cliff on Shorts).
- Boring stretches (dates, budgets, timelines) are told as stakes, or cut.

## Decision rules
- A format wins if it beats the other on % viewed by 5+ points with similar CTR. Keep it for 4 weeks (MASTER_ORDERS: don't switch a working format).
- Case files return monthly only if Azorian beats both house long-forms on views and subs per 1K at 7 days.
- Go to 2 long-forms a week (Wed + Sat) when one passes 500 views or shows Related-video traffic (MASTER_ORDERS).

## Blockers
- Rendering: edge-tts (Andrew voice) can't connect from the cloud session (the proxy blocks WebSocket). New scripts render on
  Nolan's machine / TARS's environment. Re-cuts of finished videos (like Kill-or-Keep v2 and Azorian v3) can be done here.
- Studio numbers: until 11/24, Nolan pastes the 48 h screens (Intro %, % viewed, retention curve).
