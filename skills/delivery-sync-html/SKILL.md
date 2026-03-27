---
name: delivery-sync-html
description: Create polished HTML delivery pages, rename them with clear Chinese filenames, place a copy at the workspace root for easy discovery, sync another copy to the desktop project folder, and tidy project folders so reports, docs, and system files are separated. Use when the user asks for HTML/PPT-like delivery pages, wants files synchronized to the desktop, wants Chinese-readable filenames, wants a root-level report entry file, or asks to organize project files after delivery.
---

# Delivery Sync HTML

Turn a finished delivery into something humans can actually use.

## Core rule

Do not stop at generating a `.md` file.

When the user wants something for review, reporting, or showing a boss, deliver a human-facing HTML page and make it easy to find.

## Required outputs

For each formal delivery, complete all of these unless the user says otherwise:

1. Keep the working version inside the project folder.
2. Save a polished HTML version under the project's `reports/` folder.
3. Save another copy at the workspace root with a short Chinese filename.
4. Sync another copy to the user's desktop project folder.
5. Keep markdown only as internal draft/supporting material.

If desktop sync is requested or already part of the project convention, missing the desktop copy means the delivery is not finished.

## Naming rules

Prefer obvious Chinese filenames that a human can recognize instantly.

Use patterns like:

- `项目汇报页.html`
- `项目名_阶段名_汇报页.html`
- `项目名_老板汇报版.html`

Avoid vague names like:

- `final_v2.html`
- `delivery_latest.html`
- `report_new.html`

## Folder organization rules

After delivery, make the project readable.

Preferred structure:

```text
project/
├── app/         # product/app/prototype files
├── artifacts/   # task outputs and raw drafts
├── docs/        # briefs, IA, notes, logs, previews
├── reports/     # polished HTML delivery pages for humans
├── logs/        # runtime logs
├── state/       # status machine files
└── tasks/       # automation/task runner files
```

## Reorganization workflow

When a project is messy, do this:

1. Identify human-facing report files.
2. Move briefing / IA / preview / log style markdown into `docs/`.
3. Keep raw task outputs in `artifacts/`.
4. Keep automation internals in `tasks/`, `state/`, and `logs/`.
5. Put final HTML report pages in `reports/`.
6. Add or refresh `README.md` so the user can immediately find the correct file.

Do not over-refactor the whole repo if the user only needs the delivery surfaced quickly. Prioritize visibility and usability.

## HTML quality bar

If the user wants a boss-facing page, the HTML should feel like a proposal deck, not a raw dashboard.

Aim for:

- one clear conclusion per screen/section
- strong hierarchy
- concise language
- presentation-friendly spacing
- obvious navigation
- visually polished cover / hero section

If needed, first produce a usable HTML v1, then refine into a polished presentation HTML v2.

## README rule

When you reorganize a project, update the project `README.md` to include:

- the main report HTML path
- the root-level shortcut HTML path
- the desktop-synced HTML path
- a brief explanation of what belongs in `docs/`, `reports/`, `artifacts/`, `tasks/`, and `state/`

## Delivery checklist

Before saying a delivery is done, verify:

- HTML exists in `reports/`
- Chinese-readable HTML exists at workspace root
- desktop copy exists in the target desktop folder
- project files are organized enough for a human to navigate
- README points to the right report file
- the HTML opens in a browser and renders as a human-facing page (not just a file existing on disk)
- you give the user the exact browser-openable path/URL, not only internal markdown paths

If any of the above is missing, say the delivery is not fully closed yet.

## Hard lesson: markdown is not the final delivery

If the user says they cannot read `.md` files or says the delivery should feel like a PPT / proposal / boss-facing page, do **not** report completion after only generating markdown.

Markdown is internal working material.
The real delivery is the HTML page the human can open and review.

When in doubt:
1. finish the content in markdown if needed,
2. immediately convert/summarize it into the final HTML delivery page,
3. open the HTML locally and verify it actually renders,
4. only then report the job as closed.

## Reference

Read `references/path-patterns.md` when you need a compact reminder of naming and placement conventions.
