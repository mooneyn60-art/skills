---
name: local-booking-sites
description: Build a one-page, mobile-first website with an appointment-booking flow for a local service business (barbershop, nail salon, stylist, groomer, tattoo studio, trainer) from screenshots of its Instagram or Google profile, then prepare a personalised pitch to offer it to the owner. Use when someone wants to build sites for "DM to book" businesses, turn an Instagram profile into a booking site, or run a local web-design side business with Claude.
license: Complete terms in LICENSE.txt
---

# Local Booking Sites

Many local service businesses take every booking through Instagram DMs ("DM to
book" in the bio). This skill turns their public profile into a professional,
single-file booking website in minutes, and helps the user offer it to the owner.

The workflow has four stages. Claude does stages 2 and 3; the user does stages 1
and 4, because the outreach needs a human.

1. **Find a lead** (user). On Instagram or Google Maps, look for local service
   businesses with "DM to book", "text to book" or a link-in-bio with no real
   site. Log each one: `python scripts/leads.py add "<name>" --instagram @handle --city <city>`.
2. **Extract facts** (Claude). From the user's screenshots of the profile, posts
   and tagged reviews, write `<slug>.json` in the schema in
   `references/business-schema.md`.
3. **Build the site** (Claude). Run `python scripts/build_site.py <slug>.json -o <slug>.html`,
   check it at phone width, and fix anything that looks off.
4. **Pitch it** (user). Host the file, draft the DM with
   `python scripts/leads.py dm "<name>" --link <url> --sender <name>`, edit it
   by hand, and send it from the user's own account.

## Stage 2: extracting facts

Read the screenshots carefully and copy what is there. **Do not invent any
facts.** This matters more than anything else in this skill: a site that shows
a made-up price, review or address can cost the owner customers and costs the
user the sale.

- Take the name, services, prices, hours, address, phone and handle exactly as
  shown. If a price isn't visible, leave `price` out rather than guessing.
- Quote reviews word for word, with the reviewer's first name and last initial.
  Use only real reviews: comments, tagged posts or Google reviews.
- If hours aren't shown, leave `booking.hours` out and tell the user the page
  uses a placeholder schedule of Mon–Sat, 9–5 that they must confirm.
- Pick `theme` colours and fonts that match the feel of their feed: dark and
  moody for a barber, soft and bright for a nail studio, and so on. Colours are
  a style choice, so they don't count as invented facts.
- Leave `photos` empty unless the user has image URLs they are allowed to use.
  Don't hotlink Instagram CDN URLs: they expire and they are the owner's content.
- List everything you left out or had to assume, so the user can fill the gaps.

If the user has no screenshots and only a business name, ask for them. Don't
research or fill in details from memory.

## Stage 3: building and checking

```bash
python scripts/build_site.py examples/sample-business.json --check   # validate
python scripts/build_site.py <slug>.json -o <slug>.html               # build
```

The output is one self-contained HTML file (Google Fonts is the only external
request). It has a sticky "Book Now" header, a hero, about, services and prices,
reviews, a four-step booking flow (service → day → time → name and contact),
contact details and hours, and a floating "Book Now" button on phones.

The booking flow has no server behind it. It collects a *request* and hands it
to the business by text, email or Instagram DM, or POSTs it to
`booking.endpoint` if one is set. Be upfront about this with the user. It's
good enough to show the owner and to start taking requests the same day. A
paying client should move to a real scheduler (Square Appointments, Calendly,
Booksy, Fresha and so on) so nothing gets double-booked; see
`references/business-schema.md`.

If the user wants a design beyond the template's options, edit the generated
HTML directly or write a bespoke page. Keep the same rule that every fact comes
from the screenshots.

Before handing the page over, open it at 390px wide (Playwright or a browser's
device mode), step through a booking, and confirm there's no horizontal
scrolling.

## Stage 4: outreach and pricing

Help the user write a short, personal message. Don't build a system that sends
messages automatically. Bulk or automated DMs break Instagram's terms and get
accounts restricted, and a message that obviously came from a template doesn't
get replies. One real message per business, sent by the user, is what works.

A good pitch:
- names one specific thing about their business ("your skin fades on the
  3rd post are unreal")
- names the problem: bookings get lost in DMs when they're busy
- links to the live site, clearly labelled as a free sample they can keep
- makes a clear, low-pressure offer: set it up on their own domain, connect a
  real scheduler, a one-off price, and optional monthly upkeep

On pricing, local-business sites like this usually sell for a few hundred to
about $1,500, plus an optional $25–100 a month for hosting and edits. Suggest
the user start at the lower end until they have a few testimonials. Don't
promise the user a specific income: most businesses won't reply, and a 2–5%
close rate on cold outreach is normal.

Only publish a site under the business's name after the owner has agreed.
Before that, host the sample privately (an unlisted link, or a file sent in the
DM) so it can't be mistaken for the business's official site. Remove any
sample the owner turns down.

Keep leads up to date with `leads.py status "<name>" <new|built|sent|replied|won|lost|skip>`.
Follow up once after about four days if there's no reply, then mark the lead
`lost` and move on.
