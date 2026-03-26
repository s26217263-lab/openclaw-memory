# Browser Semi-Auto Notes

Use this reference only when the user explicitly wants Jimeng browser submission help and the OpenClaw browser is already running.

## What is actually validated on this host

**Validated on 2026-03-24（今晚重大突破）：**

- 5条提示词全部成功提交并生成图片
- 关键发现：**提交成功 = 输入框被清空**，不需要等生成完成
- 即梦队列上限约 3-4 条，超过后新提交静默失败（输入框文字不消失）
- 每次提交后检查输入框状态：
  - **已清空（恢复占位文字）** → 提交成功，立即填下一条
  - **仍有文字** → 队列满，等一下再试
- `browser.act(kind="type")` + `Meta+a` 全选后再填新内容，避免累积

## Recommended workflow（已验证可行）

1. Build a queue file first with `scripts/build_prompt_queue.py`.
2. Verify environment with `scripts/check_jimeng_ready.py`.
3. Open Jimeng page: `https://jimeng.jianying.com/ai-tool/generate?type=image&workspace=0`
4. Start browser: `openclaw browser start`（if not running）
5. Get fresh tabs + snapshot each session
6. Loop: fill prompt → submit → **check: input cleared? → yes = next, no = retry**
7. If queue full (input not cleared), wait ~30s and retry

## Minimal live pattern for the agent

```python
# Get tab and fresh snapshot each round
browser.tabs(...)
browser.snapshot(targetId=<jimeng-tab>, refs="aria", compact=True)
# find textbox ref and submit button ref from snapshot

# Fill and submit one prompt
browser.act(kind="click", ref=<textbox_ref>, targetId=<jimeng-tab>)
browser.act(kind="press", key="Meta+a", targetId=<jimeng-tab>)  # select all
browser.act(kind="type", ref=<textbox_ref>, text=<prompt>, targetId=<jimeng-tab>)
browser.act(kind="click", ref=<submit_btn_ref>, targetId=<jimeng-tab>)

# Critical: check if input was cleared (submit success)
browser.snapshot(targetId=<jimeng-tab>, refs="aria", compact=True)
# If textbox paragraph still shows prompt text → queue full, retry after wait
# If textbox paragraph shows placeholder → submit success, move to next

# When queue full, wait and retry:
sleep(30)
browser.snapshot(...)
browser.act(kind="click", ref=<textbox_ref>, ...)
browser.act(kind="press", key="Meta+a", ...)
browser.act(kind="type", ref=<textbox_ref>, text=<prompt>, ...)
browser.act(kind="click", ref=<submit_btn_ref>, ...)
```

## Critical rules

- **Never wait for generation to complete before submitting next**
- **Input box cleared = submit success signal** — the only signal that matters
- Queue limit ~3-4; beyond that submissions silently fail
- refs and target ids are session-specific; always rediscover each session
- Page structure may change on refresh; re-snapshot after any page navigation

## Do not claim

- fully unattended generation
- stable ref ids across sessions
- that legacy `auto_submit.py` / `stable_submit.py` files are currently working

Treat older experimental files as unverified unless retested in current environment.
