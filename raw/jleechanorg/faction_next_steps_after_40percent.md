# Next Steps After 40% Tool Invocation Achievement

**Date:** 2026-01-15  
**Current Status:** 40% tool invocation (improved from 4% → 28% → 40%)  
**Target:** 56% (iteration_011 baseline) → 100% (ultimate goal)

## Progress Summary

| Iteration | Change | Tool Invocation | Notes |
|-----------|--------|----------------|-------|
| iteration_011 | Baseline | 56% (14/25) ✅ | Best performance |
| iteration_017 | Wrong temp (0.1) | 4% (1/25) 🔴 | Worst |
| iteration_018 | Temp 0.9 | 28% (7/25) | Temperature fix |
| iteration_019 | Force agent | 40% (10/25) ✅ | Agent selection fix |

**Total Improvement:** 4% → 40% (10x improvement)  
**Remaining Gap:** 40% vs 56% (16 percentage points)

## What We've Fixed

1. ✅ **Temperature:** Restored to 0.9 (matches iteration_011)
2. ✅ **Agent Selection:** Force FactionManagementAgent when minigame enabled (Priority 3.5)
3. ✅ **Prompt:** Already matches iteration_011 (1902 lines)

## Remaining Gap Analysis

**Why 40% vs 56%?**

**Possible causes:**
1. **Tool availability** - Tools may not be passed to API consistently
2. **LLM behavior** - Model may still choose not to call tools even when available
3. **Prompt context** - Something in the full system instruction may be interfering
4. **Model version differences** - Same version string but behavior may have changed

## Next Investigation Steps

### 🔴 HIGH PRIORITY: Verify Tool Availability

**Question:** Are tools actually being passed to Gemini API when FactionManagementAgent is selected?

**Investigation:**
1. Check `agent.get_tools()` returns `FACTION_TOOLS` when `minigame_enabled=True`
2. Verify tools are included in Gemini API request
3. Check `gemini_provider.py` tool passing logic
4. Add logging to confirm tools are in API request

**Expected:** Tools should be available 100% of the time when agent is selected

### 🟡 MEDIUM PRIORITY: Check Agent Selection Logs

**Question:** Is FactionManagementAgent being selected consistently?

**Investigation:**
1. Check server logs for `FACTION_MINIGAME_FORCE` messages
2. Verify agent selection happens on all 25 turns
3. Check if any turns use wrong agent (StoryModeAgent instead)

**Expected:** FactionManagementAgent should be selected on all turns after minigame enabled

### 🟡 MEDIUM PRIORITY: Analyze Tool Invocation Pattern

**Question:** Why are tools called on some turns but not others?

**From iteration_019:**
- Tools called: Turns 6, 7, 8, 11, 13, 15, 20, 21, 22, 23 (10 turns)
- Tools NOT called: Turns 2, 4, 5, 9, 10, 12, 14, 16, 17, 18, 19, 24 (15 turns)

**Investigation:**
1. Compare turns WITH tools vs turns WITHOUT tools
2. Check if there's a pattern (action type, input phrasing, etc.)
3. Check if LLM responses differ between tool-calling and non-tool-calling turns
4. Verify if tools are available but LLM chooses not to call them

### 🟢 LOW PRIORITY: Check System Instruction Conflicts

**Question:** Are other system instructions interfering with tool calling?

**Investigation:**
1. Review all system instructions for conflicting "MANDATORY" language
2. Check instruction ordering/precedence
3. Verify faction_minigame_instruction is included when agent is selected

## Recommended Actions

### Action 1: Add Tool Availability Logging

**Add to `mvp_site/llm_providers/gemini_provider.py`:**
```python
# Log when tools are passed to API
if gemini_tools:
    logging_util.info(f"🔧 TOOLS_PASSED_TO_API: {len(gemini_tools)} tools")
    tool_names = [t.get('function', {}).get('name') for t in gemini_tools]
    logging_util.info(f"   Tool names: {tool_names}")
```

**Add to `mvp_site/agents.py`:**
```python
# In FactionManagementAgent.get_tools()
if self._minigame_enabled:
    tools = FACTION_TOOLS
    logging_util.info(f"🏰 FACTION_TOOLS_RETURNED: {len(tools)} tools available")
    return tools
```

### Action 2: Check Server Logs

**Look for:**
- `FACTION_MINIGAME_FORCE` messages (should appear 25 times)
- `FACTION_TOOLS_RETURNED` messages (should appear 25 times)
- `TOOLS_PASSED_TO_API` messages (should appear 25 times)

**If missing:** Agent selection or tool passing is failing

### Action 3: Compare Tool-Calling vs Non-Tool-Calling Turns

**Analyze:**
- What's different about turns 6, 7, 8, 11, 13, 15, 20, 21, 22, 23?
- What's different about turns 2, 4, 5, 9, 10, 12, 14, 16, 17, 18, 19, 24?
- Are there patterns in action types, input phrasing, or LLM responses?

## Expected Outcomes

### Best Case
- Tools are available 100% of the time
- LLM is choosing not to call tools on some turns
- Need to strengthen prompt instructions or tool descriptions

### Worst Case
- Tools are NOT available on some turns
- Agent selection is failing intermittently
- Need to fix tool passing or agent selection logic

### Most Likely
- Tools are available but LLM behavior varies
- Some turns trigger tool calling, others don't
- Need to investigate why LLM chooses not to call tools

## Success Criteria

- **Short-term:** Verify tools are available 100% of the time
- **Medium-term:** Reach 56% tool invocation (iteration_011 baseline)
- **Long-term:** Achieve 100% tool invocation (ultimate goal)

## Files to Review

- **Test results:** `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/iteration_019/`
- **Code:** `mvp_site/agents.py` (agent selection), `mvp_site/llm_providers/gemini_provider.py` (tool passing)
- **Logs:** Check server logs for agent selection and tool passing confirmation
