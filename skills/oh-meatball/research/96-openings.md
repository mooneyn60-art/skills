# 96 · How the top TikToks on our topics open, next to our cuts (2026-11-12)
**Answer:** the first three seconds of our cuts are not the gap. On every opening measure we could take (when the first word is spoken, words in the first 3 seconds, cuts, how much the picture moves) our 14 pet and survival cuts sit inside the range of the 32 top TikToks on the same topics. What the biggest ones have that we do not is a real animal in a real moment and, for the fact videos, a person talking to camera. Nolan has ruled real footage out ("No, keep it all drawn"), so nothing in the template changes from this. Part 2 (our own 50 Shorts against their watch numbers) is at the end.
Asked by Nolan: 11/10 "look at outliers and how they hold their retention"; 11/12 "we hold no retention", then "focus heavy on engagement". Tool: `postkit.py teardown` (new 11/12). Rows: `data/96-openings-top-tiktoks.csv` (32 videos, the public TikToks read in research 93), `data/96-openings-ours.csv` (our 7 TikTok cuts and 7 YouTube cuts).

## 1. Method
- Each video was fetched once with yt-dlp, measured and deleted. Speech: faster-whisper small.en with word times. Cuts: ffmpeg scene change above 0.30. Movement: the mean grey-level change between 12 frames taken every 0.25 s over the first 3 seconds, middle band of the picture (0 = a still picture).
- Plays are TikTok's public counts on 11/12. The 32 were picked top-first by an earlier search, so they are winners only: this shows what winners look like, not what separates winners from losers.

## 2. Numbers (medians)
| Group | n | Length | First word | Words in first 3 s | First cut | Cuts in first 3 s | Movement |
|---|---|---|---|---|---|---|---|
| Top TikToks, all | 32 | 52.8 s | 0.00 s | 9 | 7.0 s | 0 | 6.1 |
| Top TikToks, 500K plays or more | 13 | 61.1 s | 0.00 s | 3 | none | 0 | (same pool) |
| Top TikToks, 35 s or shorter | 9 | 22.0 s | 0.00 s | 8 | none | 0 | (same pool) |
| Our TikTok cuts | 7 | 23.6 s | 0.00 s | 11 | 3.6 s | 0 | 8.7 (all 14) |
| Our YouTube cuts | 7 | 19.5 s | 0.00 s | 11 | 2.8 s | 1 | 8.7 (all 14) |

## 3. What the winners are
- The biggest are real moments with their own sound, not fact videos: a moose getting up at someone (7.0M plays, 8 s, opens "Get up."), a bear walking up to a man (6.7M), a dog caught after wrecking a hat (4.3M), a shark turned away by hand (1.5M). They say almost nothing in the first 3 seconds and never cut.
- The fact videos (about 17 of the 32) are a person talking to camera over footage of a real cat or dog: "Cats know their name, so that's actually a fact." 1.0M; "Can dogs feel guilty?" 641K; "Scientists have a new theory for why dogs wag their tails." 112K; "Does your cat know their name?" 68.7K; "Cats can't taste sweetness." 49.8K.
- Question or statement first does not separate them: question openers run from 1.8K to 857K plays, statement openers from 15 to 2.0M.
- More cuts do not go with more plays: the biggest have none.

## 4. What it means for us
- Do not spend more work on cut rate, pace or the first-word time. They are already where the winners are.
- The hook wording the fact winners use is the searched question or the bare fact in the viewer's words. Ours do the same, with the hedge the fact-check requires.
- What we can still push inside a drawn video is the part viewers answer and pass on: a question about their own pet, a line worth sending to someone, a joke. That is Nolan's 11/12 order ("focus heavy on engagement") and is now a rule in MASTER_ORDERS ("Previews and engagement").

## Could not measure
- Why a video was shown: plays depend on the account and on TikTok's own choices, and losers were not sampled.
- Watch time and finish rate of any of these videos.
- Speech in non-English or music-only videos (two of the 32 gave junk words).

## Part 2. Our own 50 Shorts: does the opening go with how long people watched? (added 11/12, 16:45 ET)
Rows: `data/96-openings-our-shorts.csv` (the measures), `data/96-hold-joined.csv` (joined to watch numbers). Watch numbers: Windsor per video per day (research 90's pull, 10/22 to 11/09), summed per video: average % viewed and engaged share (engaged views divided by views). 50 Shorts had both numbers and a file. Test: Spearman rank correlation, then the same with video length held fixed.
- Length is the one clear thing: longer Shorts have a lower average % viewed (rho -0.61, p under 0.001). This was known (research 69) and is partly arithmetic: a short loop is easy to watch twice.
- Words in the first 3 seconds, with length held fixed: rho +0.28 with engaged share (p 0.049) and +0.30 with the engaged share of days 0 and 1 (p 0.034). Among the 27 Shorts of 11 to 21 seconds: +0.39 with average % viewed (p 0.043). A weak lead only: 28 tests were run, so one or two at this level are expected by chance.
- Nothing else holds once length is fixed: time of the first cut (-0.03), cuts in the first 3 seconds (-0.04), cuts per second (+0.25, p 0.086), words per second (0.00). The first word is at 0.00 s in every one of the 50.
- So for our own videos too, the opening mechanics explain little. Keep Shorts short (16 to 20 s), start talking at once and say a full, dense first sentence. The seven funnier cuts already have 8 to 14 words in the first 3 seconds.

## Could not measure (part 2)
- Where inside a video viewers leave (no retention curve until vidIQ on 11/24).
- Topic and style are not held fixed here; with 50 videos there is not enough data to do it.
