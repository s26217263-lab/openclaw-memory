#!/usr/bin/env python3
"""
稳定版自动提交脚本 - 使用OpenClaw浏览器工具
"""
import subprocess
import time
import json
import sys
import os

JIMENG_TAB = "3AED4AAD110170346F470ACCA79A61A9"

def get_input_ref():
    """获取当前输入框的ref"""
    try:
        result = subprocess.run(
            ['openclaw', 'browser', 'snapshot', '--profile', 'chrome', '--targetId', JIMENG_TAB],
            capture_output=True, text=True, timeout=30
        )
        
        # 解析snapshot找到输入框
        import re
        match = re.search(r'textbox "请描述你想生成的图片" \[ref=(\w+)\]', result.stdout)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error getting ref: {e}")
    return None

def submit(prompt):
    """提交任务"""
    print(f"Submitting: {prompt[:30]}...")
    
    # 获取输入框ref
    ref = get_input_ref()
    if not ref:
        print("Cannot find input ref, refreshing...")
        # 刷新页面
        subprocess.run(
            ['openclaw', 'browser', 'navigate', '--profile', 'chrome', '--targetId', JIMENG_TAB,
             '--targetUrl', 'https://jimeng.jianying.com/ai-tool/generate/?type=image'],
            capture_output=True, timeout=15
        )
        time.sleep(2)
        ref = get_input_ref()
        if not ref:
            print("Still cannot find ref")
            return False
    
    # 点击输入框
    result = subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', JIMENG_TAB,
         '--request', json.dumps({"kind": "click", "ref": ref})],
        capture_output=True, text=True, timeout=15
    )
    time.sleep(0.5)
    
    # 输入文字
    result = subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', JIMENG_TAB,
         '--request', json.dumps({"kind": "type", "ref": ref, "text": prompt})],
        capture_output=True, text=True, timeout=20
    )
    time.sleep(0.5)
    
    # 按回车
    result = subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', JIMENG_TAB,
         '--request', json.dumps({"kind": "press", "key": "Enter"})],
        capture_output=True, text=True, timeout=15
    )
    
    print(f"Submitted: {prompt[:30]}...")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: submit_stable.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    if submit(prompt):
        print("OK")
    else:
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
