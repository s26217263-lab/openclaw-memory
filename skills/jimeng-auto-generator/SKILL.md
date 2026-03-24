---
name: jimeng-auto-generator
description: "从 xlsx 分镜脚本中提取即梦 AI 提示词，并通过本地 Flask 页面或命令行导出待提交队列。适用于用户提到：批量生图、上传 xlsx 生图、即梦半自动提交、Jimeng 提示词提取。仅在本机 OpenClaw 浏览器已启动且用户已登录即梦时，才尝试半自动浏览器操作。"
---

# Jimeng Auto Generator

把 Excel 分镜脚本变成可用的 Jimeng 提示词队列。

## 当前能力边界

这个 skill **现在是可运行的提示词提取/排队工具**，不是完全无人值守的即梦生成器。

可做：
- 读取 `.xlsx` 分镜脚本
- 自动识别常见提示词列（优先 `画面文字描述`，否则回退到 `提示词`/`prompt`/第二列）
- 通过 Flask 页面预览提示词
- 通过命令行导出 JSON/TXT 提示词列表
- 检查 OpenClaw gateway/browser 是否就绪

不可保证：
- 无登录态地直接提交到即梦
- 在未知页面结构下稳定点击/输入
- 跨会话复用固定 ref / target id

## 先决条件

- Python 3.9+
- `pip install -r requirements.txt`
- 若要做浏览器半自动流程：
  - OpenClaw gateway 正常
  - `openclaw browser start`
  - 在 OpenClaw 浏览器里登录 Jimeng 并打开生图页

## 最稳妥的用法

### 1) 命令行提取提示词

```bash
cd /Users/palpet/.openclaw/workspace/skills/jimeng-auto-generator
python3 scripts/parse_xlsx_prompts.py /path/to/storyboard.xlsx
python3 scripts/parse_xlsx_prompts.py /path/to/storyboard.xlsx --repeat 3 --format txt
```

### 2) 检查浏览器环境

```bash
cd /Users/palpet/.openclaw/workspace/skills/jimeng-auto-generator
./scripts/check_browser_env.sh
```

### 3) 启动本地预览页

```bash
cd /Users/palpet/.openclaw/workspace/skills/jimeng-auto-generator
python3 app.py
```

访问 `http://localhost:5001`，上传 xlsx 后确认提示词列表。

## xlsx 输入格式

优先识别这些列名：
- `画面文字描述`
- `提示词`
- `prompt`
- `description`

如果没有匹配列，则默认尝试第二列（常见分镜表的 B 列）。

## 使用原则

- 先把“提取提示词”当作确定能力。
- 只有在本地浏览器实际可用、Jimeng 页面已打开时，才继续半自动提交。
- 每次会话都重新获取快照，不要依赖旧的 ref / target id。
