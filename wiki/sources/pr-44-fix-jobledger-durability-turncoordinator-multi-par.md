---
title: "PR #44: fix: JobLedger durability + TurnCoordinator multi-party isolation"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-44.md
sources: []
last_updated: 2026-03-05
---

## Summary
- **getTurnCoordinator**: Replaced module-level singleton with `Map<string, TurnCoordinator>` keyed by `partyId`. Each party now gets its own coordinator instance, preventing stale singleton bugs when multiple parties exist in one process.
- **JobLedger**: `getJobLedger(db)` now actually uses the `better-sqlite3` Database argument. Jobs are persisted to a new `job_proofs` table in SQLite, so the leaderboard survives server restarts. Falls back to in-memory when no DB is provided (backward compat

## Metadata
- **PR**: #44
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +318/-16 in 5 files
- **Labels**: none

## Connections
