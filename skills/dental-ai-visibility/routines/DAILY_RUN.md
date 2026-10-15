# Daily run (weekdays)

This is the complete instruction set for the scheduled daily session. Work from
`skills/dental-ai-visibility/` on branch `claude/dental-ai-visibility`.

## 0. Sync and read state
1. `git fetch origin claude/dental-ai-visibility && git checkout claude/dental-ai-visibility && git pull`.
2. Read `config.json`, `SKILL.md`, `templates/emails.md`.
3. `python scripts/leads.py stats`.
4. Sending is allowed only if `send_enabled` is true AND every key in
   `required_for_sending` is non-empty. If not, skip steps 3 and 4 and say in
   the summary exactly which fields are missing.
5. If `target_city` is empty, stop and ask the owner for their city. Do nothing else.

## 1. Inbox first (replies before new outreach)
Search Gmail for replies to our threads in the last 3 days (`in:inbox newer_than:3d`).
For each reply from a lead:
- "unsubscribe", "stop", "remove", "not interested", "no" → `leads.py optout <email>`.
  Do not reply.
- Interested / "yes" / asks for details → reply with template 3 in the same
  thread, `leads.py set <name> interested`.
- A question → answer only from `SKILL.md` and the templates; otherwise use
  template 4 and flag it for the owner.
- Angry or legal-sounding → do not reply; opt them out and flag for the owner.
- Payment confirmations (Stripe or similar) → mark that lead `client`, then run
  the onboarding deliverable (section 5) for them today.
Never store reply text in the repo.

## 2. Find new leads (`new_leads_per_day`)
Use web search for "dentist {target_city} {target_state}", "family dentistry
{target_city}", "dental implants {target_city}", and neighbourhood variants.
Skip chains/DSOs (Aspen, Western Dental, Coast, Heartland, etc.), skip anything
already in `leads.csv`. For each new independent practice:
- `python scripts/audit.py <website> --city "<target_city>" --json`
- If unreachable, `leads.py add` then `set ... skip --note unreachable`.
- Find a contact email: the audit's `emails`, else the site's contact page.
  Use only an address the practice publishes. Never guess (no info@ guessing).
  No published email → status `skip`, note "no email".
- `leads.py add`, then `leads.py set <name> audited --score <score> --email <email>`.
- Practices scoring 85+ are already in good shape: mark `skip`, note "strong site".

## 3. Follow-ups (sending must be enabled)
For each row from `leads.py due`: run `leads.py can-email`, send template 2 as a
reply in the original Gmail thread, then `leads.py set <name> followed_up`.

## 4. First emails (sending must be enabled)
For `audited` leads, lowest score first, until today's total sends reach
`max_emails_per_day`:
- `leads.py can-email <email>` must print `yes`.
- Write template 1 from that practice's real audit. Every claim must come from
  the audit output or something you saw on their site. Read it back once.
- Send from Gmail to that one address (never CC/BCC lists).
- `leads.py set <name> emailed --note "first touch"`.

## 5. Client deliverables
For each `client` with no deliverable this month (check `reports/<slug>/`):
write `reports/<slug>/<YYYY-MM>.md` containing
1. Dentist JSON-LD for their site, built only from facts on their site.
2. An FAQ page (8-10 Q&As) using only facts on their site; mark anything the
   practice must confirm (prices, insurance) with `[CONFIRM]`.
3. Four Google Business Profile post drafts.
4. Replies to their most recent public Google reviews you can find, if any.
5. Re-run `audit.py` and show score then vs. now.
Email it to the client contact and note it in `leads.csv`.

## 6. Wrap up
- `git add skills/dental-ai-visibility && git commit -m "dental-ai-visibility: daily run <date>" && git push -u origin claude/dental-ai-visibility`
  (retry the push up to 4 times with backoff on network errors).
- Send the owner a short summary (5 lines max): new leads, emails sent,
  replies, new clients, anything that needs them. If nothing needs them, say so.

## Hard rules
- Max `max_emails_per_day` sends total per day, including follow-ups.
- Two touches per practice, ever. Opt-outs are permanent.
- Never claim what ChatGPT or any AI "says" about a practice unless you
  actually ran that query today and quote it. The audit measures signals, not rankings.
- Never promise rankings, patient numbers or guaranteed results.
- Never spend money or sign up for anything.
