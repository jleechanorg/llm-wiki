# Faction Tool Invocation - Next Steps Investigation

**Date:** 2026-01-15  
**Status:** Temperature 0.9 restored (28% tool invocation, improved from 4%)  
**Goal:** Reach 56%+ tool invocation (iteration_011 baseline)

## Current Status

**Temperature Fix Applied:**
- ✅ Changed from 0.1 to 0.9 (matches iteration_011)
- ✅ Tool invocation improved: 4% → 28% (7x improvement)
- ⚠️ Still below iteration_011's 56% (28% vs 56%)

**Configuration:**
- Temperature: 0.9 (matches iteration_011)
- Prompt: 1902 lines (matches iteration_011)
- Model: gemini-3-flash-preview (matches iteration_011)
- Tool definitions: Identical (confirmed)

## Remaining Gap: 28% vs 56%

**Why is iteration_018 (28%) still below iteration_011 (56%)?**

Both have:
- ✅ Same temperature (0.9)
- ✅ Same prompt structure (1902 lines)
- ✅ Same model (gemini-3-flash-preview)
- ✅ Same tool definitions

**Difference:** Semantic Intent Classifier was added AFTER iteration_011

## Key Finding: Semantic Classifier Impact

**GenesisFaction Analysis (Message 504):**
- iteration_011: Direct agent selection via `FactionManagementAgent.matches_game_state()` at Priority 7
- Current: Semantic classifier is "PRIMARY BRAIN" at Priority 5, FactionManagementAgent demoted to "fallback"

**The Classifier Routes Based on Input Phrases:**
```python
constants.MODE_FACTION: [
    "manage my faction",
    "faction management",
    "show faction status",
    ...
]
```

**Problem:** If user input doesn't match faction phrases, classifier returns `MODE_CHARACTER` (story mode).

**Example Test Inputs:**
- "How many troops do I have under my command?" → May not match faction phrases
- "What's my current standing among the factions?" → May not match faction phrases
- "I want to expand our food production. Can we build some farms?" → May not match faction phrases

**Fallback Should Work:** Priority 7 fallback checks `faction_minigame.enabled` and should still route to FactionManagementAgent.

## Investigation Questions

### 1. Is FactionManagementAgent Being Selected?

**Check logs for:**
- `🏰 FACTION_MODE_ACTIVE: Using FactionManagementAgent (state-based fallback)`
- `🏰 SEMANTIC_INTENT_FACTION: ... -> FactionManagementAgent`
- `🏰 FACTION_MINIGAME: Agent selected, minigame enabled`

**If missing:** Agent selection is failing, tools won't be available.

### 2. Is Semantic Classifier Interfering?

**Check if:**
- Classifier returns `MODE_CHARACTER` for faction queries
- Fallback at Priority 7 is being reached
- `faction_minigame.enabled` is correctly detected

**Test:** Bypass semantic classifier temporarily to see if performance improves.

### 3. Are Tools Available When Agent Is Selected?

**Check if:**
- `FactionManagementAgent.get_tools()` returns `FACTION_TOOLS` when `minigame_enabled=True`
- Tools are passed to Gemini API correctly
- Tool definitions are included in API request

### 4. Is Agent Selection Happening Too Late?

**Check if:**
- Agent selection happens before prompt building
- System instructions include faction_minigame_instruction when agent is FactionManagementAgent
- Tool definitions are available when LLM processes the request

## Recommended Next Steps (No Coding)

### Step 1: Analyze Test Logs

**Check iteration_018 logs for:**
```bash
grep -E "FACTION_MODE|FactionManagementAgent|SEMANTIC_INTENT" /tmp/faction_test_iteration_018_temp_0.9.log
```

**Look for:**
- How many times FactionManagementAgent was selected
- How many times semantic classifier returned MODE_FACTION vs MODE_CHARACTER
- Whether fallback at Priority 7 was reached

### Step 2: Compare Agent Selection Patterns

**Compare iteration_011 vs iteration_018:**
- Check if agent selection patterns differ
- Verify `faction_minigame.enabled` detection is working
- Check if semantic classifier is preventing FactionManagementAgent selection

### Step 3: Analyze Tool Invocation Patterns

**From iteration_018 results:**
- Tools called on turns: 5, 7, 8, 10, 13, 21, 24
- Pattern: Mostly power/ranking tools, only 1 battle tool
- Missing: Tools on turns 4, 6, 9, 11, 12, 14-20, 22-23

**Questions:**
- Why are tools called on some turns but not others?
- Is there a pattern (e.g., tools called after certain actions)?
- Are tools missing when semantic classifier routes to MODE_CHARACTER?

### Step 4: Check Semantic Classifier Phrases

**Review `intent_classifier.py` ANCHOR_PHRASES for MODE_FACTION:**
- Are test inputs matching these phrases?
- Should we add more phrases to catch faction queries?
- Is similarity threshold (0.65) too high?

### Step 5: Verify Fallback Logic

**Check Priority 7 fallback:**
- Is `FactionManagementAgent.matches_game_state()` being called?
- Is `faction_minigame.enabled` correctly detected?
- Is fallback working even when classifier returns MODE_CHARACTER?

## Hypothesis

**The 28% vs 56% gap is likely caused by:**

1. **Semantic Classifier Interference:**
   - Classifier routes some faction queries to MODE_CHARACTER (story mode)
   - Fallback should catch these, but may not be working correctly
   - Tools may not be available when wrong agent is selected

2. **Agent Selection Timing:**
   - Agent may be selected after prompt building
   - Tools may not be included in API request
   - System instructions may not include faction_minigame_instruction

3. **Tool Availability:**
   - Tools may not be passed to Gemini API when FactionManagementAgent is selected
   - Tool definitions may be filtered out
   - Tool calling mode may not be configured correctly

## Next Actions (Investigation Only)

1. ✅ **Analyze logs** - Check agent selection patterns
2. ✅ **Compare test inputs** - See which inputs trigger tool calls vs which don't
3. ✅ **Review semantic classifier** - Check phrase matching and thresholds
4. ✅ **Verify fallback logic** - Ensure Priority 7 fallback is working
5. ✅ **Check tool availability** - Verify tools are passed to API when agent is selected

## Expected Outcomes

**If semantic classifier is the issue:**
- Bypass classifier → Should restore 56% performance
- Add more faction phrases → Should improve matching
- Lower similarity threshold → Should catch more faction queries

**If agent selection is the issue:**
- Fix fallback logic → Should ensure FactionManagementAgent is selected
- Fix timing → Should ensure tools are available

**If tool availability is the issue:**
- Fix tool passing → Should ensure tools are in API request
- Fix tool calling mode → Should ensure tools can be called

## Files to Review

- `/tmp/faction_test_iteration_018_temp_0.9.log` - Test logs
- `mvp_site/intent_classifier.py` - Semantic classifier logic
- `mvp_site/agents.py` - Agent selection logic (Priority 7 fallback)
- `mvp_site/llm_providers/gemini_provider.py` - Tool passing to API
- Test inputs: `testing_mcp/faction/test_faction_20_turns_e2e.py` TURN_ACTIONS
