# Reference

## Workspace-specific known-good example

Working Feishu natural-trigger group in this workspace:
- `oc_a842b58b8108e7b3b44304e145c1b34d`
- agent: `ecompass`
- requireMention: `false`

Fixed new group example from this session:
- `oc_5d4c3cfbc31bff137034c14138b3fe97`
- agent: `jimeng-queue`
- requireMention: `false`

## Relevant config path

`/Users/palpet/.openclaw/openclaw.json`

Key subtree:
- `channels.feishu.groups`
- `channels.feishu.groupAllowFrom`

## Restart command

```bash
openclaw gateway restart
```

## Fast validation idea

After restart, send a plain group message without @:
- if no reply, but @ works, binding is still incomplete
- if plain message replies, the group is wired correctly
