# Gemini Code Execution Dice Fallback Issue

**Status:** Open
**Severity:** Medium
**Component:** LLM Behavior / Dice Strategy
**Discovered:** 2026-01-31
**Branch:** fix/dice-stdout-roll-singular-schema

## Summary

`gemini-3-flash-preview` inconsistently follows code_execution instructions for dice rolls. The LLM correctly uses code_execution for non-dice tasks (character creation) but falls back to `tool_requests` for combat/skill check dice rolls, causing dice to not appear in `action_resolution.mechanics.rolls`.

## Root Cause

1. **Strategy Configuration**: `gemini-3-flash-preview` is configured to use `DICE_STRATEGY_CODE_EXECUTION`
2. **System Instruction**: Clear instruction says "Do NOT output `tool_requests` for DICE... Use code_execution instead"
3. **LLM Behavior**: Model ignores instruction and emits `tool_requests` with `roll_attack`/`roll_skill_check`
4. **Server Response**: Server correctly drops dice tool_requests (code_execution strategy), no Phase 2 occurs
5. **Result**: No dice in `action_resolution.mechanics.rolls`

## Evidence

From `/tmp/worldarchitect.ai/fix/dice-stdout-roll-singular-schema/dice_roll_extraction_pr/iteration_002/`:

**Server Logs Pattern (all 4 test campaigns):**
```
initial_story: code_execution_used: True   # Character creation - CORRECT
continue_story: code_execution_used: False  # Combat action - WRONG
```

**Raw Response (single_d20_combat_roll):**
```json
{
  "tool_requests": [
    {"tool": "roll_attack", "args": {"attack_modifier": 5, "target_ac": 13, ...}}
  ],
  "action_resolution": {
    "mechanics": {"type": "attack_roll"}  // Missing "rolls" array
  }
}
```

## Impact

- Integration tests in `testing_mcp/test_dice_roll_extraction_pr.py` fail (3/4)
- UI cannot display dice results (reads from `action_resolution.mechanics.rolls`)
- Affects all combat and skill check scenarios

## Code References

- Strategy selection: `mvp_site/dice_strategy.py:19-25`
- Code execution override: `mvp_site/llm_providers/gemini_provider.py:1074-1099`
- Tool_requests stripping: `mvp_site/llm_providers/gemini_provider.py:46-67`

## Potential Fixes

1. **Make code_execution instruction more prominent** - Move to beginning of system instruction
2. **Add combat-specific code_execution examples** - Show Python code for attack rolls
3. **Repeat instruction in user prompt** - Reinforce at request time
4. **Retry mechanism** - Detect tool_requests for dice and re-prompt

## Separate From

This issue is **separate from** the `rolls` array format fix (PR #4355), which correctly documents:
- Always use `rolls` (plural, array) not `roll` (singular)
- `rolls` contains raw die values before modifiers

The format fix is correct but only applies when code_execution IS used.

## Related Files

- `mvp_site/prompts/narrative_system_instruction.md` - Added stdout schema docs
- `mvp_site/prompts/game_state_instruction.md` - Added skill check Phase 2 example
- `mvp_site/tests/test_dice_integrity_helpers.py` - TDD tests for prompt content
