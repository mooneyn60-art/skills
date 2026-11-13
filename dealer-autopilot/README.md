# Dealer Autopilot

A follow-up system for one car salesperson, built to the brief in
`skills/carsales-followup/BRIEF.md` (branch `claude/package-installation-setup-yv4j79`).
Nothing slips through the cracks, and you step in only for real conversations.

**DealerSocket stays your system of record.** Export your leads and customers from it, import them here,
and this runs your daily follow-up list on top.

## What it does

| Screen | What it's for |
|---|---|
| **Today** | Your morning list: *call these* (replies first, then appointment checks, then follow-up calls) and *approve these* (texts and emails drafted in your voice, ready to send with one tap). |
| **Customers** | Your buckets: **Follow Up** (internet lead, phone-up, be-back, appointment), **Sold**, **Outreach** (lost or bought elsewhere), and **Do not contact**. Each customer has their stock numbers, consent record, history, and one-tap buttons: *They replied*, *Book appointment*, *Mark sold*, *Do not contact*. |
| **Calendar** | Appointments. Booking drafts a confirmation text and queues reminders for the day before and 2 hours before. 30 minutes after the start time it asks you "did they show?". A no-show gets a "sorry we missed you" text drafted. |
| **Stock #s** | Every stock number, and who's interested in each one. |
| **Templates** | Every message for every stage, written friendly-professional. You approve each one once. |
| **Grow** | Your lead page and QR code, upgrade and reactivation campaigns, new-arrival matches, referrals and birthdays (see below). |
| **Scoreboard** | Weekly: response time to new leads (target under 5 min), appointment rate, show rate, close rate, and which messages get replies. |
| **Import** | Paste or upload a DealerSocket export (customers) or your inventory list. |
| **Ask TARS** | Ask anything: "who wants stock 24518?", "book Mike for Saturday at 11", "how's my show rate?" |

## Getting more customers (Grow tab)

- **Your lead page** (`/me`) with a **QR code** for business cards and social posts. Shoppers enter their info and tick a proper
  consent box, and they can save your contact card. The lead lands at the **top of Today with a 5-minute clock**, and you get an email alert once email is set up.
- **New-arrival matching.** Add a vehicle and everyone who asked about that model gets a "just came in, want photos?" text drafted.
  Mark a car sold and everyone who liked it gets a "that one sold, want me to find something similar?" text.
- **Upgrade campaign.** Past buyers at the 2–4 year mark get the "your car may be worth more than you owe" message. This is where repeat sales come from.
- **Reactivation campaign.** Leads with no contact in 60+ days get one friendly check-in.
  Campaigns are spread across days (10 a day by default), so your list never floods.
- **Referrals.** Fill in "Referred by"; when that customer buys, you get a task to thank the person who sent them.
- **Birthdays.** Add one (MM-DD) and a birthday text is drafted on the day.
- **Imported history is handled.** Old leads and past buyers pick up their schedule where it would be today, so nobody gets a
  "thanks for reaching out!" weeks late.

All of these follow the same rules: only consented customers get texts, everyone else becomes a call task, and nothing sends without you.

## Compliance is built in (Rule 0)

- **Consent:** no text or email goes to anyone without recorded consent (when and how). Instead you get a "call and ask" task.
- **STOP:** marking a customer *Do not contact* (or a STOP reply on a business number) cancels everything, permanently.
- **8 am to 9 pm:** texts can't be sent outside this window. You can narrow it but not widen it.
- **Do Not Call registry:** numbers flagged as on the registry are blocked unless the customer contacted the dealership first.
- **Email:** every email has an unsubscribe link and your dealership address.
- **Data:** only names, contact info, vehicle, stage and notes. No credit, SSN, licence or income fields.
- **Any reply stops the automation** and puts the customer at the top of your call list.
- **Nothing sends on its own** unless you approved that template, turned on automation, and it's a **Sold** or **appointment** message going to a consented customer.

Texts go from **your own phone**: tap *Send text* and your Messages app opens with the text filled in.
Replies come back to your phone, so tap **They replied** on the customer to stop their automation.
(Optional later: a registered Twilio number sends and receives automatically.)

## Setup (about 10 minutes)

Needs [Node.js](https://nodejs.org) 22.13 or newer.

```bash
cd dealer-autopilot
```

```bash
npm install
```

```bash
cp .env.example .env
```

Edit `.env`: set `APP_PASSWORD`, plus your Gmail address and a Gmail App Password for email.

```bash
npm start
```

Open http://localhost:3000. In **Settings**, add your name, dealership, dealership address and review link.
Then **Import** your DealerSocket export and open **Today**.

To try it with demo data first, run `npm run seed`, then `DB_PATH=data/demo.db npm start`.

### Using it from your phone

Run it somewhere your phone can reach: a small always-on computer at home, or a host such as Render or Railway.
Set `PUBLIC_URL` to that address and always set `APP_PASSWORD`. On your phone, open the address and use
*Add to Home Screen*.

## Run it from Claude (MCP)

Every TARS action is also an MCP tool, so you can do all of this by talking to Claude:
"what's on my list today", "import this list as internet leads", "Sara bought the RAV4".

- **claude.ai / Claude app:** Settings → Connectors → *Add custom connector*, then paste the MCP URL shown on this app's
  **Settings** page. It needs the public address, and the URL works like a password, so keep it private.
- **Claude Desktop / Claude Code on the same computer:**

  ```bash
  claude mcp add dealer-autopilot -- node /full/path/to/dealer-autopilot/src/mcp-stdio.js
  ```

  The Claude Desktop config is shown in Settings.

Keep `npm start` running either way: it's what builds the daily list and sends approved automations every minute.
If you've also connected Gmail or Google Calendar to Claude, Claude can use them alongside this.

## Calendar on your phone

Settings shows a private calendar link. Subscribe to it in Google Calendar (*Other calendars → From URL*) or on
iPhone (*Settings → Calendar → Accounts → Add Subscribed Calendar*).

## Build plan from the brief

1. **Week 1:** the table and the daily list, with nothing automatic. This is the default: automation is off.
2. **Week 2:** go through **Templates** and approve each message. Edit any wording that doesn't sound like you.
3. **Week 3:** turn on automation for Sold-stage and appointment messages only (Templates → *Automation on*, then tick *Send automatically* per template).
4. **Week 4:** check the **Scoreboard** weekly, and change one thing a week.

## Files

- `src/sequences.js`: stages and default templates
- `src/queue.js`: the daily list, sending, and stop-on-reply
- `src/appointments.js`: booking, reminders, show/no-show, calendar feed
- `src/scoreboard.js`: the weekly numbers
- `src/tars.js`: the assistant and its tools; `src/mcp.js` exposes the same tools over MCP
- `data/dealer.db`: your data (SQLite). Back it up, and don't commit it.
