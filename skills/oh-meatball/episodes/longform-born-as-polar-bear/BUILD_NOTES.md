# Polar bear long-form: build notes

Builder: the opus build agent, night of 11/13 (started 02:20 ET; stop and report by 06:15 ET).

## Files
- tools/drawn_polarlife.py: format layer (imports drawn_catlife for the meter, chips, chapter cards, voice cache, music, loudness, line sheets; changes nothing in it).
- tools/drawn_pb_art.py: the pictures (polar bear, seal, seabird, den, ice, shore, Churchill, motel, truck, stick figures, boards, Meatball's parka).
- tools/drawn_pb_shots.py: one shot per line (s<seg>.l<line>).
- scripts/longform-born-as-polar-bear.json: the build spec (from the outline).
- Scratch: /dev/shm/polar-build/ (work dirs, frames). Voice cache: episodes/longform-born-as-polar-bear/.voice-cache (git-ignored).

## Commands (from skills/oh-meatball)
- python3 tools/drawn_polarlife.py build scripts/longform-born-as-polar-bear.outline.json scripts/longform-born-as-polar-bear.json
- python3 tools/drawn_polarlife.py linesheet scripts/longform-born-as-polar-bear.json episodes/longform-born-as-polar-bear/lines-contact.jpg --work /dev/shm/polar-build/lines
- python3 tools/drawn_polarlife.py render scripts/longform-born-as-polar-bear.json episodes/longform-born-as-polar-bear/born-as-polar-bear.mp4 --work /dev/shm/polar-build/render

## Progress
- [x] art module (tools/drawn_pb_art.py)
- [x] shots table (tools/drawn_pb_shots.py, 102 lines)
- [x] format layer + spec built; says and cards proved equal to the outline (102 lines, 1,850 words)
- [x] voice all lines (cache filled)
- [x] line sheets looked at, first round of fixes (maps, dial numbers, card overlaps, swim water colour)
- [x] thumbnails pb_a, pb_b, pb_c (+ _168) in episodes/thumbs-bornas, specs appended
- [x] titles.txt, pinned_comment.txt
- [x] full render: 10:30.0, 1920x1080, 47 MB (renders in about 6.5 min on 4 cores)
- [x] gates (tools/lf_gates.py --lufs -14 --max-mb 95 --end-hold 12): size, beep scan, loudness, file size, first voice
      pass; the shots gate (no framing over 4 s) failed on s8.l5 only, fixed with five pushes per still board
- [x] voice check (faster-whisper small.en on the whole mp4, aligned per line id; then each flagged line
      transcribed alone from the mix): every line heard to its end, no line missed. Respelled for the voice only
      (captions keep `say`): s2.l1 "four-teen", s4.l3 "did hiz swim" (the plain "his" was heard "a"), s1.l6
      "leg-room" (heard "legron"), s0.l4 "Her fast, can go" (a comma only; "fast can" ran together as "fasting").
      Remaining notes are numbers heard as digits ("12", "687", "400", "%") and kilometre/kilometer spellings.
- [x] every20s.jpg, first60-every2s.jpg, lines-contact-1..4.jpg in this folder (looked at; fixes above)
- [x] description (chapter times from the render), pinned comment, titles

## How to resume
Read this file, then run the next unchecked step. Nothing here needs the earlier session's memory.

## What was fixed on the way (11/13 night)
- Beep gate: the take of s2.l1 says "fourteen" with an "ee" near 2.5 kHz that the gate flags (the same in every
  take: edge-tts is deterministic). Respelled for the voice only: TTS "four-teen" (captions keep "fourteen").
  The sound effect "zap" on s7.l1 also tripped the gate: now "thud".
- Loudness: one more pass at a -2.5 dBTP ceiling after the cat layer's pass (true peak had landed at -0.9).
- drawn.plan carries an actor's p, rot and flip over from the last line when the id and type match: every actor
  id is now made unique per line (drawn_pb_shots.table), and every Meatball key the parka wrapper reads is set on
  every line.
- Word anchors with a hyphen ("air-conditioned", "old-age") crash drawn.at_time: use another word of the line.

## State at stop (11/13, about 04:40 ET)
Everything in the brief is built: mp4 10:30.1, gates pass (lf_gates: size, beep 0, -14.0 LUFS / -1.7 dBTP,
48.4 MB, first voice 0.01 s, longest framing 3.74 s). Nothing committed (agents make no git writes).
Known small things left, none blocking: s0.l3 the eight chips sit over the den roof; s0.l4 the bowls strip sits
just under the card; s2.l7 the two-year bar is small; the Arctic map is a schematic ring of land round the sea.
