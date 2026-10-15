#!/usr/bin/env python3
"""Build a one-page, mobile-first preview website from a business JSON file.

Usage:
    python build_site.py sites/<slug>/business.json              # writes sites/<slug>/index.html
    python build_site.py business.json -o out.html
    python build_site.py business.json --check                   # validate + list placeholders
    python build_site.py business.json --final                   # no preview banner / noindex

Adapted from the local-booking-sites skill. Rules the script enforces:
  * Every string is HTML-escaped and nothing is rendered that is not in the file.
  * Any value written as {"placeholder": "..."} is shown as a dashed, clearly
    labelled placeholder on the page and listed by --check, so a guess can
    never pass as a fact.
  * `sources` (public URLs the facts came from) is required. In preview mode
    they are listed in the footer next to a "not the official site" notice.

Schema: see references/business-schema.md.
"""

import argparse
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAY_LABELS = dict(zip(WEEKDAYS, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))

DEFAULT_THEME = {
    "primary": "#23352b",
    "accent": "#e2a33b",
    "background": "#f7f3ea",
    "surface": "#ffffff",
    "text": "#1c1c1a",
    "muted": "#5f625c",
    "font_display": "Fraunces",
    "font_body": "Inter",
}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def is_ph(value) -> bool:
    return isinstance(value, dict) and "placeholder" in value


def txt(value) -> str:
    """Render a fact, or a visibly marked placeholder."""
    if is_ph(value):
        return f'<span class="ph" title="Placeholder - confirm with owner">{esc(value["placeholder"])}</span>'
    return esc(value)


def walk_placeholders(node, path="") -> list[str]:
    found = []
    if is_ph(node):
        found.append(f'{path or "(root)"}: {node["placeholder"]}')
    elif isinstance(node, dict):
        for k, v in node.items():
            if not k.startswith("_"):
                found += walk_placeholders(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            found += walk_placeholders(v, f"{path}[{i}]")
    return found


def validate(biz: dict) -> list[str]:
    errors = []
    if not biz.get("name") or is_ph(biz.get("name")):
        errors.append("`name` is required and must be a real fact")
    services = biz.get("services") or []
    if not services:
        errors.append("`services` needs at least one entry")
    for i, s in enumerate(services):
        if not s.get("name"):
            errors.append(f"services[{i}] is missing `name`")
    real_contact = [biz.get(k) for k in ("email", "phone", "instagram", "facebook")]
    if not any(v and not is_ph(v) for v in real_contact):
        errors.append("need at least one real public contact route (email, phone, instagram, facebook)")
    sources = biz.get("sources") or []
    if not sources or not all(isinstance(s, dict) and str(s.get("url", "")).startswith("http") for s in sources):
        errors.append("`sources` must list the public URLs every fact came from ({url, note})")
    cta = biz.get("cta") or {}
    if cta and cta.get("kind") not in ("email", "phone", "instagram", "facebook", "url"):
        errors.append("cta.kind must be one of email, phone, instagram, facebook, url")
    hours = biz.get("hours")
    if isinstance(hours, dict):
        for day, span in hours.items():
            if day not in WEEKDAYS:
                errors.append(f"hours key `{day}` must be one of {WEEKDAYS}")
            elif span is not None and not (isinstance(span, list) and len(span) == 2):
                errors.append(f'hours.{day} must be ["HH:MM", "HH:MM"] or null')
    elif hours is not None and not isinstance(hours, list) and not is_ph(hours):
        errors.append("`hours` must be a list of {label, value}, a mon..sun object, or a placeholder")
    return errors


def font_link(theme: dict) -> str:
    fams = []
    for key in ("font_display", "font_body"):
        if theme.get(key) and theme[key] not in fams:
            fams.append(theme[key])
    if not fams:
        return ""
    q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;600;700" for f in fams)
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{esc(q)}&display=swap">')


def price_text(s: dict, currency: str) -> str:
    p = s.get("price")
    if p is None or p == "":
        return ""
    if is_ph(p):
        return txt(p)
    if isinstance(p, (int, float)):
        return esc(f"{currency}{p:,.2f}".rstrip("0").rstrip("."))
    return esc(p)


def twelve(hhmm: str) -> str:
    h, m = (int(x) for x in hhmm.split(":"))
    return f"{(h + 11) % 12 + 1}{':%02d' % m if m else ''} {'p.m.' if h >= 12 else 'a.m.'}"


def render_services(biz: dict) -> str:
    cur = biz.get("currency", "$")
    out = []
    for s in biz["services"]:
        desc = f'<p class="svc-desc">{txt(s["description"])}</p>' if s.get("description") else ""
        price = price_text(s, cur)
        out.append('<li class="svc"><div class="svc-head">'
                   f'<h3>{txt(s["name"])}</h3>'
                   + (f'<span class="svc-price">{price}</span>' if price else "")
                   + f"</div>{desc}</li>")
    return "".join(out)


def render_hours(biz: dict) -> str:
    hours = biz.get("hours")
    if not hours:
        return ""
    if is_ph(hours):
        return f'<p>{txt(hours)}</p>'
    rows = []
    if isinstance(hours, dict):
        for d in WEEKDAYS:
            if d in hours:
                span = hours[d]
                val = "Closed" if not span else f"{twelve(span[0])} – {twelve(span[1])}"
                rows.append(f"<tr><th>{DAY_LABELS[d]}</th><td>{esc(val)}</td></tr>")
    else:
        for h in hours:
            rows.append(f"<tr><th>{txt(h.get('label', ''))}</th><td>{txt(h.get('value', ''))}</td></tr>")
    return f'<table class="hours">{"".join(rows)}</table>'


def map_url(biz: dict) -> str:
    loc = biz.get("location") or {}
    q = loc.get("map_query")
    if not q:
        parts = [loc.get(k) for k in ("address", "city", "state")]
        q = ", ".join(p for p in parts if p and not is_ph(p))
    return f"https://www.google.com/maps/search/?api=1&query={quote(q)}" if q else ""


def contact_items(biz: dict) -> list[tuple[str, str, str]]:
    """(kind, href, label) for each real contact route; placeholders get no href."""
    items = []
    for kind in ("phone", "email", "instagram", "facebook"):
        v = biz.get(kind)
        if not v:
            continue
        if is_ph(v):
            items.append((kind, "", txt(v)))
            continue
        if kind == "phone":
            href = "tel:" + "".join(c for c in v if c.isdigit() or c == "+")
        elif kind == "email":
            href = "mailto:" + v
        elif kind == "instagram":
            href = "https://instagram.com/" + v.lstrip("@")
            v = "@" + v.lstrip("@")
        else:
            href = v if v.startswith("http") else "https://facebook.com/" + v
            v = "Facebook"
        items.append((kind, href, esc(v)))
    return items


def cta_href(biz: dict) -> tuple[str, str]:
    cta = biz.get("cta") or {}
    kind = cta.get("kind")
    label = cta.get("label") or "Get in touch"
    if not kind:
        for k in ("email", "phone", "instagram", "facebook"):
            if biz.get(k) and not is_ph(biz.get(k)):
                kind = k
                break
    if kind == "url":
        return cta.get("url", "#contact"), label
    if kind == "email" and biz.get("email") and not is_ph(biz["email"]):
        subj = quote(cta.get("subject") or f"Enquiry for {biz['name']}")
        body = quote(cta.get("body") or "Hi! I'd like to ask about ")
        return f"mailto:{biz['email']}?subject={subj}&body={body}", label
    for k, href, _ in contact_items(biz):
        if k == kind and href:
            return href, label
    return "#contact", label


def build(biz: dict, final: bool = False) -> str:
    theme = {**DEFAULT_THEME, **(biz.get("theme") or {})}
    loc = biz.get("location") or {}
    city = loc.get("city") if not is_ph(loc.get("city")) else None
    town = ", ".join(x for x in (city, loc.get("state")) if x) if city else ""
    eyebrow = " · ".join(x for x in (biz.get("category"), town) if x)
    cta_link, cta_label = cta_href(biz)
    murl = map_url(biz)
    contacts = contact_items(biz)
    contact_html = "".join(
        f'<li><span class="k">{esc(k.title())}</span>'
        + (f'<a href="{esc(h)}"' + (' target="_blank" rel="noopener"' if h.startswith("http") else "") + f">{lab}</a>" if h else lab)
        + "</li>" for k, h, lab in contacts)
    if loc.get("address") or loc.get("label"):
        where = txt(loc.get("label") or loc.get("address"))
        contact_html = f'<li><span class="k">Where</span>{where}</li>' + contact_html
    highlights = "".join(f"<li>{txt(h)}</li>" for h in biz.get("highlights") or [])
    sources = "".join(
        f'<li><a href="{esc(s["url"])}" rel="noopener nofollow" target="_blank">{esc(s.get("note") or s["url"])}</a></li>'
        for s in biz.get("sources") or [])
    preview = not final
    by = biz.get("_preview_by")
    banner = (f'<div class="preview" role="note">Free preview made for {esc(biz["name"])} from public info'
              f'{" by " + esc(by) if by else ""} · not the official site</div>') if preview else ""
    footer_extra = (f'<details class="srcs"><summary>Where these details came from</summary><ul>{sources}</ul>'
                    '<p>Anything shown with a dashed outline is a placeholder for the owner to confirm.</p></details>'
                    ) if preview else ""
    map_btn = (f'<a class="btn btn-ghost" href="{esc(murl)}" target="_blank" rel="noopener">Open in Maps</a>'
               if murl else "")
    about = biz.get("about")
    return TEMPLATE.format(
        robots='<meta name="robots" content="noindex, nofollow">' if preview else "",
        title=esc(f'{biz["name"]}{" · " + town if town else ""}'),
        description=esc(biz.get("tagline") if isinstance(biz.get("tagline"), str) else biz["name"]),
        fonts=font_link(theme),
        **{k: esc(theme[k]) for k in DEFAULT_THEME},
        banner=banner,
        name=esc(biz["name"]),
        eyebrow=f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else "",
        tagline=f'<p class="tagline">{txt(biz["tagline"])}</p>' if biz.get("tagline") else "",
        cta_link=esc(cta_link),
        cta_label=esc(cta_label),
        map_btn=map_btn,
        about=(f'<section id="about" class="wrap about"><h2>About</h2><p>{txt(about)}</p>'
               + (f'<ul class="ticks">{highlights}</ul>' if highlights else "") + "</section>") if about else "",
        services_title=esc(biz.get("services_title") or "What we offer"),
        services=render_services(biz),
        hours_title=esc(biz.get("hours_title") or "Hours"),
        hours=render_hours(biz) or '<p class="muted">Ask for current hours.</p>',
        contact=contact_html,
        map_link=(f'<p><a class="maplink" href="{esc(murl)}" target="_blank" rel="noopener">'
                  f'Get directions &rarr;</a></p>') if murl else "",
        footer_extra=footer_extra,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{robots}
{fonts}
<style>
:root {{
  --primary: {primary}; --accent: {accent}; --bg: {background}; --surface: {surface};
  --text: {text}; --muted: {muted};
  --display: "{font_display}", Georgia, serif; --body: "{font_body}", system-ui, sans-serif;
  --r: 16px;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--bg); color: var(--text); font: 16px/1.6 var(--body); overflow-x: hidden; }}
a {{ color: inherit; }}
h1, h2, h3 {{ font-family: var(--display); line-height: 1.12; margin: 0 0 .5em; letter-spacing: -.01em; }}
h2 {{ font-size: clamp(1.6rem, 5vw, 2.2rem); }}
.wrap {{ max-width: 980px; margin: 0 auto; padding-left: 20px; padding-right: 20px; }}
.hero .wrap {{ position: relative; z-index: 1; }}
.preview {{ background: #111; color: #fff; text-align: center; font: 500 .8rem/1.4 var(--body); padding: 8px 16px; }}
.topbar {{ position: sticky; top: 0; z-index: 10; background: color-mix(in srgb, var(--primary) 94%, transparent);
  backdrop-filter: blur(6px); color: #fff; }}
.topbar .wrap {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; height: 58px; }}
.brand {{ font-family: var(--display); font-weight: 700; font-size: 1.1rem; text-decoration: none;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.btn {{ display: inline-block; border: 0; cursor: pointer; font: 600 1rem var(--body); padding: 13px 24px;
  border-radius: 999px; background: var(--accent); color: var(--primary); text-decoration: none; text-align: center; }}
.btn-sm {{ padding: 9px 16px; font-size: .9rem; white-space: nowrap; }}
.btn-ghost {{ background: transparent; color: #fff; box-shadow: inset 0 0 0 2px rgba(255,255,255,.6); }}
a:focus-visible, .btn:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 3px; }}
.hero {{ position: relative; overflow: hidden; color: #fff; padding: 64px 0 76px;
  background: radial-gradient(120% 90% at 100% 0%, color-mix(in srgb, var(--accent) 45%, transparent) 0, transparent 55%),
              radial-gradient(90% 80% at 0% 100%, rgba(255,255,255,.10) 0, transparent 60%), var(--primary); }}
.hero::after {{ content: ""; position: absolute; right: -120px; top: -120px; width: 230px; height: 230px;
  border-radius: 50%; border: 28px solid color-mix(in srgb, var(--accent) 55%, transparent); opacity: .5; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .14em; font-size: .78rem; font-weight: 600;
  color: var(--accent); margin: 0 0 14px; }}
.hero h1 {{ font-size: clamp(2.4rem, 11vw, 4.4rem); max-width: 14ch; }}
.tagline {{ font-size: 1.12rem; opacity: .92; margin: 0 0 28px; max-width: 34ch; }}
.actions {{ display: flex; flex-wrap: wrap; gap: 12px; }}
section {{ padding-top: 52px; padding-bottom: 52px; }}
[id] {{ scroll-margin-top: 70px; }}
.about {{ padding-bottom: 0; }}
#contact {{ padding-top: 8px; }}
.about p {{ max-width: 62ch; font-size: 1.06rem; }}
.ticks {{ list-style: none; padding: 0; margin: 18px 0 0; display: grid; gap: 10px; }}
.ticks li {{ position: relative; padding-left: 30px; }}
.ticks li::before {{ content: ""; position: absolute; left: 0; top: .45em; width: 16px; height: 9px;
  border-left: 3px solid var(--accent); border-bottom: 3px solid var(--accent); transform: rotate(-45deg); }}
.services {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 12px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
.svc {{ background: var(--surface); border-radius: var(--r); padding: 18px 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,.06), 0 6px 18px rgba(0,0,0,.04); border-top: 4px solid var(--accent); }}
.svc-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 12px; align-items: baseline; }}
.svc h3 {{ font-size: 1.12rem; margin: 0; }}
.svc-price {{ font-weight: 700; }}
.svc-desc {{ margin: 6px 0 0; color: var(--muted); font-size: .95rem; }}
.info {{ display: grid; gap: 18px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
.card {{ background: var(--surface); border-radius: var(--r); padding: 22px; box-shadow: 0 1px 2px rgba(0,0,0,.06); }}
.hours {{ border-collapse: collapse; width: 100%; }}
.hours th {{ text-align: left; vertical-align: top; padding: 6px 16px 6px 0; font-weight: 600; width: 44%; }}
.hours td {{ padding: 6px 0; }}
.hours tr + tr {{ border-top: 1px solid rgba(0,0,0,.07); }}
.contact {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; overflow-wrap: anywhere; }}
.contact .k {{ display: block; font-size: .74rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }}
.maplink {{ font-weight: 600; color: var(--primary); }}
.muted {{ color: var(--muted); }}
.ph {{ border: 2px dashed var(--accent); border-radius: 6px; padding: 0 6px; background: color-mix(in srgb, var(--accent) 12%, transparent); }}
.ph::before {{ content: "Placeholder: "; font-weight: 600; font-size: .8em; }}
.cta-band {{ background: var(--primary); color: #fff; text-align: center; }}
.cta-band p {{ opacity: .9; margin: 0 auto 22px; max-width: 40ch; }}
footer {{ padding: 28px 0 100px; color: var(--muted); font-size: .88rem; }}
.srcs summary {{ cursor: pointer; font-weight: 600; }}
.srcs ul {{ padding-left: 18px; overflow-wrap: anywhere; }}
.fab {{ position: fixed; left: 16px; right: 16px; bottom: 16px; z-index: 20; box-shadow: 0 8px 24px rgba(0,0,0,.25); }}
@media (min-width: 720px) {{ .fab {{ display: none; }} footer {{ padding-bottom: 28px; }} .hero {{ padding: 96px 0 104px; }} }}
</style>
</head>
<body>
{banner}
<header class="topbar"><div class="wrap">
  <a class="brand" href="#top">{name}</a>
  <a class="btn btn-sm" href="{cta_link}">{cta_label}</a>
</div></header>
<main id="top">
<section class="hero"><div class="wrap">
  {eyebrow}
  <h1>{name}</h1>
  {tagline}
  <div class="actions"><a class="btn" href="{cta_link}">{cta_label}</a>{map_btn}</div>
</div></section>
{about}
<section id="services" class="wrap">
  <h2>{services_title}</h2>
  <ul class="services">{services}</ul>
</section>
<section id="contact" class="wrap info">
  <div class="card"><h2>{hours_title}</h2>{hours}{map_link}</div>
  <div class="card"><h2>Contact</h2><ul class="contact">{contact}</ul></div>
</section>
<section class="cta-band"><div class="wrap">
  <h2>Say hello</h2>
  <p>Questions, orders or bookings &mdash; reach {name} directly.</p>
  <a class="btn" href="{cta_link}">{cta_label}</a>
</div></section>
</main>
<footer><div class="wrap">
  <p>&copy; <span id="yr"></span> {name}</p>
  {footer_extra}
</div></footer>
<a class="btn fab" href="{cta_link}">{cta_label}</a>
<script>document.getElementById("yr").textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("business", type=Path, help="business JSON file")
    ap.add_argument("-o", "--out", type=Path, help="output HTML (default: index.html next to the JSON)")
    ap.add_argument("--check", action="store_true", help="validate and list placeholders; write nothing")
    ap.add_argument("--final", action="store_true",
                    help="omit the preview banner, noindex tag and source list (only after the owner has paid)")
    args = ap.parse_args()

    biz = json.loads(args.business.read_text(encoding="utf-8"))
    errors = validate(biz)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        return 1
    phs = walk_placeholders(biz)
    if args.check:
        print(f"ok: {args.business}")
        for p in phs:
            print(f"  placeholder  {p}")
        return 0
    out = args.out or args.business.with_name("index.html")
    out.write_text(build(biz, final=args.final), encoding="utf-8")
    print(f"wrote {out}" + (f" ({len(phs)} placeholder(s) to confirm)" if phs else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
