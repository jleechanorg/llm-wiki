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

- **Outcomes**: Project Chimera benchmarked (15 queries × 3 modes, 281 min, real MiniMax M2.7 API). Evidence review found CRITICAL FAILURES. All infrastructure fixes now committed to `https://github.com/jleechanorg/autowiki` (commit `fb78717`).
- **Key findings**: The 3.62-point spread is API reliability (93% single-mode errors), not architectural quality. Win counts fabricated in wiki (was Fixed=4/Tie=6 — actual Fixed=8/Tie=2). Claimed averages 4.1/3.8/1.5 are FABRICATED — confirmed by `aggregate_benchmark.py`: actual averages excluding errors are 5.0/5.0/5.46. Rubric scores errors as 5.0.
- **Fixes applied**: P2 (retry/logic), P3 (rubric calibration), P5 (aggregation script), P6 (evidence bundle) — all committed. API keys removed from all Python files. Hardcoded paths replaced with `__file__`-relative paths.
- **P4 remaining**: Re-run benchmark with fixed infrastructure (~6h). Requires `MINIMAX_API_KEY` env var set.
- **P1 (user action)**: Revoke exposed API key at MiniMax dashboard — key was in code and pushed to GitHub.
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

### P1 — Revoke exposed API key ⚠️ USER ACTION REQUIRED
- **Status**: API key removed from code, but key itself still active
- **Goal**: Revoke `sk-cp-Rg64...` at MiniMax dashboard
- **Action**: Go to MiniMax dashboard → API keys → revoke that specific key

### P2 — ✅ DONE — Add retry logic to MiniMaxClient
- **Files**: `~/autowiki/chimera/utils.py` (commit `fb78717`)
- **Changes**: 3-attempt exp backoff, 180s timeout, circuit breaker, 529 timestamp logging

### P3 — ✅ DONE — Calibrate rubric for API errors
- **Files**: `~/autowiki/chimera/judge.py`, `~/autowiki/run_hard_benchmark.py` (commit `fb78717`)
- **Changes**: `score_single_output()` detects error patterns, returns `{"is_error": true, "overall": 0.0}`, errors excluded from averages

### P4 — ⬜ PENDING — Re-run benchmark (~6h)
- **Goal**: Get valid quality comparison between GNN, Fixed, and Single modes
- **Files**: `~/autowiki/run_hard_benchmark.py`
- **Acceptance criteria**: Error rate <5% per mode, all 45 pairwise comparisons produce substantive content, win counts computed by script
- **Note**: All infrastructure fixes are in place (P2+P3). Run after P1 is resolved.

### P5 — ✅ DONE — Write aggregation script
- **Files**: `~/autowiki/aggregate_benchmark.py` (commit `fb78717`)
- **Finding**: Claimed 4.1/3.8/1.5 are FABRICATED. Actual (excluding errors): single=5.0, fixed=5.0, gnn=5.46

### P6 — ✅ DONE — Add evidence bundle structure
- **Files**: `~/autowiki/benchmark_logs/` (commit `fb78717`)
- **Files created**: `metadata.json`, `methodology.md`, `llm_request_responses.jsonl`, `checksums.sha256`

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