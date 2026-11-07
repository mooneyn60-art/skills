#!/usr/bin/env bash
# Restart-safe build of the 3D Meatball explainer (KEY = tiktok | youtube cut). Every step skips work that already exists.
#   [EP=centipede|roach|bedbugs|jumpspider|dustmites|housefly] build.sh [KEY=tiktok]   (delete $W/work/chunk-TAG-*.mp4 after a shot change)
# EP picks the script + page: centipede = explainer.html (bathroom); roach / bedbugs / jumpspider / dustmites = pest.html?ep=EP (ep_*.js).
# Persistent (survives container restarts): $P/vo (voice takes), $P/timeline-KEY.json, $P/out/*.mp4
# Scratch (tmpfs): $W (three.js, fonts, chunk videos). Frames are streamed into ffmpeg, never stored.
set -euo pipefail
KEY=${1:-tiktok}
HERE=$(cd "$(dirname "$0")" && pwd)
P=${MBX_PERSIST:-/home/user/mbx-persist}; W=${MBX_WORK_ROOT:-/dev/shm/mbx}
SD=/home/user/skills/skills/oh-meatball/scripts/explainer; EP=${EP:-centipede}
case $KEY in youtube) PRE=yt; RANGE="--min 15 --max 20";; *) PRE=tt; RANGE="--min 62 --max 65";; esac
case $EP in
  centipede) SCRIPT=$SD/house-centipede-explainer.json; NAME=meatball-centipede-explainer; TAG=$KEY; TLW=timeline.json; PAGE=src/explainer.html; SHEET=$PRE-contact.jpg;;
  roach) SCRIPT=$SD/cockroach-explainer.json; NAME=roach-explainer; TAG=roach-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=roach&tl=$TLW"; SHEET=$PRE-roach-contact.jpg;;
  bedbugs) SCRIPT=$SD/bed-bugs-explainer.json; NAME=bedbugs-explainer; TAG=bedbugs-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=bedbugs&tl=$TLW"; SHEET=$PRE-bedbugs-contact.jpg;;
  jumpspider) SCRIPT=$SD/jumping-spider-explainer.json; NAME=jumpspider-explainer; TAG=jumpspider-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=jumpspider&tl=$TLW"; SHEET=$PRE-jumpspider-contact.jpg;;
  dustmites) SCRIPT=$SD/dust-mites-explainer.json; NAME=dustmites-explainer; TAG=dustmites-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=dustmites&tl=$TLW"; SHEET=$PRE-dustmites-contact.jpg;;
  housefly) SCRIPT=$SD/house-fly-explainer.json; NAME=housefly-explainer; TAG=housefly-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=housefly&tl=$TLW"; SHEET=$PRE-housefly-contact.jpg;;
  silverfish) SCRIPT=$SD/silverfish-explainer.json; NAME=silverfish-explainer; TAG=silverfish-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=silverfish&tl=$TLW"; SHEET=$PRE-silverfish-contact.jpg;;
  *) echo "unknown EP $EP"; exit 2;;
esac
OUT=$P/out/$PRE-$NAME.mp4
mkdir -p "$P/vo" "$P/out" "$W/work"
[ -d "$W/node_modules/three" ] || bash "$HERE/../setup.sh" "$W"
cp "$HERE/../"*.js "$W/src/"; cp "$HERE"/*.js "$HERE"/*.html "$W/src/"
export MBX_PERSIST=$P MBX_WORK=$W/work
if [ ! -f "$P/timeline-$TAG.json" ] || [ ! -f "$W/work/premaster-$TAG.wav" ] || [ ! -f "$W/work/vo-$TAG.wav" ]; then
  python3 "$HERE/explainer_audio.py" "$SCRIPT" "$KEY" "$TAG"
fi
cp "$P/timeline-$TAG.json" "$W/work/$TLW"
TOTAL=$(python3 -c "import json;print(json.load(open('$P/timeline-$TAG.json'))['total'])")
MID=$(python3 -c "print(round(round($TOTAL*30/2)/30, 4))")
cd "$W"
render() { # chunk index, from, to
  local f="work/chunk-$TAG-$1.mp4"
  [ -f "$f" ] && return 0
  NODE_PATH=/opt/node22/lib/node_modules node src/render.js --page "$PAGE" --out "work/chunk-$TAG-$1.part.mp4" --from "$2" --to "$3" > "work/chunk-$TAG-$1.log" 2>&1
  mv "work/chunk-$TAG-$1.part.mp4" "$f"
}
render 0 0 "$MID" & p0=$!
render 1 "$MID" "$TOTAL" & p1=$!
wait $p0; wait $p1
printf "file 'chunk-%s-0.mp4'\nfile 'chunk-%s-1.mp4'\n" "$TAG" "$TAG" > work/concat-$TAG.txt
ffmpeg -v error -y -f concat -safe 0 -i work/concat-$TAG.txt -c copy work/video-$TAG.mp4
# master: -14 LUFS integrated, limiter ceiling -1.5 dBFS (true peak stays under -1 dBFS after AAC)
G=$(python3 -c "
import numpy as np, pyloudnorm, soundfile as sf
x, sr = sf.read('$W/work/premaster-$TAG.wav'); print(round(-14.0 - pyloudnorm.Meter(sr).integrated_loudness(x) + float('${TRIM:-0}'), 2))")
TMP=$P/out/.$PRE-$TAG.tmp.mp4
ffmpeg -v error -y -i work/video-$TAG.mp4 -i "work/premaster-$TAG.wav" -map 0:v -map 1:a -c:v copy \
  -af "volume=${G}dB,alimiter=limit=0.84:attack=3:release=60:level=false" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$TMP"
mv "$TMP" "$OUT"
python3 "$HERE/checks.py" "$OUT" "$P/timeline-$TAG.json" "work/vo-$TAG.wav" $RANGE | tee "$P/out/checks-$TAG.json"
bash "$HERE/../contact.sh" "$OUT" "$P/out/$SHEET" >/dev/null
echo "done $OUT gain ${G} dB"
