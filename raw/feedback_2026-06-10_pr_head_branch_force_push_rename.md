---
name: pr-head-branch-force-push-rename
description: gh pr edit does not support --head; force-push new tip to old branch is the only path to keep PR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: accc5a5a-bae2-4e3c-96aa-4caa512ea998
---

When you need to change a PR's underlying branch (e.g., from a polluted branch to a clean one) but keep the same PR number, the head branch field is immutable after PR creation.

`gh pr edit` supports `--body`, `--title`, `--base` (kinda), `--milestone`, `--add-reviewer`/etc., but NOT `--head`. `gh pr edit --head <new>` fails with "Unknown flag: --head".

The only path that preserves PR # AND changes content:
1. Build the clean state on a new branch (e.g., `git checkout origin/main -b fix/x-v2` + cherry-pick or apply diffs)
2. Force-push the new tip onto the old branch: `git push --force-with-lease origin <new-branch>:<old-branch>`
3. The PR now points at the new SHA on the old branch name; review history, labels, and issue links stay intact

**Why**: PR #7386 was on `fix/7373-stale-anchor-choice` with a 36-file polluted diff (because main had advanced and the old branch was based on stale main). User asked for a fresh branch with the 16 PR commits preserved. The new branch `fix-7373-stale-anchor-choice-v2` had a clean 7-file diff. Closing #7386 and opening a new PR would have lost the review history; force-push kept everything.

**How to apply**: Always requires explicit in-thread human approval for `--force-with-lease` per `~/CLAUDE.md` push-safety. Restate the exact command, name the target branch, then run lease form (not plain `--force`). Lease form will fail safely if the old branch was force-pushed concurrently.

**Related**: `feedback_2026-06-08_pr_files_api_stale_base.md` (use `git diff origin/main` for scope audits, not `gh pr view --json files`). The base of a PR is also stale-prone; combine both: force-push to retarget head + diff against current `origin/main` for scope.
