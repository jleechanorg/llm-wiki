---
title: "Autonomy Diagnostic (/auton)"
type: source
tags: [autonomy, diagnostic, ao, zero-touch, pr-workflow]
sources: []
last_updated: 2026-04-14
---

## Summary

Diagnoses WHY the jleechanclaw + AO system is NOT autonomously driving PRs to 6 green and merged. Runs comprehensive diagnostics on infrastructure, session state, GitHub, rate limits, and autonomy metrics.

## Key Claims

- Measures zero-touch rate: PR is zero-touch ONLY if merged_by is github-actions[bot] (skeptic-cron auto-merge)
- Commit prefixes alone are insufficient — manual merges by humans are NOT zero-touch
- Stall detection: flags PRs >1hr gap not at 6-green
- Zombie detection: sessions on merged PRs waste tokens
- Skeptic-cron correctness spot-check: verifies gate checks agree with reality
- CHANGES_REQUESTED gap detection: flags CR_REQ PRs with no active worker session

## Key Diagnostic Outputs

- System health (poller, lifecycle-worker, orchestrator, workers, rate limits)
- Per-PR status with non-green reasons
- 6-Green rate (last 7 days): auto vs manual merge ratio
- Stalled PRs table
- Zombie sessions table

## Connections

- [[EvolveLoop]] — Adaptive evolution based on diagnostics
- [[HarnessEngineering]] — Fix dispatch for identified issues
- [[Claw]] — Spawn workers for coverage gaps

## Contradictions

- None identified
