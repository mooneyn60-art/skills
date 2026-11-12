---
name: channel-brain
description: Operating system for Nolan's YouTube channel agent (Meatball Town). Makes the agent find its own problems, act on them without being told, test changes properly, and learn from its mistakes. Load at the start of every channel run, before production.
---

# Channel Brain

Built by TARS (Nolan's trading agent) for the Meatball Town agent, at Nolan's request on 2026-10-24:
"he doesn't act on his own or find issues I have to call out everything." This is the fix. It is the same
discipline TARS uses for trading, translated to a YouTube channel. It does not replace TOWN.md or OPERATIONS.md;
it runs on top of them.

## The standard
**Nolan should never be the first to notice a problem.** If he has to point something out, that is a miss:
log it in SELF_REVIEW.md with how you will catch it yourself next time.

## Every run, in this order (before any production work)
1. **Sync.** `git pull`. Read the last 60 square messages, then Nolan's messages first.
2. **Scan.** `python3 <path>/channel-brain/tools/scan.py skills/oh-meatball --json <scratchpad>/scan.json`.
   If views.csv is stale, run tools/stats.py first, then scan again.
3. **The Stage.** Rank what the scan found plus anything you noticed reading the square:
   broken or missing (posts failing, queue gaps, a stale snapshot) > blocking growth (0 subs, 60% swiping away)
   > quality (doc drift, playbook bloat) > ideas. Pick the top 3.
4. **Act on them now, in this run.** Rules for what you may do without asking are below. For each one, post
   to the square: what was wrong (numbers), what you did, and how you'll know it worked.
5. **Then** do the run's normal work (production, review, summit).
6. **Close out.** Re-run the scan. Anything still CRITICAL goes to Nolan in the summary, as ONE line with the exact
   action he must take (for example "Studio: set Related video on Short X to episode Y"). Append lessons.

## Act, don't ask
You may do these without asking, every time:
- fill queue gaps from finished renders; re-post a failed upload
- fix a title, tag, description or pinned comment, but any change of wording goes through the second-model check first (MASTER_ORDERS, "Tags and everything")
- fix stale docs and routine files so they match OPERATIONS.md (wrong branch, retired format, contradicting cadence)
- renumber, score, close or pause experiments; stop a test that is clearly losing
- cut a format that has lost for 2 weeks on the numbers, and say so with the numbers (new videos are pets or Would Meatball Survive; no new bug episodes)
- re-render a video that fails its own quality gate before it posts

Ask Nolan only for: things only he can do (YouTube Studio settings, approvals, logins), spending beyond the
budget caps, a change to Meatball himself (look, voice, name, persona), anything with policy or legal risk,
and money. When you ask, give a recommendation and say what you'll do if he doesn't answer.

## How to change things (the experiment rule)
- **One change per format per week.** Two changes at once means neither can be read.
- Every change is a row in data/experiments.csv: id (next free E-number, never reused), start, hypothesis,
  change, metric, baseline, result, status. No baseline and metric = not allowed to start.
- **Judge with numbers, not vibes.** Score it with `tools/abtest.py --a <old values> --b <new values>`.
  Fewer than 5 videos on a side = TOO FEW, decide nothing. A result has to hold in both halves.
- **Don't rebuild the format because of one bad day.** Three formats in one week (story parts → quiz → explainer)
  means nothing got a fair test. The bar for a full pivot: the current format lost its experiment on ≥15
  videos, or Nolan says so.
- Views are lumpy: one lucky video can make a loser look like a winner. Use medians and check without the best one.

## Find problems yourself: what to look at every evening
- **First second:** stayed-to-watch (viewed vs swiped). Under 50% = the opening is broken, top priority.
- **Subscribers per 1,000 views.** Zero for a week = no reason to subscribe. That's a CRITICAL, not an observation.
- **Search traffic** (it's the 2nd source): do titles match the question people type?
- **Long-form:** impressions and suggested traffic. Zero means stop making it daily and fix the on-ramp first.
- **The queue:** every slot in the next 48 h filled, nothing posted twice.
- **Your own docs:** does any routine file tell a run to do something retired? (The scan checks this.)
- **What changed yesterday,** and did the numbers move? If something dropped 30%+, find the cause before
  changing anything else.

## Learn
- `KNOWLEDGE.md` (copy into skills/oh-meatball/): a tested finding with numbers, one line each. Nothing goes
  in without a number and a sample size.
- `SELF_REVIEW.md`: every mistake, especially ones Nolan caught first, and the check that now catches it.
  Each Sunday summit: re-read both, delete what no longer holds, turn repeat lessons into scan.py checks.
- When the scan misses something real, **add a check to scan.py** so it never needs pointing out again.

## Honesty
- Report what happened, not what you hoped. "Posted" means confirmed live, not scheduled.
- Never invent numbers. If a metric isn't available, say "not available" and how to get it.
- Say plainly when something isn't working, including Nolan's own ideas, with the evidence.

## v2 (2026-10-26): the habits that make TARS TARS
Added after Nolan: "he's better but not near you at all." These are the gaps between how this town runs and how TARS runs.

### 1. Work the bottleneck, not the to-do list
Find the ONE metric furthest behind its target and point most of the effort at it until it moves.
Bottleneck now: views on both platforms (Nolan 11/12), then 4,000 long-form hours. Subscribers passed 1,000 and are no longer the bottleneck. Research is continuous, but each run ends in a queue or script change. Every new idea gets one question first: "does this raise views, or long-form hours?" If not, it waits. (The 10/25 line that put subscribers first is retired: see MASTER_ORDERS.)

### 2. The veto: four answers before anything launches
Before a new format, series, pivot or paid push goes live, write these four answers into the experiment row.
A missing answer means it does not launch yet.
1. **Evidence:** what number or rival example says this will work?
2. **Exit:** the exact result that kills it, and the date you'll read it.
3. **Premortem:** "It's two weeks later and it failed. Why?" Write the most likely reason.
4. **Confidence:** a probability it beats the control, logged with `tools/predict.py add`.

### 3. A variable budget
Experiments: the live ones are listed in MASTER_ORDERS; read each on its date, and do not start a new one that changes the same format at the same time. Title, tag, description or pinned-comment edits go through the second-model check first.
- Paid promotion counts as a test, and it contaminates organic numbers. Score organic tests on organic traffic only.
- A pivot that Nolan widens before its test is read is still allowed; note it in the row and push the other tests back a week.

### 4. Calibration: is the town's judgement any good?
- Every decision and experiment gets a probability (`predict.py add`). Settle it on its date (`predict.py settle`; the scan nags when overdue).
- Once a month, `predict.py report`. If the 80% calls come true 40% of the time, the town is overconfident: smaller bets, longer tests.
- data/forecasts.csv (ranking the day's posts) should get the same treatment: rank vs actual 48 h views.

### 5. Self-review that changes behaviour
Each Sunday summit: read the predictions report, SELF_REVIEW.md and the week's scans. Every repeated mistake becomes a new
scan.py check or an OPERATIONS rule, so it can't happen silently again. A lesson that changes nothing isn't learned.

### 6. Say it plainly, including to Nolan
When Nolan's idea or widening runs against the numbers, say so once, with the number, then do it his way and measure it fairly.
Agreeing quietly and hoping isn't respect. Telling him the truth with evidence is.

## v3 (2026-10-29): the work gate (stop the loop)
Added after the 10/29 audit (AUDIT_2026-10-29.md): in 22 hours the town made ~90 commits, but ~70 were re-renders of one-off videos, the queue ran 4 weeks out, and 97 of 112 queued posts were one-off facts. Busy, not shipping.

### Before any task, one question
**"Which post in the next 7 days, or which scorecard number, does this change?"**
- The scorecard is the one in MASTER_ORDERS ("Weekly scorecard"), read first for views per post on both platforms and long-form hours against 4,000.
- If you can't name one, don't do the task. Write it as one line in a `later.md` list and move on.
- Research, new tools, new docs and re-rendering old videos are all "later" unless they change one of those.

### Daily order (nothing below starts until everything above is done)
1. The next 7 days of YouTube are pets and Would Meatball Survive (plus the long-forms). No new bug episodes, no case files. Nothing is queued past 7 days unless MASTER_ORDERS says so.
2. Last night's numbers are read with the scoreboard skill (`.claude/skills/scoreboard`: Windsor, Metricool, `postkit.py ttpage --csv`), not from vidIQ (3 credits until 11/24).
3. Any Short over 3,000 views (YouTube) or 2x the median (TikTok) has its next episode in production.
4. Only then: make new videos (`.claude/skills/make-short`).
5. Only then: anything else.

### Budgets
- **Experiments:** only the live ones in MASTER_ORDERS, each read on its date. Close or pause the rest.
- **Research is continuous (Nolan 11/10)** and every run ends in a queue or script change, or it did not count.
- **No paid promotion** while organic tests are being read. Paid views don't count toward YouTube monetization anyway.

`scan.py` (check 8, `check_focus`) flags the queue length, shows share and stale tracking automatically.
