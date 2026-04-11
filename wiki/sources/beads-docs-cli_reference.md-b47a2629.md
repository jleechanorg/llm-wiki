---
title: "Beads CLI Command Reference"
type: source
tags: [beads, cli, command-reference, issue-tracking, atomic-operations]
sources: [beads-docs-architecture.md-6181aac9.md]
source_file: docs/cli-reference.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Comprehensive command reference for the beads (bd) CLI tool version 0.21.0+, covering issue management, dependencies, labels, state management, and filtering operations. The CLI supports atomic operations for parallel worker scenarios and integrates with the three-layer architecture (CLI → SQLite → JSONL → Git).

## Key Claims

- **Atomic Claiming**: `bd update <id> --claim` atomically claims issues preventing race conditions in parallel worker setups
- **Hierarchical Epics**: Support for parent-child issue relationships with auto-generated IDs (e.g., `bd-a3f8e9.1`)
- **State as Labels**: Operational state tracked via `<dimension>:<value>` label convention for runtime behavior
- **External References**: Support for GitHub issues, Jira tickets via `--external-ref` flag (v0.9.2+)
- **Stdin Input**: Can read issue descriptions from stdin or files to avoid shell escaping issues

## Key Commands

### Basic Operations
- `bd info --json` — Check database path, daemon status, agent_mail_enabled
- `bd ready --json` — Find ready work (no blockers, not claimed)
- `bd stale --days 30` — Find stale issues

### Issue Management
- `bd create "Title" -t bug|feature|task -p 0-4 -d "Description"` — Create issues
- `bd update <id> --status in_progress --claim --priority 1` — Update issues
- `bd close <id> --reason "Done"` — Complete work
- `bd reopen <id> --reason "Reopening"` — Reopen issues

### Dependencies & Labels
- `bd dep add <child> <parent> --type discovered-from` — Link dependencies
- `bd create "Title" --deps discovered-from:<parent-id>` — Create and link
- `bd label add/remove <id> <label>` — Manage labels
- `bd state <id> <dimension>` — Query state value
- `bd set-state <id> <dimension>=<value>` — Set state atomically

## Connections
- [[beads-docs-architecture.md-6181aac9]] — CLI is the top layer of the three-layer architecture
- [[beads-docs-claude_integration.md-1208507f]] — CLI + Hooks integration pattern

## Contradictions
- None identified — this is a reference document, not argumentative content
