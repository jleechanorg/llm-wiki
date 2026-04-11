---
title: "PR #689: Fix deployment docs and config handling for Redis follow-up"
type: source
tags: [codex]
date: 2025-11-13
source_file: raw/prs-/pr-689.md
sources: []
last_updated: 2025-11-13
---

## Summary
- Hoist the environment detection logic inside `ConversationMCPTool` so production/PR rules are applied consistently
- Stop copying `node_modules` into the Cloud Build context, document the exact `--set-secrets` contract, and clarify how `REDIS_URL` is injected
- Enumerate the API-key secrets in `ConfigManager`, continue preferring Secret Manager values when present, and tidy the Redis enforcement test suite name

## Metadata
- **PR**: #689
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +30/-27 in 5 files
- **Labels**: codex

## Connections
