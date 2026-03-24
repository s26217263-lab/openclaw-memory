#!/usr/bin/env python3
"""Query a local SearXNG instance and print compact results.

Usage:
  python3 scripts/query_searxng.py "OpenClaw AI"
  python3 scripts/query_searxng.py "AI news" --category news --time-range day --limit 5
  python3 scripts/query_searxng.py "privacy search" --base-url http://localhost:8080
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List


def fetch_json(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-skill/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--category")
    parser.add_argument("--language")
    parser.add_argument("--time-range", choices=["day", "month", "year" ,"week"])
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    params = {"q": args.query, "format": "json"}
    if args.category:
        params["categories"] = args.category
    if args.language:
        params["language"] = args.language
    if args.time_range:
        params["time_range"] = args.time_range

    url = f"{args.base_url.rstrip('/')}/search?{urllib.parse.urlencode(params)}"

    try:
        payload = fetch_json(url)
    except Exception as exc:
        print(f"ERROR: failed to query {url}: {exc}", file=sys.stderr)
        return 1

    results: List[Dict[str, Any]] = payload.get("results", [])
    print(json.dumps({"query_url": url, "result_count": len(results), "results": results[: max(args.limit, 1)]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
