# One-time setup (owner, about 1-2 hours)

After these steps the service runs with no owner involvement (see `RUN.md`).
Never paste a key or password into chat. Keys go into environment secrets only.

## 1. Payments (Stripe, no code)
1. Create a Stripe account and complete business verification.
2. Create two **Payment Links**:
   - **AI Fact Watch: Watch**, $29.00 / month, recurring.
   - **AI Fact Watch: Emergency Fix**, $99.00, one time.
   On both, add three custom fields: `business` (text), `town` (text),
   `website` (text, optional). Turn on "Collect customer email".
   Set the after-payment message to "Thanks. Your first check arrives within the hour."
3. Turn on Stripe's customer portal (lets Watch customers cancel themselves).
4. Turn on Stripe email notifications for **successful payments** to the sender Gmail.
5. Put the two link URLs in `config.json → payment_links` and the two link ids
   (`plink_...`) in `config.json → stripe_payment_link_ids`.
6. Recommended for fully automatic refunds and cancellations: create a Stripe
   **restricted key** with Checkout Sessions read, Subscriptions write, Refunds
   write, and nothing else. Save it as environment secret `STRIPE_API_KEY`.
   Without it, payments are read from Gmail notifications and customers cancel
   through the customer portal link, but refunds cannot be issued automatically.

## 2. AI engine keys (environment secrets, not chat)
| Secret | Where | Cost |
|---|---|---|
| `SERPAPI_KEY` | serpapi.com, free plan | 250 searches/month |
| `GEMINI_API_KEY` | aistudio.google.com, API key | free tier |
| `OPENAI_API_KEY` (optional, later) | platform.openai.com | paid |

Add them as environment secrets for the scheduled agent (and as site secrets
only if the site itself ever calls them; it does not today). With no keys at
all, checks still run using the Claude web-search engine.

## 3. Site (`site/index.html`)
1. Host it (Higgsfield site with a database, or any host with a form store).
2. Create a table `check_requests` with columns: `id`, `created_at`, `email`,
   `business`, `town`, `region`, `website`, `consent` (bool), `status`
   (default `new`). Point the form's `{{FORM_ENDPOINT}}` at it.
3. Replace `{{PAYMENT_LINK_WATCH}}`, `{{PAYMENT_LINK_EMERGENCY}}`,
   `{{SUPPORT_EMAIL}}`, `{{POSTAL_ADDRESS}}` and `{{SITE_URL}}`.
4. Read and approve the copy, especially the "no guarantee" wording.

## 4. Email (Gmail)
1. A dedicated Gmail address for the service; put it in `config.json → sender.gmail`.
2. Connect it to the scheduled agent (Gmail connector) with send and label access.
3. Create labels `AIFW/free-check`, `AIFW/processed`, `AIFW/handled`.
4. A Drive folder `AIFW/` (with `reports/` inside) for report links and the run log.
5. A postal address for the email footer (`config.json → sender.postal_address`;
   a PO box works). Required by CAN-SPAM.

## 5. Approvals (one time)
- Approve emailing people **who submit the free-check form or pay** (transactional,
  they asked). This is the only email the service sends.
- Approve the refund and cancellation policy in `config.json → policy`
  (full refund within 14 days, cancel any time).
- Then set `"outbound_enabled": true` in `config.json`. Until then the agent
  runs everything but only saves Gmail drafts.

## 6. Schedule
Create one scheduled task, hourly, in a fresh session each time, with this prompt:
"Run skills/ai-fact-watch/routines/RUN.md." It needs: this repository, the
Gmail and Drive connectors, the Higgsfield connector (for `website_db`), and the
environment secrets above.

## Checklist
- [ ] Stripe account, 2 Payment Links with custom fields, customer portal, payment notifications
- [ ] `config.json` placeholders filled (`python3 scripts/ops.py preflight` shows none left)
- [ ] `SERPAPI_KEY`, `GEMINI_API_KEY` (and optionally `STRIPE_API_KEY`) as environment secrets
- [ ] Site hosted, form wired to `check_requests`, placeholders replaced, copy approved
- [ ] Sender Gmail connected, labels and Drive folder created, postal address set
- [ ] Approval to email requesters and customers; policy approved; `outbound_enabled: true`
- [ ] Hourly scheduled task created
