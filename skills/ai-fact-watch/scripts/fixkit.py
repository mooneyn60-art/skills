#!/usr/bin/env python3
"""Generate the Fix Kit for a business from its truth file and findings.

Usage:
  python fixkit.py --slug X [--date YYYY-MM-DD] [--out DIR]

Writes (default DIR = samples/<slug>/fix-kit/):
  localbusiness.jsonld   schema.org block to paste into the site <head>
  official-facts.html    an "Official facts" page (text + FAQPage schema)
  llms.txt               plain summary for AI crawlers, served at /llms.txt
  gbp-edits.md           Google Business Profile edits, in priority order
  ai-feedback.md         how to report each wrong AI answer, with pre-written text
  directories.md         listings to correct, with the exact corrected text
  README.md              the order to do it in

report.py imports build_kit() so the report and the files never disagree.
We promise detection, corrected sources and documentation. We never promise
that Google or any AI vendor will change its answer.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from urllib.parse import urlparse

from common import (DAYS, DAY_NAMES, FINDINGS_DIR, ROOT, TRUTH_DIR, fmt_time, load_json,
                    phone_digits)

SCHEMA_TYPE = {"restaurant": "Restaurant", "bookstore": "BookStore", "bakery": "Bakery",
               "store": "Store", "dentist": "Dentist", "electrician": "Electrician",
               "plumber": "Plumber", "barorpub": "BarOrPub", "hairsalon": "HairSalon"}
FEEDBACK_HOWTO = {
    "Google AI Overview": [
        "Search the exact question on Google (on the phone where customers see it).",
        "Under the AI Overview, tap the thumbs-down icon (or the three-dot menu, then Feedback).",
        "Pick the closest reason (for example 'Inaccurate'), paste the text below, and attach a "
        "screenshot of your website showing the correct fact.",
        "Repeat from a second Google account or device if the error persists; log each submission "
        "date in the evidence log.",
    ],
    "Gemini": ["In the Gemini app or gemini.google.com, ask the question, tap thumbs-down on the "
               "answer, and paste the text below."],
    "ChatGPT": ["In ChatGPT, ask the question, tap thumbs-down on the answer, and paste the text below."],
    "False legal claims": ["If an AI answer states a false lawsuit, crime or scam, keep the dated evidence log and "
              "use Google's legal removal request (https://support.google.com/legal/answer/3110420). "
              "Talk to a lawyer before making any public accusation."],
}
CORE_DIRECTORIES = [
    ("Google Business Profile", "https://business.google.com"),
    ("Apple Business Connect (Apple Maps, Siri)", "https://businessconnect.apple.com"),
    ("Bing Places (feeds Bing and Copilot)", "https://www.bingplaces.com"),
    ("Yelp for Business", "https://biz.yelp.com"),
    ("Facebook Page (About section)", "https://www.facebook.com"),
]


def split_address(addr: str) -> dict:
    m = re.match(r"\s*(.+?),\s*([^,]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)?\s*$", addr or "")
    if not m:
        return {"@type": "PostalAddress", "streetAddress": addr}
    return {"@type": "PostalAddress", "streetAddress": m.group(1), "addressLocality": m.group(2),
            "addressRegion": m.group(3), "postalCode": (m.group(4) or "")[:5] or None,
            "addressCountry": "US"}


def hours_lines(h: dict) -> list[tuple[str, str]]:
    out = []
    for d in DAYS:
        v = (h or {}).get(d)
        if v == "closed":
            out.append((DAY_NAMES[d], "Closed"))
        elif isinstance(v, dict):
            out.append((DAY_NAMES[d], f"{fmt_time(v.get('open'))} - {fmt_time(v.get('close'))}"))
        else:
            out.append((DAY_NAMES[d], "(confirm)"))
    return out


def facts_of(truth: dict) -> dict:
    f = truth["facts"]
    offers = f["offers"]["value"] or []
    return {"name": truth["name"], "address": f["address"]["value"], "phone": f["phone"]["value"],
            "website": f["website"]["value"], "hours": f["hours"]["value"] or {},
            "status": f["status"]["value"], "offers": [o["text"] for o in offers],
            "town": truth["town"], "region": truth.get("region", ""),
            "twins": truth.get("same_name_businesses", []),
            "social": [li["url"] for li in truth.get("listings", []) if li.get("kind") == "social"]}


def jsonld(truth: dict) -> dict:
    F = facts_of(truth)
    t = SCHEMA_TYPE.get((truth.get("category") or "").lower(), truth.get("category") or "LocalBusiness")
    if t.lower() == "localbusiness" and "book" in F["name"].lower():
        t = "BookStore"
    specs = []
    for d in DAYS:
        v = F["hours"].get(d)
        if v == "closed":
            specs.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_NAMES[d],
                          "opens": "00:00", "closes": "00:00"})
        elif isinstance(v, dict) and v.get("open") and v.get("close"):
            specs.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_NAMES[d],
                          "opens": v["open"], "closes": v["close"]})
    block = {"@context": "https://schema.org", "@type": t, "name": F["name"], "url": F["website"],
             "telephone": "+1-" + "-".join(re.findall(r"\d+", F["phone"] or ""))[-12:] if F["phone"] else None, "address": {k: v for k, v in split_address(F["address"]).items() if v},
             "openingHoursSpecification": specs}
    if F["social"]:
        block["sameAs"] = [s for s in F["social"]]
    if F["twins"]:
        block["description"] = disambiguation(truth)
    return block


def disambiguation(truth: dict) -> str | None:
    F = facts_of(truth)
    if not F["twins"]:
        return None
    others = "; ".join(f'{t["name"]}' + (f' ({t["address"]})' if t.get("address") else "") for t in F["twins"][:4])
    return (f'{F["name"]} at {F["address"]} (phone {F["phone"]}) is a separate business from '
            f'similarly named businesses and is not affiliated with them: {others}. '
            f'For our hours, prices and specials, use {F["website"]} only.')


def faq(truth: dict) -> list[tuple[str, str]]:
    F = facts_of(truth)
    open_days = [f"{d}: {t}" for d, t in hours_lines(F["hours"])]
    offers = ("Our current offers are listed on this page: " + " ".join(F["offers"])) if F["offers"] else \
        (f"We only run the specials posted on {F['website']}. If you see a deal anywhere else, "
         "including in an AI answer or search summary, it is not from us. Please call to confirm.")
    qa = [
        (f"Is {F['name']} open?", f"Yes. {F['name']} is open for business at {F['address']}. "
                                  "Our regular hours are: " + "; ".join(open_days) + "."),
        (f"What are {F['name']}'s hours?", "; ".join(open_days) + "."),
        (f"Where is {F['name']}?", f"{F['address']}."),
        (f"What is {F['name']}'s phone number?", f"{F['phone']}."),
        (f"Does {F['name']} have any deals or specials?", offers),
    ]
    if F["twins"]:
        qa.append((f"Is {F['name']} the same as other businesses with a similar name?", disambiguation(truth)))
    return qa


def official_facts_html(truth: dict, updated: str) -> str:
    F = facts_of(truth)
    qa = faq(truth)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    rows = "\n".join(f"      <tr><th scope=\"row\">{d}</th><td>{html.escape(t)}</td></tr>"
                     for d, t in hours_lines(F["hours"]))
    qas = "\n".join(f"    <h3>{html.escape(q)}</h3>\n    <p>{html.escape(a)}</p>" for q, a in qa)
    e = html.escape
    return f"""<!-- Official facts page. Publish at {F['website'].rstrip('/')}/official-facts and link it from your footer. -->
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Official facts: {e(F['name'])}, {e(F['town'])}</title>
  <meta name="description" content="Official, current hours, address, phone and specials for {e(F['name'])} in {e(F['town'])}, {e(F['region'])}. Updated {updated}.">
  <script type="application/ld+json">
{json.dumps(jsonld(truth), indent=2, ensure_ascii=False)}
  </script>
  <script type="application/ld+json">
{json.dumps(faq_ld, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
  <main>
    <h1>Official facts: {e(F['name'])}</h1>
    <p><strong>Last updated {updated}.</strong> This page is the official source for our hours, location,
    phone number and specials. If a search summary, AI assistant or directory says something different,
    this page is correct.</p>
    <h2>Status</h2>
    <p>We are open.</p>
    <h2>Location</h2>
    <p>{e(F['address'] or '')}</p>
    <h2>Phone</h2>
    <p><a href="tel:+1{phone_digits(F['phone'])}">{e(F['phone'] or '')}</a></p>
    <h2>Hours</h2>
    <table>
{rows}
    </table>
    <h2>Questions people ask</h2>
{qas}
  </main>
</body>
</html>
"""


def llms_txt(truth: dict, updated: str) -> str:
    F = facts_of(truth)
    lines = [f"# {F['name']}", "",
             f"> Official facts for {F['name']}, {F['town']}, {F['region']}. Updated {updated}. "
             "If any other source disagrees, these facts are correct.", "",
             "## Facts", f"- Status: open", f"- Address: {F['address']}", f"- Phone: {F['phone']}",
             f"- Website: {F['website']}", "- Hours:"]
    lines += [f"  - {d}: {t}" for d, t in hours_lines(F["hours"])]
    lines += ["- Specials and deals: " + ("; ".join(F["offers"]) if F["offers"] else
              f"only those posted on {F['website']}. Any other deal is not ours.")]
    if F["twins"]:
        lines += ["", "## Not affiliated with", *[f"- {t['name']}" + (f", {t['address']}" if t.get('address') else "")
                                                   for t in F["twins"]]]
    lines += ["", "## Pages", f"- [Official facts]({F['website'].rstrip('/')}/official-facts): hours, location, phone, specials"]
    return "\n".join(lines) + "\n"


def gbp_edits(truth: dict, findings: dict) -> list[str]:
    F = facts_of(truth)
    types = {f["type"] for f in findings.get("findings", [])}
    hrs = "; ".join(f"{d} {t}" for d, t in hours_lines(F["hours"]))
    out = [f"Confirm the business is marked Open (not 'Permanently closed' or 'Temporarily closed').",
           f"Regular hours, every day set explicitly: {hrs}.",
           f"Address exactly: {F['address']}. Open the map and drag the pin onto your door if it is off.",
           f"Primary phone exactly: {F['phone']}.",
           f"Website field: {F['website']} (or the official-facts page once published)."]
    if types & {"says_closed", "cannot_confirm_open"}:
        out.insert(0, f"Publish an Update post today: 'We are open! {hrs}. Find us at {F['address']}.' "
                      "Repeat weekly while the error persists: fresh posts are a strong 'still operating' signal.")
    if types & {"invented_deal", "unverified_deal"}:
        out.append("Post real specials only as Offer posts with start and end dates, and add an Update: "
                   "'Our only specials are the ones posted here and on our website.'")
    if F["twins"]:
        out.append("Business description: add the disambiguation statement from this kit.")
    out.append("Add 10+ current photos (storefront with signage, interior, menu or price board). "
               "Recent photos are another signal that you are operating.")
    return out


def feedback_items(truth: dict, findings: dict) -> list[dict]:
    F = facts_of(truth)
    items = []
    skip = {"official_site_not_used", "own_source_conflict", "no_structured_data", "menu_not_text"}
    for f in findings.get("findings", []):
        if not f["evidence"] or f["type"] in skip:
            continue
        ev = f["evidence"][0]
        eng = (ev.get("engine") or "").lower()
        channel = "gemini" if "gemini" in eng else "chatgpt" if ("openai" in eng or "chatgpt" in eng) \
            else "google"
        text = (f"This answer about {F['name']} ({F['town']}, {F['region']}) is wrong. "
                f"{f['title']}. Correct information: {f['true_value'][:300]}. "
                f"Official source: {f['true_source']}. I am the owner/representative of this business.")
        if f["type"] == "same_name_confusion" and F["twins"]:
            text += " " + (disambiguation(truth) or "")
        items.append({"finding": f["title"], "severity": f["severity"], "engine": ev.get("engine"),
                      "query": ev.get("query"), "channel": channel, "text": text,
                      "legal": f["type"] == "false_legal_claim"})
    return items


def directory_items(truth: dict, findings: dict) -> list[dict]:
    F = facts_of(truth)
    site = urlparse(F["website"]).netloc.replace("www.", "")
    seen, out = set(), []
    news = ("news", "magazine", "times", "spectrum", "wlox", "29news", "ground.news", "ctvnews")
    for f in findings.get("findings", []):
        for ev in f["evidence"]:
            for url in ev.get("citations", []) or []:
                h = urlparse(url).netloc.replace("www.", "")
                if not h or site in h or h in seen or any(n in h for n in news):
                    continue
                seen.add(h)
                out.append({"site": h, "url": url, "why": f"Cited in: {f['title']}"})
    for name, url in CORE_DIRECTORIES:
        out.append({"site": name, "url": url, "why": "Core source AI engines read"})
    return out


def canonical_block(truth: dict) -> str:
    F = facts_of(truth)
    hrs = "; ".join(f"{d[:3]} {t}" for d, t in hours_lines(F["hours"]))
    return f"{F['name']} | {F['address']} | {F['phone']} | {F['website']} | Hours: {hrs}"


def compact_json(obj) -> str:
    """Indented JSON with each small object (hours rows, address) on one line."""
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    return re.sub(r"\{\n\s+(\"@type\": \"(?:OpeningHoursSpecification|PostalAddress)\"[^{}]*?)\n\s*\}",
                  lambda m: "{" + re.sub(r"\s*\n\s*", " ", m.group(1)) + "}", text)


def build_kit(truth: dict, findings: dict) -> dict:
    updated = findings.get("date") or truth["collected_at"][:10]
    return {"jsonld": compact_json(jsonld(truth)),
            "official_facts_html": official_facts_html(truth, updated),
            "faq": faq(truth), "llms_txt": llms_txt(truth, updated),
            "gbp": gbp_edits(truth, findings), "feedback": feedback_items(truth, findings),
            "feedback_howto": FEEDBACK_HOWTO, "directories": directory_items(truth, findings),
            "canonical": canonical_block(truth), "disambiguation": disambiguation(truth)}


def write_kit(kit: dict, out) -> list:
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "localbusiness.jsonld": kit["jsonld"] + "\n",
        "official-facts.html": kit["official_facts_html"],
        "llms.txt": kit["llms_txt"],
        "gbp-edits.md": "# Google Business Profile edits\n\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(kit["gbp"], 1)) + "\n",
        "ai-feedback.md": "# Report each wrong AI answer\n\nNo vendor promises to change an answer. Submit, "
                          "log the date, re-check weekly.\n\n" +
                          "\n".join(f"## {k}\n" + "\n".join(f"- {s}" for s in v) + "\n"
                                    for k, v in kit["feedback_howto"].items()) + "\n" +
                          "\n".join(f"### {x['finding']} ({x['severity']})\nEngine: {x['engine']}\n"
                                    f"Query: {x['query']}\n\n> {x['text']}\n" for x in kit["feedback"]),
        "directories.md": "# Listings to correct\n\nPaste this exact block everywhere:\n\n    "
                          + kit["canonical"] + "\n\n" +
                          "\n".join(f"- **{d['site']}** <{d['url']}>: {d['why']}" for d in kit["directories"]) + "\n",
        "README.md": "# Fix Kit\n\nDo these in order:\n\n1. Paste `localbusiness.jsonld` into your website's "
                     "<head> (inside a <script type=\"application/ld+json\"> tag).\n2. Publish "
                     "`official-facts.html` at /official-facts and link it in your footer.\n3. Upload "
                     "`llms.txt` to your site root.\n4. Make the edits in `gbp-edits.md`.\n5. Correct the "
                     "listings in `directories.md`.\n6. Submit the feedback in `ai-feedback.md`.\n\n"
                     "We monitor and document; no one can guarantee an AI vendor will change its answer.\n",
    }
    if kit["disambiguation"]:
        files["disambiguation.txt"] = kit["disambiguation"] + "\n"
    for name, body in files.items():
        (out / name).write_text(body)
    return sorted(files)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--date")
    ap.add_argument("--out")
    a = ap.parse_args()
    truth = load_json(TRUTH_DIR / f"{a.slug}.json")
    files = sorted((FINDINGS_DIR / a.slug).glob("????-??-??.json"))
    findings = load_json(FINDINGS_DIR / a.slug / f"{a.date}.json") if a.date else load_json(files[-1]) if files else {}
    from pathlib import Path
    out = Path(a.out) if a.out else ROOT / "samples" / a.slug / "fix-kit"
    print("Wrote", write_kit(build_kit(truth, findings), out), "->", out)


if __name__ == "__main__":
    main()
