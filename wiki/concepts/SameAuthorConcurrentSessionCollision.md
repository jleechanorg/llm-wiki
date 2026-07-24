---
title: "Same-Author Concurrent-Session Collision"
type: concept
tags: [pr-workflow, merge-conflicts, agent-orchestration, tooling-gaps]
date: 2026-07-10
---

# Same-Author Concurrent-Session Collision

Two PRs from the **same GitHub account** (e.g. concurrent Claude Code / AO worker sessions
operating as one identity) independently edit the same file region to fix the same underlying
pain point, then collide when the first merges to main — flipping the second from CLEAN to
CONFLICTING with zero action on its own branch.

## Why standard tooling cannot see it
- **CODEOWNERS review gates**: evaluate each PR in isolation; cannot surface that a sibling open PR already edited the same lines.
- **Conflict-detector bots** (e.g. github-community-projects/pr-conflict-detector): hard-coded same-author exclusions — built for multi-contributor conflicts, structurally silent here.
- **GitHub merge queues**: only re-validate at merge-attempt time, and only gate on required status checks (which may be empty); an approved-but-unmerged PR sitting idle is never re-validated.
- **Write-time conflict predictors** (merge_train): fire when the local session writes a file, not when a sibling PR merges to main later.

## Durable mitigation (behavioral, not tooling)
1. Treat every mergeability claim as an expiring snapshot: re-fetch `mergeable`/`mergeStateStatus` before every claim, repeat, or merge action; report with SHA + UTC timestamp.
2. Resolve resulting conflicts autonomously — mechanical same-fix collisions take the already-merged side and reapply own changes.
3. Before starting CI-infra work, check for sibling open PRs touching the same paths from the same account; treat a hit as a coordination event (single-writer rule), not two independent fixes.

## Provenance
2026-07-10 incident: PR #8268 vs PR #8310 (jleechanorg/worldarchitect.ai, `.github/workflows/test.yml` checkout fetch-depth block). A 9-agent swarm adversarially refuted all 5 tooling-based fixes with live repo evidence (172 open same-file PR pairs = alert noise; zero required status checks = nothing for a merge queue to gate on).

## Connections
- [[7-Green-Proof-Artifact]]
- [[swarm-orchestration-pattern]]
- Source: [[feedback-2026-07-10-mergeability-drift-and-coderabbit-ratelimit]]
