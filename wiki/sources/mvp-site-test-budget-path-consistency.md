---
title: "test_budget_path_consistency.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
TDD tests verifying single budget path consistency - ensures only the new budget allocator is used, not legacy scaffold tokens calculation. Tests verify merge conflicts are resolved and budget integration works correctly.

## Key Claims
- No merge conflict markers in llm_service.py
- Uses new `_allocate_request_budget` from context_compaction, not legacy scaffold
- No `scaffold_tokens_raw` pattern in budget path
- Uses `budget_result.get_story_budget()` not manual calculation
- Sequence ID budget uses truncated story context
- Compacted game_state preserves campaign_id and user_settings
- Budget allocator returns expected structure with get_story_budget(), allocations, warnings, compacted_content

## Connections
- [[llm_service]] — the module being tested
- [[context_compaction]] — provides the budget allocator