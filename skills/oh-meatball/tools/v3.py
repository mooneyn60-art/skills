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
Photos come from explainer.photo() (pinned iNaturalist observations, full resolution).
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

import explainer as ex
import mascot

FPS, W, H, SR = 30, 1080, 1920, 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX_DIR = os.path.join(ROOT, "sfx")
GAIN = {"whoosh": 0.32, "boing": 0.22, "pop": 0.30, "scratch": 0.20, "splash": 0.34, "tink": 0.40,
        "crunch": 0.42, "hit": 0.40, "thud": 0.42, "zap": 0.28, "plate": 0.30}
R = 1.15          # photo bases are prepared 15% over frame size so slow pushes stay sharp
GAP = 0.12        # silence after each line (v2 used 0.35)
FLOOR = 1430      # Meatball's feet (screen y); captions sit just below
CAP_Y = 1560
MAX_SHOT = 2.4    # a shot longer than this is re-cut to a tighter crop of the same photo (gate: 2.5 s)
PUSH = 0.045      # zoom per second of the slow push (v2: 0.036)
HOME = 0.24       # Meatball's mark: left of centre, so the animal (centred in each crop) stays visible
PLAN = {}         # filled before the frame workers fork


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
    return np.asarray(im)


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
        return
    spr, pad = sprite(st, size)
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
        return
    M2 = T(-x0, -y0) @ M
    out = cv2.warpAffine(spr, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    over(frame, out, x0, y0)


# ---------------------------------------------------------------- plan

def plan_beats(spec, work):
    name, rate = spec.get("voice", "en-US-AndrewNeural"), spec.get("rate", "+0%")
    tempo = float(spec.get("tempo", 1.0))
    beats = spec["beats"]
    ex.voice(beats, work, name, rate)
    looping = any(b.get("loop") for b in beats)
    out, F, shot_no = [], 0, 0
    for i, b in enumerate(beats):
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
                mid = min((w[0] for w in words if a + 0.9 <= w[0] <= z - 0.9), key=lambda t: abs(t - (a + z) / 2),
                          default=(a + z) / 2)
                c = s.get("crop") or [0, 0, 1, 1]
                cx, cy, cw, ch = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2, (c[2] - c[0]) * 0.8, (c[3] - c[1]) * 0.8
                tight = dict(s, crop=[cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], whip=False)
                # the loop tail must END on its original crop (= frame 0), so it opens on the tight one
                pieces = [(a, mid, tight), (mid, z, dict(s, whip=False))] if b.get("loop") else [(a, mid, s), (mid, z, tight)]
            for a_, z_, s_ in pieces:
                path = ex.photo(s_["photo"], s_.get("n", 0), work, s_.get("obs"), "original")
                shots.append(dict(f0=int(round(a_ * FPS)), f1=int(round(z_ * FPS)), path=path, crop=s_.get("crop"),
                                  blur=bool(s_.get("blur")), whip=s_.get("whip", True), no=shot_no))
                shot_no += 1
        hit = word_time(words, b.get("hit"), None)
        act = b.get("act") or ("loop_out" if b.get("loop") else "stand")
        dflt = hit if hit is not None else (max(0.0, D - 0.6) if act == "run_off" else 0.25)
        t_act = word_time(words, b.get("act_at"), dflt)
        pose = b.get("pose", "deadpan")
        sts = mascot.states(pose, [list(w) for w in words], D, FPS, seed=i)
        trk = mascot.act_track(act, n, FPS, t_act, float(b.get("x", HOME)), seed=i)
        punch = b.get("punch") or []
        punch = [punch] if isinstance(punch, str) else punch
        sfx = []
        for e in b.get("sfx", []):
            nm, _, at = e.partition("@")
            t = t_act if not at else (t_act if at == "act" else word_time(words, at, t_act))
            sfx.append((F / FPS + max(0.0, t), nm))
        lab = b.get("label")
        if isinstance(lab, str):
            lab = {"text": lab}
        out.append(dict(i=i, F=F, n=n, words=words, wav=wav, shots=shots, act=act, sts=sts, trk=trk,
                        hit=None if hit is None else int(round(hit * FPS)),
                        punch=[int(round(word_time(words, p, 0.0) * FPS)) for p in punch],
                        punch_z=float(b.get("punch_z", 0.18)), sfx=sfx, size=int(b.get("size", 1000)),
                        label=lab and dict(img=label_img(lab["text"]),
                                           f=int(round(word_time(words, lab.get("at"), 0.0) * FPS))),
                        prop=b.get("prop"), prop_f=int(round(word_time(words, b.get("prop_at"), 0.3) * FPS)),
                        x=float(b.get("x", HOME)), loop=bool(b.get("loop")), first=looping and i == 0, say=b["say"]))
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


def frame(g):
    P = PLAN
    bi = max(k for k, bt in enumerate(P["beats"]) if bt["F"] <= g)
    bt = P["beats"][bi]
    f = g - bt["F"]
    shots = bt["shots"]
    k = max(j for j, s in enumerate(shots) if s["f0"] <= f or j == 0)
    sh = shots[k]
    img, z = shot_view(bt, sh, f)
    bg = None
    cut = P["whips"].get(g)  # whip pan: 6 frames centred on a cut to a different photo (also across beats)
    if cut:
        gc, pb, ps, nb, ns = cut
        u = (g - (gc - 3) + 0.5) / 6.0
        o = int(W * u * u * (3 - 2 * u))
        A = view(*shot_view(pb, ps, g - pb["F"]))
        B = view(*shot_view(nb, ns, g - nb["F"]))
        bg = np.concatenate([A[:, o:], B[:, :o]], axis=1)
        bg = cv2.blur(bg, (int(170 * math.sin(math.pi * u)) | 1, 1))
    if bg is None:
        bg = view(img, z)
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
        drop = [-900, -520, -200, 0, -40, 0][kf] if kf < 6 else 0
        over(frame_, p, int(bt["x"] * W + bt["size"] * 0.36), FLOOR - p.shape[0] + 20 + drop)
    place_meatball(frame_, st, tr, bt["size"])
    if bt["label"] and f >= bt["label"]["f"]:
        kf = f - bt["label"]["f"]
        s = [0.35, 0.75, 1.15, 1.06, 1.0][kf] if kf < 5 else 1.0
        li = bt["label"]["img"]
        li = cv2.resize(li, (max(1, int(li.shape[1] * s)), max(1, int(li.shape[0] * s))))
        over(frame_, li, W // 2 - li.shape[1] // 2, 330 - li.shape[0] // 2)
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
        cx, cy = W / 2, 860
        m = np.float32([[zc, 0, cx - zc * cx + sx], [0, zc, cy - zc * cy + sy]])
        frame_ = cv2.warpAffine(frame_, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if bt["hit"] is not None and 0 <= f - bt["hit"] < 3:  # white impact flash
        a = (0.85, 0.55, 0.25)[f - bt["hit"]]
        frame_ = (frame_.astype(np.float32) * (1 - a) + 255 * a).astype(np.uint8)
    return frame_.tobytes()


def captions(beats, path):
    """Two-word cards in the lower third, the spoken word yellow; each card pops in."""
    head = (f"[Script Info]\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
            "PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV\n"
            "Style: Cap,DejaVu Sans,100,&H00FFFFFF,&H00000000,&H64000000,-1,1,8,3,5,0\n\n"
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
            if d > 2.5 + 1e-6:
                warn.append(f"beat {bt['i']} holds one picture {d:.2f}s (max 2.5)")
            events.append(bt["F"] / FPS + s["f0"] / FPS)
        events += [bt["F"] / FPS + p / FPS for p in bt["punch"]]
        events += [t for t, _ in bt["sfx"]]
        if bt["act"] not in ("stand",):
            events.append(bt["F"] / FPS)
        if bt["label"]:
            events.append(bt["F"] / FPS + bt["label"]["f"] / FPS)
    events = sorted(events)
    gaps = [b - a for a, b in zip([0.0] + events, events + [total])]
    if max(gaps) > 3.0:
        warn.append(f"longest stretch with nothing new: {max(gaps):.1f}s")
    for w in warn:
        print("GATE WARN:", w, flush=True)
    print(f"v3 gate: {len(events)} events in {total:.1f}s, longest gap {max(gaps):.2f}s", flush=True)


def build(spec, work, out, music=None):
    os.makedirs(work, exist_ok=True)
    ex.vertical()
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
    PLAN.update(beats=beats, whips=cuts, props={"fork": np.asarray(mascot.prop("fork", 520))})
    for bt in beats:  # warm the photo cache before forking the workers
        for s in bt["shots"]:
            base(s["path"], s["crop"], s["blur"])
    total = total_f / FPS
    gate(beats, total)
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
    music = music if music and os.path.exists(music) else None
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "pipe:0", "-i", f"{work}/voice.wav", "-i", f"{work}/sfx.wav"]
    if music:
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
        for k, buf in enumerate(pool.imap(frame, range(total_f), chunksize=4)):
            proc.stdin.write(buf)
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
    print(f"ok {out} {total:.1f}s")
