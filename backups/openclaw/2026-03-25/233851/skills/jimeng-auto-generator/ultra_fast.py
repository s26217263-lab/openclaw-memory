#!/usr/bin/env python3
"""
极速自动提交 - 使用OpenClaw浏览器工具
"""
import subprocess
import time
import json
import re
import os
import sys

TAB_ID = "F90D9918A506F3A032C2B42C31A1BD38"

def get_input_ref():
    """获取输入框ref"""
    # 先刷新页面确保在正确位置
    subprocess.run(
        ['openclaw', 'browser', 'navigate', '--profile', 'chrome', '--targetId', TAB_ID,
         '--targetUrl', 'https://jimeng.jianying.com/ai-tool/image/generate'],
        capture_output=True, timeout=15
    )
    time.sleep(1)
    
    result = subprocess.run(
        ['openclaw', 'browser', 'snapshot', '--profile', 'chrome', '--targetId', TAB_ID, '--compact'],
        capture_output=True, text=True, timeout=30
    )
    # 查找输入框
    match = re.search(r'textbox "请描述你想生成的图片" \[ref=(\w+)\]', result.stdout)
    if match:
        return match.group(1)
    return None

def submit(prompt):
    """提交任务"""
    # 获取输入框ref
    for attempt in range(3):
        ref = get_input_ref()
        if not ref:
            time.sleep(0.5)
            continue
        
        # 点击输入框
        subprocess.run(
            ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', TAB_ID,
             '--request', json.dumps({"kind": "click", "ref": ref})],
            capture_output=True, timeout=15
        )
        time.sleep(0.2)
        
        # 输入文字
        subprocess.run(
            ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', TAB_ID,
             '--request', json.dumps({"kind": "type", "ref": ref, "text": prompt})],
            capture_output=True, timeout=20
        )
        time.sleep(0.2)
        
        # 按回车
        subprocess.run(
            ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', TAB_ID,
             '--request', json.dumps({"kind": "press", "key": "Enter"})],
            capture_output=True, timeout=15
        )
        
        return True
    
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: ultra_fast.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    if submit(prompt):
        print(f"OK: {prompt[:30]}")
    else:
        print(f"FAIL: {prompt[:30]}")
        sys.exit(1)

if __name__ == "__main__":
    main()
