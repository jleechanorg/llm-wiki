---
title: "PR #981: fix: Migrate Grok API from deprecated Live Search to Agent Tools API"
type: source
tags: []
date: 2026-02-05
source_file: raw/prs-/pr-981.md
sources: []
last_updated: 2026-02-05
---

## Summary
- Fixes Grok API HTTP 410 error caused by xAI deprecating their Live Search API
- Migrates from deprecated `search_parameters` field to new Agent Tools API `tools` array
- Grok was failing while Gemini and Perplexity succeeded, causing only 2/3 secondary models to return results

## Metadata
- **PR**: #981
- **Merged**: 2026-02-05
- **Author**: jleechan2015
- **Stats**: +238/-247 in 9 files
- **Labels**: none

## Connections
