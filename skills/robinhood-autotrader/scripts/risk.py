"""Position sizing caps and a daily-loss circuit breaker.

This is the safety layer every decision has to pass through before it can become an
order. Nothing in trader.py should call executor.py directly without going through
here first.
"""
import csv
import datetime
import os

import config


class TradingHalted(Exception):
    """Raised when the circuit breaker (or a pre-existing halt) blocks all trading."""


def check_halt():
    if os.path.exists(config.HALT_FILE_PATH):
        raise TradingHalted(
            f"{config.HALT_FILE_PATH} exists — trading is halted. Review trade_log.csv, "
            "understand why the circuit breaker fired (or who created this file), and "
            "delete it manually to resume. This does not clear itself."
        )


def _today_realized_and_unrealized_pnl(account_state, starting_equity: float) -> float:
    """Best-effort daily P&L: current equity vs. the equity recorded at the start of
    today's run. Requires trader.py to have recorded a start-of-day equity snapshot.
    """
    return account_state.equity - starting_equity


def enforce_daily_loss_breaker(account_state, starting_equity: float):
    """Writes the halt file and raises TradingHalted if today's loss exceeds the cap."""
    if starting_equity <= 0:
        return  # no baseline yet (first run of the day); nothing to compare against

    pnl = _today_realized_and_unrealized_pnl(account_state, starting_equity)
    loss_fraction = -pnl / starting_equity if pnl < 0 else 0.0

    if loss_fraction >= config.MAX_DAILY_LOSS_FRACTION:
        with open(config.HALT_FILE_PATH, "w") as f:
            f.write(
                f"Circuit breaker fired at {datetime.datetime.now().isoformat()}\n"
                f"Daily loss {loss_fraction:.2%} >= cap {config.MAX_DAILY_LOSS_FRACTION:.2%}\n"
                f"Starting equity: {starting_equity:.2f}, current equity: "
                f"{account_state.equity:.2f}\n"
            )
        raise TradingHalted(
            f"Daily loss {loss_fraction:.2%} breached cap "
            f"{config.MAX_DAILY_LOSS_FRACTION:.2%}. Halting and writing "
            f"{config.HALT_FILE_PATH}."
        )


def size_position(decision: dict, account_state, snapshot) -> float:
    """Returns a dollar amount to trade for a buy decision (0.0 if it shouldn't trade).

    Applies, in order: minimum confidence gate, per-trade dollar cap, and per-position
    fraction-of-equity cap. Never returns more than the account's buying power.
    """
    if decision["action"] != "buy":
        return 0.0
    if decision.get("confidence", 0.0) < config.MIN_CONFIDENCE:
        return 0.0

    existing_value = account_state.positions.get(decision["symbol"], {}).get("market_value", 0.0)
    equity_cap = config.MAX_POSITION_FRACTION_OF_EQUITY * account_state.equity
    room_left_under_equity_cap = max(0.0, equity_cap - existing_value)

    size = min(
        config.MAX_POSITION_SIZE_USD,
        room_left_under_equity_cap,
        account_state.buying_power,
    )
    return max(0.0, size)


def sell_quantity(decision: dict, account_state) -> float:
    """Returns the share quantity to sell for a sell decision (0.0 if not held)."""
    if decision["action"] != "sell":
        return 0.0
    if decision.get("confidence", 0.0) < config.MIN_CONFIDENCE:
        return 0.0
    position = account_state.positions.get(decision["symbol"])
    if not position:
        return 0.0
    return position["quantity"]


def append_trade_log(rows: list):
    file_exists = os.path.exists(config.TRADE_LOG_PATH)
    with open(config.TRADE_LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "symbol",
                "action",
                "confidence",
                "reasoning",
                "size_usd_or_qty",
                "mode",
                "order_id",
            ],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)
