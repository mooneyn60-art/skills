# The Host playbook

Desk id: `host`. Absorbs: Community. Read this before every run and append lessons after.

## Read first
- research/39 voice of Meatball
- vidiq_video_comments, vidiq_generate_comment_replies

## Rules (proven)
- Reply as Meatball: short, friendly, no links. We cannot post replies ourselves, so drafts go to the square for Nolan.
- Pin the score check on every episode; answer "is this AI?" honestly.
- Evening run: draft replies to the first 10 comments on each new post (in Meatball's voice, answering their guess/vote); Nolan approves the exact text before anything is posted.
- Send the best viewer myths and questions to the Showrunner as episode ideas (e.g. California zebras, bobcat vs lynx).
- **Evening run, Host-desk step: the case docket (Nolan approved research/50 idea 3, 10/26).**
  1. Pull `vidiq_video_comments` for the channel (UCw98RQD81t_339LX5EJqcrg, order "time", maxResult 50; 5 credits) and save the response as JSON (scratchpad, never committed).
  2. Run `python3 tools/submissions.py PULL.json --rejected`: it keeps viewer case suggestions, drops red-list ones, ranks by likes and merges into data/submissions.csv. Commit the CSV.
  3. Post the top safe submission to the Showrunner on the square for Viewer Case Friday. If it's Monday, draft the permission reply to its submitter ("Meatball wants to investigate this on Friday. OK to show your handle on screen? Reply yes.") for Nolan to approve; set `permission` from their answer (yes / no). No answer means no handle.
  4. Check every case/verdict post from the last day has the pinned submission invite (OPERATIONS "You Submit").

## KPIs this desk owns
- Reply drafts used
- Viewer ideas produced

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
- 2026-10-24 (evening): channel pull (30 newest) had 4 viewer comments, 11 of ours. One real answer (owl: 'True 🎉🎉', which is wrong) logged in research/comment-readouts.md. Wrote replies myself instead of vidiq_generate_comment_replies to save credits.
- 2026-10-25 (evening): pull (30 newest, 5 credits) had only 2 new viewer comments, both on posts with a direct question (cassowary "Noooo" to the pinned kicking-distance question; Karolina's follow-up on daddy longlegs). 0 answers on the 6 ask-kit/one-tap posts aged under 9 h, and 0 on the extinct long-form. Only 2 reply drafts were possible; never pad with replies to our own comments.
- 2026-10-25 (Sunday Summit): new job for the pivot: tag every comment that quotes a line or names a gag (the Showrunner cuts gags nobody quotes in 10 Shorts), and collect real 'real or fake?' guesses for a Saturday case read-out. Real comments only.
- 2026-10-26: new docket job (step above). First pull (channel, 50 newest threads, 5 credits) had 0 case submissions: only 6 viewer comments, all guesses or chat. The invite starts on the Verdict and case posts from 10/28; read the pass bar after 5 posts (10+ submissions, 3x comments per 1k).
