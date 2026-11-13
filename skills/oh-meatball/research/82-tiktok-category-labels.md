# 82 · TikTok files our drawn videos under "Comics & Cartoon, Anime" (2026-11-11, 6 PM)

Read-only. Source: the public page of 31 of our own TikToks, fetched 2026-11-11 about 18:05 ET (one plain request each, no login). Each page carries the video's live counts and a field called `diversificationLabels`, which is TikTok's own category for the video. TikTok does not document the field, so what it does to distribution is my inference, not a stated rule. Rows: `research/data/82-tiktok-labels.csv`. The episode type comes from `data/posted.csv`, matched by posting time.

## What the pages show
| TikTok's label | Videos | Median views | Range |
|---|---|---|---|
| Animals / Nature | 7 | 672 | 209 to 5,983 |
| Humanities / Education | 3 | 510 | 229 to 3,791 |
| Comics & Cartoon, Anime / Anime & Comics / Entertainment | 20 (plus today's post) | 340 | 86 to 2,219 |

- Animals and Education together: 10 videos, median 615. That is about 1.8 times the cartoon-labelled median of 340.
- The two biggest posts on the account are not cartoon-labelled: bombardier beetle 5,983 (Animals) and the first house centipede 3,791 (Education).
- By our own video type: the real-photo Shorts (`tiktok-pack-01`, the TRUE or FALSE posts, `v3-01`) are labelled Animals or Education in 8 of 9 cases. The drawn videos (`drawn-house`, `drawn-tt`, 3D, tier list, case files) are labelled Comics & Cartoon, Anime in 19 of 20; the one exception is the first house centipede.
- Every video sampled from 10/28 on, when the drawn look became the only look, carries the cartoon label.

## What it may mean
Nolan (11/11): "We're getting a lot of views on TikTok from search but not fyp." Search finds a video by its words, so a bug caption still reaches people who typed "house centipede". For You tests a video on people whose interests match its category. If TikTok thinks our videos are anime and cartoons, the test audience is cartoon viewers, not people who care about bugs. That would explain search views without For You growth. It is a lead, not proof.

## Why it is not proof
- 31 videos, and not a random sample: I took the top posts first and then a spread. A random sample could shrink the gap.
- Style, topic and date move together. The photo videos are from 10/23 to 10/27 and are mostly exotic animals; the drawn ones are later and mostly house bugs.
- The label may partly follow the audience that watched, not only the picture.
- The best cartoon-labelled posts still reached 718 to 2,219 (house centipede, mouse, velvet ant), so the label is not a ceiling.

## The joke cut at 6.5 hours
"Wolf Spider, Stink Bug, Earwig: Stay or Squish?" (posted 11:32 ET): 19 views, 1 like, 0 comments, 0 shares. Its review and penalty fields are identical to yesterday's three normal posts (not reviewing, not prohibited, no warning, indexed), so nothing on the page says TikTok is holding it back. Yesterday's posts at 25 to 30 hours: 140, 256 and 618. No same-age number exists for a normal post, so 19 is slow but not a verdict. Metricool had no row for it yet.

## Options (Nolan decides; the look is locked, so this needs his yes)
1. Real photos in the TikTok cuts only: open on a real photo of the bug for the first 2 seconds and pin 3 or 4 more through the minute (the old case-file mix did this), then read the label and the views on the next two cuts. YouTube stays as it is.
2. Words only: add #insects #animals #nature to the captions of the next six TikToks and read their labels. Cheap, no look change, weaker.
3. Leave it and judge the joke cuts first.
My pick: 1 and 2 together on two cuts, because the label is readable within an hour of posting, so the test answers itself fast.

## Could not be measured
- How TikTok assigns the label, and how much weight it has in For You.
- For You against Search views per video (TikTok Studio only).
- Whether the swearing changes anything: the joke cut has the same label and the same status fields as the clean posts.

## Thu 11/12 evening: the first search-led funnier cut (dog guilty look, posted 19:02 ET)

Source: the video's public page read with `tools/postkit.py ttpage` at 21:27 and 21:31 ET, and the account listing through yt-dlp.

- Label: still "Comics & Cartoon, Anime", not Pets or Animals. A drawn dog is filed as a cartoon.
- Plays 115, likes 5 (4.35%), comments 0, shares 0 at 2.4 hours. The first sweary cut had 19 views at 6.5 hours and 48 at 8.6 hours, so this one started about ten times faster. The account's median is about 229 at a day old (research 91).
- TikTok's own suggested searches on it include "guilty dogs" and "dog body language". So TikTok has matched it to the phrase people type.
- Odd: the noon pantry-moth TikTok shows the same counts (115 plays, 5 likes) on two reads and in the listing. It had 11 plays at 5 hours. Either a coincidence or a stale public counter; read both again in the morning.
- Windsor still has only the YouTube account (get_connectors, 11/12 21:32 ET), so no TikTok watch time.
