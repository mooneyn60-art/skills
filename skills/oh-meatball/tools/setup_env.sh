#!/usr/bin/env bash
# Make a fresh cloud machine ready for the channel tools. About two minutes; safe to run again.
#   bash skills/oh-meatball/tools/setup_env.sh
# It installs only what is missing, downloads the speech model the voice check uses, and runs postkit selftest.
# It ends with "ready" (exit 0) only when every step worked; otherwise "NOT READY: n problems" (exit 1).
set -u
here="$(cd "$(dirname "$0")" && pwd)"
fail=0
problem() { echo "FAIL $*"; fail=$((fail + 1)); }

command -v python3 >/dev/null || { echo "FAIL no python3 (apt-get install -y python3 python3-pip)"; echo "NOT READY: 1 problems"; exit 1; }
python3 -m pip --version >/dev/null 2>&1 || problem "no pip for python3 (apt-get install -y python3-pip)"

need=$(python3 - <<'PY'
import importlib.util
mods = {"faster_whisper": "faster-whisper", "soundfile": "soundfile", "edge_tts": "edge-tts", "PIL": "pillow",
        "numpy": "numpy", "scipy": "scipy", "yaml": "pyyaml", "cairo": "pycairo", "pyloudnorm": "pyloudnorm",
        "pandas": "pandas", "yt_dlp": "yt-dlp"}
print(" ".join(pkg for mod, pkg in mods.items() if importlib.util.find_spec(mod) is None))
PY
)
rest=$(echo " $need " | sed 's/ pycairo / /; s/^ *//; s/ *$//')
pip_hint="(if pip says externally-managed-environment, use a venv: python3 -m venv ~/venv && . ~/venv/bin/activate, then run this again)"

# Everything but pycairo first: pycairo has no Linux wheel and builds from source, and one failed build makes
# pip install nothing at all from the same command.
if [ -n "$rest" ]; then
  echo "installing: $rest"
  python3 -m pip install -q $rest || problem "pip install $rest $pip_hint"
fi

case " $need " in
  *" pycairo "*)
    echo "installing: pycairo (built from source)"
    missing=""
    command -v pkg-config >/dev/null || missing="$missing pkg-config"
    pkg-config --exists cairo 2>/dev/null || missing="$missing libcairo2-dev"
    python3 - <<'PY' 2>/dev/null || missing="$missing python3-dev"
import os, sysconfig, sys
sys.exit(0 if os.path.exists(os.path.join(sysconfig.get_paths()["include"], "Python.h")) else 1)
PY
    if [ -n "$missing" ]; then
      problem "pycairo needs system packages first: apt-get install -y$missing"
    else
      python3 -m pip install -q pycairo || problem "pip install pycairo $pip_hint"
    fi
    ;;
esac

for t in ffmpeg ffprobe curl git; do
  command -v "$t" >/dev/null || problem "missing system tool: $t (apt-get install -y $([ "$t" = ffprobe ] && echo ffmpeg || echo "$t"))"
done
# pip may put yt-dlp in ~/.local/bin, which is often not on PATH
if ! command -v yt-dlp >/dev/null; then
  if [ -x "$HOME/.local/bin/yt-dlp" ]; then
    problem "yt-dlp is in ~/.local/bin, which is not on PATH (export PATH=\"\$HOME/.local/bin:\$PATH\")"
  else
    problem "missing yt-dlp (python3 -m pip install yt-dlp)"
  fi
fi

python3 - <<'PY' || problem "speech model small.en did not load (needs faster-whisper and a network the first time)"
from faster_whisper import WhisperModel
WhisperModel("small.en", device="cpu", compute_type="int8")   # downloads once, then loads from the cache
PY

python3 - <<'PY' || problem "a Python package still does not import (see the error above)"
import faster_whisper, soundfile, edge_tts, PIL, numpy, scipy, yaml, cairo, pyloudnorm, pandas, yt_dlp
PY

python3 "$here/postkit.py" selftest >/dev/null || problem "postkit selftest (run: python3 $here/postkit.py selftest)"

if [ "$fail" -eq 0 ]; then
  echo "ready"
  exit 0
fi
echo "NOT READY: $fail problems"
exit 1
