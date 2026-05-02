---
title: "Chimera P13 Benchmark Findings"
type: source
tags: [chimera, benchmark, gnn, multi-agent, rubric]
date: 2026-04-23
source_file: chimera_p13_findings.md
---

## Summary
Project Chimera P13 benchmark tested 5 modes (Single, Fixed, GNN, Cascade, Hybrid) across 15 queries using a 20-anchor behavioral rubric. GNN (3-perspective architecture) wins with 6.73 mean and 7/15 pairwise wins. Fixed follows at 6.16 (6 wins). Hybrid fails structurally (5.24, 0 wins). Cross-iteration pattern confirms no mode universally dominates.

## Key Claims
- GNN 3-perspective architecture outperforms all other modes (6.73 mean, 7/15 wins)
- Hybrid's 0/15 wins indicates a structural design flaw, not statistical noise
- No mode universally wins across P10-P13 iterations — performance is query-dependent
- Rubric lacks gradient sensitivity; API errors are indistinguishable from mediocre output
- Mode selection should follow a decision tree based on query complexity and domain

## Key Quotes
> "The GNN allows perspectives to selectively reinforce or suppress each other's outputs based on learned graph structure over the reasoning trace" — research synthesis

> "Hybrid's arbiter faces conflicting signals from modes that were never trained to operate jointly" — second opinion analysis

## Connections
- [[SelfRefine]] — multi-aspect feedback iteration (Madaan et al., NeurIPS 2023)
- [[Process Reward Models]] — ORM vs PRM distinction (Lightman et al., BAIR 2023)
- [[CAMEL]] — multi-agent role-playing frameworks (Li et al., NeurIPS 2023)
- [[Chimera P10 Results]] — Single won at 6.73 (15-anchor v2)
- [[Chimera P12 Results]] — Single won at 7.98 (22-anchor actionability)