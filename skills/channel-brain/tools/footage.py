#!/usr/bin/env python3
"""Find licensed REAL animal video for the realistic look (STYLE_DECISION_2026-10-29.md).

    python3 footage.py "cassowary"                      list candidates from every source that works
    python3 footage.py "camel cricket" --get 3 --out footage/camel-cricket   download the best 3 + credits.json

Sources (each skipped quietly when unavailable):
  wikimedia  Wikimedia Commons video, no key. Keeps CC0 / public domain / CC BY / CC BY-SA only.
             BY and BY-SA need the credit line in the description (credits.json has it ready).
  pexels     Pexels videos (free licence, no credit required); needs env PEXELS_API_KEY (free at pexels.com/api)
  pixabay    Pixabay videos (free licence); needs env PIXABAY_API_KEY (free at pixabay.com/api/docs)
Ranked: portrait or HD first, title actually naming the animal, shortest clips first (easier to cut).
Every download is appended to footage/credits.json: put the credit lines in the video description.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.error
import urllib.request

UA = "MeatballFootageFinder/0.1 (https://github.com/mooneyn60-art/skills; channel research)"
OK_LICENSES = r"^(cc0|public domain|pd|cc by( |-)?\d|cc by-sa( |-)?\d)"


def get(url, headers=None, tries=4):
    import time
    for k in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:  # 429 = rate limited: wait as told (or 5, 10, 20 s) and retry
            if e.code != 429 or k == tries - 1:
                raise
            time.sleep(min(int(e.headers.get("Retry-After") or 5 * 2 ** k), 30))


def wikimedia(q, n=20):
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6"
           f"&gsrlimit={n}&gsrsearch={urllib.parse.quote(q + ' filemime:video')}"
           "&prop=imageinfo&iiprop=url%7Cextmetadata%7Csize%7Cmime")
    out = []
    for p in get(url).get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = re.sub("<[^>]+>", "", m.get("LicenseShortName", {}).get("value", "")).strip()
        if not re.match(OK_LICENSES, lic.lower()):
            continue
        artist = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "unknown")).strip()
        out.append({"source": "wikimedia", "title": p["title"].replace("File:", ""), "url": ii["url"],
                    "page": ii.get("descriptionurl", ""), "w": ii.get("width"), "h": ii.get("height"),
                    "secs": float(m.get("Length", {}).get("value", 0) or 0) if str(m.get("Length", {}).get("value", "")).replace(".", "").isdigit() else None,
                    "license": lic, "credit": f"{p['title'].replace('File:', '')} by {artist}, {lic}, via Wikimedia Commons"})
    return out


def pexels(q, n=20):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return []
    d = get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page={n}", {"Authorization": key})
    out = []
    for v in d.get("videos", []):
        f = max(v["video_files"], key=lambda x: (x.get("height") or 0) if (x.get("height") or 0) <= 1920 else 0)
        out.append({"source": "pexels", "title": v.get("url", "").rstrip("/").split("/")[-1], "url": f["link"],
                    "page": v["url"], "w": f.get("width"), "h": f.get("height"), "secs": v.get("duration"),
                    "license": "Pexels License", "credit": f"Video by {v['user']['name']} on Pexels"})
    return out


def pixabay(q, n=20):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return []
    d = get(f"https://pixabay.com/api/videos/?key={key}&q={urllib.parse.quote(q)}&per_page={n}")
    out = []
    for v in d.get("hits", []):
        f = v["videos"].get("large") or v["videos"].get("medium")
        if not f or not f.get("url"):
            continue
        out.append({"source": "pixabay", "title": v.get("tags", ""), "url": f["url"], "page": v["pageURL"],
                    "w": f.get("width"), "h": f.get("height"), "secs": v.get("duration"),
                    "license": "Pixabay Content License", "credit": f"Video by {v['user']} on Pixabay"})
    return out


def rank(items, q):
    words = [w for w in q.lower().split() if len(w) > 2]
    def score(x):
        named = all(w in (x["title"] + " " + x["page"]).lower() for w in words)
        tall = (x.get("h") or 0) >= (x.get("w") or 1)
        hd = (x.get("h") or 0) >= 720 or (x.get("w") or 0) >= 1280
        return (named, tall, hd, -(x.get("secs") or 99))
    return [x for x in sorted(items, key=score, reverse=True) if all(w in (x["title"] + " " + x["page"]).lower() for w in words) or x["source"] != "wikimedia"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--get", type=int, default=0, help="download the best N")
    ap.add_argument("--out", default="footage")
    a = ap.parse_args()
    items = []
    for fn in (pexels, pixabay, wikimedia):
        try:
            items += fn(a.query)
        except Exception as e:
            print(f"[{fn.__name__} skipped: {e}]", file=sys.stderr)
    items = rank(items, a.query)
    if not items:
        print("No licensed video found. Try a broader name (genus or common name), or set PEXELS_API_KEY / PIXABAY_API_KEY.")
        return 1
    for i, x in enumerate(items[:15]):
        print(f"{i + 1:2d}. [{x['source']}] {x['title'][:60]}  {x.get('w')}x{x.get('h')}  {x.get('secs') or '?'} s  {x['license']}\n    {x['page']}")
    if a.get:
        os.makedirs(a.out, exist_ok=True)
        cpath = os.path.join(a.out, "credits.json")
        credits = json.load(open(cpath)) if os.path.exists(cpath) else []
        for x in items[:a.get]:
            ext = os.path.splitext(urllib.parse.urlparse(x["url"]).path)[1] or ".mp4"
            name = re.sub(r"[^a-z0-9]+", "-", f"{x['source']}-{x['title']}".lower())[:60] + ext
            req = urllib.request.Request(x["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(os.path.join(a.out, name), "wb") as f:
                f.write(r.read())
            credits.append({"file": name, **x})
            print(f"saved {a.out}/{name}")
        json.dump(credits, open(cpath, "w"), indent=1)
        print(f"credits -> {cpath} (paste the credit lines into the description)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
