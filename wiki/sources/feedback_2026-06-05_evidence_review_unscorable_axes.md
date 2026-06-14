---
title: "Evidence Review — Unscorable Axes Anti-Pattern (2026-06-05)"
type: source
tags: [dark-factory, evidence-review, unscorable-axes, aggregator, ab-benchmark]
date: 2026-06-05
source_file: raw/feedback_2026-06-05_evidence_review_unscorable_axes.md
bead: jleechan-g8m
---

## Summary
An evidence review of dark-factory PR #16 (workflow_graphgen n=10 null + dynamic_fanout calibration) found an anti-pattern: a synthesis prose line claimed "no separation on any axis" while the aggregate JSON's `graph_quality` was `n=0 / insufficient data` for both features — a **structurally mode-invariant** axis (shared graph-IR, same fit score). The aggregator was honest; the one-line summary outran it. Verdict was PASS (first-party + independent evidence-reviewer agreed; suite 226 green).

## Key Claims
- A null on an axis that *cannot* separate by construction is **zero evidence of equivalence** — it's a non-measurement.
- When reporting "no separation on any axis," **partition axes into {measured-and-tied} vs {unscorable / structurally invariant}** and exclude the latter from "any."
- Precise claim here = "no separation on every *measured* axis (4/5); the 5th is unscorable by construction."
- Trust the aggregator's `insufficient data` / `winner=null` distinction; never let a prose roll-up erase it.
- A "true negative" claim requires the **same instrument** crediting a winner elsewhere. dynamic_fanout proved the ruler isn't blind by importing the literal same `benchmarks.workflow_graphgen.scoring.aggregate` (grep the import) and crediting 4 winners.
- Distinguish real metering from a model: dynamic_fanout tokens are a deterministic **call-count model** (disclosed in RESULTS.md), NOT billing — that disclosure is what keeps it honest, not a defect.
- State the negative space: ranges overlap at n=10 → not credited; non-adjacent state threading still needs a 1-line engine change.

## Key Quotes
> "A null on an axis that *cannot* separate by construction is zero evidence of equivalence — it's a non-measurement."

> "Trust the aggregator's `insufficient data` / `winner=null` distinction; never let a prose roll-up erase it."

## Connections
- [[project_2026-06-05_dynamic_fanout_calibration]] — the calibration that proved the ruler isn't blind
- [[project_2026-06-04_workflow_graphgen_spec]] — the n=10 null being reviewed
- [[EvidenceReview]] — /er command and methodology
- [[RangeNonOverlapAggregator]] — the shared scoring instrument
- [[DarkFactory]] — repo context
- [[StructureInvariantAxis]] — the new concept this surfaces
- [[AggregateJSONHonestProseNotHonest]] — anti-pattern of prose outrunning JSON
- [[WeakestLinkFirstArtifactCheck]] — heuristic for null-claim verification
