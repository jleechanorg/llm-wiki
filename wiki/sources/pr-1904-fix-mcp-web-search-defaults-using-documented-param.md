---
title: "PR #1904: Fix MCP web search defaults using documented parameters"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-worldarchitect-ai/pr-1904.md
sources: []
last_updated: 2025-10-30
---

## Summary
- align the Grok and Perplexity MCP installers with documented web-search configuration, including search mode defaults and the supported Sonar models
- drop the unsupported Gemini CLI web-search override while documenting that the upstream CLI already handles Google Search grounding
- ensure Grok and Perplexity patch helpers resolve template paths via SCRIPT_DIR so they work when the installer is sourced

## Metadata
- **PR**: #1904
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: codex

## Connections
