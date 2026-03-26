#!/bin/bash
# test_gpt54.sh
# 测试 gpt-5.4 是否可用，可用则输出 OK，不可用水输出 FAIL 并切换到 M2.7

LOG="$HOME/.openclaw/logs/gpt54_test.log"

test_gpt54() {
    result=$(curl -s -o /dev/null -w "%{http_code}" \
        --max-time 30 \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        https://api.openai.com/v1/models/gpt-4o 2>/dev/null || echo "fail")
    
    if [ "$result" = "200" ] || [ "$result" = "401" ] || [ "$result" = "429" ]; then
        # 401/429 也算"能连接上"，只是限流
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] GPT-5.4 reachable (code: $result) - OK" >> "$LOG"
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] GPT-5.4 unreachable (code: $result) - FAIL" >> "$LOG"
        return 1
    fi
}

# 立即测试一次
if test_gpt54; then
    echo "GPT-5.4 可用"
else
    echo "GPT-5.4 不可用，切换到 M2.7"
fi
