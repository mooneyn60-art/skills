# Email templates

Every email we send is one of these. Fill `{placeholders}` from the request,
customer record, findings file and `config.json`. Do not improvise new claims.
All emails are transactional replies to someone who asked (submitted a free
check, paid, or wrote to us). Never email anyone else.

Every email ends with this footer:

```
--
AI Fact Watch · {postal_address}
You are getting this because you {reason: requested a free check | subscribed}. Reply STOP and we will not email you again.
We document what AI tools say and give you corrected sources. We cannot make Google or any AI company change an answer.
```

## free-check-report
Subject: What AI says about {business}: {score}/100 ({n_red} to fix)

Hi,

You asked us to check what AI answers say about {business} in {town}. The full
report is attached (PDF) and online at {report_url}.

Today's check ({date}, engines: {engines}):
{top_findings: up to 3 lines, "- {title}: AI said \"{short quote}\" - true: {true_value}"}

What AI got right: {right_summary or "nothing we could confirm yet"}.

The report includes a free starter Fix Kit: a structured-data block for your
website and the exact Google Business Profile edits.

If you want us to keep watching:
- Watch, $29/month: weekly re-check of every engine, same-day alert if a fact flips, full Fix Kit. {payment_link_watch}
- Emergency Fix, $99 once: for "closed", fake deal or false lawsuit errors right now. Full Fix Kit within 48 hours, daily re-checks for 30 days, a dated evidence log. {payment_link_emergency}

Refunds: full refund within 14 days, no questions.

## free-check-clean
Subject: What AI says about {business}: {score}/100, looking good

(Same as free-check-report, but lead with "We found no wrong facts today." and
offer Watch only: "AI answers change week to week; Watch catches it the day it happens.")

## free-check-failed
Subject: We couldn't finish the check for {business}

We couldn't read {website} (or find the business) after three tries. Reply with
the correct website or Google Maps link and we will run it again.

## needs-details
Subject: Thanks - which business should we watch?

Thanks for subscribing. Reply with the business name, town and website so we can
start. Your first check runs within an hour of your reply.

## welcome-watch
Subject: Watch is on for {business}

Your first full check is attached. We re-check every {recheck_days} days and
email you the same day if anything changes. Your Fix Kit files are attached
(README.md says what to do first). Reply "cancel" any time.

## emergency-kit
Subject: Your Emergency Fix Kit for {business}

Attached: the full Fix Kit and the evidence log so far. Do steps 1-4 in
README.md today; they matter most. We re-check every day for 30 days (until
{ends_at}) and email you each day something changes, plus a summary every Monday.

## watch-alert
Subject: Alert: AI now says something new about {business}

On {date} {engine} said: "{quote}". The truth: {true_value} (source: {true_source}).
What to do: {fix_steps for this finding}. Pre-written feedback text is in the
attached report. Full evidence log attached.

## weekly-ok
Subject: {business}: no changes this week ({score}/100)

No new errors this week. Still open from before: {open_findings or "none"}.

## emergency-daily
Subject: Day {n} of 30 for {business}: {changed_or_unchanged}

{if changed: list new / resolved findings with quotes and dates}
{if unchanged: "No change since yesterday. Still showing: {open_findings}."}

## cancelled
Subject: Cancelled - {business}

Done. {if watch: "You keep Watch until {service_until}; you won't be charged again."}
{if emergency: "Daily re-checks have stopped."} Your reports stay yours.

## cancel-self-serve
Subject: Cancelling - one click

Use this link to cancel: {stripe_customer_portal_url}. Reply if it doesn't work
and we will cancel it for you.

## refund-approved
Subject: Refund issued

We refunded {amount} to your card (Stripe reference {refund_ref}). Banks take
5-10 days to show it. Your service is stopped. Sorry it wasn't a fit.

## refund-outside-window
Subject: About your refund request

Our policy is a full refund within 14 days of payment. Your payment was
{days} days ago, so we have cancelled the renewal instead: you won't be charged
again and you keep access until {service_until}.

## refund-not-found
Subject: About your refund request

We can't find a payment from this address. Reply with the email you paid with
or the Stripe receipt number and we will sort it out the same day.

## legal
Subject: Your message

Thank you. We have stopped the service, refunded your payment in full
({refund_ref}) and will not contact you again.

## sorry
Subject: Sorry about that

Sorry - that is not the experience we want. If it helps, we can refund you in
full right now; reply "refund" and it is done. {answer to any concrete problem
from the FAQ below, if one applies}

## faq-fallback
Subject: Re: {subject}

Thanks for the question. Here is what we can say: {closest FAQ answer}. If that
doesn't cover it, reply "refund" for a full refund within 14 days, or "cancel".

## FAQ (only answer from this list)
- **Can you get Google to fix it?** No one can promise that. We give you the
  corrected sources Google reads, the exact feedback to submit, and a dated
  evidence log. Many errors clear within days or weeks once sources agree; some don't.
- **Which AI tools?** Google AI Overviews, Gemini, ChatGPT (as configured) and a
  web-grounded Claude check. The report lists exactly which ran.
- **Do you need my passwords?** No. We never log in to your accounts. You (or
  your web person) paste the Fix Kit in.
- **Will you post anything for me?** No. Everything is ready to paste.
- **Contract?** No. Watch is month to month; cancel by replying "cancel".
- **Results vary?** Yes. AI answers change by location, account and day. We
  record the date and engine for every quote.
- **Lawsuit or defamation?** We are not lawyers. The evidence log is yours to
  give to one.
