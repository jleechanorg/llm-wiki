---
title: "Disk harness overhaul — snapshot blindness fixed (2026-05-24)"
type: source
tags: [disk-usage, disk-snapshot, disk-audit, feedback, infrastructure, ao-sessions, hermes, xcode-deriveddata, apfs-snapshots]
sources: [project_2026-05-24_disk_harness_overhaul]
date: 2026-05-24
source_file: raw/project_2026-05-24_disk_harness_overhaul.md
---

## Summary

Disk hit 93% (869/926 GB) on 2026-05-23, triggering an alert. Investigation revealed `disk_snapshot.sh` had 71% blindness — `.gemini` (138 GB), `.ao-sessions` (62 GB), `~/projects` (71 GB) were untracked or silently reporting 0 KB. Three compounding root causes (silent `du` timeouts, sparse-file overcounting, missing trackers) were fixed; ~14 GB reclaimed in the initial session and another ~50 GB in a follow-up on 2026-06-08. A new `snapshot_coverage_pct` field, `--discover` mode, 10 regression tests, and an AO session cleanup launchd job now prevent recurrence.

## Key Claims

- `disk_snapshot.sh` had 71% measurement blindness; numbers it reported were misleading for ~3 sessions (2026-05-12, 2026-05-21, 2026-05-23)
- Three root causes: (1) `du` timeouts silently returned 0 KB, (2) sparse files (`Docker.raw`) measured by `stat -f%z` reported apparent vs allocated size, (3) ~13 directories were not in `MONITORED_DIRS`
- Fixes landed: empty-string return on timeout → JSON `null`; `du -sk` for both files and dirs; per-entry timeouts (120–300s for slow paths); new `snapshot_coverage_pct` + `snapshot_warning: "low_coverage"`; new `timeout_keys` array; new `--discover` mode; 10 regression tests in `tests/test_disk_snapshot.py`
- Recurring bloat sources: antigravity worktrees (`~/.gemini/antigravity/worktrees/...`), `~/Library/Developer/Xcode/DerivedData` (21 GB, 100% safe to delete), `~/.ao-sessions/ao-<id>/.gemini/.../worktrees/` (79 sub-worktrees × ~1 GB)
- AO session bloat prevention: `com.jleechan.cleanup-ao-sessions.plist` (Approach 3, launchd cron at 4:23 AM) prunes ≥14-day-old session worktree venvs; agent self-cleanup rule added to `backup/Mac/gemini/GEMINI.md` (Approach 1); Approach 2 (uv hardlink venvs) not implemented
- APFS snapshot pinning gotcha: deleting 50 GB (`du`-measured) freed only ~20 GB on `df` because `com.apple.os.update-*` local snapshots (incl. `MSUPrepareUpdate`) pinned the rest; do not delete system-managed snapshots
- `disk_audit.sh --clean` is impractical for urgent cleanup — its analysis phase times out before reaching deletion; target known wins directly
- The skill `~/.claude/skills/disk-audit/SKILL.md` now has a snapshot-validation Phase 0

## Key Quotes

> "Before quoting `disk_snapshot.json` numbers, run Phase 0 of disk-audit skill (check `snapshot_coverage_pct`)."

> "`disk_audit.sh --clean` is impractical for 'I need space now' because its analysis phase (`du` over big home dirs) times out before reaching the deletion phase. For urgent cleanup, target the known wins directly (Xcode DerivedData, antigravity worktrees) rather than running the full script."

> "After a big cleanup, `df` free-gain < du-deleted is normal when APFS local snapshots exist — check `tmutil listlocalsnapshots /`."

## Connections

- [[DiskSnapshotBlindness]] — the structural defect class
- [[DiskCleanupCoverage]] — monitored paths need scheduled cleanup, manual policy, or explicit monitor-only ownership
- [[AOSessionBloat]] — `~/.ao-sessions/<id>/.gemini/.../worktrees/` recurring bloat
- [[AntigravityWorktrees]] — IDE-managed worktrees, dominant recurring bloat source
- [[XcodeDerivedDataBloat]] — 21 GB, safe to delete, regenerates
- [[APFSLocalSnapshotPinning]] — `com.apple.os.update-*` snapshots pin deleted bytes
- [[LaunchdCleanupAO]] — `com.jleechan.cleanup-ao-sessions.plist` auto-prune
- [[DiskAuditSkill]] — the skill that gained the Phase 0 snapshot-validation rule
- [[SparseFileDuAntiPattern]] — `stat -f%z` reports apparent size, not allocated
- [[SilentTimeoutZeroAntiPattern]] — `du` timeouts returning 0 looked identical to empty dirs
