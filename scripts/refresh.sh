#!/usr/bin/env bash
# Daily refresh: rebuild the Markdown pages from AltQuick's public API and push,
# but only when something other than the "Last updated:" timestamps changed.
# Usage: scripts/refresh.sh   (run from anywhere; needs git push access to origin)
set -euo pipefail
cd "$(dirname "$0")/.."
git pull --quiet --rebase origin main
python3 scripts/build.py
git add -A
if git diff --cached --quiet; then
  echo "no changes"; exit 0
fi
# Ignore lines that only carry the build timestamp.
if git diff --cached --quiet -I 'Last updated:'; then
  echo "only timestamps changed; not committing"
  git reset --quiet && git checkout --quiet -- .
  exit 0
fi
git commit --quiet -m "Refresh market data $(date -u '+%Y-%m-%d %H:%M UTC')"
git push --quiet origin main
echo "pushed"
