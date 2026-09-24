#!/usr/bin/env python3
"""Build a single-file, mobile-first booking website from a business JSON file.

Usage:
    python build_site.py business.json -o site.html
    python build_site.py business.json --check   # validate only

The JSON schema is documented in references/business-schema.md. Every string
is HTML-escaped, and nothing is rendered that is not in the input file, so the
page never shows invented facts.

The booking widget has no server. Picking a service, date and time produces a
booking *request* that the visitor sends to the business by email, text or
Instagram DM, or that is POSTed to `booking.endpoint` (for example a Formspree
form) when one is configured. The business still confirms each appointment.
"""

import argparse
import html
import json
import sys
from pathlib import Path

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

DEFAULT_THEME = {
    "primary": "#1f2a44",
    "accent": "#c8a15a",
    "background": "#faf7f2",
    "surface": "#ffffff",
    "text": "#1b1b1b",
    "muted": "#6b6b6b",
    "font_display": "Fraunces",
    "font_body": "Inter",
}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def validate(biz: dict) -> list[str]:
    """Return a list of problems; empty means the file is usable."""
    errors = []
    if not biz.get("name"):
        errors.append("`name` is required")
    services = biz.get("services") or []
    if not services:
        errors.append("`services` needs at least one entry")
    for i, s in enumerate(services):
        if not s.get("name"):
            errors.append(f"services[{i}] is missing `name`")
        dur = s.get("duration_min")
        if dur is not None and (not isinstance(dur, int) or dur <= 0):
            errors.append(f"services[{i}].duration_min must be a positive integer")
    contact = [biz.get("email"), biz.get("phone"), biz.get("instagram"),
               (biz.get("booking") or {}).get("endpoint")]
    if not any(contact):
        errors.append("need at least one of `email`, `phone`, `instagram` or "
                      "`booking.endpoint` so booking requests can reach the business")
    hours = (biz.get("booking") or {}).get("hours") or {}
    for day, span in hours.items():
        if day not in WEEKDAYS:
            errors.append(f"booking.hours key `{day}` must be one of {WEEKDAYS}")
        elif span is not None and (not isinstance(span, list) or len(span) != 2):
            errors.append(f"booking.hours.{day} must be [\"HH:MM\", \"HH:MM\"] or null")
    for i, r in enumerate(biz.get("reviews") or []):
        if not r.get("quote"):
            errors.append(f"reviews[{i}] is missing `quote`")
    return errors


def font_link(theme: dict) -> str:
    families = []
    for key in ("font_display", "font_body"):
        fam = theme.get(key)
        if fam and fam not in families:
            families.append(fam)
    if not families:
        return ""
    query = "&".join(
        "family=" + f.replace(" ", "+") + ":wght@400;600;700" for f in families
    )
    return (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{esc(query)}&display=swap">'
    )


def format_price(service: dict, currency: str) -> str:
    price = service.get("price")
    if price is None or price == "":
        return ""
    if isinstance(price, (int, float)):
        amount = f"{price:,.2f}".rstrip("0").rstrip(".")
        return f"{currency}{amount}"
    return str(price)


def render_services(biz: dict, currency: str) -> str:
    items = []
    for s in biz["services"]:
        meta = []
        price = format_price(s, currency)
        if s.get("duration_min"):
            meta.append(f'{s["duration_min"]} min')
        desc = f'<p class="svc-desc">{esc(s["description"])}</p>' if s.get("description") else ""
        items.append(
            '<li class="svc">'
            f'<div class="svc-head"><h3>{esc(s["name"])}</h3>'
            f'<span class="svc-price">{esc(price)}</span></div>'
            f'{desc}'
            f'<p class="svc-meta">{esc(" · ".join(meta))}</p>'
            "</li>"
        )
    return "\n".join(items)


def render_reviews(biz: dict) -> str:
    reviews = biz.get("reviews") or []
    if not reviews:
        return ""
    cards = []
    for r in reviews:
        who = r.get("author", "")
        src = r.get("source", "")
        cite = " · ".join(x for x in (who, src) if x)
        cards.append(
            f'<figure class="review"><blockquote>“{esc(r["quote"])}”</blockquote>'
            + (f"<figcaption>{esc(cite)}</figcaption>" if cite else "")
            + "</figure>"
        )
    return (
        '<section id="reviews" class="band"><div class="wrap">'
        '<h2>What clients say</h2><div class="reviews">'
        + "".join(cards)
        + "</div></div></section>"
    )


def render_gallery(biz: dict) -> str:
    photos = biz.get("photos") or []
    if not photos:
        return ""
    imgs = "".join(
        f'<img src="{esc(p.get("src") if isinstance(p, dict) else p)}" '
        f'alt="{esc(p.get("alt", biz["name"]) if isinstance(p, dict) else biz["name"])}" loading="lazy">'
        for p in photos
    )
    return f'<section class="gallery" aria-label="Photos">{imgs}</section>'


def render_hours(biz: dict) -> str:
    hours = (biz.get("booking") or {}).get("hours") or {}
    if not hours:
        return ""
    labels = {"mon": "Mon", "tue": "Tue", "wed": "Wed", "thu": "Thu",
              "fri": "Fri", "sat": "Sat", "sun": "Sun"}
    rows = []
    for day in WEEKDAYS:
        if day not in hours:
            continue
        span = hours[day]
        text = "Closed" if not span else f"{span[0]} – {span[1]}"
        rows.append(f"<tr><th>{labels[day]}</th><td>{esc(text)}</td></tr>")
    return f'<table class="hours">{"".join(rows)}</table>'


def render_contact(biz: dict) -> str:
    lines = []
    loc = biz.get("location") or {}
    addr = ", ".join(x for x in (loc.get("address"), loc.get("city")) if x)
    if addr:
        lines.append(f"<li>{esc(addr)}</li>")
    if biz.get("phone"):
        tel = "".join(c for c in biz["phone"] if c.isdigit() or c == "+")
        lines.append(f'<li><a href="tel:{esc(tel)}">{esc(biz["phone"])}</a></li>')
    if biz.get("email"):
        lines.append(f'<li><a href="mailto:{esc(biz["email"])}">{esc(biz["email"])}</a></li>')
    if biz.get("instagram"):
        handle = biz["instagram"].lstrip("@")
        lines.append(
            f'<li><a href="https://instagram.com/{esc(handle)}" rel="noopener" '
            f'target="_blank">@{esc(handle)}</a></li>'
        )
    return "".join(lines)


def build(biz: dict, demo: dict | None = None) -> str:
    """Render the page. `demo` ({"by", "contact"}) makes a locked preview."""
    theme = {**DEFAULT_THEME, **(biz.get("theme") or {})}
    currency = biz.get("currency", "$")
    booking = biz.get("booking") or {}
    config = {
        "name": biz["name"],
        "email": biz.get("email"),
        "phone": biz.get("phone"),
        "instagram": (biz.get("instagram") or "").lstrip("@") or None,
        "endpoint": None if demo else booking.get("endpoint"),
        "demo": demo,
        "daysAhead": booking.get("days_ahead", 21),
        "slotMinutes": booking.get("slot_minutes", 30),
        "hours": booking.get("hours") or {d: ["09:00", "17:00"] for d in WEEKDAYS[:6]},
        "services": [
            {"name": s["name"], "price": format_price(s, currency),
             "duration": s.get("duration_min", 30)}
            for s in biz["services"]
        ],
    }
    # Escape "<" so no field can close the data block early.
    config_json = json.dumps(config).replace("<", "\\u003c")

    tagline = biz.get("tagline", "")
    bio = biz.get("bio", "")
    city = (biz.get("location") or {}).get("city", "")
    title = f'{biz["name"]}{" · " + city if city else ""}'
    hero_img = ""
    photos = biz.get("photos") or []
    if photos:
        first = photos[0]
        src = first.get("src") if isinstance(first, dict) else first
        hero_img = f' style="--hero-img:url(&quot;{esc(src)}&quot;)"'

    demo_meta = demo_ribbon = ""
    if demo:
        demo_meta = '<meta name="robots" content="noindex, nofollow">'
        demo_ribbon = (
            '<div class="demo-ribbon" role="note">Demo preview by '
            f'{esc(demo["by"])} · not live yet</div>'
        )

    return TEMPLATE.format(
        demo_meta=demo_meta,
        demo_ribbon=demo_ribbon,
        title=esc(title),
        description=esc(tagline or bio or biz["name"]),
        fonts=font_link(theme),
        primary=esc(theme["primary"]),
        accent=esc(theme["accent"]),
        background=esc(theme["background"]),
        surface=esc(theme["surface"]),
        text=esc(theme["text"]),
        muted=esc(theme["muted"]),
        font_display=esc(theme["font_display"]),
        font_body=esc(theme["font_body"]),
        name=esc(biz["name"]),
        tagline=f'<p class="tagline">{esc(tagline)}</p>' if tagline else "",
        hero_img=hero_img,
        hero_class=" has-img" if photos else "",
        about=(f'<section id="about" class="wrap about"><h2>About</h2><p>{esc(bio)}</p></section>'
               if bio else ""),
        services=render_services(biz, currency),
        gallery=render_gallery(biz),
        reviews=render_reviews(biz),
        hours=render_hours(biz),
        contact=render_contact(biz),
        config=config_json,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{demo_meta}
{fonts}
<style>
:root {{
  --primary: {primary}; --accent: {accent}; --bg: {background};
  --surface: {surface}; --text: {text}; --muted: {muted};
  --display: "{font_display}", Georgia, serif;
  --body: "{font_body}", system-ui, -apple-system, sans-serif;
  --radius: 14px;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--bg); color: var(--text); font: 16px/1.6 var(--body); }}
a {{ color: inherit; }}
h1, h2, h3 {{ font-family: var(--display); line-height: 1.15; margin: 0 0 .5em; }}
h2 {{ font-size: clamp(1.6rem, 4vw, 2.2rem); }}
.wrap {{ max-width: 960px; margin: 0 auto; padding-left: 20px; padding-right: 20px; }}
.topbar {{ position: sticky; top: 0; z-index: 10; background: var(--primary); color: #fff; }}
.topbar .wrap {{ display: flex; align-items: center; justify-content: space-between; height: 60px; }}
.brand {{ font-family: var(--display); font-weight: 700; font-size: 1.15rem; text-decoration: none; }}
.btn {{ display: inline-block; border: 0; cursor: pointer; font: 600 1rem var(--body);
  padding: 12px 22px; border-radius: 999px; background: var(--accent); color: var(--primary);
  text-decoration: none; }}
.btn:focus-visible, button:focus-visible, select:focus-visible, input:focus-visible {{
  outline: 3px solid var(--accent); outline-offset: 2px; }}
.btn-lg {{ font-size: 1.15rem; padding: 16px 32px; }}
.hero {{ background: var(--primary); color: #fff; padding: 72px 0 88px; text-align: center; }}
.hero.has-img {{ background: linear-gradient(rgba(0,0,0,.55), rgba(0,0,0,.55)), var(--hero-img) center/cover; }}
.hero h1 {{ font-size: clamp(2.2rem, 8vw, 4rem); }}
.tagline {{ font-size: 1.15rem; opacity: .9; margin: 0 auto 28px; max-width: 36ch; }}
section {{ padding-top: 56px; padding-bottom: 56px; }}
[id] {{ scroll-margin-top: 72px; }}
.about {{ padding-bottom: 0; }}
.about p {{ max-width: 62ch; font-size: 1.05rem; }}
.services {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 14px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
.svc {{ background: var(--surface); border-radius: var(--radius); padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
.svc-head {{ display: flex; justify-content: space-between; gap: 12px; align-items: baseline; }}
.svc h3 {{ font-size: 1.15rem; margin: 0; }}
.svc-price {{ font-weight: 700; color: var(--primary); white-space: nowrap; }}
.svc-desc {{ margin: 8px 0 0; }}
.svc-meta {{ margin: 6px 0 0; color: var(--muted); font-size: .9rem; }}
.gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 4px; padding: 0; }}
.gallery img {{ width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }}
.band {{ background: var(--primary); color: #fff; }}
.reviews {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
.review {{ margin: 0; background: rgba(255,255,255,.08); border-radius: var(--radius); padding: 22px; }}
.review blockquote {{ margin: 0 0 12px; font-size: 1.05rem; }}
.review figcaption {{ color: var(--accent); font-weight: 600; font-size: .9rem; }}
.book {{ background: var(--surface); border-radius: var(--radius); padding: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,.08); max-width: 560px; }}
.step {{ margin-bottom: 20px; }}
.step label, .step .label {{ display: block; font-weight: 600; margin-bottom: 8px; }}
select, input {{ width: 100%; font: inherit; padding: 12px; border-radius: 10px;
  border: 1px solid #d6d6d6; background: #fff; color: #1b1b1b; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.chip {{ border: 1px solid #d6d6d6; background: #fff; color: #1b1b1b; border-radius: 999px;
  padding: 8px 14px; font: inherit; cursor: pointer; }}
.chip[aria-pressed="true"] {{ background: var(--primary); color: #fff; border-color: var(--primary); }}
.chips.days {{ flex-wrap: nowrap; overflow-x: auto; padding-bottom: 6px; }}
.chips.days .chip {{ flex: 0 0 auto; text-align: center; line-height: 1.2; }}
.chip small {{ display: block; font-size: .75rem; opacity: .8; }}
.empty {{ color: var(--muted); }}
.summary {{ background: var(--bg); border-radius: 10px; padding: 14px; margin-bottom: 16px; }}
.send {{ display: grid; gap: 10px; }}
.send .btn {{ text-align: center; }}
.btn-ghost {{ background: transparent; color: var(--primary); border: 2px solid var(--primary); }}
.note {{ color: var(--muted); font-size: .9rem; }}
.hidden {{ display: none !important; }}
.contact {{ display: grid; gap: 32px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}
.contact ul {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }}
.hours {{ border-collapse: collapse; }}
.hours th {{ text-align: left; padding: 4px 24px 4px 0; font-weight: 600; }}
.demo-ribbon {{ background: #111; color: #fff; text-align: center; font: 600 .85rem/1.4 var(--body);
  padding: 8px 16px; letter-spacing: .02em; }}
footer {{ padding: 28px 0 90px; color: var(--muted); font-size: .9rem; text-align: center; }}
.fab {{ position: fixed; left: 16px; right: 16px; bottom: 16px; text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,.25); z-index: 20; }}
@media (min-width: 720px) {{ .fab {{ display: none; }} footer {{ padding-bottom: 28px; }} }}
</style>
</head>
<body>
{demo_ribbon}
<header class="topbar"><div class="wrap">
  <a class="brand" href="#top">{name}</a>
  <a class="btn" href="#book">Book Now</a>
</div></header>

<main id="top">
<section class="hero{hero_class}"{hero_img}><div class="wrap">
  <h1>{name}</h1>
  {tagline}
  <a class="btn btn-lg" href="#book">Book Now</a>
</div></section>

{about}

<section id="services" class="wrap">
  <h2>Services &amp; prices</h2>
  <ul class="services">
{services}
  </ul>
</section>

{gallery}
{reviews}

<section id="book" class="wrap">
  <h2>Book an appointment</h2>
  <form class="book" id="booking" novalidate>
    <div class="step">
      <label for="svc">1. Service</label>
      <select id="svc" required></select>
    </div>
    <div class="step">
      <span class="label" id="day-label">2. Day</span>
      <div class="chips days" id="days" role="group" aria-labelledby="day-label"></div>
    </div>
    <div class="step">
      <span class="label" id="time-label">3. Time</span>
      <div class="chips" id="times" role="group" aria-labelledby="time-label">
        <span class="empty">Pick a day first.</span>
      </div>
    </div>
    <div class="step">
      <label for="cname">4. Your name</label>
      <input id="cname" autocomplete="name" required>
    </div>
    <div class="step">
      <label for="ccontact">Phone or email</label>
      <input id="ccontact" autocomplete="tel" required>
    </div>
    <button class="btn btn-lg" type="submit">Request booking</button>
    <p class="note" id="err" role="alert"></p>
  </form>

  <div class="book hidden" id="confirm" aria-live="polite">
    <h3>Almost done</h3>
    <div class="summary" id="summary"></div>
    <div class="send" id="send"></div>
    <p class="note">{name} will reply to confirm your appointment.</p>
    <button class="btn btn-ghost" type="button" id="back">Change details</button>
  </div>
</section>

<section id="contact" class="wrap contact">
  <div><h2>Contact</h2><ul>{contact}</ul></div>
  <div><h2>Hours</h2>{hours}</div>
</section>
</main>

<footer>&copy; <span id="yr"></span> {name}</footer>
<a class="btn btn-lg fab" href="#book">Book Now</a>

<script id="cfg" type="application/json">{config}</script>
<script>
(function () {{
  var cfg = JSON.parse(document.getElementById("cfg").textContent);
  var KEYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
  var state = {{ svc: 0, day: null, time: null }};
  var $ = function (id) {{ return document.getElementById(id); }};
  $("yr").textContent = new Date().getFullYear();

  cfg.services.forEach(function (s, i) {{
    var o = document.createElement("option");
    o.value = i;
    o.textContent = s.name + (s.price ? " — " + s.price : "");
    $("svc").appendChild(o);
  }});

  function toMin(hhmm) {{ var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }}
  function fmt(min) {{
    var h = Math.floor(min / 60), m = min % 60, ap = h >= 12 ? "PM" : "AM";
    return ((h + 11) % 12 + 1) + ":" + (m < 10 ? "0" : "") + m + " " + ap;
  }}
  function iso(d) {{
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" +
      String(d.getDate()).padStart(2, "0");
  }}

  // Start times (minutes after midnight) for the chosen service on a day,
  // skipping anything less than 30 minutes from now.
  function slots(day) {{
    var span = cfg.hours[KEYS[new Date(day + "T00:00:00").getDay()]];
    if (!span) return [];
    var dur = cfg.services[state.svc].duration || cfg.slotMinutes;
    var now = new Date(), nowMin = now.getHours() * 60 + now.getMinutes();
    var out = [];
    for (var t = toMin(span[0]); t + dur <= toMin(span[1]); t += cfg.slotMinutes) {{
      if (day === iso(now) && t <= nowMin + 30) continue;
      out.push(t);
    }}
    return out;
  }}

  function renderDays() {{
    var box = $("days"); box.innerHTML = "";
    var today = new Date(); today.setHours(0, 0, 0, 0);
    for (var i = 0; i < cfg.daysAhead; i++) {{
      var d = new Date(today); d.setDate(today.getDate() + i);
      if (!slots(iso(d)).length) continue;
      var b = document.createElement("button");
      b.type = "button"; b.className = "chip"; b.dataset.day = iso(d);
      b.setAttribute("aria-pressed", state.day === iso(d));
      b.innerHTML = "<small>" + d.toLocaleDateString(undefined, {{ weekday: "short" }}) +
        "</small>" + d.toLocaleDateString(undefined, {{ month: "short", day: "numeric" }});
      box.appendChild(b);
    }}
    if (!box.children.length) box.innerHTML = '<span class="empty">No open days right now.</span>';
  }}

  function renderTimes() {{
    var box = $("times"); box.innerHTML = "";
    if (!state.day) {{ box.innerHTML = '<span class="empty">Pick a day first.</span>'; return; }}
    slots(state.day).forEach(function (t) {{
      var b = document.createElement("button");
      b.type = "button"; b.className = "chip"; b.dataset.time = t;
      b.setAttribute("aria-pressed", state.time === t);
      b.textContent = fmt(t);
      box.appendChild(b);
    }});
    if (!box.children.length) box.innerHTML = '<span class="empty">No times left that day.</span>';
  }}

  $("svc").addEventListener("change", function () {{
    state.svc = +this.value; state.time = null;
    if (state.day && !slots(state.day).length) state.day = null;
    renderDays(); renderTimes();
  }});
  $("days").addEventListener("click", function (e) {{
    var b = e.target.closest("[data-day]"); if (!b) return;
    state.day = b.dataset.day; state.time = null; renderDays(); renderTimes();
  }});
  $("times").addEventListener("click", function (e) {{
    var b = e.target.closest("[data-time]"); if (!b) return;
    state.time = +b.dataset.time; renderTimes();
  }});

  function message() {{
    var s = cfg.services[state.svc];
    var d = new Date(state.day + "T00:00:00").toLocaleDateString(undefined,
      {{ weekday: "long", month: "long", day: "numeric" }});
    return "Hi " + cfg.name + ", I'd like to book " + s.name + " on " + d + " at " +
      fmt(state.time) + ". Name: " + $("cname").value.trim() + ". Contact: " +
      $("ccontact").value.trim() + ".";
  }}

  function link(href, text, primary) {{
    var a = document.createElement("a");
    a.className = "btn" + (primary ? "" : " btn-ghost");
    a.href = href; a.textContent = text;
    if (/^https?:/.test(href)) {{ a.target = "_blank"; a.rel = "noopener"; }}
    return a;
  }}

  $("booking").addEventListener("submit", function (e) {{
    e.preventDefault();
    var err = "";
    if (!state.day) err = "Please pick a day.";
    else if (state.time === null) err = "Please pick a time.";
    else if (!$("cname").value.trim()) err = "Please add your name.";
    else if (!$("ccontact").value.trim()) err = "Please add a phone number or email.";
    $("err").textContent = err;
    if (err) return;

    var msg = message();
    $("summary").textContent = msg;
    var send = $("send"); send.innerHTML = "";
    if (cfg.demo) {{
      var note = document.createElement("p");
      note.className = "note";
      note.textContent = "This is a demo. On the live site, this request goes straight to " +
        cfg.name + ". To make it live, contact " + cfg.demo.by +
        (cfg.demo.contact ? " at " + cfg.demo.contact : "") + ".";
      send.appendChild(note);
      $("booking").classList.add("hidden");
      $("confirm").classList.remove("hidden");
      $("confirm").scrollIntoView({{ behavior: "smooth", block: "start" }});
      return;
    }}
    if (cfg.endpoint) {{
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn"; b.textContent = "Send booking request";
      b.addEventListener("click", function () {{
        b.disabled = true; b.textContent = "Sending…";
        fetch(cfg.endpoint, {{
          method: "POST",
          headers: {{ "Content-Type": "application/json", "Accept": "application/json" }},
          body: JSON.stringify({{ message: msg, service: cfg.services[state.svc].name,
            date: state.day, time: fmt(state.time), name: $("cname").value.trim(),
            contact: $("ccontact").value.trim() }})
        }}).then(function (r) {{
          if (!r.ok) throw new Error(r.status);
          b.textContent = "Request sent ✓";
        }}).catch(function () {{
          b.disabled = false; b.textContent = "Couldn't send — try another option below";
        }});
      }});
      send.appendChild(b);
    }}
    var primary = !cfg.endpoint;
    if (cfg.phone) {{
      var tel = cfg.phone.replace(/[^+\\d]/g, "");
      send.appendChild(link("sms:" + tel + "?&body=" + encodeURIComponent(msg), "Send by text", primary));
      primary = false;
    }}
    if (cfg.email) {{
      send.appendChild(link("mailto:" + cfg.email + "?subject=" +
        encodeURIComponent("Booking request") + "&body=" + encodeURIComponent(msg), "Send by email", primary));
      primary = false;
    }}
    if (cfg.instagram) {{
      var ig = link("https://ig.me/m/" + encodeURIComponent(cfg.instagram), "Copy & open Instagram DM", primary);
      ig.addEventListener("click", function () {{
        if (navigator.clipboard) navigator.clipboard.writeText(msg).catch(function () {{}});
      }});
      send.appendChild(ig);
    }}
    $("booking").classList.add("hidden");
    $("confirm").classList.remove("hidden");
    $("confirm").scrollIntoView({{ behavior: "smooth", block: "start" }});
  }});

  $("back").addEventListener("click", function () {{
    $("confirm").classList.add("hidden");
    $("booking").classList.remove("hidden");
  }});

  renderDays();
}})();
</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("business", type=Path, help="business JSON file")
    ap.add_argument("-o", "--out", type=Path, help="output HTML path (default: <slug>.html)")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--demo-by", metavar="NAME",
                    help="build a locked demo labelled as made by NAME; booking requests are not sent")
    ap.add_argument("--demo-contact", metavar="EMAIL", default="",
                    help="where the business replies to claim the demo")
    args = ap.parse_args()

    biz = json.loads(args.business.read_text(encoding="utf-8"))
    errors = validate(biz)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1
    if args.check:
        print(f"ok: {args.business}")
        return 0

    out = args.out or args.business.with_suffix(".html")
    demo = {"by": args.demo_by, "contact": args.demo_contact} if args.demo_by else None
    out.write_text(build(biz, demo), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
