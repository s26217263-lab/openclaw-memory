#!/usr/bin/env python3
"""
提交 v极速自动2 - 使用原生openclaw CLI
"""
import subprocess
import time
import sys
import os

TAB_ID = "F90D9918A506F3A032C2B42C31A1BD38"
JIMENG_URL = "https://jimeng.jianying.com/ai-tool/image/generate"

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr

def find_input_ref():
    """从snapshot输出中找输入框ref"""
    out = run(['openclaw', 'browser', 'snapshot', '--profile', 'chrome', '--targetId', TAB_ID, '--compact'])
    # 查找 textbox "请描述你想生成的图片"
    import re
    match = re.search(r'textbox "请描述你想生成的图片" \[ref=(\w+)\]', out)
    if match:
        return match.group(1)
    return None

def submit(prompt):
    # 先刷新页面确保在正确位置
    run(['openclaw', 'browser', 'navigate', '--profile', 'chrome', '--targetId', TAB_ID, '--targetUrl', JIMENG_URL])
    time.sleep(1.5)
    
    # 获取输入框ref
    ref = find_input_ref()
    if not ref:
        # 重试一次
        time.sleep(1)
        ref = find_input_ref()
        if not ref:
            print("FAIL: Cannot find input")
            return False
    
    # 点击输入框
    run(['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', TAB_ID,
         '--request', '{"kind":"click","ref":"' + ref + '"}'])
    time.sleep(0.3)
    
    # 输入文字 - 使用相同的ref
    run(['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', TAB_ID,
         '--request', '{"kind":"type","ref":"' + ref + '","text":"' + prompt + '"}'])
    time.sleep(0.3)
    
    # 按回车
    run(['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', TAB_ID,
         '--request', '{"kind":"press","key":"Enter"}'])
    
    print(f"OK: {prompt[:30]}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ultra_fast2.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    if not submit(prompt):
        sys.exit(1)
