# 52 · Story engine: openings that stop the scroll, middles that never let go

2026-10-26. Nolan: "we need better openings then lock in and find the perfect one and how to hold attention
through the whole video... the most entertaining videos you can watch that sucks you in."

Evidence: vidIQ outliers (Shorts, last month) and Instagram/TikTok outliers (55 s+, last 30 days) for
conspiracy / declassified / weird history. vidIQ watched these 4 frame by frame:

| Video | Result | Length |
|---|---|---|
| Voggle, "The True Story of Mike the Headless Chicken" (YT Short) | 2.8M views, 347x its channel, 10.1% engagement | 2:53 |
| @realmelanieking, giant-snake rocks (TikTok) | 10M, 114x her median | 2:58 |
| @mrdeepdive, "The Disturbing Prediction That Actually Came True" (TikTok) | 565K, 7x | 2:11 |
| @danocracy, "A Deep Dive Into Area 51, Episode 2" (Instagram) | 1.1M, 301x | 4:27 |

Other outliers in the same scan (not watched): "Everybody thought he's insane until he landed the plane"
(6.9M, 137x, 2:53); "The Chess Robot That Caught Napoleon Cheating" (6.4M, 204x, 0:33); "He put his head in a
particle accelerator and survived" (234K, 103x, 1:04).

## What they all do that we don't

Our case format is a quiz: a claim, two wrong guesses, a verdict stamp. The winners tell **stories**.

1. **A person who wants something.** Lloyd wants money from his headless chicken. The CIA wants a Soviet
   submarine. The manga artist wants to warn people. Our cases have facts but no one to root for.
2. **Stacked loops.** Area 51 opens 6 questions in 4:27, and every time one is answered the next, bigger one is
   already open ("so how do you build a titanium jet when Russia owns the titanium?"). The viewer never reaches
   a natural place to swipe. Our deep cuts open one question and answer it at 50-70%.
3. **Escalating scale.** Mike: survives a minute → the night → a year → $80k a month → famous. Snake rocks:
   one pool → a cave → a mountain → 24 faces in mountain ranges. Each step is bigger than the last.
4. **A false calm, then a drop.** Mike gains weight, everything's great... then he chokes in a motel at
   night and the syringe was left at the sideshow. Peak tension sits at 80-90%, not in the opening.
5. **The opening line is a physical moment or a "this is real" claim.**
   - "The axe cut off the rooster's head..." (a scene, mid-action)
   - "This is real footage of a nuclear bomb going off in the Nevada desert in 1957." (proof up front)
   - "What if I told you that is the eye of a giant snake?" (a challenge to the viewer)
   - "In 1999, a Japanese artist released a strange comic book." (an ordinary thing that turns sinister)
6. **Something changes every 1.2-2.5 s** (cut, zoom, SFX, caption colour, diagram), **and the host or
   narrator comes back every 15-20 s** to reset the mood. We have the cuts (`max_shot` 1.8) but not the host
   resets or the per-beat SFX.
7. **Endings with an engine.** The ending is either an ironic kicker ("...killed his golden goose"), a
   cliffhanger into the next episode ("it wasn't American. We're looking into that tomorrow." plus Follow, framed
   as "so it shows up on your feed"), or a line that splits viewers into two camps who argue in the comments.
8. **Episodes.** "Episode 2" did 301x. A numbered series gives people a reason to follow.
9. **They're long.** Every watched winner runs 2:11-4:27, and the YT Short winner is 2:53. Length isn't
   the problem; empty length is. (YouTube Shorts stay 18-24 s per Nolan until a story Short proves otherwise
   on TikTok first.)

## The format: "Meatball Investigates: Story Cut" (TikTok 75-120 s first)

| Time | Beat | Rule |
|---|---|---|
| 0-3 s | Cold open | A physical moment or a "this is REAL" claim, with the best image and no title card |
| 3-8 s | Meatball's reaction + the stakes | Who is in trouble or who wants what |
| ~10 s | One-tap ask | Emoji guess card (existing kit) |
| 10-30% | Rewind | "See, in 1974..." |
| every 12-18 s | Step up | Each step bigger than the last; every answer opens the next question within 2 lines |
| 15-20 s apart | Host reset | Meatball centred: sweat, lean, "psst" |
| 60-75% | Main payoff | The real answer, with proof (document, photo) |
| 75-90% | False calm → drop | "Everything was fine. Until..." |
| last 5 s | Kicker or cliffhanger | Ironic one-liner, or "Part 2 tomorrow", plus Follow framed as convenience |

Gate: `tools/story.py` (built with the pilot) fails a Story Cut that has no protagonist, goes more than 2 lines
after a resolution before opening a new question, has fewer than 3 escalation steps, has no false calm, or
does not end on a kicker or cliffhanger.

## Lock in the perfect opening: hook lab

Each opening type is a hypothesis. Testing them takes 2 weeks on TikTok, because TikTok pays per qualified
view and shows us watch time per post:

- Same case, 3 openings (A scene, B "real footage" proof, C "what if I told you" challenge), posted on
  different days at the same slot.
- Read 3 s hold and average watch time per post (Metricool TikTok analytics; TikTok Studio from Nolan if
  Metricool lacks it).
- After 4 cases × 3 openings (12 posts), the opening that wins at least 3 of 4 becomes the house opening.
  Then test the next variable (ending: kicker vs cliffhanger), one variable at a time.
- Log results in `data/hook-lab.csv`: `date,case,variant,opening_line,views,avg_watch_s,completion,
  hold_3s,notes`.

## Safety

Story Cuts keep the red list and never present a false conspiracy as true. A "this is real" opening is used
only when the case is verified real (A119, Northwoods, Glomar, MKUltra, Acoustic Kitty); hoaxes and myths
open on a scene instead.
