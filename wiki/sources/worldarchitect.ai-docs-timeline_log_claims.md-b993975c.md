---
title: "Timeline Log Budgeting Claim Review"
type: source
tags: [worldarchitect.ai, timeline-log, budget, llm-request, duplication-factor, architecture]
sources: []
source_file: docs/timeline_log_budgeting_claims.md
last_updated: 2026-04-07
---

## Summary
Reviews and debunks the claim that timeline log text is duplicated in the structured LLM request, explaining why the `TIMELINE_LOG_DUPLICATION_FACTOR` of 2.05 was incorrectly applied. The timeline log string is built for prompt scaffolding but never serialized into the API payload.

## Key Claims
- **Claim #1**: Timeline log text is NOT serialized in structured `LLMRequest` — only truncated `story_history` plus entity-tracking metadata is sent
- **Claim #2**: `_call_llm_api_with_llm_request` sends only the JSON string from `LLMRequest.to_json()`, excluding any timeline log text
- **Claim #3**: Dividing story budget by 2.05 artificially halves usable story context without preventing any actual duplication
- **Claim #4**: The duplication guard is gated via `TIMELINE_LOG_INCLUDED_IN_STRUCTURED_REQUEST = False`, keeping full story budget

## Evidence
1. `LLMRequest.to_json()` emits structured fields (game_state, story_history, entity_tracking, checkpoint_block, core_memories, selected_prompts, sequence_ids) but NOT timeline log string
2. `_call_llm_api_with_llm_request` converts LLMRequest to JSON and calls `_call_llm_api` with that single JSON string — the earlier `full_prompt` with timeline log is excluded
3. `EntityInstructionGenerator.generate_entity_instructions` uses timeline_log_string for heuristic classification but does not embed it in serialized payload

## Impact
- Early revisions incorrectly divided story budget by 2.05 despite no duplicated timeline text being sent
- Premature truncation was triggered without preventing any overflow
- Guard is now dormant (False), preserving full story budget for structured request path

## Suggested Next Steps
- Keep duplication guard gated unless a prompt path explicitly serializes timeline_log text
- If timeline log must be sent, add it to `LLMRequest` explicitly rather than relying on legacy prompt concatenation

## Contradictions
- Contradicts earlier PR claim: The original PR asserted timeline log text was present alongside `story_history` in structured request, justifying the 2.05 duplication factor
