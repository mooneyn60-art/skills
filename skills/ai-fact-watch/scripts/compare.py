#!/usr/bin/env python3
"""Compare what AI engines said against the business's ground truth.

Usage:
  python compare.py --slug viridian-bookshop-willoughby [--date 2026-10-15]

Reads truth/<slug>.json and answers/<slug>/<date>.json (latest by default),
writes findings/<slug>/<date>.json and prints a summary.

Each finding has: field, type, severity (critical/high/medium/low), the EXACT
AI quote (a verbatim sentence from the stored answer, never paraphrased), the
true value with its source URL, and every engine/date it was seen on. Findings
seen only in press reports are kept as documented history and do not count
toward today's score. If a previous findings file exists, the output also
lists what is new and what is resolved since then (used for Watch alerts).

Detection is deterministic pattern matching. It errs toward flagging: a human
or the agent should read each quote before it goes in an email to the owner.
"""

from __future__ import annotations

import argparse
import re
import sys
from urllib.parse import urlparse

from common import (ANSWERS_DIR, DAYS, DAY_NAMES, FINDINGS_DIR, TRUTH_DIR, addresses_in,
                    fmt_time, hours_to_text, load_json, now_iso, parse_hours, phone_digits,
                    phones_in, save_json, sentence_around, sentences)

SEV_WEIGHT = {"critical": 30, "high": 12, "medium": 5, "low": 1}
SEV_ORDER = ["critical", "high", "medium", "low"]
FIELDS = [("status", "Open / closed"), ("hours", "Hours"), ("address", "Address"),
          ("phone", "Phone"), ("offers", "Deals & prices"), ("legal", "Legal / reputation"),
          ("identity", "Right business"), ("visibility", "Official sources")]

NEG = re.compile(r"\b(no|not|isn't|wasn't|didn't|doesn't|don't|couldn't|can't|cannot|without|never found|"
                 r"unrelated|none of (?:these|the results)|different (?:shops?|business(?:es)?))\b", re.I)
HEDGE = re.compile(r"\b(doesn't match|does not match|different|unrelated|not the|separate|"
                   r"I'd rely on|left (?:them|it) out)\b", re.I)
CLOSED_RE = re.compile(r"\b(permanently closed|closed for good|closed permanently|has (?:permanently )?closed|"
                       r"out of business|no longer (?:open|in business|operating)|never (?:even )?existed|"
                       r"shut down|(?:is|are) closing|will close|closing (?:on |for good|its doors|"
                       r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d))", re.I)
UNSURE_STATUS = re.compile(r"\b(couldn't confirm|can't confirm|could not confirm|unable to confirm|"
                           r"can't tell|couldn't find current hours)\b", re.I)
NOT_FOUND = re.compile(r"\b(didn't turn up|did not turn up|couldn't find|could not find|no results|"
                       r"none of the results list|found no|I can't give you|not (?:listed|found))\b", re.I)
DEAL_RE = re.compile(
    r"\b(?:deals?|promotions?|promo|discount(?:ed)?|\d+% off|coupon|bogo|buy one,? get|"
    r"second \w+ for \$\d+|same (?:price|cost) as|(?:cost|price)s? the same as|"
    r"(?:Family|Lunch|Daily|Weekly|Pizza|Kids|Senior|Combo|Party)(?: \w+)? Special\b(?! \())", re.I)
LEGAL_RE = re.compile(r"\b(sued|lawsuits?|attorney general|scam|fraud\w*|under investigation|"
                      r"class action|complaints? (?:was |were )?filed|indicted|fined|violations?)\b", re.I)
BAD_ADDR_RE = re.compile(r"\b(incorrect|wrong) address|address (?:a few doors|down the street)", re.I)
NO_SITE_RE = re.compile(r"(did not|didn't|couldn't) find (?:a |an |the )?(?:dedicated |official )?"
                        r"(?:website|site)", re.I)


def host(url: str) -> str:
    return urlparse(url or "").netloc.replace("www.", "").lower()


class Collector:
    def __init__(self):
        self.groups: dict = {}
        self.confirmations: list = []

    def add(self, key, *, field, type_, title, severity, truth_value, truth_source,
            explanation, answer=None, quote=None):
        g = self.groups.setdefault(key, {
            "key": key, "field": field, "type": type_, "title": title, "severity": severity,
            "true_value": truth_value, "true_source": truth_source, "explanation": explanation,
            "evidence": []})
        if SEV_ORDER.index(severity) < SEV_ORDER.index(g["severity"]):
            g["severity"] = severity
        if answer is not None:
            ev = {"provider": answer["provider"], "engine": answer.get("engine"),
                  "mode": answer.get("mode"), "query": answer.get("query"),
                  "observed_at": answer.get("observed_at"), "ai_quote": quote,
                  "evidence_url": None if (quote or "").startswith("(") else
                  answer.get("evidence_url") or (answer.get("citations") or [None])[0],
                  "citations": answer.get("citations", [])}
            if ev not in g["evidence"]:
                g["evidence"].append(ev)
        return g

    def ok(self, field, answer, quote):
        self.confirmations.append({"field": field, "provider": answer["provider"],
                                   "engine": answer.get("engine"), "observed_at": answer.get("observed_at"),
                                   "ai_quote": quote})


def sent_with(text: str, m: re.Match) -> str:
    return sentence_around(text, m.start(), m.end())


def negated(sentence: str, kw_pos: int) -> bool:
    return bool(NEG.search(sentence[:kw_pos][-80:])) or bool(HEDGE.search(sentence))


# ------------------------------------------------------------- detectors
def check_status(a, text, truth, c):
    st = truth["facts"]["status"]
    hit = False
    for m in CLOSED_RE.finditer(text):
        s = sent_with(text, m)
        pos = s.lower().find(m.group(0).lower())
        if pos >= 0 and negated(s, pos) and "never" not in m.group(0).lower():
            continue
        hit = True
        if st["value"] == "open":
            c.add("status:says-closed", field="status", type_="says_closed",
                  title="AI says the business is closed", severity="critical",
                  truth_value="Open: " + (st.get("note") or ""), truth_source=st["source"],
                  explanation="Customers who read this will not come. This is the most damaging error type.",
                  answer=a, quote=s)
    if not hit and a["field"] == "status":
        m = UNSURE_STATUS.search(text)
        if m:
            c.add("status:unconfirmed", field="status", type_="cannot_confirm_open",
                  title="AI cannot confirm the business is open", severity="medium",
                  truth_value="Open", truth_source=st["source"],
                  explanation="The engine found no current, trustworthy signal that you are open. "
                              "That gap is what lets a wrong 'closed' answer take hold.",
                  answer=a, quote=sent_with(text, m))


def check_hours(a, text, truth, c):
    th = truth["facts"]["hours"]["value"] or {}
    src = truth["facts"]["hours"]["source"]
    claimed = parse_hours(text)
    wrong = []
    for d, v in claimed.items():
        t = th.get(d)
        if t is None:
            continue
        if v == "closed" and t != "closed":
            wrong.append(f"{DAY_NAMES[d]}: AI says closed, actually {fmt_time(t['open'])}-{fmt_time(t['close'])}")
        elif isinstance(v, dict) and t == "closed":
            wrong.append(f"{DAY_NAMES[d]}: AI gives hours, actually closed")
        elif isinstance(v, dict) and isinstance(t, dict):
            for k in ("open", "close"):
                if v.get(k) and t.get(k) and v[k] != t[k]:
                    wrong.append(f"{DAY_NAMES[d]} {k}s: AI says {fmt_time(v[k])}, actually {fmt_time(t[k])}")
    if claimed and th:
        m = re.search(r"\d{1,2}(?::\d{2})?\s*(?:a\.?m|p\.?m|AM|PM|am|pm)", text)
        quote = sentence_around(text, m.start(), m.end(), 420) if m else text[:300]
        if wrong:
            c.add("hours:wrong", field="hours", type_="wrong_hours", title="AI gives wrong opening hours",
                  severity="high", truth_value=hours_to_text(th), truth_source=src,
                  explanation="; ".join(wrong) + ". People arrive to a locked door or skip a visit "
                              "when you are actually open.", answer=a, quote=quote)
        else:
            c.ok("hours", a, quote)
    elif a["field"] == "hours" and th:
        m = NOT_FOUND.search(text)
        if m:
            c.add("hours:missing", field="hours", type_="hours_not_found",
                  title="AI cannot find your hours", severity="medium",
                  truth_value=hours_to_text(th), truth_source=src,
                  explanation="Your hours are on your website but the engine did not find them, so it "
                              "tells customers to call or guess.", answer=a, quote=sent_with(text, m))


def check_phone(a, text, truth, c):
    tp = truth["facts"]["phone"]["value"]
    src = truth["facts"]["phone"]["source"]
    twins = {phone_digits(t["phone"]): t for t in truth.get("same_name_businesses", []) if t.get("phone")}
    found = phones_in(text)
    for p in found:
        i = text.find(p[-4:])
        quote = sentence_around(text, max(i, 0), max(i, 0) + 4)
        if tp and phone_digits(p) == phone_digits(tp):
            c.ok("phone", a, quote)
        elif phone_digits(p) in twins:
            t = twins[phone_digits(p)]
            c.add(f"identity:phone:{phone_digits(p)}", field="identity", type_="same_name_confusion",
                  title=f"AI gives the phone number of a different business ({t['name']})",
                  severity="high", truth_value=tp, truth_source=src,
                  explanation=f"{p} belongs to {t['name']}. Callers reach the wrong business.",
                  answer=a, quote=quote)
        elif tp:
            c.add(f"phone:wrong:{phone_digits(p)}", field="phone", type_="wrong_phone",
                  title="AI gives a wrong phone number", severity="high", truth_value=tp,
                  truth_source=src, explanation=f"{p} is not your number. Callers who can't reach you "
                                                "call a competitor.", answer=a, quote=quote)
    if not found and a["field"] == "phone" and tp:
        m = NOT_FOUND.search(text)
        if m:
            c.add("phone:missing", field="phone", type_="phone_not_found",
                  title="AI cannot find your phone number", severity="medium", truth_value=tp,
                  truth_source=src, explanation="Your number is on your website but the engine did "
                                                "not surface it.", answer=a, quote=sent_with(text, m))


def check_address(a, text, truth, c):
    ta = truth["facts"]["address"]["value"] or ""
    src = truth["facts"]["address"]["source"]
    tad = addresses_in(ta)
    twins = []
    for t in truth.get("same_name_businesses", []):
        for ad in addresses_in(t.get("address") or ""):
            twins.append((ad, t))
    found = addresses_in(text)
    for ad in found:
        i = text.find(ad["raw"])
        quote = sentence_around(text, i, i + len(ad["raw"]))
        twin = next((t for tw, t in twins if (tw["number"], tw["street_key"]) == (ad["number"], ad["street_key"])), None)
        if tad and (ad["number"], ad["street_key"]) == (tad[0]["number"], tad[0]["street_key"]):
            c.ok("address", a, quote)
        elif twin:
            hedged = bool(HEDGE.search(text[max(0, i - 200):i + 300]))
            c.add(f"identity:address:{ad['number']}", field="identity", type_="same_name_confusion",
                  title=f"AI mixes in the address of a same-name business ({twin['name']})",
                  severity="low" if hedged else "high", truth_value=ta, truth_source=src,
                  explanation=(f"{ad['raw']} belongs to {twin['name']}"
                               + (". The engine flagged it as different this time, but the two businesses "
                                  "are entangled in its sources." if hedged else
                                  ". Customers are sent to the wrong business.")),
                  answer=a, quote=quote)
        elif tad and ad["street_key"] == tad[0]["street_key"]:
            c.add(f"address:wrong:{ad['number']}", field="address", type_="wrong_address",
                  title="AI gives a wrong street address", severity="high", truth_value=ta,
                  truth_source=src, explanation=f"AI says {ad['raw']}; you are at {ta}. Navigation apps "
                                                "and delivery drivers follow the wrong number.",
                  answer=a, quote=quote)
    m = BAD_ADDR_RE.search(text)
    if m:
        c.add("address:wrong:reported", field="address", type_="wrong_address",
              title="AI gives a wrong street address", severity="high", truth_value=ta, truth_source=src,
              explanation="The address shown points to a different storefront.", answer=a,
              quote=sent_with(text, m))
    if not found and not m and a["field"] == "address" and ta:
        n = NOT_FOUND.search(text)
        if n:
            c.add("address:missing", field="address", type_="address_not_found",
                  title="AI cannot find your address", severity="medium", truth_value=ta,
                  truth_source=src, explanation="", answer=a, quote=sent_with(text, n))


def check_offers(a, text, truth, c):
    offers = truth["facts"]["offers"]["value"] or []
    src = truth["facts"]["offers"]["source"]
    published = " ".join(o["text"].lower() for o in offers)
    for s, _ in sentences(text):
        m = DEAL_RE.search(s)
        if not m or not re.search(r"\$\d|\d+%|\bfree\b|the same as|same (?:price|cost)|special", s, re.I):
            continue
        if negated(s, m.start()):
            continue
        prices = re.findall(r"\$\d+(?:\.\d\d)?", s)
        if prices and all(p in published for p in prices):
            c.ok("offers", a, s)
            continue
        confirmed_false = a.get("owner_confirmed_false")
        hedged = re.search(r"\b(listing|may be out of date|menu item|third-party)\b", s, re.I)
        sev = "critical" if confirmed_false else ("medium" if hedged else "high")
        c.add("offers:invented" if confirmed_false else
              f"offers:unverified:{re.sub(r'[^a-z0-9]+', '-', m.group(0).lower())}",
              field="offers", type_="invented_deal" if confirmed_false else "unverified_deal",
              title=("AI invents a deal the business never offered" if confirmed_false
                     else "AI quotes a deal or price your website does not publish"),
              severity=sev,
              truth_value=("Published offers: " + "; ".join(o["text"] for o in offers)) if offers
              else "Your website publishes no specials or deals.",
              truth_source=src,
              explanation=("The owner has stated this deal never existed. Customers demand it at the "
                           "counter and staff take the anger." if confirmed_false else
                           "This comes from a third-party listing, not from you. If it is stale, customers "
                           "will expect a price you no longer charge."),
              answer=a, quote=s)


def check_legal(a, text, truth, c):
    for s, _ in sentences(text):
        m = LEGAL_RE.search(s)
        if not m or negated(s, m.start()):
            continue
        if re.search(r"\b(search|check|look up|records?)\b.*\b(court|case\.net|BBB|Better Business)", s, re.I):
            continue  # advice to check records, not a claim
        c.add("legal:claim", field="legal", type_="false_legal_claim",
              title="AI associates the business with a lawsuit, scam or investigation",
              severity="critical", truth_value="No legal action known to the owner.",
              truth_source=truth["facts"]["website"]["value"],
              explanation="Unverified legal claims cost contracts (Wolf River Electric lost a $150k job "
                          "this way). Verify with the owner; if false, use the legal escalation in the "
                          "Fix Kit.", answer=a, quote=s)


def check_identity(a, text, truth, c):
    for t in truth.get("same_name_businesses", []):
        nm = (t.get("name") or "").split("(")[0].strip()
        if len(nm) < 4:
            continue
        addr = t.get("address") or ""
        tokens = [x for x in [t.get("phone"), (addresses_in(addr) or [{}])[0].get("number")]
                  + [p.strip() for p in addr.split(",")[1:2]] if x]
        for m in re.finditer(re.escape(nm), text, re.I):
            q = sent_with(text, m)
            if not any(tok.lower() in q.lower() for tok in tokens):
                continue  # the shared name alone is not evidence of a mix-up
            c.add(f"identity:name:{nm.lower()}", field="identity", type_="same_name_confusion",
                  title=f"AI mentions a same-name business ({t['name']})",
                  severity="low" if HEDGE.search(q) else "medium",
                  truth_value=f"{truth['name']}, {truth['facts']['address']['value']}",
                  truth_source=truth["facts"]["website"]["value"], explanation=t.get("note") or "",
                  answer=a, quote=q)
            break


def check_visibility(answers, truth, c):
    site = truth["facts"]["website"]["value"]
    h = host(site)
    by_provider: dict = {}
    for a in answers:
        if a.get("mode") == "press-report" or not a.get("text"):
            continue
        by_provider.setdefault(a["provider"], []).append(a)
    for prov, items in by_provider.items():
        if any(h in host(u) for a in items for u in a.get("citations", [])):
            continue
        quote, ans = None, items[0]
        for a in items:
            m = NO_SITE_RE.search(a["text"])
            if m:
                quote, ans = sent_with(a["text"], m), a
                break
        c.add(f"visibility:no-site:{prov}", field="visibility", type_="official_site_not_used",
              title="AI does not use your official website as a source", severity="medium",
              truth_value=site, truth_source=site,
              explanation=f"None of the {len(items)} answers from this engine cited {h}. It relied on "
                          "news articles and third-party directories instead, which is how stale or "
                          "invented facts get in.", answer=ans,
              quote=quote or f"(None of these answers cited {h}.)")


def own_site_findings(truth, c):
    for cf in truth.get("conflicts", []):
        c.add(f"ownsite:{cf['field']}", field=cf["field"] if cf["field"] in dict(FIELDS) else "visibility",
              type_="own_source_conflict", title="Your own sources disagree with each other",
              severity="medium", truth_value=cf["detail"], truth_source=cf.get("source") or
              truth["facts"]["website"]["value"],
              explanation="When your website and its structured data (or a listing) disagree, AI engines "
                          "pick one at random. Fix the source so there is one answer.")
    for ob in truth.get("observations", []):
        c.add(f"ownsite:{ob['type']}", field="offers", type_=ob["type"],
              title="Your menu and prices are not machine-readable", severity="low",
              truth_value=ob["detail"], truth_source=ob["source"],
              explanation="Publish the menu and current specials as text on your own site.")
    if not truth.get("structured_data", {}).get("present"):
        c.add("ownsite:no-schema", field="visibility", type_="no_structured_data",
              title="Your website has no LocalBusiness structured data", severity="low",
              truth_value="No schema.org LocalBusiness block found", truth_source=truth["facts"]["website"]["value"],
              explanation="Structured data is the cleanest way to tell search and AI engines your hours, "
                          "address and phone. The Fix Kit includes a ready block.")


# ------------------------------------------------------------------ main
def compare(truth: dict, answers: list[dict]) -> dict:
    c = Collector()
    for a in answers:
        text = a.get("text") or ""
        if not text:
            continue
        for fn in (check_status, check_hours, check_phone, check_address, check_offers,
                   check_legal, check_identity):
            fn(a, text, truth, c)
    check_visibility(answers, truth, c)
    own_site_findings(truth, c)

    for g in c.groups.values():
        if g["type"] in ("hours_not_found", "phone_not_found", "address_not_found"):
            provs = {e["provider"] for e in g["evidence"]}
            if any(x["field"] == g["field"] and x["provider"] in provs for x in c.confirmations):
                g["severity"] = "low"
                g["title"] = g["title"].replace("cannot find", "only sometimes finds")
                g["explanation"] = ("The same engine found it for one question and not for another, "
                                    "so customers get a different answer depending on how they ask.")
    findings = sorted(c.groups.values(), key=lambda g: (SEV_ORDER.index(g["severity"]), g["field"]))
    for f in findings:
        modes = {e.get("mode") for e in f["evidence"]}
        f["current"] = (not f["evidence"]) or bool(modes - {"press-report"})
        f["history_only"] = not f["current"]
        f["times_seen"] = len(f["evidence"])
    current = [f for f in findings if f["current"]]
    score = max(0, 100 - sum(SEV_WEIGHT[f["severity"]] for f in current))
    flags = {}
    for field, label in FIELDS:
        fs = [f for f in current if f["field"] == field]
        worst = min((SEV_ORDER.index(f["severity"]) for f in fs), default=None)
        oks = [x for x in c.confirmations if x["field"] == field]
        flag = ("red" if worst is not None and worst <= 1 else "yellow" if worst is not None and (
            worst == 2 or (worst == 3 and field == "identity"))
                else "green" if oks or (worst == 3) else "grey")
        flags[field] = {"label": label, "flag": flag, "findings": len(fs), "confirmations": len(oks)}
    return {"score": score, "flags": flags, "findings": findings, "confirmations": c.confirmations}


def latest_date(slug: str, before: str | None = None) -> str | None:
    days = sorted(p.stem for p in (ANSWERS_DIR / slug).glob("????-??-??.json"))
    if before:
        days = [d for d in days if d < before]
    return days[-1] if days else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--date")
    a = ap.parse_args()
    truth = load_json(TRUTH_DIR / f"{a.slug}.json")
    if not truth:
        sys.exit(f"No truth file for {a.slug}")
    day = a.date or latest_date(a.slug)
    if not day:
        sys.exit(f"No answers for {a.slug}. Run ask_ai.py first.")
    doc = load_json(ANSWERS_DIR / a.slug / f"{day}.json")
    result = compare(truth, doc["answers"])

    prev_files = sorted(p for p in (FINDINGS_DIR / a.slug).glob("????-??-??.json") if p.stem < day)
    prev = load_json(prev_files[-1]) if prev_files else None
    if prev:
        pk = {f["key"] for f in prev["findings"] if f["current"]}
        ck = {f["key"] for f in result["findings"] if f["current"]}
        result["changes"] = {"since": prev["date"], "new": sorted(ck - pk), "resolved": sorted(pk - ck),
                             "score_before": prev["score"]}
    out = {"slug": a.slug, "name": truth["name"], "date": day, "generated_at": now_iso(),
           "answers_file": f"answers/{a.slug}/{day}.json",
           "engines": sorted({x.get("engine") or x["provider"] for x in doc["answers"]}),
           "runs": doc.get("runs", []), **result}
    path = save_json(FINDINGS_DIR / a.slug / f"{day}.json", out)
    print(f"{truth['name']}: score {out['score']}/100  ->  {path}")
    for f, v in out["flags"].items():
        print(f"  {v['flag']:6} {v['label']}")
    for f in out["findings"]:
        tag = "history" if f["history_only"] else "current"
        print(f"  [{f['severity']:8}] ({tag}) {f['title']}  x{f['times_seen']}")
    if out.get("changes"):
        print("  changes:", out["changes"])


if __name__ == "__main__":
    main()
