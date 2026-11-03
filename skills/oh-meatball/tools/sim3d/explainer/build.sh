#!/usr/bin/env bash
# Restart-safe build of the 3D Meatball explainer (KEY = tiktok | youtube cut). Every step skips work that already exists.
#   build.sh [KEY=tiktok]   (delete $W/work/chunk-KEY-*.mp4 after a shot change)
# Persistent (survives container restarts): $P/vo (voice takes), $P/timeline-KEY.json, $P/out/*.mp4
# Scratch (tmpfs): $W (three.js, fonts, chunk videos). Frames are streamed into ffmpeg, never stored.
set -euo pipefail
KEY=${1:-tiktok}
HERE=$(cd "$(dirname "$0")" && pwd)
P=${MBX_PERSIST:-/home/user/mbx-persist}; W=${MBX_WORK_ROOT:-/dev/shm/mbx}
SCRIPT=/home/user/skills/skills/oh-meatball/scripts/explainer/house-centipede-explainer.json
case $KEY in youtube) PRE=yt; RANGE="--min 15 --max 20";; *) PRE=tt; RANGE="--min 62 --max 65";; esac
OUT=$P/out/$PRE-meatball-centipede-explainer.mp4
mkdir -p "$P/vo" "$P/out" "$W/work"
[ -d "$W/node_modules/three" ] || bash "$HERE/../setup.sh" "$W"
cp "$HERE/../"*.js "$W/src/"; cp "$HERE"/*.js "$HERE"/*.html "$W/src/"
export MBX_PERSIST=$P MBX_WORK=$W/work
if [ ! -f "$P/timeline-$KEY.json" ] || [ ! -f "$W/work/premaster-$KEY.wav" ] || [ ! -f "$W/work/vo-$KEY.wav" ]; then
  python3 "$HERE/explainer_audio.py" "$SCRIPT" "$KEY"
fi
cp "$P/timeline-$KEY.json" "$W/work/timeline.json"
TOTAL=$(python3 -c "import json;print(json.load(open('$P/timeline-$KEY.json'))['total'])")
MID=$(python3 -c "print(round(round($TOTAL*30/2)/30, 4))")
cd "$W"
render() { # chunk index, from, to
  local f="work/chunk-$KEY-$1.mp4"
  [ -f "$f" ] && return 0
  NODE_PATH=/opt/node22/lib/node_modules node src/render.js --page src/explainer.html --out "work/chunk-$KEY-$1.part.mp4" --from "$2" --to "$3" > "work/chunk-$KEY-$1.log" 2>&1
  mv "work/chunk-$KEY-$1.part.mp4" "$f"
}
render 0 0 "$MID" & p0=$!
render 1 "$MID" "$TOTAL" & p1=$!
wait $p0; wait $p1
printf "file 'chunk-%s-0.mp4'\nfile 'chunk-%s-1.mp4'\n" "$KEY" "$KEY" > work/concat-$KEY.txt
ffmpeg -v error -y -f concat -safe 0 -i work/concat-$KEY.txt -c copy work/video-$KEY.mp4
# master: -14 LUFS integrated, limiter ceiling -1.5 dBFS (true peak stays under -1 dBFS after AAC)
G=$(python3 -c "
import numpy as np, pyloudnorm, soundfile as sf
x, sr = sf.read('$W/work/premaster-$KEY.wav'); print(round(-14.0 - pyloudnorm.Meter(sr).integrated_loudness(x) + float('${TRIM:-0}'), 2))")
TMP=$P/out/.$PRE-$KEY.tmp.mp4
ffmpeg -v error -y -i work/video-$KEY.mp4 -i "work/premaster-$KEY.wav" -map 0:v -map 1:a -c:v copy \
  -af "volume=${G}dB,alimiter=limit=0.84:attack=3:release=60:level=false" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$TMP"
mv "$TMP" "$OUT"
python3 "$HERE/checks.py" "$OUT" "$P/timeline-$KEY.json" "work/vo-$KEY.wav" $RANGE | tee "$P/out/checks-$KEY.json"
bash "$HERE/../contact.sh" "$OUT" "$P/out/$PRE-contact.jpg" >/dev/null
echo "done $OUT gain ${G} dB"
