#!/usr/bin/env python3
"""Send a real text/email to your phone about due follow-ups and today's appointments.

This is meant to be run on a schedule by YOUR computer's own scheduler
(cron on Mac/Linux, Task Scheduler on Windows) — see README.md in this
folder for exact setup. It does nothing on its own; something has to run
it periodically, since this whole CRM is local (no cloud server).

Configure credentials in a `notify.env` file next to this script (never
committed — see .gitignore) or as real environment variables. Both SMS
and email are optional and independent; configure either, neither, or
both. If nothing is configured, this just prints what it would have sent.
"""
import os
import smtplib
import sys
from datetime import date, timedelta
from email.mime.text import MIMEText
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from _common import APPOINTMENTS_DIR, CUSTOMERS_DIR, parse_date, parse_front_matter  # noqa: E402

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / "notify.env"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def gather_due_items():
    today = date.today()
    lines = []

    for path in sorted(CUSTOMERS_DIR.glob("*.md")):
        f = parse_front_matter(path.read_text(encoding="utf-8"))
        if f.get("status") in ("sold", "lost") and not f.get("next_followup"):
            continue
        d = parse_date(f.get("next_followup", ""))
        if d is None or d > today:
            continue
        when = "today" if d == today else f"{(today - d).days}d overdue"
        channel = f.get("next_followup_channel", "").strip() or "unset channel"
        lines.append(f"- {f.get('name', path.stem)}: follow up ({when}, {channel})")

    for path in sorted(APPOINTMENTS_DIR.glob("*.md")):
        f = parse_front_matter(path.read_text(encoding="utf-8"))
        d = parse_date(f.get("date", ""))
        if d != today:
            continue
        confirmed = f.get("confirmed", "").strip().lower() == "true"
        flag = "" if confirmed else " [UNCONFIRMED]"
        time = f.get("time", "").strip()
        when = f" @ {time}" if time else ""
        lines.append(f"- {f.get('customer', path.stem)}: {f.get('type', 'appointment')}{when} today{flag}")

    return lines


def send_sms(body: str) -> bool:
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM_NUMBER")
    to_number = os.environ.get("TWILIO_TO_NUMBER")
    if not all([sid, token, from_number, to_number]):
        return False
    from twilio.rest import Client  # imported lazily so it's an optional dep

    client = Client(sid, token)
    client.messages.create(body=body[:1500], from_=from_number, to=to_number)
    return True


def send_email(subject: str, body: str) -> bool:
    address = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    to_addr = os.environ.get("NOTIFY_EMAIL_TO", address)
    if not all([address, app_password, to_addr]):
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = address
    msg["To"] = to_addr
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(address, app_password)
        server.sendmail(address, [to_addr], msg.as_string())
    return True


def main():
    load_env_file(ENV_FILE)
    items = gather_due_items()

    if not items:
        if os.environ.get("NOTIFY_ALWAYS", "").lower() in ("1", "true", "yes"):
            body = "CRM check: nothing due today. All caught up."
        else:
            print("Nothing due. (Set NOTIFY_ALWAYS=1 to get a message even when there's nothing due.)")
            return
    else:
        body = "CRM follow-ups due:\n" + "\n".join(items)

    sent_sms = send_sms(body)
    sent_email = send_email("CRM: follow-ups due", body)

    if not sent_sms and not sent_email:
        print("No notification channel configured (see README.md). Message would have been:\n")
        print(body)
    else:
        if sent_sms:
            print("Text sent.")
        if sent_email:
            print("Email sent.")


if __name__ == "__main__":
    sys.exit(main())
