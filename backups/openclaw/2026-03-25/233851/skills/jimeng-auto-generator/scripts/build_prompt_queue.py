#!/usr/bin/env python3
"""Build a reusable Jimeng prompt queue from an xlsx storyboard.

Usage:
  python3 scripts/build_prompt_queue.py storyboard.xlsx
  python3 scripts/build_prompt_queue.py storyboard.xlsx --repeat 3 --format jsonl
  python3 scripts/build_prompt_queue.py storyboard.xlsx --out /tmp/jimeng-queue.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from parse_xlsx_prompts import extract_prompts


def build_items(prompts: List[str], repeat: int) -> List[dict]:
    repeat = max(1, repeat)
    items = []
    for shot_index, prompt in enumerate(prompts, start=1):
        for attempt in range(1, repeat + 1):
            items.append(
                {
                    "queue_index": len(items) + 1,
                    "shot_index": shot_index,
                    "attempt": attempt,
                    "prompt": prompt,
                }
            )
    return items


def render(items: List[dict], fmt: str) -> str:
    if fmt == "jsonl":
        return "\n".join(json.dumps(item, ensure_ascii=False) for item in items) + ("\n" if items else "")
    if fmt == "txt":
        lines = [f"[{item['queue_index']}/{len(items)}][shot {item['shot_index']} #{item['attempt']}] {item['prompt']}" for item in items]
        return "\n".join(lines) + ("\n" if lines else "")
    return json.dumps({"count": len(items), "items": items}, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--format", choices=["json", "jsonl", "txt"], default="json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    prompts = extract_prompts(args.xlsx)
    items = build_items(prompts, args.repeat)
    payload = render(items, args.format)

    if args.out:
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
