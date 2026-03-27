# Delivery path and naming patterns

## Default output layers

For a formal project delivery, prefer three visible HTML copies:

1. Project formal report copy
   - `project/reports/项目名_阶段名_汇报页.html`
2. Workspace root shortcut copy
   - `/workspace/项目名_项目汇报页.html`
3. Desktop synced copy
   - `/Desktop/.../项目名_阶段名_汇报页.html`

## Example

For ecompass:

- `/Users/palpet/.openclaw/workspace/ecompass/reports/ecompass_Kickstarter第一轮交付_汇报页.html`
- `/Users/palpet/.openclaw/workspace/ecompass_项目汇报页.html`
- `/Users/palpet/Desktop/壮壮的ai助手文件/ecompass/ecompass_Kickstarter第一轮交付_汇报页.html`

## Human-readable naming guidance

Prefer:

- project name
- stage name
- report intent

Pattern:

`项目名_阶段名_汇报页.html`

If there is only one obvious report page, use:

`项目名_项目汇报页.html`

## Minimum organization pass

When cleaning a project after delivery:

- move briefs / IA / logs / previews into `docs/`
- keep raw task outputs in `artifacts/`
- keep final report pages in `reports/`
- leave automation internals in `tasks/`, `state/`, `logs/`
- update `README.md` so the user knows what to open first
