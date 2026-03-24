---
name: news-aggregator
description: "Aggregate AI and tech news from a separately running local SearXNG instance, usually at http://localhost:8080. Use for daily AI news reports or tech trend summaries only when local/private SearXNG is reachable; otherwise fall back to the normal web search tool."
---

# News Aggregator

用本地或自定义地址的 SearXNG 聚合 AI / 科技新闻；如果服务不可达，就老实回退到普通 web search。

## 先检查，再查询

```bash
cd /Users/palpet/.openclaw/workspace/skills/news-aggregator
./scripts/check_local_searxng.sh
# 或指定自定义地址
./scripts/check_local_searxng.sh http://127.0.0.1:8080
```

如果不可达，不要假装本地聚合器存在。

## 当前主机现实情况

在这台 host 上，2026-03-24 的检查结果是：
- `http://localhost:8080` 不可达
- 未检测到 `docker` / `podman`

所以这台机器目前**没有现成可用的本地 SearXNG**。只有当外部已经提供该服务，或用户后续安装了容器运行时，这个 skill 才能进入本地聚合路径。

## 推荐查询方式

复用 `searxng_search/scripts/query_searxng.py`：

```bash
python3 /Users/palpet/.openclaw/workspace/skills/searxng_search/scripts/query_searxng.py "AI人工智能新闻" --category news --time-range day --limit 10
python3 /Users/palpet/.openclaw/workspace/skills/searxng_search/scripts/query_searxng.py "科技新闻" --category news --time-range day --limit 10
python3 /Users/palpet/.openclaw/workspace/skills/searxng_search/scripts/query_searxng.py "GitHub AI 开源" --category news --time-range week --limit 10
```

## 输出要点

从结果中保留：
- `title`
- `url`
- `content`
- `publishedDate`（如果有）
- `engine`

## 回退原则

- 本地 SearXNG 不可用：用内置 `web_search`
- 用户只是要常规新闻总结：不必硬走本地 skill
