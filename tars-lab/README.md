# tars-lab

Toolkit for the TARS desk (`skills/robinhood-autotrader`). Python 3 standard library only:
nothing to download or install. It reads the desk ledger read-only and never places orders.

```
python3 -m tars improve        # the self-improvement loop (writes proposals/ and rules.json)
python3 -m tars postmortem     # options by day / size / hour, stop slippage, sleeve record
python3 -m tars rules list     # rules registry: proposed / adopted / retired
python3 -m tars rules adopt ID --by Nolan
python3 -m tars coach --side put --qty 6 --spy-move 0.1 --day-pnl -250 --last-side call --mins 4
python3 -m tars unprotected positions.json   # positions with no stop
python3 -m unittest discover -s tests        # 15 tests
```

## How it improves itself

```
 observe  ->  search  ->  validate  ->  propose  ->  (owner adopts)  ->  learn
 ledger      every       pick on the    proposals/    rules.json           adopted rules:
 postmortem  candidate   earlier days,  <date>.md     status=adopted       days broken and
             rule        score on the   + rules.json  guard enforces it    what breaking cost
                         later days     (proposed)
```

- **Two objectives.** `profit`: rules that would have made more. `protect`: rules that shrink
  the worst day while keeping 90% of the profit.
- **Walk-forward.** A rule is picked on the earlier 60% of days and must also win on the later
  40% it never saw. Rules that only fit the past are rejected and the report says so.
- **Simplest wins.** Among rules within 5% of the best, the one with fewest conditions is chosen.
- **Never self-adopts.** The loop can only *propose*. Only `rules adopt --by <owner>` turns a
  rule on, and only adopted rules are enforced by the guard. Self-improving, not self-modifying.
- **Learns from adherence.** Every run checks adopted rules against what actually happened:
  how many days the rule was broken and what breaking it cost (or saved).

## Guard (PreToolUse hook, not wired yet)

`python3 -m tars guard-hook` denies *opening* option orders placed by the desk once an adopted
limit is hit (daily loss, losses in a row, round trips, size). Closing orders and stock orders
are never blocked. It fails closed: if `state/today.json` (date, options_pnl, losses_in_row,
round_trips) is not for today, option buys are denied until the desk refreshes it. With no
adopted rules it does nothing. To wire it into the desk session, add to `.claude/settings.json`:

```json
{"hooks": {"PreToolUse": [{"matcher": "mcp__Robinhood__place_option_order",
  "hooks": [{"type": "command", "command": "cd \"$CLAUDE_PROJECT_DIR/tars-lab\" && python3 -m tars guard-hook"}]}]}}
```

## Caveat

The replay assumes trades skipped by a rule were independent of the ones kept. It ignores tilt
(a daily stop also prevents the revenge trades it never sees), so real effects of loss limits
are probably better than shown, and gains from big comeback trades are probably overstated.
