# Faction Tool Invocation Investigation - 40% Analysis

**Date**: 2025-01-XX  
**Status**: 40% tool invocation (10/25 turns)  
**Gap**: 16 percentage points to reach iteration_011's 56%

## Key Findings

### 1. Tools ARE Always Passed to API ✅
- **Location**: `mvp_site/llm_providers/gemini_provider.py:477`
- **Code**: `all_tools = DICE_ROLL_TOOLS + FACTION_TOOLS`
- **Finding**: Tools are hardcoded and ALWAYS included in API calls, regardless of agent or minigame state
- **Implication**: Tool availability is NOT the issue - tools are always available to the LLM

### 2. Prompt Has Strong Tool-Calling Instructions ✅
- **Prompt file**: `mvp_site/prompts/faction_minigame_instruction.md`
- **Stats**: 85 mentions of "tool", 32 mentions of "MUST", 13 mentions of "ALWAYS", 41 mentions of "REQUIRED"
- **Key instructions**:
  - "ALWAYS call this tool at the START of every turn when `faction_minigame.enabled = true`"
  - "ALWAYS call this tool after ANY state change"
  - "CRITICAL RULE: If you call `faction_calculate_power`, you MUST immediately call `faction_calculate_ranking`"
- **Implication**: Prompt clearly instructs tool usage - prompt quality is NOT the issue

### 3. Tool Invocation Pattern Analysis

#### By Action Type:
- **Consistent (high tool invocation)**:
  - `power`: 100% (1/1) ✅
  - `combat`: 67% (2/3) ✅
  - `build`: 62% (5/8) ⚠️
  
- **Inconsistent (partial tool invocation)**:
  - `recruit`: 50% (1/2) ⚠️
  - `intel`: 50% (1/2) ⚠️
  
- **Missing (no tool invocation)**:
  - `status`: 0% (0/2) ❌
  - `ranking`: 0% (0/1) ❌
  - `diplomacy`: 0% (0/1) ❌
  - `char_creation`: 0% (0/1) ✅ (expected - before minigame enabled)
  - `char_approval`: 0% (0/1) ✅ (expected - before minigame enabled)
  - `enable_minigame`: 0% (0/1) ✅ (expected - enabling action)
  - `tutorial`: 0% (0/1) ✅ (expected - tutorial mode)
  - `end_turn`: 0% (0/1) ⚠️ (might need tools for state updates)

#### By Turn Number:
- **First tool call**: Turn 6 (after minigame enabled)
- **Last tool call**: Turn 23
- **Average turn with tools**: 14.6
- **Turns WITHOUT tools** (after minigame enabled): 9, 10, 12, 14, 16, 17, 18, 19, 24

### 4. Critical Observations

#### Observation 1: Action Type Matters
- Some action types (`status`, `ranking`) NEVER call tools, even though they should
- Other action types (`build`, `recruit`, `intel`) are inconsistent - sometimes call tools, sometimes don't
- This suggests the LLM is making context-dependent decisions about when tools are "needed"

#### Observation 2: Tools Available But Not Used
- Tools are ALWAYS passed to the API (hardcoded in `gemini_provider.py`)
- Prompt clearly instructs tool usage
- But LLM still chooses NOT to call tools ~60% of the time
- This suggests the LLM is making a "judgment call" that tools aren't needed, even when they are

#### Observation 3: Pattern Suggests LLM "Learns" Tool Usage
- Early turns (6-8) consistently call tools
- Middle turns (9-12) skip tools
- Later turns (13-23) resume calling tools
- This suggests the LLM might be "learning" when tools are needed, but inconsistently

### 5. Root Cause Hypothesis

**Primary Hypothesis**: LLM is making context-dependent decisions about tool necessity, and these decisions are inconsistent.

**Supporting Evidence**:
1. Tools are always available (hardcoded)
2. Prompt clearly instructs tool usage
3. Some action types consistently call tools (`power`, `combat`)
4. Other action types never call tools (`status`, `ranking`)
5. Some action types are inconsistent (`build`, `recruit`, `intel`)

**Possible Contributing Factors**:
1. **Context Window**: Large prompt (1903 lines, 70,535 chars) might cause LLM to "forget" tool instructions
2. **Temperature**: Current temp=0.9 (matches iteration_011) - higher temperature = more variation
3. **Action Type Context**: LLM might think `status` doesn't need tools if it can "read" the state directly
4. **Tool Calling Mode**: `mode="AUTO"` means LLM decides when to call tools - might be too permissive

### 6. Comparison to iteration_011

**What We Know**:
- iteration_011 achieved 56% tool invocation
- Current code matches iteration_011:
  - Same prompt structure (1902 lines, identical content)
  - Same temperature (0.9)
  - Same tool definitions (byte-for-byte identical)
  - Same tool passing mechanism (hardcoded `all_tools`)

**What's Different**:
- Agent selection: Added Priority 3.5 force-selection (improved from 28% to 40%)
- Semantic classifier: Added after iteration_011 (bypassed by Priority 3.5)
- Context window: Might be different due to other prompt changes

**Gap Analysis**:
- Current: 40% (10/25 turns)
- iteration_011: 56% (14/25 turns)
- Gap: 16 percentage points (4 turns)

### 7. Next Steps

#### Priority 1: Verify Tool Availability in Actual API Calls
- **Action**: Add logging to `gemini_provider.py` to log when tools are passed to API
- **Goal**: Confirm tools are actually in every API call (not just code path)
- **Method**: Add `logging_util.info(f"🔧 TOOLS_PASSED: {len(gemini_tools)} tools")` before API call

#### Priority 2: Analyze Tool Invocation by Action Type
- **Action**: Deep dive into why `status` and `ranking` never call tools
- **Goal**: Understand LLM's decision-making for these action types
- **Method**: Compare narrative responses for `status` actions with vs without tools

#### Priority 3: Test Prompt Truncation Hypothesis
- **Action**: Check if prompt is being truncated in context window
- **Goal**: Verify tool instructions are actually reaching the LLM
- **Method**: Add logging to show actual prompt length sent to API

#### Priority 4: Consider Tool Calling Mode Change
- **Action**: Test `mode="ANY"` instead of `mode="AUTO"` (if Gemini supports it)
- **Goal**: Force LLM to consider tools more aggressively
- **Method**: Experimental change, run test, compare results

#### Priority 5: Add Reminder Tokens
- **Action**: Add explicit reminder tokens in prompt (e.g., `<<CALL-TOOLS-NOW>>`)
- **Goal**: Reinforce tool calling instructions
- **Method**: Add tokens at strategic points in prompt (start of turn, before status, etc.)

### 8. Test Results Summary

**iteration_019 (Current)**:
- Tool invocation: 40% (10/25 turns)
- Turns with tools: 6, 7, 8, 11, 13, 15, 20, 21, 22, 23
- Turns without tools: 0-5 (expected), 9, 10, 12, 14, 16, 17, 18, 19, 24

**iteration_018 (Temp 0.9)**:
- Tool invocation: 28% (7/25 turns)

**iteration_017 (Exact iteration_011 prompt)**:
- Tool invocation: 4% (1/25 turns)

**iteration_011 (Baseline)**:
- Tool invocation: 56% (14/25 turns)

### 9. Progress Timeline

1. **iteration_017**: 4% (regression after prompt changes)
2. **iteration_018**: 28% (restored temp=0.9, 7x improvement)
3. **iteration_019**: 40% (forced agent selection, 43% improvement from 28%)

**Total improvement**: 4% → 40% (10x improvement from lowest point)  
**Remaining gap**: 16 percentage points to reach 56%

### 10. Recommendations

1. **Immediate**: Add logging to verify tools are actually passed to API
2. **Short-term**: Analyze why `status` and `ranking` never call tools
3. **Medium-term**: Test prompt truncation hypothesis
4. **Long-term**: Consider tool calling mode changes or reminder tokens

**Key Insight**: The issue is NOT tool availability or prompt quality - it's LLM decision-making consistency. The LLM has all the information it needs, but chooses not to use tools ~60% of the time.
