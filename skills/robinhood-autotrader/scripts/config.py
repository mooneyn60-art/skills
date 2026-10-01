"""Configuration for the Robinhood autotrader, sourced entirely from the environment.

Nothing here is a secret. Credentials live in the user's own .env (see .env.example),
never in this file.
"""
import os


def _float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    return float(raw) if raw else default


def _list_env(name: str, default: list[str]) -> list[str]:
    raw = os.environ.get(name)
    if not raw:
        return default
    return [s.strip().upper() for s in raw.split(",") if s.strip()]


# Symbols the bot considers each pass.
WATCHLIST = _list_env("AUTOTRADER_WATCHLIST", ["AAPL", "MSFT", "SPY", "QQQ"])

# --- Risk limits ("moderate" defaults; tune before ever going live) ---
# Max dollars committed to a single new position in one pass.
MAX_POSITION_SIZE_USD = _float_env("AUTOTRADER_MAX_POSITION_USD", 2000.0)

# Circuit breaker: halt the whole loop for the day once realized+unrealized daily P&L
# drops this fraction of account equity (e.g. 0.04 = 4%).
MAX_DAILY_LOSS_FRACTION = _float_env("AUTOTRADER_MAX_DAILY_LOSS_FRACTION", 0.04)

# Never let a single position exceed this fraction of total account equity, regardless
# of MAX_POSITION_SIZE_USD.
MAX_POSITION_FRACTION_OF_EQUITY = _float_env("AUTOTRADER_MAX_POSITION_FRACTION", 0.20)

# Minimum confidence (0-1) Claude must report before a buy/sell is acted on at all.
MIN_CONFIDENCE = _float_env("AUTOTRADER_MIN_CONFIDENCE", 0.65)

# --- Execution mode ---
# Real orders are placed ONLY when this is exactly "true" (case-insensitive) in the
# environment. Every other value, including unset, means paper/dry-run mode.
LIVE_TRADING = os.environ.get("LIVE_TRADING", "false").strip().lower() == "true"

# --- Claude model for trade decisions ---
CLAUDE_MODEL = os.environ.get("AUTOTRADER_MODEL", "claude-sonnet-5")

# --- Local state / audit trail ---
STATE_DIR = os.environ.get("AUTOTRADER_STATE_DIR", os.path.dirname(os.path.abspath(__file__)))
TRADE_LOG_PATH = os.path.join(STATE_DIR, "trade_log.csv")
HALT_FILE_PATH = os.path.join(STATE_DIR, "HALT_TRADING")
