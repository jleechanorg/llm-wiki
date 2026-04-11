---
title: "PR #5783: fix: allow SMOKE_TOKEN auth for streaming route on preview"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-worldarchitect-ai/pr-5783.md
sources: []
last_updated: 2026-03-07
---

## Summary
- Fixes MCP streaming contract failures on Preview E2E (character_streaming_contract, character_streaming_dice_contract, think_streaming_contract, god_streaming_contract)
- Root cause: SMOKE_TOKEN bypass was restricted to `/mcp` path only; streaming requests hit `/api/campaigns/<id>/interaction/stream` and received 401 Unauthorized
- Extends `check_token` SMOKE_TOKEN block to allow stream route when on preview (PRODUCTION_MODE + ENVIRONMENT=preview)
- Preserves restriction: `/api/settings` still

## Metadata
- **PR**: #5783
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +261/-14 in 4 files
- **Labels**: none

## Connections
