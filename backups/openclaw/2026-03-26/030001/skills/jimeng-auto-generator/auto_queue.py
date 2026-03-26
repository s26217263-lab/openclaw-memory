#!/usr/bin/env python3
"""
即梦AI自动化提交脚本 - 通过文件队列
"""
import json
import time
import os

QUEUE_FILE = "/tmp/jimeng_queue.json"
LOG_FILE = "/tmp/jimeng_auto_log.txt"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

def get_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r") as f:
        return json.load(f)

def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f)

def main():
    log("=== 自动化队列测试开始 ===")
    queue = get_queue()
    log(f"队列中有 {len(queue)} 个任务")
    
    for i, task in enumerate(queue):
        log(f"处理任务 {i+1}: {task[:30]}...")
        # 这里只是模拟，实际通过浏览器执行
        time.sleep(0.5)  # 模拟每次操作
    
    log("=== 队列处理完成 ===")

if __name__ == "__main__":
    main()
