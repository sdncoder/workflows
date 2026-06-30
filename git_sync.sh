#!/bin/bash

REPO="/Users/cliff/Desktop/Claude_Work/workflows"
SRC_LOG="$HOME/Library/Logs/ping.log"
DEST_LOG="$REPO/ping.log"

cp "$SRC_LOG" "$DEST_LOG" 2>/dev/null || true

cd "$REPO" || exit 1

git add ping.log
git diff --cached --quiet && exit 0

git commit -m "ping log update $(date '+%Y-%m-%d')"
git push origin main
