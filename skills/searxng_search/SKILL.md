---
name: searxng_search
description: "Search the web using local SearXNG instance. Use when: user wants to search the internet and get JSON results. NOT for: when Brave API or other search providers are available."
---

# SearXNG Search Skill

Search the web using local SearXNG instance at http://localhost:8080

## When to Use

✅ **USE this skill when:**

- User wants to search the web
- Brave API is not configured
- Need JSON format results for easy parsing

## Command

curl -s "http://localhost:8080/search?q={query}&format=json"

## Example

curl -s "http://localhost:8080/search?q=OpenClaw+AI&format=json"

## Output Format

Returns JSON with results array containing:
- title: Result title
- url: Result URL  
- content: Result snippet/summary
