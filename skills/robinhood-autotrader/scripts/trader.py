#!/usr/bin/env python3
"""Entry point for the Robinhood autotrader.

    python trader.py --once            # single pass, then exit
    python trader.py --interval 900    # loop forever, one pass every N seconds

Runs fully unattended (no per-trade confirmation prompt) but every pass is gated by
risk.py's caps and circuit breaker, and defaults to paper mode until the user sets
LIVE_TRADING=true in their own environment. See SKILL.md before enabling live mode.
"""
import argparse
import datetime
import sys
import time

from dotenv import load_dotenv

load_dotenv()

import auth
import config
import executor
import market_data
import risk
import signals


def run_once(rh, starting_equity: dict):
    risk.check_halt()

    account_state = market_data.get_account_state(rh)

    today = datetime.date.today().isoformat()
    if starting_equity.get("date") != today:
        starting_equity["date"] = today
        starting_equity["equity"] = account_state.equity

    risk.enforce_daily_loss_breaker(account_state, starting_equity["equity"])

    snapshots = market_data.get_watchlist_snapshots(rh, config.WATCHLIST)
    if not snapshots:
        print("No market data available this pass (nothing fabricated) — skipping.")
        return

    decisions = signals.get_decisions(account_state, snapshots)
    snapshots_by_symbol = {s.symbol: s for s in snapshots}

    log_rows = []
    for decision in decisions:
        symbol = decision.get("symbol")
        action = decision.get("action")
        snapshot = snapshots_by_symbol.get(symbol)
        if not snapshot:
            continue

        order_id = ""
        size_label = 0

        if action == "buy":
            amount_usd = risk.size_position(decision, account_state, snapshot)
            if amount_usd > 0:
                order_id = executor.execute_buy(rh, symbol, amount_usd)
                size_label = round(amount_usd, 2)
        elif action == "sell":
            quantity = risk.sell_quantity(decision, account_state)
            if quantity > 0:
                order_id = executor.execute_sell(rh, symbol, quantity)
                size_label = quantity

        log_rows.append(
            {
                "timestamp": datetime.datetime.now().isoformat(),
                "symbol": symbol,
                "action": action,
                "confidence": decision.get("confidence"),
                "reasoning": decision.get("reasoning", "").replace("\n", " "),
                "size_usd_or_qty": size_label,
                "mode": executor.mode_label(),
                "order_id": order_id,
            }
        )

    risk.append_trade_log(log_rows)
    acted = [r for r in log_rows if r["order_id"]]
    print(
        f"[{datetime.datetime.now().isoformat()}] pass complete: "
        f"{len(decisions)} decisions, {len(acted)} orders ({executor.mode_label()} mode)."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--once", action="store_true", help="run a single pass and exit")
    group.add_argument(
        "--interval", type=int, help="loop forever, sleeping this many seconds between passes"
    )
    args = parser.parse_args()

    try:
        risk.check_halt()
    except risk.TradingHalted as e:
        sys.exit(str(e))

    rh = auth.login()
    print(f"Logged in. Mode: {executor.mode_label()}. Watchlist: {config.WATCHLIST}")

    starting_equity = {}

    if args.once:
        run_once(rh, starting_equity)
        return

    while True:
        try:
            run_once(rh, starting_equity)
        except risk.TradingHalted as e:
            print(f"HALTED: {e}")
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
