---
title: "GitHub update-branch API is non-rewriting (fails closed on drift instead of forcing a stale merge)"
type: concept
tags: [github-actions, github-api, merge-conflicts, pr-workflow, ci]
date: 2026-08-27
last_updated: 2026-08-27
---

## Concept
GitHub's update-branch REST endpoint brings a PR's head up to date with its base by merging the base into the head rather than rewriting/rebasing the head. It is not something `gh pr merge` invokes automatically — the observed call was an explicit GitHub update-branch REST request made as part of the merge workflow. When the base has advanced over lines the head branch also touches, the API does not silently pick a side or force the merge — it fails closed with HTTP 422. This turns a potential silent-stale-merge bug into a visible, resolvable conflict.

## Why this matters
Without this behavior, a PR that was verified `MERGEABLE` moments earlier could be merged against an outdated base without anyone noticing — exactly the failure mode described in [[feedback-2026-07-10-mergeability-drift-and-coderabbit-ratelimit]] (mergeability drift). The 422 forces a human/agent-visible resolution step (rebase or merge current `origin/main` in) instead of compounding the drift.

## Observed instance
PR #9458 (worldarchitect.ai, 2026-08-27): approved and `MERGEABLE` at SHA `255c3cb1a2...`. Immediately before merge, `main` had advanced over the same `.github/workflows/test.yml` block (a recurring collision hotspot — see [[GitHubActionsReusableWorkflowConcurrencyCollision]]). The update-branch call correctly 422'd; the branch was merged against current main normally, and the resulting conflict retained main's string-valued checkout expression (avoiding a falsy-numeric-zero trap). Squash-merged as `16e229ced580b5eca6e50f39825bcb423b9787c1`.

## Operational implication
Treat the 422 as expected, routine behavior on any PR competing for the same CI-config lines as sibling PRs — not as a tooling failure. The correct response is the same as any base-drift conflict: resolve via normal history-preserving integration (rebase/merge current base), re-verify `mergeable`/`mergeStateStatus` fresh, then merge. Never treat a pre-drift `/ready` or `/green` snapshot as durable authorization to force a merge through the 422.

## Connections
- [[feedback-2026-07-10-mergeability-drift-and-coderabbit-ratelimit]] — the incident this concept was extracted from (second confirmation, PR #9458)
- [[GitHubActionsReusableWorkflowConcurrencyCollision]] — `.github/workflows/test.yml` as a recurring same-file collision hotspot
- [[7-Green-Proof-Artifact]] — Gate 2 (no conflicts) requires fresh re-verification at every claim
