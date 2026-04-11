---
title: "PR #233: fix: align model token limits with shared defaults"
type: source
tags: [codex]
date: 2025-10-08
source_file: raw/prs-/pr-233.md
sources: []
last_updated: 2025-10-08
---

## Summary
- expose shared LLM token limit constants and helpers from the config-utils package
- update ConfigManager to emit maxInputTokens/maxOutputTokens across providers and keep legacy maxTokens aliases
- reuse the shared exports inside backend llmDefaults and refresh the ConfigManager tests

## Metadata
- **PR**: #233
- **Merged**: 2025-10-08
- **Author**: jleechan2015
- **Stats**: +151/-101 in 4 files
- **Labels**: codex

## Connections
