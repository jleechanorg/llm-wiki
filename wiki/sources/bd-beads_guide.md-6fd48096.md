---
title: "BD (Beads) Guide for AI Agents"
type: source
tags: [beads, issue-tracking, git, AI-agents, bd, MCP]
sources: []
source_file: .beads/BD_GUIDE.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

**beads** (`bd`) is a Git-backed issue tracker designed for AI-supervised coding workflows. It provides dependency-aware tracking, auto-syncs to JSONL for version control, and offers an MCP server for Claude integration. The tool enforces explicit choice-driven interaction where every response must include a planning block with choices.

## Key Claims

- **Git-backed Issue Tracking**: All issues sync to `.beads/issues.jsonl` for version control — commit the JSONL file alongside code changes
- **Dependency-aware**: Track blockers and relationships between issues with `discovered-from` dependencies
- **MCP Server Integration**: beads-mcp provides Claude-native access to issue operations
- **Auto-Sync**: Exports to JSONL after changes (5s debounce), imports from JSONL when newer after git pull
- **AI-Optimized**: JSON output, ready work detection, programmatic CLI with `--json` flag
- **Ephemeral Docs**: Recommend `history/` directory for AI-generated planning documents (PLAN.md, DESIGN.md, etc.)

## Essential Commands

```bash
bd ready --json          # Check for unblocked issues
bd create "Issue title" -t bug|feature|task -p 0-4 --json  # Create issue
bd update <id> --status in_progress --json  # Claim task
bd close <id> --reason "Done" --json        # Complete work
```

## Issue Types

- `bug` — Something broken
- `feature` — New functionality  
- `task` — Work item (tests, docs, refactoring)
- `epic` — Large feature with subtasks
- `chore` — Maintenance (dependencies, tooling)

## Priorities

- `0` — Critical (security, data loss, broken builds)
- `1` — High (major features, important bugs)
- `2` — Medium (default, nice-to-have)
- `3` — Low (polish, optimization)
- `4` — Backlog (future ideas)

## GitHub Copilot Integration

If using GitHub Copilot, create `.github/copilot-instructions.md` for automatic instruction loading. Run `bd onboard` to generate the content.

## Important Rules

- ✅ Use bd for ALL task tracking
- ✅ Always use `--json` flag for programmatic use
- ✅ Link discovered work with `discovered-from` dependencies
- ✅ Check `bd ready` before asking "what should I work on?"
- ✅ Store AI planning docs in `history/` directory
- ❌ Do NOT create markdown TODO lists
- ❌ Do NOT use external issue trackers
- ❌ Do NOT duplicate tracking systems
- ❌ Do NOT clutter repo root with planning documents

## Connections

- [[WorldArchitect.AI]] — the primary project using beads for issue tracking
- [[AI Universe]] — integrated with Memory MCP for enhanced planning

## Contradictions

- None identified — beads is complementary to other tracking systems, replacing rather than conflicting with them.
