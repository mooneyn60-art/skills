# 45 — Shorts v4 prototype: the animal acts, and Meatball stays off it (Studio R&D, 2026-10-25)

**Brief.** Shorts v3 (research/44) is live and Nolan likes it. It has two gaps:
1. The animal never acts. It is a still photo, so a kick or a sting is only implied.
2. Meatball sometimes covers the animal's head or neck, because nothing tells the renderer where the animal is.

Nolan's feedback on the first cassowary test (10/25) became hard rules:
- **Clean outlines.** No halo, no background fringe, no chewed edges. Use one smooth, uniform white stroke and a soft shadow.
- **Never part of an animal.** Nothing may be lost to the matte, the photo's edge, the crop, Meatball or a caption.
- **An automatic check.** The render must fail when a mask touches the photo's edge or loses more than ~3% of its area.

**Answer in one line.** v4 cuts out every animal *whole* and makes it act on the word: kick, sting, charge, turn, shake, drift, and an always-on breathing bob. The shot is re-framed around the animal so it stands beside Meatball, clear of him and of the captions. Its background is its own photo, blurred and dimmed with the animal painted out.

**Status: prototype for Nolan. Nothing is posted and the live `tools/` is unchanged.** The code lives in a scratch copy. Section 8 holds the unified diff (also `episodes/v4-proto/tools-v4.diff`), ready to merge after Nolan approves.

**Verdict, frankly: it is clearly better on what was asked, with a real cost.**
- The animal now acts in every photo shot, on the joke's word, in sync with Meatball's hit reaction and the screen shake.
- Meatball never covers an animal outside the intended contacts (poke, sting, kick, grab) and 1-5 frames of a tumble.
- Edges are clean and no animal is missing a part.
- **The cost:** the animal is smaller and the photo is less of the star. It now reads as "sticker on a soft backdrop", not "real photo with a cartoon in front". That is a step away from v3's full-bleed look. See section 7.

## 1. Files (`episodes/v4-proto/`)
| File | What |
|---|---|
| `short-cassowary.mp4` | v4 cassowary, **24.6 s** (v3: 24.6 s) |
| `short-boxjelly.mp4` | v4 box jellyfish, **22.1 s** (v3: 22.1 s) |
| `short-badger.mp4` | v4 honey badger, **24.7 s** (v3: 24.7 s) |
| `compare.mp4` | 1080x960, 71 s. Live v3 (`episodes/v3-01`) on the left, v4 on the right, labelled. The three Shorts play back to back; the audio is v4's (same lines, same voice) |
| `grab-cassowary-kick.jpg`, `grab-boxjelly-sting.jpg`, `grab-badger-charge.jpg` | 12 consecutive frames around each impact |
| `edge-closeup.jpg` | 1:1 crops of the cut-out edges from the final renders (cassowary, badger, box jelly) |
| `grab-compare.jpg` | one frame of compare.mp4 (the kick) |
| `qa-*-2fps.jpg` | 2 fps contact sheets of the three renders |
| `qa-v4.json` | per Short: every shot's cut-out verdict, Meatball's mark per line, the animal's moves, and the QA overlap counts |
| `script-v4-proto.json` | the script (= `scripts/v4-proto.json` in the copy): v3-proto lines unchanged, plus `animal`, `contact`, `subjects` and the re-picked photos |
| `credits.txt` | photo credits (all CC BY / CC0 iNaturalist) |
| `tools-v4.diff` | the code change (same as section 8) |

Voice: en-US-AndrewMultilingualNeural at +0% then atempo 1.10, the same as the live v3. Music, SFX kit and captions are unchanged.

## 2. What changed
**A. Subject detection** (`tools/animal.py`, `subject()`).
- rembg (`isnet-general-use`, the thumbnail model) runs on the shot's crop plus a margin (0.6x crop width each side, 0.3x height). If the animal runs past that margin, it runs on the whole photo.
- The result is cached per photo region in `~/.cache/meatball-subjects`.
- From the matte it takes the whole animal's box (it may extend past the shot's crop), a head guess, and a verdict.
- The subject is the matte component with the most area inside the crop. Pieces at least 15% of its size are kept with it.
- **Gates.** A shot falls back to the v3 still (printed as `V4 FALLBACK`) when:
  - the animal touches the photo's edge ("cropped in the original"),
  - cleaning the matte would lose more than 3% of the nearby raw matte,
  - the matte is in more than 2 pieces (broken tentacles or legs),
  - the subject is under 2% of the crop,
  - more than 70% of the matte is semi-transparent,
  - or the edge contrast is under 14 Lab units.
- **Hard check.** `v3.report_v4()` raises `SystemExit` if any shot drawn as a cut-out breaks the edge or loss rule. The frame loop also fails the render if an acting animal reaches the frame edge.

**Edges** (`layers()`, per Nolan):
- Holes under 1% of the animal are filled (pinholes in fur, a dark eye). Bigger enclosed gaps stay open, for example between legs whose toes touch.
- There is no morphological opening, so thin legs, tails and tentacles survive.
- The contour is resampled to the render scale, smoothed and re-thresholded, so it is one clean curve.
- The matte is eroded 1 px, so no background fringe shows.
- Over that sits a **uniform 7 px white stroke**, drawn from a distance transform and anti-aliased, plus a soft dark drop shadow.
- The sticker is premultiplied, so scaling and rotating it never drags dark fringes in.
- Close-up: `edge-closeup.jpg`.

**Staging** (`tools/stage.py`).
- Meatball keeps a left-hand mark (x = 0.21, size 880; v3 used 0.24 and 1000) and faces the animal. His acts are re-aimed: he is flung and flees *away* from the animal, peeks in from the far edge, and cowers on the far side.
- `frame_fit()` re-frames each cut-out shot around the whole animal. It picks the largest scale (up to 1.4x photo pixels) at which the animal *plus the room its moves need* fits the free space:
  - beside Meatball (or above him only if that is much bigger),
  - inside the frame, between y = 130 (top UI) and y = 1465 (above the captions),
  - below any pop-in label,
  - with 40 px of clear air from him, more for a peek, since he leans.
- The animal stands on that space's floor at the edge nearest Meatball (floaters are centred), so the two read as a scene.
- The background is the same photo, scaled to cover the frame and centred on where the animal was. It is painted out (inpainted), blurred and dimmed like a v3 host shot, and it keeps the v3 slow push. The cut-out takes no push, which gives a little parallax.
- On a v3 still (none are left in these renders), Meatball's mark is chosen to keep him off a pinned head box (`subjects.<obs>.head`, photo fractions).

**B. Animal acting** (`animal.transform()`, beat field `"animal"`).
- `lunge` (aliases `kick`, `charge`): a 3-frame lean back and squash, a 2-frame snap to 1.18x scale and 0.12 frame widths toward Meatball (+6° rotation), a 5-frame hold with a wobble, then a 17-frame settle. The snap completes **on the impact word's frame**, the frame where v3 fires the hit flash, the shake and Meatball's launch or hit reaction.
- `strike` (`snap`, `sting`): a fast jab and return over about 12 frames.
- `shake`: an angry horizontal judder with rotation.
- `turn` (`look`): a horizontal flip through a squash, about 7 frames.
- Idle, always on: `bob` (a breathing bob of ~5 px plus a 1% scale breath) or `drift` (jellyfish: they float up and sideways and the bell pulses), set per photo with `subjects.<obs>.idle`.
- Every move eases to rest over the first and last 8 frames of the Short, so the loop seam still matches.
- SFX: a `whoosh` is added at a lunge or strike only when the beat has no SFX within 0.25 s, so impact beats keep their v3 crunch or zap.

**C. Look.** These are cartoon-cutout moves on real photos, with no AI video. Host (`blur`) shots draw the animal blurred and dimmed with no outline.

## 3. The prototype (lines unchanged from v3; moves added)
**Cassowary:**
- turn on "dagger" (hook); turn on "hi"
- **lunge on "runs"**, while Meatball bolts off instead of v3's run across the bird's head
- shake on "Sometimes"
- **lunge on "kick"** (contact: he is launched on the same frame)
- strike on "whole"; lunge on "close"

**Box jelly:**
- drift idle on every shot; turn on "brain"
- **strike on "once"** (contact: the zap, the flash and his head puffing on the same frame)
- shake on "vinegar"

**Honey badger:**
- shake on "venom"; shake on "poked" (contact)
- strike on "rips"
- **lunge on "friends"** (contact)
- turn on "twists" + shake on "inside" (contact: the grab)

Impact sequences: `grab-cassowary-kick.jpg`, `grab-boxjelly-sting.jpg`, `grab-badger-charge.jpg`. In each, frames 0-5 are the wind-up, frame 6 is impact (white flash, shake, Meatball's reaction), and 7-11 are the hold and settle.

## 4. Which cut-outs fell back, and which photos were replaced
**In the final renders: 48/48 photo shots act as cut-outs; 0 fall back.** That number comes from replacing photos, not from loosening the gates. Under Nolan's whole-animal rule, most v3 photos fail, because v3 framed tight, dramatic crops:

| Photo (iNat obs) | v3 use | Verdict | Why |
|---|---|---|---|
| Cassowary 196978347 | head close-ups (4 shots) | rejected | neck and body run off the photo (bottom edge) |
| Cassowary 223029665 | legs/dagger close-up, body | rejected | body runs off the photo (bottom) |
| Cassowary 185944564 | frontal bird | rejected **by eye** | the body runs off the photo; the matte silently stopped at the chest, so no edge was touched and the automatic check passed it. Pinned `cutout: false` |
| Cassowary 296968392 | leaf-covered head | rejected | soft, see-through matte (a leaf over the casque) |
| Box jelly 323556345, 139201356, 149206600 | hook, sting, "heart" | rejected | tentacles run off the photo (right / left / bottom) |
| Box jelly 201777123 (Alatina) | "zero brains", ask | rejected | tentacles touch the left edge |
| Box jelly 201777230 (Alatina) | "24 eyes", vinegar | rejected | matte in 9 pieces (broken tentacles) |
| Cassowary 111079594 | (first replacement pick) | rejected | its tail touches the right edge at full resolution |
| Badger 92943815 crop [0.33, 0.2, 0.62, 0.8] | "Bee larvae" | fell back once | matte in 3 pieces in that region. The shot now uses the photo's main crop, whose region gives a whole matte |
| Cassowary 98776913; badger 163519989, 250982289, 92943815 | many | **kept** | whole animal, clean matte |

**Replacements.** I scanned 149 research-grade CC0/CC BY iNaturalist photos (cassowary; box jellyfish genera) with the same `subject()` check, then picked by eye:
- **Cassowary:** 10749198, 324265024, 389877079, 142570937, 20345809.
- **Box jellyfish:** *Copula sivickisi* 144280380, 329960607, 154549857, 147738498, 83881186, 143334172, 327332202. NC-licensed hits were excluded.

The facts and lines do not change. As in v3, the jelly photos are not the deadly species named in "one kind can stop a heart". The jelly Short is now all one species (Copula), so photos repeat.

## 5. QA (automatic, from the render gate and `qa-v4.json`, plus the 2 fps sheets)
| Check | Cassowary | Box jelly | Badger |
|---|---|---|---|
| Length (20-25 s) | 24.6 s | 22.1 s | 24.7 s |
| Photo shots acting as cut-outs | 16/16 | 15/15 | 17/17 |
| Animal moves in every photo shot | yes: the idle bob/drift is always on, plus 7 / 3 / 6 timed moves | yes | yes |
| Animal touches photo edge / matte loss >3% (render fails) | 0 | 0 | 0 |
| Animal reaches the frame edge (render fails) | 0 | 0 | 0 |
| Animal under the captions | 0 frames | 0 | 0 |
| Meatball over the animal, non-contact lines | 5 frames (falling in on a tumble) | 1 (tumble) | 2 (tumble) |
| Meatball over the animal, contact lines (intended) | 10 (kick) | 16 (sting) | 29 (charge, grab) |
| Loop seam, frame 0 vs last frame (mean abs diff / 255) | 0.63 | 0.16 | 0.56 |
| Halos / fringe | none visible at 1:1 (`edge-closeup.jpg`) | none | none |

The QA covers Meatball over the animal *anywhere* (not only its head), the animal under the caption band, and the animal clipped by the frame. It counts real alpha overlap per frame, outside whip pans.

## 6. How it plugs in
- `"style": "v4"` in a script makes `explainer.py` hand the build to `tools/v3.py` (same renderer), which switches on the v4 code paths. `"style": "v3"` renders exactly as before.
- `episode.py` passes `subjects` through to each Short.
- New files: `tools/animal.py` (subject, matte, sticker, moves) and `tools/stage.py` (mark, re-framing, act re-aiming). `mascot.py` is unchanged.
- **To merge:**
  1. Apply the diff.
  2. Copy `episodes/v4-proto/script-v4-proto.json` to `scripts/v4-proto.json`.
  3. Render with `tools/episode.py scripts/v4-proto.json <slug> --skip-long`.
- It needs rembg (already installed for the thumbnails). It takes about 1.5 min per Short with `MEATBALL_JOBS=4`, plus about 10 s per new photo for the first matte.
- **For new episodes:** pick photos with the *whole* animal in frame, and glance at the cut-out once. The 185944564 case shows the automatic check can miss a matte that stops short of the photo's edge.

## 7. What's still weak (frank)
1. **Smaller animals.** A whole cassowary or badger, fitted beside an 880-size Meatball with room for a lunge, comes out at 25-60% of the frame height. The badger hook and loop frames show a badger only ~25% of the frame wide. v3's opening frame was a full-bleed photo; v4's first frame is a smaller sticker. The hook may hit softer. Options: size Meatball down to ~750 on the hook only, or let the hook animal stand *in front of* a peeking Meatball.
2. **Less photographic.** The backdrop is a blurred, painted-out copy of the photo, scaled to cover. Where the animal filled the photo, the paint-out reads as a soft smear (the cassowary "hi" shot's red and green blotches). It is consistent and calm, but it is a different look from v3's crisp photos.
3. **The moves are 2D.** The "kick" is a whole-body lunge; no leg moves. A turn is a flip. They read well at speed (the impact sequences), but they are puppetry, not behaviour.
4. **Photo choice is now the bottleneck.** The whole-animal rule rejected 9 of 13 v3 photos. Good whole-animal photos of box jellies are rare (long tentacles leave the frame), so the jelly Short repeats one species. Allow time for photo picking per episode.
5. **The automatic matte check is necessary, not sufficient.** It catches edge-touching, loss, broken pieces, see-through and low-contrast mattes. It cannot tell when rembg stops at the chest of an animal whose body continues off-photo. A human look at the cut-out stays in the loop.
6. **Meatball jumps on tumble lines.** He falls in from above for 1-5 frames over the animal. These lines are not contacts, but the overlap is brief and part of the gag.
7. **Code size.** `tools/v3.py` grows from 476 to ~720 lines. If v4 replaces v3 as the default, splitting the v4 paths into their own module is the next cleanup.

## 8. Code changes (copy's `tools/` vs repo `tools/`, unified diff)

```diff
diff --git a/tools/animal.py b/tools/animal.py
new file mode 100644
index 0000000..e51a0ed
--- /dev/null
+++ b/tools/animal.py
@@ -0,0 +1,377 @@
+#!/usr/bin/env python3
+"""Shorts v4 animal layer (research/45): find the animal in a shot's photo, cut it out whole, and make it act.
+
+Used by tools/v3.py when a script has "style": "v4". Three jobs:
+  1. subject(path, crop): rembg (isnet, as in the thumbnails) on the crop plus a margin around it (the
+     whole photo if the animal runs past that), so the cut-out is the WHOLE animal even where the shot's
+     crop clips it. Returns the subject's boxes, a head guess and a verdict: "ok", or why the shot falls
+     back to the v3 still. Hard rules (Nolan, 10/25): the animal may not touch the photo's edge (it is
+     cropped in the original), and cleaning the matte may not lose more than 3% of its area.
+     Cached per photo region in ~/.cache/meatball-subjects (MEATBALL_SUBJECT_CACHE overrides).
+  2. layers(...): the blurred, dimmed photo with the animal painted out (so a move reveals no ghost), and
+     the animal as a sticker: the full matte with holes filled, contour smoothed at render resolution, eroded
+     1 px under a uniform white stroke (so no background fringe shows), soft drop shadow.
+  3. transform(...): the animal's 2D move per frame (bob, drift, lunge, strike, shake, turn).
+
+Script fields: beat "animal": "lunge@kick" (move@word|seconds; a list for several), beat "contact": true
+(Meatball may touch it: a poke, sting or kick), spec "subjects": {obs: {"head": [...], "cutout": false,
+"idle": "drift"}} (photo fractions).
+"""
+import hashlib
+import json
+import math
+import os
+
+import cv2
+import numpy as np
+from PIL import Image, ImageEnhance
+
+CACHE = os.environ.get("MEATBALL_SUBJECT_CACHE", os.path.expanduser("~/.cache/meatball-subjects"))
+MAX_SIDE = 2048   # rembg input cap (isnet runs at 1024 internally; the soft matte is upsampled)
+_SESSION = None
+VERSION = 5       # cache version (v3: whole-animal region mattes, loss vs nearby raw pieces)
+
+# quality gate: a cut-out that fails any of these falls back to the v3 still for that shot
+MIN_AREA = 0.02   # subject share of the crop
+MAX_SOFT = 0.70   # share of the matte that is semi-transparent (water, glass, fog)
+MIN_EDGE = 14.0   # mean Lab difference across the matte edge (low = camouflage, dark water)
+MAX_LOSS = 0.03   # cleaning the matte may drop at most this share of the raw subject
+STROKE = 7        # white outline width, px at base resolution (~6 px on screen)
+
+
+def _session():
+    global _SESSION
+    if _SESSION is None:
+        from rembg import new_session
+        _SESSION = new_session("isnet-general-use")
+    return _SESSION
+
+
+def _key(path, reg):
+    raw = f"v{VERSION}|{os.path.basename(path)}|{os.path.getsize(path)}|{tuple(round(c, 4) for c in reg)}"
+    return hashlib.sha1(raw.encode()).hexdigest()[:16]
+
+
+def _region(crop, grow=True):
+    c = crop or [0, 0, 1, 1]
+    if not grow:
+        return [0.0, 0.0, 1.0, 1.0]
+    w, h = c[2] - c[0], c[3] - c[1]
+    return [max(0.0, c[0] - 0.6 * w), max(0.0, c[1] - 0.3 * h), min(1.0, c[2] + 0.6 * w), min(1.0, c[3] + 0.3 * h)]
+
+
+def _px(path, reg):
+    W, H = Image.open(path).size
+    return int(reg[0] * W), int(reg[1] * H), int(reg[2] * W), int(reg[3] * H)
+
+
+def matte(path, reg):
+    """(region image, soft rembg matte at region resolution), cached per photo region."""
+    os.makedirs(CACHE, exist_ok=True)
+    f = f"{CACHE}/{_key(path, reg)}.png"
+    im = Image.open(path).convert("RGB").crop(_px(path, reg))
+    if not os.path.exists(f):
+        from rembg import remove
+        s = min(1.0, MAX_SIDE / max(im.size))
+        small = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS) if s < 1 else im
+        # same pre-boost as thumb3.cutout: rembg separates saturated subjects better
+        boost = ImageEnhance.Color(ImageEnhance.Contrast(small).enhance(1.12)).enhance(1.3)
+        remove(boost, session=_session(), only_mask=True).save(f)
+    a = np.asarray(Image.open(f).convert("L").resize(im.size, Image.BILINEAR))
+    return im, a
+
+
+def _fill(m, frac=0.01):
+    """Fill the matte's holes (pinholes in fur, a dark eye) but not the big enclosed gaps of real background,
+    such as between legs whose toes touch: a hole bigger than `frac` of the animal stays open."""
+    flood = np.pad(m, 1).copy()
+    cv2.floodFill(flood, None, (0, 0), 1)
+    holes = (1 - flood[1:-1, 1:-1]).astype(np.uint8)
+    n, lab, st, _ = cv2.connectedComponentsWithStats(holes, connectivity=4)
+    small = [k for k in range(1, n) if st[k, cv2.CC_STAT_AREA] <= frac * m.sum()]
+    return m | np.isin(lab, small).astype(np.uint8)
+
+
+def _smooth(m, sigma):
+    return (cv2.GaussianBlur(m.astype(np.float32), (0, 0), sigma) > 0.5).astype(np.uint8)
+
+
+def _head(m, facing=None):
+    """Head box guess (pixels): the top band of an upright subject, else the snout end of a long one."""
+    ys, xs = np.nonzero(m)
+    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
+    w, h = x1 - x0 + 1, y1 - y0 + 1
+    if h >= 0.8 * w:
+        band = m[y0:y0 + int(0.28 * h)]
+        cols = np.nonzero(band.any(0))[0]
+        return [int(cols.min()), int(y0), int(cols.max()), int(y0 + 0.28 * h)], "top"
+    sl = int(0.3 * w)
+    left, right = m[:, x0:x0 + sl].sum(), m[:, x1 - sl:x1 + 1].sum()
+    side = facing or ("left" if left < right else "right")
+    xa, xb = (x0, x0 + sl) if side == "left" else (x1 - sl, x1)
+    rows = np.nonzero(m[:, xa:xb + 1].any(1))[0]
+    return [int(xa), int(rows.min()), int(xb), int(rows.max())], side
+
+
+def _mask(path, crop, reg):
+    """(region image, raw hard mask of the subject's components, cleaned mask) in region pixels."""
+    im, a = matte(path, reg)
+    rx0, ry0, rx1, ry1 = _px(path, reg)
+    cx0, cy0, cx1, cy1 = _px(path, crop or [0, 0, 1, 1])
+    hard = (a > 128).astype(np.uint8)
+    n, lab, st, _ = cv2.connectedComponentsWithStats(hard, connectivity=8)
+    inside = np.zeros_like(hard)
+    inside[max(0, cy0 - ry0):cy1 - ry0, max(0, cx0 - rx0):cx1 - rx0] = 1
+    if n < 2:
+        return im, a, hard, hard
+    score = np.bincount(lab[inside.astype(bool)].ravel(), minlength=n)[1:]
+    if score.max() == 0:
+        return im, a, np.zeros_like(hard), np.zeros_like(hard)
+    main = int(score.argmax()) + 1
+    big = st[main, cv2.CC_STAT_AREA]
+    near = [k + 1 for k in range(n - 1) if score[k] > 0]          # everything rembg found that reaches the shot
+    keep = [k for k in near if st[k, cv2.CC_STAT_AREA] >= 0.15 * big or k == main]
+    m = np.isin(lab, keep).astype(np.uint8)
+    # raw = every piece rembg found within reach of the animal (2% of the region); far-off specks (marine
+    # snow, leaves) are not the animal, nearby pieces (a tentacle the matte broke off) are
+    reach = cv2.dilate(m, np.ones((2 * int(0.02 * max(m.shape)) + 1,) * 2, np.uint8))
+    raw = np.isin(lab, [k for k in near if (reach[lab == k]).any()]).astype(np.uint8)
+    m = _smooth(_fill(m), max(1.0, 0.0015 * max(m.shape)))      # holes filled, jaggies off; no opening
+    return im, a, raw, m
+
+
+def subject(path, crop, parent=None):
+    """Subject facts for one shot, boxes in crop fractions (a whole animal may extend past 0..1). A tighter
+    re-cut of a shot (`parent` = the shot's crop) uses its parent's region, so both share one outline."""
+    for grow in (True, False):
+        reg = _region(parent or crop, grow)
+        jf = f"{CACHE}/{_key(path, reg)}_{_key(path, crop or [0, 0, 1, 1])}.json"
+        if os.path.exists(jf):
+            info = json.load(open(jf))
+        else:
+            im, a, raw, m = _mask(path, crop, reg)
+            info = _facts(path, crop, reg, im, a, raw, m)
+            os.makedirs(CACHE, exist_ok=True)
+            json.dump(info, open(jf, "w"))
+        info["crop"] = list(crop or [0, 0, 1, 1])
+        if not info.get("interior"):   # whole animal inside this region, or it already is the photo
+            break
+    return info
+
+
+def _facts(path, crop, reg, im, a, raw, m):
+    H, W = m.shape
+    rx0, ry0, rx1, ry1 = _px(path, reg)
+    cx0, cy0, cx1, cy1 = _px(path, crop or [0, 0, 1, 1])
+    info = dict(reg=reg)
+    if m.sum() < 50:
+        return dict(info, quality="no subject found")
+    b = 2
+    edges = {"top": m[:b].any(), "bottom": m[-b:].any(), "left": m[:, :b].any(), "right": m[:, -b:].any()}
+    photo_edge = {"top": reg[1] <= 0, "bottom": reg[3] >= 1, "left": reg[0] <= 0, "right": reg[2] >= 1}
+    touch = [k for k, v in edges.items() if v and photo_edge[k]]
+    interior = [k for k, v in edges.items() if v and not photo_edge[k]]
+    parts = cv2.connectedComponents(m, connectivity=8)[0] - 1
+    loss = float((raw & (1 - m)).sum()) / max(1.0, float(raw.sum()))
+    in_crop = m[max(0, cy0 - ry0):cy1 - ry0, max(0, cx0 - rx0):cx1 - rx0]
+    area = float(in_crop.sum()) / max(1.0, float((cx1 - cx0) * (cy1 - cy0)))
+    soft = float(((a > 25) & (a < 230) & (cv2.dilate(m, np.ones((9, 9), np.uint8)) > 0)).sum()) / max(1.0, float(m.sum()))
+    lab = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2LAB).astype(np.float32)
+    k = max(3, int(0.012 * max(W, H)))
+    ker = np.ones((k, k), np.uint8)
+    inner = (m - cv2.erode(m, ker)).astype(bool)
+    outer = (cv2.dilate(m, ker) - m).astype(bool)
+    edge = float(np.linalg.norm(lab[inner].mean(0) - lab[outer].mean(0))) if inner.any() and outer.any() else 0.0
+    ys, xs = np.nonzero(m)
+    hb, side = _head(m)
+    cw, ch = cx1 - cx0, cy1 - cy0
+    f = lambda r: [round((r[0] + rx0 - cx0) / cw, 4), round((r[1] + ry0 - cy0) / ch, 4),
+                   round((r[2] + 1 + rx0 - cx0) / cw, 4), round((r[3] + 1 + ry0 - cy0) / ch, 4)]
+    q = "ok"
+    if interior:
+        q = "runs past the search region"
+    elif touch:
+        q = f"animal cropped in the photo (touches the {'/'.join(touch)} edge)"
+    elif parts > 2:
+        q = f"matte in pieces ({parts} parts: broken tentacles or legs)"
+    elif loss > MAX_LOSS:
+        q = f"matte clean-up would lose {loss:.0%} of the animal"
+    elif area < MIN_AREA:
+        q = f"subject too small ({area:.0%})"
+    elif soft > MAX_SOFT:
+        q = f"soft, see-through matte ({soft:.0%})"
+    elif edge < MIN_EDGE:
+        q = f"low edge contrast ({edge:.1f})"
+    return dict(info, quality=q, interior=interior, touch=touch, loss=round(loss, 4), area=round(area, 4),
+                soft=round(soft, 3), edge=round(edge, 1), box=f([xs.min(), ys.min(), xs.max(), ys.max()]),
+                head=f(hb), head_from=side, cx=round((float(xs.mean()) + rx0 - cx0) / cw, 4),
+                cy=round((float(ys.mean()) + ry0 - cy0) / ch, 4))
+
+
+# ---------------------------------------------------------------- pictures
+
+def photo_box(path, info):
+    """The subject's box in photo pixels (from subject()'s crop-fraction box)."""
+    cx0, cy0, cx1, cy1 = _px(path, info["crop"])
+    b = info["box"]
+    cw, ch = cx1 - cx0, cy1 - cy0
+    return [cx0 + b[0] * cw, cy0 + b[1] * ch, cx0 + b[2] * cw, cy0 + b[3] * ch]
+
+
+def layers(path, crop, reg, g, g_bg, blur=False):
+    """The shot re-framed around the whole animal: (background RGB = the whole photo at scale g_bg, blurred
+    and dimmed with the animal painted out; premultiplied RGBA sticker of the animal at scale g (screen px
+    per photo px); the sticker's offset in g-scaled photo px). The background is scaled at least to cover
+    the frame, so it may be larger than the animal's scale; it is only ever seen soft."""
+    im, a, raw, m = _mask(path, crop, reg)
+    rx0, ry0, _, _ = _px(path, reg)
+    photo = Image.open(path).convert("RGB")
+    PW, PH = photo.size
+    gw, gh = max(1, int(PW * g_bg)), max(1, int(PH * g_bg))
+    # background: paint the animal out at a quarter of the output scale, then blur and dim
+    sw, sh = max(8, gw // 4), max(8, gh // 4)
+    small = np.asarray(photo.resize((sw, sh), Image.BILINEAR))
+    full_m = np.zeros((PH, PW), np.uint8)
+    full_m[ry0:ry0 + m.shape[0], rx0:rx0 + m.shape[1]] = m
+    hole = cv2.dilate(cv2.resize(full_m * 255, (sw, sh), interpolation=cv2.INTER_AREA),
+                      np.ones((7, 7), np.uint8))
+    fill = cv2.inpaint(small, (hole > 30).astype(np.uint8) * 255, 6, cv2.INPAINT_TELEA)
+    bg = cv2.GaussianBlur(cv2.resize(fill, (gw, gh), interpolation=cv2.INTER_LINEAR).astype(np.float32),
+                          (0, 0), 14) * 0.78
+    # sticker: the subject's box (+ room for the stroke and shadow) at scale g
+    yy, xx = np.nonzero(m)
+    pad = int((STROKE + 30) / g) + 2
+    x0, y0 = max(0, xx.min() - pad), max(0, yy.min() - pad)
+    x1, y1 = min(m.shape[1], xx.max() + pad + 1), min(m.shape[0], yy.max() + pad + 1)
+    tw, th = max(1, int((x1 - x0) * g)), max(1, int((y1 - y0) * g))
+    col = np.asarray(im.crop((x0, y0, x1, y1)).resize((tw, th), Image.LANCZOS)).astype(np.float32)
+    # contour at output resolution: resample, smooth, threshold -> one clean curve, no stair steps
+    mm = cv2.resize(m[y0:y1, x0:x1].astype(np.float32), (tw, th), interpolation=cv2.INTER_AREA if g < 1 else cv2.INTER_LINEAR)
+    mm = (cv2.GaussianBlur(mm, (0, 0), 1.2) > 0.5).astype(np.uint8)
+    core = cv2.erode(mm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # 1 px in: no fringe
+    alpha = cv2.GaussianBlur(core.astype(np.float32), (0, 0), 0.7)
+    dist = cv2.distanceTransform((1 - core).astype(np.uint8), cv2.DIST_L2, 5)
+    rim = np.clip(STROKE + 0.5 - dist, 0, 1)                                  # uniform-width white stroke
+    shadow = cv2.warpAffine(cv2.GaussianBlur(np.maximum(rim, alpha), (0, 0), 8) * 0.42,
+                            np.float32([[1, 0, 5], [0, 1, 8]]), (tw, th))
+    if blur:  # host shot: the animal stays soft and dim like the rest of the picture, no outline
+        A = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 4)
+        C = cv2.GaussianBlur(col, (0, 0), 7) * 0.80 * A[..., None]
+    else:
+        C = np.array([30, 6, 0], np.float32) * shadow[..., None]
+        A = shadow
+        C = 255 * rim[..., None] + C * (1 - rim[..., None])
+        A = rim + A * (1 - rim)
+        C = col * alpha[..., None] + C * (1 - alpha[..., None])
+        A = alpha + A * (1 - alpha)
+    st = np.dstack([np.clip(C, 0, 255), np.clip(A * 255, 0, 255)]).astype(np.uint8)
+    return np.clip(bg, 0, 255).astype(np.uint8), st, ((rx0 + x0) * g, (ry0 + y0) * g)
+
+
+# ---------------------------------------------------------------- acting
+
+MOVES = ("lunge", "kick", "charge", "strike", "snap", "sting", "bob", "breathe", "drift", "shake", "turn", "look")
+ALIAS = {"kick": "lunge", "charge": "lunge", "snap": "strike", "sting": "strike", "breathe": "bob", "look": "turn"}
+SFX = {"lunge": ("whoosh", -0.16), "strike": ("whoosh", -0.10), "turn": ("whoosh", 0.0)}
+
+
+def parse(spec):
+    """'lunge@kick' or ['drift', 'strike@once'] -> [(move, at)]"""
+    if not spec:
+        return []
+    spec = [spec] if isinstance(spec, str) else spec
+    out = []
+    for e in spec:
+        nm, _, at = e.partition("@")
+        out.append((ALIAS.get(nm, nm), at or None))
+    return out
+
+
+def _ease(u):
+    u = min(max(u, 0.0), 1.0)
+    return u * u * (3 - 2 * u)
+
+
+def lunge(dt, toward):
+    """Kick / charge toward Meatball: 5-frame wind-up (lean back, squash), 2-frame snap (scale up +
+    translate), hold, settle. dt = seconds from the impact frame. Returns (dx, dy, scale, sx, sy, rot)."""
+    fps = 30.0
+    k = dt * fps
+    if k < -5 or k > 22:
+        return 0, 0, 1, 1, 1, 0
+    if k < -2:            # wind-up: back and down
+        u = _ease((k + 5) / 3)
+        return -0.035 * toward * u, 0.012 * u, 1 - 0.03 * u, 1 + 0.05 * u, 1 - 0.06 * u, -4 * toward * u
+    if k < 0:             # snap: two frames to full extension
+        u = (k + 2) / 2
+        return (-0.035 + 0.155 * u) * toward, 0.012 - 0.03 * u, 0.97 + 0.21 * u, 1.05 - 0.09 * u, 0.94 + 0.12 * u, (-4 + 10 * u) * toward
+    if k < 5:             # impact hold with a tiny overshoot wobble
+        w = math.sin(k * 1.9) * math.exp(-k / 2)
+        return 0.12 * toward, -0.018, 1.18 + 0.02 * w, 0.96 - 0.02 * w, 1.06 + 0.02 * w, 6 * toward
+    u = _ease((k - 5) / 17)  # settle back home
+    return 0.12 * toward * (1 - u), -0.018 * (1 - u), 1 + 0.18 * (1 - u), 1 - 0.04 * (1 - u), 1 + 0.06 * (1 - u), 6 * toward * (1 - u)
+
+
+def strike(dt, toward):
+    """Fast jab and return (sting, snap, bite): 3-frame cock back, 2-frame jab, 6-frame return."""
+    k = dt * 30.0
+    if k < -3 or k > 9:
+        return 0, 0, 1, 1, 1, 0
+    if k < -1:
+        u = _ease((k + 3) / 2)
+        return -0.025 * toward * u, 0, 1 - 0.02 * u, 1, 1, -3 * toward * u
+    if k < 1:
+        u = (k + 1) / 2
+        return (-0.025 + 0.115 * u) * toward, -0.01 * u, 0.98 + 0.12 * u, 1, 1, (-3 + 8 * u) * toward
+    u = _ease((k - 1) / 8)
+    return 0.09 * toward * (1 - u), -0.01 * (1 - u), 1.10 - 0.10 * u, 1, 1, 5 * toward * (1 - u)
+
+
+def idle(t, kind, seed):
+    """Always-on motion so a cut-out is never frozen: a breathing bob, or a slow drift for floaters."""
+    ph = (seed * 1.7) % 6.28
+    if kind == "drift":   # jellyfish / fish: float up and sideways, the bell pulses
+        pulse = math.sin(2 * math.pi * 0.9 * t + ph)
+        return (0.018 * math.sin(2 * math.pi * 0.23 * t + ph), -0.014 * t + 0.01 * math.sin(2 * math.pi * 0.4 * t),
+                1.0, 1 + 0.025 * pulse, 1 - 0.03 * pulse, 2.0 * math.sin(2 * math.pi * 0.3 * t + ph))
+    b = math.sin(2 * math.pi * 0.75 * t + ph)
+    return 0.0, -0.0045 * (1 - math.cos(2 * math.pi * 0.75 * t)) / 2, 1.0, 1 - 0.006 * b, 1 + 0.010 * b, 0.6 * b
+
+
+def shake(dt, dur=0.7):
+    if dt < 0 or dt > dur:
+        return 0.0, 0.0
+    env = math.exp(-dt * 3) * 1.0
+    return 0.012 * env * math.sin(2 * math.pi * 14 * dt), 3.5 * env * math.sin(2 * math.pi * 11 * dt + 1)
+
+
+def transform(moves, t, toward, seed, idle_kind="bob", n_left=None, ts=None, n_from=None):
+    """Combined move at beat time t (s); ts = seconds into the shot (the idle restarts each shot).
+    moves = [(name, t_at)]. Returns dict(dx, dy (frame-width fractions), s, sx, sy, rot (deg),
+    flip (0..1 progress of a turn: sx goes 1 -> -1 through a squash)). n_left / n_from = frames to the end /
+    from the start of the Short: the move eases to rest there, so the loop's last frame matches frame 0."""
+    dx, dy, s, sx, sy, rot = idle(t if ts is None else ts, idle_kind, seed)
+    flip = 0.0
+    for nm, ta in moves:
+        dt = t - ta
+        if nm == "lunge":
+            m = lunge(dt, toward)
+        elif nm == "strike":
+            m = strike(dt, toward)
+        elif nm == "shake":
+            x, r = shake(dt)
+            m = (x, 0, 1, 1, 1, r)
+        elif nm == "turn":
+            u = _ease(dt / 0.22)
+            flip = max(flip, u)
+            sq = math.sin(math.pi * u) if 0 < u < 1 else 0
+            m = (0, 0.006 * sq, 1, 1, 1 - 0.07 * sq, 0)
+        else:
+            continue
+        dx, dy, rot = dx + m[0], dy + m[1], rot + m[5]
+        s, sx, sy = s * m[2], sx * m[3], sy * m[4]
+    edge = min(n_left if n_left is not None else 99, n_from if n_from is not None else 99)
+    if edge < 8:   # ease to rest at the loop seam (last frame = frame 0)
+        e = _ease(edge / 8)
+        dx, dy, rot, s, sx, sy = dx * e, dy * e, rot * e, 1 + (s - 1) * e, 1 + (sx - 1) * e, 1 + (sy - 1) * e
+    return dict(dx=dx, dy=dy, s=s, sx=sx, sy=sy, rot=rot, flip=flip)
diff --git a/tools/episode.py b/tools/episode.py
index a430196..95a0086 100644
--- a/tools/episode.py
+++ b/tools/episode.py
@@ -154,6 +154,7 @@ def main():
                    "music": spec.get("music"), "style": spec.get("style"),
                    **({"pitch": spec["pitch"]} if spec.get("pitch") else {}),
                    **({"tempo": spec["tempo"]} if spec.get("tempo") else {}),  # v3: atempo speed-up
+                   **({"subjects": spec["subjects"]} if spec.get("subjects") else {}),  # v4: per-photo pins
                    # "short_beats" lets a joke-dense script keep more than 3 hand-picked beats (default 3).
                    "beats": hook_loop(mb) if hook else loop(tighten(mb, spec.get("short_beats", 3)))},
                   open(sspec, "w"))
diff --git a/tools/explainer.py b/tools/explainer.py
index a0d0b2e..b18c8a4 100644
--- a/tools/explainer.py
+++ b/tools/explainer.py
@@ -962,7 +962,7 @@ def main():
         MUSIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", spec["music"])
     if a.vertical:
         vertical()
-    if spec.get("style") == "v3" and a.stage == "build":  # Shorts v3 (research/44): tools/v3.py renders it
+    if spec.get("style") in ("v3", "v4") and a.stage == "build":  # Shorts v3/v4 (research/44, 45): tools/v3.py
         import v3
         return v3.build(spec, a.work, a.out, MUSIC)  # v3 imports explainer afresh: pass the bed
     if a.stage == "images":
diff --git a/tools/stage.py b/tools/stage.py
new file mode 100644
index 0000000..aaeeca8
--- /dev/null
+++ b/tools/stage.py
@@ -0,0 +1,206 @@
+#!/usr/bin/env python3
+"""Shorts v4 staging (research/45). Two jobs:
+  1. Meatball's mark and facing: on cut-out shots he keeps his left-hand mark (v3.HOME_V4); on a v3 still
+     (the animal can't move) place() keeps him off its head (a pinned head box) unless the beat is a contact.
+  2. frame_fit(): re-frame a cut-out shot around the whole animal, as large as fits, with room for its moves,
+     in the free space beside (or above) him, above the captions and inside the frame.
+track() re-aims mascot.act_track so he faces the animal and flees, peeks and cowers on the far side.
+Boxes are screen pixels (1080x1920).
+"""
+import math
+
+from PIL import Image
+
+W, H = 1080, 1920
+FLOOR = 1430
+Z_RANGE = (1.0, 1.14)
+# Meatball's body box around his hip mark, in drawing units at size 1000 (hat to feet, arms in)
+MB_HALF_W, MB_TOP = 255, 860
+_SIZES = {}
+
+
+def crop_size(path, crop):
+    if path not in _SIZES:
+        _SIZES[path] = Image.open(path).size
+    w, h = _SIZES[path]
+    c = crop or [0, 0, 1, 1]
+    return (c[2] - c[0]) * w, (c[3] - c[1]) * h
+
+
+def to_screen(path, crop, box, z, R=1.15):
+    """Crop-fraction box -> screen box at zoom z (the v3 base: cover W*R x H*R, centre-crop, view())."""
+    cw, ch = crop_size(path, crop)
+    bw, bh = int(W * R), int(H * R)
+    s = max(bw / cw, bh / ch)
+    l, t = (int(cw * s) + 1 - bw) // 2, (int(ch * s) + 1 - bh) // 2
+    k = (W / bw) * z
+    f = lambda fx, fy: (k * (fx * cw * s - l - bw / 2) + W / 2, k * (fy * ch * s - t - bh / 2) + H / 2)
+    x0, y0 = f(box[0], box[1])
+    x1, y1 = f(box[2], box[3])
+    return [x0, y0, x1, y1]
+
+
+def union(boxes):
+    boxes = [b for b in boxes if b]
+    if not boxes:
+        return None
+    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]
+
+
+def clip(b):
+    if not b:
+        return None
+    b = [max(0, b[0]), max(0, b[1]), min(W, b[2]), min(H, b[3])]
+    return b if b[2] > b[0] and b[3] > b[1] else None
+
+
+def area(b):
+    return 0.0 if not b else max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
+
+
+def inter(a, b):
+    if not a or not b:
+        return 0.0
+    return area([max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])]) if (
+        min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])) else 0.0
+
+
+def mb_box(x, size):
+    k = size / 1000.0
+    return [x * W - MB_HALF_W * k, FLOOR - MB_TOP * k, x * W + MB_HALF_W * k, FLOOR]
+
+
+def shot_boxes(sh):
+    """(head box, body box, body centre x) on screen for a shot with subject info, else Nones."""
+    info = sh.get("subj")
+    if not info or "head" not in info:
+        return None, None, None
+    head = clip(union([to_screen(sh["path"], sh["crop"], info["head"], z) for z in Z_RANGE]))
+    body = clip(union([to_screen(sh["path"], sh["crop"], info["box"], z) for z in Z_RANGE]))
+    cx = to_screen(sh["path"], sh["crop"], [info["cx"], info["cy"], info["cx"], info["cy"]], 1.0)[0]
+    return head, body, cx
+
+
+def place(shots, n, contact=False, home=0.24, size=1000):
+    """Meatball's mark over v3 stills (the animal can't move there): (x, size, side, head overlap), clear of
+    the animal's head (a pinned head box) unless the beat is a contact. side = +1 when the animal is to his
+    right. Shots are weighted by screen time; host (blurred) shots don't count. Without facts: the v3 mark."""
+    facts = [(shot_boxes(s), max(1, s["f1"] - s["f0"])) for s in shots]
+    facts = [(f, w) for (f, w), s in zip(facts, shots) if f[0] is not None and not s.get("blur")]
+    if not facts:
+        return home, size, 1, None
+    tot = sum(w for _, w in facts)
+    cx = sum(f[2] * w for f, w in facts) / tot
+    heads = union([f[0] for f, _ in facts])
+    best = None
+    for k in (1.0, 0.9, 0.8):
+        sz = int(size * k)
+        lo = MB_HALF_W * sz / 1000 / W + 0.02   # keep his whole body on screen
+        for i in range(31):
+            x = lo + (1 - 2 * lo) * i / 30
+            mb = mb_box(x, sz)
+            head_ov = sum(w * inter(mb, f[0]) / max(1.0, area(f[0])) for f, w in facts) / tot
+            body_ov = sum(w * inter(mb, f[1]) / area(mb) for f, w in facts) / tot
+            if contact:  # touch the head from the free side: overlap it by about a fifth of his width
+                d = 0.2 * (mb[2] - mb[0])
+                cost = min(abs(mb[2] - (heads[0] + d)), abs(mb[0] - (heads[2] - d))) / W + 0.4 * (1 - k)
+            else:
+                cost = 12 * head_ov + 1.2 * body_ov + 1.5 * (1 - k) + 0.15 * abs(x - home)
+            if best is None or cost < best[0]:
+                best = (cost, x, sz, head_ov)
+    _, x, sz, head_ov = best
+    return x, sz, (1 if cx >= x * W else -1), head_ov
+
+
+# ---------------------------------------------------------------- fitting a cut-out (v4)
+
+SAFE = (0.03 * W, 130.0, 0.97 * W, 1465.0)   # the animal stays inside this: clear of the Shorts UI and captions
+GAP = 40.0   # clear air between Meatball (who leans and trembles) and the animal
+REACH = {"lunge": (0.12, 1.18), "strike": (0.09, 1.10)}   # forward reach (frame widths), peak scale
+
+
+LEAN = {"peek": 0.17, "loop_out": 0.17}   # acts that lean his head toward the animal (frame widths at size 1000)
+
+
+def regions(x, size, side, top=SAFE[1], contact=False, act=None):
+    """Free screen rectangles for the animal around Meatball's mark: beside him (on the animal's side) and
+    above him. A contact beat lets the animal's box reach a quarter of the way into his."""
+    mb = mb_box(x, size)
+    reach = 0.25 * (mb[2] - mb[0]) if contact else -GAP - LEAN.get(act, 0.0) * W * size / 1000
+    beside = [mb[2] - reach, top, SAFE[2], SAFE[3]] if side == 1 else [SAFE[0], top, mb[0] + reach, SAFE[3]]
+    above = [SAFE[0], top, SAFE[2], mb[1] - GAP]
+    return [r for r in (beside, above) if r[2] - r[0] > 60 and r[3] - r[1] > 60]
+
+
+def envelope(box, moves, idle, toward, contact):
+    """The screen box an animal can occupy during its moves: peak scale about its feet, drift, and (unless
+    the beat is a contact) its forward reach toward Meatball."""
+    names = [m for m, _ in moves]
+    sc = max([REACH[m][1] for m in names if m in REACH] + [1.02])
+    fwd = 0.0 if contact else max([REACH[m][0] for m in names if m in REACH] + [0.0]) * W
+    x0, y0, x1, y1 = box
+    cx = (x0 + x1) / 2
+    e = [cx + sc * (x0 - cx), y1 + sc * (y0 - y1), cx + sc * (x1 - cx), y1]
+    if idle == "drift":
+        e = [e[0] - 0.02 * W, e[1] - 0.05 * W, e[2] + 0.02 * W, e[3] + 0.012 * W]
+    else:
+        e = [e[0] - 4, e[1] - 0.012 * W, e[2] + 4, e[3] + 4]
+    if fwd:
+        back = 0.045 * W   # the wind-up leans back before the snap
+        e = ([e[0] - fwd, e[1] - 0.03 * W, e[2] + back, e[3]] if toward == -1 else
+             [e[0] - back, e[1] - 0.03 * W, e[2] + fwd, e[3]])
+    return e
+
+
+def frame_fit(box, moves, idle, side, contact, rects, gmax=1.0):
+    """Re-frame a cut-out shot around the whole animal. box = the animal in photo px. Returns
+    dict(g, tx, ty): screen = (tx, ty) + g * photo px, the largest scale (up to gmax) at which the animal and
+    the room its moves need fit one free rectangle; it stands on that rectangle's floor (floats in the
+    middle if it drifts) at the edge nearest Meatball, so the two read as a scene."""
+    best = None
+    for r, pref in zip(rects, (1.0, 0.5)):   # beside him (on the ground) beats floating above him
+        g = gmax
+        for _ in range(6):
+            e = envelope([v * g for v in box], moves, idle, -side, contact)
+            k = min(1.0, (r[2] - r[0]) / (e[2] - e[0]), (r[3] - r[1]) / (e[3] - e[1]))
+            if k >= 0.999:
+                break
+            g *= k * 0.995
+        ex = r[0] - e[0] if side == 1 else r[2] - e[2]
+        ey = ((r[1] + r[3]) - (e[1] + e[3])) / 2 if idle == "drift" else r[3] - e[3]
+        if best is None or g * pref > best[0]:
+            best = (g * pref, dict(g=g, tx=ex, ty=ey, env=[e[0] + ex, e[1] + ey, e[2] + ex, e[3] + ey]))
+    return best[1]
+
+
+# acts whose v3 track already moves the right way when the animal is on Meatball's RIGHT (+1) or LEFT (-1)
+BASE_SIDE = {"launch": -1, "run_off": -1, "peek": -1, "loop_out": -1}
+TRAVEL = ("run_in", "run_off", "run_across", "launch")
+
+
+def track(mascot, act, n, fps, t_act, home, side, seed):
+    """mascot.act_track re-aimed for the v4 layout: he faces the animal, flees and is flung away from it,
+    peeks and cowers from the far edge, and a peek ends on his mark instead of a fixed spot."""
+    mirror = side != BASE_SIDE.get(act, 1)
+    built = 1 - home if (mirror and act in TRAVEL) else home
+    out = []
+    for e in mascot.act_track(act, n, fps, t_act, built, seed=seed):
+        e = dict(e)
+        m = mirror
+        if act in ("peek", "loop_out"):   # v3 slides in from x=1.4 to 0.9; here from the far edge to the mark
+            p = (1.4 - e["x"]) / 0.5
+            mark = 1 - home if mirror else home
+            e["x"] = 1.4 + (mark - 1.4) * p
+        elif act == "hide":               # cower at the edge away from the animal, leaning toward it
+            e["x"], e["rot"], m = (0.14 if side == 1 else 0.86), 8.0 * side, False
+        if m:
+            e["x"] = 1 - e["x"] if (act in TRAVEL or act in ("peek", "loop_out")) else 2 * home - e["x"]
+            e["rot"] = -e["rot"]
+        face = side
+        if act == "run_off" and e.get("run") is not None:
+            face = -side                  # bolting away
+        elif act == "run_across":
+            face = 1
+        e["flip"] = face == -1
+        out.append(e)
+    return out
diff --git a/tools/v3.py b/tools/v3.py
index 0ee77bb..3ffac22 100644
--- a/tools/v3.py
+++ b/tools/v3.py
@@ -22,6 +22,26 @@ Spec fields (all optional unless noted):
   shot "whip": false     hard cut instead of a whip pan (cuts to a different photo whip by default)
   shot "blur": true      blurred, dimmed photo (a host shot)
 Photos come from explainer.photo() (pinned iNaturalist observations, full resolution).
+
+"style": "v4" (research/45) adds, on top of everything above:
+  whole-animal cut-outs  every photo shot is cut out (tools/animal.py): the WHOLE animal, holes under 1%
+                         filled, contour smoothed, 1 px under a uniform white stroke, soft shadow. The shot is
+                         re-framed around it (tools/stage.py): as large as fits beside Meatball (above him if
+                         it must), clear of him, the captions and the frame edge, standing on the free space's
+                         floor, over its own photo blurred and dimmed with the animal painted out
+  animal acting          the cut-out always moves (bob, or "drift" for floaters); beat "animal": "lunge@kick" /
+                         ["turn@twists", "shake@inside"] adds lunge|kick|charge, strike|snap|sting, shake,
+                         turn|look, timed to a word, with a matching SFX unless the beat has one there
+  Meatball               keeps his left-hand mark and faces the animal; flees, is flung, peeks and cowers away
+                         from it (on a v3 still his mark comes from the pinned head instead)
+  beat "contact": true   Meatball and the animal may touch (a poke, a sting, a kick)
+  spec "subjects"        per iNaturalist obs: {"head": [x0, y0, x1, y1] photo fractions (steers Meatball on a
+                         v3 still), "cutout": false, "idle": "drift"}
+  gates                  a photo whose animal runs off the photo's edge, a matte in pieces or one whose clean-up
+                         would lose >3% of it, a see-through or low-contrast matte: that shot falls back to the
+                         v3 still (listed as V4 FALLBACK). The render fails if a cut-out breaks the edge/loss
+                         rule or an acting animal leaves the frame; Meatball-over-animal and animal-under-caption
+                         frames are reported per beat (V4 QA, and v4.json in the work dir)
 """
 import json
 import math
@@ -34,8 +54,10 @@ import cv2
 import numpy as np
 from PIL import Image, ImageDraw, ImageFilter, ImageFont
 
+import animal
 import explainer as ex
 import mascot
+import stage
 
 FPS, W, H, SR = 30, 1080, 1920, 48000
 ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@@ -49,6 +71,7 @@ CAP_Y = 1560
 MAX_SHOT = 2.4    # a shot longer than this is re-cut to a tighter crop of the same photo (gate: 2.5 s)
 PUSH = 0.045      # zoom per second of the slow push (v2: 0.036)
 HOME = 0.24       # Meatball's mark: left of centre, so the animal (centred in each crop) stays visible
+HOME_V4, SIZE_V4 = 0.21, 880   # v4: a little smaller and nearer the edge, so a whole animal fits beside him
 PLAN = {}         # filled before the frame workers fork
 
 
@@ -177,8 +200,10 @@ def sprite(st, size):
 
 def place_meatball(frame, st, tr, size):
     if tr["hidden"]:
-        return
+        return None
     spr, pad = sprite(st, size)
+    if tr.get("flip"):  # v4: face the animal on his left (the rig is symmetric about the hip)
+        spr = spr[:, ::-1]
     k = size / 1000.0
     hip = np.array([pad + 500 * k, pad + 790 * k])
     feet = np.array([pad + 500 * k, pad + 960 * k])
@@ -195,20 +220,85 @@ def place_meatball(frame, st, tr, size):
     x0, y0 = int(max(0, pts[0].min())), int(max(0, pts[1].min()))
     x1, y1 = int(min(W, pts[0].max() + 1)), int(min(H, pts[1].max() + 1))
     if x1 <= x0 or y1 <= y0:
-        return
+        return None
     M2 = T(-x0, -y0) @ M
     out = cv2.warpAffine(spr, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
     over(frame, out, x0, y0)
+    return out[..., 3], x0, y0
 
 
 # ---------------------------------------------------------------- plan
 
+def auto_sfx(b, words, t_act, F):
+    """A beat's SFX as [(seconds into the Short, name)]."""
+    out = []
+    for e in b.get("sfx", []):
+        nm, _, at = e.partition("@")
+        t = t_act if not at else (t_act if at == "act" else word_time(words, at, t_act))
+        out.append((F / FPS + max(0.0, t), nm))
+    return out
+
+
+def subject(sh, s, pin):
+    """v4: the animal facts for a shot (tools/animal.py), with the script's per-photo pins applied.
+    sh["cut"] = the shot is drawn as an acting cut-out; otherwise it is the v3 still (sh["why"] says why)."""
+    c = sh["crop"] or [0, 0, 1, 1]
+    head = pin.get("head")
+    if head:  # photo fractions -> crop fractions; a head outside the crop doesn't constrain anything
+        cw, ch = c[2] - c[0], c[3] - c[1]
+        head = [min(max((head[0] - c[0]) / cw, 0), 1), min(max((head[1] - c[1]) / ch, 0), 1),
+                min(max((head[2] - c[0]) / cw, 0), 1), min(max((head[3] - c[1]) / ch, 0), 1)]
+        if head[2] - head[0] < 0.02 or head[3] - head[1] < 0.02:
+            head = None
+    info = dict(animal.subject(sh["path"], sh["crop"], parent=sh.get("parent")))
+    if head is not None:
+        info["head"], info["head_from"] = head, "pin"
+    elif pin.get("head") and "head" in info:
+        info.pop("head")  # pinned head is out of this crop
+    ok = info.get("quality") == "ok" and pin.get("cutout", True) and s.get("cutout", True)
+    why = None if ok else info.get("quality")
+    if not ok:  # a failed matte's boxes are noise: keep only a pinned head (it still steers Meatball)
+        if pin.get("cutout", True) is False and info.get("quality") == "ok":
+            info["quality"] = "pinned: " + pin.get("_why", "cutout false")
+        h = info.get("head") if head is not None else None
+        info = h and dict(head=h, box=h, cx=(h[0] + h[2]) / 2, cy=(h[1] + h[3]) / 2, quality=info.get("quality"))
+    sh.update(subj=info if info and "box" in info else None, cut=bool(ok), idle=pin.get("idle", "bob"),
+              reg=info.get("reg") if info else None,
+              why=None if ok else (why if why != "ok" else "pinned: " + pin.get("_why", "cutout false")))
+
+
+def stage_v4(shots, n, b, moves, top, act):
+    """v4 staging for one line. Meatball's mark: clear of the head on v3 stills (stage.place), else on the
+    side away from the animal. Each cut-out shot is then re-framed around the WHOLE animal (stage.frame_fit):
+    as large as fits, with room for its moves, beside or above him and above the captions."""
+    contact = bool(b.get("contact"))
+    stills = [s for s in shots if not s.get("cut")]
+    cuts = [s for s in shots if s.get("cut")]
+    if any(s.get("subj") for s in stills):
+        x, size, side, _ = stage.place(stills, n, contact, HOME_V4, int(b.get("size", SIZE_V4)))
+    else:  # cut-outs are re-framed anyway: keep his v3 mark (left) so he doesn't hop sides between lines
+        x, size, side = HOME_V4, int(b.get("size", SIZE_V4)), 1
+    best = None
+    for sz in (size, int(size * 0.85)):
+        fits = [stage.frame_fit(animal.photo_box(s["path"], s["subj"]), moves, s["idle"], side, contact,
+                                stage.regions(x, sz, side, top, contact, act), gmax=1.4) for s in cuts]
+        worst = min([ft["g"] for ft in fits] + [9.0])
+        if best is None or worst > best[0] * 1.25:
+            best = (worst, sz, fits)
+    _, size, fits = best
+    for s, ft in zip(cuts, fits):
+        s["fit"] = ft
+    return x, size, side
+
+
 def plan_beats(spec, work):
     name, rate = spec.get("voice", "en-US-AndrewNeural"), spec.get("rate", "+0%")
     tempo = float(spec.get("tempo", 1.0))
     beats = spec["beats"]
     ex.voice(beats, work, name, rate)
     looping = any(b.get("loop") for b in beats)
+    v4 = spec.get("style") == "v4"
+    pins = {str(k): v for k, v in (spec.get("subjects") or {}).items()}
     out, F, shot_no = [], 0, 0
     for i, b in enumerate(beats):
         mp3 = ex.vo_path(b, work, name, rate)
@@ -233,13 +323,18 @@ def plan_beats(spec, work):
                           default=(a + z) / 2)
                 c = s.get("crop") or [0, 0, 1, 1]
                 cx, cy, cw, ch = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2, (c[2] - c[0]) * 0.8, (c[3] - c[1]) * 0.8
-                tight = dict(s, crop=[cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], whip=False)
+                if v4:  # re-cut from the top edge down, so a tighter crop never slices through the head
+                    cy = c[1] + ch / 2
+                tight = dict(s, crop=[cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], whip=False, parent=c)
                 # the loop tail must END on its original crop (= frame 0), so it opens on the tight one
                 pieces = [(a, mid, tight), (mid, z, dict(s, whip=False))] if b.get("loop") else [(a, mid, s), (mid, z, tight)]
             for a_, z_, s_ in pieces:
                 path = ex.photo(s_["photo"], s_.get("n", 0), work, s_.get("obs"), "original")
                 shots.append(dict(f0=int(round(a_ * FPS)), f1=int(round(z_ * FPS)), path=path, crop=s_.get("crop"),
-                                  blur=bool(s_.get("blur")), whip=s_.get("whip", True), no=shot_no))
+                                  blur=bool(s_.get("blur")), whip=s_.get("whip", True), no=shot_no,
+                                  parent=s_.get("parent")))
+                if v4:
+                    subject(shots[-1], s_, pins.get(str(s_.get("obs")), {}))
                 shot_no += 1
         hit = word_time(words, b.get("hit"), None)
         act = b.get("act") or ("loop_out" if b.get("loop") else "stand")
@@ -247,25 +342,47 @@ def plan_beats(spec, work):
         t_act = word_time(words, b.get("act_at"), dflt)
         pose = b.get("pose", "deadpan")
         sts = mascot.states(pose, [list(w) for w in words], D, FPS, seed=i)
-        trk = mascot.act_track(act, n, FPS, t_act, float(b.get("x", HOME)), seed=i)
-        punch = b.get("punch") or []
-        punch = [punch] if isinstance(punch, str) else punch
-        sfx = []
-        for e in b.get("sfx", []):
-            nm, _, at = e.partition("@")
-            t = t_act if not at else (t_act if at == "act" else word_time(words, at, t_act))
-            sfx.append((F / FPS + max(0.0, t), nm))
+        x, size, side, moves = float(b.get("x", HOME)), int(b.get("size", 1000)), 1, []
         lab = b.get("label")
         if isinstance(lab, str):
             lab = {"text": lab}
+        lab_img = lab and label_img(lab["text"])
+        if v4:
+            for nm, at in animal.parse(b.get("animal")):
+                if nm not in ("lunge", "strike", "shake", "turn"):
+                    continue
+                ta = word_time(words, at, t_act)
+                moves.append((nm, ta))
+                if nm in animal.SFX and not any(abs(t - (F / FPS + ta)) < 0.25 for t, _ in auto_sfx(b, words, t_act, F)):
+                    snd, off = animal.SFX[nm]
+                    b = dict(b, sfx=list(b.get("sfx", [])) + [f"{snd}@{max(0.0, ta + off):.3f}"])
+            if b.get("loop") and out:  # the loop tail mirrors the hook, so its last frame matches frame 0
+                h0 = out[0]
+                x, size, side = h0["x"], h0["size"], h0["side"]
+                for s_ in shots:  # a tighter re-cut of the loop shot shares its parent's framing
+                    s_["fit"] = next((t["fit"] for t in h0["shots"] if t.get("fit") and (t["path"], t["crop"])
+                                      == (s_["path"], s_.get("parent") or s_["crop"])), None)
+                    if s_.get("cut") and s_["fit"] is None:
+                        s_["fit"] = stage.frame_fit(animal.photo_box(s_["path"], s_["subj"]), moves, s_["idle"],
+                                                    side, False, stage.regions(x, size, side, act="peek"), gmax=1.4)
+            elif "x" not in b:
+                top = 330 + lab_img.shape[0] / 2 + 12 if lab else stage.SAFE[1]
+                x, size, side = stage_v4(shots, n, b, moves, top, act)
+            trk = stage.track(mascot, act, n, FPS, t_act, x, side, i)
+        else:
+            trk = mascot.act_track(act, n, FPS, t_act, x, seed=i)
+        punch = b.get("punch") or []
+        punch = [punch] if isinstance(punch, str) else punch
+        sfx = auto_sfx(b, words, t_act, F)
         out.append(dict(i=i, F=F, n=n, words=words, wav=wav, shots=shots, act=act, sts=sts, trk=trk,
                         hit=None if hit is None else int(round(hit * FPS)),
                         punch=[int(round(word_time(words, p, 0.0) * FPS)) for p in punch],
-                        punch_z=float(b.get("punch_z", 0.18)), sfx=sfx, size=int(b.get("size", 1000)),
-                        label=lab and dict(img=label_img(lab["text"]),
+                        punch_z=float(b.get("punch_z", 0.18)), sfx=sfx, size=size, side=side, moves=moves,
+                        contact=bool(b.get("contact")),
+                        label=lab and dict(img=lab_img,
                                            f=int(round(word_time(words, lab.get("at"), 0.0) * FPS))),
                         prop=b.get("prop"), prop_f=int(round(word_time(words, b.get("prop_at"), 0.3) * FPS)),
-                        x=float(b.get("x", HOME)), loop=bool(b.get("loop")), first=looping and i == 0, say=b["say"]))
+                        x=x, loop=bool(b.get("loop")), first=looping and i == 0, say=b["say"]))
         F += n
     return out
 
@@ -292,6 +409,75 @@ def shot_view(bt, sh, f):
     return img, z
 
 
+_LAYERS = {}
+
+
+def layer(sh):
+    """v4: (blurred painted-out background at g_bg, premultiplied animal sticker at g, sticker offset, g_bg),
+    cached per photo and scale."""
+    g = round(sh["fit"]["g"], 4)
+    pw, ph = stage.crop_size(sh["path"], [0, 0, 1, 1])
+    g_bg = round(max(g, W / pw, H / ph), 4)   # the background always covers the frame
+    key = (sh["path"], tuple(sh["reg"]), g, g_bg, sh["blur"])
+    if key not in _LAYERS:
+        _LAYERS[key] = animal.layers(sh["path"], sh["crop"], sh["reg"], g, g_bg, sh["blur"]) + (g_bg,)
+    return _LAYERS[key]
+
+
+def premult_over(dst, src, x, y):
+    h, w = src.shape[:2]
+    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
+    if x1 <= x0 or y1 <= y0:
+        return
+    s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
+    d = dst[y0:y1, x0:x1].astype(np.float32)
+    dst[y0:y1, x0:x1] = np.clip(d * (1 - s[..., 3:4] / 255.0) + s[..., :3], 0, 255).astype(np.uint8)
+
+
+def picture(bt, sh, f, g, dx=0.0):
+    """A shot's picture at beat frame f (global frame g): the v3 still, or (v4) the acting cut-out over its
+    blurred photo. The cut-out's move is applied on screen around its feet (bob, lunge) or middle (drift)."""
+    img, z = shot_view(bt, sh, f)
+    if not sh.get("cut"):
+        return view(img, z, dx), None
+    bg, st, (ox, oy), g_bg = layer(sh)
+    ft = sh["fit"]
+    gs = ft["g"]
+    pb = animal.photo_box(sh["path"], sh["subj"])
+    pcx, pcy = (pb[0] + pb[2]) / 2, (pb[1] + pb[3]) / 2
+    scx, scy = ft["tx"] + gs * pcx, ft["ty"] + gs * pcy          # the animal's centre on screen
+    bh, bw = bg.shape[:2]   # background: same spot of the photo behind the animal, clamped to cover the frame
+    bx = min(0.0, max(W - bw, scx - g_bg * pcx))
+    by = min(0.0, max(H - bh, scy - g_bg * pcy))
+    Mb = np.float32([[z, 0, W / 2 - z * W / 2 + z * bx + dx], [0, z, H / 2 - z * H / 2 + z * by]])
+    out = cv2.warpAffine(bg, Mb, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
+    # the cut-out takes no push: a little parallax against the background
+    V = np.array([[1, 0, ft["tx"] + ox + dx], [0, 1, ft["ty"] + oy], [0, 0, 1]])
+    a = (scx + dx, scy if sh["idle"] == "drift" else ft["ty"] + gs * pb[3])
+    toward = 1 if bt["x"] * W >= a[0] else -1
+    mv = animal.transform(bt["moves"], f / FPS, toward, sh["no"], sh["idle"], n_left=PLAN["total"] - 1 - g,
+                          ts=(f - sh["f0"]) / FPS, n_from=g)
+    r = math.radians(mv["rot"])
+    sc = mv["s"]
+    A = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]]) @ np.diag(
+        [sc * mv["sx"] * (1 - 2 * mv["flip"]), sc * mv["sy"], 1.0])
+    M = (np.array([[1, 0, a[0] + mv["dx"] * W], [0, 1, a[1] + mv["dy"] * W], [0, 0, 1]]) @ A
+         @ np.array([[1, 0, -a[0]], [0, 1, -a[1]], [0, 0, 1]]) @ V)
+    h, w = st.shape[:2]
+    pts = M @ np.array([[0, w, w, 0], [0, 0, h, h], [1, 1, 1, 1]])
+    x0, y0 = int(max(0, pts[0].min())), int(max(0, pts[1].min()))
+    x1, y1 = int(min(W, pts[0].max() + 1)), int(min(H, pts[1].max() + 1))
+    if x1 > x0 and y1 > y0:
+        M2 = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]]) @ M
+        warped = cv2.warpAffine(st, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
+        premult_over(out, warped, x0, y0)
+        wa = warped[..., 3] > 128   # the animal itself (not its shadow padding) reaching a frame edge
+        clipped = bool((x0 == 0 and wa[:, 0].any()) or (y0 == 0 and wa[0].any()) or
+                       (x1 == W and wa[:, -1].any()) or (y1 == H and wa[-1].any()))
+        return out, (warped[..., 3], x0, y0, clipped)
+    return out, None
+
+
 def frame(g):
     P = PLAN
     bi = max(k for k, bt in enumerate(P["beats"]) if bt["F"] <= g)
@@ -300,19 +486,19 @@ def frame(g):
     shots = bt["shots"]
     k = max(j for j, s in enumerate(shots) if s["f0"] <= f or j == 0)
     sh = shots[k]
-    img, z = shot_view(bt, sh, f)
     bg = None
     cut = P["whips"].get(g)  # whip pan: 6 frames centred on a cut to a different photo (also across beats)
     if cut:
         gc, pb, ps, nb, ns = cut
         u = (g - (gc - 3) + 0.5) / 6.0
         o = int(W * u * u * (3 - 2 * u))
-        A = view(*shot_view(pb, ps, g - pb["F"]))
-        B = view(*shot_view(nb, ns, g - nb["F"]))
+        A = picture(pb, ps, g - pb["F"], g)[0]
+        B = picture(nb, ns, g - nb["F"], g)[0]
         bg = np.concatenate([A[:, o:], B[:, :o]], axis=1)
         bg = cv2.blur(bg, (int(170 * math.sin(math.pi * u)) | 1, 1))
+    ani = None
     if bg is None:
-        bg = view(img, z)
+        bg, ani = picture(bt, sh, f, g)
     frame_ = np.ascontiguousarray(bg)
     st = dict(bt["sts"][min(f, len(bt["sts"]) - 1)])
     tr = bt["trk"][f]
@@ -331,8 +517,24 @@ def frame(g):
         p = P["props"][bt["prop"]]
         kf = f - bt["prop_f"]
         drop = [-900, -520, -200, 0, -40, 0][kf] if kf < 6 else 0
-        over(frame_, p, int(bt["x"] * W + bt["size"] * 0.36), FLOOR - p.shape[0] + 20 + drop)
-    place_meatball(frame_, st, tr, bt["size"])
+        px = int(bt["x"] * W + bt["size"] * 0.36) if bt["side"] == -1 or not P["v4"] else \
+            int(bt["x"] * W - bt["size"] * 0.36 - p.shape[1])   # v4: on his free side, away from the animal
+        over(frame_, p, px, FLOOR - p.shape[0] + 20 + drop)
+    placed = place_meatball(frame_, st, tr, bt["size"])
+    qa = (0, 0, False)
+    if P["v4"] and ani is not None and not cut:  # QA (not during whip pans): Meatball over the animal, animal under the captions, animal clipped
+        aa, ax0, ay0, clipped = ani
+        over_mb = 0
+        if placed is not None:
+            al, mx, my = placed
+            x0, y0 = max(ax0, mx), max(ay0, my)
+            x1, y1 = min(ax0 + aa.shape[1], mx + al.shape[1]), min(ay0 + aa.shape[0], my + al.shape[0])
+            if x1 > x0 and y1 > y0:
+                over_mb = int(((aa[y0 - ay0:y1 - ay0, x0 - ax0:x1 - ax0] > 128)
+                               & (al[y0 - my:y1 - my, x0 - mx:x1 - mx] > 128)).sum())
+        cy0 = max(0, CAP_Y - 75 - ay0)
+        under_cap = int((aa[cy0:, max(0, 150 - ax0):max(0, 930 - ax0)] > 128).sum()) if cy0 < aa.shape[0] else 0
+        qa = (over_mb, under_cap, bool(clipped))
     if bt["label"] and f >= bt["label"]["f"]:
         kf = f - bt["label"]["f"]
         s = [0.35, 0.75, 1.15, 1.06, 1.0][kf] if kf < 5 else 1.0
@@ -358,7 +560,7 @@ def frame(g):
     if bt["hit"] is not None and 0 <= f - bt["hit"] < 3:  # white impact flash
         a = (0.85, 0.55, 0.25)[f - bt["hit"]]
         frame_ = (frame_.astype(np.float32) * (1 - a) + 255 * a).astype(np.uint8)
-    return frame_.tobytes()
+    return frame_.tobytes(), qa
 
 
 def captions(beats, path):
@@ -408,6 +610,30 @@ def gate(beats, total):
     print(f"v3 gate: {len(events)} events in {total:.1f}s, longest gap {max(gaps):.2f}s", flush=True)
 
 
+def report_v4(beats, work):
+    """v4 gate: which shots act as cut-outs, which fell back to the v3 still (and why), Meatball's marks."""
+    shots, stills = [], []
+    for bt in beats:
+        for s in bt["shots"]:
+            e = dict(beat=bt["i"], photo=os.path.basename(s["path"]), crop=s["crop"], blur=s["blur"],
+                     cut=s.get("cut"), why=s.get("why"), sec=round((s["f1"] - s["f0"]) / FPS, 2))
+            shots.append(e)
+            if not s.get("cut"):
+                stills.append(e)
+                print(f"V4 FALLBACK: beat {bt['i']} {e['photo']} {s['crop']}: {s.get('why')}", flush=True)
+    marks = [dict(beat=bt["i"], x=round(bt["x"], 3), size=bt["size"], side=bt["side"], act=bt["act"],
+                  contact=bt["contact"], moves=bt["moves"]) for bt in beats]
+    n = len(shots)
+    print(f"v4 gate: {n - len(stills)}/{n} shots act as cut-outs; {len(stills)} v3 stills", flush=True)
+    for bt in beats:  # hard rules (Nolan, 10/25): a cut-out is the whole animal, none of it lost to clean-up
+        for s in bt["shots"]:
+            if s.get("cut") and (s["subj"].get("touch") or s["subj"].get("loss", 1) > animal.MAX_LOSS):
+                raise SystemExit(f"v4 gate: beat {bt['i']} cut-out touches the photo edge or loses "
+                                 f"{s['subj'].get('loss', 1):.0%} of the matte")
+    json.dump(dict(shots=shots, marks=marks), open(f"{work}/v4.json", "w"), indent=1)
+    return stills
+
+
 def build(spec, work, out, music=None):
     os.makedirs(work, exist_ok=True)
     ex.vertical()
@@ -421,12 +647,18 @@ def build(spec, work, out, music=None):
             for d in range(-3, 3):
                 cuts[g + d] = (g, pb, ps, nb, ns)
     PLAN.clear()
-    PLAN.update(beats=beats, whips=cuts, props={"fork": np.asarray(mascot.prop("fork", 520))})
-    for bt in beats:  # warm the photo cache before forking the workers
+    v4 = spec.get("style") == "v4"
+    PLAN.update(beats=beats, whips=cuts, props={"fork": np.asarray(mascot.prop("fork", 520))}, v4=v4,
+                total=total_f)
+    for bt in beats:  # warm the photo (and v4 cut-out) caches before forking the workers
         for s in bt["shots"]:
             base(s["path"], s["crop"], s["blur"])
+            if s.get("cut"):
+                layer(s)
     total = total_f / FPS
     gate(beats, total)
+    if v4:
+        stills = report_v4(beats, work)
     # audio: voice lines, SFX under them, music bed ducked by the voice
     voice = np.zeros((int(total * SR) + SR, 2), np.float32)
     sfx = np.zeros_like(voice)
@@ -461,8 +693,10 @@ def build(spec, work, out, music=None):
     proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
     jobs = int(os.environ.get("MEATBALL_JOBS", "2"))
     with mp.get_context("fork").Pool(jobs) as pool:
-        for k, buf in enumerate(pool.imap(frame, range(total_f), chunksize=4)):
+        qas = []
+        for k, (buf, qa) in enumerate(pool.imap(frame, range(total_f), chunksize=4)):
             proc.stdin.write(buf)
+            qas.append(qa)
             if k % 150 == 0:
                 print(f"v3 frame {k}/{total_f}", flush=True)
     proc.stdin.close()
@@ -473,4 +707,21 @@ def build(spec, work, out, music=None):
     json.dump([dict(i=bt["i"], start=bt["F"] / FPS, dur=bt["n"] / FPS, act=bt["act"], say=bt["say"],
                     shots=[(s["f0"] / FPS, s["f1"] / FPS) for s in bt["shots"]], sfx=bt["sfx"]) for bt in beats],
               open(f"{work}/timeline.json", "w"), indent=1)
+    if v4:  # QA by beat: frames where Meatball covers the animal (contact beats may), animal under captions
+        bad = {}
+        for g, (mb, cap, clip) in enumerate(qas):
+            bt = max((b for b in beats if b["F"] <= g), key=lambda b: b["F"])
+            e = bad.setdefault(bt["i"], dict(act=bt["act"], contact=bt["contact"], meatball=0, captions=0, clipped=0))
+            e["meatball"] += mb > 300
+            e["captions"] += cap > 300
+            e["clipped"] += bool(clip)
+        bad = {i: e for i, e in bad.items() if e["meatball"] or e["captions"] or e["clipped"]}
+        rep = json.load(open(f"{work}/v4.json"))
+        rep["overlap"] = {str(i): e for i, e in bad.items()}
+        json.dump(rep, open(f"{work}/v4.json", "w"), indent=1)
+        for i, e in sorted(bad.items()):
+            print(f"V4 QA: beat {i} ({e['act']}{', contact' if e['contact'] else ''}): Meatball over the animal "
+                  f"{e['meatball']} frames, animal under captions {e['captions']}, clipped {e['clipped']}", flush=True)
+        if any(e["clipped"] for e in bad.values()):
+            raise SystemExit("v4 gate: an acting animal leaves the frame (see V4 QA)")
     print(f"ok {out} {total:.1f}s")
```
