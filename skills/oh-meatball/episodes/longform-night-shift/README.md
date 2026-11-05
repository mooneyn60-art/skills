# Night Shift (house long-form for Sat 11/14 08:00 ET): NOT rendered, NOT scheduled

Script: `scripts/longform-night-shift.json` (70 lines, 966 words, ~5:30). One night in your house, hour by hour:
10 PM silverfish → 11 PM cockroaches → midnight house centipede (the hunter) → 1 AM mouse → 2 AM jumping spider asleep
(release beat) → 3 AM "do you swallow spiders?" (no) → 4 AM bed bugs → 5 AM face mites → 6 AM dust mites (twist: never leave).
Last line hands off to Kill-or-Keep for the end screen.

Built for the long-form reset (research/65) and Nolan's 11/5 asks: full episode, peaks every ~30 s, one Meatball gag per hour
inside the story (flashlight + clock, failed stomp, "employee of the night" trophy, tucking the spider in, face-washing),
no subscribe/like/comment asks mid-video. Every fact has its source listed in its chapter's `_sources`.

Titles for Test & Compare: see `title_candidates` in the script. Thumbnail plan: `thumb_plan`. Pinned comment: `pinned`.

preview-stills.jpg = visual check with placeholder (silent) narration: the real voice (Andrew, edge-tts) can't be generated
from the cloud box, so render it where edge-tts works:
    python3 tools/drawn_keepkill.py build scripts/longform-night-shift.json SPEC.json
    python3 tools/drawn_keepkill.py render SPEC.json OUT.mp4 --work DIR
    python3 tools/lf_gates.py OUT.mp4 --work DIR --spec SPEC.json --sheets DIR
Before posting: fact-check pass on the 5 AM and 6 AM chapters (Demodex and dust-mite sources are named, not yet linked).
