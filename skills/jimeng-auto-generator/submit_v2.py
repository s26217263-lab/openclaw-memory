#!/usr/bin/env python3
"""
使用subprocess调用openclaw browser来提交任务
"""
import subprocess
import time
import json
import sys
import re

JIMENG_TAB = "3AED4AAD110170346F470ACCA79A61A9"

def get_input_ref():
    """获取当前输入框的ref"""
    result = subprocess.run(
        ['openclaw', 'browser', 'snapshot', '--profile', 'chrome', '--targetId', JIMENG_TAB],
        capture_output=True, text=True, timeout=30
    )
    
    # 解析snapshot找到输入框
    # 查找 "请描述你想生成的图片" 对应的ref
    match = re.search(r'textbox "请描述你想生成的图片" \[ref=(\w+)\]', result.stdout)
    if match:
        return match.group(1)
    return None

def submit(prompt):
    """提交任务"""
    # 获取输入框ref
    ref = get_input_ref()
    if not ref:
        print("Cannot find input ref")
        return False
    
    # 点击输入框
    result = subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', JIMENG_TAB,
         '--request', json.dumps({"kind": "click", "ref": ref})],
        capture_output=True, text=True, timeout=15
    )
    
    if '"ok": true' not in result.stdout:
        print(f"Click failed: {result.stdout}")
        # 尝试刷新页面
        subprocess.run(
            ['openclaw', 'browser', 'navigate', '--profile', 'chrome', '--targetId', JIMENG_TAB,
             '--targetUrl', 'https://jimeng.jianying.com/ai-tool/generate/?type=image'],
            capture_output=True, timeout=15
        )
        time.sleep(2)
        ref = get_input_ref()
        if not ref:
            return False
    
    time.sleep(0.5)
    
    # 输入文字 - 使用type
    result = subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', JIMENG_TAB,
         '--request', json.dumps({"kind": "type", "ref": ref, "text": prompt})],
        capture_output=True, text=True, timeout=15
    )
    
    if '"ok": true' not in result.stdout:
        print(f"Type failed: {result.stdout}")
        return False
    
    time.sleep(0.5)
    
    # 按回车
    result = subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', JIMENG_TAB,
         '--request', json.dumps({"kind": "press", "key": "Enter"})],
        capture_output=True, text=True, timeout=15
    )
    
    return '"ok": true' in result.stdout

def main():
    if len(sys.argv) < 2:
        print("Usage: submit.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    if submit(prompt):
        print(f"OK: {prompt[:30]}...")
    else:
        print(f"FAIL: {prompt[:30]}...")

if __name__ == "__main__":
    main()
