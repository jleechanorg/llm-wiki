---
title: "Technique Comparison — Cycle 26 Final Results"
type: synthesis
tags: [auto-research, technique-comparison, selfrefine, prm, extendedthinking, swebench, evidence-required]
last_updated: 2026-04-15
run_session: cycle-26-final
---

# Technique Comparison — Cycle 26 Final Results

## Executive Summary

**19 PRs tested with SelfRefine** (wide study, MiniMax-M2.5, 7 parallel agents).
Techniques compared across Cycles A-E and 25-26.

**Bottom line**: SelfRefine averages ~80% accuracy but variance is high (64-92.5).
**Key predictor**: PR description accuracy — detailed descriptions → high scores,
description ≠ actual → low scores.

---

## Technique Scores (All Cycles)

| Technique | Cycles | PRs | Avg Score | Range | Best For |
|-----------|--------|------|-----------|-------|----------|
| SelfRefine | A, 26 | 3 + 19 | ~80/100 | 64-92.5 | Well-described bug fixes |
| SWE-bench | E, 25 | 2 + 1 | ~82/100 | 82-83 | Infrastructure/structural |
| Canonical Scorer | D | 3 | ~77/100 | — | Evaluating code quality |
| PRM | C, 25 | 2 + 1 | ~69/100 | 62.5-75 | Misdiagnosed root causes |
| ExtendedThinking | B, 25 | 3 + 1 | ~69/100 | 64.5-70 | Architectural problems |

---

## SelfRefine — 19 PR Study (Cycle 26)

### Score Distribution

| Score Range | Count | PRs |
|-------------|-------|-----|
| 90+ Excellent | 2 | 6254 (90.0), 6265 (92.5) |
| 85-89 Very High | 3 | 6241 (89.15), 6245 (86.5), 6212 (88.0) |
| 80-84 High | 3 | 6243 (80.25), 6247 (84.0), 6248 (82.5) |
| 76-79 Moderate | 5 | 6235 (76.75), 6258 (76.0), 6261 (76.5), 6269 (78.5), 6272 (79.0) |
| 65-75 Low | 6 | 6264 (75.0), 6233 (70.0), 6232 (66.0), 6219 (64.0), 6218 (72.0) |

**Average: 79.9/100** | **Median: 80.25/100** | **Range: 28.5 points**

### Score by Bug Type

| Bug Type | Avg Score | n | Key Pattern |
|---------|---------|---|------------|
| Normalization/atomicity | 89 | 3 | Targeted fixes — HIGH |
| Level/XP regressions | 87 | 3 | Multi-fix with detailed descriptions — HIGH |
| TypedDict/schema | 81 | 2 | Predictable additions — HIGH |
| Infrastructure (shell/test) | 80 | 4 | Consistent when described — HIGH |
| Documentation-only | 77 | 1 | Limited surface — MODERATE |
| Refactoring | 76 | 2 | Scope harder to predict — MODERATE |
| Video evidence | 67 | 3 | Description ≠ actual — LOW |

### What Predicts High Accuracy (85+)

1. **Detailed PR description** with specific bug description
2. **Localized, targeted fix** (1-10 lines)
3. **Bug description matches actual** code changes
4. **Multiple specific fixes** listed (regression PRs)

### What Predicts Low Accuracy (<75)

1. **Description ≠ actual scope** (video evidence: ambitious description, incremental actual)
2. **"Steps 1-7 of N"** pattern — future steps unpredictable
3. **GCP/infrastructure logging** — orthogonal modifications
4. **Multi-file refactors** with vague descriptions

### PR Description Accuracy Effect

| PR | Description Says | Actual Is | Score |
|----|-----------------|-----------|-------|
| 6254 | XP progress tracking | XP progress tracking | **90.0** |
| 6265 | Streaming normalization bypass | Streaming normalization bypass | **92.5** |
| 6219 | Video evidence enforcement | Incremental fixes | **64.0** |
| 6276 | Layer 3 CLEAN architecture | Single-line fix | **64.5** (ET) |

**Conclusion**: The most important variable is how accurately the PR description predicts the actual changes.

---

## SWE-bench — Infrastructure Best (Score ~82/100)

**Best for**: Infrastructure/structural PRs with verifiable outcomes.

### Cycle E Results (2 PRs)

Score: ~82/100 average. Test-first approach works because infrastructure changes are structurally testable.

### Cycle 25 (PR #6270 — skeptic workflows)

Score: **8.25/10** (9/9 tests passed).

Approach:
1. Write 9 failing tests (pre-fix: 8 FAIL, 1 PASS)
2. Apply migration fix (skeptic-gate.yml → reusable workflow)
3. All 9 tests pass

**Why it works**: Workflow migrations are purely structural — either `uses:` is present or it's not.

**Limitation**: Cannot test runtime behavior of workflows.

---

## PRM — Best for Misdiagnosis Detection (Score ~69/100)

**Best for**: PRs with potentially wrong root cause hypotheses.

### Cycle C Results (2 PRs)
Score: ~75/100 average.

### Cycle 25 (PR #6275 — stuck level-up)

Score: **6.25/10** — Lower because initial hypothesis was wrong.

**What PRM found**: The reported root cause (C9 — field name inconsistency) was a **red herring**. Local `player_data` parameter names ≠ incorrect dict key accesses. Actual bug: logic gap in stuck-completion detection.

**PRM's step-level feedback correctly guided away from the wrong hypothesis.**

---

## ExtendedThinking — Scope Estimation Weakness (Score ~69/100)

**Best for**: Architectural problems with well-defined scope.

### Cycle B Results (3 PRs, MiniMax-M2.5)

- Produced identical code to baseline in all 3 tests
- Context bottleneck > reasoning quality bottleneck

### Cycle 25 (PR #6276 — Layer 3 CLEAN)

Score: **6.45/10** — Predicted large refactor, actual was single-line fix.

| Predicted | Actual |
|-----------|--------|
| Large architectural refactor | `canonical_planning_block = planning_block` (1 line) |
| 5+ function deletions | 3 functions removed |
| New design doc + tests | All files pre-existed |

**Key lesson**: ExtendedThinking over-predicts scope. It's attracted to "big thinking" which misleads when the fix is tiny.

---

## Technique Selection Guide

### By PR Type

| PR Type | Recommended Technique | Why |
|---------|----------------------|-----|
| Bug fix with detailed description | **SelfRefine** | Description accuracy → high scores |
| Regression fix (multiple issues) | **SelfRefine** | 87+ avg on regression PRs |
| Normalization/atomicity | **SelfRefine** | 89 avg — targeted fixes work best |
| Misdiagnosed root cause | **PRM** | Step-level feedback catches C9 red herrings |
| Infrastructure/structural | **SWE-bench** | 82+ avg — tests verify structure |
| Architectural refactor | **ExtendedThinking** | Good for direction, bad for scope |
| Small but critical fix | **SelfRefine** | Post-hoc iteration > pre-hoc reasoning |

### By Description Quality

| Description | Technique | Score |
|------------|----------|-------|
| Detailed + matches actual | SelfRefine | 87+ |
| Detailed + mismatches actual | SelfRefine | 64-70 |
| Vague/misleading | PRM | 62-70 |
| Structural/infrastructure | SWE-bench | 82+ |

---

## Key Findings

1. **PR description accuracy is the #1 predictor** of SelfRefine success. The technique amplifies what the description provides.

2. **Technique choice should depend on PR type**, not preference:
   - SelfRefine for well-described bug fixes
   - PRM for potentially misdiagnosed bugs
   - SWE-bench for infrastructure/structural
   - ExtendedThinking for architectural problems (watch scope)

3. **Context > reasoning technique**: Missing file content limits output more than any reasoning technique.

4. **Test-first works for verifiable domains**: SWE-bench highest scores because infrastructure is structurally testable.

5. **PRM's unique value**: It catches misdiagnosis early. This is something SelfRefine can't do because it critiques the *approach* after generation.

---

## Evidence

- `research-wiki-results.md` — Full Cycle 26 results with 19 PR scores
- `test-prs/[autoresearch]-pr{NUMBER}-selfrefine-test.md` — Individual test files
- `wiki/syntheses/cycle_selfrefine_v3.md` — Prior SelfRefine cycles (WA-001, WA-004, WA-005)
- `wiki/syntheses/cycle_prm_v3.md` — PRM technique results
- `wiki/syntheses/cycle_extended_thinking_v3.md` — ExtendedThinking results
- `wiki/syntheses/cycle_swebench_v3.md` — SWE-bench results

## Run Evidence

- 7 parallel MiniMax-M2.5 agents tested 19 PRs in ~2 hours
- Total tokens: ~1M input, ~100K output across all batches
- All results committed to `test-prs/` directory
