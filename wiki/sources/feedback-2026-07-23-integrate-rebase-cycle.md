---
title: "/integrate rebase+force-push cycle on disk_magician (2026-07-23)"
type: source
tags: [integrate, github-pr, rebase, force-push, conflict-resolution, disk_magician, lesson, best-practice]
date: 2026-07-23
source_file: ../../raw/feedback_2026-07-23_integrate_rebase_cycle.md
---

## Summary

On 2026-07-23, merging 3 stale PRs (#47, #48, #21) into `disk_magician` main after pushing the sweeper-fix commit (`abc8f51` + `9157b75`) required a rebase+force-push cycle for each. GitHub reported `mergeable_state=dirty` for ~3 seconds after force-push and rejected `/pulls/<n>/merge` with 405 "Base branch was modified" until the `head_sha` ref updated. The fix is a retry-with-backoff that re-fetches origin and re-attempts the merge; the work is finished by 17:13Z when all 3 PRs land on main.

## Key Claims

- Force-pushing a rebased PR head to update the PR's `head_sha` has a 3–5 second window during which GitHub still reports `mergeable_state=dirty` and the merge API returns 405.
- The `pull/<n>/head` GitHub ref is read-only; pushing to it fails. Push to the actual head branch name (e.g. `disk-cleanup-automation-20260722` or `findings-wiki-contract-v2`) to update the PR.
- PR #21 had a 2nd conflict on `pyproject.toml` after the base moved from PR #47's merge — easy to miss the rebase-incompleteness. Always re-run `gh api pulls/<n>` to confirm `mergeable_state == "clean"` BEFORE attempting the merge.
- A rebased commit's author can change to the PR's original author (e.g. `test@test.com`); `git commit --amend --reset-author` fixes that and you need to force-push to update the PR author.
- Tools that solve the rebase loop: `git checkout --theirs <file>` (take main's version), `GIT_EDITOR=true git rebase --continue` (skip the commit-message prompt), `git fetch origin <branch>` (refresh the local tracking ref).

## Key Quotes

> "for PRs targeting the latest main, after force-pushing a rebased branch, GitHub still reports mergeable_state=dirty for ~3 seconds and rejects 405 'Base branch was modified' until the head_sha ref updates."

> "an integrate.sh script should automate the rebase → force-push → retry-with-backoff → verify mergeable_state cycle. The current /integrate just creates a new branch from main, which is only the first step."

## Connections

- [[integrate-hard-stop-uncommitted-state]] — earlier session 2026-06-19 captured a different /integrate blocker; this is the rebase-cycle class.
- [[integrate-behind-origin-main]] — also from 2026-07-04, related to the rebase lag.
- [[disk_magician]] — repo this lesson was verified on.
- [[merge-policy]] — user-scope merge safety policy requiring verbatim `merge approved`; this lesson is the *execution* pattern, not the *authorization* pattern.
- [[github-pr-tools]] — the `gh api` REST surface used to re-fetch mergeable_state and force-push.

## Reproducible 1-cycle recipe

```bash
# 1. Fetch PR head to local ref
git fetch origin pull/<n>/head:pr-<n>-head

# 2. Rebase onto main
GIT_EDITOR=true git -c user.name=... -c user.email=... rebase main

# 3. Resolve any conflicts (take main's version)
for f in $(git diff --name-only --diff-filter=U); do
  git checkout --theirs "$f" && git add "$f"
done
GIT_EDITOR=true git rebase --continue

# 4. Fix author + push to REAL head branch
git commit --amend --reset-author --no-edit
git push -f origin <real-head-branch>

# 5. Retry with backoff (3-5s window)
for i in 1 2 3 4 5; do
  STATE=$(gh api /repos/<owner>/<repo>/pulls/<n> --jq .mergeable_state)
  [ "$STATE" = "clean" ] && break
  sleep 3
done
gh api -X PUT /repos/<owner>/<repo>/pulls/<n>/merge --field merge_method=squash
```

## Verified 2026-07-23 17:13Z on jeffreys-macbook-pro / disk_magician

| PR | Conflict count | Resolution |
|---|---|---|
| #47 (clean) | 0 | direct merge |
| #48 (rebased 4 conflicts) | 4 | `--theirs` for plist, 2 scripts, pyproject.toml |
| #21 (rebased 1 conflict + author fix) | 1 + author | `--theirs` for pyproject.toml + `--amend --reset-author` |

Final main commit: `c346819` (Merge PR #21: machine-local safety guidelines + findings_wiki contract).
