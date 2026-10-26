#!/usr/bin/env python3
"""Host shots for tools/v3.py (research/49; Nolan 10/26: "Meatball needs to be in the middle of the screen
talking sometimes"). On a host shot Meatball sits centre-screen behind the investigator's desk, about half the
frame's height, faces the viewer and talks to camera (lip-flap from the word timings, blinks, breathing, a
small talk-bob), with gestures timed to words. Behind him: the case board, drawn here from the Short's own
evidence photos (pinned polaroids, index cards, red string), softly blurred and lit by a desk lamp. Nothing
to license.

Script fields (v3/v4 specs):
  beat "host": true           every shot of the line is a host shot (shots inherit beat fields)
  beat "host": {"moves": ["you@Guess", "lean@worse"], "notes": ["1962"], "fork": true}
      moves: gesture@word (or @seconds), each held ~1.1 s (lean holds to the end of the line):
        you    points at the viewer (the hand comes at the camera, drawn big)
        psst   hand cupped by his mouth, head tilted in: the conspiratorial aside
        lean   leans in to the camera (slow push to +12%) and stays there
        shrug  palms up
        sweat  nervous face with the sweat drop
        shock  hands to face
      notes: index cards on the case board (default: the shot's "board" notes)
      fork:  the Fork, bagged and tagged as evidence, on the desk (the running gag; at most once per Short)
  shot "host": true           only this shot of the line is a host shot (e.g. cut from the evidence photo
                              to Meatball on a spoken word)
Framing: a host line cuts between a medium shot and a close-up every max_shot seconds (a two-camera talk-show
cut), and the camera keeps a slow push, so something changes at least every ~2 s without leaving him.
The beat's "pose" is his base face (deadpan, nervous, think, shock...); a "point" line with no moves opens on "you".
Captions, cards, stamps and the subscribe pill draw over the host shot as usual; his face sits between the
comment card (top) and the captions (bottom) in both 9:16 and 16:9.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import investigate as inv

GESTURES = {"you": "you", "psst": "psst", "lean": "lean", "shrug": "shrug", "sweat": "nervous", "shock": "shock"}
HOLD = 1.1            # seconds a gesture is held before he settles back to his base pose
LEAN_Z = 0.12         # lean-in: extra camera push
CLOSE_Z = 1.16        # close-up framing (zoom about his face) on alternate host pieces
BASE = {"deadpan": "desk", "point": "desk", "present": "desk", "neutral": "desk", "laugh": "desk", "wave": "desk"}
AUTO = {"point": "you", "present": "you", "subpoint": None}   # a pointing line with no moves points at you first


def layout(W, H):
    """Host framing for the frame size: (x centre, desk top y, size px per 1000 units, face y).
    9:16: head top ~610 px (under the comment card), desk at 1430, captions at 1560 on the desk.
    16:9: head top ~380 px, desk at 930, captions at 1000."""
    if H > W:
        return dict(x=W / 2, desk=1430, size=1280, face=900)
    return dict(x=W / 2, desk=930, size=860, face=590)


def parse(host, pose, words, word_time, dur):
    """[(t, pose, hold)] gesture events from beat "host" moves."""
    moves = host.get("moves") if isinstance(host, dict) else None
    if moves is None:
        moves = [AUTO[pose] + "@" + f"{words[0][0] if words else 0.15:.2f}"] if AUTO.get(pose) else []
    out = []
    for m in moves:
        name, _, at = str(m).partition("@")
        if name not in GESTURES:
            raise SystemExit(f"host move {name!r}: use one of {', '.join(GESTURES)}")
        t = word_time(words, at or None, 0.15)
        out.append((t, name, max(0.4, dur - t) if name == "lean" else HOLD))
    return sorted(out)


def lean_curve(events, t):
    """Extra zoom from a lean-in at time t (eases in over 0.35 s)."""
    z = 0.0
    for t0, name, _ in events:
        if name == "lean" and t >= t0:
            u = min(1.0, (t - t0) / 0.35)
            z = max(z, LEAN_Z * u * u * (3 - 2 * u))
    return z


def _polaroid(path, w, rot, seed):
    ph = Image.open(path).convert("RGB")
    h = int(w * min(1.2, max(0.68, ph.height / ph.width)))
    s = max(w / ph.width, h / ph.height)
    ph = ph.resize((int(ph.width * s) + 1, int(ph.height * s) + 1), Image.LANCZOS)
    l, t = (ph.width - w) // 2, (ph.height - h) // 2
    ph = ph.crop((l, t, l + w, t + h))
    m = int(w * 0.06)
    pol = Image.new("RGBA", (w + 2 * m, h + m + int(m * 3.0)), (248, 246, 238, 255))
    pol.paste(ph, (m, m))
    return pol.rotate(rot, expand=True, resample=Image.BICUBIC)


def backdrop(paths, notes, work, vertical=True, case="", past=()):
    """The investigator's wall behind him: cork, the Short's evidence photos pinned as polaroids at the
    edges (where he doesn't cover them), index cards, red string; blurred a little (depth of field), dimmed,
    and lit by a warm desk-lamp pool behind his head. `past`: [(photo path, "CASE #2 PROVEN")] of earlier cases
    (tools/caseboard.py), pinned small and labelled low on the sides: the board grows from case to case.
    Returns an image path (credits copied)."""
    paths = [p for p in dict.fromkeys(paths) if p][:3]
    past = list(past)[-4:]
    key = "|".join([os.path.basename(p) for p in paths] + list(notes) + [str(vertical), case]
                   + [os.path.basename(p) + l for p, l in past])
    out = f"{work}/photos/host_{abs(hash(key)) % 10 ** 10}.jpg"
    if os.path.exists(out):
        return out
    W, H = (1300, 2311) if vertical else (2311, 1300)
    bd = inv._cork(W, H, seed=11).convert("RGBA")
    dr = ImageDraw.Draw(bd)
    if vertical:   # top corners and the high middle stay visible above his shoulders
        spots = [(0.24, 0.17, 0.40, -6), (0.78, 0.20, 0.36, 5), (0.50, 0.08, 0.26, -2)]
        cards = [(0.16, 0.50), (0.86, 0.48), (0.50, 0.215)]
    else:          # 16:9: big evidence left and right of him
        spots = [(0.19, 0.38, 0.27, -5), (0.82, 0.36, 0.24, 4), (0.50, 0.10, 0.12, -2)]
        cards = [(0.13, 0.80), (0.88, 0.78), (0.33, 0.12)]
    pins = []
    for k, p in enumerate(paths):
        cx, cy, fw, rot = spots[k]
        pol = _polaroid(p, int(W * fw), rot, k)
        x, y = int(cx * W - pol.width / 2), int(cy * H - pol.height / 2)
        sh = Image.new("RGBA", pol.size, (0, 0, 0, 0))
        sh.putalpha(pol.getchannel("A").point(lambda v: v * 0.5))
        bd.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (x + 16, y + 20))
        bd.alpha_composite(pol, (x, y))
        pins.append((int(cx * W), y + 34))
    # past cases: small polaroids low on both sides (under the index cards), the case and verdict in marker
    pspots = ([(0.12, 0.64, 0.17, -5), (0.88, 0.63, 0.17, 4), (0.10, 0.355, 0.14, 3), (0.90, 0.345, 0.14, -4)]
              if vertical else [(0.06, 0.62, 0.09, -4), (0.94, 0.60, 0.09, 5), (0.06, 0.20, 0.08, 3),
                                (0.94, 0.20, 0.08, -3)])
    # (drawn on their own layer, added after the depth-of-field blur so the case labels stay readable)
    lf = inv.font(inv.MONO, int(W * (0.034 if vertical else 0.017)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for (pp, label), (cx, cy, fw, rot) in zip(reversed(past), pspots):   # newest case nearest the desk
        pol = _polaroid(pp, int(W * fw), 0, 0)
        pd = ImageDraw.Draw(pol)
        while pd.textlength(label, font=lf) > pol.width * 0.94 and lf.size > 12:
            lf = inv.font(inv.MONO, lf.size - 2)
        lw = pd.textlength(label, font=lf)
        ink = (inv.RED if any(w in label for w in ("BUSTED", "FALSE", "HOAX", "MYTH", "FAKE")) else
               (20, 110, 50) if any(w in label for w in ("PROVEN", "TRUE", "REAL")) else inv.INK)
        pd.text(((pol.width - lw) / 2, pol.height - lf.size * 1.6), label, font=lf, fill=ink)
        pol = pol.rotate(rot, expand=True, resample=Image.BICUBIC)
        x, y = int(cx * W - pol.width / 2), int(cy * H - pol.height / 2)
        layer.alpha_composite(pol, (x, y))
        inv._pin(ImageDraw.Draw(layer), int(cx * W), y + 22, 11)
    fn = inv.font(inv.MONO, int(W * (0.046 if vertical else 0.026)))
    cpins = []
    for k, note in enumerate(list(notes)[:3]):
        nx, ny = int(cards[k][0] * W), int(cards[k][1] * H)
        tw = int(dr.textlength(note, font=fn))
        card = Image.new("RGBA", (tw + 60, int(fn.size * 2.0)), (255, 246, 170, 255))
        cd = ImageDraw.Draw(card)
        cd.line([(0, int(fn.size * 0.35)), (card.width, int(fn.size * 0.35))], fill=(230, 80, 80, 160), width=2)
        cd.text((30, int(fn.size * 0.5)), note, font=fn, fill=(25, 25, 60))
        card = card.rotate([4, -5, 2][k], expand=True, resample=Image.BICUBIC)
        bd.alpha_composite(card, (nx - card.width // 2, ny - card.height // 2))
        cpins.append((nx, ny - card.height // 2 + 20))
    for a, b in zip(pins + cpins, (pins + cpins)[1:]):
        inv._string(dr, a, b, sag=60)
    for p in pins + cpins:
        inv._pin(dr, *p, 15)
    im = bd.convert("RGB").filter(ImageFilter.GaussianBlur(3.2))
    if past:
        im = im.convert("RGBA")
        im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.8)))
        im = im.convert("RGB")
    # lamp light: a warm pool behind his head, the rest of the room falls off to dark
    a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    fy = 0.42 if vertical else 0.45
    d2 = ((xx / W - 0.5) * (1.0 if vertical else 1.7)) ** 2 + ((yy / H - fy) * (0.8 if vertical else 1.0)) ** 2
    light = 0.42 + 0.58 * np.exp(-d2 / 0.09)
    warm = np.array([1.06, 0.98, 0.86], np.float32)
    a = np.clip(a * light[..., None] * warm, 0, 255).astype(np.uint8)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.fromarray(a).save(out, quality=92)
    credit = "".join(open(p + ".credit").read().strip() + "\n" for p in paths + [p for p, _ in past]
                     if os.path.exists(p + ".credit"))
    open(out + ".credit", "w").write(credit.strip() + "\n" if credit else "")
    return out


def desk_img(W, H, desk, case="", fork=None):
    """The desk in front of him (RGBA, full frame width, from desk top to the bottom): walnut top with a lit
    edge, a banker's lamp at the left, a manila case file at the right, and optionally the bagged Fork."""
    h = H - desk + 40
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    top = 40
    for y in range(top, h):   # wood: dark gradient with faint grain
        u = (y - top) / max(1, h - top)
        c = (int(92 - 46 * u), int(56 - 30 * u), int(34 - 18 * u), 255)
        dr.line([(0, y), (W, y)], fill=c)
    rng = np.random.default_rng(3)
    for _ in range(26):
        y0 = int(rng.uniform(top + 30, h))
        dr.line([(0, y0), (W, y0 + rng.integers(-14, 14))], fill=(40, 22, 12, 70), width=2)
    dr.rectangle([0, top, W, top + 10], fill=(150, 98, 60, 255))           # lit front edge
    dr.rectangle([0, top + 10, W, top + 16], fill=(52, 30, 18, 255))
    s = W / 1080 if H > W else H / 1920 * 1.55
    # banker's lamp: brass stem, green shade, light spilling on the desk
    lx = int(W * (0.10 if H > W else 0.16))
    glow = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([lx - 260 * s, top - 30 * s, lx + 300 * s, top + 120 * s], fill=(255, 210, 120, 70))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(30 * s)))
    dr = ImageDraw.Draw(im)
    dr.rectangle([lx - 8 * s, top - 150 * s, lx + 8 * s, top + 4], fill=(176, 140, 60, 255))
    dr.ellipse([lx - 60 * s, top - 6 * s, lx + 60 * s, top + 22 * s], fill=(150, 116, 46, 255))
    dr.chord([lx - 95 * s, top - 215 * s, lx + 95 * s, top - 95 * s], 180, 360, fill=(26, 110, 62, 255),
             outline=(12, 60, 32, 255), width=max(2, int(5 * s)))
    dr.rectangle([lx - 95 * s, top - 157 * s, lx + 95 * s, top - 148 * s], fill=(255, 226, 150, 255))
    # case file: manila folder lying on the desk, typed label, red TOP SECRET band
    fx0, fy0 = int(W * 0.62), int(top + h * 0.42)
    fw, fh = int(W * 0.32), int(h * 0.30)
    dr.polygon([(fx0 + 12 * s, fy0), (fx0 + fw, fy0 - 10 * s), (fx0 + fw - 6 * s, fy0 + fh), (fx0, fy0 + fh + 8 * s)],
               fill=inv.MANILA + (255,), outline=(120, 90, 40, 255))
    f = inv.font(inv.MONO, max(12, int(26 * s)))
    if case:
        dr.text((fx0 + 26 * s, fy0 + 18 * s), case, font=f, fill=inv.INK)
    dr.rectangle([fx0 + 20 * s, fy0 + fh * 0.55, fx0 + fw - 24 * s, fy0 + fh * 0.55 + 30 * s], fill=inv.RED + (230,))
    dr.text((fx0 + 34 * s, fy0 + fh * 0.55 + 1 * s), "TOP SECRET", font=f, fill=(255, 255, 255))
    if fork is not None:   # the Fork, evidence: in a clear bag with a tag (research/39 running gag)
        fk = fork.rotate(-62, expand=True, resample=Image.BICUBIC)
        bx, by = int(W * 0.30), int(top + 30 * s)
        bag = Image.new("RGBA", (fk.width + int(40 * s), fk.height + int(30 * s)), (220, 235, 245, 70))
        ImageDraw.Draw(bag).rectangle([0, 0, bag.width - 1, bag.height - 1], outline=(230, 240, 250, 200),
                                      width=max(2, int(4 * s)))
        bag.alpha_composite(fk, (int(20 * s), int(15 * s)))
        im.alpha_composite(bag, (bx, by))
        dr = ImageDraw.Draw(im)
        dr.rectangle([bx + bag.width - 70 * s, by - 10 * s, bx + bag.width + 40 * s, by + 30 * s], fill=(250, 245, 225, 255))
        dr.text((bx + bag.width - 62 * s, by - 6 * s), "EVIDENCE #?", font=inv.font(inv.MONO, max(10, int(16 * s))),
                fill=inv.RED)
    return np.asarray(im)


def close_zoom(piece_close, f0, f, fps):
    """Camera zoom on a host piece: a slow push (2.5%/s) and, on close-up pieces, the CLOSE_Z framing."""
    return (CLOSE_Z if piece_close else 1.0) * (1.0 + 0.025 * (f - f0) / fps)


def talk_bob(level):
    """A small head-and-shoulders bob with the mouth (drawing units): he leans into stressed syllables."""
    return -4.0 * level


def base_pose(pose):
    return BASE.get(pose, pose)


def apply_face(st):
    """Host: he looks at the viewer (pupils centred) unless thinking."""
    if st.get("brow") != "tilt":
        st["look"] = (0, 0)
    return st


def ok_size(lay, H):
    """The fraction of frame height he fills above the desk (cap to hips) at the host size."""
    return 695 * lay["size"] / 1000 / H


if __name__ == "__main__":
    for W, H in ((1080, 1920), (1920, 1080)):
        lay = layout(W, H)
        print(W, H, lay, f"visible above the desk {ok_size(lay, H):.0%} of frame height", math.isfinite(lay["size"]))
