---
name: ecompass-automation
description: Build a self-running task automation system for a project using task_runner + heartbeat cron + LLM content generation + Feishu reporting. Use when setting up a new project automation from scratch, or when the current automation only generates placeholder content instead of real LLM output.
---

# ecompass Automation Skill

Build a complete self-running task execution system.

## Architecture Overview

```
task.json (intake)
    ↓
state/<id>.status.json (status machine)
    ↓
heartbeat cron (every 5 min)
    → heartbeat_auto_advance.py
    → task_runner.py (advance + LLM generate)
    → artifacts/<id>/ (real content)
    → Feishu group (report)
```

## File Roles

| File | Role |
|------|------|
| `tasks/<id>.task.json` | Task definition: id, name, goal, steps, deadline |
| `state/<id>.status.json` | State machine: current_step, status, artifact paths, runs log |
| `tasks/task_runner.py` | Core engine: advance_step(), generate_step_content(), list_tasks() |
| `tasks/heartbeat_auto_advance.py` | Heartbeat executor: reads running tasks, calls LLM, writes artifacts |
| `tasks/ecompass_heartbeat.sh` | Launchd wrapper: runs auto_advance, formats Feishu report |
| `artifacts/<id>/` | Generated content: outline.md, draft_v1.md, deliverable_v1.md |

## Setup Steps

### 1. Create task runner structure

```python
# tasks/task_runner.py must have:
STEPS = ["intake", "outlining", "drafting", "editing", "storing"]

def call_llm(prompt, system_prompt="", model=None, temperature=0.7, max_tokens=2048):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    api_base = os.environ.get("OPENAI_API_BASE", "https://api.minimax.chat/v1")
    model = model or "MiniMax-M2.7"
    # curl to api_base + "/chat/completions"
    # return content

def generate_step_content(task_id, step, existing_content="", dry_run=False):
    # read task.json
    # build prompt from template
    # call call_llm()
    # write to artifacts/<task_id>/
    # return (content, path, name)
```

### 2. Create task

```bash
python3 tasks/task_runner.py create "Task Name" "Goal description" "2026-03-27T18:00:00+08:00"
```

### 3. Add to launchd plist (EnvironmentVariables)

```xml
<key>EnvironmentVariables</key>
<dict>
    <key>OPENAI_API_KEY</key>
    <string>sk-cp-XXXXXXXXXXXX</string>
    <key>OPENAI_API_BASE</key>
    <string>https://api.minimax.chat/v1</string>
</dict>
```

### 4. Create heartbeat script

```bash
#!/bin/bash
WORKSPACE="$HOME/.openclaw/workspace/ecompass"
OPENAI_API_KEY="sk-cp-XXX" bash "$WORKSPACE/tasks/ecompass_heartbeat.sh"
```

### 5. Register launchd

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.ecompass-heartbeat.plist
```

## Key Troubleshooting

### Symptom: "WARNING: OPENAI_API_KEY not set"
**Cause**: heartbeat launchd plist does not have the key in EnvironmentVariables.
**Fix**: Add OPENAI_API_KEY to plist EnvironmentVariables dict, then `launchctl unload/load`.

### Symptom: heartbeat runs but all tasks show RUNNING=0
**Cause**: no task has status "running" — all are "pending" or "done".
**Fix**: Create a new task with `task_runner.py create` to put something in the queue.

### Symptom: LLM generates but script fails to advance step
**Cause**: advance_step() called after artifact already exists (step already done).
**Fix**: check `current_step` before advancing; use skip-exists logic.

### Symptom: Feishu report not sending
**Cause**: openclaw message tool requires --channel and --target flags.
**Fix**: Use absolute path `/opt/homebrew/bin/openclaw`.

## Verification Commands

```bash
# Check task pool
python3 tasks/task_runner.py panel

# Test LLM generation (dry run)
OPENAI_API_KEY="sk-cp-XXX" python3 tasks/task_runner.py generate <task_id> outlining --dry-run

# Run heartbeat manually
OPENAI_API_KEY="sk-cp-XXX" bash tasks/ecompass_heartbeat.sh

# Check launchd status
launchctl list | grep ecompass
```

## Prerequisite knowledge

- task_runner.py must already exist with advance_step() and generate_step_content()
- Feishu group must be in openclaw.json channels.feishu.groups with requireMention:false
- API key must be a valid MiniMax API key (sk-cp- format)
