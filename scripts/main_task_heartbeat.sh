#!/bin/bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/opt/homebrew/sbin:/usr/sbin:/sbin"

WORKSPACE="/Users/palpet/.openclaw/workspace"
PYTHON_BIN="/usr/bin/python3"
OPENCLAW_BIN="/opt/homebrew/bin/openclaw"
HEARTBEAT_PY="$WORKSPACE/scripts/main_task_heartbeat.py"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/main_task_heartbeat.log"

mkdir -p "$LOG_DIR"

REPORT=$($PYTHON_BIN "$HEARTBEAT_PY" 2>&1 || true)

echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] $REPORT" >> "$LOG_FILE"

if [[ "$REPORT" == "NO_RUNNING_TASKS"* ]]; then
  exit 0
fi

if [[ -z "${REPORT// }" ]]; then
  exit 0
fi

"$OPENCLAW_BIN" message send --channel feishu --message "$REPORT" >> "$LOG_FILE" 2>&1 || true
