---
title: "disk_magician"
type: entity
tags: [project, macos, disk-management, tooling]
sources: [snapshot-launchd-plist-corruption-and-history-diff-gate]
last_updated: 2026-09-05
---

## Description
`disk_magician` (repo `jleechanorg/disk_magician`, local checkout
`~/projects_other/disk_magician`) is Jeffrey's portable disk diagnostics,
snapshot-backup, and cleanup tool for macOS (and a Linux/cron fallback).
Deployed both as a uv tool (`disk-magician` on PATH, built from
`src/disk_magician/`) and via direct repo-root script invocation for
different launchd jobs — "commit is NOT deploy": root script changes require
`scripts/sync_package_tree.sh` + a `pyproject.toml` version bump + `uv tool
install --force --reinstall` before they take effect in the packaged copy.

Maintains a git-backed disk-usage ledger at `~/.disk_magician_backup` (one
commit per snapshot, `ledger/topdown-5g.json`) that `disk-magician history
diff --days N` uses to answer "current usage vs the lowest-used ('floor')
snapshot in the last N days" — but only over snapshots that pass a strict
schema_version-2 + full-attribution validator (see
[[Launchd]] for the 2026-09-05 incident where this correctly returned "no
valid snapshots" during a real collection outage).

## Connections
- [[Launchd]] — its snapshot collection job is a launchd agent
  (`com.jleechanorg.disk-magician.plist`, every 30 min)
- [snapshot-launchd-plist-corruption-and-history-diff-gate](../sources/snapshot-launchd-plist-corruption-and-history-diff-gate.md) — 2026-09-05 incident
