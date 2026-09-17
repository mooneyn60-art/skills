#!/usr/bin/env python3
"""Local web dashboard for the car-sales-crm skill.

Run with:  python3 app.py
Then open: http://localhost:5050

Reads/writes the same plain-Markdown files the Claude skill uses
(../customers, ../calendar/appointments, ../vehicle-specs), so anything
you do here shows up next time you talk to Claude, and vice versa.
"""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from _common import (  # noqa: E402
    APPOINTMENTS_DIR,
    CUSTOMERS_DIR,
    TEMPLATES_DIR,
    VEHICLE_SPECS_DIR,
    append_to_section,
    load_schema,
    parse_date,
    parse_front_matter,
    render_front_matter,
    split_body,
    suggest_next_followup,
    today_str,
    unique_slug,
)
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

CUSTOMER_SCHEMA = load_schema(TEMPLATES_DIR / "customer-record.md")
APPOINTMENT_SCHEMA = load_schema(TEMPLATES_DIR / "appointment.md")

for d in (CUSTOMERS_DIR, APPOINTMENTS_DIR, VEHICLE_SPECS_DIR):
    d.mkdir(parents=True, exist_ok=True)


def urgency(next_followup: str, status: str):
    d = parse_date(next_followup)
    if d is None:
        return "none"
    today = date.today()
    if d < today:
        return "overdue"
    if d == today:
        return "today"
    if d <= today + timedelta(days=3):
        return "soon"
    return "later"


def customer_to_dict(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields = parse_front_matter(text)
    fields["slug"] = path.stem
    fields["urgency"] = urgency(fields.get("next_followup", ""), fields.get("status", ""))
    fields["notes_body"] = split_body(text)
    return fields


def appointment_to_dict(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields = parse_front_matter(text)
    fields["slug"] = path.stem
    fields["notes_body"] = split_body(text)
    d = parse_date(fields.get("date", ""))
    fields["is_overdue"] = bool(d and d < date.today())
    return fields


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/customers", methods=["GET"])
def list_customers():
    customers = [customer_to_dict(p) for p in sorted(CUSTOMERS_DIR.glob("*.md"))]
    return jsonify(customers)


@app.route("/api/customers", methods=["POST"])
def create_customer():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    slug = unique_slug(CUSTOMERS_DIR, name)
    fields = {key: "" for key, _ in CUSTOMER_SCHEMA}
    fields.update({k: v for k, v in data.items() if k in fields})
    fields["status"] = fields.get("status") or "warm"
    fields["stage"] = fields.get("stage") or "new"
    fields["created"] = fields.get("created") or today_str()
    for c in ("consent_call", "consent_text", "consent_email"):
        fields[c] = fields.get(c) or "unknown"
    body = f"\n# {name}\n\n## Notes\n\n## Tips for this customer\n"
    initial_note = (data.get("note") or "").strip()
    if initial_note:
        body = append_to_section(body, "## Notes", f"- {today_str()}: {initial_note}")
    path = CUSTOMERS_DIR / f"{slug}.md"
    path.write_text(render_front_matter(CUSTOMER_SCHEMA, fields) + body, encoding="utf-8")
    return jsonify(customer_to_dict(path)), 201


@app.route("/api/customers/<slug>", methods=["GET"])
def get_customer(slug):
    path = CUSTOMERS_DIR / f"{slug}.md"
    if not path.exists():
        return jsonify({"error": "not found"}), 404
    return jsonify(customer_to_dict(path))


@app.route("/api/customers/<slug>", methods=["POST"])
def update_customer(slug):
    path = CUSTOMERS_DIR / f"{slug}.md"
    if not path.exists():
        return jsonify({"error": "not found"}), 404
    text = path.read_text(encoding="utf-8")
    fields = parse_front_matter(text)
    body = split_body(text)
    data = request.get_json(force=True)

    note = (data.pop("note", None) or "").strip()
    log_contact_channel = data.pop("log_contact_channel", None)

    for key, value in data.items():
        if key in dict(CUSTOMER_SCHEMA):
            fields[key] = value

    if log_contact_channel:
        fields["last_contact"] = today_str()
        fields["last_contact_channel"] = log_contact_channel
        if not data.get("next_followup"):
            fields["next_followup"] = suggest_next_followup(fields.get("status"))
            fields["next_followup_channel"] = log_contact_channel

    if note:
        tag = f" ({log_contact_channel})" if log_contact_channel else ""
        body = append_to_section(body, "## Notes", f"- {today_str()}{tag}: {note}")

    path.write_text(render_front_matter(CUSTOMER_SCHEMA, fields) + body, encoding="utf-8")
    return jsonify(customer_to_dict(path))


@app.route("/api/customers/<slug>", methods=["DELETE"])
def delete_customer(slug):
    path = CUSTOMERS_DIR / f"{slug}.md"
    if path.exists():
        path.unlink()
    return jsonify({"ok": True})


@app.route("/api/appointments", methods=["GET"])
def list_appointments():
    return jsonify([appointment_to_dict(p) for p in sorted(APPOINTMENTS_DIR.glob("*.md"))])


@app.route("/api/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json(force=True)
    customer = (data.get("customer") or "").strip()
    if not customer or not data.get("date"):
        return jsonify({"error": "customer and date are required"}), 400
    slug = unique_slug(APPOINTMENTS_DIR, f"{customer}-{data.get('type', 'appt')}")
    fields = {key: "" for key, _ in APPOINTMENT_SCHEMA}
    fields.update({k: v for k, v in data.items() if k in fields})
    fields["created"] = today_str()
    if not fields.get("confirmed"):
        fields["confirmed"] = "false"
    body = f"\n# {data.get('type', 'Appointment').replace('-', ' ').title()} — {customer}\n\n## Notes\n"
    note = (data.get("note") or "").strip()
    if note:
        body = append_to_section(body, "## Notes", f"- {note}")
    path = APPOINTMENTS_DIR / f"{slug}.md"
    path.write_text(render_front_matter(APPOINTMENT_SCHEMA, fields) + body, encoding="utf-8")
    return jsonify(appointment_to_dict(path)), 201


@app.route("/api/appointments/<slug>", methods=["POST"])
def update_appointment(slug):
    path = APPOINTMENTS_DIR / f"{slug}.md"
    if not path.exists():
        return jsonify({"error": "not found"}), 404
    text = path.read_text(encoding="utf-8")
    fields = parse_front_matter(text)
    body = split_body(text)
    data = request.get_json(force=True)
    for key, value in data.items():
        if key in dict(APPOINTMENT_SCHEMA):
            fields[key] = "true" if value is True else ("false" if value is False else value)
    path.write_text(render_front_matter(APPOINTMENT_SCHEMA, fields) + body, encoding="utf-8")
    return jsonify(appointment_to_dict(path))


@app.route("/api/appointments/<slug>", methods=["DELETE"])
def delete_appointment(slug):
    path = APPOINTMENTS_DIR / f"{slug}.md"
    if path.exists():
        path.unlink()
    return jsonify({"ok": True})


@app.route("/api/vehicle-specs", methods=["GET"])
def list_vehicle_specs():
    specs = []
    for p in sorted(VEHICLE_SPECS_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        fields = parse_front_matter(text)
        fields["slug"] = p.stem
        fields["body"] = split_body(text)
        specs.append(fields)
    return jsonify(specs)


@app.route("/api/summary", methods=["GET"])
def summary():
    today = date.today()
    customers = [customer_to_dict(p) for p in CUSTOMERS_DIR.glob("*.md")]
    appts = [appointment_to_dict(p) for p in APPOINTMENTS_DIR.glob("*.md")]
    overdue_followups = [c for c in customers if c["urgency"] == "overdue"]
    today_followups = [c for c in customers if c["urgency"] == "today"]
    today_appts = [a for a in appts if parse_date(a.get("date", "")) == today]
    unconfirmed_soon = [
        a
        for a in appts
        if a.get("confirmed", "").lower() != "true"
        and parse_date(a.get("date", ""))
        and today <= parse_date(a.get("date")) <= today + timedelta(days=2)
    ]
    return jsonify(
        {
            "overdue_followups": len(overdue_followups),
            "today_followups": len(today_followups),
            "today_appointments": len(today_appts),
            "unconfirmed_soon": len(unconfirmed_soon),
            "total_customers": len(customers),
        }
    )


if __name__ == "__main__":
    print("Car Sales CRM dashboard: http://localhost:5050")
    app.run(host="127.0.0.1", port=5050, debug=False)
