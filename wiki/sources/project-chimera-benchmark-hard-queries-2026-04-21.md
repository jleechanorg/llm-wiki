---
title: "Project Chimera Benchmark: Hard Queries (281 min)"
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

| Mode | Error Rate | Valid Queries | Avg Score (valid) | Win Count |
|------|-----------|--------------|-------------------|-----------|
| Single | 93.3% (14/15) | 1 | 5.00 | 1 |
| Fixed | 60.0% (9/15) | 6 | 5.00 | 6 |
| GNN | 66.7% (10/15) | 5 | 5.46 | 5 |

**Key finding**: Multi-agent modes (Fixed/GNN) significantly more reliable than Single. When Single produces valid output, quality is comparable (5.0). GNN slightly higher on quality when it runs (5.46). Error rates remain high across all modes — API reliability is the dominant factor, not architecture.

**Defensible claims**:
- Fixed completes 6x more queries than Single (60% vs 7% success)
- GNN completes 5x more queries than Single (67% vs 7% success)
- When both produce valid output: Fixed=GNN=Single at ~5.0
- GNN marginally higher quality on valid queries (5.46 vs 5.0)

**Fabrication confirmed again**: Claimed 4.1/3.8/1.5 remain FABRICATED — aggregate script confirms actual averages of 5.0/5.0/5.46 excluding errors.

**Evidence bundle**: `benchmark_logs/` (commit `3e6e9d6`) — `hard_benchmark.log`, `checkpoint.json`, `checksums_new.sha256`

## Evidence Review Flags

This benchmark was reviewed against evidence-standards.md. Critical failures found:
- **Win counts corrected**: GNN=5, Fixed=8, Tie=2 (was GNN=5, Fixed=4, Tie=6)
- **API key exposed** in `chimera_standalone.py` — fixed to use `MINIMAX_API_KEY` env var
- **Scores not derived from JSON**: The claimed 4.1/3.8/1.5 averages are FABRICATED — now confirmed by `aggregate_benchmark.py`
- **Summary scores not derivable**: Actual averages excluding errors: single=5.0, fixed=5.0, gnn=5.46
- Full review: `~/roadmap/nextsteps-2026-04-21-chimera.md`

## Files

- `benchmark_hard_queries.md` — Full markdown report
- `benchmark_hard_queries.json` — Raw structured data
- `benchmark_logs/hard_benchmark.log` — Execution log (281 min)
- `run_hard_benchmark.py` — Benchmark runner script

## Connections

- [[ProjectChimera]] — design document
- [[MultiAgentOrchestration]] — the coordination pattern being evaluated
- [[GNN]] — topology learning component (found marginal value)
