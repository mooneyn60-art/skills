# The Studio playbook

Desk id: `studio`. Absorbs: Producer, Animator. Read this before every run and append lessons after.

## Read first
- research/41 stickman reference
- research/41-animator (rig notes, when merged)
- research/23 Shorts length and loops
- OPERATIONS.md opening rules

## Rules (proven)
- Shorts v2: frame 0 is a full-screen moving photo; claim as fact; cut every 3 s or less; no quiz card or countdown; seamless loop.
- Long-form: animals on screen in the first 30 s, each as it is named; myth #1 by 25 s.
- Meatball fills 40-70% of the frame (HOST/SHOW shots) and full-frame close-ups on punchlines; captions in the lower third, never on his face.
- Motion: rigid limbs with hinge joints, pose-to-pose holds of 1-2 s, eased transitions, faces that snap between clean expressions, a 1-3 px idle bob; no teleporting arms.
- Render long jobs in the background and resume with --skip-existing; check frames before handing off; watch disk space (keep 5 GB free).

## KPIs this desk owns
- GATE WARNs per render
- Seam diff
- Render failures

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
- 2026-10-24: Premium voice path tested. vidIQ voiceover (premium voices; 14 credits per 1,000 characters, rounded up per call), then faster-whisper base.en for word timings (cached model).
  - Decode the MP3 with ffmpeg to 16 kHz mono float first; PyAV's `open()` breaks the built-in loader.
  - Whisper gives clean per-word start and end times, which is enough for captions and lip-sync.
  - Generate ONE call per Short or script (not per beat: rounding makes per-beat calls cost 14 each), then split it into beats by matching words.
