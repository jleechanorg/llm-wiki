---
title: "PR #931: Switch to OpenRouter Cerebras model for synthesis"
type: source
tags: [codex]
date: 2025-12-18
source_file: raw/prs-/pr-931.md
sources: []
last_updated: 2025-12-18
---

## Summary
- resolve Cerebras mode selection to use OpenRouter SMART mode when an OpenRouter key is present and fall back to FAST/direct when only the Cerebras key is configured
- align Cerebras primary and synthesis error metadata with the active endpoint, including web search diagnostics when routed through OpenRouter
- add test coverage for OpenRouter-key-missing fallback and set mock environment defaults for deterministic Cerebras web search assertions

## Metadata
- **PR**: #931
- **Merged**: 2025-12-18
- **Author**: jleechan2015
- **Stats**: +79/-11 in 2 files
- **Labels**: codex

## Connections
