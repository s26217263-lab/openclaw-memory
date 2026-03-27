# MEMORY.md — Long-Term Memory

## User Preferences

- **Primary model**: `openai-codex/gpt-5.4`
- **Fallback model**: `minimax/MiniMax-M2.7` (only when GPT-5.4 rate-limited)
- Model switching via `session_status(model="...")` tool
- For task-pool workflows: once a task is accepted into the pool, do not stop at `intake` waiting for user confirmation unless a real blocker appears; proactively advance it to `done` when the deliverable is actually completed.
- When reporting task-pool items, do not show only IDs like `001/002/003`; always include a plain-language task name and short human-readable note.

## Active Project: 神盘 (Shenpan) Kickstarter

- **Product**: 赛波风水师定位，欧美 Kickstarter 市场，定价 $29-$99
- **Key deliverables**: Landing page v2, compass design v1/v2, social platform crops (10 images), Jimeng AI reference images
- **Status**: Round 1 delivery complete; `kickstarter_round1_delivery.html` at `ecompass/deliverables/`
- **Pending**: Kickstarter account registration, video direction, final Hero image from Jimeng

## Skills & Tools

- **jimeng-auto-generator v2**: Can upload reference images to Jimeng AI. Verified workflow.
- **ecompass task runner V2**: Skeleton exists; real work still chat-driven.
- **Feishu**: File sending via `message.send` partially broken (text OK, files need `card`); wiki/drive lack writable targets.
- **validation-lab**: Market-validation agent should be a standalone, isolated validation lab first; MiroFish is only a future plug-in capability, not the agent's identity.

## Validation-Lab Design Baseline

- The market-validation agent should be named **`validation-lab`** and treated as an isolated experiment layer outside the main execution path.
- Its job is pre-market validation only: narrative testing, version comparison, simulated validation, feedback synthesis, risk detection, and revision suggestions.
- It must not own main project execution, main OpenClaw runtime, business orchestration, or production ops.
- Isolation baseline: separate directory, dependencies, logs, state, sandbox, and start/stop lifecycle; if it breaks, the main agent and OpenClaw core must keep running.
- Build order preference: define responsibilities, IO protocol, round mechanism, and isolation boundary first; only then consider tools like MiroFish.
- Preferred workflow is round-based, not free-form chat. Each round should have structured input and output packages and yield a clear recommendation on whether to continue iterating or move to real-world validation.

## Hard Lessons

- If user can't read `.md` → markdown is internal only. Deliver human-facing HTML and **verify in browser** before marking complete.
- launchd PATH isolation breaks absolute commands → use absolute paths in shell scripts.
- LLM-generated ecompass task drafts can fail validation (timeout) → be ready to manually repair.

## System

- Watchdog/Gateway stability restored after heartbeat PATH fixes.
- Model monitor: `scripts/check_gpt_availability.sh` + launchd timer supports GPT-first/MiniMax-fallback.
