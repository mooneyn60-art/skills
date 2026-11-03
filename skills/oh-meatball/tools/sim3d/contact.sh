#!/usr/bin/env bash
# 1 fps contact sheet (10 per row, same cell size as the reference sheets) + a side-by-side with a reference sheet.
# contact.sh VIDEO OUT.jpg [REFERENCE.jpg SIDE_BY_SIDE.jpg]
set -euo pipefail
v=$1; out=$2
n=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v" | awk '{print int($1+0.999)}')
rows=$(( (n + 9) / 10 ))
ffmpeg -v error -y -i "$v" -vf "fps=1,scale=180:320,tile=10x${rows}:padding=0" -frames:v 1 -q:v 3 "$out"
if [ $# -ge 4 ]; then
  ffmpeg -v error -y -i "$3" -i "$out" -filter_complex \
    "[0]scale=-2:2000,pad=iw+20:2060:0:60:color=white,drawtext=text='REFERENCE':x=10:y=14:fontsize=34:fontcolor=black[a];[1]scale=-2:2000,pad=iw:2060:0:60:color=white,drawtext=text='OURS':x=10:y=14:fontsize=34:fontcolor=black[b];[a][b]hstack=inputs=2" \
    -q:v 3 "$4"
fi
echo "$out"
