# TOOLS.md - Local Notes

## 语音消息处理流程

收到语音文件（.ogg）时的标准回复格式：
1. 用 Whisper 转文字
2. 先把用户说的话用文字重复一遍（"你说的是：..."）
3. 再给出自己的回复

示例：
- 用户发语音 → Whisper 转录 → "你说的是：xxx" → 我的回复：yyy

Whisper 安装路径：`/Users/palpet/Library/Python/3.9/bin/whisper`（模型：base）

## 长期自动化规则

- GitHub 凭证不要只存在聊天里；用于凌晨 3 点人格 / 记忆 / skills 备份的凭证，应放在本机环境变量中（优先 `GH_TOKEN`，兼容 `GITHUB_TOKEN`）。
- 每天 **03:00（Asia/Shanghai）** 运行本地备份脚本：`/Users/palpet/.openclaw/workspace/scripts/nightly_openclaw_backup.sh`
- 备份目标：人格/记忆/skills/OpenClaw 配置/agent 状态；输出目录：`/Users/palpet/.openclaw/workspace/backups/openclaw/`
- 备份调度：`~/Library/LaunchAgents/ai.openclaw.nightly-backup.plist`
- 备份日志：`/Users/palpet/.openclaw/workspace/logs/nightly_openclaw_backup.log`

## 模型自动切换规则（gpt-5.4 ↔ MiniMax-M2.7）

- **优先模型**：gpt-5.4
- **备用模型**：MiniMax-M2.7
- **触发 fallback**：gpt-5.4 返回 429（rate limit）
- **恢复 primary**：在 fallback 停留 2 小时后自动重试
- **状态文件**：`/Users/palpet/.openclaw/workspace/state/model_state.json`
- **检测脚本**：`/Users/palpet/.openclaw/workspace/scripts/model_monitor.py`
- **心跳集成**：每次 heartbeat 跑一次检测（约 30 分钟一次）
- **不需要用户手动干预**；可以随时对这个 agent 说"切换到 MiniMax"或"切换回 GPT"

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
