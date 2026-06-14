---
title: "disk-magician"
type: entity
tags: [project, repo, disk-cleanup, monitoring]
date: 2026-06-13
last_updated: 2026-06-13
---

# disk-magician

A small repo for disk-space auditing, growth-regression detection, and safe
cleanup of developer machines. The CLI (`disk_magician.sh`) wraps a
`disk_snapshot.sh` writer and a `disk_audit.sh` reader, both driven by a
JSON config (`config.json` or `config.json.template`).

## Repo
- URL: `https://github.com/jleechanorg/disk_magician`
- Owner: `jleechanorg` (default org per `~/.claude/CLAUDE.md`)
- Two copies of every script must stay in sync:
  - `scripts/disk_snapshot.sh` — canonical
  - `src/disk_magician/scripts/disk_snapshot.sh` — package copy installed
    by `pip install -e .`

## Subcommands
- `audit` — read latest snapshot, list cleanup candidates and regressions
- `clean` — safe cache/temp cleanup (pr clones, dev caches, orphaned worktrees)
- `clean-all` — destructive cleanup with interactive confirm
- `discover` — scan `~/$HOME` for >5GB dirs not in monitored config
- `snapshot` — write a JSON snapshot of measured path sizes
- `alert` — emit alerts when a regrowth threshold is crossed
- `history` — read past snapshots from `backup/<host>/disk_snapshot.json`

## Config schema (`config.json.template`)
- `monitored_dirs` — explicit directory paths with per-key timeout
- `monitored_file_globs` — file patterns measured by `glob_size_kb`
- `monitored_globs` — directory patterns (e.g. `~/actions-runner*`)
- `cleanup_thresholds` — age/usage thresholds for `clean` candidates

## See also
- [[DiskMagicianDiscover]] — the subcommand with the documented latent bugs
- [[RegrowthPrevention]] — the broader workflow that depends on accurate snapshots
- [[feedback-2026-06-13-disk-snapshot-discover-bugs]] — the bug-fix memory
