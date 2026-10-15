#!/usr/bin/env python3
"""Score a dental practice website on the signals AI assistants use to pick
which local businesses to recommend.

Usage:
    python audit.py https://example-dental.com --city "Orlando" [--json]

This checks only what is on the practice's own site. Review counts and
directory listings are gathered by the routine from web search and passed into
the report separately. Nothing here invents data: a check that cannot be run
(site down, blocked) is reported as "unknown", not as a failure.
"""

import argparse
import json
import re
import sys
import urllib.request
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; VisibilityAudit/1.0)"
DENTAL_TYPES = {"dentist", "localbusiness", "medicalbusiness", "medicalclinic",
                "medicalorganization", "healthandbeautybusiness"}
SERVICE_WORDS = ["implant", "invisalign", "emergency", "crown", "whitening",
                 "veneer", "root canal", "cleaning", "pediatric", "orthodont"]
BOOKING_WORDS = ["book online", "request appointment", "schedule online",
                 "book now", "schedule appointment", "request an appointment"]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
JUNK_EMAIL = ("example.", "sentry", "wixpress", "domain.com", ".png", ".jpg")

# (key, points, plain-English fix shown to the practice)
CHECKS = [
    ("https", 5, "Serve the site over HTTPS."),
    ("schema_business", 20, "Add Dentist structured data (JSON-LD) with name, address, phone, hours."),
    ("schema_faq", 10, "Add an FAQ section marked up as FAQPage."),
    ("faq_content", 10, "Answer the questions patients ask AI (cost, insurance, emergencies)."),
    ("city_in_title", 10, "Put the city and 'dentist' in the homepage title."),
    ("phone_link", 5, "Make the phone number a tap-to-call link."),
    ("address_on_page", 10, "Show the full street address as text, not only in an image or map."),
    ("service_pages", 15, "Give each main service (implants, Invisalign, emergency) its own page."),
    ("online_booking", 5, "Offer online booking or an appointment request form."),
    ("viewport", 5, "Make the site mobile-friendly (viewport tag)."),
    ("llms_txt", 5, "Publish an /llms.txt summary for AI crawlers."),
]


def fetch(url: str, timeout: int = 20) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read(3_000_000).decode("utf-8", "replace")
        return r.status, r.geturl(), body


def schema_types(soup: BeautifulSoup) -> set[str]:
    types: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            for v in (t if isinstance(t, list) else [t]):
                if isinstance(v, str):
                    types.add(v.lower())
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            walk(json.loads(tag.string or ""))
        except (ValueError, TypeError):
            continue
    return types


def find_emails(soup: BeautifulSoup, html: str) -> list[str]:
    found = {a["href"][7:].split("?")[0] for a in soup.select('a[href^="mailto:"]')}
    found |= set(EMAIL_RE.findall(html))
    return sorted(e.lower() for e in found if not any(j in e.lower() for j in JUNK_EMAIL))


def audit(url: str, city: str) -> dict:
    if not urlparse(url).scheme:
        url = "https://" + url
    try:
        status, final_url, html = fetch(url)
    except Exception as e:  # noqa: BLE001 - any fetch failure means "unknown"
        return {"url": url, "reachable": False, "error": str(e)[:200]}

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    links = " ".join((a.get("href", "") + " " + a.get_text(" ")).lower() for a in soup.find_all("a"))
    types = schema_types(soup)
    title = (soup.title.string or "").lower() if soup.title else ""

    try:
        llms_status, _, llms_body = fetch(urljoin(final_url, "/llms.txt"), timeout=10)
        has_llms = llms_status == 200 and "<html" not in llms_body[:500].lower()
    except Exception:  # noqa: BLE001
        has_llms = False

    results = {
        "https": final_url.startswith("https://"),
        "schema_business": bool(types & DENTAL_TYPES),
        "schema_faq": "faqpage" in types,
        "faq_content": "faq" in links or "frequently asked" in text,
        "city_in_title": bool(city) and city.lower() in title,
        "phone_link": bool(soup.select('a[href^="tel:"]')),
        "address_on_page": bool(re.search(r"\d{2,6}\s+\w+.*\b(st|street|ave|avenue|rd|road|blvd|dr|drive|hwy|pkwy|ln|way|suite)\b", text)),
        "service_pages": sum(w in links for w in SERVICE_WORDS) >= 3,
        "online_booking": any(w in text or w in links for w in BOOKING_WORDS),
        "viewport": bool(soup.find("meta", attrs={"name": "viewport"})),
        "llms_txt": has_llms,
    }
    score = sum(pts for key, pts, _ in CHECKS if results[key])
    fixes = [fix for key, _, fix in CHECKS if not results[key]]
    return {
        "url": final_url.replace(":443/", "/"),
        "reachable": True,
        "title": title[:150],
        "score": score,
        "checks": results,
        "fixes": fixes,
        "emails": find_emails(soup, html),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("url")
    p.add_argument("--city", default="")
    p.add_argument("--json", action="store_true", help="print raw JSON")
    a = p.parse_args()
    r = audit(a.url, a.city)
    if a.json or not r.get("reachable"):
        print(json.dumps(r, indent=2))
        sys.exit(0 if r.get("reachable") else 1)
    print(f"{r['url']}\nScore: {r['score']}/100")
    for key, pts, _ in CHECKS:
        print(f"  [{'x' if r['checks'][key] else ' '}] {key} ({pts})")
    print("Emails found:", ", ".join(r["emails"]) or "none")


if __name__ == "__main__":
    main()
