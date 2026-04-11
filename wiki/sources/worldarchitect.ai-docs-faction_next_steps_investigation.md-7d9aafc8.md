---
title: "Faction Tool Invocation - Next Steps Investigation"
type: source
tags: [faction-minigame, tool-invocation, semantic-classifier, intent-routing, temperature]
sources: []
date: 2026-01-15
source_file: docs/faction_next_steps_investigation.md
last_updated: 2026-04-07
---

## Summary
Investigates the gap between iteration_018 (28% tool invocation) vs iteration_011 (56% baseline). Temperature fix (0.1→0.9) improved tool invocation 7x (4%→28%), but a 28% gap remains. The investigation focuses on the Semantic Intent Classifier added after iteration_011, which routes based on input phrases—if input doesn't match faction phrases, it returns MODE_CHARACTER (story mode) instead of MODE_FACTION, preventing tool availability.

## Key Claims

- **Temperature Fix Works:** Changing from 0.1 to 0.9 improved tool invocation from 4% to 28% (7x improvement), matching iteration_011's temperature
- **Gap Remains:** iteration_018 (28%) still below iteration_011 (56%) — a 28% gap
- **Semantic Classifier Added After Baseline:** The Semantic Intent Classifier was introduced after iteration_011 and may be interfering with agent routing
- **Classifier Routes Based on Phrases:** Intent classifier checks input against ANCHOR_PHRASES for MODE_FACTION; if input doesn't match (e.g., "How many troops do I have?"), returns MODE_CHARACTER
- **Fallback Should Work But May Not:** Priority 7 fallback (FactionManagementAgent.matches_game_state()) should catch missed classifications but may not be functioning correctly
- **Three Investigation Areas:** (1) semantic classifier interference, (2) agent selection timing, (3) tool availability when agent IS selected

## Key Quotes

> "The Classifier Routes Based on Input Phrases" — iteration_011 used direct agent selection, current uses semantic classifier as "PRIMARY BRAIN"

> "Fallback Should Work: Priority 7 fallback checks `faction_minigame.enabled` and should still route to FactionManagementAgent"

## Investigation Questions

1. **Is FactionManagementAgent Being Selected?** Check logs for `FACTION_MODE_ACTIVE`, `SEMANTIC_INTENT_FACTION` messages
2. **Is Semantic Classifier Interfering?** Does classifier return MODE_CHARACTER for faction queries?
3. **Are Tools Available When Agent Is Selected?** Verify `FactionManagementAgent.get_tools()` returns `FACTION_TOOLS`
4. **Is Agent Selection Happening Too Late?** Agent selection may happen after prompt building, excluding tools from API request

## Recommended Next Steps

1. Analyze test logs for agent selection patterns
2. Compare test inputs that trigger tool calls vs those that don't
3. Review semantic classifier phrase matching and 0.65 similarity threshold
4. Verify Priority 7 fallback logic is working
5. Check tool availability when FactionManagementAgent is selected

## Connections

- [[Faction Tool Invocation Investigation]] — prior investigation establishing 56%→4% drop
- [[Temperature Analysis for Faction Tool Calling]] — establishes temperature 0.9 baseline
- [[LLM Game State Accuracy Analysis - Iteration 021]] — related tool integration issues

## Contradictions

- Contradicts [[Temperature Analysis for Faction Tool Calling]] on: Temperature alone explains 4%→28% but not the full 56% baseline — suggests additional factors beyond temperature
