# Car Sales CRM — Dashboard

A local web dashboard for the `car-sales-crm` skill. It reads and writes the
exact same files Claude uses (`../customers`, `../calendar/appointments`,
`../vehicle-specs`), so anything you do here shows up next time you talk to
Claude, and anything Claude files from a photo shows up here.

It runs entirely on your own computer — nothing is uploaded anywhere.

## 1. Run the dashboard

```bash
cd skills/car-sales-crm/dashboard
pip install -r requirements.txt
python3 app.py
```

Open **http://localhost:5050** in your browser. Leave the terminal running
while you use it; close it (Ctrl+C) when you're done.

What you get:
- **Customers tab** — search/filter your list, click anyone to see their full
  history, edit status/stage/consent, log a call/text/email, add a note.
- **Agenda tab** — appointments and follow-up reminders together, overdue
  items called out, one-click "Confirm" on appointments.
- **Vehicle Specs tab** — read-only view of manual/spec sheets Claude has
  filed for you.

## 2. Get real text/email notifications on your phone

The dashboard itself only shows alerts while it's open. To actually get
pinged on your phone — even when the dashboard is closed — a separate
script, `notify.py`, needs to run on a schedule via your computer's own
scheduler (there's no cloud server here, so *something* on your machine has
to wake up and check). Two independent options, pick either or both:

### Texting (via Twilio)
1. Sign up at [twilio.com](https://www.twilio.com) (free trial includes
   credit) and get a Twilio phone number.
2. From the console, grab your **Account SID**, **Auth Token**, and your
   **Twilio phone number**.
3. `pip install twilio` (already in requirements.txt).

### Email (via Gmail)
1. Turn on 2-Step Verification on your Google account, then create an
   [App Password](https://myaccount.google.com/apppasswords).
2. That's the only credential you need — no separate signup.

### Configure

Create `notify.env` in this folder (this file is git-ignored — never commit
it):

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+15551234567
TWILIO_TO_NUMBER=+15559876543

GMAIL_ADDRESS=you@gmail.com
GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
NOTIFY_EMAIL_TO=you@gmail.com

# Optional: send a message even when nothing is due, so you know it's alive
# NOTIFY_ALWAYS=1
```

Only fill in the section(s) you want (Twilio for texts, Gmail for email, or
both). Test it manually first:

```bash
python3 notify.py
```

### Schedule it

**Mac/Linux (cron)** — run `crontab -e` and add a line. This example checks
every morning at 8am and every hour from 9-6:

```
0 8 * * * cd /full/path/to/skills/car-sales-crm/dashboard && /usr/bin/python3 notify.py >> notify.log 2>&1
0 9-18 * * * cd /full/path/to/skills/car-sales-crm/dashboard && /usr/bin/python3 notify.py >> notify.log 2>&1
```

**Windows (Task Scheduler)** — create a Basic Task, trigger "Daily" (repeat
every hour if you want more frequent checks), action "Start a program":
`python.exe` with argument `notify.py` and "Start in"
`C:\full\path\to\skills\car-sales-crm\dashboard`.

Your computer needs to be on and awake at the scheduled time for this to
fire — it's a local script, not a cloud service.

## Notes

- Photo intake (worksheets, manuals) still happens by sending Claude a
  photo in a chat, not through this dashboard — that's where the actual
  reading of the image happens. The dashboard is for browsing, editing, and
  getting nudged; Claude is for filing new information from a picture.
- All customer/appointment data stays in plain Markdown files on your
  machine and is git-ignored — it's never pushed to GitHub.
