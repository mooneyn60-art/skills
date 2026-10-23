#!/usr/bin/env python3
"""Contact sheet of public-domain (CC0) artworks and artifacts from The Met's Open Access API, for
history beats that need art, mummies, mosaics or old paintings instead of a live-animal photo.
Pick by looking at the sheet, then use {"photo": "<label>", "obs": "met:<objectID>"} in a script;
explainer.py fetches and credits it.

Usage: museum.py OUTDIR "query" ["query" ...]   -> OUTDIR/met_<slug>.jpg + met_<slug>.json
"""
import concurrent.futures as cf
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

API = "https://collectionapi.metmuseum.org/public/collection/v1"
UA = {"User-Agent": "MeatballMyths/1.0"}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))


def obj(i):
    try:
        o = get(f"{API}/objects/{i}")
    except Exception:
        return None
    return o if o.get("isPublicDomain") and o.get("primaryImageSmall") else None


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for q in sys.argv[2:]:
        slug = re.sub(r"\W+", "_", q).strip("_")
        qs = urllib.parse.urlencode({"hasImages": "true", "isPublicDomain": "true", "q": q, "limit": 30})
        ids = get(f"{API}.1/search?{qs}").get("objectIDs") or []
        with cf.ThreadPoolExecutor(8) as ex:
            objs = [o for o in ex.map(obj, ids) if o][:15]
        sheet = Image.new("RGB", (5 * 300, 3 * 230), "white")
        d = ImageDraw.Draw(sheet)
        keep = []
        for i, o in enumerate(objs):
            try:
                im = Image.open(urllib.request.urlopen(urllib.request.Request(o["primaryImageSmall"], headers=UA), timeout=30)).convert("RGB")
            except Exception:
                continue
            im.thumbnail((290, 190))
            sheet.paste(im, ((i % 5) * 300, (i // 5) * 230))
            d.text(((i % 5) * 300 + 5, (i // 5) * 230 + 195), f"{i} {o['title'][:34]}", fill="red")
            keep.append({"i": i, "id": o["objectID"], "title": o["title"], "date": o.get("objectDate"), "culture": o.get("culture")})
        sheet.save(f"{out}/met_{slug}.jpg")
        json.dump(keep, open(f"{out}/met_{slug}.json", "w"), indent=1)
        print(q, len(keep))


if __name__ == "__main__":
    main()
