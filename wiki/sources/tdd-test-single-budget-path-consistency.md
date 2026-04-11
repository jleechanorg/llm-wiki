---
title: "TDD Test: Single Budget Path Consistency"
type: source
tags: [python, testing, unittest, tdd, budget-allocation, context-compaction]
source_file: "raw/tdd-test-single-budget-path-consistency.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite validating that llm_service.py uses a single budget path—the new allocator from context_compaction—rather than legacy scaffold calculations. Tests verify no merge conflict markers exist and that budget allocation integrates correctly with continue_story.

## Key Claims
- **No Merge Conflicts**: llm_service.py contains no merge conflict markers (<<<<<<< HEAD, =======, >>>>>>>)
- **Single Budget Path**: continue_story uses new _allocate_request_budget allocator, not legacy scaffold pattern
- **Budget Integration**: budget_result.get_story_budget() is used consistently, not manual max_input_allowed - scaffold_tokens calculation
- **Sequence ID Context Truncation**: _get_sequence_id_context_for_budget truncates oversized story context for budget calculations

## Key Code Patterns
```python
# New pattern (should exist):
budget_result = _allocate_request_budget(...)
budget_result.get_story_budget()

# Legacy pattern (should NOT exist):
scaffold_tokens_raw = estimate_tokens(prompt_scaffold)
max_input_allowed - scaffold_tokens
```

## Connections
- [[llm_service]] — main module under test
- [[context_compaction]] — module containing new budget allocator
- [[continue_story]] — function using budget allocation
- [[TDD]] — testing methodology
- [[BudgetAllocation]] — architectural pattern being validated

## Contradictions
- []
