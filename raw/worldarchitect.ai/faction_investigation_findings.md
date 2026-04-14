# Faction Tool Invocation Investigation - Findings

**Date:** 2026-01-15  
**Investigation Type:** Historical comparison (no code changes)  
**Status:** Key findings identified, awaiting GenesisFaction response

## Investigation Summary

Conducted historical comparison between `iteration_011` (56% tool invocation) and current state (4% tool invocation) to identify root causes.

## Key Findings

### ✅ 1. Tool Definitions - IDENTICAL

**Finding:** Tool definitions in `mvp_site/faction/tools.py` are **identical** between `iteration_011` and current state.

**Evidence:**
- No diff found: `diff -u /tmp/tools_iteration_011.py mvp_site/faction/tools.py` (empty)
- Same line count: 586 lines in both versions
- Same tool count: 5 tools (`faction_calculate_power`, `faction_calculate_ranking`, `faction_simulate_battle`, `faction_intel_operation`, `faction_fp_to_next_rank`)
- All tools present in both versions

**Conclusion:** Tool definitions are NOT the root cause.

### ✅ 2. Model Version - IDENTICAL

**Finding:** Model version used is **identical** between `iteration_011` and current state.

**Evidence:**
- Both use: `gemini-3-flash-preview` (pinned in test)
- Test file shows: `DEFAULT_MODEL = "gemini-3-flash-preview"` in both versions

**Conclusion:** Model version is NOT the root cause.

### ✅ 3. Temperature Override - IDENTICAL

**Finding:** Temperature override logic is **identical** between `iteration_011` and current state.

**Evidence:**
- Both versions: `temperature_override = 0.1` when `FactionManagementAgent.minigame_enabled == True`
- Same logging message: "Using temperature 0.1 for tool calling (allows reconsideration)"

**Conclusion:** Temperature settings are NOT the root cause.

### ✅ 4. Tool Passing to Gemini API - IDENTICAL

**Finding:** How tools are passed to Gemini API is **identical** between `iteration_011` and current state.

**Evidence:**
- Both versions: `all_tools = DICE_ROLL_TOOLS + FACTION_TOOLS`
- Both versions: `config.tools = gemini_tools` (via `_build_gemini_tools()`)
- Both versions: `function_calling_config=types.FunctionCallingConfig(mode="AUTO")`

**Conclusion:** Tool passing mechanism is NOT the root cause.

### ✅ 5. System Instruction Loading - VERIFIED WORKING

**Finding:** Faction minigame instruction IS being loaded correctly.

**Evidence:**
- `FactionManagementAgent` correctly detects `minigame_enabled = True`
- System instructions built successfully: 284,149 chars
- Faction minigame instruction (70,535 chars) is included
- Log shows: "🎮 FACTION_MINIGAME: Loaded minigame instruction"

**Conclusion:** System instruction loading is working correctly.

## Critical Observations

### 🔴 Observation 1: Only Combat Actions Trigger Tools

**Finding:** In `iteration_017`, only Turn 22 (combat action) invoked tools.

**Analysis:**
- Combat actions: `faction_simulate_battle` requires explicit battle parameters
- Status/ranking queries: Should call `faction_calculate_power` and `faction_calculate_ranking` but don't
- Build/recruit actions: Should call `faction_calculate_power` but don't

**Hypothesis:** LLM may be treating tools as "optional helpers" for complex operations (battles) but not for simple queries (status checks).

### 🔴 Observation 2: Faction Headers Generated Without Tools

**Finding:** 22/25 turns generated faction headers WITHOUT calling tools.

**Analysis:**
- Headers include FP values (e.g., "FP: 3,502")
- But `faction_calculate_power` was NOT called in those turns
- LLM is hallucinating FP values instead of calling tools

**Hypothesis:** LLM may be:
1. Using cached/previous turn FP values
2. Estimating FP values based on narrative context
3. Ignoring tool requirements entirely

### 🔴 Observation 3: Prompt Structure Hypothesis Disproven

**Finding:** Even with exact `iteration_011` prompt structure, tool invocation dropped to 4%.

**Analysis:**
- Prompt structure alone cannot explain the regression
- Other factors must be involved

## Potential Root Causes (Remaining)

### 1. LLM Behavior Changes (Model Updates)

**Hypothesis:** Gemini 3 Flash Preview model behavior may have changed between `iteration_011` and now.

**Evidence:**
- Model version is identical (`gemini-3-flash-preview`)
- But model behavior could have changed via:
  - Google's internal model updates (same version, different weights)
  - API-side behavior changes
  - Tool calling optimization changes

**Investigation Needed:**
- Check Gemini API changelog/release notes
- Compare raw API responses between iterations
- Test with different Gemini model versions

### 2. Context Window / Prompt Truncation

**Hypothesis:** System instructions may be getting truncated, cutting off tool definitions or critical instructions.

**Evidence:**
- System instructions: 284,149 chars (~71K tokens)
- Gemini 3 Flash: 1M context window (should fit)
- But tool definitions are at the END of the prompt stack

**Investigation Needed:**
- Check if tool definitions are actually included in API request
- Verify context window usage
- Check for truncation logic

### 3. Tool Calling Mode / Configuration

**Hypothesis:** Tool calling mode or configuration may have changed.

**Evidence:**
- `function_calling_config=types.FunctionCallingConfig(mode="AUTO")` is identical
- But Gemini's interpretation of "AUTO" mode may have changed

**Investigation Needed:**
- Try `mode="ANY"` (force tool calling)
- Check Gemini API documentation for mode changes
- Compare tool calling behavior with different modes

### 4. System Instruction Conflicts

**Hypothesis:** Other system instructions may be conflicting with faction tool calling instructions.

**Evidence:**
- Multiple prompts loaded: master_directive, game_state, planning_protocol, faction_management, dnd_srd, mechanics, faction_minigame
- Conflicting "MANDATORY" instructions may confuse the LLM

**Investigation Needed:**
- Review all system instructions for conflicting tool calling guidance
- Check instruction ordering/precedence
- Test with minimal prompt set

### 5. Response Parsing / Tool Detection

**Hypothesis:** Tool calls may be present in LLM responses but not being detected/parsed correctly.

**Evidence:**
- Tool invocation detection relies on `debug_info.tool_results`
- Parsing logic may have changed

**Investigation Needed:**
- Check raw Gemini API responses for tool calls
- Verify tool call extraction logic
- Compare parsing between iterations

## Next Steps (Priority Order)

### High Priority
1. **Check raw Gemini API responses** - Are tool calls present but not detected?
2. **Verify tool definitions in API request** - Are tools actually sent to Gemini?
3. **Test with `mode="ANY"`** - Force tool calling to see if behavior changes

### Medium Priority
4. **Review system instruction conflicts** - Check for conflicting "MANDATORY" instructions
5. **Check context window usage** - Verify no truncation is occurring
6. **Compare tool call parsing logic** - Ensure detection is working correctly

### Low Priority
7. **Test with different Gemini models** - Isolate model-specific behavior
8. **Check Gemini API changelog** - Look for tool calling behavior changes
9. **Review instruction ordering** - Test different prompt orderings

## Questions for GenesisFaction

1. **Model behavior changes:** Could Gemini 3 Flash Preview behavior have changed even with the same version string?
2. **Tool calling mode:** Should we try `mode="ANY"` instead of `mode="AUTO"` to force tool calling?
3. **Context window:** Could 284K chars (~71K tokens) be causing issues even within the 1M limit?
4. **Instruction conflicts:** Could conflicting "MANDATORY" instructions be confusing the LLM?
5. **Response parsing:** Should we check raw API responses to see if tool calls are present but not detected?

## Conclusion

**Key Finding:** All code-level factors (tool definitions, model version, temperature, tool passing, system instruction loading) are **identical** between `iteration_011` and current state.

**Implication:** The regression must be caused by:
1. **LLM behavior changes** (model updates, API changes)
2. **Runtime factors** (context window, instruction conflicts, parsing)
3. **Environmental factors** (API-side changes, tool calling optimization)

**Recommendation:** Focus investigation on:
- Raw API response analysis
- Tool calling mode configuration
- System instruction conflict detection
- Response parsing verification
