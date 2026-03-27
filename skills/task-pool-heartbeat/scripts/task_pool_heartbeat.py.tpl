#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_NAME = '__PROJECT_NAME__'
PROJECT_ROOT = Path('__PROJECT_ROOT__')
STATE_DIR = PROJECT_ROOT / 'state'
CACHE_PATH = STATE_DIR / '__CACHE_FILE__'

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
    return {x['task_id']: {'status': x['status'], 'phase': x['phase'], 'updated_at': x['updated_at'], 'result': x['result'], 'evidence': x['evidence'], 'blockers': x['blockers']} for x in items}


def detect_changes(prev, curr):
    changes, evidence_updates, blocker_updates = [], [], []
    for tid, now in curr.items():
        old = prev.get(tid)
        if not old:
            continue
        if old.get('status') != now.get('status') or old.get('phase') != now.get('phase'):
            changes.append(f"- {tid}: {old.get('status','?')}/{old.get('phase','')} → {now.get('status','?')}/{now.get('phase','')}")
        old_ev = old.get('evidence') or []
        new_ev = now.get('evidence') or []
        if len(new_ev) > len(old_ev):
            evidence_updates.append(f"- {tid}: " + '；'.join(str(x) for x in new_ev[len(old_ev):][:3]))
        old_bl = old.get('blockers') or []
        new_bl = now.get('blockers') or []
        if new_bl != old_bl and new_bl:
            blocker_updates.append(f"- {tid}: " + '；'.join(str(x) for x in new_bl[:3]))
    return changes, evidence_updates, blocker_updates


def build_report(running, blocked, done, changes, evidence_updates, blocker_updates):
    result_lines = [f"本轮推进了 {len(changes)} 个任务", *changes[:10]] if changes else ['任务仍在运行中，无新增推进']
    evidence_lines = evidence_updates[:10] if evidence_updates else []
    if not evidence_lines:
        for item in running[:5]:
            ev = item.get('evidence') or []
            if ev:
                evidence_lines.append(f"- {item['task_id']}: " + '；'.join(str(x) for x in ev[-2:]))
    if not evidence_lines:
        evidence_lines = ['无新增 artifact']
    blocker_lines = blocker_updates[:10] if blocker_updates else []
    if not blocker_lines:
        for item in blocked + running:
            bl = item.get('blockers') or []
            if bl:
                blocker_lines.append(f"- {item['task_id']}: " + '；'.join(str(x) for x in bl[:3]))
    if not blocker_lines:
        blocker_lines = ['无']
    report = (
        f"【{PROJECT_NAME} 心跳 {ts_human()}】\n\n"
        f"结果：{result_lines[0]}\n" + ("\n".join(result_lines[1:]) if len(result_lines) > 1 else '') + "\n"
        f"状态：RUNNING {len(running)} / BLOCKED {len(blocked)} / DONE {len(done)}\n"
        f"证据：\n" + "\n".join(evidence_lines) + "\n"
        f"阻塞：\n" + "\n".join(blocker_lines)
    )
    return report.strip() + "\n"


def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    items = collect_statuses()
    running, blocked, done = compute_counts(items)
    current = snapshot_map(items)
    if not running:
        print('NO_RUNNING_TASKS')
        CACHE_PATH.write_text(json.dumps({'updated_at': ts_human(), 'tasks': current}, ensure_ascii=False, indent=2), encoding='utf-8')
        return
    prev = safe_load_json(CACHE_PATH, {'tasks': {}})
    prev_tasks = prev.get('tasks', {}) if isinstance(prev, dict) else {}
    changes, evidence_updates, blocker_updates = detect_changes(prev_tasks, current)
    print(build_report(running, blocked, done, changes, evidence_updates, blocker_updates))
    CACHE_PATH.write_text(json.dumps({'updated_at': ts_human(), 'tasks': current}, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
