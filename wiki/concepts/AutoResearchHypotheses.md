---
title: "AutoResearchHypotheses"
type: concept
tags: [auto-research, meta-research, hypotheses]
sources: []
last_updated: 2026-04-14
---

## Overview

This page documents hypotheses generated during the 18-cycle [[AutoResearchExperiment]] (2026-04-14), their validation status, supporting evidence, and prioritized next experiments.

---

## Hypothesis Status Summary

| Hypothesis | Status | Best Score | PR(s) |
|---|---|---|---|
| H1: LLMOutputNormalizer Pattern | **Validated** | 77/100 | #6261 |
| H2: Sentinel-First Architecture | **Validated** | 72/100 | #6254 |
| H3: EvidencePipeline Abstraction | **Partial** | 77/100 | #6247, #6232, #6219 |
| H5: TypedDict Enforcement via Pre-commit Hook | **New** | — | #6276 |

---

## H1: LLMOutputNormalizer Pattern

**Status: Validated**

**Pattern that generated it:** PRs #6261, #6254, #6265, #6214 all address LLM output fragility. `DefensiveNumericConverter` handles numeric fields well but leaves string/bool fields unnormalized.

**Hypothesis:** A full `LLMOutputNormalizer` class covering numeric + string + boolean fields would prevent entire categories of field-specific bugs.

**Evidence supporting:**
- PR #6261 scored 77/100 with strong test coverage (18 tests)
- Regex-based numeric extraction handles varied LLM output formats (comma strings, float strings, etc.)
- The pattern is sound; next extension to string fields (character names, location names) and boolean fields (level_up_available) is the natural next step

**Evidence contradicting:**
- `DefensiveNumericConverter` uses `# mypy: ignore-errors` and `# ruff: noqa: PLR0911` — cop-outs that undermine type safety
- Heavy `Any` usage prevents type enforcement (Type Safety dimension scored FAIL)
- Evidence Standard scored FAIL — no test execution logged in PR

**Key pattern documented:** `_parse_numeric(val: Any) -> int | float` with three-exception handling (ValueError, TypeError, OverflowError) and fallthrough returning 0.

---

## H2: Sentinel-First Architecture

**Status: Validated**

**Pattern that generated it:** PRs #6254, #6258 expose that `has_visible_content` inline boolean coercion is fragile and error-prone.

**Hypothesis:** A dedicated `normalize_rewards_box_for_ui()` with explicit sentinel checks per field type would be more maintainable than inline coercion.

**Evidence supporting:**
- PR #6254 scored 72/100 with 19 tests covering all sentinel branches
- Explicit `coerce_int(..., default=0)` + explicit bool coercion handles LLM string/int "true" representations
- Type guard at line 17 prevents bare exceptions
- Architecture evolved to `rewards_engine.canonicalize_rewards()` which centralizes all normalization in one place

**Evidence contradicting:**
- Pervasive `Any` throughout — no `TypedDict` for rewards_box shape
- Streaming passthrough bypass (#6265) shows that even the sentinel-first function can be circumvented at the architecture level
- PR #6265 architecture uses `rewards_engine.canonicalize_rewards()` rather than direct `normalize_rewards_box_for_ui()` calls — evolution rather than pure validation

**Key pattern documented:** Explicit `is not None` checks for sentinel fallbacks, wider truthiness check for LLM output (`if value not in (None, "", 0)`).

---

## H3: EvidencePipeline Abstraction

**Status: Partial**

**Pattern that generated it:** PRs #6247, #6219, #6232 fix CI evidence pipeline failures with similar patterns: subprocess buffering, frame extraction, gate enforcement.

**Hypothesis:** An `EvidencePipeline` base class could prevent these at the pattern level.

**Evidence supporting:**
- PRs #6247, #6232, #6219 all scored 70-77/100 with consistent patterns: DEVNULL routing for subprocess, TimeoutExpired handling, return-code enforcement
- PR #6247 fixes subprocess buffering with DEVNULL routing — a reusable pattern
- Non-fatal error handling in evidence_utils.py prevents silent skips

**Evidence contradicting:**
- No EvidencePipeline base class was created in any of the 3 PRs — the abstraction remains unimplemented
- Each PR fixes one instance without creating the generalization
- H3 should be validated by creating the abstraction, not just fixing instances

**Gap:** The abstraction is the hypothesis, not the fixes. Someone needs to create `EvidencePipeline` base class.

---

## H4: Hook-First Safety Pattern

**Status: New (identified from Cycle 6)**

**Pattern that generated it:** PR #6248 — PreToolUse hook `block-merge.sh` intercepts `gh pr merge` calls and returns `permissionDecision: deny` JSON. Module doc references incidents #6161 and #6240.

**Hypothesis:** Intercepting dangerous operations at the tool-call layer is more reliable than policy documentation (CLAUDE.md rules).

**Evidence supporting:**
- PR #6248 scored 86/100 — highest of any Python/shell PR
- Shell scripts with `set -euo pipefail`, explicit `PIPESTATUS` checking, and TOCTOU protection score consistently higher than Python equivalents
- PreToolUse hook cannot be bypassed by human error the way CLAUDE.md rules can
- Modular segment parsing handles pipes, &&, ; chaining without false positives

**Evidence contradicting:**
- No unit tests for the hook itself — MARGINAL Test Coverage
- CLAUDE.md policy changes (#6235) are important harness infrastructure even though they score 53/100 — they address different failure modes than hooks
- Hook-First and Policy Documentation are complementary, not mutually exclusive

**Key pattern documented:** `DOC_SAFE_PREFIX` allow-list prevents false positives from grep/git log commands; `PIPE_MERGE` detection handles compound commands.

---

## H5: TypedDict Enforcement via Pre-commit Hook

**Status: New (identified from Cycle 19)**

**Pattern that generated it:** Cycle 19 evaluated PR #6276 (Layer 3 CLEAN refactor) which found 213 `Any` occurrences and 152 `dict[str, Any]` patterns in `world_logic.py` alone. Across all 18 cycles, **17/17 Python PRs scored FAIL on Type Safety** — the most universal dimension failure.

**Hypothesis:** A pre-commit hook that rejects `dict[str, Any]` and bare `Any` in function signatures would force TypedDict adoption structurally, rather than leaving it as aspirational documentation.

**Evidence supporting:**
- Type Safety FAIL is universal: every single Python PR scored FAIL on this dimension
- The pattern is systemic (213 `Any` in a single 700-line file) — not incidental typos
- Cycle 19 explicitly generated H5 as a new hypothesis from the evidence
- `rewards_box` shape is well-understood and stable — prime candidate for TypedDict definition

**Evidence contradicting:**
- TypedDict definitions add upfront cost; teams may route around the hook with `# type: ignore`
- Not all structured data has stable, well-defined shapes (LLM output can be unpredictable)
- Hook enforcement is fragile if the check produces false positives

**Predicted improvement:** Type Safety dimension would go from FAIL to PASS within 5 PR cycles.

**Test plan:** Implement pre-commit hook checking for `dict[str, Any]` in function signatures; run against next 5 Python PRs. Compare Type Safety verdicts before/after hook deployment.

**Related pattern:** C1 (TypedDict Adoption Gap) in the Cross-PR Patterns section — both address the same root cause from different angles. H5 is the operationalization of C1.

---

## Cross-PR Patterns (Not Yet Hypothesized)

These patterns appeared across multiple cycles but have not yet been formalized as hypotheses:

### Pattern C1: TypedDict Adoption Gap

**Observed in:** 17/17 Python PRs — Type Safety dimension scored FAIL across all cycles due to pervasive `Any`.

**Implication:** TypedDict adoption is near zero across the codebase. A formal hypothesis about forced TypedDict adoption (e.g., via linter rule or PreToolUse hook) would address the root cause rather than symptoms.

**Suggested hypothesis:** H5: TypedDict-Mandated Normalization — requiring TypedDict definitions before adding new reward/game state fields would eliminate the `Any` problem at the source.

### Pattern C2: E2E Lock-In

**Observed in:** 15/18 PRs involve E2E tests that cannot run locally, consistently failing Evidence Standard.

**Implication:** The inability to produce evidence (test execution logs) is structural — the rubric is correct that evidence is missing, but the environment prevents fixing it.

**Suggested hypothesis:** H6: Unit-First Evidence Layer — extracting normalization/business logic into unit-testable pure functions, with E2E as a thin integration layer on top.

### Pattern C3: Composite PR Quality Dilution

**Observed in:** PRs #6241 (6 regressions, score 70), #6259 (multi-file, score 73) vs single-focus PRs at 77-86.

**Implication:** Composite PRs dilute scoring but also dilute quality attention.

**Suggested hypothesis:** H7: One-PR-One-Concern Rule — PreToolUse hook or CLAUDE.md rule enforcing single-concern PRs, with composite PRs requiring explicit exemption.

### Pattern C4: Shell Script Quality Paradox

**Observed in:** Shell-based CI fixes (#6269, #6248) consistently score 86/100 vs Python PRs averaging 70-77.

**Implication:** Shell scripts have no type system (N/A) so avoid the Type Safety FAIL, freeing weight for Error Handling and Documentation.

**Suggested hypothesis:** H8: Shell-First for Glue Code — thin orchestration glue (CI scripts, hooks) should remain shell rather than being "upgraded" to Python, preserving the quality advantages of shell simplicity.

### Pattern C5: Regressions from Centralization

**Observed in:** PR #6233 (LevelUpArchitecture, score 80) caused regressions fixed by #6241, #6243, #6245.

**Implication:** Centralization PRs carry hidden regression risk that unit tests don't catch.

**Suggested hypothesis:** H9: Centralization Regression Budget — any PR that moves logic to a canonical location must include a regression test suite covering all call sites, with the PR blocked if regression count exceeds a threshold.

### Pattern C6: Regression from Centralization (Cycle 19)

**Observed in:** PR #6276 (Layer 3 CLEAN refactor) deleted `build_level_up_rewards_box` (54 lines) and `_project_level_up_ui_from_game_state` (37 lines) after centralizing to `rewards_engine.canonicalize_rewards()`. But `test_level_up_stale_flags.py` still calls these deleted functions directly — **22 test failures**.

**Implication:** Centralization deletes local wrappers that existing tests depend on. The fix must include updating all call sites, including test files.

**Key finding from Cycle 19:** PR #6276 added 7 new wiring tests (7/7 PASS) demonstrating the new architecture, but failed to update existing regression tests. The new tests are valuable; the missing test updates are the gap.

**Deeper pattern:** C5 covers stale level-up choices. C6 covers deleted function call sites. Both are regression types from [[Layer3CleanRefactor]] architectural changes.

**Suggested hypothesis:** H10: Centralization Deletion Protocol — any PR that deletes a function must also update all test files that call it, with test pass count required to not decrease.

---

## Prioritized Next Experiments

### Priority 1: H3 Implementation

**Action:** Create the `EvidencePipeline` base class that was hypothesized but never built.

**Steps:**
1. Extract common patterns from PRs #6247, #6232, #6219: DEVNULL routing, TimeoutExpired handling, return-code enforcement, non-fatal error handling
2. Create `base_evidence_pipeline.py` with `_record`, `_stop`, `_extract_frames`, `_validate` hooks
3. Refactor `base_test.py` TmuxVideoRecorder to extend it
4. Write unit tests with mocked subprocess

**Why:** H3 is "partial" because the abstraction was never created. This is the highest-value gap.

### Priority 2: H5 TypedDict Enforcement

**Action:** Add a PreToolUse hook that detects new `dict[str, Any]` usages in function signatures and warns/blocks unless a TypedDict is defined.

**Steps:**
1. Write the hook in `.claude/hooks/require-typeddict.py`
2. Test it against PR #6276 (213 Any occurrences, would trigger hook)
3. Run against next 5 Python PRs to measure Type Safety dimension improvement

**Why:** Type Safety FAIL is universal (17/17 Python PRs) and systemic (213 Any in one file). The fix must be structural — lint rules are insufficient.

### Priority 3: H6 Unit-First Evidence Layer

**Action:** For PRs with E2E-only tests, add a parallel unit test layer.

**Steps:**
1. Pick PR #6265 (streaming normalization) as the pilot
2. Extract normalization logic into pure functions callable without Firebase/server
3. Add unit tests that mock the LLM response
4. Document the pattern for future PRs

**Why:** Evidence Standard FAIL is caused by E2E not running locally. Unit tests fix this structurally.

### Priority 4: H4 Generalization

**Action:** Create a PreToolUse pattern library beyond merge-blocking.

**Steps:**
1. Document the `block-merge.sh` pattern as a template
2. Create `block-force-push.sh`, `block-destructive-clean.sh` hooks
3. Add CLAUDE.md policy describing the hook library

**Why:** H4 scored 86/100 and is the strongest new pattern. Generalizing it maximizes value.

### Priority 5: H7 One-PR-One-Concern

**Action:** Add a PreToolUse hook that detects multi-concern PR descriptions and warns.

**Steps:**
1. Parse `git diff --name-only` to count distinct subsystems
2. If >3 subsystems changed, flag for human review
3. Document exception process

**Why:** Composite PRs score 10+ points lower and carry hidden quality risk.

---

## Related Concepts

- [[AutoResearchExperiment]] — the 18-cycle experiment (expanded to 19 in follow-up run) that generated these hypotheses
- [[CanonicalCodeScorer]] — the scoring rubric used (30% Type Safety, 70% dimensional weighting)
- [[Layer3CleanRefactor]] — architectural pattern underlying H2, H3, C5, C6 (centralization of rewards logic into rewards_engine)
- [[SelfCritiqueVerificationLoop]] — the self-critique phase that feeds into scoring
