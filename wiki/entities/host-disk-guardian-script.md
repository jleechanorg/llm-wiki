---
title: HostDiskGuardianScript
type: entity
tags: [disk_magician, launchd-script, worktree, host-monitoring]
sources: [sources/feedback-2026-07-27-worktree-recency-proxies-wrong.md]
last_updated: 2026-07-27
---

External to disk_magician: `~/.worldarchitect.ai/.claude/skills/host-disk-guardian/scripts/host-disk-guardian.sh`,
launchd as `org.jleechanorg.host-disk-guardian`, `StartInterval=900`, ThrottleInterval=300.
Monitors host free disk and runs auto-clean when free < 20 GB.

Its worktree-cleanup function `clean_merged_pr_worktrees` at line ~205-265 removes any
worktree whose branch has a merged PR and whose HEAD matches the merged SHA. **No `min-age`
check at all.** Currently scoped via `HOST_DISK_GUARDIAN_WORKTREE_GLOB` (default
`/private/tmp/wa-*`) — so blast radius today is `/private/tmp` only.

Open bead `disk_magician-si1` covers the machine-wide binding gap: this script does NOT
respect the [[WorktreeFourteenDayRule]]. A future operator setting the glob to
`~/projects/worktree_*` would re-introduce the same defect that was just fixed in
disk_magician proper.

`git worktree remove` is called *without* `--force`, so the script's own backstop is the
native git refusal when the working tree is dirty. `--force` previously bypassed that refusal
entirely (bead `rev-9qxkm`).
