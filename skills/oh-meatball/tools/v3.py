#!/usr/bin/env python3
"""Shorts v3 renderer (research/44): Meatball in jeopardy, with motion, impacts and sound effects.

Selected by "style": "v3" in a Shorts spec (explainer.py dispatches here; episode.py --skip-long builds it).
Every frame is composed in Python (numpy/cv2) and piped once into ffmpeg, so the camera can move across
cuts: the photo always pushes, cuts to a new photo whip-pan, key words punch in, hits shake the frame and
flash white, and Meatball performs an action move over his talking rig (mascot.act_track).

Spec fields (all optional unless noted):
  "tempo": 1.10          voice sped up with ffmpeg atempo; word timings are scaled to match
  beat "act"             stand | run_in | run_off | run_across | launch | tumble | shake | peek | hide | hit
                         | puff  (the loop tail defaults to loop_out: he peeks, then slides off-frame)
  beat "act_at"          word (or seconds into the line) when the move lands; default: the "hit" word
  beat "hit"             word: impact = white flash (3 frames) + screen shake
  beat "punch"           word or list of words: punch-in zoom to ~118% (beat "punch_z" overrides)
  beat "sfx"             ["whoosh", "crunch@kick", "pop@1.2"]: name[@word|@seconds]; bare names play at
                         the act moment. Kit in sfx/ (tools/make_sfx.py), mixed under the voice
  beat "label"           big pop-in word card on the picture, e.g. {"text": "4 INCHES", "at": "dagger"}
  beat "x"               Meatball's mark as a fraction of the frame width (default 0.24)
  beat "size"            Meatball's size in px per 1000 drawing units (default 1000: ~40% of the frame)
  beat "prop": "fork"    the Fork drops in beside him at "prop_at" (word)
  shot "whip": false     hard cut instead of a whip pan (cuts to a different photo whip by default)
  shot "blur": true      blurred, dimmed photo (a host shot)
  Ask kit (research/46; Nolan 10/25: "do it in the beginning so people will actually be watching"). Order:
  hook 0-3 s (no ask) -> guess card 3-6 s -> subscribe pill 6-10 s -> story -> "Were you right?" -> loop.
  beat "ask" (a dict)    a comment card: {"q": "WHY FAKE IT?", "choices": ["🦹 FOOL THIEVES", "🎭 FOR FUN"],
                         "at": "word"}; each choice chip pops in 0.18 s after the last, with a pop. Right after the
                         hook it is a guess-first prompt ("Guess before I tell you. Comment."); the Short must then
                         answer it. Without "choices" it is a one-line reminder card ("WERE YOU RIGHT? 👇") for the
                         last beat before the loop. Cards end with their beat, so the last frame still matches frame 0
  beat "sub"             {"at": "Subscribe", "text": "SUBSCRIBE"} or true. Meatball points down toward the follow
                         button (pose "subpoint"), a red pill pops in on the "at" word and is pressed 0.45 s later
                         with a click. One quick line with a concrete, true reason ("Subscribe. I face a new animal
                         every day.")
  gate                   warns on any ask before 3 s, a guess card outside 3-7 s, a pill outside 5.5-10.5 s
Long-forms (spec "aspect": "16:9", no --vertical; landscape()): the same renderer at 1920x1080. Meatball keeps
  ~50% of the frame height at the left (size 680, v4 600), labels/props scale by UI = 0.62, the ask kit by 0.9, captions sit
  under his feet. A line longer than 3.4 s alternates its photo with a tighter crop every <=3.4 s (gate: no picture
  over 3.5 s, nothing new for over 4 s). Ask gate: no ask in the first 15 s (cold open), guess card 15-40 s, one
  subscribe pill 28-55 s, "Were you right?" reminder in the last 90 s.
  beat "aside"           a small footnote joke plate, low right, popping in at 55% of the line (or "aside_at")
  beat "counter"         {"n": 2, "of": 5, "text": "#4"} on a chapter's first beat: a "2 OF 5" badge (or "text"),
                         top right, with one dot per chapter, held until the next counter, "counter": false or an
                         "outro" chapter (research/47, gate: tools/retention.py R3)
  spec "progress": true  a thin progress bar along the top edge with a tick at every counted chapter
                         Both are drawn after the camera moves (they never shake or punch in), 16:9 only.
Photos come from explainer.photo() (pinned iNaturalist observations, "wm:" Commons files, "ov:"/"met:" art).
"Meatball Investigates" (tools/investigate.py, research/48): spec "series" (case-file card + tag), beat "stamp"
  (verdict stamp slam: TRUE / FALSE / PROVEN / BUSTED / CLASSIFIED), shot "board" (evidence board: polaroid,
  notes, red string), spec "captions": "bold"; spec "music": "gen:mystery" | "gen:detective" renders an original
  bed to the video's timeline (tools/music.py: builds into each stamp, drops out right before it, hits on it,
  loop-safe) and mixes it by loudness: voice -16 LUFS, music -20 LUFS ducked under the voice, master -14.

"style": "v4" (research/45) adds, on top of everything above:
  whole-animal cut-outs  every photo shot is cut out (tools/animal.py): the WHOLE animal, holes under 1%
                         filled, contour smoothed, 1 px under a uniform white stroke, soft shadow. The shot is
                         re-framed around it (tools/stage.py): as large as fits beside Meatball, leaning over
                         his head where its outline leaves room, clear of him, the captions and the frame edge,
                         standing on the floor, over its own photo blurred and dimmed with the animal painted
                         out. Before he peeks in on a hook, it has the frame to itself and pulls back as he
                         arrives; a lunge or strike reaches less far where the full reach would cost size
  animal acting          the cut-out always moves (bob, or "drift" for floaters); beat "animal": "lunge@kick" /
                         ["turn@twists", "shake@inside"] adds lunge|kick|charge, strike|snap|sting, shake,
                         turn|look, timed to a word, with a matching SFX unless the beat has one there
  Meatball               tucked against the left edge (840, or 0.92x / 0.84x of that when it lets the animal
                         grow) and faces the animal; flees, is flung, peeks and cowers away from it (on a v3
                         still his mark comes from the pinned head instead)
  beat "contact": true   Meatball and the animal may touch (a poke, a sting, a kick)
  spec "subjects"        per iNaturalist obs: {"head": [x0, y0, x1, y1] photo fractions (steers Meatball on a
                         v3 still), "cutout": false, "idle": "drift"}
  gates                  a photo whose animal runs off the photo's edge, a matte in pieces or one whose clean-up
                         would lose >3% of it, a see-through or low-contrast matte: that shot falls back to the
                         v3 still (listed as V4 FALLBACK). The render fails if a cut-out breaks the edge/loss
                         rule or an acting animal leaves the frame; Meatball-over-animal and animal-under-caption
                         frames are reported per beat (V4 QA, and v4.json in the work dir)
"""
import json
import math
import multiprocessing as mp
import os
import subprocess
import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import animal
import explainer as ex
import investigate
import mascot
import stage

FPS, W, H, SR = 30, 1080, 1920, 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX_DIR = os.path.join(ROOT, "sfx")
GAIN = {"whoosh": 0.32, "boing": 0.22, "pop": 0.30, "scratch": 0.20, "splash": 0.34, "tink": 0.40,
        "crunch": 0.42, "hit": 0.40, "thud": 0.42, "zap": 0.28, "plate": 0.30, "click": 0.45, "stamp": 0.55,
        "case": 0.50}
R = 1.15          # photo bases are prepared 15% over frame size so slow pushes stay sharp
GAP = 0.12        # silence after each line (v2 used 0.35)
FLOOR = 1430      # Meatball's feet (screen y); captions sit just below
CAP_Y = 1560
MAX_SHOT = 2.4    # a shot longer than this is re-cut to a tighter crop of the same photo (gate: 2.5 s)
PUSH = 0.045      # zoom per second of the slow push (v2: 0.036)
HOME = 0.24       # Meatball's mark: left of centre, so the animal (centred in each crop) stays visible
HOME_V4, SIZE_V4 = 0.21, 840   # v4: smaller and tucked at the edge (stage.tuck), so the animal gets most of the frame
SIZE = 1000       # Meatball's default size (px per 1000 drawing units)
UI = 1.0          # scale of the labels, footnotes and props (landscape() shrinks them for 1080 px of height)
CARD = 1.0        # scale of the ask kit (comment card, chips, subscribe pill): kept big enough to read and tap
LABEL_Y = 330     # centre line of pop-in labels and the comment card's title
PILL_Y = 1440     # the subscribe pill, just under his pointing hand
CAM_Y = 860       # centre of punch-ins and shakes
CAP_FS = 100      # caption font size
HOLD_MAX, GAP_MAX = 2.5, 3.0   # gate: longest single picture, longest stretch with nothing new (s)
# ask-kit placement gate (s): no ask before, guess card window, pill window (Shorts; landscape() sets long-form)
ASK_NONE, ASK_GUESS, ASK_PILL = 3.0, (3.0, 7.0), (5.5, 10.5)
PLAN = {}         # filled before the frame workers fork


def landscape():
    """16:9 long-form layout (1920x1080): same moves, cards and gates, re-scaled for the wide frame.
    Meatball keeps his share of the frame's height (~45%) at the left; the picture gets the rest."""
    global W, H, FLOOR, CAP_Y, MAX_SHOT, HOME, HOME_V4, SIZE_V4, SIZE, UI, CARD, LABEL_Y, PILL_Y, CAM_Y, CAP_FS
    global HOLD_MAX, GAP_MAX, ASK_NONE, ASK_GUESS, ASK_PILL
    W, H, FLOOR, CAP_Y = 1920, 1080, 930, 1000
    SIZE, SIZE_V4, HOME, HOME_V4 = 680, 600, 0.17, 0.13
    UI, CARD, LABEL_Y, PILL_Y, CAM_Y, CAP_FS = 0.62, 0.9, 190, 860, 500, 66
    MAX_SHOT, HOLD_MAX, GAP_MAX = 3.4, 3.5, 4.0   # Nolan 10/25: a new picture or a whip every 3-4 s at most
    ASK_NONE, ASK_GUESS, ASK_PILL = 15.0, (15.0, 40.0), (28.0, 55.0)  # long-form: cold open, then the early asks
    stage.configure(W, H, FLOOR, (0.015 * W, 30.0, 0.985 * W, FLOOR + 25.0))


def _ui(a, k=None):
    """An RGBA card array at the layout's UI (or CARD) scale."""
    k = UI if k is None else k
    if k == 1.0:
        return a
    return cv2.resize(a, (max(1, int(a.shape[1] * k)), max(1, int(a.shape[0] * k))), interpolation=cv2.INTER_AREA)


def _key(w):
    return w.lower().strip(".,!?;:'\"")


def word_time(words, at, default=None, after=-1.0):
    """Seconds into the line of the first word matching `at` (a word, or a number of seconds)."""
    if at is None:
        return default
    if isinstance(at, (int, float)):
        return float(at)
    try:
        return float(at)
    except ValueError:
        pass
    k = _key(at)
    hit = next((s for s, e, w in words if _key(w) == k and s > after), None)
    if hit is None:
        print(f"V3 WARN: word {at!r} not in line; using {default}", flush=True)
        return default
    return hit


def speed(mp3, tempo):
    """Beat audio sped up by `tempo` (pitch kept), as 48 kHz stereo WAV, with word timings scaled."""
    wav = mp3[:-4] + f"_t{tempo:.3f}.wav"
    if not os.path.exists(wav):
        af = f"atempo={tempo:.4f}," if abs(tempo - 1) > 1e-3 else ""
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-af", af + "aresample=48000",
                        "-ac", "2", "-c:a", "pcm_s16le", wav], check=True)
    words = [(s / tempo, e / tempo, w) for s, e, w in json.load(open(mp3 + ".words.json"))]
    return wav, words


def read_wav(path):
    with wave.open(path) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, f.getnchannels())
    a = a.astype(np.float32) / 32768.0
    return a if a.shape[1] == 2 else np.repeat(a, 2, axis=1)


def write_wav(path, a):
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- pictures

_BASES = {}


def base(path, crop=None, blur=False):
    """The shot's photo cropped and scaled to cover the frame at R x size (cached)."""
    key = (path, tuple(crop or ()), blur)
    if key not in _BASES:
        im = Image.open(path).convert("RGB")
        if crop:
            im = im.crop((int(crop[0] * im.width), int(crop[1] * im.height), int(crop[2] * im.width),
                          int(crop[3] * im.height)))
        bw, bh = int(W * R), int(H * R)
        s = max(bw / im.width, bh / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        l, t = (im.width - bw) // 2, (im.height - bh) // 2
        im = im.crop((l, t, l + bw, t + bh))
        if blur:
            im = im.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.78))
        _BASES[key] = np.asarray(im)
    return _BASES[key]


def view(img, z, dx=0.0):
    """Frame of a base at zoom z (1 = the whole base), sub-pixel smooth; dx shifts it (whip pans)."""
    bh, bw = img.shape[:2]
    s = (W / bw) * z
    m = np.float32([[s, 0, W / 2 - s * bw / 2 + dx], [0, s, H / 2 - s * bh / 2]])
    return cv2.warpAffine(img, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def label_img(text):
    f = ImageFont.truetype(ex.BOLD, 150)
    lines = text.split("\n")
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(max(d.textlength(x, font=f) for x in lines)) + 60
    im = Image.new("RGBA", (tw, int(len(lines) * 175) + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, line in enumerate(lines):
        x = (tw - d.textlength(line, font=f)) / 2
        d.text((x, 20 + k * 175), line, font=f, fill=ex.YELLOW, stroke_width=12, stroke_fill=(0, 0, 0))
    im = im.rotate(5, expand=True, resample=Image.BICUBIC)
    return _ui(np.asarray(im))


def aside_img(text):
    """A small typed footnote joke ("(it was a raccoon)"), white on a dark plate."""
    f = ImageFont.truetype(ex.ASIDE_FONT, 52)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(d.textlength(text, font=f))
    im = _rounded(tw + 56, 84, 22, (20, 20, 24, 215))
    ImageDraw.Draw(im).text((28, 12), text, font=f, fill=(255, 255, 255))
    return _ui(np.asarray(im))


EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
SUB_RED = (230, 33, 23)


def _rounded(w, h, r, fill, outline=None, width=0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=fill, outline=outline, width=width)
    return im


def _emoji(text, height):
    """Colour emoji (Noto renders only at 109 px; scaled to height)."""
    f = ImageFont.truetype(EMOJI, 109)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, embedded_color=True)
    im = Image.new("RGBA", (x1 - x0 + 8, y1 - y0 + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - x0, 4 - y0), text, font=f, embedded_color=True)
    return im.resize((max(1, int(im.width * height / im.height)), height), Image.LANCZOS)


def pill_img(text="SUBSCRIBE"):
    """The red follow pill (ask kit)."""
    f = ImageFont.truetype(ex.BOLD, 70)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(d.textlength(text, font=f))
    im = _rounded(tw + 110, 128, 64, SUB_RED + (255,), (255, 255, 255, 255), 8)
    ImageDraw.Draw(im).text((55, 22), text, font=f, fill=(255, 255, 255))
    return _ui(np.asarray(im), CARD)


def chip_img(choice):
    """One answer chip: leading emoji (colour) + optional bold word, on white."""
    head, _, rest = choice.partition(" ")
    emo, word = (head, rest) if head and not head.isascii() else ("", choice)
    f = ImageFont.truetype(ex.BOLD, 64)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    e = _emoji(emo, 96) if emo else None
    tw = int(d.textlength(word.upper(), font=f)) if word else 0
    w = 44 + (e.width if e else 0) + (18 if e and word else 0) + tw + 44
    im = _rounded(w, 140, 34, (255, 255, 255, 255), (0, 0, 0, 255), 7)
    x = 44
    if e:
        im.alpha_composite(e, (x, 22))
        x += e.width + 18
    if word:
        ImageDraw.Draw(im).text((x, 34), word.upper(), font=f, fill=(20, 20, 20))
    return np.asarray(im)


def ask_imgs(q):
    """The comment card: title plate and one chip per choice (laid out by frame())."""
    f = ImageFont.truetype(ex.BOLD, 96)
    lines = q["q"].upper().split("\n")
    emo = "".join(ch for ch in lines[-1] if ord(ch) > 0x2000)   # trailing emoji: colour font, not DejaVu tofu
    lines[-1] = "".join(ch for ch in lines[-1] if ord(ch) <= 0x2000).rstrip()
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(max(d.textlength(x, font=f) for x in lines)) + 80
    im = Image.new("RGBA", (tw, len(lines) * 112 + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, line in enumerate(lines):
        d.text(((tw - d.textlength(line, font=f)) / 2, 16 + k * 112), line, font=f, fill=ex.YELLOW,
               stroke_width=10, stroke_fill=(0, 0, 0))
    if emo:
        e = _emoji(emo, 96)
        wide = Image.new("RGBA", (im.width + e.width + 10, im.height), (0, 0, 0, 0))
        wide.alpha_composite(im, (0, 0))
        wide.alpha_composite(e, (im.width - 30, im.height - 112 - 8))
        im = wide
    if im.width > W - 60:  # long questions shrink to fit the frame
        im = im.resize((W - 60, int(im.height * (W - 60) / im.width)), Image.LANCZOS)
    im = _ui(np.asarray(im), CARD)
    chips = [_ui(chip_img(c), CARD) for c in q.get("choices") or []]
    chips = [c if c.shape[1] <= W - 60 else cv2.resize(c, (W - 60, int(c.shape[0] * (W - 60) / c.shape[1])))
             for c in chips]
    return im, chips


def counter_img(c):
    """Chapter badge for long-forms: "2 OF 5" (or c["text"]) over one dot per chapter, passed ones filled."""
    text = c.get("text") or f"{c['n']} OF {c['of']}"
    f = ImageFont.truetype(ex.BOLD, 84)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    n, of = int(c.get("n", 1)), int(c.get("of", 1))
    tw = int(d.textlength(text, font=f))
    dots = 34 * of - 12
    w = max(tw, dots) + 70
    im = _rounded(w, 178, 30, (20, 20, 24, 210), (255, 255, 255, 230), 5)
    dr = ImageDraw.Draw(im)
    dr.text(((w - tw) / 2, 14), text, font=f, fill=ex.YELLOW, stroke_width=4, stroke_fill=(0, 0, 0))
    x0 = (w - dots) / 2
    for k in range(of):
        box = [x0 + 34 * k, 128, x0 + 34 * k + 22, 150]
        dr.ellipse(box, fill=ex.YELLOW if k < n else None, outline=(255, 255, 255), width=3)
    return _ui(np.asarray(im))


def hud(frame_, bt, g):
    """Long-form chapter counter + progress bar (screen space, after the camera)."""
    c = bt.get("counter")
    if c:
        _over_scaled(frame_, c["img"], _pop(g - c["F"]), W - 36 - c["img"].shape[1] / 2, 36 + c["img"].shape[0] / 2)
    if PLAN.get("progress"):
        h, u = 10, g / max(1, PLAN["total"] - 1)
        frame_[:h] = (frame_[:h].astype(np.float32) * 0.45).astype(np.uint8)
        frame_[:h, :int(W * u)] = ex.YELLOW
        for f in PLAN["ticks"]:
            x = int(W * f / max(1, PLAN["total"] - 1))
            frame_[:h + 6, max(0, x - 2):x + 2] = (255, 255, 255)


def _pop(kf, k=1.0):
    return ([0.35, 0.75, 1.15, 1.06, 1.0][kf] if kf < 5 else 1.0) * k


def _over_scaled(dst, img, s, cx, cy):
    if s <= 0:
        return
    im = cv2.resize(img, (max(1, int(img.shape[1] * s)), max(1, int(img.shape[0] * s))))
    over(dst, im, int(cx - im.shape[1] / 2), int(cy - im.shape[0] / 2))


def over(dst, src, x, y):
    """Alpha-composite RGBA array src onto RGB array dst with its top-left at (x, y), clipped."""
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = s[..., 3:4] / 255.0
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (d * (1 - a) + s[..., :3] * a).astype(np.uint8)


# ---------------------------------------------------------------- Meatball

def sprite(st, size):
    """Meatball (white rim + soft shadow) as an RGBA array with room for squash, puff and spins."""
    pad = int(size * 0.45)
    cw = size + 2 * pad
    got = mascot.render(st, size, 2 if size <= 1400 else 1, (pad, pad), (cw, cw))
    canvas = Image.new("RGBA", (cw, cw), (0, 0, 0, 0))
    if got:
        im, (x, y) = got
        margin = max(13, int(size / 66)) + 2
        pim = Image.new("RGBA", (im.width + 2 * margin, im.height + 2 * margin), (0, 0, 0, 0))
        pim.alpha_composite(im, (margin, margin))
        canvas.alpha_composite(mascot._sticker(pim, size, True), (x - margin, y - margin))
    return np.asarray(canvas), pad


def place_meatball(frame, st, tr, size):
    if tr["hidden"]:
        return None
    spr, pad = sprite(st, size)
    if tr.get("flip"):  # v4: face the animal on his left (the rig is symmetric about the hip)
        spr = spr[:, ::-1]
    k = size / 1000.0
    hip = np.array([pad + 500 * k, pad + 790 * k])
    feet = np.array([pad + 500 * k, pad + 960 * k])
    tx = tr["x"] * W + tr.get("jx", 0.0) * k
    ty = FLOOR - 170 * k + tr["y"] * k + tr.get("jy", 0.0) * k
    sx, sy = tr["body"]
    T = lambda x, y: np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], dtype=np.float64)
    a = math.radians(tr["rot"])
    Rm = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    S = np.diag([sx, sy, 1.0])
    M = T(tx, ty) @ Rm @ T(-hip[0], -hip[1]) @ T(feet[0], feet[1]) @ S @ T(-feet[0], -feet[1])
    h, w = spr.shape[:2]
    pts = M @ np.array([[0, w, w, 0], [0, 0, h, h], [1, 1, 1, 1]])
    x0, y0 = int(max(0, pts[0].min())), int(max(0, pts[1].min()))
    x1, y1 = int(min(W, pts[0].max() + 1)), int(min(H, pts[1].max() + 1))
    if x1 <= x0 or y1 <= y0:
        return None
    M2 = T(-x0, -y0) @ M
    out = cv2.warpAffine(spr, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    over(frame, out, x0, y0)
    return out[..., 3], x0, y0


# ---------------------------------------------------------------- plan

def auto_sfx(b, words, t_act, F):
    """A beat's SFX as [(seconds into the Short, name)]."""
    out = []
    for e in b.get("sfx", []):
        nm, _, at = e.partition("@")
        t = t_act if not at else (t_act if at == "act" else word_time(words, at, t_act))
        out.append((F / FPS + max(0.0, t), nm))
    return out


def subject(sh, s, pin):
    """v4: the animal facts for a shot (tools/animal.py), with the script's per-photo pins applied.
    sh["cut"] = the shot is drawn as an acting cut-out; otherwise it is the v3 still (sh["why"] says why)."""
    c = sh["crop"] or [0, 0, 1, 1]
    head = pin.get("head")
    if head:  # photo fractions -> crop fractions; a head outside the crop doesn't constrain anything
        cw, ch = c[2] - c[0], c[3] - c[1]
        head = [min(max((head[0] - c[0]) / cw, 0), 1), min(max((head[1] - c[1]) / ch, 0), 1),
                min(max((head[2] - c[0]) / cw, 0), 1), min(max((head[3] - c[1]) / ch, 0), 1)]
        if head[2] - head[0] < 0.02 or head[3] - head[1] < 0.02:
            head = None
    info = dict(animal.subject(sh["path"], sh["crop"], parent=sh.get("parent")))
    if head is not None:
        info["head"], info["head_from"] = head, "pin"
    elif pin.get("head") and "head" in info:
        info.pop("head")  # pinned head is out of this crop
    ok = info.get("quality") == "ok" and pin.get("cutout", True) and s.get("cutout", True)
    why = None if ok else info.get("quality")
    if not ok:  # a failed matte's boxes are noise: keep only a pinned head (it still steers Meatball)
        if pin.get("cutout", True) is False and info.get("quality") == "ok":
            info["quality"] = "pinned: " + pin.get("_why", "cutout false")
        h = info.get("head") if head is not None else None
        info = h and dict(head=h, box=h, cx=(h[0] + h[2]) / 2, cy=(h[1] + h[3]) / 2, quality=info.get("quality"))
    sh.update(subj=info if info and "box" in info else None, cut=bool(ok), idle=pin.get("idle", "bob"),
              reg=info.get("reg") if info else None,
              why=None if ok else (why if why != "ok" else "pinned: " + pin.get("_why", "cutout false")))


def stage_v4(shots, n, b, moves, top, act):
    """v4 staging for one line. Meatball's mark: clear of the head on v3 stills (stage.place), else tucked
    against the left edge (a little smaller when that lets the animal grow). Each cut-out shot is then
    re-framed around the WHOLE animal (stage.frame_fit): as large as fits, with room for its moves, beside him
    or leaning over his head where its outline leaves room, above the captions and inside the frame."""
    contact = bool(b.get("contact"))
    stills = [s for s in shots if not s.get("cut")]
    cuts = [s for s in shots if s.get("cut")]
    side = 1
    if any(s.get("subj") for s in stills):
        x, size, side, _ = stage.place(stills, n, contact, HOME_V4, int(b.get("size", SIZE_V4)))
        marks = [(x, size)]
    else:  # cut-outs are re-framed anyway: keep him on the left so he doesn't hop sides between lines
        size = int(b.get("size", SIZE_V4))
        marks = [(stage.tuck(sz), sz) for sz in (size, int(size * 0.92), int(size * 0.84))]
    best = None
    for x, sz in marks:
        keep = stage.keepout(x, sz, side, top, contact, act)
        fits = [stage.frame_fit(outline(s), moves, s["idle"], side, contact, keep) for s in cuts]
        worst = min([ft["g"] for ft in fits] + [9.0])
        if best is None or worst > best[0] * 1.08:
            best = (worst, x, sz, fits)
    _, x, size, fits = best
    for s, ft in zip(cuts, fits):
        s["fit"] = ft
    return x, size, side


def outline(sh):
    return animal.outline(sh["path"], sh["crop"], sh["reg"])


def plan_beats(spec, work):
    name, rate = spec.get("voice", "en-US-AndrewNeural"), spec.get("rate", "+0%")
    tempo = float(spec.get("tempo", 1.0))
    beats = spec["beats"]
    ex.voice(beats, work, name, rate)
    looping = any(b.get("loop") for b in beats)
    v4 = spec.get("style") == "v4"
    pins = {str(k): v for k, v in (spec.get("subjects") or {}).items()}
    out, F, shot_no, cur = [], 0, 0, None
    for i, b in enumerate(beats):
        c = b.get("counter")
        if c is False or (b.get("chapter") and b.get("myth") == "outro"):
            cur = None
        elif isinstance(c, dict):
            cur = dict(img=counter_img(c), F=F)
        mp3 = ex.vo_path(b, work, name, rate)
        wav, words = speed(mp3, tempo)
        # cut on the last word, not the TTS file's trailing silence (~0.3 s a line)
        spoken = min(ex.duration(wav), (words[-1][1] + 0.06) if words else ex.duration(wav))
        n = int(round((spoken + GAP + float(b.get("hold", 0))) * FPS))
        D = n / FPS
        # pictures: cut on "at" words; a shot longer than MAX_SHOT is re-cut tighter on the same photo
        vis = ex.shots(b)
        starts, after = [0.0], -1.0
        for s in vis[1:]:
            t = word_time(words, s.get("at"), None, after)
            starts.append(t if t is not None else D * len(starts) / len(vis))
            after = starts[-1]
        shots = []
        for k, s in enumerate(vis):
            a, z = starts[k], (starts[k + 1] if k + 1 < len(vis) else D)
            pieces = [(a, z, s)]
            if z - a > MAX_SHOT:
                n_cut = max(2, math.ceil((z - a) / MAX_SHOT))   # Shorts: 2; long lines alternate crops every <=MAX_SHOT
                cuts_ = []
                for j in range(1, n_cut):
                    aim = a + (z - a) * j / n_cut
                    lo = (cuts_[-1] if cuts_ else a) + 0.9
                    cuts_.append(min((w[0] for w in words if lo <= w[0] <= z - 0.9), key=lambda t: abs(t - aim),
                                     default=aim))
                mid = cuts_[0]
                c = s.get("crop") or [0, 0, 1, 1]
                cx, cy, cw, ch = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2, (c[2] - c[0]) * 0.8, (c[3] - c[1]) * 0.8
                if v4:  # re-cut from the top edge down, so a tighter crop never slices through the head
                    cy = c[1] + ch / 2
                tight = dict(s, crop=[cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], whip=False, parent=c)
                # the loop tail must END on its original crop (= frame 0), so it opens on the tight one
                pieces = [(a, mid, tight), (mid, z, dict(s, whip=False))] if b.get("loop") else [(a, mid, s), (mid, z, tight)]
                if n_cut > 2 and not b.get("loop"):
                    edges = [a] + cuts_ + [z]
                    pieces = [(edges[j], edges[j + 1], (tight if j % 2 else (s if j == 0 else dict(s, whip=False))))
                              for j in range(n_cut)]
            for a_, z_, s_ in pieces:
                path = ex.photo(s_["photo"], s_.get("n", 0), work, s_.get("obs"), "original")
                if s_.get("board"):   # evidence board: the photo pinned to cork with notes and red string
                    path = investigate.board(path, s_["board"], work, vertical=H > W)
                shots.append(dict(f0=int(round(a_ * FPS)), f1=int(round(z_ * FPS)), path=path, crop=s_.get("crop"),
                                  blur=bool(s_.get("blur")), whip=s_.get("whip", True), no=shot_no,
                                  parent=s_.get("parent")))
                if v4 and s_.get("board"):
                    shots[-1].update(subj=None, cut=False, idle="bob", reg=None, why="evidence board")
                elif v4:
                    subject(shots[-1], s_, pins.get(str(s_.get("obs")), {}))
                shot_no += 1
        hit = word_time(words, b.get("hit"), None)
        act = b.get("act") or ("loop_out" if b.get("loop") else "stand")
        dflt = hit if hit is not None else (max(0.0, D - 0.6) if act == "run_off" else 0.25)
        t_act = word_time(words, b.get("act_at"), dflt)
        sub, ask = b.get("sub"), b.get("ask") if isinstance(b.get("ask"), dict) else None
        if sub:  # ask kit: he points down at the follow button; the pill pops, then is pressed with a click
            sub = {"at": "Subscribe"} if sub is True else dict(sub)
            t_sub = word_time(words, sub.get("at", "Subscribe"), 0.2)
            b = dict(b, sfx=list(b.get("sfx", [])) + [f"pop@{t_sub:.3f}", f"click@{t_sub + 0.45:.3f}"])
            sub = dict(img=pill_img(sub.get("text", "SUBSCRIBE")), f=int(round(t_sub * FPS)),
                       press=int(round((t_sub + 0.45) * FPS)))
        if ask:  # ask kit: a pick-one comment card; each choice chip pops in after the last
            t_ask = word_time(words, ask.get("at"), 0.0)
            title, chips = ask_imgs(ask)
            fs = [int(round((t_ask + 0.25 + 0.18 * k) * FPS)) for k in range(len(chips))]
            b = dict(b, sfx=list(b.get("sfx", [])) + [f"pop@{f / FPS:.3f}" for f in fs])
            ask = dict(title=title, chips=chips, f=int(round(t_ask * FPS)), fs=fs)
        pose = "subpoint" if sub else b.get("pose", "deadpan")
        sts = mascot.states(pose, [list(w) for w in words], D, FPS, seed=i)
        x, size, side, moves = float(b.get("x", HOME)), int(b.get("size", SIZE)), 1, []
        lab = b.get("label")
        if isinstance(lab, str):
            lab = {"text": lab}
        lab_img = lab and label_img(lab["text"])
        stamps = []
        for sp in ([b["stamp"]] if isinstance(b.get("stamp"), (dict, str)) else b.get("stamp") or []):
            sp = {"text": sp} if isinstance(sp, str) else sp
            t_st = word_time(words, sp.get("at"), 0.5 * D)
            st_img = investigate.stamp_img(sp["text"], sp.get("color"), 1.35 * UI)
            if st_img.shape[1] > 0.86 * W:   # long words ("TOP SECRET") shrink to fit the frame, slam included
                k_ = 0.86 * W / st_img.shape[1]
                st_img = cv2.resize(st_img, (int(st_img.shape[1] * k_), int(st_img.shape[0] * k_)),
                                    interpolation=cv2.INTER_AREA)
            stamps.append(dict(img=st_img, f=int(round(t_st * FPS)),
                               y=float(sp.get("y", 0.40)), text=sp["text"], reveal=sp.get("reveal", True)))
            b = dict(b, sfx=list(b.get("sfx", [])) + [f"stamp@{t_st:.3f}"])
            if hit is None:
                hit = t_st
        if v4:
            for nm, at in animal.parse(b.get("animal")):
                if nm not in ("lunge", "strike", "shake", "turn"):
                    continue
                ta = word_time(words, at, t_act)
                moves.append((nm, ta))
                if nm in animal.SFX and not any(abs(t - (F / FPS + ta)) < 0.25 for t, _ in auto_sfx(b, words, t_act, F)):
                    snd, off = animal.SFX[nm]
                    b = dict(b, sfx=list(b.get("sfx", [])) + [f"{snd}@{max(0.0, ta + off):.3f}"])
            if b.get("loop") and out:  # the loop tail mirrors the hook, so its last frame matches frame 0
                h0 = out[0]
                x, size, side = h0["x"], h0["size"], h0["side"]
                for s_ in shots:  # a tighter re-cut of the loop shot shares its parent's framing
                    t0 = next((t for t in h0["shots"] if t.get("fit") and (t["path"], t["crop"])
                               == (s_["path"], s_.get("parent") or s_["crop"])), {})
                    s_["fit"], s_["solo"] = t0.get("fit"), t0.get("solo")
                    if s_.get("cut") and s_["fit"] is None:
                        s_["fit"] = stage.frame_fit(outline(s_), moves, s_["idle"], side, False,
                                                    stage.keepout(x, size, side, act="peek"))
            elif "x" not in b:
                top = LABEL_Y + lab_img.shape[0] / 2 + 12 if lab else stage.SAFE[1]
                x, size, side = stage_v4(shots, n, b, moves, top, act)
                if act == "peek":  # before he peeks in, the animal has the frame to itself: big opening frame
                    for s_ in shots:
                        if s_.get("cut"):
                            s_["solo"] = stage.frame_fit(outline(s_), moves, s_["idle"], side, False,
                                                         dict(stage.SOLO, top=top))
            trk = stage.track(mascot, act, n, FPS, t_act, x, side, i)
        else:
            trk = mascot.act_track(act, n, FPS, t_act, x, seed=i)
        punch = b.get("punch") or []
        punch = [punch] if isinstance(punch, str) else punch
        sfx = auto_sfx(b, words, t_act, F)
        out.append(dict(i=i, F=F, n=n, words=words, wav=wav, shots=shots, act=act, sts=sts, trk=trk,
                        hit=None if hit is None else int(round(hit * FPS)),
                        punch=[int(round(word_time(words, p, 0.0) * FPS)) for p in punch],
                        punch_z=float(b.get("punch_z", 0.18)), sfx=sfx, size=size, side=side, moves=moves,
                        contact=bool(b.get("contact")), stamps=stamps,
                        label=lab and dict(img=lab_img,
                                           f=int(round(word_time(words, lab.get("at"), 0.0) * FPS))),
                        prop=b.get("prop"), prop_f=int(round(word_time(words, b.get("prop_at"), 0.3) * FPS)),
                        x=x, loop=bool(b.get("loop")), first=looping and i == 0, say=b["say"], sub=sub, ask=ask,
                        counter=cur,
                        aside=b.get("aside") and dict(img=aside_img(b["aside"]),
                                                      f=int(round(word_time(words, b.get("aside_at"), 0.55 * D) * FPS)))))
        F += n
    return out


# ---------------------------------------------------------------- frames

def _ease_out(u):
    u = min(max(u, 0.0), 1.0)
    return 1 - (1 - u) ** 3


def shot_view(bt, sh, f):
    """Background frame for shot sh at beat frame f: a slow push that never stops."""
    img = base(sh["path"], sh["crop"], sh["blur"])
    t = (f - sh["f0"]) / FPS
    if bt["loop"]:
        z = 1.0 + PUSH * (bt["n"] - 1 - f) / FPS   # ends exactly on frame 0's zoom
    elif bt["first"] and sh is bt["shots"][0]:
        z = 1.0 + PUSH * t                          # frame 0 starts at zoom 1.0
    elif sh["no"] % 2:
        z = max(1.0, 1.0 + PUSH * 3 - PUSH * t)     # push out
    else:
        z = 1.0 + PUSH * t
    return img, z


_LAYERS = {}


def layer(sh, g=None):
    """v4: (blurred painted-out background at g_bg, premultiplied animal sticker at g, sticker offset, g_bg),
    cached per photo and scale. g defaults to the shot's fit."""
    g = round(g or sh["fit"]["g"], 4)
    pw, ph = stage.crop_size(sh["path"], [0, 0, 1, 1])
    g_bg = round(max(g, W / pw, H / ph), 4)   # the background always covers the frame
    key = (sh["path"], tuple(sh["reg"]), g, g_bg, sh["blur"])
    if key not in _LAYERS:
        _LAYERS[key] = animal.layers(sh["path"], sh["crop"], sh["reg"], g, g_bg, sh["blur"]) + (g_bg,)
    return _LAYERS[key]


def premult_over(dst, src, x, y):
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = np.clip(d * (1 - s[..., 3:4] / 255.0) + s[..., :3], 0, 255).astype(np.uint8)


def picture(bt, sh, f, g, dx=0.0):
    """A shot's picture at beat frame f (global frame g): the v3 still, or (v4) the acting cut-out over its
    blurred photo. The cut-out's move is applied on screen around its feet (bob, lunge) or middle (drift)."""
    img, z = shot_view(bt, sh, f)
    if not sh.get("cut"):
        return view(img, z, dx), None
    bg, st, (ox, oy), g_bg = layer(sh)
    ft = sh["fit"]
    gs, tx, ty, k = ft["g"], ft["tx"], ft["ty"], 1.0
    q = bt["trk"][min(f, len(bt["trk"]) - 1)].get("peek", 1.0)
    if sh.get("solo") and q < 1:  # he is peeking in: pull back from the solo framing as he arrives
        so, e = sh["solo"], q * q * (3 - 2 * q)
        gs, tx, ty = (so[c] + (ft[c] - so[c]) * e for c in ("g", "tx", "ty"))
        _, st, (ox, oy), _ = layer(sh, so["g"])   # the background stays the fit's: only the animal moves
        k = gs / round(so["g"], 4)
    pb = animal.photo_box(sh["path"], sh["subj"])
    pcx, pcy = (pb[0] + pb[2]) / 2, (pb[1] + pb[3]) / 2
    scx, scy = tx + gs * pcx, ty + gs * pcy          # the animal's centre on screen
    bh, bw = bg.shape[:2]   # background: same spot of the photo behind the animal, clamped to cover the frame
    bx = min(0.0, max(W - bw, scx - g_bg * pcx))
    by = min(0.0, max(H - bh, scy - g_bg * pcy))
    Mb = np.float32([[z, 0, W / 2 - z * W / 2 + z * bx + dx], [0, z, H / 2 - z * H / 2 + z * by]])
    out = cv2.warpAffine(bg, Mb, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # the cut-out takes no push: a little parallax against the background
    V = np.array([[k, 0, tx + k * ox + dx], [0, k, ty + k * oy], [0, 0, 1]])
    a = (scx + dx, scy if sh["idle"] == "drift" else ty + gs * pb[3])
    toward = 1 if bt["x"] * W >= a[0] else -1
    mv = animal.transform(bt["moves"], f / FPS, toward, sh["no"], sh["idle"], n_left=PLAN["total"] - 1 - g,
                          ts=(f - sh["f0"]) / FPS, n_from=g, reach=ft.get("reach", 1.0))
    r = math.radians(mv["rot"])
    sc = mv["s"]
    A = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]]) @ np.diag(
        [sc * mv["sx"] * (1 - 2 * mv["flip"]), sc * mv["sy"], 1.0])
    M = (np.array([[1, 0, a[0] + mv["dx"] * W], [0, 1, a[1] + mv["dy"] * W], [0, 0, 1]]) @ A
         @ np.array([[1, 0, -a[0]], [0, 1, -a[1]], [0, 0, 1]]) @ V)
    h, w = st.shape[:2]
    pts = M @ np.array([[0, w, w, 0], [0, 0, h, h], [1, 1, 1, 1]])
    x0, y0 = int(max(0, pts[0].min())), int(max(0, pts[1].min()))
    x1, y1 = int(min(W, pts[0].max() + 1)), int(min(H, pts[1].max() + 1))
    if x1 > x0 and y1 > y0:
        M2 = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]]) @ M
        warped = cv2.warpAffine(st, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        premult_over(out, warped, x0, y0)
        wa = warped[..., 3] > 128   # the animal itself (not its shadow padding) reaching a frame edge
        clipped = bool((x0 == 0 and wa[:, 0].any()) or (y0 == 0 and wa[0].any()) or
                       (x1 == W and wa[:, -1].any()) or (y1 == H and wa[-1].any()))
        return out, (warped[..., 3], x0, y0, clipped)
    return out, None


def frame(g):
    P = PLAN
    bi = max(k for k, bt in enumerate(P["beats"]) if bt["F"] <= g)
    bt = P["beats"][bi]
    f = g - bt["F"]
    shots = bt["shots"]
    k = max(j for j, s in enumerate(shots) if s["f0"] <= f or j == 0)
    sh = shots[k]
    bg = None
    cut = P["whips"].get(g)  # whip pan: 6 frames centred on a cut to a different photo (also across beats)
    if cut:
        gc, pb, ps, nb, ns = cut
        u = (g - (gc - 3) + 0.5) / 6.0
        o = int(W * u * u * (3 - 2 * u))
        A = picture(pb, ps, g - pb["F"], g)[0]
        B = picture(nb, ns, g - nb["F"], g)[0]
        bg = np.concatenate([A[:, o:], B[:, :o]], axis=1)
        bg = cv2.blur(bg, (int(170 * math.sin(math.pi * u)) | 1, 1))
    ani = None
    if bg is None:
        bg, ani = picture(bt, sh, f, g)
    frame_ = np.ascontiguousarray(bg)
    st = dict(bt["sts"][min(f, len(bt["sts"]) - 1)])
    tr = bt["trk"][f]
    if tr["run"] is not None:
        st = mascot.apply_run(st, tr["run"])
    if tr["pose"] and tr["pose"] in mascot.POSES and tr["pose"] != "nervous":
        po = mascot.POSES[tr["pose"]]
        st["mouth"] = "o" if tr["pose"] == "shock" else po["mouth"]
        st["brow"] = po["brow"]
    elif tr["pose"] == "nervous":
        st["brow"] = "worry"
    if tr["eyes"]:
        st["eyes"] = tr["eyes"]
    st["head_s"] = tr["head"]
    if bt["prop"] and f >= bt["prop_f"]:  # the Fork drops in beside him and stands there
        p = P["props"][bt["prop"]]
        kf = f - bt["prop_f"]
        drop = int(([-900, -520, -200, 0, -40, 0][kf] if kf < 6 else 0) * UI)
        px = int(bt["x"] * W + bt["size"] * 0.36) if bt["side"] == -1 or not P["v4"] else \
            int(bt["x"] * W - bt["size"] * 0.36 - p.shape[1])   # v4: on his free side, away from the animal
        over(frame_, p, px, FLOOR - p.shape[0] + int(20 * UI) + drop)
    placed = place_meatball(frame_, st, tr, bt["size"])
    qa = (0, 0, False)
    if P["v4"] and ani is not None and not cut:  # QA (not during whip pans): Meatball over the animal, animal under the captions, animal clipped
        aa, ax0, ay0, clipped = ani
        over_mb = 0
        if placed is not None:
            al, mx, my = placed
            x0, y0 = max(ax0, mx), max(ay0, my)
            x1, y1 = min(ax0 + aa.shape[1], mx + al.shape[1]), min(ay0 + aa.shape[0], my + al.shape[0])
            if x1 > x0 and y1 > y0:
                over_mb = int(((aa[y0 - ay0:y1 - ay0, x0 - ax0:x1 - ax0] > 128)
                               & (al[y0 - my:y1 - my, x0 - mx:x1 - mx] > 128)).sum())
        cy0 = max(0, CAP_Y - 75 - ay0)
        c0, c1 = int(W / 2 - 390 * W / 1080), int(W / 2 + 390 * W / 1080)   # the caption band
        under_cap = int((aa[cy0:, max(0, c0 - ax0):max(0, c1 - ax0)] > 128).sum()) if cy0 < aa.shape[0] else 0
        qa = (over_mb, under_cap, bool(clipped))
    if bt["label"] and f >= bt["label"]["f"]:
        kf = f - bt["label"]["f"]
        s = [0.35, 0.75, 1.15, 1.06, 1.0][kf] if kf < 5 else 1.0
        li = bt["label"]["img"]
        li = cv2.resize(li, (max(1, int(li.shape[1] * s)), max(1, int(li.shape[0] * s))))
        over(frame_, li, W // 2 - li.shape[1] // 2, LABEL_Y - li.shape[0] // 2)
    if bt.get("aside") and f >= bt["aside"]["f"]:  # the footnote joke, low right, clear of the captions
        ai = bt["aside"]["img"]
        _over_scaled(frame_, ai, _pop(f - bt["aside"]["f"]), W - 40 - ai.shape[1] / 2, CAP_Y - 95 * UI - ai.shape[0] / 2)
    for sp in bt["stamps"]:   # verdict stamp: slams down from big and settles, then holds to the end of the line
        kf = f - sp["f"]
        if kf >= 0:
            s = [2.3, 1.6, 1.12, 0.95, 1.02][kf] if kf < 5 else 1.0
            _over_scaled(frame_, sp["img"], s, W / 2, H * sp["y"])
    # camera: punch-in zooms and impact shake on the whole picture
    zc, sx, sy = 1.0, 0.0, 0.0
    for pf in bt["punch"]:
        d = f - pf
        if d >= 0:
            env = _ease_out((d + 1) / 3) if d < 3 else (1.0 if d < 3 + 0.75 * FPS else max(0.0, 1 - (d - 3 - 0.75 * FPS) / 8))
            zc = max(zc, 1 + bt["punch_z"] * env)
    if bt["hit"] is not None and 0 <= f - bt["hit"] < 10:
        d = f - bt["hit"]
        amp = 34 * math.exp(-d / 3.5)
        sx, sy = amp * math.sin(d * 2.3 + 0.7), amp * math.cos(d * 2.9)
        zc = max(zc, 1.04)
    if zc != 1.0 or sx or sy:
        cx, cy = W / 2, CAM_Y
        m = np.float32([[zc, 0, cx - zc * cx + sx], [0, zc, cy - zc * cy + sy]])
        frame_ = cv2.warpAffine(frame_, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if bt["hit"] is not None and 0 <= f - bt["hit"] < 3:  # white impact flash
        a = (0.85, 0.55, 0.25)[f - bt["hit"]]
        frame_ = (frame_.astype(np.float32) * (1 - a) + 255 * a).astype(np.uint8)
    if bt["sub"] and f >= bt["sub"]["f"]:  # ask kit: the pill sits down and out from his pointing hand
        su = bt["sub"]
        s = _pop(f - su["f"]) * (0.88 if 0 <= f - su["press"] < 4 else 1.0)
        hw = su["img"].shape[1] * 0.85 / 2
        cx = min(max(bt["x"] * W + bt["side"] * bt["size"] * 0.62, hw + 30), W - hw - 30)
        _over_scaled(frame_, su["img"], s * 0.85, cx, PILL_Y)   # just under his hand, clear of the captions
    if bt["ask"] and f >= bt["ask"]["f"]:  # ask kit: the comment card, title then chips in one or two rows
        q = bt["ask"]
        _over_scaled(frame_, q["title"], _pop(f - q["f"]), W / 2, LABEL_Y)
        chips, gap = q["chips"], 30 * CARD
        rows = [chips] if sum(c.shape[1] for c in chips) + gap * (len(chips) - 1) <= W - 80 else \
            [chips[:(len(chips) + 1) // 2], chips[(len(chips) + 1) // 2:]]
        k = 0
        y = LABEL_Y + q["title"].shape[0] / 2 + 110 * CARD
        for row in rows:
            ww = sum(c.shape[1] for c in row) + gap * (len(row) - 1)
            x = (W - ww) / 2
            for c in row:
                if f >= q["fs"][k]:
                    _over_scaled(frame_, c, _pop(f - q["fs"][k]), x + c.shape[1] / 2, y)
                x += c.shape[1] + gap
                k += 1
            y += 165 * CARD
    if W > H:   # long-form HUD only (16:9)
        hud(frame_, bt, g)
    if P.get("series"):   # "Meatball Investigates": the tag on every frame, the case-file card on the hook
        card, tag = P["series"]
        over(frame_, tag, int(30 * W / 1080), int((140 if H > W else 24) * UI))
        if bi == 0 and f >= 4:
            kf = f - 4
            dy = [-260, -120, -30, 8, 0][kf] if kf < 5 else 0
            over(frame_, card, int(W / 2 - card.shape[1] / 2), int((215 if H > W else 70) + dy))
    return frame_.tobytes(), qa


def captions(beats, path):
    """Two-word cards in the lower third, the spoken word yellow; each card pops in."""
    bold = PLAN.get("captions") == "bold"   # Meatball Investigates: heavier, bigger, thicker outline
    style = (f"Style: Cap,Inter Black,{int(CAP_FS * 1.12)},&H00FFFFFF,&H00000000,&H96000000,0,1,11,5,5,0\n\n" if bold
             else f"Style: Cap,DejaVu Sans,{CAP_FS},&H00FFFFFF,&H00000000,&H64000000,-1,1,8,3,5,0\n\n")
    head = (f"[Script Info]\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
            "PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV\n"
            + style +
            "[Events]\nFormat: Layer, Start, End, Style, Text\n")
    from facts import ass_time
    lines = []
    for bt in beats:
        T0, words = bt["F"] / FPS, bt["words"]
        for i in range(0, len(words), 2):
            group = words[i:i + 2]
            for j, (s, e, _) in enumerate(group):
                nxt = words[i + 2][0] if i + 2 < len(words) else e + 0.08
                end = group[j + 1][0] if j + 1 < len(group) else min(e + 0.08, nxt)
                pop = r"\fscx70\fscy70\t(0,90,\fscx112\fscy112)" if j == 0 else r"\fscx112\fscy112"
                text = " ".join(("{\\c&H00FFFF&}" + w.upper() + "{\\c&HFFFFFF&}") if q == j else w.upper()
                                for q, (_, _, w) in enumerate(group))
                lines.append(f"Dialogue: 0,{ass_time(T0 + s)},{ass_time(T0 + end)},Cap,"
                             f"{{\\an5\\pos({W // 2},{CAP_Y}){pop}}}{text}")
    open(path, "w").write(head + "\n".join(lines) + "\n")


def gate(beats, total):
    """v3 self-check: cut lengths and how often something new happens."""
    warn, events = [], []
    for bt in beats:
        for s in bt["shots"]:
            d = (s["f1"] - s["f0"]) / FPS
            if d > HOLD_MAX + 1e-6:
                warn.append(f"beat {bt['i']} holds one picture {d:.2f}s (max {HOLD_MAX})")
            events.append(bt["F"] / FPS + s["f0"] / FPS)
        events += [bt["F"] / FPS + p / FPS for p in bt["punch"]]
        events += [t for t, _ in bt["sfx"]]
        if bt["act"] not in ("stand",):
            events.append(bt["F"] / FPS)
        if bt["label"]:
            events.append(bt["F"] / FPS + bt["label"]["f"] / FPS)
        if bt["sub"]:
            events.append(bt["F"] / FPS + bt["sub"]["f"] / FPS)
        if bt["ask"]:
            events += [bt["F"] / FPS + f / FPS for f in [bt["ask"]["f"]] + bt["ask"]["fs"]]
        if bt.get("aside"):
            events.append(bt["F"] / FPS + bt["aside"]["f"] / FPS)
        events += [bt["F"] / FPS + sp["f"] / FPS for sp in bt["stamps"]]
    for bt in beats:  # ask kit placement (research/46): hook first, guess card 3-6 s, pill 6-10 s, reminder at the end
        if bt["sub"]:
            t = (bt["F"] + bt["sub"]["f"]) / FPS
            if not ASK_PILL[0] <= t <= ASK_PILL[1]:
                warn.append(f"beat {bt['i']} subscribe pill at {t:.1f}s (aim {ASK_PILL[0]:g}-{ASK_PILL[1]:g} s)")
        if bt["ask"]:
            t = (bt["F"] + bt["ask"]["f"]) / FPS
            if t < ASK_NONE:
                warn.append(f"beat {bt['i']} comment card at {t:.1f}s: no ask in the first {ASK_NONE:g} s")
            elif bt["ask"]["chips"] and not ASK_GUESS[0] <= t <= ASK_GUESS[1]:
                warn.append(f"beat {bt['i']} guess card at {t:.1f}s (aim {ASK_GUESS[0]:g}-{ASK_GUESS[1]:g} s, "
                            "right after the hook)")
            elif not bt["ask"]["chips"] and any(b_["loop"] for b_ in beats) and bt["i"] + 1 < len(beats) \
                    and not beats[bt["i"] + 1]["loop"]:
                warn.append(f"beat {bt['i']} reminder card is not the last beat before the loop")
            elif not bt["ask"]["chips"] and total - t > 90:   # long-form: "Were you right?" sits in the ending
                warn.append(f"beat {bt['i']} reminder card {total - t:.0f}s before the end (aim: the last 90 s)")
        if bt["F"] / FPS < ASK_NONE and bt["sub"]:
            warn.append(f"beat {bt['i']} subscribe ask in the first {ASK_NONE:g} s")
    if sum(1 for bt in beats if bt["sub"]) > 1:
        warn.append("more than one subscribe pill (one early ask; no nagging)")
    events = sorted(events)
    gaps = [b - a for a, b in zip([0.0] + events, events + [total])]
    if max(gaps) > GAP_MAX:
        warn.append(f"longest stretch with nothing new: {max(gaps):.1f}s")
    for w in warn:
        print("GATE WARN:", w, flush=True)
    print(f"v3 gate: {len(events)} events in {total:.1f}s, longest gap {max(gaps):.2f}s", flush=True)


def report_v4(beats, work):
    """v4 gate: which shots act as cut-outs, which fell back to the v3 still (and why), Meatball's marks."""
    shots, stills = [], []
    for bt in beats:
        for s in bt["shots"]:
            e = dict(beat=bt["i"], photo=os.path.basename(s["path"]), crop=s["crop"], blur=s["blur"],
                     cut=s.get("cut"), why=s.get("why"), sec=round((s["f1"] - s["f0"]) / FPS, 2))
            shots.append(e)
            if not s.get("cut"):
                stills.append(e)
                print(f"V4 FALLBACK: beat {bt['i']} {e['photo']} {s['crop']}: {s.get('why')}", flush=True)
    marks = [dict(beat=bt["i"], x=round(bt["x"], 3), size=bt["size"], side=bt["side"], act=bt["act"],
                  contact=bt["contact"], moves=bt["moves"]) for bt in beats]
    n = len(shots)
    print(f"v4 gate: {n - len(stills)}/{n} shots act as cut-outs; {len(stills)} v3 stills", flush=True)
    for bt in beats:  # hard rules (Nolan, 10/25): a cut-out is the whole animal, none of it lost to clean-up
        for s in bt["shots"]:
            if s.get("cut") and (s["subj"].get("touch") or s["subj"].get("loss", 1) > animal.MAX_LOSS):
                raise SystemExit(f"v4 gate: beat {bt['i']} cut-out touches the photo edge or loses "
                                 f"{s['subj'].get('loss', 1):.0%} of the matte")
    json.dump(dict(shots=shots, marks=marks), open(f"{work}/v4.json", "w"), indent=1)
    return stills


def build(spec, work, out, music=None, vertical=True):
    os.makedirs(work, exist_ok=True)
    if vertical:
        ex.vertical()
    else:
        landscape()
    beats = plan_beats(spec, work)
    total_f = beats[-1]["F"] + beats[-1]["n"]
    cuts = {}
    flat = [(bt, s) for bt in beats for s in bt["shots"]]
    for (pb, ps), (nb, ns) in zip(flat, flat[1:]):
        g = nb["F"] + ns["f0"]
        if ns["whip"] and (ns["path"], ns["crop"]) != (ps["path"], ps["crop"]) and not ns.get("blur"):
            for d in range(-3, 3):
                cuts[g + d] = (g, pb, ps, nb, ns)
    PLAN.clear()
    v4 = spec.get("style") == "v4"
    PLAN.update(progress=bool(spec.get("progress")) and not vertical,
                ticks=sorted({bt["counter"]["F"] for bt in beats if bt.get("counter")}))
    investigate.ensure_sfx(SFX_DIR)
    PLAN.update(series=spec.get("series") and investigate.series_imgs(spec["series"], W),
                captions=spec.get("captions"))
    if spec.get("series"):   # the case sting under the card drop
        beats[0]["sfx"] = list(beats[0]["sfx"]) + [(4 / FPS, "case")]
    PLAN.update(beats=beats, whips=cuts, props={"fork": np.asarray(mascot.prop("fork", int(520 * UI)))}, v4=v4,
                total=total_f)
    for bt in beats:  # warm the photo (and v4 cut-out) caches before forking the workers
        for s in bt["shots"]:
            base(s["path"], s["crop"], s["blur"])
            if s.get("cut"):
                layer(s)
                if s.get("solo"):
                    layer(s, s["solo"]["g"])
    total = total_f / FPS
    gate(beats, total)
    if v4:
        stills = report_v4(beats, work)
    # audio: voice lines, SFX under them, music bed ducked by the voice
    voice = np.zeros((int(total * SR) + SR, 2), np.float32)
    sfx = np.zeros_like(voice)
    kit = {}
    for bt in beats:
        a = read_wav(bt["wav"])
        s0 = int(bt["F"] / FPS * SR)
        voice[s0:s0 + len(a)] += a[:len(voice) - s0]
        for t, nm in bt["sfx"]:
            if nm not in kit:
                kit[nm] = read_wav(f"{SFX_DIR}/{nm}.wav")
            a = kit[nm] * GAIN.get(nm, 0.3)
            s1 = int(t * SR)
            sfx[s1:s1 + len(a)] += a[:len(sfx) - s1]
    write_wav(f"{work}/voice.wav", voice)
    write_wav(f"{work}/sfx.wav", sfx)
    cap = f"{work}/cap.ass"
    captions(beats, cap)
    gen = str(spec.get("music") or "")
    lufs = gen.startswith("gen:") or spec.get("music_mix") == "lufs"
    if gen.startswith("gen:"):   # an original bed rendered to this timeline (tools/music.py)
        import music as mus
        reveals = [(bt["F"] + sp["f"]) / FPS for bt in beats for sp in bt["stamps"] if sp["reveal"]]
        music = f"{work}/music-{gen[4:]}.wav"
        mus.render(gen[4:], total, reveals, music)
    music = music if music and os.path.exists(music) else None
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "pipe:0", "-i", f"{work}/voice.wav", "-i", f"{work}/sfx.wav"]
    if music and lufs:   # Nolan 10/25: music around -20 LUFS against the voice at -16, ducked; voice always clear
        cmd += (["-i", music] if gen.startswith("gen:") else ["-stream_loop", "-1", "-i", music])
        af = ("[1:a]loudnorm=I=-16:TP=-2,asplit[vo][key];[3:a]loudnorm=I=-20:TP=-4[m];[m][key]sidechaincompress="
              "threshold=0.05:ratio=3:attack=20:release=350[d];[vo][d][2:a]amix=inputs=3:duration=first:normalize=0,"
              "loudnorm=I=-14:TP=-1.5[a]")
    elif music:
        cmd += ["-stream_loop", "-1", "-i", music]
        af = ("[1:a]asplit[vo][key];[3:a]volume=0.12[m];[m][key]sidechaincompress=threshold=0.02:ratio=6:"
              "attack=30:release=500[d];[vo][d][2:a]amix=inputs=3:duration=first:normalize=0,"
              "loudnorm=I=-14:TP=-1.5[a]")
    else:
        af = "[1:a][2:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]"
    cmd += ["-filter_complex", f"[0:v]ass={cap},format=yuv420p[v];{af}", "-map", "[v]", "-map", "[a]",
            "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac",
            "-b:a", "160k", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    jobs = int(os.environ.get("MEATBALL_JOBS", "2"))
    with mp.get_context("fork").Pool(jobs) as pool:
        qas = []
        for k, (buf, qa) in enumerate(pool.imap(frame, range(total_f), chunksize=4)):
            proc.stdin.write(buf)
            qas.append(qa)
            if k % 150 == 0:
                print(f"v3 frame {k}/{total_f}", flush=True)
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    used = sorted({s["path"] for bt in beats for s in bt["shots"]})
    open(f"{work}/credits.txt", "w").write("".join(open(u + ".credit").read() + "\n" for u in used))
    json.dump([dict(i=bt["i"], start=bt["F"] / FPS, dur=bt["n"] / FPS, act=bt["act"], say=bt["say"],
                    shots=[(s["f0"] / FPS, s["f1"] / FPS) for s in bt["shots"]], sfx=bt["sfx"]) for bt in beats],
              open(f"{work}/timeline.json", "w"), indent=1)
    if v4:  # QA by beat: frames where Meatball covers the animal (contact beats may), animal under captions
        bad = {}
        for g, (mb, cap, clip) in enumerate(qas):
            bt = max((b for b in beats if b["F"] <= g), key=lambda b: b["F"])
            e = bad.setdefault(bt["i"], dict(act=bt["act"], contact=bt["contact"], meatball=0, captions=0, clipped=0))
            e["meatball"] += mb > 300
            e["captions"] += cap > 300
            e["clipped"] += bool(clip)
        bad = {i: e for i, e in bad.items() if e["meatball"] or e["captions"] or e["clipped"]}
        rep = json.load(open(f"{work}/v4.json"))
        rep["overlap"] = {str(i): e for i, e in bad.items()}
        json.dump(rep, open(f"{work}/v4.json", "w"), indent=1)
        for i, e in sorted(bad.items()):
            print(f"V4 QA: beat {i} ({e['act']}{', contact' if e['contact'] else ''}): Meatball over the animal "
                  f"{e['meatball']} frames, animal under captions {e['captions']}, clipped {e['clipped']}", flush=True)
        if any(e["clipped"] for e in bad.values()):
            raise SystemExit("v4 gate: an acting animal leaves the frame (see V4 QA)")
    print(f"ok {out} {total:.1f}s")
