# Faction Tool Invocation - Next Steps Summary

**Current Status**: 40% tool invocation (10/25 turns)  
**Target**: 56% (iteration_011 baseline)  
**Gap**: 16 percentage points (4 turns)

## Completed Actions

### ✅ Priority 1: Verify Tool Availability
- **Action**: Added logging to `gemini_provider.py`
- **Result**: Logs now show:
  - Tools passed to API (tool names and counts)
  - Tools invoked by LLM (which tools were called)
- **Status**: Committed and pushed

### ✅ Priority 2: Analyze Status/Ranking Actions
- **Action**: Analyzed why `status` (0%) and `ranking` (0%) never call tools
- **Finding**: LLM treats cached `game_state` values as source of truth instead of calling tools
- **Root Cause**: Prompt has conflicting signals - explicit instructions vs. cached values that look "ready to use"
- **Status**: Documented in `docs/faction_status_ranking_analysis.md`

## Next Steps (Priority Order)

### 🔴 Priority 1: Add Explicit Warning About Cached Values
**Action**: Update prompt to explicitly warn that cached values are stale
**Location**: `mvp_site/prompts/faction_minigame_instruction.md`
**Change**: Add section near top:
```
**🚨 CRITICAL: Cached Values Are Stale (MANDATORY)**
The values in `game_state.faction_minigame.faction_power` and `game_state.faction_minigame.ranking` are CACHED and may be STALE. 
NEVER use these cached values directly. ALWAYS call tools to get fresh, accurate values.
```

**Expected Impact**: Addresses root cause - LLM will know cached values are unreliable

### 🟡 Priority 2: Add Reminder Tokens
**Action**: Add explicit reminder tokens at strategic points in prompt
**Location**: `mvp_site/prompts/faction_minigame_instruction.md`
**Change**: Add tokens before status/ranking sections:
```
<<CALL-TOOLS-NOW>>
Before showing ANY faction status or ranking, you MUST call:
1. faction_calculate_power
2. faction_calculate_ranking
NEVER use cached values from game_state.
```

**Expected Impact**: Reinforces tool-calling instructions at decision points

### 🟡 Priority 3: Add Wrong vs. Correct Examples
**Action**: Add examples showing incorrect (using cached) vs. correct (using tools) behavior
**Location**: `mvp_site/prompts/faction_minigame_instruction.md`
**Change**: Add to tool usage section:
```
**Example - WRONG (using cached values):**
User: "What's my ranking?"
Response: "You rank #58" ❌ (used cached value without calling tools)

**Example - CORRECT (using tools):**
User: "What's my ranking?"
[tool_requests: faction_calculate_power, faction_calculate_ranking]
Response: "You rank #58" ✅ (called tools first, then used results)
```

**Expected Impact**: Shows LLM concrete examples of correct behavior

### 🟢 Priority 4: Test Prompt Truncation Hypothesis
**Action**: Add logging to verify prompt length sent to API
**Location**: `mvp_site/llm_service.py` or `mvp_site/llm_providers/gemini_provider.py`
**Change**: Log actual prompt/system instruction length before API call
**Expected Impact**: Confirms if 1903-line prompt is being truncated

### 🟢 Priority 5: Consider Tool Calling Mode Change
**Action**: Test if changing `mode="AUTO"` to `mode="ANY"` (if Gemini supports it) improves consistency
**Location**: `mvp_site/llm_providers/gemini_provider.py:473`
**Change**: Experimental - test different tool calling modes
**Expected Impact**: Might force LLM to consider tools more aggressively

## Implementation Plan

### Phase 1: Prompt Updates (Priorities 1-3)
1. Add explicit warning about cached values
2. Add reminder tokens
3. Add wrong vs. correct examples
4. Run 20-turn E2E test
5. Compare results: expect improvement in `status`/`ranking` tool invocation

### Phase 2: Verification (Priority 4)
1. Add prompt length logging
2. Run test and check logs
3. Verify prompt is not truncated
4. If truncated, investigate context window limits

### Phase 3: Experimental (Priority 5)
1. Test different tool calling modes (if supported)
2. Compare results
3. Revert if no improvement

## Success Criteria

- **Short-term**: `status` and `ranking` actions call tools (0% → 50%+)
- **Medium-term**: Overall tool invocation improves from 40% → 50%+
- **Long-term**: Reach iteration_011 baseline of 56%+

## Risk Assessment

- **Low Risk**: Prompt updates (Priorities 1-3) - can revert easily
- **Medium Risk**: Tool calling mode change (Priority 5) - might break other functionality
- **Low Risk**: Logging additions (Priority 4) - no functional changes

## Timeline

- **Immediate**: Implement Priorities 1-3 (prompt updates)
- **This Week**: Run tests, analyze results
- **Next Week**: Implement Priorities 4-5 if needed
