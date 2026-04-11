---
title: "PR #355: feat: enforce live web search across llm stack"
type: source
tags: [codex]
date: 2025-10-16
source_file: raw/prs-/pr-355.md
sources: []
last_updated: 2025-10-16
---

## Summary
- attach provider-specific `webSearchDiagnostics`, source counts, and totals to `agent.second_opinion` responses so smoke and integration suites can assert live search enforcement end-to-end
- extend the shared OpenAI config typing plus every LLM tool to normalize and expose enforced web-search payloads (tool choice, search options, and retrieved citations) via response metadata/getters
- exercise the updated pipeline against the local MCP server to confirm the JSON payload now carries enforced

## Metadata
- **PR**: #355
- **Merged**: 2025-10-16
- **Author**: jleechan2015
- **Stats**: +2859/-344 in 25 files
- **Labels**: codex

## Connections
