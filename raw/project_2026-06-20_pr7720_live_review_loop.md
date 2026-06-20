---
name: PR 7720 live review loop: current-head gates before merge-ready claims
description: Repeated PR checks must refresh live state, distinguish attached PR-context gates from workflow_dispatch runs, and close only on MERGED state.
type: project
bead: rev-hygyj
---

# PR 7720 Live Review Loop

On 2026-06-20, PR https://github.com/jleechanorg/worldarchitect.ai/pull/7720 was repeatedly checked while it moved from pending gates to merged.

Durable rule: repeated PR review turns must recompute live current-head state every time. Do not carry forward a stale verdict.

Key distinctions:

- A successful `workflow_dispatch` run does not supersede a queued, pending, cancelled, or failing check attached to the PR context.
- Green Gate check-row success is not enough when the workflow can exit 0; inspect the exact run log for gate-by-gate verdicts.
- Cancelled checks stay blockers unless a newer same-name current-head run supersedes them.
- Review-thread state comes from GraphQL `reviewThreads.isResolved`, not REST comment count.
- Evidence captured at an earlier SHA can support a narrower behavior claim, but not an exact-byte current-head claim.
- After the user reports merge, verify live `state=MERGED`, `mergedAt`, and `mergeCommit.oid`.

Closeout facts:

- PR head before merge: `8ccd88d535ab6e33ff22c12c3888055f88a1fd02`
- Merge commit: `21cf81df853ca958601a2a0cb33302223c90dddc`
- Merged at: `2026-06-20T23:27:01Z`
- Bead: `rev-hygyj`

Reusable commands:

```bash
unset GITHUB_TOKEN
gh pr view 7720 --repo jleechanorg/worldarchitect.ai --json number,title,state,mergedAt,mergeCommit,headRefName,headRefOid,url
gh pr checks 7720 --repo jleechanorg/worldarchitect.ai --json name,state,bucket,description,startedAt,completedAt,workflow,link
gh run view <run_id> --repo jleechanorg/worldarchitect.ai --log
```

[[jeffrey-oracle]]: NO.
