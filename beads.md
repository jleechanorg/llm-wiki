---
name: beads
type: project
provenance:
  source: /Users/jleechan/projects_other/beads
  ingested: 2026-04-07
  last_seen: 2026-04-07
---

# Beads Issue Tracker

Go-based issue tracking system (bd). Lightweight, fast issue tracker with SQLite backend.

## Purpose

Provides Git-native issue tracking with branch linkage, similar to GitHub Issues but local-first.

## Key Files

- `cmd/bd/main.go` - CLI entry point
- `internal/db/` - SQLite operations
- `internal/github/` - GitHub integration

## How to Use

```bash
cd /Users/jleechan/projects_other/beads
go build ./cmd/bd
./bd init
./bd issue create -t "Bug fix"
```

## Related

- [code-projects](code-projects.md) - Full project catalog
- [index](index.md) - Wiki index