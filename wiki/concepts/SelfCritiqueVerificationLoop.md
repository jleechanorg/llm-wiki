---
title: "SelfCritiqueVerificationLoop"
type: concept
tags: [agent-harness, coding-agents, verification, self-correction]
sources: [auto-product-master-system, auto-research-experiment-v21]
last_updated: 2026-04-14
---

## Definition

A 3-iteration-cap verification loop for rigorous coding agent output. Combines ReVeal (2026) test-generation-and-execution with Self-Correction (2025) iterative refinement. Mandated before any code output in the auto-research experiment.

## How It Works

**Phase 0 – Prompt Chaining**
Insert a short "canonical pattern" prompt extracted from the wiki (e.g., "FastAPI error handling pattern") before any generation.

**Phase 1 – Generation**
Think step-by-step and generate the initial code.

**Phase 2 – Test Generation & Execution**
Generate a full test suite (unit, integration, edge cases). Run the tests in a sandbox (Docker/virtualenv). Capture any failures, compilation errors, or runtime exceptions.

**Phase 3 – Self-Critique**
Using the concrete test results, critique the code against:
- Correctness vs. PR requirements
- Edge-case coverage
- Efficiency & style
- Security / robustness
- Evidence-standard compliance

If any issue is found and fewer than 3 iterations have been performed, go back to Phase 2 with revised tests or code.
If all tests pass and the critique is clean, output ONLY the final verified code.

## Output Format (exact)

```
Initial code
Tests + execution results
Critique
Revised code (only if needed)
Final verified code only
```

## Key Design Choices

- **3-iteration cap**: Balances quality improvement against token cost explosion
- **Sandboxed test execution**: Real test results, not self-assessed quality
- **Canonical pattern prompt chaining**: Grounds generation in proven patterns from the wiki
- **Exact output format**: Forces clean separation between process and final artifact

## Integration Points

- Used by [[AutoResearchLoop]] in Phase 2 (Implementation)
- Outputs feed into [[CanonicalCodeScorer]] for quantitative evaluation
- Canonical patterns sourced from [[AutoProductMasterSystem]] wiki pages

## Evidence: OpenClaw Self-Refine Experiment (Cycle 1)

**Finding**: Self-refine WITHOUT file context hits token cap (4,096 tokens, 45s) and still fails to match ground truth. Context > Self-Critique for deterministic fixes.

Key insight from [[openclaw-self-refine-experiment]] — self-critique cannot compensate for missing context. The [[SelfCritiqueVerificationLoop]] provides context via canonical pattern prompt chaining, which addresses this failure mode.

## Related Concepts

- [[AutoResearchLoop]] — the outer loop that calls this as a subroutine
- [[CanonicalCodeScorer]] — scores the final verified output
- [[SelfCorrection2025]] — the self-correction component of the loop
- [[ReVeal2026]] — the test-generation-and-execution component
