---
title: "integrate.sh fails in worktree when main is checked out elsewhere"
type: source
tags: [feedback, integrate, worktree, git, worldarchitect]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_integrate_sh_worktree_main_elsewhere.md
---

## Summary
`./integrate.sh` assumes a single-repo layout and fails in the worldarchitect.ai worktree fleet in two ways: it hard-stops on local-only commits ahead of remote, and its `git checkout main` is fatal when `main` is already checked out in another worktree. The worktree-correct equivalent is to fetch `origin main`, branch off it directly with the `dev{epoch}` naming convention, and verify the clean tree — producing the same outcome `/integrate` intends without the worktree conflict.

## Key Claims
- integrate.sh's `git checkout main` is unsafe under `git worktree` because a ref can only be checked out in one worktree at a time
- When `/integrate` reports "Failed to switch to main / already checked out at <path>", do NOT use `--force` blindly — branch off `origin/main` directly
- When integrate reports "unsynced commits with remote", push the current branch to its own remote first, then re-run
- The manual worktree-correct equivalent: `git fetch origin main --quiet && git checkout -b "dev$(date +%s)" origin/main && git branch --set-upstream-to=origin/main "$(git branch --show-current)" && git status --short --branch`
- The script's test-server-stop cleanup step has already run by the time it fails, so the manual workaround can proceed

## Key Quotes
> "`main` checked out in another worktree → `git checkout main` fatal. `fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_prompt_ignore'`. The script cannot switch to main, so it aborts with 'Failed to switch to main'."

> "Branching directly off `origin/main` sidesteps the conflict and is the canonical worktree pattern."

## Connections
- [[feedback_2026-06-11_bash_cwd_does_not_persist_across_invocations]] — related cwd/invocation issue
- [[WorldArchitect]] — repo where the integrate.sh / worktree fleet is used
- [[IntegrateSh]] — the script that fails under worktree layout
- [[WorktreeFleet]] — pattern of ~10 worktrees of `~/projects/worldarchitect.ai`
