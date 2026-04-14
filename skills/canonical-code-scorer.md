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
