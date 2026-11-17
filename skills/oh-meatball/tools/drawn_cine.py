"""Cinematic pass for tools/drawn.py (Studio 11/17 "not AI slop" brief): camera on every line, a live bug, light
and dark, a small shot library, Meatball acting, the BUG ID card and sound hits on every cut.

On by default for macro specs (beats with "m"); spec "cine": false turns it off, a dict tunes it:
  "cine": {"push": 0.07, "punch": 0.17, "drift": 1.0, "light": "auto" | "off", "dark": 0.68,
           "shots": "auto" | "off", "transitions": true, "skitter": true, "music_drop": true}
Beat keys (macro lines pass them through):
  insert      {"type": "bugcam" | "seccam" | "sizecheck", "at": "35%", "dur": 1.1} (or a list): a shot from the
              library replaces the picture for that window (the voice and captions run on)
                bugcam     macro close-up of the bug's head inside a magnifying-glass ring, "BUG CAM" label
                seccam     night-vision security-cam angle: green grade, noise, scanlines, REC, timestamp
                sizecheck  the bug on the floor next to a coin, drawn to its real body-to-coin proportion
                           (body ~1.35 coin widths: 25-38 mm adult body vs a 24 mm coin); no numbers shown
  punch       ["word", ...] fast punch-ins (default: one picked from the line's key words); false = none
  scare       a word / time: 5-frame shake, eye-pop burst, a music drop right before it, a hit on it
              (the calm macro sets it at 65 %, escalate at 55 %)
  light       "flashlight" (dark room, one cone on the bug) | "lamp" (dim room, light pools on the two
              characters) | "off"; default: hook = flashlight, night scenes = lamp
  enter       {"from": "drain", "at": "55%", "x": 840, "y": 1560, "dur": 0.3}: the bug is down the drain (its
              antennae feel around the grate) and bursts up out of it
  transition  "whip" | "smash" | "cut" into this line (default: alternate whip / smash; scare lines smash)
Spec key:
  id_card     {"name": "HOUSE CENTIPEDE", "rows": ["15 PAIRS OF LEGS", ...], "beat": 5, "at": "10%", "dur": 2.4,
              "type": actor type for the icon (default the stage actor)}: the same card design every episode.
              Rows must be words already in the script.
"""
import math

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from drawn_kit import INK, OUT, PAL, ease, ink, p_ellipse, src, stroke

D = None   # the drawn module (bound by drawn.main)
CFG = {}
W, H = 1080, 1920
DEFAULTS = {"push": 0.07, "punch": 0.17, "drift": 1.0, "light": "auto", "dark": 0.68, "shots": "auto",
            "transitions": True, "skitter": True, "music_drop": True}
POSE_ROT = ["nervous", "think", "point", "shock", "shrug", "deadpan", "laugh"]
KEYWORDS = {"bite", "squish", "hunting", "fastest", "fifteen", "nope", "bed", "thirty", "run", "silverfish",
            "spiders", "flies", "all", "chase", "legs"}


def setup(module, spec):
    """Bind to drawn and read the spec's "cine" key; returns the config or None (off)."""
    global D
    D = module
    c = spec.get("cine", any("_m" in b for b in spec.get("beats", [])))
    if not c:
        CFG.clear()
        return None
    CFG.clear()
    CFG.update(DEFAULTS, **(c if isinstance(c, dict) else {}))
    CFG["id_card"] = spec.get("id_card")
    CFG["stage_type"] = (spec.get("stage") or {}).get("actor") or ("sp." + str((spec.get("stage") or {}).get("creature")))
    return CFG


def _t(b, at, default=0.0):
    return D.at_time(b["words"], at, default)


def _hero(b):
    a = b["actors"].get("hero") if isinstance(b["actors"], dict) else None
    return a


def hero_at(b, t):
    """(x, y, s, face) of the hero in world px, or None."""
    a = _hero(b)
    if a is None:
        return None
    x, y, s, _, _, _ = D.track(a.get("pos", (0, 0)), a.get("moves", []), b["words"], t, a.get("s", 1.0), a.get("rot", 0.0))
    face = -1 if a.get("flip") else 1
    for m in a.get("moves", []):
        if "face" in m and t >= _t(b, m.get("at")):
            face = m["face"]
    return x, y, s, face


def mb_at(b, t):
    mb = b["mb"]
    if mb.get("hidden"):
        return None
    x, y, size, _, _, _ = D.track(mb["pos"], mb["moves"], b["words"], t, mb["size"])
    return x, y, size


# ---------------------------------------------------------------- plan pass

def plan_pass(spec, beats):
    """Resolve the per-line cine marks (times in seconds) and add the cine sound cues. Runs after drawn.plan."""
    if not CFG:
        return
    cues = []
    prev_pose = None
    last_ins = None
    for i, b in enumerate(beats):
        m = b.get("_m")
        # light
        lt = b.get("light")
        if lt is None:
            if CFG["light"] == "off":
                lt = "off"
            elif m == "hook":
                lt = "flashlight"
            else:
                night = (b.get("scene_p") or {}).get("time") == "night" or b["scene"] in ("bathroom", "basement")
                lt = "lamp" if night else "off"
        b["_light"] = lt
        # scare
        b["_scare"] = [_t(b, b["scare"])] if b.get("scare") is not None else []
        # punch-ins
        pk = b.get("punch")
        pts = []
        if pk is not False:
            if pk:
                pts = [_t(b, w) for w in pk]
            elif CFG["punch"]:
                for s0, e0, w in b["words"]:
                    k = "".join(ch for ch in w.lower() if ch.isalnum())
                    if k in KEYWORDS and s0 > 0.25 and all(abs(s0 - s) > 0.6 for s in b["_scare"]):
                        pts = [s0]
                        break
        b["_punch"] = pts
        for p_ in pts:
            cues.append((b["t0"] + p_, "thud"))
        # transition
        tr = b.get("transition")
        if tr is None:
            tr = "cut" if i == 0 or not CFG["transitions"] else ("smash" if (b["_scare"] or i % 2 == 0) else "whip")
        b["_tr"] = tr
        b["_dir"] = 1 if i % 4 in (1, 2) else -1
        if i:
            cues.append((max(0.0, b["t0"] - 0.06), "whoosh" if tr == "whip" else "hit"))
        for s in b["_scare"]:
            cues.append((b["t0"] + s, "sting" if m != "escalate" else "hit"))
        # inserts
        ins = b.get("insert")
        if ins is None and CFG["shots"] == "auto" and _hero(b) is not None and b["dur"] > 2.6 and not b.get("card") \
                and m not in ("hook", "calm", "escalate"):
            rot = ["bugcam", "seccam", "sizecheck"]
            kind = rot[(rot.index(last_ins) + 1) % 3] if last_ins in rot else "bugcam"
            ins = {"type": kind, "at": "40%", "dur": 1.1}
        b["_ins"] = []
        for x in ([ins] if isinstance(ins, dict) else (ins or [])):
            a = _t(b, x.get("at", "40%"))
            b["_ins"].append(dict(x, _a=a, _z=min(b["dur"], a + x.get("dur", 1.1))))
            last_ins = x["type"]
            cues.append((b["t0"] + a, "whoosh"))
        # the drain entrance
        en = b.get("enter")
        hero = _hero(b)
        if en and hero is not None:
            ex, ey = en.get("x", 840), en.get("y", 1560)
            a = _t(b, en.get("at", "55%"))
            hero["pos"] = [ex, ey]
            hero["moves"] = [mv for mv in hero.get("moves", []) if _t(b, mv.get("at")) >= a]
            b["_enter"] = dict(en, _a=a, _d=en.get("dur", 0.3), x=ex, y=ey)
            cues.append((b["t0"] + a, "scratch"))
        # skitter: a scratch whenever the bug moves (one per move start, the cue list keeps them apart)
        if CFG["skitter"] and hero is not None:
            px, py = hero.get("pos", (0, 0))
            n = 0
            for mv in hero.get("moves", []):
                if "pos" in mv and math.hypot(mv["pos"][0] - px, mv["pos"][1] - py) > 40 and n < 2:
                    cues.append((b["t0"] + _t(b, mv.get("at")), "scratch"))
                    n += 1
                if "pos" in mv:
                    px, py = mv["pos"]
        # Meatball never holds the same pose two lines running
        mb = b["mb"]
        import mascot
        if mb.get("pose") and mb["pose"] not in mascot.POSES:   # e.g. "scared": the rig would fall back to neutral
            mb["pose"] = {"scared": "nervous"}.get(mb["pose"], "shock")
        if not mb.get("hidden"):
            if mb.get("pose") == prev_pose:
                mb["pose"] = next(p for p in POSE_ROT[i % len(POSE_ROT):] + POSE_ROT if p != prev_pose)
            prev_pose = mb.get("pose")
    spec["_cine_cues"] = cues
    spec["_cine_scares"] = [b["t0"] + s for b in beats for s in b["_scare"]]


# ---------------------------------------------------------------- camera

def insert_at(b, t):
    for x in b.get("_ins", []):
        if x["_a"] <= t < x["_z"]:
            return x
    return None


def _noise(seed):
    return (math.sin(seed * 12.9898) * 43758.5453) % 1 - 0.5


def camera(b, t, T, cam, ins):
    """The base camera plus the cine moves. Returns (cam, whip shift px for the blur)."""
    x, y, z = cam
    whip = 0.0
    if ins is not None:
        k = ins["type"]
        h = hero_at(b, t)
        u = (t - ins["_a"]) / max(0.05, ins["_z"] - ins["_a"])
        if k == "bugcam" and h:
            hx, hy, s, face = h
            x, y, z = hx + face * 150 * s, hy - 110 * s, 3.0 + 0.35 * u
        elif k == "seccam":
            x, y, z = (h[0] if h else 540) - 60, (h[1] if h else 1500) - 380, 1.0
            return [x, y, z], 0.0   # a security cam does not move
        else:
            return [x, y, z], 0.0
    else:
        u = t / max(b["dur"], 1e-3)
        z *= 1 + CFG["push"] * ease(u)                     # slow push-in, every line
        for p_ in b.get("_punch", []):                     # fast punch-in on the key word
            v = t - p_
            if 0 <= v < 0.75:
                e = min(1.0, v / 0.07) if v < 0.07 else (1.0 if v < 0.4 else 1 - ease((v - 0.4) / 0.35))
                z *= 1 + CFG["punch"] * e
    h = hero_at(b, t) if ins is None else None             # keep the bug on frame and above the captions
    if h is not None and not b.get("_enter") or (h is not None and t >= b["_enter"]["_a"]):
        sx, sy = D.world_to_screen([x, y, z], h[0], h[1] - 110 * h[2])
        dx = min(0.0, 930 - sx) + max(0.0, 150 - sx)
        dy = min(0.0, 1330 - sy) + max(0.0, 520 - sy)
        x, y = x - dx / z, y - dy / z
    dr = CFG["drift"]                                       # handheld drift: nothing is ever still
    x += dr * (7 * math.sin(T * 1.3) + 3 * math.sin(T * 3.1)) / max(z, 0.5)
    y += dr * (5 * math.sin(T * 1.7 + 1)) / max(z, 0.5)
    for s in b.get("_scare", []):                          # 5-frame scare shake
        v = t - s
        if 0 <= v < 5 / 30:
            f = int(v * 30)
            x += 34 * _noise(f + 3.1 * b["i"]) * 2 / z
            y += 26 * _noise(f + 7.7) * 2 / z
            z *= 1.06
    tr = b.get("_tr")
    if tr == "whip" and t < 0.2:
        q = (1 - t / 0.2) ** 2
        x += b["_dir"] * 520 * q / z
        whip = b["_dir"] * 90 * q
    elif tr == "smash" and t < 0.15:
        z *= 1 + 0.12 * (1 - ease(t / 0.15))
    return [x, y, z], whip


# ---------------------------------------------------------------- the bug: shadow, smear, speed lines, drain

def actor_extras(ctx, cam, a, b, t, draw_core):
    """Wraps drawn.draw_actor for the hero: ground shadow, ghost smear and speed lines when it scuttles, and the
    drain entrance. Returns True when it drew the actor itself."""
    if not CFG or a.get("id") != "hero":
        return False
    words = b["words"]
    x, y, s, _, _, _ = D.track(a.get("pos", (0, 0)), a.get("moves", []), words, t, a.get("s", 1.0), a.get("rot", 0.0))
    x0, y0, *_ = D.track(a.get("pos", (0, 0)), a.get("moves", []), words, max(0.0, t - 1 / 30), a.get("s", 1.0))
    speed = math.hypot(x - x0, y - y0) * 30
    en = b.get("_enter")
    rise = None
    if en:
        v = t - en["_a"]
        if v < 0:   # down the drain: only the antennae feel around the grate
            D.set_layer(ctx, cam, 1.0)
            for k in (-1, 1):
                w = math.sin(b["t0"] + t * 7 + k) * 25
                stroke(ctx, [(en["x"] + k * 18, en["y"] - 4), (en["x"] + k * 40 + w, en["y"] - 90),
                             (en["x"] + k * 90 + w * 1.6, en["y"] - 150)], 4, smooth=True)
            return True
        rise = min(1.0, v / en["_d"])
    D.set_layer(ctx, cam, a.get("depth", 1.0))
    if rise is None or rise >= 1:   # ground shadow
        p_ellipse(ctx, x, y + 6, 360 * s, 34 * s)
        src(ctx, (0, 0, 0), 0.28)
        ctx.fill()
    if speed > 260 and rise is None:   # speed lines + smear (ghost frames behind it)
        d = 1 if x > x0 else -1
        ctx.save()
        for k in range(5):
            yy = y - 40 * s - k * 45 * s
            ln = min(420, speed * 0.35) * (0.6 + 0.4 * ((k * 37) % 5) / 5)
            stroke(ctx, [(x - d * 330 * s, yy), (x - d * (330 * s + ln), yy)], 5, color=(1, 1, 1), a=0.65)
        ctx.restore()
        for k, al in ((3, 0.12), (2, 0.2), (1, 0.3)):
            ctx.save()
            ctx.push_group()
            draw_core(ctx, cam, a, b, max(0.0, t - k * 0.03), words)
            ctx.pop_group_to_source()
            ctx.identity_matrix()
            ctx.paint_with_alpha(al)
            ctx.restore()
    if rise is not None and rise < 1:   # bursting up out of the drain, clipped at the floor
        D.set_layer(ctx, cam, 1.0)
        p_ellipse(ctx, en["x"], en["y"], 90, 24)
        src(ctx, (0.04, 0.04, 0.05))
        ctx.fill()
        ctx.identity_matrix()
        _, fy = D.world_to_screen(cam, 0, en["y"])
        ctx.save()
        ctx.rectangle(0, 0, W, fy)
        ctx.clip()
        ctx.push_group()
        draw_core(ctx, cam, a, b, t, words)
        pat = ctx.pop_group()
        ctx.identity_matrix()
        pat.set_matrix(cairo.Matrix(x0=0, y0=-380 * s * (1 - ease(rise)) * cam[2]))
        ctx.set_source(pat)
        ctx.paint()
        ctx.restore()
        return True
    ctx.save()
    draw_core(ctx, cam, a, b, t, words)
    ctx.restore()
    return True


# ---------------------------------------------------------------- Meatball acting

def mb_transform(ctx, b, t, fx, fy, k):
    """Idle breathing, anticipation crouch before a hop, stretch on the way up. Called about his feet."""
    if not CFG:
        return
    br = math.sin((b["t0"] + t) * 2 * math.pi * 0.7)
    sx, sy = 1 - 0.012 * br, 1 + 0.022 * br
    for m in b["mb"].get("moves", []):
        if not m.get("hop"):
            continue
        a = _t(b, m.get("at"))
        d = m.get("dur", 0.5)
        if a - 0.14 <= t < a:
            q = math.sin(math.pi * (t - (a - 0.14)) / 0.14 * 0.5)
            sx, sy = sx * (1 + 0.15 * q), sy * (1 - 0.15 * q)
        elif a <= t < a + 0.4 * d:
            q = 1 - (t - a) / (0.4 * d)
            sx, sy = sx * (1 - 0.08 * q), sy * (1 + 0.12 * q)
    ctx.translate(fx, fy)
    ctx.scale(sx, sy)
    ctx.translate(-fx, -fy)


def mb_overlay(ctx, b, t, head, k):
    """Eye-pop burst on the scare / reveal, a sweat drop on the nervous lines."""
    if not CFG:
        return
    hx, hy = head
    pops = list(b.get("_scare", []))
    if b.get("_m") == "hook" and b["mb"].get("moves"):
        pops.append(_t(b, b["mb"]["moves"][0].get("at")) + 0.35)
    for s in pops:
        v = t - s
        if 0 <= v < 0.45:
            q = ease(min(1.0, v / 0.12))
            ctx.save()
            ink(ctx, 14 * k)
            for j in range(9):
                ang = math.radians(-170 + j * 20)
                r0, r1 = 290 * k * (0.9 + 0.2 * q), 290 * k * (1.0 + 0.45 * q)
                ctx.move_to(hx + r0 * math.cos(ang), hy + r0 * math.sin(ang))
                ctx.line_to(hx + r1 * math.cos(ang), hy + r1 * math.sin(ang))
            ctx.stroke()
            ctx.restore()
    if b["mb"].get("pose") in ("nervous", "scared") or b.get("_scare"):
        v = ((b["t0"] + t) * 0.9) % 1.0
        dx, dy = hx + 230 * k, hy - 120 * k + 160 * k * v
        ctx.save()
        ctx.move_to(dx, dy - 40 * k)
        ctx.curve_to(dx + 26 * k, dy, dx + 26 * k, dy + 30 * k, dx, dy + 30 * k)
        ctx.curve_to(dx - 26 * k, dy + 30 * k, dx - 26 * k, dy, dx, dy - 40 * k)
        src(ctx, (0.55, 0.82, 1.0), 1 - v * 0.6)
        ctx.fill_preserve()
        ink(ctx, 7 * k, 1 - v * 0.6)
        ctx.stroke()
        ctx.restore()


# ---------------------------------------------------------------- light

def light(ctx, b, t, T, cam, hand=None):
    """Darken the room and cut light into it: a flashlight cone on the bug, or lamp pools on the two characters."""
    lt = b.get("_light", "off")
    if not CFG or lt == "off":
        return
    h = hero_at(b, t)
    hs = D.world_to_screen(cam, h[0], h[1] - 110 * h[2]) if h else (W * 0.6, H * 0.6)
    ctx.identity_matrix()
    dark = CFG["dark"]
    ctx.push_group()
    if lt == "flashlight":
        frame = int(round(T * 30))
        on = frame >= 1                             # frame 0: the dark room; frame 1: the cone hits the bug
        flick = 1.0 if frame > 3 else (0.0 if not on else (0.6 if frame == 2 else 1.0))
        ctx.set_source_rgba(0.01, 0.015, 0.05, 0.86)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_DEST_OUT)
        sx, sy = hand if hand else (-160 + 30 * math.sin(T * 1.1), H + 140)
        tx, ty = hs[0] + 30 * math.sin(T * 1.9), hs[1] + 20 * math.sin(T * 1.3)
        ang = math.atan2(ty - sy, tx - sx)
        dist = math.hypot(tx - sx, ty - sy)
        nx, ny = -math.sin(ang), math.cos(ang)
        for wk, al in ((1.5, 0.22), (1.15, 0.3), (0.85, 0.4), (0.6, 0.5)):
            w = 190 * wk
            far = dist + 500
            ex, ey = sx + far * math.cos(ang), sy + far * math.sin(ang)
            ctx.move_to(sx, sy)
            ctx.line_to(ex + nx * w * far / dist, ey + ny * w * far / dist)
            ctx.line_to(ex - nx * w * far / dist, ey - ny * w * far / dist)
            ctx.close_path()
            ctx.set_source_rgba(0, 0, 0, al * flick)
            ctx.fill()
        g = cairo.RadialGradient(tx, ty, 0, tx, ty, 380)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.9 * flick)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.pop_group_to_source()
        ctx.paint()
        if flick:   # warm beam
            ctx.move_to(sx, sy)
            w = 190 * 1.15
            far = dist + 500
            ex, ey = sx + far * math.cos(ang), sy + far * math.sin(ang)
            ctx.line_to(ex + nx * w * far / dist, ey + ny * w * far / dist)
            ctx.line_to(ex - nx * w * far / dist, ey - ny * w * far / dist)
            ctx.close_path()
            ctx.set_source_rgba(1.0, 0.94, 0.7, 0.10 * flick)
            ctx.fill()
        return
    # lamp: a dim room with soft pools on the bug and on Meatball
    ctx.set_source_rgba(0.02, 0.03, 0.09, dark)
    ctx.paint()
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)
    pools = [(hs[0], hs[1], 520 * min(1.6, cam[2]))]
    m = mb_at(b, t)
    if m:
        mx, my = D.world_to_screen(cam, m[0], m[1] - 0.45 * m[2])
        pools.append((mx, my, 0.75 * m[2] * cam[2] + 120))
    for px, py, r in pools:
        g = cairo.RadialGradient(px, py, 0, px, py, r)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
        g.add_color_stop_rgba(0.55, 0, 0, 0, 0.6)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g)
        ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()
    g = cairo.RadialGradient(hs[0], hs[1] - 300, 0, hs[0], hs[1] - 300, 700)   # warm lamp spill from above
    g.add_color_stop_rgba(0, 1.0, 0.85, 0.55, 0.10)
    g.add_color_stop_rgba(1, 1.0, 0.85, 0.55, 0.0)
    ctx.set_source(g)
    ctx.paint()


# ---------------------------------------------------------------- shot library: draw-time pieces

def draw_sizecheck(ctx, b, t, T):
    """The bug on a floor tile next to a coin. Body : coin = 1.35 : 1 (adult body 25-38 mm; a coin ~24 mm)."""
    ctx.identity_matrix()
    ctx.rectangle(0, 0, W, H)
    src(ctx, (0.80, 0.82, 0.84))
    ctx.fill()
    ink(ctx, 4, 0.25)
    for gx in range(-200, W + 400, 360):
        ctx.move_to(gx, 0)
        ctx.line_to(gx - 200, H)
    for gy in range(200, H, 360):
        ctx.move_to(0, gy)
        ctx.line_to(W, gy + 60)
    ctx.stroke()
    D_coin = 300
    cx, cy = 250, 1260
    p_ellipse(ctx, cx + 10, cy + 16, D_coin / 2, D_coin / 2 * 0.92)
    src(ctx, (0, 0, 0), 0.25)
    ctx.fill()
    p_ellipse(ctx, cx, cy, D_coin / 2, D_coin / 2 * 0.92)
    src(ctx, PAL["steel"])
    ctx.fill_preserve()
    ink(ctx, OUT)
    ctx.stroke()
    p_ellipse(ctx, cx, cy, D_coin / 2 - 22, D_coin / 2 * 0.92 - 22)
    ink(ctx, 4, 0.5)
    ctx.stroke()
    for j in range(5):   # a plain star stamp (no real coin design)
        a0 = math.radians(-90 + j * 144)
        (ctx.move_to if j == 0 else ctx.line_to)(cx + 60 * math.cos(a0), cy + 55 * math.sin(a0))
    ctx.close_path()
    src(ctx, PAL["steel_dk"])
    ctx.fill()
    p_ellipse(ctx, cx - 50, cy - 60, 40, 18, -0.5)
    src(ctx, (1, 1, 1), 0.5)
    ctx.fill()
    a = _hero(b) or {"type": CFG["stage_type"], "id": "hero"}
    body = 350.0                                   # house_centipede body length in actor units
    s = 1.35 * D_coin / body
    bx = 690 + 25 * math.sin(T * 2.2)
    by = cy + 120
    ctx.save()
    p_ellipse(ctx, bx, by + 6, 360 * s, 30 * s)
    src(ctx, (0, 0, 0), 0.25)
    ctx.fill()
    ctx.translate(bx, by)
    ctx.scale(-s, s)
    D.ACTORS[a["type"]](ctx, b["t0"] + t, {"walk": 1.0, "walking": True, "look": [1, 0]})
    ctx.restore()


def bugcam_overlay(arr, ctx, surf, T):
    """Inside a magnifying glass: dark outside a circle, a steel ring, a glint."""
    cx, cy, r = 540, 900, 470
    m = _mask("bugcam", lambda yy, xx: np.clip((np.hypot(xx - cx, yy - cy) - r) / 18, 0, 1) * 0.9)
    arr[..., :3] = (arr[..., :3] * (1 - m[..., None])).astype(np.uint8)
    surf.mark_dirty()
    ctx.identity_matrix()
    ctx.arc(cx, cy, r + 10, 0, 2 * math.pi)
    src(ctx, PAL["steel_dk"])
    ctx.set_line_width(46)
    ctx.stroke()
    ctx.arc(cx, cy, r + 10, 0, 2 * math.pi)
    ink(ctx, 8)
    ctx.set_line_width(8)
    ctx.stroke()
    ctx.arc(cx, cy, r - 40, math.radians(200), math.radians(245))
    ctx.set_source_rgba(1, 1, 1, 0.45)
    ctx.set_line_width(22)
    ctx.stroke()
    ctx.save()   # handle
    ctx.translate(cx + (r + 10) * 0.7, cy + (r + 10) * 0.7)
    ctx.rotate(math.radians(45))
    ctx.rectangle(0, -34, 300, 68)
    src(ctx, PAL["wood_dk"])
    ctx.fill_preserve()
    ink(ctx, OUT)
    ctx.stroke()
    ctx.restore()
    surf.flush()
    D.paste(arr, label("BUG CAM", 64, (255, 211, 77)), cx - 150, cy + r + 90)


_MASK = {}


def _mask(name, fn):
    if name not in _MASK:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _MASK[name] = fn(yy, xx).astype(np.float32)
    return _MASK[name]


def seccam_post(arr, T):
    """Night-vision security cam: green luminance, noise, scanlines, vignette, REC and a running timestamp."""
    f = arr[..., :3].astype(np.float32)
    lum = (0.11 * f[..., 0] + 0.59 * f[..., 1] + 0.30 * f[..., 2])
    lum = 255 * (lum / 255) ** 0.7
    rng = np.random.default_rng(int(T * 30))
    lum = lum + rng.normal(0, 14, lum.shape[:1] + (1,)).astype(np.float32) * 0.4 \
        + rng.normal(0, 16, lum.shape).astype(np.float32)
    vig = _mask("vig", lambda yy, xx: 1 - 0.55 * np.clip((np.hypot((xx - 540) / 540, (yy - 960) / 960) - 0.45) / 0.75, 0, 1))
    scan = _mask("scan", lambda yy, xx: np.where((yy.astype(np.int32) // 3) % 2 == 0, 1.0, 0.82))
    lum = lum * vig * scan
    arr[..., 0] = np.clip(lum * 0.30, 0, 255).astype(np.uint8)
    arr[..., 1] = np.clip(lum * 1.00 + 10, 0, 255).astype(np.uint8)
    arr[..., 2] = np.clip(lum * 0.45, 0, 255).astype(np.uint8)
    sec = 3 * 3600 + 14 * 60 + 7 + int(T)
    stamp = "11-17  %02d:%02d:%02d AM" % (sec // 3600, sec // 60 % 60, sec % 60)
    D.paste(arr, label(stamp, 50, (220, 255, 220), plate=False), 250, 320)
    D.paste(arr, label("CAM 2", 56, (220, 255, 220), plate=False), 140, 240)
    if int(T * 2) % 2 == 0:
        D.paste(arr, label("● REC", 56, (255, 70, 70), plate=False), 920, 240)


_LBL = {}


def label(text, px, color, plate=True):
    key = (text, px, color, plate)
    if key not in _LBL:
        try:
            f = ImageFont.truetype(D.FONT, px)
        except OSError:
            f = ImageFont.load_default()
        if "●" in text:
            f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", px) \
                if __import__("os").path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else f
            text = text.replace("●", "")
            dot = True
        else:
            dot, f2 = False, f
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=5)
        pad = 26 if plate else 6
        extra = px if dot else 0
        im = Image.new("RGBA", (x1 - x0 + 2 * pad + extra, y1 - y0 + 2 * pad), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        if plate:
            dr.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=im.height // 2, fill=(18, 22, 40, 230),
                                 outline=(255, 255, 255, 255), width=4)
        if dot:
            r = px // 3
            dr.ellipse((pad, im.height // 2 - r, pad + 2 * r, im.height // 2 + r), fill=color + (255,))
        dr.text((pad + extra - x0, pad - y0), text, font=f, fill=color + (255,), stroke_width=0 if plate else 4,
                stroke_fill=(0, 0, 0, 255))
        _LBL[key] = im
    return _LBL[key]


# ---------------------------------------------------------------- BUG ID card

_IDC = {}


def id_card_img(card):
    key = repr(card)
    if key in _IDC:
        return _IDC[key]
    Wc = 940
    fN = ImageFont.truetype(D.FONT, 92)
    fR = ImageFont.truetype(D.FONT, 50)
    fH = ImageFont.truetype(D.FONT, 44)
    rows = card.get("rows", [])
    hh, nh, rh = 78, 120, 74
    Hc = hh + nh + rh * len(rows) + 40
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((0, 0, Wc - 1, Hc - 1), radius=34, fill=(20, 24, 38, 240), outline=(255, 255, 255, 255), width=6)
    dr.rounded_rectangle((6, 6, Wc - 7, hh), radius=28, fill=(255, 211, 77, 255))
    dr.rectangle((6, hh - 26, Wc - 7, hh), fill=(255, 211, 77, 255))
    dr.text((34, 14), "BUG ID", font=fH, fill=(20, 20, 20, 255))
    dr.text((Wc - 300, 14), "MEATBALL MYTHS", font=fH, fill=(20, 20, 20, 255))
    icon = _icon(card.get("type") or CFG.get("stage_type"), 300, 150)
    if icon is not None:
        im.alpha_composite(icon, (Wc - 330, hh + 6))
    dr.text((34, hh + 14), card.get("name", ""), font=fN, fill=(255, 255, 255, 255))
    y = hh + nh
    for r in rows:
        dr.rounded_rectangle((34, y + 16, 60, y + 42), radius=6, fill=(255, 211, 77, 255))
        dr.text((80, y + 2), r, font=fR, fill=(255, 255, 255, 255))
        y += rh
    _IDC[key] = im
    return im


def _icon(kind, w, h):
    fn = D.ACTORS.get(kind)
    if fn is None:
        return None
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    ctx.translate(w / 2, h * 0.9)
    ctx.scale(0.36, 0.36)
    try:
        fn(ctx, 0.3, {"walk": 0.5})
    except Exception:
        return None
    surf.flush()
    a = np.ndarray((h, w, 4), np.uint8, surf.get_data()).copy()
    al = a[..., 3:4].astype(np.float32)
    rgb = np.where(al > 0, a[..., [2, 1, 0]].astype(np.float32) * 255 / np.maximum(al, 1), 0)
    out = np.concatenate([np.clip(rgb, 0, 255), al], -1).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def id_card(arr, b, t):
    card = CFG.get("id_card")
    if not card or card.get("beat") != b["i"]:
        return
    a = _t(b, card.get("at", "10%"))
    v = t - a
    dur = card.get("dur", 2.4)
    if not 0 <= v < dur:
        return
    im = id_card_img(card)
    sc = card.get("scale", 0.88)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    if v < 0.25:   # pop with an overshoot
        u = v / 0.25
        k = 0.55 + 0.55 * math.sin(u * math.pi * 0.75) if u < 0.8 else 1.0 + 0.1 * (1 - u) / 0.2
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))))
    y = card.get("y", 200)
    if v > dur - 0.2:
        y -= int(900 * ((v - (dur - 0.2)) / 0.2) ** 2)
    D.paste(arr, im, W // 2, y + im.height // 2)


# ---------------------------------------------------------------- post (after the cairo frame)

def post(arr, ctx, surf, b, t, T, ins, whip):
    if not CFG:
        return
    if ins is not None:
        if ins["type"] == "seccam":
            seccam_post(arr, T)
        elif ins["type"] == "bugcam":
            bugcam_overlay(arr, ctx, surf, T)
        elif ins["type"] == "sizecheck":
            D.paste(arr, label("SIZE CHECK", 64, (255, 211, 77)), W // 2, 300)
        v = t - ins["_a"]
        if v < 2 / 30:   # a one-frame white pop into the shot
            arr[..., :3] = (arr[..., :3].astype(np.uint16) * 1 + 255 * 1) // 2
    if abs(whip) > 2:   # horizontal motion blur on the whip-pan
        acc = np.zeros(arr.shape[:2] + (3,), np.uint16)
        n = 6
        for k in range(n):
            acc += np.roll(arr[..., :3], int(whip * k / n), axis=1)
        arr[..., :3] = (acc // n).astype(np.uint8)
    id_card(arr, b, t)


# ---------------------------------------------------------------- audio

def music_env(spec, n, SR):
    """Gain on the music bus: a short drop to near silence right before each scare, back in on it."""
    g = np.ones(n, np.float32)
    if not CFG or not CFG["music_drop"]:
        return g
    for s in spec.get("_cine_scares", []):
        a, z = int((s - 0.55) * SR), int(s * SR)
        r = int(0.08 * SR)
        if a < 0:
            continue
        g[a:a + r] = np.minimum(g[a:a + r], np.linspace(1, 0.08, r))
        g[a + r:z] = np.minimum(g[a + r:z], 0.08)
    return g
