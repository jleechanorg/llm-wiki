---
title: "PR #4985: fix(grok): recover narrative from truncated JSON responses"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-4985.md
sources: []
last_updated: 2026-02-08
---

## Summary
- Add JSON recovery for "Unterminated string" errors from Grok/OpenRouter truncated responses
- Log `finish_reason` and token usage from OpenAI-compatible API responses for truncation diagnosis

**Key themes:**
- Grok JSON truncation recovery
- Observability improvement for OpenRouter responses

## Metadata
- **PR**: #4985
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +293/-20 in 5 files
- **Labels**: none

## Connections
