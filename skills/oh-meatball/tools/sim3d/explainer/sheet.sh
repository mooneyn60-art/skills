#!/usr/bin/env bash
# Tile a directory of render.js stills (t<seconds>.jpg) into labelled sheets of 18, in time order.
#   sheet.sh STILLS_DIR OUT_PREFIX
set -euo pipefail
d=$1; out=$2
mapfile -t files < <(for f in "$d"/t*.jpg; do b=$(basename "$f" .jpg); printf '%010.3f %s\n' "${b#t}" "$f"; done | sort -n | cut -d' ' -f2)
for ((s=0; s*18<${#files[@]}; s++)); do
  sub=("${files[@]:$((s*18)):18}"); k=${#sub[@]}; fc=""; lay=""; ins=()
  for ((j=0;j<k;j++)); do b=$(basename "${sub[$j]}" .jpg); ins+=(-i "${sub[$j]}"); fc+="[$j]scale=240:426,drawtext=text='${b#t}':x=6:y=6:fontsize=22:fontcolor=red[s$j];"; done
  for ((j=0;j<k;j++)); do fc+="[s$j]"; lay+="$(( (j%9)*240 ))_$(( (j/9)*426 ))"; [ $j -lt $((k-1)) ] && lay+="|"; done
  ffmpeg -v error -y "${ins[@]}" -filter_complex "${fc}xstack=inputs=$k:layout=$lay:fill=black" -frames:v 1 -q:v 3 "${out}$s.jpg"
  echo "${out}$s.jpg"
done
