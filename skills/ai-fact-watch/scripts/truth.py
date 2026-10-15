#!/usr/bin/env python3
"""Collect a business's ground truth from its OWN public sources.

Usage:
  python truth.py --name "The Viridian Bookshop" --town Willoughby --region OH \\
      --website https://viridianbookshop.com \\
      [--listing URL ...]      # Google Business-style / directory pages to cross-check
      [--social URL ...]       # Facebook / Instagram / TikTok bios (often blocked; logged)
      [--press URL ...]        # news articles quoting the owner (evidence only)
      [--twin "Name|address|phone|url|note" ...]   # known same-name businesses
      [--set field=value --set-source URL ...]     # owner-confirmed overrides
      [--slug custom-slug]

What it does:
  1. Fetches the homepage plus up to 6 same-site pages whose links look like
     contact / location / hours / about / specials pages.
  2. Reads schema.org JSON-LD (LocalBusiness and subtypes) AND the visible text,
     and records BOTH: if they disagree (e.g. structured data omits a day the
     text lists), that is logged under "conflicts" because AI engines may read
     either one.
  3. If SERPAPI_KEY is set, also pulls Google's knowledge panel for
     "<name> <town>" as a listing source and cross-checks it.
  4. Writes truth/<slug>.json. Every fact carries the URL it came from.

Nothing is invented: a fact that cannot be found is left null with a note.
The website is treated as the owner's source of truth; listings are compared
against it and disagreements become fix-kit items, not facts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from common import (DAYS, TRUTH_DIR, addresses_in, clean_text, fetch, hours_to_text,
                    now_iso, parse_hours, phone_digits, phones_in, save_json, slugify)

BUSINESS_TYPES = {
    "localbusiness", "restaurant", "foodestablishment", "store", "bookstore", "bakery",
    "cafeorcoffeeshop", "dentist", "medicalbusiness", "medicalclinic", "homeandconstructionbusiness",
    "electrician", "plumber", "hvacbusiness", "roofingcontractor", "generalcontractor",
    "autorepair", "beautysalon", "hairsalon", "healthandbeautybusiness", "professionalservice",
    "legalservice", "attorney", "accountingservice", "realestateagent", "lodgingbusiness",
    "hotel", "barorpub", "fastfoodrestaurant", "icecreamshop", "sportsactivitylocation",
    "entertainmentbusiness", "clothingstore", "hardwarestore", "petstore", "florist",
}
PAGE_HINTS = ("contact", "location", "hours", "visit", "about", "find-us", "special",
              "deal", "promo", "offer", "coupon", "menu", "faq")
OFFER_RE = re.compile(
    r"[^.!?]*\b(specials|(?:daily|weekly|lunch|dinner|today'?s|our|pizza|family|senior|kids?) special|deal|deals|% off|percent off|coupon|promo|discount|discounts|"
    r"happy hour|bogo|buy one|free \w+ with|member(?:s|ship)? (?:price|discount|perk))\b[^.!?]*[.!?]?",
    re.I)
CLOSED_RE = re.compile(r"\b(permanently closed|closed for good|closed permanently|"
                       r"we have closed|we are closing|final day|last day of business)\b", re.I)
GENERIC_NAV = {"home", "contact", "contact us", "about", "about us", "my account", "cart",
               "checkout", "search", "log in", "login", "sign up / log in", "more", "skip to content",
               "menu", "menus", "order online", "shop", "gallery", "get hired!", "contact us!",
               "terms of service", "privacy policy", "top of page", "bottom of page"}
DAY_LD = {"monday": "mon", "tuesday": "tue", "wednesday": "wed", "thursday": "thu",
          "friday": "fri", "saturday": "sat", "sunday": "sun"}


# ----------------------------------------------------------------- JSON-LD
def ld_nodes(soup: BeautifulSoup) -> list[dict]:
    nodes: list[dict] = []

    def walk(n):
        if isinstance(n, dict):
            nodes.append(n)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            walk(json.loads(tag.string or tag.get_text() or ""))
        except (ValueError, TypeError):
            continue
    return nodes


def node_types(n: dict) -> set[str]:
    t = n.get("@type")
    return {x.lower() for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)}


def ld_business(nodes: list[dict]) -> dict | None:
    for n in nodes:
        if node_types(n) & BUSINESS_TYPES:
            return n
    return None


def ld_hours(biz: dict) -> dict:
    out: dict = {}
    for spec in biz.get("openingHoursSpecification") or []:
        if not isinstance(spec, dict):
            continue
        days = spec.get("dayOfWeek")
        for d in (days if isinstance(days, list) else [days]):
            if not isinstance(d, str):
                continue
            key = DAY_LD.get(d.rsplit("/", 1)[-1].lower())
            if key:
                o, c = spec.get("opens"), spec.get("closes")
                out[key] = "closed" if (o == c == "00:00") else {"open": (o or "")[:5] or None,
                                                                 "close": (c or "")[:5] or None}
    oh = biz.get("openingHours")
    if not out and oh:
        out = parse_hours(" ".join(oh) if isinstance(oh, list) else str(oh))
    return out


def ld_address(biz: dict) -> str | None:
    a = biz.get("address")
    if isinstance(a, str):
        return clean_text(a)
    if isinstance(a, dict):
        parts = [a.get("streetAddress"), a.get("addressLocality"),
                 " ".join(x for x in (a.get("addressRegion"), a.get("postalCode")) if x)]
        return ", ".join(clean_text(p) for p in parts if p)
    return None


# --------------------------------------------------------------- crawling
def get_page(url: str, log: list) -> tuple[BeautifulSoup | None, str, str]:
    try:
        status, final, html = fetch(url)
        log.append({"url": final, "requested": url, "status": status, "fetched_at": now_iso()})
        return BeautifulSoup(html, "html.parser"), final, html
    except Exception as e:  # noqa: BLE001 - any failure is logged, not fatal
        log.append({"url": url, "status": "error", "error": str(e)[:160], "fetched_at": now_iso()})
        return None, url, ""


def page_text(soup: BeautifulSoup) -> str:
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return clean_text(soup.get_text(" ", strip=True))


def candidate_pages(soup: BeautifulSoup, base: str) -> list[str]:
    host = urlparse(base).netloc.replace("www.", "")
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = urljoin(base, a["href"]).split("#")[0]
        if urlparse(href).netloc.replace("www.", "") != host or href in seen:
            continue
        label = (a["href"] + " " + a.get_text(" ")).lower()
        if any(h in label for h in PAGE_HINTS):
            seen.add(href)
            out.append(href)
    return out[:6]


def nav_services(soup: BeautifulSoup) -> list[str]:
    labels = []
    for a in soup.select("nav a, header a, .menu a, [role=navigation] a"):
        t = clean_text(re.sub(r"\(.*?\)", "", a.get_text(" "))).rstrip("!")
        if 2 < len(t) < 30 and t.lower() not in GENERIC_NAV and t not in labels:
            labels.append(t)
    return labels[:12]


# --------------------------------------------------------------- listings
def serpapi_listing(name: str, town: str, region: str, log: list) -> dict | None:
    key = os.environ.get("SERPAPI_KEY")
    if not key:
        return None
    q = urllib.parse.urlencode({"engine": "google", "q": f"{name} {town} {region}",
                                "location": f"{town}, {region}, United States", "api_key": key})
    try:
        _, _, body = fetch(f"https://serpapi.com/search.json?{q}", timeout=60)
        kg = json.loads(body).get("knowledge_graph") or {}
    except Exception as e:  # noqa: BLE001
        log.append({"url": "serpapi:google", "status": "error", "error": str(e)[:160]})
        return None
    log.append({"url": "serpapi:google knowledge_graph", "status": 200, "fetched_at": now_iso()})
    hours = {}
    for day, v in (kg.get("hours") or {}).items():
        k = DAY_LD.get(day.lower())
        if k:
            hours.update({k: parse_hours(f"{k} {v.get('opens', '')} - {v.get('closes', '')}").get(k)
                          or ("closed" if "closed" in json.dumps(v).lower() else None)})
    return {"kind": "google_listing", "url": "https://www.google.com/search?q=" +
            urllib.parse.quote(f"{name} {town}"), "title": kg.get("title"),
            "address": kg.get("address"), "phone": kg.get("phone"),
            "hours": {k: v for k, v in hours.items() if v}, "status": kg.get("type")}


def scan_listing(url: str, kind: str, log: list) -> dict:
    soup, final, _ = get_page(url, log)
    if not soup:
        return {"kind": kind, "url": url, "reachable": False}
    if re.search(r"/(login|accounts/login)\b", final):
        log[-1]["status"] = "login wall"
        return {"kind": kind, "url": url, "reachable": False,
                "note": "Behind a login wall; check this profile manually."}
    nodes = ld_nodes(soup)
    biz = ld_business(nodes) or {}
    text = page_text(soup)
    adds = addresses_in(text)
    return {"kind": kind, "url": final, "reachable": True,
            "title": clean_text(soup.title.string) if soup.title and soup.title.string else None,
            "address": ld_address(biz) or (adds[0]["raw"] if adds else None),
            "phone": biz.get("telephone") or (phones_in(text)[:1] or [None])[0],
            "hours": ld_hours(biz) or parse_hours(text),
            "bio_excerpt": text[:300]}


# ------------------------------------------------------------------- main
def fact(value, source, evidence=None, note=None):
    f = {"value": value, "source": source}
    if evidence:
        f["evidence"] = evidence[:300]
    if note:
        f["note"] = note
    return f


def collect(a) -> dict:
    log: list = []
    website = a.website if urlparse(a.website).scheme else "https://" + a.website
    soup, home, html = get_page(website, log)
    for _ in range(2):  # transient network errors are common; retry the homepage
        if soup:
            break
        soup, home, html = get_page(website, log)
    if not soup:
        sys.exit(f"Website unreachable: {website}. Pass --set overrides with sources instead.")

    pages = [(home, soup)]
    for url in candidate_pages(soup, home):
        s, final, _ = get_page(url, log)
        if s:
            pages.append((final, s))

    nodes, texts = [], []
    services = [x for x in nav_services(soup) if x.lower() != a.name.lower()]
    for url, s in pages:
        nodes += [(url, n) for n in ld_nodes(s)]
    observations = []
    for url, s in pages:
        imgs = len(s.find_all("img"))
        texts.append((url, page_text(s)))
        if "menu" in url.lower() and len(texts[-1][1]) < 1500 and imgs >= 3:
            observations.append({"type": "menu_not_text", "source": url, "detail": (
                "The menu page has almost no readable text (the menu appears to be images or an "
                "embedded widget), so AI engines cannot read your real prices and specials and "
                "fall back to third-party listings.")})

    biz_url, biz = next(((u, n) for u, n in nodes if node_types(n) & BUSINESS_TYPES), (None, None))
    facts: dict = {}
    conflicts: list = []

    # name
    facts["name"] = fact(a.name, home)
    if biz and biz.get("name") and biz["name"].strip().lower() != a.name.lower():
        facts["name"]["note"] = f'Structured data calls it "{biz["name"]}".'

    # address
    ld_addr = ld_address(biz) if biz else None
    text_addr = None
    for url, t in texts:
        for ad in addresses_in(t):
            i = t.find(ad["raw"]) + len(ad["raw"])
            tail = re.match(r"\.?,?\s*([A-Z][A-Za-z .'-]{2,30}),?\s+([A-Z]{2})\.?\s+(\d{5})", t[i:i + 60])
            full = ad["raw"] + (f", {tail.group(1).strip()}, {tail.group(2)} {tail.group(3)}" if tail else "")
            text_addr = (full, url, t)
            break
        if text_addr:
            break
    if ld_addr:
        facts["address"] = fact(ld_addr, biz_url, note="from schema.org structured data")
    elif text_addr:
        facts["address"] = fact(text_addr[0], text_addr[1], evidence=text_addr[0])
    else:
        facts["address"] = fact(None, None, note="No street address found on the website.")

    # phone
    tel = None
    for url, s in pages:
        link = s.select_one('a[href^="tel:"]')
        if link:
            tel = (phones_in(link["href"].replace("tel:", "")) or [None])[0], url
            break
    text_phone = next(((phones_in(t)[0], u) for u, t in texts if phones_in(t)), None)
    ld_phone = (phones_in(biz.get("telephone", "")) or [None])[0] if biz else None
    best = ld_phone and (ld_phone, biz_url) or tel or text_phone
    facts["phone"] = fact(best[0], best[1]) if best else fact(None, None, note="No phone found.")
    seen_phones = {p for p in (ld_phone, tel and tel[0], text_phone and text_phone[0]) if p}
    if len({phone_digits(p) for p in seen_phones}) > 1:
        conflicts.append({"field": "phone", "detail": f"Website shows several numbers: {sorted(seen_phones)}"})

    # hours: structured data vs visible text
    ld_h = ld_hours(biz) if biz else {}
    text_h, text_h_url, text_h_ev = {}, None, None
    for url, t in texts:
        m = re.search(r"(hours|open)", t, re.I)
        h = parse_hours(t)
        if len(h) >= 3:
            text_h, text_h_url = h, url
            i = m.start() if m else 0
            text_h_ev = t[i:i + 220]
            break
    if ld_h and text_h:
        diffs = [d for d in DAYS if ld_h.get(d) != text_h.get(d)]
        if diffs:
            conflicts.append({
                "field": "hours",
                "detail": ("Structured data (what search engines and AI read) says "
                           f"{hours_to_text(ld_h)}; the visible page says {hours_to_text(text_h)}. "
                           f"They disagree on: {', '.join(d.title() for d in diffs)}."),
                "source": text_h_url})
    if text_h:
        facts["hours"] = fact(text_h, text_h_url, evidence=text_h_ev,
                              note="visible page text (what the owner wrote for customers)")
    elif ld_h:
        facts["hours"] = fact(ld_h, biz_url, note="from schema.org structured data")
    else:
        facts["hours"] = fact(None, None, note="No opening hours found on the website.")

    # status
    closed_hit = next(((u, m) for u, t in texts for m in [CLOSED_RE.search(t)] if m), None)
    modified = None
    for _, n in nodes:
        modified = modified or n.get("dateModified")
    if closed_hit:
        facts["status"] = fact("closed", closed_hit[0], evidence=closed_hit[1].group(0),
                               note="The website itself mentions closing - confirm with owner.")
    else:
        facts["status"] = fact("open", home, note=(
            "Website is live and lists current hours" + (f"; page last updated {str(modified)[:10]}" if modified else "")
            + ". No closure notice on the site."))

    # offers
    offers = []
    blocks = [(url, clean_text(el.get_text(" "))) for url, sp in pages
              for el in sp.find_all(["p", "li", "td", "h2", "h3", "h4"])]
    for url, t in blocks:
        for m in OFFER_RE.finditer(t):
            s = clean_text(m.group(0))
            if 15 < len(s) < 260 and s not in [o["text"] for o in offers]:
                offers.append({"text": s, "source": url})
    facts["offers"] = fact(offers[:8], home, note=(
        "Offers published on the website. Any deal an AI states that is not here is unverified."
        if offers else "The website publishes no specials or deals."))

    facts["services"] = fact(services, home, note="from the site navigation")
    facts["website"] = fact(home, home)

    listings = []
    serp = serpapi_listing(a.name, a.town, a.region, log)
    if serp:
        listings.append(serp)
    for url in a.listing:
        listings.append(scan_listing(url, "listing", log))
    for url in a.social:
        listings.append(scan_listing(url, "social", log))
    sources = [{"kind": "fetch", **p} for p in log]

    # cross-check listings against the website
    for li in listings:
        if not li.get("reachable", True):
            continue
        tp = facts["phone"]["value"]
        if li.get("phone") and tp and phone_digits(li["phone"]) != phone_digits(tp):
            conflicts.append({"field": "phone", "source": li["url"],
                              "detail": f'{li["kind"]} lists {li["phone"]}; website says {tp}.'})
        ta = facts["address"]["value"] or ""
        la = addresses_in(li.get("address") or "")
        tad = addresses_in(ta)
        if la and tad and (la[0]["number"], la[0]["street_key"]) != (tad[0]["number"], tad[0]["street_key"]):
            conflicts.append({"field": "address", "source": li["url"],
                              "detail": f'{li["kind"]} lists "{li["address"]}"; website says "{ta}".'})
        lh, th = li.get("hours") or {}, facts["hours"]["value"] or {}
        if len(lh) >= 3 and th:
            diffs = [d for d in DAYS if d in lh and lh.get(d) != th.get(d)]
            if diffs:
                conflicts.append({"field": "hours", "source": li["url"],
                                  "detail": f'{li["kind"]} hours differ on {", ".join(d.title() for d in diffs)}: '
                                            f'{hours_to_text(lh)}'})

    twins = []
    for t in a.twin:
        p = (t.split("|") + [""] * 5)[:5]
        twins.append({"name": p[0], "address": p[1] or None, "phone": p[2] or None,
                      "url": p[3] or None, "note": p[4] or None})

    for s in a.set:
        k, _, v = s.partition("=")
        try:
            v = json.loads(v)
        except ValueError:
            pass
        facts[k] = fact(v, a.set_source or "owner-confirmed", note="manual override")

    return {
        "slug": a.slug or slugify(f"{a.name} {a.town}"),
        "name": a.name, "town": a.town, "region": a.region,
        "category": (sorted(node_types(biz) - {"localbusiness"}) or ["LocalBusiness"])[0] if biz else a.category,
        "collected_at": now_iso(),
        "facts": facts,
        "structured_data": {"present": bool(biz), "types": sorted(node_types(biz)) if biz else [],
                            "hours": ld_h or None, "source": biz_url},
        "conflicts": conflicts,
        "observations": observations,
        "same_name_businesses": twins,
        "listings": listings,
        "press": [{"url": u} for u in a.press],
        "sources": sources,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", required=True)
    p.add_argument("--town", required=True)
    p.add_argument("--region", default="")
    p.add_argument("--website", required=True)
    p.add_argument("--category", default="LocalBusiness")
    p.add_argument("--listing", action="append", default=[])
    p.add_argument("--social", action="append", default=[])
    p.add_argument("--press", action="append", default=[])
    p.add_argument("--twin", action="append", default=[])
    p.add_argument("--set", action="append", default=[])
    p.add_argument("--set-source")
    p.add_argument("--slug")
    a = p.parse_args()
    truth = collect(a)
    path = save_json(TRUTH_DIR / f"{truth['slug']}.json", truth)
    f = truth["facts"]
    print(f"Saved {path}")
    print(f"  address: {f['address']['value']}\n  phone:   {f['phone']['value']}")
    print(f"  hours:   {hours_to_text(f['hours']['value'] or {})}")
    print(f"  status:  {f['status']['value']}   offers: {len(f['offers']['value'])}")
    for c in truth["conflicts"]:
        print(f"  CONFLICT [{c['field']}] {c['detail']}")


if __name__ == "__main__":
    main()
