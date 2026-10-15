# 03 — Own-channel analytics deep-dive: Certified Bart (UCw98RQD81t_339LX5EJqcrg)

Pulled 2026-10-15 via vidIQ owner analytics (YouTube Analytics API). Window: **2026-06-17 → 2026-10-12** (last day with data; 118 days).
Channel at pull time: 943 subs, 304,346 lifetime views, 161 videos (`vidiq_user_channels`).
Credits used: ~540 (6,573 → 6,033). Read-only; nothing was posted, edited or uploaded.

**Legend:** **[M]** = measured (number straight from the API). **[I]** = inference (my interpretation of measured numbers).
**Views note:** since 2026-08-27 YouTube counts views from the first frame. Comparisons across that date use **engagedViews (EV)**.
**Data limit:** the Analytics API exposes no Shorts *impressions* metric. "Near-zero impressions" is approximated by near-zero views and zero `SHORTS` traffic.

---

## 0. Headline findings

1. **[M]** 115,663 of the window's 162,962 engaged views (71%) came in 14 days, **Aug 17–30**. They came from 15 Joe Bartolozzi Shorts uploaded once a day, each 13–25 s long. One Short, *"Roasts People Who Fake Smile at TikToks"* (kuVrpi1LAqQ), produced 48,043 EV, which is 29% of the window.
2. **[M]** The channel has almost no long tail. On days with no new upload (or only a suppressed one), Shorts-feed views fall to near zero the next day. Examples: Jul 21 had 15 views, Sep 4 had 43, Sep 14 had 28. Since Sep 14 the channel has run at about 28 EV/day, and ~85% of that comes from YouTube search (mostly the query "joe bartolozzi").
3. **[M]** The decline started **Aug 25**. kuVr's daily views fell from 2,808 to 564 that day. A second wave from the "Can't Decide" series (loydE-mFTN0) carried Aug 28–29. Cadence then dropped from 1 Short/day to every 2 days in Sep. The last upload (Sep 15, l2JDONwyPqA) has **0 views after 30 days**, and posting stopped.
4. **[M]** Comparing the top 10 and bottom 10 Shorts:
   - Top 10: mean length 21 s, mean average % viewed 100% (people rewatch), engaged/views 59%.
   - Bottom 10: mean length 64 s, mean average % viewed 40%, engaged/views 31%.
   - Bottom-10 viewers swipe away in seconds 4–10: retention falls from ~1.0 to ~0.3–0.5 by the 25% mark.
   - Both groups get 91–95% of views from the Shorts feed, so the difference is retention and not where traffic comes from.
5. **[M]** **709 of the 883 subscribers gained in the window (80%) came from India on Jun 24–Jul 6, against only 436 Indian views.** Subscribers produced 246 of 293,557 views (0.08%). **[I]** This looks like purchased, bot or sub-for-sub subscribers, not organic fans. The subscriber count overstates the real audience.
6. **[M]** At least 15 public Shorts uploaded in the window got fewer than 100 views. Most are re-uploads or near-duplicates of an earlier Short (same title, same clip or same topic). **[I]** This is consistent with duplicate/reused-content filtering, on a channel whose whole premise is clips of another creator.

---

## 1. Daily views / engaged views / subs (Jun 17 – Oct 12)

### 1a. Period summary [M]

| Period | Days | Views | Engaged views | EV/day | Subs gained | Subs lost | Net |
|---|---|---|---|---|---|---|---|
| P1 Jun 17–Jul 24: active posting (74 public Shorts + 1 long; philosophy/grief/Cars, then Joe cruise/DUI clips, 30–90 s) | 38 | 68,600 | 35,008 | 921 | 775 | 33 | +742 |
| P2 Jul 25–Aug 16: **no uploads** | 23 | 776 | 493 | **21** | 0 | 2 | −2 |
| P3 Aug 17–Aug 30: **spike** (15 Joe Shorts, 13–25 s, ~1/day) | 14 | 198,890 | 115,663 | **8,262** | 42 | 17 | +25 |
| P4 Aug 31–Sep 13: taper (8 Shorts + 1 long, every ~1–2 days) | 14 | 23,595 | 10,977 | 784 | 65 | 41 | +24 |
| P5 Sep 14–Oct 12: dormant (1 upload, which got 0 views) | 29 | 1,698 | 821 | **28** | 1 | 1 | 0 |
| **Total** | 118 | 293,559 | 162,962 | 1,381 | 883 | 94 | +789 |

### 1b. Spike days and the videos behind them [M]

| Date | Views | EV | Subs | What drove it (video daily data / upload log) |
|---|---|---|---|---|
| Jun 19 | 3,508 | 1,712 | 3 | 3 uploads (0GUYgE3S7Oo, HK7gOOAq0a0, kt_RxTa8tBo), each ~800–900 views |
| Jun 26 | 3,416 | 2,222 | 86 | 5 uploads, **plus 1,161 EXT_URL views on a private 14 s video (lEmGGPDRMNs, avg % viewed 5.5%)** **[I] probably embedded or bought traffic** |
| Jul 2 | 4,639 | 1,860 | 63 | 4 Mater/Cars Shorts uploaded (EMdDVgGGZYo, G6ApszPEPMU, 9-rqa5hoKd0, mrN5HFRjqsM) |
| Jul 9 | 4,384 | 2,394 | 4 | 3 Joe uploads (QA5JQyrLPR4 2,530 views, 1hYlud5YXJ0, xAwpbGfPfrQ); search spiked to 220 |
| Aug 17 | 3,742 | 1,972 | 0 | Restart after 23 dead days: ikoqOSTbH08 (HOA) + -3J0fPFZc8g (AI sob story) |
| **Aug 19** | **31,988** | **18,338** | 7 | kuVr day 2 (10,515 views) + v9uqILXmXN4 (diabetes fan, 22k lifetime) + zsHgPAeqQM8 |
| **Aug 22** | **24,009** | **15,266** | 5 | **kuVr peak day: 17,166 views / 11,611 EV** + vMnZ8kBdLRY (Godfather) |
| Aug 24 | 22,531 | 11,791 | 7 | vYI6xQk3hNU ($50K charities, 20.9k) + 2qzaMqfy6Jg + kuVr tail (2,808) |
| Aug 28–29 | 12,079 / 15,346 | 6,809 / 8,616 | 1 / 1 | loydE-mFTN0 "Can't Decide Erase Worst Memory" (24.1k lifetime); search jumped to 1,613 / 1,296 views/day |
| Sep 4–6 | 1,416 / 640 / 2,905 | 233 / 167 / 1,179 | 9 / 21 / 32 | **2,524 ADVERTISING views (only 382 EV)** going to the long-form HNHO_0wmbJg. Subs lost 3 / 12 / 21 in the same days. **[I] A paid promotion that brought low-quality subscribers who churned** |

**kuVrpi1LAqQ lifecycle [M]:** daily views were 11,452 (Aug 18), 10,515, 9,844, 10,948, **17,166 (Aug 22)**, 6,401, 2,808, 564 (Aug 25), then 340–460/day to Aug 28, under 100/day from Aug 30, and under 10/day from Sep 2. **A breakout Short lasted about 7 days.**

### 1c. Upload cadence vs Shorts-feed traffic [M]
- Days with zero or near-zero `SHORTS` traffic: Jul 4 (183), Jul 5 (41), Jul 12 (80), Jul 21 (15), Jul 26–Aug 16 (≤10/day), Sep 4 (43), Sep 5 (31), Sep 7 (18), Sep 14+ (≤12/day).
  - Each of these is a day with no upload, or with only an upload that got under 15 views. Jul 4–5 had exUewaJ3Nt8 (62 views), hNOFR1bofB4 (10) and GPv8kNCvvJ0 (13).
- YouTube search is the only source that persists. It ran 7–67 views/day through the dead stretches. The top search term in the window was "joe bartolozzi" with 8,672 views (other terms: "joe bart cruise" 293, "joe bartolozzi cruise" 219, "joe bart iron man mask" 170).
- **[I]** The feed treats each Short as a 1–2 day test. Growth depends on a steady daily cadence, and any gap resets distribution to near zero.

### 1d. When and why the decline started [M + I]
1. **Aug 25 [M]:** kuVr fell from 2,808 to 564 views/day. Total EV dropped from 11,791 (Aug 24) to 5,990 (Aug 25), then 2,306 (Aug 26). **No upload on Aug 26 [M]**, the first skipped day since Aug 17.
2. **Aug 30 – Sep 3 [M]:** the "Can't Decide" follow-ups (F7dkVdsJ61A 971 EV, gXVIEcIfnjs 705 EV) and the Sep 1–3 uploads got only 700–2,250 EV each. **[I]** The series format had saturated: the same "Joe Bartolozzi Can't Decide X or Y" template appeared 6 times in 8 days.
3. **Sep 3 onward [M]:** cadence dropped to every 2 days (Sep 3, 6, 8, 10, 12, 15). Shorts traffic fell to ~0 on every off day.
4. **Sep 15 [M]:** l2JDONwyPqA ("Gambling Quits & Goat Dilemmas #shorts", 37 s, no tags) has 0 views every day through Oct 13 (vidIQ video_stats) and does not appear in Analytics at all. No uploads since. **[I]** Either the upload was blocked or filtered (gambling topic, or a reused clip), or it never became eligible for the feed. In either case the channel has received no new test traffic since Sep 13.

---

## 2. Top 10 vs bottom 10 Shorts

Selection: public Shorts published in the window. Top 10 = highest EV. Bottom 10 = lowest EV among Shorts with ≥100 views; the near-zero ones are covered in §5.
Retention values are YouTube `audienceWatchRatio` at 1% / 25% / 50% / 75% / 100% of runtime. Values above 1.0 mean rewatches or looping.
"Other page" = `YT_OTHER_PAGE`, the closest the API gets to browse. Traffic shares are of the video's views in the window.

### 2a. Per-video table [M]

| Title (truncated) | Len | Views | EV | EV/views | Avg dur | Avg % viewed | Retention 1/25/50/75/100% | Shorts feed | Search | Other page | Subs per 1k views | Likes/EV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **TOP 10** | | | | | | | | | | | | |
| Roasts People Who Fake Smile at TikToks | 21s | 71,380 | 48,043 | 67% | 18s | 89% | 1.40/1.13/0.94/0.76/0.42 | 92.8% | 3.8% | 2.8% | 0.21 | 3.5% |
| Can't Decide Erase Worst Memory or Relive Best | 25s | 24,145 | 13,759 | 57% | 25s | 100% | 1.63/1.25/0.98/0.80/0.65 | 83.8% | **13.3%** | 2.3% | 0.08 | **5.5%** |
| Comforts Fan Who Has Type 1 Diabetes | 23s | 22,077 | 11,959 | 54% | 18s | 81% | 1.53/1.03/0.74/0.63/0.56 | 93.2% | 3.4% | 2.9% | 0.09 | 2.6% |
| Drops $50K on Charities Chat Picked | 17s | 20,854 | 10,594 | 51% | 20s | 121% | 1.84/1.52/1.15/1.00/0.88 | 93.4% | 4.2% | 2.2% | 0.14 | 1.7% |
| Can't Believe Haaland Goals Look Like Ai | 20s | 13,059 | 7,164 | 55% | 20s | 102% | 1.73/1.26/1.01/0.85/0.75 | 94.2% | 3.6% | 1.9% | **0.54** | 2.1% |
| Can't Believe Everyone Picks The Godfather | 19s | 8,444 | 4,159 | 49% | 20s | 109% | 1.76/1.36/1.10/0.93/0.73 | 86.1% | 10.6% | 2.8% | 0.24 | 3.7% |
| Roasts People Who LARP as Him on TikTok | 24s | 5,911 | 3,606 | 61% | 21s | 91% | 1.55/1.20/0.89/0.66/0.56 | 89.5% | 6.9% | 2.1% | 0.17 | 2.2% |
| Roasts a Drug Dealer Who Thought He Did Coke | 22s | 6,360 | 3,455 | 54% | 19s | 89% | 1.62/1.23/0.77/0.66/0.59 | 94.7% | 2.5% | 2.2% | 0.16 | 2.6% |
| Neighbor Shot at His Cats… HOA Twist | 21s | 5,784 | 3,014 | 52% | 20s | 97% | 1.64/1.18/0.92/0.78/0.68 | 88.7% | 6.5% | 4.1% | 0.00 | 2.3% |
| Can't Believe He Doesn't Care About the Past | 22s | 5,805 | 2,955 | 51% | 26s | **122%** | 1.91/1.46/1.18/1.04/0.94 | 93.2% | 3.0% | 3.0% | 0.17 | 2.0% |
| **BOTTOM 10** | | | | | | | | | | | | |
| The Farmer's Burden: More Than Just Crops | 67s | 216 | 72 | 33% | 21s | 32% | 1.08/0.43/0.25/0.14/0.10 | 96.3% | 0.5% | 2.8% | 0.00 | 1.4% |
| Are You Trapped in the Marketplace? | 67s | 130 | 89 | 68% | 18s | 27% | 1.08/0.29/0.16/0.12/0.07 | 82.3% | 0.8% | 14.6% | 0.00 | 0.0% |
| Joe Bartolozzi Exposes Disney's Mater Conspiracy | 52s | 429 | 97 | 23% | 23s | 45% | 1.20/0.55/0.34/0.31/0.22 | 94.9% | 2.8% | 1.2% | 0.00 | 4.1% |
| Find Hope Within: Thoreau's Wisdom | 65s | 502 | 113 | 23% | 15s | 24% | 1.04/0.27/0.12/0.07/0.04 | 96.0% | 0.2% | 3.6% | 0.00 | 0.9% |
| Money Buys Stress Relief, Not Happiness | 86s | 300 | 139 | 46% | 16s | 19% | 1.02/0.24/0.09/0.05/0.02 | 93.3% | 0.3% | 5.3% | 0.00 | 2.2% |
| Mater's Unexplained God Power | 72s | 721 | 179 | 25% | 39s | 54% | 1.36/0.57/0.45/0.39/0.36 | 96.8% | 1.9% | 0.8% | 0.00 | 2.2% |
| Are There Humans in the Cars Universe? | 67s | 878 | 237 | 27% | 29s | 45% | 1.31/0.48/0.35/0.33/0.29 | 95.7% | 2.5% | 1.4% | 0.00 | 3.8% |
| The Emotional Reality of Hospice Care | 52s | 668 | 239 | 36% | 17s | 35% | 1.16/0.37/0.22/0.18/0.15 | 94.0% | 0.7% | 4.8% | 1.50 | 1.7% |
| Joe Bartolozzi Can't Handle This Cars Pixar Theory | 67s | 865 | 280 | 32% | 30s | 45% | 1.28/0.47/0.37/0.35/0.30 | 95.7% | 2.7% | 1.3% | 1.16 | 1.8% |
| Drunk Driver Chugs Whiskey During Traffic Stop | 44s | 989 | 304 | 31% | 31s | 71% | 1.52/0.77/0.63/0.57/0.53 | 95.3% | 2.5% | 1.8% | 0.00 | 2.6% |

### 2b. Cohort aggregates [M]

| Metric | Top 10 | Bottom 10 |
|---|---|---|
| Mean length | **21.4 s** | **63.9 s** |
| Total views / EV | 183,819 / 108,708 | 5,698 / 1,749 |
| EV ÷ views (share of viewers who stay past the first moments) | **59%** | **31%** |
| Mean average view duration | 20.7 s | 23.9 s |
| Mean average % viewed | **100%** | **40%** |
| Mean retention at 1 / 25 / 50 / 75 / 100% | 1.66 / 1.26 / 0.97 / 0.81 / 0.67 | 1.21 / 0.44 / 0.30 / 0.25 / 0.21 |
| Traffic: Shorts feed / search / other page / channel / subscriber | 91.4% / 5.4% / 2.6% / 0.2% / 0.17% | 95.1% / 1.8% / 2.5% / 0.4% / 0.04% |
| Subs gained per 1k views | 0.18 (33 subs) | 0.35 (2 subs; sample too small) |
| Likes per EV | 3.25% | 2.23% |

### 2c. Where people swipe away [M + I]
- **Bottom 10 [M]:** every curve has a cliff between **5% and 20% of runtime**. For a 65–86 s Short that is seconds 4–13.
  - LX4S3gFb3w4: 1.00 → 0.43 between 5% and 12% (≈ s 4–10).
  - OVpkRWU6Y8Q: 1.03 → 0.54 between 7% and 12%.
  - euQBufZpYw4: 1.01 → 0.48 between 7% and 15%.
  - qYwYb9lZ7bE: 1.00 → 0.67 between 7% and 12%.
  - **[I]** These are long podcast-style opinion clips with no hook. Viewers leave as soon as they realise the clip is a monologue.
- **Top 10 [M]:** curves start at 1.4–1.9 (heavy looping) and decline smoothly with no early cliff. The largest drops are mid-clip (zsHg: 1.25 → 0.77 between 24% and 50%) or at the payoff/end (kuVr: 0.56 → 0.46 between 90% and 94%; vMnZ: 0.79 → 0.75 at 94–95%).
  - Four of the 10 are still at or above 0.88 at 100% (vYI6 0.88, 9vNK 0.94). **[I]** Viewers loop short clips that end on the punchline.
- **[I]** Traffic mix does not separate winners from losers: both cohorts are about 90–95% Shorts feed. What differs is how many feed testers stay. The feed then scales the winners: top-10 Shorts got 5k–66k feed views, while bottom-10 Shorts stopped at 100–950.

---

## 3. Audience (Jun 17 – Oct 14) [M]

### 3a. Age × gender (viewerPercentage)

| Age | Male | Female | User-specified | Total |
|---|---|---|---|---|
| 13–17 | 22.6% | 2.4% | 0.3% | 25.3% |
| 18–24 | 18.6% | 1.5% | 0.1% | 20.2% |
| **25–34** | **31.5%** | 2.5% | 0.4% | **34.4%** |
| 35–44 | 9.5% | 1.7% | 0 | 11.2% |
| 45–54 | 5.1% | 1.3% | 0 | 6.4% |
| 55–64 | 1.4% | 0.2% | – | 1.6% |
| 65+ | 0.6% | 0.1% | – | 0.7% |
| **Gender total** | **89.3%** | **9.7%** | 0.8% | |

**[I]** The audience is overwhelmingly male and aged 13–34 (91% of signed-in viewers fall in 13–44). A quarter are under 18, which matters for ad suitability and topic choice (drugs, gambling).

### 3b. Countries (views, top 15)

| Country | Views | EV | Share of views | Avg dur |
|---|---|---|---|---|
| US | 187,897 | 105,685 | 64.0% | 21s |
| GB | 17,788 | 10,025 | 6.1% | 21s |
| CA | 17,723 | 10,030 | 6.0% | 21s |
| AU | 7,295 | 4,252 | 2.5% | 23s |
| DE | 5,857 | 2,905 | 2.0% | 24s |
| NL | 3,300 | 1,774 | 1.1% | 19s |
| SE | 2,954 | 1,646 | 1.0% | 24s |
| IN | 2,532 | 1,371 | 0.9% | 17s |
| IE | 1,937 | 1,085 | 0.7% | 21s |
| PL | 1,850 | 1,004 | 0.6% | 23s |
| ZA, NO, DK, PH, NZ | 1,616 / 1,536 / 1,513 / 1,490 / 1,285 | | 0.4–0.6% each | |

The US, UK, Canada and Australia together account for 78.6% of views.

### 3c. Devices

| Device | Views | Share | Avg % viewed |
|---|---|---|---|
| Mobile | 224,570 | 76.5% | 64.4% |
| Desktop | 33,727 | 11.5% | 73.1% |
| TV | 17,692 | 6.0% | **83.5%** |
| Tablet | 17,340 | 5.9% | 64.8% |

### 3d. Format and subscriber status
- Shorts: 289,846 views / 161,391 EV (98.7%). Long-form: 3,717 views / 1,571 EV (1.3%).
- Subscribed viewers: **246 views (0.08%)**, avg % viewed 36.5%. Unsubscribed viewers: 293,311 views, avg % viewed 66.9%.

### 3e. Subscriber-quality red flag [M + I]
- **[M]** Jun 24–Jul 6: **India +709 subs on 436 views**. No other country in the result gained subs in that span, and Indian views over the whole window were only 0.9% of total. Daily subs ran 58–96/day from Jun 25 to Jul 5 while views were 81–4,639/day. Per-video attribution for that span shows at most 1 sub on any video.
- **[M]** Sep 4–6: +62 / −36 subs while 2,524 ADVERTISING views ran (engaged rate 15%).
- **[I]** About 80% of the window's gained subscribers are probably inorganic. They do not watch: 0.08% of views come from subscribers. They may hurt the channel, because uploads pushed to the subscriber feed get no response. The organic subscribe rate from content is about 0.1–0.2 subs per 1k views.

---

## 4. Which title, topic and length features go with high EV and retention

Dataset: 98 public Shorts published Jun 17–Sep 15. Analytics from Jun 17 to Oct 14.

| Segment | n | Median EV | Mean EV | Median avg % viewed (≥100 views) | n with <100 views |
|---|---|---|---|---|---|
| All | 98 | 456 | 1,610 | 49% | 15 |
| Era A Jun 17–Jul 7: philosophy/grief/Cars monologues, mostly no "Joe" | 49 | 379 | 310 | 43% | 9 |
| Era B Jul 8–24: Joe cruise/DUI "Reacts to…", 30–90 s | 25 | 524 | 637 | 49% | 5 |
| **Era C Aug 17–Sep 15: Joe clips, 13–25 s** | 24 | **2,166** | **5,277** | **96%** | 1 |
| Length ≤25 s | 24 | 2,166 | 5,299 | 94% | 0 |
| Length 26–45 s | 27 | 406 | 562 | 54% | 7 |
| Length 46–60 s | 7 | 328 | 283 | 41% | 1 |
| Length >60 s | 40 | 396 | 335 | 41% | 7 |
| Title includes "Joe"/"Bartolozzi" | 49 | 902 | 2,900 | 81% | 7 |
| Title without Joe | 49 | 379 | 320 | 44% | 8 |
| "Can't Decide X or Y" series | 6 | 1,727 | 3,585 | 99% | 0 |
| "Can't Believe …" (Era C) | 5 | 3,014 | 3,688 | 102% | 0 |
| "Roasts …" | 3 | 3,606 | 18,368 | 89% | 0 |
| "Reacts to …" (Era B) | 10 | 548 | 803 | 67% | 3 |
| Title includes "#shorts" | 61 | 396 | 357 | 45% | 11 |
| No "#shorts" | 37 | 1,309 | 3,674 | 89% | 4 |

Correlations across the 83 Shorts with ≥100 views [M]:
- log(EV) vs average % viewed: **r = +0.76**
- log(EV) vs length: **r = −0.60**
- average % viewed vs length: **r = −0.78**
- log(EV) vs title length: r = +0.39

What this means:
- **[I]** Length, era, the "Joe" name and dropping "#shorts" are almost perfectly confounded, because they all changed together on Aug 17. The defensible conclusion is that **sub-25 s, single-beat Joe clips with near-100% average % viewed** are what the feed rewards. The "#shorts" tag has no causal effect; it is a marker of the older, longer content.
- **[I]** Topic signals within Era C:
  - The best performers have a **relatable "people who…" roast or a surprising-number hook**: Fake Smile 48k EV, $50K Charities 10.6k, Diabetes Fan 12k.
  - Or a **"would you rather" dilemma** (Erase Worst Memory, 13.8k), which also pulled the most search (13.3%) and the most likes per EV (5.5%).
  - Repeating a template decays fast. "Can't Decide" went 2,622 → 1,364 → 13,759 → 2,090 → 971 → 705 EV over consecutive uploads.
- **[M]** Search demand is real but narrow: "joe bartolozzi" alone drove 8,672 search views. Evergreen topical keywords also pull search: "the godfather reaction" 135 + "godfather reaction" 56, "one chip challenge" 82, "joe bart iron man mask" 170.

---

## 5. Duplicate / reused-content suppression signals

Public Shorts with near-zero lifetime distribution. Views are window analytics plus vidIQ/Data API lifetime counts.

| Video | Published | Views | Likely duplicate of (views) | Signal |
|---|---|---|---|---|
| l2JDONwyPqA "Gambling Quits & Goat Dilemmas" | Sep 15 | **0** (30 days of 0 in video_stats; absent from Analytics) | n/a; gambling topic, no tags | **[M]** total non-distribution |
| UjId8-CKsTc "Coping with the Death of Loved Ones" | Jun 20 | **0** | kt_RxTa8tBo, **identical title**, uploaded the previous day (872) | **[M]** |
| 7zrrQZ-ttmg "Reacts to Drunk Driver Who Forgot How to Talk" | Jul 19 | 69 | M9Oq-WkgDnM, **identical title and tags**, Jul 17 (1,605) | **[M]** |
| AwPmol1ovb8 "Joe & Friends Try Scorpion Shots" | Jul 8 | 4 | dqfPml2exF0 "$40 Scorpion Shot Challenge" (1,046) | **[M]** views; **[I]** same footage |
| OUMZU2Y3seg "Experiencing Loss at Different Ages" | Jun 21 | 1 | ugoOYSvArVk / Cm-44gLsVRE / mcEK8LXpnVY (same "grief at different ages" clip) | **[M/I]** |
| mcEK8LXpnVY "Evolving Emotions of Grief Through Childhood" | Jul 1 | 6 | Cm-44gLsVRE "Childhood Grief … Different Ages" (805) | **[M/I]** |
| SKXSSVZNoiM "Money, Happiness, and Stress Explained" | Jun 26 | 1 | LX4S3gFb3w4 / xGC2YP9RanE (money ≠ happiness) | **[M/I]** |
| hNOFR1bofB4 "Mater Is a Demi-God" | Jul 4 | 10 | mrN5HFRjqsM "Mater's God Power" / G6ApszPEPMU (721 / 972) | **[M/I]** |
| GPv8kNCvvJ0 "Proves Cars Are Dinosaurs" | Jul 5 | 13 | W5QA0m17LMc "Cars: Evolution or Intelligent Design" (866) | **[M/I]** |
| 8x2W6A8sgJA "Almost Cries Talking About His Grandpa" | Jul 12 | 53 | 7yWyjyxiXao / dqVKgavJmQc / LA2-CSqbaOU (grandpa clip, 3+ prior cuts) | **[M/I]** |
| 3bvFLakPG28 "Most Unhinged Bar Ever" | Jul 15 | 3 | cruise-bar footage also in d083ZWnkNkY | **[I]** |
| -CPghbhJHQw "Reacts to Jack Pembrook's Swinger Setup" | Jul 14 | 21 | contains a third creator's vlog footage | **[I]** reused third-party content |
| Fb4w1Zpj8yk "Stop 'Rise and Grind' Madness" | Jun 27 | 2 | productivity monologue series (YqCRSjU8ZJg, K1AICHSIJXY) | **[I]** |
| exUewaJ3Nt8 "Solitude…", OhRqsp_yyqs "Zyns in Iceland" | Jul 4 / Jun 30 | 62 / 33 | off-niche monologues | weak distribution |
| Pre-window: tLiJy0SHQyw (cheating, 4th+ version), WbZPTYtLR1o (Boltzmann, duplicate of MY_8KU_kyCM 945), uqfoROdNOvE (Popper, 12; the later re-upload cBNLs4BMLXs got 933), LTAi1VidI1I, ylclGRZG0sk, Wct3JLJ-_UQ | Jun 5–13 | 0–32 | multiple re-cuts of the same topics | **[M]** views |

Pattern [M]:
- **15 of 98** public Shorts in the window got fewer than 100 views. Six of them are exact or near-exact title or topic repeats of a Short posted 1–14 days earlier.
- In Era A, Shorts that were accepted got a remarkably uniform **~750–970 views** each (e.g. 805, 826, 849, 850, 872, 887, 896, 910, 915, 928, 932, 933). Shorts that were not accepted got **0–13**. There is almost nothing in between.

[I] What the pattern suggests:
- The bimodal "~850 or ~0" split looks like an eligibility gate before the feed's seed test, not a test that was tried and failed. That matches YouTube's duplicate and reused-content filtering.
- The risk is structural: the channel republishes another creator's stream footage. Repeated re-uploads of the same clip probably raise channel-level "reused content" scrutiny. That would explain the Sep 15 Short getting 0 views and the channel's search-only floor since.
- Not measured: Studio-only signals such as copyright or Content ID claims and the "reused content" monetization review. Check them in YouTube Studio for l2JDONwyPqA and UjId8-CKsTc.

---

## 6. Other anomalies worth knowing [M]
- **Jun 26 EXT_URL burst:** 1,161 external views and 1,160 EV in one day on lEmGGPDRMNs. That video is now private, is a "long" video only 14 s long, and has an average % viewed of 5.46%. Organic external traffic is otherwise 0–11/day. **[I]** Probably an embed autoplay or a bought-views source.
- **Advertising Sep 3–7:** 2,524 views, of which only 382 were engaged (15%). Average view duration was 87 s against a 5:23 runtime (27% viewed) on HNHO_0wmbJg. Subscribers churned in the same days (−36).

## 7. Methods and gaps
- Tools: `vidiq_channel_analytics` (day, video, traffic source by day and per video, retention curves per video, age/gender, country, device, content type, subscribed status, search terms, country of subs for the anomaly windows), `vidiq_user_videos` (3 pages, 148 uploads back to May 29), `vidiq_video_stats` (l2JDONwyPqA).
- Not run, to stay inside the ~700-credit budget: `vidiq_subscriber_insights`, `vidiq_comment_insights` (niche-wide, not channel-specific), and per-video retention/traffic for Shorts outside the top/bottom 10.
- No impressions or CTR for Shorts are available via the API. Suppression is inferred from near-zero views and zero Shorts-feed traffic.
