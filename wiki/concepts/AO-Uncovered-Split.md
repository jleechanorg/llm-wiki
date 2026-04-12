---
title: "AO Uncovered vs Blocked Split"
type: concept
tags: [agent-orchestrator, claims, coverage, blocked, uncovered]
last_updated: 2026-04-09
---

AO coverage checks were flattening blocked claim attempts into plain `UNCOVERED`. After surfacing `lifecycle.backfill.claim_failed` entries, the live picture changed: PRs are actually blocked, not uncovered.

## Problem

Coverage check output shows `UNCOVERED` for PRs that are actually blocked by legitimate blockers like `Workspace has uncommitted changes`. These need different handling.

## Legitimate Blockers

- `Workspace has uncommitted changes` — worktree dirty
- `claim_failed` entries — claim attempt failed, needs review

## Fake Uncovered

Fetch-stage stale-worktree failure now self-heals in local `scm-github`. Don't treat as permanent uncovered.

## Pattern

PRs #389, #394, and #396 were all `UNCOVERED` but actually blocked by workspace state.

## Connections

- [[AO-Claim-Fail-Closed]] — AO claim fail-closed
- [[AO-Blocker-Matrix]] — PR blocker triage
- [[AO-Split-Brain]] — AO split-brain
