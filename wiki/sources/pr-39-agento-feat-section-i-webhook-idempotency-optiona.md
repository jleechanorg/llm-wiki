---
title: "PR #39: [agento] feat(section-i): webhook idempotency + optional X-API-Key auth"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-39.md
sources: []
last_updated: 2026-03-29
---

## Summary
Section I implements two production-hardening features for the blog MCP server:

- **I.1 Webhook idempotency** — deduplicate posts by `X-GitHub-Delivery` ID; same delivery replayed twice creates only one post (200, `duplicate: true`)
- **I.2 Optional X-API-Key auth** — when `AUTH_API_KEY` env var or `authApiKey` option is set, `POST /mcp` requires `X-API-Key` header; `GET` routes remain open

## Metadata
- **PR**: #39
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +215/-2 in 5 files
- **Labels**: none

## Connections
