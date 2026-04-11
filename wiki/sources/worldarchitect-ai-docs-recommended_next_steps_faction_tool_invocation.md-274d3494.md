---
title: "Recommended Next Steps - Faction Tool Invocation"
type: source
tags: [worldarchitect-ai, faction-minigame, tool-invocation, agent-selection, semantic-classifier, gemini]
sources: []
date: 2026-01-15
source_file: raw/recommended_next_steps_faction_tool_invocation.md
last_updated: 2026-04-07
---

## Summary
Analysis of tool invocation rate issues for WorldArchitect.AI faction minigame system. Current 28% tool invocation is below 56% target. Root cause identified as semantic classifier interfering with direct agent selection. Recommended fix is to force FactionManagementAgent selection when minigame is enabled (Priority 1), bypassing the classifier entirely to match iteration_011 behavior.

## Key Claims
- **Tool Invocation Gap**: Current 28% vs target 56% — semantic classifier is interfering with agent selection
- **Root Cause**: Classifier added after iteration_011 changed direct agent selection behavior
- **Priority 1 Fix**: Force FactionManagementAgent when `faction_minigame.enabled=True` before semantic classifier runs
- **Expected Impact**: Should restore 56% tool invocation by matching iteration_011 behavior
- **Alternative**: If Priority 1 fails, investigate agent selection logging and tool availability

## Key Quotes
> "Force FactionManagementAgent selection when `faction_minigame.enabled=True` (before semantic classifier runs)" — Recommended Priority 1 fix

> "Matches iteration_011 behavior (no classifier existed)" — Rationale for direct agent selection

## Connections
- [[WorldArchitect.AI]] — main platform
- [[WorldArchitect.AI testing_mcp/ Agent Instructions]] — agent selection logic

## Contradictions
- None identified

## Technical Details

### Current State (28%)
- Temperature: 0.9 (fixed, matches iteration_011)
- Prompt: 1902 lines (identical to iteration_011)
- Tool definitions: Identical to iteration_011
- Model: gemini-3-flash-preview (same)
- Agent selection: Semantic classifier added after iteration_011

### Recommended Priority Actions
1. **HIGH**: Force FactionManagementAgent when minigame enabled (Priority 1-2, before classifier)
2. **MEDIUM**: Verify agent selection logging in server logs
3. **MEDIUM**: Verify tools are passed to API when agent selected
4. **LOW**: Add more faction phrases to classifier