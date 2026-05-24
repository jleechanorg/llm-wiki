---
title: "Attractor Parallel Execution"
type: concept
tags: [attractor, parallel, fan-out, fan-in]
date: 2026-05-24
---

## Overview

Fan-out/fan-in parallel execution pattern for Attractor pipeline DOT graphs. Implemented in [[Kilroy]] and [[Smasher]]; notably absent from dark-factory, making it the only implementation without parallel execution.

## DOT Shapes

| Shape | Role | Used By |
|---|---|---|
| `component` | Fan-out — spawns parallel branches | [[Kilroy]] |
| `tripleoctagon` | Fan-in — waits for parallel branches and joins results | [[Kilroy]] |

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

## Why dark-factory Lacks This

dark-factory's engine (`runner/engine.py`) walks a single path from `start` to `exit` sequentially via `_edge_matches`. There is no mechanism to spawn concurrent branches or join their results. Adding parallel execution would require a fundamental engine redesign — from linear walk to DAG execution with concurrent node dispatch.

## Connections

- [[Kilroy]] — Go implementation with full fan-out/fan-in
- [[Smasher]] — Rust implementation with bounded parallel concurrency
- [[AttractorPattern]] — The pattern this extends