---
title: "Extended Thinking / Test-Time Compute"
type: concept
tags: [reasoning, test-time-compute, chain-of-thought, inference-budget]
sources: []
last_updated: 2026-04-14
---

## Summary

Extended Thinking provides step-by-step reasoning prefixes before code generation, giving the model a "thinking budget" to analyze the problem before writing output. Distinct from Self-Refine because reasoning happens BEFORE generation rather than iterating AFTER.

## Key Claims

- Reasoning before generation can identify root causes and plan approaches
- Step-by-step thinking surfaces edge cases and downstream effects
- Canonical pattern application during reasoning phase can improve code quality

## Findings from Cycle B

- Extended thinking produced **identical code to baseline** in all 3 tests on worldarchitect.ai
- Reasoning was accurate but didn't change output — model likely applies internal reasoning regardless
- **Context is the bottleneck, not reasoning quality** — missing file content limits output more than missing reasoning prefixes
- Small, well-specified fixes (95%) vs medium/complex (<75%) — specificity of prompt matters more than thinking technique
- Canonical pattern references were shallow — applied at surface level, not integrated architecturally

## Technique Comparison

| Aspect | Extended Thinking | Self-Refine | Process Reward |
|---|---|---|---|
| Timing | Before generation | After generation | During generation |
| Feedback loop | None (one-shot) | Yes (iterative) | Yes (step-level) |
| Context dependency | High (needs problem spec) | High (needs output) | Medium |
| Token overhead | Medium | High | Medium |

## Usage Guidelines

- **Use when**: Problem is complex but well-specified with examples
- **Don't use when**: The bottleneck is missing file context (provide actual files instead)
- **Combine with**: File content access for best results
- **Skip for**: Small, well-specified fixes (direct generation is equally effective)

## Related Concepts

- [[SelfRefine]] — iterative refinement after generation — distinct from pre-hoc extended thinking
- [[ProcessRewardModel]] — step-level feedback during generation
- [[ChainOfThought]] — reasoning trace techniques
- [[TestTimeCompute]] — inference-time computation budget research
- [[BeamSearchOverReasoning]] — PRM-guided beam search for efficient test-time compute exploration
