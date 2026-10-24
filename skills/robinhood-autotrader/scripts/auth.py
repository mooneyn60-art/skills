"""Robinhood login via robin_stocks, using a TOTP secret so no manual 2FA code is
needed on each run.

Credentials come from the environment only. Never hardcode them, never log them, and
never print robin_stocks' own login response (it can include session tokens).
"""
import os
import sys

import pyotp
import robin_stocks.robinhood as rh


REQUIRED_ENV_VARS = ("ROBINHOOD_USERNAME", "ROBINHOOD_PASSWORD", "ROBINHOOD_TOTP_SECRET")


def login():
    """Log into Robinhood and return the robin_stocks module, ready to use.

    Exits with a clear error if required credentials are missing, rather than letting
    robin_stocks fail deeper in the call stack with a less obvious error.
    """
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        sys.exit(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in your own Robinhood credentials."
        )

    username = os.environ["ROBINHOOD_USERNAME"]
    password = os.environ["ROBINHOOD_PASSWORD"]
    totp_secret = os.environ["ROBINHOOD_TOTP_SECRET"]

    mfa_code = pyotp.TOTP(totp_secret).now()
    rh.login(username=username, password=password, mfa_code=mfa_code, store_session=True)
    return rh


def logout():
    import robin_stocks.robinhood as rh
    rh.logout()
