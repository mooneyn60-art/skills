#!/usr/bin/env python3
"""Wolf-rule check for long-form thumbnails (OPERATIONS.md "Wolf rule", 10/26). The wolf thumbnail
(Uqj0QL8G0d4, 57 views in 2 days) beat every Meatball-face thumbnail, so long-form thumbnails must have:
  1. ONE recognizable subject, sharp and bright, filling 45-60% of the frame (bounding box)
  2. a visual contrast, a transformation, or one shocking detail (declared as "hook")
  3. 1-3 words of text, huge (cap height >= 9 px at 168x94) and high contrast, NOT repeating the title
  4. Meatball at most ~20% of the frame, a reaction, never the subject
  5. readable at 168x94 (the downscale is saved: LOOK at it)
  6. no more than 2 cut-outs besides Meatball; no clutter (<= 5 elements, calm background)

Usage:
  thumbcheck.py IMG.jpg                     # reads IMG.json written by wolf_thumb.py, if present
  thumbcheck.py IMG.jpg --title "..." --text "HOW?!" --subject x0,y0,x1,y1 [--meatball x0,y0,x1,y1]
                [--cutouts N] [--elements N] [--hook transformation|contrast|detail] [--text-box x0,y0,x1,y1]
Boxes are 1280x720 pixels. Writes IMG_168.png and IMG_168x4.png (nearest-neighbour blow-up to look at).
Prints a score out of 100 and exits 1 when a hard rule fails.
"""
import argparse
import json
import os
import re
import sys

import numpy as np
from PIL import Image, ImageFilter

W, H = 1280, 720
STOP = set("a an the of in on to is are was were it its and or for you your that this what how why who with "
           "one be by at from just not no do did does as so".split())


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP]


def repeats_title(text, title):
    """Share of the text's content words that the title already says (4-letter stems: hid ~ hiding)."""
    tw = words(text)
    if not tw or not title:
        return 0.0
    stems = {w[:4] for w in words(title)}
    return sum(w[:4] in stems for w in tw) / len(tw)


def luma(im):
    return np.asarray(im.convert("L"), dtype=np.float32)


def sharpness(gray):
    """Variance of a 4-neighbour Laplacian on a 320 px-wide copy, so sizes compare."""
    g = gray
    lap = -4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    return float(lap.var())


def box_area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1]) / (W * H)


def check(img_path, spec):
    im = Image.open(img_path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    base = img_path.rsplit(".", 1)[0]
    small = im.resize((168, 94), Image.LANCZOS)
    small.save(base + "_168.png")
    small.resize((168 * 4, 94 * 4), Image.NEAREST).save(base + "_168x4.png")

    res, score = [], 100

    def rule(name, ok, detail, hard=True, cost=15):
        nonlocal score
        res.append({"rule": name, "ok": bool(ok), "hard": hard, "detail": detail})
        if not ok:
            score -= cost

    text = spec.get("text", "")
    n_words = len(text.split())
    rule("text 1-3 words", 1 <= n_words <= 3, f"{n_words} words: {text!r}")
    rep = repeats_title(text, spec.get("title", ""))
    rule("text does not repeat the title", rep < 0.5, f"{rep:.0%} of text words are in the title")

    sb = spec.get("subject_box")
    if sb:
        a = box_area(sb)
        rule("one subject fills 45-60%", 0.45 <= a <= 0.60, f"subject box {a:.0%} of frame",
             hard=not (0.40 <= a <= 0.66), cost=10 if 0.40 <= a <= 0.66 else 20)
        x0, y0, x1, y1 = (max(0, int(v)) for v in sb)
        crop = im.crop((x0, y0, min(W, x1), min(H, y1)))
        mask = spec.get("subject_mask")
        g = luma(crop.resize((320, max(1, int(320 * crop.height / max(1, crop.width))))))
        if mask and os.path.exists(mask):  # only the subject's own pixels, not the background in its box
            m = np.asarray(Image.open(mask).convert("L").resize((g.shape[1], g.shape[0]))) > 128
            vals = g[m] if m.sum() > 50 else g.ravel()
        else:
            vals = g.ravel()
        bright, spread = float(vals.mean()), float(np.percentile(vals, 90) - np.percentile(vals, 10))
        sh = sharpness(g)
        rule("subject bright", bright >= 85, f"mean luma {bright:.0f} (>= 85)")
        rule("subject contrasty", spread >= 70, f"p10-p90 spread {spread:.0f} (>= 70)", hard=False, cost=8)
        rule("subject sharp", sh >= 60, f"Laplacian var {sh:.0f} (>= 60)")
    else:
        rule("one subject fills 45-60%", False, "no subject box given (pass --subject or a spec)")

    mb = spec.get("meatball_box")
    if mb:
        a = box_area(mb)
        rule("Meatball <= 20% (reaction only)", a <= 0.20, f"Meatball box {a:.0%} of frame",
             hard=a > 0.24, cost=20 if a > 0.24 else 8)
        if sb:
            rule("Meatball smaller than the subject", box_area(mb) < 0.5 * box_area(sb),
                 f"{box_area(mb):.0%} vs subject {box_area(sb):.0%}")
    else:
        rule("Meatball present as a reaction", False, "no Meatball box", hard=False, cost=5)

    cut = spec.get("cutouts", 1)
    rule("<= 2 cut-outs besides Meatball", cut <= 2, f"{cut} cut-outs")
    el = spec.get("elements", 0)
    if el:
        rule("<= 5 elements (no clutter)", el <= 5, f"{el} elements (cut-outs + Meatball + text + devices)")
    rule("hook: contrast/transformation/detail", spec.get("hook") in ("transformation", "contrast", "detail"),
         f"hook={spec.get('hook')}", hard=False, cost=10)

    # Background calm: edge density outside the subject, Meatball and text boxes, at feed size.
    e = np.asarray(small.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32)
    keep = np.ones_like(e, dtype=bool)
    for b in (sb, mb, spec.get("text_box")):
        if b:
            sx = 168 / W
            keep[int(b[1] * sx):int(b[3] * sx) + 1, int(b[0] * sx):int(b[2] * sx) + 1] = False
    busy = float((e[keep] > 40).mean()) if keep.any() else 0.0
    rule("calm background", busy <= 0.22, f"{busy:.0%} edge pixels outside subject/text/Meatball (<= 22%)",
         hard=False, cost=10)

    tb = spec.get("text_box")
    cap = spec.get("cap_px")
    if cap:
        cap168 = cap * 94 / H
        rule("text huge (cap >= 9 px at 168x94)", cap168 >= 9, f"cap height {cap168:.1f} px at 168x94")
    if tb:
        sx = 168 / W
        t = np.asarray(small.convert("L"), dtype=np.float32)[int(tb[1] * sx):int(tb[3] * sx) + 1,
                                                             int(tb[0] * sx):int(tb[2] * sx) + 1]
        c = float(np.percentile(t, 95) - np.percentile(t, 5)) if t.size else 0
        rule("text high contrast at 168x94", c >= 150, f"text-box luma p5-p95 {c:.0f} (>= 150)")

    score = max(0, score)
    failed = [r for r in res if not r["ok"] and r["hard"]]
    return {"image": img_path, "score": score, "pass": not failed, "preview": base + "_168x4.png", "rules": res}


def box(s):
    return [float(v) for v in s.split(",")] if s else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--title")
    ap.add_argument("--text")
    ap.add_argument("--subject")
    ap.add_argument("--meatball")
    ap.add_argument("--text-box")
    ap.add_argument("--cap-px", type=float)
    ap.add_argument("--cutouts", type=int)
    ap.add_argument("--elements", type=int)
    ap.add_argument("--hook")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sp = a.image.rsplit(".", 1)[0] + ".json"
    spec = json.load(open(sp)) if os.path.exists(sp) else {}
    for k, v in (("title", a.title), ("text", a.text), ("subject_box", box(a.subject)),
                 ("meatball_box", box(a.meatball)), ("text_box", box(a.text_box)), ("cap_px", a.cap_px),
                 ("cutouts", a.cutouts), ("elements", a.elements), ("hook", a.hook)):
        if v is not None:
            spec[k] = v
    r = check(a.image, spec)
    if a.json:
        print(json.dumps(r, indent=1))
    else:
        for x in r["rules"]:
            mark = "ok  " if x["ok"] else ("FAIL" if x["hard"] else "warn")
            print(f"  {mark} {x['rule']}: {x['detail']}")
        print(f"{'PASS' if r['pass'] else 'FAIL'} {r['score']}/100 {a.image}  look at: {r['preview']}")
    sys.exit(0 if r["pass"] else 1)


if __name__ == "__main__":
    main()
