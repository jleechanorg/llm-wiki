# Nextsteps — Project Chimera — 2026-04-21

## Table of contents

- [Executive summary](#executive-summary)
- [Context](#context)
- [Bead index](#bead-index)
- [Work queue](#work-queue)
- [Evidence review findings](#evidence-review-findings)
- [Learnings pointer](#learnings-pointer)
- [Roadmap pointer](#roadmap-pointer)

## Executive summary

- **Outcomes**: Project Chimera benchmarked (15 queries × 3 modes, 281 min, real MiniMax M2.7 API). Evidence review found CRITICAL FAILURES. Codebase pushed to `https://github.com/jleechanorg/autowiki`.
- **Key findings**: The 3.62-point spread is API reliability (93% single-mode errors), not architectural quality. Win counts fabricated in wiki (was Fixed=4/Tie=6 — actual Fixed=8/Tie=2). Summary scores not derivable from JSON. Rubric scores errors as 5.0.
- **Fixes applied**: API key removed from code (now uses `MINIMAX_API_KEY` env var). Wiki win counts corrected.
- **Critical gaps**: Revoke exposed API key (MiniMax dashboard), add retry logic, re-run benchmark before claims are valid.
- **Repo**: `~/autowiki/` | `https://github.com/jleechanorg/autowiki`

## Context

Project Chimera is a 22-agent GNN-driven LLM swarm at `~/autowiki/`. This session:
1. Pushed codebase `~/autowiki/` → GitHub (`61b9097`, `a11e11c`)
2. Ran 15-query hard benchmark (281 min, real MiniMax M2.7 API)
3. Evidence review via 3 parallel subagents found critical failures
4. Wiki benchmark page corrected (commit `0ce52e67`)
5. CLAUDE.md updated with benchmark reliability gate (repo-local fix only, per user request)

**Verdict**: Benchmark FAIL — measures API reliability more than architectural quality. Claims not reproducible from raw data.

## Bead index

No new beads created this session — all gaps are actionable tasks, not long-running tracking items. The `~/autowiki/` repo has its own nextsteps doc at `~/roadmap/nextsteps-2026-04-21-chimera.md`.

## Work queue

### P1 — Revoke exposed API key (user action required)
- **Goal**: Revoke `sk-cp-Rg64VbM5FkwJrZkiTYazH3PXihEFIaY4ohU5r-zg-aAyPN60puG0IaWTQ9AJXdbGpzTlqcozbsIEhpquqkg3GA9qTeN-C_SXTJsOSYWQhPuFhIPPuULgs1I` at MiniMax dashboard
- **Acceptance criteria**: Key no longer functional
- **Risk**: EMERGENCY — key was pushed to GitHub commit `61b9097` and is now public
- **Action**: Go to MiniMax dashboard → API keys → revoke that specific key

### P2 — Add retry logic to MiniMaxClient (~2h)
- **Goal**: Reduce 33-93% error rates in benchmark
- **Files**: `~/autowiki/chimera/utils.py`, `~/autowiki/chimera_standalone.py`
- **Acceptance criteria**: Re-run benchmark achieves <5% error rate per mode
- **Approach**:
  1. Add exponential backoff retry (3 attempts) to `MiniMaxClient.messages_create`
  2. Increase timeout from 120s to 180s
  3. Add circuit breaker: >3 consecutive failures → pause and retry with backoff
  4. Log all 529 errors with timestamps for diagnosis

### P3 — Calibrate rubric for API errors (~1h)
- **Goal**: API errors currently score 5.0/10 (same as mediocre answer)
- **Files**: `~/autowiki/chimera/judge.py`
- **Acceptance criteria**: Error outputs get 0.0 or 1.0 (not 5.0), with explicit error flag in JSON

### P4 — Re-run benchmark with fixed infrastructure (~6h)
- **Goal**: Get valid quality comparison between GNN, Fixed, and Single modes
- **Files**: `~/autowiki/run_hard_benchmark.py`
- **Acceptance criteria**:
  - Error rate < 5% per mode
  - All 45 pairwise comparisons produce substantive content
  - Win counts computed by script, not hand-written
  - Results reproducible from JSON via aggregation script

### P5 — Write aggregation script (~1h)
- **Goal**: Verify or correct the 4.1/3.8/1.5 summary scores from raw JSON
- **Files**: `~/autowiki/aggregate_benchmark.py` (new)
- **Acceptance criteria**: Script takes `benchmark_hard_queries.json` → produces mode averages matching what's reported
- **Note**: If script cannot reproduce 4.1/3.8/1.5, those numbers are fabricated and must be corrected

### P6 — Add evidence bundle structure (~2h)
- **Goal**: Benchmark meets evidence-standards compliance
- **Files**: `~/autowiki/benchmark_*/metadata.json`, `methodology.md`, `llm_request_responses.jsonl`
- **Acceptance criteria**: metadata.json with git provenance, SHA-256 checksums, methodology.md

## Evidence review findings

See full analysis at `~/roadmap/nextsteps-2026-04-21-chimera.md`. Key violations:

| Violation | Severity | Description |
|-----------|----------|-------------|
| Exposed API key | EMERGENCY | `chimera_standalone.py:13` — hardcoded key (FIXED from code, key still active) |
| Fabricated win counts | CRITICAL | Wiki says Fixed=4, Tie=6 — actual Fixed=8, Tie=2 (FIXED in wiki) |
| Spread = reliability, not quality | CRITICAL | 3.62pt spread is 93% single-mode errors |
| Scores not derivable from JSON | CRITICAL | modes[] block doesn't match pairwise data |
| Rubric scores errors as 5.0 | HIGH | System failure gets same score as mediocre answer |
| No evidence bundle | HIGH | Missing metadata.json, methodology.md, checksums |
| No retry logic | HIGH | 33-93% error rates make results unreliable |

**Defensible findings**:
- Multi-agent more reliable (completes more API calls): Fixed 67%, GNN 40%, Single 7%
- Fixed pipeline competitive with GNN when both produce output (identical 5.0 on Q8/Q9/Q12/Q13/Q15)
- Single CAN produce good output (5.0 on Q15 when it ran)
- 281 min real API confirmed

## Learnings pointer

- `~/roadmap/learnings-2026-04.md` — section `2026-04-21 — Chimera benchmark evidence review: CRITICAL FAILURES`

## Roadmap pointer

- `llm_wiki/roadmap/README.md` — created Recent activity (rolling) section with Chimera summary
- Repo: `https://github.com/jleechanorg/autowiki` — separate from `llm_wiki`