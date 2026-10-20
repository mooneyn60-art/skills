# YouTube agent skills — Oh Meatball

11 skills for running **Oh Meatball** ([UCw98RQD81t_339LX5EJqcrg](https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg)):
realistic AI "caught on camera" animal Shorts (doorbell / security / dashcam / phone look, 8-12 s, plot-twist titles).
First A/B: realistic raccoon doorbell cam 904 views vs obvious-AI beaver 2. **It drafts, you decide.**
Policy, algorithm and keyword sources live in [../oh-meatball/playbook/](../oh-meatball/playbook/); these skills link to them.

| # | Skill | Does |
|---|---|---|
| 1 | [hooks](hooks/SKILL.md) | 21 first-second hook formulas (visual + <=6-word text) |
| 2 | [titles-thumbnail-text](titles-thumbnail-text/SKILL.md) | 10 scored titles + 5 thumbnail texts, Shorts vs long-form |
| 3 | [reply-drafts](reply-drafts/SKILL.md) | comment replies, incl. "it's fake/AI" -> engagement, never "it's real" |
| 4 | [weekly-plan](weekly-plan/SKILL.md) | 7-day plan, 2 Shorts/weekday 10 AM + 4 PM ET, rotation rules |
| 5 | [virality](virality/SKILL.md) | `scripts/outliers.py`: niche videos beating their channel median -> "our version" briefs |
| 6 | [tags-seo](tags-seo/SKILL.md) | tags <=480 chars, 3-5 hashtags, description, AI disclosure on |
| 7 | [script-prompt](script-prompt/SKILL.md) | idea -> realistic video-gen prompt + safety gate |
| 8 | [produce](produce/SKILL.md) | generate.py -> camify.sh -> meta.py -> thumbnail.py |
| 9 | [publish](publish/SKILL.md) | Metricool createScheduledPost (short, tags, isAiGeneratedContent) + raw GitHub media URL |
| 10 | [analytics-review](analytics-review/SKILL.md) | 48 h / 7 d review, metrics.csv, decision rules, day-30 criteria |
| 11 | [compilation](compilation/SKILL.md) | weekly 48-60 s Short + 8-12 min long-form with countdown and chapters |

## Daily flow
```
morning   analytics-review (48 h rows for clips from 2 days ago)  ->  reply-drafts on yesterday's comments
          today's 2 plan rows from weekly-plan
          script-prompt -> hooks -> produce -> titles-thumbnail-text -> tags-seo
          publish (10:00 + 16:00 ET)  ->  human approves title + slot
first hour after each post: reply-drafts
Saturday  compilation      Sunday  virality -> weekly-plan (next week) + 7 d analytics-review
```
