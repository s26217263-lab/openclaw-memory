---
name: news-aggregator
description: "Aggregate AI and tech news from a separately running local SearXNG instance, usually at http://localhost:8080. Use for daily AI news reports or tech trend summaries only when SearXNG is already available; otherwise fall back to normal web search."
---

# News Aggregator

Aggregate AI / tech news through local SearXNG **only after** verifying the service is reachable.

## Check local service first

```bash
cd /Users/palpet/.openclaw/workspace/skills/news-aggregator
./scripts/check_local_searxng.sh
```

If the check fails, do **not** use this skill as-is; use the normal web search tool instead.

## Example searches

### AI news

```bash
curl -fsS "http://localhost:8080/search?q=AI人工智能新闻&categories=news&format=json&time_range=day"
```

### Tech headlines

```bash
curl -fsS "http://localhost:8080/search?q=科技新闻&categories=news&format=json&time_range=day"
```

### Open-source / GitHub topics

```bash
curl -fsS "http://localhost:8080/search?q=GitHub+AI+开源&categories=news&format=json&time_range=week"
```

## What to extract

From each result, keep:
- `title`
- `url`
- `content`
- `publishedDate` or equivalent timestamp if present
- `engine`

## Operating note

This skill documents query patterns; it does not install or manage SearXNG for you.
