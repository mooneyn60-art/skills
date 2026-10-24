"""Pulls account state and watchlist market data from Robinhood via robin_stocks."""
from dataclasses import dataclass, field


@dataclass
class AccountState:
    equity: float
    buying_power: float
    positions: dict = field(default_factory=dict)  # symbol -> {quantity, avg_cost, market_value}


@dataclass
class SymbolSnapshot:
    symbol: str
    price: float
    change_pct_today: float
    recent_closes: list  # last N daily closes, oldest first


def get_account_state(rh) -> AccountState:
    profile = rh.profiles.load_account_profile()
    portfolio = rh.profiles.load_portfolio_profile()

    equity = float(portfolio.get("equity") or 0.0)
    buying_power = float(profile.get("buying_power") or portfolio.get("withdrawable_amount") or 0.0)

    positions = {}
    for holding_symbol, holding in (rh.build_holdings() or {}).items():
        positions[holding_symbol] = {
            "quantity": float(holding.get("quantity") or 0.0),
            "avg_cost": float(holding.get("average_buy_price") or 0.0),
            "market_value": float(holding.get("equity") or 0.0),
        }

    return AccountState(equity=equity, buying_power=buying_power, positions=positions)


def get_watchlist_snapshots(rh, symbols: list) -> list:
    snapshots = []
    quotes = rh.stocks.get_quotes(symbols) or []
    quotes_by_symbol = {q["symbol"]: q for q in quotes if q and q.get("symbol")}

    for symbol in symbols:
        quote = quotes_by_symbol.get(symbol)
        if not quote:
            # No real quote available for this symbol right now — skip it rather than
            # fabricate a price. See CLAUDE.md RULE #1 in the lumibot repo for why:
            # missing data must stay missing, never be filled in with a guess.
            continue

        price = float(quote.get("last_trade_price") or 0.0)
        prev_close = float(quote.get("adjusted_previous_close") or quote.get("previous_close") or 0.0)
        change_pct = ((price - prev_close) / prev_close * 100.0) if prev_close else 0.0

        historicals = rh.stocks.get_stock_historicals(
            symbol, interval="day", span="month", bounds="regular"
        ) or []
        recent_closes = [
            float(bar["close_price"])
            for bar in historicals
            if bar and bar.get("close_price")
        ]

        snapshots.append(
            SymbolSnapshot(
                symbol=symbol,
                price=price,
                change_pct_today=change_pct,
                recent_closes=recent_closes[-20:],
            )
        )

    return snapshots
