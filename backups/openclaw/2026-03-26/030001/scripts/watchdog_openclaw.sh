#!/bin/bash
# watchdog_openclaw.sh
# OpenClaw 本地 watchdog - 方案B：自动重启一次
# 策略：fail一次→重试→fail两次→restart→检查→还不行则停

set -e

LOG="/tmp/openclaw-watchdog.log"
STATE_DIR="/tmp/openclaw-watchdog"
mkdir -p "$STATE_DIR"

# 探针命令：用 openclaw health --json 检查网关状态
check_gateway() {
    openclaw health --json 2>/dev/null | python3.11 -c "
import sys, json
d = json.load(sys.stdin)
# 新版 openclaw health 直接返回顶层 ok；旧版可能还有 gateway.rpc.ok
ok = bool(d.get('ok', False))
gateway = d.get('gateway')
rpc_ok = None
if isinstance(gateway, dict):
    rpc = gateway.get('rpc')
    if isinstance(rpc, dict) and 'ok' in rpc:
        rpc_ok = bool(rpc.get('ok'))
healthy = ok if rpc_ok is None else (ok and rpc_ok)
print('1' if healthy else '0')
" 2>/dev/null || echo "0"
}

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [WATCHDOG] $1" >> "$LOG"
}

# 主逻辑
fail_count_file="$STATE_DIR/fail_count"
last_restart_file="$STATE_DIR/last_restart"
alerted_file="$STATE_DIR/alerted"

# 读取失败计数
FAIL_COUNT=$(cat "$fail_count_file" 2>/dev/null || echo "0")
LAST_RESTART=$(cat "$last_restart_file" 2>/dev/null || echo "0")
NOW=$(date +%s)

log "=== Start check === fail_count=$FAIL_COUNT"

# 执行探针
RESULT=$(check_gateway)
log "Probe result: $RESULT"

if [ "$RESULT" = "1" ]; then
    # 健康：重置失败计数
    echo "0" > "$fail_count_file"
    log "Gateway OK - reset fail count"
    exit 0
fi

# 不健康
FAIL_COUNT=$((FAIL_COUNT + 1))
echo "$FAIL_COUNT" > "$fail_count_file"

if [ "$FAIL_COUNT" -eq 1 ]; then
    # 第一次失败：等待30秒后重试
    log "First failure - waiting 30s then retry..."
    sleep 30
    RESULT=$(check_gateway)
    if [ "$RESULT" = "1" ]; then
        echo "0" > "$fail_count_file"
        log "Retry OK - recovered"
        exit 0
    else
        FAIL_COUNT=2
        echo "2" > "$fail_count_file"
    fi
fi

if [ "$FAIL_COUNT" -ge 2 ]; then
    # 第二次失败：执行重启
    log "Second failure - executing restart..."
    openclaw gateway restart 2>&1 | tee -a "$LOG"
    echo "$NOW" > "$last_restart_file"
    
    # 等待重启生效
    sleep 15
    
    # 检查重启后状态
    RESULT=$(check_gateway)
    if [ "$RESULT" = "1" ]; then
        echo "0" > "$fail_count_file"
        log "Restart succeeded - recovered"
        exit 0
    else
        # 重启后仍不健康，告警并停止
        log "Restart failed - alerting and giving up"
        
        # 发送飞书告警
        openclaw message send --channel feishu --target ou_2369d90c137e41169ecf225ba3a7e356 \
            --message "⚠️ OpenClaw Watchdog: 重启后仍不健康，已停止自动修复。请人工检查 Mac mini 上的 OpenClaw 服务状态。" 2>&1 | tee -a "$LOG"
        
        # 标记已告警，不再继续重启
        touch "$alerted_file"
        exit 1
    fi
fi
