---
title: "Response Compression System"
type: concept
tags: [compression, token-reduction, summarization]
sources: ["context-optimization-implementation-plan-phases-2-4"]
last_updated: 2026-04-08
---

## Description
Phase 4 of the Context Optimization Implementation Plan focused on implementing smart truncation and summarization of tool responses, reducing tokens by 40-50%.

## Key Components

### Response Compressor
File: `.claude/hooks/response_compressor.py`
Compression rules per response type:
- **test_output**: preserve failures/errors/summary, compress passed_tests/progress, max 50 lines
- **file_listing**: preserve directories/important_files, compress timestamps/permissions, max 30 entries
- **search_results**: preserve matches/context, compress repetitive patterns, max 20 results

### Smart Summarization
File: `.claude/services/response_summarizer.py`
- Applies compression based on tool type
- Preserves critical information while reducing verbosity

## Success Metrics
- 40-50% token reduction in tool responses
- Preserves critical failure/error information
- Maintains actionable context

## Connections
- [[Context Optimization Implementation Plan Phases 2-4]] — Parent plan
- [[Command Output Trimmer Hook]] — Phase 1 parallel implementation
- [[Claude Code]] — Execution environment
