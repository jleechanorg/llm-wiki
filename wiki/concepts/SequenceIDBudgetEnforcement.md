---
title: "Sequence ID Budget Enforcement"
type: concept
tags: [token-budget, llm-context, context-truncation]
sources: []
last_updated: 2026-04-08
---

## Description
Mechanism ensuring sequence IDs included in LLM requests stay within allocated token budget. When sequence ID list exceeds budget, most recent IDs are preserved while oldest are removed.

## Problem
Previously, `sequence_id_list_string` was measured on `sequence_id_context` (bounded to 20% of story) but built from `truncated_story_context` (full allocated). This mismatch caused actual sequence ID list to exceed allocated budget.

## Solution
Cap `final_sequence_ids` to allocated budget measured on the same context used for construction. Keep most recent sequence IDs to maintain relevance to current game state.

## Related
- [[TokenBudgetCalculation]]
- [[ContextTruncation]]
- [[LLMRequestContext]]
