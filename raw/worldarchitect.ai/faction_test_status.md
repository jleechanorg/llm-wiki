# Faction Test Status - iteration_020

**Test Name**: `iteration_020_prompt_warnings`  
**Started**: 2026-01-15 01:14 AM  
**Status**: ⏳ Running

## Changes in This Iteration

### Prompt Updates (Priorities 1-3)
1. ✅ Added critical section: "Cached Values Are Stale" warning at top of prompt
2. ✅ Added reminder tokens (`<<CALL-TOOLS-NOW>>`) at strategic points:
   - Before `faction_calculate_power` usage section
   - Before `faction_calculate_ranking` usage section  
   - In "Faction Tool Usage" section
3. ✅ Added wrong vs. correct examples:
   - Example showing WRONG usage (using cached values)
   - Example showing CORRECT usage (calling tools first)
4. ✅ Enhanced forbidden rules:
   - Explicitly forbids using cached `game_state.faction_minigame.faction_power`
   - Explicitly forbids using cached `game_state.faction_minigame.ranking`

### Code Changes
- ✅ Added tool availability logging in `gemini_provider.py`
- ✅ Logs show tools passed to API and tools invoked by LLM

## Expected Results

After test completes, we expect:
- **Status actions**: 0% → 50%+ tool invocation (currently 0% in iteration_019)
- **Ranking actions**: 0% → 50%+ tool invocation (currently 0% in iteration_019)
- **Overall**: 40% → 50%+ tool invocation (currently 40% in iteration_019)

## Test Progress

The test is currently running. It performs 20+ turns with LLM API calls, which typically takes 10-20 minutes.

**Evidence Location** (created when test completes):
`/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/iteration_020_prompt_warnings/`

## Next Steps After Test Completes

1. Analyze results and compare to iteration_019
2. Check if status/ranking actions now call tools
3. Verify overall tool invocation improvement
4. Document findings and plan next iteration if needed
