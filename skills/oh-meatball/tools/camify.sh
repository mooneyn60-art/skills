#!/usr/bin/env bash
# camify.sh IN OUT PRESET [LABEL] [DATETIME]
# Presets: doorbell_night | security_day | dashcam | phone
# DATETIME: anything `date -d` understands, e.g. "2026-10-14 03:12:44" (default: random recent night/day time)
# Env: CRF (default 20), SPEED (dashcam text, default "34 MPH"), MONO_FONT
set -euo pipefail
source "$(dirname "$0")/lib.sh"
usage(){ sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
[[ $# -lt 3 ]] && usage
IN=$1; OUT=$2; PRESET=$3; LABEL=${4:-}; DT=${5:-}
[[ -f $IN ]] || { echo "camify: input not found: $IN" >&2; exit 1; }
FONT=${MONO_FONT:-/usr/share/fonts/truetype/freefont/FreeMono.ttf}
BFONT=/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf; [[ -f $BFONT ]] || BFONT=$FONT
CRF=${CRF:-20}; SPEED=${SPEED:-34 MPH}

if [[ -z $DT ]]; then
  case $PRESET in doorbell_night) DT="$(date -d '-2 day' +%F) 03:$((RANDOM%50+10)):$((RANDOM%50+10))";;
                  *) DT="$(date -d '-2 day' +%F) 1$((RANDOM%6+1)):$((RANDOM%50+10)):$((RANDOM%50+10))";; esac
fi
EPOCH=$(date -u -d "$DT" +%s) || { echo "camify: bad DATETIME: $DT" >&2; exit 1; }

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
printf '%s' "$LABEL" > "$TMP/label.txt"; printf '%s' "$SPEED" > "$TMP/speed.txt"
# Timestamp ticks in real time: pts offset from EPOCH, rendered in UTC so DATETIME is shown verbatim.
ts(){ # $1=strftime fmt (colons pre-escaped)  $2=extra drawtext opts
  echo "drawtext=fontfile=$BFONT:text='%{pts\\:gmtime\\:$EPOCH\\:$1}':$2"; }
lbl(){ [[ -n $LABEL ]] && echo ",drawtext=fontfile=$BFONT:textfile=$TMP/label.txt:$1" || true; }
HMS='%H\\\:%M\\\:%S'
BASE="scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
SH="shadowcolor=black@0.8:shadowx=2:shadowy=2"

case $PRESET in
  doorbell_night)
    V="$BASE,format=gray,eq=contrast=1.35:brightness=0.06:gamma=1.15,lenscorrection=k1=0.28:k2=0.06,crop=640:1138,scale=720:1280,format=yuv420p,vignette=angle=PI/3.2,noise=alls=28:allf=t+u,gblur=sigma=0.6,"
    V+="$(ts "%m/%d/%Y $HMS" "fontsize=34:fontcolor=white:x=24:y=40:$SH")"
    V+="$(lbl "fontsize=34:fontcolor=white:x=w-tw-24:y=h-th-48:$SH")"
    V+=",drawtext=fontfile=$BFONT:text='● LIVE':fontsize=28:fontcolor=red:x=w-tw-24:y=40" ;;
  security_day)
    V="$BASE,eq=saturation=0.72:contrast=1.08,unsharp=5:5:-0.4,noise=alls=12:allf=t+u,format=yuv420p,"
    V+="$(ts "%Y-%m-%d $HMS" "fontsize=32:fontcolor=white:x=20:y=28:box=1:boxcolor=black@0.45:boxborderw=6")"
    V+="$(lbl "fontsize=32:fontcolor=white:x=20:y=h-th-40:box=1:boxcolor=black@0.45:boxborderw=6")"
    V+=",drawtext=fontfile=$BFONT:text='REC':fontsize=28:fontcolor=red:x=w-tw-24:y=30:enable='lt(mod(t\\,1)\\,0.6)'" ;;
  dashcam)
    V="$BASE,lenscorrection=k1=0.18:k2=0.04,crop=630:1120,scale=720:1280,eq=saturation=0.9:contrast=1.05,gblur=sigma=0.9,noise=alls=8:allf=t+u,format=yuv420p,"
    V+="$(ts "%Y/%m/%d $HMS" "fontsize=30:fontcolor=white:x=20:y=h-th-36:$SH")"
    V+=",drawtext=fontfile=$BFONT:textfile=$TMP/speed.txt:fontsize=30:fontcolor=white:x=w-tw-20:y=h-th-36:$SH"
    V+="$(lbl "fontsize=26:fontcolor=white:x=20:y=30:$SH")" ;;
  phone)
    # Handheld shake: animated crop window, re-scaled to full frame.
    V="$BASE,crop=684:1216:x='18+9*sin(2*PI*t*1.1)+5*sin(2*PI*t*2.7)':y='32+12*sin(2*PI*t*0.9+1)+5*sin(2*PI*t*3.1)',scale=720:1280,noise=alls=7:allf=t+u,format=yuv420p"
    V+="$(lbl "fontsize=28:fontcolor=white:x=24:y=40:$SH")" ;;
  *) echo "camify: unknown preset '$PRESET'" >&2; usage;;
esac
printf '%s' "$V" > "$TMP/vf.txt"

HASA=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | head -1)
if [[ -n $HASA ]]; then AIN=(); AMAP="0:a:0"; else AIN=(-f lavfi -t 3600 -i anullsrc=r=48000:cl=stereo); AMAP="1:a"; fi
ffmpeg -v error -y -i "$IN" "${AIN[@]}" -filter_script:v "$TMP/vf.txt" \
  -af "aresample=48000,aformat=channel_layouts=stereo" \
  -map 0:v:0 -map "$AMAP" -shortest \
  -c:v libx264 -preset medium -crf "$CRF" -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart "$OUT"
loudnorm_2pass "$OUT" -14
echo "camify: wrote $OUT ($PRESET, starts $DT)"
