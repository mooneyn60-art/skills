#!/usr/bin/env python3
"""Variant (a): pullback entry. Prints data only (R14.1)."""
from mom_screen_base import hurdles

if __name__ == "__main__":
    hurdles("variant a pullback", "LONG", entry_mode="pullback")
    hurdles("variant a pullback", "WIDE", entry_mode="pullback")
