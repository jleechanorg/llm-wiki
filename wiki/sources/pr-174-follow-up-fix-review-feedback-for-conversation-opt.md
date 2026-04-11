---
title: "PR #174: Follow-up: Fix review feedback for conversation optimistic cache"
type: source
tags: [codex]
date: 2025-11-11
source_file: raw/prs-/pr-174.md
sources: []
last_updated: 2025-11-11
---

## Summary
- preserve optimistic cache snapshots without duplicating resolved temp messages by cross-checking pending optimistic IDs
- regenerate canonical schemas and update mock/sample data so both `tokens` and `tokensUsed` remain available during the transition
- clarify the MCP token field comment and extend mocks/tests to emit `tokensUsed` alongside `tokens`

## Metadata
- **PR**: #174
- **Merged**: 2025-11-11
- **Author**: jleechan2015
- **Stats**: +40/-12 in 7 files
- **Labels**: codex

## Connections
