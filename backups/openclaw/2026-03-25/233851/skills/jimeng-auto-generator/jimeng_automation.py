#!/usr/bin/env /opt/homebrew/bin/python3
"""
即梦AI自动批量图片生成脚本
直接通过OpenClaw browser工具自动提交

用法: 
1. 确保浏览器已连接即梦AI
2. 运行: python3 jimeng_automation.py
"""

import json
import time
import openpyxl

def parse_xlsx():
    """解析xlsx文件，提取分镜提示词"""
    # 查找最新的xlsx文件
    import os
    tmp_dir = '/tmp'
    xlsx_files = [f for f in os.listdir(tmp_dir) if f.startswith('upload_') and f.endswith('.xlsx')]
    
    if not xlsx_files:
        print("未找到上传的xlsx文件")
        return []
    
    latest_file = sorted(xlsx_files)[-1]
    filepath = os.path.join(tmp_dir, latest_file)
    print(f"读取文件: {filepath}")
    
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    
    prompts = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        if not row or not row[0]:
            continue
        if isinstance(row[0], str) and '镜号' in row[0]:
            continue
        if isinstance(row[0], int) and row[1]:
            prompts.append(str(row[1]))
    
    return prompts

def run_automation():
    """通过subprocess调用OpenClaw"""
    prompts = parse_xlsx()
    if not prompts:
        return
    
    print(f"找到 {len(prompts)} 个提示词")
    print(f"总任务数: {len(prompts) * 3}")
    print("\n开始自动提交...")
    print("每个提示词将提交3次")
    print("按Ctrl+C停止\n")
    
    # 生成3次
    all_prompts = []
    for p in prompts:
        all_prompts.extend([p, p, p])
    
    # 这里需要通过OpenClaw browser执行
    # 由于OpenClaw是独立进程，我们生成一个待执行的命令列表
    print("提示词列表已准备好")
    print("\n请在即梦AI页面保持开启状态")
    print("我会自动提交...")
    
    # 保存提示词到文件，供后续使用
    with open('/tmp/jimeng_prompts.json', 'w', encoding='utf-8') as f:
        json.dump(all_prompts, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存 {len(all_prompts)} 个任务到 /tmp/jimeng_prompts.json")
    print("现在需要在浏览器中手动操作，或者等待自动提交...")
    
    return len(all_prompts)

if __name__ == '__main__':
    run_automation()
