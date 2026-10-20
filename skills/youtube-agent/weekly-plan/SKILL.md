---
name: weekly-plan
description: Build the 7-day Oh Meatball upload plan (2 Shorts per weekday at 10 AM + 4 PM ET, lighter weekends, 1 compilation per week) with every clip a distinct animal x camera x location x twist. Use on Sundays, when asked for a content calendar, a weekly plan, or "what do we post this week".
---

# Weekly plan

Why this cadence: Metricool best-time data puts YouTube peaks at 4 PM and 10 AM ET on weekdays, weekends at about
half ([research/14](../../oh-meatball/research/14-pivot-satisfying-ai.md)); 1-2 Shorts/day + 1 compilation/week
([algorithm.md §4 Posting frequency](../../oh-meatball/playbook/algorithm.md)).

## Inputs
1. Idea backlog + seasonal calendar: [seo-packaging.md §6](../../oh-meatball/playbook/seo-packaging.md).
2. Outlier briefs from [virality](../virality/SKILL.md) (run it first; 2-3 "our version" slots per week).
3. Last 10 uploads (titles in [data/metrics.csv](../../oh-meatball/data/metrics.csv) / YouTube) and winners from
   [analytics-review](../analytics-review/SKILL.md).
4. Comment-sourced ideas from [reply-drafts](../reply-drafts/SKILL.md).

## Slots (America/New_York)
| Day | 10:00 | 16:00 |
|---|---|---|
| Mon-Fri | Short | Short |
| Sat | Compilation (Short 48-60 s, or long-form from week 3) | Short |
| Sun | Short | (review + plan next week) |

= 12 Shorts + 1 compilation. Put the strongest idea of the day at 16:00.

## Rotation rules (inauthentic-content guard)
Each clip is a tuple **animal x camera x location x twist type**. Inside one week:
- No tuple repeats; no animal more than 3 times; no camera type more than 5 times (doorbell is the anchor, so cap it).
- Never the same animal + same twist as any of the last 10 uploads ([algorithm.md §6](../../oh-meatball/playbook/algorithm.md)).
- At least 4 twist types per week: *returns it*, *backup arrives*, *mistaken identity*, *caught and freezes*,
  *wrong object*, *polite crime*, *unexpected skill (plausible)*, *series callback*.
- Cameras: doorbell_night, security_day, dashcam, phone ([camify presets](../../oh-meatball/tools/README.md)).
- Safety filter on every row: no animal in danger, pain, attack, chase or rescue.
- Doubling down on a winner = new twist with the same animal/character, never a copy.

## Output (markdown table, then a JSON block the other skills read)
```
| Day | Time | Animal | Camera | Location | Twist | Hook # | Source |
| Mon | 10:00 | raccoon | doorbell_night | front porch | returns the package | 2 | backlog #1 |
| Mon | 16:00 | goose | security_day | driveway | steals 2nd shoe on return | 17 | outlier brief B |
...
```
```json
[{"date":"2026-10-26","time":"10:00","animal":"raccoon","camera":"doorbell_night",
  "location":"front porch","twist":"returns the package","hook":2,"source":"backlog #1"}]
```
Save it to `skills/oh-meatball/data/plan-YYYY-WW.json` only if the user asks; otherwise print it.
Each row then flows: [script-prompt](../script-prompt/SKILL.md) -> [produce](../produce/SKILL.md) -> [publish](../publish/SKILL.md).

## Budget check
One 8 s generation per Short (single shot). Before committing to 12, check credits / free backends
(`generate.py` tries free backends first). If short, drop the Sunday Short and Sat 16:00 first.
