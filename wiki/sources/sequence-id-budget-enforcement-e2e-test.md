---
title: "Sequence ID Budget Enforcement E2E Test (worktree_logs6-cc4)"
type: source
tags: [e2e-testing, sequence-ids, token-budget, context-truncation, llm-service]
source_file: "raw/sequence-id-budget-enforcement-e2e-test-worktree_logs6-cc4.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end test verifying that sequence IDs in LLM requests respect the allocated budget from `budget_result`. The bug fix ensures `final_sequence_ids` is capped when over budget, preserving the most recent sequence IDs (truncation from oldest).

## Key Claims
- **Budget Allocation**: Sequence IDs in LLM requests must respect allocated budget from `budget_result`
- **Budget Cap Fix**: Fix applies cap to `final_sequence_ids` when over budget
- **Most Recent Preserved**: Truncation keeps most recent sequence IDs, removes oldest ones
- **Context Mismatch Bug**: Previously `sequence_id_list_string` was measured on `sequence_id_context` (bounded to 20% of story) but built from `truncated_story_context` (full allocated), causing budget overflow

## Key Quotes
> "Previously, sequence_id_list_string was measured on sequence_id_context (bounded to 20% of story) but built from truncated_story_context (full allocated). This meant the actual sequence ID list could exceed the allocated budget."

> "Fix: Now sequence_id_list_string is capped to allocated budget as final_sequence_ids, keeping the most recent IDs to fit within the token budget."

## Connections
- [[token_utils]] — contains `estimate_tokens` for token budget calculation
- [[llm_service]] — LLM service that handles sequence ID context injection
- [[End2EndBaseTestCase]] — base test class for E2E tests

## Contradictions
- None identified
