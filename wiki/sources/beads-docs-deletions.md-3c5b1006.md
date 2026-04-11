---
title: "Deletion Tracking"
type: source
tags: [bd, beads, tombstones, sync, deletion-propagation, git-sync]
sources: []
date: 2026-04-07
source_file: docs/deletion-tracking.md
last_updated: 2026-04-07
---

## Summary
Describes how bd tracks and propagates deletions across repository clones using inline tombstones. Deleted issues are converted to special tombstone status entries in `issues.jsonl`, providing audit trail, atomic sync, TTL-based expiration, and proper 3-way merge conflict resolution.

## Key Claims
- **Inline Tombstones**: Deleted issues stay in `issues.jsonl` with status `"tombstone"` rather than being removed — enables atomic sync and audit trail
- **Audit Trail**: Tombstones preserve deletion metadata (`deleted_at`, `deleted_by`, `delete_reason`, `original_type`)
- **TTL Expiration**: Default 30-day TTL prevents unbounded growth; 1-hour grace period handles clock skew
- **Conflict Resolution**: Fresh tombstones win over live issues; expired tombstones allow resurrection
- **Migration**: Prior format used separate `deletions.jsonl` manifest; migrate with `bd migrate tombstones`

## Key Quotes
> "Beads uses inline tombstones — deleted issues are converted to a special `tombstone` status and remain in `issues.jsonl`."

> "This provides: Full audit trail (who, when, why), Atomic sync with issue data (no separate manifest to merge), TTL-based expiration (default 30 days), Proper 3-way merge conflict resolution"

## Connections
- [[Daemon Management Guide]] — tombstone sync happens via daemon auto-sync mechanism
- [[Beads Configuration System]] — tombstone TTL is configurable via `tombstone.ttl_days`

## Tombstone Commands
- `bd delete bd-42 --force` — delete single issue
- `bd list --status=tombstone` — list all tombstones
- `bd admin compact` — prune expired tombstones
- `bd migrate tombstones` — migrate from legacy format

## Contradictions
- None identified with existing wiki content
