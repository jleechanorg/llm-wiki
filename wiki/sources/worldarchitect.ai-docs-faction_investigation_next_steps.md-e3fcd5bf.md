---
title: "Faction Tool Invocation Investigation - Next Steps"
type: source
tags: [faction-tool, tool-invocation, regression, gemini, iteration-011, worldarchitect]
sources: []
date: 2026-01-15
last_updated: 2026-04-07
---

## Summary
Investigation into 4% tool invocation regression in faction mode. Identifies 6 key areas: compare tool definitions, compare LLM service tool calling logic, verify model version, check system instruction assembly, debug tool calling in real-time, and check context window usage. Goal is to restore tool invocation rate to 56%+ (iteration_011 baseline).

## Key Claims
- **Tool Definition Changes**: Tool schemas (description, parameters, names, registration logic) may have changed since iteration_011, making them less likely to be invoked
- **LLM Service Changes**: Tool calling mechanism in llm_service.py may have changed, affecting how tools are presented to the LLM
- **Model Version Differences**: iteration_011 may have used a different Gemini model version with different tool calling behavior
- **System Instruction Conflicts**: Other system instructions may be interfering with faction tool calling instructions
- **Tool Filtering/Availability**: Tools may be available but LLM choosing not to call them, or tool calls being filtered out
- **Context Truncation**: Prompt may be getting truncated, cutting off tool definitions or critical instructions

## Investigation Phases

### Phase 1: Historical Comparison
- Compare tool definitions (faction/tools.py)
- Compare LLM service tool calling logic (llm_service.py)
- Check model version used in iteration_011

### Phase 2: Runtime Debugging
- Add detailed logging to tool calling pipeline
- Run single-turn test with verbose logging
- Capture raw Gemini API requests/responses

### Phase 3: Systematic Testing
- Test with different model versions
- Test with simplified tool definitions
- Test with minimal system instructions

## Expected Outcomes

### Best Case
- Find single root cause (tool definition change, model version difference)
- Tool invocation rate returns to 56%+

### Worst Case
- Multiple interacting factors
- Requires systematic debugging

### Most Likely
- Combination of factors requiring incremental fixes

## Success Criteria
- **Short-term:** Identify root cause(s) of regression
- **Medium-term:** Restore tool invocation rate to 56%+ (iteration_011 baseline)
- **Long-term:** Achieve 100% tool invocation correctness

## Key Questions
1. Are tools actually available to the LLM?
2. Is the LLM receiving tool definitions?
3. Is the LLM choosing not to call tools?
4. Are tool calls being filtered out?