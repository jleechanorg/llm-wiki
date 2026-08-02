---
title: "2026-07-29 disk-full — 5 structural root causes ranked (recurrence class)"
type: source
tags: [disk_magician, disk-full, root-cause, structural-producers, agent-venv, worktree, /private/tmp, antigravity]
date: 2026-07-29
source_file: /Users/jleechan/llm_wiki/raw/feedback_2026-07-29_root_cause_disk_full.md
---

## Summary

Free disk dropped 30 GiB in 50 hours after the 2026-07-26 16:49-17:36 emergency reclaim
restored 60 GiB. The /learn capture on 2026-07-26 closed `disk_magician-y7t` with the
correct label "mass sweep" but did not address any structural producer. Same input creates
the same output every 50 hours — this captures the taxonomy of 5 producers, ranked by
reclaimable size and the structural fix each needs. Reclaim headroom if all 5 are fixed:
~76 GiB without touching `~/Library/Caches` or `~/.gemini`.

## Key Claims

- Pressure_sweep is a one-shot release valve, not a maintainer. Any structural fix for
  disk fullness has to live in a cron/launchd sweep with retention policy, not a manual
  sweep caller.
- agent-* venv bloat (`worldarchitect.ai/.claude/worktrees/agent-*/venv` + `venv.bak.<ts>`)
  is in scope of NO disk_magician sweep — `cleanup_worktree_venvs.sh` only walks
  `~/projects/worktree_*` and `~/worktrees_*`. ~25 GiB reclaimable.
- `~/.worktrees` siblings (jleechanorg-fix, wa-pr8536-finish, etc.) are also outside
  cleanup_worktrees.sh's reach. ~30 GiB reclaimable.
- `/private/tmp/{ambientfix*,crashfix,ios-app-prev}` (6 dirs × ~1.4 GiB) is unowned cruft
  that no cleanup script on this machine has any allowlist for. ~8.4 GiB reclaimable.
- `~/.gemini/antigravity-cli/{brain,conversations}` is owned by the Antigravity CLI and
  is out of disk_magician scope; bead `disk_magician-1f9` covers the related
  whole-root-symlink retirement issue but not these specific dirs. ~12.7 GiB; conservative
  care.
- `.git` history bloat (~6 GiB across `.worktrees` and `~/.hermes/.git`) would be reclaimed
  by `git gc --prune=now`. `scripts/set_gc_worktree_prune.sh` exists but is not scheduled.

## Key Quotes

> A 30 GiB drop in 50 hours implies ~8 GiB/day net growth. We do not have a measurement of
> growth rate per producer, so the ranking is by static size at this snapshot.

> The fix-on-discovery rule excludes all 5: none is <10 lines, none is user-managed config,
> and at 29 GiB free there is no immediate pager. Each fix is a discrete PR with its own
> bead and retention-policy review.

## Connections

- [[DiskMagician]] — owning tooling
- [[DiskCleanupCoverage]] — overall coverage map
- [[DiskDiagnosisReconciliation]] — three-lane diagnosis pattern
- [[CleanupWorktreeVenvsScript]] — extend scope for root cause #1
- [[CleanupWorktreesScript]] — extend scope for root cause #2
- [[PressureSweep]] — emergency release valve (root cause none of the 5)
- [[HostDiskGuardianScript]] — complementary process-class for the "what pressure-sweep
  doesn't sweep" problem
- [[WorldArchitectFourLeakPrevention]] — parallel pattern from earlier session
- Beads: `disk_magician-7v3` (this), `disk_magician-y7t` (2026-07-26 forensics, still OPEN),
  `disk_magician-1f9` (Antigravity .gemini symlink, parallel work), `disk_magician-si1`
  (machine-wide 14-day floor would fix #1 and #2 if extended), `disk_magician-yua`
  (deploy drift pattern)
