---
title: "Recommended Next Steps: Faction Tool Invocation"
type: source
tags: [worldarchitect-ai, faction-minigame, tool-invocation, semantic-classifier, agent-selection, gemini]
sources: []
date: 2026-01-15
source_file: raw/recommended_next_steps_faction_tool_invocation.md
last_updated: 2026-04-07
---

## Summary
Analysis identifies root cause of 28% tool invocation rate (vs 56% target): semantic classifier interferes with FactionManagementAgent selection when minigame is enabled. Temperature and prompts match iteration_011 exactly. Recommended fix: force FactionManagementAgent selection before semantic classifier runs.

## Key Claims
- **Gap Identified**: 28% tool invocation vs 56% target (down from 56% in iteration_011)
- **Root Cause**: Semantic classifier added after iteration_011 interferes with direct agent selection
- **Fix**: Force FactionManagementAgent when `faction_minigame.enabled=True` before classifier runs
- **Expected Impact**: Should restore 56% performance

## Key Quotes
> "The Gap: 28% vs 56%"
> "Root Cause Hypothesis: Semantic classifier is interfering with agent selection."

## Connections
- [[WorldArchitect.AI React V2 Execution Plan Gap Analysis]] — related execution analysis
- [[The /qwen Slash Command]] — multi-model orchestration patterns

## Contradictions
- None identified — this analysis builds on prior iterations

## Recommended Actions (Priority Order)

### HIGH PRIORITY: Force FactionManagementAgent When Minigame Enabled
Check `faction_minigame.enabled` BEFORE semantic classifier runs (Priority 1-2). This bypasses classifier interference and matches iteration_011 behavior.

### MEDIUM PRIORITY: Verify Agent Selection Logging
Check server logs for agent selection messages to confirm FactionManagementAgent is actually being selected.

### MEDIUM PRIORITY: Verify Tool Availability
Confirm tools are passed to API when FactionManagementAgent is selected.

### LOW PRIORITY: Add More Faction Phrases to Classifier
Expand semantic classifier phrases for MODE_FACTION.
