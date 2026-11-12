#!/usr/bin/env python3
"""16:9 "Why It Sucks to Be Born as a House Cat" long-form (the "born as" shape, research 85; Nolan's pick 11/11).
A format layer on tools/drawn_dontsquish.py (recipes, chips, chapter cards, stamps, per-line voice cache, music
envelope with dips, 12 s end screen, two-pass loudness), copied from tools/drawn_treecheck.py, with its own overlays:

  cl_meter   DEAL METER: top bar from RAW DEAL (red, left) to SWEET DEAL (green, right), no digits; the marker eases
             to each line's `meter` (0..100) with a soft tick, pulses and swells on a move of 8 or more; slides in on
             the cold open's last line; p: v, on, pulse, swell, blink (0..1 the plate blinks)
  cl_chips8  a row of eight small progress chips (cold open, "That's five", "Eight for eight"); p: n (shown),
             filled (0..8), pulse, y

Pictures: tools/drawn_cl_art.py. Shots (one per line): tools/drawn_cl_shots.py.

  build OUTLINE.json SPEC.json        outline -> spec (every `say` and `card` kept; ids s<seg>.l<line>)
  render SPEC.json OUT.mp4 [--lines A-B] [--work DIR]
  linesheet SPEC.json OUT.jpg [--only ids] [--work DIR]   one frame per line, part sheets of 30 lines
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
import drawn_dontsquish as ds  # noqa: E402
import drawn  # noqa: E402
import drawn_keepkill as kk  # noqa: E402
import drawn_cl_art as cla  # noqa: E402
from drawn_kit import back_out, ease, hexc  # noqa: E402

W, H = 1920, 1080
ROOT = os.path.dirname(HERE)
EP = os.path.join(ROOT, "episodes", "longform-born-as-house-cat")
CACHE = os.path.join(EP, ".voice-cache")
RED, GREEN, YEL = ds.RED, ds.GREEN, ds.YEL
# pronunciation respellings (captions always use `say`); found by transcribing the takes, see the build notes
# (11/12 build: every take transcribed with faster-whisper small.en; each respelling tried on fresh takes; the
# other "taurine" lines and "phalangectomy" were heard right as written, "meowed" / "rawer" did not improve;
# 11/12 review: "meowed" is heard "me out" in every wording, so that line now says "let out a meow")
TTS = {r"\bthe cats taurine\.": "the cats tawreen.",   # line end heard "touring"; respelled heard "taurine"
       r"\bActual hearts\b": "Ackchual hearts",           # heard "Actualeerts"; respelled heard "Actual hearts"
       r"\bdeclawing\b": "dee-clah-wing"}                 # heard "decline" (5 spellings tried); this one "declawing"


# ================================================================================================ DEAL METER

def _face(ctx, cx, cy, col, happy):
    import math as m
    ctx.arc(cx, cy, 20, 0, 2 * m.pi)
    kk.fill(ctx, col, 1.0, 4)
    for s in (-1, 1):
        ctx.arc(cx + s * 7, cy - 4, 3, 0, 2 * m.pi)
        ctx.set_source_rgb(0.07, 0.07, 0.07)
        ctx.fill()
    ctx.new_sub_path()
    if happy:
        ctx.arc(cx, cy + 2, 10, 0.2 * m.pi, 0.8 * m.pi)
    else:
        ctx.arc(cx, cy + 16, 10, 1.2 * m.pi, 1.8 * m.pi)
    ctx.set_line_width(3.5)
    ctx.stroke()


def cl_meter(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    v = max(0.0, min(100.0, p.get("v", 50.0)))
    pulse = max(0.0, p.get("pulse", 0.0))
    sw = max(0.0, p.get("swell", 0.0))
    sc = 1.0 + 0.13 * sw
    cy = 66 - 170 * (1 - ease(min(1.0, on))) + 6 * sw
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(sc, sc)
    bl = p.get("blink", 0.0)
    blink = bl * (0.5 + 0.5 * math.sin(t * 9))
    kk.rrect(ctx, -590, -44, 1180, 88, 44)
    kk.fill(ctx, (18, 22, 40), 0.9, 0)
    kk.rrect(ctx, -590, -44, 1180, 88, 44)
    if bl > 0.01:
        ctx.set_source_rgba(0.9, 0.22 + 0.5 * (1 - blink), 0.23, 1)
    else:
        ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(4 + 4 * blink)
    ctx.stroke()
    _face(ctx, -545, 0, RED, False)
    kk.blit(ctx, kk.text_img("RAW DEAL", 38, RED, 5), -425, 0)
    kk.blit(ctx, kk.text_img("SWEET DEAL", 38, GREEN, 5), 410, 0)
    _face(ctx, 545, 0, GREEN, True)
    x0, x1, bh = -300, 300, 30
    import cairo
    kk.rrect(ctx, x0, -bh / 2, x1 - x0, bh, bh / 2)
    g = cairo.LinearGradient(x0, 0, x1, 0)
    for u, c in ((0.0, RED), (0.5, YEL), (1.0, GREEN)):
        r, gg, b = hexc(c)
        g.add_color_stop_rgb(u, r, gg, b)
    ctx.set_source(g)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.07, 0.07, 0.07)
    ctx.set_line_width(4)
    ctx.stroke()
    for k in range(11):   # ticks, no digits
        x = x0 + (x1 - x0) * k / 10
        ctx.move_to(x, bh / 2 + 3)
        ctx.line_to(x, bh / 2 + (12 if k % 5 == 0 else 7))
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.set_line_width(3)
        ctx.stroke()
    mx = x0 + (x1 - x0) * v / 100.0
    if v < 100:
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


def cl_chips8(ctx, t, p):
    """Eight small progress chips in a row, birth (left) to old age (right); p n (how many shown, slides them in),
    filled (0..8 chips filled with a paw), pulse (0..1 the filled ones pulse), y (screen)."""
    n = p.get("n", 8.0)
    if n <= 0.01:
        return
    ctx.identity_matrix()
    y = p.get("y", 200)
    fl = p.get("filled", 0.0)
    pu = p.get("pulse", 0.0)
    for i in range(8):
        u = max(0.0, min(1.0, (n - i) * 2))
        if u <= 0:
            continue
        x = W / 2 + (i - 3.5) * 150
        s = back_out(u)
        f = max(0.0, min(1.0, fl - i))
        if f > 0 and pu > 0:
            s *= 1 + 0.12 * pu * (0.5 + 0.5 * math.sin(t * 10))
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        kk.rrect(ctx, -60, -40, 120, 80, 40)
        kk.fill(ctx, YEL if f >= 0.5 else (18, 22, 40), 0.95, 4)
        if f >= 0.5:
            cla._paw(ctx, 0, 6, 0.38, (0.15, 0.12, 0.1))
        ctx.restore()


OVERLAYS = {"cl_meter": cl_meter, "cl_chips8": cl_chips8}
drawn.ACTORS.update(OVERLAYS)
drawn.ACTORS.update(cla.ACTORS)
drawn.SCENES.update(cla.SCENES)
import drawn_tc_art  # noqa: E402
drawn.SCENES.setdefault("tc_combo", drawn_tc_art.tc_combo)   # two scenes in one world (the cross-cut in the verdict)


# ------------------------------------------------------------------ Meatball's hand props for this episode
_orig_draw_prop = drawn.draw_prop
MB_PROPS = {   # name -> (scale in rig units, rotation, dx, dy)
    "kitten": (0.55, 0.0, -60, 40), "kitten_sub": (0.55, 0.0, -170, 20), "cake": (0.8, 0.0, 0, 0),
    "phone": (0.55, 0.12, -30, 200), "bottle": (0.45, 0.0, 0, 80), "book": (0.7, 0.0, 40, -40),
    "toymouse": (1.0, 0.0, 0, 0), "saucer": (0.9, 0.0, 0, 60), "carrier": (0.45, 0.0, 0, 300),
    "cone": (0.7, 0.0, 0, 80),
}


def _draw_prop(ctx, prop, hx, hy, k, t):
    if prop not in MB_PROPS:
        return _orig_draw_prop(ctx, prop, hx, hy, k, t)
    sc, rot, dx, dy = MB_PROPS[prop]
    ctx.save()
    ctx.translate(hx + dx * k, hy + dy * k)
    ctx.rotate(rot)
    ctx.scale(k * sc, k * sc)
    if prop == "kitten":   # held gently in both hands
        cla.cl_cat(ctx, t, {"age": "kitten", "mood": "happy", "look": [1, 0], "sit": 0.6})
    elif prop == "kitten_sub":   # held stiff and level like a sub sandwich
        ctx.translate(0, 120)
        cla.cl_cat(ctx, t, {"age": "kitten", "mood": "worry", "look": [1, -0.3], "sit": 0.0})
    elif prop == "cake":
        cla.cl_cake(ctx, t, {})
    elif prop == "phone":
        ctx.translate(0, -120)
        cla.cl_phone(ctx, t, {})
    elif prop == "bottle":
        cla.cl_bottle(ctx, t, {})
    elif prop == "book":
        cla.cl_book(ctx, t, {"upside": 1.0})
    elif prop == "toymouse":
        ctx.translate(80, 560)
        cla.cl_toy(ctx, t, {"kind": "mouse", "sx": -40, "sy": -500})
    elif prop == "saucer":
        cla.cl_saucer(ctx, t, {})
    elif prop == "carrier":
        cla.cl_carrier(ctx, t, {})
    elif prop == "cone":
        cla.cl_cone(ctx, t, {})
    ctx.restore()


drawn.draw_prop = _draw_prop


# ================================================================================================ build

def build(outline, out_spec):
    import drawn_cl_shots
    shots = drawn_cl_shots.table()
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
    spec = {"_note": "Built by tools/drawn_catlife.py build from " + os.path.basename(outline) +
                     ". Each line: id (s<seg>.l<line>), the outline fields (say/vis/card/meter/src) and shot "
                     "(recipe + args, tools/drawn_cl_shots.py). `tts` = a pronunciation respelling (captions use say).",
            "builder": "drawn_catlife",
            "voice": o.get("voice", "en-US-AndrewMultilingualNeural"), "rate": o.get("rate", "+10%"),
            "pitch": o.get("pitch", "+3Hz"), "music": "mystery", "music_db": -15, "captions": 62, "caption_y": 985,
            "cut_whoosh": True, "sfx_gain": 0.22, "meter_start": o.get("meter_start", 50),
            "meter_labels": o.get("meter_labels"),
            "cap_key": ["cat", "cats", "kitten", "kittens", "deal", "raw", "sweet", "eight", "five", "taurine", "lilies",
                        "daylilies", "vet", "milk", "window", "carrier", "purr", "x-ray", "kidney", "dental",
                        "never", "verdict", "wildcat", "mice", "sugar", "six", "four", "three", "half", "badass"],
            "pause_lines": ["s4.l5", "s5.l13", "s8.l2"], "music_out": [],
            "end_hold": 12.0, "end_label": o.get("end_screen_video"), "segments": segs, "titles": o.get("titles"),
            "pinned_comment": o.get("pinned_comment"), "lines": lines}
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    print(f"{out_spec}: {len(lines)} lines, {sum(len(L['say'].split()) for L in lines)} words, "
          f"{len(lines) - todo} with hand-made shots, {todo} TODO")


# ================================================================================================ expand

def _card_rows(text, max_w=1500, px=110, min_px=84):
    """The card verbatim: one row if it fits at >= min_px, else two rows split at the best word break (after a ?, : or ,
    when there is one)."""
    from PIL import ImageFont

    def wid(s, z):
        return ImageFont.truetype(kk.FONT, z).getlength(s)
    z = px
    while z > min_px and wid(text, z) > max_w:
        z -= 4
    if wid(text, z) <= max_w:
        return [[text, YEL, z]]
    words = text.split(" ")
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        m = max(wid(a, 100), wid(b, 100)) - (400 if a.endswith(("?", ":", ",")) else 0)   # break after punctuation
        if best is None or m < best[0]:
            best = (m, a, b)
    _, a, b = best
    z = px
    while z > 56 and max(wid(a, z), wid(b, z)) > max_w:
        z -= 4
    return [[a, YEL, z], [b, YEL, z]]


def states(spec):
    v = float(spec.get("meter_start", 50))
    out, on = {}, False
    for L in spec["lines"]:
        st = {"v0": v, "on0": on}
        if L["shot"].get("meter_in"):
            on = True
        if "meter" in L:
            v = float(L["meter"])
        st.update(v1=v, on1=on)
        out[L["id"]] = st
    return out


def expand(spec, lines):
    segs = spec["segments"]
    order = [L["id"] for L in spec["lines"]]
    ST = states(spec)
    beats = []
    for L in lines:
        a = L["shot"]
        b = ds.RECIPES[a.get("r", "scene")](L, a)
        if a.get("norecut"):
            b["norecut"] = True
        if a.get("recut") is False:
            b["recut"] = False
        st = ST[L["id"]]
        seg = segs[L["seg"]]
        last = L["id"] == order[-1]
        first_of_seg = L["id"] == f"s{L['seg']}.l0"
        kks = []
        # ---- DEAL METER
        if st["on1"]:
            v0, v1 = st["v0"], st["v1"]
            mat = a.get("meter_at", "60%")
            mp = {"v": v0, "on": 1.0, "pulse": 0.0, "swell": 0.0, "blink": 0.0}
            sets = []
            if not st["on0"]:
                mp["on"] = 0.0
                sets.append({"at": a["meter_in"], "dur": 0.55, "p": {"on": 1.0}})
                b["sfx"] = [f"whoosh@{a['meter_in']}"] + list(b["sfx"])
            if abs(v1 - v0) > 0.01:
                sets.append({"at": mat, "dur": 0.7, "p": {"v": v1}})
                b["sfx"] = [f"click@{mat}"] + list(b["sfx"])
                if abs(v1 - v0) >= 8:
                    sets += [{"at": mat, "p": {"pulse": 1.0}}, {"at": mat, "dur": 0.9, "p": {"pulse": 0.0}},
                             {"at": mat, "dur": 0.3, "p": {"swell": 1.0}},
                             {"at": ds._after(mat, 1.25), "dur": 0.4, "p": {"swell": 0.0}}]
            if a.get("meter_blink"):
                sets += [{"at": a["meter_blink"], "dur": 0.2, "p": {"blink": 1.0}}]
            if a.get("meter_swing"):   # a dip and a recovery on the same value (the "miss them" line)
                lo, at1, at2 = a["meter_swing"]
                sets += [{"at": at1, "dur": 0.6, "p": {"v": lo}}, {"at": at2, "dur": 0.8, "p": {"v": v1}}]
                b["sfx"] = [f"click@{at1}"] + list(b["sfx"])
            if a.get("meter_climb"):   # a climb past the value and back (the "pretty damn sweet" line)
                hi, at1, at2 = a["meter_climb"]
                sets += [{"at": at1, "dur": 0.8, "p": {"v": hi}}, {"at": at2, "dur": 0.6, "p": {"v": v1}}]
                b["sfx"] = [f"click@{at1}"] + list(b["sfx"])
            if last:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            kks.append({"id": "meter", "type": "cl_meter", "pos": [0, 0], "front": True, "p": mp, "set": sets})
        # ---- chip (top left)
        chip = seg.get("chip")
        if chip:
            cp = {"text": chip, "on": 1.0, "done": 0.0}
            sets = []
            if first_of_seg:
                cp["on"] = 0.0
                sets.append({"at": 1.15, "dur": 0.35, "p": {"on": 1.0}})
            if last:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            kks.append({"id": "chip", "type": "ds_qchip", "pos": [0, 0], "front": True, "p": cp, "set": sets})
        # ---- the eight progress chips
        if a.get("chips8"):
            c8 = a["chips8"]
            cp = {"n": c8.get("n0", 8.0), "filled": c8.get("filled0", 0.0), "pulse": 0.0, "y": c8.get("y", 200)}
            sets = copy.deepcopy(c8.get("sets", []))
            kks.append({"id": "chips8", "type": "cl_chips8", "pos": [0, 0], "front": True, "p": cp, "set": sets})
        # ---- stamps
        for k2, stp in enumerate(a.get("stamps", [])):
            kks.append({"id": f"stamp{k2}", "type": "ds_stamp", "pos": [0, 0], "front": True,
                        "p": dict({"on": 0.0}, **{k: v for k, v in stp.items() if k != "at"}),
                        "set": [{"at": stp.get("at", "40%"), "dur": 0.25, "p": {"on": 1.0}}]})
            b["sfx"] = [f"stamp@{stp.get('at', '40%')}"] + list(b["sfx"])
        # ---- chapter card (<= 1.2 s) on each chaptered segment's first line (never on the cold open)
        if first_of_seg and L["seg"] > 0:
            kks.append({"id": "chap", "type": "ds_chapter", "pos": [0, 0], "front": True,
                        "p": {"on": 0.0, "kicker": seg.get("chip") if seg.get("chip", "").endswith("OF 8") else "",
                              "title": seg["chapter"].upper()},
                        "set": [{"at": 0.0, "dur": 0.15, "p": {"on": 1.0}}, {"at": 1.0, "dur": 0.2, "p": {"on": 0.0}}]})
            b["sfx"] = ["whoosh@0.02"] + list(b["sfx"])
        # ---- card
        if L.get("card") and not a.get("no_card"):
            b["card"] = {"rows": _card_rows(L["card"], max_w=a.get("card_w", 1500), px=a.get("card_px", 110)),
                         "y": a.get("card_y", 150), "at": a.get("card_at", "25%"), "x": a.get("card_x", 960)}
        for key in ("tint", "flash", "shake"):
            if a.get(key):
                b[key] = a[key]
        if last:
            kks.append({"id": "end", "type": "kk_end", "pos": [0, 0], "front": True,
                        "p": {"on": 0.0}, "set": [{"at": "100%", "dur": 0.5, "p": {"on": 1.0}}]})
            b["pad"] = spec.get("end_hold", 12.0)
        b["actors"] = b["actors"] + kks + copy.deepcopy(a.get("top_actors", []))   # top_actors: drawn over the overlays
        b["say"] = L["say"]
        if L.get("tts"):
            b["tts"] = L["tts"]
        b.setdefault("pad", a.get("pad", 0.1))
        if L["id"] in spec.get("pause_lines", []):
            b["pad"] = max(b["pad"], 0.6)
        if b.get("norecut") and len(b["shots"]) == 1:
            s0 = b["shots"][0]
            c1 = list(s0.get("to", s0["cam"]))
            b["shots"] = [dict(s0, to=c1),
                          {"at": "40%", "cam": c1, "to": [c1[0] + 14, c1[1] + 4, round(c1[2] * 1.03, 4)], "dur": 0.6},
                          {"at": "75%", "cam": [c1[0] + 14, c1[1] + 4, round(c1[2] * 1.03, 4)],
                           "to": [c1[0] - 6, c1[1], round(c1[2] * 1.05, 4)], "dur": 0.6}]
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


# ================================================================================================ voice (validated)

def voice_lines(beats, dsx, work):
    """ds.voice_lines with one more check on cached takes: a take that is cut short (facts.take_complete: the last
    spoken word must be the line's last word and the audio must reach it) is thrown away and spoken again."""
    from facts import take_complete
    os.makedirs(CACHE, exist_ok=True)
    for b in beats:
        text = b.get("tts", b["say"])
        c = os.path.join(CACHE, ds._vkey(text, dsx["voice"], dsx["rate"], dsx["pitch"]) + ".mp3")
        if os.path.exists(c) and os.path.exists(c + ".words.json"):
            words = json.load(open(c + ".words.json"))
            if not (ds._good(c, words) and take_complete(text, words, c)):
                print(f"  voice: dropping a bad cached take: {text[:60]}", flush=True)
                os.remove(c)
    ds.voice_lines(beats, dsx, work, CACHE)
    # a respelled word: drawn checks the take against `say` and spells the captions from the timings, so the work
    # copy of the timings carries the `say` spelling of each respelled word (the timings themselves are unchanged)
    def key(w):
        return "".join(ch for ch in w.lower() if ch.isalnum())
    for i, b in enumerate(beats):
        if b.get("tts") and b["tts"] != b["say"]:
            ts, ss = b["tts"].split(), b["say"].split()
            swap = {key(a): re.sub(r"[^\w'-]", "", c) for a, c in zip(ts, ss) if a != c} if len(ts) == len(ss) else {}
            wp = f"{work}/v{i:02d}.mp3.words.json"
            words = json.load(open(wp))
            for w in words:
                if key(w[2]) in swap:
                    w[2] = swap[key(w[2])]
            json.dump(words, open(wp, "w"))


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
    voice_lines(dsx["beats"], dsx, work)
    sp = os.path.join(work, "drawn_spec.json")
    json.dump(dsx, open(sp, "w"), indent=1)
    sys.argv = ["drawn.py", sp, out, "--work", work]
    os.environ.setdefault("CRF", "27")
    drawn.main()
    loudness(out)


def loudness(path, target=-14.0, tp=-2.0):
    """Peak limiter, then two-pass linear loudnorm to `target` LUFS (as tools/drawn_treecheck.py)."""
    import subprocess
    pre = "alimiter=limit=0.63:level=false:attack=2:release=60"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"{pre},loudnorm=I={target}:TP={tp}:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    af = (f"{pre},loudnorm=I={target}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    tmp = path + ".ln.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", af,
                    "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, path)
    print(f"loudness: measured {m['input_i']} LUFS / {m['input_tp']} dBTP (after the limiter) -> {target} LUFS", flush=True)


def _frame(spec, L, frac, work):
    dsx = drawn_spec(spec, [L])
    w = os.path.join(work, L["id"])
    os.makedirs(w, exist_ok=True)
    voice_lines(dsx["beats"], dsx, w)
    beats, total = drawn.plan(drawn.drawn_macros.expand(dsx), w)
    drawn.G.update(fps=30, beats=beats, rigs=drawn.rig_tracks(beats, 30), caps=drawn.caption_chunks(beats),
                   cap_px=dsx.get("captions", 62), cap_y=dsx.get("caption_y", 985), counter=None,
                   cap_key=set(dsx.get("cap_key", ())), ticks=[], raw_out=False, nocap_out=False)
    f = int(frac * beats[0]["speech"] * 30)
    arr = np.frombuffer(drawn.frame_at(f)[-1], np.uint8).reshape(H, W, 4)
    from PIL import Image
    return Image.fromarray(arr[..., [2, 1, 0]].copy()), beats[0]["dur"]


def linesheet(spec_path, out, only=None, frac=0.6, work="/tmp/catlife-lines", cols=5, big=None):
    from PIL import Image, ImageDraw
    spec = json.load(open(spec_path))
    tiles = []
    for L in spec["lines"]:
        if only and L["id"] not in only:
            continue
        fr = L["shot"].get("sheet_at", frac)
        im, dur = _frame(spec, L, fr, work)
        if big:
            os.makedirs(big, exist_ok=True)
            im.save(os.path.join(big, L["id"] + ".png"))
        im = im.resize((576, 324))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 300, 150, 324), fill=(0, 0, 0))
        d.text((4, 304), f"{L['id']} {dur:.1f}s", fill=(255, 255, 0))
        tiles.append(im)

    def sheet(ts, path):
        rows = (len(ts) + cols - 1) // cols
        s = Image.new("RGB", (576 * cols, 324 * rows))
        for i, im in enumerate(ts):
            s.paste(im, ((i % cols) * 576, (i // cols) * 324))
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
        linesheet(x.spec, x.out, x.only.split(",") if x.only else None, x.frac, x.work or "/tmp/catlife-lines", big=x.big)
    elif x.cmd == "voice":
        spec = json.load(open(x.spec))
        dsx = drawn_spec(spec, spec["lines"])
        voice_lines(dsx["beats"], dsx, x.work or "/tmp/catlife-voice-work")
    else:
        raise SystemExit(__doc__)
