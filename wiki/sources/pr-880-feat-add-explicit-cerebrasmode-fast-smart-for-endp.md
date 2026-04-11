---
title: "PR #880: feat: Add explicit CerebrasMode (FAST/SMART) for endpoint selection"
type: source
tags: []
date: 2025-12-02
source_file: raw/prs-/pr-880.md
sources: []
last_updated: 2025-12-02
---

## Summary
- Introduces `CerebrasMode` enum to explicitly control Cerebras endpoint routing
- **FAST**: Direct Cerebras API (80k context, faster, no web search)
- **SMART**: OpenRouter endpoint (32k context, web search capable)
- Updates `ToolRegistry.getLLMCaller` to accept optional `cerebrasMode` parameter
- Refactors `SecondOpinionAgent` to use explicit modes instead of bypassing `getLLMCaller`
- Removes duplicated endpoint selection logic
- Runtime behavior (validated by REAL smoke tests on PR preview

## Metadata
- **PR**: #880
- **Merged**: 2025-12-02
- **Author**: jleechan2015
- **Stats**: +391/-179 in 15 files
- **Labels**: none

## Connections
