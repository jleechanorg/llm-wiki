---
title: "MergeTrain — jleechanorg/merge_train"
type: entity
tags: [repo, github, jleechanorg, hooks, merge-train]
date: 2026-06-23
sources: [hook-tui-exit-codes-2026-06-23]
---

## jleechanorg/merge_train

**URL:** https://github.com/jleechanorg/merge_train
**Owner:** jleechanorg
**Purpose:** Stacked/sequential PR merge tooling with Claude Code PreToolUse hook integration

## Hook Cache Location

`/tmp/merge_train_cache_{repo_name}.json` — keyed by repository name. Tests that mock repos with `tmp_path / "repo"` collide on this cache key.

## Key PRs

- [[PR34]] — 2026-06-23 hook TUI visibility fix (commit `3dfa796`)

## Connections

- [[PreToolUseHookExitCodes]] — three-mode exit-code contract used by hooks in this repo
