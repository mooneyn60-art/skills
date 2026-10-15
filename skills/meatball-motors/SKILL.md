---
name: meatball-motors
description: Produce "Meatball Motors", an AI-animated sitcom Shorts series about Meatball, an orange cat who sells used cars. Use to write episodes, generate shots with vidIQ (Veo 3.1), assemble, title, and schedule them, and to review performance.
---

# Meatball Motors

## Why this format (evidence: skills/bart-clips/research/06-09)
- Recurring-character AI sitcoms/animal shows are the formats converting views
  into followers in Sept-Oct 2026 (pet sitcom 30.6M reel -> 101K followers in 34
  posts; Cozy Paws avg 2.9M/video; top earners all have a recurring cast).
- Pure templates spike then stall in 60-90 days and are what the 2026
  "inauthentic content" enforcement targets. A named cast, running gags and
  original writing (Nolan's real car-sales life) are the defense.
- vidIQ plan generates Veo 3.1 / Kling / Seedance video at no extra cost.

## Cast (keep descriptions IDENTICAL in every prompt)
- **Meatball**: chubby orange tabby cat, upright, tiny blue polo shirt, gold name
  tag "MEATBALL", slicked-back fur, huge salesman grin, fast-talking excited voice.
  Catchphrase: "What monthly payment are we looking for today?"
- **Biscuit**: nervous golden retriever in a grey hoodie, first-time buyer, says little.
- (later) **The Manager**: stern grey bulldog in a tie who "has to check with" himself.
- Setting: sunny used-car lot, colorful flags, "MEATBALL MOTORS" sign, small red hatchback.
- Style line: "Pixar-style 3D animated comedy, vertical frame, bright cheerful lighting".

## Episode format
- 2 shots x 8 s (veo-3.1-fast, 720p, 9:16, native audio with dialogue) = ~16 s.
- Shot 1 = setup line; shot 2 = punchline. One joke per episode, loopable end.
- Title: `Meatball Motors Ep N: <situation> 😭`; caption ends "#ai #animation #cat".
- Label as AI-generated on every platform (YouTube altered/synthetic, TikTok AI label).
- Joke sources: real dealership moments (payment talk, "let me talk to my manager",
  trade-in lowballs, extended warranty, the test drive, "this deal ends today").

## Pipeline
1. Write episode in `episodes/NNN.json` (shots, prompts, title).
2. Generate each shot with `vidiq_generate_video`; poll `vidiq_job_poll`.
   For consistency, pass a still of Meatball from Ep 1 as an ingredient (veo-3.1, 8 s).
3. Concatenate shots (`vidiq_compose` with keepNativeAudio, or ffmpeg locally).
4. Check frames, then queue/upload. Log credits used per episode in `data/log.csv`.
5. Monday: compare episodes (engaged views, viewed-vs-swiped, subs/1k views); keep
   the jokes and characters that win.
