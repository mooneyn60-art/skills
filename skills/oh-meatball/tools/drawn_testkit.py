#!/usr/bin/env python3
"""A/B/C test kit for tools/drawn.py (11/3 frame-0 test: drawn v6 vs drawn + real-photo MIX vs drawn POV hook).

Run a spec through it instead of drawn.py (it patches drawn, then hands over to drawn.main()), or set an outline's
`renderer: drawn_testkit.py` so tools/drawn_quick.py uses it:
  python3 tools/drawn_testkit.py SPEC.json OUT.mp4 [--work DIR] [--stills 0.1,2.5]

Outline-line keys (carried through drawn_macros.expand by index; everything else stays v6):
  real: {"until": s | null, "shots": [{"file", "c": [fx, fy], "z": [z0, z1], "dur": s}], "credit": "text"}
        REAL licensed photos, full screen (cover crop centred on c, a share of the image), a slow push z0 -> z1 per
        shot; a shot whose z0 jumps above the previous shot's end is a punch-in. "until" (seconds into the line):
        the drawn scene (Meatball hopping in) takes over after it; null = the whole line. Shots without "dur" split
        the real span evenly. Files: absolute, or relative to env REAL_DIR (default /dev/shm/test3/real).
        Cards and captions still draw on top; Meatball and drawn animals are hidden while a photo is up.
  dark: s     the line opens in the dark (lights off) and the light snaps on at s with a white flash (POV hook)
  x_shots: [...]   replace the macro's camera shots for this line (drawn.py "shots" format)
  x_hero: {...}    merged into the macro's hero actor (e.g. "moves" that rush it at the camera, "front": true)
  x_mb: {...}      merged into the macro's Meatball dict
"""
import math
import os
import sys

import cairo
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn  # noqa: E402

W, H = drawn.W, drawn.H
REAL_DIR = os.environ.get("REAL_DIR", "/dev/shm/test3/real")
ZMAX = 1.6
_IMG = {}
_orig_expand = drawn.drawn_macros.expand


def expand(spec):
    out = _orig_expand(spec)
    if out is spec:
        return out
    for line, b in zip(spec.get("beats", []), out["beats"]):
        for k in ("real", "dark"):
            if k in line:
                b[k] = line[k]
        if "x_shots" in line:
            b["shots"] = line["x_shots"]
        if "x_mb" in line:
            b["mb"] = dict(b.get("mb", {}), **line["x_mb"])
        if "x_hero" in line:
            for a in b.get("actors", []):
                if a.get("id") == "hero":
                    a.update(line["x_hero"])
    return out


drawn.drawn_macros.expand = expand


def beat_at(T):
    beats = drawn.G["beats"]
    return beats[max(i for i, b in enumerate(beats) if b["t0"] <= T + 1e-9)]


def real_span(b):
    r = b.get("real")
    if not r:
        return 0.0
    u = r.get("until")
    return b["dur"] if u is None else min(float(u), b["dur"])


def real_on(b, t):
    return t < real_span(b)


def surf(path):
    """The photo pre-scaled to cover 1080x1920 at ZMAX (cached per worker)."""
    if path not in _IMG:
        im = Image.open(path if os.path.isabs(path) else os.path.join(REAL_DIR, path)).convert("RGB")
        k = max(W / im.width, H / im.height) * ZMAX
        im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS).convert("RGBA")
        _IMG[path] = drawn.pil_to_surface(im)
    return _IMG[path]


def paint_real(ctx, b, t):
    r = b["real"]
    span = real_span(b)
    shots = r["shots"]
    fixed = sum(s.get("dur", 0) for s in shots)
    free = [s for s in shots if "dur" not in s]
    each = max(0.0, span - fixed) / len(free) if free else 0.0
    t0 = 0.0
    shot, u = shots[-1], 1.0
    for s in shots:
        d = s.get("dur", each)
        if t < t0 + d:
            shot, u = s, (t - t0) / max(d, 1e-3)
            break
        t0 += d
    (sf, _buf) = surf(shot["file"])
    z0, z1 = shot.get("z", [1.0, 1.12])
    z = (z0 + (z1 - z0) * (u * u * (3 - 2 * u))) / ZMAX   # eased slow push
    sw, sh = sf.get_width() * z, sf.get_height() * z
    fx, fy = shot.get("c", [0.5, 0.5])
    x = min(0.0, max(W - sw, W / 2 - fx * sw))
    y = min(0.0, max(H - sh, H / 2 - fy * sh))
    ctx.save()
    ctx.identity_matrix()
    ctx.translate(x, y)
    ctx.scale(z, z)
    ctx.set_source_surface(sf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint()
    ctx.restore()
    if shot.get("credit") or r.get("credit"):   # CC BY credit, small, bottom left, under the app UI
        txt = shot.get("credit") or r.get("credit")
        ctx.save()
        ctx.identity_matrix()
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(22)
        ctx.move_to(24, H - 28)
        ctx.text_path(txt)
        ctx.set_source_rgba(0, 0, 0, 0.6)
        ctx.set_line_width(4)
        ctx.stroke_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.fill()
        ctx.restore()


def wrap_scene(fn):
    def scene(ctx, T, layer, p):
        b = beat_at(T)
        t = T - b["t0"]
        if real_on(b, t):
            return paint_real(ctx, b, t)
        fn(ctx, T, layer, p)
        if b.get("dark") is not None:   # lights off until "dark" s, then the light snaps on with a flash
            on = float(b["dark"])
            ctx.save()
            ctx.identity_matrix()
            if t < on:
                flick = 0.92 if int(t * 20) % 7 else 0.8
                ctx.rectangle(0, 0, W, H)
                ctx.set_source_rgba(0.02, 0.03, 0.06, flick)
                ctx.fill()
            elif t < on + 0.22:
                ctx.rectangle(0, 0, W, H)
                ctx.set_source_rgba(1, 1, 0.92, 0.7 * (1 - (t - on) / 0.22))
                ctx.fill()
            ctx.restore()
    return scene


for _k in list(drawn.SCENES):
    drawn.SCENES[_k] = wrap_scene(drawn.SCENES[_k])

_draw_actor, _draw_mb = drawn.draw_actor, drawn.draw_meatball


def draw_actor(ctx, cam, a, b, t, words):
    if real_on(b, t):
        return
    if b.get("dark") is not None and t < float(b["dark"]) and a.get("id") != "hero":
        return
    return _draw_actor(ctx, cam, a, b, t, words)


def draw_meatball(ctx, cam, b, st, t):
    if real_on(b, t):
        return
    return _draw_mb(ctx, cam, b, st, t)


drawn.draw_actor, drawn.draw_meatball = draw_actor, draw_meatball


if __name__ == "__main__":
    drawn.main()
