#!/usr/bin/env python3
"""16:9 "Kill It or Keep It?" long-form (Studio 11/3: helpful vs harmful bugs, a KEEP / MEH / KILL / DANGER
column board). Same locked drawn look and drawn_macros lines as the house Shorts, rendered at 1920x1080 by
tools/drawn.py; this module only adds the long-form layer:

  build OUTLINE.json SPEC.json      outline (segments of macro lines) -> one drawn.py spec + chapter list
  render SPEC.json OUT.mp4 --work D [--stills 1,2]   drawn.main() at 1920x1080 with the overlays below

Overlays (screen-space actors, drawn before the captions so the yellow key-word captions stay on top):
  kk_board   the four-column verdict board; the newest creature icon drops into its column with a stamp
  kk_hud     top-right danger meter (0-10, sourced score) + "BUG n OF 12" chip during a creature's segment
  kk_end     the end-screen area (dims the scene, two empty slots for YouTube's end-screen elements)
The portrait macro cameras are re-framed for 16:9 (zoom x CAM_K, lifted CAM_DY) so the floor stays in frame.
"""
import copy
import json
import math
import os
import sys

import cairo
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn  # noqa: E402

drawn.W, drawn.H = 1920, 1080
import drawn_macros  # noqa: E402
from drawn_kit import back_out, ease  # noqa: E402

W, H = 1920, 1080
FONT = os.path.join(os.path.dirname(HERE), "brand/fonts/Anton-Regular.ttf")
CAM_K, CAM_DY = 0.72, -30
ZOOM_MIN = 0.8
CAST_K = 1.2   # creatures a little bigger than in the Shorts: the animal, not Meatball, carries the frame
COLS = [("KEEP", "#3fb950"), ("MEH", "#8a94a6"), ("KILL", "#ff9f1c"), ("DANGER", "#e5383b")]
STAMP = {"KEEP": "KEEP IT", "MEH": "MEH", "KILL": "KILL IT", "DANGER": "DANGER"}
_IMG, _ICON = {}, {}


# ------------------------------------------------------------------------------------------------ text helpers

def _hex(c):
    return tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def text_img(text, px, color="#ffffff", stroke=None, rot=0.0):
    key = (text, px, color, stroke, rot)
    if key not in _IMG:
        f = ImageFont.truetype(FONT, px)
        sw = max(4, px // 11) if stroke is None else stroke
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=sw)
        im = Image.new("RGBA", (x1 - x0 + 12, y1 - y0 + 12), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((6 - x0, 6 - y0), text, font=f, fill=_hex(color) + (255,), stroke_width=sw,
                                stroke_fill=(17, 17, 17, 255))
        if rot:
            im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
        _IMG[key] = drawn.pil_to_surface(im)
    return _IMG[key]


def blit(ctx, key_surf, cx, cy, s=1.0, a=1.0):
    surf, _buf = key_surf
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    ctx.set_source_surface(surf, -surf.get_width() / 2, -surf.get_height() / 2)
    ctx.paint_with_alpha(max(0.0, min(1.0, a)))
    ctx.restore()


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def fill(ctx, rgb, a=1.0, line=0.0):
    c = [v / 255 for v in (_hex(rgb) if isinstance(rgb, str) else rgb)]
    ctx.set_source_rgba(*c, a)
    if line:
        ctx.fill_preserve()
        ctx.set_source_rgba(0.07, 0.07, 0.07, a)
        ctx.set_line_width(line)
        ctx.stroke()
    else:
        ctx.fill()


# ------------------------------------------------------------------------------------------------ icons

def icon(ic, box=(340, 170)):
    """A creature drawn once into a recording surface, scaled to fit a board slot (like drawn_tier._icon)."""
    key = (json.dumps(ic, sort_keys=True), box)
    if key not in _ICON:
        rec = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
        c = cairo.Context(rec)
        p = dict({"mood": "happy", "look": [0, 0]}, **ic.get("p", {}))
        if "cfg" in ic:
            drawn.ACTORS["creature"](c, 0.0, dict(p, cfg=ic["cfg"]))
        else:
            drawn.ACTORS[ic["type"]](c, 0.0, p)
        x, y, w, h = rec.ink_extents()
        k = min(box[0] / max(w, 1), box[1] / max(h, 1))
        _ICON[key] = (rec, k, x + w / 2, y + h / 2)
    return _ICON[key]


def draw_icon(ctx, ic, cx, cy, s=1.0, a=1.0, box=(340, 170)):
    rec, k, ox, oy = icon(ic, box)
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(k * s, k * s)
    ctx.translate(-ox, -oy)
    ctx.set_source_surface(rec, 0, 0)
    ctx.paint_with_alpha(a)
    ctx.restore()


# ------------------------------------------------------------------------------------------------ actors

def kk_board(ctx, t, p):
    """p: on (0..1), icons [{"ic", "col"}] (the last one is the newest), drop (0..1), stamp (0..1), heads (0..1
    header pop-in), title (bool)."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    ctx.rectangle(0, 0, W, H)
    fill(ctx, "#1b1724", min(1.0, on * 1.4))
    if on < 0.7:
        return
    ctx.save()   # a faint grid, so the board isn't a flat slab
    ctx.set_source_rgba(1, 1, 1, 0.04)
    ctx.set_line_width(2)
    for x in range(0, W, 80):
        ctx.move_to(x + (t * 6) % 80, 0)
        ctx.line_to(x + (t * 6) % 80, H)
    ctx.stroke()
    ctx.restore()
    if p.get("title", True):
        blit(ctx, text_img(p.get("title_text", "KILL IT OR KEEP IT?"), 74, "#ffd34d"), W / 2, 72)
    cols = [tuple(c) for c in p.get("cols", COLS)]   # only the piles the episode uses (v2 has no MEH)
    gap, top, bot = 30, 140, 905
    cw = (1690 - gap * (len(cols) - 1)) / len(cols)
    x0 = (W - (cw * len(cols) + gap * (len(cols) - 1))) / 2
    heads = p.get("heads", 1.0)
    icons = p.get("icons", [])
    newest = len(icons) - 1
    nlast = icons[-1]["col"] if icons else None
    for k, (name, col) in enumerate(cols):
        x = x0 + k * (cw + gap)
        rrect(ctx, x, top, cw, bot - top, 22)
        hl = icons and name == nlast and p.get("drop", 1.0) > 0
        fill(ctx, "#2c2838" if not hl else "#3a3448", 1.0, 6)
        if hl:   # the newest icon's column pulses its colour
            rrect(ctx, x, top, cw, bot - top, 22)
            c = [v / 255 for v in _hex(col)]
            ctx.set_source_rgba(*c, 0.16 + 0.08 * math.sin(t * 9))
            ctx.fill()
        u = back_out(min(1.0, max(0.0, heads * 4 - k * 0.6)))
        if u > 0:
            ctx.save()
            ctx.translate(x + cw / 2, top + 55)
            ctx.scale(u, u)
            rrect(ctx, -cw / 2 + 14, -42, cw - 28, 84, 18)
            fill(ctx, col, 1.0, 5)
            blit(ctx, text_img(name, 62), 0, 0)
            ctx.restore()
    for name in p.get("locked", []):
        if name in [c[0] for c in cols]:
            k = [c[0] for c in cols].index(name)
            blit(ctx, text_img("?", 260, "#ffd34d", 14), x0 + k * (cw + gap) + cw / 2, 540, 1.0 + 0.06 * math.sin(t * 6))
            blit(ctx, text_img("#1", 70, "#ffffff", 7), x0 + k * (cw + gap) + cw / 2, 760)
    slots = {}
    step, isc = 178, 1.0
    if p.get("fit"):   # opt-in (myth episodes): squeeze a column of 5+ icons so the last one stays on the board
        most = max([sum(1 for it in icons if it["col"] == c[0]) for c in cols] or [0])
        if most > 4:
            step = (bot - top - 260) / (most - 1)
            isc = step / 178
    for i, it in enumerate(icons):
        k = [c[0] for c in cols].index(it["col"])
        n = slots.get(it["col"], 0)
        slots[it["col"]] = n + 1
        cx = x0 + k * (cw + gap) + cw / 2
        cy = top + 200 + n * step
        a, s = 1.0, isc
        if i == newest:
            d = p.get("drop", 1.0)
            u = back_out(min(1.0, d * 1.05)) if d > 0 else 0.0
            cy = -200 + (cy + 200) * u
            a = min(1.0, d * 4)
            s = 1.12 * isc
        draw_icon(ctx, it["ic"], cx, cy + 4 * math.sin(t * 3 + i), s, a, box=(min(340, int(cw - 34)), 170))
    st = p.get("stamp", 0.0)
    if icons and st > 0:
        k = [c[0] for c in cols].index(nlast)
        cx = x0 + k * (cw + gap) + cw / 2
        sy = top + 200 + (slots[nlast] - 1) * step + 95 * isc   # just under the newest icon
        sc = 1.0 if st >= 1 else 1.9 - 0.9 * ease(st)
        blit(ctx, text_img(p.get("stamps", STAMP).get(nlast, nlast), 96, cols[k][1], 8, rot=10), min(max(cx, 260), W - 260), min(sy, 860), sc, min(1.0, st * 3))


def kk_hud(ctx, t, p):
    """p: score (0..10, may ramp), n, of, on."""
    if p.get("on", 1.0) <= 0:
        return
    ctx.identity_matrix()
    v = p.get("score", 0.0)
    if p.get("n") and not p.get("meter", True):   # myth episodes: no danger meter, only the "MYTH n OF 8" chip
        blit(ctx, text_img(f"{p.get('chip', 'BUG')} {p['n']} OF {p['of']}", 40, "#ffffff", 5), 150, 58)
        if p.get("loop"):   # opt-in: the open loop's reminder, top right, until it is paid off
            im = text_img(p["loop"], 36, "#ffd34d", 5)
            blit(ctx, im, W - 30 - im[0].get_width() / 2, 58)
        return
    x, y, w, h = W - 520, 24, 496, 96
    rrect(ctx, x, y, w, h, 20)
    fill(ctx, (18, 22, 40), 0.86, 4)
    blit(ctx, text_img("DANGER", 34, "#ffffff", 4), x + 78, y + 30)
    blit(ctx, text_img(f"{int(round(v))}/10", 46, "#ffd34d", 5), x + 78, y + 70)
    for i in range(10):
        bx = x + 156 + i * 33
        rrect(ctx, bx, y + 22, 27, 52, 6)
        f = max(0.0, min(1.0, v - i))
        hot = (int(80 + 17.5 * i), int(200 - 16 * i), 70)
        fill(ctx, (70, 74, 92), 1.0)
        if f > 0:
            rrect(ctx, bx, y + 22 + 52 * (1 - f), 27, 52 * f, 6)
            jit = 1.5 * math.sin(t * 40) if v >= 8 else 0
            ctx.translate(0, jit)
            fill(ctx, hot, 1.0)
            ctx.translate(0, -jit)
    if p.get("n"):
        blit(ctx, text_img(f"{p.get('chip', 'BUG')} {p['n']} OF {p['of']}", 40, "#ffffff", 5), 150, 58)


def kk_end(ctx, t, p):
    on = p.get("on", 0.0)
    if on <= 0:
        return
    ctx.identity_matrix()
    ctx.rectangle(0, 0, W, H)
    fill(ctx, "#120f18", 0.78 * on)
    a = min(1.0, on * 1.5)
    blit(ctx, text_img("WATCH NEXT", 92, "#ffd34d"), W / 2, 130, 1.0, a)
    if p.get("label"):   # opt-in (myth episode): name the video the end screen points at
        blit(ctx, text_img(p["label"], 46, "#ffffff", 5), W / 2, 214, 1.0, a)
    if p.get("ask"):   # opt-in: the comment question stays up under the end-screen slots
        blit(ctx, text_img(p["ask"], 66, "#ffd34d", 7), W / 2, 940, 1.0, a)
    rrect(ctx, 150, 260, 1000, 562, 26)   # video slot (YouTube end-screen element goes here)
    ctx.set_source_rgba(1, 1, 1, 0.9 * a)
    ctx.set_line_width(8)
    ctx.stroke()
    ctx.arc(1520, 541, 210, 0, 2 * math.pi)   # subscribe slot
    ctx.stroke()


def kk_count(ctx, t, p):
    """p: on (0..1), n (3/2/1, 0 = done), label. The ranked episode's prediction beat: the viewer locks a guess."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    a = min(1.0, on)
    cx, cy = W - 300, 470
    ctx.arc(cx, cy, 175, 0, 2 * math.pi)
    fill(ctx, (18, 22, 40), 0.88 * a, 8)
    n = int(p.get("n", 0))
    ring = (n / 3.0) if n else 0.0
    if ring > 0:
        ctx.set_source_rgba(1.0, 0.83, 0.3, a)
        ctx.set_line_width(16)
        ctx.arc(cx, cy, 160, -math.pi / 2, -math.pi / 2 + 2 * math.pi * ring)
        ctx.stroke()
    blit(ctx, text_img(p.get("label", "LOCK IT IN"), 54, "#ffffff", 6), cx, cy - 245, 1.0, a)
    if n:
        pulse = 1.0 + 0.08 * math.sin(t * 14)
        blit(ctx, text_img(str(n), 230, "#ffd34d", 12), cx, cy, pulse, a)
    else:
        blit(ctx, text_img("?", 230, "#ffd34d", 12), cx, cy, 1.0, a)


drawn.ACTORS.update(kk_board=kk_board, kk_hud=kk_hud, kk_end=kk_end, kk_count=kk_count)


# ------------------------------------------------------------------------------------------------ 16:9 cameras

_orig_expand = drawn_macros.expand


def _wide(c):
    # zoom floor: the rooms are drawn ~2600 px wide around the stage, so a wider pull-out shows the canvas edge
    return [c[0], c[1] + CAM_DY, round(max(c[2] * CAM_K, ZOOM_MIN), 4)] if isinstance(c, list) and len(c) == 3 else c


def expand(spec):
    kks = [b.get("kk", []) for b in spec["beats"]]   # the macros rebuild each line, so carry the overlays by index
    helm = [b.get("helmet") for b in spec["beats"]]   # opt-in line key (myth episode): Meatball's bubble helmet
    shots = [b.get("kk_shots") for b in spec["beats"]]   # opt-in line key: this line's shots, already in 16:9 camera terms
    out = _orig_expand(spec)
    for b, h in zip(out["beats"], helm):
        if h is not None and isinstance(b.get("mb"), dict):
            b["mb"]["helmet"] = bool(h)
    for b, kk, sh in zip(out["beats"], kks, shots):
        if sh:
            b["shots"] = copy.deepcopy(sh)
        for s in ([] if sh else b.get("shots", [])):
            for k in ("cam", "to"):
                if k in s:
                    s[k] = _wide(s[k])
        b.pop("kk", None)
        # the HUD meter is the only danger gauge: drop the macros' dial gag (drawn_gags "g.meter")
        b["actors"] = [a for a in b.get("actors", []) if a.get("type") != "g.meter"] + kk   # the long-form overlays, after the macro's actors
    return out


drawn_macros.expand = expand
_orig_auto_gag = drawn_macros.drawn_acting.auto_gag


def auto_gag(say, skip=()):
    """The macros' word-picked gag, with the dial ("meter") swapped for an alarm mark: the HUD is the gauge here."""
    g = _orig_auto_gag(say, skip)
    if isinstance(g, dict) and "meter" in g:
        return {"mark": "alarm", **({"at": g["at"]} if "at" in g else {})}
    return g


drawn_macros.drawn_acting.auto_gag = auto_gag
drawn.RECUT_ZOOM = 1.12


# ------------------------------------------------------------------------------------------------ build

def build(outline, out_spec):
    o = json.load(open(outline))
    beats, icons, chapters = [], [], []
    segs = o["segments"]
    nseg = sum(1 for s in segs if s.get("tier"))
    cast_k = o.get("cast_k", CAST_K)   # outline override: v2 (11/5) runs the animals bigger
    used = {s.get("tier") for s in segs}
    piles = o.get("piles", COLS)   # outline override (myth episodes: MYTH / TRUE); default = the KEEP/KILL board
    cols = [list(c) for c in piles if c[0] in used] or [list(c) for c in piles]
    board_x = {k2: o[k2] for k2 in ("title_text", "stamps", "fit") if k2 in o}
    hud_x = {k2: o[k2] for k2 in ("meter", "chip") if k2 in o}
    k = 0
    loop_txt, loop_on = o.get("loop_chip"), False   # opt-in: a line's "loop_on"/"loop_off" shows/hides the reminder chip
    for seg in segs:
        if seg.get("chapter"):
            chapters.append((len(beats), seg["chapter"]))
        if seg.get("tier"):
            k += 1
        for j, ln in enumerate(seg["lines"]):
            b = {key: v for key, v in ln.items() if key not in ("board", "end", "hud", "hud_demo", "lockin", "pause",
                                                                "loop_on", "loop_off")}
            if ln.get("loop_on"):
                loop_on = True
            if ln.get("loop_off"):
                loop_on = False
            if seg.get("cast"):
                b.setdefault("cast", seg["cast"])
            if b.get("cast") and "s" in b["cast"]:
                b["cast"] = dict(b["cast"], s=round(b["cast"]["s"] * cast_k, 3))
            if seg.get("scene") and "scene" not in b:
                b["scene"] = seg["scene"]
                b["scene_p"] = seg.get("scene_p", {})
            kk = []
            if ln.get("hud_demo"):   # the intro shows the scale: the meter runs 0 -> 10 under "danger score"
                kk.append({"id": "hud", "type": "kk_hud", "pos": [0, 0], "front": True, "p": {"score": 0.0},
                           "set": [{"at": "30%", "dur": 1.6, "p": {"score": 10.0}}]})
            if seg.get("tier"):
                hud = {"id": "hud", "type": "kk_hud", "pos": [0, 0], "front": True,
                       "p": {"score": seg.get("danger", 0), "n": k, "of": nseg, **hud_x}}
                if j == 0:   # the meter fills on the name line
                    hud["p"]["score"] = 0.0
                    hud["set"] = [{"at": "45%", "dur": 0.9, "p": {"score": float(seg.get("danger", 0))}}]
                if loop_txt and loop_on:
                    hud["p"]["loop"] = loop_txt
                kk.append(hud)
            bd = ln.get("board")
            if bd:
                if bd.get("add"):
                    icons.append({"ic": seg["icon"], "col": seg["tier"]})
                off = bd.get("off", "62%")
                p = {"cols": cols, "on": 0.0, "icons": list(icons) if bd.get("add") else list(icons), "drop": 0.0 if bd.get("add") else 1.0,
                     "stamp": 0.0, "heads": 0.0 if bd.get("heads") else 1.0, **board_x}
                if bd.get("locked"):
                    p["locked"] = bd["locked"]
                at = bd.get("at", 0.0)
                sets = [{"at": at, "dur": 0.12, "p": {"on": 1.0}}]
                if bd.get("heads"):
                    sets.append({"at": at, "dur": 1.6, "p": {"heads": 1.0}})
                if bd.get("add"):
                    sets += [{"at": bd.get("drop_at", "12%"), "dur": 0.55, "p": {"drop": 1.0}},
                             {"at": bd.get("stamp_at", "30%"), "dur": 0.2, "p": {"stamp": 1.0}}]
                if off:
                    sets.append({"at": off, "p": {"on": 0.0}})
                kk.append({"id": "board", "type": "kk_board", "pos": [0, 0], "front": True, "p": p, "set": sets})
            pz = ln.get("pause")
            if pz:   # a pause-and-reveal beat: the "?" ring hangs in the line's closing silence (its pad); no countdown
                pz = pz if isinstance(pz, dict) else {}
                kk.append({"id": "count", "type": "kk_count", "pos": [0, 0], "front": True,
                           "p": {"on": 0.0, "n": 0, "label": pz.get("label", "REALLY?")},
                           "set": [{"at": pz.get("at", "100%"), "dur": 0.15, "p": {"on": 1.0}}]})
            lk = ln.get("lockin")
            if lk:   # {"words": ["three", "two", "one"]} or true
                ws = lk.get("words", ["three", "two", "one"]) if isinstance(lk, dict) else ["three", "two", "one"]
                pct = ["55%", "70%", "85%"]
                sets = [{"at": lk.get("at", "8%") if isinstance(lk, dict) else "8%", "dur": 0.25, "p": {"on": 1.0}}]
                sets += [{"at": f"{w}|{q}", "p": {"n": 3 - i}} for i, (w, q) in enumerate(zip(ws, pct))]
                kk.append({"id": "count", "type": "kk_count", "pos": [0, 0], "front": True,
                           "p": {"on": 0.0, "n": 0, "label": lk.get("label", "LOCK IT IN") if isinstance(lk, dict) else "LOCK IT IN"},
                           "set": sets})
            if ln.get("end"):
                kk.append({"id": "end", "type": "kk_end", "pos": [0, 0], "front": True,
                           "p": {"on": 0.0, **({"label": o["end_label"]} if o.get("end_label") else {}),
                                 **({"ask": o["end_ask"]} if o.get("end_ask") else {})},
                           "set": [{"at": "100%", "dur": 0.5, "p": {"on": 1.0}}]})
            if kk:
                b["kk"] = kk
            beats.append(b)
    spec = {k2: o[k2] for k2 in ("voice", "rate", "pitch", "music", "music_db", "captions", "caption_y", "cut_whoosh",
                                 "cap_key", "sfx_gain") if k2 in o}
    spec.update(stage=o["stage"], beats=beats, recut=True, _note="Built by tools/drawn_keepkill.py build from " +
                os.path.basename(outline), chapters=[[i, c] for i, c in chapters])
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    print(f"{out_spec}: {len(beats)} lines, {sum(len(b['say'].split()) for b in beats)} words, {nseg} creatures")


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3])
    else:
        sys.argv.pop(1)   # "render"
        drawn.main()
