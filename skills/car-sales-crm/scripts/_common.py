"""Shared helpers for the car-sales-crm scripts and dashboard. No third-party deps."""
import re
from datetime import date, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CUSTOMERS_DIR = SKILL_DIR / "customers"
APPOINTMENTS_DIR = SKILL_DIR / "calendar" / "appointments"
VEHICLE_SPECS_DIR = SKILL_DIR / "vehicle-specs"
TEMPLATES_DIR = SKILL_DIR / "templates"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.split("#", 1)[0].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def parse_date(value: str):
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (name or "").strip().lower()).strip("-")
    return slug or "record"


def unique_slug(directory: Path, name: str) -> str:
    base = slugify(name)
    slug = base
    n = 2
    while (directory / f"{slug}.md").exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


def load_schema(template_path: Path):
    """Read a template's front matter as an ordered list of (key, comment)."""
    text = template_path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    schema = []
    if not match:
        return schema
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        comment = rest.split("#", 1)[1].strip() if "#" in rest else ""
        schema.append((key.strip(), comment))
    return schema


def render_front_matter(schema, fields: dict) -> str:
    lines = ["---"]
    for key, comment in schema:
        value = fields.get(key, "")
        line = f"{key}: {value}"
        if comment:
            line += f"  # {comment}"
        lines.append(line)
    lines.append("---")
    return "\n".join(lines) + "\n"


def split_body(text: str) -> str:
    match = FRONT_MATTER_RE.match(text)
    return text[match.end():] if match else text


def write_record(path: Path, schema, fields: dict, body: str):
    path.write_text(render_front_matter(schema, fields) + body, encoding="utf-8")


def append_to_section(body: str, heading: str, new_line: str) -> str:
    """Insert new_line as the last item of the named '## Heading' section."""
    lines = body.splitlines()
    heading_idx = next((i for i, l in enumerate(lines) if l.strip() == heading.strip()), None)
    if heading_idx is None:
        sep = "" if body.endswith("\n") or not body else "\n"
        return body + f"{sep}\n{heading}\n{new_line}\n"
    insert_at = len(lines)
    for j in range(heading_idx + 1, len(lines)):
        if lines[j].startswith("## "):
            insert_at = j
            break
    new_lines = lines[:insert_at] + [new_line] + lines[insert_at:]
    return "\n".join(new_lines) + "\n"


def suggest_next_followup(status: str, today: date = None) -> str:
    """Cadence from references/followup-cadence.md, as a date string (or '' for sold/lost)."""
    today = today or date.today()
    status = (status or "").strip().lower()
    if status == "hot":
        d = today + timedelta(days=1)
        while d.weekday() >= 5:  # Sat/Sun -> next business day
            d += timedelta(days=1)
        return d.isoformat()
    if status == "cold":
        return (today + timedelta(days=10)).isoformat()
    if status in ("sold", "lost"):
        return ""
    return (today + timedelta(days=3)).isoformat()  # warm, or unknown status


def today_str() -> str:
    return date.today().isoformat()
