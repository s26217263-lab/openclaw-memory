#!/usr/bin/env python3
"""
极速提交 - 使用pyautogui - 自动导航到生成页面
"""
import subprocess
import time
import pyperclip
import pyautogui
import sys

def submit(prompt):
    # 激活Chrome
    subprocess.run(['osascript', '-e', 'tell application "Google Chrome" to activate'], capture_output=True)
    time.sleep(0.3)
    
    # 按Cmd+L 然后输入URL导航到生成页面
    pyautogui.hotkey('command', 'l')
    time.sleep(0.2)
    pyperclip.copy('https://jimeng.jianying.com/ai-tool/image/generate')
    pyautogui.hotkey('command', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2)
    
    # 点击输入框位置
    pyautogui.click(x=1280, y=900)
    time.sleep(0.2)
    
    # 全选删除
    pyautogui.hotkey('command', 'a')
    time.sleep(0.05)
    pyautogui.press('delete')
    time.sleep(0.05)
    
    # 复制提示词并粘贴
    pyperclip.copy(prompt)
    time.sleep(0.05)
    pyautogui.hotkey('command', 'v')
    time.sleep(0.1)
    
    # 等待一下
    time.sleep(0.2)
    
    # 点击生成按钮
    pyautogui.click(x=1600, y=900)
    time.sleep(0.1)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py_submit.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    if submit(prompt):
        print(f"OK: {prompt[:30]}")
    else:
        print(f"FAIL: {prompt[:30]}")
        sys.exit(1)
