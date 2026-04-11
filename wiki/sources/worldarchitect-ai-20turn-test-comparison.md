---
title: "20-Turn Test Comparison: Before vs After Prompt Fixes"
type: source
tags: [worldarchitect-ai, testing, prompt-engineering, faction-system, QA]
date: 2026-01-12
source_file: worldarchitect-ai-docs/20turn_test_comparison.md
last_updated: 2026-04-07
---

## Summary
A/B testing comparison document evaluating prompt clarification fixes for WorldArchitect.AI's faction minigame system. Tests compared Iteration 004 (before fixes) against Iteration 005 (after 5 prompt clarifications) using 25-turn campaigns. Both tests completed successfully with no functional regressions, but Iteration 005 showed significant improvements in narrative coherence.

## Key Claims
- Both iterations completed 25 turns successfully with no failed turns
- Timestamp progression improved: Iteration 005 eliminated all time reversals (e.g., jumping from 11:15 back to 10:45)
- Gold calculation fixed: Added dual gold clarification preventing confusion between character.gold and faction.resources.gold
- Level progression fixed: Character now shows incremental level-ups (Level 1 → 2) instead of jumps (Level 1 → 3)
- Tutorial completion clarified: "tutorial complete" now clearly means "tutorial PHASE complete, campaign continues"

## Key Fixes Applied
1. **Timestamp Rules**: Added "NEVER go backwards in time" + increment rules (small actions +5-15min, combat +30-60min, end turn +7 days)
2. **Dual Gold Clarification**: Explained two separate gold pools with explicit calculation examples
3. **Level Progression Rule**: Always show incremental progression, never skip levels
4. **Tutorial Clarification**: Explicit message "[TUTORIAL PHASE COMPLETE - Campaign continues]"

## Connections
- [[WorldArchitect.AI]] — the platform being tested
- [[Faction System]] — the specific feature under test (faction minigame)

## Test Evidence
- Iteration 004: `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/iteration_004/`
- Iteration 005: `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/iteration_005/`
- Campaign ID (005): `w8rjgODGJ2UUFHaSiPi4`