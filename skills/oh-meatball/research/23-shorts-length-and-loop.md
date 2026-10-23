# 23 — Shorts length and the loop (2026-10-23)

## Data
vidIQ outliers, English Shorts from the last month, keyword "animal facts myths true or false", 50 results.
Rival Shorts scraped with yt-dlp are too few (most rivals have no Shorts tab, and YouTube bot-blocks the scraper).

On-topic single-myth or single-fact breakouts:

| Short | Length | Views | vs. its channel |
|---|---|---|---|
| Why an Empty Turtle Shell Isn't What you Think | 17 s | 5.2M | 106x |
| Big lie tiger never climbed on tree | 23 s | 2.2M | 64x |
| Why Is It Difficult To Put Fish Into the Tank | 22 s | 626k | 20x |
| Do Old Lions Really Dig Their Own Graves? | 30 s | 108k | 61x |
| The Moose is the massive titan of the deer world | 20 s | 194k | 62x |
| Animals that may go extinct in 2050 | 22 s | 1.8M | 186x |
| The secret to a cat's lightning reflexes | 35 s | 1.8M | 67x |
| Bull Shark vs Great White — You've Been Getting This Wrong | 39 s | 585k | 11x |

The outliers that run 1-3 minutes are compilations ("Animal Facts So Insane...", "Can You Guess These 10 Animals").
Title pattern: contradiction or a promise of a twist ("Big lie", "Isn't What You Think", "You've Been Getting This Wrong").

## Rules (built 10/23)
- A Short is one myth in about 17-23 s: claim first, a 1.5 s countdown, the reveal, the punchline card, then a loop line.
  This is `episode.loop` + `tighten(mb, 2)`.
- Seamless loop:
  - The last beat sits on the same quiz card as the first frame (still frame, no pop-in), and the music has no fade-in.
  - The voice ends "So be honest. Did you really think", which runs into the opening
    "<claim>. True or false?".
  - Measured mean pixel difference between the last and first frames: 2/255.
- Measure: average % viewed (a value over 100% means people loop) and stayed-to-watch, against the earlier 25-30 s Shorts.

## Still to test
- Contradiction titles in place of "TRUE or FALSE: X? 🤔" for half of the Shorts.
