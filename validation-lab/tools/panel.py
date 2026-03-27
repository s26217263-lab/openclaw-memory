#!/usr/bin/env python3
import os, json
BASE='/Users/palpet/.openclaw/workspace/validation-lab/state'
r=[];d=[];b=[]
for fn in sorted(os.listdir(BASE)):
    if not fn.endswith('.json'): continue
    x=json.load(open(os.path.join(BASE,fn)))
    s=x.get('status')
    if s=='running': r.append(x)
    elif s=='done': d.append(x)
    elif s in ('blocked','needs_revision'): b.append(x)
print('=== validation-lab 任务池 ===')
print(f'[ RUNNING ] ({len(r)})')
for x in r: print(f"  {x['task_id']} | {x['task_name']} | {x['current_step']} | blocker:{x['blocker']}")
print(f'[ BLOCKED ] ({len(b)})')
for x in b: print(f"  {x['task_id']} | {x['task_name']} | {x['current_step']} | blocker:{x['blocker']}")
print(f'[ DONE ] ({len(d)})')
for x in d[-5:]: print(f"  ✓ {x['task_id']} | {x['task_name']} | {x['current_step']}")
