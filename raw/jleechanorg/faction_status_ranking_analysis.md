# Status and Ranking Actions Analysis

**Date**: 2025-01-XX  
**Issue**: `status` (0%) and `ranking` (0%) actions never call tools, even though prompt requires it

## Findings

### Status Actions Without Tools (2 instances)

**Turn 2**:
- **Input**: "How many troops do I have under my command?"
- **LLM Response**: Provided numbers directly (5,000 total: 4,000 soldiers, 500 elite guards, 500 militia)
- **Issue**: LLM read cached values from `game_state` instead of calling `faction_calculate_power`

**Turn 5**:
- **Input**: "What's my current standing among the factions?"
- **LLM Response**: Provided ranking directly (#58 out of 201)
- **Issue**: LLM read cached `ranking` value from `game_state.faction_minigame.ranking` instead of calling tools

### Ranking Actions Without Tools (1 instance)

**Turn 9**:
- **Input**: "Where do we rank compared to other factions?"
- **LLM Response**: Provided ranking information directly
- **Issue**: LLM read cached ranking instead of calling `faction_calculate_ranking`

## Root Cause Hypothesis

**The LLM is treating cached game state values as "source of truth" instead of calling tools to recalculate.**

### Why This Happens

1. **Game State Contains Cached Values**:
   - `game_state.faction_minigame.faction_power` - cached FP value
   - `game_state.faction_minigame.ranking` - cached ranking value
   - These values are visible to the LLM in the prompt

2. **LLM Decision-Making**:
   - LLM sees: "Player asks for ranking" → "I can see `ranking: 58` in game_state" → "I'll use that value"
   - LLM doesn't realize: "These cached values might be stale" or "I MUST call tools to get accurate values"

3. **Prompt Instructions vs. LLM Behavior**:
   - Prompt says: "ALWAYS call `faction_calculate_power` before showing FP values"
   - Prompt says: "When player asks about ranking" → call ranking tool
   - But LLM thinks: "I can just read the cached value - it's faster and the prompt doesn't explicitly say the cached value is wrong"

### The Problem

The prompt has **conflicting signals**:
1. **Explicit instruction**: "ALWAYS call tools before showing values"
2. **Implicit signal**: Game state contains cached values that look "ready to use"

The LLM is choosing the "easier" path (read cached values) over the "correct" path (call tools).

## Prompt Instructions (Current)

### For Status/Header Generation:
```
- **ALWAYS call this tool** before generating faction status or faction header
- **ALWAYS call this tool** when showing FP values to the player
```

### For Ranking Queries:
```
- **ALWAYS call `faction_calculate_ranking`** when:
  - When player asks about ranking
  - Before showing ranking information
```

### Critical Rule:
```
**CRITICAL RULE:** On EVERY turn where `faction_minigame.enabled = true`, you MUST call BOTH `faction_calculate_power` AND `faction_calculate_ranking` as a pair. This is not optional.
```

## Why LLM Ignores Instructions

1. **Cached Values Look "Correct"**: The LLM sees `ranking: 58` and thinks "this is accurate"
2. **No Explicit Warning**: Prompt doesn't say "NEVER use cached values - they are stale"
3. **Efficiency Bias**: LLM thinks "why call tools when I can just read the value?"
4. **Context Window**: Large prompt (1903 lines) might cause LLM to "forget" tool instructions

## Potential Solutions

### Solution 1: Add Explicit Warning About Cached Values
Add to prompt:
```
**🚨 CRITICAL: Cached Values Are Stale (MANDATORY)**
The values in `game_state.faction_minigame.faction_power` and `game_state.faction_minigame.ranking` are CACHED and may be STALE. 
NEVER use these cached values directly. ALWAYS call tools to get fresh, accurate values.
```

### Solution 2: Remove Cached Values from Game State (Not Recommended)
- Would require major refactoring
- Other parts of codebase might depend on cached values
- Would break existing functionality

### Solution 3: Add Reminder Tokens
Add explicit tokens in prompt:
```
<<CALL-TOOLS-NOW>>
Before showing ANY faction status or ranking, you MUST call:
1. faction_calculate_power
2. faction_calculate_ranking
NEVER use cached values from game_state.
```

### Solution 4: Make Tool Calling More Explicit in Examples
Add examples showing:
- ❌ WRONG: "Your ranking is #58" (using cached value)
- ✅ CORRECT: [calls tools] "Your ranking is #58" (using tool results)

### Solution 5: Force Tool Calls for Status/Ranking Actions
Add code-level enforcement:
- If action_type == "status" or "ranking" → require tool calls before response
- This would be a server-side validation, not prompt-based

## Recommended Approach

**Combine Solutions 1 + 3 + 4**:
1. Add explicit warning about cached values being stale
2. Add reminder tokens at strategic points
3. Add examples showing wrong vs. correct behavior

This addresses the root cause (LLM thinks cached values are valid) without requiring code changes.

## Test Plan

After implementing solutions:
1. Run 20-turn E2E test
2. Check if `status` and `ranking` actions now call tools
3. Verify tool invocation rate improves from 40% to target (56%+)
