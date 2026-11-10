#!/usr/bin/env python3
"""16:9 "Don't squish it" long-form (format: channel-brain MASTER_ORDERS, "Long-form format from 11/10"). The viewer
holds a shoe over the creature; Meatball has three questions to talk them out of it; a SQUISH / SPARE meter keeps
score for the whole video; the verdict lands at the end. Same locked drawn look, Meatball and Andrew voice: this
module only adds a format layer on top of tools/drawn_keepkill.py (16:9, kk_end) and tools/drawn.py (renderer).

  build OUTLINE.json SPEC.json             outline -> buildable spec (every `say` kept; each line gets an "id"
                                           (s<segment>.l<line>) and a "shot" recipe from SHOTS below; re-running
                                           keeps shots already edited in SPEC.json for ids whose `say` is unchanged)
  render SPEC.json OUT.mp4 [--lines A-B] [--work DIR]     render (all lines, or a range of spec line indices)
  stills SPEC.json OUT.jpg --at ID@FRAC,ID@FRAC,...       one frame per line (FRAC = share of that line), as a
                                           contact sheet; the plan (voice) covers only the lines needed
  voice SPEC.json                          voice every line now (cached, validated)

Overlays (screen space, drawn over the scene and under the captions):
  ds_meter   SQUISH (red, shoe icon) ... SPARE (green, spider icon) bar near the top; the marker eases to each line's
             `meter` value with a soft tick ("click"), pulses on a move of >= 8 points, blinks an alarm under 40;
             p: v, on (slide in), pulse, big (0..1: centre frame, bigger)
  ds_qchip   "QUESTION n OF 3" chip, top left, with a green tick when that question is answered (done 0..1)
  ds_chapter chapter card (<= 1.2 s): kicker + title on a dark band
  ds_three   the cold open's three question chips, one per question
  ds_stamp   a rubber stamp (SPARE, NOT A CURE, URBAN LEGEND ...)
  ds_vs      versus card (CAROL vs THE BIG ONE)
World: ds_shoe (the viewer's shoe over the corner; height follows the meter), plus tools/drawn_ds_art.py.

Voice: en-US-AndrewMultilingualNeural +10% +3Hz, one mp3 per line cached by a hash of the spoken text (+ voice,
rate, pitch) in <episode>/.voice-cache/; a take that is empty, silent or without word timings is never accepted
(5 tries). A line may carry "tts" (a pronunciation respelling); captions always use `say`.
Music: "mystery" bed at -15 dB (as Part 2), dips under each pause-and-reveal hold, drops out for the line marked
"music_out"; whoosh on cuts; loudnorm -14 LUFS in the encode (drawn.encode_cmd).
"""
import copy
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_keepkill as kk  # noqa: E402  (sets drawn to 1920x1080, registers kk_end, wraps the macro expander)
import drawn  # noqa: E402
import drawn_ds_art as art  # noqa: E402
from drawn_kit import INK, OUT, back_out, darker, ease, flat, hexc, p_ellipse, p_poly, p_rrect, shape, src, stroke  # noqa: E402

W, H = 1920, 1080
ROOT = os.path.dirname(HERE)
FONT = kk.FONT
RED, GREEN, YEL = "#e5383b", "#3fb950", "#ffd34d"


# ================================================================================================ screen overlays

def _pill(ctx, x, y, w, h, fill_rgb, a=0.9, line=4):
    kk.rrect(ctx, x, y, w, h, h / 2)
    kk.fill(ctx, fill_rgb, a, line)


def _tiny_spider(ctx, cx, cy, k=1.0, col=(0.95, 0.92, 0.85)):
    """A legible little spider glyph (pale body, long legs) for the meter's SPARE end."""
    for s in (-1, 1):
        for i, (a1, a2) in enumerate(((70, 20), (45, 0), (20, -25), (0, -50))):
            r1, r2 = 20 * k, 22 * k
            x1 = cx + s * r1 * math.cos(math.radians(a1))
            y1 = cy - r1 * math.sin(math.radians(a1))
            x2 = x1 + s * r2 * math.cos(math.radians(a2))
            y2 = y1 - r2 * math.sin(math.radians(a2))
            stroke(ctx, [(cx, cy), (x1, y1), (x2, y2)], 5.5 * k)
            stroke(ctx, [(cx, cy), (x1, y1), (x2, y2)], 2.6 * k, color=col)
    shape(ctx, lambda c: p_ellipse(c, cx - 6 * k, cy + 9 * k, 7 * k, 12 * k, 0.5), col, 2.5 * k, None)
    shape(ctx, lambda c: p_ellipse(c, cx, cy, 8 * k, 8 * k), col, 2.5 * k, None)


def ds_meter(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    big = ease(p.get("big", 0.0))
    v = max(0.0, min(100.0, p.get("v", 30.0)))
    pulse = max(0.0, p.get("pulse", 0.0))
    sc = 1.0 + 0.75 * big
    cy = 66 + (500 - 66) * big - 170 * (1 - ease(on))
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(sc, sc)
    # plate
    alarm = v < 40
    blink = 0.5 + 0.5 * math.sin(t * 9) if alarm else 0.0
    kk.rrect(ctx, -555, -44, 1110, 88, 44)
    kk.fill(ctx, (18, 22, 40), 0.9, 0)
    kk.rrect(ctx, -555, -44, 1110, 88, 44)
    ctx.set_source_rgba(1, 1, 1, 0.9) if not alarm else ctx.set_source_rgba(0.9, 0.22 + 0.5 * (1 - blink), 0.23, 1)
    ctx.set_line_width(4 + 4 * blink)
    ctx.stroke()
    # ends: shoe + SQUISH, SPARE + spider
    ctx.save()
    ctx.translate(-492, 18)
    ctx.rotate(-0.15)
    art._shoe(ctx, 0.12)
    ctx.restore()
    ks = 1.0 + (0.12 * blink if alarm else 0.0)
    kk.blit(ctx, kk.text_img("SQUISH", 40, RED, 5), -360, 0, ks)
    kk.blit(ctx, kk.text_img("SPARE", 40, GREEN, 5), 372, 0)
    _tiny_spider(ctx, 490, 2, 1.05)
    # bar
    x0, x1, bh = -280, 280, 30
    kk.rrect(ctx, x0, -bh / 2, x1 - x0, bh, bh / 2)
    import cairo
    g = cairo.LinearGradient(x0, 0, x1, 0)
    for u, c in ((0.0, RED), (0.5, YEL), (1.0, GREEN)):
        r, gg, b = hexc(c)
        g.add_color_stop_rgb(u, r, gg, b)
    ctx.set_source(g)
    ctx.fill_preserve()
    ink_ = INK
    ctx.set_source_rgb(*ink_)
    ctx.set_line_width(4)
    ctx.stroke()
    mx = x0 + (x1 - x0) * v / 100.0
    if v < 100:   # the part past the marker is dimmed: the score so far
        kk.rrect(ctx, mx, -bh / 2 + 2, x1 - mx, bh - 4, (bh - 4) / 2)
        ctx.set_source_rgba(0.05, 0.06, 0.12, 0.55)
        ctx.fill()
    if pulse > 0:
        ctx.new_sub_path()
        ctx.arc(mx, 0, 26 + 50 * (1 - pulse), 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.8 * pulse)
        ctx.set_line_width(6)
        ctx.stroke()
    mk = 1.0 + 0.45 * pulse
    ctx.save()
    ctx.translate(mx, 0)
    ctx.scale(mk, mk)
    kk.rrect(ctx, -13, -30, 26, 60, 10)
    kk.fill(ctx, "#ffffff", 1.0, 5)
    ctx.move_to(-12, -40)
    ctx.line_to(12, -40)
    ctx.line_to(0, -28)
    ctx.close_path()
    kk.fill(ctx, "#ffffff", 1.0, 4)
    ctx.restore()
    ctx.restore()


def ds_qchip(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01 or not p.get("text"):
        return
    ctx.identity_matrix()
    im = kk.text_img(p["text"], 38, "#ffffff", 0)
    w = im[0].get_width()
    x, y = 28 - 400 * (1 - ease(on)), 34
    _pill(ctx, x, y, w + 44, 66, (18, 22, 40), 0.9, 4)
    kk.blit(ctx, im, x + 22 + w / 2, y + 33)
    d = p.get("done", 0.0)
    if d > 0:
        s = back_out(min(1.0, d))
        cx, cy = x + w + 44 + 40, y + 33
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(s, s)
        ctx.arc(0, 0, 30, 0, 2 * math.pi)
        kk.fill(ctx, GREEN, 1.0, 5)
        stroke(ctx, [(-14, 1), (-4, 12), (15, -12)], 9, color=(1, 1, 1))
        ctx.restore()


def ds_chapter(ctx, t, p):
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    a = min(1.0, on)
    ctx.rectangle(0, 330, W, 400)
    ctx.set_source_rgba(0.07, 0.06, 0.1, 0.84 * a)
    ctx.fill()
    dx = -120 * (1 - ease(on))
    if p.get("kicker"):
        kk.blit(ctx, kk.text_img(p["kicker"], 54, "#ffffff", 6), W / 2 + dx, 420, 1.0, a)
    title = p.get("title", "")
    px = 130 if len(title) < 18 else 104
    kk.blit(ctx, kk.text_img(title, px, YEL, 10), W / 2 - dx, 560, 1.0, a)


def ds_three(ctx, t, p):
    n = p.get("n", 0.0)
    items = p.get("items", [])
    if n <= 0.01:
        return
    ctx.identity_matrix()
    for i, it in enumerate(items):
        u = max(0.0, min(1.0, (n - i) * 2.5))
        if u <= 0:
            continue
        s = back_out(u)
        y = 300 + i * 150
        x = W - 330
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        im = kk.text_img(it, 64, "#ffffff", 0)
        w = im[0].get_width()
        _pill(ctx, -w / 2 - 90, -50, w + 130, 100, (18, 22, 40), 0.92, 5)
        ctx.arc(-w / 2 - 40, 0, 34, 0, 2 * math.pi)
        kk.fill(ctx, YEL, 1.0, 4)
        kk.blit(ctx, kk.text_img(str(i + 1), 50, "#222222", 0), -w / 2 - 40, 0)
        kk.blit(ctx, im, 25, 0)
        ctx.restore()


def ds_stamp(ctx, t, p):
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    sc = 1.0 if on >= 1 else 2.3 - 1.3 * ease(on)
    col = p.get("color", GREEN)
    ctx.save()
    ctx.translate(p.get("x", W / 2), p.get("y", 540))
    ctx.rotate(math.radians(p.get("rot", -10)))
    ctx.scale(sc, sc)
    im = kk.text_img(p["text"], p.get("px", 170), col, 0)
    w, h = im[0].get_width(), im[0].get_height()
    kk.rrect(ctx, -w / 2 - 40, -h / 2 - 20, w + 80, h + 40, 26)
    ctx.set_source_rgba(1, 1, 1, 0.85 * min(1.0, on * 3))
    ctx.fill_preserve()
    r, g, b = hexc(col)
    ctx.set_source_rgba(r, g, b, min(1.0, on * 3))
    ctx.set_line_width(16)
    ctx.stroke()
    kk.blit(ctx, im, 0, 0, 1.0, min(1.0, on * 3))
    ctx.restore()


def ds_vs(ctx, t, p):
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    u = ease(min(1.0, on))
    ctx.rectangle(0, 0, W / 2 * u, H)
    kk.fill(ctx, "#2b5f3f", 0.92)
    ctx.rectangle(W - W / 2 * u, 0, W / 2 * u, H)
    kk.fill(ctx, "#6b2a2a", 0.92)
    if u > 0.6:
        kk.blit(ctx, kk.text_img(p.get("left", "CAROL"), 110, "#ffffff", 9), W / 4, 760)
        kk.blit(ctx, kk.text_img(p.get("right", "THE BIG ONE"), 110, "#ffffff", 9), 3 * W / 4, 760)
        s = back_out(min(1.0, (u - 0.6) * 2.5))
        kk.blit(ctx, kk.text_img("VS", 200, YEL, 14), W / 2, 470, s)


OVERLAYS = {"ds_meter": ds_meter, "ds_qchip": ds_qchip, "ds_chapter": ds_chapter, "ds_three": ds_three,
            "ds_stamp": ds_stamp, "ds_vs": ds_vs}


# ------------------------------------------------------------------ a few more small world actors (format-specific)

def ds_ring(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    r = p.get("r", 40) * (1 + 0.06 * math.sin(t * 7))
    ctx.new_sub_path()
    ctx.arc(0, 0, r * back_out(min(1.0, on)), 0, 2 * math.pi)
    ctx.set_source_rgba(1, 0.83, 0.3, min(1.0, on))
    ctx.set_line_width(p.get("lw", 6))
    ctx.stroke()


def ds_notes(ctx, t, p):
    """Whistling: little music notes drifting up."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    for k in range(3):
        u = (t * 0.6 + k / 3) % 1
        x, y = 40 * k + 20 * math.sin(t * 3 + k), -200 * u
        a = on * (1 - u)
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 16, 12, -0.4), INK, 0, None, a=a)
        stroke(ctx, [(x + 14, y - 4), (x + 14, y - 64), (x + 34, y - 54)], 6, a=a)


def ds_feet(ctx, t, p):
    """The viewer's two socked feet standing on the chair seat (no likeness)."""
    for x in (-90, 60):
        shape(ctx, lambda c, x=x: p_rrect(c, x - 10, -330, 70, 330, 30), hexc("#3b4b6b"), OUT, (0.1, 0))
        shape(ctx, lambda c, x=x: p_rrect(c, x - 40, -60, 150, 66, 30), hexc("#f2f2ea"), OUT, (0, 0.2))


def ds_cross(ctx, t, p):
    """A red X drawn over something (on 0..1)."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    r = p.get("r", 120)
    for (a, b) in (((-r, -r), (r, r)), ((r, -r), (-r, r))):
        e = (a[0] + (b[0] - a[0]) * min(1.0, on), a[1] + (b[1] - a[1]) * min(1.0, on))
        stroke(ctx, [a, e], 34)
        stroke(ctx, [a, e], 20, color=hexc(RED))


drawn.ACTORS.update(art.ACTORS)
drawn.ACTORS.update(OVERLAYS)
drawn.ACTORS.update(ds_ring=ds_ring, ds_notes=ds_notes, ds_feet=ds_feet, ds_cross=ds_cross)
drawn.SCENES.update(art.SCENES)

# a beat may opt out of the automatic re-cut (boards whose text must stay in frame)
_orig_recut = drawn.recut


def _recut(b, shots, dur, hero, k, until):
    return shots if b.get("norecut") else _orig_recut(b, shots, dur, hero, k, until)


drawn.recut = _recut


# ================================================================================================ geometry helpers

CORNER = (700, 150)
CAROL = [720, 610]
CS = 0.6
CAMS = {"close": [720, 560, 1.9], "mid": [720, 500, 1.3], "wide": [700, 470, 1.0], "face": [720, 588, 4.6],
        "low": [700, 520, 0.92]}


def leg_tip(pos, s, leg=0, side=1):
    """World point of a Carol leg tip (no sway), for brackets and silk targets."""
    fem, tib, tar = art.LEGS[leg]
    hx, hy = side * (14 - leg * 3), 8 + leg * 4
    fa, ta, ra = (math.radians(a[1]) for a in (fem, tib, tar))
    kx, ky = hx + side * fem[0] * math.cos(fa), hy - fem[0] * math.sin(fa)
    ax, ay = kx + side * tib[0] * math.cos(ta), ky - tib[0] * math.sin(ta)
    tx, ty = ax + side * tar[0] * math.cos(ra), ay - tar[0] * math.sin(ra)
    return [pos[0] + tx * s, pos[1] + ty * s]


def carol(p=None, pos=None, s=CS, sets=None, moves=None, idn="hero", front=False):
    a = {"id": idn, "type": "carol", "pos": list(pos or CAROL), "s": s, "front": front,
         "p": dict({"mood": "calm", "look": [0, 0.2], "work": 0.0, "flick": 0.0, "whirl": 0.0, "eggs": 0.0,
                    "wave": 0.0, "reach": 0.0, "shrug": 0.0, "eyes8": 0.0, "still": False, "hat": 0.0, "shades": 0.0},
                   **(p or {}))}
    if sets:
        a["set"] = sets
    if moves:
        a["moves"] = moves
    return a


def web(p=None, pos=None, s=1.0, idn="web"):
    return {"id": idn, "type": "ds_web", "pos": list(pos or CORNER), "s": s, "p": dict({"w": 720, "h": 820}, **(p or {}))}


def actor(idn, typ, pos, s=1.0, p=None, sets=None, moves=None, front=False, flip=False, rot=0.0):
    a = {"id": idn, "type": typ, "pos": list(pos), "s": s, "p": dict(p or {}), "front": front}
    if flip:
        a["flip"] = True
    if rot:
        a["rot"] = rot
    if sets:
        a["set"] = sets
    if moves:
        a["moves"] = moves
    return a


def pop(at, dur=0.3, key="on"):
    return [{"at": at, "dur": dur, "p": {key: 1.0}}]


def mb(pose="neutral", pos=(1500, 1500), size=900, **kw):
    m = {"pose": pose, "pos": list(pos), "size": size, "look": kw.pop("look", "viewer"), "prop": kw.pop("prop", None)}
    m.update(kw)
    return m


HIDDEN = {"hidden": True, "pose": "neutral", "pos": [-2000, 1500], "size": 600}


def cam(c, to=None, at=None, dur=None):
    s = {"cam": list(CAMS.get(c, c) if isinstance(c, str) else c)}
    s["to"] = list(CAMS.get(to, to) if isinstance(to, str) else to) if to is not None else list(s["cam"])
    if at is not None:
        s["at"] = at
    if dur is not None:
        s["dur"] = dur
    return s


def push(c, k=1.08, dx=0, dy=0):
    c = list(CAMS.get(c, c) if isinstance(c, str) else c)
    return [c[0] + dx, c[1] + dy, round(c[2] * k, 3)]


# ================================================================================================ line recipes
# Each recipe: f(L, a) -> beat dict (scene, scene_p, actors, shots, mb, sfx, extra keys). L = the spec line, a = its
# shot args. The format layer (meter, chip, shoe, chapter card, card placement) is added afterwards by expand().

def r_corner(L, a):
    """The ceiling corner with Carol in her web. a: cam, to, carol (p), carol_sets, carol_moves, extras, mb, shoe
    (default true), web (p), sfx."""
    c0 = a.get("cam", "mid")
    shots = a.get("shots") or [cam(c0, a.get("to", push(c0, 1.07)))]
    acts = [web(a.get("web")), carol(a.get("carol"), a.get("carol_pos"), a.get("carol_s", CS), a.get("carol_sets"),
                                      a.get("carol_moves"))]
    acts += [copy.deepcopy(x) for x in a.get("extras", [])]
    return {"scene": "ds_corner", "scene_p": {}, "actors": acts, "shots": shots,
            "mb": a.get("mb", HIDDEN), "sfx": a.get("sfx", []), "shoe": a.get("shoe", True)}


def r_scene(L, a):
    """Any scene with explicit actors: a: scene, scene_p, cam/to or shots, actors, mb, sfx."""
    c0 = a.get("cam", [700, 600, 1.0])
    shots = a.get("shots") or [cam(c0, a.get("to", push(c0, 1.06)))]
    return {"scene": a["scene"], "scene_p": a.get("scene_p", {}), "actors": copy.deepcopy(a.get("actors", [])),
            "shots": shots, "mb": a.get("mb", HIDDEN), "sfx": a.get("sfx", []), "shoe": a.get("shoe", False)}


RECIPES = {"corner": r_corner, "scene": r_scene}

# ------------------------------------------------------------------ the shot table: outline line -> recipe + args
# Kept as data so a line edit only touches its own entry. Word anchors ("hunting") fall back to a share ("|40%").

FLY = lambda idn, pos, s, sets=None, moves=None: actor(idn, "fly", pos, s, {"wrapped": 0.0}, sets, moves)  # noqa: E731


def _shots_table():
    T = {}
    tipR = leg_tip(CAROL, CS, 0, 1)
    # ----------------------------------------------------------------------------------------- cold open
    T["s0.l0"] = {"r": "corner", "cam": "close", "to": push("close", 1.08), "shoe": False,
                  "shots": [cam("close", push("close", 1.07)), cam(push("close", 1.07), [710, 470, 1.15], at="hunting|55%", dur=0.9)],
                  "carol": {"work": 1.0, "look": [0.4, 0.5], "mood": "calm"},
                  "carol_sets": [{"at": "hunting|55%", "dur": 0.3, "p": {"work": 0.0, "look": [0.5, 0.8], "mood": "smug"}}],
                  "sfx": ["sting@0", "whoosh@hunting|55%"], "card_at": "hunting|55%"}
    T["s0.l1"] = {"r": "scene", "scene": "ds_floor", "cam": [700, 760, 1.0], "to": [760, 780, 1.12],
                  "actors": [actor("shadow", "ds_shadow", [1900, 1000], 1.25, {"a": 0.62}, rot=-8,
                                   moves=[{"at": 0, "dur": 2.6, "pos": [-300, 820], "linear": True}])],
                  "sfx": ["thud@0.2", "step@much|50%"]}
    T["s0.l2"] = {"r": "corner", "cam": "wide", "to": [700, 455, 1.06],
                  "carol": {"look": [0.2, -0.6], "mood": "worry"},
                  "carol_sets": [{"at": "shoe|70%", "dur": 0.2, "p": {"mood": "shock", "look": [0.1, -1.0]}}],
                  "shoe_enter": "holding|55%", "meter_in": "shoe|70%", "sfx": ["whoosh@holding|55%"]}
    T["s0.l3"] = {"r": "corner", "cam": [760, 470, 1.08], "to": [780, 470, 1.18],
                  "carol": {"look": [0.8, -0.3], "mood": "worry"},
                  "mb": mb("shrug", (1160, 1700), 520, float=True, look="viewer",
                           moves=[{"at": 0.05, "dur": 0.55, "pos": [1130, 830], "hop": 160}], gest=[["swing|70%", "shock", 1.0]]),
                  "sfx": ["boing@0.1"], "card_at": "three|30%"}
    T["s0.l4"] = {"r": "corner", "cam": [880, 480, 1.0], "to": [860, 470, 1.06],
                  "carol": {"look": [-0.3, 0.2]},
                  "mb": mb("point", (1100, 830), 520, float=True, look="hero",
                           gest=[["hunting", "point", 0.8], ["hurt", "think", 0.8], ["leave", "shrug", 1.0]]),
                  "three": ["HUNTING?", "HURT YOU?", "LEAVE IT?"], "three_at": ["hunting|20%", "hurt|50%", "leave|80%"],
                  "sfx": ["pop@hunting|20%", "pop@hurt|50%"]}
    T["s0.l5"] = {"r": "scene", "scene": "bedroom", "scene_p": {"time": "night"}, "cam": [760, 1100, 0.78], "to": [800, 1080, 0.86],
                  "actors": [actor("chair", "chair", [760, 1500], 1.0), actor("feet", "ds_feet", [770, 1032], 1.0)],
                  "mb": mb("lean", (1010, 1500), 900, look="viewer", gest=[["squish|60%", "deadpan", 2.0]],
                           moves=[{"at": "chair|80%", "dur": 0.3, "pos": [980, 1500]}]),
                  "meter_pulse": "meter|25%", "sfx": ["thud@chair|80%"]}
    # ----------------------------------------------------------------------------------------- question 1
    T["s1.l0"] = {"r": "corner", "cam": "wide", "to": [700, 470, 1.1], "carol": {"work": 0.6}, "chapter": True}
    T["s1.l1"] = {"r": "corner", "cam": [760, 400, 1.12], "to": [760, 400, 1.18],
                  "carol": {"mood": "happy", "look": [0, 0]},
                  "extras": [actor("dim1", "ds_dim", [CAROL[0] - 175 * CS * 1.0, CAROL[1] + 150 * CS], 1.0,
                                   {"to": [215 * CS, -150 * CS], "grow": 0.0, "text": "1/4 INCH", "lx": -150, "ly": 40, "px": 60},
                                   sets=[{"at": "quarter|45%", "dur": 0.45, "p": {"grow": 1.0}}]),
                             actor("dim2", "ds_dim", [CAROL[0] + 10, CAROL[1] + 5], 1.0,
                                   {"to": [tipR[0] - CAROL[0] - 10, tipR[1] - CAROL[1] - 5], "grow": 0.0, "text": "2 INCHES",
                                    "lx": 90, "ly": 30, "px": 64},
                                   sets=[{"at": "two|78%", "dur": 0.6, "p": {"grow": 1.0}}])],
                  "card_at": "cellar|10%", "sfx": ["tink@quarter|45%", "whoosh@two|78%"]}
    T["s1.l2"] = {"r": "corner", "cam": [720, 594, 3.2], "to": "face", "shoe": False,
                  "carol": {"eyes8": 1.0, "look": [0, 0], "mood": "calm", "still": True},
                  "extras": [actor("ring%d" % i, "ds_ring", [CAROL[0] + x * CS, CAROL[1] - 30 * CS + y * CS], 1.0,
                                   {"on": 0.0, "r": r, "lw": 3},
                                   sets=[{"at": "three|%d%%" % (60 + 8 * i), "dur": 0.3, "p": {"on": 1.0}}])
                             for i, (x, y, r) in enumerate(((-38, 0, 15), (0, 10, 21), (38, 0, 15)))],
                  "sfx": ["tink@eight|35%", "pop@three|65%"]}
    T["s1.l3"] = {"r": "corner", "cam": [860, 500, 1.15], "to": [860, 490, 1.22],
                  "carol": {"mood": "happy", "look": [0.6, 0.2]},
                  "carol_sets": [{"at": "Carol|50%", "dur": 0.3, "p": {"wave": 1.0}}],
                  "extras": [actor("tag", "ds_tag", [CAROL[0] - 230, CAROL[1] + 40], 0.8, {"on": 0.0, "text": "CAROL"},
                                   sets=pop("Carol|50%", 0.35))],
                  "mb": mb("wave", (1230, 900), 480, float=True, look="hero",
                           moves=[{"at": 0, "dur": 0.4, "pos": [1210, 880], "hop": 80}]),
                  "sfx": ["pop@Carol|50%"]}
    T["s1.l4"] = {"r": "corner", "cam": [720, 600, 1.7], "to": [700, 470, 1.02],
                  "carol": {"still": True, "mood": "calm", "look": [0, 0.3]},
                  "carol_sets": [{"at": "waits|80%", "dur": 0.25, "p": {"look": [-0.8, 0.2]}},
                                 {"at": "waits+0.5", "dur": 0.25, "p": {"look": [0.8, 0.2]}}],
                  "extras": [actor("tag", "ds_tag", [CAROL[0] - 230, CAROL[1] + 40], 0.8, {"on": 1.0, "text": "CAROL"})],
                  "sfx": ["whoosh@0"]}
    fpos, lpos = [1130, 470], [420, 740]
    T["s1.l5"] = {"r": "corner", "cam": [740, 500, 1.15], "to": [720, 520, 1.2],
                  "carol": {"look": [0.8, -0.3]},
                  "carol_sets": [{"at": "insects|20%", "dur": 0.2, "p": {"flick": 1.0, "flick_to": [700, -260], "look": [0.9, -0.4]}},
                                 {"at": "Woodlice|50%", "dur": 0.2, "p": {"flick_to": [-560, 220], "look": [-0.9, 0.4]}},
                                 {"at": "blunders|85%", "dur": 0.2, "p": {"flick": 0.0, "mood": "smug", "look": [0, 0]}}],
                  "extras": [FLY("fly", [1700, 300], 0.32, sets=[{"at": "insects|20%", "dur": 0.6, "p": {"wrapped": 1.0}}],
                                 moves=[{"at": 0, "dur": 0.6, "pos": fpos}]),
                             actor("louse", "woodlouse", [lpos[0], -300], 0.42, {"wrapped": 0.0}, flip=True,
                                   sets=[{"at": "Woodlice+0.3", "dur": 0.6, "p": {"wrapped": 1.0}}],
                                   moves=[{"at": "Woodlice|40%", "dur": 0.45, "pos": lpos}])],
                  "sfx": ["zap@insects|20%", "thud@Woodlice|40%"]}
    T["s1.l6"] = {"r": "scene", "scene": "ds_lab", "cam": [760, 640, 0.95], "to": [800, 640, 1.03],
                  "actors": [actor("arena", "ds_arena", [560, 900], 1.25),
                             carol({"look": [0.6, 0.2], "mood": "happy"}, [560, 540], 0.3,
                                   sets=[{"at": "eggs|85%", "dur": 0.4, "p": {"eggs": 1.0}}]),
                             actor("cal", "ds_prop", [1260, 400], 0.8, {"kind": "calendar", "day": 1.0},
                                   sets=[{"at": "every|45%", "dur": 1.6, "p": {"day": 4.0}}]),
                             actor("plate", "ds_prop", [1720, 820], 0.5, {"kind": "plate"},
                                   moves=[{"at": "fly|25%", "dur": 0.9, "pos": [980, 820], "walk": True}]),
                             FLY("fly", [1720, 790], 0.16, moves=[{"at": "fly|25%", "dur": 0.9, "pos": [980, 790]}])],
                  "mb": mb("present", (1900, 900), 560, look="hero",
                           moves=[{"at": "fly|25%", "dur": 0.9, "pos": [1140, 900], "walk": True}]),
                  "norecut": False, "sfx": ["step@fly|30%", "pop@eggs|85%"]}
    T["s1.l7"] = {"r": "corner", "cam": [720, 430, 1.12], "to": [720, 420, 1.2],
                  "carol": {"look": [0.2, -1.0], "mood": "worry"}, "shoe_twitch": "shoe|70%",
                  "extras": [actor("tag", "ds_tag", [CAROL[0] - 230, CAROL[1] + 40], 0.8, {"on": 1.0, "text": "CAROL"})],
                  "sfx": ["scratch@shoe|70%"]}
    T["s1.l8"] = {"r": "scene", "scene": "ds_shed", "cam": [250, 1000, 0.82], "to": [800, 1000, 0.86],
                  "actors": [actor("eng", "ds_label", [1030, 80], 1.0, {"text": "ENGLAND", "px": 56, "on": 0.0},
                                   sets=pop("England|10%")),
                             actor("tray", "ds_prop", [-80, 1150], 0.7, {"kind": "tray", "n": 0},
                                   moves=[{"at": "emptied|30%", "dur": 2.4, "pos": [620, 1150], "walk": True}],
                                   sets=[{"at": "emptied|30%", "dur": 2.6, "p": {"n": 12}}])],
                  "mb": mb("present", (40, 1500), 820, look="viewer", prop="magnifier",
                           moves=[{"at": "emptied|30%", "dur": 2.4, "pos": [740, 1500], "walk": True}],
                           gest=[["leftovers|85%", "point", 1.0]]),
                  "sfx": ["step@emptied|35%", "pop@leftovers|85%"]}
    T["s1.l9"] = {"r": "scene", "scene": "ds_board_bg", "cam": [0, 40, 1.0], "to": [0, 40, 1.04], "norecut": True,
                  "actors": [actor("board", "ds_board", [0, 60], 1.0, {"n": 0, "sort": 0.0, "sort2": 0.0},
                                   sets=[{"at": 0.05, "dur": 1.5, "p": {"n": 102}}])],
                  "sfx": ["pop@0.1", "tink@dead|80%"]}
    T["s1.l10"] = {"r": "scene", "scene": "ds_board_bg", "cam": [0, 40, 1.04], "to": [-80, 60, 1.1], "norecut": True,
                   "actors": [actor("board", "ds_board", [0, 60], 1.0, {"n": 102, "sort": 0.0, "count": False},
                                    sets=[{"at": "house|50%", "dur": 1.2, "p": {"sort": 1.0}}])],
                   "card_at": "Sixty|10%", "sfx": ["whoosh@house|50%"]}
    T["s1.l11"] = {"r": "scene", "scene": "ds_board_bg", "cam": [-40, 60, 1.08], "to": [60, 60, 1.1], "norecut": True,
                   "actors": [actor("board", "ds_board", [0, 60], 1.0, {"n": 102, "sort": 1.0, "sort2": 0.0, "count": False,
                                                                         "label2": "CELLAR SPIDERS"},
                                    sets=[{"at": "Six|15%", "dur": 0.8, "p": {"sort2": 1.0}}]),
                              carol({"look": [1, -0.6], "mood": "smug", "still": True}, [840, -330], 0.3, idn="carolw"),
                              actor("notes", "ds_notes", [940, -400], 1.0, {"on": 0.0}, sets=pop("cellar|60%"))],
                   "sfx": ["pop@Six|25%"]}
    T["s1.l12"] = {"r": "scene", "scene": "ds_board_bg", "cam": [0, 0, 1.0], "to": [0, 0, 1.05], "norecut": True,
                   "actors": [actor("pie", "ds_pie", [-330, 70], 1.0,
                                    {"slices": [[63, "#c98a4a", "63 HOUSE SPIDERS"], [6, "#e2d3b0", "6 CELLAR SPIDERS"],
                                                [33, "#8a94a6", "33 UNIDENTIFIED SPIDER BITS"]], "sweep": 0.0},
                                    sets=[{"at": 0.05, "dur": 1.2, "p": {"sweep": 1.0}}])],
                   "card_at": "Every|55%", "sfx": ["whoosh@0.05", "stamp@Every|60%"]}
    # ----------------------------------------------------------------------------------------- hard visuals (stills check)
    left = [520, 600]
    T["s1.l14"] = {"r": "corner", "cam": [840, 600, 0.92], "to": [860, 610, 0.98], "carol_pos": left,
                   "carol": {"look": [1, 0.4], "mood": "smug"},
                   "extras": [actor("giant", "giant_spider", [1250, 1010], 0.66, {"mood": "angry", "look": [-0.6, 0.1]},
                                    flip=True, moves=[{"at": 0, "dur": 1.2, "pos": [1180, 1010], "walk": True}]),
                              actor("glabel", "ds_label", [1180, 1110], 1.0, {"text": "GIANT HOUSE SPIDER", "px": 50, "on": 0.0},
                                    sets=pop("giant|35%"))],
                   "card_at": "big|70%", "sfx": ["thud@giant|35%", "boing@big|70%"]}
    tgt = [1060, 960]
    T["s1.l21"] = {"r": "corner", "cam": [820, 660, 1.2], "to": [840, 690, 1.3], "carol_pos": [560, 600],
                   "carol": {"flick": 0.0, "flick_to": [(tgt[0] - 560) / CS, (tgt[1] - 180 - 600) / CS], "mood": "angry",
                             "look": [1, 0.4]},
                   "carol_sets": [{"at": "flicks|35%", "dur": 0.3, "p": {"flick": 1.0}}],
                   "extras": [actor("giant", "giant_spider", tgt, 0.52, {"mood": "shock", "wrapped": 0.0, "walk": 0.6}, flip=True,
                                    sets=[{"at": "flicks|35%", "dur": 2.0, "p": {"wrapped": 0.45}}])],
                   "sfx": ["whoosh@flicks|35%"]}
    lineup = [actor("lineup", "ds_lineup", [700, 1250], 1.0, {"lit": [1, 1, 1]}),
              actor("sus1", "harvestman", [140, 1170], 0.62, {"mood": "worry"}),
              actor("sus2", "crane_fly", [700, 1170], 0.62, {"mood": "worry"}),
              carol({"thread": 600, "mood": "smug", "look": [0, 0.2]}, [1260, 760], 0.42, idn="hero")]

    def lineup_line(lit, lit_to=None, at="30%", labels=(), extra_sets=()):
        acts = copy.deepcopy(lineup)
        acts[0]["p"]["lit"] = list(lit)
        mask = actor("mask", "ds_lineup_mask", [700, 1250], 1.0, {"lit": list(lit)}, front=True)
        if lit_to:
            acts[0]["set"] = [{"at": at, "dur": 0.4, "p": {"lit": lit_to}}]
            mask["set"] = [{"at": at, "dur": 0.4, "p": {"lit": lit_to}}]
        acts.append(mask)
        for i, (txt, col, on0, lat) in enumerate(labels):
            x = [140, 700, 1260][i]
            acts.append(actor(f"lab{i}", "ds_label", [x, 1185], 1.0, {"text": txt, "color": col, "px": 54, "on": on0},
                              sets=pop(lat) if lat else None, front=True))
        return acts
    L1 = ("NOT A SPIDER", "#ffffff")
    L2 = ("INSECT", "#ffffff")
    L3 = ("THE SPIDER", YEL)
    T["s2.l3"] = {"r": "scene", "scene": "ds_board_bg", "scene_p": {"color": "#20242e"}, "cam": [700, 760, 0.98],
                  "to": [700, 760, 1.03], "norecut": True,
                  "actors": lineup_line([0, 0, 0], [0.12, 0.12, 0.12], "Three|40%"), "sfx": ["thud@Three|40%"]}
    T["s2.l4"] = {"r": "scene", "scene": "ds_board_bg", "scene_p": {"color": "#20242e"}, "cam": [700, 760, 0.98],
                  "to": [520, 780, 1.06], "norecut": True,
                  "actors": lineup_line([0.12, 0.12, 0.12], [1, 0.12, 0.12], "harvestman|15%",
                                        [(L1[0], L1[1], 0.0, "Not|55%")]), "sfx": ["click@harvestman|15%", "stamp@Not|55%"]}
    T["s2.l5"] = {"r": "scene", "scene": "ds_board_bg", "scene_p": {"color": "#20242e"}, "cam": [560, 780, 1.04],
                  "to": [760, 780, 1.06], "norecut": True,
                  "actors": lineup_line([1, 0.12, 0.12], [1, 1, 0.12], "crane|15%",
                                        [(L1[0], L1[1], 1.0, None), (L2[0], L2[1], 0.0, "insect|60%")]),
                  "sfx": ["click@crane|15%", "stamp@insect|60%"]}
    T["s2.l6"] = {"r": "scene", "scene": "ds_board_bg", "scene_p": {"color": "#20242e"}, "cam": [760, 780, 1.04],
                  "to": [700, 760, 0.98], "norecut": True,
                  "actors": lineup_line([1, 1, 0.12], [1, 1, 1], "Carol|10%",
                                        [(L1[0], L1[1], 1.0, None), (L2[0], L2[1], 1.0, None), (L3[0], L3[1], 0.0, "only|60%")]),
                  "sfx": ["click@Carol|10%", "stamp@only|60%"]}
    T["s3.l4"] = {"r": "corner", "cam": [720, 640, 1.75], "to": [720, 650, 1.9],
                  "carol": {"eggs": 1.0, "mood": "happy", "look": [0, 0.8]}, "sfx": ["tink@eggs|30%"]}
    T["s3.l27"] = {"r": "corner", "cam": [820, 600, 1.0], "to": [800, 600, 1.08],
                   "carol": {"mood": "shock", "look": [1, 0.5]},
                   "carol_sets": [{"at": "whirls|10%", "dur": 0.3, "p": {"whirl": 1.0}}],
                   "extras": [actor("js", "jumper", [1260, 1010], 0.5, {"mood": "smug", "look": [-0.6, -0.2]}, flip=True)],
                   "card_at": "blur|60%", "sfx": ["whoosh@whirls|10%", "whoosh@blur|60%"]}
    T["s5.l4"] = {"r": "corner", "cam": [720, 470, 1.05], "to": [720, 460, 1.12], "meter_big": 1.0,
                  "carol": {"mood": "happy", "look": [0, 0], "shades": 0.0},
                  "carol_sets": [{"at": "down|70%", "dur": 0.3, "p": {"wave": 1.0}}],
                  "meter_at": "Put|35%", "shoe_lift": "down|70%", "no_card": True,
                  "stamp": {"text": "SPARE", "color": GREEN, "at": "down|70%", "y": 790, "px": 170},
                  "sfx": ["stamp@down|70%"]}
    return T


SHOTS = _shots_table()


def default_shot(sid, L, seg):
    """Lines without a hand-made entry yet: Carol in her corner, Meatball reacting, a rotating camera."""
    k = sum(map(ord, sid)) % 4
    c0 = ["mid", "wide", [760, 520, 1.15], [680, 480, 1.1]][k]
    out = {"r": "corner", "cam": c0, "to": push(c0, 1.08, 20 if k % 2 else -20), "_todo": True}
    if k in (1, 3):
        out["mb"] = mb(["think", "point", "shrug", "deadpan"][k], (1230, 900), 460, float=True, look="hero")
    return out


# ================================================================================================ build (outline -> spec)

def _strip(s):
    return re.sub(r"\s+", " ", s.strip())


def build(outline, out_spec):
    o = json.load(open(outline))
    old = {}
    if os.path.exists(out_spec):
        for ln in json.load(open(out_spec)).get("lines", []):
            old[ln["id"]] = ln
    lines = []
    for si, seg in enumerate(o["segments"]):
        for li, ln in enumerate(seg["lines"]):
            sid = f"s{si}.l{li}"
            L = {k: v for k, v in ln.items()}
            L["id"] = sid
            L["seg"] = si
            prev = old.get(sid)
            if prev and prev.get("say") == ln["say"] and prev.get("shot") and not prev["shot"].get("_todo"):
                L["shot"] = prev["shot"]
            else:
                L["shot"] = copy.deepcopy(SHOTS.get(sid) or default_shot(sid, L, seg))
            if prev and prev.get("tts"):
                L["tts"] = prev["tts"]
            lines.append(L)
    segs = [{k: v for k, v in s.items() if k != "lines"} for s in o["segments"]]
    spec = {"_note": "Built by tools/drawn_dontsquish.py build from " + os.path.basename(outline) +
                     ". Each line: id (s<seg>.l<line>), the outline fields (say/vis/card/meter/src) and shot (recipe + "
                     "args). Edit a line's say and re-render: only that line is re-voiced (hash cache).",
            "voice": o.get("voice", "en-US-AndrewMultilingualNeural"), "rate": o.get("rate", "+10%"),
            "pitch": o.get("pitch", "+3Hz"), "music": "mystery", "music_db": -15, "captions": 62, "caption_y": 985,
            "cut_whoosh": True, "sfx_gain": 0.22, "meter_start": o.get("meter_start", 30),
            "cap_key": ["squish", "spare", "shoe", "spider", "spiders", "carol", "hunting", "venom", "fangs", "web",
                        "eggs", "bigger", "giant", "recluse", "recluses", "harmless", "beneficial", "vacuum", "verdict",
                        "two", "three", "five", "six", "seven", "eight", "ten", "fifty", "hundred", "sixty-three",
                        "quarter", "inches", "eyes", "whirls", "blur", "mild", "rumor", "lab", "every"],
            "pause_lines": ["s1.l19", "s3.l26", "s5.l0"], "music_out": ["s1.l18"],
            "end_hold": 12.0, "end_label": o.get("end_screen_video"), "segments": segs, "titles": o.get("titles"),
            "pinned_comment": o.get("pinned_comment"), "lines": lines}
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    todo = sum(1 for L in lines if L["shot"].get("_todo"))
    print(f"{out_spec}: {len(lines)} lines, {sum(len(L['say'].split()) for L in lines)} words, "
          f"{len(lines) - todo} with hand-made shots, {todo} on the default corner shot")


# ================================================================================================ expand (spec -> drawn beats)

def _card_rows(text, px=118, max_w=1500):
    from PIL import ImageFont
    f = ImageFont.truetype(FONT, px)
    while px > 60 and f.getlength(text) > max_w:
        px -= 6
        f = ImageFont.truetype(FONT, px)
    return [[text, YEL, px]]


def expand(spec, lines):
    """drawn.py beats for these spec lines, with the format layer: meter, chip, shoe, chapter card, cards."""
    segs = spec["segments"]
    allL = spec["lines"]
    # meter state before each line, over the WHOLE episode (so a sub-range starts at the right value)
    v = float(spec.get("meter_start", 30))
    before, meter_on_from = {}, None
    for L in allL:
        before[L["id"]] = v
        if L["shot"].get("meter_in") and meter_on_from is None:
            meter_on_from = L["id"]
        if "meter" in L:
            v = float(L["meter"])
    order = [L["id"] for L in allL]
    on_idx = order.index(meter_on_from) if meter_on_from else 0
    answered = {"s1": "s1.l38", "s2": "s2.l25", "s3": "s5.l3"}
    beats = []
    for L in lines:
        a = L["shot"]
        b = RECIPES[a.get("r", "corner")](L, a)
        idx = order.index(L["id"])
        seg = segs[L["seg"]]
        v0 = before[L["id"]]
        v1 = float(L.get("meter", v0))
        mat = a.get("meter_at", "60%")
        kks = []
        # ---- meter
        if idx >= on_idx:
            mp = {"v": v0, "on": 1.0, "pulse": 0.0, "big": a.get("meter_big", 0.0)}
            sets = []
            if L["id"] == meter_on_from:
                mp["on"] = 0.0
                sets.append({"at": a["meter_in"], "dur": 0.5, "p": {"on": 1.0}})
            if a.get("meter_big_to") is not None:
                sets.append({"at": a.get("meter_big_at", "5%"), "dur": 0.45, "p": {"big": a["meter_big_to"]}})
            if abs(v1 - v0) > 0.01:
                sets.append({"at": mat, "dur": 0.7, "p": {"v": v1}})
                b["sfx"] = [f"click@{mat}"] + list(b["sfx"])
                if abs(v1 - v0) >= 8:
                    sets += [{"at": mat, "p": {"pulse": 1.0}}, {"at": mat, "dur": 0.9, "p": {"pulse": 0.0}}]
            if a.get("meter_pulse"):
                sets += [{"at": a["meter_pulse"], "p": {"pulse": 1.0}}, {"at": a["meter_pulse"], "dur": 0.9, "p": {"pulse": 0.0}}]
                b["sfx"] = [f"click@{a['meter_pulse']}"] + list(b["sfx"])
            if L["id"] == allL[-1]["id"]:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            kks.append({"id": "meter", "type": "ds_meter", "pos": [0, 0], "front": True, "p": mp, "set": sets})
        # ---- question chip
        chip = seg.get("chip")
        if chip:
            cp = {"text": chip, "on": 1.0, "done": 0.0}
            sets = []
            key = chip.startswith("QUESTION") and f"s{L['seg']}"
            if L["id"] == f"s{L['seg']}.l0":
                cp["on"] = 0.0
                sets.append({"at": 1.1, "dur": 0.35, "p": {"on": 1.0}})
            if key and answered.get(key) == L["id"]:
                sets.append({"at": "answered|40%", "dur": 0.35, "p": {"done": 1.0}})
            kks.append({"id": "chip", "type": "ds_qchip", "pos": [0, 0], "front": True, "p": cp, "set": sets})
        # ---- chapter card (<= 1.2 s), first line of a question segment
        if a.get("chapter"):
            n = chip.split()[1] if chip and chip.startswith("QUESTION") else ""
            kks.append({"id": "chap", "type": "ds_chapter", "pos": [0, 0], "front": True,
                        "p": {"on": 0.0, "kicker": f"QUESTION {n}" if n else "", "title": seg["chapter"].upper()},
                        "set": [{"at": 0.0, "dur": 0.15, "p": {"on": 1.0}}, {"at": 1.0, "dur": 0.2, "p": {"on": 0.0}}]})
            b["sfx"] = ["whoosh@0.02"] + list(b["sfx"])
        # ---- the three question chips
        if a.get("three"):
            sets = [{"at": at, "dur": 0.4, "p": {"n": float(i + 1)}} for i, at in enumerate(a["three_at"])]
            kks.append({"id": "three", "type": "ds_three", "pos": [0, 0], "front": True,
                        "p": {"n": 0.0, "items": a["three"]}, "set": sets})
        # ---- stamp / versus
        if a.get("stamp"):
            st = a["stamp"]
            kks.append({"id": "stamp", "type": "ds_stamp", "pos": [0, 0], "front": True,
                        "p": dict({"on": 0.0}, **{k: v for k, v in st.items() if k != "at"}),
                        "set": [{"at": st.get("at", "40%"), "dur": 0.25, "p": {"on": 1.0}}]})
        if a.get("vs"):
            kks.append({"id": "vs", "type": "ds_vs", "pos": [0, 0], "front": True, "p": dict({"on": 0.0}, **a["vs"]),
                        "set": [{"at": a["vs"].get("at", "10%"), "dur": 0.45, "p": {"on": 1.0}}]})
        # ---- the shoe (corner scenes): follows the meter
        if b.pop("shoe", False) and idx >= on_idx and not (L["id"] == meter_on_from and not a.get("shoe_enter")):
            hero = next((x for x in b["actors"] if x["id"] == "hero"), None)
            sp = {"v": v0, "enter": 1.0, "twitch": 0.0, "lift": 0.0, "k": a.get("shoe_k", 1.0)}
            sets = []
            if a.get("shoe_enter"):
                sp["enter"] = 0.0
                sets.append({"at": a["shoe_enter"], "dur": 0.55, "p": {"enter": 1.0}})
            if abs(v1 - v0) > 0.01:
                sets.append({"at": mat, "dur": 0.8, "p": {"v": v1}})
            if a.get("shoe_twitch"):
                sets += [{"at": a["shoe_twitch"], "p": {"twitch": 1.0}}, {"at": a["shoe_twitch"], "dur": 0.8, "p": {"twitch": 0.0}}]
            if a.get("shoe_lift"):
                sets.append({"at": a["shoe_lift"], "dur": 0.9, "p": {"lift": 1.0}})
            for k2 in ("tie", "spot"):
                if a.get("shoe_" + k2):
                    sp[k2] = a["shoe_" + k2]
            if hero is not None:
                b["actors"].append({"id": "shoe", "type": "ds_shoe", "pos": list(hero["pos"]), "s": hero["s"],
                                    "p": sp, "set": sets, "moves": copy.deepcopy(hero.get("moves", []))})
        # ---- card: always below the meter plate (top 120 px) and above the captions
        if L.get("card") and not a.get("no_card"):
            b["card"] = {"rows": _card_rows(L["card"]), "y": a.get("card_y", 150), "at": a.get("card_at", "30%")}
        # ---- end screen after the last line (kk_end, meter hidden)
        if L["id"] == allL[-1]["id"] and L in lines:
            kks.append({"id": "end", "type": "kk_end", "pos": [0, 0], "front": True,
                        "p": {"on": 0.0, **({"label": spec["end_label"].split(" (")[0].upper()} if spec.get("end_label") else {})},
                        "set": [{"at": "100%", "dur": 0.5, "p": {"on": 1.0}}]})
            b["pad"] = spec.get("end_hold", 12.0)
        b["actors"] = b["actors"] + kks
        b["say"] = L["say"]
        if L.get("tts"):
            b["tts"] = L["tts"]
        b.setdefault("pad", 0.1)
        if L["id"] in spec.get("pause_lines", []):
            b["pad"] = max(b["pad"], 0.55)
        b["kk_shots"] = b.pop("shots")
        b["ds_id"] = L["id"]
        beats.append(b)
    return beats


def drawn_spec(spec, lines):
    out = {k: spec[k] for k in ("voice", "rate", "pitch", "music", "music_db", "captions", "caption_y", "cut_whoosh",
                                "cap_key", "sfx_gain") if k in spec}
    out.update(beats=expand(spec, lines), recut=True, stage={},
               ds={"pause": spec.get("pause_lines", []), "music_out": spec.get("music_out", [])})
    for b in out["beats"]:   # the 16:9 camera conversion is for the macros only: these shots are already 16:9
        b["shots"] = b["kk_shots"]
    return out


# ================================================================================================ voice

def _vkey(text, voice, rate, pitch):
    return hashlib.sha1(json.dumps([text, voice, rate, pitch]).encode()).hexdigest()[:16]


def _good(mp3, words):
    if not os.path.exists(mp3) or os.path.getsize(mp3) < 2000 or not words:
        return False
    try:
        a = drawn.decode(mp3)
    except Exception:
        return False
    return len(a) > drawn.SR * 0.3 and float(np.sqrt(np.mean(a ** 2))) > 0.01


def voice_lines(beats, spec, work, cache):
    """Every beat's mp3 + words.json + .key in work (the names drawn.plan expects), from the per-text cache."""
    import asyncio
    import shutil
    from facts import speak
    os.makedirs(cache, exist_ok=True)
    os.makedirs(work, exist_ok=True)
    voice, rate, pitch = spec["voice"], spec["rate"], spec["pitch"]
    todo = []
    for i, b in enumerate(beats):
        text = b.get("tts", b["say"])
        c = os.path.join(cache, _vkey(text, voice, rate, pitch) + ".mp3")
        ok = os.path.exists(c + ".words.json") and _good(c, json.load(open(c + ".words.json")))
        if not ok:
            todo.append((text, c))
    todo = list(dict(todo).items())

    async def one(text, c, sem):
        async with sem:
            for k in range(5):
                tmp = c + ".tmp.mp3"
                try:
                    words = await speak(text, voice, tmp, rate, pitch)
                except Exception as e:   # noqa: BLE001  (NoAudioReceived, network)
                    print(f"  tts retry {k + 1}/5 ({type(e).__name__}): {text[:50]}", flush=True)
                    await asyncio.sleep(2 + 2 * k)
                    continue
                if _good(tmp, words):
                    os.replace(tmp, c)
                    json.dump(words, open(c + ".words.json", "w"))
                    return
                print(f"  tts retry {k + 1}/5 (empty/silent take): {text[:50]}", flush=True)
                await asyncio.sleep(2 + 2 * k)
            raise SystemExit(f"dontsquish: no usable voice after 5 tries for: {text!r}")

    async def run():
        sem = asyncio.Semaphore(4)
        await asyncio.gather(*(one(t_, c, sem) for t_, c in todo))
    if todo:
        print(f"voice: {len(todo)} new line(s)", flush=True)
        asyncio.run(run())
    for i, b in enumerate(beats):
        text = b.get("tts", b["say"])
        c = os.path.join(cache, _vkey(text, voice, rate, pitch) + ".mp3")
        mp3 = f"{work}/v{i:02d}.mp3"
        shutil.copy(c, mp3)
        shutil.copy(c + ".words.json", mp3 + ".words.json")
        open(mp3 + ".key", "w").write(drawn.line_key(b["say"], voice, rate, pitch))


# ================================================================================================ music envelope

_ENV = {}
_orig_mix, _orig_bed = drawn.mix_audio, drawn.music_bed


def _music_bed(kind, total, reveals=(), **kw):
    bed = _orig_bed(kind, total, reveals, **kw)
    env = _ENV.get("env")
    if env is None:
        return bed
    n = min(len(bed), len(env))
    e = env[:n] if bed.ndim == 1 else env[:n, None]
    out = bed.copy()
    rms0 = float(np.sqrt(np.mean(out ** 2)) + 1e-9)
    out[:n] = out[:n] * e
    rms1 = float(np.sqrt(np.mean(out ** 2)) + 1e-9)
    return out * (rms0 / rms1)   # drawn.mix_audio normalises the bed by its RMS: keep the dips as dips


def _mix_audio(spec, beats, total, path):
    SR = drawn.SR
    env = np.ones(int(total * SR) + SR, np.float32)
    ds = spec.get("ds", {})

    def ramp(t0, t1, g, r=0.25):
        a, b_ = int(t0 * SR), int(t1 * SR)
        if b_ <= a:
            return
        seg = np.full(b_ - a, g, np.float32)
        k = min(int(r * SR), (b_ - a) // 2)
        if k > 0:
            seg[:k] = np.linspace(1, g, k)
            seg[-k:] = np.linspace(g, 1, k)
        env[a:b_] = np.minimum(env[a:b_], seg)
    for b in beats:
        if b.get("ds_id") in ds.get("pause", []):   # dip under the half-second hold at the line's end
            ramp(b["t0"] + b["speech"] - 0.15, b["t0"] + b["dur"] + 0.2, 0.25, 0.12)
        if b.get("ds_id") in ds.get("music_out", []):   # the music drops out for this line
            ramp(b["t0"] - 0.1, b["t0"] + b["dur"] + 0.1, 0.0, 0.15)
    _ENV["env"] = env
    try:
        return _orig_mix(spec, beats, total, path)
    finally:
        _ENV.clear()


drawn.mix_audio = _mix_audio
drawn.music_bed = _music_bed


# ================================================================================================ render / stills

def _pick(spec, rng):
    if not rng:
        return spec["lines"]
    a, b = rng.split("-")
    return spec["lines"][int(a):int(b) + 1]


def _ep_dir(out):
    return os.path.dirname(os.path.abspath(out))


def render(spec_path, out, rng=None, work=None):
    spec = json.load(open(spec_path))
    lines = _pick(spec, rng)
    ds = drawn_spec(spec, lines)
    work = work or os.path.join(_ep_dir(out), ".work-" + os.path.splitext(os.path.basename(out))[0])
    os.makedirs(work, exist_ok=True)
    voice_lines(ds["beats"], ds, work, os.path.join(ROOT, "episodes", "longform-dont-squish-cellar-spider", ".voice-cache"))
    sp = os.path.join(work, "drawn_spec.json")
    json.dump(ds, open(sp, "w"), indent=1)
    sys.argv = ["drawn.py", sp, out, "--work", work]
    drawn.main()


def stills(spec_path, out, at, work):
    """at: ["s1.l14@0.6", ...]: plan only the needed lines (each as its own one-line plan), draw one frame each."""
    from PIL import Image
    spec = json.load(open(spec_path))
    ids = [x.split("@")[0] for x in at]
    ims = []
    for item in at:
        sid, fr = item.split("@")
        L = next(L for L in spec["lines"] if L["id"] == sid)
        ds = drawn_spec(spec, [L])
        w = os.path.join(work, sid)
        os.makedirs(w, exist_ok=True)
        voice_lines(ds["beats"], ds, w, os.path.join(ROOT, "episodes", "longform-dont-squish-cellar-spider", ".voice-cache"))
        dsx = drawn.drawn_macros.expand(ds)
        beats, total = drawn.plan(dsx, w)
        drawn.G.update(fps=30, beats=beats, rigs=drawn.rig_tracks(beats, 30), caps=drawn.caption_chunks(beats),
                       cap_px=ds.get("captions", 62), cap_y=ds.get("caption_y", 985), counter=None,
                       cap_key=set(ds.get("cap_key", ())), ticks=[], raw_out=False, nocap_out=False)
        f = int(float(fr) * beats[0]["speech"] * 30)
        arr = np.frombuffer(drawn.frame_at(f)[-1], np.uint8).reshape(H, W, 4)
        im = Image.fromarray(arr[..., [2, 1, 0]].copy())
        im.save(os.path.join(work, f"{sid}.png"))
        ims.append(im.resize((960, 540)))
    cols = 2
    rows = (len(ims) + 1) // 2
    sheet = Image.new("RGB", (960 * cols, 540 * rows), (0, 0, 0))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * 960, (i // cols) * 540))
    sheet.save(out, quality=88)
    print("stills:", out, ids)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build(sys.argv[2], sys.argv[3])
    elif cmd == "render":
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        ap.add_argument("spec")
        ap.add_argument("out")
        ap.add_argument("--lines")
        ap.add_argument("--work")
        x = ap.parse_args()
        render(x.spec, x.out, x.lines, x.work)
    elif cmd == "stills":
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        ap.add_argument("spec")
        ap.add_argument("out")
        ap.add_argument("--at", required=True)
        ap.add_argument("--work", default="/tmp/dontsquish-stills")
        x = ap.parse_args()
        stills(x.spec, x.out, x.at.split(","), x.work)
    elif cmd == "voice":
        spec = json.load(open(sys.argv[2]))
        ds = drawn_spec(spec, spec["lines"])
        voice_lines(ds["beats"], ds, "/tmp/dontsquish-voice-work",
                    os.path.join(ROOT, "episodes", "longform-dont-squish-cellar-spider", ".voice-cache"))
    else:
        raise SystemExit(__doc__)
