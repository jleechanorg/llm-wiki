---
name: newbranch-cherrypick-forcepush-retarget
description: To retarget a polluted PR to a clean branch, the recipe is: /newb with cherry-pick + commit refactor + force-push new tip onto old branch (preserves PR #, review history, issue link)
metadata:
  node_type: memory
  type: feedback
  originSessionId: accc5a5a-bae2-4e3c-96aa-4caa512ea998
---

When a PR's branch was based on stale `origin/main` and the diff has ballooned to 30+ files (most pollution from main drift, not the actual fix), the user wants a CLEAN PR with the original 7-file fix preserved — without losing the PR number, review history, or issue link. The recipe is the 3-step /newb + force-push sequence:

**Step 1: `/newb <clean-name> with cherry-pick**
```bash
git stash push --include-untracked -m "pre-newb stash"   # save ao settings + untracked
/newb <clean-name>                                        # script fetches origin/main, creates new branch from origin/main
git cherry-pick <sha1> <sha2> ... <shaN>                 # bring forward ONLY the 16 real fix commits
# or: newbranch.py auto-detects "bring in changes" keyword and cherry-picks for you
```

**Step 2: commit the refactor** (Skeptic recommendation closure, in-scope polish)
```bash
git add <new-shared-module> <updated-imports>
git commit -m "fix(<N>): extract helper to shared module — closes Skeptic gate X"
```

**Step 3: force-push new tip onto OLD branch name** (preserves PR #)
```bash
git push --force-with-lease origin <clean-branch>:<old-polluted-branch>
# e.g. git push --force-with-lease origin fix-7373-stale-anchor-choice-v2:fix/7373-stale-anchor-choice
```

`gh pr edit` does NOT support `--head` — the head branch field is immutable after PR creation. Force-push is the ONLY path that changes content while keeping the PR number.

**Required permissions**: `--force-with-lease` is forbidden without explicit in-thread human approval per `~/CLAUDE.md` push-safety. Ask via AskUserQuestion with "Force-push new tip to old branch (Recommended)" as the recommended option. Once approved, restate the exact command + target branch, then run `--force-with-lease` (NOT plain `--force` — lease form fails safely if the old branch was force-pushed concurrently).

**Branch name normalization**: `newbranch.py` normalizes slashes to dashes in branch names. If you want `fix/7373-stale-anchor-choice-v2`, the script will give you `fix-7373-stale-anchor-choice-v2`. Document this — it's not a bug, it's the documented behavior. Use the dash form in the force-push source ref.

**Result for PR #7386**: 36-file polluted diff at head `69baab590f` → 7-file clean diff at new head `f21bd61478` on the SAME `fix/7373-stale-anchor-choice` branch. Review history, labels, and `fix(#7373)` issue link all preserved.

**Why**: Closing #7386 and opening a new PR would have lost the `fix(#7373)` issue link and CodeRabbit's stale CHANGES_REQUESTED history. The user explicitly chose force-push after seeing the recommendation.

**How to apply**: Trigger condition — `gh pr diff <N> --stat` shows >>2× the expected file count, and `git diff origin/main -- <expected-files>` is empty (file changes are merge pollution, not real work). Before recommending this, verify scope with `git diff origin/main...<head>` so the user can see exactly what they're approving to be discarded.

**Related**: `feedback_2026-06-10_pr_head_branch_force_push_rename.md` (the `gh pr edit --head` learning); `feedback_2026-06-08_pr_files_api_stale_base.md` (scope audit pattern).
