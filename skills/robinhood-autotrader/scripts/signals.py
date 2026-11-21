"""Turns a market snapshot into structured trade decisions using the anthropic SDK.

Uses tool-calling so the response is a parseable list of decisions rather than free
text that has to be regex'd apart.
"""
import json
import os

import anthropic

import config


DECISION_TOOL = {
    "name": "report_trade_decisions",
    "description": "Report a buy/sell/hold decision for each symbol in the watchlist.",
    "input_schema": {
        "type": "object",
        "properties": {
            "decisions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "action": {"type": "string", "enum": ["buy", "sell", "hold"]},
                        "confidence": {
                            "type": "number",
                            "description": "0.0-1.0 confidence in this decision",
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "1-3 sentence justification grounded in the "
                            "provided data only",
                        },
                    },
                    "required": ["symbol", "action", "confidence", "reasoning"],
                },
            }
        },
        "required": ["decisions"],
    },
}

SYSTEM_PROMPT = """You help decide trades for a moderate-risk equities account.

Rules:
- Base decisions ONLY on the data provided in the user message. Never invent prices,
  news, or fundamentals you were not given.
- If the data given for a symbol is insufficient to form a view, decide "hold" with
  low confidence rather than guessing.
- This account has real money and moderate risk tolerance: prefer well-reasoned,
  conservative sizing signals over speculative or high-confidence claims you can't
  support from the data.
- "sell" only applies to symbols the account currently holds; report "hold" for
  symbols with no position if you would not open one.
- Call report_trade_decisions exactly once with one entry per symbol you were given.
"""


def get_decisions(account_state, snapshots) -> list:
    """Returns a list of dicts: {symbol, action, confidence, reasoning}."""
    if not snapshots:
        return []

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    positions_summary = {
        symbol: pos["quantity"] for symbol, pos in account_state.positions.items()
    }
    market_summary = [
        {
            "symbol": s.symbol,
            "price": s.price,
            "change_pct_today": round(s.change_pct_today, 2),
            "recent_closes": s.recent_closes,
        }
        for s in snapshots
    ]

    user_content = (
        f"Account equity: {account_state.equity:.2f}\n"
        f"Buying power: {account_state.buying_power:.2f}\n"
        f"Current positions (symbol: shares): {json.dumps(positions_summary)}\n\n"
        f"Watchlist market data:\n{json.dumps(market_summary, indent=2)}"
    )

    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        tools=[DECISION_TOOL],
        tool_choice={"type": "tool", "name": "report_trade_decisions"},
        messages=[{"role": "user", "content": user_content}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "report_trade_decisions":
            return block.input.get("decisions", [])

    return []
