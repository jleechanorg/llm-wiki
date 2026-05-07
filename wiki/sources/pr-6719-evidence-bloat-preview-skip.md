---
title: "PR 6719 Evidence Bloat Skipped Preview Deploy"
type: source
tags: [worldarchitect, ci, evidence, preview-deploy, level-up]
date: 2026-04-30
source_file: raw/feedback_2026-04-30_pr_6719_evidence_bloat_preview_skip.md
---

## Summary

PR 6719 became hard to merge because generated evidence and design-doc churn expanded the change set to 430 files, pushing production files beyond GitHub's path-filter evaluation window. The preview deploy workflow did not run for the final PR head even though production files changed, and Layer 3/Layer 4/Skeptic evidence became stale whenever follow-up commits advanced the SHA.

The durable lesson is process-level: keep evidence bundles out of large production PRs where possible, provide a manual preview deploy escape hatch, and freeze the PR SHA before expensive evidence and skeptic review. For debugging claims, verify the actual remote head and definitions, not just search hits.

## Key Claims

- GitHub `pull_request.paths` filtering only considered the first 300 changed files; PR 6719's first preview-triggering files were past that window.
- A successful preview run at an older SHA did not prove the final PR head was deployed.
- Stale Layer 3/Layer 4 evidence cannot prove a newer production head.
- `rg` hits for `_planning_has_level_up_choices` call sites were not enough to prove a `NameError`; the current remote head had module-level aliases.
- Current-head TDD fixed the stale level-up projection bugs in commit `ecca6c5f40c1a68abdd7db4ed23551cff51db372`.

## Key Quotes

> "Large generated evidence/doc bundles can hide deploy-triggering files beyond GitHub's path-filter window; freeze SHA before evidence and keep preview deploy manually runnable."

> "Did not treat `rg` call-site hits as proof of a `NameError`; checked module-level aliases at the actual remote SHA."

## Connections

- [[WorldArchitectAI]] - PR 6719 was a WorldArchitect.AI level-up/rewards merge.
- [[GitHubActions]] - Preview deploy skipped because of `pull_request.paths` filtering behavior.
- [[GitHubPathFilterWindow]] - Captures the 300-file path-filter failure mode.
- [[EvidenceShaFreeze]] - Captures the evidence-current-head requirement.
- [[EvidenceBundles]] - Evidence artifacts must be tied to the current commit, not just the PR.
- [[SkepticGate]] - Gate verdicts are SHA-specific and must be rerun after new commits.
- [[LevelUpStaleFlagGuards]] - The production bug class fixed by the PR 6719 TDD follow-up.
