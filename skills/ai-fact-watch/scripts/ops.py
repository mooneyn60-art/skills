#!/usr/bin/env python3
"""Operations state for the self-serve service: free-check requests, paying
customers, payments, cancellations and refunds. The scheduled agent drives
everything through this CLI so every decision is logged and repeatable.

State lives in data/ (JSON, plus an append-only data/events.jsonl audit log).

Commands:
  ops.py preflight                         # is outbound allowed? (config filled + enabled)
  ops.py add-request --email E --business B --town T [--region R] [--website U] [--ref ID]
  ops.py due                               # JSON list of work due now
  ops.py done --id ID --score N --report PATH [--findings PATH]
  ops.py fail --id ID --reason TEXT
  ops.py parse-payment --file EMAIL.txt    # Stripe notification email -> {email, amount, plan}
  ops.py stripe-sync                       # STRIPE_API_KEY: activate new paid checkouts
  ops.py activate --email E --plan watch|emergency --ref PAYMENT_REF [--business B --town T --website U]
  ops.py classify --file REPLY.txt         # customer reply -> cancel|refund|legal|angry|question|other
  ops.py cancel --email E [--reason TEXT]
  ops.py refund-decision --email E         # applies config.policy, prints the decision
  ops.py mark-refunded --email E --ref REFUND_ID
  ops.py optout --email E
  ops.py status
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone

from common import DATA_DIR, ROOT, fetch, load_json, now_iso, save_json, slugify

REQ = DATA_DIR / "requests.json"
CUS = DATA_DIR / "customers.json"
OPT = DATA_DIR / "optout.json"
EVENTS = DATA_DIR / "events.jsonl"
CONFIG = load_json(ROOT / "config.json", {})
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(d: datetime) -> str:
    return d.isoformat()


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s)


def log(kind: str, **data) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a") as f:
        f.write(json.dumps({"at": now_iso(), "event": kind, **data}) + "\n")


def out(obj) -> None:
    print(json.dumps(obj, indent=2))


def placeholders_left() -> list[str]:
    return sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", json.dumps(CONFIG))))


# ----------------------------------------------------------------- requests
def add_request(a) -> None:
    email = a.email.strip().lower()
    if not EMAIL_RE.fullmatch(email):
        sys.exit("invalid email")
    reqs = load_json(REQ, [])
    if email in load_json(OPT, []):
        out({"accepted": False, "reason": "opted out"})
        return
    today = now().date().isoformat()
    biz_slug = slugify(f"{a.business} {a.town}")
    if any(r["email"] == email and r["slug"] == biz_slug for r in reqs):
        out({"accepted": False, "reason": "duplicate request"})
        return
    lim = CONFIG.get("limits", {})
    per_email = sum(1 for r in reqs if r["email"] == email)
    if per_email >= lim.get("free_checks_per_email", 1):
        out({"accepted": False, "reason": "free check already used for this email"})
        return
    todays = sum(1 for r in reqs if r["created_at"][:10] == today and r["status"] != "queued_overflow")
    status = "pending" if todays < lim.get("free_checks_per_day", 20) else "queued_overflow"
    r = {"id": f"req-{len(reqs) + 1:05d}", "ref": a.ref, "email": email, "business": a.business.strip(),
         "town": a.town.strip(), "region": (a.region or "").strip(), "website": (a.website or "").strip(),
         "slug": biz_slug, "status": status, "created_at": now_iso(), "attempts": 0}
    reqs.append(r)
    save_json(REQ, reqs)
    log("request_added", id=r["id"], email=email, slug=biz_slug, status=status)
    out({"accepted": True, **r})


def due(_a) -> None:
    t = now()
    reqs = load_json(REQ, [])
    lim = CONFIG.get("limits", {}).get("free_checks_per_day", 20)
    done_today = sum(1 for r in reqs if (r.get("finished_at") or "")[:10] == t.date().isoformat())
    work = []
    for r in reqs:
        if r["status"] in ("pending", "queued_overflow") and r["attempts"] < 3 and done_today < lim:
            work.append({"kind": "free_check", **r})
            done_today += 1
    for c in load_json(CUS, []):
        if c["status"] != "active":
            continue
        if c["plan"] == "emergency" and not c.get("kit_sent_at"):
            work.append({"kind": "emergency_kit", **c})
        if parse(c["next_check_at"]) <= t:
            work.append({"kind": f"{c['plan']}_recheck", **c})
    out(work)


def finish(a, ok: bool) -> None:
    reqs, cus = load_json(REQ, []), load_json(CUS, [])
    for coll, path in ((reqs, REQ), (cus, CUS)):
        for r in coll:
            if r["id"] != a.id:
                continue
            if ok:
                if path == REQ:
                    r.update(status="done", finished_at=now_iso(), score=a.score, report=a.report)
                else:
                    days = CONFIG["plans"][r["plan"]]["recheck_days"]
                    r.setdefault("history", []).append({"at": now_iso(), "score": a.score, "report": a.report,
                                                        "findings": a.findings})
                    r["next_check_at"] = iso(now() + timedelta(days=days))
                    if a.kit:
                        r["kit_sent_at"] = now_iso()
                    if r["plan"] == "emergency" and parse(r["ends_at"]) <= now():
                        r["status"] = "completed"
            else:
                r["attempts"] = r.get("attempts", 0) + 1
                r["last_error"] = a.reason
                if path == REQ and r["attempts"] >= 3:
                    r["status"] = "failed"
            save_json(path, coll)
            log("work_done" if ok else "work_failed", id=a.id, score=getattr(a, "score", None),
                reason=getattr(a, "reason", None))
            out(r)
            return
    sys.exit(f"unknown id {a.id}")


# ----------------------------------------------------------------- payments
def plan_for_amount(cents: int) -> str | None:
    for name, p in CONFIG.get("plans", {}).items():
        if p.get("price_usd") and int(p["price_usd"] * 100) == cents:
            return name
    return None


def parse_payment(a) -> None:
    text = open(a.file).read()
    m = re.search(r"\$\s?(\d{1,4}(?:,\d{3})*\.\d{2})", text)
    cents = int(round(float(m.group(1).replace(",", "")) * 100)) if m else None
    own = (CONFIG.get("sender", {}).get("gmail") or "").lower()
    emails = [e.lower() for e in EMAIL_RE.findall(text)
              if not re.search(r"stripe\.com|noreply|no-reply", e, re.I) and e.lower() != own]
    is_stripe = bool(re.search(r"stripe", text, re.I))
    out({"is_stripe": is_stripe, "amount_cents": cents, "plan": plan_for_amount(cents) if cents else None,
         "customer_email": emails[0] if emails else None,
         "ref": (re.search(r"\b(pi_|ch_|cs_)[A-Za-z0-9]+", text) or [None])[0],
         "trust": "verify with stripe-sync when STRIPE_API_KEY is set; otherwise only act on emails "
                  "from a stripe.com sender that passed DKIM (Gmail shows 'signed-by: stripe.com')"})


def stripe_get(path: str, params: dict) -> dict:
    key = os.environ["STRIPE_API_KEY"]
    _, _, body = fetch(f"https://api.stripe.com/v1/{path}?{urllib.parse.urlencode(params)}",
                       headers={"Authorization": f"Bearer {key}"})
    return json.loads(body)


def stripe_sync(_a) -> None:
    if not os.environ.get("STRIPE_API_KEY"):
        out({"skipped": "STRIPE_API_KEY not set; use Gmail payment notifications + parse-payment"})
        return
    ids = {v: k for k, v in CONFIG.get("stripe_payment_link_ids", {}).items() if not v.startswith("{{")}
    since = int((now() - timedelta(days=3)).timestamp())
    sessions = stripe_get("checkout/sessions", {"limit": 50, "created[gte]": since, "status": "complete"})
    known = {c.get("ref") for c in load_json(CUS, [])} | {c.get("sub_ref") for c in load_json(CUS, [])}
    activated = []
    for s in sessions.get("data", []):
        if s["id"] in known or s.get("payment_status") not in ("paid", "no_payment_required"):
            continue
        plan = ids.get(s.get("payment_link")) or plan_for_amount(s.get("amount_total") or 0)
        email = (s.get("customer_details") or {}).get("email")
        if plan in ("watch", "emergency") and email:
            fields = {f.get("key"): (f.get("text") or {}).get("value") for f in s.get("custom_fields", [])}
            activated.append(_activate(email, plan, s["id"], fields.get("business"), fields.get("town"),
                                       fields.get("website"), s.get("subscription")))
    out({"activated": activated})


def _activate(email, plan, ref, business=None, town=None, website=None, sub_ref=None) -> dict:
    email = email.lower()
    cus = load_json(CUS, [])
    if any(c.get("ref") == ref for c in cus):
        return {"already_active": ref}
    req = next((r for r in reversed(load_json(REQ, [])) if r["email"] == email), {})
    t = now()
    c = {"id": f"cus-{len(cus) + 1:05d}", "email": email, "plan": plan, "ref": ref, "sub_ref": sub_ref,
         "business": business or req.get("business"), "town": town or req.get("town"),
         "region": req.get("region", ""), "website": website or req.get("website"),
         "slug": slugify(f"{business or req.get('business', '')} {town or req.get('town', '')}"),
         "status": "active" if (business or req.get("business")) else "needs_details",
         "paid_at": iso(t), "next_check_at": iso(t)}
    if plan == "emergency":
        c["ends_at"] = iso(t + timedelta(days=CONFIG["plans"]["emergency"]["duration_days"]))
    cus.append(c)
    save_json(CUS, cus)
    log("customer_activated", id=c["id"], email=email, plan=plan, ref=ref, status=c["status"])
    return c


def activate(a) -> None:
    out(_activate(a.email, a.plan, a.ref, a.business, a.town, a.website))


# ------------------------------------------------------------ replies/policy
CLASSES = [
    ("legal", r"\b(lawyer|attorney|sue|lawsuit|legal action|cease and desist|defam)"),
    ("refund", r"\b(refund|money back|charge ?back|dispute|didn'?t authori[sz]e)"),
    ("cancel", r"\b(cancel|unsubscribe|stop (?:the |my )?(?:subscription|emails|service)|remove me)"),
    ("angry", r"\b(scam|ripoff|rip-off|furious|terrible|useless|garbage|worst)"),
    ("question", r"\?"),
]


def classify(a) -> None:
    text = open(a.file).read()
    body = re.split(r"\n(?:On .+ wrote:|>)", text, maxsplit=1)[0]
    hits = [k for k, rx in CLASSES if re.search(rx, body, re.I)]
    out({"class": hits[0] if hits else "other", "all": hits,
         "action": {"legal": "refund-decision + cancel + optout; send template 'legal'; no further contact",
                    "refund": "refund-decision, then template 'refund-*'",
                    "cancel": "cancel, then template 'cancelled'",
                    "angry": "apologise with template 'sorry', offer refund per policy",
                    "question": "answer from templates/emails.md FAQ only; if not covered, send 'faq-fallback'",
                    "other": "no reply needed unless it asks something"}[hits[0] if hits else "other"]})


def cancel(a) -> None:
    cus = load_json(CUS, [])
    hit = [c for c in cus if c["email"] == a.email.lower() and c["status"] in ("active", "needs_details")]
    for c in hit:
        c["status"] = "cancelled"
        c["cancelled_at"] = now_iso()
        c["cancel_reason"] = a.reason
        if c["plan"] == "watch":
            c["service_until"] = iso(parse(c["paid_at"]) + timedelta(days=30))
    save_json(CUS, cus)
    log("cancelled", email=a.email.lower(), n=len(hit), reason=a.reason)
    out({"cancelled": [c["id"] for c in hit],
         "stripe": "cancel subscription via API (DELETE /v1/subscriptions/<sub_ref>) when STRIPE_API_KEY "
                   "is set; otherwise send template 'cancel-self-serve' with the Stripe customer portal link"})


def refund_decision(a) -> None:
    pol = CONFIG.get("policy", {})
    cus = [c for c in load_json(CUS, []) if c["email"] == a.email.lower()]
    if not cus:
        out({"decision": "no_payment_found", "template": "refund-not-found"})
        return
    c = cus[-1]
    age = (now() - parse(c["paid_at"])).days
    window = pol.get("refund_window_days", 14)
    if age <= window:
        d = {"decision": "full_refund", "template": "refund-approved"}
    elif c["plan"] == "emergency" and not c.get("kit_sent_at"):
        d = {"decision": "full_refund", "template": "refund-approved", "why": "kit not delivered"}
    else:
        d = {"decision": "cancel_no_refund", "template": "refund-outside-window"}
    d.update(customer=c["id"], plan=c["plan"], days_since_payment=age, payment_ref=c.get("ref"),
             how="POST /v1/refunds with payment_intent of the checkout session (STRIPE_API_KEY)")
    log("refund_decision", email=a.email.lower(), **{k: v for k, v in d.items() if k != "how"})
    out(d)


def mark_refunded(a) -> None:
    cus = load_json(CUS, [])
    for c in cus:
        if c["email"] == a.email.lower():
            c["status"], c["refund_ref"], c["refunded_at"] = "refunded", a.ref, now_iso()
    save_json(CUS, cus)
    log("refunded", email=a.email.lower(), ref=a.ref)
    out({"ok": True})


def optout(a) -> None:
    lst = load_json(OPT, [])
    if a.email.lower() not in lst:
        lst.append(a.email.lower())
    save_json(OPT, lst)
    log("optout", email=a.email.lower())
    out({"ok": True})


def preflight(_a) -> None:
    left = placeholders_left()
    keys = {k: bool(os.environ.get(k)) for k in ("SERPAPI_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY", "STRIPE_API_KEY")}
    ok = CONFIG.get("outbound_enabled") is True and not left
    out({"outbound_allowed": ok, "outbound_enabled": CONFIG.get("outbound_enabled"),
         "placeholders_left": left, "provider_keys": keys,
         "note": "When outbound_allowed is false: run checks and build reports, save Gmail DRAFTS only, send nothing."})


def status(_a) -> None:
    reqs, cus = load_json(REQ, []), load_json(CUS, [])
    count = lambda xs, k: {v: sum(1 for x in xs if x[k] == v) for v in sorted({x[k] for x in xs})}
    out({"requests": count(reqs, "status"), "customers": count(cus, "status"),
         "plans": count([c for c in cus if c["status"] == "active"], "plan")})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add-request")
    for k in ("email", "business", "town"):
        p.add_argument(f"--{k}", required=True)
    for k in ("region", "website", "ref"):
        p.add_argument(f"--{k}")
    sub.add_parser("due")
    p = sub.add_parser("done")
    p.add_argument("--id", required=True)
    p.add_argument("--score", type=int, required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--findings")
    p.add_argument("--kit", action="store_true", help="the Fix Kit was delivered in this run")
    p = sub.add_parser("fail")
    p.add_argument("--id", required=True)
    p.add_argument("--reason", required=True)
    p = sub.add_parser("parse-payment")
    p.add_argument("--file", required=True)
    sub.add_parser("stripe-sync")
    p = sub.add_parser("activate")
    p.add_argument("--email", required=True)
    p.add_argument("--plan", choices=["watch", "emergency"], required=True)
    p.add_argument("--ref", required=True)
    for k in ("business", "town", "website"):
        p.add_argument(f"--{k}")
    p = sub.add_parser("classify")
    p.add_argument("--file", required=True)
    p = sub.add_parser("cancel")
    p.add_argument("--email", required=True)
    p.add_argument("--reason")
    for name in ("refund-decision", "optout"):
        sub.add_parser(name).add_argument("--email", required=True)
    p = sub.add_parser("mark-refunded")
    p.add_argument("--email", required=True)
    p.add_argument("--ref", required=True)
    sub.add_parser("preflight")
    sub.add_parser("status")
    a = ap.parse_args()
    fn = {"add-request": add_request, "due": due, "done": lambda x: finish(x, True),
          "fail": lambda x: finish(x, False), "parse-payment": parse_payment, "stripe-sync": stripe_sync,
          "activate": activate, "classify": classify, "cancel": cancel, "refund-decision": refund_decision,
          "mark-refunded": mark_refunded, "optout": optout, "preflight": preflight, "status": status}[a.cmd]
    fn(a)


if __name__ == "__main__":
    main()
