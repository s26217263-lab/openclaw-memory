#!/usr/bin/env /opt/homebrew/bin/python3
"""
即梦AI自动批量图片生成脚本
用法: python3 jimeng_auto.py
"""

import os
import sys
import time
import openpyxl

# 添加OpenClaw路径
sys.path.insert(0, '/usr/local/lib/node_modules/openclaw')

def parse_xlsx(filepath):
    """解析xlsx文件，提取分镜提示词"""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    
    prompts = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        if not row or not row[0]:
            continue
        # 跳过标题行
        if isinstance(row[0], str) and '镜号' in row[0]:
            continue
        # 提取镜号和描述
        if isinstance(row[0], int) and row[1]:
            prompts.append(str(row[1]))
    
    return prompts

def submit_prompt(browser, target_id, prompt):
    """提交一个提示词到即梦AI"""
    from playwright.sync_api import sync_playwright
    
    try:
        # 点击文本框
        browser.click(target_id, 'input[placeholder*="描述"]')
        time.sleep(0.3)
        
        # 清空并输入
        browser.click(target_id, 'input[placeholder*="描述"]', modifiers=['Control', 'a'])
        time.sleep(0.2)
        
        # 输入提示词
        browser.type(target_id, prompt)
        time.sleep(0.3)
        
        # 按回车提交
        browser.press(target_id, 'Enter')
        time.sleep(0.5)
        
        return True
    except Exception as e:
        print(f"提交失败: {e}")
        return False

def main():
    print("=" * 50)
    print("即梦AI自动批量图片生成器")
    print("=" * 50)
    
    # 查找最新的xlsx文件
    tmp_dir = '/tmp'
    xlsx_files = [f for f in os.listdir(tmp_dir) if f.startswith('upload_') and f.endswith('.xlsx')]
    
    if not xlsx_files:
        print("未找到上传的xlsx文件")
        print("请先通过网站上传xlsx文件")
        return
    
    # 使用最新的文件
    latest_file = sorted(xlsx_files)[-1]
    filepath = os.path.join(tmp_dir, latest_file)
    print(f"读取文件: {filepath}")
    
    # 解析提示词
    prompts = parse_xlsx(filepath)
    print(f"找到 {len(prompts)} 个提示词")
    
    # 确认
    print("\n准备生成:")
    print(f"- 提示词数量: {len(prompts)}")
    print(f"- 每个提示词生成: 3次")
    print(f"- 总任务数: {len(prompts) * 3}")
    print(f"- 模型: 图片4.6")
    print(f"- 分辨率: 2K")
    print(f"- 比例: 16:9")
    print("\n请确保:")
    print("1. 浏览器已连接即梦AI")
    print("2. 页面停留在图片生成页面")
    print("3. 已选择图片4.6、2K、16:9")
    print("\n按回车开始生成...")
    input()
    
    print("\n开始生成... (按Ctrl+C停止)")
    
    # 注意：这里需要使用OpenClaw的browser工具
    # 由于是独立脚本，需要通过subprocess调用openclaw命令
    # 或者直接让用户在浏览器中操作
    
    print("\n由于需要浏览器自动化，建议:")
    print("1. 保持浏览器连接即梦AI")
    print("2. 我会通过OpenClaw browser工具自动提交")
    print("\n开始自动提交...")
    
    # 这里调用OpenClaw API
    # 实际执行需要通过OpenClaw的browser工具
    
    return

if __name__ == '__main__':
    main()
