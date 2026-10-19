# Shared helpers for camify.sh / compile.sh (sourced, not executed).
# loudnorm_2pass FILE [I]: measure integrated loudness, then apply exact gain + true-peak limiter
# (-1.5 dBTP) so the output lands on target (default -14 LUFS). Video is stream-copied.
# loudnorm's own dynamic mode under-shoots on short (<10 s) clips, hence gain+limiter.
loudnorm_2pass() {
  local f=$1 I=${2:--14} m gain tmp
  m=$(ffmpeg -hide_banner -nostats -i "$f" -vn -af ebur128=framelog=quiet -f null - 2>&1 | awk '/^ *I:/{v=$2} END{print v}')
  [[ -z $m || $m == -inf || $m == -70.0 ]] && { echo "loudnorm: silent audio, skipping" >&2; return 0; }
  for _ in 1 2 3 4; do  # later iterations correct for loudness lost to the limiter
    gain=$(awk -v t="$I" -v m="$m" 'BEGIN{printf "%.2f", t-m}')
    tmp="${f%.*}.ln_tmp.${f##*.}"
    ffmpeg -v error -y -i "$f" -map 0:v:0 -map 0:a:0 -c:v copy \
      -af "volume=${gain}dB,alimiter=limit=0.84:level=false:attack=2:release=60,aresample=48000" \
      -c:a aac -b:a 160k -ar 48000 -movflags +faststart "$tmp" && mv "$tmp" "$f"
    m=$(ffmpeg -hide_banner -nostats -i "$f" -vn -af ebur128=framelog=quiet -f null - 2>&1 | awk '/^ *I:/{v=$2} END{print v}')
    if awk -v t="$I" -v m="$m" 'BEGIN{d=t-m; exit !(d<0.5 && d>-0.5)}'; then break; fi
  done
  echo "loudnorm: $f -> ${m} LUFS" >&2
}
