# 64 — YouTube Studio AI data, 11/3 (980 subs): what to make, and the v6 template

Source: Studio AI panels pasted by Nolan 11/3 (28 days) + same-day Studio deep-dives; not re-measured here.

## The data
- **Top sub-gainers are almost all Things Living In Your House**: #8 cockroach without a head (1,343 views, +3),
  #21 house centipede (+2), #5 basement spider hunts black widows (+2), #7 bed bugs (+2), #4 silverfish/books (+2),
  #9 mouse droppings (260 views, +2). Also: "fakes death, smells like a corpse" (+4), ghost crabs, cassowary
  (Would Meatball Survive #1), owl.
- **Best stayed-to-watch (55-63%)**: #6 window spider watching you 63%, #21 house centipede 62%, #1 30-legged hunter
  59%, #8 cockroach 58.5%, #5 basement spider 56%, daddy longlegs 54%.
- **Worst (20-28%)**: every TRUE or FALSE myth-quiz title (porcupine, camel, owl 360, goldfish memory, ostrich).
- **Retention curve**: on every house Short, 15-25% leave between 4.0 and 6.5 s, exactly where the script names or
  describes the creature (jumping spider 107% → 79%). A second cliff when "Subscribe"/"Part X" is said or an outro
  shows (46% → 28%, 35% → 13%). 95%+ of subs come from the Shorts feed; under 1% visit the channel page.
- Animal close-up openings average 58% stayed vs 35% for Meatball/avatar openings. Cuts every 1.5-2.5 s: 68% APV vs
  under 50% for lingering shots. "Tiny monsters in your bed eating your skin" ran 103% APV; honey badger 161%
  (Would Meatball Survive loops best). Winners run 15-30 s; things in YOUR house beat exotic animals. A number in the title: 52.8% vs 33.4% stayed. Series titles get ~2x subs.
- YT 15-20 s: 74.8% APV and 70%+ of subs, vs 48.9% for 30-60 s.
- Subs per 1k views by topic: household pests 1.8, house spiders 1.4, Would Meatball Survive 1.2, exotic 0.7,
  history/myths 0.2.
- Audience peaks weekdays 10:00-15:00 ET, weekends 08:00-13:00 and 14:00-17:00 ET (US, Ireland, UK, Philippines).
  Two Shorts a day 6-8 h apart don't cannibalize; uploads at 9:00-11:30 ET get traction fastest; Tue and Sat are
  the strongest days. Long-form CTR 2.07%; 26-44% leave in the first 12 s.

## Decisions
1. YouTube Shorts are ~80% Things Living In Your House, the rest Is This Spider Venomous? and Would Meatball
   Survive?. Fill YT by topic weight: household pests, house spiders, Would Meatball Survive, then exotic.
2. No TRUE or FALSE / quiz titles or hooks on YouTube. Banned title words: TRUE or FALSE, Myth, Believe, Cartoons,
   Lied, "Did you know". Winning words: Your House, Lives, Spider, Bed, Hunter, Basement, Blood, Survive.
3. Titles: 45-65 characters with the series tag "(Things Living In Your House #N)" or the show tag, a "Your
   [room]" phrase, a concrete number, one creature emoji, a creepy specific fact.
4. "Loop what's working": replacements are sequels of proven winners first (house centipede Part 4, window/
   jumping spider Part 2, cockroach Part 2, dust mites Part 2, bed bugs Part 2, basement spider Part 2, mouse
   Part 2, then a Would Meatball Survive). New sourced facts only; pinned comment "Part 1 is in the Related video."
   November extras after the sequels: stink bugs, Asian lady beetles, boxelder bugs, cluster flies, mice, house
   spiders coming in for winter. Later series idea: "Friend or Foe?".
5. YT cadence: weekdays 10:00 + 16:00 ET, weekends 08:00 + 14:00 ET (second slot ≥6 h after the first). TikTok
   unchanged. `CADENCE` in both scan.py copies.
6. Next long-form (plan for the week of 11/9, not built): "Every Creature Living In Your House, Ranked by Danger",
   16:9, case-file quality, opening straight on creature #1 with no intro bumper.

## The v6 template (supersedes v5; same locked look and Andrew voice)
1. Narration starts at 0.00 s (first voice sample < 0.1 s): no music intro, title card or silent frame.
2. Frame 0 is a big TARS-anatomy animal close-up, already moving at the camera (`open: animal` on the hook).
   Meatball hops in at ~2.3 s, smaller, as the reactor. The middle stays animal-focused.
3. The hook is a visceral, personal threat: "you" + a sourced number where possible.
4. Line 2 (3-7 s) is ACTION or DANGER, never the name, an anatomy list or stats; the animal moves in that beat.
   The name goes in a later line, the title or the caption.
5. No spoken or visual outro (`outro: false`): no Subscribe, Part X, Follow, end card or sign-off. The last line
   flows into the hook's first words, in the hook's room. The comment question is a small top-corner pill during
   the last line (`loop_pill`) and goes in the pinned comment and post text.
6. Every second delivers a new fact or visual; cut every 1.5-2.5 s; a new room each line; big keyword cards in
   seconds 1-4; center-screen word captions (`caption_y: 1180`); yellow key words; -13 dB bed, whoosh on cuts.
7. YT 15-20 s, TT 61-75 s. TikTok gets the same rules (no "Follow for Part X" on screen or spoken; caption only).
8. Gates: outline_lint, vidcheck, beep scan 0, first-voice < 0.1 s, contact sheet reviewed.

## Comment- and search-driven topics (added 11/3)
- "Can 'Mommy Longlegs' Hurt You?" (viewers asked "where is mommy long legs" on the daddy longlegs Short): harvestman
  vs cellar spider vs crane fly, sourced. First in line; pinned comment "You asked where Mommy Longlegs is 👇".
- "What Happens If You Squish a House Centipede?" and "The Bugs Living In Your Bathroom Drain" (drain flies).
- Search demand: carpet beetle larvae in your bed, drain fly vs fruit fly, silverfish damage, brown recluse bite
  signs (CDC/university facts only, "see a doctor" phrasing, no scare claims).
- Community poll: brown recluse (A) vs cellar spider (B), `episodes/community/poll-recluse-vs-cellar.png` + `.txt`.

## TikTok (Metricool, 10/23-11/3)
- Account average (TikTok AI): 207 plays/video, 34.8% 5-s retention, 2.9% finish rate, 0.27% follow rate.
- Breakouts: bombardier beetle 63 s 5,899; house centipede Part 1 66 s 3,308; centipede Part 2 1,037; tarantula
  hawk 839; horned lizard 661; bird broken-wing 22 s 508; ghost crab 21 s 403. The 21-24 s TikToks (10/25) averaged
  ~290 plays; the 60-75 s ones after 10/27 mostly 120-280 (median ~200); case files 86-151.
- Rule: split 50/50 between short loopers (15-25 s, the YT v6 cut, no outro) and 61-65 s Rewards cuts, the long
  ones only for proven series (house centipede, house spiders, cockroach, bed bugs). New TikTok slots alternate
  short and long; slots already holding a long cut keep it. Drop TikTok case-file Shorts except the weekly one.
- Captions open with the creepy fact, the poll goes last; no "Follow Meatball for Part X" (use "Part 1 in my
  playlist").
- 28 days to 11/2 (Nolan's screen recording): 25.2K views, 107 profile views, 14 shares; rewards $0.00 (lifetime
  $0.11). Traffic: For You 79.4%, Search 18.4%, profile 1.4%. 70% male; 25-34 36%, 18-24 29%. US 45.8%, South Africa
  28.0%, Pakistan 6.4%. 9,341 followers, net -58. Rules: the plain search phrase ("house centipede", "spider in
  house", "is it dangerous") leads the caption and shows on screen in the first 2 s; don't stretch weak topics to 61 s
  (Rewards pays ~$0); keep the TikTok queue on-niche (house bugs, spiders, dangerous animals), no random topics.

## Peak-stacking rule (Nolan's reference video, 11/3)
- The old arc (setup, rising action, climax) loses people before it gets good. Start the story at "70 out of 100": the hook sets up the context in the first 5 s.
- Spike to "90" within 5-10 s with a contrarian line or a shocking stat.
- Then re-hook every 20-30 s (peak, release, peak) until the end. No single climax; stack peaks.
- Applies to TikTok long cuts (61-65 s: at least 3 peaks), long-form (a peak every 20-30 s, not every 60-90 s) and what-if simulations (every doubling is a peak).

## Format-first packaging (Nolan's reference, "YouTube automation" strategy video, 11/3)
- Copy a proven FORMAT, not just a niche. Two videos on the same topic get 500 vs 500,000 views because of packaging (title + thumbnail).
- Long-form title formula: Number + Adjective + Topic + Enforcement, in second person ("25 Most Incredible Birds You Must See", "9 Most Shocking Fish You Must See"). Enforcement options: "You Must See", "That Will Shock You", "You Should Never Kill".
- Thumbnail: ONE centered subject that looks real and strange or exotic, plus minimal text.
- Niche bend: take a format already exploding (e.g. the "backyard bird", "Feline" and wildlife compilation channels) and pivot it sideways to an adjacent audience (bugs in your house), where competition is weak.
- Find outliers: channels with low subs, high views and a recent start. vidIQ (free extension is enough) shows the multiplier. Search proven formats: "7 levels of", "your life as", "what if".
- Once a format works, DON'T switch it. The video's example channel died when it left its winning format.
- Applied: the Kill It or Keep It primary title uses the formula; the house series format stays; 3D what-ifs are a separate test, not a replacement.
