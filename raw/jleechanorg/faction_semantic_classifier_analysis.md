# Semantic Classifier Analysis - Faction Tool Invocation Gap

**Date:** 2026-01-15  
**Issue:** Tool invocation at 28% vs iteration_011's 56% despite matching configuration  
**Hypothesis:** Semantic classifier may be routing faction queries to wrong agent

## Test Input Analysis

**Test inputs that SHOULD trigger faction tools:**

| Turn | Input | Should Match? | Actual Match? |
|------|-------|---------------|---------------|
| 2 | "How many troops do I have under my command?" | ✅ "how many troops do i have?" | ✅ Matches |
| 5 | "What's my current standing among the factions?" | ⚠️ Partial match | ⚠️ May not match |
| 6 | "I want to expand our food production. Can we build some farms?" | ✅ "build farms" | ✅ Matches |
| 7 | "We need more soldiers. How can I recruit more men?" | ✅ "recruit soldiers" | ✅ Matches |
| 8 | "Let's set up training facilities for our troops." | ❌ No direct match | ❌ May not match |
| 9 | "Where do we rank compared to other factions?" | ⚠️ Partial match | ⚠️ May not match |
| 10 | "I'd like to gather intelligence. Can we recruit some spies?" | ✅ "faction intel" | ✅ Matches |
| 11 | "Send some of our spies to gather information about the Iron Legion." | ✅ "faction intel" | ✅ Matches |
| 12 | "We should boost our economy. Build some artisan workshops." | ❌ No direct match | ❌ May not match |
| 13 | "Let's test our forces with a small skirmish against the Iron Legion." | ✅ "faction battle" | ✅ Matches |

## Semantic Classifier Phrases (MODE_FACTION)

```python
constants.MODE_FACTION: [
    "manage my faction",
    "faction management",
    "strategic faction system",
    "activate faction minigame",
    "show faction status",
    "check faction power",
    "what's my faction ranking?",
    "build farms",
    "recruit soldiers",
    "faction operations",
    "faction intel",
    "faction battle",
    "faction territory",
    "how many troops do i have?",
    "faction suggestions",
]
```

## Matching Analysis

**Test inputs that MATCH faction phrases:**
- ✅ Turn 2: "How many troops..." → matches "how many troops do i have?"
- ✅ Turn 6: "build some farms" → matches "build farms"
- ✅ Turn 7: "recruit more men" → matches "recruit soldiers"
- ✅ Turn 10: "gather intelligence" → matches "faction intel"
- ✅ Turn 11: "gather information" → matches "faction intel"
- ✅ Turn 13: "skirmish" → matches "faction battle"

**Test inputs that MAY NOT MATCH:**
- ⚠️ Turn 5: "What's my current standing among the factions?" → No exact match
- ❌ Turn 8: "Let's set up training facilities" → No match
- ⚠️ Turn 9: "Where do we rank compared to other factions?" → No exact match
- ❌ Turn 12: "Build some artisan workshops" → No match

## Tool Invocation Pattern (iteration_018)

**Tools called on turns:** 5, 7, 8, 10, 13, 21, 24

**Analysis:**
- Turn 5: "What's my current standing..." → Tools called ✅ (may have matched via fallback)
- Turn 7: "recruit more men" → Tools called ✅ (matches "recruit soldiers")
- Turn 8: "training facilities" → Tools called ✅ (may have matched via fallback)
- Turn 10: "gather intelligence" → Tools called ✅ (matches "faction intel")
- Turn 13: "skirmish" → Tools called ✅ (matches "faction battle")

**Tools NOT called on:**
- Turn 2: "How many troops..." → No tools ❌ (should match!)
- Turn 6: "build some farms" → No tools ❌ (should match!)
- Turn 9: "Where do we rank..." → No tools ❌
- Turn 11: "gather information" → No tools ❌ (should match!)
- Turn 12: "artisan workshops" → No tools ❌

## Key Finding: Inconsistent Matching

**Problem:** Even inputs that SHOULD match faction phrases aren't triggering tools consistently.

**Examples:**
- Turn 2: "How many troops..." matches "how many troops do i have?" but NO tools called
- Turn 6: "build some farms" matches "build farms" but NO tools called
- Turn 11: "gather information" matches "faction intel" but NO tools called

**But:**
- Turn 7: "recruit more men" matches "recruit soldiers" and tools ARE called ✅
- Turn 10: "gather intelligence" matches "faction intel" and tools ARE called ✅

## Hypothesis

**The semantic classifier may be:**
1. **Not matching consistently** - Similar inputs sometimes match, sometimes don't
2. **Similarity threshold too high** - 0.65 threshold may be filtering out valid matches
3. **Fallback not working** - Priority 7 fallback may not be catching mismatches
4. **Agent selected but tools not available** - Agent may be selected but tools not passed to API

## Next Investigation Steps

### 1. Check Similarity Scores
- What similarity scores are test inputs getting?
- Are they above/below 0.65 threshold?
- Why do some similar inputs match and others don't?

### 2. Verify Fallback Logic
- Is Priority 7 fallback (`FactionManagementAgent.matches_game_state()`) being reached?
- Is `faction_minigame.enabled` correctly detected?
- Are fallback logs present in server logs?

### 3. Check Agent Selection Logs
- Why are no agent selection logs in test output?
- Are logs going to server log file instead?
- Is logging disabled for test runs?

### 4. Verify Tool Availability
- When FactionManagementAgent is selected, are tools passed to API?
- Is `agent.get_tools()` returning `FACTION_TOOLS`?
- Are tools included in Gemini API request?

## Recommendations

### Short-term
1. **Add more faction phrases** to semantic classifier to catch more test inputs
2. **Lower similarity threshold** from 0.65 to 0.55-0.60 to catch more matches
3. **Verify fallback logic** is working correctly

### Long-term
1. **Bypass semantic classifier** for faction queries when `faction_minigame.enabled=True`
2. **Force FactionManagementAgent** when minigame is enabled (Priority 1 check)
3. **Improve phrase matching** with more diverse faction-related phrases

## Files to Review

- `mvp_site/intent_classifier.py` - Semantic classifier logic
- `mvp_site/agents.py` - Agent selection (Priority 7 fallback)
- Test inputs: `testing_mcp/faction/test_faction_20_turns_e2e.py` TURN_ACTIONS
- Server logs: Check for agent selection logging
