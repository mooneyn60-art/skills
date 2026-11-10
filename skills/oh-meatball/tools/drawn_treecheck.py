#!/usr/bin/env python3
"""16:9 "tree check" long-form (Christmas-tree bugs, publish by 2026-11-24): the "Don't squish it" format layer
(tools/drawn_dontsquish.py: recipes, chips, chapter cards, stamps, card placement, per-line voice cache with retries,
music envelope with dips and a drop-out, 12 s end screen, two-pass loudness) with two format overlays of its own:

  tc_panic   PANIC METER: the same top bar as the SQUISH/SPARE meter, on a 0-10 scale from CALM (green, left) to
             PANIC (red, right); the marker eases to each line's `panic` with a tick ("click"), the bar swells on a
             move of 2 or more, the plate blinks red at 8+ and glows green at 1 or less. No digits on it.
             p: v (0..10), on (slide in), swell, pulse, big (0..1: centre frame, bigger)
  tc_list    TREE CHECK: a compact checklist panel, top right, that appears with the first `check`; each `check`
             adds its numbered item (sorted by number) with a tick, or replaces the item with the same number.
             In the segment "The tree check" it grows to fill the right half (big 0..1), the ticks clear, and each
             step highlights (h<n>) and ticks (t<n>) as it is narrated.
             p: items [[n, text, old_text|None]], on, big, t1..t5 (ticks), h1..h5 (highlight), n1..n5 (new: 0 =
             not shown yet, 1 = settled), r1..r5 (0..1 old text -> new text)
  tc_stamps  the cold open's four verdict stamps in a row (IGNORE x6, VACUUM x1, CLIP x1, CHECK THE TRUNK x1)

Pictures: tools/drawn_tc_art.py. Shots (one per line): tools/drawn_tc_shots.py.

  build OUTLINE.json SPEC.json        outline -> spec (every `say` kept; ids s<seg>.l<line>; a shot per line)
  render SPEC.json OUT.mp4 [--lines A-B] [--work DIR]
  linesheet SPEC.json OUT.jpg [ids]   one frame per line (60% of its speech), tiled; part sheets of 36 lines
  voice SPEC.json                     voice every line now (cached in the episode's .voice-cache)
"""
import copy
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_dontsquish as ds  # noqa: E402  (registers the format layer, the 1920x1080 renderer and the music envelope)
import drawn  # noqa: E402
import drawn_keepkill as kk  # noqa: E402
import drawn_tc_art as tca  # noqa: E402
from drawn_kit import back_out, ease, hexc, stroke  # noqa: E402

W, H = 1920, 1080
ROOT = os.path.dirname(HERE)
EP = os.path.join(ROOT, "episodes", "longform-christmas-tree-check")
CACHE = os.path.join(EP, ".voice-cache")
RED, GREEN, YEL = ds.RED, ds.GREEN, ds.YEL
TTS = {r"\bAdelgids\b": "uh-DELL-jids"}   # pronunciation respellings (captions always use `say`)


# ================================================================================================ PANIC METER

def _lerpc(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def _vcol(v):
    """Marker colour by value: green (0) -> yellow (5) -> red (10)."""
    g, y, r = hexc(GREEN), hexc(YEL), hexc(RED)
    u = max(0.0, min(1.0, v / 10.0))
    return _lerpc(g, y, u * 2) if u < 0.5 else _lerpc(y, r, (u - 0.5) * 2)


def _calm_face(ctx, cx, cy, k, col):
    ctx.arc(cx, cy, 20 * k, 0, 2 * math.pi)
    kk.fill(ctx, col, 1.0, 4)
    for s in (-1, 1):
        ctx.arc(cx + s * 7 * k, cy - 4 * k, 3 * k, 0, 2 * math.pi)
        ctx.set_source_rgb(0.07, 0.07, 0.07)
        ctx.fill()
    ctx.new_sub_path()
    ctx.arc(cx, cy + 2 * k, 10 * k, 0.2 * math.pi, 0.8 * math.pi)
    ctx.set_line_width(3.5 * k)
    ctx.stroke()


def _alarm(ctx, cx, cy, k, col, t):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(0.12 * math.sin(t * 20))
    ctx.move_to(0, -24 * k)
    ctx.line_to(23 * k, 18 * k)
    ctx.line_to(-23 * k, 18 * k)
    ctx.close_path()
    kk.fill(ctx, col, 1.0, 4)
    kk.blit(ctx, kk.text_img("!", int(30 * k), "#111111", 0), 0, 3 * k)
    ctx.restore()


def tc_panic(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    big = ease(p.get("big", 0.0))
    v = max(0.0, min(10.0, p.get("v", 9.0)))
    pulse = max(0.0, p.get("pulse", 0.0))
    sw = max(0.0, p.get("swell", 0.0))
    sc = (1.0 + 0.5 * big) * (1.0 + 0.13 * sw)
    cy = 66 + (330 - 66) * big - 170 * (1 - ease(min(1.0, on))) + 6 * sw
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(sc, sc)
    alarm = v >= 7.95
    calm = v <= 1.05
    blink = 0.5 + 0.5 * math.sin(t * 9) if alarm else 0.0
    kk.rrect(ctx, -555, -44, 1110, 88, 44)
    kk.fill(ctx, (18, 22, 40), 0.9, 0)
    kk.rrect(ctx, -555, -44, 1110, 88, 44)
    if alarm:
        ctx.set_source_rgba(0.9, 0.22 + 0.5 * (1 - blink), 0.23, 1)
    elif calm:
        ctx.set_source_rgba(0.25, 0.73, 0.31, 1)
    else:
        ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(4 + 4 * blink + (3 if calm else 0))
    ctx.stroke()
    _calm_face(ctx, -505, 0, 1.0, GREEN)
    kk.blit(ctx, kk.text_img("CALM", 40, GREEN, 5), -405, 0)
    ks = 1.0 + (0.12 * blink if alarm else 0.0)
    kk.blit(ctx, kk.text_img("PANIC", 40, RED, 5), 400, 0, ks)
    _alarm(ctx, 503, -2, 1.0, RED, t if alarm else 0.0)
    x0, x1, bh = -320, 320, 30
    kk.rrect(ctx, x0, -bh / 2, x1 - x0, bh, bh / 2)
    import cairo
    g = cairo.LinearGradient(x0, 0, x1, 0)
    for u, c in ((0.0, GREEN), (0.5, YEL), (1.0, RED)):
        r, gg, b = hexc(c)
        g.add_color_stop_rgb(u, r, gg, b)
    ctx.set_source(g)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.07, 0.07, 0.07)
    ctx.set_line_width(4)
    ctx.stroke()
    for k in range(11):   # scale ticks, no digits
        x = x0 + (x1 - x0) * k / 10
        ctx.move_to(x, bh / 2 + 3)
        ctx.line_to(x, bh / 2 + (12 if k % 5 == 0 else 7))
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.set_line_width(3)
        ctx.stroke()
    mx = x0 + (x1 - x0) * v / 10.0
    if mx < x1:
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
    col = _vcol(v)
    ctx.save()
    ctx.translate(mx, 0)
    ctx.scale(mk, mk)
    kk.rrect(ctx, -13, -30, 26, 60, 10)
    kk.fill(ctx, (int(col[0] * 255), int(col[1] * 255), int(col[2] * 255)), 1.0, 5)
    ctx.move_to(-12, -40)
    ctx.line_to(12, -40)
    ctx.line_to(0, -28)
    ctx.close_path()
    kk.fill(ctx, "#ffffff", 1.0, 4)
    ctx.restore()
    ctx.restore()


# ================================================================================================ TREE CHECK list

_FONTS = {}


def _wrap(text, px, width):
    from PIL import ImageFont
    f = _FONTS.get(px) or _FONTS.setdefault(px, ImageFont.truetype(kk.FONT, px))
    out, cur = [], ""
    for w in text.split(" "):
        nxt = (cur + " " + w).strip()
        if cur and f.getlength(nxt) > width:
            out.append(cur)
            cur = w
        else:
            cur = nxt
    if cur:
        out.append(cur)
    return out


def _ltext(ctx, s, x, y, px, color, a=1.0):
    """Left-aligned text, top-left at (x, y)."""
    im = kk.text_img(s, int(px), color, 0)
    w, h = im[0].get_width(), im[0].get_height()
    kk.blit(ctx, im, x + w / 2 - 6, y + h / 2 - 6, 1.0, a)
    return h - 12


CMP = {"x": 1476, "y": 126, "w": 426, "hpx": 34, "px": 25, "box": 28, "tx": 60, "lh": 31, "gap": 10, "pad": 16}
BIG = {"x": 976, "y": 128, "w": 912, "hpx": 72, "px": 50, "box": 52, "tx": 96, "lh": 60, "gap": 28, "pad": 30}


def _lay(u):
    return {k: CMP[k] + (BIG[k] - CMP[k]) * u for k in CMP}


def _item_rows(items, L):
    rows = []
    for n, text, old in items:
        rows.append((n, _wrap(text, int(L["px"]), L["w"] - L["tx"] - L["pad"] - 6),
                     _wrap(old, int(L["px"]), L["w"] - L["tx"] - L["pad"] - 6) if old else None))
    return rows


def tc_list(ctx, t, p):
    on = p.get("on", 0.0)
    items = p.get("items") or []
    if on <= 0.01 or not items:
        return
    ctx.identity_matrix()
    u = ease(min(1.0, max(0.0, p.get("big", 0.0))))
    L = _lay(u)
    dx = (1 - ease(min(1.0, on))) * 520
    x, y, w = L["x"] + dx, L["y"], L["w"]
    rows = _item_rows(items, L)
    # height of the panel: header + each shown row (a row grows in as it arrives: n<k> 0..1)
    hh = L["hpx"] + L["pad"] * 1.6
    heights = []
    for n, lines, old in rows:
        g = ease(min(1.0, p.get(f"n{n}", 1.0) * 2.0))
        r = p.get(f"r{n}", 1.0)
        nl = len(lines) if (old is None or r >= 0.5) else max(len(old), 1)
        heights.append(g * (max(nl, 1) * L["lh"] + L["gap"]))
    total = hh + sum(heights) + L["pad"] * 0.6
    if u > 0.01:   # big mode: the panel fills the right half
        total = total + (900 - total) * u
    kk.rrect(ctx, x, y, w, total, 22 + 10 * u)
    kk.fill(ctx, (18, 22, 40), 0.9, 4 + 2 * u)
    _ltext(ctx, "TREE CHECK", x + L["pad"], y + L["pad"] * 0.8, L["hpx"], YEL)
    yy = y + hh
    for (n, lines, old), hgt in zip(rows, heights):
        if hgt < 1:
            continue
        g = ease(min(1.0, p.get(f"n{n}", 1.0) * 2.0))
        a = min(1.0, p.get(f"n{n}", 1.0) * 2.0)
        hi = max(0.0, min(1.0, p.get(f"h{n}", 0.0)))
        r = p.get(f"r{n}", 1.0)
        fl = max(0.0, 1.0 - abs(r - 0.5) * 4) if old is not None else 0.0   # flash while the text is replaced
        newfl = max(0.0, 1.0 - abs(p.get(f"n{n}", 1.0) - 0.6) * 3) if p.get(f"n{n}", 1.0) < 1 else 0.0
        glow = max(hi, fl, newfl)
        ctx.save()
        ctx.rectangle(x, yy - 4, w, hgt + 4)
        ctx.clip()
        show = lines if (old is None or r >= 0.5) else old
        rh = max(len(show), 1) * L["lh"]
        if glow > 0.01:
            kk.rrect(ctx, x + L["pad"] * 0.4, yy - 6, w - L["pad"] * 0.8, rh + 10, 14)
            kk.fill(ctx, YEL, 0.95 * glow, 0)
        bx, by, bs = x + L["pad"], yy + (L["lh"] - L["box"]) / 2 + 2, L["box"]
        kk.rrect(ctx, bx, by, bs, bs, 6)
        kk.fill(ctx, "#ffffff", a, 3 + 2 * u)
        tk = max(0.0, min(1.0, p.get(f"t{n}", 1.0)))
        if tk > 0.01:
            s = back_out(tk)
            ctx.save()
            ctx.translate(bx + bs / 2, by + bs / 2)
            ctx.scale(s * bs / 30, s * bs / 30)
            stroke(ctx, [(-11, 0), (-3, 9), (14, -12)], 9, color=(0.07, 0.07, 0.07))
            stroke(ctx, [(-11, 0), (-3, 9), (14, -12)], 5.5, color=hexc(GREEN))
            ctx.restore()
        for k, ln in enumerate(show):
            ty = yy + k * L["lh"] + (L["lh"] - L["px"] * 1.18) / 2
            if glow < 0.99:
                _ltext(ctx, ln, x + L["tx"] - dx * 0, ty, L["px"], "#ffffff", a * (1 - glow))
            if glow > 0.01:
                _ltext(ctx, ln, x + L["tx"], ty, L["px"], "#1a1a1a", a * glow)
        ctx.restore()
        yy += hgt


def tc_stamps(ctx, t, p):
    """The cold open's four verdict stamps in a row; p: n (0..4 how many are down), items [[text, count, color]]."""
    n = p.get("n", 0.0)
    if n <= 0.01:
        return
    ctx.identity_matrix()
    items = p.get("items", [])
    xs = p.get("xs") or [300 + i * 440 for i in range(len(items))]
    for i, (txt, cnt, col) in enumerate(items):
        u = max(0.0, min(1.0, (n - i) * 2.0))
        if u <= 0:
            continue
        ds.ds_stamp(ctx, t, {"on": u, "text": txt, "color": col, "x": xs[i], "y": p.get("y", 560), "px": p.get("px", 74),
                             "rot": [-8, 6, -5, 7][i % 4]})
        if u >= 1:
            ctx.identity_matrix()
            kk.blit(ctx, kk.text_img(cnt, 80, "#ffffff", 8), xs[i], p.get("y", 560) + 120)


OVERLAYS = {"tc_panic": tc_panic, "tc_list": tc_list, "tc_stamps": tc_stamps}
drawn.ACTORS.update(OVERLAYS)
drawn.ACTORS.update(tca.ACTORS)
drawn.SCENES.update(tca.SCENES)


# ================================================================================================ build

def build(outline, out_spec):
    import drawn_tc_shots
    shots = drawn_tc_shots.table()
    o = json.load(open(outline))
    old = {}
    if os.path.exists(out_spec):
        for ln in json.load(open(out_spec)).get("lines", []):
            old[ln["id"]] = ln
    lines, todo = [], 0
    for si, seg in enumerate(o["segments"]):
        for li, ln in enumerate(seg["lines"]):
            sid = f"s{si}.l{li}"
            L = dict(ln, id=sid, seg=si)
            prev = old.get(sid)
            if prev and prev.get("shot", {}).get("_keep"):
                L["shot"] = prev["shot"]
            elif sid in shots:
                L["shot"] = copy.deepcopy(shots[sid])
            else:
                todo += 1
                L["shot"] = {"r": "scene", "scene": "ds_board_bg", "cam": [0, 0, 1.0], "_todo": True,
                             "actors": [ds.actor("todo", "ds_label", [0, 0], 1.0, {"text": "TODO " + sid, "px": 80})]}
            tts = L["say"]
            for pat, rep in TTS.items():
                tts = re.sub(pat, rep, tts)
            if tts != L["say"]:
                L["tts"] = tts
            lines.append(L)
    segs = [{k: v for k, v in s.items() if k != "lines"} for s in o["segments"]]
    spec = {"_note": "Built by tools/drawn_treecheck.py build from " + os.path.basename(outline) +
                     ". Each line: id (s<seg>.l<line>), the outline fields (say/vis/card/check/panic/src) and shot "
                     "(recipe + args, tools/drawn_tc_shots.py). `tts` = a pronunciation respelling (captions use say).",
            "voice": o.get("voice", "en-US-AndrewMultilingualNeural"), "rate": o.get("rate", "+10%"),
            "pitch": o.get("pitch", "+3Hz"), "music": "mystery", "music_db": -15, "captions": 62, "caption_y": 985,
            "cut_whoosh": True, "sfx_gain": 0.22, "panic_start": o.get("panic_start", 9),
            "cap_key": ["tree", "christmas", "marshmallow", "eggs", "hundred", "thousand", "twenty-five", "mantis",
                        "aphid", "aphids", "tick", "ticks", "six", "eight", "spiders", "nine", "one", "two", "three",
                        "four", "five", "seven", "vacuum", "squash", "spray", "shake", "clip", "nest", "trunk",
                        "lanternfly", "fire", "ignore", "never", "purple", "panic", "starve", "evergreen"],
            "pause_lines": ["s1.l13", "s5.l0", "s7.l0"], "music_out": ["s6.l0"],
            "end_hold": 12.0, "end_label": o.get("end_screen_video"), "segments": segs, "titles": o.get("titles"),
            "pinned_comment": o.get("pinned_comment"), "tree_check_final": o.get("tree_check_final"), "lines": lines}
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    print(f"{out_spec}: {len(lines)} lines, {sum(len(L['say'].split()) for L in lines)} words, "
          f"{len(lines) - todo} with hand-made shots, {todo} TODO")


# ================================================================================================ expand

def _num(check):
    return int(check.split(".")[0])


def states(spec):
    """Per line id: panic before/after, list items before/after, list visible before."""
    v = float(spec.get("panic_start", 9))
    items = {}
    out = {}
    seen_meter = False
    for L in spec["lines"]:
        st = {"v0": v, "items0": dict(items), "meter_on0": seen_meter}
        if L["shot"].get("meter_in"):
            seen_meter = True
        if "panic" in L:
            v = float(L["panic"])
        if L.get("check"):
            items[_num(L["check"])] = L["check"]
        st.update(v1=v, items1=dict(items), meter_on1=seen_meter)
        out[L["id"]] = st
    return out


def _seg_title(seg):
    return seg["chapter"].upper()


def expand(spec, lines):
    segs = spec["segments"]
    allL = spec["lines"]
    order = [L["id"] for L in allL]
    ST = states(spec)
    big_seg = next((i for i, s in enumerate(segs) if s["chapter"].lower() == "the tree check"), None)
    beats = []
    for L in lines:
        a = L["shot"]
        b = ds.RECIPES[a.get("r", "scene")](L, a)
        if a.get("norecut"):
            b["norecut"] = True
        st = ST[L["id"]]
        seg = segs[L["seg"]]
        last = L["id"] == order[-1]
        kks = []
        # ---- PANIC METER
        if st["meter_on1"]:
            v0, v1 = st["v0"], st["v1"]
            mat = a.get("meter_at", "60%")
            mp = {"v": v0, "on": 1.0, "pulse": 0.0, "big": a.get("meter_big", 0.0), "swell": 0.0}
            sets = []
            if not st["meter_on0"]:
                mp["on"] = 0.0
                sets.append({"at": a["meter_in"], "dur": 0.55, "p": {"on": 1.0}})
                b["sfx"] = [f"whoosh@{a['meter_in']}"] + list(b["sfx"])
            if a.get("meter_big_to") is not None:
                sets.append({"at": a.get("meter_big_at", "5%"), "dur": 0.45, "p": {"big": a["meter_big_to"]}})
            if a.get("meter_big_back"):
                sets.append({"at": a["meter_big_back"], "dur": 0.45, "p": {"big": 0.0}})
            if abs(v1 - v0) > 0.01:
                sets.append({"at": mat, "dur": 0.7, "p": {"v": v1}})
                b["sfx"] = [f"click@{mat}"] + list(b["sfx"])
                if abs(v1 - v0) >= 2:
                    sets += [{"at": mat, "p": {"pulse": 1.0}}, {"at": mat, "dur": 0.9, "p": {"pulse": 0.0}}]
                    if not a.get("meter_big") and a.get("meter_big_to") is None:
                        sets.insert(0, {"at": mat, "dur": 0.3, "p": {"swell": 1.0}})
                        sets.append({"at": ds._after(mat, 1.25), "dur": 0.4, "p": {"swell": 0.0}})
            if last:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            kks.append({"id": "meter", "type": "tc_panic", "pos": [0, 0], "front": True, "p": mp, "set": sets})
        # ---- STOWAWAY chip (or a line's own chip text)
        chip = a.get("chip_text") or seg.get("chip")
        if chip:
            cp = {"text": chip, "on": 1.0, "done": 0.0}
            sets = []
            first_of_seg = L["id"] == f"s{L['seg']}.l0"
            if a.get("chip_at"):
                cp["on"] = 0.0
                sets.append({"at": a["chip_at"], "dur": 0.35, "p": {"on": 1.0}})
            elif first_of_seg:
                cp["on"] = 0.0
                sets.append({"at": 1.15, "dur": 0.35, "p": {"on": 1.0}})
            if a.get("chip_done"):
                sets.append({"at": a["chip_done"], "dur": 0.35, "p": {"done": 1.0}})
            kks.append({"id": "chip", "type": "ds_qchip", "pos": [0, 0], "front": True, "p": cp, "set": sets})
        # ---- TREE CHECK list
        i0, i1 = st["items0"], st["items1"]
        if i1:
            is_big = big_seg is not None and L["seg"] == big_seg
            was_big = big_seg is not None and L["seg"] == big_seg + 1 and L["id"] == f"s{L['seg']}.l0"
            items = []
            lp = {"on": 1.0 if i0 else 0.0, "big": 1.0 if is_big else (1.0 if was_big else 0.0)}
            sets = []
            cat = a.get("check_at", "45%")
            for n in sorted(i1):
                old = i0.get(n) if i0.get(n) != i1[n] else None
                items.append([n, i1[n], old])
                lp[f"t{n}"] = 1.0
                lp[f"h{n}"] = 0.0
                lp[f"n{n}"] = 1.0 if n in i0 else 0.0
                lp[f"r{n}"] = 0.0 if old else 1.0
                if n not in i0:
                    sets.append({"at": cat, "dur": 0.7, "p": {f"n{n}": 1.0}})
                elif old:
                    sets.append({"at": cat, "dur": 0.7, "p": {f"r{n}": 1.0}})
            if L.get("check"):
                b["sfx"] = [f"tink@{cat}"] + list(b["sfx"])
            if not i0:
                sets.insert(0, {"at": cat, "dur": 0.45, "p": {"on": 1.0}})
            if is_big:
                stepn = a.get("list_step")
                first_big = L["id"] == f"s{big_seg}.l0"
                for n in sorted(i1):
                    lp[f"t{n}"] = 0.0 if first_big else (1.0 if (stepn and n < stepn) else 0.0)
                if first_big:
                    lp["big"] = 0.0
                    for n in sorted(i1):
                        lp[f"t{n}"] = 1.0
                    sets += [{"at": "5%", "dur": 0.6, "p": {"big": 1.0}}]
                    sets += [{"at": "45%", "dur": 0.3, "p": {f"t{n}": 0.0}} for n in sorted(i1)]
                if stepn:
                    sets += [{"at": "3%", "dur": 0.3, "p": {f"h{stepn}": 1.0}},
                             {"at": a.get("tick_at", "70%"), "dur": 0.35, "p": {f"t{stepn}": 1.0}}]
                    b["sfx"] = [f"tink@{a.get('tick_at', '70%')}"] + list(b["sfx"])
                if a.get("list_all"):
                    for k2, n in enumerate(sorted(i1)):
                        lp[f"t{n}"] = 1.0 if n < 5 else 0.0
                        sets += [{"at": f"{10 + 12 * k2}%", "dur": 0.25, "p": {f"h{n}": 1.0}},
                                 {"at": f"{22 + 12 * k2}%", "dur": 0.25, "p": {f"h{n}": 0.0}}]
                    sets += [{"at": "15%", "dur": 0.35, "p": {"t5": 1.0}}]
            if was_big:
                sets += [{"at": "4%", "dur": 0.6, "p": {"big": 0.0}}]
            if last:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            kks.append({"id": "list", "type": "tc_list", "pos": [0, 0], "front": True, "p": dict(lp, items=items),
                        "set": sets})
            list_mode = "big" if is_big else "compact"
        else:
            list_mode = None
        # ---- stamps
        for k2, stp in enumerate(a.get("stamps", [])):
            kks.append({"id": f"stamp{k2}", "type": "ds_stamp", "pos": [0, 0], "front": True,
                        "p": dict({"on": 0.0}, **{k: v for k, v in stp.items() if k != "at"}),
                        "set": [{"at": stp.get("at", "40%"), "dur": 0.25, "p": {"on": 1.0}}]})
            b["sfx"] = [f"stamp@{stp.get('at', '40%')}"] + list(b["sfx"])
        if a.get("four"):
            f4 = a["four"]
            kks.append({"id": "four", "type": "tc_stamps", "pos": [0, 0], "front": True,
                        "p": {"n": 0.0, "items": f4["items"], "y": f4.get("y", 560)},
                        "set": [{"at": at, "dur": 0.3, "p": {"n": float(i + 1)}} for i, at in enumerate(f4["at"])]})
        # ---- chapter card (<= 1.2 s)
        if a.get("chapter"):
            kks.append({"id": "chap", "type": "ds_chapter", "pos": [0, 0], "front": True,
                        "p": {"on": 0.0, "kicker": seg.get("chip") or "", "title": _seg_title(seg)},
                        "set": [{"at": 0.0, "dur": 0.15, "p": {"on": 1.0}}, {"at": 1.0, "dur": 0.2, "p": {"on": 0.0}}]})
            b["sfx"] = ["whoosh@0.02"] + list(b["sfx"])
        # ---- card: under the meter, clear of the list
        if L.get("card") and not a.get("no_card"):
            if list_mode == "big":
                cx, mw = 480, 860
            elif list_mode == "compact":
                cx, mw = 730, 1180
            else:
                cx, mw = 960, 1500
            mw = a.get("card_w", mw)
            b["card"] = {"rows": ds._card_rows(L["card"], px=a.get("card_px", 118), max_w=mw), "y": a.get("card_y", 150),
                         "at": a.get("card_at", "30%"), "x": a.get("card_x", cx)}
        if a.get("tint"):
            b["tint"] = a["tint"]
        if a.get("flash"):
            b["flash"] = a["flash"]
        if a.get("shake"):
            b["shake"] = a["shake"]
        if last:
            kks.append({"id": "end", "type": "kk_end", "pos": [0, 0], "front": True,
                        "p": {"on": 0.0, **({"label": spec["end_label"].split(" (")[0].upper()} if spec.get("end_label") else {})},
                        "set": [{"at": "100%", "dur": 0.5, "p": {"on": 1.0}}]})
            b["pad"] = spec.get("end_hold", 12.0)
        b["actors"] = b["actors"] + kks
        b["say"] = L["say"]
        if L.get("tts"):
            b["tts"] = L["tts"]
        b.setdefault("pad", a.get("pad", 0.1))
        if L["id"] in spec.get("pause_lines", []):
            b["pad"] = max(b["pad"], 0.55)
        if b.get("norecut") and len(b["shots"]) == 1:
            s0 = b["shots"][0]
            c1 = list(s0.get("to", s0["cam"]))
            b["shots"] = [dict(s0, to=c1),
                          {"at": "40%", "cam": c1, "to": [c1[0] + 14, c1[1] + 4, round(c1[2] * 1.03, 4)], "dur": 0.6},
                          {"at": "75%", "cam": [c1[0] + 14, c1[1] + 4, round(c1[2] * 1.03, 4)], "to": [c1[0] - 6, c1[1], round(c1[2] * 1.05, 4)], "dur": 0.6}]
        b["kk_shots"] = b.pop("shots")
        b["ds_id"] = L["id"]
        beats.append(b)
    return beats


def drawn_spec(spec, lines):
    out = {k: spec[k] for k in ("voice", "rate", "pitch", "music", "music_db", "captions", "caption_y", "cut_whoosh",
                                "cap_key", "sfx_gain") if k in spec}
    out.update(beats=expand(spec, lines), recut=True, stage={},
               ds={"pause": spec.get("pause_lines", []), "music_out": spec.get("music_out", [])})
    for b in out["beats"]:
        b["shots"] = b["kk_shots"]
    return out


# ================================================================================================ render / sheets

def _pick(spec, rng):
    if not rng:
        return spec["lines"]
    a, b = rng.split("-")
    return spec["lines"][int(a):int(b) + 1]


def render(spec_path, out, rng=None, work=None):
    spec = json.load(open(spec_path))
    lines = _pick(spec, rng)
    dsx = drawn_spec(spec, lines)
    work = work or os.path.join(os.path.dirname(os.path.abspath(out)), ".work-" + os.path.splitext(os.path.basename(out))[0])
    os.makedirs(work, exist_ok=True)
    ds.voice_lines(dsx["beats"], dsx, work, CACHE)
    sp = os.path.join(work, "drawn_spec.json")
    json.dump(dsx, open(sp, "w"), indent=1)
    sys.argv = ["drawn.py", sp, out, "--work", work]
    os.environ.setdefault("CRF", "27")
    drawn.main()
    ds.loudness(out)


def _frame(spec, L, frac, work):
    dsx = drawn_spec(spec, [L])
    w = os.path.join(work, L["id"])
    os.makedirs(w, exist_ok=True)
    ds.voice_lines(dsx["beats"], dsx, w, CACHE)
    beats, total = drawn.plan(drawn.drawn_macros.expand(dsx), w)
    drawn.G.update(fps=30, beats=beats, rigs=drawn.rig_tracks(beats, 30), caps=drawn.caption_chunks(beats),
                   cap_px=dsx.get("captions", 62), cap_y=dsx.get("caption_y", 985), counter=None,
                   cap_key=set(dsx.get("cap_key", ())), ticks=[], raw_out=False, nocap_out=False)
    f = int(frac * beats[0]["speech"] * 30)
    arr = np.frombuffer(drawn.frame_at(f)[-1], np.uint8).reshape(H, W, 4)
    from PIL import Image
    return Image.fromarray(arr[..., [2, 1, 0]].copy()), beats[0]["dur"]


def linesheet(spec_path, out, only=None, frac=0.6, work="/tmp/treecheck-lines", cols=6, big=None):
    from PIL import Image, ImageDraw
    spec = json.load(open(spec_path))
    tiles = []
    for L in spec["lines"]:
        if only and L["id"] not in only:
            continue
        fr = L["shot"].get("sheet_at", frac)
        im, dur = _frame(spec, L, fr, work)
        if big:
            im.save(os.path.join(big, L["id"] + ".png"))
        im = im.resize((480, 270))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 246, 150, 270), fill=(0, 0, 0))
        d.text((4, 250), f"{L['id']} {dur:.1f}s", fill=(255, 255, 0))
        tiles.append(im)

    def sheet(ts, path):
        rows = (len(ts) + cols - 1) // cols
        s = Image.new("RGB", (480 * cols, 270 * rows))
        for i, im in enumerate(ts):
            s.paste(im, ((i % cols) * 480, (i // cols) * 270))
        s.save(path, quality=85)
    if only:
        sheet(tiles, out)
    else:
        base = os.path.splitext(out)[0]
        for k in range(0, len(tiles), 30):
            sheet(tiles[k:k + 30], f"{base}-{k // 30 + 1}.jpg")
    print("linesheet:", out, len(tiles))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("spec")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--lines")
    ap.add_argument("--work")
    ap.add_argument("--only")
    ap.add_argument("--big")
    ap.add_argument("--frac", type=float, default=0.6)
    x = ap.parse_args()
    if x.cmd == "build":
        build(x.spec, x.out)
    elif x.cmd == "render":
        render(x.spec, x.out, x.lines, x.work)
    elif x.cmd == "linesheet":
        linesheet(x.spec, x.out, x.only.split(",") if x.only else None, x.frac, x.work or "/tmp/treecheck-lines", big=x.big)
    elif x.cmd == "voice":
        spec = json.load(open(x.spec))
        dsx = drawn_spec(spec, spec["lines"])
        ds.voice_lines(dsx["beats"], dsx, "/tmp/treecheck-voice-work", CACHE)
    else:
        raise SystemExit(__doc__)
