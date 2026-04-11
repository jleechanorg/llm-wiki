---
title: "PR #49: [agento] feat(blog): RSS/Atom feed endpoint GET /feed (#jleechan-mopb)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-/pr-49.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Add `GET /feed` endpoint to blog MCP server returning Atom 1.0 XML (`application/atom+xml`)
- Returns latest 20 published posts from `list_posts`
- Optional `?repo=owner/repo` query param filters by repo
- Each entry: title, content (truncated 500 chars), link (#post-ID), updated (ISO-8601), author (eventType)
- Feed title: "AI Universe Living Blog — {repoKey}" (first registered repo or "all")
- 3 new integration tests covering Content-Type, XML validity, and repo filtering

## Metadata
- **PR**: #49
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +110/-0 in 2 files
- **Labels**: none

## Connections
