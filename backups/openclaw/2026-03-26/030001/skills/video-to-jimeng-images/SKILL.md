---
name: video-to-jimeng-images
description: "从视频脚本Excel文件自动生成图片。读取xlsx脚本，用Jimeng AI批量生成图片"
---

# Video Script to Jimeng Images

Generate AI images from video script Excel file using Jimeng AI browser automation.

## When to Use

When user asks to:
- "生成图片" from video script
- "用即梦AI生成" video images
- Submit prompts to Jimeng from Excel file

## Workflow

### 1. Prepare Script File

Location: `/Users/poposhijue/Desktop/` or user-provided path

Required Excel format (column B = description):
```
| 序号 | 画面文字描述 | ... |
| 1    | 清晨阳光洒入客厅... | ... |
```

### 2. Connect Browser

1. Open Chrome → https://jimeng.jianying.com/ai-tool/generate/?type=image
2. Click OpenClaw extension icon
3. Wait for "连接成功"

### 3. Submit Prompts

For each row in Excel:
1. Read description from column B
2. Type into Jimeng input box
3. Press Enter to submit
4. Wait briefly, then next prompt

**Critical Technical Details:**

- **Target ID**: `B7664DCF816DFAC6A59319A33A352583`
- **Input box ref**: Use `compact=false` snapshot → find textbox with `请描述你想生成的图片`
- **Submit**: Press Enter key

```python
# Get snapshot with full refs
browser.snapshot(compact=False, targetId="B7664DCF816DFAC6A59319A33A352583")

# Find input box (ref changes, look for "请描述你想生成的图片")
# Type prompt
browser.act(request={"kind": "type", "ref": "e668", "text": "prompt"})
# Submit
browser.act(request={"key": "Enter", "kind": "press"})
```

### 4. Monitor Progress

- Check "生成 X" in Jimeng menu (X = tasks in queue)
- Queue typically holds 4-8 tasks
- Keep submitting - Jimeng processes automatically

### 5. Report Progress

Every 5 minutes, send Feishu message:

```markdown
📊 进度汇报 (HH:MM)

✅ 已提交：XX个图片
- 正在生成：X批
- 已完成：多个版本

持续自动提交中...
```

### 6. Completion

When all prompts submitted (monitor queue empties):
1. Record end time
2. Calculate total duration
3. Send final report:

```markdown
✅ 全部完成！

📊 总耗时：约 XX 分钟
📊 生成图片：XX+ 张

可以在即梦AI的"资产"或"生成"页面查看所有图片。
```

## Settings

- Model: 图片5.0 Lite
- Ratio: 16:9
- Resolution: 2K

## Notes

- Always notify user on completion - don't assume they'll check
- Track start time for duration calculation
- Browser refs change each session - always take fresh snapshot
- Use `compact=false` for working aria refs
- File transfer: copy to workspace first, then send via OpenClaw

## Example Commands

```bash
# Read Excel prompts
python3 -c "
import pandas as pd
df = pd.read_excel('/path/to/file.xlsx')
for i, row in df.iterrows():
    print(row.iloc[1])  # Column B
"
```

## Related Skills

- `video-script-generator` - Generate script from product info
- `send-to-feishu` - Send files via Feishu
