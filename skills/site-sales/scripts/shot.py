#!/usr/bin/env python3
"""Screenshot a built site at phone width (390px) with Playwright.

Usage:
    python shot.py sites/<slug>/index.html                  # -> sites/<slug>/shot-390.png (full page)
    python shot.py sites/*/index.html --fold                # also save the first screen (shot-390-fold.png)

Uses the Chromium already on the machine (PW_CHROMIUM env var, or
/opt/pw-browsers/chromium if present). Never runs `playwright install`.
Also reports horizontal overflow, which is the most common mobile bug.
"""

import argparse
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

CANDIDATES = [os.environ.get("PW_CHROMIUM"), "/opt/pw-browsers/chromium"]


def chromium_path() -> str | None:
    for c in CANDIDATES:
        if not c:
            continue
        p = Path(c)
        if p.is_file() and os.access(p, os.X_OK):
            return str(p)
        if p.is_dir():  # a browsers dir: find the chrome binary inside
            for name in ("chrome", "chromium", "headless_shell"):
                hits = sorted(p.rglob(name))
                hits = [h for h in hits if h.is_file() and os.access(h, os.X_OK)]
                if hits:
                    return str(hits[0])
    return None  # let Playwright use its own registered browser


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pages", nargs="+", type=Path)
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--fold", action="store_true", help="also save a first-screen-only image")
    args = ap.parse_args()

    exe = chromium_path()
    problems = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": args.width, "height": args.height},
                                  device_scale_factor=2, is_mobile=True, has_touch=True)
        for page_path in args.pages:
            page = ctx.new_page()
            page.goto(page_path.resolve().as_uri(), wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(400)
            overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            msg = "wrote"
            if args.fold:  # first screen as a visitor sees it, floating button included
                fold = page_path.with_name(f"shot-{args.width}-fold.png")
                page.screenshot(path=str(fold))
                msg += f" {fold}"
            # Fixed elements repeat over the stitched full-page image, so hide them there.
            page.add_style_tag(content=".fab{display:none!important}.topbar{position:static!important}")
            out = page_path.with_name(f"shot-{args.width}.png")
            page.screenshot(path=str(out), full_page=True)
            msg += f" {out}"
            if overflow > 0:
                problems += 1
                msg += f"  WARNING: horizontal overflow {overflow}px"
            print(msg)
            page.close()
        browser.close()
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
