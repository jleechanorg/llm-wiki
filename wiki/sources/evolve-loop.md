---
title: "Evolve Loop (/eloop)"
type: source
tags: [autonomy, evolution, ao, zero-touch, diagnostic]
sources: []
last_updated: 2026-04-14
---

## Summary

Autonomous evolution loop that observes AO ecosystem, measures zero-touch rate, diagnoses friction, and dispatches fixes. Adaptive — skips phases when system is healthy.

## Key Claims

- Adaptive loop: Not every phase runs every cycle
- If all workers alive and PRs progressing -> just report status and wait
- If zero-touch rate unchanged and no new friction -> skip diagnose/fix phases
- Only run /harness, /nextsteps, /claw when there's a NEW problem to solve
- Always measure (Phase 2) and always recap (Phase 7)
- Run via /loop 10m /eloop (every 10min, max 12h) or single cycle with /eloop

## Connections

- [[Auton]] — Autonomy diagnostic
- [[HarnessEngineering]] — Fix dispatch
- [[Claw]] — Agent dispatch for fixes

## Contradictions

- None identified
