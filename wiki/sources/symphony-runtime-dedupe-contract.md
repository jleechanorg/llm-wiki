---
title: "Symphony Runtime Dedupe Contract"
type: source
tags: [symphony, daemon, deduplication, runtime, openclaw]
sources: []
source_file: "raw/symphony-runtime-dedupe-contract.md"
last_updated: 2026-04-07
---

## Summary
Defines the contract for retaining local extensions (plugins, benchmarks, dispatch scripts) while enabling runtime deduplication in Symphony daemon. Establishes explicit non-goals to prevent feature creep and documents rollback procedures.

## Key Claims
- **Local plugin input shaping retained**: `prepare-symphony-payload.py` and `symphony_plugins.py` remain local as repository-specific curation layers
- **Benchmark catalogs retained**: `leetcode_hard_5.json` and `swe_bench_verified_5.json` stay local as curated benchmark sets
- **Stable dispatch wrapper**: `sym-dispatch.sh` retained as local wrapper for freeform text and plugin payload dispatch
- **Explicit non-goals**: No runtime `WORKFLOW.md` generation, no policy expansion at daemon bootstrap, no default `memory_tracker_issues` RPC enqueue for non-benchmark dispatch

## Key Quotes
> "These are retained because they are repository-specific curation layers, not Symphony runtime primitives."

## Connections
- [[Genesis]] — orchestration layer that Symphony extends
- [[OpenClaw]] — parent system for daemon operations

## Contradictions
- None identified
