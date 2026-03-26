#!/usr/bin/env python3
"""
即梦AI自动提交脚本 - 稳定版
使用方法: python3 auto_submit.py <prompt>
"""
import subprocess
import time
import json
import re
import sys

JIMENG_URL = "https://jimeng.jianying.com/ai-tool/generate/?type=image"

def get_tab_id():
    """获取即梦AI标签页ID"""
    result = subprocess.run(
        ['openclaw', 'browser', 'tabs', '--profile', 'chrome'],
        capture_output=True, text=True, timeout=30
    )
    # 查找jimeng标签
    for line in result.stdout.split('\n'):
        if 'jimeng' in line.lower():
            match = re.search(r'id: (\w+)', line)
            if match:
                return match.group(1)
    return None

def get_input_ref(tab_id):
    """获取输入框ref"""
    result = subprocess.run(
        ['openclaw', 'browser', 'snapshot', '--profile', 'chrome', '--targetId', tab_id],
        capture_output=True, text=True, timeout=30
    )
    match = re.search(r'textbox "请描述你想生成的图片" \[ref=(\w+)\]', result.stdout)
    if match:
        return match.group(1)
    return None

def ensure_jimeng_page(tab_id):
    """确保在即梦AI生成页面"""
    result = subprocess.run(
        ['openclaw', 'browser', 'snapshot', '--profile', 'chrome', '--targetId', tab_id],
        capture_output=True, text=True, timeout=30
    )
    if '请描述你想生成的图片' not in result.stdout:
        # 导航到即梦AI
        subprocess.run(
            ['openclaw', 'browser', 'navigate', '--profile', 'chrome', '--targetId', tab_id,
             '--targetUrl', JIMENG_URL],
            capture_output=True, timeout=30
        )
        time.sleep(2)
        return get_input_ref(tab_id)
    return get_input_ref(tab_id)

def submit(prompt, tab_id=None):
    """提交任务"""
    if not tab_id:
        tab_id = get_tab_id()
    if not tab_id:
        print("ERROR: Cannot find Jimeng tab")
        return False
    
    # 获取输入框ref
    ref = ensure_jimeng_page(tab_id)
    if not ref:
        # 刷新页面重试
        subprocess.run(
            ['openclaw', 'browser', 'navigate', '--profile', 'chrome', '--targetId', tab_id,
             '--targetUrl', JIMENG_URL],
            capture_output=True, timeout=30
        )
        time.sleep(3)
        ref = get_input_ref(tab_id)
        if not ref:
            print("ERROR: Cannot find input ref")
            return False
    
    # 点击输入框
    subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', tab_id,
         '--request', json.dumps({"kind": "click", "ref": ref})],
        capture_output=True, timeout=15
    )
    time.sleep(0.3)
    
    # 输入文字
    subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', tab_id,
         '--request', json.dumps({"kind": "type", "ref": ref, "text": prompt})],
        capture_output=True, timeout=20
    )
    time.sleep(0.3)
    
    # 按回车
    subprocess.run(
        ['openclaw', 'browser', 'act', '--profile', 'chrome', '--targetId', tab_id,
         '--request', json.dumps({"kind": "press", "key": "Enter"})],
        capture_output=True, timeout=15
    )
    
    print(f"OK: {prompt[:40]}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: auto_submit.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    submit(prompt)

if __name__ == "__main__":
    main()
