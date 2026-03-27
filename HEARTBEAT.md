# HEARTBEAT.md — 模型自动切换 + 每日记忆

## 心跳频率
每 ~30 分钟一次。每次心跳跑以下检查。

---

## 1. 模型状态检查（最重要）

运行：
```bash
python3 /Users/palpet/.openclaw/workspace/scripts/model_monitor.py
```

### 工作原理

**状态文件：** `state/model_state.json`

**逻辑：**
- `active_model`：当前优先使用的模型
- 正常：一直用 `openai-codex/gpt-5.4`
- 触发切换 → 变成 `minimax/MiniMax-M2.7`，记录 `fallback_start` 时间
- 在 MiniMax 上每 2 小时重试一次（自动切回 gpt-5.4 如果恢复了）

**触发 fallback 的方式：**
- 手动：对这个 agent 说"切换到 MiniMax"
- 自动：当 gpt-5.4 返回 429 时（rate limit），自动切换

**切回的方式：**
- 自动：2 小时后自动尝试切回 gpt-5.4（如果还限流，下一次 429 继续触发切换）
- 手动：对这个 agent 说"切换回 GPT"

**当前状态查询：**
直接看 `state/model_state.json`：
```bash
cat /Users/palpet/.openclaw/workspace/state/model_state.json
```

---

## 2. 每日记忆（每天 1 次即可）

每次心跳时，如果发现是当天第一次心跳（或距离上次写入已 > 24h），则：
1. 读取 `memory/YYYY-MM-DD.md`
2. 检查是否有需要从 daily notes 升级到 MEMORY.md 的内容
3. 如有，更新 MEMORY.md

---

## 3. Gateway / 系统状态

如有异常（如 Gateway 不通、OpenClaw 服务断开），在 `logs/` 记录。
