#!/usr/bin/env python3
"""Extract prompts from a storyboard Excel file for Jimeng workflows.

Usage:
  python3 scripts_parse_xlsx_prompts.py input.xlsx
  python3 scripts_parse_xlsx_prompts.py input.xlsx --repeat 3 --format txt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Optional

import openpyxl

PREFERRED_HEADERS = [
    "画面文字描述",
    "提示词",
    "prompt",
    "Prompt",
    "description",
    "描述",
]

INDEX_HEADERS = ["镜号", "序号", "shot", "id", "编号"]


def normalize(value: object) -> str:
    return str(value).strip() if value is not None else ""


def find_column(headers: List[str], candidates: Iterable[str]) -> Optional[int]:
    lowered = [h.lower() for h in headers]
    for candidate in candidates:
        c = candidate.lower()
        for i, h in enumerate(lowered):
            if h == c or c in h:
                return i
    return None


def extract_prompts(path: Path) -> List[str]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []

    headers = [normalize(v) for v in rows[0]]
    prompt_col = find_column(headers, PREFERRED_HEADERS)
    index_col = find_column(headers, INDEX_HEADERS)

    prompts: List[str] = []
    data_rows = rows[1:] if any(headers) else rows

    if prompt_col is not None:
        for row in data_rows:
            if prompt_col < len(row):
                value = normalize(row[prompt_col])
                if value:
                    prompts.append(value)
        return prompts

    # Fallback: use column B when there are at least two columns.
    for row in data_rows:
        if len(row) > 1:
            value = normalize(row[1])
            if value:
                prompts.append(value)
                continue
        # Final fallback: if first column is not just an index, keep it.
        if row and row[0] is not None:
            first = normalize(row[0])
            if first and (index_col is None or len(row) == 1):
                prompts.append(first)
    return prompts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--format", choices=["json", "txt"], default="json")
    args = parser.parse_args()

    prompts = extract_prompts(args.xlsx)
    prompts = [p for p in prompts for _ in range(max(args.repeat, 1))]

    if args.format == "txt":
        print("\n".join(prompts))
    else:
        print(json.dumps({"count": len(prompts), "prompts": prompts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
