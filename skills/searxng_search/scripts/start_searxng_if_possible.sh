#!/bin/sh
set -eu

URL="${1:-http://localhost:8080}"
PORT="${URL##*:}"

if curl -fsS "$URL/search?q=test&format=json" >/dev/null 2>&1; then
  echo "SearXNG already reachable at $URL"
  exit 0
fi

if command -v docker >/dev/null 2>&1; then
  echo "Docker detected. Starting a local SearXNG container on port $PORT..."
  echo "Command: docker run -d --name openclaw-searxng -p ${PORT}:8080 -e BASE_URL=${URL}/ searxng/searxng:latest"
  docker rm -f openclaw-searxng >/dev/null 2>&1 || true
  docker run -d --name openclaw-searxng -p "${PORT}:8080" -e "BASE_URL=${URL}/" searxng/searxng:latest
  sleep 4
  exec "$(dirname "$0")/check_local_searxng.sh" "$URL"
fi

if command -v podman >/dev/null 2>&1; then
  echo "Podman detected. Starting a local SearXNG container on port $PORT..."
  echo "Command: podman run -d --name openclaw-searxng -p ${PORT}:8080 -e BASE_URL=${URL}/ docker.io/searxng/searxng:latest"
  podman rm -f openclaw-searxng >/dev/null 2>&1 || true
  podman run -d --name openclaw-searxng -p "${PORT}:8080" -e "BASE_URL=${URL}/" docker.io/searxng/searxng:latest
  sleep 4
  exec "$(dirname "$0")/check_local_searxng.sh" "$URL"
fi

echo "No local SearXNG detected at $URL." >&2
echo "No Docker/Podman runtime is available on this host, so this script cannot self-start SearXNG." >&2
echo "Practical paths:" >&2
echo "1. Install Docker Desktop or Podman, then rerun this script." >&2
echo "2. Point --base-url at an already running SearXNG reachable from this machine." >&2
exit 1
