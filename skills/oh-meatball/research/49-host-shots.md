# 49 · Host shots: Meatball centre-screen, talking to camera (Studio R&D, 2026-10-26)

**Brief (Nolan, 10/26).** "Meatball needs to be in the middle of the screen talking sometimes."
**Answer.** A new shot type: Meatball sits centred behind an investigator's desk, about half the frame tall, faces
the viewer and talks to camera, in front of the case board for that case. It is one beat field (`"host"`), it works in
9:16 and 16:9, and the scaling agent's live tools are untouched: the change is `research/49-host-shots.diff`.
Evidence that the format works: 8 of 16 IG/TikTok outliers in our niche show a presenter on screen (split screen or
talking head, 22-89x their medians; research/50 §2).

## 1. Files
| File | What |
|---|---|
| `research/49-host-shots.diff` | Patch against the live `tools/` (`git apply --check` passes from the repo root): new `tools/host.py`, edits to `tools/v3.py` and `tools/mascot.py` |
| `episodes/host-test/short-northwoods-host.mp4` | Case #2 (Operation Northwoods) with 3 host beats, 23.4 s, 9:16 |
| `episodes/host-test/compare.mp4` | Current tools left, host version right, same audio track (the voice lines and timing are identical) |
| `episodes/host-test/landscape-host.mp4` | A 3-beat 16:9 cut (host, photo, host verdict) to prove the long-form layout |
| `episodes/host-test/frames.jpg` | QA grab: every host moment of the Short |
| `scripts/host-test-northwoods.json`, `scripts/host-test-northwoods-169.json` | The test scripts (the pilot's Northwoods beats with host beats added; the 16:9 cut). Re-render: `episode.py scripts/host-test-northwoods.json host-test --skip-long --no-openloop` after applying the diff |

## 2. What a host beat looks like
- **Framing.** Meatball at frame centre behind a walnut desk; the desk top hides his hips. 9:16: head top about 610 px,
  desk at 1430, size 1280 (46% of the frame height above the desk, ~56% for the whole figure). 16:9: size 860, 55% of
  the height above the desk. His face sits between the comment card (top) and the captions (on the desk), so nothing
  covers it; a verdict stamp on a host beat moves up to 21% of the frame height, above his head.
- **Backdrop: the case board, not the blurred photo.** The blurred photo is how every faceless channel looks; the
  board is ours. It is drawn per Short from the case's own evidence: this beat's photo plus the last two photos shown,
  pinned as polaroids where his body doesn't cover them (the top corners in 9:16, left and right in 16:9), index cards
  (the beat's `board` notes), red string, a 3 px depth-of-field blur, and a warm desk-lamp pool behind his head. The
  desk carries a banker's lamp and a manila case file labelled with the case number; `"fork": true` adds the Fork,
  bagged and tagged "EVIDENCE #?" (research/39 running gag; once per Short at most).
- **Talking.** The rig already lip-syncs: the mouth opens per syllable from the TTS word timings (levels 0-3, eased so
  it never flickers), with blinks and breathing. Host shots add a small talk-bob on open syllables and keep his pupils
  on the viewer.
- **Gestures** (beat `"host": {"moves": ["psst@Wait", "lean@memo"]}`): `you` (points straight at the viewer: the hand
  comes at the camera, drawn big with a fingertip), `psst` (hand cupped by his mouth, head tilted, one brow up),
  `lean` (the camera pushes in 12% and stays), `shrug`, `sweat` (nervous face, sweat drop), `shock`. A `point` line
  with no moves opens on `you` automatically. A bare number after `@` is read as seconds (`psst@1962` fires at
  1,962 s), so time a gesture to a word, not a year. The rest of the line uses the beat's pose for his face (deadpan becomes
  "hands on the desk").
- **Never static.** A host line cuts between a medium shot and a close-up (zoom 1.16 on his face) every `max_shot`
  seconds (1.8 s in the case packs), the camera pushes 2.5%/s throughout, and a whip pan brings us in from the
  previous photo. The v3 gate counts every cut, so host lines still pass "a new picture every 2.5 s".
- **Shot-level host.** `"host"` on one shot instead of the beat cuts from evidence to Meatball inside one line (the
  test's "Wait, it gets worse" beat: host on "Wait, it gets worse. Fake an", then the memo on "airliner").

## 3. Cadence (recommendation)
| Where | Host beats | Why |
|---|---|---|
| **Case Short (20-25 s)** | **2-4**: the guess ask ("Guess." with `you`), the "wait, it gets worse" turn (`psst` or `lean`), the verdict (stamp above him), optionally one aside. Never the hook's frame 0 or the loop tail | Frame 0 must be the evidence and the headline (coldopen.py, loop seam). The ask lines are where he speaks *to* the viewer, so that is where facing the viewer pays off |
| **Deep dive / 60-120 s Short** | One per ~15 s, on each turn, never two in a row | Keeps the evidence on screen most of the time |
| **Long-form (16:9)** | **One per chapter**: the chapter's open or its verdict, plus the cold-open promise after the first evidence shot | Gives the long-form a presenter; host lines alternate medium/close every 3.4 s, so the retention gate (nothing new for over 4 s) still holds |
- Rule of thumb: about 25-35% of a Short's runtime on host shots. More than that and the Short loses the evidence the
  title promised.
- One gesture per host line, two at most. `you` for asks, `psst` for the secret or the twist, `lean` for the verdict.

## 4. QA (this render)
- v3 gate: 40 events in 23.4 s, longest gap 1.67 s, no warnings (the current version: the same 40 / 1.67 s). v4 gate:
  host shots are listed separately ("5 host shots"), not as cut-out fallbacks. The 16:9 cut: 11 events in 8.4 s,
  longest gap 2.62 s.
- Non-host renders are unchanged: every new rig field defaults to the old behaviour (no `hands`, no `extra`).
- Checked frames (`frames.jpg`): face clear of the comment card, the stamp and the captions in every host frame;
  captions sit on the desk and stay readable; no Meatball/animal overlap (host shots have no cut-out).
- 16:9: same layout at 1920x1080 (see `landscape-host.mp4`).
- The 9:16 sample was rendered one revision before the final diff: in the final version the host board also pins
  photos first shown on host shots, and the v4 gate line names host shots. The 16:9 cut was rendered with the final diff.
- Not checked: how it reads at phone size to a real viewer. Nolan should watch `compare.mp4` and say which side he
  prefers.

## 5. Next steps
- **Split-screen host** (the IG/TikTok winner format, research/50 idea 2): the evidence shot in the top 55%, Meatball
  at the desk in the bottom 45%. It reuses `host.desk_img` and the host states; it needs one layout in `host.layout`.
- Mouth shapes beyond open/closed (an "o" for rounded vowels) if the lip-flap reads too simple at host size.
