---
title: "PR #374: fix: guard Cerebras web search payloads for native endpoints"
type: source
tags: [codex]
date: 2025-10-16
source_file: raw/prs-/pr-374.md
sources: []
last_updated: 2025-10-16
---

## Summary
- disable Cerebras web search when the configured endpoint is not the OpenRouter gateway and log the reason
- reuse the shared DEFAULT_PRIMARY_MODEL fallback and derive response metadata provider from the endpoint domain

## Metadata
- **PR**: #374
- **Merged**: 2025-10-16
- **Author**: jleechan2015
- **Stats**: +22/-3 in 1 files
- **Labels**: codex

## Connections
