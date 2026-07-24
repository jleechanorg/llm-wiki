---
title: "Attractor Parallel Execution"
type: concept
tags: [attractor, parallel, fan-out, fan-in]
date: 2026-05-24
---

## Overview

Fan-out/fan-in parallel execution pattern for Attractor pipeline DOT graphs. Implemented in [Kilroy](../entities/Kilroy.md) and [Smasher](../entities/Smasher.md); notably absent from dark-factory, making it the only implementation without parallel execution.

## DOT Shapes

| Shape | Role | Used By |
|---|---|---|
| `component` | Fan-out — spawns parallel branches | [Kilroy](../entities/Kilroy.md) |
| `tripleoctagon` | Fan-in — waits for parallel branches and joins results | [Kilroy](../entities/Kilroy.md) |

Smasher uses `futures::stream::buffer_unordered` with bounded concurrency instead of explicit fan-out/fan-in shapes.

## Join Policies

How fan-in nodes decide when to proceed:

| Policy | Behavior | Example Use |
|---|---|---|
| `wait_all` | Wait for ALL branches to complete | Merge review where all reviewers must finish |
| `first_success` | Proceed on first successful branch | Redundant API calls, take fastest response |
| `k_of_n` | Proceed when K of N branches succeed | Tolerate partial failures, need 2/3 reviewers |
| `quorum` | Proceed when majority succeed | Consensus-based decisions |

## Error Policies

How fan-in nodes handle branch failures:

| Policy | Behavior |
|---|---|
| `continue` | Ignore failures, proceed with successful branches |
| `fail_fast` | Terminate remaining branches on first failure |
| `ignore` | Silently drop failed branches |

## Historical Gap: dark-factory Lacked This

dark-factory's engine (`runner/engine.py`) walks a single path from `start` to `exit` sequentially via `_edge_matches`. There is no mechanism to spawn concurrent branches or join their results. Adding parallel execution would require a fundamental engine redesign — from linear walk to DAG execution with concurrent node dispatch.

## Update 2026-06-27 — reviewer-lane parallelization

dark-factory now uses `type="parallel_reviewer"` for redundant/independent reviewer lanes where appropriate. This is not a blanket DAG rewrite; it is a targeted reviewer-node parallelization that preserves the Attractor requirement that independent reviewers remain cold and separately logged.

Rule: parallelization is valid only when every reviewer lane keeps its own full output, transcript refs, outcome metadata, and hashes, and the downstream coder/fix node receives a combined free-form review bundle rather than a status-only token.

Source: [Dark Factory reviewer/output/evidence contract and deterministic install smoke](../sources/project-2026-06-27-dark-factory-reviewer-output-evidence-contract.md).

## Connections

- [Kilroy](../entities/Kilroy.md) — Go implementation with full fan-out/fan-in
- [Smasher](../entities/Smasher.md) — Rust implementation with bounded parallel concurrency
- [AttractorPattern](AttractorPattern.md) — The pattern this extends
