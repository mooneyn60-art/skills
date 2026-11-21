"""Weekly postmortem from the ledger: what happened, what it cost, which pattern."""
from collections import defaultdict

from . import ledger


def _bucket(q):
    return "1-2" if q <= 2 else "3-5" if q <= 5 else "6-10" if q <= 10 else ">10"


def options_report(trades):
    if not trades:
        return ["No owner option round trips in the ledger."]
    pnl = [t["pnl"] for t in trades]
    wins = [p for p in pnl if p > 0]
    losses = [p for p in pnl if p <= 0]
    out = [f"Owner options: {len(trades)} round trips, net {sum(pnl):+.0f}; "
           f"{len(wins)} wins avg {sum(wins)/max(len(wins),1):+.0f}, "
           f"{len(losses)} losses avg {sum(losses)/max(len(losses),1):+.0f}."]
    out.append("")
    out.append("| day | trips | net | best | worst |")
    out.append("|---|---|---|---|---|")
    for d, ts in ledger.by_day(trades).items():
        p = [t["pnl"] for t in ts]
        out.append(f"| {d} | {len(ts)} | {sum(p):+.0f} | {max(p):+.0f} | {min(p):+.0f} |")
    for title, key in (("size", lambda t: _bucket(t["qty"])), ("hour ET (close)", lambda t: f"{t['hour_et']:02d}")):
        g = defaultdict(list)
        for t in trades:
            g[key(t)].append(t["pnl"])
        out.append("")
        out.append(f"| {title} | trips | net | win% |")
        out.append("|---|---|---|---|")
        for k in sorted(g):
            v = g[k]
            out.append(f"| {k} | {len(v)} | {sum(v):+.0f} | {100*sum(1 for x in v if x > 0)/len(v):.0f}% |")
    # sizing after a loss vs after a win (same day)
    after_loss, after_win = [], []
    for ts in ledger.by_day(trades).values():
        for a, b in zip(ts, ts[1:]):
            (after_loss if a["pnl"] <= 0 else after_win).append(b["qty"])
    if after_loss and after_win:
        out.append("")
        out.append(f"Average size after a loss {sum(after_loss)/len(after_loss):.1f} vs after a win "
                   f"{sum(after_win)/len(after_win):.1f} contracts.")
    return out


def equity_report(rows):
    eq = ledger.closed_equity(rows)
    out = []
    slips = []
    for r in eq:
        stop = r.get("stop")
        if stop and "stop" in str(r.get("exit_reason", "")) and r["exit"] < stop:
            slips.append((r["symbol"], r["closed"][:10], (r["exit"] / stop - 1) * 100))
    if slips:
        out.append("Stops that filled below their level (gap slippage):")
        for s, d, pct in slips:
            out.append(f"- {s} {d}: {pct:.1f}% under the stop")
    g = defaultdict(list)
    for r in eq:
        if r.get("r_multiple") is not None:
            g[str(r.get("exit_reason"))].append(float(r["r_multiple"]))
    if g:
        out.append("")
        out.append("| exit reason | n | mean R |")
        out.append("|---|---|---|")
        for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
            out.append(f"| {k} | {len(v)} | {sum(v)/len(v):+.2f} |")
    sleeve = [r for r in eq if r.get("strategy") == "momentum_satellite" and r.get("r_multiple") is not None]
    sleeve.sort(key=lambda r: r["closed"])
    streak = 0
    for r in reversed(sleeve):
        if r["r_multiple"] < 0:
            streak += 1
        else:
            break
    if sleeve:
        out.append("")
        out.append(f"Momentum sleeve: {len(sleeve)} closes, net {sum(r['r_multiple'] for r in sleeve):+.2f}R, "
                   f"current losing streak {streak}.")
    return out


def report(rows):
    trades = ledger.owner_option_trades(rows)
    return "\n".join(["# Postmortem", "", "## Options", ""] + options_report(trades)
                     + ["", "## Stocks", ""] + equity_report(rows)) + "\n"
