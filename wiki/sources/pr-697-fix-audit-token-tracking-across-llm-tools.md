---
title: "PR #697: fix: audit token tracking across llm tools"
type: source
tags: [codex]
date: 2025-11-17
source_file: raw/prs-/pr-697.md
sources: []
last_updated: 2025-11-17
---

## Summary
- update the Gemini tool to reuse the grounded prompt text for token estimation, honor the provider usage metadata, and log prompt/completion tokens into the summary so the cost calculator receives real counts
- switch the Perplexity tool to report the configured model id and feed its total token usage through the centralized cost calculator for accurate tier-based pricing
- recognize `step2-final-synthesis` as a synthesis identifier across both cost calculator implementations and document the s

## Metadata
- **PR**: #697
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +279/-33 in 11 files
- **Labels**: codex

## Connections
