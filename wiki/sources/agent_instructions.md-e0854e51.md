---
title: "Detailed Agent Instructions for Beads Development"
type: source
tags: [beads, development, guidelines, go, testing, git, dolt]
sources: []
source_file: agent_instructions.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Comprehensive operational instructions for AI agents working on beads (a Dolt-backed issue tracker) development, testing, and releases. Covers Go 1.24+ code standards, file organization, testing workflows with isolated databases, git hooks for JSONL sync, and the mandatory "landing the plane" push procedure.

## Key Claims

- **Go Version**: Requires 1.24+ with golangci-lint for linting
- **Test Isolation**: Never pollute production database — use `BEADS_DB` env var or `t.TempDir()` for isolated testing
- **Database**: Uses Dolt as primary database with SQLite legacy support
- **Git Hooks**: `bd hooks install` enables automatic JSONL export on commit for git portability
- **Landing the Plane**: Mandatory workflow requiring ALL steps including `git push` — never stop before push completes
- **Issue Convention**: Include issue ID in commit messages `(bd-abc)` for orphan detection

## Key Quotes

> "NEVER stop before `git push` - that leaves work stranded locally"

> "The plane has NOT landed until `git push` completes successfully"

> "WARNING: bd will warn you when creating issues with 'Test' prefix in the production database"

## Connections

- [[DoltDatabase]] — primary database backend
- [[GoDevelopment]] — language and tooling
- [[GitHooks]] — automation for JSONL sync
- [[TestingIsolation]] — test database management patterns

## Contradictions

- None currently documented in wiki

## Development Workflow

### Testing Commands
```bash
# Manual testing with isolated database
BEADS_DB=/tmp/test.db ./bd init --quiet --prefix test
BEADS_DB=/tmp/test.db ./bd create "Test issue" -p 1

# Automated tests use t.TempDir()
func TestMyFeature(t *testing.T) {
    tmpDir := t.TempDir()
    testDB := filepath.Join(tmpDir, ".beads", "beads.db")
    s := newTestStore(t, testDB)
}
```

### Quality Gates (Required Before Push)
1. `make lint` or `golangci-lint run ./...`
2. `make test` (full CGO: `make test-full-cgo`)
3. File P0 issues if gates fail
