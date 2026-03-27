#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path('/Users/palpet/.openclaw/workspace/validation-lab')
ROUNDS = ROOT / 'rounds'
shanghai = timezone(timedelta(hours=8))


def ts():
    return datetime.now(shanghai).strftime('%Y-%m-%dT%H:%M:%S+08:00')


def main():
    existing = []
    for p in ROUNDS.glob('round-*'):
        try:
            existing.append(int(p.name.replace('round-','')))
        except Exception:
            pass
    n = max(existing) + 1 if existing else 1
    rid = f'round-{n:03d}'
    rd = ROUNDS / rid
    rd.mkdir(parents=True, exist_ok=True)
    for name, title in [
        ('brief.md', '# brief\n'),
        ('audience.md', '# audience\n'),
        ('version-a.md', '# version-a\n'),
        ('version-b.md', '# version-b\n'),
        ('version-c.md', '# version-c\n'),
        ('questions.md', '# questions\n'),
        ('result-summary.md', '# result-summary\n'),
        ('next-actions.md', '# next-actions\n'),
    ]:
        (rd / name).write_text(title, encoding='utf-8')
    state = {
        'round_id': rid,
        'project': 'validation-lab',
        'status': 'running',
        'current_stage': 'brief',
        'inputs_ready': False,
        'versions': ['A', 'B', 'C'],
        'decision': None,
        'updated_at': ts(),
    }
    (rd / 'round-state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    print(rid)


if __name__ == '__main__':
    main()
