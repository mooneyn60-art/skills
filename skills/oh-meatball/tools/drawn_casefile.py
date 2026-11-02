#!/usr/bin/env python3
""""Meatball Investigates" case-file kit for tools/drawn.py: archive photos inside drawn frames, the case-file
branding, yellow key-word cards and yellow key-word captions (Nolan 11/2, the bat-bomb mixed drawn + photo cut).

Run a spec through it instead of drawn.py (it registers itself, then hands over to drawn.main()):
  python3 tools/drawn_casefile.py SPEC.json OUT.mp4 [--work DIR] [--stills 1,5,9]

Actors added:
  photo       an archive print (white border, tape), feet = its bottom centre. p: photo + obs (fetched through
              explainer.photo into WORK/photos; or file, a local jpg), w / h (the
              box it fits in, px), tape (bool). It drifts very slightly; never upscaled past 1.5x
  bat_bomb    the WWII bat-bomb canister: finned bomb body with tray bands, nose right. p: open (0..1 trays out)
  firebomb    the tiny pencil-shaped incendiary a bat carried; p: lit (0..1 a flame at its tail)
  hangar      a Quonset-hut aircraft hangar on its floor line, ~900 wide. p: fire (0..1)
  fuel_tank   a round fuel tank on legs, ~360 wide
  flames      a flickering fire cluster, ~300 wide. p: n (tongues), k (size 0..1)
  armed_bat   the stage bat (spec "stage" creature_cfg) with a small firebomb strapped under it. p: bomb (bool)
Spec additions:
  "series": {"text", "case"}   the case-file tag top left on every frame (investigate.series_imgs)
  beat 0 "headline"            a red-tape headline on frame 0 (held "headline_s", and again for the last 0.5 s)
  beat "label": {"text", "at"} a big yellow word card popping in on the word
  beat "stamp": {"text", "at"} the verdict stamp slam (investigate.stamp_img) with a camera shake
  beat "keys": [words]         the caption's yellow word (else any number, else the chunk's longest word)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn  # noqa: E402
import investigate  # noqa: E402
from drawn_creatures import build  # noqa: E402
from drawn_kit import OUT, PAL, flat, hexc, p_ellipse, p_poly, p_rrect, shape, src, stroke  # noqa: E402

P = PAL
YELLOW = (255, 214, 10)
_PH = {}


def photo(ctx, t, p):
    key = (p["file"], p.get("w", 960), p.get("h", 1100))
    if key not in _PH:
        im = Image.open(p["file"]).convert("RGBA")
        k = min(key[1] / im.width, key[2] / im.height, 1.5)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        _PH[key] = drawn.pil_to_surface(im)
    surf, _buf = _PH[key]
    w, h = surf.get_width(), surf.get_height()
    z = 1.0 + 0.012 * math.sin(t * 0.9)
    ctx.scale(z, z)
    b = 22
    ctx.save()
    p_rrect(ctx, -w / 2 - b + 10, -h - 2 * b + 14, w + 2 * b, h + 2 * b, 6)   # drop shadow
    src(ctx, (0, 0, 0), 0.35)
    ctx.fill()
    ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -w / 2 - b, -h - 2 * b, w + 2 * b, h + 2 * b, 6), (0.97, 0.96, 0.92), OUT * 0.6, None)
    ctx.save()
    ctx.set_source_surface(surf, -w / 2, -h - b)
    ctx.paint()
    ctx.restore()
    if p.get("tape", True):
        for sx in (-1, 1):
            ctx.save()
            ctx.translate(sx * (w / 2 - 30), -h - 2 * b + 4)
            ctx.rotate(sx * 0.5)
            flat(ctx, lambda c: c.rectangle(-70, -22, 140, 44), (0.93, 0.86, 0.62), a=0.85)
            ctx.restore()


def bat_bomb(ctx, t, p):
    body = hexc("#7d8a6a")
    u = p.get("open", 0.0)
    for k in range(5):   # trays sliding out of the back
        if u > 0.01:
            shape(ctx, lambda c, k=k: p_rrect(c, -330 - 120 * u * (1 - k / 6), -86 + k * 34, 120, 24, 6),
                  hexc("#c9b48a"), OUT * 0.5, None)
    shape(ctx, lambda c: (c.move_to(-280, -110), c.line_to(170, -110), c.curve_to(330, -110, 360, 0, 360, 0),
                          c.curve_to(360, 0, 330, 110, 170, 110), c.line_to(-280, 110), c.close_path()),
          body, OUT, (0.0, 0.18))
    for x in (-180, -60, 60):
        stroke(ctx, [(x, -108), (x, 108)], OUT * 0.7)
    for d in (-1, 1):   # tail fins
        shape(ctx, lambda c, d=d: p_poly(c, [(-280, 70 * d), (-400, 175 * d), (-430, 175 * d), (-380, 20 * d)]),
              hexc("#66725a"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -440, -20, 170, 40, 10), hexc("#66725a"), OUT * 0.8, None)
    flat(ctx, lambda c: p_ellipse(c, 250, -50, 34, 16, -0.4), (1, 1, 1), a=0.35)


def firebomb(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -60, -14, 120, 28, 14), hexc("#c0503a"), OUT * 0.6, (0, 0.25))
    stroke(ctx, [(-20, -14), (-20, 14)], OUT * 0.5)
    stroke(ctx, [(20, -14), (20, 14)], OUT * 0.5)
    lit = p.get("lit", 0.0)
    if lit > 0.01:
        f = 0.8 + 0.2 * math.sin(t * 31)
        shape(ctx, lambda c: p_poly(c, [(-60, -12), (-60 - 70 * lit * f, 0), (-60, 12)]), (1, 0.62, 0.1), OUT * 0.4, None)


def flames(ctx, t, p):
    n, k = int(p.get("n", 5)), p.get("k", 1.0)
    if k < 0.02:
        return
    for i in range(n):
        x = (i - (n - 1) / 2) * 70 * k
        hh = (170 + 90 * math.sin(t * 9 + i * 1.7)) * k * (1.15 if i % 2 else 0.85)
        w = 62 * k
        shape(ctx, lambda c, x=x, hh=hh, w=w: (c.move_to(x - w, 0), c.curve_to(x - w, -hh * 0.5, x - w * 0.2, -hh * 0.7, x, -hh),
                                                c.curve_to(x + w * 0.2, -hh * 0.7, x + w, -hh * 0.5, x + w, 0), c.close_path()),
              (0.98, 0.45, 0.12), OUT * 0.6, None)
        shape(ctx, lambda c, x=x, hh=hh, w=w: (c.move_to(x - w * 0.5, 0), c.curve_to(x - w * 0.5, -hh * 0.3, x, -hh * 0.45, x, -hh * 0.6),
                                                c.curve_to(x, -hh * 0.45, x + w * 0.5, -hh * 0.3, x + w * 0.5, 0), c.close_path()),
              (1, 0.85, 0.25), 0, None)


def hangar(ctx, t, p):
    shape(ctx, lambda c: (c.move_to(-450, 0), c.curve_to(-450, -560, 450, -560, 450, 0), c.close_path()),
          hexc("#9aa3a8"), OUT, (0.15, 0.05))
    for x in range(-360, 400, 90):
        stroke(ctx, [(x, -3), (x * 0.92, -400 + abs(x) * 0.55)], OUT * 0.4)
    shape(ctx, lambda c: c.rectangle(-210, -260, 420, 260), hexc("#5d6870"), OUT * 0.8, None)
    fire = p.get("fire", 0.0)
    if fire > 0.01:
        for x, y, s in ((-250, -330, 1.0), (60, -410, 1.25), (300, -260, 0.9)):
            ctx.save()
            ctx.translate(x, y)
            flames(ctx, t + x, {"n": 4, "k": fire * s})
            ctx.restore()
        for k in range(4):   # smoke
            u = (t * 0.35 + k / 4) % 1
            flat(ctx, lambda c, u=u, k=k: p_ellipse(c, -100 + 80 * k + 60 * u, -560 - 420 * u, 90 + 120 * u, 70 + 90 * u),
                 (0.25, 0.25, 0.27), a=0.55 * fire * (1 - u))


def fuel_tank(ctx, t, p):
    for x in (-130, 130):
        stroke(ctx, [(x, 0), (x, -150)], OUT * 1.6)
    shape(ctx, lambda c: p_rrect(c, -180, -330, 360, 190, 90), hexc("#c8c2b0"), OUT, (0.1, 0.2))
    stroke(ctx, [(-120, -330), (-120, -140)], OUT * 0.5)
    stroke(ctx, [(120, -330), (120, -140)], OUT * 0.5)


_BAT = {}


def armed_bat(ctx, t, p):
    if "fn" not in _BAT:
        _BAT["fn"] = build(_BAT["cfg"])
    _BAT["fn"](ctx, t, p)
    if p.get("bomb", True):
        ctx.save()
        ctx.translate(10, -_BAT["cfg"].get("leg_len", 40) - 28)
        ctx.scale(1.5, 1.5)
        firebomb(ctx, t, {"lit": p.get("lit", 0.0)})
        ctx.restore()


# ---------------------------------------------------------------- overlays

def _font(px):
    return ImageFont.truetype(drawn.FONT, px)


_IMG = {}


def word_card(text):
    if ("w", text) not in _IMG:
        f = _font(150)
        lines = text.split("\n")
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        tw = int(max(d.textlength(x, font=f) for x in lines)) + 60
        im = Image.new("RGBA", (tw, len(lines) * 175 + 60), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        for k, line in enumerate(lines):
            dr.text(((tw - dr.textlength(line, font=f)) / 2, 10 + k * 175), line, font=f, fill=YELLOW + (255,),
                    stroke_width=12, stroke_fill=(0, 0, 0, 255))
        im = im.rotate(5, expand=True, resample=Image.BICUBIC)
        k = min(1.0, (drawn.W - 90) / im.width)
        if k < 1:
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        _IMG[("w", text)] = np.asarray(im)
    return _IMG[("w", text)]


def paste(dst, rgba, cx, cy, s=1.0):
    """Alpha-composite an RGBA array onto a BGRA frame, centred at cx, cy, scaled by s."""
    if s != 1.0:
        im = Image.fromarray(rgba)
        rgba = np.asarray(im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR))
    h, w = rgba.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(dst.shape[1], x0 + w), min(dst.shape[0], y0 + h)
    if xa >= xb or ya >= yb:
        return
    a = rgba[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32)
    al = a[..., 3:4] / 255
    reg = dst[ya:yb, xa:xb, :3].astype(np.float32)
    dst[ya:yb, xa:xb, :3] = (reg * (1 - al) + a[..., [2, 1, 0]] * al).astype(np.uint8)


def pop(u):   # 0 -> overshoot -> 1 over the first 0.25 s
    if u <= 0:
        return 0.0
    if u >= 0.25:
        return 1.0
    x = u / 0.25
    return 0.6 + 0.55 * math.sin(x * math.pi * 0.75)


def overlay(frame, T):
    """Series tag, headline, word cards and stamps on one BGRA frame (in place)."""
    beats = drawn.G["beats"]
    bi = max(i for i, b in enumerate(beats) if b["t0"] <= T + 1e-9)
    b = beats[bi]
    t = T - b["t0"]
    total = beats[-1]["t0"] + beats[-1]["dur"]
    if CF.get("tag") is not None:
        tag = CF["tag"]
        paste(frame, tag, 30 + tag.shape[1] / 2, 150 + tag.shape[0] / 2)
    if CF.get("headline") is not None and (T < CF["headline_s"] or T > total - 0.5):
        paste(frame, CF["headline"], drawn.W / 2, 420)
    lab = b.get("label")
    if lab:
        t1 = drawn.at_time(b["words"], lab.get("at"), 0.0)
        if t >= t1:
            paste(frame, word_card(lab["text"]), drawn.W / 2, lab.get("y", 470), pop(t - t1))
    st = b.get("stamp")
    if st:
        t1 = drawn.at_time(b["words"], st.get("at"), 0.0)
        if t >= t1:
            if ("s", st["text"]) not in _IMG:
                _IMG[("s", st["text"])] = investigate.stamp_img(st["text"], st.get("color"), 1.35)
            u = t - t1
            s = 1.0 if u > 0.16 else 1.8 - 0.8 * u / 0.16   # slams down from big and settles
            paste(frame, _IMG[("s", st["text"])], drawn.W / 2, st.get("y", 760), s)


CF = {}
_orig_frame = drawn.frame_at


def frame_at(f):
    outs = _orig_frame(f)
    T = f / drawn.G["fps"]
    res = []
    for o in outs:
        a = np.frombuffer(o, np.uint8).reshape(drawn.H, drawn.W, 4).copy()
        overlay(a, T)
        res.append(a.tobytes())
    return res


# ---------------------------------------------------------------- captions: the key word yellow

_orig_chunks = drawn.caption_chunks


def caption_chunks(beats):
    out = []
    for b in beats:
        keys = {k.lower().strip(".,!?") for k in b.get("keys", [])}
        for s, e, text in _orig_chunks([b]):
            ws = text.split()
            hot = [q for q, w in enumerate(ws) if w.lower().strip(".,!?'") in keys or any(c.isdigit() or c == "$" for c in w)]
            if not hot:
                hot = [max(range(len(ws)), key=lambda q: len(ws[q].strip(".,!?")))]
            out.append((s, e, " ".join(("\x01" + w) if q in hot else w for q, w in enumerate(ws))))
    return out


def caption_img(text, px):
    key = (text, px)
    if key not in drawn._CAP:
        f = _font(px)
        sw = max(5, px // 11)
        toks = text.split(" ")
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        space = d.textlength(" ", font=f)
        widths = [d.textlength(w.lstrip("\x01"), font=f) for w in toks]
        tw = int(sum(widths) + space * (len(toks) - 1)) + 2 * sw + 8
        x0, y0, x1, y1 = d.textbbox((0, 0), "AGJQ", font=f, stroke_width=sw)
        im = Image.new("RGBA", (tw, y1 - y0 + 8), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        x = sw + 4
        for w, ww in zip(toks, widths):
            dr.text((x, 4 - y0), w.lstrip("\x01"), font=f, fill=(YELLOW if w.startswith("\x01") else (255, 255, 255)) + (255,),
                    stroke_width=sw, stroke_fill=(17, 17, 17, 255))
            x += ww + space
        if im.width > drawn.W - 40:
            k = (drawn.W - 40) / im.width
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        drawn._CAP[key] = im
    return drawn._CAP[key]


def resolve_photos(raw, work):
    """Photo actors name an archive picture as {"photo": label, "obs": "wm:File.jpg" | "ov:id"}: fetch (or reuse)
    it into WORK/photos through explainer.photo, so the spec never holds a local path."""
    import explainer
    os.makedirs(f"{work}/photos", exist_ok=True)
    for b in raw["beats"]:
        for a in b.get("actors", []):
            p = a.get("p", {})
            if a.get("type") == "photo" and "file" not in p:
                p["file"] = explainer.photo(p["photo"], 0, work, p.get("obs"))


def setup(spec_path):
    import json
    raw = json.load(open(spec_path))
    argv = sys.argv
    work = argv[argv.index("--work") + 1] if "--work" in argv else os.path.join(
        os.path.dirname(os.path.abspath(argv[2])), ".work-" + os.path.splitext(os.path.basename(argv[2]))[0])
    resolve_photos(raw, work)
    resolved = f"{work}/spec.resolved.json"
    json.dump(raw, open(resolved, "w"), ensure_ascii=False)
    sys.argv[1] = resolved
    st = raw.get("stage", {})
    _BAT["cfg"] = dict(st.get("creature_cfg", {}))
    drawn.ACTORS.update(photo=photo, bat_bomb=bat_bomb, firebomb=firebomb, flames=flames, hangar=hangar,
                        fuel_tank=fuel_tank, armed_bat=armed_bat)
    armed_bat.cfg = _BAT["cfg"]   # drawn_acting reads the hero's size from the actor's cfg
    if raw.get("series"):
        CF["tag"] = investigate.series_imgs(raw["series"], drawn.W)[1]
    hl = raw["beats"][0].get("headline")
    if hl:
        CF["headline"] = investigate.headline_img(hl, drawn.W)
        CF["headline_s"] = float(raw["beats"][0].get("headline_s", 2.0))
    drawn.frame_at = frame_at
    drawn.caption_chunks = caption_chunks
    drawn.caption_img = caption_img


if __name__ == "__main__":
    setup(sys.argv[1])
    drawn.main()
