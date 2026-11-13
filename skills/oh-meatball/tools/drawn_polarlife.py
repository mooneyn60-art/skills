#!/usr/bin/env python3
"""16:9 "Your Life as a Polar Bear" long-form (the "born as" shape, research 85; Nolan's pick 11/12).
A thin format layer on tools/drawn_catlife.py: the same DEAL METER (RAW DEAL / SWEET DEAL), the eight chips,
chapter cards, stamps, cards, per-line voice cache, music, 12 s end screen and two-pass loudness are imported from
it, not copied. Nothing in drawn_catlife changes: this module only points its voice cache at this episode, adds
the polar pictures (tools/drawn_pb_art.py), Meatball's orange parka and props, and names the end-screen video.

Pictures: tools/drawn_pb_art.py. Shots (one per line): tools/drawn_pb_shots.py.

  build OUTLINE.json SPEC.json        outline -> spec (every `say` and `card` kept; ids s<seg>.l<line>)
  render SPEC.json OUT.mp4 [--lines A-B] [--work DIR]
  linesheet SPEC.json OUT.jpg [--only ids] [--work DIR] [--frac F]   one frame per line, part sheets of 30
  voice SPEC.json [--work DIR]        voice every line now (cached in the episode's .voice-cache)

Meatball keys in a shot's mb (read by the parka wrapper below): parka (default on), hood (0..1) or hood_at (word
anchor: the hood drops then), gloves, floaties (+ goggles, no parka), coats (six coats), sweat.
"""
import copy
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_catlife as cl  # noqa: E402  (registers the meter, chips, cat art; wraps drawn.draw_prop)
import drawn  # noqa: E402
import drawn_dontsquish as ds  # noqa: E402
import drawn_pb_art as pba  # noqa: E402
import mascot  # noqa: E402
from drawn_kit import OUT, darker, ease, hexc, limb, p_ellipse, p_rrect, shape, stroke  # noqa: E402

ROOT = os.path.dirname(HERE)
EP = os.path.join(ROOT, "episodes", "longform-born-as-polar-bear")
cl.CACHE = os.path.join(EP, ".voice-cache")   # cl.voice_lines reads this module global
END_LABEL = "YOUR LIFE AS A HOUSE CAT"
TTS = {r"\bfourteen\b": "four-teen",
       r"\bdid his swim\b": "did hiz swim",   # s4.l3: the plain take's "his" is heard "a" (whole file and the line alone)
       r"\blegroom\b": "leg-room",            # s1.l6: heard "legron" / "they roam"; "leg-room" heard "leg room"
       r"\bHer fast can go\b": "Her fast, can go"}   # s0.l4: "fast can" ran together as "fasting"; a comma only   # pronunciation respellings (captions always use `say`): the plain take's
# "fourteen" (s2.l1) holds an "ee" near 2.5 kHz that the long-form beep gate flags; "four-teen" scans clean

drawn.ACTORS.update(pba.ACTORS)
drawn.SCENES.update(pba.SCENES)


# ------------------------------------------------------------------ Meatball: parka, hood, gloves, floaties, coats
_orig_draw_mb = drawn.draw_meatball


def _draw_meatball(ctx, cam, b, st, t):
    mb = b["mb"]
    if mb.get("hidden"):
        return
    if mb.get("coats"):   # the coats go under nothing: he is a ball with a head on top
        _extras(ctx, cam, b, st, t, coats_only=True)
    _orig_draw_mb(ctx, cam, b, st, t)
    _extras(ctx, cam, b, st, t)


def _extras(ctx, cam, b, st, t, coats_only=False):
    mb = b["mb"]
    words = b["words"]
    x, y, size, rot, land, walking = drawn.track(mb["pos"], mb["moves"], words, t, mb["size"])
    st = dict(st)
    if walking:
        st = mascot.apply_run(st, (b["t0"] + t) * 14)
    sh = mb.get("shake") or 0.0
    jx = sh * 10 * math.sin((b["t0"] + t) * 57)
    fx, fy = drawn.world_to_screen(cam, x + jx, y)
    k = size * cam[2] / 1000
    origin = (fx - 500 * k, fy - 960 * k)
    j = mascot.body(st)
    U = lambda q: (origin[0] + q[0] * k, origin[1] + q[1] * k)  # noqa: E731
    ctx.save()
    ctx.identity_matrix()
    ctx.translate(fx, fy)
    if land is not None and land < 0.3:
        q = 1 - land / 0.3
        ctx.scale(1 + 0.16 * q * math.cos(land * 20), 1 - 0.16 * q * math.cos(land * 20))
    if rot:
        ctx.rotate(math.radians(rot))
    ctx.translate(-fx, -fy)
    if coats_only:
        pba.coats(ctx, j, U, k)
        ctx.restore()
        return
    hood = mb.get("hood", 0.0)
    if mb.get("hood_at"):
        hood = ease((t - drawn.at_time(words, mb["hood_at"])) / 0.35)
    if mb.get("floaties"):
        for side, key in ((-1, "l"), (1, "r")):
            el, _, _ = mascot.arm_points(j, side, st[key])
            a, e = U(j["sh"]), U(el)
            cx, cy = (a[0] + e[0]) / 2, (a[1] + e[1]) / 2
            shape(ctx, lambda c, cx=cx, cy=cy: p_ellipse(c, cx, cy, 46 * k, 40 * k), hexc("#f2711c"), OUT * k, (0.1, 0.1))
        hx, hy = U(j["head"])
        stroke(ctx, [(hx - 150 * k, hy - 30 * k), (hx + 150 * k, hy - 30 * k)], 14 * k, color=hexc("#2a2a2e"))
        for s_ in (-1, 1):
            shape(ctx, lambda c, s_=s_: p_ellipse(c, hx + s_ * 55 * k, hy - 30 * k, 48 * k, 38 * k), hexc("#7fd0f0"), OUT * 0.8 * k, None, a=0.8)
    elif mb.get("parka", True) and not mb.get("coats"):
        pba.parka(ctx, j, U, k, dict(st, camera=mb.get("camera", True)), hood)
        prop = mb.get("prop")
        if prop:   # the prop again over the sleeve
            _, _, hand = mascot.arm_points(j, 1, st["r"])
            hx_, hy_ = U(hand)
            drawn.draw_prop(ctx, prop, hx_, hy_, k, b["t0"] + t)
    if mb.get("gloves"):
        for side, key in ((-1, "l"), (1, "r")):
            _, _, hand = mascot.arm_points(j, side, st[key])
            hx_, hy_ = U(hand)
            shape(ctx, lambda c, hx_=hx_, hy_=hy_: p_ellipse(c, hx_, hy_, 34 * k, 30 * k), hexc("#3b6bb0"), OUT * 0.8 * k, None)
    if mb.get("sweat"):
        hx, hy = U(j["head"])
        from drawn_kit import sweat
        for s_ in (-1, 1):
            sweat(ctx, hx + s_ * 170 * k, hy - 40 * k + 20 * k * math.sin((b["t0"] + t) * 5 + s_), 26 * k, OUT * 0.6 * k)
    ctx.restore()


drawn.draw_meatball = _draw_meatball

# ------------------------------------------------------------------ Meatball's hand props for this episode
_prev_draw_prop = drawn.draw_prop
PB_PROPS = {"ticket", "clip", "suitcase", "brochure", "stick", "glass", "sandwich", "card", "ticket_new"}


def _draw_prop(ctx, prop, hx, hy, k, t):
    if prop not in PB_PROPS:
        return _prev_draw_prop(ctx, prop, hx, hy, k, t)
    ctx.save()
    ctx.translate(hx, hy)
    ctx.scale(k, k)
    if prop in ("ticket", "ticket_new"):
        ctx.rotate(-0.25)
        shape(ctx, lambda c: p_rrect(c, -20, -120, 260, 110, 10), hexc("#ffd34d"), OUT, None)
        for i in range(8):
            stroke(ctx, [(10 + i * 30, -120), (10 + i * 30, -10)], 3, color=hexc("#b8873f"))
    elif prop == "clip":
        ctx.rotate(0.1)
        shape(ctx, lambda c: p_rrect(c, -10, -240, 190, 250, 14), hexc("#b07a48"), OUT, None)
        shape(ctx, lambda c: c.rectangle(10, -215, 150, 200), hexc("#fbf8ef"), OUT * 0.6, None)
        for i in range(5):
            stroke(ctx, [(30, -180 + i * 34), (140, -180 + i * 34)], 5, color=hexc("#9aa3ab"))
    elif prop == "suitcase":
        shape(ctx, lambda c: p_rrect(c, -110, 20, 220, 170, 16), hexc("#6b3b22"), OUT, (0.05, 0.1))
        stroke(ctx, [(-40, 20), (-40, -10), (40, -10), (40, 20)], 10)
    elif prop == "brochure":
        ctx.rotate(-0.15)
        shape(ctx, lambda c: c.rectangle(-10, -200, 150, 200), hexc("#fbf8ef"), OUT * 0.8, None)
        shape(ctx, lambda c: c.rectangle(5, -185, 120, 60), hexc("#3d6b8f"), OUT * 0.5, None)
    elif prop == "stick":
        stroke(ctx, [(0, -60), (20, 330)], 18, color=hexc("#7c5232"))
        stroke(ctx, [(0, -60), (20, 330)], 4)
    elif prop == "glass":
        ctx.translate(0, 40)
        pba.pb_glass(ctx, t, {})
    elif prop == "sandwich":
        pba.pb_sandwich(ctx, t, {})
    elif prop == "card":
        ctx.translate(120, -150)
        ctx.scale(0.45, 0.45)
        pba.pb_review(ctx, t, {"stars": 1, "text": "COAT NOT|INCLUDED.", "rot": 180})
    ctx.restore()


drawn.draw_prop = _draw_prop


# ------------------------------------------------------------------ the end screen names the house-cat video
_cat_expand = cl.expand


def expand(spec, lines):
    beats = _cat_expand(spec, lines)
    for b in beats:
        for a in b["actors"]:
            if isinstance(a, dict) and a.get("type") == "kk_end":
                a["p"]["label"] = spec.get("end_label_short", END_LABEL)
    return beats


cl.expand = expand   # cl.drawn_spec (render, line sheets) looks the name up at call time


# ================================================================================================ build

def build(outline, out_spec):
    import drawn_pb_shots
    shots = drawn_pb_shots.table()
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
    spec = {"_note": "Built by tools/drawn_polarlife.py build from " + os.path.basename(outline) +
                     ". Each line: id (s<seg>.l<line>), the outline fields (say/vis/card/meter/src) and shot "
                     "(recipe + args, tools/drawn_pb_shots.py). `tts` = a pronunciation respelling (captions use say).",
            "builder": "drawn_polarlife",
            "voice": o.get("voice", "en-US-AndrewMultilingualNeural"), "rate": o.get("rate", "+10%"),
            "pitch": o.get("pitch", "+3Hz"), "music": "mystery", "music_db": -15, "captions": 62, "caption_y": 985,
            "cut_whoosh": True, "sfx_gain": 0.22, "meter_start": o.get("meter_start", 50),
            "meter_labels": o.get("meter_labels"),
            "cap_key": ["bear", "bears", "polar", "cub", "cubs", "seal", "seals", "ice", "den", "deal", "raw", "sweet",
                        "eight", "four", "star", "one", "swim", "nine", "687", "kilometres", "73", "20", "verdict",
                        "badass", "town", "time", "nose", "fat", "coat"],
            "pause_lines": ["s4.l6", "s7.l7", "s10.l3"], "music_out": [],
            "end_hold": 12.0, "end_label": o.get("end_screen_video"), "end_label_short": END_LABEL, "segments": segs,
            "titles": o.get("titles"), "pinned_comment": o.get("pinned_comment"), "lines": lines}
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    print(f"{out_spec}: {len(lines)} lines, {sum(len(L['say'].split()) for L in lines)} words, "
          f"{len(lines) - todo} with hand-made shots, {todo} TODO")


def render(spec_path, out, rng=None, work=None):
    cl.render(spec_path, out, rng, work)
    # one more loudness pass with a lower true-peak ceiling: after the first pass the AAC encode can land the
    # true peak just over -1 dBFS (the long-form gate's limit)
    cl.loudness(out, -14.0, -2.5)


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
        cl.linesheet(x.spec, x.out, x.only.split(",") if x.only else None, x.frac, x.work or "/dev/shm/polar-build/lines",
                     big=x.big)
    elif x.cmd == "voice":
        spec = json.load(open(x.spec))
        dsx = cl.drawn_spec(spec, spec["lines"])
        cl.voice_lines(dsx["beats"], dsx, x.work or "/dev/shm/polar-build/voice")
    else:
        raise SystemExit(__doc__)
