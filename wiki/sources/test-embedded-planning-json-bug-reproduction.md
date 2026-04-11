---
title: "Embedded Planning JSON Bug Reproduction Test"
type: source
tags: [python, testing, bug-reproduction, json-parsing, narrative-response]
source_file: "raw/test_embedded_planning_json_bug.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Red-Green test suite for embedded planning block JSON appearing raw in narrative text. Reproduces a bug where LLM responses include raw JSON like `{"thinking": ..., "choices": ...}` in the narrative field instead of only in the separate structured `planning_block` field.

## Key Claims
- **Bug Reproduction**: When LLM includes raw JSON in narrative text, it should be stripped via `_strip_embedded_planning_json()`
- **JSON Keys Stripped**: Keys like `"thinking"`, `"choices"`, `"magical_oaths_binding"`, `"analysis"` must be removed from displayed narrative
- **Parsing Pipeline**: `parse_structured_response()` must clean narrative before returning
- **Edge Case Handling**: Narrative that is entirely JSON should be handled gracefully

## Key Test Functions
- `test_narrative_with_embedded_planning_json_is_cleaned`: Validates JSON keys stripped from narrative
- `test_narrative_with_only_embedded_json_is_cleaned`: Handles edge case of JSON-only narrative

## Connections
- [[PlanningBlock]] — the structured field that should contain the JSON data
- [[EmbeddedJsonStripping]] — the function that removes embedded JSON from narrative
- [[NarrativeResponseSchema]] — module containing `parse_structured_response`

## Contradictions
- None identified
