#!/usr/bin/env bash
# sim3d: low-poly 3D what-if Shorts. Sets up a work dir (default /dev/shm/sim3d, tmpfs) with this source,
# three.js 0.160.0 and the Lora font, then prints the render commands.
#   tools/sim3d/setup.sh [WORKDIR]
# Render (deterministic, 30 fps, 1080x1920 out; 3D drawn at 540x960 and upscaled, text at full res):
#   node src/render.js --out work/a.mp4 --from 0 --to 20      # split into 2-3 chunks and run them in parallel
#   node src/render.js --stills 1,12,30 --outdir work/st      # quick JPEG checks
#   python3 src/music_bed.py work/bed.wav; python3 src/mix.py work/video.mp4 work/bed.wav final/out.mp4
#   bash src/contact.sh final/out.mp4 work/sheet.jpg [/dev/shm/ref3/s2.jpg work/side.jpg]
# Meatball dialogue test: python3 src/meatball_audio.py; node src/render.js --page src/meatball.html --out work/mb.mp4
set -euo pipefail
W=${1:-/dev/shm/sim3d}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W/src" "$W/fonts" "$W/work" "$W/final"
cp "$HERE"/*.js "$HERE"/*.html "$HERE"/*.py "$HERE"/*.sh "$HERE"/credits.txt "$W/src/"
cd "$W"
[ -d node_modules/three ] || { npm init -y >/dev/null; npm i --silent three@0.160.0; }
cd "$W/fonts"
if [ ! -f fonts.css ]; then
  curl -sS -A "Mozilla/5.0" "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" > lora.css
  for u in $(grep -o "https://[^)]*" lora.css | sort -u); do curl -sS -O "$u"; done
  sed -E 's#https://fonts.gstatic.com/s/lora/v[0-9]+/##' lora.css > fonts.css
fi
echo "sim3d ready in $W"
