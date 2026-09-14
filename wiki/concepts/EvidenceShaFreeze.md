---
title: "Evidence SHA Freeze"
type: concept
tags: [evidence, ci, skeptic, provenance]
sources: [luna-integration-learning-2026-09-13, pr-6719-evidence-bloat-preview-skip, feedback-2026-05-01-pr6737-evidence-artifact-verification, pr-review-live-head-verdict-discipline-2026-05-07]
last_updated: 2026-09-13
---

## Summary

Evidence SHA freeze is the rule that expensive evidence, preview proof, and skeptic review must be generated against the exact commit that will be reviewed or merged. If production files change after evidence generation, the evidence is stale even when the tests were valid for the older commit.

PR 6737 adds the artifact-publication corollary: it is not enough for the operator to have run valid evidence locally. The PR body, release, gist, or linked bundle must expose the current-SHA artifacts reviewers will inspect.

## Failure Pattern

- Layer 3 or Layer 4 evidence records one `git_head`.
- Follow-up commits change production files.
- The PR still cites the old evidence as proof of the new head.
- Reviewers or gates correctly reject the evidence because it does not prove the current code.
- Public evidence artifacts are stale or incomplete even though local terminal output looked valid.

## Mitigations

- Freeze the PR head before Layer 3, Layer 4, and Skeptic evidence.
- Rerun evidence after any production commit.
- Include exact commit URLs and command output in PR evidence sections.
- Verify remote head before accepting worker claims about current-state bugs.
- Verify the public PR/release/gist artifacts after upload: raw logs, checksums, media, and current HEAD must all be inspectable.

## Connections

- [EvidenceBundles](EvidenceBundles.md) - Evidence must include provenance tied to the current SHA.
- [SkepticGate](SkepticGate.md) - Skeptic verdicts are per-SHA.
- [GitHubPathFilterWindow](GitHubPathFilterWindow.md) - Preview deploy proof can become stale or absent for the same reason.
- [EvidenceSkepticalReview](EvidenceSkepticalReview.md) - Reviewers must inspect artifacts, not accept local-only claims.

## 2026-05-05 Update — CI Auto-Commit Staleness

The `generate-pr-design-docs` CI workflow auto-commits on every push, advancing HEAD past the evidence SHA. Always wait for CI auto-commits to settle before recording `head_commit` in `metadata.json`.

## 2026-05-07 Update — Runtime Delta Classification

PR 6818 added the review corollary that not all post-evidence SHA drift has the
same risk. If the evidence bundle is current for the last runtime commit and the
live head only advances generated docs, the production proof can still be
behaviorally relevant. Strict 7-green may still require same-SHA Skeptic and PR
body cleanup, but reviewers should label that as provenance/process cleanup
rather than a serious implementation defect.

## 2026-09-10 Update — Dirty-Worktree Capture (the reverse direction)

PR #9831 (worldarchitect.ai) surfaced the mirror-image failure: evidence
captured *before* the fix was committed, not evidence going stale *after*
capture. A `testing_ui/capture_*.py` script computed `git rev-parse HEAD` at
capture time and burned it into a video caption while the actual code fix
was staged on disk but uncommitted — the video's SHA predated the fix it
claimed to demonstrate. An independent `/er` review caught it not by SHA
equality but by content diff: `git diff <burned-in-sha> <fix-sha> -- <file>`
showed the fix absent at the burned-in SHA. Mitigation: any script that
burns a git SHA into evidence media must check `git status --porcelain` is
clean before trusting the capture, and must be re-run fresh after every
commit that changes the demonstrated behavior — not just once per PR.
See [[feedback-2026-09-10-dirty-worktree-sha-burned-into-evidence-video]].

## 2026-09-13 Raw-byte Publication Check

CLI display formatting can transform ESC bytes, including JSON escapes. Compare raw HTTPS response content against the captured bytes and manifest before declaring artifact corruption; retain any failed review sample and correction provenance. Avoid formatting/republication churn after evidence is frozen. Source: [[luna-integration-learning-2026-09-13]].
