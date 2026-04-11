---
title: "WorldArchitect.AI 20-Turn Test Improvement"
type: source
tags: [worldarchitect-ai, testing, e2e, iteration-comparison, prompt-engineering]
date: 2026-01-12
source_file: raw/20turn-test-comparison.md
last_updated: 2026-04-07
---

## Summary
Analysis comparing E2E test iterations 004 (before prompt fixes) and 005 (after 5 prompt clarifications) for WorldArchitect.AI's 20-turn test. Both tests completed successfully with 25 turns each, but iteration 005 shows significant improvements in coherence: timestamp progression (no reversals), gold calculation (consistent amounts), level progression (incremental), and tutorial completion (clarified meaning).

## Key Claims
- **Both iterations passed**: 25 successful turns, 0 failed turns in both 004 and 005
- **Timestamp progression**: Iteration 005 eliminates reversals (e.g., 11:15→10:45) and ensures forward progression with small increments (5-15 min per action)
- **Gold calculation**: Dual gold clarification prevents confusion between character.gold and faction.resources.gold; iteration 005 shows consistent 10gp amounts
- **Level progression**: Iteration 005 ensures incremental progression (Level 1→Level 2) vs iteration 004's jump (Level 1→Level 3)
- **Tutorial clarification**: Iteration 005 clarifies "tutorial PHASE complete" vs "campaign complete"
- Test evidence stored in `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/`

## Key Quotes
> "NEVER go backwards in time" — timestamp progression rule added to faction_minigame_instruction.md
> "Always show level progression incrementally" — level progression rule added to game_state_instruction.md
> "[TUTORIAL PHASE COMPLETE - Campaign continues]" — clarified tutorial completion message

## Connections
- [[WorldArchitect.AI]] — the platform being tested
- [[WorldArchitect.AI Full User Journey Test Spec]] — related E2E test specification
- [[WorldArchitect.AI GitHub Development Statistics]] — development velocity metrics

## Contradictions
- None detected — iteration 005 improvements address all iteration 004 issues
