#!/usr/bin/env bash
# Publish an Oh Meatball part with no human tap, via Upload-Post (verified app).
# Usage: post.sh <video.mp4> "<title>" "<description>" [platforms...]
# Default platforms: youtube instagram  (tiktok needs a paid Upload-Post plan)
# Needs env UPLOAD_POST_API_KEY; profile name in UPLOAD_POST_USER (default ohmeatball).
set -euo pipefail
video=$1; title=$2; desc=$3; shift 3
platforms=("${@:-youtube instagram}")
[ $# -eq 0 ] && platforms=(youtube instagram)
: "${UPLOAD_POST_API_KEY:?add UPLOAD_POST_API_KEY in the environment settings}"
user=${UPLOAD_POST_USER:-ohmeatball}

args=(-sS -X POST https://api.upload-post.com/api/upload
  -H "Authorization: Apikey ${UPLOAD_POST_API_KEY}"
  -H "Idempotency-Key: $(sha256sum "$video" | cut -c1-32)"
  -F "video=@${video}" -F "user=${user}"
  -F "title=${title}" -F "description=${desc}"
  -F "privacyStatus=public" -F "media_type=REELS")
for p in "${platforms[@]}"; do args+=(-F "platform[]=${p}"); done
curl "${args[@]}"
echo
