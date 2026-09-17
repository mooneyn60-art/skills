---
name: car-sales-crm
description: A personal, lightweight CRM for a car salesperson, built entirely out of plain files instead of a dealership CRM platform. Use this skill whenever the user wants to add or update a customer (including by uploading a photo of a paper worksheet, sign-in sheet, deal jacket, or vehicle manual/spec sheet), asks who they need to call/email/text today, asks for follow-up reminders, wants a message drafted (call talking points, email, or text) for a specific customer, wants sales tips to keep a lead engaged, or wants to review/search their customer list. Trigger on phrases like "my customers", "follow up", "who do I need to call", "add this customer", "log this deal sheet", "CRM", or a photo of a handwritten worksheet.
---

# Car Sales CRM

A one-person CRM that lives in plain Markdown files instead of a bloated dealership platform (VinSolutions, DealerSocket, etc.). Every customer is one file. There is no database, login, or app to fight with — just this skill reading and writing files, plus a small script for the daily follow-up list.

Everything under `customers/` and `vehicle-specs/` is real customer data and is git-ignored (see `.gitignore`) — it stays on the user's machine/session and is never committed to this repo. Do not remove those ignore rules.

## Setup (first run only)

If `customers/` or `vehicle-specs/` don't exist yet under this skill's folder, create them. They start empty — do not invent sample customers.

## Core concept: one file per customer

Each customer is a Markdown file at `customers/<first-last>.md` (slugified, e.g. `customers/john-smith.md`), built from `templates/customer-record.md`. It has YAML front matter for structured fields (used for sorting/filtering and the digest script) and a running, dated notes log underneath. Never delete a customer's existing notes — this file is their whole history. Always append.

Matching an existing customer: match on name + phone/email, not name alone (two "Mike"s are common). If genuinely ambiguous, ask which customer before writing.

## Adding/updating a customer from a photo

The user will often just hand you a photo — a paper sign-in sheet, a deal worksheet, a trade-in appraisal, a handwritten note, or a page from a vehicle's owner's manual/spec sheet. Read the image directly (you can read images natively; don't ask the user to transcribe it).

1. **Identify what kind of photo it is:**
   - Customer worksheet / sign-in sheet / deal jacket / handwritten note → it's about a customer.
   - Owner's manual page / window sticker / spec sheet for a vehicle → it's vehicle reference info, not tied to one customer unless it's clearly attached to their deal.

2. **For a customer photo:**
   - Extract whatever is legible: name, phone, email, vehicle they're interested in (or trading in), budget/payment target, trade-in details, financing notes, stated timeline, objections, and anything handwritten in the margins.
   - Find or create their file (see naming above). Fill in/update the front-matter fields you now know (never blank out a field you don't have new info for).
   - Append a dated entry under `## Notes` summarizing what the photo showed, tagged `(from photo)`. Quote or closely paraphrase handwritten remarks — those are often the most useful part ("wife wants 3rd row", "needs to stay under $650/mo").
   - If the photo implies next steps (e.g. "call back Thursday with numbers"), set `next_followup` and `next_followup_channel` accordingly, and say so back to the user.
   - Tell the user in one line what you filed and where (new file vs. updated existing).

3. **For a vehicle manual/spec photo:**
   - File it under `vehicle-specs/<year-make-model>.md` (create from `templates/vehicle-spec.md` if new) — a shared reference, not a customer file.
   - If the user was clearly showing you this because of a specific customer's deal, also add a short note to that customer's file referencing the spec (e.g. "confirmed tow capacity for their trade question").

## Manual add/update (no photo)

Same file-per-customer model. Ask only for what's missing to file something useful (name + one contact method + what they're interested in is enough to start); don't interrogate the user for a full intake before creating the record.

## Follow-up cadence

When you set `next_followup` after any contact or new lead, use this default cadence unless the user gives a different date:

- **status: hot** (actively deciding, was just in / just talked numbers) → next business day
- **status: warm** (engaged, not urgent) → 3–4 days out
- **status: cold** (early / browsing / went quiet) → 7–14 days out
- **status: sold** or **status: lost** → no follow-up needed; leave `next_followup` blank

Full detail and how to move a lead between stages: `references/followup-cadence.md`.

## "Who do I need to follow up with today?"

Run `scripts/daily_digest.py` (reads every file in `customers/`, no arguments needed) to get the due/overdue list sorted by urgency. Then, for each customer on it, don't just read the list back — give the user something they can act on immediately:

- The channel to use (`next_followup_channel` — call, email, or text), or your best judgment from their history if it's blank.
- One line of *why* (pull from their most recent note — what's the open thread?).
- A ready-to-use message: a short set of talking points for a call, or an actual drafted text/email they can copy-paste. Keep texts short and casual; emails a bit more complete but still brief — nobody reads a long email from a salesperson.
- One tip from `references/followup-tips.md` matched to their stage/situation to help keep them engaged (create urgency, add value, handle their stated objection, etc.) — don't just repeat the same tip for everyone.

After the user acts on a follow-up (or tells you they did), update that customer's file: append the note, update `last_contact`/`last_contact_channel`, and set the new `next_followup` per the cadence above.

## Searching / reviewing customers

For "show me my hot leads", "who hasn't been contacted in 2 weeks", etc., read the relevant files under `customers/` (grep the front matter) rather than asking the user to remember details — that's the point of the system.

## Style

Keep customer files terse and scannable — a busy salesperson skims these between calls. Bullet notes, not paragraphs. No filler. When drafting messages, sound like a person, not a dealership auto-reply.
