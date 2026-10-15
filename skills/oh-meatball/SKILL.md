---
name: oh-meatball
description: Produce "Oh Meatball" (@Oh_meatball), an AI-animated cat soap-opera Shorts series. Use to write episodes, generate shots with vidIQ (Veo 3.1), assemble, title and schedule them, keep the cast consistent, and review performance.
---

# Oh Meatball

A soap opera starring a very round orange cat. Every part ends on a cliffhanger.

## Why (evidence: skills/bart-clips/research/06-09)
- Animal soap operas with "Part 1/2/3" episodes are the top Reels trend (5-13M per reel);
  animal emotional stories rank #2 on YouTube; recurring casts convert views into followers.
- YouTube allows "using AI to visualize a unique character and narrative you invented";
  templates and borrowed IP are what get channels hit. Our cast and story are original.

## Cast (copy these descriptions word-for-word into every prompt)
- **Meatball** (lead): a very chubby, round orange tabby cat, upright, tiny black tuxedo and a
  bright red bow tie, fluffy cheeks, big hopeful green eyes. Sweet, dramatic, loves too hard.
- **Duchess**: an elegant fluffy white Persian cat, red scarf (lace veil at the wedding),
  big sunglasses pushed up on her head. Glamorous, secretive.
- **Smokey**: a scruffy grey alley cat with a torn ear and a leather jacket, raspy voice. Duchess's past.
- **Biscuit**: Meatball's loyal best friend, a goofy golden retriever in a grey hoodie.
- **Grandma Shelly**: an old wise tortoise with round glasses; officiant, gossip, narrator.
- Style line: "Pixar-style 3D animated soap-opera drama, vertical frame, warm cinematic lighting".

## Season 1 arc: "The Wedding"
1. The wedding: "If anyone objects..." - Smokey bursts in: "Duchess, tell him the truth!"
2. The truth: Duchess and Smokey were secretly married... and never divorced.
3. Meatball runs off; Biscuit finds him crying into a bowl of spaghetti.
4. Smokey reveals a kitten - "Meet your... nephew?"
5. Grandma Shelly knows a bigger secret about Meatball's own family.
(Extend by comments: whatever viewers argue about most gets the next part.)

## Episode format (UPDATED 2026-10-15: Nolan said parts were bland, "nothing happens")
- 4 shots x 8 s = 32 s per part. Every shot is a BEAT: something happens, someone says a line,
  and at least 2 shots contain a twist/reveal. Each part should cover what used to be 2 parts.
- Shot pattern: 1) fallout/action from last cliffhanger, 2) new scene + new info, 3) escalation,
  4) reveal + cliffhanger + sting. Vary locations and weather (storm, rain, night) for drama.
- Lines: 1-2 short lines per shot, each clearly attributed; comedy beat in at least one shot.

## Breakout rules (research/10 + 11, 2026-10-15; apply to every part from Part 4)
- Frame 0 = the disaster already happening, first line spoken in the first second. No establishing shots.
- Name the cast on screen: finish.py --label puts "MEATBALL" / "DUCHESS" etc. (time it to when that character is the focus) the
  first time they appear in a part. Use #MeatballAndDuchess in every caption.
- Every part has its own payoff (a reveal lands) AND a cliffhanger. Viewers who land on Part 7 first must
  still get a complete beat.
- Spoken call to action one beat before the final reveal, in character (e.g. Biscuit: "Comment who's side
  you're on!"). Rotate wording.
- Pace: ask Veo for 2-3 quick cuts inside each 8 s shot ("cut to close-up of ... then cut to ...").
- Titles: `[Name] [shocking act]… then [twist] 😱 | Oh Meatball Pt N`; score >= 85.
- Plot engine: classic soap tropes (secret child, rich rival, betrayal at the altar, poor-to-rich, amnesia,
  evil twin) with our cast. Happy beats are allowed; the biggest hit in the niche ended happy.
- TikTok earns only on >= 61 s originals: the nightly recap stitches the last 3 parts PLUS one new 8 s
  teaser shot of the next part at the end (new footage = original, and it sells the next part).

## Episode format (original notes)
- 2 shots x 8 s (veo-3.1-fast, 720p, 9:16, native dialogue) = ~16 s; end on a cliffhanger.
- Title: `<hook> 😱 | Oh Meatball Pt N` - score with vidiq_score_title, keep >= 85.
- Description: 1-line recap + "Part N+1 tomorrow" + hashtags `#shorts #catdrama #ai #animation #cat #ohmeatball`.
- Cost: ~255 vidIQ credits per 8 s shot (measured 2026-10-15), ~510 per part.

## Pipeline
1. Write `episodes/NN.json` (two shot prompts, title, description).
2. Generate both shots in parallel (`vidiq_generate_video`), poll `vidiq_job_poll`.
3. Download, check frames + transcribe dialogue (faster-whisper) to confirm lines.
4. `vidiq_compose` both clips (keepNativeAudio) + "PART N+1 TOMORROW" text overlay -> hosted MP4.
5. Post: OpusClip `submit_project` (skipSlicing) -> `schedule_publish` 6 pm ET -> Nolan approves one link.
6. Monday: engaged views, viewed-vs-swiped, subs per 1k views; let comments steer the plot.
