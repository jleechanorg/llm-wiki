---
title: WorktreeHygieneScript
type: entity
tags: [disk_magician, worktree, launchd-script, recency, fail-closed]
sources: [sources/feedback-2026-07-27-worktree-recency-proxies-wrong.md]
last_updated: 2026-07-27
---

`scripts/worktree_hygiene.sh` in `jleechanorg/disk_magician`. The canonical SAFE/NEEDS-REVIEW
triage script for git worktrees across configured repos. DRY-RUN by default; `--execute`
requires `WORKTREE_APPROVED=1`.

## Three defects fixed in PR #50 (commit `9d702c6`, merged 2026-07-27 as `01e25fe`)

1. The age computation used `stat -f '%m' "$path"` as the empty-find fallback. That value is
   the worktree root's directory mtime, which only changes when a *top-level* entry is added
   or removed. Editing files deep in the tree never touches it. So the safety check failed
   **OPEN** whenever its find pipeline returned empty — exactly the wrong direction.
2. The find pipeline was `find ... | sort -rn | head -1`. Under `set -o pipefail` (which this
   script sets), `head -1` closing the pipe early raises SIGPIPE in `sort`, making a healthy
   scan return an empty result — and triggering defect #1.
3. The age computation was repeated verbatim across `cleanup_worktrees.sh` and
   `cleanup_worktree_venvs.sh` with two different but equally wrong `stat`-based proxies.
   Replaced by a single shared helper `scripts/lib/worktree_recency.sh` that the three scripts
   source.

## Installable launchd job

`launchd/com.jleechanorg.disk-magician-worktree-hygiene.plist.template` — installed as
`~/Library/LaunchAgents/com.jleechanorg.disk-magician-worktree-hygiene.plist`. The installed
plist on 2026-07-26 was dry-run only (no `--execute`, no `WORKTREE_APPROVED`), which is the
state that produced the exoneration in the 47-worktree forensics bead `disk_magician-y7t`.

## See also

- [[WorktreeFourteenDayRule]]
- [[FailClosedSafety]]
- [[DiskMagicianRepo]]
