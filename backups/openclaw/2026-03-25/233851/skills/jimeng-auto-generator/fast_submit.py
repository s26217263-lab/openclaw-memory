#!/usr/bin/env python3
"""
极速自动提交 - 使用pyautogui键盘控制
"""
import subprocess
import time
import os
import pyperclip
import pyautogui

def activate_chrome():
    """激活Chrome"""
    subprocess.run(['osascript', '-e', 'tell application "Google Chrome" to activate'], 
                   capture_output=True)
    time.sleep(0.5)

def submit_prompt(prompt):
    """极速提交提示词"""
    # 复制提示词到剪贴板
    pyperclip.copy(prompt)
    
    # 点击输入框位置 - 根据即梦AI页面调整 (2560x1440屏幕)
    pyautogui.click(x=1280, y=900)
    time.sleep(0.2)
    
    # 全选删除
    pyautogui.hotkey('command', 'a')
    time.sleep(0.05)
    pyautogui.press('delete')
    time.sleep(0.05)
    
    # 粘贴
    pyautogui.hotkey('command', 'v')
    time.sleep(0.15)
    
    # 回车
    pyautogui.press('enter')
    time.sleep(0.1)
    
    return True

def main():
    if len(os.sys.argv) < 2:
        print("Usage: fast_submit.py <prompt>")
        return
    
    prompt = os.sys.argv[1]
    activate_chrome()
    submit_prompt(prompt)
    print(f"OK: {prompt[:30]}")

if __name__ == "__main__":
    main()
