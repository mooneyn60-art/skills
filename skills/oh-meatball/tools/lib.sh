# Shared helpers for camify.sh / compile.sh (sourced, not executed).
# loudnorm_2pass FILE [I] : measure, then re-encode audio only to the target (default -14 LUFS, TP -1.5); video is copied.
loudnorm_2pass() {
  local f=$1 I=${2:--14} tp=-1.5 lra=11 j tmp
  j=$(ffmpeg -hide_banner -nostats -i "$f" -vn -af "loudnorm=I=$I:TP=$tp:LRA=$lra:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
  val(){ printf '%s' "$j" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
  tmp="${f%.*}.ln_tmp.${f##*.}"
  ffmpeg -v error -y -i "$f" -map 0:v:0 -map 0:a:0 -c:v copy \
    -af "loudnorm=I=$I:TP=$tp:LRA=$lra:measured_I=$(val input_i):measured_TP=$(val input_tp):measured_LRA=$(val input_lra):measured_thresh=$(val input_thresh):offset=$(val target_offset):linear=true,aresample=48000" \
    -c:a aac -b:a 160k -ar 48000 -movflags +faststart "$tmp" && mv "$tmp" "$f"
}
