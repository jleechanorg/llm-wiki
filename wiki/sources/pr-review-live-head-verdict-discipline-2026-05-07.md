---
title: "PR review live-head verdict discipline"
type: source
date: 2026-05-07
tags: [pr-review, evidence, skeptic, worldarchitect, workflow]
source_file: raw/feedback_2026-05-07_pr_review_live_head_verdict_discipline.md
bead: rev-awmxd
---

# PR Review Live-Head Verdict Discipline

## Summary

PR review verdicts must be grounded in the current live PR head, not pasted
handoffs or older review artifacts. For
https://github.com/jleechanorg/worldarchitect.ai/pull/6818, the reviewed head
advanced to `2edcdabe3c7fa975ad69082eda9e988dd36cc533` after the latest
behavioral evidence bundle at
`64d4fa40ab94f96ae2519b5c3ef95bc007559543`.

The later delta was generated PR design docs only, so it did not create a
serious production-code blocker. The remaining concerns were strict green
process gaps: no same-SHA Skeptic `VERDICT: PASS` in the Green Gate log, and
stale evidence text in the PR body.

## Reusable Rule

Before answering "all issues fixed?", verify:

- Live `headRefOid`.
- Evidence bundle `git_head`.
- Whether commits after evidence touch runtime code or docs only.
- Green Gate logs for same-SHA Skeptic verdict behavior.
- PR evidence/body text when strict 7-green status is the question.

Answer code/product risk separately from process/provenance cleanup. A skipped
Skeptic verdict or stale PR body can block strict green without proving a serious
implementation defect.

## Related Concepts

- [[EvidenceShaFreeze]]
- [[EvidenceSkepticalReview]]
- [[SkepticGate]]

[[jeffrey-oracle]]: NO.
