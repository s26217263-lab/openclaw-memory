# MEMORY.md — Long-Term Memory

## User Preferences

- **Primary model**: `openai-codex/gpt-5.4`
- **Fallback model**: `minimax/MiniMax-M2.7` (only when GPT-5.4 rate-limited)
- Model switching via `session_status(model="...")` tool
- For task-pool workflows: once a task is accepted into the pool, do not stop at `intake` waiting for user confirmation unless a real blocker appears; proactively advance it to `done` when the deliverable is actually completed.
- When reporting task-pool items, do not show only IDs like `001/002/003`; always include a plain-language task name and short human-readable note.
- **Commercial priority rule**: business-stage stability beats cleverness. Do not keep expanding features by default.
- Prefer: fix bugs, reduce complexity, reduce token burn, improve uptime, and improve recoverability.
- Default operating stance: 能不动就不动；能本地解决就不走模型；避免引入新依赖、新复杂链路、新花哨自动化。

## Active Project: TrueNorth (原神盘/Shenpan) Kickstarter

- **Product**: 桌面黄铜罗盘 + NFC 触发数字体验，欧美 Kickstarter 市场
- **Brand**: TrueNorth（英文品牌，2026-03-29 确认）；神盘降为内部代号
- **Slogan**: "Find your true north."
- **定价**（2026-03-29 修订）: $49（限量引爆）→ $79（主力）→ $99+（利润款）；$29 档取消
- **Key deliverables**: Landing page v2, compass design v1/v2, social platform crops (10 images), Jimeng AI reference images
- **Status**: Pre-launch 准备阶段（Week -8）；Round 1 交付完成
- **Pending**: Kickstarter 付款验证（银行账户）、NFC 抗金属样品实测
- **市场研究**: GPT × Gemini 双平台深度研究（2026-03-29 完成）
- **报告存档**: `ecompass/docs/TRUENORTH_PROJECT_REPORT_v3.md` + HTML版
- **Reddit**: `Lower_Ad_9127`（注册 × 1）
- **Launching Soon 页面**: `桌面/TrueNorth_Launching_Soon.html`（深色主题，含邮件订阅 + VIP $1 入口）
- **邮件工具**: Kit (ConvertKit) API `kit_90d3130d80a9b0252c738db94a56d4c1`（账号审核中，API 未验证）
- **Carrd**: 已注册（暂不用，用于手动重建）
- **Kickstarter 草稿**: https://www.kickstarter.com/projects/610821454/345031883/edit/basics（账号触发审核，无法创建新项目，需联系 support@kickstarter.com 解审核）
- **Launching Soon**: https://s26217263-lab.github.io/truenorth-launch/（已上线）

## Skills & Tools

- **jimeng-auto-generator v2**: Can upload reference images to Jimeng AI. Verified workflow.
- **ecompass task runner V2**: Skeleton exists; real work still chat-driven.
- **Feishu**: File sending via `message.send` partially broken (text OK, files need `card`); wiki/drive lack writable targets.
- **validation-lab**: Market-validation agent should be a standalone, isolated validation lab first; MiroFish is only a future plug-in capability, not the agent's identity.
- **launch-prep agent** (created 2026-03-29): Kickstarter pre-launch specialist. Location: ~/.openclaw/agents/launch-prep/. Responsibilities: Launching Soon page, Reddit seeding, email list, influencer outreach, content calendar. **Activation now ready** (Blocker #1-4 all fixed). Brand name for all pre-launch materials: **TrueNorth**.

## Active Project: 神盘 (Shenpan) Kickstarter

- **Brand 品牌**: TrueNorth（英文，对外）；神盘/Shenpan（内部代号）
- **Hero images** (2026-03-29 完成): prompt1_hero.webp / prompt2_texture.webp / prompt3_lifestyle.webp，保存于 `~/workspace/ecompass/artifacts/hero_images/`
- **Kickstarter 项目草稿** (2026-03-29 创建): https://www.kickstarter.com/projects/610821454/345031883/edit/basics
- **launch-prep agent** 可激活（Blocker #1-4 全部清除）

### 三大必须解决的问题（GPT × Gemini 研究结论，2026-03-29）

| 优先级 | 问题 | 解决方案 |
|--------|------|---------|
| 🔴 最紧急 | NFC + 黄铜物理冲突（标准标签被屏蔽）| 抗金属铁氧体标签 + 铣凹槽 |
| 🔴 已解决 | $29 定价每件亏损 | 改为 $49/$79/$99+ |
| 🔴 已解决 | 预热邮件目标 300-500 严重偏低 | 升级为 $1 VIP 订金漏斗，目标 200+ VIP 用户 |

### 4 周验证闸门（上线前必须达标）

1. 卖点清晰度：LP 转化率 ≥ 6% 或 KS Follow ≥ 8%
2. 价格接受度：$79 成主力，$49 有抢购意愿
3. NFC 可用性：20 人实测成功率 ≥ 85%
4. 预热规模：$1 VIP 订金用户 ≥ 200

## Blocker Status (as of 2026-03-29)

| Blocker | Description | Status |
|---------|-------------|--------|
| #1 | Two-Pack $89→$125 pricing fix | ✅ Done |
| #2 | Project background copy (东方哲学/文化根基) | ✅ Done |
| #3 | Hero image generation via Jimeng AI | ✅ Done (3张图全部生成并选定) |
| #4 | Kickstarter account registration | ✅ Done (项目草稿已创建) |

**注意**: Blocker #1-4 全部清零。但真正的上线硬性前提是 Kickstarter **付款验证**（填银行账户，1-3 工作日审核），这个还未完成。

## Pre-Launch Plan（修订版，2026-03-29）

- **文档**: ecompass/docs/PRELAUNCH_PLAN.md + ecompass/docs/STRATEGIC_PIVOT_v2.md
- **时间轴**: 6-8 weeks before Kickstarter launch
- **KPI**（修订）: $1 VIP 订金用户 200+ / Kickstarter Follower 500+ / Reddit 20+ posts
- **预热策略升级**: Reddit + Meta 广告 + $1 VIP 订金漏斗（不再是纯 300-500 邮件）
- **启动条件**: Blocker #1-#4 全部修复；launch-prep agent 可激活

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
- 品牌名决定后必须同步更新所有文件（PROJECT_BRIEF / CONTENT / app/*.html / deliverables/*.html），不能只改一个地方。
- GPT × Gemini 深度研究结果显示：NFC + 黄铜物理冲突是项目最大未知风险，必须独立实测验证，不能靠想当然。
- Kickstarter 预热"300-500 邮件"目标在数学上不足以支撑首日 momentum，必须升级到 $1 VIP 订金漏斗。

## System

- Watchdog/Gateway stability restored after heartbeat PATH fixes.
- Model monitor: `scripts/check_gpt_availability.sh` + launchd timer supports GPT-first/MiniMax-fallback.

### Cron Automation (as of 2026-03-27/28)
- **watchdog** (`7dd53373`): every 5 minutes — model state check + heartbeat
- **healthcheck** (`3df614d0`): daily — host security / OpenClaw health
- **nightly backup** (`ai.openclaw.nightly-backup.plist`): daily 03:00 Asia/Shanghai — local backup → GitHub push
- **Backup GitHub push fix (2026-03-27)**: session/jsonl files contained GitHub PAT-like secrets; GitHub push protection was blocking. Fixed by: creating `backup-main-clean` branch, skipping `sessions/` and `jsonl/` in backup script, deleting old `main` branch.
- **Lesson**: local backup success ≠ GitHub push success. Both must be verified independently.

### System Fixes Log

- **watchdog_openclaw.sh PATH fix (2026-03-30)**: Added `export PATH="/opt/homebrew/bin:$PATH"` at script start to fix openclaw command not found causing 274 consecutive failures.
- **watchdog** (`7dd53373`): every 5 minutes — model state check + heartbeat
- **healthcheck** (`3df614d0`): daily — host security / OpenClaw health
- **nightly backup** (`ai.openclaw.nightly-backup.plist`): daily 03:00 Asia/Shanghai — local backup → GitHub push
- **Backup GitHub push fix (2026-03-27)**: session/jsonl files contained GitHub PAT-like secrets; GitHub push protection was blocking. Fixed by: creating `backup-main-clean` branch, skipping `sessions/` and `jsonl/` in backup script, deleting old `main` branch.
- **Lesson**: local backup success ≠ GitHub push success. Both must be verified independently.
