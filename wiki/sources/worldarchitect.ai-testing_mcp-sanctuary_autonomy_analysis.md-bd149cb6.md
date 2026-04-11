---
title: "Sanctuary Mode Autonomy Analysis"
type: source
tags: [worldarchitect-ai, testing, sanctuary-mode, autonomy, game-mechanics]
sources: []
source_file: testing_mcp/sanctuary_autonomy_analysis.md
last_updated: 2026-04-07
---

## Summary
Analysis of Sanctuary Mode activation and expiration autonomy in WorldArchitect AI. Tests reveal that activation requires explicit completion language (not autonomous), while expiration happens automatically when the turn counter passes the expiry threshold.

## Key Claims
- **Activation: NOT Autonomous** — Sanctuary requires explicit completion language ("quest complete", "mission finished", "successfully completed") to activate
- **Expiration: Autonomous** — Once activated, sanctuary automatically expires when `current_turn >= expires_turn` without player action
- **Neutral actions don't trigger** — Actions like "I search the body" or "I continue exploring" are not recognized as quest completion
- **Required language patterns** — "quest complete", "mission finished", "successfully completed", explicit scale indicators ("MINOR scale", "MAJOR arc")

## Test Evidence

### Prompted Activation (PASSED)
- Input: "The quest is finished. I have successfully completed the Cragmaw Hideout mission. This is a MINOR scale quest completion."
- Result: Sanctuary activated at turn 5, expires turn 10
- Evidence: `/tmp/worldarchitect.ai/claude/add-sanctuary-mode-DNbxo/sanctuary_lifecycle/iteration_007/`

### Autonomous Activation (FAILED)
- Input: "I search Klarg's body for valuables."
- Result: No sanctuary_mode state created
- Evidence: `/tmp/worldarchitect.ai/claude/add-sanctuary-mode-DNbxo/sanctuary_lifecycle_autonomous/iteration_001/`

## Recommendations
1. **Production use:** Use explicit completion language in prompts/instructions for reliable activation
2. **Testing:** Use prompted mode for CI/CD tests to avoid flakiness
3. **Future enhancement:** Consider improving LLM prompts to recognize completion from context (boss defeated, dungeon cleared)
