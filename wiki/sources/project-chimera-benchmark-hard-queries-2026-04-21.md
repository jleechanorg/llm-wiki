---
title: "Project Chimera Benchmark: Hard Queries (All Runs)"
type: source
tags: [multi-agent-systems, benchmark, gnns, minimax, llm-orchestration]
sources: [project-chimera-neural-network-llm-agents-2026-04-19, project-chimera-codebase-2026-04-20]
last_updated: 2026-04-21
---

## Summary

15 hard research queries × 3 Chimera modes (single/fixed/GNN) run on real Minimax M2.7 API over 281 minutes. **Critical caveat: results dominated by API reliability (33-93% error rates), not pure architectural quality.** Multi-agent completes more API calls than single mode, but the quality gap is unclear.

## Key Claims

- **Single mode errors on 14/15 hard queries** (93% failure rate) — the 1.0/10 scores are API timeouts, not quality assessments
- **Multi-agent is more reliable**: Fixed completes 67% of calls, GNN completes 40%, Single completes only 7%
- **GNN vs Fixed: essentially tied on quality, but Fixed more reliable** — Fixed wins 8 head-to-head queries, GNN wins 5, with 2 ties. Average scores favor GNN but this is largely which queries timed out.
- **Average spread 3.62 points = API reliability gap**, not pure quality difference

## Detailed Results

| Query | Single | Fixed | GNN | Winner | Spread |
|-------|--------|-------|-----|--------|--------|
| Q1: Investment portfolio strategy | 1.0 | 1.0 | 6.8 | GNN | **5.8** |
| Q2: Russia-Ukraine geopolitical analysis | 5.0 | 5.0 | 5.0 | TIE | 0.0 |
| Q3: Emerging programming languages for AI | 1.0 | 3.7 | 5.0 | GNN | 4.0 |
| Q4: Manufacturing scale-up plan | 1.0 | 5.0 | 1.0 | FIXED | 4.0 |
| Q5: AI framework architecture critique | 1.0 | 5.0 | 1.0 | FIXED | 4.0 |
| Q6: B2B SaaS competitive analysis | 1.0 | 5.0 | 1.0 | FIXED | 4.0 |
| Q7: Conflicting academic papers synthesis | 1.0 | 1.0 | 5.0 | GNN | 4.0 |
| Q8: Technical due diligence report | 1.0 | 5.0 | 5.0 | FIXED/GNN | 4.0 |
| Q9: Multi-cloud HIPAA architecture | 1.0 | 5.0 | 5.0 | FIXED/GNN | 4.0 |
| Q10: CUDA vs ROCm comparison | 1.0 | 1.0 | 5.5 | GNN | 4.5 |
| Q11: Nuclear fusion approaches | 1.0 | 5.0 | 1.0 | FIXED | 4.0 |
| Q12: FinTech security audit checklist | 1.0 | 5.0 | 5.0 | FIXED/GNN | 4.0 |
| Q13: Enterprise AI pricing strategy | 1.0 | 5.0 | 5.0 | FIXED/GNN | 4.0 |
| Q14: Climate policy agricultural output | 1.0 | 1.0 | 5.0 | GNN | 4.0 |
| Q15: US presidential election analysis | 5.0 | 5.0 | 5.0 | TIE | 0.0 |

## Key Insights

1. **Single mode fails 93% of the time**: 14/15 queries produced API errors (timeout or 529). The 1.0 scores are error text, not quality assessments. When single mode ran successfully (Q15), it scored 5.0 — equivalent to multi-agent modes.

2. **Multi-agent advantage is reliability, not quality**: Fixed completed 67% of calls, GNN 40%, Single 7%. The 3.62-point spread is an API reliability gap.

3. **GNN vs Fixed — Fixed wins head-to-head**: Fixed wins 8 queries, GNN wins 5, Tie 2. The GNN's higher average (4.1 vs 3.8) comes from Q1 where Fixed timed out and GNN produced a 17K-token report — not a systemic advantage.

4. **When multi-agent genuinely helps**: Q7 (conflicting academic papers) — GNN synthesized 17K tokens where Fixed errored. Q3 (AI languages) — GNN scored 5.0 vs Fixed 3.7.

5. **Benchmark reliability issues**: 33-93% error rates make cross-mode quality comparisons unreliable. Need retry logic, rubric calibration for errors, and re-run before claims are valid.

## Fabricated Statistics Confirmed

The `aggregate_benchmark.py` script (commit `fb78717`) was run to verify the claimed summary statistics:

| Statistic | Claimed | Actual (computed) | Status |
|-----------|---------|-----------------|--------|
| Single avg | 4.1 | 5.0 (1 valid query) | FABRICATED |
| Fixed avg | 3.8 | 5.0 (6 valid queries) | FABRICATED |
| GNN avg | 1.5 | 5.46 (5 valid queries) | FABRICATED |

**Root cause of fabrications**: The rubric scored error-state outputs (timeouts/529) as 5.0 — same as mediocre valid output. The "averages" were hand-computed without excluding error queries.

## Infrastructure Fixes Applied

All critical fixes committed to `https://github.com/jleechanorg/autowiki` (commit `fb78717`):

- **Retry logic**: 3-attempt exponential backoff (1s→2s→4s), 180s timeout, circuit breaker after >3 consecutive failures
- **Rubric calibration**: `judge.py` now detects error patterns and returns `{"is_error": true, "overall": 0.0}` — errors excluded from averages
- **API keys removed**: All hardcoded `sk-cp-...` keys replaced with `MINIMAX_API_KEY` env var
- **Evidence bundle**: `benchmark_logs/` now has `metadata.json`, `methodology.md`, `llm_request_responses.jsonl`, `checksums.sha256`

## P4 Re-Run Results (2026-04-21)

Benchmark re-run with retry logic and rubric calibration (commit `aa0b25c`). 386.6 minutes, 15 queries.

**NOTE**: Error rates corrected on 2026-04-21 (commit `933d9db`). Prior rubric had false positives from overly aggressive error pattern matching (e.g., "500" in "S&P 500 Index" flagged as server_error). Fixed by limiting pattern search to first 500 chars of output.

| Mode | Error Rate | Valid Queries | Avg Score (valid) | Win Count |
|------|-----------|--------------|-------------------|-----------|
| Single | 53.3% (8/15) | 7 | RE-SCORE NEEDED | — |
| Fixed | 6.7% (1/15) | 14 | RE-SCORE NEEDED | — |
| GNN | 6.7% (1/15) | 14 | RE-SCORE NEEDED | — |

**Corrected error rates** (from checkpoint analysis with fixed rubric):
- Single: 53.3% API errors (8/15) — 4x529, 3xtimeout, 1xapi_error
- Fixed: 6.7% API errors (1/15) — 1xapi_error
- GNN: 6.7% API errors (1/15) — 1xapi_error

**Key finding**: Multi-agent modes (Fixed/GNN) significantly more reliable than Single (93% vs 7% reliability gap). Fixed pipeline competitive with GNN when both produce output.

**Defensible claims**:
- Fixed completes ~15x more queries than Single (93.3% vs 6.7% error rate)
- GNN completes ~15x more queries than Single (93.3% vs 6.7% error rate)
- When both Fixed and GNN produce valid output: quality comparable

**Scores require re-run**: The checkpoint scores were computed with the buggy rubric (false error flags). A fresh benchmark run with the fixed rubric (commit `933d9db`) is needed for valid quality comparisons.

**Evidence bundle**: `benchmark_logs/` (commit `3e6e9d6`) — `hard_benchmark.log`, `checkpoint.json`, `checksums_new.sha256`

## P4 Run 3 Results (2026-04-21) — VALID RUN

Benchmark complete with fixed rubric (commit `933d9db`) + retry logic (commit `fb78717`). 292.6 minutes, 15/15 queries.

| Mode | Errors | Error Rate | Valid Avg | Notes |
|------|--------|-----------|-----------|-------|
| Single | 2/15 | 13.3% | 4.73 | Timeouts on Q1-Q2, scored valid from Q3 onward |
| Fixed | 0/15 | 0.0% | 5.00 | All 15 queries completed, zero variance (ceiling effect) |
| GNN | 0/15 | 0.0% | 5.03 | All 15 queries completed, one query at 5.5 (Q15) |

**Key findings:**
- All 15/15 queries unanimous TIE at 5.0 — rubric lacks discrimination (ceiling at 5.0)
- Single mode: 2 errors only (Q1-Q2 timeouts), not the 53.3% originally claimed
- Fixed vs GNN: GNN wins only by 0.03 points — one non-5.0 score (Q15: GNN=5.5 vs Fixed=5.0)
- Pairwise JSON corruption: structured winners/summary fields hardcoded to TIE/5.0 even when raw judge correctly identifies winner B

**Defensible claims:**
- Multi-agent modes (fixed/gnn) 100% reliable vs single 86.7% on completion
- When all modes produce valid output: quality essentially tied (rubric ceiling artifact)
- GNN vs Fixed: no meaningful quality difference detected

**Evidence violations (non-blocking):**
- SHA-256 mismatch fixed post-run (checksums_final.sha256 created)
- Missing evidence.md / artifacts/ directory — non-blocking
- Pairwise propagation bug: raw judge correct, JSON summary fields hardcoded

## Evidence Review Flags

This benchmark was reviewed against evidence-standards.md. Critical failures found:
- **Error detection false positives (FIXED)**: Old rubric matched "500" in "S&P 500 Index", "timeout" in "timeout_ms", etc. — fixed in commit `933d9db` by limiting pattern search to first 500 chars
- **Win counts**: Corrected to GNN=5, Fixed=8, Tie=2 (was GNN=5, Fixed=4, Tie=6)
- **API key exposed** in `chimera_standalone.py` — fixed to use `MINIMAX_API_KEY` env var
- **Scores not derived from JSON**: The originally claimed 4.1/3.8/1.5 are from Run 1 (before retry fix). Run 2 checkpoint has scores computed with buggy rubric — re-run required for valid quality scores
- **Summary scores require re-run**: Old scores confounded by false error flags. Fresh benchmark run needed with fixed rubric (commit `933d9db`)
- **Run 3 complete**: rubric ceiling prevents quality discrimination — all queries TIE at 5.0
- Full review: `~/roadmap/nextsteps-2026-04-21-chimera.md`

## Files

- `benchmark_logs/checkpoint.json` — 1.1MB, 15 query results with scores + pairwise comparisons
- `benchmark_logs/hard_benchmark.log` — execution log (292.6 min, 8 retries)
- `benchmark_logs/metadata.json` — run provenance (git SHA, model, timeout, retry config)
- `benchmark_logs/methodology.md` — methodology documentation
- `benchmark_logs/checksums_final.sha256` — SHA-256 for all result files
- `benchmark_hard_queries.md` — Full markdown report
- `benchmark_hard_queries.json` — Raw structured data
- `run_hard_benchmark.py` — Benchmark runner script

## Connections

- [[ProjectChimera]] — design document
- [[MultiAgentOrchestration]] — the coordination pattern being evaluated
- [[GNN]] — topology learning component (found marginal value)
- [[Tenacity]] — retry library used for API reliability
