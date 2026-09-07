---
title: "Advice runner LFS smudge bug (fixed) + concurrent-session merge race"
type: source
tags: [git, lfs, advice-runner, harness, ci, concurrency]
date: 2026-09-06
source_file: /Users/jleechan/.claude-wa/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-09-06_advice_runner_lfs_smudge_and_concurrent_merge_race.md
---

## Summary

While driving PR #9743 through `/ready`, `~/.claude/skills/advice/scripts/run_primary_pair.py`'s `create_clone()` was found to break Git LFS smudge downloads 100% reproducibly: it removes the `origin` remote before `git checkout`, so LFS has no remote to fetch tracked blobs from, and checkout fails with exit 128 ("missing protocol"). Fixed by setting `GIT_LFS_SKIP_SMUDGE=1` on both the clone and checkout subprocess calls. Separately, a different concurrent session on the same account squash-merged the exact PR being reviewed mid-`/ready`, without the reviewing session calling `gh pr merge`.

## Key Claims

- `git remote remove origin` followed by `git checkout` on a commit whose tree reaches an LFS pointer fails deterministically, not intermittently — confirmed by isolating the exact clone→remote-remove→checkout sequence outside the runner and capturing real stderr.
- `subprocess.CalledProcessError.__str__()` never includes captured stderr text, so opaque `exit 128` errors need a standalone repro with stderr explicitly printed to diagnose.
- `git clone --no-local` on a large repo can legitimately take 5-10+ minutes under load (real `pack-objects`/`index-pack` work) — don't assume a slow clone is hung.
- A stale `objects/maintenance.lock` (week-old, no owning process) in a shared `.git` dir across many worktrees can independently block clones — a real but separate hazard from the LFS bug.
- On a shared account running multiple concurrent agent sessions, a PR can be merged by a sibling session mid-review; re-check `gh pr view --json state,mergedAt` before continuing a long `/ready` cycle, and cherry-pick any post-merge commit onto a fresh PR.

## Key Quotes

> "Error downloading object: docs/user-stories-ui/videos/....mp4: Smudge error: ... missing protocol: \"\"" — the actual LFS failure once origin was removed.

## Connections

- [[AdviceRunner]] — the reviewed script; fix applied to `create_clone()`.
- [[GitLfsSmudgeFilter]] — the mechanism that broke.
- [[SameAuthorConcurrentSessionCollision]] — the sibling-session merge pattern observed (merge-out-from-under-you variant).
- PR #9743, PR #9768 (jleechanorg/worldarchitect.ai)
