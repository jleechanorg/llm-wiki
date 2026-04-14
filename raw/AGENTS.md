# Global AGENTS Policy

This repository defines **home-level default guardrails** for agent behavior.

## Rules and config locations in `~`

| Purpose | Path |
|--------|------|
| **Claude Code rules (user-level)** | `~/.claude/CLAUDE.md` |
| **Claude Code agents** | `~/.claude/agents/` |
| **Claude Code MCP servers** | `~/.claude.json` (NOT `~/.claude/settings.json`) |
| **Cursor MCP servers** | `~/.cursor/mcp.json` |
| **Cursor user rules** | Cursor Settings → General → Rules for AI (not a file) |
| **Codex MCP servers** | `~/.codex/config.toml` |

## Force-push safety (non-negotiable)

- Never run `git push --force` or `git push --force-with-lease` unless the human gives explicit in-thread approval and names the target branch.
- Ask first, exactly:
  - "I need to force-push `<local_ref>` to `<remote>/<branch>` because `<reason>`. Approve force-push?"
- If approved, restate exact command before running.
- Safest form:
  - `git push --force-with-lease=<remote>/<branch>:<expected_old_sha> <remote> <local_ref>:<branch>`
- After force-push, report old SHA -> new SHA.
- If approval is missing/ambiguous: do not force-push. Propose merge/revert/follow-up/new-branch PR.

## Branch-target safety checks (before any push)

Print and verify:
- current branch: `git branch --show-current`
- upstream: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`
- target: explicit `<local_ref>:<remote_branch>`

If current branch and intended target differ unexpectedly, stop and ask.

## Audit logging requirement

For every push, log/report:
- command run
- whether force was used
- old SHA and new SHA
- confirmation that explicit force approval was present (if force)

<!-- BEGIN BEADS INTEGRATION -->
## Issue Tracking with br (beads)

**IMPORTANT**: This project uses **br (beads_rust)** for ALL issue tracking. Do NOT use markdown TODOs, task lists, or other tracking methods.

### Why br?

- Dependency-aware: Track blockers and relationships between issues
- Git-friendly: Auto-syncs to JSONL for version control
- Agent-optimized: JSON output, ready work detection, discovered-from links
- Prevents duplicate tracking systems and confusion

### Quick Start

**Check for ready work:**

```bash
br ready
```

**Create new issues:**

```bash
br create "Issue title" --description "Detailed context" --type task --priority 1
br create "Child task" --parent epic-id --estimate 60
```

**Claim and update:**

```bash
br update issue-id --status in_progress
br update issue-id --priority 1
```

**Complete work:**

```bash
br close issue-id
```

### Issue Types

- `bug` - Something broken
- `feature` - New functionality
- `task` - Work item (tests, docs, refactoring)
- `epic` - Large feature with subtasks
- `chore` - Maintenance (dependencies, tooling)

### Priorities

- `0` - Critical (security, data loss, broken builds)
- `1` - High (major features, important bugs)
- `2` - Medium (default, nice-to-have)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

### Workflow for AI Agents

1. **Check ready work**: `br ready` shows unblocked issues
2. **Claim your task**: `br update <id> --status in_progress`
3. **Work on it**: Implement, test, document
4. **Discover new work?** Create linked issue:
   - `br create "Found bug" --description "Details" --priority 1` then `br dep add new-id parent-id --type discovered-from`
5. **Complete**: `br close <id>`

### Dependencies

```bash
# Add dependency (issue-a blocks on issue-b)
br dep add issue-a issue-b --type blocks

# Dependency types: blocks, parent-child, related, discovered-from
```

### Auto-Sync

br automatically syncs with git:

- Exports to `.beads/issues.jsonl` after changes
- Imports from JSONL when newer (e.g., after `git pull`)
- No manual export/import needed!

### Important Rules

- ✅ Use br for ALL task tracking
- ✅ Use `br ready` to find unblocked work
- ✅ Link discovered work with dependencies
- ✅ Check `br ready` before asking "what should I work on?"
- ❌ Do NOT create markdown TODO lists
- ❌ Do NOT use external issue trackers
- ❌ Do NOT duplicate tracking systems

For more details, see README.md and docs/QUICKSTART.md.

<!-- END BEADS INTEGRATION -->

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
