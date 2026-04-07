# ecompass Agent Directory Structure v1.1

## 目录说明

| 目录 | 用途 | 规则 |
|------|------|------|
| **inbox/** | 接收来自 specialist 的回报、升级通知 | 只读，不放过程文件 |
| **outbox/** | 发出给 specialist 的任务 dispatch | 由 ecompass 写入，specialist 读取 |
| **tasks/** | 所有 task.json 文件 | task_runner 管理 |
| **docs/** | 架构文档、路由规则、模板 | AGENTS_ARCHITECTURE_v1.0/v1.1、ROUTING_RULES.md |
| **state/** | 任务状态 .status.json | task_runner 管理 |
| **logs/** | ecompass 运行日志 | 日志文件 |
| **sessions/** | session 历史记录 | 自动管理 |

## 通信规则

**主链路：文件**
- ecompass 把 task_dispatch.json 写入 specialist inbox/
- specialist 完成后把 task_report.json / escalation.json 写入自己的 outbox/

**辅链路：sessions_send**
- 只发提醒，不传内容
- 例："你有新任务，去收 inbox"

## 当前 specialist

- **validation-lab**：市场验证专家（Phase 2 接入协议）
- **launch-prep**：Kickstarter 预热专家（Phase 3 创建）
