#!/usr/bin/env bash
# Make a fresh cloud machine ready for the channel tools. About two minutes; safe to run again.
#   bash skills/oh-meatball/tools/setup_env.sh
# It installs only what is missing, downloads the speech model the voice check uses, and ends with "ready".
set -u
need=$(python3 - <<'PY'
import importlib.util
mods = {"faster_whisper": "faster-whisper", "soundfile": "soundfile", "edge_tts": "edge-tts", "PIL": "pillow",
        "numpy": "numpy", "scipy": "scipy", "yaml": "pyyaml", "cairo": "pycairo", "pyloudnorm": "pyloudnorm",
        "pandas": "pandas", "yt_dlp": "yt-dlp"}
print(" ".join(pkg for mod, pkg in mods.items() if importlib.util.find_spec(mod) is None))
PY
)
if [ -n "$need" ]; then
  echo "installing: $need"
  pip install -q $need || echo "FAIL pip install (pycairo needs: apt-get install -y libcairo2-dev pkg-config python3-dev)"
fi
for t in ffmpeg ffprobe curl git yt-dlp; do
  command -v "$t" >/dev/null || echo "MISSING system tool: $t"
done
python3 - <<'PY' || echo "FAIL speech model"
from faster_whisper import WhisperModel
WhisperModel("small.en", device="cpu", compute_type="int8")   # downloads once, then loads from the cache
PY
python3 "$(dirname "$0")/postkit.py" --help >/dev/null && echo "ready"
