# site-sales: websites for local businesses

Tooling to find local businesses that have a public email or Instagram but no
website, build each one a one-page mobile preview from **public facts only**,
and prepare (not send) a compliant offer. Status: **preparation only. Nothing
has been sent, drafted in Gmail, or charged.**

Adapted from the `local-booking-sites` skill (branch
`claude/tiktok-automation-full-scale-8jisnq`): same escaping, "no invented
facts" rule and JSON-driven template, extended with placeholders, required
sources, a map link and a preview/final mode.

## Layout

```
site-sales/
  README.md                 this file
  OFFER.md                  what the business gets ($149 + optional $19/mo)
  references/business-schema.md   business JSON format
  scripts/build_site.py     business.json -> index.html
  scripts/shot.py           390px Playwright screenshots (+ overflow check)
  scripts/dedupe.py         validate + de-duplicate data/leads.csv
  data/leads.csv            lead list
  sites/<slug>/             business.json, index.html, shot-390*.png
  templates/first_email.txt, followup.txt, faq.md
```

## Pipeline

1. **Find leads.** Look for businesses with a public business email or
   Instagram and no website (city/market vendor directories, chamber listings,
   local news, Instagram bios). Confirm there is no site: check the listing's
   website field, the Instagram bio link, and a search for the name. Add a row
   to `data/leads.csv` with the `source_url`, then run
   `python scripts/dedupe.py`.
   Columns: `business, category, town, state, public_email, phone, instagram,
   website_status, source_url, found_at, status`.
   Statuses: `new, researched, preview_built, approved_to_contact, contacted,
   followed_up, replied, won, lost, opted_out, skip`.
2. **Write facts.** Create `sites/<slug>/business.json`
   (`references/business-schema.md`). Copy only what the sources say; every
   source URL goes in `sources`. Unknowns become
   `{"placeholder": "..."}` and render with a dashed "Placeholder:" outline.
3. **Build.** `python scripts/build_site.py sites/<slug>/business.json --check`
   (lists placeholders), then without `--check` to write `index.html`. Preview
   mode is the default: "not the official site" banner, `noindex`, and a
   source list in the footer.
4. **Check on a phone width.** `python scripts/shot.py sites/<slug>/index.html --fold`
   writes `shot-390.png` (full page) and `shot-390-fold.png` (first screen) and
   warns on horizontal overflow. Look at both images and fix anything ugly.
   It uses the existing Chromium (`PW_CHROMIUM` or `/opt/pw-browsers/chromium`);
   never run `playwright install`.
5. **Outreach (blocked until the approvals below).** Fill
   `templates/first_email.txt` by hand per lead, one message at a time, with
   one follow-up at most (`templates/followup.txt`). Answer replies from
   `templates/faq.md`. Update `status` in `leads.csv` after every step;
   `opted_out` is permanent.
6. **After payment.** Apply the owner's corrections, remove every placeholder,
   rebuild with `--final`, and publish to the host they chose.

## Before any outreach: owner approvals and config still required

None of these are set. Do not send anything until **all** are done:

| Item | Needed for | Where it goes |
| --- | --- | --- |
| Sender name + sending address (a real mailbox you control, accurate From/Reply-To) | CAN-SPAM accurate header info | `{{SENDER_NAME}}`, `{{SENDER_EMAIL}}`, `{{SENDER_BUSINESS_NAME}}` |
| Valid physical postal address (street, P.O. box, or registered private mailbox) | CAN-SPAM requirement | `{{POSTAL_ADDRESS}}` |
| Opt-out route that works for at least 30 days, honoured within 10 business days, plus a suppression list | CAN-SPAM opt-out | `{{OPT_OUT_EMAIL}}`; mark `opted_out` in `leads.csv` |
| Payment link ($149 one-time; separate $19/mo subscription if offered) | Taking payment | `{{PAYMENT_LINK}}` |
| Refund policy | FAQ | `{{REFUND_POLICY}}` |
| Host for private, unlisted previews (e.g. unguessable URLs, `noindex`), and a way to delete them | `{{PREVIEW_URL}}` | one URL per `sites/<slug>/index.html` |
| **Explicit owner approval to send**, per batch, after reviewing each filled email | Any email at all | record by setting `status=approved_to_contact` |

Also decide: who does the monthly updates, how domains are handled, and
whether the leads below (found via a city vendor directory, where emails are
published for customers) are acceptable to contact. Some listing emails look
personal rather than business-branded (see notes below); skipping those is the
cautious choice.

## Rules this tooling keeps

- No invented facts, reviews, testimonials, photos, prices or urgency.
- No income or results guarantees (see `OFFER.md`).
- Previews are labelled drafts and never published as the business's site.
- One personal message per business, sent by a human; no bulk sending,
  scraping-then-blasting, or tracking pixels. Subject lines say
  "(advertisement)" and are not disguised as replies.

## Current leads (researched 2026-10-15)

All five are vendors in the City of Bloomington, IN farmers' market vendor
directory, which lists their email and no website. The emails on those pages
are hidden from simple scrapers but shown to every visitor. Market hours come
from the city's market page. Listing text for some vendors was last updated in
2025, and all five still appear in the 2026 directory.

| Slug | Business | Town | Contact | Notes |
| --- | --- | --- | --- | --- |
| littlest-bird-farm | Littlest Bird Farm | Bloomington, IN | email + Instagram | Instagram bio checked: no link. |
| moon-valley-farm | Moon Valley Farm | sells at Bloomington market | email + Facebook | Farm location not public. |
| old-post-gardens | Old Post Gardens | sells at Bloomington market | email + Facebook | "15 years" is from a 2025 listing. Tuesday hours are a placeholder. |
| poseys-and-pumpkins | Poseys and Pumpkins | North Vernon, IN | email (msn) + Facebook | Greenhouse size differs between sources; the page uses the city's "over an acre". |
| poole-mill-produce | Poole Mill Produce | sells at Bloomington market | email (looks personal) | Sells through the Market Wagon marketplace, but has no website of its own. |

Rejected during research: Risin' Creek Creamery has its own website
(risincreek.com).
