---
name: .claude_reference commands + LLM-first export guards
description: Use git mv to .claude_reference/commands/ for archived duplicates; export commands must do LLM assessment + dry-run + confirmation before any writes
type: feedback
bead: rev-j5rvr
---

## Context

PR [#6998](https://github.com/jleechanorg/worldarchitect.ai/pull/6998) cleaned up 204 duplicate `.claude/commands/` files that were shadows of user-scope `~/.claude/commands/` entries. Initially deleted them outright, but user corrected: use `git mv` to `.claude_reference/commands/` instead (preserve for reference, out of active listing).

## Technical Detail

### git mv approach (not deletion)
```bash
# Restore deleted files from origin/main, then move to reference dir
git checkout origin/main -- <files>
git mv .claude/commands/<file> .claude_reference/commands/<file>
```
204 renames committed at SHA `89decc0024`. 18 project-exclusive commands stay in `.claude/commands/`.

### LLM-first export architecture
Both `/localexportcommands` and `/exportcommands` updated in `~/.claude/commands/`:

**Phase 0 (LLM gate — always runs first):**
- Count project commands, warn if >30
- Find name collisions with `~/.claude/commands/`, read both, build `SKIP_COMMANDS`
- Audit content filter coverage for leakage
- Count `.claude_reference/commands/` (maps to `~/.claude_reference/commands/`)
- Produce dry-run summary showing what would be exported/skipped

**Mandatory confirmation gate (always, no exceptions):**
> "Proceed with export? (yes/no)" — wait for explicit user confirmation before any writes

**Phase 1 (execution — only after confirmation):**
- `/localexportcommands`: rsyncs each component; reference commands → `~/.claude_reference/commands/`
- `/exportcommands`: runs `bash ~/.claude/commands/exportcommands.sh` → reports PR URL

### exportcommands.py changes
- `_export_commands()`: stages `.claude_reference/commands/` → `staging/reference_commands/`
- phase2 `dirs_mapping`: `"reference_commands"` → `repo/.claude_reference/commands/`

## Rule

**Never delete project-scope commands that might have reference value — `git mv` to `.claude_reference/commands/` instead.**

**Why:** Deletion is irreversible; reference dir preserves history while removing from active listing.

**How to apply:** Any future command pruning in `.claude/commands/` should use `git mv .claude/commands/<file> .claude_reference/commands/<file>` not `git rm`.

**Export commands must be LLM-first.** Phase 0 assessment + dry-run + explicit confirmation before any rsync/copy writes. This prevents clobbering user-scope commands that have more value than project versions.

## References

- PR: [#6998](https://github.com/jleechanorg/worldarchitect.ai/pull/6998)
- Bead: rev-j5rvr
- Commits: `89decc0024` (git mv), `7807afcae1` (restore es/header/4layer), `47217265` (original deletion)
- Files modified: `~/.claude/commands/localexportcommands.md`, `~/.claude/commands/exportcommands.md`, `~/.claude/commands/exportcommands.py`
