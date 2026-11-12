#!/bin/bash
# SessionStart hook: make a fresh cloud machine ready for Meatball Myths work without holding up the session.
# It installs nothing on a personal computer (only when CLAUDE_CODE_REMOTE is "true").
root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$root" ] && [ -f "$root/skills/oh-meatball/tools/setup_env.sh" ] || exit 0
if python3 -c "import faster_whisper, edge_tts, soundfile, PIL, numpy" 2>/dev/null \
   && command -v ffmpeg >/dev/null 2>&1 && command -v yt-dlp >/dev/null 2>&1; then
  state="render tools ready"
elif [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  log="${TMPDIR:-/tmp}/meatball-setup.log"
  ( cd "$root" && nohup bash skills/oh-meatball/tools/setup_env.sh >"$log" 2>&1 & ) >/dev/null 2>&1
  state="render tools are installing in the background (log: $log; it ends with 'ready')"
else
  state="render tools missing: run bash skills/oh-meatball/tools/setup_env.sh"
fi
echo "Meatball Myths: $state. Read skills/channel-brain/MASTER_ORDERS.md first (one Read). Now: $(TZ=America/New_York date '+%a %m/%d %H:%M ET')."
exit 0
