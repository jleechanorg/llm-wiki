---
title: "Merge Readiness Contract"
type: concept
tags: [merge-readiness, merge-gate, ci-green, no-conflicts, no-serious-comments, evidence-reviewed, openclaw-approved, pr-readiness-6-gate, live-head, multi-writer-pr]
last_updated: 2026-06-12
sources: [jleechanclaw-orchestration-system-design, feedback-2026-06-12-pr-readiness-minimum-gates]
sources: [jleechanclaw-orchestration-system-design]
---

## Summary
A PR is considered merge-ready only when all five gates are true simultaneously: CI green, no conflicts, no serious review comments, evidence reviewed, and OpenClaw approved. The developer only needs to hit the merge button — the system tells them when.

**User-superseded 6-gate manual contract (2026-06-12, PR #7467 review):** For manual merges on multi-writer PRs, the user's "Minimum before merge" list is the canonical gate superset (see `feedback-2026-06-12-pr-readiness-minimum-gates.md`, bead `rev-1ver0`). The 6 gates:
1. **Live head SHA matches PR body evidence.** `git fetch origin && git rev-parse origin/<branch>` must equal the SHA cited in the PR description.
2. **CI green at current head.** No "queued/running" lingering. `gh pr checks` or statusCheckRollup all SUCCESS.
3. **All review threads resolved.** `gh pr view <N> --json comments` — every thread body shows "✅ Addressed" or explicit dismissal. Stale CR "X open" summaries are unreliable.
4. **CodeRabbit enabled + reviewDecision APPROVED.** Not skipped, not paused. `reviewDecision ∈ {"", "APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"}`; only `APPROVED` is mergeable.
5. **Real-LLM test re-run at live head passes.** If the test was run at an older local head, re-run at the live head. A passing result on an older SHA is not proof for the current PR.
6. **Skeptic verdict matches live head.** Skeptic gate's "VERDICT: PASS" must cite the live head SHA, not an earlier SHA.

## The Five Gates

| Gate | Source | Check |
|------|--------|-------|
| **CI green** | GitHub Actions | All required checks `conclusion == success` |
| **No conflicts** | GitHub API | `mergeable == "MERGEABLE"` |
| **No serious comments** | CodeRabbit, Copilot, Cursor Bugbot | No `REQUEST_CHANGES` verdict |
| **Evidence reviewed** | CodeRabbit / Codex via `/er` | Evidence review PASS or WARN |
| **OpenClaw approved** | `pr_reviewer.py` LLM | `ReviewDecision.approve` |

## Gate Implementation Details

**Gate 1 - CI Green**: GitHub Actions all required checks must have `conclusion == success`. AO detects via `scm-github` plugin.

**Gate 2 - No Conflicts**: GitHub API `mergeable` field must be `"MERGEABLE"`. GitHub's mergeability check handles this.

**Gate 3 - No Serious Comments**: CodeRabbit, Copilot, and Cursor Bugbot review verdicts are checked. Any `REQUEST_CHANGES` verdict blocks merge.

**Gate 4 - Evidence Reviewed**: CodeRabbit/Codex `/er` evidence review must return PASS or WARN. The evidence bundle (docs/evidence/{repo}/PR-{N}/*/verdict.json) is required for code PRs. Evidence gate checks stage1 PASS, stage2 PASS, and independence_verified.

**Gate 5 - OpenClaw Approved**: `pr_reviewer.py` LLM reviews the PR and returns `ReviewDecision.approve`, `changes`, or `escalate`. Only `approve` allows auto-merge.

## The Developer's Role

The system handles: CI failures auto-fixed, review comments auto-addressed, CodeRabbit approval obtained, merge-readiness gates passed.

The developer only does: write code and open PR (step 1), final merge approval (step 5).

## North Star

Jeffrey reviews a Slack message that says "PR #173 is merge-ready" and hits merge. The 2 hours of CI debugging and comment-fixing never touched his attention.

## Contrast with Manual Merge

| Manual | Autonomous |
|--------|-----------|
| Developer waits for CI | CI auto-fixed, retry strategies |
| Developer monitors review | Review comments auto-addressed |
| Developer checks mergeability | System verifies all 5 gates |
| Developer decides when to merge | System notifies "ready to merge" |
| Hours to days | Minutes to hours |

## Related Concepts
- [AutonomousAgentLoop](AutonomousAgentLoop.md)
- [EscalationRouter](EscalationRouter.md)
- [TwoStageEvidencePipeline](TwoStageEvidencePipeline.md)
- [HarnessEngineering](HarnessEngineering.md)