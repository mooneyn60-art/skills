#!/usr/bin/env python3
"""16:9 drawn cut-ins for the long-forms (Nolan 11/2: the case-file mix look inside a 1920x1080 video).

Runs a drawn_casefile spec at 1920x1080 instead of 1080x1920 (drawn.py reads its frame size from drawn.W/H):
  python3 tools/drawn_wide.py SPEC.json OUT.mp4 --work DIR [--stills 1,3] [--nocap OUT_NOCAP.mp4]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn  # noqa: E402

drawn.W, drawn.H = 1920, 1080
import drawn_casefile  # noqa: E402

if __name__ == "__main__":
    drawn_casefile.setup(sys.argv[1])
    drawn.main()
