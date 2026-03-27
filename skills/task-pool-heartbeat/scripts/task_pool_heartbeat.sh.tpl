#!/bin/bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/opt/homebrew/sbin:/usr/sbin:/sbin"

PROJECT_ROOT="__PROJECT_ROOT__"
PYTHON_BIN="__PYTHON_BIN__"
OPENCLAW_BIN="__OPENCLAW_BIN__"
HEARTBEAT_PY="$PROJECT_ROOT/scripts/task_pool_heartbeat.py"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/__LOG_FILE__"
FEISHU_TARGET="__FEISHU_TARGET__"

mkdir -p "$LOG_DIR"
REPORT=$($PYTHON_BIN "$HEARTBEAT_PY" 2>&1 || true)
echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] $REPORT" >> "$LOG_FILE"

if [[ "$REPORT" == "NO_RUNNING_TASKS"* ]]; then
  exit 0
fi

if [[ -z "${REPORT// }" ]]; then
  exit 0
fi

"$OPENCLAW_BIN" message send --channel feishu --target "$FEISHU_TARGET" --message "$REPORT" >> "$LOG_FILE" 2>&1 || true
