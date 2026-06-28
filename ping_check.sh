#!/bin/bash

LOG="/Users/cliff/Desktop/Claude_Work/workflows/ping.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

WEST=$(ping -c 10 -q 8.8.8.8 2>/dev/null | tail -1 | awk -F'/' '{print $5}')
EAST=$(ping -c 10 -q 1.1.1.1 2>/dev/null | tail -1 | awk -F'/' '{print $5}')

echo "$TIMESTAMP | WEST=${WEST}ms | EAST=${EAST}ms" >> "$LOG"
