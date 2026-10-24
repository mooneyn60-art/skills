# 41 — Meatball 2.0 rig (The Animator, 2026-10-24)

**Brief (Nolan).** "Something about the way the meatball moves throws me off. He's our main character, we need to treat him like it." Then: "Make him bigger, make him take more control of the videos, not just the corners," and "see how the stickmen are animated and mimic it" (research/41-stickman-reference.md).
**Answer in one line.** Meatball is now a jointed rig that acts pose to pose: he hits a pose on a stressed word, holds it, eases to the next, breathes, blinks and lip-syncs. In Shorts he is the host of the video, framed by a shot grammar (show / host / together / close-up / card) instead of a sticker in the corner. His drawing (head art, colours, line widths, proportions) is unchanged.

Files: `research/41-animator/compare.mp4` (OLD | NEW, Meatball alone, then the same lines as a vertical Short from each explainer), `research/41-animator/contact.png` (2 s of consecutive frames at 8 fps, OLD row and NEW row), `research/41-animator/short-contact.png` (the rig-test Short, one frame every 0.5 s), `episodes/rig-test/short-tiger.mp4` (the pilot tiger Short rendered with the new rig).

## 1. What was wrong (from frames of current renders)
| Problem | Cause in the old code |
|---|---|
| Arms teleport between unrelated poses every 1-2 frames | `_gesture` flicked both hands on every word with offsets quantized to 8 units; the `SWAP` map switched to a second pose every 2.2 s with no in-between |
| Gestures don't match the line (shocked hands-on-head on a calm sentence) | The beat's pose was held for the whole line, whatever the words said |
| Face twitches | The mouth toggled open/closed every 0.11 s regardless of syllables |
| Dead from the waist down | Fixed straight legs, no breathing, no weight |
| Choppy | 15 fps frames overlaid on a 30 fps video (every frame shown twice) |
| Tiny in Shorts | 12-25% of the frame, a corner sticker over the photo |

## 2. What changed
**Rig (tools/mascot.py).** A skeleton: hip, knees (two-bone IK, feet planted), spine, shoulders, head on a neck pivot. Each arm has shoulder / elbow / wrist angles with fixed bone lengths, so every pose is on-model. Hands that must touch something (think: chin; shock: cheeks; facepalm: eyes; nervous: clasped) are IK targets on the head or chest, so they stay put while the head tilts or he breathes. Body params: torso lean, head tilt, knee bend, shoulder shrug, breath. Drawing is supersampled 2x (smoother edges, sub-pixel motion); the art itself is the same code as before.
**Poses** (angle sets): neutral (relaxed rest), point (toward the photo), present (open palm toward the photo), shrug, think, shock, laugh, facepalm, wave, plus the Showrunner's deadpan and nervous. Each pose also sets the face (brow shape, base mouth, eyes) and gaze (viewer, content, up).
**Motion.** Keypose events blend with an eased in-out curve that dips slightly before moving (anticipation) and overshoots a few percent before settling, 7 frames for a gesture and 8 to enter or settle at 30 fps. The torso and head follow the hands 2 frames later over a gentler curve (overlapping action). Big moves (shock, shrug, wave, laugh) start with a small knee crouch; realization moves (shock, laugh) land with a 7% scale-pop.
**Acting plan (deterministic per beat seed).** The beat's `pose` is the primary acting choice. He starts each line relaxed, eases into the primary pose just before the first word, and settles back to rest after the last word, so every line begins and ends on the same frame (no jumps at cuts, exact Short loop seam). Extra gestures happen only on emphasis words (ALL CAPS, a capital mid-sentence, stress words like *every / never / exactly / not*, numbers, the word before a pause = punctuation), at most one per 1.5 s, and every pose is held at least ~1 s. Reaction poses are short: shock holds ~1.2 s and then he presents the photo, laugh and wave ~1.5 s. Persona poses (deadpan, nervous, think, facepalm) hold for the whole line; the face is the joke, and emphasis only adds a tiny head nod. Long stretches without a stressed word relax to rest after ~2 s.
**Life.** Breathing: 1.6 px at any size, a whole number of cycles per line (period ~3-4 s), so it is zero at both ends. Blinks every 2.5-5 s (half, closed, half: 3 frames), never on the first or last frames. Pupils look at the photo while pointing or presenting, up while thinking, at the viewer otherwise and on "you / your / yourself". Nervous hands rub slowly; wave waves.
**Face.** Expressions snap between clean drawings and never morph: every face now has eyebrows (calm dashes, raised arcs, worry slants, cross, the deadpan lids), laugh uses closed-arc "bliss" eyes, and `draw(..., eyes="x")` gives defeated X eyes for thumbnails.
**Lip-sync.** From the edge-tts word timings already passed in: each word is split into syllables (vowel groups); each syllable opens to a level set by its vowel (a/o open, e/u mid, i small) for 70% of its span and closes. The level moves at most one step per frame, so 0 -> open goes through mid: eased, no random flicker. Shock keeps its "o" and laugh its grin, scaled by the same levels.
**Rendering.** 30 fps (was 15). Frames render in 2 worker processes (`MEATBALL_JOBS`). A 26.7 s Short takes about 5.5 minutes on this loaded 4-CPU box.
**Emotion glow.** White rim by default. A beat's `"glow": "yellow" | "red" | "green"` adds a soft coloured halo (warning / danger / good) that fades in and out with the line; reveals that open on "True" glow green automatically.

**Shot grammar (tools/explainer.py, vertical Shorts, classic style).** Each picture picks a framing from its content, alternating so the framing changes every ~1.5-3 s. A photo shot longer than 2.6 s is split on the word nearest its middle into two framings of the same photo.
| Framing | When | Meatball | Photo | Captions |
|---|---|---|---|---|
| show | frame 0 and the loop tail (the animal must be clear), then alternating | ~42% tall, entering lower-left, cut at the waist, pointing/presenting, soft drop shadow | full-bleed, sharp, slow push | lower third, right of his head |
| host | alternates with show | 60-75% tall, centred-left, white rim | full-bleed, blurred and dimmed | lower third, over his body, never his face |
| together | nervous or shock lines on a photo | full figure ~45% tall standing in the scene beside the animal, drop shadow | full-bleed, sharp | lower third |
| close | lines with no picture (persona punchlines) | face and upper body fill the frame, slow push-in on his face | off-white | lower third over his torso; aside top-right; the Fork stands at the right edge |
| card | text and quiz cards | text cards: ~52% tall under the text; quiz cards keep the old size so the quiz photo and countdown stay clear | | none on cards |
`"frame": "show|host|together|close|card"` on a beat or a shot overrides the choice. Long-form (16:9) keeps the photo panel beside Meatball at ~58% of the frame height and uses the close-up for lines with no picture. The punch style is unchanged.

**Other changes.** `overlay_mascot` composites full-frame transparent 30 fps frames (one continuous performance can cut between framings) and burns the captions on top of him. The quiz countdown carries the think pose across its three segments (`enter`/`exit` flags) instead of re-entering it each second.

## 3. How Meatball moves (guide for all future work)
1. **Pose to pose.** Pick the beat's `pose` for what the line *means*, not for its first word. Shock is for real shock only; for a calm fact use point or present.
2. **Gestures land on stressed words.** If a word must get a gesture, write it in CAPS ("Please do NOT test this") or end the clause on it. Never more than one gesture per ~1.5 s.
3. **Hold.** Every pose is held at least a second. Stillness is a choice, not a bug: deadpan and nervous lines hold one pose the whole line.
4. **Every line starts and ends at rest.** This is what makes cuts and the Short loop seamless. Don't add motion at line ends.
5. **Life is small.** Breathing is 1.6 px; blinks are 3 frames; the pupils move. No bobbing, bouncing or shaking (Nolan, research/39).
6. **The face snaps.** Change expression by pose, never per frame. The mouth only moves with syllables.
7. **He is the host.** In Shorts he fills 40-75% of the frame; the corner sticker is gone. Use `frame` overrides only when a picture needs it (e.g. `together` when the photo has empty ground beside the animal).
8. **Glow sparingly.** Red for danger, green for true, yellow for warning; at most one or two lines per Short.
9. **Check by frames.** After any change, run `tools/mascot_test.py` and look at consecutive frames: no limb may move more than a few degrees between two frames except inside a 7-8 frame transition.
10. **Keep the design.** Head art, colours, line widths and proportions live in `_head_base`, `_face`, `LIMB`, `HAND_R` and the bone lengths. Don't touch them for animation reasons.

## 4. Remaining limitations
- **Stroke width vs the reference.** The stickman reference uses 6-8 px strokes at 1080 wide. Meatball keeps his own proportional line width (26/1000 of his size), so at host and close-up sizes his limbs are 35-65 px thick. Changing that would change the design, which the brief forbids; it is a decision for Nolan.
- **No walk cycle, no grabbing props.** The Fork is still a still prop drawn in the background.
- **Emphasis is guessed from text and timing.** edge-tts gives no stress or punctuation, so emphasis comes from capitals, a stress-word list, pauses and word length. A beat can't yet name its gesture word explicitly (a future `"hit": "word"` field).
- **Together shots don't know the photo.** He always stands lower-left; on a photo where the animal is lower-left he overlaps it. Use `"frame": "host"` or a different `crop` there.
- **Close-ups at very large sizes render without supersampling** (cost), so the head outline is slightly stair-stepped at 2570 px; it reads fine on a phone.
- **Render cost.** ~16 ms of drawing per frame plus PNG I/O; a 26.7 s Short takes ~5.5 min on this shared box.
- **Thumbnails changed slightly.** `draw()` stills now use the rig poses (same art, consistent with the video) and calm faces have eyebrows. Thumbnail tools crop `draw()` output at fixed coordinates; their poses still fit those crops, but re-check a thumbnail before the next upload.
- **Watermark check is manual.** The pilot's hook photo (iNaturalist obs 368498398) carries "© Wilmot Snaratne 2023 Photography" in its lower-left corner. The rig-test script drops the blurry stripe crop that showed it and shifts the hook crop to [0.22, 0, 0.68, 1] so the text is out of frame; the same fix is applied to `scripts/pilot-showrunner.json` in this copy.
