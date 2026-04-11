---
title: "PR #6055: [agento] feat(openclaw): public OpenAI-compatible inference proxy (/v1/chat/completions)"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6055.md
sources: []
last_updated: 2026-04-05
---

## Summary
- **New Flask routes**: `POST /v1/chat/completions` and `GET /v1/models` — forward external clients' inference requests to each user's personal OpenClaw gateway, returning OpenAI-compatible JSON or streaming SSE responses
- **Auth**: `worldai_` personal API keys (same mechanism as `/mcp` — no new auth layer needed; `@check_token` already handles prefix tokens)
- **URL resolution**: per-user `gateway_url` + `gateway_token` from Firestore settings (same `get_user_settings()` path as existing OpenC

## Metadata
- **PR**: #6055
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +1828/-20 in 14 files
- **Labels**: none

## Connections
