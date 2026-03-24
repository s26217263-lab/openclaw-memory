---
name: searxng_search
description: "Search the web using a separately running local or user-specified SearXNG instance that exposes JSON results, typically at http://localhost:8080. Use when the user explicitly wants local/private SearXNG search or already has SearXNG running. Verify reachability first, and fall back to built-in web_search if no SearXNG service is available."
---

# SearXNG Search

只在确认 SearXNG 可达时使用这个 skill。

## 当前主机现实情况

本机 2026-03-24 实测：
- `http://localhost:8080/search?...format=json` 失败
- 没有 `docker` / `podman`
- 因此不能在不安装额外运行时的前提下直接拉起本地容器

也就是说，这个 skill 现在的可用路径是：
1. 用户已经有一个本地/内网/隧道后的 SearXNG 实例
2. 或后续先安装 Docker / Podman，再用脚本尝试拉起容器

## 检查命令

```bash
cd /Users/palpet/.openclaw/workspace/skills/searxng_search
./scripts/check_local_searxng.sh
./scripts/check_local_searxng.sh http://127.0.0.1:8080
```

## 查询命令

```bash
cd /Users/palpet/.openclaw/workspace/skills/searxng_search
python3 scripts/query_searxng.py "OpenClaw AI"
python3 scripts/query_searxng.py "AI news" --category news --time-range day --limit 10
python3 scripts/query_searxng.py "隐私搜索" --base-url http://localhost:8080
```

## 尝试自启（仅在有 Docker / Podman 时）

```bash
cd /Users/palpet/.openclaw/workspace/skills/searxng_search
./scripts/start_searxng_if_possible.sh
```

这个脚本会：
- 先检查服务是否已存在
- 如果有 Docker / Podman，就尝试启动官方容器
- 如果没有运行时，就明确失败并给出下一步建议

## 使用原则

- 检查失败就回退到内置 `web_search`
- 把 `localhost:8080` 当默认约定，不要当既定事实
- 优先使用 JSON 查询脚本，而不是手写 `curl` 再临时拼解析逻辑
