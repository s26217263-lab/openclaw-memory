#!/usr/bin/env python3
"""Small helper for inspecting Jimeng storyboard files.

This replaces an incomplete draft that did not compile.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.parse_xlsx_prompts import extract_prompts


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview prompts extracted from an xlsx storyboard")
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    prompts = extract_prompts(args.xlsx)
    print(f"count={len(prompts)}")
    for idx, prompt in enumerate(prompts[: args.limit], start=1):
        print(f"{idx}. {prompt}")
    if len(prompts) > args.limit:
        print(f"... {len(prompts) - args.limit} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
