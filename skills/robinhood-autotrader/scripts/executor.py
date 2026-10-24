"""Places orders — or, in paper mode (the default), just records what would have been
ordered. Real orders only ever happen when config.LIVE_TRADING is True, which is set
by the user's own LIVE_TRADING=true environment variable, never by this code.
"""
import datetime

import config


def execute_buy(rh, symbol: str, amount_usd: float) -> str:
    """Returns an order id (paper mode: a synthetic 'PAPER-...' id)."""
    if amount_usd <= 0:
        return ""

    if not config.LIVE_TRADING:
        return f"PAPER-BUY-{symbol}-{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}"

    order = rh.orders.order_buy_fractional_by_price(
        symbol, amount_usd, timeInForce="gtc"
    )
    return (order or {}).get("id", "")


def execute_sell(rh, symbol: str, quantity: float) -> str:
    """Returns an order id (paper mode: a synthetic 'PAPER-...' id)."""
    if quantity <= 0:
        return ""

    if not config.LIVE_TRADING:
        return f"PAPER-SELL-{symbol}-{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}"

    order = rh.orders.order_sell_fractional_by_quantity(
        symbol, quantity, timeInForce="gtc"
    )
    return (order or {}).get("id", "")


def mode_label() -> str:
    return "live" if config.LIVE_TRADING else "paper"
