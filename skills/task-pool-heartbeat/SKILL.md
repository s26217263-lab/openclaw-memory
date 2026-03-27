---
name: task-pool-heartbeat
description: Install a silent task-pool heartbeat for any project or agent that uses tasks/*.task.json and state/*.status.json. Use when the user wants to reuse the ecompass/main heartbeat pattern, wants a 5-minute launchd heartbeat, wants structured progress pings only while tasks are running, or wants "有 running task 就发结构化心跳，没有就静默" turned into reusable automation.
---

# Task Pool Heartbeat

Install a reusable heartbeat mechanism for any task pool.

## Core rule

Only speak when a real task is alive.

- If one or more tasks are `running`, emit a structured heartbeat on a fixed interval.
- If there are no `running` tasks, stay silent.
- Never fake progress just because the scheduler fired.

## Expected task pool shape

This skill assumes the project uses:
- `tasks/*.task.json`
- `state/*.status.json`

The status files should contain at least:
- `status` (`running` / `blocked` / `done`)
- `updated_at`
- one of `phase` or `current_step`
- optional `evidence`, `blockers`, `blocker`, `result`

## Default output format

Use this compact operator report:

```text
【<project> 心跳 <timestamp>】

结果：本轮推进了 X 个任务
<task transitions or "任务仍在运行中，无新增推进">
状态：RUNNING <n> / BLOCKED <n> / DONE <n>
证据：<evidence lines or "无新增 artifact">
阻塞：<blocker lines or "无">
```

## Install workflow

When asked to set this up for a project:

1. Identify the project root.
2. Confirm the task pool lives in `tasks/` and `state/` under that root.
3. Copy `scripts/task_pool_heartbeat.py.tpl` into the target project and replace placeholders.
4. Copy `scripts/task_pool_heartbeat.sh.tpl` into the target project and replace placeholders.
5. Copy `scripts/com.openclaw.task-pool-heartbeat.plist.tpl` into the target project and replace placeholders.
6. Make the script files executable.
7. Install the plist into `~/Library/LaunchAgents/`.
8. `launchctl load` and `kickstart` it.
9. Run one manual test.
10. Commit the changes.

## Required placeholders

Replace these placeholders in the templates:
- `__PROJECT_NAME__`
- `__PROJECT_ROOT__`
- `__CACHE_FILE__`
- `__LOG_FILE__`
- `__LAUNCH_LABEL__`
- `__FEISHU_TARGET__`
- `__OPENCLAW_BIN__` (default `/opt/homebrew/bin/openclaw`)
- `__PYTHON_BIN__` (default `/usr/bin/python3`)

## Silence rule

If no task is `running`, the script must exit without sending any message.

## Anti-fake rules

Do not claim progress because:
- the scheduler ran
- the script ran successfully
- the agent replied in chat
- a stale artifact still exists

If tasks are still running but nothing changed, explicitly say:
- `任务仍在运行中，无新增推进`

## Reference files

Read these only when needed:
- `references/launchd-notes.md` for launchd install/reload pattern
- `references/status-shape.md` for tolerated status schema variants
