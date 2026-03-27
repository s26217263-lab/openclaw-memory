#!/bin/bash
# GPT-5.4 / M2.7 状态维护脚本
# 每小时由 launchd 计时器运行
# 作用：维护 fallback 窗口，窗口结束后自动清除，恢复优先 GPT-5.4
# 注意：真正的限流检测在 agent 响应时做（见 HEARTBEAT.md）

WORKSPACE="$HOME/.openclaw/workspace"
STATE_FILE="$WORKSPACE/state/gpt_model_state.json"
LOG_FILE="$WORKSPACE/logs/model_switcher.log"

FALLBACK_DURATION=10800   # 3小时，单位秒
CHECK_INTERVAL=3600       # 每小时检查

mkdir -p "$WORKSPACE/logs"
mkdir -p "$WORKSPACE/state"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

python3 -c "
import sys, json, os
STATE_FILE = '$STATE_FILE'
FALLBACK_DURATION = $FALLBACK_DURATION

try:
    with open(STATE_FILE) as f:
        d = json.load(f)
except:
    d = {}

now = int(os.path.getmtime(STATE_FILE)) if os.path.exists(STATE_FILE) else 0
import time; now = int(time.time())

fallback_until = d.get('fallback_until', 0)

if fallback_until > 0 and now >= fallback_until:
    log_msg = 'Fallback 窗口已到期，清除状态（恢复 GPT-5.4）'
    print(log_msg)
    d = {'fallback_until': 0, 'auto_cleared': True}
elif fallback_until > 0:
    remaining = fallback_until - now
    log_msg = f'Fallback 窗口未到期，剩余 {remaining}s，继续使用 M2.7'
    print(log_msg)
else:
    print('GPT-5.4 可用，无 fallback 进行中')

with open(STATE_FILE, 'w') as f:
    json.dump(d, f)
" 2>/dev/null

log "$(python3 -c "
import sys, json, time
try:
    with open('$STATE_FILE') as f:
        d = json.load(f)
except: d = {}
fallback_until = d.get('fallback_until', 0)
now = int(time.time())
if fallback_until > 0:
    print(f'状态: M2.7 fallback中，剩余 {fallback_until-now}s')
else:
    print('状态: GPT-5.4 可用')
")"
