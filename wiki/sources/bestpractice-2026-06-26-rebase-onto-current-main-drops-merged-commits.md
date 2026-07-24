---
title: "Best Practice 2026 06 26 Rebase Onto Current Main Drops Merged Commits"
type: source
tags: [best-practice, git, pr-cleanup, rebase, 2026-06]
date: 2026-06-26
source_file: .claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-26_rebase-onto-current-main-drops-merged-commits.md
---

## Summary

When a PR is open, base = `main`, and `gh pr diff <N> --name-only` shows files the author did NOT touch, the branch was created from a stale `main` tip. The "extra" commits in the PR's diff are commits that landed on `main` between the tip the branch forked from and the current `main` HEAD. They appear in the PR's diff because the PR's base is `main` and `git diff` compares HEAD against `main`, not against the branch's original tip.

**Fix:** `git rebase --onto origin/main <old-merge-base> HEAD` followed by `git push --force-with-lease`. The rebase replays the real commits on top of current `main` and **drops** the stale commits as "patch contents already upstream". The push rewrites the PR's head ref. The PR's base stays `main`.

## Why --force-with-lease, not --force

The lease guard refuses to overwrite remote history someone else updated since the last fetch. Plain `--force` would silently nuke a teammate's commit. If `--force-with-lease` fails with "stale info", `git fetch` then re-verify before retrying.

## Diagnostic (run before rebase)

```bash
MB=$(git merge-base origin/main HEAD)
git log --oneline -1 $MB
git log --oneline -1 origin/main
# If $MB != origin/main, main has moved past your branch point.

git log --oneline $MB..HEAD --no-merges
# Anything not authored by you is "stale" — will drop during rebase.

git diff origin/main HEAD --name-only
# Should match `gh pr diff <N> --name-only`. If they differ, sync.
```

## Recipe (verbatim from jleechanorg/worldarchitect.ai PR #7957 cleanup)

```bash
git rebase --onto origin/main $(git merge-base origin/main HEAD) HEAD
# expect: "dropping <sha> <subject> -- patch contents already upstream"

git diff origin/main HEAD --name-only
# expect: only files you authored

git push --force-with-lease origin <branch>
```

## Where this lives in the skill tree

Cross-referenced into `~/.hermes_prod/skills/git/pr-clean-worktree/SKILL.md` as **Case D** of the "Stale-Branch Rebase" section. The pre-existing skill already covered Cases A/B/C (added 2026-06-13 for PR #7200, pre-push). Case D is the **post-push** complement: "PR is already open, base is `main`, diff has unrelated files." Same skill, different stage of the PR lifecycle. Per the `skillify` "cross-reference, don't duplicate" rule, a Case D addition is the right shape — not a new standalone skill.

## Triggered by

PR [#7957](https://github.com/jleechanorg/worldarchitect.ai/pull/7957) (jleechanorg/worldarchitect.ai, 2026-06-26). Branch `fix/unforeseen-complication-frequency` was created from local main's tip at `4bfc956408` (Lever 3 perf change). Between then and push, main moved to `45747b819a` (rate-limit rename + bump). The PR's diff included 2 unrelated commits (`670f3944` chore(rate-limit), `730d7be6` test(evidence)) — 5 files the user did not author. After the rebase: 3 files, 2 commits, both authored by the user. Unit tests 5/5 still green.

## Related

- `~/.hermes_prod/skills/git/pr-clean-worktree/SKILL.md` (Case D added 2026-06-26)
- `~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-26_rebase-onto-current-main-drops-merged-commits.md`
- `~/roadmap/learnings-2026-06.md` (entry appended 2026-06-26)
- `feedback-2026-06-11-rebase-clears-presubmit-base-drift` (related: presubmit failures cleared by rebase; different symptom, same root cause)
- jleechanorg/worldarchitect.ai PR [#7957](https://github.com/jleechanorg/worldarchitect.ai/pull/7957), issue [#7956](https://github.com/jleechanorg/worldarchitect.ai/issues/7956)
