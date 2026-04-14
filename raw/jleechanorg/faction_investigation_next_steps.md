# Faction Tool Invocation Investigation - Next Steps

**Date:** 2026-01-15  
**Status:** Awaiting GenesisFaction response + parallel investigation  
**Goal:** Identify root cause of 4% tool invocation regression

## Immediate Actions

### 1. Compare Tool Definitions (HIGH PRIORITY)

**Hypothesis:** Tool schemas may have changed since `iteration_011`, making them less likely to be invoked.

**Actions:**
```bash
# Find iteration_011 commit
git log --oneline --all --grep="iteration_011" | head -1

# Compare tool definitions
git show <iteration_011_commit>:mvp_site/faction/tools.py > /tmp/tools_iteration_011.py
diff -u /tmp/tools_iteration_011.py mvp_site/faction/tools.py

# Check tool registration/availability
git log --oneline --all -S "FACTION_TOOLS" --since="2025-12-01"
```

**What to look for:**
- Changes to tool `description` fields
- Changes to tool `parameters` schemas
- Changes to tool name strings
- Changes to tool registration logic

### 2. Compare LLM Service Tool Calling Logic (HIGH PRIORITY)

**Hypothesis:** Tool calling mechanism in `llm_service.py` may have changed, affecting how tools are presented to the LLM.

**Actions:**
```bash
# Compare llm_service.py around tool calling
git show <iteration_011_commit>:mvp_site/llm_service.py > /tmp/llm_service_iteration_011.py

# Focus on:
# - Tool filtering logic
# - Tool availability checks
# - Tool presentation to LLM
# - Response parsing for tool calls
```

**Key sections to check:**
- Tool filtering/availability logic
- How tools are passed to Gemini API
- Tool result parsing
- Temperature/parameter overrides

### 3. Verify Model Version Used in iteration_011 (MEDIUM PRIORITY)

**Hypothesis:** `iteration_011` may have used a different Gemini model version with different tool calling behavior.

**Actions:**
```bash
# Check test file history for model pinning
git log -p --all -S "gemini-3-flash-preview" -- testing_mcp/faction/test_faction_20_turns_e2e.py

# Check for model version changes
git log -p --all -S "DEFAULT_MODEL" -- testing_mcp/faction/test_faction_20_turns_e2e.py

# Check LLM provider changes
git log --oneline --all --since="2025-12-01" -- mvp_site/llm_providers/gemini_provider.py
```

**What to look for:**
- Model version pinning in test
- Model version changes in provider
- Model-specific tool calling behavior differences

### 4. Check System Instruction Assembly (MEDIUM PRIORITY)

**Hypothesis:** Other system instructions may be interfering with faction tool calling instructions.

**Actions:**
```bash
# Check how system instructions are assembled
grep -r "faction_minigame_instruction" mvp_site/ --include="*.py"

# Check for instruction conflicts
grep -r "MANDATORY\|ALWAYS\|MUST" mvp_site/prompts/ --include="*.md" | grep -v faction_minigame

# Check instruction ordering/precedence
grep -r "system_instruction\|prompt.*instruction" mvp_site/llm_service.py
```

**What to look for:**
- Instruction ordering (faction instructions may be overridden)
- Conflicting "MANDATORY" instructions
- Instruction truncation/limiting logic

### 5. Debug Tool Calling in Real-Time (MEDIUM PRIORITY)

**Hypothesis:** Tools may be available but LLM is choosing not to call them, or tool calls are being filtered out.

**Actions:**
- Add detailed logging to `llm_service.py`:
  - Log which tools are available to LLM
  - Log tool definitions sent to Gemini
  - Log raw Gemini responses
  - Log tool call detection/parsing

**Code locations:**
- `mvp_site/llm_service.py` - tool filtering/presentation
- `mvp_site/llm_providers/gemini_provider.py` - Gemini API calls
- `mvp_site/faction/tools.py` - tool definitions

### 6. Check Context Window Usage (LOW PRIORITY)

**Hypothesis:** Prompt may be getting truncated, cutting off tool definitions or critical instructions.

**Actions:**
```python
# Add logging to measure prompt length
# Check Gemini API token counts
# Verify tool definitions are included in full prompt
```

## Investigation Strategy

### Phase 1: Historical Comparison (Today)
1. ✅ Compare tool definitions (`mvp_site/faction/tools.py`)
2. ✅ Compare LLM service tool calling logic (`mvp_site/llm_service.py`)
3. ✅ Check model version used in `iteration_011`

### Phase 2: Runtime Debugging (Today/Tomorrow)
4. Add detailed logging to tool calling pipeline
5. Run single-turn test with verbose logging
6. Capture raw Gemini API requests/responses

### Phase 3: Systematic Testing (Tomorrow)
7. Test with different model versions
8. Test with simplified tool definitions
9. Test with minimal system instructions

## Key Questions to Answer

1. **Are tools actually available to the LLM?**
   - Check tool registration
   - Check tool filtering logic
   - Verify tools are in API request

2. **Is the LLM receiving tool definitions?**
   - Check prompt assembly
   - Check context window limits
   - Verify tool schemas are included

3. **Is the LLM choosing not to call tools?**
   - Check raw Gemini responses
   - Check tool call detection logic
   - Verify response parsing

4. **Are tool calls being filtered out?**
   - Check post-processing logic
   - Check validation/error handling
   - Verify tool results are preserved

## Expected Outcomes

### Best Case
- Find a single root cause (e.g., tool definition change, model version difference)
- Fix is straightforward (revert change or adjust configuration)
- Tool invocation rate returns to 56%+

### Worst Case
- Multiple interacting factors
- Requires systematic debugging
- May need to rebuild tool calling approach

### Most Likely
- Combination of factors:
  - Model version differences
  - Tool definition changes
  - System instruction conflicts
- Requires incremental fixes and testing

## Success Criteria

- **Short-term:** Identify root cause(s) of regression
- **Medium-term:** Restore tool invocation rate to 56%+ (iteration_011 baseline)
- **Long-term:** Achieve 100% tool invocation correctness (ultimate goal)

## Related Documents

- `docs/faction_tool_invocation_regression_analysis.md` - Full analysis
- `testing_mcp/faction/test_faction_20_turns_e2e.py` - Test script
- `mvp_site/prompts/faction_minigame_instruction.md` - Current prompt
- `mvp_site/faction/tools.py` - Tool definitions
- `mvp_site/llm_service.py` - LLM service (tool calling logic)
