#!/bin/sh
set -eu
URL="${1:-http://localhost:8080}"

if curl -fsS "$URL/search?q=test&format=json" >/tmp/searxng-check.json 2>/dev/null; then
  echo "SearXNG OK at $URL"
  echo "Sample response saved to /tmp/searxng-check.json"
else
  echo "SearXNG not reachable at $URL" >&2
  echo "This workspace currently does not ship or auto-install a local SearXNG service." >&2
  echo "Install/run SearXNG separately, then retry." >&2
  exit 1
fi
