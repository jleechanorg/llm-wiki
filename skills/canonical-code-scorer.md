# Canonical Code Scorer – Rubric + Diff Metric

Score generated code against canonical patterns from the ingested repos (FastAPI, tRPC, Requests, Axum, etc.).

## Rubric Dimensions (Pass/Fail each)

1. **Naming & Consistency** — Variables, functions, files follow consistent naming conventions
2. **Error Handling & Robustness** — Proper exception handling, input validation, edge cases covered
3. **Type Safety / Architecture** (30% weight) — Strong typing, correct data structures, clean architecture
4. **Test Coverage & Clarity** — Tests are readable, cover unit/integration/edge cases
5. **Documentation & Comments** — Docstrings, comments explain *why*, not *what*
6. **Evidence-Standard Adherence** — Output meets harness evidence standards (video, proof, etc.)

## Diff Similarity

Compute token-level edit distance between the generated file and the ground-truth PR file. Convert to a 0–100 similarity score.

## Overall Score Formula

```
Overall score = 0.7 × rubric-weighted Pass-rate + 0.3 × diff similarity
```

## Type Safety FAIL Is the #1 Systematic Problem — Enforce This Strictly

Across 18 cycles of auto-research (2026-04-14), every single Python PR scored FAIL on Type Safety. This is not noise — it is the dominant failure mode.

**Automatic FAIL conditions:**
- `# mypy: ignore-errors` anywhere in the file
- `# ruff: noqa` blanket suppressions
- `Any` used for structured data (rewards_box, game_state, evidence_bundle)
- `dict[str, Any]` without a corresponding TypedDict
- `result: dict` with no TypedDict annotation

**Automatic PASS conditions:**
- TypedDict used for all structured data
- `Any` only for genuinely untyped external data (e.g., raw JSON from third-party API)
- Three-exception pattern for parsing: `try: ... except (ValueError, TypeError, OverflowError): return default`

**Partial credit (MARGINAL):**
- TypedDict defined but not fully used — still penalize incomplete adoption
- `dict[str, Any]` with inline comment explaining why TypedDict is not possible — rarely acceptable

### Shell Scripts Score Differently

Shell scripts (`.sh`) have no type system. The Type Safety dimension is **excluded** (N/A) rather than treated as FAIL. The 30% weight is redistributed to other dimensions. Shell scripts consistently score 86/100 due to excellent error handling and documentation.

### Composite/Multi-File PRs Score Lower

PRs touching 4+ files (#6241 SixRegressionFixes: 70/100, #6259 PRRegressionResolution: 73/100) score 7-10 points lower than single-focus PRs (77-80/100). Flag this in scoring notes but do not artificially deflate — record it as a structural observation.

### Policy Documents Misfit the Rubric

CLAUDE.md harness policy changes score ~53/100 because the rubric is designed for code. Do not penalize policy docs for missing type safety or test coverage. Apply a modified rubric: documentation quality only. Policy effectiveness can only be measured over time.

### Evidence Standard Almost Universally FAIL

Almost all 18 cycles scored FAIL on Evidence Standard because E2E tests (Firebase required) cannot run locally. Before declaring FAIL, check:
1. Was test execution attempted and logged? (even a screenshot counts)
2. Is the failure a structural limitation (E2E requiring Firebase) or an oversight?
3. If structural: document the limitation explicitly in the notes, do not just mark FAIL silently

## Output Format

```
Overall score: [0–100]
Per-dimension breakdown:
  - Naming & Consistency: Pass/Fail [optional comment]
  - Error Handling & Robustness: Pass/Fail [optional comment]
  - Type Safety / Architecture: Pass/Fail [optional comment]
  - Test Coverage & Clarity: Pass/Fail [optional comment]
  - Documentation & Comments: Pass/Fail [optional comment]
  - Evidence-Standard Adherence: Pass/Fail [optional comment]

Improvement suggestions:
- [suggestion referencing concrete wiki pages]
```

## Integration

- Called by [[AutoResearchLoop]] Phase 3 (Evaluation)
- Canonical patterns sourced from ingested repos: FastAPI, tRPC, Requests, Axum
- Results feed back into the wiki "Results on My Codebase" section

## Tags

#agent-harness #coding-agents #evaluation #scoring
