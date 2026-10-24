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
- fill queue gaps from finished renders; re-post a failed upload; fix a title, tag, description or pinned comment
- fix stale docs and routine files so they match OPERATIONS.md (wrong branch, retired format, contradicting cadence)
- renumber, score, close or pause experiments; stop a test that is clearly losing
- cut a format that has lost for 2 weeks on the numbers, and say so with the numbers
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
