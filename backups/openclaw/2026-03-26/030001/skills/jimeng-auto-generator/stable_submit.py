#!/usr/bin/env python3
"""
稳定版自动提交 - 使用OpenClaw browser工具
"""
import subprocess
import time
import json
import re
import sys
import os

TAB_ID = None

def get_tab_id():
    result = subprocess.run(
        ["openclaw", "browser", "tabs", "--profile", "chrome"],
        capture_output=True, text=True, timeout=30
    )
    for line in result.stdout.split("\n"):
        if "jimeng" in line.lower():
            match = re.search(r"id:\s*(\w+)", line)
            if match:
                return match.group(1)
    return None

def navigate_to_generate(tab_id):
    subprocess.run(
        ["openclaw", "browser", "navigate", "--profile", "chrome", "--targetId", tab_id,
         "--targetUrl", "https://jimeng.jianying.com/ai-tool/image/generate"],
        capture_output=True, timeout=30
    )
    time.sleep(2)

def get_input_ref(tab_id):
    result = subprocess.run(
        ["openclaw", "browser", "snapshot", "--profile", "chrome", "--targetId", tab_id],
        capture_output=True, text=True, timeout=30
    )
    match = re.search(r'textbox "请描述你想生成的图片" \[ref=(\w+)\]', result.stdout)
    if match:
        return match.group(1)
    return None

def submit(prompt):
    global TAB_ID
    
    if not TAB_ID:
        TAB_ID = get_tab_id()
    if not TAB_ID:
        print("FAIL: Cannot find Jimeng tab")
        return False
    
    navigate_to_generate(TAB_ID)
    time.sleep(1)
    
    ref = get_input_ref(TAB_ID)
    if not ref:
        time.sleep(1)
        ref = get_input_ref(TAB_ID)
        if not ref:
            print("FAIL: Cannot find input ref")
            return False
    
    subprocess.run(
        ["openclaw", "browser", "act", "--profile", "chrome", "--targetId", TAB_ID,
         "--request", json.dumps({"kind": "click", "ref": ref})],
        capture_output=True, timeout=15
    )
    time.sleep(0.3)
    
    subprocess.run(
        ["openclaw", "browser", "act", "--profile", "chrome", "--targetId", TAB_ID,
         "--request", json.dumps({"kind": "type", "ref": ref, "text": prompt})],
        capture_output=True, timeout=20
    )
    time.sleep(0.3)
    
    subprocess.run(
        ["openclaw", "browser", "act", "--profile", "chrome", "--targetId", TAB_ID,
         "--request", json.dumps({"kind": "press", "key": "Enter"})],
        capture_output=True, timeout=15
    )
    
    print(f"OK: {prompt[:30]}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: stable_submit.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    if not submit(prompt):
        TAB_ID = None
        if not submit(prompt):
            sys.exit(1)
