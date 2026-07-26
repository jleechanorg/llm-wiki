---
name: integrate-rebase-cycle-2026-07-23
description: For PRs targeting the latest main, after force-pushing a rebased branch, GitHub reports mergeable_state=dirty for ~3 seconds and 405 'Base branch was modified' until the head_sha ref updates. Always do a final `git fetch origin ; gh api pulls/<n>/merge` retry with backoff.
type: feedback
bead: jleechan-7k9o
---
On 2026-07-23, when merging 3 PRs into disk_magician main after pushing the ironclad-sweeper fix (`abc8f51` + `9157b75`), all 3 PRs (47, 48, 21) had dirty mergeable_state because the sweeper-fix commit had touched the same files the PRs modified. Each PR needed:

1. `git fetch origin pull/<n>/head:pr-<n>-head` (fetch the PR head to a local ref)
2. `git rebase main` inside the local ref (resolve conflicts, prefer main's version with `git checkout --theirs <file>`)
3. `git push -f origin <branch>` (force-push to the PR's actual head branch — note: `pull/<n>/head` is a TRACKING ref; the real head is the named branch like `disk-cleanup-automation-20260722` or `findings-wiki-contract-v2`; pushing to the tracking ref doesn't update the PR)
4. wait ~3s for GitHub to update the head_sha
5. `gh api -X PUT /repos/<owner>/<repo>/pulls/<n>/merge` — may return 405 with "Base branch was modified" if the base was just moved; in that case RE-FETCH and re-merge.

Gotchas:
- PR #21 had a 2nd conflict on `pyproject.toml` after the base moved from #47's merge — easy to miss the rebase-incompleteness. Always re-run `gh api pulls/<n>` to confirm `mergeable_state == "clean"` BEFORE attempting the merge.
- Author on the rebased commit can change to "test@test.com" if the original PR author was different — `git commit --amend --reset-author` fixes that, and you need to push force to update the PR author.
- The `pull/<n>/head` ref is read-only; pushing to it fails with "can't lock ref" or similar. Push to the real head branch.

Tools gained:
- `git checkout --theirs <path>` — take main's version of a conflicted file
- `GIT_EDITOR=true git rebase --continue` — skip past the commit-message prompt
- `git fetch origin <branch>` — refresh the local tracking ref after a force-push

Pattern for /integrate: an `integrate.sh` script should automate the rebase → force-push → retry-with-backoff → verify mergeable_state cycle. The current /integrate just creates a new branch from main, which is only the first step. Real automation would also: stop the active test server, fetch all open PRs targeting the integration branch, attempt rebase-merge for each, log per-PR result, and write a final report.

Verified 2026-07-23 17:13Z on jeffreys-macbook-pro / disk_magician repo: PR #47 (clean), #48 (rebased 4 conflicts → --theirs), #21 (rebased 1 conflict, author fix → --amend --reset-author) — all 3 merged to main.
