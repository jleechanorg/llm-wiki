---
title: "Temperature Analysis for Faction Tool Calling"
type: source
tags: [llm, temperature, tool-calling, faction, iteration-testing]
sources: []
source_file: worldarchitect.ai-docs-temperature_analysis_faction_tool_calling.md
date: 2026-01-15
last_updated: 2026-04-07
---

## Summary

Analysis of how LLM temperature settings affect tool calling behavior in faction systems. Counter-intuitively, higher temperature (0.9) performs BETTER for tool calling (56% invocation rate) than lower temperatures (4-20%). Lower temperature causes "pattern lock-in" where the model reinforces whatever pattern it starts with, while higher temperature allows exploration and breaking out of "skip tools" patterns.

## Key Claims

- **Higher Temperature Performs Better**: iteration_011 with temperature 0.9 achieved 56% tool invocation rate, significantly outperforming lower temperatures (0.0-0.2) which ranged from 4-20%
- **Pattern Lock-In Phenomenon**: Lower temperature causes the model to "lock in" to whatever pattern it starts with — if it begins skipping tools, it keeps skipping due to deterministic behavior
- **Exploration Required**: Tool calling requires the model to "decide" to call tools, which needs some randomness to explore different approaches
- **Recommended Setting**: Temperature 0.7-0.9 for tool calling tasks; lower temperatures (0.0-0.3) better for mathematical calculations, code correctness, and factual responses
- **Current Configuration**: Temperature 0.9 (matches iteration_011 which achieved best results)

## Key Quotes

> "Paradox: Lower temperature (more deterministic) should follow instructions better, but actually performs WORSE for tool calling." — Analysis finding

> "Lower temperature causes the model to 'lock in' to a pattern of NOT calling tools. Once it starts skipping tools, it keeps skipping (deterministic pattern)." — Root cause hypothesis

## Evidence Table

| Iteration | Temperature | Tool Invocation Rate | Notes |
|-----------|-------------|---------------------|-------|
| iteration_011 | 0.9 (default) | **56%** ✅ | Best performance - high temperature |
| iteration_014 | 0.2 | 20% | Low temperature, worse than 0.9 |
| iteration_015 | 0.0 | 12% | Zero temperature, worst performance |
| iteration_016 | 0.1 | 12% | Very low temperature, still poor |
| iteration_017 | 0.1 | 4% | Very low temperature, worst result |

## Recommendations

**For Tool Calling**: Use temperature 0.7-0.9
- Allows exploration of different approaches
- Can break out of "skip tools" patterns
- Model may "discover" that calling tools is beneficial

**For Other Tasks**: Use lower temperature (0.0-0.3)
- Mathematical calculations
- Code generation (when correctness is critical)
- Factual responses
- Consistent formatting

## Conclusion

**Do NOT minimize variation for tool calling.** The goal is 100% tool invocation, not minimal variation. Higher temperature achieves better tool calling performance, making it the right trade-off despite more variable outputs.