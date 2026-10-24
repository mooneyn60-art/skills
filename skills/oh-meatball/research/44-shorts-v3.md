# 44 — Shorts v3: Meatball in jeopardy (Studio + Showrunner, 2026-10-24)

**Brief (Nolan).** The content "lowkey is boring and sucks". The data agrees: our best Short (Sharks in the River, 29 s) keeps ~100% to 5 s, then falls from 70% to 40% between 5 and 13 s, ending at 8%. relativeRetentionPerformance is ≈0.19. The hook works. The middle (a still photo plus a calm narrator explaining) does not.
**Answer in one line.** Every Short is now a little disaster that happens *to* Meatball: he approaches the animal, it goes wrong, and the true fact lands as the punchline. The camera never stops (push, whip pans, punch-ins, shake, flash), small SFX sit under the voice, and lines are 8 words or fewer, ~10% faster.

**Status: prototype for Nolan's review. Nothing is posted and nothing in the live `tools/` is changed.** The code lives in a scratch copy. The unified diff is in section 6 (also `episodes/v3-proto/tools-v3.diff`), ready for the Mayor to merge after Nolan approves.

## 1. Files
| File | What |
|---|---|
| `episodes/v3-proto/short-cassowary.mp4` | v3 cassowary, **24.9 s** |
| `episodes/v3-proto/short-boxjelly.mp4` | v3 box jellyfish, **22.2 s** |
| `episodes/v3-proto/short-badger.mp4` | v3 honey badger, **24.7 s** |
| `episodes/v3-proto/compare.mp4` | 1080x960 side by side: old survive-01 cassowary (left, 37.3 s) vs v3 (right). It plays twice: pass 1 with the old audio, pass 2 with the v3 audio (labels say which side is audible) |
| `episodes/v3-proto/script-v3-proto.json` | the 3 rewritten scripts with sources (= `scripts/v3-proto.json` in the copy) |
| `episodes/v3-proto/grab-*.jpg` | frame grabs (below) |
| `episodes/v3-proto/sfx/` | the SFX kit + `LICENSE.txt` (Kenney CC0 + ffmpeg-synthesized); the merge copies it to `sfx/` |
| `episodes/v3-proto/tools-v3.diff` | the code change (same as section 6) |
| `episodes/v3-proto/release.json`, `credits.txt` | titles, descriptions, pinned comments and photo credits, if Nolan wants to post them |

Durations follow the coordinator's live data from 10/24: 20-22 s Shorts win (daddy longlegs 20 s: 733 views in 3 h; elephant 22 s: 877), and 43 s+ flopped. The first cassowary cut was 29.7 s. Two lines came out ("On each foot.", "It jumps seven feet straight up.") and two lines got shorter. No joke was cut.

## 2. What changed (v2 → v3)
| | v2 (survive-01) | v3 |
|---|---|---|
| Story | Meatball narrates facts, then a pun card | Cause and effect: hook claim → he tries something ("So naturally, I went to say hi.") → it goes wrong (kicked, stung, flung) → the true fact is the punchline → twist/callback ("Best case? I become a tree." / "I'm a pickle now." / "I evolved sauce.") |
| Meatball | Talking, gesturing host | Action moves on top of the talking rig: **run in / run across / run off, launch with a spin arc, tumble and land with squash, tremble, peek in from the frame edge, cower, hit reaction with head squash and stretch and X eyes, puff up when stung and deflate**. He moves in every line |
| Camera | Slow Ken Burns per picture, hard cuts | Slow push always (4.5%/s, never still, also across cuts); **whip pans** (6 frames with horizontal motion blur) on every cut to a new photo; **punch-in** to 118% on key words (from the word timestamps); **screen shake + 3-frame white flash** on hits; pop-in word labels ("4 INCHES", "31 MPH", "0 BRAINS", "PICKLE") |
| Cuts | ≤3 s gate | ≤2.5 s gate (longest real shot: 2.37 s); a long shot is re-cut to a tighter crop of the same photo |
| Sound | Music bed + one "tink" | Music bed + 1-2 SFX per line (whoosh, boing, crunch, pop, record scratch, splash, thud, zap, tink), mixed 5-10 dB under the voice |
| Writing | 10-20 word lines, about 1 joke per 5-8 s | ≤8 words per line; about 12 lines per Short; a joke, escalation or reveal every ~2-4 s; never more than 1 line of explaining in a row |
| Pace | +4% voice, 0.35 s between lines | +10% (atempo, timestamps scaled), 0.12 s between lines, lines cut on the last word instead of the TTS file's trailing silence |
| Ask | Spoken comment ask on 5/10 | Cassowary + box jellyfish end on "Would you…? Comment." before the loop line; badger ends on the twist. Never in the first 3 s |
| Loop | Hook photo zoom matches frame 0 | Same; Meatball peeks in on frame 1+ and slides out on the last frames, so the first and last frames are the same picture (measured mean pixel difference 1.9-2.5/255 = encoder noise) |

**Tension with research/39, said plainly.** The show bible said "no shakes, zooms, SFX"; Nolan rejected the 10/23 "punch" style as "too much". v3 brings motion back, with three differences from punch: the motion is *story* (something happens to Meatball), the voice stays calm and deadpan (the persona survives: "I don't have a heart", "I evolved sauce"), and SFX stay under the voice. If Nolan finds it too much, the cheapest dials are in `tools/v3.py`: `GAIN` (SFX level), `punch_z` (0.18 → 0.10), and the whip-pan blur.

## 3. Frame grabs
- Old v2 cassowary, 1 frame every 3-4 s: `episodes/v3-proto/grab-old-cassowary.jpg`. The same photo for long stretches, Meatball standing.
- v3, 1 frame per second: `grab-cassowary-1fps.jpg`, `grab-boxjelly-1fps.jpg`, `grab-badger-1fps.jpg`.
- The kick, 12 consecutive frames: `grab-cassowary-kick.jpg`. Hit → head squash, white flash (3 frames) + shake → flung up and right, spinning, X eyes.
- The sting, 12 consecutive frames: `grab-boxjelly-sting.jpg`. Zap, flash, his head swells to 1.5x and trembles.
- One frame of compare.mp4 at 10 s: `grab-compare.jpg`.

## 4. The scripts (lines as spoken; sources in the script file)
**Cassowary (24.9 s).** "This bird has a four-inch dagger." *(peeks in, trembling; 4 INCHES pops)* / "So naturally, I went to say hi." *(runs in)* / "It runs thirty-one miles an hour." *(he flees across the frame; 31 MPH)* / "I can roll. Downhill. Sometimes." *(tumbles in, thud)* / "One kick can slice open a threat." *(KICK: crunch, flash, shake, launched spinning)* / "Good news: it mostly eats fruit." *(falls back in, boing)* / "Bad news: it swallows fruit whole." *(the Fork drops in, tink)* / "I'm round. I'm bite-sized." *(head squash, X eyes)* / "Its poop plants rainforests." / "Best case? I become a tree." *(record scratch)* / "Would you get this close? Comment." / loop: "Never say hi. Because" → "This bird has…".
Facts: San Diego Zoo cassowary page (claw up to 4 in; one kick can slice open a threat; 31 mph; seeds sprout better after passing through a cassowary); Mental Floss (mostly fruit, swallowed whole).

**Box jellyfish (22.2 s).** "This jellyfish has twenty-four eyes." / "And zero brains." / "So I jumped in to outsmart it." *(splash)* / "It doesn't need a brain." / "Its tentacles are covered in stingers." / "One brushed me. Just once." *(zap, flash, head puffs up)* / "One kind can stop a heart in minutes." / "Good news: I don't have a heart." *(deflates, pop)* / "Australian first aid is vinegar." / "A meatball. In vinegar." / "I'm a pickle now." / "Would you swim there? Comment." / loop: "Four of them are watching you. Because" → "This jellyfish…".
Facts: Garm et al. 2011 (24 eyes, four always look up); Scientific American (no real brain); Chironex fleckeri can kill in 2-5 min (Fenner 2005, via Wikipedia); ANZCOR guideline 9.4.5 (vinegar, then call 000). The bonus/description gives the full first-aid line. Photos are other box jellyfish, as in survive-01.

**Honey badger (24.7 s).** "This badger is built to resist cobra venom." / "A tiny change blocks part of the toxin." / "So, obviously, I poked it." *(runs in)* / "It eats snakes. Scorpions. Bee larvae." *(3 cuts)* / "It rips open beehives for snacks." / "It did not want to be friends." *(crunch, flash, launched)* / "Its skin is thick and super loose." *(tumbles back)* / "Grab it, and it twists around inside." *(hit reaction)* / "I'll be over here. Forever." *(cowers)* / "Hedgehogs evolved the same trick." / "I evolved sauce." *(Fork + tink)* / loop: "Anyway. Don't poke it. Because" → "This badger…".
Facts: Drabeck, Dean & Jansa 2015 (receptor change; hedgehogs, pigs, mongooses); the wording rule holds ("resist", "blocks part of", never "immune"); Wikipedia/Honey badger (loose skin lets it twist; raids beehives for larvae; eats snakes and scorpions).

## 5. Self-check (tools: 1 fps contact sheets, frame-difference scan, voice/SFX level scan)
| Check | Cassowary | Box jelly | Badger | Pass? |
|---|---|---|---|---|
| Something new at least every 3 s (cuts, punch-ins, SFX, acts, labels from the render gate) | 45 events, longest gap 2.05 s | 46, 2.13 s | 47, 1.80 s | yes |
| Longest shot | 2.17 s | 2.37 s | 2.23 s | yes (≤2.5) |
| Longest run of near-identical frames (mean diff < 0.4/255) | 0.27 s | 0.20 s | 0.23 s | yes (no still frame) |
| Meatball moves in every shot | an action move on every line (peek, run, tumble, launch, shake, hit, puff, hide); "stand" lines still gesture and lip-sync | same | same | yes, checked on the 1 fps sheets |
| SFX under the voice | SFX peak −10.5 dBFS vs voice peak −5.2 dBFS; per event, SFX RMS sits 0.6-12 dB under the voice around it, except one record scratch (+2.6 dB) that lands in a pause | peak −12.4 vs −6.8 | peak −10.5 vs −6.5 | yes. The first pass had the scratch and boing 5-9 dB over the voice, so I cut them from 0.30 to 0.20 and 0.22 |
| Loop seam (frame 0 vs last frame) | 1.9/255 | 2.1/255 | 2.5/255 | yes |
| Lines ≤ 8 words; no ask in the first 3 s | yes | yes | yes | yes |
Fixed during the check: music was silently missing (v3 imported a fresh `explainer` module, so the bed path wasn't set; the path is now passed in). Captions overlapped for one frame between cards. A 3.2 s loop tail is now re-cut. Meatball moved from 32% to 24% of the frame width so he covers less of the animal. Trailing TTS silence is trimmed.

## 6. Code changes (copy's `tools/` vs repo `tools/`, unified diff)
How it plugs in: `"style": "v3"` in a script → `explainer.py` hands the build to the new `tools/v3.py` (all other styles render exactly as before). `episode.py --skip-long` passes `tempo` through and lets a hook set `loop_sfx`. `mascot.py` gains `feet` and `head_s` rig parameters (unused by old callers, so their output is unchanged), `act_track()` (action moves) and `apply_run()` (stride). `make_sfx.py` rebuilds `sfx/` from the Kenney packs.
To merge: apply the diff, copy `episodes/v3-proto/sfx/` to `sfx/`, and copy `episodes/v3-proto/script-v3-proto.json` to `scripts/`. Render with `tools/episode.py scripts/v3-proto.json <slug> --skip-long`; it takes about 2-3 min per Short on this box with `MEATBALL_JOBS=2`.

```diff
diff -u a/tools/episode.py b/tools/episode.py
--- a/tools/episode.py
+++ b/tools/episode.py
@@ -62,6 +62,7 @@
     h = beats[0]
     first = explainer.shots(h)[0]
     tail = {"say": h["loop_say"], "pose": h.get("pose", "deadpan"), "myth": h.get("myth"), "loop": True,
+            **({"sfx": h["loop_sfx"]} if h.get("loop_sfx") else {}),
             "bleed": h.get("bleed"), "shots": [{k: v for k, v in first.items() if k in explainer.VISUAL}]}
     return beats + [tail]
 
@@ -152,6 +153,7 @@
         json.dump({"voice": spec.get("voice", "en-US-AndrewNeural"), "rate": spec.get("short_rate", "+8%"),
                    "music": spec.get("music"), "style": spec.get("style"),
                    **({"pitch": spec["pitch"]} if spec.get("pitch") else {}),
+                   **({"tempo": spec["tempo"]} if spec.get("tempo") else {}),  # v3: atempo speed-up
                    # "short_beats" lets a joke-dense script keep more than 3 hand-picked beats (default 3).
                    "beats": hook_loop(mb) if hook else loop(tighten(mb, spec.get("short_beats", 3)))},
                   open(sspec, "w"))
diff -u a/tools/explainer.py b/tools/explainer.py
--- a/tools/explainer.py
+++ b/tools/explainer.py
@@ -952,6 +952,9 @@
         MUSIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", spec["music"])
     if a.vertical:
         vertical()
+    if spec.get("style") == "v3" and a.stage == "build":  # Shorts v3 (research/44): tools/v3.py renders it
+        import v3
+        return v3.build(spec, a.work, a.out, MUSIC)  # v3 imports explainer afresh: pass the bed
     if a.stage == "images":
         images(spec["beats"], a.work, a.seeds)
     else:
diff -u a/tools/mascot.py b/tools/mascot.py
--- a/tools/mascot.py
+++ b/tools/mascot.py
@@ -108,18 +108,19 @@
 
 
 def body(p):
-    """Joint positions for body params p (lean, tilt, knee, shrug, breath, hip_x)."""
+    """Joint positions for body params p (lean, tilt, knee, shrug, breath, hip_x; v3 "feet" = moved feet)."""
     hip = (HIP[0] + p.get("hip_x", 0.0), HIP[1] + p.get("knee", 0.0))
+    feet = p.get("feet") or FEET
     knees = []
-    for side, foot in ((-1, FEET[0]), (1, FEET[1])):
-        half = math.dist(HIP, foot) / 2
+    for side, foot in ((-1, feet[0]), (1, feet[1])):
+        half = max(math.dist(HIP, FEET[0]), math.dist(hip, foot) + 2) / 2
         s, e = _ik(foot, hip, half, half, -side, 1)  # knees bend outward; zero bend = the old straight legs
         knees.append(_add(foot, _dir(-side, s), half))
     lean, b = p.get("lean", 0.0), p.get("breath", 0.0)
     top = _add(hip, _rot((0, -(SPINE_UP + b)), lean))
     sh = _add(hip, _rot((0, -(SHOULDER_UP + b + p.get("shrug", 0.0))), lean))
     head = _add(top, _rot((0, -HEAD_UP), lean + p.get("tilt", 0.0)))
-    return {"hip": hip, "knees": knees, "top": top, "sh": sh, "head": head}
+    return {"hip": hip, "knees": knees, "top": top, "sh": sh, "head": head, "feet": feet}
 
 
 def arm_angles(spec, side, j, content=CONTENT):
@@ -283,8 +284,10 @@
     k = size / 1000.0
     j = body(st)
     hands = [arm_points(j, side, st[key])[2] for side, key in ((-1, "l"), (1, "r"))]
-    xs = [p[0] for p in hands + [j["sh"], j["hip"]] + list(FEET) + j["knees"]] + [j["head"][0] - 240, j["head"][0] + 240]
-    ys = [p[1] for p in hands + list(FEET)] + [j["head"][1] - 250, j["head"][1] + 170]
+    hs = max(st.get("head_s", (1.0, 1.0)))  # v3 squash/stretch and puff can grow the head
+    xs = [p[0] for p in hands + [j["sh"], j["hip"]] + list(j["feet"]) + j["knees"]] + [j["head"][0] - 240 * hs,
+                                                                                      j["head"][0] + 240 * hs]
+    ys = [p[1] for p in hands + list(j["feet"])] + [j["head"][1] - 250 * hs - 100 * (hs - 1), j["head"][1] + 170]
     box = [min(xs) - 40, min(ys) - 40, max(xs) + 40, max(ys) + 40]
     if canvas is None:
         origin, box_px = (0.0, 0.0), (0, 0, size, size)
@@ -297,13 +300,17 @@
     im = Image.new("RGBA", ((box_px[2] - box_px[0]) * ss, (box_px[3] - box_px[1]) * ss), (0, 0, 0, 0))
     pen = _Pen(im, kk, ((box_px[0] - origin[0]) / k, (box_px[1] - origin[1]) / k))
     pen.line(j["top"], j["hip"])                                   # spine
-    for knee, foot in zip(j["knees"], FEET):                       # legs
+    for knee, foot in zip(j["knees"], j["feet"]):                  # legs
         pen.line(j["hip"], knee)
         pen.line(knee, foot)
     tilt = st.get("lean", 0.0) + st.get("tilt", 0.0)
     head = _head_layer(round(kk, 4), st["mouth"], st["brow"], st.get("look", (0, 0)), st.get("level", 0),
                        st.get("blink", 0), st.get("eyes"))
     pivot = (-HEAD_BOX[0] * kk, (-HEAD_BOX[1] + HEAD_UP) * kk)    # the spine top, in layer pixels
+    sx, sy = st.get("head_s", (1.0, 1.0))
+    if abs(sx - 1) > 0.01 or abs(sy - 1) > 0.01:  # v3: squash/stretch about the neck (hits, stings)
+        head = head.resize((max(1, int(head.width * sx)), max(1, int(head.height * sy))), Image.BICUBIC)
+        pivot = (pivot[0] * sx, pivot[1] * sy)
     if abs(tilt) > 0.05:
         head = head.rotate(-tilt, resample=Image.BICUBIC, center=pivot)
     top = pen.p(*j["top"])
@@ -692,6 +699,140 @@
     return len(jobs)
 
 
+# ---------------------------------------------------------------- v3 action moves (research/44)
+# Shorts v3 puts Meatball in jeopardy: things happen TO him. An action move is a per-frame body transform
+# laid over the talking rig (lip-sync, face, blinks stay): where his hip is on screen, a rotation, a body
+# squash, a head squash/puff, running legs, a tremble, and face overrides (X eyes when hit).
+ACTS = ("stand", "run_in", "run_off", "run_across", "launch", "tumble", "shake", "peek", "hide", "hit", "puff",
+        "puffed", "deflate", "loop_out")
+JITTER = {"shake": 9.0, "peek": 4.0, "hide": 8.0, "puff": 6.0, "puffed": 6.0}  # tremble amplitude, drawing units
+
+
+def _clamp01(u):
+    return min(max(u, 0.0), 1.0)
+
+
+def _squash(f):
+    """Impact squash and stretch over frames since the hit: flat, tall, settle (sx, sy)."""
+    seq = [(1.32, 0.68), (1.28, 0.72), (0.86, 1.18), (0.9, 1.14), (1.06, 0.95), (1.03, 0.98)]
+    return seq[f] if 0 <= f < len(seq) else (1.0, 1.0)
+
+
+def act_track(act, n, fps, t_act=0.25, home=0.5, seed=0):
+    """Per-frame transform of an action move for a line of n frames. t_act = the impact / start moment (s).
+    Each entry: x (hip position as a fraction of frame width; <0 or >1 is off-screen), y (drawing units,
+    + = down), rot (degrees, + = clockwise), body (sx, sy), head (sx, sy), run (stride phase or None),
+    flip (faces left), eyes / pose overrides, jitter (tremble amplitude)."""
+    rng = random.Random(f"act|{act}|{seed}")
+    ph = rng.uniform(0, 6.28)
+    fa = int(round(t_act * fps))
+    out = []
+    for f in range(n):
+        t = f / fps
+        e = dict(x=home, y=0.0, rot=0.0, body=(1.0, 1.0), head=(1.0, 1.0), run=None, flip=False, eyes=None,
+                 pose=None, jitter=JITTER.get(act, 0.0), hidden=False)
+        if act == "run_in":  # sprint in from the left, skid to a stop on his mark
+            u = _clamp01(t / 0.55)
+            e["x"] = -0.45 + (home + 0.45) * (1 - (1 - u) ** 2)
+            if u < 1:
+                e["run"], e["rot"] = 2 * math.pi * 3.6 * t, 9.0 * (1 - u)
+            elif f - int(0.55 * fps) < 6:
+                e["body"] = _squash(f - int(0.55 * fps) + 2)
+        elif act == "run_off":  # stand, then bolt off to the right
+            if f >= fa:
+                u = _clamp01((t - t_act) / 0.5)
+                e["x"] = home + 1.05 * u * u
+                e["run"], e["rot"] = 2 * math.pi * 4.2 * (t - t_act), 10.0
+                e["pose"], e["eyes"] = "shock", None
+            if e["x"] > 1.45:
+                e["hidden"] = True
+        elif act == "run_across":  # panic sprint left to right across the whole line
+            e["x"] = -0.4 + 1.8 * t / max(n / fps, 0.1)
+            e["run"], e["rot"], e["pose"] = 2 * math.pi * 4.0 * t, 10.0, "shock"
+        elif act == "launch":  # kicked: squash, then flung up and out with a spinning arc
+            if f >= fa:
+                k = f - fa
+                u = (t - t_act) / 0.75
+                if k < 2:
+                    e["body"], e["head"] = _squash(k), (1.3, 0.72)
+                else:
+                    e["x"] = home + 0.95 * u
+                    e["y"] = -2600 * u + 900 * u * u
+                    e["rot"] = 760 * u
+                e["eyes"], e["pose"] = "x", "shock"
+                if u > 1.05:
+                    e["hidden"] = True
+        elif act == "tumble":  # falls in spinning from above, lands with a squash, dazed
+            if f < fa:
+                u = f / max(fa, 1)
+                e["x"] = home + 0.22 * (1 - u)
+                e["y"] = -2200 * (1 - u) ** 2
+                e["rot"] = -540 * (1 - u)
+                e["pose"] = "shock"
+            else:
+                k = f - fa
+                e["body"] = _squash(k)
+                e["head"] = (1.0 + 0.6 * (e["body"][0] - 1), 1.0 + 0.6 * (e["body"][1] - 1))
+                if k < int(0.6 * fps):
+                    e["eyes"], e["rot"] = "x", 6 * math.sin(2 * math.pi * 3 * (t - t_act)) * math.exp(-3 * (t - t_act))
+        elif act == "peek":  # leans in from the right edge, trembling
+            u = _clamp01(t / 0.25)
+            e["x"] = 1.4 - 0.5 * ease_inout(u)
+            e["rot"], e["pose"] = -16.0, "nervous"
+        elif act == "loop_out":  # the loop tail: peek, then slide back out so the last frame = frame 0
+            T = n / fps
+            u = _clamp01((T - t) / 0.3)
+            e["x"] = 1.4 - 0.5 * ease_inout(u)
+            e["rot"], e["pose"] = -16.0, "nervous"
+            if f >= n - 1:
+                e["hidden"] = True
+        elif act == "hide":  # cowering low at the left edge, trembling
+            e["x"], e["y"], e["rot"], e["pose"] = 0.14, 120.0, 8.0, "nervous"
+        elif act == "hit":  # hit reaction: head squash and stretch, knocked back, X eyes
+            if f >= fa:
+                k = f - fa
+                e["head"] = _squash(k)
+                e["x"] = home - 0.07 * math.exp(-(t - t_act) * 5) * min(1.0, k / 2 + 0.5)
+                e["rot"] = -12 * math.exp(-(t - t_act) * 4)
+                if t - t_act < 0.7:
+                    e["eyes"], e["pose"] = "x", "shock"
+        elif act == "puff":  # stung: the head swells and stays swollen, trembling
+            if f >= fa:
+                k = f - fa
+                g = [1.15, 1.35, 1.55, 1.62, 1.55, 1.5][k] if k < 6 else 1.5
+                e["head"], e["pose"] = (g, g), "shock"
+            else:
+                e["jitter"] = 0.0
+        elif act == "puffed":  # still swollen from the last line
+            e["head"], e["pose"] = (1.5, 1.5), "shock"
+        elif act == "deflate":  # swollen until t_act, then shrinks back with a wobble
+            if f < fa:
+                e["head"], e["pose"], e["jitter"] = (1.5, 1.5), "shock", 6.0
+            else:
+                k = f - fa
+                g = [1.3, 1.05, 0.88, 0.95, 1.04, 1.0][k] if k < 6 else 1.0
+                e["head"] = (g, 2 - g if k < 6 else 1.0)
+        elif act == "shake":
+            e["pose"] = "nervous"
+        if e["jitter"] and not e["hidden"]:
+            e["jx"] = e["jitter"] * math.sin(2 * math.pi * 17 * t + ph)
+            e["jy"] = 0.4 * e["jitter"] * math.sin(2 * math.pi * 23 * t + 2 * ph)
+            e["rot"] += 0.25 * e["jitter"] * math.sin(2 * math.pi * 13 * t + ph)
+        out.append(e)
+    return out
+
+
+def apply_run(st, phase):
+    """Scissor stride on a rig state: feet swing and lift, hips bob, arms swing opposite, lean forward."""
+    s = math.sin(phase)
+    lf = (FEET[0][0] + 85 * s, FEET[0][1] - 55 * max(0.0, math.cos(phase)))
+    rf = (FEET[1][0] - 85 * s, FEET[1][1] - 55 * max(0.0, -math.cos(phase)))
+    st = dict(st, feet=(lf, rf), knee=st.get("knee", 0.0) + 22 + 10 * abs(s), lean=st.get("lean", 0.0) + 9)
+    st["l"] = (38 - 50 * s, -60.0, 0.0)
+    st["r"] = (38 + 50 * s, -60.0, 0.0)
+    return st
+
+
 def prop(name, height):
     """A still prop that stands beside Meatball (RGBA, `height` px tall). The fork is the show's silent
     running gag: it turns up, upright and unexplained, whenever a line is about eating (research/39)."""
diff -u /dev/null b/tools/make_sfx.py
--- /dev/null
+++ b/tools/make_sfx.py
@@ -0,0 +1,61 @@
+#!/usr/bin/env python3
+"""Build the Shorts v3 sound-effect kit in sfx/ (48 kHz stereo WAV, peak -3 dBFS).
+
+Usage: make_sfx.py KENNEY_DIR [OUT_DIR]
+  KENNEY_DIR  a folder holding the unzipped Kenney CC0 packs (kenney.nl "Impact Sounds",
+              "Interface Sounds", "Digital Audio"); only .ogg files are read, nothing in it is run.
+  OUT_DIR     default: ../sfx next to this tools/ folder
+Kenney sounds are CC0. The rest are synthesized here with ffmpeg (nothing to license).
+"""
+import glob
+import os
+import subprocess
+import sys
+
+SYNTH = {  # name -> lavfi source (and an optional filter chain)
+    "whoosh": ("anoisesrc=d=0.42:c=pink:r=48000:a=0.9",
+               "highpass=f=350,lowpass=f=3200,afade=t=in:d=0.22:curve=exp,afade=t=out:st=0.22:d=0.2:curve=exp"),
+    "boing": ("aevalsrc=0.8*sin(2*PI*(150*t+300*t*t)+2.4*sin(2*PI*12*t))*exp(-3.2*t):d=0.6:s=48000", None),
+    "pop": ("aevalsrc=0.9*sin(2*PI*(280*t+2600*t*t))*exp(-22*t):d=0.13:s=48000", None),
+    "scratch": ("aevalsrc=(0.7*sin(2*PI*(160*t+1500*t*t-2600*t*t*t))+0.3*(2*random(0)-1))*(1-t/0.42):d=0.42:s=48000",
+                "bandpass=f=1400:w=2200"),
+    "splash": ("anoisesrc=d=0.75:c=white:r=48000:a=0.9",
+               "highpass=f=250,lowpass=f=2600,afade=t=in:d=0.03,afade=t=out:st=0.05:d=0.7:curve=exp"),
+    "tink": ("aevalsrc=0.30*sin(2*PI*2960*t)*exp(-22*t)+0.18*sin(2*PI*4410*t)*exp(-30*t)"
+             "+0.10*sin(2*PI*6650*t)*exp(-40*t):d=0.35:s=48000", None),
+}
+KENNEY = {  # name -> file inside the packs
+    "crunch": "impactPunch_heavy_002.ogg",
+    "hit": "impactPunch_medium_001.ogg",
+    "thud": "impactSoft_heavy_001.ogg",
+    "zap": "zap2.ogg",
+    "plate": "impactPlate_light_002.ogg",
+}
+
+
+def norm(src_args, out, chain=None):
+    af = (chain + "," if chain else "") + "aformat=sample_rates=48000:channel_layouts=stereo"
+    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + src_args + ["-af", af, "/tmp/_sfx.wav"], check=True)
+    peak = subprocess.run(["ffmpeg", "-i", "/tmp/_sfx.wav", "-af", "volumedetect", "-f", "null", "-"],
+                          capture_output=True, text=True).stderr
+    mx = float(peak.split("max_volume: ")[1].split(" dB")[0])
+    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "/tmp/_sfx.wav", "-af", f"volume={-3 - mx}dB",
+                    "-c:a", "pcm_s16le", out], check=True)
+
+
+def main():
+    kdir = sys.argv[1]
+    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sfx")
+    os.makedirs(out, exist_ok=True)
+    for name, (src, chain) in SYNTH.items():
+        norm(["-f", "lavfi", "-i", src], f"{out}/{name}.wav", chain)
+    for name, fn in KENNEY.items():
+        hit = glob.glob(f"{kdir}/**/{fn}", recursive=True)
+        if not hit:
+            raise SystemExit(f"missing {fn} in {kdir}")
+        norm(["-i", hit[0]], f"{out}/{name}.wav")
+    print("ok", out, sorted(os.listdir(out)))
+
+
+if __name__ == "__main__":
+    main()
diff -u /dev/null b/tools/v3.py
--- /dev/null
+++ b/tools/v3.py
@@ -0,0 +1,476 @@
+#!/usr/bin/env python3
+"""Shorts v3 renderer (research/44): Meatball in jeopardy, with motion, impacts and sound effects.
+
+Selected by "style": "v3" in a Shorts spec (explainer.py dispatches here; episode.py --skip-long builds it).
+Every frame is composed in Python (numpy/cv2) and piped once into ffmpeg, so the camera can move across
+cuts: the photo always pushes, cuts to a new photo whip-pan, key words punch in, hits shake the frame and
+flash white, and Meatball performs an action move over his talking rig (mascot.act_track).
+
+Spec fields (all optional unless noted):
+  "tempo": 1.10          voice sped up with ffmpeg atempo; word timings are scaled to match
+  beat "act"             stand | run_in | run_off | run_across | launch | tumble | shake | peek | hide | hit
+                         | puff  (the loop tail defaults to loop_out: he peeks, then slides off-frame)
+  beat "act_at"          word (or seconds into the line) when the move lands; default: the "hit" word
+  beat "hit"             word: impact = white flash (3 frames) + screen shake
+  beat "punch"           word or list of words: punch-in zoom to ~118% (beat "punch_z" overrides)
+  beat "sfx"             ["whoosh", "crunch@kick", "pop@1.2"]: name[@word|@seconds]; bare names play at
+                         the act moment. Kit in sfx/ (tools/make_sfx.py), mixed under the voice
+  beat "label"           big pop-in word card on the picture, e.g. {"text": "4 INCHES", "at": "dagger"}
+  beat "x"               Meatball's mark as a fraction of the frame width (default 0.24)
+  beat "size"            Meatball's size in px per 1000 drawing units (default 1000: ~40% of the frame)
+  beat "prop": "fork"    the Fork drops in beside him at "prop_at" (word)
+  shot "whip": false     hard cut instead of a whip pan (cuts to a different photo whip by default)
+  shot "blur": true      blurred, dimmed photo (a host shot)
+Photos come from explainer.photo() (pinned iNaturalist observations, full resolution).
+"""
+import json
+import math
+import multiprocessing as mp
+import os
+import subprocess
+import wave
+
+import cv2
+import numpy as np
+from PIL import Image, ImageDraw, ImageFilter, ImageFont
+
+import explainer as ex
+import mascot
+
+FPS, W, H, SR = 30, 1080, 1920, 48000
+ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
+SFX_DIR = os.path.join(ROOT, "sfx")
+GAIN = {"whoosh": 0.32, "boing": 0.22, "pop": 0.30, "scratch": 0.20, "splash": 0.34, "tink": 0.40,
+        "crunch": 0.42, "hit": 0.40, "thud": 0.42, "zap": 0.28, "plate": 0.30}
+R = 1.15          # photo bases are prepared 15% over frame size so slow pushes stay sharp
+GAP = 0.12        # silence after each line (v2 used 0.35)
+FLOOR = 1430      # Meatball's feet (screen y); captions sit just below
+CAP_Y = 1560
+MAX_SHOT = 2.4    # a shot longer than this is re-cut to a tighter crop of the same photo (gate: 2.5 s)
+PUSH = 0.045      # zoom per second of the slow push (v2: 0.036)
+HOME = 0.24       # Meatball's mark: left of centre, so the animal (centred in each crop) stays visible
+PLAN = {}         # filled before the frame workers fork
+
+
+def _key(w):
+    return w.lower().strip(".,!?;:'\"")
+
+
+def word_time(words, at, default=None, after=-1.0):
+    """Seconds into the line of the first word matching `at` (a word, or a number of seconds)."""
+    if at is None:
+        return default
+    if isinstance(at, (int, float)):
+        return float(at)
+    try:
+        return float(at)
+    except ValueError:
+        pass
+    k = _key(at)
+    hit = next((s for s, e, w in words if _key(w) == k and s > after), None)
+    if hit is None:
+        print(f"V3 WARN: word {at!r} not in line; using {default}", flush=True)
+        return default
+    return hit
+
+
+def speed(mp3, tempo):
+    """Beat audio sped up by `tempo` (pitch kept), as 48 kHz stereo WAV, with word timings scaled."""
+    wav = mp3[:-4] + f"_t{tempo:.3f}.wav"
+    if not os.path.exists(wav):
+        af = f"atempo={tempo:.4f}," if abs(tempo - 1) > 1e-3 else ""
+        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-af", af + "aresample=48000",
+                        "-ac", "2", "-c:a", "pcm_s16le", wav], check=True)
+    words = [(s / tempo, e / tempo, w) for s, e, w in json.load(open(mp3 + ".words.json"))]
+    return wav, words
+
+
+def read_wav(path):
+    with wave.open(path) as f:
+        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, f.getnchannels())
+    a = a.astype(np.float32) / 32768.0
+    return a if a.shape[1] == 2 else np.repeat(a, 2, axis=1)
+
+
+def write_wav(path, a):
+    with wave.open(path, "wb") as f:
+        f.setnchannels(2)
+        f.setsampwidth(2)
+        f.setframerate(SR)
+        f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
+
+
+# ---------------------------------------------------------------- pictures
+
+_BASES = {}
+
+
+def base(path, crop=None, blur=False):
+    """The shot's photo cropped and scaled to cover the frame at R x size (cached)."""
+    key = (path, tuple(crop or ()), blur)
+    if key not in _BASES:
+        im = Image.open(path).convert("RGB")
+        if crop:
+            im = im.crop((int(crop[0] * im.width), int(crop[1] * im.height), int(crop[2] * im.width),
+                          int(crop[3] * im.height)))
+        bw, bh = int(W * R), int(H * R)
+        s = max(bw / im.width, bh / im.height)
+        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
+        l, t = (im.width - bw) // 2, (im.height - bh) // 2
+        im = im.crop((l, t, l + bw, t + bh))
+        if blur:
+            im = im.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.78))
+        _BASES[key] = np.asarray(im)
+    return _BASES[key]
+
+
+def view(img, z, dx=0.0):
+    """Frame of a base at zoom z (1 = the whole base), sub-pixel smooth; dx shifts it (whip pans)."""
+    bh, bw = img.shape[:2]
+    s = (W / bw) * z
+    m = np.float32([[s, 0, W / 2 - s * bw / 2 + dx], [0, s, H / 2 - s * bh / 2]])
+    return cv2.warpAffine(img, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
+
+
+def label_img(text):
+    f = ImageFont.truetype(ex.BOLD, 150)
+    lines = text.split("\n")
+    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
+    tw = int(max(d.textlength(x, font=f) for x in lines)) + 60
+    im = Image.new("RGBA", (tw, int(len(lines) * 175) + 60), (0, 0, 0, 0))
+    d = ImageDraw.Draw(im)
+    for k, line in enumerate(lines):
+        x = (tw - d.textlength(line, font=f)) / 2
+        d.text((x, 20 + k * 175), line, font=f, fill=ex.YELLOW, stroke_width=12, stroke_fill=(0, 0, 0))
+    im = im.rotate(5, expand=True, resample=Image.BICUBIC)
+    return np.asarray(im)
+
+
+def over(dst, src, x, y):
+    """Alpha-composite RGBA array src onto RGB array dst with its top-left at (x, y), clipped."""
+    h, w = src.shape[:2]
+    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
+    if x1 <= x0 or y1 <= y0:
+        return
+    s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
+    a = s[..., 3:4] / 255.0
+    d = dst[y0:y1, x0:x1].astype(np.float32)
+    dst[y0:y1, x0:x1] = (d * (1 - a) + s[..., :3] * a).astype(np.uint8)
+
+
+# ---------------------------------------------------------------- Meatball
+
+def sprite(st, size):
+    """Meatball (white rim + soft shadow) as an RGBA array with room for squash, puff and spins."""
+    pad = int(size * 0.45)
+    cw = size + 2 * pad
+    got = mascot.render(st, size, 2 if size <= 1400 else 1, (pad, pad), (cw, cw))
+    canvas = Image.new("RGBA", (cw, cw), (0, 0, 0, 0))
+    if got:
+        im, (x, y) = got
+        margin = max(13, int(size / 66)) + 2
+        pim = Image.new("RGBA", (im.width + 2 * margin, im.height + 2 * margin), (0, 0, 0, 0))
+        pim.alpha_composite(im, (margin, margin))
+        canvas.alpha_composite(mascot._sticker(pim, size, True), (x - margin, y - margin))
+    return np.asarray(canvas), pad
+
+
+def place_meatball(frame, st, tr, size):
+    if tr["hidden"]:
+        return
+    spr, pad = sprite(st, size)
+    k = size / 1000.0
+    hip = np.array([pad + 500 * k, pad + 790 * k])
+    feet = np.array([pad + 500 * k, pad + 960 * k])
+    tx = tr["x"] * W + tr.get("jx", 0.0) * k
+    ty = FLOOR - 170 * k + tr["y"] * k + tr.get("jy", 0.0) * k
+    sx, sy = tr["body"]
+    T = lambda x, y: np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], dtype=np.float64)
+    a = math.radians(tr["rot"])
+    Rm = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
+    S = np.diag([sx, sy, 1.0])
+    M = T(tx, ty) @ Rm @ T(-hip[0], -hip[1]) @ T(feet[0], feet[1]) @ S @ T(-feet[0], -feet[1])
+    h, w = spr.shape[:2]
+    pts = M @ np.array([[0, w, w, 0], [0, 0, h, h], [1, 1, 1, 1]])
+    x0, y0 = int(max(0, pts[0].min())), int(max(0, pts[1].min()))
+    x1, y1 = int(min(W, pts[0].max() + 1)), int(min(H, pts[1].max() + 1))
+    if x1 <= x0 or y1 <= y0:
+        return
+    M2 = T(-x0, -y0) @ M
+    out = cv2.warpAffine(spr, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
+    over(frame, out, x0, y0)
+
+
+# ---------------------------------------------------------------- plan
+
+def plan_beats(spec, work):
+    name, rate = spec.get("voice", "en-US-AndrewNeural"), spec.get("rate", "+0%")
+    tempo = float(spec.get("tempo", 1.0))
+    beats = spec["beats"]
+    ex.voice(beats, work, name, rate)
+    looping = any(b.get("loop") for b in beats)
+    out, F, shot_no = [], 0, 0
+    for i, b in enumerate(beats):
+        mp3 = ex.vo_path(b, work, name, rate)
+        wav, words = speed(mp3, tempo)
+        # cut on the last word, not the TTS file's trailing silence (~0.3 s a line)
+        spoken = min(ex.duration(wav), (words[-1][1] + 0.06) if words else ex.duration(wav))
+        n = int(round((spoken + GAP + float(b.get("hold", 0))) * FPS))
+        D = n / FPS
+        # pictures: cut on "at" words; a shot longer than MAX_SHOT is re-cut tighter on the same photo
+        vis = ex.shots(b)
+        starts, after = [0.0], -1.0
+        for s in vis[1:]:
+            t = word_time(words, s.get("at"), None, after)
+            starts.append(t if t is not None else D * len(starts) / len(vis))
+            after = starts[-1]
+        shots = []
+        for k, s in enumerate(vis):
+            a, z = starts[k], (starts[k + 1] if k + 1 < len(vis) else D)
+            pieces = [(a, z, s)]
+            if z - a > MAX_SHOT:
+                mid = min((w[0] for w in words if a + 0.9 <= w[0] <= z - 0.9), key=lambda t: abs(t - (a + z) / 2),
+                          default=(a + z) / 2)
+                c = s.get("crop") or [0, 0, 1, 1]
+                cx, cy, cw, ch = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2, (c[2] - c[0]) * 0.8, (c[3] - c[1]) * 0.8
+                tight = dict(s, crop=[cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], whip=False)
+                # the loop tail must END on its original crop (= frame 0), so it opens on the tight one
+                pieces = [(a, mid, tight), (mid, z, dict(s, whip=False))] if b.get("loop") else [(a, mid, s), (mid, z, tight)]
+            for a_, z_, s_ in pieces:
+                path = ex.photo(s_["photo"], s_.get("n", 0), work, s_.get("obs"), "original")
+                shots.append(dict(f0=int(round(a_ * FPS)), f1=int(round(z_ * FPS)), path=path, crop=s_.get("crop"),
+                                  blur=bool(s_.get("blur")), whip=s_.get("whip", True), no=shot_no))
+                shot_no += 1
+        hit = word_time(words, b.get("hit"), None)
+        act = b.get("act") or ("loop_out" if b.get("loop") else "stand")
+        dflt = hit if hit is not None else (max(0.0, D - 0.6) if act == "run_off" else 0.25)
+        t_act = word_time(words, b.get("act_at"), dflt)
+        pose = b.get("pose", "deadpan")
+        sts = mascot.states(pose, [list(w) for w in words], D, FPS, seed=i)
+        trk = mascot.act_track(act, n, FPS, t_act, float(b.get("x", HOME)), seed=i)
+        punch = b.get("punch") or []
+        punch = [punch] if isinstance(punch, str) else punch
+        sfx = []
+        for e in b.get("sfx", []):
+            nm, _, at = e.partition("@")
+            t = t_act if not at else (t_act if at == "act" else word_time(words, at, t_act))
+            sfx.append((F / FPS + max(0.0, t), nm))
+        lab = b.get("label")
+        if isinstance(lab, str):
+            lab = {"text": lab}
+        out.append(dict(i=i, F=F, n=n, words=words, wav=wav, shots=shots, act=act, sts=sts, trk=trk,
+                        hit=None if hit is None else int(round(hit * FPS)),
+                        punch=[int(round(word_time(words, p, 0.0) * FPS)) for p in punch],
+                        punch_z=float(b.get("punch_z", 0.18)), sfx=sfx, size=int(b.get("size", 1000)),
+                        label=lab and dict(img=label_img(lab["text"]),
+                                           f=int(round(word_time(words, lab.get("at"), 0.0) * FPS))),
+                        prop=b.get("prop"), prop_f=int(round(word_time(words, b.get("prop_at"), 0.3) * FPS)),
+                        x=float(b.get("x", HOME)), loop=bool(b.get("loop")), first=looping and i == 0, say=b["say"]))
+        F += n
+    return out
+
+
+# ---------------------------------------------------------------- frames
+
+def _ease_out(u):
+    u = min(max(u, 0.0), 1.0)
+    return 1 - (1 - u) ** 3
+
+
+def shot_view(bt, sh, f):
+    """Background frame for shot sh at beat frame f: a slow push that never stops."""
+    img = base(sh["path"], sh["crop"], sh["blur"])
+    t = (f - sh["f0"]) / FPS
+    if bt["loop"]:
+        z = 1.0 + PUSH * (bt["n"] - 1 - f) / FPS   # ends exactly on frame 0's zoom
+    elif bt["first"] and sh is bt["shots"][0]:
+        z = 1.0 + PUSH * t                          # frame 0 starts at zoom 1.0
+    elif sh["no"] % 2:
+        z = max(1.0, 1.0 + PUSH * 3 - PUSH * t)     # push out
+    else:
+        z = 1.0 + PUSH * t
+    return img, z
+
+
+def frame(g):
+    P = PLAN
+    bi = max(k for k, bt in enumerate(P["beats"]) if bt["F"] <= g)
+    bt = P["beats"][bi]
+    f = g - bt["F"]
+    shots = bt["shots"]
+    k = max(j for j, s in enumerate(shots) if s["f0"] <= f or j == 0)
+    sh = shots[k]
+    img, z = shot_view(bt, sh, f)
+    bg = None
+    cut = P["whips"].get(g)  # whip pan: 6 frames centred on a cut to a different photo (also across beats)
+    if cut:
+        gc, pb, ps, nb, ns = cut
+        u = (g - (gc - 3) + 0.5) / 6.0
+        o = int(W * u * u * (3 - 2 * u))
+        A = view(*shot_view(pb, ps, g - pb["F"]))
+        B = view(*shot_view(nb, ns, g - nb["F"]))
+        bg = np.concatenate([A[:, o:], B[:, :o]], axis=1)
+        bg = cv2.blur(bg, (int(170 * math.sin(math.pi * u)) | 1, 1))
+    if bg is None:
+        bg = view(img, z)
+    frame_ = np.ascontiguousarray(bg)
+    st = dict(bt["sts"][min(f, len(bt["sts"]) - 1)])
+    tr = bt["trk"][f]
+    if tr["run"] is not None:
+        st = mascot.apply_run(st, tr["run"])
+    if tr["pose"] and tr["pose"] in mascot.POSES and tr["pose"] != "nervous":
+        po = mascot.POSES[tr["pose"]]
+        st["mouth"] = "o" if tr["pose"] == "shock" else po["mouth"]
+        st["brow"] = po["brow"]
+    elif tr["pose"] == "nervous":
+        st["brow"] = "worry"
+    if tr["eyes"]:
+        st["eyes"] = tr["eyes"]
+    st["head_s"] = tr["head"]
+    if bt["prop"] and f >= bt["prop_f"]:  # the Fork drops in beside him and stands there
+        p = P["props"][bt["prop"]]
+        kf = f - bt["prop_f"]
+        drop = [-900, -520, -200, 0, -40, 0][kf] if kf < 6 else 0
+        over(frame_, p, int(bt["x"] * W + bt["size"] * 0.36), FLOOR - p.shape[0] + 20 + drop)
+    place_meatball(frame_, st, tr, bt["size"])
+    if bt["label"] and f >= bt["label"]["f"]:
+        kf = f - bt["label"]["f"]
+        s = [0.35, 0.75, 1.15, 1.06, 1.0][kf] if kf < 5 else 1.0
+        li = bt["label"]["img"]
+        li = cv2.resize(li, (max(1, int(li.shape[1] * s)), max(1, int(li.shape[0] * s))))
+        over(frame_, li, W // 2 - li.shape[1] // 2, 330 - li.shape[0] // 2)
+    # camera: punch-in zooms and impact shake on the whole picture
+    zc, sx, sy = 1.0, 0.0, 0.0
+    for pf in bt["punch"]:
+        d = f - pf
+        if d >= 0:
+            env = _ease_out((d + 1) / 3) if d < 3 else (1.0 if d < 3 + 0.75 * FPS else max(0.0, 1 - (d - 3 - 0.75 * FPS) / 8))
+            zc = max(zc, 1 + bt["punch_z"] * env)
+    if bt["hit"] is not None and 0 <= f - bt["hit"] < 10:
+        d = f - bt["hit"]
+        amp = 34 * math.exp(-d / 3.5)
+        sx, sy = amp * math.sin(d * 2.3 + 0.7), amp * math.cos(d * 2.9)
+        zc = max(zc, 1.04)
+    if zc != 1.0 or sx or sy:
+        cx, cy = W / 2, 860
+        m = np.float32([[zc, 0, cx - zc * cx + sx], [0, zc, cy - zc * cy + sy]])
+        frame_ = cv2.warpAffine(frame_, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
+    if bt["hit"] is not None and 0 <= f - bt["hit"] < 3:  # white impact flash
+        a = (0.85, 0.55, 0.25)[f - bt["hit"]]
+        frame_ = (frame_.astype(np.float32) * (1 - a) + 255 * a).astype(np.uint8)
+    return frame_.tobytes()
+
+
+def captions(beats, path):
+    """Two-word cards in the lower third, the spoken word yellow; each card pops in."""
+    head = (f"[Script Info]\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
+            "PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV\n"
+            "Style: Cap,DejaVu Sans,100,&H00FFFFFF,&H00000000,&H64000000,-1,1,8,3,5,0\n\n"
+            "[Events]\nFormat: Layer, Start, End, Style, Text\n")
+    from facts import ass_time
+    lines = []
+    for bt in beats:
+        T0, words = bt["F"] / FPS, bt["words"]
+        for i in range(0, len(words), 2):
+            group = words[i:i + 2]
+            for j, (s, e, _) in enumerate(group):
+                nxt = words[i + 2][0] if i + 2 < len(words) else e + 0.08
+                end = group[j + 1][0] if j + 1 < len(group) else min(e + 0.08, nxt)
+                pop = r"\fscx70\fscy70\t(0,90,\fscx112\fscy112)" if j == 0 else r"\fscx112\fscy112"
+                text = " ".join(("{\\c&H00FFFF&}" + w.upper() + "{\\c&HFFFFFF&}") if q == j else w.upper()
+                                for q, (_, _, w) in enumerate(group))
+                lines.append(f"Dialogue: 0,{ass_time(T0 + s)},{ass_time(T0 + end)},Cap,"
+                             f"{{\\an5\\pos({W // 2},{CAP_Y}){pop}}}{text}")
+    open(path, "w").write(head + "\n".join(lines) + "\n")
+
+
+def gate(beats, total):
+    """v3 self-check: cut lengths and how often something new happens."""
+    warn, events = [], []
+    for bt in beats:
+        for s in bt["shots"]:
+            d = (s["f1"] - s["f0"]) / FPS
+            if d > 2.5 + 1e-6:
+                warn.append(f"beat {bt['i']} holds one picture {d:.2f}s (max 2.5)")
+            events.append(bt["F"] / FPS + s["f0"] / FPS)
+        events += [bt["F"] / FPS + p / FPS for p in bt["punch"]]
+        events += [t for t, _ in bt["sfx"]]
+        if bt["act"] not in ("stand",):
+            events.append(bt["F"] / FPS)
+        if bt["label"]:
+            events.append(bt["F"] / FPS + bt["label"]["f"] / FPS)
+    events = sorted(events)
+    gaps = [b - a for a, b in zip([0.0] + events, events + [total])]
+    if max(gaps) > 3.0:
+        warn.append(f"longest stretch with nothing new: {max(gaps):.1f}s")
+    for w in warn:
+        print("GATE WARN:", w, flush=True)
+    print(f"v3 gate: {len(events)} events in {total:.1f}s, longest gap {max(gaps):.2f}s", flush=True)
+
+
+def build(spec, work, out, music=None):
+    os.makedirs(work, exist_ok=True)
+    ex.vertical()
+    beats = plan_beats(spec, work)
+    total_f = beats[-1]["F"] + beats[-1]["n"]
+    cuts = {}
+    flat = [(bt, s) for bt in beats for s in bt["shots"]]
+    for (pb, ps), (nb, ns) in zip(flat, flat[1:]):
+        g = nb["F"] + ns["f0"]
+        if ns["whip"] and (ns["path"], ns["crop"]) != (ps["path"], ps["crop"]) and not ns.get("blur"):
+            for d in range(-3, 3):
+                cuts[g + d] = (g, pb, ps, nb, ns)
+    PLAN.clear()
+    PLAN.update(beats=beats, whips=cuts, props={"fork": np.asarray(mascot.prop("fork", 520))})
+    for bt in beats:  # warm the photo cache before forking the workers
+        for s in bt["shots"]:
+            base(s["path"], s["crop"], s["blur"])
+    total = total_f / FPS
+    gate(beats, total)
+    # audio: voice lines, SFX under them, music bed ducked by the voice
+    voice = np.zeros((int(total * SR) + SR, 2), np.float32)
+    sfx = np.zeros_like(voice)
+    kit = {}
+    for bt in beats:
+        a = read_wav(bt["wav"])
+        s0 = int(bt["F"] / FPS * SR)
+        voice[s0:s0 + len(a)] += a[:len(voice) - s0]
+        for t, nm in bt["sfx"]:
+            if nm not in kit:
+                kit[nm] = read_wav(f"{SFX_DIR}/{nm}.wav")
+            a = kit[nm] * GAIN.get(nm, 0.3)
+            s1 = int(t * SR)
+            sfx[s1:s1 + len(a)] += a[:len(sfx) - s1]
+    write_wav(f"{work}/voice.wav", voice)
+    write_wav(f"{work}/sfx.wav", sfx)
+    cap = f"{work}/cap.ass"
+    captions(beats, cap)
+    music = music if music and os.path.exists(music) else None
+    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
+           "-r", str(FPS), "-i", "pipe:0", "-i", f"{work}/voice.wav", "-i", f"{work}/sfx.wav"]
+    if music:
+        cmd += ["-stream_loop", "-1", "-i", music]
+        af = ("[1:a]asplit[vo][key];[3:a]volume=0.12[m];[m][key]sidechaincompress=threshold=0.02:ratio=6:"
+              "attack=30:release=500[d];[vo][d][2:a]amix=inputs=3:duration=first:normalize=0,"
+              "loudnorm=I=-14:TP=-1.5[a]")
+    else:
+        af = "[1:a][2:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]"
+    cmd += ["-filter_complex", f"[0:v]ass={cap},format=yuv420p[v];{af}", "-map", "[v]", "-map", "[a]",
+            "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac",
+            "-b:a", "160k", "-movflags", "+faststart", out]
+    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
+    jobs = int(os.environ.get("MEATBALL_JOBS", "2"))
+    with mp.get_context("fork").Pool(jobs) as pool:
+        for k, buf in enumerate(pool.imap(frame, range(total_f), chunksize=4)):
+            proc.stdin.write(buf)
+            if k % 150 == 0:
+                print(f"v3 frame {k}/{total_f}", flush=True)
+    proc.stdin.close()
+    if proc.wait():
+        raise SystemExit("ffmpeg failed")
+    used = sorted({s["path"] for bt in beats for s in bt["shots"]})
+    open(f"{work}/credits.txt", "w").write("".join(open(u + ".credit").read() + "\n" for u in used))
+    json.dump([dict(i=bt["i"], start=bt["F"] / FPS, dur=bt["n"] / FPS, act=bt["act"], say=bt["say"],
+                    shots=[(s["f0"] / FPS, s["f1"] / FPS) for s in bt["shots"]], sfx=bt["sfx"]) for bt in beats],
+              open(f"{work}/timeline.json", "w"), indent=1)
+    print(f"ok {out} {total:.1f}s")
```

## 7. Frank assessment
**Is v3 clearly more entertaining?** Yes, in what's on screen: the measurable gap is large. The old cassowary Short cuts about every 3 s between near-still photos, with a standing Meatball and a calm explainer, for 37 s. v3 has something new every ~0.5-2 s, a story with stakes, and, in my judgement, 4-5 real laughs per Short ("I don't have a heart", "I'm a pickle now", "I evolved sauce", "Best case? I become a tree"). It is also 12-15 s shorter. Whether it *retains* better is unproven until it's posted. The test is the same as research/39: post v3 cassowary against the old one and watch the 5-13 s drop.

**What it still lacks (honest):**
1. **The animal never acts.** It's a still photo, so the kick is implied: Meatball flies, but no leg moves. The biggest upgrade would be real CC footage (Wikimedia Commons / Pexels clips) or a 3-4 frame cut-out "kick" of the animal photo.
2. **Meatball and the animal don't share space.** He stands in front of the photo and sometimes covers the animal's neck or head. Nothing on the photo marks where the animal is (no per-photo coordinates), so contact moments (poke, sting) are staged by timing, not position.
3. **The voice is still TTS.** The prototype uses edge-tts Andrew (rate +0% × atempo 1.10 = +10%). **The final version would use Bill**: 37 new lines across the 3 Shorts (loop lines included), ≈21 vidIQ credits per the Studio estimate (≈7 per Short). No credits were spent on the prototype. Comic timing (a pause before "Just once.") would land better with a human-paced read.
4. **The run cycle is functional, not funny.** The stride and arm swing read at phone size but are stiff up close. The launch and tumble read best.
5. **SFX are generic.** The synthesized whoosh, boing and scratch are serviceable; the Kenney impacts are good. A curated CC0 cartoon pack (e.g. Kenney's later packs or freesound CC0) would add character.
6. **It is busier than Nolan's stated taste** (research/39 §10). It's a deliberate bet on the retention data; the dials are listed in §2.
7. **Facts are true but simplified.** "Its poop plants rainforests" is a compression of "some seeds only sprout after passing through it". The description `bonus` lines carry the precise version. A fact-check pass is still needed before posting, as for any Short.
