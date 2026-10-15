---
name: off-the-lot
description: Run "Off The Lot", a Shorts/TikTok/Reels channel where a working car salesman explains what dealers don't tell buyers. Use to script, render, schedule and review Off The Lot videos, or to answer questions about the brand, series, pipeline and launch plan.
---

# Off The Lot

**Promise:** "A car salesman tells you what the dealer won't."
Evidence: research/05 in `skills/bart-clips/research/05_clean_start_niches.md`
(car buying tips +166%, car dealer +86%, competition 37-50; dealership
ad-channels get views but no subs; first-person expertise is the strongest
defense against the 2026 originality/reused-content rules).

## Brand
- Name: Off The Lot. Handle: @OffTheLot (fallbacks @OffTheLotTalk, @OffTheLotCars).
- Look: asphalt black `#111214`, sticker yellow `#FFD400`, white `#F5F5F0`,
  grey `#8A8D93`. Heavy sans captions, centred. Logo = "OFF THE LOT" wordmark
  with a yellow underline that doubles as the progress bar.
- Host: Nolan's real voice, anonymous. No face, no store name, no customer
  data, no real deal jackets. Tone: deadpan, insider, slightly guilty
  ("this is the part where I'm supposed to say..."). Never trash buyers.
- Every description: "Not financial or legal advice. Prices/rates are examples."

## Series (rotate; each is numbered so people binge)
1. **Dealer Trick #N** - one tactic, the math, the fix. (anchor series)
2. **Finance Office Menu** - one add-on (GAP, paint protection, VSC, etching): what it costs dealers vs what you pay, when it's worth it.
3. **Payment Math** - a common deal run through the calculator on screen.
4. **Ask the Salesman** - answer a real comment (reply-to-comment Short).
5. **Salesman Life** - relatable floor stories, shift humor (reach + subs).
Ratio for the first month: 3 Dealer Trick, 1 Finance Office, 1 Payment Math,
1 Ask, 1 Salesman Life per week.

## Packaging rules (from Certified Bart data + niche outliers)
- 20-35 s. Second 0 = the claim ("I'm a car salesman. Watch for the 4 boxes.").
- Titles ~7 words, one emoji, a number or "salesman" in it.
- One idea per Short. On-screen numbers must be computed, never guessed.
- End: "Follow. Dealer Trick #N+1 tomorrow." Post daily, no gap days.

## Pipeline (who does what)
1. **Claude, daily:** pick topic (backlog + vidIQ rising keywords + comments),
   write the script as `shorts/NNN-slug.json` (voiceover lines + scenes),
   compute all math in code.
2. **Nolan, ~2 min:** read the voiceover lines into a phone voice memo and send
   it (or later: approve his cloned voice from VoiceStudio for bulk lines).
3. **Claude:** `python scripts/render_short.py shorts/NNN.json -o NNN.mp4 --audio memo.m4a`,
   check frames, fix timing to the voice.
4. **Post:** YouTube + TikTok + Reels as clean native uploads (no watermarks).
   Until a direct posting route exists, Nolan uploads the finished file (1 min)
   or approves the OpusClip link.
5. **Monday review:** engaged views, viewed-vs-swiped, subs per 1k views per
   series; double down on the best series; log in ruflo memory namespace `off-the-lot`.

## Money (realistic order)
1. Lead-gen from day one: "Want me to look over your deal? Link in bio" (free
   form; later paid deal reviews). Check dealership policy first.
2. Affiliates once there's traffic: credit score, insurance comparison, car-buying services.
3. Long-form "full deal breakdown" 1-2x/month (higher RPM, search traffic).
4. YouTube Partner Program after 1,000 subs + views threshold.

## Risks
- Employer: read the dealership's social-media / non-disparagement policy, or stay fully anonymous.
- Facts: rates, fees and laws vary by state; say "usually" / "in most states" and keep math examples labelled.
- Synthetic voice: disclose in YouTube's altered-content setting if a cloned voice is used.
