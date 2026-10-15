# AI Fact Watch: the scheduled run (zero human steps)

This file is the complete instruction set for the scheduled agent. After the
one-time setup in `SETUP.md`, nothing here needs the owner: requests come in
through the site, checks run, reports go out, payments start service,
cancellations and refunds follow the written policy.

Work from `skills/ai-fact-watch/`. All scripts are in `scripts/`.

## Hard rules (every run)
1. **Inbound only.** Email only people who (a) submitted the free-check form,
   (b) paid, or (c) wrote to us. Never contact a business that did not ask,
   even if its errors are public. No cold email, no DMs, no calls.
2. **Outbound gate.** Run `python3 scripts/ops.py preflight` first. If
   `outbound_allowed` is false, do all the work but save Gmail **drafts** only
   and send nothing, and do not issue refunds. Outbound turns on only when the
   owner has filled `config.json` and set `"outbound_enabled": true`.
3. **Never promise** that Google, OpenAI or any vendor will change an answer.
   Use only the wording in `templates/emails.md`.
4. **Never paste or print secrets.** Keys come from environment secrets.
5. **Limits:** `config.json → limits`. Overflow free checks wait for the next day.
6. **Privacy:** never name a customer or their results anywhere public.
7. Before any send, re-read the quotes going in the email against
   `answers/<slug>/<date>.json` (they must be verbatim) and check the business
   name, town and recipient match the request.

## Schedule
| Cadence | Job |
|---|---|
| Hourly | A. intake, B. free checks, C. payments, D. inbox |
| Daily 07:00 local | E. Emergency re-checks + Emergency Kit deliveries |
| Weekly Mon 07:00 | F. Watch re-checks; monthly summary on the first Monday |

`ops.py due` returns everything due right now, so one hourly run can do A-F;
the schedule only bounds how often re-checks fire.

## A. Intake (hourly)
1. Read new rows from the site's `check_requests` table (Higgsfield
   `website_db`, query rows with `status = 'new'`).
2. For each row: `python3 scripts/ops.py add-request --email ... --business ...
   --town ... --region ... --website ... --ref <row id>`.
3. Mark the row `queued` in `website_db` (or `rejected` with the reason the
   script gave: duplicate, already used, opted out). Rejected requests get no email.

## B. Free checks (hourly)
For each `free_check` item from `python3 scripts/ops.py due`:
1. **Truth:** `python3 scripts/truth.py --name "<business>" --town "<town>"
   --region <ST> --website <url> --slug <slug>`. Add `--listing` / `--social`
   URLs found with WebSearch ("<business> <town>"): Google Maps, Yelp, Facebook.
   If two businesses share the name, add each as `--twin "Name|address|phone|url|note"`.
   If the site is unreachable after 3 tries: `ops.py fail` and on the third
   failure send `free-check-failed`.
2. **Ask the AI engines:** `python3 scripts/ask_ai.py --slug <slug>`. It uses
   every provider whose key is set (SerpApi Google AI Overview, Gemini, OpenAI)
   and skips the rest cleanly.
3. **Claude web-search check (always, and the only engine when no keys are set):**
   - `python3 scripts/ask_ai.py --slug <slug> --print-queries`
   - Run each query with the WebSearch tool. Copy the answer text **verbatim**
     and the URLs it cites. Do not summarize or fix it.
   - Write them to `answers/<slug>/<date>.claude-websearch.import.json`
     (format in the `ask_ai.py` docstring) with `observed_at` set to now (UTC),
     then `python3 scripts/ask_ai.py --slug <slug> --import <that file>`.
   - Label this engine "Claude web search" in emails. Never call it Google's answer.
4. **Compare:** `python3 scripts/compare.py --slug <slug>`.
5. **Read the findings yourself.** For each red or yellow finding, open the quote
   in the answers file and confirm it says what the title says. Delete false
   positives by editing the findings JSON (keep a `"dismissed_reason"`) and re-run step 6.
6. **Report:** `python3 scripts/report.py --slug <slug> --out reports/<slug>/<date>/`.
7. **Deliver:** reply to the requester with `free-check-report` (or
   `free-check-clean` when the score is 80+ and nothing is red), PDF attached.
   If the Gmail tool cannot attach files, upload the PDF to the Drive folder
   `AIFW/reports/` and share it view-only with the requester's email, then link it.
   Label the thread `AIFW/free-check`.
8. `python3 scripts/ops.py done --id <req id> --score <score> --report <pdf path>`.
   Update the `website_db` row to `sent`.

## C. Payments (hourly)
1. If `STRIPE_API_KEY` is set: `python3 scripts/ops.py stripe-sync`. It
   activates every completed checkout from the two Payment Links (plan chosen by
   payment link id, then by amount) using the custom fields business/town/website.
2. Otherwise read Gmail for Stripe "payment received" notifications (search
   `from:stripe.com newer_than:2d -label:AIFW/processed`). Accept only messages
   from a stripe.com sender with a passing signature. Save the body to a temp file,
   `python3 scripts/ops.py parse-payment --file <tmp>`, then
   `ops.py activate --email <customer_email> --plan <plan> --ref <ref>`.
   Label the email `AIFW/processed`.
3. New `active` customers: run B steps 1-6 right away (Watch) or the full
   Emergency flow (E). Send `welcome-watch` or `emergency-kit`.
   `needs_details` customers get `needs-details`; activation completes when they reply.

## D. Inbox (hourly)
Search Gmail `to:<sender> is:unread -from:stripe.com newer_than:7d`. For each
message from a requester or customer:
1. Save the body, `python3 scripts/ops.py classify --file <tmp>`, and follow the
   returned `action`:
   - **cancel** → `ops.py cancel --email ...`; cancel the Stripe subscription via
     API when `STRIPE_API_KEY` is set (`DELETE /v1/subscriptions/<sub_ref>`), else
     send `cancel-self-serve`. Then send `cancelled`.
   - **refund** → `ops.py refund-decision --email ...`. If `full_refund` and
     `STRIPE_API_KEY` is set, create the refund (`POST /v1/refunds` with the
     checkout session's payment_intent), `ops.py mark-refunded`, cancel, send
     `refund-approved`. Otherwise send the template the decision names.
   - **legal** → full refund + cancel + `ops.py optout`, send `legal`, then no
     further contact. Do not argue or explain.
   - **angry** → send `sorry` (offers a refund).
   - **STOP / unsubscribe** → `ops.py optout` and cancel; no reply needed.
   - **question** → answer only from the FAQ in `templates/emails.md`; otherwise
     `faq-fallback`.
   - Replies to `needs-details` that contain business/town/website →
     update the customer (activate again with those fields) and run its first check.
2. Label handled threads `AIFW/handled`. The policy in `config.json → policy`
   decides every refund; there is no owner escalation.

## E. Emergency (daily) and F. Watch (weekly)
For each `emergency_kit`, `emergency_recheck` or `watch_recheck` item from `ops.py due`:
1. Re-run B steps 2-6 for its slug (truth only weekly, or when the site changed).
2. `compare.py` reports `changes.new` / `changes.resolved` against the previous run.
3. Send: `emergency-kit` (first time, with `fix-kit/` files and the report),
   `watch-alert` when anything new is red or yellow, `emergency-daily` for
   Emergency customers, `weekly-ok` for Watch with no change. On the first Monday
   of the month also attach the month's reports as the monthly summary.
4. `python3 scripts/ops.py done --id <cus id> --score <score> --report <pdf> [--kit]`.
   Emergency customers complete automatically after 30 days.

## End of every run
- `python3 scripts/ops.py status` and append one line to the Drive file
  `AIFW/run-log` (counts only, no customer names).
- If any step failed three runs in a row (see `data/events.jsonl`), add a line to
  the run log; the service keeps running for everyone else.

## Engines and what each costs
| Engine | Needs | Free tier |
|---|---|---|
| Claude web search | nothing (session WebSearch) | included |
| Google AI Overview | `SERPAPI_KEY` | 250 searches/month (6 per check) |
| Gemini + Google Search grounding | `GEMINI_API_KEY` | free tier |
| ChatGPT web search | `OPENAI_API_KEY` | paid; add after MRR > $200 |
