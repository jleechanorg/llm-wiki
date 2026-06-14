---
title: "Regrowth-Prevention PR Series (disk_magician)"
type: source
tags: [disk-magician, regrowth-prevention, launchd, sweeper, snapshot-freshness, post-job-docker-prune]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-other-user-scope/memory/project_2026-06-12_regrowth_prevention_prs.md
---

## Summary
4-PR regrowth-prevention series shipped to `regrowth-prevention-consolidated` branch (PR #4) after disk hit 95% full for the 6th time in 6 weeks. Reclaimed ~42 GB this session and shipped 4 guards (A: post-job Docker prune, B: launchd worktree venv sweeper, C: snapshot freshness + growth-rate, D: sweeper health check) to bound future regrowth.

## Key Claims
- Reclaimed ~42 GB; 4 launchd sweepers (cleanup-docker, cleanup-antigravity-brain) were loaded but never logging — root cause of repeated 95% full.
- Section A (`post_job_docker_prune.sh`, 225 lines, 17 tests) fail-soft: `docker system prune -f` always, builder prune only when cache > 2048 MB.
- Section B `disk-magician-worktree-venvs.plist` Sunday 04:00, MUST pin `/opt/homebrew/bin/bash` (macOS `/bin/bash` 3.2.57 crashes on `declare -A WT_AGE_CACHE`).
- Section C `disk_snapshot.sh` +134/-3, `disk_history.sh` +82/-1, `disk_audit.sh` +40/-3: `snapshot_metadata` block (captured_at, age_seconds, coverage_pct, measurement_status), `lc_<safe_name>` top-20 Library/Containers subdirs, `--growth-rate` linear regression KB/day. Stale-snapshot warning at >14400s, refuses `measurement_status=timeout`.
- Section D `sweeper_health_check.sh` (202 lines, 9 tests) walks `~/Library/LaunchAgents/com.jleechan.cleanup-*.plist`, classifies log state OK | WARN | MISS by `--threshold-days`. Live verified: detects 2 known MISS sweepers.
- 42 passing assertions across the 3 test files.
- 3 different python sources on this host (uv 3.12.12, system 3.12, system 3.13) — solved via pyvenv.cfg `home` field check.
- 6 worktree venvs in worldarchitect.ai symlinked to fix-level-up-combined/venv (canonical, 731M). Reclaimed 4.4 GB.
- Install order: D (observe) → A (highest impact) → B (prevents venv regrowth) → C (gives the watchdog something to alert on).

## Key Quotes
> "pyproject.toml is TOML, not a pip install -r target. Original symlink-shared-venvs.sh v1 tried `pip install -r pyproject.toml` — fixed by v2 picking the LARGEST existing venv as canonical."

> "Bash 3.2 vs 4+: launchd plists that need `declare -A` MUST pin `/opt/homebrew/bin/bash` (5.3.3 on this host). sweeper_health_check is bash 3.2 compatible (uses temp file instead of `mapfile`) so its plist can use `/bin/bash`."

## Connections
- [[LaunchdMacOS]] — launchd plist installation standards
- [[WorktreeWorkflow]] — worktree venv canonicalization
- [[BeadFollowupTemplates]] — bead tracking for regrowth prevention
- [[DiskSpaceRegression]] — disk fill recurrence pattern
