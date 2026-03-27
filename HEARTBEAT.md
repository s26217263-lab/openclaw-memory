# HEARTBEAT.md — 模型自动切换 + 每日记忆

## 心跳频率
每 ~30 分钟一次。

---

## 1. 模型状态检查（最重要）

### 状态文件
`/Users/palpet/.openclaw/workspace/state/gpt_model_state.json`

### 读状态（每次心跳必须做）
```bash
python3 -c "
import json, time
try:
    with open('/Users/palpet/.openclaw/workspace/state/gpt_model_state.json') as f:
        d = json.load(f)
except: d = {}
fallback_until = d.get('fallback_until', 0)
now = int(time.time())
if fallback_until > 0 and now < fallback_until:
    remaining = fallback_until - now
    print(f'RECOMMEND_M2.7: Fallback窗口，剩余{remaining}秒')
elif fallback_until > 0:
    print('Fallback窗口已到期，应恢复GPT-5.4')
else:
    print('GPT-5.4可用')
"
```

### 判断逻辑
- `fallback_until == 0` 或已到期 → **GPT-5.4 可用**
- `fallback_until > now` → **应使用 M2.7**

### 怎么做模型切换
用 `session_status` 工具：
- 切到 M2.7：`session_status(model="minimax/MiniMax-M2.7")`
- 切到 GPT-5.4：`session_status(model="openai-codex/gpt-5.4")`

---

## 2. 每日记忆（每天 1 次即可）

每次心跳时，如果发现是当天第一次心跳（或距离上次写入已 > 24h），则：
1. 读取 `memory/YYYY-MM-DD.md`
2. 检查是否有需要从 daily notes 升级到 MEMORY.md 的内容
3. 如有，更新 MEMORY.md

---

## 3. Gateway / 系统状态

如有异常（如 Gateway 不通、OpenClaw 服务断开），在 `logs/` 记录。

---

## 4. 任务静默规则

如果当前没有 `running` task：
- 不主动发送进度消息
- 不发送“无新增推进”类反馈
- 直接静默 / `HEARTBEAT_OK`

只有存在 `running` task、`done` 结果、或 blocker 时，才允许反馈。
