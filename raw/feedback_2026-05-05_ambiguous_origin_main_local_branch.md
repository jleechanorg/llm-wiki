---
name: Ambiguous local branch named origin/main blocks integrate.sh
description: A local branch literally named "origin/main" shadows the remote tracking ref, causing integrate.sh to compare against stale ref and falsely report 570 unmerged commits
type: feedback
bead: none
originSessionId: a4ae05e8-54e6-4c57-9bfa-1a989881ad94
---
## Context

Running `/integrate` from branch `dev1777969762` in worktree `/Users/jleechan/worktree_level2` produced a "HARD STOP: 570 commits not in origin/main" error. The branch was actually at the same HEAD as `refs/remotes/origin/main`.

## Root Cause

A local branch named `origin/main` existed at `refs/heads/origin/main` (SHA `733a44f18`), which is a stale snapshot from earlier. Git's `origin/main` refname is **ambiguous** — it resolves to the local branch `refs/heads/origin/main` rather than the remote tracking ref `refs/remotes/origin/main` when both exist.

Symptoms: `warning: refname 'origin/main' is ambiguous.` in git output.

The `integrate.sh` script calls `git rev-list origin/main..HEAD` which resolved to the stale local branch, reporting 570 "unmerged" commits that were in fact all already in remote main.

## Diagnosis Command

```bash
git for-each-ref --format='%(refname)' | grep -i "origin/main"
# Shows refs/heads/origin/main AND refs/remotes/origin/main = ambiguous
```

## Fix

Delete the confusingly-named local branch:

```bash
git branch -d "origin/main"
```

Safe to delete: it had no unique commits (it was behind remote main by hundreds of commits).

**Why**: Local branches should never be named using `/`-paths that shadow remote tracking refs. The branch was likely created by an AO worker or worktree clone that used `origin/main` as a base ref.

## How to Apply

Before running `/integrate` and seeing the 570-commits block, run:
```bash
git for-each-ref --format='%(refname)' | grep "refs/heads/origin/"
```
If this returns any results, those local branches are shadowing remote refs. Delete them.

The `--force` flag on integrate.sh does NOT bypass the 570-commit hard-stop check (it only overrides uncommitted-changes and squash-merge checks).
