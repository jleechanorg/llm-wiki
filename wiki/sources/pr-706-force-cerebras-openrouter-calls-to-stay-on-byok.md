---
title: "PR #706: Force Cerebras OpenRouter calls to stay on BYOK"
type: source
tags: [codex]
date: 2025-11-17
source_file: raw/prs-/pr-706.md
sources: []
last_updated: 2025-11-17
---

## Summary
- add a dedicated helper to detect OpenRouter endpoints and attach the `provider.only` guard when calling Cerebras through OpenRouter so BYOK traffic never falls back to other providers
- keep the web search diagnostics logic aligned with the new helper and update the end-to-end payload test to assert the `provider` block

## Metadata
- **PR**: #706
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +64/-7 in 2 files
- **Labels**: codex

## Connections
