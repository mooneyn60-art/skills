#!/usr/bin/env bash
# Restart-safe build of the 3D Meatball explainer (KEY = tiktok | youtube cut). Every step skips work that already exists.
#   [EP=centipede|roach|bedbugs|jumpspider|dustmites|housefly|silverfish|fruitfly|stinkbug|clothesmoth] build.sh [KEY=tiktok|youtube|loop|long]   (delete $W/work/chunk-TAG-*.mp4 after a shot change)
# EP picks the script + page: centipede = explainer.html (bathroom); roach / bedbugs / jumpspider / dustmites = pest.html?ep=EP (ep_*.js).
# Persistent (survives container restarts): $P/vo (voice takes), $P/timeline-KEY.json, $P/out/*.mp4
# Scratch (tmpfs): $W (three.js, fonts, chunk videos). Frames are streamed into ffmpeg, never stored.
set -euo pipefail
KEY=${1:-tiktok}
HERE=$(cd "$(dirname "$0")" && pwd)
P=${MBX_PERSIST:-/home/user/mbx-persist}; W=${MBX_WORK_ROOT:-/dev/shm/mbx}
SD=/home/user/skills/skills/oh-meatball/scripts/explainer; EP=${EP:-centipede}
case $KEY in youtube) PRE=yt; RANGE="--min 15 --max 20";; loop) PRE=yt; RANGE="--min 7 --max 9";; long) PRE=lf; RANGE="--min 240 --max 360";; *) PRE=tt; RANGE="--min 62 --max 65";; esac
VIEW=""; NCH=2
case $EP in
  centipede) SCRIPT=$SD/house-centipede-explainer.json; NAME=meatball-centipede-explainer; TAG=$KEY; TLW=timeline.json; PAGE=src/explainer.html; SHEET=$PRE-contact.jpg;;
  roach) SCRIPT=$SD/cockroach-explainer.json; NAME=roach-explainer; TAG=roach-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=roach&tl=$TLW"; SHEET=$PRE-roach-contact.jpg;;
  bedbugs) SCRIPT=$SD/bed-bugs-explainer.json; NAME=bedbugs-explainer; TAG=bedbugs-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=bedbugs&tl=$TLW"; SHEET=$PRE-bedbugs-contact.jpg;;
  jumpspider) SCRIPT=$SD/jumping-spider-explainer.json; NAME=jumpspider-explainer; TAG=jumpspider-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=jumpspider&tl=$TLW"; SHEET=$PRE-jumpspider-contact.jpg;;
  dustmites) SCRIPT=$SD/dust-mites-explainer.json; NAME=dustmites-explainer; TAG=dustmites-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=dustmites&tl=$TLW"; SHEET=$PRE-dustmites-contact.jpg;;
  housefly) SCRIPT=$SD/house-fly-explainer.json; NAME=housefly-explainer; TAG=housefly-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=housefly&tl=$TLW"; SHEET=$PRE-housefly-contact.jpg;;
  silverfish) SCRIPT=$SD/silverfish-explainer.json; NAME=silverfish-explainer; TAG=silverfish-$KEY; TLW=timeline-$TAG.json; PAGE="src/pest.html?ep=silverfish&tl=$TLW"; SHEET=$PRE-silverfish-contact.jpg;;
  fruitfly|stinkbug|clothesmoth)   # NEW-opening Shorts (research 68); KEY=youtube or loop (7-9 s micro-loop)
    declare -A SN=([fruitfly]=fruit-fly [stinkbug]=stink-bug [clothesmoth]=clothes-moth)
    SCRIPT=$SD/${SN[$EP]}-explainer.json; NAME=$EP-$([ "$KEY" = loop ] && echo loop || echo explainer); TAG=$EP-$KEY; TLW=timeline-$TAG.json
    PAGE="src/pest.html?ep=$EP&tl=$TLW"; SHEET=$PRE-$EP-$KEY-contact.jpg;;
  centlong) KEY=long; PRE=lf; RANGE="--min 240 --max 360"; SCRIPT=$SD/house-centipede-longform.json; NAME=house-centipede-longform; TAG=centlong; TLW=timeline-centlong.json
    PAGE="src/explainer.html?tl=$TLW&wide=1&vfov=30"; SHEET=lf-centlong-contact.jpg; VIEW="--w 1920 --h 1080"; NCH=4;;   # 16:9 long-form (ep_centipede_long.js)
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
  NODE_PATH=/opt/node22/lib/node_modules node src/render.js --page "$PAGE" $VIEW --out "work/chunk-$TAG-$1.part.mp4" --from "$2" --to "$3" > "work/chunk-$TAG-$1.log" 2>&1
  mv "work/chunk-$TAG-$1.part.mp4" "$f"
}
pids=(); : > work/concat-$TAG.txt
for c in $(seq 0 $((NCH - 1))); do   # chunk edges on whole frames
  a=$(python3 -c "print(round(round($TOTAL*30*$c/$NCH)/30, 4))"); b=$(python3 -c "print(round(round($TOTAL*30*($c+1)/$NCH)/30, 4))")
  [ "$c" = $((NCH - 1)) ] && b=$TOTAL
  render "$c" "$a" "$b" & pids+=($!); echo "file 'chunk-$TAG-$c.mp4'" >> work/concat-$TAG.txt
done
for p in "${pids[@]}"; do wait "$p"; done
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
