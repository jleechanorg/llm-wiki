---
title: "Beads Agent Instructions"
type: source
tags: [beads, bd, agent-instructions, cli, development-guidelines]
sources: []
source_file: AGENTS.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Comprehensive agent instructions for the Beads (bd) issue tracking system, covering issue tracking workflows, development guidelines, visual design standards for CLI output, and mandatory session completion procedures. Includes critical warnings about interactive commands and non-interactive shell patterns.

## Key Claims
- **Visual Design**: Unicode symbols with semantic colors (○ ◐ ● ✓ ❄) preferred over emoji-style icons (🔴🟠🟡🔵⚪) to reduce cognitive overload
- **Interactive Commands**: AI agents must use `bd update` with flags instead of `bd edit` which opens interactive editor
- **Testing Standards**: Use `make test` for default, `make test-full-cgo` for full CGO suite, never raw `CGO_ENABLED=1 go test ./...` on macOS without ICU flags
- **Session Completion**: Mandatory workflow includes file issues, run quality gates, update issue status, push to remote, clean up, verify, hand off

## Key Quotes
> "DO NOT use `bd edit` - it opens an interactive editor ($EDITOR) which AI agents cannot use."

> "Work is NOT complete until `git push` succeeds"

> "ALWAYS use non-interactive flags with file operations to avoid hanging on confirmation prompts"

## Connections
- [[Beads]] — the issue tracking system these instructions govern
- [[BD Guide for AI Agents]] — companion guide with MCP integration details

## Contradictions
- None identified

## Visual Design Anti-Patterns
**NEVER use emoji-style icons** (🔴🟠🟡🔵⚪) in CLI output. They cause cognitive overload.

**ALWAYS use small Unicode symbols** with semantic colors:
- Status: `○ ◐ ● ✓ ❄`
- Priority: `● P0` (filled circle with color)

## Non-Interactive Shell Patterns
```bash
# Force overwrite without prompting
cp -f source dest           # NOT: cp source dest
mv -f source dest           # NOT: mv source dest
rm -f file                  # NOT: rm file

# For recursive operations
rm -rf directory            # NOT: rm -r directory
```

## Landing the Plane Workflow
1. File issues for remaining work
2. Run quality gates (tests, linters, builds)
3. Update issue status
4. Pull rebase and push to remote
5. Clear stashes, prune remote branches
6. Verify all changes committed AND pushed
7. Provide context for next session
