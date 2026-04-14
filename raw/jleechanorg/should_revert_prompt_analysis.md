# Should We Revert to Old Prompt Version? Analysis

**Date:** 2026-01-15  
**Question:** Should we revert to an older prompt version to restore 56% tool invocation?

## Current Situation

**Current Prompt:** 1902 lines (exact iteration_011 structure)  
**Current Performance:** 28% tool invocation (iteration_018)  
**Target Performance:** 56% tool invocation (iteration_011)

## Key Finding: Prompt Already Matches iteration_011

**Verification:**
- Current prompt: 1902 lines
- iteration_011 prompt: 1902 lines
- **Diff check:** Prompt is IDENTICAL to iteration_011

**Conclusion:** We already HAVE the iteration_011 prompt. Reverting won't help.

## Performance Comparison

| Iteration | Prompt Lines | Temperature | Tool Invocation | Notes |
|-----------|--------------|-------------|----------------|-------|
| iteration_011 | 1902 | 0.9 (default) | **56%** ✅ BEST | Baseline |
| iteration_014 | 2013 | 0.2 | 20% | Had explicit "Tool Usage" section |
| iteration_015 | 413 | 0.0 | 12% | Too condensed |
| iteration_016 | 2013 | 0.1 | 12% | Restored baseline |
| iteration_017 | 1902 | 0.1 | 4% 🔴 WORST | Exact iteration_011 prompt, wrong temp |
| iteration_018 | 1902 | 0.9 | 28% ⚠️ | Exact iteration_011 prompt + temp |

## Analysis: Why Same Prompt Performs Differently

**Same Configuration:**
- ✅ Prompt: 1902 lines (identical)
- ✅ Temperature: 0.9 (matches iteration_011)
- ✅ Model: gemini-3-flash-preview (same)
- ✅ Tool definitions: Identical

**Different Configuration:**
- ❌ Semantic Intent Classifier: Added AFTER iteration_011
- ❌ Agent selection logic: Changed (classifier at Priority 5, fallback at Priority 7)

## Root Cause: Not the Prompt

**The issue is NOT the prompt.** Even with the exact iteration_011 prompt:
- iteration_017 (temp 0.1): 4% - Wrong temperature
- iteration_018 (temp 0.9): 28% - Correct temperature, but still below 56%

**The gap (28% vs 56%) is caused by:**
1. **Semantic classifier interference** - May route faction queries to wrong agent
2. **Agent selection timing** - Fallback may not be reached consistently
3. **Tool availability** - Tools may not be passed to API when agent is selected

## Should We Revert?

### ❌ NO - Reverting Won't Help

**Reasons:**
1. **Prompt already matches iteration_011** - We have the exact same prompt
2. **Other prompt versions performed WORSE** - 2013-line version got 20%, 413-line got 12%
3. **The issue is agent selection, not prompt** - Semantic classifier is the difference

### ✅ YES - But Not the Prompt

**What we SHOULD revert/investigate:**
1. **Agent selection logic** - Bypass semantic classifier when `faction_minigame.enabled=True`
2. **Force FactionManagementAgent** - Check `faction_minigame.enabled` at Priority 1 (before classifier)
3. **Verify fallback** - Ensure Priority 7 fallback is working correctly

## Alternative: Try Different Prompt Versions

**If we want to experiment:**

### Option 1: Try 2013-line version (had explicit "Tool Usage" section)
- **Performance:** 20% (worse than current 28%)
- **Risk:** Low (can revert)
- **Benefit:** Unlikely to help (performed worse)

### Option 2: Try iteration_011 exact commit
- **Performance:** 56% (best)
- **Risk:** None (already have it)
- **Benefit:** Already using it, won't change anything

### Option 3: Hybrid approach
- Keep 1902-line prompt structure
- Add explicit "Tool Usage" section at top (like 2013-line version)
- **Risk:** Medium (may confuse LLM)
- **Benefit:** Unclear

## Recommendation

**DO NOT revert the prompt.** Instead:

1. **Keep current prompt** (1902 lines, matches iteration_011)
2. **Fix agent selection** - Ensure FactionManagementAgent is selected when `faction_minigame.enabled=True`
3. **Bypass semantic classifier** - Check minigame status BEFORE classifier runs
4. **Verify tool availability** - Ensure tools are passed to API when agent is selected

**The prompt is correct. The problem is agent selection and tool availability.**

## Next Steps

1. **Verify agent selection** - Check if FactionManagementAgent is being selected
2. **Check fallback logic** - Ensure Priority 7 fallback works
3. **Bypass classifier** - Force FactionManagementAgent when minigame enabled
4. **Verify tool passing** - Ensure tools are in API request

**Bottom line:** The prompt is fine. Fix agent selection, not the prompt.
