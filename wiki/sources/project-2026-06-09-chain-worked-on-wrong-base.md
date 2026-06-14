---
title: "Level-up chain worked on wrong base (4 PRs, divergent)"
type: source
tags: [level-up, pr-chain, divergent-base, worktree, worldarchitect-ai]
date: 2026-06-09
source_file: raw/project_2026-06-09_chain_worked_on_wrong_base.md
---

## Summary
Built 4 chain PRs on parallel worktree branches forked from PR 1 base, not from the user's review branch (PR #7366 base fix/level-up-session-reducer). Local 6-unpushed-commits line and 2-unpulled-commits remote line are divergent, neither is a superset. Force-push either direction destroys unique work. User concluded 'sounds like you got nothing done' because from their branch the reducer is a well-tested island wired into one call site. Lesson: when sitting in a worktree on a divergent branch, surface the divergence as the lead item, not as a side note.

## Key Claims
- 4 PRs: #7374 (PR 5.5), #7376 (PR 4), #7377 (PR 5), #7378 (PR 6 v2) — all branched from PR 1/PR 5.5 base, not from PR #7366 base
- 6 unpushed commits on fix/level-up-session-reducer (this worktree) vs 2 unpulled on origin/fix/level-up-session-reducer; force-push either direction destroys unique work
- Push local over #7366: loses schema ownership registry + CI gate + god-mode prompt + in-repo docs
- Push #7366 over local: loses the 14-fn reducer depth + PR 2 fail-closed + PR 3 graft

## Connections
- [[project_2026-06-09_pr7366_supersedes_pr1_conflict]]
- [[StackedPrSingleWriterRule]]
- [[LevelUpChain]]
