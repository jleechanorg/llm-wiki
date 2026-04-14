# Faction Tool Failure Examples - Iteration 021

**Date:** 2026-01-16  
**Test Run:** Iteration 021 (Full 25-Turn Completion)  
**Campaign ID:** `yWzKs8COpEeXrV20b8rX`

## Overview

This document catalogs specific examples of when faction tools (`faction_calculate_power`, `faction_calculate_ranking`) either:
1. **Were not invoked** when they should have been
2. **Were invoked but failed validation** (hallucination errors)
3. **Failed completely** (timeout)

## Category 1: Tools Not Invoked (Missed Opportunities)

### Turn 5: Ranking Query - ❌ NO TOOLS
**Action:** "What's my current standing among the factions?"  
**Expected:** Should invoke `faction_calculate_ranking`  
**Actual:** Tools: none  
**Why it failed:** LLM answered ranking question without calling the tool, likely using cached/stale data

```
Turn 5: Natural curiosity about ranking
Action: What's my current standing among the factions?
✅ Turn 5 completed in 19.9s
   Tools: none  ← SHOULD HAVE CALLED faction_calculate_ranking
   Faction header: Yes
```

### Turn 12: Building Action - ❌ NO TOOLS
**Action:** "We should boost our economy. Build some artisan workshops."  
**Expected:** Should invoke `faction_calculate_power` after building  
**Actual:** Tools: none  
**Why it failed:** LLM processed building request but didn't recalculate power to show impact

```
Turn 12: Natural economic development
Action: We should boost our economy. Build some artisan workshops.
✅ Turn 12 completed in 13.5s
   Tools: none  ← SHOULD HAVE CALLED faction_calculate_power
   Faction header: Yes
```

### Turn 13: Combat Action - ❌ NO TOOLS
**Action:** "Let's test our forces with a small skirmish against the Iron Legion."  
**Expected:** Could invoke `faction_calculate_power` to assess combat readiness  
**Actual:** Tools: none  
**Why it failed:** Combat was handled narratively without power calculation

```
Turn 13: Natural combat exploration
Action: Let's test our forces with a small skirmish against the Iron Legion.
✅ Turn 13 completed in 25.4s
   Tools: none  ← COULD HAVE CALLED faction_calculate_power
   Faction header: Yes
```

### Turn 14: Diplomatic Action - ❌ NO TOOLS
**Action:** "I want to form an alliance with the Shadow Covenant. Can we reach out to them?"  
**Expected:** Could invoke `faction_calculate_ranking` to check relative standing  
**Actual:** Tools: none  
**Why it failed:** Diplomacy handled without checking ranking/standing

```
Turn 14: Natural diplomatic approach
Action: I want to form an alliance with the Shadow Covenant. Can we reach out to them?
✅ Turn 14 completed in 16.1s
   Tools: none  ← COULD HAVE CALLED faction_calculate_ranking
   Faction header: Yes
```

### Turn 16: Building Action - ❌ NO TOOLS
**Action:** "Set up a library for research and learning."  
**Expected:** Should invoke `faction_calculate_power` after building  
**Actual:** Tools: none  
**Why it failed:** Building processed without power recalculation

```
Turn 16: Natural research building
Action: Set up a library for research and learning.
✅ Turn 16 completed in 19.8s
   Tools: none  ← SHOULD HAVE CALLED faction_calculate_power
   Faction header: Yes
```

### Turn 18: Combat/Pillage Action - ❌ NO TOOLS
**Action:** "The Golden Dawn has been raiding our trade routes. Let's strike back and take their resources."  
**Expected:** Should invoke `faction_calculate_power` and `faction_calculate_ranking` after combat  
**Actual:** Tools: none  
**Why it failed:** Retaliatory action handled narratively without tool calls

```
Turn 18: Natural retaliatory action
Action: The Golden Dawn has been raiding our trade routes. Let's strike back and take their resources.
✅ Turn 18 completed in 37.8s
   Tools: none  ← SHOULD HAVE CALLED faction_calculate_power, faction_calculate_ranking
   Faction header: Yes
```

### Turn 20: Building Action - ❌ NO TOOLS
**Action:** "Set up magical wards to protect against enemy spells."  
**Expected:** Should invoke `faction_calculate_power` after building  
**Actual:** Tools: none  
**Why it failed:** Building processed without power recalculation

```
Turn 20: Natural magical defense
Action: Set up magical wards to protect against enemy spells.
✅ Turn 20 completed in 21.7s
   Tools: none  ← SHOULD HAVE CALLED faction_calculate_power
   Faction header: Yes
```

### Turn 23: Power Assessment Query - ❌ NO TOOLS (CRITICAL MISS)
**Action:** "How powerful are we now? What's our total faction strength?"  
**Expected:** **MUST** invoke `faction_calculate_power` - this is a direct power query  
**Actual:** Tools: none  
**Why it failed:** LLM answered power question without calling tool - likely hallucinated value

```
Turn 23: Natural power assessment
Action: How powerful are we now? What's our total faction strength?
✅ Turn 23 completed in 22.6s
   Tools: none  ← CRITICAL: SHOULD HAVE CALLED faction_calculate_power
   Faction header: Yes
```

**Analysis:** Turn 23 is the most egregious failure - the player explicitly asked for faction power, and the LLM answered without invoking the tool. This suggests the LLM is using cached/stale data or hallucinating values.

## Category 2: Tools Invoked But Failed Validation (Hallucination)

### Turn 4: Tutorial Exploration - ⚠️ TOOLS INVOKED BUT VALIDATION FAILED
**Action:** "Show me what I can do with this faction system."  
**Tools Invoked:** `faction_calculate_power`, `faction_calculate_ranking`  
**Validation Error:** FP hallucination detected

```
Turn 4: Natural exploration - should trigger tutorial
Action: Show me what I can do with this faction system.
❌ Turn 4 completed in 30.8s
   Tools: faction_calculate_power, faction_calculate_ranking  ← Tools called
   Faction header: Yes
   ⚠️ FP VALIDATION FAILED: FP hallucination detected: expected ~54000, got 29000 (off by 25000, allowed variance: 5400)
```

**Analysis:** Tools were invoked correctly, but the LLM reported a faction power of 29,000 when it should have been ~54,000. This suggests:
- Tool was called but LLM ignored the result
- LLM used cached/stale data instead of tool output
- Tool result wasn't properly integrated into response

### Turn 8: Building Request - ⚠️ TOOLS INVOKED BUT VALIDATION FAILED
**Action:** "Let's set up training facilities for our troops."  
**Tools Invoked:** `faction_calculate_power`, `faction_calculate_ranking`  
**Validation Error:** FP hallucination detected

```
Turn 8: Natural building request
Action: Let's set up training facilities for our troops.
❌ Turn 8 completed in 33.4s
   Tools: faction_calculate_power, faction_calculate_ranking  ← Tools called
   Faction header: Yes
   ⚠️ FP VALIDATION FAILED: FP hallucination detected: expected ~54000, got 29000 (off by 25000, allowed variance: 5400)
```

**Analysis:** Same pattern as Turn 4 - tools invoked but LLM reported wrong value (29,000 vs 54,000).

### Turn 11: Intel Operation - ⚠️ TOOLS INVOKED BUT VALIDATION FAILED
**Action:** "Send some of our spies to gather information about the Iron Legion."  
**Tools Invoked:** `faction_calculate_power`, `faction_calculate_ranking`  
**Validation Error:** FP hallucination detected

```
Turn 11: Natural intel operation
Action: Send some of our spies to gather information about the Iron Legion.
❌ Turn 11 completed in 26.1s
   Tools: faction_calculate_power, faction_calculate_ranking  ← Tools called
   Faction header: Yes
   ⚠️ FP VALIDATION FAILED: FP hallucination detected: expected ~54000, got 29000 (off by 25000, allowed variance: 5400)
```

**Analysis:** Consistent pattern - tools invoked but LLM consistently reports 29,000 instead of ~54,000. This suggests a systematic issue where:
- Tool results are being ignored
- LLM is using initial/seed value (29,000) instead of updated values
- Tool output integration is broken

## Category 3: Complete Failure (Timeout)

### Turn 22: Major Military Action - ❌ TIMEOUT
**Action:** "The Frost Wolves have been threatening our borders. Launch a full assault to break their power."  
**Expected:** Should invoke `faction_calculate_power` and `faction_calculate_ranking`  
**Actual:** Request timed out after 60 seconds  
**Why it failed:** Complex combat operation exceeded timeout limit

```
Turn 22: Natural major military action
Action: The Frost Wolves have been threatening our borders. Launch a full assault to break their power.
❌ Turn 22 failed in 60.0s: timed out  ← NO TOOLS INVOKED (timeout)
```

**Analysis:** The request timed out before tools could be invoked. This suggests:
- Complex combat operations need longer timeout
- LLM may be generating very long responses for major military actions
- System needs optimization for complex scenarios

## Summary Statistics

### Tools Not Invoked (8 turns)
- Turn 5: Ranking query
- Turn 12: Building action
- Turn 13: Combat action
- Turn 14: Diplomatic action
- Turn 16: Building action
- Turn 18: Combat/pillage action
- Turn 20: Building action
- Turn 23: **Power assessment query (CRITICAL)**

### Tools Invoked But Failed Validation (3 turns)
- Turn 4: FP hallucination (29k vs 54k)
- Turn 8: FP hallucination (29k vs 54k)
- Turn 11: FP hallucination (29k vs 54k)

### Complete Failure (1 turn)
- Turn 22: Timeout (60s limit)

## Root Cause Analysis

### Issue 1: LLM Ignoring Tool Results
**Pattern:** Tools are invoked but LLM reports wrong values (29,000 vs 54,000)  
**Likely Cause:** 
- Tool output not properly integrated into LLM context
- LLM using cached/stale game state instead of tool results
- Prompt not emphasizing "MUST use tool results"

**Fix Needed:** Strengthen prompt instructions to force LLM to use tool output, not cached values

### Issue 2: LLM Not Invoking Tools on Direct Queries
**Pattern:** Player explicitly asks for power/ranking, LLM answers without tools  
**Likely Cause:**
- LLM thinks it "knows" the answer from context
- Prompt doesn't emphasize "ALWAYS call tools for power/ranking queries"
- Tool invocation instructions not strong enough

**Fix Needed:** Add explicit rule: "If player asks about power/ranking, you MUST call tools - never answer from memory"

### Issue 3: Inconsistent Tool Usage on Building Actions
**Pattern:** Some building actions invoke tools (Turn 6, 8, 15), others don't (Turn 12, 16, 20)  
**Likely Cause:**
- Inconsistent prompt interpretation
- LLM deciding "this building doesn't need power recalculation"
- No explicit requirement to always recalculate after building

**Fix Needed:** Add explicit rule: "After ANY building action, you MUST call faction_calculate_power"

### Issue 4: Timeout on Complex Operations
**Pattern:** Turn 22 (major military action) timed out  
**Likely Cause:**
- Complex combat operations generate very long responses
- 60-second timeout too short for complex scenarios
- No timeout handling for tool calls

**Fix Needed:** Increase timeout for complex operations or optimize prompt for faster responses

## Recommendations

1. **Strengthen Tool Invocation Rules**
   - Add explicit requirement: "If player asks about power/ranking, you MUST call tools"
   - Add explicit requirement: "After ANY building/recruitment/combat action, you MUST call faction_calculate_power"
   - Use stronger language: "MANDATORY", "REQUIRED", "MUST"

2. **Fix Tool Result Integration**
   - Ensure tool output is prominently placed in LLM context
   - Add validation that LLM actually used tool results
   - Add prompt instruction: "You MUST use the tool result value, not your memory"

3. **Increase Timeout for Complex Operations**
   - Consider 90-120 second timeout for combat operations
   - Or optimize prompts to generate shorter responses

4. **Add Tool Invocation Validation**
   - Pre-validate that power/ranking queries trigger tool calls
   - Post-validate that tool results match reported values
   - Log warnings when tools should be called but aren't

## Conclusion

The faction tool system is **partially working** (57% invocation rate) but has **systematic issues**:

1. **LLM ignoring tool results** - Tools called but wrong values reported (3 cases)
2. **LLM not invoking tools** - Direct queries answered without tools (8 cases, including critical Turn 23)
3. **Timeout failures** - Complex operations exceed timeout (1 case)

These issues suggest the prompt needs strengthening to:
- Force tool invocation on specific query types
- Force tool result usage instead of cached values
- Handle complex operations more efficiently
