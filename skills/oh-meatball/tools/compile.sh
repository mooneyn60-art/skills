#!/usr/bin/env bash
# compile.sh OUT ORIENTATION CLIP1 CLIP2 ...
# ORIENTATION: vertical (720x1280 Shorts, warns over 60 s) | horizontal (1920x1080, blurred-fill background)
# Clips play in the given order with a "#N ... #1" countdown overlay for the first 2 s of each; hard cuts.
# Env: CRF (default 20), COUNTDOWN=0 to disable overlay, BOLD_FONT
set -euo pipefail
[[ $# -lt 3 ]] && { sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
OUT=$1; ORIENT=$2; shift 2; CLIPS=("$@"); N=${#CLIPS[@]}
FONT=${BOLD_FONT:-/usr/share/fonts/truetype/freefont/FreeSansBold.ttf}
CRF=${CRF:-20}; COUNTDOWN=${COUNTDOWN:-1}
case $ORIENT in
  vertical)   W=720;  H=1280; FS=150;;
  horizontal) W=1920; H=1080; FS=170;;
  *) echo "compile: ORIENTATION must be vertical|horizontal" >&2; exit 1;;
esac
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
INPUTS=(); FG=""; CAT=""; TOTAL=0; idx=0
for i in "${!CLIPS[@]}"; do
  c=${CLIPS[$i]}; [[ -f $c ]] || { echo "compile: missing clip $c" >&2; exit 1; }
  D=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$c" | head -1)
  [[ -z $D || $D == N/A ]] && D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$c")
  TOTAL=$(awk -v a="$TOTAL" -v b="$D" 'BEGIN{print a+b}')
  INPUTS+=(-i "$c"); vin=$idx; idx=$((idx+1))
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$c" | grep -q .; then ain="$vin:a:0"
  else INPUTS+=(-f lavfi -i "anullsrc=r=48000:cl=stereo"); ain="$idx:a"; idx=$((idx+1)); fi
  num=$((N-i)); printf '#%d' "$num" > "$TMP/n$i.txt"
  V="[$vin:v]trim=duration=$D,setpts=PTS-STARTPTS,fps=30"
  if [[ $ORIENT == vertical ]]; then
    V+=",scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,format=yuv420p"
  else
    V+=",split[f$i][b$i];[b$i]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,gblur=sigma=12,eq=brightness=-0.10:saturation=1.2,scale=$W:$H,setsar=1[bg$i];"
    V+="[f$i]scale=-2:$H,setsar=1[fg$i];[bg$i][fg$i]overlay=(W-w)/2:0,format=yuv420p"
  fi
  [[ $COUNTDOWN == 1 ]] && V+=",drawtext=fontfile=$FONT:textfile=$TMP/n$i.txt:fontsize=$FS:fontcolor=yellow:borderw=10:bordercolor=black:x=(w-tw)/2:y=h*0.06:enable='lt(t,2)'"
  FG+="$V[v$i];"
  # Normalize every clip's audio (any rate/layout) to 48 kHz stereo and pin it to the video length.
  FG+="[$ain]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,asetpts=PTS-STARTPTS,apad,atrim=duration=$D[a$i];"
  CAT+="[v$i][a$i]"
done
FG+="${CAT}concat=n=$N:v=1:a=1[vc][ac];[ac]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[ao]"
printf '%s' "$FG" > "$TMP/fc.txt"
if [[ $ORIENT == vertical ]] && awk -v t="$TOTAL" 'BEGIN{exit !(t>60)}'; then
  echo "compile: WARNING total ${TOTAL}s exceeds the 60 s Shorts limit" >&2; fi
ffmpeg -v error -y "${INPUTS[@]}" -filter_complex_script "$TMP/fc.txt" -map "[vc]" -map "[ao]" \
  -c:v libx264 -preset medium -crf "$CRF" -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart "$OUT"
echo "compile: wrote $OUT ($ORIENT, $N clips, ${TOTAL}s)"
