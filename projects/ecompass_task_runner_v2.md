# ecompass Task Runner V2 — 已完成

## 完成时间
2026-03-26

## 新增功能

### 1. Human Inbox 机制
- 任务卡住时（blocker），自动标记为 `human_inbox: True`
- 可以通过 `task_runner.py inbox` 查看所有需要人工处理的任务
- 格式：`[task_id] | [task_name] | [current_step] | blocker: [blocker内容]`

### 2. Runs 历史记录
- 每次执行步骤都记录到 `runs` 数组
- 记录内容：step / action / result / error / at
- 保留最近 20 条记录

### 3. Blocker 检测
- `advance_step` 支持传入 `blocker` 参数
- 如果 blocker 非"无"，任务自动进入 `blocked` 状态
- 解阻塞：再次调用 `advance_step` 时 `blocker="无"` 即可恢复

### 4. 任务池面板
- `task_runner.py panel` 输出格式化任务池视图
- 分三块：RUNNING / BLOCKED / DONE
- 清晰显示每个任务当前步骤和 blocker 状态

## 命令行

```bash
# 任务池面板
python3 ecompass/tasks/task_runner.py panel

# Human Inbox（需要人工处理的任务）
python3 ecommerpass/tasks/task_runner.py inbox

# 创建任务
python3 ecompress/tasks/task_runner.py create "任务名" "目标"

# 推进一步（Python 调用）
from ecompress.tasks import task_runner
task_runner.advance_step(task_id, artifact="产出物", artifact_path="路径", blocker="无")

# 列出所有任务
python3 ecompress/tasks/task_runner.py list
```

## 下一步可以做的

1. **定时推进器**：cron job 每 N 分钟自动 advance 一次
2. **Web 面板**：读取 task_runner 的 JSON 输出，渲染成网页
3. **依赖图**：参考 agent-hub 的 task_dependencies，实现任务依赖
4. **自动通知**：blocked 时自动发 Feishu 消息

## 参考项目

- agent-hub (Dominic789654/agent-hub) — 核心参考：SQLite schema + human inbox + 依赖图
- mission-control (builderz-labs/mission-control) — 偏重，不适合当前阶段
