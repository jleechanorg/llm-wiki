---
title: "Mergeability drift + CodeRabbit rate-limit cosmetic success (2026-07-10)"
type: source
tags: [pr-workflow, ci, merge-conflicts, coderabbit, swarm, adversarial-review]
date: 2026-07-10
source_file: raw/feedback_2026-07-10_mergeability_drift_and_coderabbit_ratelimit.md
---

## Summary
During the PR #8312/#8268 green-drive (worldarchitect.ai), PR #8268 — verified `mergeable=MERGEABLE, mergeStateStatus=CLEAN` at 10:02Z — silently flipped CONFLICTING at 12:19Z when same-author sibling PR #8310 merged to main editing the exact same `.github/workflows/test.yml` checkout lines. Separately, CodeRabbit's check-run reported `conclusion=success` while its `output.summary` read "Skipped - Review rate limited" (account-wide, ~18h). A 9-agent swarm adversarially refuted all 5 of its own tooling-based fix proposals with live repo evidence, reframing the failure class as same-account concurrent-session collision — invisible to all standard multi-contributor tooling.

## Key Claims
- Mergeability is a live, base-branch-dependent computation recomputed asynchronously by GitHub; any "/green" or "ready to merge" claim is a snapshot that expires — re-fetch `mergeable`/`mergeStateStatus` before every claim, repeat, or merge action, and report with SHA + UTC timestamp.
- Merge conflicts from post-verification base drift are routine, not an escalation event: resolve autonomously (rebase, take the correct side of mechanical collisions, reapply own changes) and report afterward.
- CodeRabbit check-run `conclusion` can be cosmetic; the ground truth is `output.summary` — a rate-limited skip still posts `success`.
- Same-author concurrent-session PR collisions bypass CODEOWNERS (per-PR isolation), pr-conflict-detector bots (hard-coded same-author exclusion), and GitHub merge queues (repo had zero required status checks to gate on).
- merge_train (`conflict-warn-pre-tool.sh`) is a write-time guard by design — it cannot and is not meant to catch post-merge base drift.

## Key Quotes
> "Result: Skipped - Review rate limited" — CodeRabbit check-run output.summary, under `conclusion: "success"`, both PRs

> "same-author exclusion... the tool structurally would never have alerted on this exact case" — codex adversarial verdict killing the pr-conflict-detector proposal

## Connections
- [[7-Green-Proof-Artifact]] — Gate 2 (no conflicts) now requires fresh re-verification at every claim, never cached values
- [[CodeRabbitDismissedPattern]] — sibling CodeRabbit-status-misreading failure class
- [[swarm-orchestration-pattern]] — the 9-agent research/brainstorm/adversarial-verify workflow that refuted its own proposals
- [[GitHubActionsReusableWorkflowConcurrencyCollision]] — same file (test.yml) as a recurring collision hotspot
