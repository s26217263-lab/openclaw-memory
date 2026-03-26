#!/usr/bin/env python3
"""Check whether OpenClaw browser is ready for Jimeng semi-automation.

This does not submit anything. It only reports whether a Jimeng tab is open and
whether the current snapshot still exposes a textbox.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Dict, Optional

JIMENG_HINTS = ("jimeng", "即梦")
TEXTBOX_HINTS = ("textbox", "请描述", "描述你想生成的图片")
SNAPSHOT_POSITIVE_HINTS = ("textbox",)


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, timeout=30)


def browser_json(*args: str) -> Dict[str, Any]:
    proc = run("openclaw", "browser", "--json", *args)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw browser command failed")
    return json.loads(proc.stdout)


def find_jimeng_tab() -> Optional[Dict[str, Any]]:
    tabs = browser_json("tabs").get("tabs", [])
    for tab in tabs:
        hay = f"{tab.get('title', '')} {tab.get('url', '')}".lower()
        if any(hint in hay for hint in JIMENG_HINTS):
            return tab
    return None


def snapshot_has_textbox(target_id: str) -> bool:
    proc = run("openclaw", "browser", "snapshot", "--target-id", target_id, "--format", "aria", "--compact")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "snapshot failed")
    lower = proc.stdout.lower()
    return any(token in lower for token in SNAPSHOT_POSITIVE_HINTS)


def main() -> int:
    result: Dict[str, Any] = {"browser_running": False, "jimeng_tab": None, "textbox_ready": False}

    try:
        status = browser_json("status")
        result["browser_running"] = bool(status.get("running"))
    except Exception as exc:
        result["error"] = f"browser status failed: {exc}"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    if not result["browser_running"]:
        result["error"] = "OpenClaw browser is not running"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    tab = find_jimeng_tab()
    if not tab:
        result["error"] = "No Jimeng tab found"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    result["jimeng_tab"] = {k: tab.get(k) for k in ("targetId", "title", "url", "type")}

    try:
        result["textbox_ready"] = snapshot_has_textbox(tab["targetId"])
    except Exception as exc:
        result["error"] = f"snapshot failed: {exc}"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    if not result["textbox_ready"]:
        result["error"] = "Jimeng tab found, but prompt textbox was not detected in the current snapshot"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
