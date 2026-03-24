---
name: news-aggregator
description: "Aggregate AI and tech news from multiple sources using SearXNG. Use for: daily AI news reports, tech trends. NOT for: when direct API access is available."
---

# News Aggregator Skill

Collect AI and tech news using local SearXNG instance at http://localhost:8080

## When to Use

✅ **USE this skill when:**

- User wants daily AI/Tech news
- Building morning/evening news reports
- Need web search results in JSON format

## How It Works

This skill uses SearXNG to search for news. It queries multiple topics and aggregates results.

## Commands

### Search for AI News
```bash
curl -s "http://localhost:8080/search?q=AI人工智能新闻+2026年&format=json&freshness=pd"
```

### Search for GitHub Trending
```bash
curl -s "http://localhost:8080/search?q=开源项目+GitHub+AI+2026&format=json&freshness=pm"
```

### Search for Tech News
```bash
curl -s "http://localhost:8080/search?q=科技新闻+2026年3月&format=json&freshness=pd"
```

## Output Format

Returns JSON with results array containing:
- title: Result title
- url: Result URL
- content: Result snippet/summary
- publishedDate: Publication date (if available)
- engine: Search engine used

## Usage in Agent

Use exec tool to call curl commands above, then parse JSON results.

## Notes

- SearXNG must be running on localhost:8080
- Use `freshness=pd` for today, `freshness=pm` for this week
- Add `&num_results=10` to limit results
