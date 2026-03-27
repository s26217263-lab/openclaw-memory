# status shape

The heartbeat tolerates two common status schemas.

## Shape A

```json
{
  "id": "task-001",
  "status": "running",
  "phase": "drafting",
  "updated_at": "2026-03-27T13:21:00+08:00",
  "evidence": ["artifact created"],
  "blockers": []
}
```

## Shape B

```json
{
  "task_id": "ecompass-001",
  "status": "running",
  "current_step": "editing",
  "updated_at": "2026-03-27T13:21:00+08:00",
  "blocker": "无"
}
```

The script should map:
- `id` or `task_id` -> task id
- `phase` or `current_step` -> current phase
- `blockers` or `blocker` -> blocker list

If `evidence` is missing, fall back to `无新增 artifact`.
