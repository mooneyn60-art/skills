#!/usr/bin/env python3
"""16:9 Wednesday flagship 11/25 "Never Bring a Christmas Tree Inside Before You Check for This" (about 9:50).
Episode layer on top of tools/drawn_ranked.py (the flagship engine: framings and hard cuts, BUG CAM rings, Meatball
bursts, freak-out, re-hook slams, captions, gap lint), like tools/drawn_bathroom.py. The pictures come from
tools/drawn_tc_art.py (registered by drawn_treecheck, which drawn_ranked already imports); this file adds:

  rooms      the living room with the tree, the tree lot, the yard, the bark close-up, the woods, the farm, ...
  HUD        the PANIC METER (tc_panic, 0-10, with the value on a badge) from s0.l6 on, eased to each line's
             `panic`; the TREE CHECK list (tc_list) built from each line's `check` (it fills the right half in
             the chapter "The tree check"); the chapter re-hook slam (STOWAWAY n OF 9)
  voice      E2 plain (kokoro:adam-puck; free_voice drops pitch/formant/drive), per-line act -> speed only.
             The [BLEEP] line is two takes with a 1 kHz bleep tone over the gap: the voice never says the word
             or "bleep", and the caption shows neither. "damn" is captioned "dang" (spec cap_swap).
  shots      SHOTS below, one per line id.

  build OUTLINE.json SPEC.json      outline -> spec
  render SPEC.json OUT.mp4 [--lines A-B|sN] [--work DIR]
  lint SPEC.json STEM.wav [--work REPORT.txt]   voice-only stem + silencedetect gap report
  linesheet SPEC.json OUT.jpg [--only ids] [--fracs a,b]
  check SPEC.json                   runtime, holds, chapter starts
  voice SPEC.json                   voice every line now

Rules from the brief: nothing killed or squashed on screen for shock (the nymphs "eat each other" line cuts away;
the slipper never lands); spraying the tree is only ever shown as a NO, with no fire drawn.
"""
import copy
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_ranked as R  # noqa: E402
import drawn  # noqa: E402
import drawn_treecheck as TC  # noqa: E402
import drawn_keepkill as kk  # noqa: E402
from drawn_kit import ease  # noqa: E402
from PIL import ImageFont  # noqa: E402

W, H = R.W, R.H
YEL, RED, GREEN = R.YEL, R.RED, R.GREEN
A, lab, popset, stamp = R.A, R.lab, R.popset, R.stamp
BLEEP = "[BLEEP]"

# ================================================================================================ HUD: panic meter with its value


def xm_panic(ctx, t, p):
    TC.tc_panic(ctx, t, p)
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    big = ease(p.get("big", 0.0))
    v = max(0.0, min(10.0, p.get("v", 9.0)))
    sc = 1.0 + 0.5 * big
    cy = 66 + (330 - 66) * big - 170 * (1 - ease(min(1.0, on)))
    mx = W / 2 + sc * (-320 + 640 * v / 10.0)
    col = TC._vcol(v)
    hexs = "#%02x%02x%02x" % tuple(int(c * 255) for c in col)
    ctx.identity_matrix()
    kk.blit(ctx, kk.text_img("%d/10" % round(v), int(40 * sc), hexs, 6), mx, cy + 62 * sc)


drawn.ACTORS["xm_panic"] = xm_panic

# ================================================================================================ rooms
# tc_* scenes put the floor at y = 900 (Meatball's feet there); the bark and bokeh close-ups have no floor.

R.ROOMS.update({
    "liv": {"scene": "tc_living", "sp": {}, "mx": 1550, "bug": None, "light": "off"},
    "livN": {"scene": "tc_living", "sp": {}, "mx": 1550, "bug": None, "light": "lamp"},
    "close": {"scene": "tc_bokeh", "sp": {}, "mx": None, "bug": None, "light": "off"},
    "case": {"scene": "tc_bokeh", "sp": {}, "mx": None, "bug": None, "light": "off"},
    "closeG": {"scene": "tc_bokeh", "sp": {"green": True}, "mx": None, "bug": None, "light": "off"},
    "lot": {"scene": "tc_lot", "sp": {}, "mx": 1400, "bug": None, "light": "off"},
    "yard": {"scene": "tc_yard", "sp": {}, "mx": 1300, "bug": None, "light": "off"},
    "yardS": {"scene": "tc_yard", "sp": {"spring": 1.0}, "mx": 1300, "bug": None, "light": "off"},
    "trunk": {"scene": "tc_trunk", "sp": {}, "mx": None, "bug": None, "light": "off"},
    "woods": {"scene": "tc_snowwood", "sp": {}, "mx": 1400, "bug": None, "light": "off"},
    "farm": {"scene": "tc_farm", "sp": {}, "mx": 1400, "bug": None, "light": "off"},
    "road": {"scene": "tc_road", "sp": {}, "mx": None, "bug": None, "light": "off"},
    "curb": {"scene": "tc_curb", "sp": {}, "mx": 1400, "bug": None, "light": "off"},
    "cork": {"scene": "tc_cork", "sp": {"papers": []}, "mx": 1450, "bug": None, "light": "off"},
    "lab": {"scene": "ds_lab", "sp": {}, "mx": 1450, "bug": None, "light": "off"},
    "board": {"scene": "rk_board_bg", "sp": {"color": "#1b1724"}, "mx": None, "bug": None, "light": "off"},
})
CH_ROOM = ["liv", "cork", "close", "liv", "close", "trunk", "livN", "lot", "liv"]
CH_TINT = [None, None, None, None, [0.6, 1.0, 0.7, 0.06], None, [1.0, 0.4, 0.3, 0.07], None, [1.0, 0.9, 0.6, 0.08]]
for _k, _v in R.ROOMS.items():   # tc_* rooms: frame the tree / the subject, not the ranked rooms' bug mark
    if _v["scene"].startswith(("tc_", "ds_lab")) and "bpos" not in _v:
        _v.update(bpos=[960, 560], bs=0.5)
R.CH_ROOM = CH_ROOM
R.CH_BUG = [None] * 9
R.BEATS = []   # filled by build from BEAT_IDS
BEAT_IDS = ["s0.l3", "s1.l6", "s2.l4", "s2.l16", "s3.l7", "s4.l13", "s6.l4", "s8.l0"]   # >= 30 s apart; checked by lint

_orig_expand = R.expand

# ================================================================================================ voice: E2 plain, act -> speed

DIRECT = {}   # filled from the shot table ("act") and the outline ("act"); default by the line's source


def direction(L):
    if L.get("act"):
        return L["act"]
    if L["id"] in DIRECT:
        return DIRECT[L["id"]]
    return "fact" if L.get("src") and L["src"] != "joke" else "story"


R.direction = direction


def _split_bleep(say):
    a, b = say.split(BLEEP, 1)
    return a.strip(), b.strip()


def _decode(mp3, sr=24000):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def make_bleep(spec, L):
    """The [BLEEP] line: take A + 40 ms + a 0.42 s 1 kHz bleep + 40 ms + take B, stored as the line's own cached take
    (key = the full `say`), with word times from the two takes (no word for the bleep)."""
    import numpy as np
    import soundfile as sf
    import free_voice
    import premium_voice as pv
    v = R._kvoice(spec, L)
    cname = free_voice.cache_name(v)
    if pv.cached(cname, L["say"]):
        return
    ta, tb = _split_bleep(L["say"])
    ma, mb_ = free_voice.make(v, ta), free_voice.make(v, tb)
    sr = 24000
    xa, xb = _decode(ma, sr), _decode(mb_, sr)
    wa, wb = json.load(open(ma + ".words.json")), json.load(open(mb_ + ".words.json"))
    # cut each take to its speech (the mp3 has encoder padding) so the bleep sits right in the gap
    ea = int(min(len(xa), (wa[-1][1] + 0.06) * sr))
    sb = int(max(0, (wb[0][0] - 0.03) * sr))
    xa, xb = xa[:ea], xb[sb:]
    gap = np.zeros(int(0.04 * sr), np.float32)
    n = int(0.42 * sr)
    tt = np.arange(n) / sr
    env = np.minimum(1.0, np.minimum(tt, tt[::-1]) / 0.01)
    tone = (0.22 * np.sin(2 * np.pi * 1000 * tt) * env).astype(np.float32)
    out = np.concatenate([xa, gap, tone, gap, xb])
    off = (len(xa) + 2 * len(gap) + n) / sr - sb / sr
    words = [list(w) for w in wa] + [[w[0] + off, w[1] + off, w[2]] for w in wb]
    base = f"{pv.CACHE}/{pv.key(cname, L['say'])}"
    sf.write(base + ".wav", out, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base + ".wav", "-q:a", "2", base + ".mp3"], check=True)
    os.remove(base + ".wav")
    json.dump(words, open(base + ".mp3.words.json", "w"))
    print(f"bleep take: {base}.mp3 ({len(out) / sr:.2f} s, bleep {len(xa) / sr + 0.04:.2f}-{len(xa) / sr + 0.46:.2f} s)")


_orig_voice_cache = R.voice_cache


def voice_cache(spec, lines):
    for L in lines:
        if BLEEP in L["say"]:
            make_bleep(spec, L)
    _orig_voice_cache(spec, lines)


R.voice_cache = voice_cache

_orig_drawn_spec = R.drawn_spec


def drawn_spec(spec, lines):
    out = _orig_drawn_spec(spec, lines)
    if spec.get("cap_swap"):
        out["cap_swap"] = spec["cap_swap"]
    return out


R.drawn_spec = drawn_spec

# ================================================================================================ HUD states per line


def _num(check):
    return int(check.split(".")[0])


def hud_states(spec):
    v = float(spec.get("panic_start", 9))
    items, out, meter = {}, {}, False
    for L in spec["lines"]:
        st = {"v0": v, "items0": dict(items), "m0": meter}
        if L["shot"].get("meter_in"):
            meter = True
        if "panic" in L:
            v = float(L["panic"])
        if L.get("check"):
            items[_num(L["check"])] = L["check"]
        st.update(v1=v, items1=dict(items), m1=meter)
        out[L["id"]] = st
    return out


def _after(at, s):
    return f"{at}+{s}" if isinstance(at, str) and "|" not in at and not at.endswith("%") else at


def _card_rows(rows, px, mw):
    crow = []
    for k, r in enumerate(rows):
        p_ = px if k == 0 else int(px * 0.8)
        f = ImageFont.truetype(R.FONT, p_)
        while f.getlength(r[0]) > mw and p_ > 46:
            p_ -= 6
            f = ImageFont.truetype(R.FONT, p_)
        crow.append([r[0], r[1], p_])
    return crow


def _expand(spec, lines, durs):
    beats = _orig_expand(spec, lines, durs)
    ST = hud_states(spec)
    segs = spec["segments"]
    big_seg = next((i for i, s in enumerate(segs) if s["chapter"].lower() == "the tree check"), None)
    allL = spec["lines"]
    for b, L in zip(beats, lines):
        a = L["shot"]
        st = ST[L["id"]]
        seg = L["seg"]
        last = L["id"] == allL[-1]["id"]
        if CH_TINT[seg] and not b.get("tint") and not a.get("no_tint") and b.get("scene") not in ("rk_board_bg", "tc_cork"):
            b["tint"] = CH_TINT[seg]
        hud = []
        sfx = list(b.get("sfx", []))
        # ---- PANIC METER
        if st["m1"] and not a.get("no_meter"):
            v0, v1 = st["v0"], st["v1"]
            mat = a.get("meter_at", "55%")
            mp = {"v": v0, "on": 1.0, "pulse": 0.0, "big": a.get("meter_big", 0.0), "swell": 0.0}
            sets = []
            if not st["m0"]:
                mp["on"] = 0.0
                sets.append({"at": a["meter_in"], "dur": 0.55, "p": {"on": 1.0}})
                sfx.append(f"whoosh@{a['meter_in']}")
            if a.get("meter_big_to") is not None:
                sets.append({"at": a.get("meter_big_at", "5%"), "dur": 0.45, "p": {"big": a["meter_big_to"]}})
            if abs(v1 - v0) > 0.01:
                sets.append({"at": mat, "dur": 0.7, "p": {"v": v1}})
                sfx.append(f"click@{mat}")
                if abs(v1 - v0) >= 2:
                    sets += [{"at": mat, "p": {"pulse": 1.0}}, {"at": mat, "dur": 0.9, "p": {"pulse": 0.0}},
                             {"at": mat, "dur": 0.3, "p": {"swell": 1.0}}, {"at": _after(mat, 1.25), "dur": 0.4, "p": {"swell": 0.0}}]
            if last:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            hud.append({"id": "meter", "type": "xm_panic", "pos": [0, 0], "front": True, "p": mp, "set": sets})
        # ---- TREE CHECK list
        i0, i1 = st["items0"], st["items1"]
        list_mode = None
        if i1 and not a.get("no_list"):
            is_big = big_seg is not None and seg == big_seg
            was_big = big_seg is not None and seg == big_seg + 1 and L["id"] == f"s{seg}.l0"
            items, sets = [], []
            lp = {"on": 1.0 if i0 else 0.0, "big": 1.0 if (is_big or was_big) else 0.0}
            cat = a.get("check_at", "45%")
            for n in sorted(i1):
                old = i0.get(n) if i0.get(n) != i1[n] else None
                items.append([n, i1[n], old])
                lp.update({f"t{n}": 1.0, f"h{n}": 0.0, f"n{n}": 1.0 if n in i0 else 0.0, f"r{n}": 0.0 if old else 1.0})
                if n not in i0:
                    sets.append({"at": cat, "dur": 0.7, "p": {f"n{n}": 1.0}})
                elif old:
                    sets.append({"at": cat, "dur": 0.7, "p": {f"r{n}": 1.0}})
            if L.get("check"):
                sfx.append(f"tink@{cat}")
            if not i0:
                sets.insert(0, {"at": cat, "dur": 0.45, "p": {"on": 1.0}})
            if is_big:
                stepn = a.get("list_step")
                first_big = L["id"] == f"s{big_seg}.l0"
                for n in sorted(i1):
                    lp[f"t{n}"] = 1.0 if (stepn and n < stepn) else 0.0
                if first_big:
                    lp["big"] = 0.0
                    for n in sorted(i1):
                        lp[f"t{n}"] = 1.0
                    sets += [{"at": "5%", "dur": 0.6, "p": {"big": 1.0}}]
                    sets += [{"at": "45%", "dur": 0.3, "p": {f"t{n}": 0.0}} for n in sorted(i1)]
                if stepn:
                    sets += [{"at": "3%", "dur": 0.3, "p": {f"h{stepn}": 1.0}},
                             {"at": a.get("tick_at", "70%"), "dur": 0.35, "p": {f"t{stepn}": 1.0}}]
                    sfx.append(f"tink@{a.get('tick_at', '70%')}")
                if a.get("list_all"):
                    for k2, n in enumerate(sorted(i1)):
                        lp[f"t{n}"] = 1.0 if n < 5 else 0.0
                        sets += [{"at": f"{10 + 12 * k2}%", "dur": 0.25, "p": {f"h{n}": 1.0}},
                                 {"at": f"{22 + 12 * k2}%", "dur": 0.25, "p": {f"h{n}": 0.0}}]
                    sets += [{"at": "15%", "dur": 0.35, "p": {"t5": 1.0}}]
            if was_big:
                sets += [{"at": "4%", "dur": 0.6, "p": {"big": 0.0}}]
            if a.get("list_hide"):
                sets += [{"at": "2%", "dur": 0.3, "p": {"on": 0.0}}]
            if last:
                sets.append({"at": "100%", "dur": 0.3, "p": {"on": 0.0}})
            hud.append({"id": "list", "type": "tc_list", "pos": [0, 0], "front": True, "p": dict(lp, items=items), "set": sets})
            list_mode = "big" if is_big else ("compact" if not a.get("list_hide") else None)
        b["actors"] = b["actors"] + hud
        b["sfx"] = sfx
        # ---- the card: under the meter, clear of the list
        if b.get("card"):
            c = b["card"]
            if list_mode == "big":
                c["x"], mw = 480, 860
            elif list_mode == "compact":
                c["x"], mw = min(c.get("x", 730), 730) if c.get("x", 960) != 960 else 730, 1100
            else:
                mw = 1700
            c["rows"] = _card_rows(c["rows"], c["rows"][0][2], mw)
            if st["m1"] and not a.get("no_meter"):
                c["y"] = a.get("card_y", 150)
    return beats


R.expand = _expand

# ================================================================================================ shots

SHOTS = {}
try:
    from drawn_xmas_shots import table as _shots_table   # noqa: E402
    SHOTS = _shots_table()
except ImportError:
    pass


def build(outline, out_spec):
    o = json.load(open(outline))
    R.SHOTS = copy.deepcopy(SHOTS)
    for si, seg in enumerate(o["segments"]):   # the chapter re-hook slam on each chapter's first line
        if si == 0:
            continue
        sh = R.SHOTS.setdefault(f"s{si}.l0", {"f": "wm"})
        kick = seg["chapter"].split(".", 1)[-1].strip().upper() if seg["chapter"][0].isdigit() else seg["chapter"].upper()
        sh.setdefault("ov", []).insert(0, {"type": "suspect", "text": seg.get("chip") or kick, "kicker": kick, "at": 0.0})
        sh.setdefault("sfx", [])[:0] = ["sting@0", "hit@0.05"]
        sh["card_at"] = 1.5
    R.BEATS = list(BEAT_IDS)
    R.build(outline, out_spec)
    spec = json.load(open(out_spec))
    for L in spec["lines"]:
        if L["shot"].get("act"):
            L["act"] = L["shot"]["act"]
    spec.update(burst="loud", voice=o.get("voice", "kokoro:adam-puck"), beat_lines=list(BEAT_IDS), speed_k=float(o.get("speed_k", 0.70)),
                panic_start=o.get("panic_start", 9), music="mystery", music_db=-17,
                end_text="WATCH NEXT  ·  THE SPIDER IN YOUR CORNER", end_hold=float(o.get("end_screen_seconds", 12)),
                cap_swap={"damn": "dang"},
                cap_key=["tree", "christmas", "marshmallow", "eggs", "hundred", "thousand", "twenty-five", "mantis",
                         "aphid", "aphids", "tick", "ticks", "six", "eight", "spiders", "nine", "vacuum", "squash",
                         "spray", "shake", "clip", "nest", "trunk", "lanternfly", "fire", "ignore", "never", "purple",
                         "panic", "starve", "evergreen", "babies", "cannibals", "rumor"],
                _note=spec["_note"].replace("tools/drawn_ranked.py build", "tools/drawn_xmas.py build (drawn_ranked engine)"))
    spec.pop("formant", None)   # E2 plain (Nolan 11/18): free_voice ignores formant anyway; keep it out of the spec
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    todo = [L["id"] for L in spec["lines"] if L["shot"].get("_todo")]
    if todo:
        print("default shots:", ", ".join(todo))


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
    ap.add_argument("--fracs")
    x = ap.parse_args()
    if x.cmd == "build":
        build(x.spec, x.out)
    elif x.cmd == "render":
        R.render(x.spec, x.out, x.lines, x.work)
    elif x.cmd == "linesheet":
        R.linesheet(x.spec, x.out, x.only.split(",") if x.only else None, x.frac, x.work or "/dev/shm/xmas-lines", big=x.big,
                    fracs=[float(v) for v in x.fracs.split(",")] if x.fracs else None)
    elif x.cmd == "check":
        R.check(x.spec)
    elif x.cmd == "lint":
        if x.out and x.out.lower().endswith((".mp4", ".mov", ".mkv")):
            sys.exit("lint: OUT is the voice-stem .wav to write, not the video (%s)" % x.out)
        sys.exit(0 if R.gap_lint(x.spec, x.out, x.work or os.path.splitext(x.out)[0] + "-gaps.txt") else 1)
    elif x.cmd == "voice":
        sp = json.load(open(x.spec))
        R.voice_cache(sp, sp["lines"])
    else:
        raise SystemExit(__doc__)
