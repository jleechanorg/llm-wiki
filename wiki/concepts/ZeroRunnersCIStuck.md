---
title: "ZeroRunnersCIStuck"
type: concept
tags: []
sources: []
last_updated: 2026-04-16
---

## Summary
Zero self-hosted runners are available online, causing all GitHub Actions CI (green-gate, skeptic-gate) to queue indefinitely. This is an infrastructure issue, not a code issue, and blocks all PRs from achieving 7-green.

## Impact
- All PRs with CI pending show: `mergeStateStatus: UNSTABLE` or `QUEUED`
- green-gate runs stuck
- skeptic-gate runs stuck
- No CodeRabbit reviews can be triggered (CR depends on CI webhooks)
- No tests can run

## Status
- Bead: br-pz6tp (P1) — Restore self-hosted runners for worldarchitect.ai
- No code fix possible — infrastructure restoration required

## How to Apply
When PR shows CI PENDING/QUEUED for >30min with no runners available, recognize this as an infrastructure blocker, not a code blocker. Do not attempt code fixes to "unstick" CI.
