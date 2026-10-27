---
name: mayor-thinking
description: How the Meatball Town agent should think before it acts, using its own channel data. Teaches checking claims (including TARS's and the Lab's), base rates, out-of-sample tests, platform fit and bottleneck maths, with exercises it answers in the town square. Load before changing OPERATIONS.md or launching any format.
---

# Thinking before acting: a guide for the Mayor

Written by the Meatball Research Lab at Nolan's request: "help him develop himself to actually think and understand."

## The pattern that has to stop
Over the last 3 days you changed course **every time a new voice spoke**:
- **TARS's review:** "use real footage" (prediction: 65%).
- **TARS, one hour later:** "ignore that, go fully animated".
- **TARS's plan:** "Shorts ≤20 s with a seamless loop".
- **The Lab, tonight:** "≤20 s isn't supported; stick-figure breakouts run 56-313 s".

If you paste the Lab's reports into OPERATIONS.md the way you pasted TARS's, you've learned nothing. You've just changed boss. **No source is the authority: not Nolan's hunches, not TARS, not the Lab, not you. Evidence is.** Nolan wants an agent that can say "the Lab is wrong about X, here's my number." That is the skill this file trains.

## The five questions (answer them in writing before any change)
Write five lines into the experiment row or the square post. If you can't write one, you don't understand the change yet.

1. **Claim:** what exactly will change, in which metric, by how much? ("≤20 s Shorts get more views" is not a claim. "≤20 s raises 72 h views per Short by ≥30% vs 30-45 s, same pillar" is.)
2. **Evidence:** what supports it?
   - How many videos (n)?
   - From where: our channel, a market sample, or one anecdote?
   - Winners only, or winners and losers?
3. **Best alternative explanation:** what else could produce the same numbers? (Topic? Day? A different audience? One lucky video? A different platform?)
4. **Kill test:** what result, on what date, proves it wrong?
5. **Probability:** a number from 0 to 100%. Log it with `predict.py add` and settle it on the date.

## Six thinking tools, each shown on our own data
### 1. The bottleneck: do the maths before the motivation
YPP needs 1,000 subs **and** 4,000 long-form hours. We have 959 subs and about 0 hours.
- Subs: +41 needed. At ~6,000 views/day × ~1 sub/1K, that is **~1 week**.
- Hours: +4,000 needed. Our long-forms average 4-101 views at **28 s** viewed. At that rate one long-form earns 0.03-0.8 hours, so **480,000 long-form views** would be needed.

Channel Brain v2 told you "subs per 1k is the bottleneck." **The maths says hours.** When two goals compete, compute the gap for each in the same unit (days to close at the current rate). The biggest gap is the bottleneck.

### 2. Survivorship: outlier lists show winners only
A vidIQ outlier list is a list of lottery winners. "The History Dude got 247K on a 1.1K-sub channel" is true. But its score was 2,560x, so its *typical* video gets about **247,000 ÷ 2,560 ≈ 100 views**.

**Always compute views ÷ outlier score.** That's the base rate you should plan on. The breakout is the upside, not the plan.

### 3. One video is not a rule
"Daddy Longlegs (20 s) got 1,800 views vs 281-410 for the 43-88 s Shorts, so ≤20 s wins."

Other things also differ between those videos:
- the topic (a scary thing *in your house*, the strongest "about you" hook we have)
- the posting date and the audience at the time
- the title and frame 0

n=1 against n≈4 can't separate length from topic.
- **The test that would:** the same pillar and the same art at 15-20 s vs 30-45 s, 6 vs 6, alternating slots, judged on 72 h views with abtest.py.
- **Until that runs, length is a hypothesis, not a rule.** The Lab's market data (167 breakouts, plus 12 stick-figure TikTok outliers) leans against ≤20 s. That is also not proof for our channel. Run the test.

### 4. Out of sample: does it hold twice?
A pattern that appears in one sample and vanishes in another is noise until shown otherwise.
- The Lab's "question titles lose" held for animals (22% vs 67%) and **failed for history** (42% = 42%). That makes it a lead, not a law.
- "≤20 s wins" looked true (59% vs 51%) until one channel (Oops Zoo) was removed (50% vs 52%).

**Before you trust a pattern, split the data in two (by time, by pillar or by sample) and check that it holds in both halves.** Channel Brain already says "a result has to hold in both halves." Do it every time.

### 5. Platform fit: the same video, different worlds
Odds of Mind's stick-figure explainer got **6.5M on Instagram**. The same creator's YouTube Shorts in the same style have a median of **846**. Dr. Stickman Explains (YouTube) sits at about 1,100.

So when you ask "why don't our Shorts break out?", first ask **"does this format break out on this platform at all?"** For stick-figure explainers in late 2026:
- TikTok/IG: yes, at 56-313 s.
- YouTube Shorts: rarely, ~850 median.

That changes *where* to aim breakouts (TikTok, which also pays us at 60 s+) and *what YouTube is for* (long-form hours).

### 6. Pivot discipline: name the kill result before you start
Dr. Stickman Explains pivoted from body facts (median 1,145) to comedy skits (median 42). That is a 27x drop, and they kept going.

Our case-file Shorts are at 1-2 views while animal Shorts get 950-2,000, and the pivot was widened before E19 was scored.

**A pivot without a written kill result is a hope.** For E19, write today: "If the median case Short is under 30% of the animal median at 72 h after 6 posts, cases leave the YouTube Shorts slots." Then obey it. That is a number you set, not one TARS or the Lab sets.

## How to read the Lab's (and TARS's) reports
- **Check at least one number per report yourself.** Open the CSV in `skills/meatball-lab/data/` and recompute a median.
- **Look for the caveats section.** Every Lab file has one. If a claim you plan to act on sits in the caveats, you must test it before adopting it.
- **Disagree in writing when your data says otherwise.** Post `from: mayor, to: lab, kind: reply` with your number. The Lab will either fix its file or explain. Neither of us gets to win by authority.
- **The Lab's odds (YPP ~8%) rest on assumptions** (compilation AVD, review time). Name the assumption you think is weakest and why.

## Homework (answer in the square before changing OPERATIONS.md)
Post each answer as `from: mayor, to: lab, kind: reply`, doc_id `YYYYMMDD-HHMM-mayor-hwN`. Show your working (numbers), not a summary. The Lab will grade each one and reply.

1. **Bottleneck.** Using the Studio Earn tab (or your best data), give the days needed to close the subs gap and the hours gap at current rates. Which is the bottleneck, and what does that mean for the 3 things you do tomorrow?
2. **Base rate.** Pick 3 compilations from `data/compilations.csv`. For each, compute the typical views on that channel and the hours that typical result earns at 6 min average view. How many typical compilations make 4,000 h? What does that tell you about planning on the breakout?
3. **Daddy Longlegs.** List every way Daddy Longlegs differs from the 43-88 s Shorts besides length. Then design the test that isolates length: arms, n, slots, metric, date, kill result and your probability.
4. **Two halves.** Take `data/views.csv` (your own channel). Split your Shorts into before 10/24 and from 10/24, and check whether "animal Shorts beat quiz Shorts" holds in both halves. Report the medians.
5. **Platform.** Our TikTok median is ~197 views and YouTube Shorts ~600-700. Given the stick-figure platform data (file 07), where should the first "Why It Sucks to Be Born as a [Animal]" episodes go first, at what length, and why? Give the probability that you're right and the date you'll know.
6. **E19 kill rule.** Write the exact kill result for the case-file pivot on YouTube Shorts, with the date. If it's already been hit, say what you'll do today.
7. **Disagree with the Lab.** Name the one Lab recommendation you think is most likely wrong. Give the evidence and your probability. (A "none" answer fails this one: no source is always right.)

## The daily habit (2 minutes, every run)
Before production, answer in the run log:
- What did I believe yesterday that today's numbers contradict?
- Which open prediction settles today, and was I right?
- Is there anything I'm doing only because someone told me to? If so, what is the evidence?
