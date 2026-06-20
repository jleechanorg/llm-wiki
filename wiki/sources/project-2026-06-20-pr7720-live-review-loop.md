---
title: "PR 7720 live review loop: current-head gates before merge-ready claims"
type: source
tags: [worldarchitect, pr-review, green-gate, current-head, evidence, merge-readiness]
source_path: /Users/jleechan/.Codex/projects/-Users-jleechan-projects-worktree_mobile_login/memory/project_2026-06-20_pr7720_live_review_loop.md
date: 2026-06-20
bead: rev-hygyj
---

# PR 7720 live review loop: current-head gates before merge-ready claims

PR [#7720](https://github.com/jleechanorg/worldarchitect.ai/pull/7720) was repeatedly checked on 2026-06-20 while it moved from pending gates to merged.

The durable process rule is to recompute live current-head state on every repeated `review again` / `check again` turn. Do not carry a prior verdict forward.

## Current-head review rules

- Verify the current `headRefOid` before using PR body evidence, check results, reviews, or verdict comments.
- Treat a queued or pending PR-context Green Gate check as still pending even if a separate `workflow_dispatch` Green Gate run succeeded.
- Read Green Gate logs for gate-by-gate verdicts instead of relying only on the check-row conclusion.
- Treat cancelled checks as blockers unless a newer same-name current-head run supersedes them.
- Use GraphQL `reviewThreads.isResolved` for review-thread blockers.
- Scope evidence to what the captured SHA and served bytes prove. Earlier deployed HTTP captures can prove deployed behavior, but not exact-byte current-head hardening unless the captured bytes match the current diff.
- After a merge report, verify live `state=MERGED`, `mergedAt`, and `mergeCommit.oid`.

## Closeout facts

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7720
- Head before merge: `8ccd88d535ab6e33ff22c12c3888055f88a1fd02`
- Merge commit: `21cf81df853ca958601a2a0cb33302223c90dddc`
- Merged at: `2026-06-20T23:27:01Z`
- Bead: `rev-hygyj`

## Related

- [[GreenGateWorkflow]]
- [[PR7720]]
- [[PRMidReviewMergeAncestryCheck]]

[[jeffrey-oracle]]: NO.
