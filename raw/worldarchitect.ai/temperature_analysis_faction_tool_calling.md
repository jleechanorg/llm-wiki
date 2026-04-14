# Temperature Analysis for Faction Tool Calling

**Date:** 2026-01-15  
**Question:** What does temperature do, and should we minimize variation?

## What Temperature Does

Temperature controls the **randomness/exploratory behavior** of LLM token selection:

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| **0.0** | Completely deterministic - always picks highest probability token | Maximum consistency, no variation |
| **0.1-0.3** | Low randomness - mostly follows highest probability | Focused, deterministic responses |
| **0.5-0.7** | Moderate randomness - explores alternatives | Balanced creativity/consistency |
| **0.8-1.0** | High randomness - explores many possibilities | Creative, exploratory responses |
| **>1.0** | Very high randomness - may produce unexpected outputs | Experimental, creative writing |

### For Tool Calling Specifically

**Lower Temperature (0.0-0.2):**
- ✅ More deterministic - follows instructions strictly
- ✅ Consistent behavior across similar inputs
- ❌ May "lock in" to patterns (if it starts skipping tools, keeps skipping)
- ❌ Less exploratory - may not "try" tool calling if initial pattern is to skip

**Higher Temperature (0.7-1.0):**
- ✅ More exploratory - may "try" different approaches
- ✅ Can break out of patterns (if skipping tools, might reconsider)
- ❌ Less deterministic - behavior may vary
- ❌ May call tools inconsistently

## Evidence from Our Tests

| Iteration | Temperature | Tool Invocation Rate | Notes |
|-----------|-------------|---------------------|-------|
| iteration_011 | **0.9** (default) | **56%** ✅ | Best performance - high temperature |
| iteration_014 | 0.2 | 20% | Low temperature, worse than 0.9 |
| iteration_015 | **0.0** | 12% | Zero temperature, worst performance |
| iteration_016 | 0.1 | 12% | Very low temperature, still poor |
| iteration_017 | 0.1 | 4% | Very low temperature, worst result |
| iteration_018 | **0.9** (testing) | TBD | Restored to match iteration_011 |

## Key Finding: Higher Temperature Performs Better

**Paradox:** Lower temperature (more deterministic) should follow instructions better, but actually performs WORSE for tool calling.

**Hypothesis:** 
- Lower temperature causes the model to "lock in" to a pattern of NOT calling tools
- Once it starts skipping tools, it keeps skipping (deterministic pattern)
- Higher temperature allows the model to "explore" tool calling as an option
- The model needs randomness to break out of the "skip tools" pattern

## Should We Minimize Variation?

**Answer: NO - for tool calling, we need SOME variation.**

### Why Lower Temperature Fails

1. **Pattern Lock-In:** If the model starts with a pattern of skipping tools, lower temperature reinforces that pattern
2. **No Exploration:** Lower temperature doesn't allow the model to "try" calling tools
3. **Instruction Following Paradox:** Lower temperature should follow instructions better, but tool calling requires the model to "decide" to call tools, which needs exploration

### Why Higher Temperature Works

1. **Exploration:** Higher temperature allows the model to explore different approaches
2. **Pattern Breaking:** Can break out of "skip tools" patterns
3. **Tool Discovery:** Model may "discover" that calling tools is beneficial

## Recommended Approach

### For Tool Calling: Use Moderate-High Temperature (0.7-0.9)

**Rationale:**
- iteration_011 achieved 56% with 0.9
- Lower temperatures (0.0-0.2) consistently perform worse (4-20%)
- Need exploration to break out of "skip tools" patterns

### For Other Tasks: Use Lower Temperature

**Tasks that benefit from low temperature:**
- Mathematical calculations
- Code generation (when correctness is critical)
- Factual responses
- Consistent formatting

**Tasks that benefit from higher temperature:**
- Creative writing
- Exploration of options
- Tool calling (needs to "try" calling tools)
- Breaking out of patterns

## Current Configuration

**Temperature: 0.9** (default, matches iteration_011)
- This is the configuration that achieved 56% tool invocation
- Higher than typical "deterministic" settings, but necessary for tool calling

## Alternative Approaches

If we want to minimize variation while maintaining tool calling:

1. **Temperature 0.7-0.8:** Moderate randomness, still exploratory
2. **Temperature 0.9:** Current setting (matches iteration_011)
3. **Temperature 1.0:** Maximum exploration (may be too random)

**Recommendation:** Stick with 0.9 (matches iteration_011) until we have evidence that a different value works better.

## Conclusion

**For tool calling, we should NOT minimize variation.** Higher temperature (0.9) performs better because:
- Tool calling requires exploration
- Lower temperature causes pattern lock-in
- The model needs randomness to "try" calling tools

**The goal is 100% tool invocation, not minimal variation.** If higher temperature achieves better tool calling, that's the right trade-off.
