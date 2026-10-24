# 34 — vidIQ playbook (Mayor, 2026-10-24)

Nolan bought vidIQ for the month: **2,000 credits, resetting 2026-11-24**. Most calls cost 5 credits;
comment-reply drafts cost 1. Budget: about 45 credits a day, plus 500 held in reserve for follow-ups on a hit.

## What the first pull showed (10/24)
- **Traffic, 10/19-10/24:**
  - Shorts feed: 4,547 views, 1,797 engaged (40%), average view 130%, so the loops work.
  - YouTube search: 98 views. Channel page: 42.
- YouTube Analytics lags 2-3 days, so per-video numbers for the new quiz Shorts aren't in yet.
- **Shorts that broke out on small channels this month (outliers, under 200k subs):**

  | Short | Views | Channel size |
  |---|---|---|
  | "Never Play Dead with Bears" | 682K | 1.7K subs |
  | "Right Way to Escape Elephants" | 268K | 1.7K subs |
  | "Big lie tiger never climbed tree" | 2.2M | 8.6K subs |
  | "Bull Shark vs Great White — You've Been Getting This Wrong" | 595K | 97K subs |
  | "The Biggest Camel Myth Busted!" | 413K | 156K subs |
  | "Whose Tail Is It? Guess the Animal!" | 8.8M | 45K subs |

  These confirm research/28: danger-to-you myths and "you've been getting this wrong" framing win, and so do guess-the-animal quizzes.
- **Searched animal questions with low competition** (monthly searches / competition, 0-100, lower is easier). These are "Meatball Explains" and search-first episode topics:

  | Question | Searches/mo | Competition | Note |
  |---|---|---|---|
  | why humans live so much longer than most wild animals | 176K | 28 | |
  | why do wild animals follow humans for miles without attacking? | 77K | 30 | |
  | why evolution keeps turning animals into cats | 76K | 39 | |
  | do animals know they're pets? | 44K | 41 | growth +732% |
  | why can humans eat almost anything while most animals can't? | 36K | 33 | |
  | do animals understand death? | 26K | 29 | |
  | why cave animals lose their eyes | 17K | 7 | |
  | why islands turn animals into giants | 17K | 26 | growth +322% |
  | why don't animals try to eat humans? | 14K | 26 | |
  | why do wild animals sometimes seek human help? | 14K | 11 | |
- **Title scores:**

  | Episode | Old title | Score | New title | Score |
  |---|---|---|---|---|
  | 4 | "12 Animal Myths That Could Actually Get You Hurt" | 91 | "Playing Dead Can Get You Killed (12 Animal Myths That Can Hurt You)" | 96 |
  | 6 | "12 Cat & Dog Myths You STILL Believe" | 84 | "12 Things You Believe About Your Cat and Dog (Most Are Wrong)" | 96 |

  Both titles were updated in Metricool. Rejected: "Never Play Dead With This Bear" scored 98, but it is wrong for the brown bear in the thumbnail, so it failed the fact check.

## Daily use (built into the routines)
| When | Who | Call | Credits |
|---|---|---|---|
| Morning | Writer | `vidiq_score_title` on 3 candidate titles per new episode; keep the best one that is accurate | 15 |
| Morning | Hitmaker | `vidiq_outliers` (Shorts, "animal myths/facts", max 200k subs) **or** `vidiq_keyword_research` questions, alternating | 5 |
| Evening | Analyst | `vidiq_channel_analytics`: `top_videos` (engagedViews, averageViewPercentage, subscribersGained) and `traffic_sources` | 10 |
| Evening | Host | `vidiq_video_comments` (channel, newest), then `vidiq_generate_comment_replies` for the best 3 | 8 |
| Sunday | Scout + Historian | `vidiq_keyword_research` rising (niche) + `vidiq_outliers` long-form + `vidiq_channel_analytics` audience_retention on the week's best episode | 20 |

## Rules
- Accuracy beats score. Never use a title that misstates the video's answer.
- Hold 500 credits for the follow-up rule: when a Short hits 3x the median, run retention, comments and title tests on it.
- Check `vidiq_balance` at the start of each run. Below 300, keep only the evening analytics.

## Revised caps (CMO, 10/24 12:17)
The first research wave spent about 530 credits in one day, leaving 1,468 until 11/24 (about 47 a day).
- **Per-run caps:** morning 20, marketing desk 30, evening 15, night shift 25, Sunday summit 60.
- **Approval:** no parallel research waves without the CMO's approval.
- **Thumbnails:** vidIQ refuses GitHub raw URLs. Score thumbnails by sending the image inline at about 192 px (research/37).
