---
title: "Process Reward Model (PRM)"
type: concept
tags: [prm, process-reward, step-level-feedback, reasoning, llm]
sources: []
last_updated: 2026-04-15
---

## Summary

Process Reward Model (PRM) breaks fix generation into step-level evaluation, scoring each step 1-10 before proceeding. Unlike [[SelfRefine]] which critiques the full output, PRM guides generation by rewarding individual steps — catching misdiagnosis early before wasting compute on wrong approaches.

## How It Works

1. **Decompose** the fix into logical steps (root cause, guard clause, TypedDict, error propagation, tests)
2. **Score each step** 1-10 on quality and correctness
3. **Revise step** if score < 7 before moving to next step
4. **Sum weighted step scores** for final evaluation

## Key Claims

- **Early misdiagnosis detection**: Step-level feedback catches wrong root cause hypotheses before they cascade
- **Guided refinement**: Low-scoring steps get revision passes, not the whole output
- **Better than outcome reward**: Process feedback identifies *why* something is wrong, not just that it is wrong

## Findings from Cycle C (PR #6275)

**PR #6275**: fix(level-up): synthesize rewards_box when level_up_complete=True but box missing

### What PRM Found

PRM correctly identified that the **reported root cause (C9 — field name inconsistency) was a red herring**. The actual bug was a logic gap in stuck-completion detection.

| Step | Description | Score | Verdict |
|------|-------------|-------|---------|
| 1 | HasLevelUpUISignal detects stuck completion | 1.0/1.0 | CORRECT |
| 2 | ResolveCanonicalPair synthesizes box | 1.0/1.0 | CORRECT |
| 3 | Field name consistency | 1.0/1.0 | CORRECT (but C9 was misdiagnosis) |
| 4 | Integration end-to-end | 1.0/1.0 | CORRECT |

**Score: 6.25/10** — Lower than expected because the root cause hypothesis was wrong initially. PRM's step-level feedback helped correct course.

### Key Insight
PRM's strength is **guiding away from wrong hypotheses**. The step-level scoring surfaced that the C9 field name issue was benign (local parameter names, not dict keys). The actual fix was adding stuck-completion detection logic.

### When PRM Works Best

| Scenario | PRM Score | Why |
|----------|-----------|-----|
| PRs with misleading/misdiagnosed root causes | HIGH | Step feedback catches misdiagnosis early |
| PRs where description ≠ actual bug | HIGH | C9 was wrong; PRM corrected course |
| Simple targeted fixes | MODERATE | Overhead not worth it |
| Well-understood bugs | LOW | No misdiagnosis to catch |

### Limitation
Requires good step decomposition. For poorly-understood bugs, scoring steps is as hard as fixing them.

## Comparison with Other Techniques

| Aspect | PRM | [[SelfRefine]] | [[ExtendedThinking]] | [[SWE-bench]] |
|--------|-----|----------------|---------------------|--------------|
| Granularity | Step-level | Full output | Full reasoning | Test-level |
| Feedback timing | During generation | After generation | Before generation | After test |
| Misdiagnosis detection | **STRONG** | Weak | Moderate | Moderate |
| Token overhead | Medium | High | Medium | High |
| Best for | Complex/misdiagnosed bugs | Well-described fixes | Architecture reasoning | Infrastructure |

## Usage Guidelines

**Use PRM when:**
- PR description mentions a root cause that might be wrong
- The reported bug could have multiple causes
- Step-by-step reasoning would help isolate the real issue

**Don't use PRM when:**
- The fix is straightforward and well-understood
- Token budget is constrained
- Multiple orthogonal changes (step decomposition gets messy)

## Related Concepts

- [[SelfRefine]] — iterative refinement after full output — PRM is more granular
- [[ExtendedThinking]] — pre-hoc reasoning without step rewards
- [[ChainOfThought]] — reasoning traces without process rewards
- [[BeamSearchOverReasoning]] — PRM-guided search over reasoning paths
- [[SelfCritique]] — PRM step feedback resembles critique, but during generation not after
