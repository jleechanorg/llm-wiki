---
title: "Faction Ranking Recompute Tests"
type: source
tags: [python, testing, faction-combat, ranking, fp-calculation, game-mechanics]
source_file: "raw/test_faction_ranking_recompute.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating faction ranking recompute logic in gemini_provider. Tests verify that ranking is correctly recomputed when LLM emits ranking without power tool, when LLM emits ranking with stale FP causing mismatch detection, and that Phase 2 response includes tool_requests mirroring server-executed args/results. This is a HIGH priority fix for FP/ranking divergence.

## Key Claims
- **Ranking Without Power Tool**: When LLM emits faction_calculate_ranking without faction_calculate_power, the ranking tool request is DROPPED (not executed with placeholder FP), power is auto-invoked from state_updates, and ranking is auto-attached using the FP from auto-invoked power
- **Stale FP Detection**: When LLM emits ranking with stale FP, mismatch is detected and ranking is recomputed with correct FP
- **Phase 2 Tool Request Mirroring**: Phase 2 response includes tool_requests that mirror server-executed args/results
- **Auto-Attachment Pattern**: Ranking is auto-attached only after power calculation completes with correct values

## Key Test Scenarios
1. **test_ranking_without_power_is_dropped_and_recomputed**: Verifies ranking with FP=0 is dropped, power is auto-invoked, ranking recalculated with correct FP
2. **test_ranking_with_stale_fp_mismatch**: Verifies detection when LLM provides ranking with outdated FP values
3. **test_phase2_tool_request_mirroring**: Verifies Phase 2 tool requests match server execution

## Connections
- [[Faction Combat Power Calculation]] — power calculation that must precede ranking
- [[Faction Ranking]] — ranking depends on accurate power values
- [[Gemini Provider]] — provider handling the ranking recompute logic

## Contradictions
- None currently documented
