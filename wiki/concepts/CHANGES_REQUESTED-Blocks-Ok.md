---
title: "CHANGES_REQUESTED Blocks Ok Unconditionally"
type: concept
tags: [jeffrey, oracle, PR-review, review-workflow]
sources: [jeffrey-oracle]
last_updated: 2026-04-10
---

A CodeRabbit or human `CHANGES_REQUESTED` verdict blocks an "ok" verdict unconditionally, even when all other oracle checks pass (CI green, minimal changes, caller verified, body matches diff). The PR must be re-reviewed after the requested changes are resolved before it can be approved. This rule applies to OPEN PRs — merged PRs with outstanding change requests are already blocked from merging by the review process itself.

The rationale is straightforward: a reviewer who found something worth requesting changes on has identified a real issue. Approving a PR while a CHANGES_REQUESTED is outstanding means skipping the review resolution step, which violates the principle that code review comments must be resolved before claiming done. Jeffrey iterates until satisfied and moves on only after all review gates are cleared.

This pattern was observed across batches 4, 5, and 6: PR #6177 had its "ok" verdict blocked by an active CHANGES_REQUESTED despite passing other checks, PR #6187 was rejected on multiple grounds including an active CHANGES_REQUESTED, and the oracle repeatedly states that CHANGES_REQUESTED unconditionally blocks "ok" until resolved and re-reviewed. [[jeffrey-oracle]]
