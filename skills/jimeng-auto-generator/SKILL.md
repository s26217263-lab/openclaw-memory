---
name: jimeng-auto-generator
description: "从 xlsx 分镜脚本中提取即梦 AI 提示词，构建待提交队列，并在 OpenClaw 浏览器已运行且用户已登录即梦时辅助半自动提交。适用于用户提到：批量生图、上传 xlsx 生图、即梦半自动提交、Jimeng 提示词提取、浏览器里逐条辅助提交。"
---

# Jimeng Auto Generator

把 Excel 分镜脚本变成可用的 Jimeng 提示词队列，并在浏览器条件满足时推进到**真实但保守的半自动提交**。

## 当前能力边界

确定可做：
- 读取 `.xlsx` 分镜脚本
- 自动识别常见提示词列（优先 `画面文字描述`，否则回退到 `提示词`/`prompt`/第二列）
- 导出 JSON / JSONL / TXT 队列
- 检查 OpenClaw browser 是否运行、Jimeng 标签页是否存在、当前快照里是否还能看到提示词输入框
- 在 live task 中使用 `browser.snapshot(refs="aria")` + `browser.act` 做逐条半自动输入

不要默认承诺：
- 完全无人值守提交
- 固定 ref / target id 跨会话复用
- 旧的实验脚本（`auto_submit.py` / `stable_submit.py` / `submit_v2.py` 等）现在一定可用

## 先决条件

- Python 3.9+
- `pip install -r requirements.txt`
- 若要做浏览器半自动流程：
  - OpenClaw gateway 正常
  - `openclaw browser start`
  - 在 OpenClaw 浏览器里登录 Jimeng 并打开生图页

## 标准流程

### 1) 先提取提示词

```bash
cd /Users/palpet/.openclaw/workspace/skills/jimeng-auto-generator
python3 scripts/parse_xlsx_prompts.py /path/to/storyboard.xlsx
python3 scripts/build_prompt_queue.py /path/to/storyboard.xlsx --repeat 3 --format jsonl
```

### 2) 检查浏览器是否真的可用

```bash
cd /Users/palpet/.openclaw/workspace/skills/jimeng-auto-generator
./scripts/check_browser_env.sh
python3 scripts/check_jimeng_ready.py
```

`check_jimeng_ready.py` 只做检查，不提交任何内容。

### 3) 需要半自动提交时，再读参考说明

只有在用户明确要推进浏览器提交时，才读取：
- `references/browser-semi-auto.md`

它记录了这个 host 上已验证过的最小可行路径，以及哪些说法不能乱承诺。

## xlsx 输入格式

优先识别这些列名：
- `画面文字描述`
- `提示词`
- `prompt`
- `description`

如果没有匹配列，则默认尝试第二列（常见分镜表的 B 列）。

## 使用原则

- 先把“提取提示词 / 构建队列”当作确定能力。
- 进入浏览器动作前，必须重新拿 `tabs` 和 `snapshot`。
- 先做一次**不提交的 dry run**（只输入，不按提交）。
- 页面结构变化时立即重拍快照，不要依赖旧 ref。
- 大批量任务优先小批次串行，不要一口气盲提很多条。
