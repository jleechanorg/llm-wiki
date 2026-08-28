---
title: "Mergeability drift + CodeRabbit rate-limit cosmetic success (2026-07-10, confirmed 2026-08-27)"
type: source
tags: [pr-workflow, ci, merge-conflicts, coderabbit, swarm, adversarial-review]
date: 2026-07-10
source_file: raw/feedback_2026-07-10_mergeability_drift_and_coderabbit_ratelimit.md
last_updated: 2026-08-27
---

## Summary
During the PR #8312/#8268 green-drive (worldarchitect.ai), PR #8268 — verified `mergeable=MERGEABLE, mergeStateStatus=CLEAN` at 10:02Z — silently flipped CONFLICTING at 12:19Z when same-author sibling PR #8310 merged to main editing the exact same `.github/workflows/test.yml` checkout lines. Separately, CodeRabbit's check-run reported `conclusion=success` while its `output.summary` read "Skipped - Review rate limited" (account-wide, ~18h). A 9-agent swarm adversarially refuted all 5 of its own tooling-based fix proposals with live repo evidence, reframing the failure class as same-account concurrent-session collision — invisible to all standard multi-contributor tooling.

## Key Claims
- Mergeability is a live, base-branch-dependent computation recomputed asynchronously by GitHub; any "/green" or "ready to merge" claim is a snapshot that expires — re-fetch `mergeable`/`mergeStateStatus` before every claim, repeat, or merge action, and report with SHA + UTC timestamp.
- Merge conflicts from post-verification base drift are routine, not an escalation event: resolve autonomously (rebase, take the correct side of mechanical collisions, reapply own changes) and report afterward.
- CodeRabbit check-run `conclusion` can be cosmetic; the ground truth is `output.summary` — a rate-limited skip still posts `success`.
- Same-author concurrent-session PR collisions bypass CODEOWNERS (per-PR isolation), pr-conflict-detector bots (hard-coded same-author exclusion), and GitHub merge queues (repo had zero required status checks to gate on).
- merge_train (`conflict-warn-pre-tool.sh`) is a write-time guard by design — it cannot and is not meant to catch post-merge base drift.

## Confirmation (2026-08-27, PR #9458)
The same pattern recurred seven weeks later on a different PR: #9458 was independently approved and `MERGEABLE` at SHA `255c3cb1a239586ef06965077adfa733905ffe14`. Immediately before the authorized merge, a fresh `gh pr view` showed `mergeable=CONFLICTING, mergeStateStatus=DIRTY` — `main` had advanced over the same `.github/workflows/test.yml` block again. The explicit GitHub update-branch REST request made to bring the branch up to date is non-rewriting (it merges base into head rather than rebasing), so it correctly failed closed with HTTP 422 instead of silently forcing a stale merge. The branch merged current `origin/main` normally; the only conflict retained main's string-valued checkout expression (avoiding a falsy-numeric-zero trap). Post-resolution: 488 tests + 84 subtests passed, an independent reviewer approved the resolution, and the PR squash-merged as `16e229ced580b5eca6e50f39825bcb423b9787c1`.

This is a second independent confirmation of the core rule: refresh live mergeability immediately before the merge call, even after exact-head review approval — an earlier `/ready` or `/green` snapshot is never durable merge authorization evidence.

## Key Quotes
> "Result: Skipped - Review rate limited" — CodeRabbit check-run output.summary, under `conclusion: "success"`, both PRs

> "same-author exclusion... the tool structurally would never have alerted on this exact case" — codex adversarial verdict killing the pr-conflict-detector proposal

## Connections
- [[7-Green-Proof-Artifact]] — Gate 2 (no conflicts) now requires fresh re-verification at every claim, never cached values
- [[CodeRabbitDismissedPattern]] — sibling CodeRabbit-status-misreading failure class
- [[swarm-orchestration-pattern]] — the 9-agent research/brainstorm/adversarial-verify workflow that refuted its own proposals
- [[GitHubActionsReusableWorkflowConcurrencyCollision]] — same file (test.yml) as a recurring collision hotspot
- [[GitHubUpdateBranchNonRewritingSafety]] — the fail-closed HTTP 422 mechanism that protected PR #9458 from a stale merge during the 2026-08-27 recurrence
