---
name: CodeRabbit incremental review behavior
description: CodeRabbit does not re-issue formal APPROVED reviews for new commits on already-reviewed PRs
type: feedback
bead: none
---

## Context
PR #6945 had CodeRabbit APPROVED on commit c359533c45 (first commit). After pushing
commits e8b97a0f4 (design doc) and 530d99d9d (symlink fix), CodeRabbit commented
"No actionable comments were generated" and "Review triggered" but did NOT issue a new
formal APPROVED review. GitHub's reviewDecision field remained empty string.

## Technical detail
- CodeRabbit is an incremental reviewer — it reviews new diffs only, not the full PR
- It does not re-issue APPROVED state for subsequent commits
- GitHub reviewDecision may lag (show empty string) even when an APPROVED review exists
- The Green Gate workflow checks for CR approval independently (status+comment check)
- Pinging @coderabbitai review generates comments but not formal review records

## Solution / Rule
For PRs with CodeRabbit APPROVED on an earlier commit:
1. The existing APPROVED review is valid — CodeRabbit doesn't revoke it
2. New commits get incremental comments, not new formal reviews
3. Green Gate workflow independently verifies CR approval (doesn't rely on reviewDecision)
4. If reviewDecision is empty but APPROVED review exists, trust the review, not the field
5. For lite-green, one APPROVED review at any commit in the PR satisfies Gate 3

## Verification
PR #6945: Green Gate reported "GATE-3 PASS: CR=APPROVED(status+comment)" despite empty reviewDecision.

## References
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6945
