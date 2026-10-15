# 01 — Outlier Shorts research for Certified Bart

Pulled 2026-10-15 from vidIQ (read-only). Nothing was posted, uploaded, edited or published.

**Labels used in this file**
- **MEASURED**: a number or string copied from a vidIQ API response, or counted from those responses by `analyze.py` (in this folder; raw records are in `data.py`).
- **INFERENCE**: my interpretation. It is always marked as inference.

**Method (measured)**
- `vidiq_outliers` with contentType=short and publishedWithin=threeMonths (about 90 days, 2026-07-17 to 2026-10-15). Keywords: "Joe Bartolozzi", "Joe Bart" (min 300k views, sorted by views), "Jynxzi", "Kai Cenat", "Caseoh", "moistcritikal" (all title terms required), "Ludwig" (all title terms required), "streamer reacts funny reaction" (min 100k views), "streamer clips funny moments" (min 500k views, max 100k subs). A run filtered to the IDs of Joe's own channels (@joebartshorts UCSUPawe0FE_M9ZTUYE-NiNQ and the main channel) returned **0 results**, so no outliers from Joe's own channels are in this set.
- `vidiq_channel_videos` (latest 50 Shorts) for **Certified Bart**, JB Highlights, JOE CLIPPER and quikraid. Used to measure cadence and baselines.
- `vidiq_video_transcript` on the top 10 outliers to get hooks.
- **Breakout x** is vidIQ's breakoutScore: how many times the video beat the channel's typical views.
- Records left out on purpose: videos under about 100k views, plus off-topic keyword collisions such as "Chompin Charlie" toys, "Ludwig" drum kits and pet "Charlie" channels.
- Some records come from channel_videos instead of outliers. For these, breakout is that tool's value, and the publish date is ISO (5 rows: wC_xgSVUyJg, koSILloSPWs, T6A9O4F6Rng, yfcRN4Mg_7Y, KjwJOa9wS7g, j0yVV5Zaqf8).
- Credits: the balance went from 6,573 to 6,033, so **540 credits were used** (budget 800). Per-call prices were higher than the "5 credits" listed in the tool descriptions.

**Measured baseline for Certified Bart.** Latest 50 Shorts, 2026-07-06 to 2026-09-15:
- Median **1,654 views**. Best was 71,384 ("Joe Bartolozzi Roasts People Who Fake Smile at TikToks", breakout 32.5x).
- 0 of 50 reached 500k.
- **No upload since 2026-09-15**, which is 30 days before this pull.

## 1. Data table (102 outliers; 49 Joe Bart, 38 streamer-clip, 15 reaction/commentary)

Hook column:
- **MEASURED** means the first words spoken in the vidIQ transcript. Transcripts have no timestamps, so "first 2 seconds" is approximated by the first spoken line.
- **inference** means the video was not transcribed.

| # | Niche | Title | Channel | Subs | Views | Breakout x | Dur s | Published | Hook (first words) |
|---|---|---|---|---:|---:|---:|---:|---|---|
| 1 | Joe Bart clips | "No biggie we wipe" / Joe Bartolozzi ([link](https://youtu.be/9Joz54wfo20)) | JB Highlights | 31,600 | 10,781,859 | 105.08 | 8 | 2026-07-23 | MEASURED: "Cody's first dinner of the week was gochang butter cabbage and steak..." (Joe reacting to someone else's clip; punchline at ~5s) |
| 2 | Joe Bart clips | Joe Bartolozzi ATTIC INNCIDENT ([link](https://youtu.be/rr8lHC65-to)) | Aleksander | 1,150 | 9,915,421 | 3434.41 | 48 | 2026-09-22 | MEASURED: "Okay. Ready? Come on. Is there anything up there?" (cold open mid-story, no setup) |
| 3 | Joe Bart clips | Joe Bart & Deji Took This Spelling Battle TOO Far 🤬😭 ([link](https://youtu.be/juidfriR5OI)) | jynxzi&bartolozziclips | 6,010 | 9,241,786 | 244.6 | 123 | 2026-10-04 | MEASURED: "Can you spell recipient? There we go. All right. Spell chicken. Are we [f-ing] serious?" (rapid-fire game, payoff inside 3s) |
| 4 | Joe Bart clips | Who Actually Misses Old Joe Bart?✌️  #joebart #funny #joebartolozzi ([link](https://youtu.be/3O81gBJED_k)) | JoeBartolozer | 49,900 | 8,682,468 | 33.9 | 25 | 2026-09-14 | MEASURED: "Now, I hate to be that guy, but that's a piggy bank." (opinionated one-liner, starts mid-rant) |
| 5 | Joe Bart clips | Joe Bart Finds Out what PK means 😂 ([link](https://youtu.be/Pe_9YWr231Q)) | JOE CLIPPER | 42,900 | 6,204,595 | 8.25 | 28 | 2026-09-21 | inference: n/a - not transcribed |
| 6 | Joe Bart clips | Joe pump fakes in musical chairs / Joe Bartolozzi ([link](https://youtu.be/1MO1Jyxff-Q)) | JB Highlights | 31,600 | 5,714,598 | 14.01 | 24 | 2026-08-02 | inference: n/a - not transcribed |
| 7 | Joe Bart clips | "Not that crazy" 💔 / Joe Bartolozzi ([link](https://youtu.be/TwWYlJVyxLw)) | JB Highlights | 31,600 | 5,656,537 | 61.67 | 17 | 2026-08-26 | MEASURED: "We need like a $500,000 fish right now. We need something crazy." (setup line -> [music] -> 'Not that crazy' payoff; title = punchline) |
| 8 | Joe Bart clips | Joe Bart Shows Off His CRAZY Stretch Marks 💀 ([link](https://youtu.be/qZuQHMpqRKM)) | JOE CLIPPER | 42,900 | 5,535,654 | 11.03 | 22 | 2026-08-28 | inference: n/a - not transcribed |
| 9 | Joe Bart clips | Mcdonalds is not a 5/5 💔 / Joe Bartolozzi ([link](https://youtu.be/wC_xgSVUyJg)) | JB Highlights | 31,600 | 5,531,023 | 18.97 | 33 | 2026-09-03 | inference: n/a - not transcribed |
| 10 | Joe Bart clips | Same Person Btw (Joe Bartolozzi) 😭💀 ([link](https://youtu.be/LJD-zIJkWSM)) | Pixly Edits | 2,770 | 5,098,760 | 208.75 | 25 | 2026-09-09 | MEASURED: "Gingerbread houses. Joe, no. I want to show my own." (contrast edit: calm Joe -> screaming Joe) |
| 11 | Joe Bart clips | No Way Joe Bart Said That💀🥀 ([link](https://youtu.be/1SEuI1tLe08)) | DailyDoseOfJBart | 3,120 | 5,073,712 | 143.02 | 14 | 2026-08-26 | MEASURED: "A duck walked up to the lemonade stand..." (old/cringe TikTok, starts instantly on the bit) |
| 12 | Joe Bart clips | Joe Bart is a multiversal threat // #joebart #jynxzi #twitchclips #edit ([link](https://youtu.be/Yp3Pb_0Nbv8)) | RealMoney | 5,920 | 4,860,311 | 163.51 | 27 | 2026-08-05 | inference: n/a - not transcribed |
| 13 | Joe Bart clips | Joe Bart Takes An Egg To The Back 😭🎯 ([link](https://youtu.be/wEixizvs6-M)) | JOE CLIPPER | 42,900 | 4,129,908 | 17.92 | 27 | 2026-09-07 | inference: n/a - not transcribed |
| 14 | Joe Bart clips | Joe Bart Won't Stream With Rakai Again 😂 ([link](https://youtu.be/wduAv2DitCk)) | JOE CLIPPER | 42,900 | 4,104,573 | 17.78 | 31 | 2026-09-08 | inference: n/a - not transcribed |
| 15 | Joe Bart clips | Joe's perfect pausing / Joe Bartolozzi ([link](https://youtu.be/UEmGWZthhVg)) | JB Highlights | 31,600 | 3,739,277 | 34.3 | 23 | 2026-07-20 | inference: n/a - not transcribed |
| 16 | Joe Bart clips | Joe Bart tries not to laugh 😭🌹 ([link](https://youtu.be/69n0IBvuv1c)) | Joe Bart'O Clipz | 48,100 | 3,351,048 | 24.69 | 29 | 2026-09-23 | inference: n/a - not transcribed |
| 17 | Joe Bart clips | Average Discord mod / Joe Bartolozzi ([link](https://youtu.be/iDUEBua-ikY)) | JB Highlights | 31,600 | 2,867,661 | 8.24 | 33 | 2026-09-05 | inference: n/a - not transcribed |
| 18 | Joe Bart clips | Joe Bart Secret Trick To Hide Search History 💀 ([link](https://youtu.be/wU5NUKW0hho)) | JOE CLIPPER | 42,900 | 2,742,377 | 15.59 | 42 | 2026-10-05 | inference: n/a - not transcribed |
| 19 | Joe Bart clips | Too many things happening 😭🙏 / Joe Bartolozzi ([link](https://youtu.be/F6zByji5DlI)) | JB Highlights | 31,600 | 2,549,656 | 27.81 | 10 | 2026-08-24 | inference: n/a - not transcribed |
| 20 | Joe Bart clips | Joe Bart finds the stronghold Just to pass away  #joebartolozzi  #joebart #minecraft ([link](https://youtu.be/uaChHweTU3Y)) | Joe Clipz | 252 | 2,355,442 | 1295.22 | 59 | 2026-09-02 | MEASURED: "Where is it? [screaming] Where is it? Oh my god. No way." (opens on peak emotion) |
| 21 | Joe Bart clips | Joe Bart EDITOR Salary EXPLAINED💸🤔 ([link](https://youtu.be/fN_UUUYcbWM)) | jynxzi&bartolozziclips | 6,010 | 1,986,145 | 104.61 | 27 | 2026-08-29 | inference: n/a - not transcribed |
| 22 | Joe Bart clips | "If I ever go on a cruise" / Joe Bartolozzi ([link](https://youtu.be/T6A9O4F6Rng)) | JB Highlights | 31,600 | 1,969,106 | 7.26 | 13 | 2026-09-11 | inference: quoted line in title is likely the opening/payoff line |
| 23 | Joe Bart clips | Joe Bart plays GTA V for the first time 😭🌹 ([link](https://youtu.be/6VzUA4CLT10)) | Joe Bart'O Clipz | 48,100 | 1,860,032 | 19.58 | 23 | 2026-10-08 | inference: n/a - not transcribed |
| 24 | Joe Bart clips | That censor did nothing 😭 / Joe Bartolozzi ([link](https://youtu.be/yfcRN4Mg_7Y)) | JB Highlights | 31,600 | 1,693,658 | 5.81 | 12 | 2026-09-04 | inference: n/a - not transcribed |
| 25 | Joe Bart clips | “I’ll be back with more sh*t” 😭 // Joe Bartolozzi ([link](https://youtu.be/KjwJOa9wS7g)) | quikraid | 24,300 | 1,672,663 | 47.95 | 33 | 2026-08-25 | inference: quoted line in title is likely the opening/payoff line |
| 26 | Joe Bart clips | Joe Bart Discovers Insider Trading In GTA 5 😭💀 ([link](https://youtu.be/Y8uktVd-W5c)) | Joe Bart Verse | 4,250 | 1,547,013 | 32.18 | 25 | 2026-10-11 | inference: n/a - not transcribed |
| 27 | Joe Bart clips | Joe Bart Reacts To Most Insane Stone Crusher... ([link](https://youtu.be/bxDuJ8NhqvY)) | Not The Real Joe Bart | 22,200 | 1,505,603 | 21.55 | 128 | 2026-09-14 | inference: n/a - not transcribed |
| 28 | Joe Bart clips | Joe Bart Hears About Dolly Parton Passing. ([link](https://youtu.be/j2sst5cWzNk)) | Not The Real Joe Bart | 22,200 | 1,442,549 | 33.56 | 80 | 2026-08-27 | inference: n/a - not transcribed |
| 29 | Joe Bart clips | Prehistoric Joe Bart😭✌️  #joebart #funny #joebartolozzi ([link](https://youtu.be/9yBRFi0jWvc)) | JoeBartolozer | 49,900 | 1,351,784 | 41.31 | 16 | 2026-09-12 | inference: n/a - not transcribed |
| 30 | Joe Bart clips | Joe Has the Funniest Jynxzi Impression 😂 / Joe Bartolozzi #joebartolozzi #viral #shorts ([link](https://youtu.be/hX3j85dEMck)) | Bart_clips99 | 3,700 | 1,228,812 | 179.2 | 7 | 2026-08-17 | inference: n/a - not transcribed |
| 31 | Joe Bart clips | Joe Bart Almost Laughs At This💀 ([link](https://youtu.be/8krsosSgTcU)) | SnowTanked | 537 | 1,098,919 | 85.7 | 16 | 2026-09-22 | inference: n/a - not transcribed |
| 32 | Joe Bart clips | Dubbing Joe Bart Hello clip as Cleveland Brown ([link](https://youtu.be/Iy1_7weX0zI)) | Cj Laws | 13,300 | 1,073,319 | 54.86 | 24 | 2026-09-03 | inference: n/a - not transcribed |
| 33 | Joe Bart clips | Joe’s old search history💔😭 // Joe Bartolozzi ([link](https://youtu.be/K2jJN8Jjopo)) | quikraid | 24,300 | 1,055,522 | 5.99 | 35 | 2026-08-19 | inference: n/a - not transcribed |
| 34 | Joe Bart clips | Joe Bart Opened A Bath Bomb With Up To $1,000 Inside 💀😭 ([link](https://youtu.be/EW2uOrVxt-Q)) | BartaliniClips | 8,590 | 976,904 | 387.14 | 76 | 2026-09-25 | inference: n/a - not transcribed |
| 35 | Joe Bart clips | McDonald’s is not a 5/5💔 // Joe Bartolozzi ([link](https://youtu.be/koSILloSPWs)) | quikraid | 24,300 | 967,865 | 20.97 | 33 | 2026-09-06 | inference: n/a - not transcribed |
| 36 | Joe Bart clips | “SHUT THE F*CK UP JOE”😭💔🥀 // Joe Bartolozzi // Jynxzi ([link](https://youtu.be/J5VHhXhUO1Q)) | quikraid | 24,300 | 863,736 | 11.84 | 35 | 2026-09-19 | inference: quoted line in title is likely the opening/payoff line |
| 37 | Joe Bart clips | Joe Bart explains the average gym build // Joe Bartolozzi ([link](https://youtu.be/bhtGWKamu7M)) | quikraid | 24,300 | 740,594 | 12.82 | 67 | 2026-10-07 | inference: n/a - not transcribed |
| 38 | Joe Bart clips | Joe Bartolozzi on the Grow a Garden Creator 😳 ([link](https://youtu.be/3mm51gTmUY0)) | JoeBartbest_moments | 183 | 704,651 | 373.27 | 40 | 2026-10-03 | MEASURED: "Are people still playing like Grow a Garden? No, dude. That game completely died." (hot-take question) |
| 39 | Joe Bart clips | Joe Bart Explains How Huge Ronnie Coleman Really Was... ([link](https://youtu.be/sFQ5da9iwjE)) | Not The Real Joe Bart | 22,200 | 697,708 | 64.66 | 20 | 2026-10-06 | inference: n/a - not transcribed |
| 40 | Joe Bart clips | Ranking The Funniest Joe Bart Moments #fyp #joebartolozzi #joebartclips #funnymoments #funny ([link](https://youtu.be/ER1LZRXIY_E)) | RankVerse_ | 2,510 | 598,252 | 46.48 | 72 | 2026-10-05 | inference: n/a - not transcribed |
| 41 | Joe Bart clips | “You look breedable today”😭 // Joe Bartolozzi ([link](https://youtu.be/j0yVV5Zaqf8)) | quikraid | 24,300 | 540,329 | 15.5 | 13 | 2026-08-23 | inference: quoted line in title is likely the opening/payoff line |
| 42 | Joe Bart clips | "Joe above you" / Joe Bartolozzi ([link](https://youtu.be/FCiNxGMqBN8)) | JB Highlights | 31,600 | 493,864 | 9.66 | 10 | 2026-10-12 | inference: quoted line in title is likely the opening/payoff line |
| 43 | Joe Bart clips | Joe Bartolozzi BECOMES A VOICE ACTOR! 😭✌️ ([link](https://youtu.be/t_6fCzDQDkY)) | Joe FartoIozzi | 744 | 470,297 | 16.61 | 28 | 2026-08-25 | inference: n/a - not transcribed |
| 44 | Joe Bart clips | Joe Bart WON'T Pay His Mods 💀😭 ([link](https://youtu.be/YMgLlGvPD4I)) | BartaliniClips | 8,590 | 400,097 | 34.75 | 60 | 2026-08-27 | inference: n/a - not transcribed |
| 45 | Joe Bart clips | Joe Bartolozzi Tries To Reason With Flat Earthers ([link](https://youtu.be/G8E7_eswkAo)) | JOE CLIPS | 108 | 225,646 | 8.34 | 24 | 2026-09-29 | inference: n/a - not transcribed |
| 46 | Joe Bart clips | Joe Bartolozzi Streamer Games Fail / Is Joe Colorblind? ([link](https://youtu.be/3tXtNQQGG8A)) | BartMan | 446 | 216,522 | 31.05 | 13 | 2026-08-06 | inference: n/a - not transcribed |
| 47 | Joe Bart clips | Joe Reacts to his Streamer Games Musical Chairs ([link](https://youtu.be/leDvJQBVkyc)) | OverSprint | 1,590 | 206,327 | 18.37 | 38 | 2026-08-12 | inference: n/a - not transcribed |
| 48 | Joe Bart clips | Joe Bartolozzi Remembers School Fundraiser Prizes ([link](https://youtu.be/_ADviUizXAs)) | JOE CLIPS | 108 | 155,160 | 5.54 | 36 | 2026-09-30 | inference: n/a - not transcribed |
| 49 | Joe Bart clips | Joe Bartolozzi caught lacking 😮 ([link](https://youtu.be/wiqJ32i8JV0)) | AverageJoeBart | 784 | 136,946 | 21.76 | 76 | 2026-09-19 | inference: n/a - not transcribed |
| 50 | Reaction/commentary | Why everyone loves Lacy's clips 😭🤣 #lacy #funny #streamer ([link](https://youtu.be/ggDAqwPKFto)) | Tadirunning | 1,940 | 4,912,432 | 235.76 | 52 | 2026-08-25 | inference: n/a - not transcribed |
| 51 | Reaction/commentary | Glad she saved it 😎 #yonna #clips #streamer ([link](https://youtu.be/L9XJFPwKwJA)) | L8on | 675 | 4,065,092 | 2419.69 | 14 | 2026-08-22 | inference: n/a - not transcribed |
| 52 | Reaction/commentary | Piano Has 500 Ping 💀 #drdonut #streamer #clips #reaction ([link](https://youtu.be/okxduM7MFqc)) | TLN_Clips | 1,390 | 3,916,485 | 741.82 | 21 | 2026-09-15 | inference: n/a - not transcribed |
| 53 | Reaction/commentary | Ranking The Funniest Streamer University Moments Part 3😂 #funny #streameruniversity ([link](https://youtu.be/0UY3szJ3Yd0)) | MarkRizz Ranking | 70,200 | 3,749,111 | 193.18 | 60 | 2026-07-20 | inference: n/a - not transcribed |
| 54 | Reaction/commentary | Geo HITS NIC Out Of HER MOUTH?!😭🥀#funny #brisortiz #twitch #clips #streamer #meme ([link](https://youtu.be/48jpNLI21jQ)) | bris ortiz | 33,000 | 3,748,105 | 539.71 | 14 | 2026-09-14 | inference: n/a - not transcribed |
| 55 | Reaction/commentary | STREAMER Reaction to Drake’s Shabang MUSIC 😂 ([link](https://youtu.be/klMie8-8wsc)) | Zaion Mafia | 204,000 | 2,064,173 | 47.83 | 22 | 2026-10-05 | inference: n/a - not transcribed |
| 56 | Reaction/commentary | Twitch-KEYOHANA #streamer #funnyvideo #reaction #clips #fyp ([link](https://youtu.be/VvYa1R-hZ0Q)) | KEYOHANA | 47,800 | 1,912,307 | 159.72 | 16 | 2026-10-06 | inference: n/a - not transcribed |
| 57 | Reaction/commentary | How would you react? 😭🥀 #clips #neon #viral #streamer ([link](https://youtu.be/tcLRQ_DZFZU)) | L8on | 675 | 1,911,583 | 227.13 | 16 | 2026-08-27 | inference: n/a - not transcribed |
| 58 | Reaction/commentary | 🎤❤️ Agent Reacts To Ray Streamer Award Speech ([link](https://youtu.be/0NfubXVuSbU)) | Clipsy Media | 2,790 | 1,869,632 | 52.84 | 11 | 2026-07-28 | inference: n/a - not transcribed |
| 59 | Reaction/commentary | Kai Cenat Reacts To GTA VI Adding Streamer Into The Game! 🤣 ([link](https://youtu.be/lQtFv5yv_Rs)) | Snickerly | 1,450,000 | 1,523,543 | 6.3 | 12 | 2026-08-27 | inference: n/a - not transcribed |
| 60 | Reaction/commentary | Best Funny Streamer Moments 2026!!! ( Part 2 ) ([link](https://youtu.be/31HM_tq4sdA)) | IceBearRanks | 1,500 | 1,034,918 | 43.24 | 56 | 2026-09-26 | inference: n/a - not transcribed |
| 61 | Reaction/commentary | I Ranked 4 Streamers Moments, The Last One Took Me Out. #funnymoments #streamer #ranking g ([link](https://youtu.be/Q3mTv45NzfY)) | Top5RushYT | 515 | 980,845 | 833.87 | 116 | 2026-10-01 | inference: n/a - not transcribed |
| 62 | Reaction/commentary | Ranking the Most Wholesome Streamer Moments #shorts #ishowspeed ([link](https://youtu.be/FXLywmLczmk)) | THE RANKERS | 16,500 | 880,715 | 67.37 | 91 | 2026-09-12 | inference: n/a - not transcribed |
| 63 | Reaction/commentary | Jason Reacts to Streamer University's Weirdest Student ([link](https://youtu.be/nqzSrdaVCNA)) | taclipz | 12,800 | 528,843 | 21.19 | 70 | 2026-07-18 | inference: n/a - not transcribed |
| 64 | Reaction/commentary | XQC reacts to 'Crash me Outside' 😂 #streamer #funny #xqc ([link](https://youtu.be/7sr8X4WDgrQ)) | TrendyTwitchClipz (TTClipz) | 15,800 | 167,265 | 58.76 | 79 | 2026-10-13 | inference: n/a - not transcribed |
| 65 | Streamer clips | Wolverine Is Just That Good #moistcritikal #penguinz0 #shorts #wolverine ([link](https://youtu.be/3nOj3TDs0Jk)) | Moist Charlie Clips | 1,340,000 | 25,523,387 | 230.18 | 24 | 2026-09-16 | inference: n/a - not transcribed |
| 66 | Streamer clips | Caseoh timing NEEDS to be studied 💔😭 #caseoh #givemebackmykids ([link](https://youtu.be/v272yGBEQFw)) | MaybeTH | 13,400 | 8,386,464 | 602.5 | 66 | 2026-08-01 | inference: n/a - not transcribed |
| 67 | Streamer clips | CaseOh CLUTCHED This Wordle 😭 #caseoh #wordle ([link](https://youtu.be/nKDlQVDsZTQ)) | MoreClipsForYou | 400,000 | 7,093,481 | 26.65 | 100 | 2026-08-21 | inference: n/a - not transcribed |
| 68 | Streamer clips | Jynxzi meets his match 😭🌹#shorts #jynxzi ([link](https://youtu.be/9OztXcXcjN4)) | Jumping Otter | 109,000 | 5,863,006 | 260.1 | 85 | 2026-10-03 | MEASURED: "How's it going? Hi. Oh my gosh. Sorry. I don't know how to talk to men." (dating-show interaction, awkward line in first 2s) |
| 69 | Streamer clips | Ludwig leaks his own earnings🤯#ludwig ([link](https://youtu.be/jCIk6ZorSvw)) | ViralVault | 22,200 | 4,876,232 | 1450.97 | 160 | 2026-07-20 | inference: n/a - not transcribed |
| 70 | Streamer clips | Ludwig is actually a great teacher 🐐 #streameruniversity #ludwig #trending ([link](https://youtu.be/2dO7wEAC-qg)) | Top Tier | 8,080 | 4,739,901 | 228.52 | 56 | 2026-07-18 | inference: n/a - not transcribed |
| 71 | Streamer clips | Feels The Aura #moistcritikal #penguinz0 #shorts #wolverine ([link](https://youtu.be/Q9SUMq1ekRc)) | Moist Charlie Clips | 1,340,000 | 4,314,490 | 38.98 | 16 | 2026-09-16 | inference: n/a - not transcribed |
| 72 | Streamer clips | CaseOh Found A JENGA Tower In The Bathroom ([link](https://youtu.be/jPeMFE3Sdps)) | Pixeliplier | 87,100 | 3,254,474 | 49.62 | 28 | 2026-10-12 | inference: n/a - not transcribed |
| 73 | Streamer clips | The Rat That Made Kai Cenat Famous ([link](https://youtu.be/cckhJ4A_l3Y)) | N2N Films | 32,400 | 2,889,197 | 34.73 | 31 | 2026-09-30 | inference: n/a - not transcribed |
| 74 | Streamer clips | CaseOh loses it playing Happy Wheels 😭✌ ([link](https://youtu.be/NJAk8v9tfUE)) | tentinpants_ | 8,040 | 2,876,992 | 239.48 | 22 | 2026-10-11 | inference: n/a - not transcribed |
| 75 | Streamer clips | Solid Press Conference #moistcritikal #penguinz0 #shorts #gta #gta5 ([link](https://youtu.be/Iq-VnupGM74)) | Moist Charlie Clips | 1,340,000 | 2,175,705 | 10.2 | 31 | 2026-08-30 | inference: n/a - not transcribed |
| 76 | Streamer clips | Jynxzi Reacts to the "Smartest" Player🔥 #jynxzi #r6 ([link](https://youtu.be/m5xPAzEw1X4)) | Jumping Otter | 109,000 | 1,894,335 | 42.25 | 79 | 2026-09-17 | inference: quoted line in title is likely the opening/payoff line |
| 77 | Streamer clips | KNOCKOFF ELDEN RING??  #moistcritikal #penguinz0 #nodusfall #eldenring #soulslike ([link](https://youtu.be/gvRGG2ZYhr0)) | Cr1tikally Online | 10,100 | 1,803,332 | 8.19 | 31 | 2026-08-28 | inference: n/a - not transcribed |
| 78 | Streamer clips | Kai Cenat gets a Kai Mafia Tattoo ([link](https://youtu.be/mscGNCxtir4)) | Raysean | 18,200 | 1,705,551 | 109.68 | 18 | 2026-08-29 | inference: n/a - not transcribed |
| 79 | Streamer clips | Jynxzi is different 🤯🔥 #jynxzi #r6 ([link](https://youtu.be/3duToojcD_8)) | Jumping Otter | 109,000 | 1,508,656 | 63.83 | 62 | 2026-10-02 | inference: n/a - not transcribed |
| 80 | Streamer clips | Kai Cenat Gets a Gift From Duke Dennis 😂 ([link](https://youtu.be/PrxH572imeI)) | CleverClipsYT | 770 | 1,407,966 | 489.02 | 66 | 2026-10-06 | inference: n/a - not transcribed |
| 81 | Streamer clips | Going Jynxzi for Jynxzi in the bathroom 😭✌️ ([link](https://youtu.be/grBkPAHqd0Y)) | dvnielshorts | 2,760 | 1,304,528 | 192.9 | 24 | 2026-10-05 | inference: n/a - not transcribed |
| 82 | Streamer clips | CaseOh Goes Insane Over This Sausage 💀😭 #caseoh #meme ([link](https://youtu.be/IZwU4shZAek)) | CaseOh Moments | 388,000 | 1,095,987 | 23.55 | 141 | 2026-09-26 | inference: n/a - not transcribed |
| 83 | Streamer clips | Cgeezy meets Kai cenat in the VIVET store❤️ ([link](https://youtu.be/qdGtQbfKuzY)) | nyte | 3,450 | 1,071,148 | 110.96 | 27 | 2026-10-04 | inference: n/a - not transcribed |
| 84 | Streamer clips | Why Kai Cenat is Actually INSANE ([link](https://youtu.be/-CWfrc2GKOU)) | ScienceVillager | 1,270 | 981,342 | 164.41 | 21 | 2026-09-07 | inference: n/a - not transcribed |
| 85 | Streamer clips | CaseOh Reacts To PERFECT Chinese Food Ranking 😳😂 #caseoh #shorts ([link](https://youtu.be/1EmcFXQpgso)) | QuickCase | 9,270 | 862,343 | 16.75 | 82 | 2026-09-20 | inference: n/a - not transcribed |
| 86 | Streamer clips | Jynxzi Uses Random Deck Blind😳😱 #jynxzi #clashroyale #clips ([link](https://youtu.be/M-jowcQXcPY)) | Junko clipz | 59,700 | 852,152 | 16.91 | 141 | 2026-10-06 | inference: n/a - not transcribed |
| 87 | Streamer clips | CaseOh Won't Leave Vanilla Alone 😭 #caseoh #funny ([link](https://youtu.be/B6Tfdn9Gz74)) | VM Highlights | 9,880 | 486,777 | 14.54 | 29 | 2026-09-09 | inference: n/a - not transcribed |
| 88 | Streamer clips | Jynxzi Plays Against a Finnish Player ([link](https://youtu.be/2RZw_n5rCnM)) | kingclips | 3,420 | 443,429 | 271.7 | 177 | 2026-10-03 | inference: n/a - not transcribed |
| 89 | Streamer clips | Jynxzi can't handle Marlon 😭 #jynxzi #marlon #streamer ([link](https://youtu.be/FkdJcZJ4D7w)) | PlaqueClips | 11,200 | 430,174 | 16.34 | 50 | 2026-09-26 | inference: n/a - not transcribed |
| 90 | Streamer clips | jynxzi uses only random decks #jynxzi #clashroyale ([link](https://youtu.be/0V31M6cvI3c)) | Arthur | 1,290 | 428,969 | 17.24 | 181 | 2026-09-28 | inference: n/a - not transcribed |
| 91 | Streamer clips | Jynxzi Reacts To A Player with Insane Gamesense 😲🔥 ([link](https://youtu.be/4Ao025liyZA)) | Daily Junko | 27,000 | 377,269 | 26.93 | 124 | 2026-10-13 | inference: n/a - not transcribed |
| 92 | Streamer clips | Jynxzi reacts to Zen hitting 3000 MMR!!!🔥😱 #jynxzi #zen #rocketleague ([link](https://youtu.be/ZeKSQicqnVM)) | Jynxziclips | 544 | 359,258 | 130.59 | 26 | 2026-09-15 | inference: n/a - not transcribed |
| 93 | Streamer clips | Ludwig goes in on student 🫢#ludwig #shorts #streameruniversity ([link](https://youtu.be/NLj4X8lUIVk)) | TrendyTwitchClipz (TTClipz) | 15,800 | 337,258 | 12.28 | 66 | 2026-07-18 | inference: n/a - not transcribed |
| 94 | Streamer clips | CaseOh Reacts To GRIEF Being VERIFIED!? 😲 ([link](https://youtu.be/6hTHFPy98xg)) | AverageBumClips | 21,700 | 301,482 | 19.15 | 70 | 2026-10-05 | inference: n/a - not transcribed |
| 95 | Streamer clips | Ludwig couldn't contain himself 😭 #ludwig #valkyrae #fuslie #squeex ([link](https://youtu.be/YkP0YQ24f1g)) | SqueeniePanini | 2,080 | 282,874 | 9.45 | 45 | 2026-07-23 | inference: n/a - not transcribed |
| 96 | Streamer clips | BLOOD OF DAWNWALKER IS SUPER REPETETIVE #penguinz0 #moistcritikal #dawnwalker ([link](https://youtu.be/Esj5QM-oHKc)) | MoistDailyRants | 413 | 274,260 | 16.3 | 25 | 2026-09-11 | inference: n/a - not transcribed |
| 97 | Streamer clips | Nobody Warned Kai Cenat About This 😭💀 ([link](https://youtu.be/zGPW9FyVoSU)) | BrainBlast Clips | 514 | 238,376 | 25.1 | 51 | 2026-09-15 | inference: n/a - not transcribed |
| 98 | Streamer clips | Kai Cenat Said ONE Thing And Got BANNED 😭💀 ([link](https://youtu.be/fPc-asm9uWU)) | ToExtra | 8,920 | 228,507 | 12.33 | 17 | 2026-10-14 | inference: n/a - not transcribed |
| 99 | Streamer clips | Jynxzi shows off the “Jynxzi Run-out”👀🔥 #jynxzi #tiktok #siege #r6 #funnyfails #viral #gaming #fyp ([link](https://youtu.be/Tmk_nt3dSGI)) | RizzClipzz | 353 | 206,454 | 17.24 | 10 | 2026-10-11 | inference: quoted line in title is likely the opening/payoff line |
| 100 | Streamer clips | CaseOh Pulls Up the Difficulty Settings #CaseOh #Minecraft ([link](https://youtu.be/ltTa0wJ2zvo)) | CaseOhFanClips | 747 | 174,429 | 104.93 | 25 | 2026-09-24 | inference: n/a - not transcribed |
| 101 | Streamer clips | BIDDY BLAS ?? / Star Wars Galactic Racer /  #moistcritikal #penguinz0 #starwars ([link](https://youtu.be/6eW3W4LMtY4)) | MoistZclipper | 487 | 143,114 | 29.46 | 59 | 2026-10-08 | inference: n/a - not transcribed |
| 102 | Streamer clips | realest words from Caseoh ever #caseoh #funny #trending ([link](https://youtu.be/aJZmwnYPDvA)) | ghpumi | 2,380 | 109,068 | 46.11 | 14 | 2026-09-01 | inference: n/a - not transcribed |

### Feature counts (measured on titles; N per niche)

| Feature | Joe Bart (N=49) | Streamer (N=38) | Reaction (N=15) | All (N=102) | Certified Bart last 24 titles |
|---|---|---|---|---|---|
| starts with creator name/handle (Joe, Jynxzi, CaseOh, Kai...) | 32/49 (65%) | 26/38 (68%) | 5/15 (33%) | 63/102 (62%) | 17/24 (71%) |
| contains a quoted line ("..." or “...”) | 7/49 (14%) | 2/38 (5%) | 0/15 (0%) | 9/102 (9%) | 3/24 (12%) |
| uses >=1 emoji | 30/49 (61%) | 24/38 (63%) | 10/15 (67%) | 64/102 (63%) | 0/24 (0%) |
| uses 😭 | 16/49 (33%) | 11/38 (29%) | 3/15 (20%) | 30/102 (29%) | 0/24 (0%) |
| uses 💀 | 8/49 (16%) | 3/38 (8%) | 1/15 (7%) | 12/102 (12%) | 0/24 (0%) |
| uses 💔 or 🥀 | 6/49 (12%) | 1/38 (3%) | 2/15 (13%) | 9/102 (9%) | 0/24 (0%) |
| uses 😂/🤣 | 3/49 (6%) | 2/38 (5%) | 5/15 (33%) | 10/102 (10%) | 0/24 (0%) |
| has hashtags in title | 6/49 (12%) | 25/38 (66%) | 10/15 (67%) | 41/102 (40%) | 2/24 (8%) |
| has ALL-CAPS emphasis word (>=4 letters) | 5/49 (10%) | 11/38 (29%) | 3/15 (20%) | 19/102 (19%) | 1/24 (4%) |
| names a 2nd creator (collab/guest) | 4/49 (8%) | 5/38 (13%) | 2/15 (13%) | 11/102 (11%) | 0/24 (0%) |
| reaction verb (reacts/finds out/hears/discovers) | 5/49 (10%) | 5/38 (13%) | 8/15 (53%) | 18/102 (18%) | 1/24 (4%) |
| suffix '| Joe Bartolozzi' / '|| Joe Bartolozzi' | 17/49 (35%) | 0/38 (0%) | 0/15 (0%) | 17/102 (17%) | 0/24 (0%) |
| states an outcome/claim (not a question) | 47/49 (96%) | 35/38 (92%) | 13/15 (87%) | 95/102 (93%) | 22/24 (92%) |

### Length / duration stats

- Joe Bart clips: median title words (hashtags stripped) 8, median chars 42, median duration 27s, <=20s: 13/49 (27%), 21-40s: 25/49 (51%), >40s: 11/49 (22%), median views 1,672,663, median breakout 27.81x
- Streamer clips: median title words (hashtags stripped) 6.0, median chars 36.0, median duration 47.5s, <=20s: 5/38 (13%), 21-40s: 13/38 (34%), >40s: 20/38 (53%), median views 1,026,245, median breakout 36.855x
- Reaction/commentary: median title words (hashtags stripped) 7, median chars 43, median duration 22s, <=20s: 6/15 (40%), 21-40s: 2/15 (13%), >40s: 7/15 (47%), median views 1,911,583, median breakout 159.72x
- ALL: median title words (hashtags stripped) 7.0, median chars 39.0, median duration 30.0s, <=20s: 24/102 (24%), 21-40s: 40/102 (39%), >40s: 38/102 (37%), median views 1,507,130, median breakout 34.74x
- Certified Bart last 24 titles: median words 10.0, median chars 57.0
- Certified Bart titles containing "Can't Decide"/"Can't Believe": 11/24 (46%)
- Joe-niche outlier titles containing "Can't Decide"/"Can't Believe": 0/49 (0%)
- Joe niche 0-20s: n=13, median views 1,351,784, median breakout 41.31x
- Joe niche 21-40s: n=25, median views 1,986,145, median breakout 18.97x
- Joe niche 41-999s: n=11, median views 1,442,549, median breakout 34.75x

### Posting cadence & hit rate (latest 50 Shorts per channel)

| Channel | Window | Uploads/day | Median views | >=500k views | >=1M views | Max |
|---|---|---:|---:|---:|---:|---:|
| JB Highlights | 2026-08-28 -> 2026-10-15 | 1.04 | 86,301 | 8/50 (16%) | 4/50 (8%) | 5,531,023 |
| JOE CLIPPER | 2026-09-23 -> 2026-10-15 | 2.27 | 511,726 | 25/50 (50%) | 16/50 (32%) | 2,977,198 |
| quikraid | 2026-08-20 -> 2026-10-15 | 0.89 | 38,536 | 5/50 (10%) | 1/50 (2%) | 1,672,663 |
| Certified Bart | 2026-07-06 -> 2026-09-15 | 0.70 | 1,654 | 0/50 (0%) | 0/50 (0%) | 71,384 |


## 2. Patterns

Every count below is MEASURED from the 102 titles or the transcripts above. The "So what" lines are INFERENCE.

### P1. Short, emoji-tagged statement titles beat long descriptive ones (strongest evidence)
- Median outlier title is **7 words / 39 characters** with hashtags removed. The Joe niche median is 8 words / 42 characters.
- Certified Bart's median is **10 words / 57 characters**.
- **64/102 (63%)** outliers have at least one emoji. Certified Bart: **0/24 (0%)**.
- Most common emoji:
  - 😭: 30/102 (Joe niche 16/49)
  - 💀: 12/102
  - 💔 or 🥀: 9/102 (Joe niche 6/49)
  - 😂/🤣: 10/102 (5 of the 15 reaction outliers)
- **95/102 (93%)** titles state an outcome or claim instead of asking a question.
- So what (INFERENCE): emoji and tighter titles are the largest measurable gap between Certified Bart and the outliers. Correlation does not prove the emoji cause the views.

### P2. Two title formats dominate the Joe niche
- **Format A, the caption/quote line plus a "| Joe Bartolozzi" suffix: 16/49 Joe outliers.** These include the #1 video by views ("No biggie we wipe", 10.8M, 105x), "Not that crazy" (5.7M, 62x), "Mcdonalds is not a 5/5" (5.5M) and "Average Discord mod" (2.9M).
  - Used by JB Highlights (31.6k subs) and quikraid (24.3k subs).
  - 7/49 titles are a literal quoted line.
- **Format B, "Joe Bart + verb + specific thing + emoji": 19/49 Joe outliers start with "Joe Bart" (short form).** Examples: "Joe Bart Finds Out what PK means 😂" (6.2M), "Joe Bart Shows Off His CRAZY Stretch Marks 💀" (5.5M), "Joe Bart Takes An Egg To The Back 😭🎯" (4.1M).
- Only **7/49 start with the full "Joe Bartolozzi"**. One of them is the single largest breakout (ATTIC INNCIDENT, 3,434x, from a 1,150-sub channel). The other six are all under 750k views.
- Certified Bart's own phrasing ("Can't Decide" / "Can't Believe") appears in **11/24 of its titles and 0/49 Joe outliers**.
- So what (INFERENCE): switch the default title to Format A or B. Retire "Joe Bartolozzi Can't Decide X or Y".

### P3. Topics that repeatedly break out in the Joe niche
- **Old/cringe/past Joe and "same guy" contrast: 7/49.** Examples: "Who Actually Misses Old Joe Bart?" 8.7M, "Same Person Btw" 5.1M, "No Way Joe Bart Said That" 5.1M, "Prehistoric Joe Bart" 1.4M, old search history 1.1M, search-history trick 2.7M.
- **Named game moment: 7/49.** GTA V first time 1.9M, GTA insider trading 1.5M, Minecraft stronghold 2.4M, musical chairs 5.7M.
- **Another creator named: 6/49.** Deji 9.2M, SypherPK/"PK" 6.2M, Rakai 4.1M, Jynxzi x2, Ludwig/Jynxzi edit 4.9M.
- **Money: 4/49.** Editor salary 2.0M, $1,000 bath bomb 1.0M, won't pay mods 0.4M.
- **Body/gym: 3/49.** Stretch marks 5.5M, gym build 0.7M, Ronnie Coleman 0.7M.
- **Death/news reaction: 3/49.** Dolly Parton passing 1.4M, Grow a Garden creator 0.7M, flat earthers 0.2M. JOE CLIPPER's latest-50 also includes RJ Mitte passing (675k).
- **Food hot take: same clip, 2 outliers.** "McDonald's is not a 5/5" hit 5.5M on JB Highlights (19x) and 968k on quikraid (21x).
- **Same clip on 2+ channels, more examples:** "Joe above you" (JB 494k / quikraid 925k) and "Boy shut the freak up" (JB 685k / quikraid 44.6k).
- So what (INFERENCE): proven clips can be re-cut, and the title/packaging decides the result.

### P4. Streamer-clip and reaction niches lean on hashtags, CAPS and identity claims
- Hashtags in the title: **25/38 streamer-clip and 10/15 reaction outliers, versus 6/49 in the Joe niche**.
- ALL-CAPS emphasis word: 11/38 streamer-clip.
- Identity claims ("is different", "is actually", "meets his match", "Just That Good", "multiversal threat"): **6/102**, but very large ones. Examples: Wolverine Is Just That Good 25.5M (230x), Jynxzi meets his match 5.9M (260x), Ludwig is actually a great teacher 4.7M (229x), Joe Bart is a multiversal threat 4.9M (164x).
- "Reacts to" titles: **15/102**, and **8/15 in the reaction niche**.
- Ranking/top-N compilations: **6/102**. Examples: "Ranking The Funniest Joe Bart Moments" 598k (46x, 2.5k-sub channel), "I Ranked 4 Streamers Moments, The Last One Took Me Out" 981k (834x).

### P5. Length
- Joe-niche median duration is **27s**:
  - 13/49 run 20s or less
  - 25/49 run 21–40s
  - 11/49 run over 40s
- Breakout by length:
  - 20s or less: median breakout **41x**, median views 1.35M
  - 21–40s: **19x**, 1.99M
  - Over 40s: **35x**, 1.44M
- Streamer-clip outliers run longer (median **47.5s**; 20/38 are over 40s). Many Jynxzi Clash Royale and CaseOh Wordle clips run 100–181s.
- The two biggest short ones: "No biggie we wipe" 8s (10.8M) and "Not that crazy" 17s (5.7M).
- So what (INFERENCE): no single length wins. Under 20s gives the highest breakout ratio in the Joe niche. A story or game can run 60s+ when the payoff is late.

### P6. Hooks (MEASURED on 10 transcripts)
- **10/10 start mid-action or mid-sentence**, with no intro, greeting or context line.
- **7/10 open with Joe or the subject speaking a strong line or question**: "Is there anything up there?", "Can you spell recipient?", "Now, I hate to be that guy, but that's a piggy bank", "Are people still playing Grow a Garden? No, dude. That game completely died", "I don't know how to talk to men", "Where is it? [screaming]", "We need like a $500,000 fish".
- **3/10 are setup, then payoff**, and the title quotes the payoff: "Not that crazy" (payoff about 4s in), "No biggie we wipe" (payoff at the end of an 8s clip), "Same Person Btw" (calm, then screaming).
- So what (INFERENCE): cut the first frame to the line, and use the punchline as the title, not a description of the setup.

### P7. Posting cadence (measured on the latest 50 Shorts per channel)
- **JOE CLIPPER: 2.27 uploads/day.** 25/50 reached 500k or more, median 512k.
- **JB Highlights: 1.04/day.** 8/50 reached 500k, median 86k.
- **quikraid: 0.89/day.** 5/50 reached 500k, median 39k.
- **Certified Bart: 0.70/day** over its window, then **0 uploads in the last 30 days**. 0/50 reached 500k, median 1.7k.
- Even the top channels hit 500k on only 10–50% of uploads.
- So what (INFERENCE): outliers come from volume times packaging. Daily posting is the norm for the channels that produce them.

## 3. Ten title templates, ranked by evidence (count = measured supporting outliers in this set)

| Rank | Template | Supporting outliers (measured) | Example from data |
|---|---|---|---|
| 1 | `Joe Bart <verb> <specific thing> <😭/💀/😂>` | 19 start "Joe Bart"; 30 use 😭 | Joe Bart Finds Out what PK means 😂 (6.2M) |
| 2 | `"<exact punchline Joe says>" <💔/😭> \| Joe Bartolozzi` | 16 suffix-format; 7 quoted | "No biggie we wipe" \| Joe Bartolozzi (10.8M, 105x) |
| 3 | `<Short deadpan caption of the moment> <emoji> \| Joe Bartolozzi` | 16 suffix-format, of which about 9 are non-quote captions | Mcdonalds is not a 5/5 💔 (5.5M); Average Discord mod (2.9M) |
| 4 | `<Old/Prehistoric/Same guy> Joe Bart <emoji>` / `No Way Joe Bart Said That 💀` | 7 past/cringe | Who Actually Misses Old Joe Bart? (8.7M) |
| 5 | `Joe Bart & <Other Creator> <did X> TOO Far <emoji>` / `Joe Bart Won't <X> With <Creator> Again 😂` | 6 name another creator (11/102 across niches) | Joe Bart & Deji Took This Spelling Battle TOO Far (9.2M, 245x) |
| 6 | `Joe Bart <first time / discovers> <named game thing> <emoji>` | 7 named-game | Joe Bart Discovers Insider Trading In GTA 5 😭💀 (1.5M) |
| 7 | `<Creator> is <different / actually X / a multiversal threat> <emoji>` | 6 identity-claim (largest breakouts) | Joe Bart is a multiversal threat (4.9M, 164x) |
| 8 | `Joe Bart <CAPS word> <money/body detail> 💀` | 19 CAPS emphasis overall; 4 money; 3 body | Joe Bart Shows Off His CRAZY Stretch Marks 💀 (5.5M) |
| 9 | `Joe Bart Reacts To / Hears About <news or viral thing>` | 15 "reacts" overall; 3 news/death in Joe niche | Joe Bart Hears About Dolly Parton Passing. (1.4M) |
| 10 | `Ranking The Funniest Joe Bart Moments` / `I Ranked N Joe Moments, The Last One…` | 6 ranking compilations | Ranking The Funniest Joe Bart Moments (598k, 46x) |

**Inference / caveats**
- vidIQ breakout and views are point-in-time and are not independent of channel size. Channels under 1k subs produce huge breakout multipliers (for example 3,434x or 2,420x) from a few viral hits.
- Feature counts are correlational. No A/B test was run.
- The hook column covers 10 transcripts only, and the transcripts have no timestamps.
- "Uses 😭" was counted on the raw title. "Starts with creator name" includes "Joe", "Joe Bart" and "Joe Bartolozzi".
