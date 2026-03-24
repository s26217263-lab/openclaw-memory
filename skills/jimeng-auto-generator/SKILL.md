---
name: jimeng-auto-generator
description: "从 xlsx 分镜脚本中读取提示词，并通过本地网页服务配合即梦 AI 批量生成图片。适用于用户提到：批量生图、上传 xlsx 生图、即梦自动提交、Jimeng 自动生成。"
---

# Jimeng Auto Image Generator

从 xlsx 文件读取分镜脚本，在即梦 AI 中批量生成图片的本地自动化流程。

## Requirements

- Python 3.10+（至少需要能安装依赖并运行本地服务）
- Python packages: `openpyxl`, `flask`
- Chrome 浏览器
- 保持即梦网页已登录

## Workflow

1. 安装依赖：`pip install openpyxl flask`
2. 在 skill 目录启动本地服务：`python app.py`
3. 打开 `http://localhost:5001`
4. 上传 xlsx 分镜脚本
5. 从表格中提取提示词并启动批处理流程
6. 注意：当前版本的浏览器自动提交通路未完全接通，更适合作为提示词提取与半自动提交页面

## Expected File Format

xlsx 需要至少包含这些列：

- `镜号`
- `画面文字描述`

通常将 `画面文字描述` 作为生成提示词来源。

## Notes

- 当前环境若缺少依赖，需要先补装 Python 包
- 当前仓库中的 `app.py` 主要完成 xlsx 解析、任务队列和页面展示；真正自动提交到即梦的链路仍需继续改造
- 如果要稳定复用，优先把脚本整理到 `scripts/` 目录并补充最小使用说明
- 若浏览器自动化依赖扩展或固定页面结构，每次使用前先确认即梦页面仍兼容
