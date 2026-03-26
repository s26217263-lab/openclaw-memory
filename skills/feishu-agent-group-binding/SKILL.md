---
name: feishu-agent-group-binding
description: Bind a newly created OpenClaw agent to a Feishu group and enable direct group conversation without @ mentions. Use when creating a new Feishu work group for an agent, when a group can receive proactive messages but does not naturally trigger replies, or when copying the working ecompass-style group wiring to a new agent.
---

# Feishu Agent Group Binding

Make a new agent speak naturally in a Feishu group without requiring @ mentions.

## Core diagnosis

If a bot can **send** into a Feishu group but only **replies when mentioned**, the usual root cause is not the agent prompt. The group is missing binding in `openclaw.json`.

The required pieces are all under `channels.feishu`:
- `groups.<chat_id>.agentId`
- `groups.<chat_id>.requireMention: false`
- `groupAllowFrom` contains the same `chat_id`

A working example already existed in this workspace:
- ecompass group `oc_a842b58b8108e7b3b44304e145c1b34d`

## Standard fix

1. Identify the target Feishu chat id.
2. Open `/Users/palpet/.openclaw/openclaw.json`.
3. Under `channels.feishu.groups`, add:
   - the target chat id
   - `agentId` = the new agent id
   - `requireMention` = `false`
4. Under `channels.feishu.groupAllowFrom`, add the same chat id.
5. Restart Gateway: `openclaw gateway restart`
6. Test in the group **without @**.

## Example pattern

```json
{
  "channels": {
    "feishu": {
      "groups": {
        "oc_example": {
          "agentId": "jimeng-queue",
          "requireMention": false
        }
      },
      "groupAllowFrom": [
        "oc_example"
      ]
    }
  }
}
```

## What this fixes

This changes the group from:
- can receive proactive bot messages
- can reply when @ mentioned

into:
- natural direct group conversation
- no @ required

## What this does NOT fix

If the group is already allowlisted and `requireMention` is already false, but messages still do not trigger, then the problem is deeper than mention gating. At that point inspect:
- channel logs
- group routing
- session creation
- gateway status

## Verification checklist

Success means all are true:
- bot can proactively send into the group
- plain human message in the group gets a reply without @
- reply lands under the intended `agentId`

Failure pattern to remember:
- proactive send works
- `@bot` works
- plain message ignored

That pattern usually means **group binding incomplete**, not model failure.
