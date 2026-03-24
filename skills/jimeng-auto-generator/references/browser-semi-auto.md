# Browser Semi-Auto Notes

Use this reference only when the user explicitly wants Jimeng browser submission help and the OpenClaw browser is already running.

## What is actually validated on this host

Validated in this workspace on 2026-03-24:
- `browser.status` reported the OpenClaw browser running.
- A live Jimeng page existed at `https://jimeng.jianying.com/ai-tool/generate?type=image&workspace=0`.
- `browser.snapshot(... refs="aria")` exposed a prompt textbox (`ref=e413` in that session).
- `browser.act(kind="click")` and `browser.act(kind="type")` worked against that textbox **without submitting**.

This means semi-automation is real, but still fragile:
- refs are session-specific; never reuse old refs
- target ids are session-specific; rediscover each run
- submission buttons / queue widgets may shift as Jimeng updates

## Recommended workflow

1. Build a queue file first with `scripts/build_prompt_queue.py`.
2. Verify environment with `scripts/check_jimeng_ready.py`.
3. In the live task, use OpenClaw `browser.tabs` + fresh `browser.snapshot(refs="aria")`.
4. Start with one dry-run prompt typed into the textbox **without submit**.
5. Only after visual confirmation, submit one item at a time or in small bursts.
6. Re-snapshot whenever the page changes.

## Minimal live pattern for the agent

```python
browser.tabs(...)
browser.snapshot(targetId=<jimeng-tab>, refs="aria", compact=True)
# find textbox ref from the snapshot, then:
browser.act(kind="click", ref=<textbox_ref>, targetId=<jimeng-tab>)
browser.act(kind="type", ref=<textbox_ref>, text=<prompt>, targetId=<jimeng-tab>)
# optional after human confirmation:
browser.act(kind="press", key="Enter", targetId=<jimeng-tab>)
```

## Do not claim

- fully unattended generation
- stable ref ids across sessions
- that legacy `auto_submit.py` / `stable_submit.py` files are trustworthy just because they exist

Treat those older files as experiments unless you retest them in the current environment.
