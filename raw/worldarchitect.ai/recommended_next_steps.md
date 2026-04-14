# Recommended Next Steps - Faction Tool Invocation

**Date:** 2026-01-15  
**Current Status:** 28% tool invocation (improved from 4%, still below 56% target)  
**Analysis:** Temperature fixed, prompt matches iteration_011, issue is agent selection

## My Analysis

### What We Know
1. ✅ **Temperature fixed** - 0.9 restored (matches iteration_011)
2. ✅ **Prompt correct** - 1902 lines, identical to iteration_011
3. ✅ **Tool definitions correct** - Identical to iteration_011
4. ✅ **Model correct** - gemini-3-flash-preview (same)
5. ❌ **Agent selection changed** - Semantic classifier added after iteration_011

### The Gap: 28% vs 56%

**Root Cause Hypothesis:** Semantic classifier is interfering with agent selection.

**Evidence:**
- iteration_011: Direct agent selection (no classifier) → 56%
- Current: Classifier at Priority 5, fallback at Priority 7 → 28%
- No agent selection logs in test output (concerning)
- Test inputs may not match classifier phrases consistently

## Recommended Actions (Priority Order)

### 🔴 HIGH PRIORITY: Force FactionManagementAgent When Minigame Enabled

**Action:** Check `faction_minigame.enabled` BEFORE semantic classifier runs (Priority 1-2)

**Why:** 
- Ensures FactionManagementAgent is ALWAYS selected when minigame is enabled
- Bypasses semantic classifier interference
- Matches iteration_011 behavior (no classifier existed)

**Implementation:**
```python
# In get_agent_for_input(), add BEFORE semantic classifier:
# Priority 1.5: Force FactionManagementAgent if minigame enabled
if FactionManagementAgent.matches_game_state(game_state):
    logging_util.info("🏰 FACTION_MINIGAME_ENABLED: Forcing FactionManagementAgent (bypass classifier)")
    return FactionManagementAgent(game_state)
```

**Expected Impact:** Should restore 56% tool invocation (matches iteration_011)

### 🟡 MEDIUM PRIORITY: Verify Agent Selection Logging

**Action:** Check server logs for agent selection messages

**Why:**
- No logs found in test output (may be in server logs)
- Need to verify FactionManagementAgent is actually being selected
- Need to see if fallback is being reached

**Implementation:**
- Check `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/*/flask_backend.log`
- Look for `🏰 FACTION_MODE_ACTIVE`, `🏰 SEMANTIC_INTENT_FACTION`, `🏰 FACTION_MINIGAME`
- Verify agent selection pattern matches tool invocation pattern

**Expected Impact:** Confirms or refutes agent selection hypothesis

### 🟡 MEDIUM PRIORITY: Verify Tool Availability

**Action:** Check if tools are passed to API when FactionManagementAgent is selected

**Why:**
- Agent may be selected but tools not available
- Need to verify `agent.get_tools()` returns `FACTION_TOOLS`
- Need to verify tools are in Gemini API request

**Implementation:**
- Add logging in `gemini_provider.py` when tools are passed to API
- Check if `FACTION_TOOLS` are included when FactionManagementAgent selected
- Verify tool calling mode is configured correctly

**Expected Impact:** Confirms or refutes tool availability hypothesis

### 🟢 LOW PRIORITY: Add More Faction Phrases to Classifier

**Action:** Expand semantic classifier phrases for MODE_FACTION

**Why:**
- Current phrases may not catch all faction queries
- Test inputs like "How many troops..." may not match

**Implementation:**
- Add more phrases to `ANCHOR_PHRASES[MODE_FACTION]`
- Include variations: "troops", "forces", "army", "faction status", etc.
- Lower similarity threshold from 0.65 to 0.55-0.60

**Expected Impact:** May improve classifier matching, but fallback should catch these anyway

## My Recommendation: Do Priority 1 First

**Force FactionManagementAgent selection when minigame enabled** - This is the most likely fix and matches iteration_011 behavior.

**Rationale:**
1. **Matches iteration_011** - No classifier existed, agent was selected directly
2. **Simplest fix** - One code change, clear logic
3. **Highest impact** - Should restore 56% performance
4. **Low risk** - Only affects faction minigame, doesn't change other behavior

**If Priority 1 doesn't work:**
- Then investigate Priority 2 (agent selection logging)
- Then investigate Priority 3 (tool availability)
- Priority 4 is optional (classifier improvement)

## Alternative Approach: Bypass Classifier Entirely

**If Priority 1 doesn't work, consider:**
- Temporarily disable semantic classifier for faction queries
- Test if this restores 56% performance
- If yes, then fix classifier; if no, investigate other causes

## Expected Outcome

**After Priority 1 fix:**
- Tool invocation should return to 56%+ (matches iteration_011)
- FactionManagementAgent always selected when minigame enabled
- Tools always available when agent is selected
- Consistent behavior regardless of input phrasing

**If still below 56%:**
- Then investigate tool passing to API
- Check for other differences between iteration_011 and current
- Consider model behavior changes (same version, different weights)

## Summary

**Do this first:** Force FactionManagementAgent selection when `faction_minigame.enabled=True` (before semantic classifier runs)

**Why:** This matches iteration_011 behavior and should restore 56% tool invocation.

**If that doesn't work:** Then investigate agent selection logging and tool availability.
