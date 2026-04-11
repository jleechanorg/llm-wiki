---
title: "Faction Tool Failure Examples - Iteration 021"
type: source
tags: [faction-minigame, tool-invocation, tool-failure, hallucination, game-state, investigation]
sources: [worldarchitect.ai-docs-faction_status_ranking_analysis.md-f06f5508, worldarchitect.ai-docs-faction_investigation_next_steps.md-e3fcd5bf, worldarchitect.ai-docs-faction_next_steps_summary.md-08c1c614, worldarchitect.ai-docs-faction_next_steps_after_40percent.md-11b18b81, worldarchitect.ai-docs-faction_llm_game_state_accuracy.md-46bd38d0]
date: 2026-04-07
source_file: Faction Tool Failure Examples - Iteration 021
last_updated: 2026-04-07
---

## Summary
Analysis of 25-turn test run (Iteration 021) cataloging specific examples where faction tools (`faction_calculate_power`, `faction_calculate_ranking`) were either not invoked when they should have been, or were invoked but failed validation due to hallucination. The most critical finding: Turn 23 explicitly asked "How powerful are we now?" and the LLM answered without calling the tool—suggesting cached/stale data or hallucinated values.

## Key Claims

### Category 1: Tools Not Invoked (Missed Opportunities)

| Turn | Action | Expected Tool | Actual | Severity |
|------|--------|---------------|--------|----------|
| 5 | "What's my current standing among the factions?" | faction_calculate_ranking | none | Medium |
| 12 | "Build some artisan workshops" | faction_calculate_power | none | Medium |
| 13 | "Test our forces with a small skirmish" | faction_calculate_power | none | Low |
| 14 | "Form an alliance with the Shadow Covenant" | faction_calculate_ranking | none | Low |
| 16 | "Set up a library for research" | faction_calculate_power | none | Medium |
| 18 | "Strike back and take their resources" | faction_calculate_power, faction_calculate_ranking | none | High |
| 20 | "Set up magical wards" | faction_calculate_power | none | Medium |
| 23 | "How powerful are we now? What's our total faction strength?" | faction_calculate_power | none | **CRITICAL** |

### Category 2: Tools Invoked But Failed Validation

- **Turn 4**: Tools invoked correctly (`faction_calculate_power`, `faction_calculate_ranking`) but validation failed—LLM reported 29,000 FP when it should have been ~54,000 (off by 25,000, variance threshold 5,400). Tool was called but LLM ignored the result.

### Root Cause Analysis

The LLM appears to read cached game state values (`faction_power`, `ranking`) directly instead of calling tools to recalculate. Cached values appear "correct" to the LLM, and the prompt lacks explicit warnings about stale cached data. This explains:
1. Why explicit power queries (Turn 23) get answered without tool calls
2. Why Turn 4 showed tool invocation but wrong values—the tool was called, but LLM used stale cached value instead of tool output

## Connections
- [[worldarchitect.ai-docs-faction_status_ranking_analysis.md-f06f5508]] — root cause: LLM reads cached values instead of calling tools
- [[worldarchitect.ai-docs-faction_investigation_next_steps.md-e3fcd5bf]] — 6-phase investigation plan
- [[worldarchitect.ai-docs-faction_next_steps_summary.md-08c1c614]] — 40%→56% gap analysis
- [[worldarchitect.ai-docs-faction_llm_game_state_accuracy.md-46bd38d0]] — related finding: LLM calculates correctly but ignores tool output

## Contradictions
- Contradicts [[worldarchitect.ai-docs-faction_llm_game_state_accuracy.md-46bd38d0]] on Turn 5: That source says LLM "can calculate from game state" correctly, but this source shows Turn 5 didn't call tools. The distinction: calculation capability exists but is not being used when it should be.
