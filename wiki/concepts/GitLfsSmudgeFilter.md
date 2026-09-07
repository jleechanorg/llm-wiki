---
title: "Git LFS Smudge Filter Requires a Remote"
type: concept
tags: [git, lfs, tooling-gaps]
date: 2026-09-06
---

# Git LFS Smudge Filter Requires a Remote

Git LFS pointer files (small text stubs committed to the repo) are expanded back
into real binary content by the `git-lfs filter-process` **smudge** filter at
`git checkout` time. That filter needs a configured remote (`origin`, or
`lfs.url`) to fetch the actual blob from a batch API — if no remote is configured,
the smudge filter fails with something like:

```
Error downloading object: <path>: Smudge error: ... missing protocol: ""
error: external filter 'git-lfs filter-process' failed
fatal: <path>: smudge filter lfs failed
```

and `git checkout` exits non-zero (128).

## Trap: removing `origin` for review isolation

A common pattern for spinning up a disposable, read-only review clone is:
`git clone --no-local --no-checkout <src> <dest>` → `git remote remove origin`
(so the reviewer can't accidentally push/fetch) → `git checkout --detach <sha>`.
If the checked-out tree reaches **any** LFS-tracked path, this sequence fails
**100% of the time**, not intermittently — it looks like a flaky/race failure
(especially since a large repo's initial clone can independently take minutes,
inviting the "it's just slow/hung" misdiagnosis) but is fully deterministic once
you isolate the exact commands and print real `stderr`
(`subprocess.CalledProcessError.__str__()` never includes it).

## Fix

If the review clone doesn't need real binary content (a code reviewer doesn't need
actual video/image bytes), skip the smudge filter entirely:
`env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")`, passed to both the `clone` and
`checkout` subprocess calls. LFS pointer files are left as-is; `checkout` succeeds.

## Provenance

Found and fixed 2026-09-06 in [[AdviceRunner]] (`~/.claude/skills/advice/scripts/run_primary_pair.py`), while driving PR #9743 through `/ready`.

## Connections

- [[AdviceRunner]]
- Source: [[feedback-2026-09-06-advice-runner-lfs-smudge-and-concurrent-merge-race]]
