#!/usr/bin/env python3
"""
自动提交任务到即梦AI - 使用pyautogui
"""
import subprocess
import time
import json
import sys

def submit_task(prompt):
    """使用pyautogui提交任务"""
    import pyautogui
    
    # 等待一下确保浏览器在前台
    time.sleep(0.5)
    
    # 点击输入框位置 (需要先获取坐标)
    # 假设输入框在屏幕中央上方位置
    pyautogui.click(x=600, y=700)  # 点击输入框区域
    time.sleep(0.3)
    
    # 全选删除
    pyautogui.hotkey('command', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    
    # 输入提示词
    pyautogui.write(prompt, interval=0.05)
    time.sleep(0.3)
    
    # 按回车
    pyautogui.press('enter')
    time.sleep(0.5)
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: submit.py <prompt>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    submit_task(prompt)
    print(f"Submitted: {prompt[:30]}...")

if __name__ == "__main__":
    main()
