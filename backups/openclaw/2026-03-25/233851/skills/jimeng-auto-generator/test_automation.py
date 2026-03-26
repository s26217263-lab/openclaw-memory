#!/usr/bin/env python3
"""
即梦AI自动化测试脚本
测试完整流程：解析xlsx -> 提交到即梦AI
"""

import os
import sys
import time

# 使用subprocess调用系统命令执行浏览器操作

XLSX_FILE = "/Users/poposhijue/.openclaw/workspace/skills/jimeng-auto-generator/test_script.xlsx"

# 测试用的提示词列表（从xlsx解析）
TEST_PROMPTS = [
    "主角的脸，他正头痛地揉着太阳穴",
    "工作室环境中，主显示器上布满了窗口，他手忙脚乱地在多个应用间切换",
    "会议环境中，主角正在开Zoom会议表情茫然错过了关键信息",
    "镜头穿梭在桌面上杂乱的线缆和设备中移动前推",
    "光线扫过Quake的CNC铝合金机身产品周围亮起来屏幕也亮起来",
]

def test_browser_automation():
    """测试浏览器自动化流程"""
    print("=" * 50)
    print("即梦AI自动化测试")
    print("=" * 50)
    
    print("\n[1] 检查xlsx文件...")
    if os.path.exists(XLSX_FILE):
        print(f"    ✅ 文件存在: {XLSX_FILE}")
    else:
        print(f"    ❌ 文件不存在")
        return False
    
    print("\n[2] 解析提示词...")
    import openpyxl
    wb = openpyxl.load_workbook(XLSX_FILE)
    ws = wb.active
    prompts = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        if row[0] and isinstance(row[0], int) and row[1]:
            prompts.append(str(row[1]))
    print(f"    ✅ 解析到 {len(prompts)} 个提示词")
    
    # 只测试前5个
    test_prompts = prompts[:5]
    print(f"    📝 测试用前 {len(test_prompts)} 个提示词")
    
    print("\n[3] 测试浏览器操作...")
    print("    需要通过OpenClaw浏览器执行...")
    print("    ")
    print("    测试步骤:")
    print("    1. 点击文本框")
    print("    2. 输入提示词")
    print("    3. 按回车提交")
    print("    4. 等待生成")
    print("    5. 重复3次")
    
    print("\n[4] 开始自动化测试...")
    print("    ⚠️  需要浏览器已连接即梦AI")
    print("    ⚠️  页面需要在图片生成页面")
    print("    ⚠️  需要选择图片4.6 + 2K + 16:9")
    
    # 生成测试命令
    print("\n[5] 生成自动化脚本...")
    
    # 保存提示词到文件
    import json
    all_tasks = []
    for p in test_prompts:
        all_tasks.extend([p, p, p])  # 每个3次
    
    with open('/tmp/jimeng_test_tasks.json', 'w', encoding='utf-8') as f:
        json.dump(all_tasks, f, ensure_ascii=False, indent=2)
    
    print(f"    ✅ 保存了 {len(all_tasks)} 个任务到 /tmp/jimeng_test_tasks.json")
    
    print("\n" + "=" * 50)
    print("测试准备完成!")
    print("=" * 50)
    print("""
下一步: 
1. 打开浏览器到即梦AI图片生成页面
2. 选择: 图片4.6 + 2K + 16:9
3. 运行自动化提交

要开始吗?
""")
    
    return True

if __name__ == '__main__':
    test_browser_automation()
