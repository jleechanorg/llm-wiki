---
title: "PR #757: fix: harden perplexity token handling"
type: source
tags: [codex]
date: 2025-11-17
source_file: raw/prs-/pr-757.md
sources: []
last_updated: 2025-11-17
---

## Summary
- normalize Perplexity usage parsing to coerce `total_tokens` into a number before cost calculation
- include the configured model in Perplexity token usage logging for clearer post-merge observability

## Metadata
- **PR**: #757
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +4/-2 in 1 files
- **Labels**: codex

## Connections
