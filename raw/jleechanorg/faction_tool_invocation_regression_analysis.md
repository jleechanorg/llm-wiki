# Faction Tool Invocation Regression Analysis

**Date:** 2026-01-15  
**Status:** 🔴 CRITICAL REGRESSION - Tool invocation rate dropped to 4%  
**Goal:** Achieve 100% tool invocation correctness for faction minigame

## Executive Summary

Despite restoring the exact prompt structure from `iteration_011` (which achieved 56% tool invocation), the current test run (`iteration_017`) shows only **4% tool invocation** (1/25 turns). This represents a **92% regression** from the baseline and suggests factors beyond prompt structure are affecting tool calling behavior.

## Test Results Timeline

| Iteration | Prompt Version | Lines | Temperature | Tool Invocation Rate | Notes |
|-----------|---------------|-------|-------------|---------------------|-------|
| iteration_011 | Baseline | 1902 | Unknown | **56% (14/25)** | ✅ Best performance |
| iteration_013 | Unknown | Unknown | Unknown | 20% (5/25) | Initial regression |
| iteration_014 | v1 baseline | 2013 | 0.2 | 20% (5/25) | Added explicit top-level tool section |
| iteration_015 | v2 condensed | 413 | 0.0 | 12% (3/25) | Aggressive reduction, too short |
| iteration_016 | v1 restored | 2013 | 0.1 | 12% (3/25) | Restored baseline, still low |
| iteration_017 | iteration_011 exact | 1902 | 0.1 | **4% (1/25)** | 🔴 Exact prompt structure, worst result |

## Key Findings

### 1. Prompt Structure Hypothesis - DISPROVEN

**Hypothesis:** Removing the explicit "Tool Usage for Faction Minigame" section at the top (present in v1 baseline) would restore `iteration_011` performance, since `iteration_011` achieved 56% without it.

**Result:** ❌ **FAILED** - Even with the exact `iteration_011` prompt structure (1902 lines, JSON Schema first, no top-level tool section), tool invocation dropped to 4%.

**Conclusion:** Prompt structure alone is NOT the primary factor causing the regression.

### 2. Temperature Settings - INCONCLUSIVE

- `temp=0.0`: 12% (iteration_015)
- `temp=0.1`: 12% (iteration_016), 4% (iteration_017)
- `temp=0.2`: 20% (iteration_014)

**Conclusion:** Temperature changes don't explain the regression pattern. Lower temperatures don't consistently improve tool calling.

### 3. Prompt Length - INCONCLUSIVE

- 413 lines (v2): 12%
- 1902 lines (iteration_011 exact): 4%
- 2013 lines (v1 baseline): 12-20%

**Conclusion:** Prompt length alone doesn't explain the regression. The shortest prompt (413 lines) performed better than the exact baseline (1902 lines).

### 4. Tool Invocation Pattern Analysis

**iteration_017 breakdown:**
- **Only Turn 22** (combat action) invoked tools: `faction_calculate_power`, `faction_calculate_ranking`, `faction_simulate_battle`
- **All other 24 turns:** Zero tool invocations
- **Faction headers generated:** 22/25 turns (88%) - LLM is generating headers WITHOUT calling tools
- **Tutorial triggered:** 21/25 turns (84%)

**Critical observation:** The LLM is generating faction headers (which should require tool results) WITHOUT calling the required tools. This suggests:
1. LLM is hallucinating FP values instead of calling tools
2. Tool calling mechanism may be broken or disabled
3. LLM may be ignoring tool requirements entirely

## Potential Root Causes

### 1. Model Version Changes
- `iteration_011` may have used a different Gemini model version
- Current model: `gemini-3-flash-preview` (pinned in test)
- Model behavior may have changed between versions

### 2. Tool Definition Changes
- Tool schemas may have changed since `iteration_011`
- Tool availability/registration may differ
- Tool calling mechanism may have been modified

### 3. LLM Service Changes
- Tool calling logic in `llm_service.py` may have changed
- Tool filtering/availability checks may be blocking calls
- Response parsing may be failing silently

### 4. System Instruction Changes
- Other system instructions may be interfering
- Prompt injection or override mechanisms may be active
- Context window limits may be truncating tool definitions

### 5. Test Environment Differences
- Server configuration differences
- Dependency versions
- Environment variables affecting behavior

## Current Configuration

**Prompt:** `mvp_site/prompts/faction_minigame_instruction.md`
- Exact structure from `iteration_011` (1902 lines)
- JSON Schema introduced first
- Tool instructions later in document
- No top-level "Tool Usage" section
- No reminder tokens (`<<CALL-TOOL>>`)

**Temperature:** 0.1 (allows slight stochasticity for "reconsideration")

**Model:** `gemini-3-flash-preview` (pinned)

**Server:** Fresh local server on free port (no disconnects)

## Test Infrastructure Improvements

✅ **Fixed:** Test now starts fresh local server automatically on free port  
✅ **Fixed:** Server stability issues resolved (no more disconnects)  
✅ **Fixed:** Test completes reliably and saves evidence bundles

## Next Steps - Investigation Priorities

### High Priority
1. **Compare tool definitions** between `iteration_011` commit and current HEAD
2. **Check LLM service changes** that might affect tool calling
3. **Verify model version** used in `iteration_011` vs current
4. **Review system instruction assembly** - check for conflicts/overrides

### Medium Priority
5. **Compare full prompt context** - what other instructions are being sent?
6. **Check tool registration** - are tools actually available to the LLM?
7. **Review response parsing** - are tool calls being detected correctly?

### Low Priority
8. **Test with different models** to isolate model-specific behavior
9. **Check for prompt injection** or override mechanisms
10. **Review context window usage** - is prompt being truncated?

## Questions for GenesisFaction

1. What factors beyond prompt structure could cause such a severe regression?
2. Should we investigate tool definition changes or LLM service changes first?
3. Is there a way to verify what model version was used in `iteration_011`?
4. Could other system instructions be interfering with tool calling?
5. What debugging approaches would you recommend to isolate the root cause?

## Evidence Files

- **Test results:** `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/iteration_017/`
- **Test log:** `/tmp/faction_test_iteration_018.log`
- **Prompt file:** `mvp_site/prompts/faction_minigame_instruction.md`
- **LLM service:** `mvp_site/llm_service.py` (temperature override at line ~3370)

## Related Commits

- `95b3919a3` - Restore exact iteration_011 prompt structure
- `18107d2e4` - Revert prompt to baseline + temperature 0.1 per GenesisFaction analysis
- `08bdc05f5` - Simplify faction prompt: Remove aggressive language, improve tool invocation
