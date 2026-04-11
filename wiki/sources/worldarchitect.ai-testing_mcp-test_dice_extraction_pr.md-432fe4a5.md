---
title: "Dice Roll Extraction Test (PR #3588)"
type: source
tags: [testing, mcp, dice-rolls, pr-3588, ui-extraction, backward-compatibility]
sources: []
date: 2026-04-07
source_file: raw/test_dice_roll_extraction_pr.md
last_updated: 2026-04-07
---

## Summary
Test suite validating PR #3588's dice roll extraction feature. Ensures dice rolls are extracted from `action_resolution.mechanics.rolls` and populate the `dice_rolls` field for UI display while maintaining backward compatibility with legacy responses.

## Key Claims
- **Roll Extraction**: Dice rolls extracted from `action_resolution.mechanics.rolls` field, not from legacy `dice_rolls` location
- **UI Population**: Extracted rolls properly populate `dice_rolls` field for frontend display
- **Backward Compatibility**: Legacy responses with `dice_rolls` still work; system accepts either extracted or legacy format
- **Evidence Capture**: Test results saved to `/tmp/<repo>/<branch>/test_dice_roll_extraction_pr/iteration_NNN/` with full provenance
- **Server Options**: Tests run against GCP preview server, local server on port 8001, or auto-start local server

## Test Scenarios

### 1. Single d20 Combat Roll
- **Action**: "I attack the goblin with my longsword."
- **Expected**: Single d20 roll extracted from action_resolution
- **Validates**: Basic extraction works

### 2. Multiple Rolls (Attack + Damage)
- **Action**: "I attack the goblin with my longsword. Resolve the attack and damage."
- **Expected**: Multiple rolls (attack and damage) extracted
- **Validates**: Multiple roll extraction works

### 3. Skill Check Roll
- **Action**: "I try to sneak past the guards. Make a Stealth check."
- **Expected**: d20 + modifier roll extracted
- **Validates**: Non-combat rolls work

### 4. Backward Compatibility
- **Action**: Various actions
- **Expected**: Either extracted rolls OR legacy dice_rolls present
- **Validates**: Backward compatibility maintained

## Evidence Output

Results are saved to:
```
/tmp/<repo>/<branch>/test_dice_roll_extraction_pr/iteration_NNN/
├── README.md              # Package manifest
├── methodology.md         # Testing approach
├── evidence.md            # Summary with metrics
├── metadata.json          # Machine-readable metadata
├── test_results.json      # Test results and provenance
└── latest -> iteration_NNN (symlink)
```

Each iteration includes: Git provenance (branch, commit, origin), server health status, full test results per scenario, timestamps and run ID.

## Related Files
- **Feature Implementation**: `mvp_site/action_resolution_utils.py`
- **Tests**: `mvp_site/tests/test_action_resolution_utils.py`
- **LLM Instructions**:
  - `mvp_site/prompts/narrative_system_instruction.md`
  - `mvp_site/prompts/game_state_instruction.md`
- **Backward Compatibility Note**: `mvp_site/world_logic.py`

## Connections
- [[Testing MCP - Server-Level Tests with Real LLMs]] — testing framework used
- [[Smart Skill Check Testing (DICE-ayy Regression Tests)]] — related testing infrastructure

## PR Reference
- **PR #3588**: Fix: Centralize dice rolls and auto-extract to UI field
- **Related PR #3568**: Original PR (archived)