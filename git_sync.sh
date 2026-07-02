#!/bin/bash

REPO="/Users/cliff/Desktop/Claude_Work/workflows"
SRC_LOG="$HOME/Library/Logs/ping.log"
DEST_LOG="$REPO/ping.log"

cp "$SRC_LOG" "$DEST_LOG" 2>/dev/null || true

git -C "$REPO" add ping.log
git -C "$REPO" diff --cached --quiet && exit 0

git -C "$REPO" commit -m "ping log update $(date '+%Y-%m-%d')"
git -C "$REPO" push origin main
