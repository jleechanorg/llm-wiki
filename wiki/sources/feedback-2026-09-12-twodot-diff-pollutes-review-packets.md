---
title: "Two-dot diff pollutes review packets with unrelated main commits"
type: source
tags: [git, code-review, evidence-standards, web-advice]
date: 2026-09-12
source_file: raw/feedback_2026-09-12_twodot_diff_pollutes_review_packets_with_unrelated_main_commits.md
---

## Summary

Building a `/web-advice` review packet for PR #9846 with a two-dot `git diff origin/main <branch>` pulled in unrelated commits that landed on `main` after the branch forked, making it look like the PR deleted application code it never touched. An external Gemini reviewer correctly flagged the phantom deletion as a blocker. The fix is diffing against the merge-base (`git diff $(git merge-base origin/main <branch>) <branch>`), which is the three-dot-equivalent, base-anchored comparison.

## Key Claims

- Two-dot diff (`git diff A B`) is not base-anchored: it shows *every* difference between the two tips, including commits added to `A` after `B` diverged from it, which appear as reversed/phantom changes in `B`'s apparent diff.
- The correct comparison for "what did this branch actually change" is a merge-base diff, not a direct two-ref diff.
- An external reviewer flagging unrelated code in a diff is itself a signal to check the diff's base before assuming the reviewed work is broken.
- This compounds with [[rtk-diff-truncation]] (bead rev-mdl72): both are reasons `git diff`/`gh pr diff` output cannot be trusted at face value in this environment without extra care (truncation *and* base selection).

## Key Quotes

> "re-ran with the merge-base diff — output shrank from 6 files/290+229 lines to the true 3 files/254 insertions... Gemini approved on the corrected packet."

## Connections

- [[rtk-diff-truncation]] — sibling diff-integrity gotcha in the same review session
- [[web-advice]] — the review mechanism whose packet this bug corrupted
- [[evidence-standards]] — packet/evidence construction discipline this reinforces
