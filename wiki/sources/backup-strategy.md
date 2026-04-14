---
title: "Backup Strategy for Fragile Branches and Worktrees"
type: source
tags: [backup, git, worktree, disaster-recovery, restic]
sources: []
last_updated: 2026-04-14
---

## Summary

Auto-backup strategy for repos without mutating fragile branches/worktrees. Provides fast restore path for branch tips, unstaged/staged diffs, and worktree mapping with encrypted off-host retention.

## Key Claims

- No mutation during backup: no rebase, commit, push, or branch rewrite
- Snapshot approach: capture exact state as-is including messy worktrees
- Git bundle for full history + metadata
- Patch artifacts for WIP (diff-working.patch, diff-staged.patch)
- restic for encrypted incremental backup with retention policy
- Restore playbook: recover bundle, create restore repo, import bundle, reconstruct worktrees

## What Gets Backed Up Per Repo

- repo.bundle via git bundle create --all
- remotes.txt, branches.txt, worktrees.txt, status.txt, head.txt
- recent-commits.txt
- diff-working.patch, diff-staged.patch

## Connections

- [[NewMachineSetup]] — Restore procedure after system rebuild

## Contradictions

- None identified
