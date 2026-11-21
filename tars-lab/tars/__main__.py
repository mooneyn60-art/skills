"""CLI: python3 -m tars <command>

  improve                 run the self-improvement loop (writes proposals/, rules.json)
  postmortem              print the postmortem
  rules list              show the rules registry
  rules adopt ID --by NAME / rules retire ID --by NAME / rules reject ID --by NAME
  guard-hook              PreToolUse hook entry point (reads hook JSON on stdin)
  unprotected FILE        list positions without a stop from a positions JSON dump
  coach --side call --qty 5 --spy-move 0.2 [--day-pnl -250 --last-side put --mins 4 --stop]
"""
import argparse
import json
import sys

from . import coach, guard, improve, ledger, postmortem, registry


def main(argv=None):
    p = argparse.ArgumentParser(prog="tars")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("improve")
    sub.add_parser("postmortem")
    r = sub.add_parser("rules")
    r.add_argument("action", choices=["list", "adopt", "retire", "reject"])
    r.add_argument("id", nargs="?")
    r.add_argument("--by")
    sub.add_parser("guard-hook")
    u = sub.add_parser("unprotected")
    u.add_argument("file")
    c = sub.add_parser("coach")
    c.add_argument("--side", required=True, choices=["call", "put"])
    c.add_argument("--qty", type=float, required=True)
    c.add_argument("--spy-move", type=float, required=True)
    c.add_argument("--day-pnl", type=float, default=0.0)
    c.add_argument("--last-side", choices=["call", "put"])
    c.add_argument("--mins", type=float)
    c.add_argument("--usual-qty", type=float, default=3)
    c.add_argument("--stop", action="store_true")
    a = p.parse_args(argv)

    if a.cmd == "improve":
        text, _ = improve.run()
        print(text)
    elif a.cmd == "postmortem":
        print(postmortem.report(ledger.load()))
    elif a.cmd == "rules":
        if a.action == "list":
            for x in registry.load()["rules"]:
                print(f"{x['id']:28s} {x['status']:9s} {json.dumps(x['params'])}")
        else:
            if not (a.id and a.by):
                p.error("rules adopt/retire/reject needs ID and --by NAME")
            status = {"adopt": "adopted", "retire": "retired", "reject": "rejected"}[a.action]
            print(registry.set_status(a.id, status, a.by))
    elif a.cmd == "guard-hook":
        return guard.hook_main()
    elif a.cmd == "unprotected":
        data = json.load(open(a.file))
        pos = data.get("data", data).get("positions", data) if isinstance(data, dict) else data
        bad = guard.unprotected(pos)
        print(json.dumps(bad, indent=2))
        return 1 if bad else 0
    elif a.cmd == "coach":
        w = coach.check(a.side, a.qty, a.spy_move, a.day_pnl, a.last_side, a.mins, a.usual_qty, a.stop)
        print("\n".join(w) if w else "no warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
