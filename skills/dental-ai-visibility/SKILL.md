---
name: dental-ai-visibility
description: Run an automated "AI search visibility" service for local dental practices - find independent dentists in a city, score their websites on the signals AI assistants use to recommend local businesses, email them a free audit, handle replies, and deliver monthly fixes to paying clients. Use when running or changing the daily routine, auditing a practice, or answering a prospect's question.
---

# Dental AI Visibility

A one-person service business run by scheduled Claude sessions. Patients
increasingly ask ChatGPT, Gemini and Google's AI answers for a dentist. Those
tools pull from a practice's website and listings. Most independent practices
have never optimised for this. We audit them free, then fix it monthly.

## Offer
- **Free:** an audit email with a 0-100 score and the top three gaps.
- **Paid, ${price_per_month_usd}/month, cancel any time:** Dentist structured
  data, an FAQ page, service page copy, 4 Google Business Profile posts, review
  replies, and a monthly score report. Everything is delivered ready to paste.
  If the practice gives us manager access to their Google Business Profile,
  we post for them.
- No guarantees of rankings or patients. We improve the signals AI tools use.

## Files
- `config.json` - city, sender identity, payment link, daily limits. Outreach
  stays off until the required fields are set.
- `scripts/audit.py` - deterministic website check, prints score + fixes + emails.
- `scripts/leads.py` - pipeline CSV in `data/leads.csv`, opt-outs in `data/optout.txt`.
- `templates/emails.md` - every email we send.
- `routines/DAILY_RUN.md` - the scheduled routine; it is the full instruction set.
- `reports/<slug>/` - monthly client deliverables.

## Answers for prospects (only say what is here)
- Contract? No, month to month.
- What do you need from us? Who updates your website; optionally Google
  Business Profile manager access.
- Do you touch our site? No, we hand your web person ready-made code and copy,
  unless you ask us to.
- Results? We report your score monthly; we don't promise rankings.

## Compliance
US CAN-SPAM: true sender and subject, postal address and an unsubscribe line in
every outreach email, opt-outs honoured immediately and permanently. Business
addresses only, one recipient per email, at most two touches.
