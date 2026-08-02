---
title: "Worktree recency proxies were unsafe; fail-closed helper shipped in disk_magician PR #50 (2026-07-27)"
type: source
tags: [disk_magician, worktree, recency, fail-closed, safety, agent-orchestrator, claude-skill-evolution]
date: 2026-07-27
source_file: /Users/jleechan/llm_wiki/raw/feedback_2026-07-27_worktree_recency_proxies_wrong.md
---

## Summary

Two `stat`-based proxies for "when was this worktree last touched?" were measured wrong against
the live 340-worktree worldarchitect.ai registry on 2026-07-26: 2 of 30 sampled worktrees read
20.4 days old from both proxies while their newest file was 12.8 days old — inside the protected
14-day window. The fix — `scripts/lib/worktree_recency.sh` — fails closed and ships via disk_magician
PR #50 (commit `9d702c6`, merged to `01e25fe` 2026-07-27), with 11 regression cases including
explicit failure-of-old-proxies and a fail-closed assertion.

## Key Claims

- `stat <wt>/.git` on a linked worktree measures **creation** age, not use — `.git` is a
  one-line `gitdir:` pointer written once by `git worktree add`.
- `stat <wt>` (parent dir mtime) only moves on top-level add/remove; deep edits never touch it.
- `worktree_hygiene.sh`'s fallback path used `stat <wt>` when its find pipeline returned empty,
  which was the most stale-biased number available — a fail-OPEN safety check, the opposite of
  what it should do on its failure path.
- `sort -rn | head -1` under `set -o pipefail` (a third defect in `worktree_hygiene.sh`) can
  make a healthy scan return EMPTY: `head -1` closing the pipe raises SIGPIPE in sort. Replaced
  with a single-pass awk max.
- Git metadata is NOT activity: `git status --porcelain` rewrites the index, and
  `worktree_hygiene.sh` runs it on every candidate during triage. Counting it would make each
  run permanently exempt the worktrees the previous run had identified.
- A separate fix lives at bead `disk_magician-si1` (OPEN): the 14-day floor still does not bind
  machine-wide — `host-disk-guardian` deletes merged-PR worktrees with **no** min-age check.

## Key Quotes

> Both proxies are durable defects, not race conditions. (`feedback_2026-07-27_worktree_recency_proxies_wrong.md`)

> git metadata is not activity. `git status` rewrites the index and worktree_hygiene.sh runs
> it on every candidate during triage. (`CLAUDE.md`, "Worktree 14-day rule", 2026-07-27)

## Connections

- [[WorktreeFourteenDayRule]] — new canonical rule authored this session
- [[FailClosedSafety]] — generalised pattern: unmeasurable → protected
- [[SortHeadSigpipePipefail]] — secondary defect fixed in the same PR
- [[DiskMagicianRepo]] — owning repo
- [[WorktreeHygieneScript]] — call site that previously failed open via the empty-find fallback
- [[CleanupWorktreeVenvsScript]] — second call site; failed the same way
- [[HostDiskGuardianScript]] — separate `disk_magician-si1` machine-wide binding gap
- [[DiskMagician957APrime]] — open forensics bead for the same-day 47-worktree sweep (which
  this rule would have protected, if it had been live then)
- [[AgentOrchestrator]] — workflow context
