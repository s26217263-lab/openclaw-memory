#!/bin/sh
set -eu
URL="${1:-http://localhost:8080}"

if curl -fsS "$URL/search?q=test&format=json" >/tmp/searxng-check.json 2>/dev/null; then
  echo "SearXNG OK at $URL"
  echo "Sample response saved to /tmp/searxng-check.json"
else
  echo "SearXNG not reachable at $URL" >&2
  echo "This workspace does not bundle a guaranteed local SearXNG service." >&2
  echo "If Docker/Podman is available, try: ../searxng_search/scripts/start_searxng_if_possible.sh ${URL}" >&2
  echo "Otherwise point searxng_search/scripts/query_searxng.py at an already running SearXNG base URL, or fall back to built-in web_search." >&2
  exit 1
fi
