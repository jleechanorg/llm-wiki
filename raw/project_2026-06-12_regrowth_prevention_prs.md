---
name: project-2026-06-12-regrowth-prevention-prs
description: disk_magician 4-PR regrowth-prevention series shipped to PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 0bddbf49-2e15-4207-aa4c-d67e7479703e
---

# 2026-06-12 Regrowth-Prevention PR Series (disk_magician)

**Context.** Disk was 95% full (47 GiB free) for the 6th time in 6 weeks. The
recurrence pattern: stale snapshot +3 days, no growth-rate detection, and
2 launchd sweepers (cleanup-docker, cleanup-antigravity-brain) loaded but
never logging. Reclaimed ~42 GB this session, then shipped 4 regrowth
guards to bound future regrowth.

**Deliverables (all on branch `regrowth-prevention-consolidated`,
PR https://github.com/jleechanorg/disk_magician/pull/4):**

- **Section A** — `scripts/post_job_docker_prune.sh` (225 lines, 17 tests).
  `docker system prune -f` always; `docker builder prune -f --filter
  "until=24h"` only when cache > 2048 MB. Fail-soft.
- **Section B** — `launchd/com.jleechan.disk-magician-worktree-venvs.plist`
  Sunday 04:00. Pinned `/opt/homebrew/bin/bash` (macOS `/bin/bash` 3.2.57
  crashes on `declare -A WT_AGE_CACHE` in `cleanup_worktree_venvs.sh`).
  `WORKTREE_APPROVED=1` baked into `EnvironmentVariables`.
- **Section C** — `disk_snapshot.sh` +134/-3, `disk_history.sh` +82/-1,
  `disk_audit.sh` +40/-3. `snapshot_metadata` block (captured_at,
  age_seconds, coverage_pct, measurement_status: complete|partial|timeout),
  `lc_<safe_name>` top-20 Library/Containers subdirs, `--growth-rate`
  linear regression KB/day. `disk_audit.sh` emits `STALE SNAPSHOT
  WARNING` when age > 14400s and refuses `measurement_status=timeout`.
- **Section D** — `scripts/sweeper_health_check.sh` (202 lines, 9 tests).
  Walks `~/Library/LaunchAgents/com.jleechan.cleanup-*.plist`, classifies
  log state as OK | WARN | MISS by `--threshold-days` (default 7). Live
  verified: detects the 2 known MISS sweepers.

**Installed and verified firing:**
- `~/Library/LaunchAgents/com.jleechan.disk-magician-sweeper-health.plist`
  (daily 09:00, `/bin/bash`, `/tmp/disk-magician-sweeper-health.log`)
- `~/Library/LaunchAgents/com.jleechan.disk-magician-worktree-venvs.plist`
  (Sunday 04:00, `/opt/homebrew/bin/bash`,
  `/tmp/disk-magician-worktree-venvs.log`)

**Test totals on the branch:** 9 (sweeper_health) + 17 (post_job_docker)
+ 16 (snapshot_freshness) = 42 passing assertions.

**Key gotchas (instructive):**
- pyproject.toml is TOML, not a pip install -r target. Original
  symlink-shared-venvs.sh v1 tried `pip install -r pyproject.toml` — fixed
  by v2 picking the LARGEST existing venv as canonical.
- Three different python sources on this host (uv 3.12.12, system 3.12,
  system 3.13). Mixed by accident would change behavior. Solved via
  pyvenv.cfg `home` field check.
- 6 worktree venvs in worldarchitect.ai symlinked to
  fix-level-up-combined/venv (canonical, 731M). Reclaimed 4.4 GB.
- Bash 3.2 vs 4+: launchd plists that need `declare -A` MUST pin
  `/opt/homebrew/bin/bash` (5.3.3 on this host). sweeper_health_check
  is bash 3.2 compatible (uses temp file instead of `mapfile`) so its
  plist can use `/bin/bash`.

**Why:** the disk-fill recurrence was unbounded — 47→88 GiB this session,
but no guards meant the next session would hit the same emergency. Each
of A/B/C/D sets a steady-state ceiling rather than a target.

**How to apply:** install in this order — D first (observe), A (highest
impact), B (prevents venv regrowth), C (gives the watchdog something
to alert on). README "Recommended rollout order" section is the
canonical reference.
