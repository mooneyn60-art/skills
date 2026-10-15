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

## Episode format
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
