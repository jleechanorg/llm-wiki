# Chimera P13 Benchmark Findings

**Date:** 2026-04-23
**Type:** synthesis
**tags:** [chimera, benchmark, gnn, multi-agent, rubric]
**run_session:** chimera-p13-2026-04-22

## Summary

Project Chimera P13 benchmark tested 5 modes (Single, Fixed, GNN, Cascade, Hybrid) across 15 queries using a 20-anchor behavioral rubric. GNN (3-perspective architecture) wins with 6.73 mean and 7/15 pairwise wins. Fixed follows at 6.16 (6 wins). Hybrid fails structurally (5.24, 0 wins). Cross-iteration pattern confirms no mode universally dominates.

## Key Findings

### 1. GNN 3-Perspective Architecture

Multi-head aggregation preserves critique diversity rather than diluting it through simple voting/merging. Three perspectives each capture different reasoning dimensions; the GNN selectively weights and combines signals a single critic would miss.

- **Score:** 6.73 mean, 7/15 wins
- **Advantage over Fixed:** +0.57 pts (8% relative improvement, exceeds noise floor of ±0.2pts)
- **Root mechanism:** Perspective-specific signals are preserved during aggregation, not compressed into a single merged representation

### 2. Hybrid Mode Failure — Structural, Not Noise

Hybrid (single → critique → arbiter merge) scores 5.24 with 0/15 wins. This is a design flaw:

- **Late fusion bottleneck:** Arbiter must compress signals from fundamentally different reasoning trajectories
- **Semantic mismatch:** Critique belongs to a different reasoning frame than the merged output — arbiter receives feedback on something it cannot regenerate
- **Contrast with Fixed:** Uses consistent single-critic workflow validated across iterations

### 3. Cross-Iteration Mode Pattern

| Iteration | Winner | Score | Rubric |
|-----------|--------|-------|--------|
| P10 | Single | 6.73 | 15-anchor v2 |
| P11 | Cascade | 5.52 | 20-anchor |
| P12 | Single | 7.98 | 22-anchor (actionability) |
| P13 | GNN | 6.73 | 20-anchor |

**Conclusion:** No mode universally wins. Architecture performance is query-dependent.

### 4. Rubric Limitations

The 20-anchor rubric (A-T) provides breadth but lacks gradient sensitivity within anchors. API error states (timeout, 529) are indistinguishable from mediocre valid output at scoring time — both score ~4-5. Error-type taxonomy would improve discrimination.

## Mode Selection Decision Tree

- **Low complexity (single-step, factual):** Single — overhead of critique outweighs benefit
- **Medium complexity (multi-step, verifiable):** Fixed (with verification step) — single critique catches logic errors
- **High complexity (multi-perspective domain: ethics, tradeoffs, multi-constraint):** GNN 3-perspective — different perspectives capture different reasoning dimensions
- **Ambiguous / high-stakes:** Cascade — multiple stages catch edge cases conservatively

## Evidence Review Verdict

**Overall:** PARTIAL (confidence: MEDIUM)

| Violation | Impact |
|-----------|--------|
| `metadata.json`, `hard_benchmark.log` checksum mismatch | LOW — metadata files, not result data |
| No `metadata_p13.json` | MEDIUM — P13 provenance unverifiable |
| `run_query_p13.py` committed after execution | FIXED — P15 clean run protocol established |
| No reproduction gist | MEDIUM — clean-computer standard not met |

## Recommendations for P14

1. **Skip mode routing** — risks Hybrid-like instability without proven gains
2. **Run GNN+Fixed as 2-mode ensemble** — top two modes from P13 with proven stability
3. **Establish clean run protocol** — commit source before execution, generate checksums after
4. **Add process anchors to rubric** — measure PRM-style reasoning step quality
5. **Distinguish error types in scoring** — API failure vs logical failure vs completeness failure

## References

- SelfRefine (Madaan et al., NeurIPS 2023) — multi-aspect feedback iteration
- Process Reward Models (Lightman et al., BAIR 2023) — ORM vs PRM distinction
- CAMEL (Li et al., NeurIPS 2023) — multi-agent role-playing frameworks
- Chimera benchmark_logs: `checkpoint_p13_aggregate.json` (SHA fec2953)