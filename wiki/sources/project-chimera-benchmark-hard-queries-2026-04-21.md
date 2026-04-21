---
title: "Project Chimera Benchmark: Hard Queries (281 min)"
type: source
tags: [multi-agent-systems, benchmark, gnns, minimax, llm-orchestration]
sources: [project-chimera-neural-network-llm-agents-2026-04-19, project-chimera-codebase-2026-04-20]
last_updated: 2026-04-21
---

## Summary

15 hard research queries × 3 Chimera modes (single/fixed/GNN) run on real Minimax M2.7 API over 281 minutes. Real spread achieved: multi-agent modes outperform single mode on complex queries by avg 3.62 points. GNN edges Fixed by only 0.3 pts — dynamic topology adds marginal value over a well-designed static pipeline.

## Key Claims

- **Single mode scores 1.0/10 on 10/15 hard queries** — completely fails on complex multi-perspective tasks requiring synthesis of conflicting information
- **Multi-agent is mandatory for hard queries**: 13/15 queries show spread > 1.0 point between modes
- **GNN vs Fixed is essentially tied**: GNN (4.1 avg) vs Fixed (3.8 avg) — dynamic topology routing doesn't add significant value over parallel execution + critique loops
- **Average spread: 3.62 points** — rubric now discriminating properly on hard queries (vs 0.4 on easy queries)

## Mode Averages

| Mode | Avg Score | Wins | Win Rate |
|------|----------|------|----------|
| GNN | 4.1/10 | 5 | 33% |
| Fixed | 3.8/10 | 4 | 27% |
| Single | 1.5/10 | 0 | 0% |
| Tie | — | 6 | 40% |

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

1. **Single mode is a brittle baseline**: Scores 1.0/10 on 10/15 queries. Concise, well-structured output looks good to AI Judge on simple queries but falls apart on complex synthesis tasks.

2. **GNN topology routing ≠ multi-agent collaboration**: The GNN mode's advantage comes from parallel execution + multiple expert perspectives, not from smart topology selection. Fixed pipeline is nearly as good.

3. **When multi-agent pays off**:
   - Queries requiring synthesis of conflicting information (Q7: academic papers)
   - Queries needing domain-specific deep analysis (Q3: AI languages, Q11: fusion)
   - Queries requiring multiple technical perspectives (Q8: due diligence, Q9: architecture)

4. **When modes tie**: High-level analytical queries (Q2: geopolitical) and structured analytical tasks (Q15: election) where single synthesizer produces adequate output.

## Files

- `benchmark_hard_queries.md` — Full markdown report
- `benchmark_hard_queries.json` — Raw structured data
- `benchmark_logs/hard_benchmark.log` — Execution log (281 min)
- `run_hard_benchmark.py` — Benchmark runner script

## Connections

- [[ProjectChimera]] — design document
- [[MultiAgentOrchestration]] — the coordination pattern being evaluated
- [[GNN]] — topology learning component (found marginal value)
