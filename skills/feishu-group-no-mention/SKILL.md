---
name: feishu-group-no-mention
description: Configure a Feishu group so the OpenClaw agent responds without needing to be @mentioned. Use when the user wants a Feishu group to receive proactive messages from the agent without any @mention required, or when enabling "always-on" group mode for a Feishu channel.
---

# Feishu Group — No Mention Mode

Enable a Feishu group to receive agent replies without requiring @mentions.

## What this skill does

Configures `requireMention: false` for a given Feishu group in the OpenClaw channel config, then restarts the gateway so the change takes effect.

## When to use

- User wants another Feishu group to work like this one (`requireMention: false`)
- User says "这个群能不能不需要at就回"
- Setting up a new group for agent monitoring / alerts

## Steps

### Step 1 — Get the group chat_id

Try in order:

1. **From a group invite link**: extract the chat ID from the URL
2. **From the group itself**: ask the user to look in group settings → group ID
3. **From CLI**: run `openclaw directory --channel feishu groups` to list known groups

### Step 2 — Determine the agent to bind

Ask the user which agent should handle this group (e.g. `ecompass`, `main`, `ops`).

### Step 3 — Update the config

Edit `~/.openclaw/openclaw.json`:
- Add the group to `channels.feishu.groups` with `requireMention: false`
- Add the group to `channels.feishu.groupAllowFrom`

```python
import json

config_path = Path.home() / ".openclaw" / "openclaw.json"
config = json.loads(config_path.read_text())

group_id = "<chat_id_from_step1>"
agent_id = "<agent_id_from_step2>"   # e.g. "ecompass"

# Add to groups
config.setdefault("channels", {}).setdefault("feishu", {}).setdefault("groups", {})
config["channels"]["feishu"]["groups"][group_id] = {
    "agentId": agent_id,
    "requireMention": False
}

# Add to allowlist
config["channels"]["feishu"].setdefault("groupAllowFrom", [])
if group_id not in config["channels"]["feishu"]["groupAllowFrom"]:
    config["channels"]["feishu"]["groupAllowFrom"].append(group_id)

config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False))
```

### Step 4 — Restart gateway

```bash
openclaw gateway restart
```

### Step 5 — Verify

Ask the user to send a message in the group without @mention. If the agent replies, the config is correct.

## Checklist before reporting done

- [ ] Group chat_id obtained
- [ ] `requireMention: false` set in config
- [ ] `groupAllowFrom` updated
- [ ] Gateway restarted
- [ ] User confirmed the group responds without @mention

## Reference

Config file: `~/.openclaw/openclaw.json`
