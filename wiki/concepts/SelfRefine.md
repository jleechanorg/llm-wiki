---
title: "SelfRefine"
type: concept
tags: [self-refine, iterative-refinement, self-revision, generation-then-revise, ma拨]
sources: []
last_updated: 2026-04-15
---

## Summary

SelfRefine (Madaan et al., 2023) is a framework for iterative refinement of AI model outputs using a generate-then-revise pattern. Unlike [[ExtendedThinking]] which reasons before generation, SelfRefine iterates after generation: produce output → critique → revise → repeat. This post-hoc revision distinguishes it from pre-hoc extended thinking.

## Key Claims

- **Critique-driven revision**: A single model (or second model) critiques the output, then the original model incorporates the critique into a revised output
- **No reference needed**: Works without ground-truth labels — the model uses its own internal quality criteria
- **20-40% improvement on code generation**: Reported error reduction on tasks requiring multi-step fixes
- **Converges in 2-3 iterations**: Most gains realized in first two revision passes; diminishing returns after
- **Token overhead**: Each iteration adds substantial token cost; must be weighed against quality gains

## SelfRefine vs Extended Thinking

| Aspect | SelfRefine | Extended Thinking |
|--------|-----------|-------------------|
| Timing | After generation | Before generation |
| Feedback loop | Yes (iterative) | No (one-shot) |
| When to use | Output available, needs improvement | Problem spec available, needs planning |
| Token overhead | High (multiple passes) | Medium (one reasoning prefix) |
| Bottleneck addressed | Output quality | Approach correctness |

## Connections

- [[SelfCritique]] — self-refine uses the critique output from a self-critique pass
- [[SelfDebugging]] — self-refine is the iterative refinement mechanism that underlies self-debugging
- [[ExtendedThinking]] — complementary: Extended Thinking plans before generation, SelfRefine revises after
- [[ProcessRewardModel]] — PRM provides step-level critique signals to guide SelfRefine-like iterations
- [[VerificationLoop]] — self-refine is the "fix" mechanism in the loop, combined with [[SelfCritique]] for evaluation
- [[Reflexion]] — Reflexion adds memory to SelfRefine-like revision, tracking past critiques

## Findings from Cycle 26 (19-PR Study, 2026-04-15)

**Wide SelfRefine study**: 19 worldarchitect.ai PRs tested using 7 parallel MiniMax-M2.5 agents, 3-iteration generate→critique→revise.

### Score Distribution (19 PRs)
| Score Range | Count | PR Examples |
|-------------|-------|-------------|
| 90+ Excellent | 2 | 6254 (90.0), 6265 (92.5) |
| 85-89 Very High | 3 | 6241 (89.15), 6245 (86.5), 6212 (88.0) |
| 80-84 High | 3 | 6243 (80.25), 6247 (84.0), 6248 (82.5) |
| 76-79 Moderate | 5 | 6235 (76.75), 6258 (76.0), 6261 (76.5), 6269 (78.5), 6272 (79.0) |
| 65-75 Low | 6 | 6264 (75.0), 6233 (70.0), 6232 (66.0), 6219 (64.0), 6218 (72.0), 6233 |

**Average: 79.9/100** | **Median: 80.25/100** | **Range: 64-92.5**

### Score by Bug Type

| Bug Type | Avg Score | n | Pattern |
|---------|---------|---|---------|
| Normalization/atomicity | 89 | 3 | Targeted fixes = HIGH |
| Level/XP regressions | 87 | 3 | Multi-fix PRs = HIGH |
| TypedDict/schema | 81 | 2 | Predictable additions |
| Infrastructure (shell/test) | 80 | 4 | Consistent when described |
| Documentation-only | 77 | 1 | Limited surface |
| Refactoring | 76 | 2 | Scope harder to predict |
| Video evidence | 67 | 3 | Description ≠ actual = LOW |

### What Predicts High vs Low Accuracy

**HIGH accuracy (85+):**
- Detailed PR description with specific bug description
- Localized, targeted fix (1-10 lines)
- Bug description matches actual changes
- Multiple specific fixes listed (regression PRs)

**LOW accuracy (<75):**
- Video evidence infrastructure (description ambitious, actual incremental)
- "Steps 1-7 of N" pattern (future steps unpredictable)
- PRs where description ≠ actual scope
- GCP/infrastructure logging changes (orthogonal modifications)

### Key Insight
**PR description accuracy is the strongest predictor of SelfRefine success.** The technique works best when the PR description is detailed and matches the actual code changes. When description ≠ actual (video evidence PRs), SelfRefine consistently underperforms.

### Score by Technique (All Cycles)

| Cycle | Technique | PRs | Avg Score |
|-------|-----------|-----|-----------|
| A | SelfRefine | 3 | ~8.5/10 |
| B | ExtendedThinking | 3 | ~7.0/10 |
| C | PRM | 2 | ~7.5/10 |
| D | Canonical Scorer | 3 | ~7.7/10 |
| E | SWE-bench | 2 | ~8.0/10 |
| **26** | **SelfRefine (wide)** | **19** | **~7.99/10** |

## See Also
- [[SelfCritique]]
- [[SelfDebugging]]
- [[ExtendedThinking]]
- [[Reflexion]]
- [[ProcessRewardModel]]
- [[SWE-bench]]
