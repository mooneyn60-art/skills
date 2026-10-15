"""Rules registry: every rule has a status (proposed / adopted / retired) and a history.

Only `adopt` with an owner name moves a rule to adopted; the improvement loop can
only add proposals. That is the line between self-improving and self-modifying.
"""
import json
import os
from datetime import datetime, timedelta, timezone

ET = timezone(timedelta(hours=-4))
PATH = os.environ.get("TARS_RULES", os.path.join(os.path.dirname(__file__), "..", "rules.json"))


def load(path=None):
    try:
        with open(path or PATH) as f:
            return json.load(f)
    except OSError:
        return {"rules": []}


def save(data, path=None):
    with open(path or PATH, "w") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")


def _now():
    return datetime.now(timezone.utc).astimezone(ET).isoformat(timespec="minutes")


def propose(rule_id, params, evidence, path=None):
    data = load(path)
    for r in data["rules"]:
        if r["id"] == rule_id:
            if r["status"] == "proposed":
                r["params"], r["evidence"] = params, evidence
                r["history"].append({"at": _now(), "event": "re-proposed"})
                save(data, path)
            return r
    r = {"id": rule_id, "kind": "options_discipline", "status": "proposed", "params": params,
         "evidence": evidence, "history": [{"at": _now(), "event": "proposed"}]}
    data["rules"].append(r)
    save(data, path)
    return r


def set_status(rule_id, status, by, path=None):
    assert status in ("adopted", "retired", "rejected")
    data = load(path)
    for r in data["rules"]:
        if r["id"] == rule_id:
            r["status"] = status
            r["history"].append({"at": _now(), "event": status, "by": by})
            save(data, path)
            return r
    raise KeyError(rule_id)


def adopted_limits(path=None):
    limits = {}
    for r in load(path)["rules"]:
        if r["status"] == "adopted" and r.get("kind") == "options_discipline":
            for k, v in r["params"].items():
                limits[k] = min(v, limits[k]) if k in limits else v
    return limits
