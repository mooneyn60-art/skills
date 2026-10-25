# 47 · Long-form retention: autopsy, gate, fixes (Retention desk, 2026-10-25)

Nolan: "Retention on long form is a huge issue, we need it fixed."

**Credits: 20 vidIQ** (channel_analytics by video 5, audience_retention 5, outliers 5, transcript 5). Balance 660 → 640.

## 1. What we have (YouTube Analytics, 9/25-10/25, dimension = video)

- Only **one long-form has retention data: gFhrONKK0rI** ("Everything You Know About Animals Is WRONG").
  - It is the **2:15 quiz pilot** (episodes/myths-01/ep01.mp4, 134.9 s), not a 9-10 min episode.
  - 11 views, 11 engaged, 9 minutes watched, **53 s average view duration, 39.8% average view percentage**.
- The other long-forms (myths quiz RwbgzQisvYM, wolves history Uqj0QL8G0d4, 8-21 public views in data/views.csv) return **no rows yet**: Analytics lags 2-3 days. Their curves get pulled by the evening routine (§6).
- Shorts in the same report hold 47-88% (13-24 s AVD).
- With 11 viewers, every step in the curve is **one person**. Read the drops as *what each person left on*, not as percentages.

## 2. Drop points, matched to the script (whisper transcript of ep01.mp4)

| Time | Kept | Line on screen | Cause |
|---|---|---|---|
| 0:02 | 100% → 91% | "Quick quiz. What does an ostrich do when it gets scared?" | Quiz framing at frame 0 (retired since) |
| 0:04 | 91% → 82% | "If you said it buries its head in the sand... you've been lied to" | **Answered its own question at 4 s**: the loop closed before it opened |
| 0:14 | 82% → 64% | "Today we're fixing the animal facts that your teacher... got completely wrong" | **Agenda/intro line.** The biggest single drop (2 of 9 still watching) |
| 0:18 | 64% → 55% | "Let's start with the ostrich. Ostriches do not bury their heads" | Re-states the answer already given |
| 0:28 | 55% → 45% | "...would not have survived very long" | 25 s on one myth, no tease of what's next |
| 0:46 | 45% → 36% | "It runs at about 70 km an hour, or it kicks..." | Same myth still running: **45 s on one item** |
| 1:12 | 36% → 27% | "...they remember these tricks for months" | Evidence list, no twist or new picture |
| 1:12-2:15 | 27% flat | bull, bat, "the next one involves Disney..." | The 3 who stayed past 1:12 watched to the end |

Log: data/retention.csv.

**Pattern:** people left on (a) intros and agendas, (b) a promise answered too early, (c) one item running past ~30-45 s with no tease of the next. Nobody left on a new animal, a joke landing, or a tease.

## 3. What works for small channels (vidIQ outliers, long-form, under 100K subs, last year)

| Video | Channel (subs) | Views, breakout | Length | Shape |
|---|---|---|---|---|
| Every Continent's Deadliest Animal Explained | The Animal Dude (25.9K) | 692K, 106x | 16:23 | 10 animals, one per continent |
| SCARY Nature Moments That Don't Feel Real... | Haven (20.1K) | 318K, 422x | 12:50 | compilation of moments |
| 42 Strangest Creatures on Earth You Won't Believe Exist | Curious Elephant (39.9K) | 114K, 46x | 28:13 | 42 items, about 40 s each |
| Fun Science: Insects & Plants' Bizarre Survival Tactics! | fridge_111 (60.9K) | 107K, 100x | 23:05 | list of tactics |

(Kids' sing-along and nursery breakouts in the same search are skipped: different audience.)

**Transcript teardown, "Every Continent's Deadliest Animal Explained":**
- **First 30 s:** no intro, no welcome, no channel name. Frame 0 is the first animal's name ("Cape buffalo."), then a correction hook: "people assume lions or crocodiles... but they're wrong." The first fact lands at 0:03.
- **Chapter shape:** 10 segments of **75-100 s**, each opening on the animal's name as a header and a mini-hook ("the deadliest animal isn't a jaguar... it's a frog smaller than your thumb").
- **Re-hooks:** every new animal is the re-hook, so one lands every ~90 s. There are no between-segment teases.
- **Open loop:** the title itself ("every continent") is a countdown the viewer can track. They know how many are left.
- **Asks:** one subscribe line at 9:28 (58%) and one at the end. Nothing in the first 9 minutes.
- **Weak spot:** segments end on a summary sentence ("It became X's deadliest by..."), the exact beat where our pilot lost people.

**What we take from it:** start on the animal, make the structure countable, and change animal (or twist) at least every 75 s. Our version is shorter and funnier, and it also teases what's next, which they don't do.

## 4. The rules (tools/retention.py, wired into episode.py like openloop.py)

Times come from spoken words. The rate is 3.35 words/s for Kokoro at +0%, calibrated on the 10/25 renders; chapter estimates landed within 5 s of the real ones. Exact times come from `--timeline WORK/timeline.json`. R1-R7 fail the build; `--no-retention` exists only for old episodes.

| Rule | Threshold | Evidence |
|---|---|---|
| **R1 Cold open** | Payoff promised in the first 30 s ("at the end", "the last one", "number one", `promise: true`). Frame 0 is an unblurred animal photo with no text card. No intro, welcome or agenda line ("I'm Meatball", "today we", "today:", "welcome", "in this video") before 30 s | 0:02, 0:04 and 0:14 drops; rival opens on the animal |
| **R2 Open loops** | A tease, cliffhanger, countdown step or twist at least every **75 s** from 0:30 to the payoff (warn above 60 s; aim 45-60) | 0:28/0:46 drops after 25-45 s without a tease |
| **R3 Visible structure** | Every story chapter opens with `counter: {n, of}` (drawn as "2 OF 5" or "#4", with dots), numbered 1..N, plus spec `progress: true` (progress bar with chapter ticks) | Rival's "every continent" countdown |
| **R4 Segments** | No stretch over **75 s** without a new animal, a twist, or a Meatball jeopardy beat (`jeopardy: true`) | Rival segments 75-100 s; our 1:12 drop |
| **R5 Save the best** | Exactly one `payoff: true` chapter. It is the last counted chapter, starts in the **back 35%**, is teased in the first 30 s (R1) and again at 30-70% (warning), and the outro wrap-up after it runs **60 s at most** | 0:04 drop: never pay off early. Viewers leave once the promise is paid |
| **R6 Expectation match** | At least half the title's (and `thumb_text`'s) key words are said or shown in the first 60 s, and story chapter 1 starts by 0:60 | Title/thumbnail promise kept in the first minute |
| **R7 Length** | **5:00-7:00** while AVD is under 2:00 | See below |

**Length trade-off:**
- Mid-roll ads need 8:00+. At 5-7 min we earn only pre/post-roll once monetized.
- We aren't monetized yet (YPP needs 4,000 watch hours), and watch hours come from AVD × views.
  - A 6-min video at 40% AVD returns 2.4 min a view.
  - A 10-min video at 15% AVD returns 1.5 min.
- Shorter wins until AVD clears 2:00.
- Revisit: when 3 long-forms in a row hold above 2:00 AVD and 50% at 0:30, test one 8:30 episode with a mid-roll at a chapter break.

The existing ask layout stays and does not conflict with these rules: guess card at 15-40 s, one subscribe pill at 28-55 s, one like ask mid-video, "Were you right?" in the last 90 s.

## 5. What changed in the two queued episodes

Before the fix, both failed:
- **explains-03:** R1 (the "I'm Meatball... Today: real zombie animals" agenda line at 0:16), R2 (105 s with no re-hook), R3 (no counter or progress), R4 (78 s), R5 (no payoff flag).
- **explains-02:** R1 (agenda line at 0:08), R2 (99 s and 112 s gaps), R3, R5.

Facts are unchanged in both, and no viewer quotes were added.

**explains-03 (zombies, Sat 10/31):**
- The agenda line is replaced by a countdown promise: "Five zombie animals, counting down. Each one creepier than the last. And the last one might be you."
  - The label "5 ZOMBIE ANIMALS" lands on "five".
- "I'm Meatball, by the way" moves into the subscribe line (0:3x, after the cold open). "Okay, while you type, a quick favor" is cut.
- Each chapter gets an on-screen counter, 1 OF 5 to 5 OF 5, plus a progress bar with ticks.
- Toxoplasma ("the one that might be in you") is flagged as the payoff, and stays last.
- Chapter-end teases, as Meatball lines:
  - "And that was the gentle one. Number two walks its victim on a leash."
  - "Next, a snail. And its eyes are doing something eyes should never do."
  - "Okay. One left. The one I promised you."
- Mid-video tease added to the like ask: "And the one that might be inside you? Still coming."
- "Now, people." is marked as the twist inside the 80 s payoff chapter.

**explains-02 (deadliest, Tue 11/3):**
- The agenda line is replaced by the ranking promise: "Five animals, ranked by how many people they actually kill. Smallest number first. Each one deadlier than the last."
  - New label: "RANKED BY BODY COUNT".
- The subscribe line no longer opens with "Okay, while you type, a quick favor".
- Counters run #5 to #1 (shark, kissing bug, dog, snakes, mosquito), plus a progress bar.
- "The snake that sizzles" folds into the "Snakes" chapter. The mosquito is flagged as the payoff.
- Teases:
  - after sharks: "Number four? It bites you in your sleep."
  - the like ask now ends: "Two to go. The next one makes a sound I really don't like. And number one? Smaller than you'd guess."

- explains-02 cold open also gains "As a meatball, I am taking very careful notes." so the guess card and pill stay in their 15-40 s / 28-55 s windows after the agenda line was cut.

| Episode | Before | After (rendered) | Metricool |
|---|---|---|---|
| explains-03 zombies, Sat 10/31 2 PM | 6:18, chapters 0:40/1:58/3:07/3:52/4:35 | **6:31**, chapters 0:39/2:01/3:13/4:02/4:48 (payoff at 74%) | 406039119 → **406077563**, read back 2026-10-31T14:00 America/New_York |
| explains-02 deadliest, Tue 11/3 2 PM | 6:08 | **6:12**, chapters 0:36/1:21/2:12/3:19, payoff 4:21 (70%) | 406039276 → **406099474**, read back 2026-11-03T14:00 America/New_York |

Both pass tools/retention.py on their exact render timelines.

## 6. Routine

Every evening the Intel desk does the following (research/experts/intel.md):
1. Pull `audience_retention` for every long-form older than 48 h.
2. Log each drop of 5+ points in data/retention.csv, with the line on screen (whisper the ep.mp4 or read the script timeline) and its cause.
3. Send the top drop cause to the Showrunner.

**Scoring:** keep the gate's thresholds while explains-01/02/03 reach at least 50% at 0:30 and 2:00 AVD. Where a drop repeats at a rule's limit (e.g. people leave at 60 s into segments), tighten that threshold by 15 s.
