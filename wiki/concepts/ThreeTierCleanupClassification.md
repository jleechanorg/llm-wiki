# Three-Tier Cleanup Classification

A pattern for classifying and cleaning up disk paths that fall outside the standard `/diskm` auto-clean paths (cleanup_dev_caches, cleanup_tmp, cleanup_worktrees, cleanup_llm_inspector, cleanup_agent_artifacts).

## Tiers

### Tier A — Always safe to automate (no user approval)

- **Examples**: launchd-style rotated logs (e.g., `cmux-codex-launchd.YYYYMMDDTHHMMSS.log`), package manager caches older than threshold
- **Safety rule**: explicit never-touch list for active files (active log + stderr + state file)
- **Cleanup shape**: small dedicated script that pattern-matches timestamped rotations only, defaults to dry-run, `--clean` applies
- **Wire-in**: add to `scripts/disk_audit.sh` between existing cleanups so `./disk_magician.sh clean` runs it on every pass
- **New floor**: keep retention to ~7 × cap = bounded growth

### Tier B — `~/.ao-sessions/wa-*` and similar agent session dirs (requires `WORKTREE APPROVED` if < 14d)

- **Examples**: `wa-2327` per-worker colima bootstrap artifact, 172M-2.7G wa-* dirs
- **Safety filter applied before delete**:
  1. Skip orchestrator (e.g., `wa-orchestrator`) — must preserve
  2. Skip < 100M (fresh workers, just-completed)
  3. Skip < 30m old (in-flight)
  4. Rest: `rm -rf`
- **Never-delete list override**: `~/.ao-sessions` is NOT in the disk_magician never-delete list. Only `~/.codex/sessions`, `~/.codex/sessions_archive/`, `~/.codex/state*.sqlite`, `~/.codex/log`, `~/.claude/projects` are off-limits.

### Tier C — `/private/tmp/wt-*` and `/private/tmp/wa-*` scratch worktrees (lower risk than B)

- **Examples**: `wt-7278-rebase`, `wa-pr-truly-raw`, `wa-skeptic-gate8-fix` — 264-277 MB each
- **Why existing cleanups miss them**:
  - `cleanup_tmp.sh` requires `.git` directory (these have `.git` file pointing to parent's worktree, not a directory)
  - `cleanup_worktrees.sh` only walks `~/.gemini/antigravity/worktrees/`
- **Safety filter**:
  1. Skip < 100M (small briefs/notes may be in-flight evidence)
  2. Skip < 30m old (in-flight agent work)
  3. Rest: `rm -rf`

## Decision flow

For any disk-growth path that `/diskm` doesn't auto-clean:

1. **Is it in the never-delete list?** → NEVER touch.
2. **Is it > 14 days old?** → auto-clean OK via existing paths; the 14d rule is the only hard constraint.
3. **< 14 days, not in the never-delete list** → classify:
   - Launchd-style rotated logs → Tier A pattern (always safe to automate, new script)
   - Agent session dirs (`wa-*` / `wt-*`) → Tier B or C pattern (needs explicit user approval + safety filter)

## 2026-06-14 example

Reclaimed 15.5 GB in one `/diskm` rerun:

- Tier A: 1.7 GB (39 × 50 MB supervisor launchd log rotations, 19 days of accumulation). New `scripts/cleanup_supervisor_logs.sh` wired into `disk_audit.sh`. New floor: ~7 × 50 MB = 350 MB.
- Tier B: 9.8 GB (29 wa-* sessions, including the 2.7 GB wa-2327/.colima bootstrap artifact). User approved with `WORKTREE APPROVED`.
- Tier C: 4.0 GB (15 /private/tmp scratch worktrees, 264-277 MB each). User approved with `WORKTREE APPROVED`.

Disk: 133 Gi → 147 Gi free.

## References

- Source: `sources/feedback-2026-06-14-disk-cleanup-three-tier.md`
- Memory: `~/.claude/projects/-Users-jleechan-projects-other-disk-magician/memory/feedback_2026-06-14_disk_cleanup_three_tier.md`
- Sibling concept: `DiskCleanupCoverage` (the "monitoring vs cleanup coverage" question)
- Implementation: `scripts/cleanup_supervisor_logs.sh`, `scripts/disk_audit.sh` line 263-266
- Repo: jleechanorg/disk_magician, commit `5b3e3a6` on `dev1781402943`
