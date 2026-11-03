#!/usr/bin/env bash
# Commit the explainer source files to the branch on origin without touching the working index (restart-safe checkpoint).
#   checkpoint.sh "message"
set -euo pipefail
BR=claude/youtube-monetization-strategy-m9vz6i
DIR=skills/oh-meatball/tools/sim3d/explainer
cd /home/user/skills
for attempt in 1 2 3 4; do
  git fetch -q origin "$BR"
  export GIT_INDEX_FILE=/dev/shm/idx.$$
  git read-tree "origin/$BR"
  for f in "$DIR"/*; do
    [ -f "$f" ] || continue
    sz=$(stat -c %s "$f"); [ "$sz" -lt 400000 ] || continue
    h=$(git hash-object -w "$f")
    mode=100644; [ -x "$f" ] && mode=100755
    git update-index --add --cacheinfo "$mode,$h,$f"
  done
  t=$(git write-tree)
  rm -f "$GIT_INDEX_FILE"; unset GIT_INDEX_FILE
  if [ "$t" = "$(git rev-parse "origin/$BR^{tree}")" ]; then echo "nothing new; origin at $(git rev-parse --short "origin/$BR")"; exit 0; fi
  c=$(printf '%s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01B6g5mJGtBmh6CLoEx3Vyyw\n' "$1" | git commit-tree "$t" -p "origin/$BR")
  if git push -q origin "$c:refs/heads/$BR"; then
    if git merge-base --is-ancestor HEAD "$c"; then git update-ref "refs/heads/$BR" "$c" && git reset -q; fi
    echo "checkpoint $c"; exit 0
  fi
  echo "push rejected, retrying"; sleep 2
done
exit 1
