---
title: "Chimera P14 Benchmark Findings"
type: source
tags: [chimera, benchmark, gnn, fixed, 2-mode]
date: 2026-04-24
source_file: chimera_p14_findings.md
---

## Summary
Project Chimera P14 benchmark tested 2 modes (GNN 3-perspective, Fixed with verification) across 15 queries using the 20-anchor behavioral rubric. **Fixed wins with 6.20 mean and 9/15 pairwise wins.** GNN scores 5.53 mean (3/15 wins). This is the **opposite result of P13**, where GNN won (6.73 vs 6.16).

## Key Finding: Mode Advantage Reverses

| Mode | P13 Score | P13 Wins | P14 Score | P14 Wins |
|------|-----------|----------|-----------|----------|
| **GNN** | 6.73 | 7/15 | 5.53 | 3/15 |
| **Fixed** | 6.16 | 6/15 | 6.20 | 9/15 |

**Implication:** Neither GNN nor Fixed is universally superior. Mode performance is query-dependent. GNN's advantage may be specific to certain query types (complexity, domain) or random variation.

## Score Distribution

| Query | GNN | Fixed | Winner |
|-------|-----|-------|--------|
| Q1 | 4.0 | 10.0 | Fixed |
| Q2 | 8.8 | 4.0 | GNN |
| Q3 | 9.6 | 4.0 | GNN |
| Q4 | 7.2 | 7.2 | Tie |
| Q5 | 4.0 | 6.8 | Fixed |
| Q6 | 7.0 | 9.5 | Fixed |
| Q7 | 6.8 | 9.5 | Fixed |
| Q8 | 9.5 | 7.0 | GNN |
| Q9 | 4.2 | 4.26 | Fixed |
| Q10 | 4.0 | 4.0 | Tie |
| Q11 | 4.0 | 7.1 | Fixed |
| Q12 | 4.0 | 5.8 | Fixed |
| Q13 | 4.0 | 5.8 | Fixed |
| Q14 | 4.0 | 4.0 | Tie |
| Q15 | 1.8 | 4.0 | Fixed |

## Bug Fix Applied

- Q9 Fixed had invalid score 99.99 (LLM judge returned out-of-range value)
- Fixed by capping parsed scores at 10.0 in run_query_p14.py
- P13 Q9 had the same bug (13.0 → capped at 9.5)

## Cross-Iteration Summary

| Iteration | Winner | Score | Modes Tested |
|-----------|--------|-------|--------------|
| P10 | Single | 6.73 | single, fixed, gnn |
| P11 | Cascade | 5.52 | single, fixed, gnn, cascade |
| P12 | Single | 7.98 | single, fixed, gnn, cascade, ensemble |
| P13 | GNN | 6.73 | single, fixed, gnn, cascade, hybrid |
| P14 | **Fixed** | **6.20** | **gnn, fixed** |

**Conclusion:** No mode is universally superior. Query complexity and domain determine which architecture works best.

## Connections
- [[Chimera P13 Benchmark Findings]] — P13 had GNN win; P14 has Fixed win
- [[SelfRefine]] — Fixed mode uses critique+verify; GNN uses multi-perspective aggregation
- [[Process Reward Models]] — Fixed's verification step is PRM-light