---
title: "Streaming Refactoring Plan - Task to Bead Mapping"
type: source
tags: [streaming, llm-api, refactoring, json-mode, tool-execution, response-validation]
sources: []
date: 2026-01-20
last_updated: 2026-04-07
---

## Summary

Implementation plan mapping streaming architecture refactoring tasks to tracking beads for PR #2541. Addresses critical consolidation of streaming/non-streaming paths, JSON mode support, two-phase tool execution, and response validation. All tests passing, ready for implementation.

## Key Claims

- **Critical Bug Fixed**: Missing json import in gemina_provider.py resolved 7 test failures (commit 2413aa290)
- **REV-h1g - Consolidate Streaming and Non-Streaming**: Create unified codepath for story generation via `_prepare_story_request()` and `_generate_story_response(streaming: bool)`, eliminating ~150 lines of duplication
- **REV-05w - Add JSON Mode + Tool Execution**: Two-phase streaming with Phase 1 JSON chunks containing tool_requests, tool execution during streaming, Phase 2 final narrative with injected results
- **REV-m7u - Add Response Validation**: Validate streaming responses before Firestore persistence including schema, dice rolls, faction minigame state
- **REV-69t - Add Integration Tests**: Verify streaming produces equivalent results to non-streaming (narrative, tool execution, structured output parity)
- **REV-nh9 - Update Frontend for Tool Events**: Real-time tool execution display during streaming

## Key Quotes

> "Create single unified codepath for story generation" — REV-h1g objective

> "Streaming should produce same structured output as non-streaming" — REV-05w objective

> "Streaming persists LLM responses without validation" — Current issue in REV-m7u

## Connections

- [[WorldArchitect.AI]] — the platform being refactored
- [[Beads]] — tracking system for implementation tasks

## Contradictions

None identified.

