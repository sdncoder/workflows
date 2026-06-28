#!/bin/bash

REPO="/Users/cliff/Desktop/Claude_Work/workflows"
cd "$REPO" || exit 1

git add ping.log
git diff --cached --quiet && exit 0

git commit -m "ping log update $(date '+%Y-%m-%d')"
git push origin main
