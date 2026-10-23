#!/usr/bin/env python3
"""Contact sheet of reusable images (CC0, public domain, CC BY, CC BY-SA) from Openverse, for history
beats that need art, fossils or museum pieces instead of a live-animal photo. Pick by looking at the
sheet, then use {"photo": "<label>", "obs": "ov:<id>"} in a script; explainer.py fetches and credits it.

Usage: openverse.py OUTDIR "query" ["query" ...]   -> OUTDIR/ov_<slug>.jpg + ov_<slug>.json (ids)
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

UA = {"User-Agent": "MeatballMyths/1.0"}


def search(q, n=15):
    qs = urllib.parse.urlencode({"q": q, "license": "cc0,pdm,by,by-sa", "page_size": 20})
    req = urllib.request.Request(f"https://api.openverse.org/v1/images/?{qs}", headers=UA)
    res = json.load(urllib.request.urlopen(req, timeout=60))["results"]
    # Landscape-ish and big enough for a 1080p panel.
    return [r for r in res if (r.get("width") or 0) >= 800 and (r.get("width") or 0) >= 0.9 * (r.get("height") or 1)][:n]


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for q in sys.argv[2:]:
        slug = re.sub(r"\W+", "_", q).strip("_")
        try:
            res = search(q)
        except Exception as e:
            print(q, "search failed:", e)
            continue
        sheet = Image.new("RGB", (5 * 300, 3 * 230), "white")
        d = ImageDraw.Draw(sheet)
        for i, r in enumerate(res):
            try:
                req = urllib.request.Request(r.get("thumbnail") or r["url"], headers=UA)
                im = Image.open(urllib.request.urlopen(req, timeout=30)).convert("RGB")
            except Exception:
                continue
            im.thumbnail((290, 190))
            sheet.paste(im, ((i % 5) * 300, (i // 5) * 230))
            d.text(((i % 5) * 300 + 5, (i // 5) * 230 + 195), f"{i} {r['license']} {r['title'][:30]}", fill="red")
        sheet.save(f"{out}/ov_{slug}.jpg")
        json.dump([{"id": r["id"], "title": r["title"], "license": r["license"], "creator": r.get("creator")} for r in res],
                  open(f"{out}/ov_{slug}.json", "w"), indent=1)
        print(q, len(res))


if __name__ == "__main__":
    main()
