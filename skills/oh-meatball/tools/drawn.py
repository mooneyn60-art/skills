#!/usr/bin/env python3
"""Fully drawn Meatball renderer (Nolan 10/27: no pop-up text, Meatball big and inside the scene, everything
drawn, animated). One JSON scene spec -> one 1080x1920 video; a new video is just a new spec.

Usage: drawn.py SPEC.json OUT.mp4 [--nocap OUT_NOCAP.mp4] [--fps 30] [--frames-only N]
       (renders the voice once; writes the captioned cut and, with --nocap, the same cut without captions)

Spec (see scripts/drawn-1027/*.json):
  voice, rate, pitch       edge-tts voice for Meatball's narration (he is the narrator; his mouth flaps on it)
  music, music_db          a tools/music.py bed kind ("detective", "cold-war", "ocean", ...) and its level
  captions                 caption size in px (small 1-3 word spoken-word captions; the --nocap cut drops them)
  beats[]                  one spoken line each:
    say                    the line
    scene, scene_p         a drawn habitat from drawn_assets.SCENES (inherits from the previous beat)
    shots[]                camera cuts inside the beat: {"at": time, "cam": [x, y, zoom], "to": [x, y, zoom],
                           "dur": s}; the camera eases cam -> to; no "cam" = continue from where it was
    actors[]               {"id", "type" (drawn_actors / drawn_cast ACTORS), "pos": [x, y], "s", "flip", "front",
                           "p": {...params}, "moves": [{"at", "dur", "pos", "s", "rot", "hop", "walk"}],
                           "set": [{"at", "p": {...}}]} ; an id seen in the previous beat inherits its end state
    keep                   true = carry every actor of the previous beat forward; "drop": [ids] removes some
    mb                     Meatball: {"pose", "pos": feet [x, y], "size" (px per 1000 rig units at zoom 1),
                           "moves": [...as actors], "gest": [[at, pose, hold]], "look": actor id | "viewer",
                           "shake": 0..1, "helmet": bool, "prop": "flashlight" | "mic" | "paper"}
    sfx                    ["pop@word", "whoosh@0.4"]: tools' sfx/*.wav at a word or time in the beat
    flash                  [at, ...] white camera-flash frames;  shake: [at, ...] camera shake hits
  "at" is seconds into the beat or a spoken word ("claw", "claw+0.3", "claw#2" = its 2nd occurrence).
"""
import asyncio
import json
import math
import os
import subprocess
import sys
import wave

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mascot  # noqa: E402
import music  # noqa: E402
from drawn_kit import INK, OUT, PAL, ease, ink, p_ellipse, src, stroke  # noqa: E402
from drawn_assets import SCENES  # noqa: E402
from drawn_actors import ACTORS as A1  # noqa: E402
from drawn_cast import ACTORS as A2  # noqa: E402

ACTORS = {**A1, **A2}
ROOT = os.path.dirname(HERE)
W, H = 1080, 1920
SR = 48000
FONT = os.path.join(ROOT, "brand/fonts/Anton-Regular.ttf")


# ---------------------------------------------------------------- voice

def tts(text, voice, rate, pitch, mp3):
    from facts import speak
    if not (os.path.exists(mp3) and os.path.exists(mp3 + ".words.json")):
        words = asyncio.run(speak(text, voice, mp3, rate, pitch))
        json.dump(words, open(mp3 + ".words.json", "w"))
    return json.load(open(mp3 + ".words.json"))


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


# ---------------------------------------------------------------- timing helpers

def at_time(words, at, default=0.0):
    """Seconds into the beat for an "at": a number, or a word ("word", "word+0.3", "word#2")."""
    if at is None:
        return default
    if isinstance(at, (int, float)):
        return float(at)
    w, off = at, 0.0
    for sign in ("+", "-"):
        if sign in w[1:]:
            w, o = w.rsplit(sign, 1)
            off = float(o) * (1 if sign == "+" else -1)
    nth = 1
    if "#" in w:
        w, n = w.split("#")
        nth = int(n)
    key = w.lower().strip(".,!?'\"")
    seen = 0
    for s, e, x in words:
        if x.lower().strip(".,!?'\"").startswith(key):
            seen += 1
            if seen == nth:
                return max(0.0, s + off)
    raise SystemExit(f"drawn: word {at!r} not in line {' '.join(x for _, _, x in words)!r}")


def track(start, moves, words, t, scale0=1.0, rot0=0.0):
    """Position/scale/rotation at t from a start pos and a move list. Returns (x, y, s, rot, hop_land_f, walking)."""
    x, y = start
    s, rot = scale0, rot0
    land, walking, dist = None, False, 0.0
    for m in moves:
        a = at_time(words, m.get("at"), 0.0)
        d = max(m.get("dur", 0.5), 1e-3)
        u = (t - a) / d
        tx, ty = m.get("pos", (x, y))
        ts, tr = m.get("s", s), m.get("rot", rot)
        if u <= 0:
            break
        k = ease(u) if not m.get("hop") else min(u, 1.0)
        if m.get("linear"):
            k = min(u, 1.0)
        nx, ny = x + (tx - x) * k, y + (ty - y) * k
        if m.get("hop") and u < 1:
            ny -= m["hop"] * 4 * k * (1 - k)
        if m.get("walk") and u < 1:
            walking = True
        dist += math.hypot(nx - x, ny - y) if m.get("walk") else 0.0
        if m.get("hop") and u >= 1:
            land = t - (a + d)
        x, y, s, rot = nx, ny, s + (ts - s) * ease(u), rot + (tr - rot) * ease(u)
    return x, y, s, rot, land, walking


# ---------------------------------------------------------------- plan

def plan(spec, work):
    voice, rate, pitch = spec.get("voice", "en-US-AndrewMultilingualNeural"), spec.get("rate", "+4%"), \
        spec.get("pitch", "+0Hz")
    beats, t0 = [], 0.0
    prev_actors, scene, scene_p, cam = {}, None, {}, [540, 960, 1.0]
    prev_mb = {}
    for i, b in enumerate(spec["beats"]):
        mp3 = f"{work}/v{i:02d}.mp3"
        words = [tuple(w) for w in tts(b["say"], voice, rate, pitch, mp3)]
        audio = decode(mp3)
        speech = len(audio) / SR
        dur = speech + b.get("pad", 0.18)
        scene = b.get("scene", scene)
        scene_p = b.get("scene_p", scene_p if "scene" not in b else {})
        # actors: inherit end states
        actors = {}
        if b.get("keep"):
            actors = {k: dict(v, moves=[], set=[]) for k, v in prev_actors.items() if k not in b.get("drop", [])}
        for a in b.get("actors", []):
            base = dict(prev_actors.get(a["id"], {}), moves=[], set=[])
            base.update(a)
            if a["id"] in prev_actors and "p" in a:
                base["p"] = {**prev_actors[a["id"]].get("p", {}), **a["p"]}
            actors[a["id"]] = base
        shots = b.get("shots") or [{}]
        sh2 = []
        for s in shots:
            c0 = list(s.get("cam", cam))
            c1 = list(s.get("to", c0))
            sh2.append(dict(s, cam=c0, to=c1, at=at_time(words, s.get("at"), 0.0)))
            cam = c1
        mb = dict(prev_mb)
        mb.update(b.get("mb", {}))
        mb.setdefault("pos", [540, 1700])
        mb.setdefault("size", 1100)
        mb["moves"] = b.get("mb", {}).get("moves", [])
        mb["gest"] = b.get("mb", {}).get("gest", [])
        for k in ("shake", "helmet", "prop", "look", "hidden", "mute", "float"):
            if k not in b.get("mb", {}):
                mb[k] = prev_mb.get(k) if k in ("helmet", "float") else None
        beats.append(dict(b, i=i, t0=t0, dur=dur, speech=speech, words=words, audio=audio, scene=scene,
                          scene_p=scene_p, actors=actors, shots=sh2, mb=mb))
        # end states for inheritance
        end = {}
        for k, a in actors.items():
            x, y, s, r, _, _ = track(a.get("pos", (0, 0)), a.get("moves", []), words, dur, a.get("s", 1.0),
                                     a.get("rot", 0.0))
            p = dict(a.get("p", {}))
            for st in a.get("set", []):
                p.update(st["p"])
            end[k] = dict(a, pos=[x, y], s=s, rot=r, p=p)
        prev_actors = end
        x, y, s, _, _, _ = track(mb["pos"], mb["moves"], words, dur, mb["size"])
        prev_mb = dict(mb, pos=[x, y], size=s)
        t0 += dur
    return beats, t0


def rig_tracks(beats, fps):
    """Meatball's acting per beat from mascot.states (lip-sync, blinks, gestures), cross-blended at beat joins."""
    out, last = [], None
    for k, b in enumerate(beats):
        mb, words = b["mb"], b["words"]
        n = int(round(b["dur"] * fps))
        extra = [(at_time(words, g[0]), g[1], g[2] if len(g) > 2 else 1.0) for g in mb.get("gest", [])]
        sts = mascot.states(mb.get("pose", "neutral"), words, n / fps, fps, seed=k, enter=False,
                            exit=(k == len(beats) - 1 and b.get("loop_rest", False)), size=mb["size"],
                            extra=extra)
        while len(sts) < n:
            sts.append(dict(sts[-1]))
        if last is not None:
            for f in range(min(6, n)):
                u = ease((f + 1) / 7)
                st = sts[f]
                for key in ("lean", "tilt", "knee", "shrug"):
                    st[key] = last[key] + (st[key] - last[key]) * u
                for key in ("l", "r"):
                    st[key] = tuple(a + (c - a) * u for a, c in zip(last[key], st[key]))
        out.append(sts[:n])
        last = sts[n - 1] if n else last
    return out


# ---------------------------------------------------------------- frame drawing

def cam_at(b, t):
    cur = b["shots"][0]
    for s in b["shots"]:
        if s["at"] <= t + 1e-6:
            cur = s
    nxt = [s["at"] for s in b["shots"] if s["at"] > cur["at"]]
    end = cur.get("dur") or ((min(nxt) if nxt else b["dur"]) - cur["at"])
    u = ease((t - cur["at"]) / max(end, 1e-3)) if cur.get("ease", "inout") != "linear" else \
        min(1, (t - cur["at"]) / max(end, 1e-3))
    c = [a + (z - a) * u for a, z in zip(cur["cam"], cur["to"])]
    return c, cur


def set_layer(ctx, cam, depth):
    ctx.identity_matrix()
    z = 1 + (cam[2] - 1) * depth
    ctx.translate(W / 2, H / 2)
    ctx.scale(z, z)
    ref = (540, 960)
    ctx.translate(-(ref[0] + (cam[0] - ref[0]) * depth), -(ref[1] + (cam[1] - ref[1]) * depth))


def world_to_screen(cam, x, y):
    return (x - cam[0]) * cam[2] + W / 2, (y - cam[1]) * cam[2] + H / 2


def blinker(seed, t):
    r = (math.sin(seed * 12.9898) * 43758.5453) % 1
    period = 3.1 + 1.7 * r
    u = (t + r * period) % period
    return 1.0 if u < 0.12 else 0.0


def draw_actor(ctx, cam, a, b, t, words):
    x, y, s, rot, land, walking = track(a.get("pos", (0, 0)), a.get("moves", []), words, t, a.get("s", 1.0),
                                        a.get("rot", 0.0))
    p = dict(a.get("p", {}))
    for st in a.get("set", []):
        t1 = at_time(words, st.get("at"), 0.0)
        if t >= t1:
            u = ease((t - t1) / st["dur"]) if st.get("dur") else 1.0
            for key, v in st["p"].items():
                old = p.get(key, 0.0)
                p[key] = old + (v - old) * u if isinstance(v, (int, float)) and isinstance(old, (int, float)) \
                    and not isinstance(v, bool) else v
    if p.get("hidden"):
        return
    p["blink"] = blinker(hash(a["id"]) % 97, b["t0"] + t)
    p["walking"] = walking
    p["phase"] = (b["t0"] + t) * p.get("pace", 9.0)
    if a.get("talks"):
        p["talk"] = talk_level(words, t)
    set_layer(ctx, cam, a.get("depth", 1.0))
    ctx.translate(x, y)
    if land is not None and land < 0.25:
        q = 1 - land / 0.25
        ctx.scale(1 + 0.18 * q, 1 - 0.18 * q)
    ctx.rotate(math.radians(rot))
    ctx.scale(s * (-1 if a.get("flip") else 1), s)
    ACTORS[a["type"]](ctx, b["t0"] + t, p)


def talk_level(words, t):
    for s, e, _ in words:
        if s <= t <= e:
            return 0.5 + 0.5 * abs(math.sin((t - s) * 22))
    return 0.0


def pil_to_surface(im):
    a = np.asarray(im, dtype=np.uint16)
    al = a[..., 3:4]
    pre = (a[..., :3] * al // 255).astype(np.uint8)
    bgra = np.concatenate([pre[..., ::-1], al.astype(np.uint8)], axis=2).copy()
    surf = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, im.width, im.height,
                                              im.width * 4)
    return surf, bgra


def draw_meatball(ctx, cam, b, st, t):
    mb = b["mb"]
    if mb.get("hidden"):
        return
    words = b["words"]
    x, y, size, rot, land, walking = track(mb["pos"], mb["moves"], words, t, mb["size"])
    st = dict(st)
    if walking:
        st = mascot.apply_run(st, (b["t0"] + t) * 14)
    sh = mb.get("shake") or 0.0
    jx = sh * 10 * math.sin((b["t0"] + t) * 57)
    look = mb.get("look")
    if look == "viewer":
        st["look"] = (0, 0)
    elif look:
        tgt = b["actors"].get(look) if isinstance(look, str) else None
        if tgt is not None:
            tx, ty, *_ = track(tgt.get("pos", (0, 0)), tgt.get("moves", []), words, t)
            ty -= 150 * tgt.get("s", 1.0)
        else:
            tx, ty = look
        dx, dy = tx - x, ty - (y - 600 * size / 1000)
        n = math.hypot(dx, dy) or 1
        st["look"] = (round(10 * dx / n), round(10 * dy / n))
    if mb.get("mute"):
        st["level"] = 0
    if mb.get("float"):
        y += 22 * math.sin((b["t0"] + t) * 2.1)
    fx, fy = world_to_screen(cam, x + jx, y)
    kpx = size * cam[2]
    k = kpx / 1000
    ctx.identity_matrix()
    if not mb.get("float"):  # ground shadow
        p_ellipse(ctx, fx, fy + 4, 150 * k, 26 * k)
        src(ctx, (0, 0, 0), 0.22)
        ctx.fill()
    origin = (fx - 500 * k, fy - 960 * k)
    got = mascot.render(st, kpx, 2 if kpx <= 1500 else 1, origin, (W, H))
    if not got:
        return
    im, (ix, iy) = got
    surf, keep = pil_to_surface(im)
    ctx.save()
    ctx.identity_matrix()
    ctx.translate(fx, fy)
    if land is not None and land < 0.3:
        q = 1 - land / 0.3
        ctx.scale(1 + 0.16 * q * math.cos(land * 20), 1 - 0.16 * q * math.cos(land * 20))
    if rot:
        ctx.rotate(math.radians(rot))
    ctx.translate(-fx, -fy)
    ctx.set_source_surface(surf, ix, iy)
    ctx.paint()
    j = mascot.body(st)
    U = lambda q: (origin[0] + q[0] * k, origin[1] + q[1] * k)  # noqa: E731
    prop = mb.get("prop")
    if prop:
        _, _, hand = mascot.arm_points(j, 1, st["r"])
        hx, hy = U(hand)
        draw_prop(ctx, prop, hx, hy, k, b["t0"] + t)
    if mb.get("helmet"):
        hx, hy = U(j["head"])
        p_ellipse(ctx, hx, hy + 10 * k, 235 * k, 235 * k)
        src(ctx, (0.75, 0.92, 1.0), 0.22)
        ctx.fill_preserve()
        ink(ctx, OUT * 1.4 * k)
        ctx.stroke()
        ctx.new_sub_path()
        ctx.arc(hx, hy + 10 * k, 190 * k, math.radians(200), math.radians(250))
        ctx.set_source_rgba(1, 1, 1, 0.85)
        ctx.set_line_width(16 * k)
        ctx.stroke()
        ctx.rectangle(hx - 150 * k, hy + 225 * k, 300 * k, 40 * k)
        src(ctx, PAL["steel"])
        ctx.fill_preserve()
        ink(ctx, OUT * k)
        ctx.stroke()
    ctx.restore()


def draw_prop(ctx, prop, hx, hy, k, t):
    if prop == "flashlight":
        ctx.save()
        ctx.move_to(hx + 30 * k, hy - 30 * k)
        ctx.line_to(hx + 900 * k, hy - 330 * k)
        ctx.line_to(hx + 900 * k, hy + 230 * k)
        ctx.close_path()
        src(ctx, PAL["light"], 0.22 + 0.03 * math.sin(t * 9))
        ctx.fill()
        ctx.translate(hx, hy)
        ctx.rotate(-0.12)
        ctx.rectangle(-50 * k, -22 * k, 100 * k, 44 * k)
        src(ctx, PAL["steel_dk"])
        ctx.fill_preserve()
        ink(ctx, OUT * k)
        ctx.stroke()
        ctx.rectangle(40 * k, -32 * k, 34 * k, 64 * k)
        src(ctx, PAL["steel"])
        ctx.fill_preserve()
        ctx.stroke()
        ctx.restore()
    elif prop == "mic":
        ctx.save()
        ctx.translate(hx, hy)
        ctx.rotate(-0.5)
        ctx.rectangle(-12 * k, -10 * k, 24 * k, 140 * k)
        src(ctx, INK)
        ctx.fill()
        p_ellipse(ctx, 0, -40 * k, 36 * k, 42 * k)
        src(ctx, PAL["steel"])
        ctx.fill_preserve()
        ink(ctx, OUT * k)
        ctx.stroke()
        ctx.restore()
    elif prop == "paper":
        ctx.save()
        ctx.translate(hx, hy)
        ctx.rotate(0.15)
        ctx.rectangle(-20 * k, -150 * k, 150 * k, 190 * k)
        src(ctx, PAL["paper"])
        ctx.fill_preserve()
        ink(ctx, OUT * 0.8 * k)
        ctx.stroke()
        for r in range(5):
            stroke(ctx, [(0, (-120 + r * 30) * k), (110 * k, (-120 + r * 30) * k)], 8 * k,
                   color=INK if r != 2 else PAL["suit"])
        ctx.restore()


# ---------------------------------------------------------------- captions (spoken-word, 1-3 words)

def caption_chunks(beats):
    out = []
    for b in beats:
        toks = b["say"].split()
        ws, k = [], 0
        for s0, e0, w0 in b["words"]:   # edge-tts drops punctuation: take each word's spelling from the line
            key = "".join(ch for ch in w0.lower() if ch.isalnum())
            for j in range(k, min(k + 3, len(toks))):
                if "".join(ch for ch in toks[j].lower() if ch.isalnum()).startswith(key[:3]):
                    w0, k = toks[j], j + 1
                    break
            ws.append((s0, e0, w0))
        i = 0
        while i < len(ws):
            group = [ws[i]]
            while (len(group) < 3 and i + len(group) < len(ws)
                   and not group[-1][2].endswith((",", ".", "?", "!"))
                   and len(" ".join(g[2] for g in group + [ws[i + len(group)]])) <= 15):
                group.append(ws[i + len(group)])
            s = b["t0"] + group[0][0]
            e = b["t0"] + (ws[i + len(group)][0] if i + len(group) < len(ws) else group[-1][1] + 0.15)
            out.append((s, e, " ".join(g[2] for g in group).upper().rstrip(",.")))
            i += len(group)
    return out


_CAP = {}


def caption_img(text, px):
    if (text, px) not in _CAP:
        f = ImageFont.truetype(FONT, px)
        sw = max(5, px // 11)
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=sw)
        im = Image.new("RGBA", (x1 - x0 + 8, y1 - y0 + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - x0, 4 - y0), text, font=f, fill=(255, 255, 255, 255), stroke_width=sw,
                                stroke_fill=(17, 17, 17, 255))
        _CAP[(text, px)] = im
    return _CAP[(text, px)]


# ---------------------------------------------------------------- the render loop

G = {}


def frame_at(f):
    fps, beats, rigs = G["fps"], G["beats"], G["rigs"]
    T = f / fps
    bi = max(i for i, b in enumerate(beats) if b["t0"] <= T + 1e-9)
    b = beats[bi]
    t = T - b["t0"]
    rf = min(int(round(t * fps)), len(rigs[bi]) - 1)
    cam, shot = cam_at(b, t)
    cam = list(cam)
    for hit in b.get("shake", []):
        u = t - at_time(b["words"], hit)
        if 0 <= u < 0.35:
            cam[0] += 22 * math.sin(u * 70) * (1 - u / 0.35)
            cam[1] += 14 * math.cos(u * 61) * (1 - u / 0.35)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    SCENES[b["scene"]](ctx, T, lambda d: set_layer(ctx, cam, d), b["scene_p"])
    behind = [a for a in b["actors"].values() if not a.get("front")]
    front = [a for a in b["actors"].values() if a.get("front")]
    for a in behind:
        ctx.save()
        draw_actor(ctx, cam, a, b, t, b["words"])
        ctx.restore()
    ctx.identity_matrix()
    draw_meatball(ctx, cam, b, rigs[bi][rf], t)
    for a in front:
        ctx.save()
        draw_actor(ctx, cam, a, b, t, b["words"])
        ctx.restore()
    ctx.identity_matrix()
    for fl in b.get("flash", []):
        u = t - at_time(b["words"], fl)
        if 0 <= u < 0.2:
            ctx.rectangle(0, 0, W, H)
            ctx.set_source_rgba(1, 1, 1, 0.55 * (1 - u / 0.2))
            ctx.fill()
    tint = b.get("tint")
    if tint:
        ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(*tint)
        ctx.fill()
    surf.flush()
    base = np.ndarray((H, W, 4), np.uint8, surf.get_data()).copy()
    outs = [base]
    if G.get("cap_px"):
        cap = base.copy()
        for s, e, text in G["caps"]:
            if s <= T < e:
                im = caption_img(text, G["cap_px"])
                arr = np.asarray(im).astype(np.float32)
                x0 = (W - im.width) // 2
                y0 = int(G.get("cap_y", 1530)) - im.height // 2
                reg = cap[y0:y0 + im.height, x0:x0 + im.width].astype(np.float32)
                al = arr[..., 3:4] / 255
                rgb_bgr = arr[..., [2, 1, 0]]
                reg[..., :3] = reg[..., :3] * (1 - al) + rgb_bgr * al
                cap[y0:y0 + im.height, x0:x0 + im.width] = reg.astype(np.uint8)
                break
        outs.append(cap)
    return [o.tobytes() for o in outs]


def mix_audio(spec, beats, total, path):
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    sfx = np.zeros(n, np.float32)
    for b in beats:
        a = b["audio"]
        o = int(b["t0"] * SR)
        voice[o:o + len(a)] += a[:max(0, n - o)]
        for e in b.get("sfx", []):
            name, _, at = e.partition("@")
            num = at.replace(".", "", 1).isdigit()
            t = b["t0"] + at_time(b["words"], float(at) if num else (at or 0.0))
            with wave.open(os.path.join(ROOT, "sfx", name + ".wav")) as w:
                raw = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
                if w.getnchannels() == 2:
                    raw = raw.reshape(-1, 2).mean(1)
                if w.getframerate() != SR:
                    idx = np.arange(0, len(raw), w.getframerate() / SR)
                    raw = np.interp(idx, np.arange(len(raw)), raw).astype(np.float32)
            o = int(t * SR)
            sfx[o:o + len(raw)] += raw[:max(0, n - o)] * spec.get("sfx_gain", 0.45)
    bed = music.render(spec.get("music", "detective"), total)
    bed = bed.mean(1) if bed.ndim == 2 else bed
    g = 10 ** (spec.get("music_db", -21) / 20)
    mus = np.zeros(n, np.float32)
    mus[:len(bed)] = bed[:n] * g / (np.sqrt(np.mean(bed ** 2)) + 1e-9) * 0.1
    mix = voice + sfx + mus
    mix = mix[:int(total * SR)]
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())


def encode_cmd(out, fps, wav):
    return ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(fps),
            "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
            "-crf", os.environ.get("CRF", "21"), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-shortest", "-movflags", "+faststart", out]


def main():
    import argparse
    import multiprocessing as mp
    import time
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--nocap")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--stills", help="write PNG stills at these comma-separated seconds and stop")
    ap.add_argument("--work")
    args = ap.parse_args()
    spec = json.load(open(args.spec))
    work = args.work or os.path.join(os.path.dirname(os.path.abspath(args.out)), ".work-" +
                                     os.path.splitext(os.path.basename(args.out))[0])
    os.makedirs(work, exist_ok=True)
    t_start = time.time()
    beats, total = plan(spec, work)
    G.update(fps=args.fps, beats=beats, rigs=rig_tracks(beats, args.fps), caps=caption_chunks(beats),
             cap_px=spec.get("captions", 66), cap_y=spec.get("caption_y", 1530))
    nf = int(total * args.fps)
    print(f"plan: {len(beats)} beats, {total:.2f} s, {nf} frames", flush=True)
    if args.stills:
        G["cap_px"] = spec.get("captions", 66)
        for s in args.stills.split(","):
            outs = frame_at(int(float(s) * args.fps))
            arr = np.frombuffer(outs[-1], np.uint8).reshape(H, W, 4)
            Image.fromarray(arr[..., [2, 1, 0]]).save(f"{work}/still-{float(s):05.1f}.png")
        print("stills in", work)
        return
    wav = f"{work}/mix.wav"
    mix_audio(spec, beats, total, wav)
    procs = [subprocess.Popen(encode_cmd(args.out, args.fps, wav), stdin=subprocess.PIPE)]
    if args.nocap:
        procs.append(subprocess.Popen(encode_cmd(args.nocap, args.fps, wav), stdin=subprocess.PIPE))
    else:
        G["cap_px"] = None if not spec.get("captions", 66) else G["cap_px"]
    with mp.get_context("fork").Pool(int(os.environ.get("DRAWN_JOBS", "4"))) as pool:
        for k, outs in enumerate(pool.imap(frame_at, range(nf), chunksize=4)):
            # outs[0] = no captions, outs[-1] = captioned
            procs[0].stdin.write(outs[-1])
            if args.nocap:
                procs[1].stdin.write(outs[0])
            if k % 150 == 0:
                print(f"  frame {k}/{nf}  {time.time() - t_start:.0f}s", flush=True)
    for p in procs:
        p.stdin.close()
        p.wait()
    print(f"done {args.out} in {time.time() - t_start:.0f}s", flush=True)


if __name__ == "__main__":
    main()
