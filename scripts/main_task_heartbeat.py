#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

WORKSPACE = Path('/Users/palpet/.openclaw/workspace')
TASKS_DIR = WORKSPACE / 'tasks'
STATE_DIR = WORKSPACE / 'state'
CACHE_PATH = STATE_DIR / 'main_heartbeat_cache.json'

shanghai = timezone(timedelta(hours=8))


def ts_human():
    return datetime.now(shanghai).strftime('%Y-%m-%d %H:%M:%S +08:00')


def safe_load_json(path: Path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {} if default is None else default


def collect_statuses():
    items = []
    if not STATE_DIR.exists():
        return items
    for p in sorted(STATE_DIR.glob('*.status.json')):
        data = safe_load_json(p, {})
        task_id = data.get('id') or data.get('task_id') or p.name.replace('.status.json', '')
        items.append({
            'task_id': task_id,
            'status': data.get('status', 'unknown'),
            'phase': data.get('phase') or data.get('current_step') or '',
            'updated_at': data.get('updated_at') or '',
            'result': data.get('result'),
            'evidence': data.get('evidence') or [],
            'blockers': data.get('blockers') or ([data.get('blocker')] if data.get('blocker') and data.get('blocker') != '无' else []),
        })
    return items


def compute_counts(items):
    running = [x for x in items if x['status'] == 'running']
    blocked = [x for x in items if x['status'] == 'blocked']
    done = [x for x in items if x['status'] == 'done']
    return running, blocked, done


def snapshot_map(items):
    return {
        x['task_id']: {
            'status': x['status'],
            'phase': x['phase'],
            'updated_at': x['updated_at'],
            'result': x['result'],
            'evidence': x['evidence'],
            'blockers': x['blockers'],
        }
        for x in items
    }


def detect_changes(prev, curr):
    changes = []
    evidence_updates = []
    blocker_updates = []
    for tid, now in curr.items():
        old = prev.get(tid)
        if not old:
            continue
        if old.get('status') != now.get('status') or old.get('phase') != now.get('phase'):
            changes.append(f"- {tid}: {old.get('status','?')}/{old.get('phase','')} → {now.get('status','?')}/{now.get('phase','')}")
        old_ev = old.get('evidence') or []
        new_ev = now.get('evidence') or []
        if len(new_ev) > len(old_ev):
            added = new_ev[len(old_ev):]
            evidence_updates.append(f"- {tid}: " + '；'.join(str(x) for x in added[:3]))
        old_bl = old.get('blockers') or []
        new_bl = now.get('blockers') or []
        if new_bl != old_bl and new_bl:
            blocker_updates.append(f"- {tid}: " + '；'.join(str(x) for x in new_bl[:3]))
    return changes, evidence_updates, blocker_updates


def build_report(running, blocked, done, changes, evidence_updates, blocker_updates):
    result_lines = []
    if changes:
        result_lines.append(f"本轮推进了 {len(changes)} 个任务")
        result_lines.extend(changes[:10])
    else:
        result_lines.append('任务仍在运行中，无新增推进')

    evidence_lines = []
    if evidence_updates:
        evidence_lines.extend(evidence_updates[:10])
    else:
        for item in running[:5]:
            ev = item.get('evidence') or []
            if ev:
                evidence_lines.append(f"- {item['task_id']}: " + '；'.join(str(x) for x in ev[-2:]))
        if not evidence_lines:
            evidence_lines.append('无新增 artifact')

    blocker_lines = []
    if blocker_updates:
        blocker_lines.extend(blocker_updates[:10])
    else:
        current_blockers = []
        for item in blocked + running:
            bl = item.get('blockers') or []
            if bl:
                current_blockers.append(f"- {item['task_id']}: " + '；'.join(str(x) for x in bl[:3]))
        blocker_lines = current_blockers[:10] if current_blockers else ['无']

    report = (
        f"【main 心跳 {ts_human()}】\n\n"
        f"结果：{result_lines[0]}\n" + ("\n".join(result_lines[1:]) if len(result_lines) > 1 else '') + "\n"
        f"状态：RUNNING {len(running)} / BLOCKED {len(blocked)} / DONE {len(done)}\n"
        f"证据：" + ("\n" + "\n".join(evidence_lines) if evidence_lines else '无') + "\n"
        f"阻塞：" + ("\n" + "\n".join(blocker_lines) if blocker_lines else '无')
    )
    return report.strip() + "\n"


def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    items = collect_statuses()
    running, blocked, done = compute_counts(items)

    if not running:
        print('NO_RUNNING_TASKS')
        current = snapshot_map(items)
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump({'updated_at': ts_human(), 'tasks': current}, f, ensure_ascii=False, indent=2)
        return

    prev = safe_load_json(CACHE_PATH, {'tasks': {}})
    prev_tasks = prev.get('tasks', {}) if isinstance(prev, dict) else {}
    curr_tasks = snapshot_map(items)
    changes, evidence_updates, blocker_updates = detect_changes(prev_tasks, curr_tasks)
    report = build_report(running, blocked, done, changes, evidence_updates, blocker_updates)
    print(report)
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump({'updated_at': ts_human(), 'tasks': curr_tasks}, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
