---
title: "workflow_graphgen Spec + Benchmark IMPLEMENTED (PR #16)"
type: source
tags: ["dark-factory", "benchmark", "workflow-graphgen", "pr-16"]
date: 2026-06-04
source_file: project_2026-06-04_workflow_graphgen_spec.md
---

## Summary
workflow_graphgen feature IMPLEMENTED + smoke-run done on `feat_workflow-graphgen-benchmark` (unpushed). Real n=10 measurement = NO separation on ANY axis at n=10. PR #16 7-GREEN at HEAD `56bb22a`.

## Key Claims
- Mode A (runner walks every node) vs Mode A+B (Workflow runs dynamic middle via `agent()`, runner runs guaranteed-node tail)
- Spec status: cold-reviewer PASS at iteration 3; `specs/workflow_graphgen.md` + `benchmarks/attractor-spec-review/spec/workflow_graphgen.feature.md` (186/186 reviewable)
- Smoke: 4/4 records, 0 tracebacks, honest cache-inclusive tokens
- Real n=10: conformance 50/50 & 90/90 both modes (perfect tie), tokens_total ranges overlap, wall_ms A+B directionally slower but overlaps
- PR #16 7-GREEN at HEAD 56bb22a; 24 Bugbot/CR comments fixed across 7 push iterations

## Key Quotes
> dispatch path is irrelevant for tasks the model solves first-pass; does NOT generalize to fix-loop tasks (next experiment)

## Connections
- [[AttractorFourLayer]] — related spec
- [[CanonicalCodeScorer]] — scoring methodology
