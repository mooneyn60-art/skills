"""The self-improvement loop.

  observe  -> postmortem of the ledger
  search   -> replay every candidate discipline rule over past days
  validate -> walk-forward: pick on the earlier days, score on the later days
  propose  -> write proposals/<date>.md and add the winner to rules.json as PROPOSED
  learn    -> for ADOPTED rules, count days the rule was broken and what that cost

It never adopts anything. Adoption is the owner's call (`python3 -m tars rules adopt`).
"""
import json
import os
from datetime import datetime, timezone

from . import ledger, postmortem, registry, rules_sim

HERE = os.path.dirname(__file__)
PROPOSALS = os.path.join(HERE, "..", "proposals")
MIN_TEST_DAYS = 5


def rule_id(rule):
    abbrev = {"daily_stop": "ds", "max_losses_in_row": "lr", "max_qty": "q", "max_trades": "n"}
    return "opt-" + "-".join(f"{abbrev[k]}{rule[k]:g}" for k in sorted(rule))


def _profit(res, base):
    return res["total"] - base["total"]


def _protect(res, base, keep=0.9):
    """Improve the worst day while keeping most of the profit; -inf if it gives up too much."""
    floor = base["total"] - abs(base["total"]) * (1 - keep)
    if res["total"] < floor:
        return float("-inf")
    return res["worst_day"] - base["worst_day"]


OBJECTIVES = {"profit": _profit, "protect": _protect}


def search(days, train_frac=0.6, objective="profit"):
    score = OBJECTIVES[objective]
    keys = list(days)
    cut = max(1, int(len(keys) * train_frac))
    train = {k: days[k] for k in keys[:cut]}
    test = {k: days[k] for k in keys[cut:]}
    base_tr, base_te = rules_sim.run(train), rules_sim.run(test)
    scored = []
    for rule in rules_sim.candidates():
        if not rule:
            continue
        tr = rules_sim.run(train, **rule)
        scored.append((score(tr, base_tr), -len(rule), rule, tr))
    scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
    best_gain = scored[0][0] if scored else 0
    # among rules within 5% of the best train gain, prefer the simplest
    near = [s for s in scored if best_gain > 0 and s[0] >= 0.95 * best_gain]
    pick = min(near, key=lambda s: (len(s[2]), -s[0])) if near else None
    result = {"objective": objective, "train_days": len(train), "test_days": len(test), "base_train": base_tr, "base_test": base_te}
    if pick:
        rule = pick[2]
        result.update(rule=rule, train=pick[3], test=rules_sim.run(test, **rule),
                      full=rules_sim.run(days, **rule), base_full=rules_sim.run(days))
    return result


def adherence(days, rules):
    """For adopted rules: days after adoption where trading continued past the limit."""
    out = []
    for r in rules:
        if r["status"] != "adopted":
            continue
        since = next((h["at"][:10] for h in reversed(r["history"]) if h["event"] == "adopted"), None)
        broken, cost = 0, 0.0
        for d, ts in days.items():
            if since and d < since:
                continue
            kept, _ = rules_sim.apply(ts, **r["params"])
            actual = sum(t["pnl"] for t in ts)
            if abs(actual - kept) > 0.005:
                broken += 1
                cost += actual - kept
        out.append({"id": r["id"], "since": since, "days_broken": broken, "cost_of_breaking": round(cost, 2)})
    return out


def run(rows=None, write=True, today=None):
    rows = rows if rows is not None else ledger.load()
    today = today or datetime.now(timezone.utc).astimezone(registry.ET).date().isoformat()
    trades = ledger.owner_option_trades(rows)
    days = ledger.by_day(trades)
    reg = registry.load()
    adh = adherence(days, reg["rules"])
    lines = [f"# Improvement run {today}", ""]
    lines.append(f"Data: {len(trades)} owner option round trips over {len(days)} days.")
    lines.append("")
    verdicts, res = {}, {}
    for obj, title in (("profit", "Rules that would have made more money"),
                       ("protect", "Rules that cut the worst day but keep 90% of the profit")):
        r_ = search(days, objective=obj)
        res[obj] = r_
        lines += [f"## {title}", "", f"Picked on the earlier {r_['train_days']} days, checked on the later {r_['test_days']}.", ""]
        if "rule" not in r_:
            lines += ["No candidate passed on the earlier days. Nothing proposed.", ""]
            verdicts[obj] = "none"
            continue
        r = r_["rule"]
        lines += [f"Best: **{rules_sim.describe(r)}**", "",
                  "| | baseline | with rule |", "|---|---|---|",
                  f"| earlier days: net | {r_['base_train']['total']:+.0f} | {r_['train']['total']:+.0f} |",
                  f"| later days (unseen): net | {r_['base_test']['total']:+.0f} | {r_['test']['total']:+.0f} |",
                  f"| later days: worst day | {r_['base_test']['worst_day']:+.0f} | {r_['test']['worst_day']:+.0f} |",
                  f"| all days: worst day | {r_['base_full']['worst_day']:+.0f} | {r_['full']['worst_day']:+.0f} |", ""]
        passed = OBJECTIVES[obj](r_["test"], r_["base_test"]) > 0
        if passed:
            verdicts[obj] = "propose"
            ev = {"run": today, "objective": obj, "test_days": r_["test_days"],
                  "test_net": r_["test"]["total"], "base_test_net": r_["base_test"]["total"],
                  "worst_day": r_["full"]["worst_day"], "base_worst_day": r_["base_full"]["worst_day"],
                  "low_evidence": r_["test_days"] < MIN_TEST_DAYS}
            if write:
                registry.propose(rule_id(r), r, ev)
            lines.append(f"Verdict: PROPOSED as `{rule_id(r)}`; it also held up on the unseen days.")
            if r_["test_days"] < MIN_TEST_DAYS:
                lines.append(f"Evidence is thin: only {r_['test_days']} unseen days (want {MIN_TEST_DAYS}+).")
        else:
            verdicts[obj] = "reject"
            lines.append("Verdict: not proposed; it did not hold up on the unseen days (overfit).")
        lines.append("")
    lines += ["", "Caveat: replay assumes skipped trades were independent of kept ones (ignores tilt).", ""]
    if adh:
        lines += ["## Adopted rules: were they followed?", "", "| rule | since | days broken | cost |", "|---|---|---|---|"]
        lines += [f"| {a['id']} | {a['since']} | {a['days_broken']} | {a['cost_of_breaking']:+.0f} |" for a in adh]
        lines.append("")
    lines.append(postmortem.report(rows).replace("# Postmortem", "## Postmortem"))
    text = "\n".join(lines)
    if write:
        os.makedirs(PROPOSALS, exist_ok=True)
        with open(os.path.join(PROPOSALS, f"{today}.md"), "w") as f:
            f.write(text)
        with open(os.path.join(PROPOSALS, "log.jsonl"), "a") as f:
            f.write(json.dumps({"date": today, "verdicts": verdicts,
                                "rules": {k: v.get("rule") for k, v in res.items()},
                                "trips": len(trades), "days": len(days), "adherence": adh}) + "\n")
    return text, res
