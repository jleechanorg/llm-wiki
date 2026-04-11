---
title: "PR #1484: Context Optimization: Remove unused MCP servers to reduce token consumption"
type: source
tags: []
date: 2025-08-27
source_file: raw/prs-worldarchitect-ai/pr-1484.md
sources: []
last_updated: 2025-08-27
---

## Summary
- Remove unused MCP servers consuming ~34K tokens (notion, puppeteer, react)
- Disable playwright and ios-simulator by default with environment flags
- Preserve all essential functionality while reducing context consumption
- Improve session longevity from 93% to ~70% context usage

## Metadata
- **PR**: #1484
- **Merged**: 2025-08-27
- **Author**: jleechan2015
- **Stats**: +365/-114 in 3 files
- **Labels**: none

## Connections
