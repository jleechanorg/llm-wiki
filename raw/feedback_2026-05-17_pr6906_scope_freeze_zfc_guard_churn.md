---
name: PR6906 scope freeze before ZFC guard churn
description: Freeze or split a level-up/ZFC PR once backend correction guards, evidence reruns, and review-thread fixes start replacing the original prompt-first scope.
type: feedback
bead: rev-46450
---

# PR6906 Scope Freeze Before ZFC Guard Churn

On 2026-05-17, PR https://github.com/jleechanorg/worldarchitect.ai/pull/6906 had grown to current head `c7de608fcb4d8b7039dcaab43202c21bc64ce5b4`, 49 files, and +4311/-767. The original prompt-first level-up planning/modal cleanup had expanded into retained backend correction guards, opaque choice-ID migration planning, testing harness work, CI changes, generated docs, and repeated evidence reruns.

Durable lesson: freeze or split a level-up/ZFC PR once retained backend semantic guards and guard-asserting tests start replacing the original prompt/schema scope. The current PR should carry only the smallest prompt/schema/root-cause fix and deletion of proven-unneeded guards. Opaque choice migration, guard-removal telemetry, harness gates, and CI/doc automation belong in separate follow-up PRs.

References: PR #6906, head `c7de608fcb4d8b7039dcaab43202c21bc64ce5b4`, evidence path `/tmp/worldarchitect.ai/worktree_level_choices/pr6906_guard_proof/iteration_001/metadata.json` anchored at `853cca3261287cba866d75a1719204a24687aad9`, bead `rev-46450`.

Does not affect `[[jeffrey-oracle]]`; this is workflow and architecture discipline.
