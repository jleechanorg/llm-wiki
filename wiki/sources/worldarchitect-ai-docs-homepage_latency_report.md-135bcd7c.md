---
title: "Homepage Latency Optimization Report"
type: source
tags: [worldarchitect-ai, performance, latency, optimization, firestore]
sources: [worldarchitect-ai]
date: 2026-01-29
source_file: raw/homepage_latency_report.md
last_updated: 2026-04-07
---

## Summary
PR #4181 implements two key optimizations to reduce WorldArchitect.AI homepage and game page latency: Field Selection reduces campaigns list payload by 99% (1,349KB → 14KB), and Parallel I/O executes 4 Firestore queries concurrently achieving 26% faster game page load (1,261ms → 938ms).

## Key Claims
- **Field Selection**: Campaigns list fetches only 5 display-relevant fields instead of entire document, reducing response size by **99%** (1,349KB → 14KB)
- **Parallel I/O**: Game page loads 4 Firestore queries concurrently (campaign metadata, story, settings, game state), improving latency by **26%** (1,261ms → 938ms)
- **True Cold Start**: Improved by 18% (802ms → 655ms) for campaigns list
- **Theoretical vs Measured**: Parallel I/O theoretical improvement was 395ms, measured improvement was 323ms (30% theoretical vs 26% measured)

## Key Quotes
> "Response size reduced by **98x** (1,349KB → 14KB)" — Field Selection result
> "TOTAL (parallel max): 926ms" — Compared to sequential sum of 1,321ms

## Connections
- [[WorldArchitect.AI]] — the project being optimized
- [[Firestore]] — database service where optimizations were applied
- [[GitHub Development Statistics]] — other WorldArchitect.AI performance metrics

## Contradictions