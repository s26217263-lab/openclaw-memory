---
name: searxng_search
description: "Search the web using a separately running local SearXNG instance that exposes JSON search results, typically at http://localhost:8080. Use when: the user explicitly wants local/private SearXNG search or already has SearXNG running. Do not assume SearXNG is installed; verify availability first."
---

# SearXNG Search

Use this skill only after confirming a local SearXNG instance is reachable.

## Reality check

This workspace does **not** include a bundled SearXNG server. On this machine, `http://localhost:8080` must already be provided by a separate install (Docker, local service, VM, remote tunnel, etc.).

Check first:

```bash
cd /Users/palpet/.openclaw/workspace/skills/searxng_search
./scripts/check_local_searxng.sh
```

## Search command

```bash
curl -fsS "http://localhost:8080/search?q=OpenClaw+AI&format=json"
```

Optional parameters:
- `categories=news`
- `language=zh-CN`
- `time_range=day`
- `pageno=1`

## Notes

- If the check script fails, fall back to the built-in `web_search` tool instead of pretending local SearXNG exists.
- Treat `localhost:8080` as a convention, not a guarantee.
